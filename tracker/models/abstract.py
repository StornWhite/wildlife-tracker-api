from django.contrib.gis.db import models

from uuid import uuid4


class AbstractTrackerModel(models.Model):
    """
    Base class for all models in the tracker application.
    """

    class Meta:
        abstract = True

    tracker_id = models.UUIDField(
        help_text="UUID primary key",
        primary_key=True,
        default=uuid4
    )
    name = models.CharField(
        help_text="Friendly name",
        max_length=100
    )


class AbstractNamedTrackerModel(AbstractTrackerModel):
    """
    Adds a name field to the tracker application base class.
    """

    class Meta:
        abstract = True

    name = models.CharField(
        help_text="Friendly name",
        max_length=100
    )


class AbstractLocationTrackerModel(AbstractTrackerModel):
    """
    Relates models to families and adds location and timestamp fields.
    """

    class Meta:
        abstract = True
        required_db_features = ["gis_enabled"]

    location = models.PointField(
        help_text="Lat/long location",
        srid=4326,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
