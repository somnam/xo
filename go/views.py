# Create your views here.

from threading import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, Http404
from django.http import HttpResponse 
from common.models import Game, Chat
from go.forms import GameCreateForm, GameEditForm
from go.models import Board, Stone, STONE_COLORS
import go.utils

go_event = Event()
chat_event = Event()

@login_required
def game_list(request):

    return render(request, 'go/game_list.html', {
        'games' : Game.objects.all()
    })

@login_required
def game_create(request):
    if request.method == "POST":
        form = GameCreateForm(request.user, request.POST)
        if form.is_valid():
            game = form.save()
            # Redirect directly to game screen
            return redirect('go.views.game_play', game_id=game.id)
    else:
        form = GameCreateForm(request.user)

    return render(
        request, 
        'go/game_create.html',
        { 'form' : form },
    )

@login_required
def game_edit(request, game_id):
    if request.method == "POST":
        form = GameEditForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('go.views.game_list')
    else:
        game = Game.objects.get(pk=game_id)
        form = GameEditForm(
            request.user,
            initial = { 'name' : game.name, 'size' : game.board.size }
        )

    return render(
        request, 
        'go/game_create.html',
        { 'form' : form },
    )

@login_required
def game_delete(request, game_id):

    # Delete game by given id
    game = Game.objects.get(pk=game_id)
    game.delete()

    return redirect('go.views.game_list')

@login_required
def game_join(request, game_id):

    # Add second player to game
    game = Game.objects.get(pk=game_id)
    game.users.add(request.user.id)
    game.save()

    # Add stones for second player
    game.board.add_stones(request.user, STONE_COLORS['white'])

    # Player join chat message
    chat = Chat.objects.get(pk=game_id)
    chat.join(request.user)

    return game_play(request, game_id)

@login_required
def game_play(request, game_id):
    # Get game board
    board = Board.objects.get(pk=game_id)

    # Get all stones placed on current Board
    stones = board.get_stones_by_row_and_col()

    # Get stone color for current user
    stone_color = board.get_user_stone_color(request.user)

    # Get stone color for next move
    next_move_color = board.get_next_move_color()

    # Get player chat
    chat = Chat.objects.get(pk=game_id)

    # Render board
    return render(request, 'go/game_play.html', {
        'board'           : board,
        'stones'          : stones,
        'stone_color'     : stone_color,
        'next_move_color' : next_move_color,
        # Get chat messages
        'messages'        : chat.message_set.all(),
    })

@login_required
def game_update(request, game_id):

    if request.method == "POST":
        # Ajax sends stone coords when we need to update Board state
        has_stone = (
            request.POST.has_key('row') and
            request.POST.has_key('col')
        )

        response = None

        # Update Board state after current players move
        if has_stone:
            # Update stone state with users move
            go.utils.stone_update(request, game_id)

            # All waiting listeners are awakened
            go_event.set()

            # Subsequent calls to 'wait' will block unitl 'set' is called
            go_event.clear()

            # Refresh board via ajax
            response = HttpResponse()
        # Update Board after other players move
        else:
            # Block listeners until another thread calls 'set'
            go_event.wait()

            # Get updated board data in serialized form
            response = HttpResponse(
                go.utils.get_board_update_json(game_id)
            )

        return response
    else:
        raise Http404

@login_required
def chat_say(request, game_id):
    if request.method == "POST":
        # Update chat state after current players message
        response = None
        if request.POST.has_key('message'):
            go.utils.chat_update(request, game_id)

            # All waiting listeners are awakened
            go_event.set()

            # Subsequent calls to 'wait' will block unitl 'set' is called
            go_event.clear()

            # Refresh board via ajax
            response = HttpResponse()
        else:
            # Block listeners until another thread calls 'set'
            go_event.wait()

            response = HttpResponse(
                go.utils.get_chat_update_json(game_id)
            )

        return response
    else:
        raise Http404
