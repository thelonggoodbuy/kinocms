from email import message
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash


from .forms import RegisterUserForm, LoginForm, SimpleTextErrorList, ChangeUserForm



def sign_up(request):
    if request.method=="POST":
        form = RegisterUserForm(request.POST, error_class=SimpleTextErrorList)

        if form.is_valid():

            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            update_session_auth_hash(request, user)
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



def change_user_data(request):
    message = ''
    if request.method == "POST":       
        form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            # user = form.save(commit=False)
            # password = form.cleaned_data['password']
            # user.set_password(password)
            # user.save()
            # update_session_auth_hash(request, user)
            
            form.save()


            message = 'Изменения успешно применены!'
    else:
        form = ChangeUserForm(instance=request.user)

    return render(request, 'users/change_user_data.html', context={'form': form, 'message': message})