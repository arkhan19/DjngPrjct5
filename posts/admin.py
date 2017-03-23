from django.contrib import admin
from posts import models
# Register your models here.
admin.site.register(models.Posts)  # to show Post table in admin page
