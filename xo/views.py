# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    # TODO: implement actual view
    return render(request, 'base.html')

