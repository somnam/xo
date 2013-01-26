from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import simplejson
from go.models import Board
from go.forms import StoneCreateForm, StoneDeleteForm

def stone_update(request, game_id):
    """Update stone state with users move."""

    # Get user action performed on stone (by default assume 'add')
    action = 'add'
    if request.POST.has_key('action'):
        action = request.POST['action']

    # Get game board
    board = Board.objects.get(pk=game_id)

    # 'add' - user adds stone to board
    # 'del' - user removes stone from board
    form,stone = None,None
    if action == 'add':
        # Get first stone that isn't placed on Board
        stone = board.get_first_not_placed_stone(request.user.id)
        # Update stone with users move coordinates
        stone.row,stone.col = request.POST['row'],request.POST['col']
        # Create add form
        form = StoneCreateForm(
            request = request,
            data    = model_to_dict(stone),
        )
    elif action == 'del':
        try:
            # Get stone by user coordinates
            stone = board.stone_set.get(
                row = request.POST['row'],
                col = request.POST['col']
            )
        except ObjectDoesNotExist:
            pass
        else:
            # Set stone coordinates to -1, -1
            stone.row,stone.col = -1,-1
            # Create delete from
            form = StoneDeleteForm(
                request = request,
                data    = model_to_dict(stone),
            )

    # Validate stone
    if form and form.is_valid():
        # Update stone state
        stone.save()

def get_board_update_json(game_id):
    """Serialize board stones and additional data for board update."""

    # Get game board
    board = Board.objects.get(pk=game_id)

    # First convert placed stones query to python struct, so it can be easily
    # serialized via simplejson
    placed_stones = serializers.serialize(
        'python',
        board.get_placed_stones(),
        fields=('row', 'col', 'color')
    )

    # Get color of next move
    next_move_color = board.get_next_move_color()

    return simplejson.dumps({
        'placed_stones'     : placed_stones,
        'next_move_color'   : next_move_color,
    })

