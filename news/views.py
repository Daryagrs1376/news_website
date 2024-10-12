from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import News, User
from .serializers import NewsSerializer, AddUserSerializer, NewsEditSerializer, UserSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AddUserForm
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from rest_framework.decorators import action
from .forms import AddCategoryForm
from django.http import HttpResponse, JsonResponse
from .serializers import UserSerializer 
from django.shortcuts import get_object_or_404
from.models import News
from .models import Subtitle
from .forms import SubtitleForm
from django.views import View



class UserDetail(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
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

class NewsDetail(APIView):
    
    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            return None
        
    def get(self, request, pk):
        news = self.get_object(pk)
        if news is None:
            return Response({'error': 'News not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'title': news.title, 'content': news.content})

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
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class NewsDetail(APIView):
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

        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = self.get_object(pk)
        if news is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserProfile(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get(self, request, username):
        user = self.get_object(username)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    def put(self, request, username):
        user = User.objects.get(username=username)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if user.password != current_password:
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.password = new_password
        user.save()
        return Response({'message': 'Password changed successfully.'})

class SignOut(APIView):
    def post(self, request):
        return Response({'message': 'User signed out successfully.'})
    
def list_users(request):
    query = request.GET.get('search', '')
    users = User.objects.filter(name__icontains=query) if query else User.objects.all()
    return render(request, 'list_users.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            # ارسال پیامک برای رمز عبور
            # your_sms_function(phone_number=form.cleaned_data['phone_number'], password=form.cleaned_data['password'])
            return redirect('list_users')
    else:
        form = AddUserForm()
    return render(request, 'add_user.html', {'form': form})

def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = AddUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = AddUserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('list_users')

class UserList(APIView):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            users = User.objects.filter(name__icontains=search_query)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetail(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def put(self, request, user_id):
        user = self.get_object(user_id)
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = self.get_object(user_id)
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddCategory(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return JsonResponse({"message": "Category deleted successfully!"})
    return JsonResponse({"error": "Only POST method is allowed"}, status=400)

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

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
            return redirect('some_view_name')  # نام view مناسب برای ریدایرکت بعد از ویرایش
    else:
        form = SubtitleForm(instance=subtitle)
    return render(request, 'template_name.html', {'form': form})

def delete_subtitle(request, pk):
    subtitle = get_object_or_404(Subtitle, pk=pk)
    if request.method == "POST":
        subtitle.delete()
        return redirect('some_view_name')  # نام view مناسب برای ریدایرکت بعد از حذف
    return render(request, 'template_name.html', {'subtitle': subtitle})
