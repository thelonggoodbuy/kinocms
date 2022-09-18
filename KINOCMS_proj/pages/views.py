from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from django.shortcuts import redirect



from .models import NewsAndPromotions
from cinema.models import SeoBlock
# from .views import GaleryImageForm
from .forms import SimpleTextErrorList, NewsForm, MainImage, GaleryImageForm, SeoBlockForm

from cinema.models import Galery



def index(request):
    return render(request, 'pages/main.html') 

@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def all_news(request):

    news = NewsAndPromotions.objects.filter(publ_type='news')
    context = {'news': news}
    return render(request, 'pages/all_news.html', context)


@login_required
@user_passes_test(lambda admin: admin.is_superuser)
def news_detail(request, pk):  
    # one_news = get_object_or_404(NewsAndPromotions, pk=pk)
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