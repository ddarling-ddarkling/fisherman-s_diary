from django.contrib import admin
from .models import Diary, Comment, Mark, Image

admin.site.register(Diary)
admin.site.register(Comment)
admin.site.register(Mark)
admin.site.register(Image)
