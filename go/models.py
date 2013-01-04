from django.db import models
from django.contrib.auth.models import User
from common.models import Game
from go.validators import StoneValidator

# Create your models here.

# Board
BOARD_SIZES = (
    (u'9x9',   u'Small'),
    (u'13x13', u'Regular'),
    (u'19x19', u'Large'),
)
STONE_COLORS = {
    'black' : 0,
    'white' : 1,
}
DECODED_COLOR = { 
    0 : 'black',
    1 : 'white',
}
class Board(models.Model):
    STONES_BY_BOARD_SIZE = {
        '9x9'   : { STONE_COLORS['black'] : 41,  STONE_COLORS['white'] : 40  },
        '13x13' : { STONE_COLORS['black'] : 85,  STONE_COLORS['white'] : 84  },
        '19x19' : { STONE_COLORS['black'] : 181, STONE_COLORS['white'] : 180 },
    }
    game = models.OneToOneField(Game, primary_key=True)
    size = models.CharField(max_length=5, choices=BOARD_SIZES, default='13x13')

    rows    = None
    columns = None

    def __init__(self, *args, **kwargs):
        # Run base constructor
        super(Board, self).__init__(*args, **kwargs)

        # Set rows and cols values
        self.rows,self.columns = map(
            lambda(c) : int(c),
            self.size.split('x')
        )

    def add_stones(self, user_id, color):
        """Append stones of given color to given user."""

        # Get parameters for stones
        stones_by_board  = self.STONES_BY_BOARD_SIZE[self.size]
        stones_count     = stones_by_board[color]

        # Get current stones count
        current_stones_count = self.stone_set.count()

        # Add black stones only when there are no stones added yet
        # Add white stones only when there are black stones added
        can_add_stones = (
            (color == STONE_COLORS['black'] and current_stones_count == 0) or
            (
                color == STONE_COLORS['white'] and
                current_stones_count == stones_by_board[STONE_COLORS['black']]
            )
        )

        if can_add_stones:
            # Create Stone instances
            for _ in range(0, stones_count):
                self.stone_set.create(user_id=user_id, color=color)
            # Save changes
            self.save()

    def get_placed_stones(self):
        """Get all stones placed on given board."""
        return self.stone_set.exclude(row=-1, col=-1)

    def get_latest_placed_stone_color_code(self):
        """Get color code of last placed stone."""

        placed_stones = self.get_placed_stones()

        color_code = None
        if placed_stones.count():
            color_code = placed_stones.latest().color

        return color_code

    def get_next_move_color(self):
        """Get color code for next board move."""
        latest_placed_color = self.get_latest_placed_stone_color_code()

        # By default set 'black' as next move color
        next_move_color_code = STONE_COLORS['black']
        if not latest_placed_color is None:
            next_move_color_code = 0 if latest_placed_color else 1

        return DECODED_COLOR[next_move_color_code]

    def get_stones_by_row_and_col(self):
        """Map stones placed on board by row and column."""

        # Get all stones that have coordinates set on board
        stones = self.get_placed_stones()

        # Map by row and column
        placed_stones = {}
        for stone in stones:
            if not placed_stones.has_key(stone.row):
                placed_stones[stone.row] = {}
            placed_stones[stone.row][stone.col] = stone.get_color()

        return placed_stones

    def get_user_stone_color_code(self, user_id):
        """Get color code of stones for given user."""
        user    = User.objects.get(pk=user_id)
        stone   = user.stone_set.filter(board_id = self.game_id)[0]
        return stone.color

    def get_user_stone_color(self, user_id):
        return DECODED_COLOR[self.get_user_stone_color_code(user_id)]

    def get_first_not_placed_stone(self, user_id):
        """Get first stone that is not placed on Board."""

        user = User.objects.get(pk=user_id)

        # Check if there are any non-placed stones left
        query_params = {
            'board_id' : self.game_id,
            'row'      : -1,
            'col'      : -1,
        }
        has_non_placed_stones = user.stone_set.filter(**query_params).count()

        # Add stones to users set if all were placed on board
        if not has_non_placed_stones:
            self.add_stones(user_id, self.get_user_stone_color_code())

        # Get first non-placed stone
        return user.stone_set.filter(**query_params)[0]

# Stone
class Stone(models.Model):
    board    = models.ForeignKey(Board)
    user     = models.ForeignKey(User)
    row      = models.SmallIntegerField(default=-1)
    col      = models.SmallIntegerField(default=-1)
    color    = models.SmallIntegerField()
    set_date = models.DateTimeField(auto_now=True)

    class Meta:
        # Used for fetching latest created stone
        get_latest_by = 'set_date'
    
    def clean(self):
        StoneValidator(self).clean()

    def get_color(self):
        return DECODED_COLOR[self.color]
