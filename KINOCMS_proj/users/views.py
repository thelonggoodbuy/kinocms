
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse




from .forms import RegisterUserForm, LoginForm, SimpleTextErrorList, ChangeUserForm
from .models import CustomUser



def sign_up(request):
    if request.method=="POST":
        form = RegisterUserForm(request.POST, error_class=SimpleTextErrorList)

        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if password != '':
                user.set_password(password)
                user.save()
            login(request, user)

            return redirect('pages:index')
    else:        
        form = RegisterUserForm(error_class=SimpleTextErrorList)
    return render(request, template_name="users/sign_up.html", context={'form': form})



def sign_in(request):
    message = ""
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
                    message = 'Пользователь не активен'
            else:
                message = 'Не правильный пароль'
    else:
        form = LoginForm()

    return render(request, 'users/sign_in.html', context={'form': form, 'message': message})


def log_out(request):
    logout(request)
    return redirect('pages:index')


@login_required
def change_user_data(request):
    message = ''
    form_user_data = ChangeUserForm(request.POST, instance=request.user, error_class=SimpleTextErrorList)
    if request.method == "POST":   
        form_user_data = ChangeUserForm(request.POST, instance=request.user, error_class=SimpleTextErrorList)

        if form_user_data.is_valid():
            
            if form_user_data.cleaned_data['password'] == '':
                request.user.save(update_fields=['name', "surname", "nickname", 
                                                "email", "address", "card_id", 
                                                "language", "sex", "town", 
                                                "phone_number", "born"])
            else:
                user = form_user_data.save(commit=False)
                password = form_user_data.cleaned_data['password']
                user.set_password(password)
                update_session_auth_hash(request, user)
                user.save()

    else:
        form_user_data = ChangeUserForm(instance=request.user, error_class=SimpleTextErrorList)

    return render(request, 'users/change_user_data.html', context={'form_user_data': form_user_data,
                                                                     'message': message})


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def del_user(request, pk):

    user = get_object_or_404(CustomUser, id=pk)
    context = {"user": user}
    if request.method == "POST":
        user.delete()
        return HttpResponseRedirect(reverse('cinema:all_users'))
    return render(request, "users/delete_user.html", context)


