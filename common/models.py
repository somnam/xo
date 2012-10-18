from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Game class
class Game(models.Model):
    users = models.ManyToManyField(User)
    name  = models.CharField(max_length=128)

