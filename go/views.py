# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def game_list(request):

    return render(request, 'go/game_list.html', {
        'games' : request.user.game_set.all()
    })

@login_required
def test(request):
    return render(request, 'go/test.html', { 
        'columns' : 19,
        'rows' : 19,
    })
