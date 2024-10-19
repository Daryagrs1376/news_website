from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .serializers import CategorySerializer, ReporterProfileSerializer, AddUserSerializer, NewsSerializer, NewsEditSerializer
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
from.models import News, Category, Subtitle, ReporterProfile
from.forms import SubtitleForm, AddCategoryForm
from django.views import View
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwner
from rest_framework import generics, filters
from .serializers import UserSerializer, UserCreateSerializer
from .models import Advertising, Setting, User, Role
from .serializers import AdvertisingSerializer, AdvertisingCreateUpdateSerializer
from rest_framework import generics
from .serializers import SettingSerializer, SettingCreateUpdateSerializer
from rest_framework import viewsets
from .models import News, Category, UserProfile, Operation
from .serializers import UserProfileSerializer, OperationSerializer



# لیست تنظیمات
class SettingListView(generics.ListAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

# افزودن تنظیمات جدید
class SettingCreateView(generics.CreateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingCreateUpdateSerializer

# ویرایش تنظیمات
class SettingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingCreateUpdateSerializer

# لیست تبلیغات با امکان جستجو
class AdvertisingListView(generics.ListAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['onvan_tabligh', 'location']  # فیلتر بر اساس عنوان و موقعیت

# افزودن تبلیغ جدید
class AdvertisingCreateView(generics.CreateAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingCreateUpdateSerializer

# ویرایش تبلیغ
class AdvertisingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingCreateUpdateSerializer

# حذف تبلیغ
class AdvertisingDeleteView(generics.DestroyAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer


# لیست و فیلتر کاربران
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'mobile', 'role__name']  # فیلتر بر اساس نام، موبایل و نقش

# اضافه کردن کاربر
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # ارسال پیام به موبایل کاربر جدید (پیاده‌سازی شده با سیستم پیام‌رسانی)
        # send_password_to_user(user.mobile, user.password)
        return Response({'detail': 'User created and password sent to mobile'})

# عملیات ویرایش و حذف کاربر
class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
    else:
        form = AddCategoryForm(instance=category)

        return JsonResponse({"message": "Category edited successfully!"})
    return JsonResponse({"error": "Only POST method is allowed"}, status=400)

def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            onvan = form.cleaned_data['onvan']
            main_category = form.cleaned_data['main_category']

    else:
        form = AddCategoryForm()

        return JsonResponse({"message": "Category added successfully!"})
    return JsonResponse({"error": "Only POST method is allowed"}, status=400)

def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many= True)
        return JsonResponse({"message": "Category list"})
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class CategoryDetail(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class AddCategory(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return JsonResponse({"message": "Category deleted successfully!"})
    return JsonResponse({"error": "Only POST method is allowed"}, status=400)

def subtitle_list(request):
    subtitles = Subtitle.objects.all()
    return render(request, 'subtitle_list.html', {'subtitles': subtitles})

def add_subtitle(request):
    if request.method == 'POST':
        form = SubtitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subtitle-list')
    else:
        form = SubtitleForm()
    return render(request, 'add_subtitle.html', {'form': form})

class SubtitleList(View):
    def get(self, request):
        subtitles = Subtitle.objects.all()
        return render(request, 'news/subtitle_list.html', {'subtitles': subtitles}) 
    
class AddSubtitle(View):
    def get(self, request):
        form = SubtitleForm()
        return render(request, 'news/add_subtitle.html', {'form': form}) 

    def post(self, request):
        form = SubtitleForm(request.POST) 
        if form.is_valid():
            form.save() 
            return redirect('subtitle-list')  
        return render(request, 'news/add_subtitle.html', {'form': form})  

def edit_subtitle(request, pk):
    subtitle = get_object_or_404(Subtitle, pk=pk)
    if request.method == "POST":
        form = SubtitleForm(request.POST, instance=subtitle)
        if form.is_valid():
            form.save()
            return redirect('some_view_name')  
    else:
        form = SubtitleForm(instance=subtitle)
    return render(request, 'template_name.html', {'form': form})

def delete_subtitle(request, pk):
    subtitle = get_object_or_404(Subtitle, pk=pk)
    if request.method == "POST":
        subtitle.delete()
        return redirect('some_view_name') 
    return render(request, 'template_name.html', {'subtitle': subtitle})

# TODO: change this to UserListCreateView (انجام شد)
class UserListCreateView(generics.ListCreateAPIView):
    # TODO: change this to User.objects.all() (انجام شد)
    queryset = User.objects.all()
    serializer_class = ReporterProfileSerializer

# TODO: change this to UserProfileDetailView (انجام شد)
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReporterProfile.objects.all()
    serializer_class = ReporterProfileSerializer

class NewsList(APIView):
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TODO:only owner must can delete news(انجام شد)
class NewsDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # اگر درخواست DELETE بود، چک کنیم که فقط صاحب خبر اجازه حذف داشته
        if self.request.method == 'DELETE':
            return [IsOwner()]
        return super().get_permissions()

    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            return None

    def get(self, request, pk):
        news = self.get_object(pk)
        if news is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, pk):
        news = self.get_object(pk)
        if news is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NewsEditSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = self.get_object(pk)
        if news is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # هر خبرنگار فقط باید بتونه خبر خودش رو پاک بکنه (انجام شد)
        if news.reporter != self.request.user:
            raise PermissionDenied("Only the owner of this news can delete it.")
        
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ویوست News برای مدیریت اخبار
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q')
        if query:
            news = self.queryset.filter(title__icontains=query)
            serializer = self.get_serializer(news, many=True)
            return Response(serializer.data)
        return Response({"message": "No search query provided."})

# ویوست Category برای فیلتر دسته‌بندی‌ها
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ویوست UserProfile برای مدیریت پروفایل کاربران
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['patch'])
    def change_phone(self, request, pk=None):
        profile = self.get_object()
        new_phone = request.data.get('phone_number')
        profile.phone_number = new_phone
        profile.save()
        return Response({"message": "Phone number updated successfully."})

    @action(detail=False, methods=['patch'])
    def change_username(self, request, pk=None):
        user = request.user
        new_username = request.data.get('username')
        user.username = new_username
        user.save()
        return Response({"message": "Username updated successfully."})

# ویوست Operation برای ویرایش و حذف اخبار
class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer