from email import message
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.forms.utils import ErrorList
from django.http import HttpResponse


from .forms import RegisterUserForm, LoginForm, SimpleTextErrorList



def sign_up(request):
    if request.method=="POST":
        form = RegisterUserForm(request.POST, error_class=SimpleTextErrorList)

        if form.is_valid():

            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            return redirect('pages:index')
    else:        
        form = RegisterUserForm(error_class=SimpleTextErrorList)
    return render(request, template_name="users/sign_up.html", context={'form': form})



def sign_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('pages:index')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'users/sign_in.html', context={'form': form})


def log_out(request):
    logout(request)
    return redirect('pages:index')


