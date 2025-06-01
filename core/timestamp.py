from django.db import models 


class TimeStampModel(models.Model):
    """
    Abstract model to add created and modified timestamps.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 