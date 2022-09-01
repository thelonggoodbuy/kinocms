from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

# from .models import Galery, BannerWithTimeScrolling
from .models import Galery, HighestBannerWithTimeScrolling, BannerCell, ThroughBackroundBanner
from users.models import CustomUser
from .forms import AddBannerCellForm, HighestBannerForm, ThroughBackroundBannerForm, AddPhotoToGalleryForm
from users.forms import ChangeUserForm, SimpleTextErrorList
from django import forms



@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_users(request):
    users_list = CustomUser.objects.filter(is_active=True, is_superuser=False)
    context = {'users_list': users_list}
    return render(request, 'cinema/all_users.html', context)


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
        my_banner = HighestBannerWithTimeScrolling.objects.get(pk=1)
        
    except:
        my_banner = HighestBannerWithTimeScrolling(pk=1, on_of_status=True, timescrolling=5)

    try:
        through_background_banner = ThroughBackroundBanner.objects.get(pk=1)
    except:
        through_background_banner = ThroughBackroundBanner(pk=1, background_type='simple_photo', background=None)


    AddBannerCellFormSet = forms.modelformset_factory(BannerCell, form = AddBannerCellForm, 
                                            can_delete=True, extra=0, min_num=1,
                                             max_num=25)

    # highest banner forms    
    highest_banner_form = HighestBannerForm(request.POST, instance = my_banner)
    add_banner_cell_formset = AddBannerCellFormSet(request.POST, request.FILES)

    # through background banner forms 
    through_background_banner_form = ThroughBackroundBannerForm(request.POST, instance = through_background_banner)
    add_photo_to_galery_form = AddPhotoToGalleryForm(request.POST, request.FILES, instance = through_background_banner.background )



    if request.method == 'POST':
        # highest banner logic
        if highest_banner_form.is_valid() and add_banner_cell_formset.is_valid():
            current_banner = highest_banner_form.save(commit=False)
            add_banner_cell_formset.save()
            for form in add_banner_cell_formset:
                if form.instance.id != None:
                    current_banner.banner_cell.add(form.instance.id)
            current_banner.save()
            return redirect(request.path)

         # through background banner logic
        if through_background_banner_form.is_valid() and add_photo_to_galery_form.is_valid():
            current_though_banner = through_background_banner_form.save(commit = False)
            photo =  add_photo_to_galery_form.save()
            current_though_banner.background = photo
            current_though_banner.save()
            return redirect(request.path)

        
    else:
        # highest banner forms
        highest_banner_form = HighestBannerForm(instance = my_banner)
        add_banner_cell_formset = AddBannerCellFormSet(queryset=my_banner.banner_cell.all())        

        # through background banner forms 
        through_background_banner_form = ThroughBackroundBannerForm(instance = through_background_banner)
        add_photo_to_galery_form = AddPhotoToGalleryForm(instance = through_background_banner.background)


    context = {'highest_banner_form': highest_banner_form,
                'add_banner_cell_formset': add_banner_cell_formset,
                'through_background_banner_form': through_background_banner_form,
                'add_photo_to_galery_form': add_photo_to_galery_form,
                }

    return render(request, 'cinema/add_banners.html', context)