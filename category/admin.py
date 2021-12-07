# from django.contrib import admin
# from .models import Categories
from django.contrib import admin
from category.models import Products

# Register your models here.
# admin.site.register(Categories)
admin.site.register(Products)

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('category_name',)}
#     list_display = ('category_name','slug')
