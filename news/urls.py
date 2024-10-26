from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet, CategoryViewSet, UserProfileViewSet, 
    OperationViewSet, NewsList, NewsDetail, 
    SettingListView, SettingCreateView, SettingUpdateView,
    AdvertisingListView, AdvertisingCreateView, 
    AdvertisingUpdateView, AdvertisingDeleteView,
    UserListView, UserCreateView, UserUpdateDeleteView,
    AddCategory, edit_category, delete_category, CategoryDetailView, CategoryListView,
    subtitle_list, add_subtitle, SubtitleList, AddSubtitle, 
    edit_subtitle, delete_subtitle, UserProfileDetailView,
    DailyStatsView, WeeklyStatsView, ProtectedView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# تنظیمات مستندات API
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for news site",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router برای ویوست‌ها
router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofiles')
router.register(r'operations', OperationViewSet, basename='operations')

urlpatterns = [
    # path('admin/', admin.site.urls),  # مسیر پنل مدیریت Django

    # مسیرهای مرتبط با تنظیمات (Settings)
    path('settings/', SettingListView.as_view(), name='setting-list'),
    path('settings/add/', SettingCreateView.as_view(), name='setting-create'),
    path('settings/<int:pk>/edit/', SettingUpdateView.as_view(), name='setting-update'),

    # مسیرهای مرتبط با تبلیغات (Advertising)
    path('advertising/', AdvertisingListView.as_view(), name='advertising-list'),
    path('advertising/add/', AdvertisingCreateView.as_view(), name='advertising-create'),
    path('advertising/<int:pk>/edit/', AdvertisingUpdateView.as_view(), name='advertising-update'),
    path('advertising/<int:id>/delete/', AdvertisingDeleteView.as_view(), name='delete_advertising'),

    # مسیرهای مرتبط با کاربران (User)
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/add/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', UserUpdateDeleteView.as_view(), name='user-update-delete'),

    # مسیرهای مرتبط با اخبار (News)
    path('news/', NewsList.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),

    # مسیرهای مرتبط با دسته‌بندی‌ها (Categories)
    path('categories/add/', AddCategory.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', edit_category, name='category-edit'),
    path('categories/<int:pk>/delete/', delete_category, name='category-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),

    # مسیرهای مرتبط با زیرنویس‌ها (Subtitles)
    path('subtitles/', subtitle_list, name='subtitle-list'),
    path('subtitles/add/', add_subtitle, name='subtitle-add'),
    path('subtitles/<int:pk>/edit/', edit_subtitle, name='subtitle-edit'),
    path('subtitles/<int:pk>/delete/', delete_subtitle, name='subtitle-delete'),

    # مسیرهای مرتبط با پروفایل کاربر (UserProfile)
    path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),

    # مسیرهای مرتبط با آمار بازدید
    path('daily/', DailyStatsView.as_view(), name='daily-stats'),
    path('weekly/', WeeklyStatsView.as_view(), name='weekly-stats'),

    # مسیرهای احراز هویت JWT با نام جدید Token
    path('Token/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('Token/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # مسیر مستندات Swagger و Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # سایر مسیرها
    path('protected/', ProtectedView.as_view(), name='protected_view'),

    # استفاده از روت‌های پیش‌فرض برای ویوست‌ها
    path('', include(router.urls)),
]



# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     NewsViewSet, CategoryViewSet, UserProfileViewSet, 
#     OperationViewSet, NewsList, NewsDetail, 
#     SettingListView, SettingCreateView, SettingUpdateView,
#     AdvertisingListView, AdvertisingCreateView, 
#     AdvertisingUpdateView, AdvertisingDeleteView,
#     UserListView, UserCreateView, UserUpdateDeleteView,
#     AddCategory, edit_category, delete_category,
#     subtitle_list, add_subtitle, SubtitleList, AddSubtitle, 
#     edit_subtitle, delete_subtitle, UserProfileDetailView
# )
# from .views import DailyStatsView, WeeklyStatsView
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from django.urls import path
# from .views import CategoryListView, CategoryDetailView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from django.urls import path
# from .views import ProtectedView
# from . import views
# from django.urls import path
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# schema_view = get_schema_view(
#     openapi.Info(
#         title="API Documentation",
#         default_version='v1',
#         description="API documentation for news site",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )


# # اطلاعات مستندات API
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Your API",
#         default_version='v1',
#         description="Your API description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@yourapi.local"),
#         license=openapi.License(name="License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )


# # Router برای ویوست‌ها
# router = DefaultRouter()
# router.register(r'news', NewsViewSet, basename='news')
# router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'userprofiles', UserProfileViewSet, basename='userprofiles')
# router.register(r'operations', OperationViewSet, basename='operations')

# urlpatterns = [
#     # path('admin/', admin.site.urls),

#     # مسیرهای مرتبط با تنظیمات (Settings)
#     path('settings/', SettingListView.as_view(), name='setting-list'),
#     path('settings/add/', SettingCreateView.as_view(), name='setting-create'),
#     path('settings/<int:pk>/edit/', SettingUpdateView.as_view(), name='setting-update'),

#     # مسیرهای مرتبط با تبلیغات (Advertising)
#     path('advertising/', AdvertisingListView.as_view(), name='advertising-list'),
#     path('advertising/add/', AdvertisingCreateView.as_view(), name='advertising-create'),
#     path('advertising/<int:pk>/edit/', AdvertisingUpdateView.as_view(), name='advertising-update'),
#     path('advertising/<int:id>/delete/', views.delete_advertising, name='delete_advertising'),

#     # مسیرهای مرتبط با کاربران (User)
#     path('users/', UserListView.as_view(), name='user-list'),
#     path('users/add/', UserCreateView.as_view(), name='user-create'),
#     path('users/<int:pk>/edit/', UserUpdateDeleteView.as_view(), name='user-update-delete'),

#     # مسیرهای مرتبط با اخبار (News)
#     path('news/', NewsList.as_view(), name='news-list'),
#     path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),

#     # مسیرهای مرتبط با دسته‌بندی‌ها (Categories)
#     path('categories/add/', AddCategory.as_view(), name='category-add'),
#     path('categories/<int:pk>/edit/', edit_category, name='category-edit'),
#     path('categories/<int:pk>/delete/', delete_category, name='category-delete'),
#     path('categories/', CategoryListView.as_view(), name='category-list'),
#     path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),


#     # مسیرهای مرتبط با زیرنویس‌ها (Subtitles)
#     path('subtitles/', subtitle_list, name='subtitle-list'),
#     path('subtitles/add/', add_subtitle, name='subtitle-add'),
#     path('subtitles/<int:pk>/edit/', edit_subtitle, name='subtitle-edit'),
#     path('subtitles/<int:pk>/delete/', delete_subtitle, name='subtitle-delete'),

#     # مسیرهای مرتبط با پروفایل کاربر (UserProfile)
#     path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),

#     # مسیرهای مرتبط با اضافه کردن/ویرایش زیرنویس‌ها با کلاس-based views
#     path('news/subtitles/', SubtitleList.as_view(), name='subtitle-list-cbv'),
#     path('news/subtitles/add/', AddSubtitle.as_view(), name='subtitle-add-cbv'),

#     # استفاده از روت‌های پیش‌فرض برای ویوست‌ها
#     path('', include(router.urls)),

#     path('daily/', DailyStatsView.as_view(), name='daily-stats'),
#     path('weekly/', WeeklyStatsView.as_view(), name='weekly-stats'),

# # آمار بازدید
#     path('daily/', DailyStatsView.as_view(), name='daily-stats'),
#     path('weekly/', WeeklyStatsView.as_view(), name='weekly-stats'),
#    # مسیر Swagger
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     # مسیر ReDoc
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('protected/', ProtectedView.as_view(), name='protected_view'),

#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
# ]