from django.contrib import admin
from .models import *



admin.site.register(CustomPages)
admin.site.register(Contact)
admin.site.register(MainPage)
admin.site.register(NewsAndPromotions)

class PhonesAdmin(admin.ModelAdmin):
    list_display = ('page', 'number')
admin.site.register(Phones, PhonesAdmin)