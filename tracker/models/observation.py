from django.db import models

from . import AbstractFamilyLocationTrackerModel


EVENT_TYPE_CHOICES = {
    'birth': 'birth',
    'death': 'death',
    'depart': 'departing members',
    'join': 'joining members',
    'obsv': 'observation'
}


class Observation(AbstractFamilyLocationTrackerModel):
    """
    A data observation recorded for a family.
    """
    family_size = models.PositiveSmallIntegerField(
        help_text="Count of family members"
    )
    health_rating = models.PositiveSmallIntegerField(
        help_text="Health rating (1-10)"
        # Todo: storn add validator
    )
    event_type = models.CharField(
        help_text="notable event",
        max_length=10,
        choices=EVENT_TYPE_CHOICES,
        null=True,
    )
    description = models.TextField(
        help_text="event description"
    )
