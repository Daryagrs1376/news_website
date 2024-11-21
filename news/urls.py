from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import(
TokenObtainPairView,
TokenRefreshView,
)
from .views import (
AdminAdvertisingViewSet,
PublicAdvertisingViewSet,
PostViewSet,
NewsViewSet,
CategoryViewSet,
NewsListView,
NewsCreateView, 
NewsDetailView,
SettingListView,
SettingCreateView,
SettingUpdateView,
AdvertisingListView,
AdvertisingCreateView,
AdvertisingUpdateView,
AdvertisingDeleteView,
UserListView,
UserCreateView,
UserUpdateDeleteView,
AddCategory,
CategoryListView,
CategoryDetailView,
DailyStatsView,
WeeklyStatsView,
ProtectedView,
AdminAdvertisingListView,
PublicAdvertisingListView,
PasswordResetRequestView,
PasswordResetView,
UserRegistrationView,
RegisterView,
RequestPasswordResetAPIView,
ResetPasswordAPIView,
subtitle_list,
add_subtitle,
edit_subtitle,
delete_subtitle,
edit_category,
delete_category,
create_news,
)

schema_view = get_schema_view(
    openapi.Info(
        title="News API",
        default_version="v1",
        description="API documentation for the News application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@news.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'userprofiles', UserProfileViewSet, basename='userprofiles')
# router.register(r'operations', OperationViewSet, basename='operations')
router.register(r'posts', PostViewSet)
router.register(r'admin/advertisements', AdminAdvertisingViewSet, basename='admin-advertisements')
router.register(r'advertisements', PublicAdvertisingViewSet, basename='public-advertisements')


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

    path('settings/', SettingListView.as_view(), name='setting-list'),
    path('settings/add/', SettingCreateView.as_view(), name='setting-create'),
    path('settings/<int:pk>/edit/', SettingUpdateView.as_view(), name='setting-update'),

    path('advertising/', AdvertisingListView.as_view(), name='advertising-list'),
    path('advertising/add/', AdvertisingCreateView.as_view(), name='advertising-create'),
    path('advertising/<int:pk>/edit/', AdvertisingUpdateView.as_view(), name='advertising-update'),
    path('advertising/<int:id>/delete/', AdvertisingDeleteView.as_view(), name='delete-advertising'),
    path('advertisements/', PublicAdvertisingListView.as_view(), name='public-advertising-list'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('users/add/', UserCreateView.as_view(), name='user-create'),
    path('user/<int:pk>/', UserUpdateDeleteView.as_view(), name='user-update-delete'),

    path('categories/add/', AddCategory.as_view(), name='category-add'),
    path('categories/edit/<int:pk>/', edit_category, name='edit-category'),
    path('categories/<int:pk>/delete/', delete_category, name='category-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),

    path('subtitles/', subtitle_list, name='subtitle-list'),
    path('subtitles/add/', add_subtitle, name='subtitle-add'),
    path('subtitles/<int:pk>/edit/', edit_subtitle, name='subtitle-edit'),
    path('subtitles/<int:pk>/delete/', delete_subtitle, name='subtitle-delete'),

    # path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),

    path('daily/', DailyStatsView.as_view(), name='daily-stats'),
    path('weekly/', WeeklyStatsView.as_view(), name='weekly-stats'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token_create/', obtain_auth_token, name='token_create'),
    path('protected/', ProtectedView.as_view(), name='protected-view'),

    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/password-reset/<uidb64>/<token>/', PasswordResetView.as_view(), name='password-reset'),

    path('register/', RegisterView.as_view(), name='register'),

    path('', include(router.urls)),
    path('api/', include(router.urls)), 
    path('create-news/', create_news, name='create_news'),
    path('password-reset/', RequestPasswordResetAPIView.as_view(), name='password-reset-request'),
    path('password-reset/<str:token>/', ResetPasswordAPIView.as_view(), name='password-reset'),
]


# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework import permissions
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.authtoken.views import obtain_auth_token
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework.permissions import AllowAny
# from .views import PostViewSet
# from .views import create_news
# from .views import RegisterView
# from .views import (
# NewsViewSet,
# CategoryViewSet,
# UserProfileViewSet,
# RequestPasswordResetAPIView,
# ResetPasswordAPIView,
# OperationViewSet,
# NewsListView,
# NewsCreateView,
# NewsDetailView,
# SettingListView,
# SettingCreateView,
# SettingUpdateView,
# AdvertisingListView,
# AdvertisingCreateView,
# AdvertisingUpdateView,
# AdvertisingDeleteView,
# UserListView,
# UserCreateView,
# UserUpdateDeleteView,
# AddCategory,
# edit_category,
# delete_category,
# CategoryListView,
# CategoryDetailView,
# subtitle_list,
# add_subtitle,
# edit_subtitle,
# delete_subtitle,
# UserProfileDetailView,
# DailyStatsView,
# WeeklyStatsView,
# ProtectedView,
# AdminAdvertisingListView,
# PublicAdvertisingListView,
# PasswordResetRequestView,
# PasswordResetView,
# UserRegistrationView
# )

# # تنظیمات مستندات API
# schema_view = get_schema_view(
#     openapi.Info(
#         title="News API",
#         default_version="v1",
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@news.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(AllowAny,),  # استفاده از آبجکت تابع
# )

# # Router برای ویوست‌ها
# router = DefaultRouter()
# router.register(r'news', NewsViewSet, basename='news')
# router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'userprofiles', UserProfileViewSet, basename='userprofiles')
# router.register(r'operations', OperationViewSet, basename='operations')
# router.register(r'posts', PostViewSet)

# # تعریف مسیرهای URL
# urlpatterns = [
#     # مسیرهای مستندات API
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

#     # مسیرهای مرتبط با اخبار (News)
#     path('news/', NewsListView.as_view(), name='news-list'),
#     path('news/create/', NewsCreateView.as_view(), name='news-create'),
#     path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

#     # مسیرهای مرتبط با تنظیمات (Settings)
#     path('settings/', SettingListView.as_view(), name='setting-list'),
#     path('settings/add/', SettingCreateView.as_view(), name='setting-create'),
#     path('settings/<int:pk>/edit/', SettingUpdateView.as_view(), name='setting-update'),

#     # مسیرهای مرتبط با تبلیغات (Advertising)
#     path('advertising/', AdvertisingListView.as_view(), name='advertising-list'),
#     path('advertising/add/', AdvertisingCreateView.as_view(), name='advertising-create'),
#     path('advertising/<int:pk>/edit/', AdvertisingUpdateView.as_view(), name='advertising-update'),
#     path('advertising/<int:id>/delete/', AdvertisingDeleteView.as_view(), name='delete-advertising'),
#     path('advertisements/', PublicAdvertisingListView.as_view(), name='public-advertising-list'),

#     # مسیرهای مرتبط با کاربران (User)
#     path('users/', UserListView.as_view(), name='user-list'),
#     path('users/add/', UserCreateView.as_view(), name='user-create'),
#     path('user/<int:pk>/', UserUpdateDeleteView.as_view(), name='user-update-delete'),

#     # مسیرهای مرتبط با دسته‌بندی‌ها (Categories)
#     path('categories/add/', AddCategory.as_view(), name='category-add'),
#     path('categories/edit/<int:pk>/', edit_category, name='edit-category'),
#     path('categories/<int:pk>/delete/', delete_category, name='category-delete'),
#     path('categories/', CategoryListView.as_view(), name='category-list'),
#     path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),

#     # مسیرهای مرتبط با زیرنویس‌ها (Subtitles)
#     path('subtitles/', subtitle_list, name='subtitle-list'),
#     path('subtitles/add/', add_subtitle, name='subtitle-add'),
#     path('subtitles/<int:pk>/edit/', edit_subtitle, name='subtitle-edit'),
#     path('subtitles/<int:pk>/delete/', delete_subtitle, name='subtitle-delete'),

#     # مسیرهای مرتبط با پروفایل کاربری
#     path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),

#     # مسیرهای آماری
#     path('daily/', DailyStatsView.as_view(), name='daily-stats'),
#     path('weekly/', WeeklyStatsView.as_view(), name='weekly-stats'),

#     # مسیرهای JWT و احراز هویت
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('token_create/', obtain_auth_token, name='token_create'),

#     # مسیرهای محافظت‌شده
#     path('protected/', ProtectedView.as_view(), name='protected-view'),

#     # مسیرهای ثبت‌نام و بازنشانی رمز عبور
#     path('register/', RegisterView.as_view(), name='register'),
#     path('register/', UserRegistrationView.as_view(), name='user-registration'),
#     path('api/password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
#     path('api/password-reset/<uidb64>/<token>/', PasswordResetView.as_view(), name='password-reset'),

#     # مسیرهای مرتبط با تبلیغات عمومی
#     path('', include(router.urls)),
#     path('api/', include(router.urls)), 
#     path('create-news/', create_news, name='create_news'),

#     path('password-reset/', RequestPasswordResetAPIView.as_view(), name='password-reset-request'),
#     path('password-reset/<str:token>/', ResetPasswordAPIView.as_view(), name='password-reset'),
# ]