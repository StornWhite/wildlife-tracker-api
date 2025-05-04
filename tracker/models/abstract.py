from django.contrib.gis.db import models


class AbstractTrackerModel(models.Model):
    """
    Base class for all models in the tracker application.
    """

    class Meta:
        abstract = True

    tracker_id = models.UUIDField(
        help_text="UUID primary key",
        primary_key=True
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


class AbstractFamilyLocationTrackerModel(AbstractTrackerModel):
    """
    Relates models to families and adds location and timestamp fields.
    """

    class Meta:
        abstract = True
        required_db_features = ["gis_enabled"]

    family = models.ForeignKey(
        help_text="Related family",
        to="Family",
        on_delete=models.CASCADE,
    )
    location = models.PointField(
        help_text="Lat/long location",
        srid=4326,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
