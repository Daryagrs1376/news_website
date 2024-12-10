import uuid
import random
from haystack import indexes  # type: ignore
from django import forms
from django.db import models
from django.apps import apps
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.auth.models import(
AbstractBaseUser,
BaseUserManager,
AbstractUser,
User,
Group,
Permission,
PermissionsMixin,
)


User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class media(models.Model):
    file = models.FileField(upload_to='uploads/')
    article = models.ForeignKey(Article, related_name='media', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.file.name}" 

class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return News
    
class OTP(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)
        
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_reset_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and (now() - self.created_at).total_seconds() < 86400
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField()
    verification_code = models.CharField(default='2345', max_length=4)
    
    def __str__(self):
        return self.user.username

class Subtitle(models.Model):
    title = models.CharField(max_length=255)
    subtitle_title = models.CharField(max_length=85)
    date = models.DateTimeField(default=timezone.now)
    registration = models.DateTimeField(auto_now_add=True)
    description = models.TextField() 

    def __str__(self):
        return self.subtitle_title
    class Meta:
        verbose_name = 'Subtitle'
        verbose_name_plural = 'Subtitles'

    def add_keywords(self, keyword_list):
        for word in keyword_list:
            keyword, created = Keyword.objects.get_or_create(word=word)
            self.keywords.add(keyword)
            
class NewsCategory(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE) 
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  
    status = models.BooleanField(default=True)
    articles = models.ManyToManyField('NewsArticle') 

    def __str__(self):
        return f"{self.news.title} - {self.category.title}"

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

    def add_keyword(self, keyword_name):
        keyword, created = Keyword.objects.get_or_create(word=keyword_name)
        self.keywords.add(keyword)
        
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
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField('Category', through='Newscategory', related_name='news_categories')
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    short_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    keywords = models.ManyToManyField('Keyword', blank=True, related_name='news')
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
    special_category1 = models.ForeignKey('SpecialCategory', on_delete=models.SET_NULL, null=True, related_name='special_category1')
    special_category2 = models.ForeignKey('SpecialCategory', on_delete=models.SET_NULL, null=True, related_name='special_category2')

    def __str__(self):
        return f"Attributes: {self.special_feature1}, {self.special_category1}"

class NewsReporter(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    news_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    special_attributes = models.OneToOneField('NewsSpecialAttributes', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class ReporterProfile(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=13, null=True)

    def __str__(self):
        return f"Profile of {self.reporter.username}"
    
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
        
class NewsKeywords(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.news.title} - {self.keyword.word}"

    def get_or_create_keywords(keyword_list):
        keywords = []
        for keyword in keyword_list:
            obj, created = Keyword.objects.get_or_create(name=keyword)
            keywords.append(obj)
        return keywords

class AnotherModel(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)

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
    phone_number = models.CharField(max_length=15, unique=True) 
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True) 
    status = models.BooleanField(default=True) 
    groups = models.ManyToManyField(
        Group,
        related_name='news_user_groups', 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='news_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    def __str__(self):
        return self.username

class Advertising(models.Model):
    LOCATION_CHOICES = [
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
    ]
    title  = models.CharField(max_length=255)
    link = models.URLField()
    banner = models.ImageField(upload_to='banners/')
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    start_date = models.DateField()
    expiration_date = models.DateField()
    status = models.BooleanField(null=True, blank=True, default=None)

    def __str__(self):
        return self.title 

    @property
    def is_active(self):
        """Check if the advertisement is active and not expired."""
        return self.status and self.expiration_date >= now().date()
    
class Setting(models.Model):
    subcategory_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logos/')
    contact_us = models.TextField()
    about_us = models.TextField()

    def __str__(self):
        return self.subcategory_name
    
class Dashboard(models.Model):
    admin_panel = models.BooleanField(default=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dashboard for {self.news.title}"
    
class PageView(models.Model):
    date = models.DateField()
    total_visits = models.IntegerField()
    social_visits = models.IntegerField()
    bounce_rate = models.FloatField()
    page_views = models.JSONField()  
    
class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  
    news_article = models.ForeignKey('NewsArticle', on_delete=models.CASCADE)  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    approved = models.BooleanField(default=False)  
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.news_article.title}"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)  
    reason = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Report by {self.user.username} on comment {self.comment.id}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    news_article = models.ForeignKey('NewsArticle', on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Like by {self.user.username} on {self.news_article.title}"

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()