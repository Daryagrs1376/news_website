from django.contrib import admin
from .models import News, Category, Subtitle, ReporterProfile, Keyword, SpecialFeature, SpecialCategory



# ثبت مدل News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'category', 'created_at', 'status')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'reporter__username', 'category__name', 'keywords__word')
    date_hierarchy = 'created_at'
    ordering = ['created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_category_display', 'status')
    list_filter = ('status', 'parent_category')

    # متدی برای نمایش نام دسته‌بندی والد در لیست نمایش
    def parent_category_display(self, obj):
        return obj.parent_category.title if obj.parent_category else '-'
    
    parent_category_display.short_description = 'Parent Category'
    

# ثبت مدل Keyword
@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ('word',)

# ثبت مدل SpecialFeature
@admin.register(SpecialFeature)
class SpecialFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name',)
    search_fields = ('feature_name',)

# ثبت مدل SpecialCategory
@admin.register(SpecialCategory)
class SpecialCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)

# ثبت مدل ReporterProfile
@admin.register(ReporterProfile)
class ReporterProfileAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'phone')
    search_fields = ('reporter__username', 'phone')

# ثبت مدل Subtitle
@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle_title', 'date', 'registration')
    list_filter = ('date', 'registration')
    search_fields = ('title', 'subtitle_title')
    date_hierarchy = 'date'


# from django.contrib import admin
# from .models import Category, News
# from .models import ReporterProfile
# from django.contrib.admin import RelatedOnlyFieldListFilter
# from .models import Subtitle



# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'parent_category', 'status')
#     list_filter = ('status', ('parent_category', RelatedOnlyFieldListFilter))
#     search_fields = ('name', 'parent_category__name')

#     fieldsets = (
#         (None, {
#             'fields': ('name', 'parent_category', 'status')
#         }),
#     )

# admin.site.register(Category, CategoryAdmin)

# class NewsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'status', 'date')
#     search_fields = ('title', 'keywords')
#     list_filter = ('category', 'status', 'date')

# admin.site.register(News, NewsAdmin)

# @admin.register(ReporterProfile)
# class ReporterProfileAdmin(admin.ModelAdmin):
#     list_display = ('reporter', 'phone')
#     search_fields = ('reporter__username', 'phone')
    

# class SubtitleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'date', 'operation')  # فیلدهایی که در لیست نمایش داده می‌شوند
#     search_fields = ('title',)  # فیلدهایی که برای جستجو استفاده می‌شوند
#     list_filter = ('date',)  # فیلدهایی که برای فیلتر استفاده می‌شوند
#     list_per_page = 10  # تعداد ردیف‌ها در هر صفحه

#     def operation(self, obj):
#         return f'ویرایش | حذف'  # عمل ویرایش و حذف

#     operation.short_description = 'عملیات'

# admin.site.register(Subtitle, SubtitleAdmin)