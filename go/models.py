from django.db import models
from django.contrib.auth.models import User
from common.models import Game

# Create your models here.

# Board
BOARD_SIZES = (
    (u'9x9',   u'Small'),
    (u'13x13', u'Regular'),
    (u'19x19', u'Large'),
)
class Board(models.Model):
    game = models.OneToOneField(Game, primary_key=True)
    size = models.CharField(max_length=5, choices=BOARD_SIZES, default='13x13')

    def __init__(self, *args, **kwargs):
        # Run base constructor
        super(Board, self).__init__(*args, **kwargs)

        # Set rows and cols values
        self.rows,self.columns = map(
            lambda(c) : int(c),
            self.size.split('x')
        )

# Cell
class Cell(models.Model):
    board = models.ForeignKey(Board)


# Stone
class Stone(models.Model):
    cell = models.ForeignKey(Cell)
    user = models.ForeignKey(User)
