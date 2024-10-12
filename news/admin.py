from django.contrib import admin
from .models import Category, News
from .models import User
from django.contrib.admin import RelatedOnlyFieldListFilter
from .models import Subtitle



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'status')
    list_filter = ('status', ('parent_category', RelatedOnlyFieldListFilter))
    search_fields = ('name', 'parent_category__name')

    fieldsets = (
        (None, {
            'fields': ('name', 'parent_category', 'status')
        }),
    )

admin.site.register(Category, CategoryAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'date')
    search_fields = ('title', 'keywords')
    list_filter = ('category', 'status', 'date')

admin.site.register(News, NewsAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'role', 'status')  # اصلاح فیلدهای موجود در list_display
    search_fields = ('name', 'phone_number')
    list_filter = ('role', 'status')

    
admin.site.register(User, UserAdmin)

class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'operation')  # فیلدهایی که در لیست نمایش داده می‌شوند
    search_fields = ('title',)  # فیلدهایی که برای جستجو استفاده می‌شوند
    list_filter = ('date',)  # فیلدهایی که برای فیلتر استفاده می‌شوند
    list_per_page = 10  # تعداد ردیف‌ها در هر صفحه

    def operation(self, obj):
        return f'ویرایش | حذف'  # عمل ویرایش و حذف

    operation.short_description = 'عملیات'

admin.site.register(Subtitle, SubtitleAdmin)