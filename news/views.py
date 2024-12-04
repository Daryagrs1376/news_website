from .utils import send_sms
from .models import News
from .serializers import CommentSerializer
from .serializers import PostSerializer
from rest_framework import generics
from .permissions import IsNotAuthenticated
from.forms import SubtitleForm, AddCategoryForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import now, timedelta
from django.views.generic.dates import ArchiveIndexView
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import(
SessionAuthentication,
TokenAuthentication )
from django.utils.http import (
urlsafe_base64_encode,
urlsafe_base64_decode)
from django.contrib.auth.tokens import (
PasswordResetTokenGenerator)
from rest_framework.generics import(
RetrieveAPIView,
CreateAPIView,
UpdateAPIView,
ListAPIView,
)
from .serializers import(
UserProfileSerializer,
PublicAdvertisingSerializer,
AdminAdvertisingSerializer,
RegisterSerializer,
)
from django.http import (
HttpResponseForbidden,
HttpResponse,
JsonResponse,    
)
from django.shortcuts import (
get_object_or_404, 
redirect,
render,   
)
from rest_framework.exceptions import (
ValidationError,
PermissionDenied,  
)
from rest_framework.decorators import(
api_view,
permission_classes,
authentication_classes,
action,    
)  
from rest_framework import(
status,
viewsets,
generics,
filters,
permissions,    
)
from rest_framework.permissions import(
AllowAny, 
IsAuthenticatedOrReadOnly,
IsAuthenticated,
IsAdminUser,
IsAuthenticated, 
IsAdminUser, 
)
from .serializers import(
AdvertisingSerializer,
AdvertisingCreateUpdateSerializer,
NewsSerializer,
SettingSerializer,
SettingCreateUpdateSerializer,
PageViewSerializer,
CategorySerializer,
ReporterProfileSerializer,
NewsSerializer,
NewsEditSerializer,
UserCreateSerializer,
AdminAdvertisingSerializer,
PublicAdvertisingSerializer,
NewsDetailSerializer,
UserRegistrationSerializer,
PasswordResetRequestSerializer,
PasswordResetSerializer,
RegisterSerializer,
PostSerializer,
)
from.models import(
Comment,
Advertising,
Category,
Subtitle,
ReporterProfile,
UserProfile,
PasswordResetToken,
PageView,
Advertising,
Setting,
User,
OTP, 
Role,
Post,
News,
)          
from .permissions import(
IsOwner,
IsAdminUserOrReadOnly,
)

User = get_user_model()

@api_view(['POST'])
def like_news(request, pk):
    """
    این تابع تعداد لایک‌های یک خبر مشخص را افزایش می‌دهد.
    """
    try:
        news_item = News.objects.get(pk=pk)  # خبر را از دیتابیس پیدا کنید
        news_item.likes += 1  # فرض کنید فیلد likes در مدل شما وجود دارد
        news_item.save()
        return Response({'message': 'News liked successfully!'})
    except News.DoesNotExist:
        return Response({'error': 'News item not found'}, status=404)
    
    def like_news(request, pk):
        return HttpResponse(f"News {pk} liked!")

def send_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        if not phone:
            return JsonResponse({"success": False, "message": "شماره تلفن وارد نشده است"})

        otp_record = OTP.objects.filter(phone=phone).last()
        if otp_record and otp_record.created_at > now() - timedelta(minutes=2):
            return JsonResponse({"success": False, "message": "کد تأیید قبلاً ارسال شده است."})

        otp, created = OTP.objects.update_or_create(phone=phone, defaults={"created_at": now()})

        message = f"کد تأیید شما: {otp.code}"
        send_sms(phone, message)

        return JsonResponse({"success": True, "message": "کد تأیید ارسال شد."})
    return JsonResponse({"success": False, "message": "فقط درخواست POST مجاز است"})

def verify_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        code = request.POST.get("code")
        if not phone or not code:
            return JsonResponse({"success": False, "message": "شماره تلفن یا کد وارد نشده است."})

        otp_record = OTP.objects.filter(phone=phone, code=code).last()
        if not otp_record:
            return JsonResponse({"success": False, "message": "کد تأیید اشتباه است."})

        if otp_record.created_at < now() - timedelta(minutes=5):
            return JsonResponse({"success": False, "message": "کد تأیید منقضی شده است."})
        return JsonResponse({"success": True, "message": "ورود موفقیت‌آمیز بود!"})
    return JsonResponse({"success": False, "message": "فقط درخواست POST مجاز است"})

class NewsArchiveView(ArchiveIndexView):
    model = News  # مدل مرتبط با اخبار
    date_field = "published_date"  # فرض کنید تاریخ انتشار این فیلد است
    template_name = "news_archive.html"  # نام فایل قالب HTML
    
class UserProfileDetailView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class AdvertisingReadView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        advertisement = Advertising.objects.get(pk=pk)
        return Response({'data': advertisement})
class AdvertisementsListView(APIView):
    authentication_classes = []  
    permission_classes = []  

    def get(self, request):
        advertisements = Advertising.objects.all()
        return Response({'data': advertisements})
    
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated] 

class PublicAdvertisingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicAdvertisingSerializer
    permission_classes = [permissions.AllowAny]  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location']  
    search_fields = ['location']   

    def get_queryset(self):
        return Advertising.objects.filter(
            status=True,
            expiration_date__gte=now().date()
        )

class AdminAdvertisingViewSet(viewsets.ModelViewSet):
    queryset = Advertising.objects.all()
    serializer_class = AdminAdvertisingSerializer
    permission_classes = [permissions.IsAdminUser] 
    
class ResetPasswordAPIView(APIView):
    def post(self, request, token):
        try:
            reset_token = PasswordResetToken.objects.get(token=token, is_used=False)
            
            if not reset_token.is_valid():
                raise ValidationError("Token is invalid or expired.")
            
            new_password = request.data.get('password')
            if not new_password:
                return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = reset_token.user
            user.password = make_password(new_password)
            user.save()

            reset_token.is_used = True
            reset_token.save()

            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_404_NOT_FOUND)
        
class RequestPasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            
            token = PasswordResetToken.objects.create(user=user)
            reset_url = f"http://yourdomain.com/reset-password/{token.token}/"
            
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link below to reset your password:\n{reset_url}",
                from_email="no-reply@yourdomain.com",
                recipient_list=[email],
            )
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class RegisterView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"detail": "شما قبلاً لاگین کرده‌اید و نمی‌توانید دوباره ثبت‌نام کنید."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "ثبت‌نام موفقیت‌آمیز بود."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = []  
    permission_classes = [IsAuthenticated]  
    
    @action(detail=False, methods=['post'])
    def create_post(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="مولفین").exists():
            return HttpResponseForbidden("شما اجازه ایجاد خبر ندارید.")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)  
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_news(request):
    title = request.data.get('title')
    content = request.data.get('content')

    if not title or not content:
        return Response({'error': 'Title and content are required.'}, status=status.HTTP_400_BAD_REQUEST)

    news = News.objects.create(title=title, content=content, author=request.user)
    return Response({'message': 'News created successfully!', 'news_id': news.id}, status=status.HTTP_201_CREATED)

class CreateNewsView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        content = request.data.get('content')

        if not title or not content:
            return Response({'error': 'Title and content are required.'}, status=status.HTTP_400_BAD_REQUEST)

        news = News.objects.create(title=title, content=content, author=request.user)
        return Response({'message': 'News created successfully!', 'news_id': news.id}, status=status.HTTP_201_CREATED)

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    permission_classes = [AllowAny]

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = f"http://yourfrontend.com/reset-password/{uid}/{token}/"
            
            send_mail(
                subject="Password Reset Request",
                message=f"Use the following link to reset your password: {reset_link}",
                from_email="noreply@yourdomain.com",
                recipient_list=[email],
            )
            return Response({"message": "ایمیل بازیابی رمز عبور ارسال شد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "لینک معتبر نیست."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordResetSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"message": "رمز عبور با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsCreate(APIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "خبر با موفقیت ایجاد شد"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'published_date']
    ordering_fields = ['published_date']
    search_fields = ['title', 'content', 'short_description']
    pagination_class = None  
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_queryset(self):
        queryset = News.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            created_at = self.request.query_params.get('created_at', None)
        if created_at: 
            queryset = queryset.filter(created_at__date=created_at)
        return queryset
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_advertising(request, id):
    advertising = get_object_or_404(Advertising, id=id)
    advertising.delete()
    return redirect('some_view_name')

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class AdvertisingViewSet(viewsets.ModelViewSet):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    authentication_classes = [JWTAuthentication]
    
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view."})

class MyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You are authenticated!'})

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny] 

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def news_list(request):
    news = News.objects.filter(is_approved=True) 
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)

class SettingListView(generics.ListAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class SettingCreateView(generics.CreateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class AddNewsView(APIView):
    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        content = request.data.get('content')
        keyword_list = request.data.get('keywords', []) 

        news = News.objects.create(title=title, content=content)
        news.add_keywords(keyword_list)

        return Response({"message": "News created successfully!"}, status=status.HTTP_201_CREATED)

class SettingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class AdvertisingListView(generics.ListAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['title', 'location']
    filterset_fields = ['location', 'status']
    permission_classes = [AllowAny] 
    
class AdvertisingCreateView(generics.CreateAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    
class AdvertisingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class AdvertisingDeleteView(generics.DestroyAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'phone_number', 'role__name']  
    permission_classes = [AllowAny]   
    
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({'detail': 'User created successfully'})
    
class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

def edit_category(request, pk):
    if request.method == "POST":
        category = get_object_or_404(Category, pk=pk)
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return JsonResponse({"message": "Category deleted successfully!"})


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

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ReporterProfileSerializer

# class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ReporterProfile.objects.all()
#     serializer_class = ReporterProfileSerializer

class NewsList(APIView):
    def get(self, request):
        news = News.objects.filter(is_approved=True)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsOwner()]
        return super().get_permissions()

    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            return None

    def delete(self, request, pk):
        news = self.get_object(pk)
        if news is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if news.reporter != self.request.user:
            raise PermissionDenied("Only the owner of this news can delete it.")
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated] 
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request):
        query = request.query_params.get('q')
        if query:
            news = self.queryset.filter(title__icontains=query)
            serializer = self.get_serializer(news, many=True)
            return Response(serializer.data)
        return Response({"message": "No search query provided."})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer

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

# class OperationViewSet(viewsets.ModelViewSet):
#     queryset = Operation.objects.all()
#     serializer_class = OperationSerializer
    
class DailyStatsView(APIView):
    def get(self, request):
        filter_type = request.GET.get('filter_type', 'daily')
        today = datetime.today()

        if filter_type == 'daily':
            start_date = today
            end_date = today
        elif filter_type == 'weekly':
            start_date = today - timedelta(days=7)
            end_date = today
        elif filter_type == 'monthly':
            start_date = today.replace(day=1)
            end_date = today
        elif filter_type == 'yearly':
            start_date = today.replace(month=1, day=1)
            end_date = today
        else:
            return Response({"status": "error", "message": "Invalid filter_type"}, status=400)

        stats = PageView.objects.filter(date__range=[start_date, end_date])
        serializer = PageViewSerializer(stats, many=True)
        return Response({"status": "success", "data": serializer.data})
    
class WeeklyStatsView(APIView):
    def get(self, request):
        time_period = request.GET.get('time_period', 'this_week')
        today = datetime.today()

        if time_period == 'today':
            start_date = today
            end_date = today
        elif time_period == 'this_week':
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif time_period == 'this_month':
            start_date = today.replace(day=1)
            end_date = today
        elif time_period == 'yearly':
            start_date = today.replace(month=1, day=1)
            end_date = today
        else:
            return Response({"status": "error", "message": "Invalid time_period"}, status=400)

        stats = PageView.objects.filter(date__range=[start_date, end_date])
        serializer = PageViewSerializer(stats, many=True)
        return Response({"status": "success", "data": serializer.data})

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] 

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    
class NewsUpdateView(UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

    # def get(self, request, *args, **kwargs):
    #     query = request.GET.get("query")
    #     # جستجو در اخبار بر اساس query
    #     results = News.objects.filter(title__icontains=query)
    #     serialized_results = ...  # سریالایز کردن خروجی
    #     return Response({"message": "News search works!"})
    
class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]  
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
        
    def post(self, request, *args, **kwargs):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = NewsSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save()  
            news = serializer.save()
            keywords = request.data.get('keywords', [])
            for keyword_name in keywords:
                news.add_keyword(keyword_name)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminAdvertisingListView(ListAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = AdminAdvertisingSerializer
    queryset = Advertising.objects.all()
    
class PublicAdvertisingListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicAdvertisingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['location']
    
    def get_queryset(self):
        return Advertising.objects.filter(
            status=True,
            expiration_date__gte=timezone.now()
        )
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
 
    
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from .models import UserProfile
# from django.db.utils import IntegrityError

# @swagger_auto_schema(
#     method='post', 
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
#         },
#         required=['phone'],
#     ),
#     responses={200: openapi.Response('Successful Response', openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
#         },
#     ))}
# )
# @api_view(['POST'])
# def send_sms(request):
#     phone = request.data.get('phone')
#     if phone and request.user.is_anonymous:
#         verification_code_number = randint(1000, 9999)
#         verification_code = str(verification_code_number)
#         user = None 
#         try:
#             user = User.objects.create_user(username=phone)
#             UserProfile.objects.create(user=user,phone_number=phone,verification_code=verification_code)
    
#             try:
#                 client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#                 message = client.messages.create(
#                     body=f"Your verification code is {verification_code}",
#                     from_=settings.TWILIO_PHONE_NUMBER,
#                     to=phone
#                 )
#                 return Response({'message': f'User created and SMS verification sent to {phone}'})
#             except Exception as e:
#                 return Response({'message': f'Failed to send SMS: {str(e)}'}, status=500)
           
#         except IntegrityError:
#             user = User.objects.get(username=phone)
#             user.profile.verification_code = verification_code
#             user.profile.save()
#             return Response({'message': 'Waiting to receive verification code!'})
#         return Response({'message': 'fill phone number'})

# @swagger_auto_schema(
#     method='post', 
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
#             'code': openapi.Schema(type=openapi.TYPE_STRING, description='Verification code'),
#         },
#         required=['phone', 'code'],
#     ),
#     responses={200: openapi.Response('Successful Response', openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
#             'code': openapi.Schema(type=openapi.TYPE_STRING, description='Verification code'),
#         },
#     ))}
# )
# @api_view(['POST'])
# def verify_code(request):
#     phone = request.data.get('phone')
#     code = request.data.get('code')
#     return Response({'phone': phone, 'code': code})
