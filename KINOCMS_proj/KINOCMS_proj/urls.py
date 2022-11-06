from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('', include('pages.urls')),
    path('cinema_cms/', include('cinema.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
