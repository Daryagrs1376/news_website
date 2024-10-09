from django.contrib import admin
from .models import Category, News
from .models import User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory_name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)

admin.site.register(Category, CategoryAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'date')
    search_fields = ('title', 'keywords')
    list_filter = ('category', 'status', 'date')

admin.site.register(News, NewsAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'role', 'status')
    search_fields = ('name', 'phone_number')
    list_filter = ('role', 'status')

    
admin.site.register(User, UserAdmin)
