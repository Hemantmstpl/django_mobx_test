from django.core.validators import MinValueValidator
from django.db import models

from .base import BaseModel
from .tickets import Tickets


class Purchase(BaseModel):
    """
        The model to store purchase details.
    """
    email = models.EmailField()
    ticket = models.ForeignKey(
        Tickets, on_delete=models.CASCADE, related_name='purchase')
    count = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Number of tickets to be purchased.',
    )

    def __str__(self):
        return self.email
