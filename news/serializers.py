from rest_framework import serializers
from .models import User
from .models import News
from .models import Category
from .models import ReporterProfile



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