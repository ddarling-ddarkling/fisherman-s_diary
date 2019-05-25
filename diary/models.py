from django.conf import settings
from django.db import models
from django.utils import timezone

class Diary(models.Model):
    WEATHER_CHOICES = [
        ('sun', 'ясно'),
        ('cloud', 'облачно'),
        ('thundercloud', 'пасмурно'),
        ('rain', 'небольшой дождь'),
        ('rainstorm', 'сильный дождь'),
    ]
    FISHING_TIME_CHOICES = [
        ('morning', 'утро'),
        ('afternoon', 'день'),
        ('evening', 'вечер'),
        ('night', 'ночь'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    published_date = models.DateField(blank=True, null=True)
    catch_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    feeding_type = models.CharField(max_length=30, blank=True, null=True)
    catch_type = models.CharField(max_length=50, blank=True, null=True)
    tackle_type = models.CharField(max_length=50, blank=True, null=True)
    fishing_time = models.CharField(max_length=12, choices=FISHING_TIME_CHOICES, default='morning')
    weather = models.CharField(max_length=12, choices=WEATHER_CHOICES, default='sun')
    deleted = models.BooleanField(blank=True, default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def comments_amount(self):
        return len(Comment.objects.filter(diary_id=self))


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)
    description = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


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

