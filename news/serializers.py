from rest_framework import serializers
from .models import News, Setting, User, Role, Category, UserProfile, ReporterProfile, Operation, Advertising
from .models import PageView
from rest_framework import serializers
from .models import News
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from .models import News, Keyword



class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['word']

class NewsDetailSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True)
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)

    class Meta:
        model = News
        fields = [
            'id', 
            'title', 
            'reporter_name',
            'category', 
            'content', 
            'short_description',
            'news_text', 
            'created_at', 
            'status', 
            'keywords'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        # بررسی مطابقت رمز عبور و تایید رمز عبور
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("رمز عبور و تایید رمز عبور باید یکسان باشند.")
        return data

    def create(self, validated_data):
        # حذف confirm_password قبل از ذخیره در دیتابیس
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # چک می‌کند که آیا ایمیل در دیتابیس وجود دارد یا خیر
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("کاربری با این ایمیل یافت نشد.")
        return value
    
class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_token(self, value):
        # اعتبارسنجی توکن برای اطمینان از اینکه معتبر است
        user = self.context.get('user')
        if not PasswordResetTokenGenerator().check_token(user, value):
            raise serializers.ValidationError("توکن معتبر نیست یا منقضی شده است.")
        return value
class SubtitleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField(max_length=200)


# آمار بازدید
class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = '__all__'
        
# سریالایزر برای نمایش تنظیمات
class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['id', 'subcategory_name', 'status', 'logo', 'contact_us', 'about_us']

# سریالایزر برای ایجاد یا ویرایش تنظیمات
class SettingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['subcategory_name', 'status', 'logo', 'contact_us', 'about_us']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'phone_number', 'password', 'profile_picture']
#         extra_kwargs = {'password': {'write_only': True}}
#         fields = ['id', 'name', 'phone_number', 'role', 'status']

class ReporterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporterProfile
        fields = ['id', 'reporter', 'phone']
        
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id', 'reporter', 'category', 'title', 'content', 'short_description',
            'news_text', 'created_at', 'updated_at', 'status', 'date', 'keywords', 'is_approved'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        # به طور خودکار reporter را از request.user بگیرید
        user = self.context['request'].user  # گرفتن کاربر از request
        news = News.objects.create(reporter=user, **validated_data)  # ایجاد خبر
        return news

class NewsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'short_description', 'category', 'keywords', 'news_text']  # فیلدهای ویرایش خبر
        
class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'phone_number', 'password', 'confirm_password', 'role']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
# سریالایزر نقش (Role)
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

# سریالایزر کاربر (User)
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()  # نمایش نقش به صورت آبجکت

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'role', 'status']

# سریالایزر اضافه کردن کاربر
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'mobile', 'password', 'password2', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
# سریالایزر برای نمایش تبلیغات (برای مشاهده توسط همه کاربران)
class AdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = [
            'id', 'onvan_tabligh', 'link', 'banner', 'location',
            'start_date', 'expiration_date', 'status'
        ]
        
# سریالایزر برای ایجاد، ویرایش یا حذف تبلیغ (برای ادمین‌ها)
class AdvertisingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = [
            'onvan_tabligh', 'link', 'banner', 'location',
            'start_date', 'expiration_date', 'status'
        ]
        
# سریالایزر UserProfile برای مدیریت پروفایل کاربران
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'user']

# سریالایزر Operation برای عملیات ویرایش و حذف
class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'news', 'operation_type', 'performed_at']
        
class AdminAdvertisingSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Advertising
        fields = ['id', 'location', 'start_date', 'expiration_date', 'status']

    def get_status(self, obj):
        return "approved" if obj.status else "pending"

class PublicAdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = ['id', 'link', 'banner', 'location']