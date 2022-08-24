from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

from .models import Galery, BannerWithTimeScrolling
from users.models import CustomUser
from .forms import SearchUserForm, AddImageToGalery
from users.forms import ChangeUserForm, SimpleTextErrorList
from django import forms



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
    print(user.name)
    form_user_data = ChangeUserForm(request.POST, instance=user, error_class=SimpleTextErrorList)
    if request.method == "POST":   
        form_user_data = ChangeUserForm(request.POST, instance=user, error_class=SimpleTextErrorList)
        if form_user_data.is_valid():
            print(user.phone_number)
            if form_user_data.cleaned_data['password'] == '':
                user.save(update_fields=['name', "surname", "nickname", 
                                                "email", "address", "card_id", 
                                                "language", "sex", "town", 
                                                "phone_number", "born"])
                if form_user_data.has_changed():
                    message = 'данные пользователя изменены'
            
            else:
                user_with_password = form_user_data.save(commit=False)
                password = form_user_data.cleaned_data['password']
                user_with_password.set_password(password)
                user_with_password.save()
                if form_user_data.has_changed():
                    message = 'данные пользователя и пароль изменены'
    else:
        form_user_data = ChangeUserForm(instance=user, error_class=SimpleTextErrorList)

    return render(request, 'cinema/change_user_data.html', context={'form_user_data': form_user_data,
                                                                     'message': message})


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def add_banners(request):
    try:
        my_banner = BannerWithTimeScrolling.objects.get(pk=1)
    except:
        my_banner = BannerWithTimeScrolling(pk=1)

    ImageFormSet = forms.modelformset_factory(Galery, form = AddImageToGalery, 
                                            can_delete=True, extra=0,
                                             max_num=25)
    if request.method == 'POST':
        image_form_set = ImageFormSet(request.POST, request.FILES)
        if image_form_set.is_valid():
            image_form_set.save()
            for form in image_form_set:
                if form.instance.id != None:
                    my_banner.galery.add(form.instance.id)
            my_banner.save()
            
            return redirect(request.path)
            
    else:
        image_form_set = ImageFormSet(queryset=my_banner.galery.all())

    context = { 'image_form_set': image_form_set,
                'my_banner': my_banner}

    return render(request, 'cinema/add_banners.html', context)

