from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from.forms import SubtitleForm, AddCategoryForm
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import UserProfile
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
UserProfileSerializer,
OperationSerializer,
PageViewSerializer,
CategorySerializer,
ReporterProfileSerializer,
AddUserSerializer,
NewsSerializer,
NewsEditSerializer,
UserSerializer,
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
News,
Category,
Subtitle,
ReporterProfile,
Operation,
PageView,
Advertising,
Setting,
User, 
Role,
Post,
News,
)          
from .permissions import(
IsOwner,
IsAdminUserOrReadOnly,
)


User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        # چک کردن لاگین بودن کاربر
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
    authentication_classes = []  # در اینجا نوع احراز هویت را مشخص می‌کنیم
    permission_classes = [IsAuthenticated]  # تنها کاربرانی که وارد شده‌اند اجازه دارند

    # اضافه کردن اکشن اختصاصی برای ایجاد خبر
    @action(detail=False, methods=['post'])
    def create_post(self, request, *args, **kwargs):
        # بررسی اینکه آیا کاربر عضو گروه "مولفین" است
        if not request.user.groups.filter(name="مولفین").exists():
            return HttpResponseForbidden("شما اجازه ایجاد خبر ندارید.")
        
        # ایجاد پست جدید
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)  # پست ایجاد شده را برمی‌گرداند
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_news(request):
    title = request.data.get('title')
    content = request.data.get('content')

    if not title or not content:
        return Response({'error': 'Title and content are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # ایجاد خبر
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

        # ایجاد خبر (news creation)
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
            
            # ایجاد لینک بازیابی رمز عبور
            reset_link = f"http://yourfrontend.com/reset-password/{uid}/{token}/"
            
            # ارسال ایمیل
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

# ایجاد یک خبر جدید (برای کاربران احراز هویت‌شده)
class NewsCreate(APIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت شده می‌توانند اقدام کنند

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "خبر با موفقیت ایجاد شد"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (SearchFilter,)  # فعال کردن جستجو
    search_fields = ['title', 'content', 'short_description']  # فیلدهایی که می‌توان جستجو کرد
    pagination_class = None  # می‌توانید پیجینیشن هم اضافه کنید
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_queryset(self):
        """
        این متد queryset را فیلتر می‌کند. می‌توانیم فیلترهای بیشتری اضافه کنیم.
        """
        queryset = News.objects.all()
        # اضافه کردن فیلترهای اضافی به درخواست
        # به عنوان مثال، فیلتر وضعیت اخبار یا دسته‌بندی
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        # فیلتر براساس تاریخ ایجاد (می‌توانید فیلترهای دیگر هم اضافه کنید)
        created_at = self.request.query_params.get('created_at', None)
        if created_at:
            queryset = queryset.filter(created_at__date=created_at)

        return queryset
    
# حذف تبلیغات (فقط برای ادمین‌ها)
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

# مشاهده و ویرایش تبلیغات (فقط برای ادمین‌ها)
class AdvertisingViewSet(viewsets.ModelViewSet):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    authentication_classes = [JWTAuthentication]
    
    # اجازه دسترسی عمومی برای مشاهده تبلیغات
    permission_classes = [AllowAny]  # مشاهده تبلیغات برای همه کاربران

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:  # فقط برای عملیات ایجاد، ویرایش، حذف نیاز به ادمین بودن است
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

# جزئیات خبر بدون نیاز به لاگین
class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]  # اجازه دسترسی به همه کاربران

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)
    
# لیست اخبار تأیید شده بدون نیاز به لاگین
@api_view(['GET'])
@permission_classes([AllowAny])
def news_list(request):
    news = News.objects.filter(is_approved=True)  # تنها اخبار تایید شده نمایش داده می‌شود
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)

# مشاهده و ویرایش تنظیمات (فقط برای ادمین‌ها)
class SettingListView(generics.ListAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

# افزودن تنظیمات جدید
class SettingCreateView(generics.CreateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


# ویرایش تنظیمات
class SettingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

# لیست تبلیغات با امکان جستجو
class AdvertisingListView(generics.ListAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['onvan_tabligh', 'location']  
    permission_classes = [AllowAny]  # AllowAny برای دسترسی عمومی
    
# افزودن تبلیغ جدید (فقط برای ادمین‌ها)
class AdvertisingCreateView(generics.CreateAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    
# ویرایش تبلیغ (فقط برای ادمین‌ها)
class AdvertisingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

# حذف تبلیغ (فقط برای ادمین‌ها)
class AdvertisingDeleteView(generics.DestroyAPIView):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

# لیست و فیلتر کاربران
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'phone_number', 'role__name']  
    permission_classes = [AllowAny]  # AllowAny برای دسترسی عمومی
    
# افزودن کاربر (فقط برای ادمین‌ها)
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()
        # ارسال پیام به موبایل کاربر جدید (در صورت نیاز)
        return Response({'detail': 'User created successfully'})
    
# عملیات ویرایش و حذف کاربر (فقط برای ادمین‌ها)
class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

# ویرایش دسته‌بندی‌ها (فقط برای ادمین‌ها)
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


# حذف دسته‌بندی‌ها (فقط برای ادمین‌ها)
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

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReporterProfile.objects.all()
    serializer_class = ReporterProfileSerializer

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

# ویرایش و حذف خبر (مالکیت بررسی شده)
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

    
# سایر ویو‌ها
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت شده می‌توانند خبر ایجاد کنند

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

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    
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

# لیست دسته‌بندی‌ها
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # AllowAny برای دسترسی عمومی

# جزئیات یک دسته‌بندی خاص
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    
class NewsUpdateView(UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # مشاهده عمومی، ویرایش نیازمند احراز هویت

class NewsSearchView(APIView):
    
    @permission_classes([AllowAny])  # استفاده از دکوراتور به درستی

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")
        # جستجو در اخبار بر اساس query
        results = News.objects.filter(title__icontains=query)
        serialized_results = ...  # سریالایز کردن خروجی
        return Response({"message": "News search works!"})
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def news_search(request):
        query = request.GET.get("query")
        results = News.objects.filter(title__icontains=query)
        serialized_results = ...  # سریالایز کردن خروجی
        return Response(serialized_results)
    
class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت شده می‌توانند دسترسی داشته باشند
    
    def perform_create(self, serializer):
        # اطمینان حاصل می‌کنیم که "reporter" به کاربری که خبر را ایجاد کرده نسبت داده شود.
        serializer.save(reporter=self.request.user)
        
    def post(self, request, *args, **kwargs):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        # سریالایز کردن داده‌ها
        serializer = NewsSerializer(data=request.data, context={'request': request})  # ارسال context با request
        if serializer.is_valid():
            serializer.save()  # خبر جدید را ذخیره می‌کند

            # ذخیره خبر
            news = serializer.save()
            
            # اضافه کردن کیوردها به خبر
            keywords = request.data.get('keywords', [])
            for keyword_name in keywords:
                news.add_keyword(keyword_name)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ویوی لیست تبلیغات برای ادمین
class AdminAdvertisingListView(ListAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = AdminAdvertisingSerializer
    queryset = Advertising.objects.all()
    
# ویوی لیست تبلیغات برای کاربران
class PublicAdvertisingListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicAdvertisingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['location']
    
    def get_queryset(self):
        # فیلتر تبلیغات تایید شده که تاریخ انقضای آن‌ها نگذشته باشد
        return Advertising.objects.filter(
            status=True,
            expiration_date__gte=timezone.now()
        )
        
