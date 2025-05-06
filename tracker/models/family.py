from django.db import models

from .abstract import AbstractNamedTrackerModel


class Family(AbstractNamedTrackerModel):
    """
    A family unit within a herd.
    """

    herd = models.ForeignKey(
        help_text="Related herd",
        to="Herd",
        related_name="families",
        on_delete=models.CASCADE
    )
