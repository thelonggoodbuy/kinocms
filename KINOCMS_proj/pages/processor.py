from pages.models import CustomPages, MainPage, Contact, Phones
from itertools import chain




def list_of_active_pages(request):
    pages = CustomPages.objects.filter(is_active=True)
    main_page = MainPage.objects.filter(is_active=True)
    contact_page = Contact.objects.filter(is_active=True)

    pages_list = sorted(
                chain(pages, main_page, contact_page),
                key=lambda page: page.is_active,
                reverse=True)

    return {'active_pages_base_context': pages_list}

def list_of_phones(request):
    phones = Phones.objects.all()
    return {'list_of_phones': phones}
