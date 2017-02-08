from django.contrib import admin

# Register your models here.
from models import Advert, Category, SubCategory


admin.site.register(Category)
admin.site.register(SubCategory)


class AdvertAdmin(admin.ModelAdmin):
    list_display = ('header', 'owner', 'is_moderated', 'is_active', 'is_sold', 'is_best')
    list_editable = ('is_moderated', 'is_active', 'is_sold', 'is_best')
    search_fields = ('header', 'text', 'owner')
    list_filter = ('is_moderated', 'is_active', 'is_sold', 'is_best')

admin.site.register(Advert, AdvertAdmin)