from django.contrib import admin
from .models import Diary, Comment, Mark

admin.site.register(Diary)
admin.site.register(Comment)
admin.site.register(Mark)
