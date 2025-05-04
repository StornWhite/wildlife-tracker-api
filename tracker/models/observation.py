from django.db import models

from . import AbstractFamilyLocationTrackerModel


class Observation(AbstractFamilyLocationTrackerModel):
    """
    A data observation recorded for a family.
    """
    size = models.PositiveSmallIntegerField(
        help_text="Count of family members"
    )
    health_rating = models.PositiveSmallIntegerField(
        help_text="Health rating (1-10)"
        # Todo: storn add validator
    )
