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
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import views
from rest_framework.permissions import AllowAny
from .views import AdminAdvertisingListView, PublicAdvertisingListView
from .views import PasswordResetRequestView, PasswordResetView
from .views import UserRegistrationView
from .views import NewsDetailView
from .views import NewsCreateView
from .views import NewsListView
from rest_framework.authtoken.views import obtain_auth_token  # اضافه کردن این خط
from .views import NewsListView


# تنظیمات مستندات API
schema_view = get_schema_view(
    openapi.Info(
        title="News API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@news.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),  # استفاده از tuple به جای list یا str
)


# Router برای ویوست‌ها
router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofiles')
router.register(r'operations', OperationViewSet, basename='operations')


urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # # path('api/news/', NewsListView.as_view(), name='news-list'),

    # مسیرهای مرتبط با اخبار (News)
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),

    # مسیرهای مرتبط با تنظیمات (Settings)
    path('settings/', SettingListView.as_view(), name='setting-list'),
    path('settings/add/', SettingCreateView.as_view(), name='setting-create'),
    path('settings/<int:pk>/edit/', SettingUpdateView.as_view(), name='setting-update'),

    # مسیرهای مرتبط با تبلیغات (Advertising)
    path('advertising/', AdvertisingListView.as_view(), name='advertising-list'),
    path('advertising/add/', AdvertisingCreateView.as_view(), name='advertising-create'),
    path('advertising/<int:pk>/edit/', AdvertisingUpdateView.as_view(), name='advertising-update'),
    path('advertising/<int:id>/delete/', AdvertisingDeleteView.as_view(), name='delete_advertising'),

    # # مسیرهای مرتبط با کاربران (User)
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/add/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', UserUpdateDeleteView.as_view(), name='user-update-delete'),

    # # مسیرهای مرتبط با دسته‌بندی‌ها (Categories)
    path('categories/add/', AddCategory.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', edit_category, name='category-edit'),
    path('categories/<int:pk>/delete/', delete_category, name='category-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),

    # # مسیرهای مرتبط با زیرنویس‌ها (Subtitles)
    path('subtitles/', subtitle_list, name='subtitle-list'),
    path('subtitles/add/', add_subtitle, name='subtitle-add'),
    path('subtitles/<int:pk>/edit/', edit_subtitle, name='subtitle-edit'),
    path('subtitles/<int:pk>/delete/', delete_subtitle, name='subtitle-delete'),

    path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),

    path('daily/', DailyStatsView.as_view(), name='daily-stats'),
    path('weekly/', WeeklyStatsView.as_view(), name='weekly-stats'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token_create/', obtain_auth_token, name='token_create'),  # اصلاح شده برای استفاده از obtain_auth_token به صورت مستقیم

    path('protected/', ProtectedView.as_view(), name='protected_view'),

    path('register/', UserRegistrationView.as_view(), name='user_registration'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token_create/', obtain_auth_token, name='token_create'), 
    
    path('news/', NewsListView.as_view(), name='news_list'),

    # path('admin/advertisements/', AdminAdvertisingListView.as_view(), name='admin_advertising_list'),
    path('advertisements/', PublicAdvertisingListView.as_view(), name='public_advertising_list'),
    
    path('api/password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password-reset/<uidb64>/<token>/', PasswordResetView.as_view(), name='password_reset'),
    
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),

    path('news/create/', NewsCreateView.as_view(), name='create_news'),

    path('', include(router.urls)),
]
