from go.models import Board, BOARD_SIZES, STONE_COLORS
from common.models import Game
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

class GameCreateForm(forms.Form):
    name = forms.CharField(
        max_length=128,
        label="Game name",
    )
    size = forms.ChoiceField(
        choices=BOARD_SIZES,
        label="Board size"
    )

    def __init__(self, user=None, *args, **kwargs):
        super(GameCreateForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self):
        # Create a new Game instance for current user
        game = Game(name=self.cleaned_data['name'])
        game.save()
        game.users.add(self.user.id)
        game.save()
        
        # Create a new Board instance and assign it to created game
        board = Board(game_id=game.id, size=self.cleaned_data['size'])

        # Create black Stone instances for first player.
        # Second player will have white stones.
        board.add_stones(self.user, STONE_COLORS['black'])

        return game

class GameEditForm(GameCreateForm):
    # TODO
    pass

class StoneCreateForm(forms.Form):
    board = forms.ModelChoiceField(queryset = Board.objects.all())
    user  = forms.ModelChoiceField(queryset = User.objects.all())
    row   = forms.IntegerField()
    col   = forms.IntegerField()
    color = forms.IntegerField()

    def __init__(self, request=None, *args, **kwargs):
        super(StoneCreateForm, self).__init__(*args, **kwargs)
        # Append request to form for validation
        self.request = request

    def clean(self):
        # Run base validation
        cleaned_data = super(StoneCreateForm, self).clean()

        self.clean_coordinates(cleaned_data)
        self.clean_can_place_stone(cleaned_data)

        return cleaned_data

    def clean_coordinates(self, cleaned_data):
        """Check if stone with given coords already exists."""

        already_exists = cleaned_data['board'].stone_set.filter(
            row = cleaned_data['row'],
            col = cleaned_data['col'],
        ).count()

        if already_exists:
            raise ValidationError('ERR_STONE_001')

    def clean_can_place_stone(self, cleaned_data):
        """Check if it's users turn to place stone on board."""

        # Get color of last placed stone
        board               = cleaned_data['board']
        latest_placed_color = board.get_latest_placed_stone_color_code()
        user_color          = board.get_user_stone_color_code(
            cleaned_data['user']
        )

        if latest_placed_color == user_color:
            raise ValidationError('ERR_STONE_002')

class StoneDeleteForm(StoneCreateForm):
    def clean(self):
        # Run base validation
        cleaned_data = super(StoneCreateForm, self).clean()

        self.clean_can_remove_stone(cleaned_data)

        return cleaned_data

    def clean_can_remove_stone(self, cleaned_data):
        """Check if user can remove selected stone from board."""

        board               = cleaned_data['board']
        latest_placed_color = board.get_latest_placed_stone_color_code()
        user_color          = board.get_user_stone_color_code(
            self.request.user
        )

        # User can remove stone only:
        can_remove_stone = (
            # - after placing his stone on board
            latest_placed_color == user_color and
            # - when it's the second players stone
            cleaned_data['color'] != user_color
        )

        if not can_remove_stone:
            raise ValidationError('ERR_STONE_003')


