# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from go.forms import GameCreateForm
from common.models import Game

@login_required
def game_list(request):

    return render(request, 'go/game_list.html', {
        'games' : request.user.game_set.all()
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
def game_delete(request, game_id):

    # Delete game by given id
    game = Game.objects.get(pk=game_id)
    game.delete()

    return redirect('go.views.game_list')

@login_required
def game_join(request, game_id):

    # Get board size
    board = Game.objects.get(pk=game_id).board

    return render(request, 'go/test.html', {
        'columns' : board.columns,
        'rows' : board.rows,
        'size' : board.size,
    })
