# from django.conf import settings
# from django.db import models
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     region = models.CharField(max_length=160, null=True, blank=True)
#     bio = models.CharField(max_length=160, null=True, blank=True)
#     birthday = models.DateField(null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
