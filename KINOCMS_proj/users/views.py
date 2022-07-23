from email import message
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


from .forms import RegisterUserForm





def sign_up(request):
    if request.method=="POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages:index')

    form = RegisterUserForm()
    return render(request=request, template_name="users/sign_up.html", context={'form': form})
