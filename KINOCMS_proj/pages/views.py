from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from django.shortcuts import redirect
import datetime
from datetime import timedelta
from django.utils.datetime_safe import datetime
import json
from django.core import serializers
from django.contrib import messages
from itertools import chain
from datetime import date
from django.db.models import Q
from django.http import JsonResponse
from dateutil.rrule import rrule, DAILY

from .models import NewsAndPromotions, CustomPages, MainPage, Phones, Contact, ContactCell
from cinema.models import SeoBlock, Show
# from .views import GaleryImageForm
from .forms import SimpleTextErrorList, NewsForm, MainImage, GaleryImageForm, SeoBlockForm, CustomPageForm, MainPageForm, PhoneForm, ContactCellForm

from cinema.models import Galery, Show, Movie, HighestBannerWithTimeScrolling, BannerCell, BannerPromotionsAndNews, ThroughBackroundBanner, Cinema, CinemaHall
from users.models import DevicesStatisticCounter, CustomUser, Ticket


# ************************************************************************
# frontend data 
# ************************************************************************
# main page
def main_page(request):
    today_shows = Show.objects.filter(date_show = date.today()).distinct('movie')
    announced_date_start = date.today()
    announced_date_finish = date.today() + timedelta(days=30)
    next_month_announced = Movie.objects.filter(movie_distribution_start__range=(announced_date_start, announced_date_finish))
    highest_banner = HighestBannerWithTimeScrolling.objects.all()[0]
    top_bannest_cells = BannerCell.objects.filter(purpose="highest_banner")
    highest_banner_timescrolling = highest_banner.timescrolling*1000
    banner_promo_and_news = BannerPromotionsAndNews.objects.all()[0]
    promo_and_news_bannercells = BannerCell.objects.filter(purpose="banner_news_and_promotions")
    banner_promo_and_news_timescrolling = banner_promo_and_news.timescrolling*1000
    though_background = ThroughBackroundBanner.objects.all()[0]
    print(though_background.background.image.url)

    today_date = date.today()
    context = {'today_shows': today_shows,
                'today_date': today_date,
                'next_month_announced': next_month_announced,
                'highest_banner': highest_banner,
                'top_bannest_cells': top_bannest_cells,
                'highest_banner_timescrolling': highest_banner_timescrolling,
                'banner_promo_and_news': banner_promo_and_news,
                'promo_and_news_bannercells': promo_and_news_bannercells,
                'banner_promo_and_news_timescrolling': banner_promo_and_news_timescrolling,
                'though_background': though_background,
                }
    
    return render(request, 'pages/main.html', context) 

# cinema and halls data
def all_cinemas(request):
    cinema_list = Cinema.objects.all()
    context = {'cinema_list': cinema_list}
    return render(request, 'pages/all_cinemas.html', context)


def about_cinema(request, pk):
    cinema = Cinema.objects.get(id=pk)
    cinema_halles = CinemaHall.objects.filter(cinema=cinema)
    today_show_filter = Q(cinema_hall__in = cinema_halles) & Q(date_show = date.today())
    today_show = Show.objects.filter(today_show_filter)
    # print(today_show)
    context = {'cinema': cinema,
                'cinema_halles': cinema_halles,
                'today_show': today_show}
    return render(request, 'pages/about_cinema.html', context)


def front_all_promo(request):
    actual_promo = Q(publ_type = 'promotion') & Q(is_active = True)
    all_promo = NewsAndPromotions.objects.filter(actual_promo)
    context = {
        'all_promo': all_promo
    }
    return render(request, 'pages/front_all_promo.html', context)

def front_promo_detail(request, pk):
    promo = NewsAndPromotions.objects.get(id=pk)
    context = {'promo': promo}
    return render(request, 'pages/front_promo_detail.html', context)


def front_schedule(request):
    start_date = datetime.now().date()
    finish_date = datetime.now().date() + timedelta(days=7)

    # datetime.now().date()- timedelta(days=27)

    # print(start_date, finish_date)
    seanses = Show.objects.filter(date_show__range=[start_date, finish_date]).order_by('time_show')

    date_of_seanses = set()
    for seanse in seanses:
        date_of_seanses.add(seanse.date_show)
    print(date_of_seanses)

    # data_list = []
    # for date_seance in range(start_date, finish_date):
    #     print(date_seance)

    # print(data_list)

    cinemas = Cinema.objects.all()
    cinema_halles = CinemaHall.objects.all()
    context = {'seanses': seanses, 
                'cinemas': cinemas,
                'cinema_halles': cinema_halles}
    return render(request, 'pages/front_schedule.html', context)


def schedule_sort_cinema(request):
    cinema_name = request.GET.get('title_cinema', None)
    cinema_hall_test = CinemaHall.objects.filter(cinema=Cinema.objects.get(title_cinema = cinema_name))
    seanses_filter = Q(date_show=date.today()) & Q(cinema_hall__in=cinema_hall_test)
    cinema_shows = Show.objects.filter(seanses_filter).order_by('time_show')
    shows = [show.id for show in cinema_shows]

    data = {
        'this_film_seanses': shows
    }
    return JsonResponse(data)

def schedule_sort_cinema_hall(request):
    hall_name = request.GET.get('cinema_hall_name')
    cinema_hall = CinemaHall.objects.filter(cinema_hall_name=hall_name)
    seanses_filteret_by_cinema_hall = Show.objects.filter(cinema_hall__in=cinema_hall)#.order_by('time_show')
    show_filtered_id = [show.id for show in seanses_filteret_by_cinema_hall]
    data = {
        'show_filtered_id': show_filtered_id
    }
    print(f'data from view: {data}')
    return JsonResponse(data)

# ************************************************************************
# CMS data
# ************************************************************************
# news
@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_news(request):

    news = NewsAndPromotions.objects.filter(publ_type='news')
    context = {'news': news}
    return render(request, 'pages/all_news.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def news_detail(request, pk):  
    one_news = NewsAndPromotions.objects.select_related('main_image', 'seo_block').prefetch_related('image_galery').get(pk=pk)
    NewsHallImageFormset = forms.modelformset_factory(Galery, form = GaleryImageForm,
                                                    can_delete=True, extra=0, min_num=1,
                                                    max_num=5)
    if request.method == 'POST':
        one_news_form = NewsForm(request.POST, instance=one_news, prefix="pages_news_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(request.POST, request.FILES, instance = one_news.main_image, prefix="pages_news_main_image", error_class=SimpleTextErrorList)
        one_news_image_formset = NewsHallImageFormset(request.POST, request.FILES, queryset = one_news.image_galery.all())
        one_news_seo_block = SeoBlockForm(request.POST, instance=one_news.seo_block, prefix="pages_news_seo_form", error_class=SimpleTextErrorList)

 
        if one_news_form.is_valid() and main_image_form.is_valid() and one_news_image_formset.is_valid() and one_news_seo_block.is_valid():
            # main form
            one_news_form = one_news_form.save(commit=False)
            # main image form
            try:
                highest_banner = main_image_form.save() 
                one_news.main_image = highest_banner
            except:
                  one_news.main_image = None

            # galery formset
            one_news_image_formset.save()
            for image_form in one_news_image_formset:
                if image_form.instance.id != None:
                    one_news.image_galery.add(image_form.instance.id)

            # seo form
            seo = one_news_seo_block.save()
            one_news.seo_block = seo

            # final save
            one_news_form.save()
            return redirect('pages:all_news')
        else:
            print(f'{one_news_form.errors}, {main_image_form.errors}, {one_news_image_formset.errors}, {one_news_seo_block.errors}')
    else:
        one_news_form = NewsForm(instance=one_news, prefix="pages_news_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(instance = one_news.main_image, prefix="pages_news_main_image", error_class=SimpleTextErrorList)
        one_news_image_formset = NewsHallImageFormset(queryset = one_news.image_galery.all())
        one_news_seo_block = SeoBlockForm(instance=one_news.seo_block, prefix="pages_news_seo_form", error_class=SimpleTextErrorList)

    context = {'one_news_form': one_news_form,
                'main_image_form': main_image_form,
                'one_news_image_formset': one_news_image_formset,
                'one_news_seo_block': one_news_seo_block}

    return render(request, 'pages/news_detail.html', context)




@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def create_news(request):
    
    NewsHallImageFormset = forms.modelformset_factory(Galery, form = GaleryImageForm,
                                                        can_delete=True, extra=0, min_num=1,
                                                         max_num=5)   

    if request.method == 'POST':

        one_news_form = NewsForm(request.POST, prefix="pages_news_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(request.POST, request.FILES, prefix="pages_news_main_image", error_class=SimpleTextErrorList)
        one_news_image_formset = NewsHallImageFormset(request.POST, request.FILES)
        one_news_seo_block = SeoBlockForm(request.POST, prefix="pages_news_seo_form", error_class=SimpleTextErrorList)

        if one_news_form.is_valid() and main_image_form.is_valid() and one_news_image_formset.is_valid() and one_news_seo_block.is_valid():
            
            one_news = NewsAndPromotions()
            one_news = one_news_form.save(commit=False)
            try:
                highest_banner = main_image_form.save() 
                 
                one_news.main_image = highest_banner
            except:
                  one_news.main_image = None

            # galery formset
            one_news_image_formset.save(commit=False)
            for image_form in one_news_image_formset:
                if image_form.instance.id != None:
                    one_news.image_galery.add(image_form.instance.id)

            # seo form
            seo = one_news_seo_block.save()
            one_news.seo_block = seo

            # final save
            # one_news.is_active = 'on'
            one_news.publ_type = 'news'
            one_news.save()
            
            return redirect('pages:all_news')

    else:
        one_news_form = NewsForm(prefix="pages_news_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(prefix="pages_news_main_image", error_class=SimpleTextErrorList)
        one_news_image_formset = NewsHallImageFormset(queryset = Galery.objects.none())
        one_news_seo_block = SeoBlockForm(prefix="pages_news_seo_form", error_class=SimpleTextErrorList)

    context = {'one_news_form': one_news_form,
                'main_image_form': main_image_form,
                'one_news_image_formset': one_news_image_formset,
                'one_news_seo_block': one_news_seo_block}

    return render(request, 'pages/create_news.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def del_news(request, pk):

    news = NewsAndPromotions.objects.get(id=pk)
    news.delete()
    return redirect('pages:all_news')




# promo
@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_promo(request):

    promo = NewsAndPromotions.objects.filter(publ_type='promotion')
    context = {'promo': promo}
    return render(request, 'pages/all_promo.html', context)



@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def create_promo(request):
    
    PromoImageFormset = forms.modelformset_factory(Galery, form = GaleryImageForm,
                                                        can_delete=True, extra=0, min_num=1,
                                                         max_num=5)   

    if request.method == 'POST':

        one_promo_form = NewsForm(request.POST, prefix="pages_promo_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(request.POST, request.FILES, prefix="pages_promo_main_image", error_class=SimpleTextErrorList)
        one_promo_image_formset = PromoImageFormset(request.POST, request.FILES)
        one_promo_seo_block = SeoBlockForm(request.POST, prefix="pages_promo_seo_form", error_class=SimpleTextErrorList)

        if one_promo_form.is_valid() and main_image_form.is_valid() and one_promo_image_formset.is_valid() and one_promo_seo_block.is_valid():
            
            one_news = NewsAndPromotions()
            one_news = one_promo_form.save(commit=False)
            try:
                highest_banner = main_image_form.save() 
                 
                one_news.main_image = highest_banner
            except:
                  one_news.main_image = None

            # galery formset
            one_promo_image_formset.save(commit=False)
            for image_form in one_promo_image_formset:
                if image_form.instance.id != None:
                    one_news.image_galery.add(image_form.instance.id)

            # seo form
            seo = one_promo_seo_block.save()
            one_news.seo_block = seo

            # final save
            one_news.publ_type = 'promotion'
            one_news.save()
            
            return redirect('pages:all_promo')

    else:
        one_promo_form = NewsForm(prefix="pages_promo_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(prefix="pages_promo_main_image", error_class=SimpleTextErrorList)
        one_promo_image_formset = PromoImageFormset(queryset = Galery.objects.none())
        one_promo_seo_block = SeoBlockForm(prefix="pages_promo_seo_form", error_class=SimpleTextErrorList)

    context = {'one_promo_form': one_promo_form,
                'main_image_form': main_image_form,
                'one_promo_image_formset': one_promo_image_formset,
                'one_promo_seo_block': one_promo_seo_block}

    return render(request, 'pages/create_promo.html', context)






@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def promo_detail(request, pk):
    
    one_promo = NewsAndPromotions.objects.select_related('main_image', 'seo_block').prefetch_related('image_galery').get(pk=pk)
    NewsHallImageFormset = forms.modelformset_factory(Galery, form = GaleryImageForm,
                                                    can_delete=True, extra=0, min_num=1,
                                                    max_num=5)
    if request.method == 'POST':
        one_promo_form = NewsForm(request.POST, instance=one_promo, prefix="pages_promo_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(request.POST, request.FILES, instance = one_promo.main_image, prefix="pages_promo_main_image", error_class=SimpleTextErrorList)
        one_promo_image_formset = NewsHallImageFormset(request.POST, request.FILES, queryset = one_promo.image_galery.all())
        one_promo_seo_block = SeoBlockForm(request.POST, instance=one_promo.seo_block, prefix="pages_promo_seo_form", error_class=SimpleTextErrorList)

 
        if one_promo_form.is_valid() and main_image_form.is_valid() and one_promo_image_formset.is_valid() and one_promo_seo_block.is_valid():
            # main form
            one_promo_form = one_promo_form.save(commit=False)
            # main image form
            try:
                highest_banner = main_image_form.save() 
                one_promo.main_image = highest_banner
            except:
                  one_promo.main_image = None

            # galery formset
            one_promo_image_formset.save()
            for image_form in one_promo_image_formset:
                if image_form.instance.id != None:
                    one_promo.image_galery.add(image_form.instance.id)

            # seo form
            seo = one_promo_seo_block.save()
            one_promo.seo_block = seo

            # final save
            one_promo_form.save()
            return redirect('pages:all_promo')
    else:
        one_promo_form = NewsForm(instance=one_promo, prefix="pages_promo_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(instance = one_promo.main_image, prefix="pages_promo_main_image", error_class=SimpleTextErrorList)
        one_promo_image_formset = NewsHallImageFormset(queryset = one_promo.image_galery.all())
        one_promo_seo_block = SeoBlockForm(instance=one_promo.seo_block, prefix="pages_promo_seo_form", error_class=SimpleTextErrorList)

    context = {'one_promo_form': one_promo_form,
                'main_image_form': main_image_form,
                'one_promo_image_formset': one_promo_image_formset,
                'one_promo_seo_block': one_promo_seo_block}

    return render(request, 'pages/promo_detail.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def promo_del(request, pk):
    promo = NewsAndPromotions.objects.get(id=pk)
    promo.delete()
    return redirect('pages:all_promo')



# custom page(for unified pages)

@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_pages(request):

    pages = CustomPages.objects.all()
    main_page = MainPage.objects.all()
    contact_page = Contact.objects.all()
    
    pages_list = sorted(
                chain(pages, main_page, contact_page),
                key=lambda page: page.is_active,
                reverse=True)

    context = {'pages_list': pages_list,
                'pages': pages}

    # print(context)
    return render(request, 'pages/all_pages.html', context)



@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def create_page(request):

    PageImageFormset = forms.modelformset_factory(Galery, form = GaleryImageForm,
                                                        can_delete=True, extra=0, min_num=1,
                                                         max_num=5)   


    if request.method == 'POST':

        page_form = CustomPageForm(request.POST, prefix="page_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(request.POST, request.FILES, prefix="page_main_image", error_class=SimpleTextErrorList)
        page_image_formset = PageImageFormset(request.POST, request.FILES)
        page_seo_block = SeoBlockForm(request.POST, prefix="page_seo_form", error_class=SimpleTextErrorList)

        if page_form.is_valid() and main_image_form.is_valid() and page_image_formset.is_valid() and page_seo_block.is_valid():
            
            page = CustomPages()
            page = page_form.save(commit=False)
            try:
                highest_banner = main_image_form.save() 
                 
                page.main_image = highest_banner
            except:
                  page.main_image = None

            # galery formset
            page_image_formset.save(commit=False)
            for image_form in page_image_formset:
                if image_form.instance.id != None:
                    page.image_galery.add(image_form.instance.id)

            # seo form
            seo = page_seo_block.save()
            page.seo_block = seo

            # final save
            # page.publ_type = 'promotion'

            page.save()
            
            return redirect('pages:all_pages')

    else:
        page_form = CustomPageForm(prefix="page_base_form", error_class=SimpleTextErrorList)
        main_image_form = MainImage(prefix="page_main_image", error_class=SimpleTextErrorList)
        page_image_formset = PageImageFormset(queryset = Galery.objects.none())
        page_seo_block = SeoBlockForm(prefix="page_seo_form", error_class=SimpleTextErrorList)

    context = {'page_form': page_form,
                'main_image_form': main_image_form,
                'page_image_formset': page_image_formset,
                'page_seo_block': page_seo_block}

    return render(request, 'pages/create_page.html', context)




@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def page_detail(request, pk):
     
    page = CustomPages.objects.select_related('main_image', 'seo_block')\
                                .prefetch_related('image_galery').get(pk=pk)

    PageImageFormset = forms.modelformset_factory(Galery,
                                                     form = GaleryImageForm,
                                                    can_delete=True, extra=0,
                                                     min_num=1, max_num=5)

    if request.method == 'POST':
        page_form = CustomPageForm(request.POST,
                    instance=page, prefix="page_base_form", 
                    error_class=SimpleTextErrorList)

        main_image_form = MainImage(request.POST, request.FILES, 
                    instance = page.main_image, prefix="page_main_image",
                    error_class=SimpleTextErrorList)

        page_image_formset = PageImageFormset(request.POST, request.FILES,
                    queryset = page.image_galery.all())

        page_seo_block = SeoBlockForm(request.POST, 
                    instance=page.seo_block, prefix="page_seo_form", 
                    error_class=SimpleTextErrorList)

 
        if page_form.is_valid() and main_image_form.is_valid()\
            and page_image_formset.is_valid() and page_seo_block.is_valid():
            # main form
            page = page_form.save(commit=False)
            # main image form
            try:
                highest_banner = main_image_form.save() 
                page.main_image = highest_banner
            except:
                  page.main_image = None

            # galery formset
            page_image_formset.save()
            for image_form in page_image_formset:
                if image_form.instance.id != None:
                    page.image_galery.add(image_form.instance.id)

            # seo form
            seo = page_seo_block.save()
            page.seo_block = seo

            # final save
            page.save()
            return redirect('pages:all_pages')
    else:

        page_form = CustomPageForm(instance=page, prefix="page_base_form",
                                    error_class=SimpleTextErrorList)

        main_image_form = MainImage(instance = page.main_image, prefix="page_main_image",
                                    error_class=SimpleTextErrorList)

        page_image_formset = PageImageFormset(queryset = page.image_galery.all())

        page_seo_block = SeoBlockForm(instance=page.seo_block, prefix="page_seo_form",
                                    error_class=SimpleTextErrorList)

    context = {'page_form': page_form,
                'main_image_form': main_image_form,
                'page_image_formset': page_image_formset,
                'page_seo_block': page_seo_block}

    return render(request, 'pages/page_detail.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def page_del(request, pk):
    page = CustomPages.objects.get(id=pk)
    page.delete()
    messages.success(request, 'Сторінка видалена.')
    return redirect('pages:all_pages')


# main mage
@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def main_page_detail(request, pk):

    main_page = MainPage.objects.select_related('seo_block').get(pk=pk)
    try:
        phones = Phones.objects.prefetch_related('page').get(pk=main_page.pk)
    except:
        pass

    PhoneFormset = forms.inlineformset_factory(MainPage, Phones, 
                                            form=PhoneForm, fk_name='page',
                                            extra=0, min_num=2, max_num=2)
    
    if request.method == "POST":
        main_page_form = MainPageForm(request.POST, instance=main_page, prefix="main_page_form")
        phone_formset = PhoneFormset(request.POST, instance=main_page)
        seo_form = SeoBlockForm(request.POST, 
                    instance=main_page.seo_block, prefix="main_page_seo_form", 
                    error_class=SimpleTextErrorList)

        if main_page_form.is_valid() and phone_formset.is_valid() and seo_form.is_valid():
            main_page = main_page_form.save(commit=False)

            phone_formset.save()

            seo = seo_form.save()
            main_page.seo_block = seo
            return redirect('pages:all_pages')


    else:
        print(Phones.objects.filter(page=main_page.id))
        main_page_form = MainPageForm(instance=main_page, prefix="main_page_form")
        phone_formset = PhoneFormset(instance=main_page)
        seo_form = SeoBlockForm(instance=main_page.seo_block, prefix="main_page_seo_form", 
                    error_class=SimpleTextErrorList)

    context = {'main_page_form': main_page_form,
                'phone_formset': phone_formset,
                'seo_form': seo_form}
    return render(request, 'pages/main_page_detail.html', context)

@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def contacts_detail(request, pk):
    contacts_page = Contact.objects.select_related('seo_block').get(pk=pk)

    exists_contacts = ContactCell.objects.all()

    ContactFormset = forms.modelformset_factory(ContactCell, 
                                            form=ContactCellForm,
                                            can_delete=True, extra=0, min_num=1)
    
    if request.method == "POST":
        contact_formset = ContactFormset(request.POST, request.FILES, queryset=exists_contacts)
        seo_form = SeoBlockForm(request.POST, 
                    instance=contacts_page.seo_block, 
                    error_class=SimpleTextErrorList)

        if contact_formset.is_valid() and seo_form.is_valid():
            contact_formset.save()
            seo = seo_form.save()
            contacts_page.seo_block = seo
            contacts_page.save()
            return redirect('pages:all_pages')

        else:
            print(request.POST)
            print(seo_form.errors)
            print(contact_formset.errors)
            print('ERROR!!!')

    else:
        contact_formset = ContactFormset(queryset=exists_contacts)
        seo_form = SeoBlockForm(instance=contacts_page.seo_block, 
                    error_class=SimpleTextErrorList)

    context = {'contacts_page': contacts_page,
                'contact_formset': contact_formset,
                'seo_form': seo_form}
    return render(request, 'pages/contacts_page_detail.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def statistics(request):


    # devices data
    device_rought_data = DevicesStatisticCounter.objects.filter(date__gte=(datetime.now().date() - timedelta(days=27)),
                                                                date__lte=datetime.now().date())
    shows_rought_data = Show.objects.filter(date_show__gte=(datetime.now().date() - timedelta(days=27)),
                                                                date_show__lte=datetime.now().date())
    tickets_rought_data = Ticket.objects.filter(show__in=shows_rought_data)
    
    date_labels_list=[]
    start_day = datetime.now().date()- timedelta(days=27)
    finish_day = datetime.now().date()
    actual_day = start_day
    day_counter = 0

    # date_label
    while actual_day <= finish_day:
        day_counter+=1
        if day_counter==1 or day_counter%8==0:
            date_labels_list.append(f'{actual_day.day} {actual_day.strftime("%b")}.')
        else:
            date_labels_list.append('')
        actual_day += timedelta(days=1)

    # devices statistics
    actual_day = start_day
    day_counter = 0
    tablet_and_sensor = []
    pc = []
    mobile = []
    sex={}
    # shows statistics
    shows_per_day=[]
    buy_per_day=[]
    book_per_day=[]
    # statistic_counter
    while actual_day <= finish_day:
        day_counter+=1
        try:
            visitors_with_tablet = device_rought_data.filter(device_type='tablet_and_other_sensor_devices').get(date=actual_day)
            tablet_and_sensor.append(visitors_with_tablet.number)
        except:
            tablet_and_sensor.append(0)
        try:
            visitors_pc = device_rought_data.filter(device_type='pc').get(date=actual_day)
            pc.append(visitors_pc.number)
        except:
            pc.append(0)
        try:
            visitors_mobile = device_rought_data.filter(device_type='mobile').get(date=actual_day)
            mobile.append(visitors_mobile.number)
        except:
            mobile.append(0)
        # shows statistics
        try:
            shows_this_day = shows_rought_data.filter(date_show=str(actual_day))
            shows_per_day.append(len(shows_this_day))
        except:
            shows_per_day.append(0)

        booking=0
        buyng=0
        shows_this_day = shows_rought_data.filter(date_show=str(actual_day))
        if shows_this_day.count()==0:
            buy_per_day.append(0)
            book_per_day.append(0)
        else:
            for show in shows_this_day:
                if show.total_booked != None:
                    booking+=show.total_booked
                    buyng+=show.total_bought
                else:
                    buy_per_day.append(0)
                    book_per_day.append(0)
            buy_per_day.append(buyng)
            book_per_day.append(booking)

        actual_day += timedelta(days=1)
    male = 0
    female = 0
    for ticket in tickets_rought_data:
        if ticket.user.sex=='male': male+=1
        if ticket.user.sex=='female': female+=1
    
    sex['чоловіча'] = male
    sex['жіноча'] = female
    all_devices = [sum(x) for x in zip(tablet_and_sensor, pc, mobile)]

    #  users statistics
    users = CustomUser.objects.filter(is_superuser=False, is_staff=False)
    users_counter = users.count()
    town_list = []
    # users city statistics
    city_list = users.values_list('town').distinct()
    [town_list.append(obj[0]) for obj in city_list]
    town_dict = {}
    for town in town_list:
        if town==None:
            town_dict['Не вказано'] = (users.filter(town=town)).count()
            continue
        town_dict[town] = (users.filter(town=town)).count()

    context = {'tablet_and_sensor': tablet_and_sensor,
                'date_labels_list': date_labels_list,
                'pc': pc,
                'mobile': mobile,
                'all_devices': all_devices,
                'shows_per_day': shows_per_day,
                'users_counter': users_counter,
                'town_dict': town_dict,
                'buy_per_day': buy_per_day,
                'book_per_day': book_per_day,
                'sex': sex}

    return render(request, 'pages/statistics.html', context)