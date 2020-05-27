from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
        The basic model for logging events.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
