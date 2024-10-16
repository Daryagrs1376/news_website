"""
URL configuration for news_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news import views
from news.views import (
    NewsList, NewsDetail, CategoryDetail, AddCategory, 
    edit_category, delete_category, add_category, category_list, 
    subtitle_list, add_subtitle, edit_subtitle, delete_subtitle, 
    SubtitleList, AddSubtitle, UserListCreateView, UserProfileDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', NewsList.as_view(), name='news-list'),  # لیست اخبار
    path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),  # جزئیات خبر

    # مسیرهای مربوط به دسته‌بندی‌ها (Categories)
    path('categories/', category_list, name='category-list'),  # لیست دسته‌بندی‌ها
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),  # جزئیات یک دسته‌بندی خاص
    path('categories/add/', add_category, name='add-category'),  # اضافه کردن دسته‌بندی
    path('categories/<int:pk>/edit/', edit_category, name='edit-category'),  # ویرایش دسته‌بندی
    path('categories/<int:pk>/delete/', delete_category, name='delete-category'),  # حذف دسته‌بندی

    # مسیرهای مربوط به زیرنویس‌ها (Subtitles)
    path('subtitles/', subtitle_list, name='subtitle-list'),  # لیست زیرنویس‌ها
    path('subtitles/add/', add_subtitle, name='add-subtitle'),  # اضافه کردن زیرنویس
    path('subtitles/<int:pk>/edit/', edit_subtitle, name='edit-subtitle'),  # ویرایش زیرنویس
    path('subtitles/<int:pk>/delete/', delete_subtitle, name='delete-subtitle'),  # حذف زیرنویس

    # مسیرهای مربوط به نمای لیستی و اضافه‌کردن زیرنویس با استفاده از کلاس‌های View
    path('subtitles/class-based/', SubtitleList.as_view(), name='subtitle-list-class'),  # لیست زیرنویس‌ها با کلاس View
    path('subtitles/add/class-based/', AddSubtitle.as_view(), name='add-subtitle-class'),  # اضافه‌کردن زیرنویس با کلاس View

    # مسیرهای مربوط به کاربران (User)
    path('users/', UserListCreateView.as_view(), name='user-list-create'),  # لیست و اضافه‌کردن کاربران
    path('users/<int:pk>/', UserProfileDetailView.as_view(), name='user-detail'),  # جزئیات پروفایل کاربر
]