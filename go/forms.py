from go.models import Board, BOARD_SIZES
from common.models import Game
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

    def __init__(self, user, *args, **kwargs):
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
        board.save()

        # TODO: create Cell/Stone instances

        return game
