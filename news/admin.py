from django.contrib import admin
from .models import (
    Newscategory,
    Category,
    Keyword,
    location,
    Feature,
    News,
    SpecialFeature,
    SpecialCategory,
    NewsSpecialAttributes,
    ReporterProfile,
    Role,
    User,
    Advertising,
    Setting,
    Dashboard,
    Operation,
    UserProfile,
    Subtitle,
    Grouping,
    PageView,
)



class NewscategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'title', 'parent_category', 'status')
    search_fields = ('category_name', 'title')
    list_filter = ('status',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'description')
    
    search_fields = ('name',)

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('word', 'category')
    search_fields = ('word',)
    list_filter = ('category',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'news_text', 'content')
    search_fields = ('title',)

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name',)
    search_fields = ('feature_name',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'created_at', 'is_approved')
    list_filter = ('is_approved','created_at')
    search_fields = ('title', 'short_description')
    list_editable = ('is_approved',)
    ordering = ('-created_at',)
    
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'role', 'status')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('role', 'status')
    
# تنظیمات مربوط به مدل Advertising
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ('onvan_tabligh', 'link', 'location', 'start_date', 'expiration_date', 'status')
    search_fields = ('onvan_tabligh', 'location')
    list_filter = ('location', 'status', 'start_date', 'expiration_date')
    
    # فقط ادمین‌ها قادر به ویرایش یا حذف خواهند بود
    def has_change_permission(self, request, obj=None):
        # فقط ادمین‌ها می‌توانند تغییرات را اعمال کنند
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # فقط ادمین‌ها می‌توانند تبلیغ را حذف کنند
        return request.user.is_superuser

    def has_add_permission(self, request):
        # فقط ادمین‌ها می‌توانند تبلیغ جدید اضافه کنند
        return request.user.is_superuser

# تنظیمات مربوط به مدل Setting
class SettingAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'status')
    search_fields = ('subcategory_name',)
    list_filter = ('status',)

class DashboardAdmin(admin.ModelAdmin):
    list_display = ('news', 'admin_panel')
    search_fields = ('news__title',)

class OperationAdmin(admin.ModelAdmin):
    list_display = ('news', 'operation_type', 'performed_at')
    search_fields = ('news__title', 'operation_type')
    list_filter = ('operation_type', 'performed_at')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

class PageViewAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_visits', 'social_visits', 'bounce_rate')  # فیلدهایی که در لیست ادمین نمایش داده می‌شوند
    list_filter = ('date',)  # فیلتر کردن بر اساس تاریخ
    search_fields = ('date',)  # امکان جستجو بر اساس تاریخ


# ثبت مدل‌ها در پنل ادمین
admin.site.register(Newscategory)
admin.site.register(Category)
admin.site.register(Keyword)
admin.site.register(location)
admin.site.register(Feature)
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
admin.site.register(Dashboard)
admin.site.register(Operation)
admin.site.register(UserProfile)
admin.site.register(PageView)
admin.site.register(Subtitle)
