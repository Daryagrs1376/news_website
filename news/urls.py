from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserList, UserDetail, NewsList, NewsDetail, UserProfile, ChangePassword, SignOut
from .views import CategoryViewSet, CategoryList, AddCategory, EditCategory, DeleteCategory, Category, CategoryDetail
from . import views



router = DefaultRouter()
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/add/', AddCategory, name='add-category'),
    path('categories/edit/<int:category_id>/', EditCategory, name='edit-category'),
    path('categories/delete/<int:category_id>/', DeleteCategory, name='delete-category'),
    path('', include(router.urls)),
    path('news/', NewsList.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),
    path('profile/<str:username>/', UserProfile.as_view(), name='user-profile'),
    path('change-password/<str:username>/', ChangePassword.as_view(), name='change-password'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('users/', views.list_users, name='list_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/', UserList.as_view(), name='list_users'),
    path('users/<int:user_id>/', UserDetail.as_view(), name='user_detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/add/', AddCategory.as_view(), name='category-add'),
    path('categories/edit/<int:pk>/', EditCategory.as_view(), name='category-edit'),
    path('categories/delete/<int:pk>/', DeleteCategory.as_view(), name='category-delete'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
]
