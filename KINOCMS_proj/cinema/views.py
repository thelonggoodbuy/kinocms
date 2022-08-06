from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test


from users.models import CustomUser
from .forms import SearchUserForm
from users.forms import ChangeUserForm, ChangeUserPassword



@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_users(request):
    users_list = CustomUser.objects.filter(is_active=True, is_superuser=False)
    context = {'users_list': users_list}
    return render(request, 'cinema/all_users.html', context)

# @login_required
# @user_passes_test(lambda admin: admin.is_superuser)
# def all_users(request):
#     users_list = CustomUser.objects.filter(is_active=True, is_superuser=False)
#     if 'keyword' in request.GET:
#         keyword = request.GET['keyword']
#         q = (Q(name__icontains=keyword) | 
#         Q(nickname__icontains=keyword) |
#         Q(surname__icontains=keyword) |
#         Q(email__icontains=keyword))
#         users_list = users_list.filter(q)
#     else:
#         keyword = ''
#     search_form = SearchUserForm(initial={'keyword':keyword})
#     paginator = Paginator(users_list, 5)
#     if 'page' in request.GET:
#         page_num = request.GET['page']    
#     else:
#         page_num = 1
#     page = paginator.get_page(page_num)
#     context = {'page': page, 'users_list': page.object_list, 'form': search_form}
#     return render(request, 'cinema/all_users.html', context)

@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def change_user_data_by_admin(request, pk):
    message = ''
    user = get_object_or_404(CustomUser, id=pk)
    form_user_data = ChangeUserForm(request.POST, instance=user)
    form_user_access = ChangeUserPassword(request.POST)
    if request.method == "POST":
        if 'email' in request.POST:
            form_user_data = ChangeUserForm(request.POST, instance=user)
            if form_user_data.is_valid():
                form_user_data.save()
                if form_user_data.has_changed():
                    message = 'данные пользователя изменены'

        else:
            form_user_data = ChangeUserForm(instance=user)

        if request.POST['password'] != '':
            form_user_access = ChangeUserPassword(request.POST, instance=user)
            if form_user_access.is_valid():
                user = form_user_access.save(commit=False)
                password = form_user_access.cleaned_data['password']
                user.set_password(password)
                user.save()
        else:
            form_user_access = ChangeUserPassword()

    else:
        form_user_data = ChangeUserForm(instance=user)
        form_user_access = ChangeUserPassword()


    if form_user_access.has_changed():
        message = 'пароль изменен'

    return render(request, 'cinema/change_user_data.html', context={'form_user_data': form_user_data,
                                                                    'form_user_access': form_user_access,
                                                                     'message': message})