# Create your views here.

from threading import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, Http404
from django.http import HttpResponse 
from django.core import serializers
from common.models import Game
from go.forms import GameCreateForm, GameEditForm
from go.models import Board, Stone, STONE_COLORS

_event = Event()

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
            form.save()
            return redirect('go.views.game_list')
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

    # Get game board
    board = game.board

    # Add stones for second player
    board.add_stones(request.user.id, STONE_COLORS['white'])

    # Get all stones placed on current Board
    stones = board.get_stones_by_row_and_col()

    # Get stone color for current user
    stone_color = board.get_stone_color(request.user.id)

    # Render board
    return render(request, 'go/test.html', {
        'board'       : board,
        'stones'      : stones,
        'stone_color' : stone_color,
    })

@login_required
def game_play(request, game_id):
    # Get game board
    board = Board.objects.get(pk=game_id)

    # Get all stones placed on current Board
    stones = board.get_stones_by_row_and_col()

    # Get stone color for current user
    stone_color = board.get_stone_color(request.user.id)

    # Render board
    return render(request, 'go/test.html', {
        'board'       : board,
        'stones'      : stones,
        'stone_color' : stone_color,
    })

@login_required
def game_update(request, game_id):

    if request.method == "POST":
        # Get game board
        board = Board.objects.get(pk=game_id)

        # Ajax sends stone coords when we need to update Board state
        has_stone = (
            request.POST.has_key('row') and
            request.POST.has_key('col')
        )

        response = None

        # Update Board state after current players move
        if has_stone:
            # Get first stone that isn't placed on Board
            stone = board.get_first_not_placed_stone(request.user.id)
            
            # Update stone state with users move
            stone.row,stone.col = request.POST['row'], request.POST['col']
            stone.save()

            # All waiting listeners are awakened
            _event.set()

            # Subsequent calls to 'wait' will block unitl 'set' is called
            _event.clear()

            # Refresh board via ajax
            response = HttpResponse()
        # Update Board after other players move
        else:
            # Block listeners until another thread calls 'set'
            _event.wait()

            # Refresh board via ajax
            serialized_stones = serializers.serialize(
                'json',
                board.get_placed_stones(),
                fields=('row', 'col', 'color')
            )
            response = HttpResponse(serialized_stones)

        return response
    else:
        raise Http404

