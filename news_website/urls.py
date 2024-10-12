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
from django.urls import path
from news import views
from news.views import NewsDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),
    path('api/categories/', views.category_list, name='category-list'),
    path('api/categories/add/', views.add_category, name='add-category'),
    path('api/categories/edit/<int:pk>/', views.edit_category, name='edit-category'),
    path('api/categories/delete/<int:pk>/', views.delete_category, name='delete-category'),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]
