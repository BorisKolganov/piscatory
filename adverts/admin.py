from django.contrib import admin

# Register your models here.
from models import Advert, Category, SubCategory

admin.site.register(Advert)
admin.site.register(Category)
admin.site.register(SubCategory)