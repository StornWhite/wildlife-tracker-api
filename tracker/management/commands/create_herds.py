import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.gis.geos import GEOSGeometry, Point as DjangoPoint

import us
import geopandas as gpd
from shapely import Polygon, MultiPolygon, Point
from shapely.ops import transform
from pyproj import Transformer, CRS

from tracker.models import (
    Herd,
    Family,
    Observation,
)
from tracker.data.species import SPECIES_CHOICES, SPECIES_DATA


SPECIES = SPECIES_CHOICES.keys()
STATES = [state.abbr.lower() for state in us.STATES]
PATH_TO_STATE_SHAPES = 'tracker/data/gis_data/cb_2022_us_state_500k.zip'


class Command(BaseCommand):
    help = "Generate new loads.txt file for Galveston"

    def add_arguments(self, parser):
        parser.add_argument(
            "--species",
            choices=SPECIES,
            default="deer",
            help=(
                f"Choices for heard_type are {SPECIES}"
            )
        )
        parser.add_argument(
            "--num_herds",
            default=10,
            help=(
                "Specify the number of herds that will be created."
            )
        )
        parser.add_argument(
            "--state",
            choices=STATES,
            default="vt",
            help=(
                "Specify the state where the herds will appear e.g. vt"
            )
        )

    def handle(self, *args, **options) -> None:

        herd_generator = HerdGenerator(
            species=options["species"],
            num_herds=options["num_herds"],
            state=options["state"]
        )
        herd_generator.create_herds()
        herd_generator.create_observations()


class HerdGenerator:
    """
    A class for randomly generating herds of a species at points within
    a state, plus their associated families along with family observations
    and events.
    """

    def __init__(
        self,
        species: str,
        num_herds: int,
        state: str,
    ):
        self.species = species
        self.species_data = SPECIES_DATA[species]
        self.num_herds = int(num_herds)
        self.state = us.states.lookup(state)
        self.family_data = dict()
        self.observations_created = 0
        self.events_created = 0
        self.herd_location = None
        self.num_herd_observations = 0
        self.start_date = date.today()
        self.herd_ids = list()

    def create_herds(self):
        """
        Call this first to create all the herds and their related families.
        """

        with transaction.atomic():
            for i in range(0, self.num_herds):

                herd = Herd(
                    name=f"{self.species} {i}",    # eg moose 6
                    species=self.species
                )
                herd.save()
                self.herd_ids.append(herd.pk)

                self.create_families(herd)

        return

    def create_families(self, herd: Herd):

        family_count = random.randint(
            1, (2 * self.species_data["ave_families_per_herd"])
        )
        for i in range(1, family_count):

            family = Family(
                herd=herd,
                name=(herd.name + f".{i}")      # eg moose 6.3
            )
            family.save()
            family_size = random.randint(
                1, (2 * self.species_data["ave_family_size"])
            )
            family_health = random.randint(1, 10)
            self.family_data[family.pk] = {
                "size": family_size,
                "health": family_health
            }

        return

    def create_observations(self) -> None:
        """
        Call this second to create observations for all of the herds.
        """

        herds = Herd.objects.filter(pk__in=self.herd_ids)
        for herd in herds:
            self.create_herd_observations(herd)

    def create_herd_observations(self, herd: Herd):
        """
        A Herd will start at a random point in the state.  It will be observed
        several times during the year and it will move between each
        observation to a random place within it's maximum range.  The families
        in the herd are randomly placed within the extent of the herd.
        Families can grow or shrink depending on herd health and we record
        these events.
        """

        self.herd_location = self.get_point_in_state()
        self.num_herd_observations = random.randint(5, 15)
        days_between_observations = (365 // self.num_herd_observations)

        for i in range(0, self.num_herd_observations):

            time_between_observations = timedelta(
                days=random.randint(1, 2 * days_between_observations)
            )
            timestamp = (
                    self.start_date
                    + time_between_observations
                    + self.get_random_timedelta()
            )
            self.move_herd(self.herd_location, days_between_observations)

            for family in Family.objects.filter(herd=herd):

                family_data = self.family_data[family.pk]
                health_change = random.randint(-2, 2)
                family_data["health"] += health_change
                family_data["health"] = max(1, min(family_data["health"], 10))

                size_change = self.get_family_size_change(
                    family_data["health"]
                )
                family_data["size"] += size_change
                family_data["size"] = max(family_data["size"], 0)

                event_type, description = self.get_event_type(size_change)
                location = self.get_family_location(herd)

                obs = Observation(
                    family=family,
                    location=GEOSGeometry(location.wkt),
                    timestamp=timestamp,
                    family_size=family_data["size"],
                    health_rating=family_data["health"],
                    event_type=event_type,
                    description=description
                )
                obs.save()
                self.family_data[family.pk] = family_data

        return

    def get_point_in_state(self):
        """
        Returns a random point inside the state boundary.
        """

        boundary = self.get_state_boundary(self.state)
        return self.get_random_point_in_polygon(boundary)

    @staticmethod
    def get_state_boundary(
        state: us.states.State
    ) -> Polygon | MultiPolygon:

        gdf = gpd.read_file(PATH_TO_STATE_SHAPES)
        return gdf.loc[gdf['STUSPS'] == state.abbr].iloc[0]['geometry']

    @staticmethod
    def get_random_point_in_polygon(
        polygon: Polygon | MultiPolygon,
        max_tries: int = 1000,
    ) -> Point:

        min_x, min_y, max_x, max_y = polygon.bounds

        for _ in range(max_tries):
            p = Point(
                random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            )
            if polygon.contains(p):
                return p

        raise RuntimeError(f"failed to find point inside polygon!")

    @staticmethod
    def get_random_timedelta():

        seconds = random.randint(0, 86400)      # seconds in a day
        return timedelta(seconds=seconds)

    @staticmethod
    def get_family_size_change(family_health: int) -> int:
        """
        In this model, changes in family size depends on the family's health.
        """

        if family_health <= 2:
            family_size_change = -2
        elif family_health <= 3:
            family_size_change = -1
        elif family_health >= 8:
            family_size_change = 2
        elif family_health >= 6:
            family_size_change = 1
        else:
            family_size_change = 0

        random_death = random.randint(0, 1)

        return family_size_change + random_death

    @staticmethod
    def get_event_type(family_size_change: int) -> (str, str):
        """
        Event type depends on the change in family size.
        """

        if family_size_change > 0:
            event_type = ["birth", "join"][random.randint(0, 1)]
            if event_type == "birth":
                description = "We welcome a birth!"
            else:
                description = "New members have joined!"
        if family_size_change < 0:
            event_type = ["death", "depart"][random.randint(0, 1)]
            if event_type == "death":
                description = "Tears are the silent language of grief."
            else:
                description = "Buh-bye!"
        else:
            event_type = "obsv"
            description = ""

        return event_type, description

    def get_family_location(self, herd: Herd):
        """
        The family will be within a radius of the herd.
        """
        herd_circle = self.create_circle_in_miles(
            self.herd_location,
            self.species_data["spread"]
        )
        return self.get_random_point_in_polygon(herd_circle)

    def move_herd(self, herd_location: Point, days: int) -> None:
        """
        The herd will be within a radius of max straight line travel.
        """
        max_range = self.create_circle_in_miles(
            herd_location,
            self.species_data["speed"] * days
        )
        self.herd_location = self.get_random_point_in_polygon(max_range)

    @staticmethod
    def create_circle_in_miles(location: Point, radius_miles: float):

        # Convert miles to meters
        radius_meters = radius_miles * 1609.34

        # Define coordinate systems
        wgs84 = CRS("EPSG:4326")  # Lat/lon
        utm = CRS(
            proj='utm',
            zone=33,
            ellps='WGS84',
            south=location.y < 0
        )

        # Transformer from WGS84 to UTM
        project_to_utm = Transformer.from_crs(
            wgs84,
            utm,
            always_xy=True
        ).transform
        project_to_wgs84 = Transformer.from_crs(
            utm,
            wgs84,
            always_xy=True
        ).transform

        # Create point and buffer in UTM
        center_utm = transform(project_to_utm, location)
        circle_utm = center_utm.buffer(radius_meters)

        # Project back to WGS84
        circle_wgs84 = transform(project_to_wgs84, circle_utm)

        return circle_wgs84
