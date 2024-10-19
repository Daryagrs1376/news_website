from rest_framework import serializers
from .models import News, Setting, User, Role, Category, UserProfile, ReporterProfile, Operation, Advertising




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
        fields = ['id', 'name', 'subcategory_name', 'status']

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
        fields = ['id', 'title', 'short_description', 'category', 'keywords', 'news_text', 'created_at', 'updated_at']

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
    
# سریالایزر تبلیغات
class AdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = [
            'id', 'onvan_tabligh', 'link', 'banner', 'location',
            'start_date', 'expiration_date', 'status'
        ]

# سریالایزر برای ایجاد یا ویرایش تبلیغ
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