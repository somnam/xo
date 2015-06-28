# Create your views here.

import django.contrib.auth.views

from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm

def login(request):
    response = None

    # Init authenticated user
    if not request.method == "POST" and request.user.is_authenticated():
        # Redirect to home view
        response = redirect(settings.LOGIN_REDIRECT_URL)
    # Init or save not authenticated user
    else:
        # Init - redirect to login page
        # Save - validate login data
        response = django.contrib.auth.views.login(request)

    return response

def register(request):
    # Save
    if request.method == "POST":
        # Validate registration form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Form is ok - store new user
            form.save()
            # Redirect to login page
            return redirect('authorization.views.login')
    # Init
    else:
        form = UserCreationForm()

    # Init with/without errors
    return render(
        request,
        'registration/register.html',
        { 'form' : form },
    )
