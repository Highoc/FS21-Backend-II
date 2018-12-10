from django.db import models

from users.models import User


class File(models.Model):
    name = models.CharField( max_length=32, default='unnamed_file' )
    mime = models.CharField( max_length=72 )
    key = models.CharField( max_length=72 )
    content = models.FileField( null=True, upload_to='files' )
    owners = models.ManyToManyField( User, related_name='files' )

class Feedback(models.Model):
    description = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    issue = models.CharField(max_length=100)