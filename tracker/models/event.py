from django.db import models

from . import AbstractFamilyLocationTrackerModel


EVENT_TYPE_CHOICES = {
    'birth': 'birth',
    'death': 'death',
    'depart': 'departing members',
    'join': 'joining members',
}


class Event(AbstractFamilyLocationTrackerModel):
    """
    A notable event observed for a family.
    """
    event_type = models.CharField(
        help_text="notable event",
        max_length=10,
        choices=EVENT_TYPE_CHOICES
    )
    description = models.TextField(
        help_text="event description"
    )
