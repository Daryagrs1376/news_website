from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from .models import(
News,
Setting,
Comment,
Role,
Post,
Keyword,
Category,
ReporterProfile,
UserProfile,
Advertising,
Comment,
PageView,
)

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

        fields = ['id', 'user', 'news_article', 'text','content', 'created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'created_at']
        
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'title', 'word']

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
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("رمز عبور و تایید رمز عبور باید یکسان باشند.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("کاربری با این ایمیل یافت نشد.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_token(self, value):
        user = self.context.get('user')
        if not PasswordResetTokenGenerator().check_token(user, value):
            raise serializers.ValidationError("توکن معتبر نیست یا منقضی شده است.")
        return value
class SubtitleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField(max_length=200)

class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = '__all__'
        
class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['id', 'subcategory_name', 'status', 'logo', 'contact_us', 'about_us']

class SettingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['subcategory_name', 'status', 'logo', 'contact_us', 'about_us']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ReporterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporterProfile
        fields = ['id', 'reporter', 'phone']
        
class NewsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    keywords = serializers.CharField()
    class Meta:
        model = News
        # fields = [
        fields = '__all__'
            # 'id',
            # 'reporter',
            # 'categories'
            # 'title'
            # 'content'
            # 'short_description',
            # 'news_text'
            # 'created_at'
            # 'updated_at'
            # 'published_at',
            # 'status'
            # 'date'
            # 'keywords'
            # 'is_approved',
        # ]
        
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if not data.get('categories'):
            raise serializers.ValidationError("فیلد 'categories' نمی‌تواند خالی باشد.")
        if not data.get('keywords'):
            raise serializers.ValidationError("فیلد 'keywords' نمی‌تواند خالی باشد.")
        return data


class NewsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'short_description', 'category', 'keywords', 'news_text'] 

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

    class Meta:
        model = User
        fields = ['email','id', 'username', 'profile']

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

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
    
class AdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = [
            'id', 'title', 'link', 'banner', 'location',
            'start_date', 'expiration_date', 'status'
        ]    
class AdvertisingCreateUpdateSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    class Meta:
        model = Advertising
        fields = [
            'title', 'link', 'banner', 'location',
            'start_date', 'expiration_date', 'status'
        ]
        
    def get_status(self, obj):
        return "approved" if obj.status else "rejected"

class AdminAdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = ['id', 'location', 'start_date', 'expiration_date', 'status']
        
    def get_status(self, obj):
        return "approved" if obj.status else "pending"

class PublicAdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = ['id', 'link', 'banner', 'location']

class NewsSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'subtitle', 'content', 'created_at', 'author']


# class OperationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Operation
#         fields = ['id', 'news', 'operation_type', 'performed_at']
        
# class AdminAdvertisingSerializer(serializers.ModelSerializer):
#     status = serializers.SerializerMethodField()

#     class Meta:
#         model = Advertising
#         fields = ['id', 'location', 'start_date', 'expiration_date', 'status']

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'phone_number']

# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer()
    
# class AddUserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['name', 'phone_number', 'password', 'confirm_password', 'role']

#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords do not match")
#         return data

#     def create(self, validated_data):
#         user = User(
#             name=validated_data['name'],
#             phone_number=validated_data['phone_number'],
#             role=validated_data['role'],
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user