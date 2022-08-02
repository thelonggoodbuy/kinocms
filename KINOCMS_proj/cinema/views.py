from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render


from users.models import CustomUser
from .forms import SearchUserForm




def all_users(request):
    users_list = CustomUser.objects.filter(is_active=True, is_superuser=False)
    # if 'keyword' in request.GET:
    #     keyword = request.GET['keyword']
    #     q = Q(name__icontains=keyword) | Q(email__icontains=keyword)
    #     users_list = users_list.filter(q)
    # else:
    #     keyword = ''
    # search_form = SearchUserForm(initial={'keyword':keyword})
    paginator = Paginator(users_list, 5)
    if 'page' in request.GET:
        page_num = request.GET['page']    
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    # context = {'page': page, 'users_list': users_list, 'form': search_form}
    context = {'page': page, 'users_list': page.object_list}
    
    
    return render(request, 'cinema/all_users.html', context)