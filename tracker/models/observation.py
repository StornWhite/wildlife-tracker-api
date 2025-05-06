from django.db import models

from .family import Family
from .abstract import AbstractLocationTrackerModel


EVENT_TYPE_CHOICES = {
    'birth': 'birth',
    'death': 'death',
    'depart': 'departing members',
    'join': 'joining members',
    'obsv': 'observation'
}


class Observation(AbstractLocationTrackerModel):
    """
    A data observation recorded for a family.
    """
    family = models.ForeignKey(
        help_text="Related family",
        to=Family,
        on_delete=models.CASCADE,
    )
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
