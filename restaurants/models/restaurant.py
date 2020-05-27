from django.contrib.auth.models import User
from django.db import models

from .base import BaseModel


class Restaurants(BaseModel):
    """
        The Restaurants Model.
    """
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='restaurants')

    def __str__(self):
        return f'<Restaurant:{self.id}-{self.name}>'
