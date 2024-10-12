from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django import forms



class Category(models.Model):
    title = models.CharField(max_length=255) 
    search_query = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    subcategory_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class News(models.Model):
    CATEGORY_CHOICES = [
        ('sport', 'Sport'),
        ('economy', 'Economy'),
        ('iran', 'Iran'),
        ('world', 'World'),
        ('politics', 'Politics'),
        ('culture', 'Culture'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    short_description = models.TextField(null=True, blank=True)
    news_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True) 
    date = models.DateTimeField(auto_now_add=True)
    keywords = models.CharField(max_length=255) 
    special_feature1 = models.BooleanField(default=False)  
    special_feature2 = models.BooleanField(default=False) 
    featured = models.BooleanField(default=False)  
    special_category1 = models.BooleanField(default=False)  
    special_category2 = models.BooleanField(default=False)  

    def __str__(self):
        return self.title

class ReporterProfile(models.Model):
    reporter  = models.ForeignKey(User,  on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=13, null=True)

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15, unique=True)
#     password = models.CharField(max_length=128)
#     role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('reporter', 'Reporter')])
#     status = models.BooleanField(default=True)
#     last_login = models.DateTimeField(blank=True, null=True)  # فیلد last_login اضافه شده است
    
#     def __str__(self):
#         return self.name

    
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# class User(AbstractBaseUser):
#     name = models.CharField(max_length=100, blank=True, null=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     password = models.CharField(max_length=128)
#     role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('reporter', 'Reporter')])
#     status = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True, null=True)
#     last_name = models.CharField(max_length=30, blank=True, null=True)
    
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
    
#     objects = UserManager()

#     USERNAME_FIELD = 'phone_number'

#     pass

#     def __str__(self):
#         return self.phone_number
    
class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
class Subtitle(models.Model):
    title = models.CharField(max_length=255)  # عنوان زیرنویس
    subtitle_title = models.CharField(max_length=85)  # متن زیرنویس، حداقل 85 حرف
    date = models.DateTimeField(default=timezone.now)  # تاریخ ثبت
    registration = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subtitle_title

    class Meta:
        verbose_name = 'Subtitle'
        verbose_name_plural = 'Subtitles'