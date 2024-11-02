from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import AbstractUser, Group, Permission


class Subtitle(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField() 

class Newscategory(models.Model):
    category_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255) 
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Category(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class Keyword(models.Model):
    word = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.word

class location(models.Model):
    title = models.CharField(max_length=255)
    news_text = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title


class Feature(models.Model):
    feature_name = models.CharField(max_length=50)
    news = models.ForeignKey('News', on_delete=models.CASCADE)

    def __str__(self):
        return self.feature_name

class Grouping(models.Model):
    Grouping_name = models.CharField(max_length=100) 

    def __str__(self):
        return self.Grouping_name
    
    
class News(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    content = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    news_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField(Keyword)
    is_approved = models.BooleanField(default=False) 

    def __str__(self):
        return self.title
     
class SpecialFeature(models.Model):
    feature_name = models.CharField(max_length=50)

    def __str__(self):
        return self.feature_name

class SpecialCategory(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class NewsSpecialAttributes(models.Model):
    special_feature1 = models.ForeignKey(SpecialFeature, on_delete=models.SET_NULL, null=True, related_name='special_feature1')
    special_feature2 = models.ForeignKey(SpecialFeature, on_delete=models.SET_NULL, null=True, blank=True)
    featured = models.BooleanField(default=False)
    special_category1 = models.ForeignKey(SpecialCategory, on_delete=models.SET_NULL, null=True, related_name='special_category1')
    special_category2 = models.ForeignKey(SpecialCategory, on_delete=models.SET_NULL, null=True, related_name='special_category2')

    def __str__(self):
        return f"Attributes: {self.special_feature1}, {self.special_category1}"


class News_reporter(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    news_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField(Keyword)
    special_attributes = models.OneToOneField(NewsSpecialAttributes, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        abstract = False 
        
    def __str__(self):
        return self.title

class ReporterProfile(models.Model):
    reporter  = models.ForeignKey(User,  on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=13, null=True)
  
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
        
class NewsKeywords(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.news.title} - {self.keyword.word}"

class AnotherModel(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)

# مدل نقش (Role)
class Role(models.Model):
    ADMIN = 'admin'
    REPORTER = 'reporter'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (REPORTER, 'Reporter'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)  # فیلد موبایل اضافه شده
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)  # نقش کاربر
    status = models.BooleanField(default=True)  # وضعیت فعال/غیرفعال بودن
    
     # تغییر نام دسترسی معکوس (related_name) برای جلوگیری از تداخل با مدل پیش‌فرض auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='news_user_groups',  # اضافه کردن related_name منحصر به فرد
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='news_user_permissions',  # اضافه کردن related_name منحصر به فرد
        blank=True,
        help_text='Specific permissions for this user.'
    )
    
class Advertising(models.Model):
    LOCATION_CHOICES = [
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
    ]

    onvan_tabligh = models.CharField(max_length=255)  # عنوان تبلیغ
    link = models.URLField()  # لینک تبلیغ
    banner = models.ImageField(upload_to='banners/')  # بنر تبلیغ
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)  # موقعیت تبلیغ
    start_date = models.DateField()  # تاریخ شروع
    expiration_date = models.DateField()  # تاریخ انقضا
    status = models.BooleanField(default=True)  # وضعیت فعال/غیرفعال بودن تبلیغ

    def __str__(self):
        return self.onvan_tabligh
    
# مدل تنظیمات (Setting)
class Setting(models.Model):
    subcategory_name = models.CharField(max_length=255)  # نام زیرمجموعه
    status = models.BooleanField(default=True)  # وضعیت فعال یا غیرفعال
    logo = models.ImageField(upload_to='logos/')  # لوگو
    contact_us = models.TextField()  # اطلاعات تماس
    about_us = models.TextField()  # اطلاعات درباره ما

    def __str__(self):
        return self.subcategory_name
    
# مدل Dashboard
class Dashboard(models.Model):
    admin_panel = models.BooleanField(default=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dashboard for {self.news.title}"

# مدل برای Operation (ویرایش و حذف)
class Operation(models.Model):
    EDIT = 'edit'
    DELETE = 'delete'
    OPERATION_CHOICES = [
        (EDIT, 'Edit'),
        (DELETE, 'Delete'),
    ]

    news = models.ForeignKey(News, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_operation_type_display()} on {self.news.title}"

# مدل برای مدیریت پروفایل کاربرانUserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class PageView(models.Model):
    date = models.DateField()
    total_visits = models.IntegerField()
    social_visits = models.IntegerField()
    bounce_rate = models.FloatField()
    page_views = models.JSONField()  # ذخیره جزئیات بازدید هر صفحه