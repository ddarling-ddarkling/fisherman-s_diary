from django.conf import settings
from django.db import models
from django.utils import timezone

class Diary(models.Model):
    name = models.CharField(max_length=50)
    published_date = models.DateField(blank=True, null=True)
    catch_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    feeding_type = models.CharField(max_length=30, blank=True, null=True)
    #catch_type = models.CharField(max_length=50)
    #tackle_type = models.CharField(max_length=50)
    #weather = models.CharField(max_length=50)
    #fishing_time = models.TimeField()
    #deleted = models.BooleanField() #??

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
