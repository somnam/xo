from django.db import models
from django.contrib.auth.models import User
from common.models import Game

# Create your models here.

# Board
class Board(models.Model):
    game = models.OneToOneField(Game, primary_key=True)

# Cell
class Cell(models.Model):
    board = models.ForeignKey(Board)

# Stone
class Stone(models.Model):
    cell = models.ForeignKey(Cell)
    user = models.ForeignKey(User)
