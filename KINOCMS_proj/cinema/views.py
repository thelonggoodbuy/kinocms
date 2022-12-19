from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib import messages


# from .models import Galery, BannerWithTimeScrolling
from .models import Galery, HighestBannerWithTimeScrolling, BannerCell, ThroughBackroundBanner, BannerPromotionsAndNews, Movie, Cinema, CinemaHall
from users.models import CustomUser
from .forms import AddBannerCellForm, HighestBannerForm, ThroughBackroundBannerForm, AddPhotoToGalleryForm, BannerPromotionsAndNewsForm, AddBannerPromotionAndNewsCellForm, MovieForm, MovieMainImage, MovieGaleryImageForm, SeoBlockForm, SimpleTextErrorList, CinemaHallForm, CinemaForm
from users.forms import ChangeUserForm, SimpleTextErrorList
from django import forms


# Users logic***********************************************************************************************************
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




# Banner logic***********************************************************************************************************
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

    try:
        banner_promotion_and_news = BannerPromotionsAndNews.objects.get(pk=1)
    except:
        banner_promotion_and_news = BannerPromotionsAndNews(pk=1, on_of_status=True, timescrolling=10)
    

    # highest banner forms
    AddBannerCellFormSet = forms.modelformset_factory(BannerCell, form = AddBannerCellForm, 
                                            can_delete=True, extra=0, min_num=1,
                                             max_num=25)
    highest_banner_form = HighestBannerForm(request.POST, instance = my_banner, prefix='highest_banner')
    add_banner_cell_formset = AddBannerCellFormSet(request.POST, request.FILES)

    # through background banner forms 
    through_background_banner_form = ThroughBackroundBannerForm(request.POST, instance = through_background_banner)
    add_photo_to_galery_form = AddPhotoToGalleryForm(request.POST, request.FILES, instance = through_background_banner.background)

    # banner from promotions and news
    AddBannerPromoFormset = forms.modelformset_factory(BannerCell, form = AddBannerPromotionAndNewsCellForm,
                                                        can_delete=True, extra=0, min_num=1,
                                                        max_num=25)
    banner_promotions_and_news_form = BannerPromotionsAndNewsForm(request.POST, instance = banner_promotion_and_news, prefix='banner_promotion_and_news')
    add_bannee_promo_cell_formset = AddBannerPromoFormset(request.POST, request.FILES)
    

    if request.method == 'POST':
        # highest banner logic
        if "btnform1" in request.POST:
            if highest_banner_form.is_valid() and add_banner_cell_formset.is_valid():
                print('оба баннера валидированы')
                highest_banner_form.save()
                add_banner_cell_formset.save()
                messages.success(request, "Верхній баннер(и) змінено")
                return redirect(request.path)
            else:
                list_of_error = []
                # print(f' баннер: {highest_banner_form.is_valid()}')
                # print(f' ячейки: {add_banner_cell_formset.is_valid()}')
                print(highest_banner_form.errors)
                if highest_banner_form.is_valid() == False:
                    list_of_error = highest_banner_form.errors.as_data()
                    print(f'This is banner: {list_of_error}.')
                    for err in list_of_error: 
                        # print(err)
                        if bool(err):
                            # print(err)
                            messages.error(request, f"Верхній баннер(и) помилка: {err}")

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                if add_banner_cell_formset.is_valid() == False:
                    list_of_error = add_banner_cell_formset.errors
                    # print(list_of_error)
                    for err in list_of_error:
                        print(err)
                        if bool(err):
                            messages.error(request, err)
                            
        else:
            highest_banner_form = HighestBannerForm(instance = my_banner, prefix='highest_banner')      
            add_banner_cell_formset = AddBannerCellFormSet(queryset=BannerCell.objects.filter(purpose='highest_banner').all()) 
            

         # through background banner logic
        if "btnform2" in request.POST:
            print('валидация второго баннера')
            if through_background_banner_form.is_valid() and add_photo_to_galery_form.is_valid():
                current_though_banner = through_background_banner_form.save(commit = False)
                photo =  add_photo_to_galery_form.save()
                try:
                    current_though_banner.background = photo
                    current_though_banner.save()
                except:
                    current_though_banner.background = None
                    current_though_banner.background_type = 'simple_photo'
                return redirect(request.path)

        else:
            through_background_banner_form = ThroughBackroundBannerForm(instance = through_background_banner, prefix='through_banner')
            add_photo_to_galery_form = AddPhotoToGalleryForm(instance = through_background_banner.background, prefix='photo_through_banner')
        # promo and news banner logic

        if "btnform3" in request.POST:
            print('валидация третьего баннера')
            if banner_promotions_and_news_form.is_valid() and add_bannee_promo_cell_formset.is_valid():
                
                banner_promotions_and_news_form.save()
                add_bannee_promo_cell_formset.save()
                return redirect(request.path)
        else:
            banner_promotions_and_news_form = BannerPromotionsAndNewsForm(instance = banner_promotion_and_news, prefix='banner_promotion_and_news')
            add_bannee_promo_cell_formset = AddBannerPromoFormset(queryset=BannerCell.objects.filter(purpose='banner_news_and_promotions').all())

        
    else:
        # highest banner form
        highest_banner_form = HighestBannerForm(instance = my_banner, prefix='highest_banner')      
        add_banner_cell_formset = AddBannerCellFormSet(queryset=BannerCell.objects.filter(purpose='highest_banner').all())

        # through background banner form 
        through_background_banner_form = ThroughBackroundBannerForm(instance = through_background_banner)
        add_photo_to_galery_form = AddPhotoToGalleryForm(instance = through_background_banner.background)

        # banner with promotions and news
        banner_promotions_and_news_form = BannerPromotionsAndNewsForm(instance = banner_promotion_and_news, prefix='banner_promotion_and_news')
        add_bannee_promo_cell_formset = AddBannerPromoFormset(queryset=BannerCell.objects.filter(purpose='banner_news_and_promotions').all())


    context = {'highest_banner_form': highest_banner_form,
                'add_banner_cell_formset': add_banner_cell_formset,

                'through_background_banner_form': through_background_banner_form,
                'add_photo_to_galery_form': add_photo_to_galery_form,

                'banner_promotions_and_news_form': banner_promotions_and_news_form,
                'add_bannee_promo_cell_formset': add_bannee_promo_cell_formset,
                }

    return render(request, 'cinema/add_banners.html', context)


# Movie logic***********************************************************************************************************
@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_movies(request):
    all_films = Movie.objects.all()
    context = {'all_films': all_films}
    
    return render(request, 'cinema/all_movies.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def movie_detail(request, pk=None):
  
    movie_instance = get_object_or_404(Movie, pk=pk)
    MovieImageFormset = forms.modelformset_factory(Galery, form = MovieGaleryImageForm,
                                                        can_delete=True, extra=0, min_num=1,
                                                        max_num=5)

    if request.method == 'POST':
        movie_main_form = MovieForm(request.POST, instance = movie_instance, error_class=SimpleTextErrorList)
        movie_main_image_form = MovieMainImage(request.POST, request.FILES, instance = movie_instance.main_image)
        movie_image_formset = MovieImageFormset(request.POST, request.FILES, queryset = movie_instance.image_galery.all())
        movie_seo_block = SeoBlockForm(request.POST, instance=movie_instance.seo_block)


        if movie_main_form.is_valid() == False:
            print(movie_main_form.errors.as_text())
            messages.error(request, f'{movie_main_form.errors.as_text()}')
        elif movie_main_image_form.is_valid() == False:
            print(movie_main_image_form.errors.as_text())
            messages.error(request, f'{movie_main_image_form.errors.as_text()}')
        elif movie_image_formset.is_valid() == False:
            print(movie_main_image_form.errors.as_text())
            messages.error(request, f'{movie_main_image_form.errors.as_text()}')
        elif movie_seo_block.is_valid() == False:
            print(movie_seo_block.errors.as_text())
            messages.error(request, f'{movie_seo_block.errors.as_text()}')

        if movie_main_form.is_valid() and movie_main_image_form.is_valid() and movie_image_formset.is_valid() and movie_seo_block.is_valid():
            movie = movie_main_form.save(commit=False)
         
            try:
                main_image = movie_main_image_form.save() 
                movie.main_image = main_image
            except:
                movie.main_image = None


            movie_image_formset.save()
            for movie_image_form in movie_image_formset:
                if movie_image_form.instance.id != None:
                    movie.image_galery.add(movie_image_form.instance.id)

            seo = movie_seo_block.save()
            movie.seo_block = seo
            movie.save()
            messages.success(request, f'Сторінка фільму {movie.title_movie} успішно відредагована.')
            return redirect('cinema:all_movies')
        # else:
            # messages.error(request, errors)
            

    else:
        movie_main_form = MovieForm(instance = movie_instance, error_class=SimpleTextErrorList)
        movie_main_image_form = MovieMainImage(instance = movie_instance.main_image)
        movie_image_formset = MovieImageFormset(queryset = movie_instance.image_galery.all())
        movie_seo_block = SeoBlockForm(instance=movie_instance.seo_block)

    context = {'movie_main_form': movie_main_form, 
                'movie_image_formset': movie_image_formset,
                'movie_main_image_form': movie_main_image_form,
                'movie_seo_block': movie_seo_block}

    return render(request, 'cinema/movie_detail.html', context)



@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def new_movie(request):
    MovieImageFormset = forms.modelformset_factory(Galery, form = MovieGaleryImageForm,
                                                        can_delete=True, extra=0, min_num=1,
                                                        max_num=5)

    if request.method == 'POST':
        movie_main_form = MovieForm(request.POST, error_class=SimpleTextErrorList)
        movie_main_image_form = MovieMainImage(request.POST, request.FILES)
        movie_image_formset = MovieImageFormset(request.POST, request.FILES)
        movie_seo_block = SeoBlockForm(request.POST)


        if movie_main_form.is_valid() and movie_main_image_form.is_valid() and movie_image_formset.is_valid() and movie_seo_block.is_valid():
            movie = Movie()
            movie = movie_main_form.save(commit=False)
         
            try:
                main_image = movie_main_image_form.save() 
                movie.main_image = main_image
            except:
                movie.main_image = None


            movie_image_formset.save(commit=False)
            for movie_image_form in movie_image_formset:
                if movie_image_form.instance.id != None:
                    movie.image_galery.add(movie_image_form.instance.id)

            seo = movie_seo_block.save()
            movie.seo_block = seo
            movie.save()
            messages.success(request, f'Сторінка фільму {movie.title_movie} створена.')
            return redirect('cinema:all_movies')
        else:
            print(movie_main_form.errors, movie_main_image_form.errors, movie_image_formset.errors, movie_seo_block.errors)

    else:
        movie_main_form = MovieForm(error_class=SimpleTextErrorList)
        movie_main_image_form = MovieMainImage()
        movie_image_formset = MovieImageFormset(queryset = Galery.objects.none())
        movie_seo_block = SeoBlockForm()

    context = {'movie_main_form': movie_main_form, 
                'movie_image_formset': movie_image_formset,
                'movie_main_image_form': movie_main_image_form,
                'movie_seo_block': movie_seo_block}

    return render(request, 'cinema/new_movie.html', context)

@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def del_movie(request, pk):
    movie = Movie.objects.get(id=pk)
    movie_name = str(movie.title_movie)
    movie.delete()
    messages.success(request, f'Сторінка фільму {movie_name} видалена')
    return redirect('cinema:all_movies')


# Cinema logic***********************************************************************************************************
@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_cinemas(request):
    cinemas = Cinema.objects.all()
    context = {'all_cinemas': cinemas}
    return render(request, 'cinema/all_cinemas.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def cinema_detail(request, pk=None):
    cinema_instance = get_object_or_404(Cinema, pk=pk)
    MovieImageFormset = forms.modelformset_factory(Galery, form = MovieGaleryImageForm,
                                                    can_delete=True, extra=0, min_num=1,
                                                    max_num=5)
    cinema_hall = CinemaHall.objects.filter(cinema = cinema_instance.id)

    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, instance=cinema_instance, prefix="cinema_base_form")
        cinema_logo_form = MovieMainImage(request.POST, request.FILES, instance = cinema_instance.logo, prefix="cinema_logo_form")
        cinema_highest_banner_form = MovieMainImage(request.POST, request.FILES, instance = cinema_instance.image_top_banner, prefix="cinema_highest_banner")
        cinema_image_formset = MovieImageFormset(request.POST, request.FILES, queryset = cinema_instance.image_galery.all())
        cinema_seo_block = SeoBlockForm(request.POST, instance=cinema_instance.seo_block, prefix="cinema_seo_form")

        if cinema_form.is_valid() and cinema_logo_form.is_valid() and cinema_highest_banner_form.is_valid() and cinema_image_formset.is_valid() and cinema_seo_block.is_valid():
            # main form
            cinema = cinema_form.save(commit=False)
            # logo form
            try:
                logo = cinema_logo_form.save() 
                cinema.logo = logo
            except:
                cinema.logo = None

            # highest banner form
            try:
                highest_banner = cinema_highest_banner_form.save() 
                cinema.image_top_banner = highest_banner
            except:
                cinema.image_top_banner = None

            # galery formset
            cinema_image_formset.save()
            for movie_image_form in cinema_image_formset:
                if movie_image_form.instance.id != None:
                    cinema.image_galery.add(movie_image_form.instance.id)

            # seo form
            seo = cinema_seo_block.save()
            cinema.seo_block = seo

            # final save
            cinema.save()
            return redirect("cinema:all_cinemas")
        else:
            print(f'{cinema_form.errors}, {cinema_logo_form.errors}, {cinema_highest_banner_form.errors}, {cinema_image_formset.errors}, {cinema_seo_block.errors}')

    else:
        cinema_form = CinemaForm(instance=cinema_instance, prefix="cinema_base_form")
        cinema_logo_form = MovieMainImage(instance = cinema_instance.logo, prefix="cinema_logo_form")
        cinema_highest_banner_form = MovieMainImage(instance = cinema_instance.image_top_banner, prefix="cinema_highest_banner")
        cinema_image_formset = MovieImageFormset(queryset = cinema_instance.image_galery.all())
        cinema_seo_block = SeoBlockForm(instance=cinema_instance.seo_block, prefix="cinema_seo_form")

    context = {'cinema_form': cinema_form,
                'cinema_logo_form': cinema_logo_form,
                'cinema_highest_banner_form': cinema_highest_banner_form,
                'cinema_image_formset': cinema_image_formset,
                'cinema_hall': cinema_hall,
                'cinema_seo_block': cinema_seo_block}

    return render(request, 'cinema/cinema_detail.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def new_cinema(request):
    MovieImageFormset = forms.modelformset_factory(Galery, form = MovieGaleryImageForm,
                                                    can_delete=True, extra=0, min_num=1,
                                                    max_num=5)

    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, prefix="cinema_base_form")
        cinema_logo_form = MovieMainImage(request.POST, request.FILES, prefix="cinema_logo_form")
        cinema_highest_banner_form = MovieMainImage(request.POST, request.FILES, prefix="cinema_highest_banner")
        cinema_image_formset = MovieImageFormset(request.POST, request.FILES)
        cinema_seo_block = SeoBlockForm(request.POST, prefix="cinema_seo_form")

        if cinema_form.is_valid() and cinema_logo_form.is_valid() and cinema_highest_banner_form.is_valid() and cinema_image_formset.is_valid() and cinema_seo_block.is_valid():
            # main form
            cinema = cinema_form.save(commit=False)
            # logo form
            try:
                logo = cinema_logo_form.save() 
                cinema.logo = logo
            except:
                cinema.logo = None

            # highest banner form
            try:
                highest_banner = cinema_highest_banner_form.save() 
                cinema.image_top_banner = highest_banner
            except:
                cinema.image_top_banner = None

            # galery formset
            cinema_image_formset.save()
            for movie_image_form in cinema_image_formset:
                if movie_image_form.instance.id != None:
                    cinema.image_galery.add(movie_image_form.instance.id)

            # seo form
            seo = cinema_seo_block.save()
            cinema.seo_block = seo

            # final save
            cinema.save()
            return redirect('cinema:all_cinemas')


    else:
        cinema_form = CinemaForm(prefix="cinema_base_form")
        cinema_logo_form = MovieMainImage(prefix="cinema_logo_form")
        cinema_highest_banner_form = MovieMainImage(prefix="cinema_highest_banner")
        cinema_image_formset = MovieImageFormset(queryset = Galery.objects.none())
        cinema_seo_block = SeoBlockForm(prefix="cinema_seo_form")

    context = {'cinema_form': cinema_form,
                'cinema_logo_form': cinema_logo_form,
                'cinema_highest_banner_form': cinema_highest_banner_form,
                'cinema_image_formset': cinema_image_formset,
                'cinema_seo_block': cinema_seo_block}

    return render(request, 'cinema/new_cinema.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def del_cinema(request, pk):
    cinema = Cinema.objects.get(id=pk)
    cinema.delete()
    return redirect('cinema:all_cinemas')


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def cinema_hall_detail(request, pk):
    
    cinema_hall = get_object_or_404(CinemaHall, pk=pk)

    CinemaHallImageFormset = forms.modelformset_factory(Galery, form = MovieGaleryImageForm,
                                                    can_delete=True, extra=0, min_num=1,
                                                    max_num=5)

    if request.method == 'POST':

        cinema_hall_form = CinemaHallForm(request.POST, instance=cinema_hall, prefix="cinema_hall_base_form")
        cinema_hall_banner_form = MovieMainImage(request.POST, request.FILES, instance = cinema_hall.image_top_banner, prefix="cinema_hall_highest_banner")
        cinema_hall_image_formset = CinemaHallImageFormset(request.POST, request.FILES, queryset = cinema_hall.image_galery.all())
        cinema_hall_seo_block = SeoBlockForm(request.POST, instance=cinema_hall.seo_block, prefix="cinema_hall_seo_form")

        if cinema_hall_form.is_valid() and cinema_hall_banner_form.is_valid() and cinema_hall_image_formset.is_valid() and cinema_hall_seo_block.is_valid():
            # main form
            
            cinema_hall = cinema_hall_form.save(commit=False)
            
            # highest banner form
            try:
                highest_banner = cinema_hall_banner_form.save() 
                cinema_hall_banner_form.image_top_banner = highest_banner
            except:
                cinema_hall_banner_form.image_top_banner = None

            # galery formset
            cinema_hall_image_formset.save()
            for cinema_hall_image_form in cinema_hall_image_formset:
                if cinema_hall_image_form.instance.id != None:
                    cinema_hall.image_galery.add(cinema_hall_image_form.instance.id)

            # seo form
            seo = cinema_hall_seo_block.save()
            cinema_hall.seo_block = seo

            # final save
            cinema_hall.save()
            return redirect(request.path)
        else:
            print(f'{cinema_hall_form.errors}, {cinema_hall_banner_form.errors}, {cinema_hall_image_formset.errors}, {cinema_hall_seo_block.errors}')
    else:
        cinema_hall_form = CinemaHallForm(instance=cinema_hall, prefix="cinema_hall_base_form")
        cinema_hall_banner_form = MovieMainImage(instance = cinema_hall.image_top_banner, prefix="cinema_hall_highest_banner")
        cinema_hall_image_formset = CinemaHallImageFormset(queryset = cinema_hall.image_galery.all())
        cinema_hall_seo_block = SeoBlockForm(instance=cinema_hall.seo_block, prefix="cinema_hall_seo_form")

    context = {'cinema_hall_form': cinema_hall_form,
                'cinema_hall_banner_form': cinema_hall_banner_form,
                'cinema_hall_image_formset': cinema_hall_image_formset,
                'cinema_hall_seo_block': cinema_hall_seo_block}

    return render(request, 'cinema/cinema_hall_detail.html', context)



@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def del_cinema_hall(request, pk, cinema_id):
    hall = CinemaHall.objects.get(id=pk)
    hall.delete()
    return redirect('cinema:cinema_detail', pk=cinema_id)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def new_cinema_hall(request, cinema_id):
    CinemaHallImageFormset = forms.modelformset_factory(Galery, form = MovieGaleryImageForm,
                                                    can_delete=True, extra=0, min_num=1,
                                                    max_num=5)
    current_cinema = Cinema.objects.get(id=cinema_id)

    if request.method == 'POST':

        cinema_hall_form = CinemaHallForm(request.POST, prefix="cinema_hall_base_form")
        cinema_hall_banner_form = MovieMainImage(request.POST, request.FILES, prefix="cinema_hall_highest_banner")
        cinema_hall_image_formset = CinemaHallImageFormset(request.POST, request.FILES, queryset = Galery.objects.none())
        cinema_hall_seo_block = SeoBlockForm(request.POST, prefix="cinema_hall_seo_form")

        if cinema_hall_form.is_valid() and cinema_hall_banner_form.is_valid() and cinema_hall_image_formset.is_valid() and cinema_hall_seo_block.is_valid():
            # main form
            
            cinema_hall = cinema_hall_form.save(commit=False)
            
            # highest banner form
            try:
                highest_banner = cinema_hall_banner_form.save() 
                cinema_hall_banner_form.image_top_banner = highest_banner
            except:
                cinema_hall_banner_form.image_top_banner = None

            # galery formset
            cinema_hall_image_formset.save()
            for cinema_hall_image_form in cinema_hall_image_formset:
                if cinema_hall_image_form.instance.id != None:
                    cinema_hall.image_galery.add(cinema_hall_image_form.instance.id)

            # seo form
            seo = cinema_hall_seo_block.save()
            cinema_hall.seo_block = seo

            # final save
            cinema_hall.cinema = current_cinema
            cinema_hall.save()
            return redirect('cinema:cinema_detail', pk=current_cinema.id)
    else:
        cinema_hall_form = CinemaHallForm(prefix="cinema_hall_base_form")
        cinema_hall_banner_form = MovieMainImage(prefix="cinema_hall_highest_banner")
        cinema_hall_image_formset = CinemaHallImageFormset(queryset = Galery.objects.none())
        cinema_hall_seo_block = SeoBlockForm(prefix="cinema_hall_seo_form")

    context = {'cinema_hall_form': cinema_hall_form,
                'cinema_hall_banner_form': cinema_hall_banner_form,
                'cinema_hall_image_formset': cinema_hall_image_formset,
                'cinema_hall_seo_block': cinema_hall_seo_block}

    return render(request, 'cinema/new_cinema_hall.html', context)

