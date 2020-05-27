import os
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .base import BaseModel
from .restaurant import Restaurants


class Tickets(BaseModel):
    """
        The Tickets Model.
    """
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    restaurant = models.ForeignKey(
        Restaurants, on_delete=models.CASCADE, related_name='tickets')
    max_purchase_count = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Number of coupons/tickets can be purchased.',
    )
    purchased_count = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Number of coupons/tickets already purchased.',
    )

    def __str__(self):
        return f'<Ticket: {self.name} - {self.restautant.name}>'

    @property
    def available_quantity(self):
        return self.max_purchase_count - self.purchased_count

    @property
    def purchase_url(self):
        return '{}/api/tickets/{}/purchase/'.format(os.environ.get('HOST'), self.code)

    def clean(self):
        if self.max_purchase_count - self.purchased_count < 0:
            raise ValidationError(
                'Purchased count cannot be higher than Max Purchase count')
