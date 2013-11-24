from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import simplejson
from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import User
from go.models import Board
from go.forms import StoneCreateForm, StoneDeleteForm
from common.models import Chat, Message
import redis

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
        stone = board.get_first_not_placed_stone(request.user)
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

def emit_board_update(game_id, channel):
    redis.StrictRedis().publish(channel, get_board_update_json(game_id))

def get_board_update_json(game_id):
    """Serialize board stones and additional data for board update."""

    # Get game board
    board = Board.objects.get(pk=game_id)

    # First convert placed stones query to python struct, so it can be easily
    # serialized via simplejson
    serialize_fields  = ('row', 'col', 'color')
    placed_stones     = board.get_placed_stones()
    serialized_stones = serializers.serialize(
        'python',
        placed_stones,
        fields=serialize_fields
    )

    # Get color of next move
    next_move_color = board.get_next_move_color()

    # Get latest placed stone
    latest_placed_stone = None
    if placed_stones.count():
        # Hackish serialization, but it works ;-)
        latest_placed_stone = serializers.serialize(
            'python',
            (placed_stones.latest(),),
            fields=serialize_fields
        )[0]

    return simplejson.dumps({
        'placed_stones'         : serialized_stones,
        'next_move_color'       : next_move_color,
        'latest_placed_stone'   : latest_placed_stone,
    })

def emit_chat_update(game_id, channel):
    redis.StrictRedis().publish(channel, get_chat_update_json(game_id))

def chat_update(request, game_id):
    chat = Chat.objects.get(pk=game_id)

    # Update chat state with users message
    message = Message(
        chat=chat,
        author=request.user,
        message=request.POST['message'],
    )
    message.save()

def get_chat_update_json(game_id):
    chat = Chat.objects.get(pk=game_id)

    # Get updated chat data in serialized form
    chat_messages = serializers.serialize(
        'python',
        chat.message_set.all(),
        fields=('author', 'type', 'message', 'timestamp')
    )

    for message in chat_messages:
        fields = message['fields']

        # Append author name to serialized data
        user_id = fields['author']
        if user_id:
            user    = User.objects.get(pk=user_id)
            message['fields']['author'] = user.username

        # Get timestamp in current timezone
        timestamp = fields['timestamp'].astimezone(tz=get_current_timezone())
        # Append formated timestamp
        message['fields']['timestamp'] = timestamp.strftime('%X')

    return simplejson.dumps({
        'chat_messages' : chat_messages,
    })
