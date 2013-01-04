from django.core.exceptions import ValidationError

class StoneValidator:
    """Validator object for Stone class."""

    def __init__(self, stone):
        self.stone = stone
        self.board = stone.board

    def clean(self):
        """Run all validation methods."""
        self.coordinates()
        self.can_place_stone()

    def coordinates(self):
        """Check if stone with given coords already exists."""

        already_exists = self.board.stone_set.filter(
            row = self.stone.row,
            col = self.stone.col,
        ).count()

        if already_exists:
            raise ValidationError('ERR_STONE_001')

    def can_place_stone(self):
        """Check if it's users turn to place stone on board."""

        # Get color of last placed stone
        latest_placed_color = self.board.get_latest_placed_stone_color_code()
        user_color          = self.board.get_user_stone_color_code(
            self.stone.user.id
        )

        if latest_placed_color == user_color:
            raise ValidationError('ERR_STONE_002')
