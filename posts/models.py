from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# models for people will create post


class Posts(models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField()
    author = models.ForeignKey(User)  # ForeignKey helps in indicating that this Author field will be linked to User
    # model rather than a single user from database. So if the user changes his name or something, this FK will point to
    # the object instead of a database entry
    pub_date = models.DateTimeField()
    commends = models.IntegerField(default=0)
