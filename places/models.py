from django.conf import settings
from django.db import models


class Place(models.Model):
    VISIBILITY_CHOICES = [
        ('me', 'Только мне'),
        ('all', 'Всем'),
    ]

    name = models.CharField(max_length=30)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=3, choices=VISIBILITY_CHOICES, default='me')
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    deleted = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name
