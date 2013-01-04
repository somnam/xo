from django.core.exceptions import ValidationError
from django.core import serializers
from django.utils import simplejson
from go.models import Board

def stone_update(request, game_id):
    """Update stone state with users move."""

    # Get game board
    board = Board.objects.get(pk=game_id)

    # Get first stone that isn't placed on Board
    stone = board.get_first_not_placed_stone(request.user.id)

    # Get users move coordinates
    stone.row,stone.col = request.POST['row'],request.POST['col']

    # Validate stone
    try:
        stone.full_clean()
    # Validation failed - don't update
    except ValidationError as e:
        pass
    # Move is correct - update stone state
    else:
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

