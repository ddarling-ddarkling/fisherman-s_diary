from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone


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

    def average_rating(self):
        if Rating.objects.filter(place_id=self):
            return Rating.objects.filter(place_id=self).aggregate(Sum('rating')).get('rating__sum', 0) / (len(Rating.objects.filter(place_id=self)))
        else:
            return 0


class Rating(models.Model):
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

