from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django import forms



class Category(models.Model):
    title = models.CharField(max_length=255) 
    # TODO: delete search query (انجام شد)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# TODO: کتگوری باید فارنکی باشه به مدل کتگوری نباید چویسس باشه
class Keyword(models.Model):
    """
    در این مدل کلیدواژه های هر خبر ذخیره میشود
    """
    # TODO: پس فارنکیت کو؟
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word

# TODO: اسم این مدل باید به یه چیزی مثل پوزیشن یا لوکیشن تغییر کنه
class SpecialFeature(models.Model):
    """
    در این قسمت مشخص میشود که هر خبر در کدام قسمت سایت قرار است نمایش داده شود
    """
    # TODO: الان این به کدام خبر وصل است؟
    # TODO: اگر هر خبر بتواند در چند موقعیت نمایش داده شود و یا اینکه یک موقعیت بتواند
    # چند خبر داشته باشند رابطه بین این مدل با خبر منی‌تو‌منی میشود
    feature_name = models.CharField(max_length=50)

    def __str__(self):
        return self.feature_name

# TODO: اسم مدل به کتگوری تغییر کند
class SpecialCategory(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name
    
    
# TODO: کلمات کلیدی مثل کتگوری باید خودشون یه جدول بشن(انجام شد)
class News(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # TODO: این فیلد باید منی‌تو‌منی
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    news_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField(Keyword)
    
    
    # TODO: این پنج تا فیلد باید شبیه به کتگوری خودشون یه جدول بشن(انجام شد)
    # ویژگی‌های خاص (ForeignKey به مدل‌های SpecialFeature و SpecialCategory)
    # special_feature1 = models.ForeignKey(SpecialFeature, on_delete=models.SET_NULL, null=True, related_name='special_feature1')
    # special_feature2 = models.ForeignKey(SpecialFeature, on_delete=models.SET_NULL, null=True, blank=True)
    # featured = models.BooleanField(default=False)
    # special_category1 = models.ForeignKey(SpecialCategory, on_delete=models.SET_NULL, null=True, related_name='special_category1')
    # special_category2 = models.ForeignKey(SpecialCategory, on_delete=models.SET_NULL, null=True, related_name='special_category2')

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