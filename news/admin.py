from django.contrib import admin
from .models import (
    Newscategory, Category, Keyword, location, Feature,
    News, SpecialFeature, SpecialCategory, NewsSpecialAttributes,
    ReporterProfile, Role, User, Advertising, Setting, Dashboard,
    Operation, UserProfile
)
from .models import PageView
from .models import Grouping



# تنظیمات مربوط به مدل Newscategory
class NewscategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'title', 'parent_category', 'status')
    search_fields = ('category_name', 'title')
    list_filter = ('status',)

# تنظیمات مربوط به مدل Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'description')
    
    search_fields = ('name',)

# تنظیمات مربوط به مدل Keyword
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('word', 'category')
    search_fields = ('word',)
    list_filter = ('category',)

# تنظیمات مربوط به مدل location
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'news_text', 'content')
    search_fields = ('title',)

# تنظیمات مربوط به مدل Feature
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name',)
    search_fields = ('feature_name',)

# تنظیمات مربوط به مدل News
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'created_at', 'status')
    search_fields = ('title', 'short_description', 'news_text')
    list_filter = ('status', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

# تنظیمات مربوط به مدل Role
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# تنظیمات مربوط به مدل User
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'role', 'status')
    search_fields = ('username', 'email', 'mobile')
    list_filter = ('role', 'status')

# تنظیمات مربوط به مدل Advertising
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ('onvan_tabligh', 'link', 'location', 'start_date', 'expiration_date', 'status')
    search_fields = ('onvan_tabligh', 'location')
    list_filter = ('location', 'status', 'start_date', 'expiration_date')

# تنظیمات مربوط به مدل Setting
class SettingAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'status')
    search_fields = ('subcategory_name',)
    list_filter = ('status',)

# تنظیمات مربوط به مدل Dashboard
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('news', 'admin_panel')
    search_fields = ('news__title',)

# تنظیمات مربوط به مدل Operation
class OperationAdmin(admin.ModelAdmin):
    list_display = ('news', 'operation_type', 'performed_at')
    search_fields = ('news__title', 'operation_type')
    list_filter = ('operation_type', 'performed_at')

# تنظیمات مربوط به مدل UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

# تعریف نحوه نمایش مدل در پنل ادمین
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_visits', 'social_visits', 'bounce_rate')  # فیلدهایی که در لیست ادمین نمایش داده می‌شوند
    list_filter = ('date',)  # فیلتر کردن بر اساس تاریخ
    search_fields = ('date',)  # امکان جستجو بر اساس تاریخ


# ثبت مدل‌ها در پنل ادمین
admin.site.register(Newscategory, NewscategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(location, LocationAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Grouping)
admin.site.register(News, NewsAdmin)
admin.site.register(SpecialFeature)
admin.site.register(SpecialCategory)
admin.site.register(NewsSpecialAttributes)
admin.site.register(ReporterProfile)
admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Advertising, AdvertisingAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PageView, PageViewAdmin)
