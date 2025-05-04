from django.db import models

from .abstract import AbstractNamedTrackerModel
from ..data.species import SPECIES_CHOICES


class Herd(AbstractNamedTrackerModel):
    """
    A collection of families from the same species who range together.
    """

    species = models.CharField(
        help_text="Species",
        max_length=100,
        choices=SPECIES_CHOICES,
    )
