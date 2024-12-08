# پروژه بک‌اند پلتفرم خبرگزاری


_این پروژه شامل بک‌اند یک پلتفرم خبرگزاری است که با استفاده از Django و Django REST Framework توسعه داده شده است. هدف این پروژه ارائه یک سیستم کامل برای مدیریت اخبار، کاربران، جستجو و دسته‌بندی محتوا است.


# ویژگی‌های پروژه

احراز هویت کاربران:
ثبت‌نام و ورود امن با استفاده از JWT (توکن‌های وب JSON) از طریق پکیج SimpleJWT.

مدیریت اخبار:
امکان ایجاد، خواندن، ویرایش و حذف خبرها، دسته‌بندی‌ها و برچسب‌ها.

جستجو و فیلتر پیشرفته:
قابلیت جستجوی متنی کامل با استفاده از Haystack و فیلتر کردن بر اساس دسته‌بندی با پکیج django-filters.

پشتیبانی از CORS:
تنظیم شده برای مدیریت درخواست‌های کراس اوریجین با django-cors-headers.

صف وظایف غیرهمزمان:
انجام وظایف پس‌زمینه با استفاده از Celery و Redis.

مستندسازی API:
مستندات تعاملی با استفاده از پکیج drf-yasg.

مدیریت تصاویر:
پردازش و بهینه‌سازی تصاویر با استفاده از کتابخانه Pillow.

گسترش پنل مدیریت:
امکانات بیشتر برای مدیریت با استفاده از django-extensions.


# تکنولوژی‌های استفاده شده

فریم‌ورک اصلی: Django 5.1.2
API REST: Django REST Framework 3.15.2
پایگاه داده: PostgreSQL (قابل جایگزینی با هر پایگاه داده‌ای که توسط Django پشتیبانی می‌شود)
صف وظایف: Celery 5.3.0
جستجو: Elasticsearch (با استفاده از Django Haystack)
مدیریت تصاویر: Pillow 11.0.0

# مراحل نصب

۱.کلون کردن مخزن:

git clone https://github.com/Daryagrs1376/news_website.git
cd news_website

2.ایجاد محیط مجازی:

python -m venv venv

# فعال سازی محیط مجازی در لینوکس
source venv/bin/activate  

# فعال سازی محیط مجازی در ویندوز
venv\Scripts\activate

# با اجرای دستور زیر تمام پکیج های روی پروژه را نصب کن
- pip install -r requirements.txt

# لیست پکیج‌ها و دستورات نصب
_ در ادامه لیستی از تمام پکیج‌های استفاده شده در پروژه همراه با نسخه‌ی به‌روز و دستور نصب هر پکیج آورده شده است. این دستورها را می‌توانید به صورت جداگانه اجرا کنید یا در فایل requirements.txt قرار دهید.

asgiref: 3.8.2  ==> pip install asgiref==3.8.2
Django==5.2  ==> pip install Django==5.2
djangorestframework==3.16.0  ==> pip install djangorestframework==3.16.0
sqlparse==0.5.4 ==> pip install sqlparse==0.5.4
tzdata==2024.4  ==> pip install tzdata==2024.4
django-cors-headers==4.8.0 ==> pip install django-cors-headers==4.8.0
drf-yasg==1.21.9 ==>  pip install drf-yasg==1.21.9
django-extensions==3.2.5 ==>  pip install django-extensions==3.2.5
djangorestframework-simplejwt==5.4.1 ==> pip install djangorestframework-simplejwt==5.4.1
pillow==11.1.0 ==>  pip install Pillow==11.1.0
django-filters==24.5 ==>  pip install django-filters==24.5
corsheaders==4.0.0 ==>  
rest_framework.authtoken==3.16.0 ==> rest_framework.authtoken (به صورت خودکار در DRF موجود است)نیازی به نصب جداگانه ندارد.
celery==5.3.0  ==>  pip install celery==5.3.0
django-haystack==3.1  ==>  pip install django-haystack==3.1
kavenegar==1.2.6  ==> pip install kavenegar==1.2.6

# با اجرای این دستور پایگاه داده را ایجاد کنید و مهاجرت‌ها را اجرا کن
- python manage.py migrate

# با دستور زیر پروژه را اجرا کن
- python manage.py runserver

# اجرای Celery:

_ celery -A project_name worker --loglevel=info

# مستندات API
_احراز هویت:

POST /api/auth/login/: ورود کاربران
POST /api/auth/register/: ثبت‌نام کاربران

_مدیریت اخبار:

GET /api/news/: لیست تمام اخبار
POST /api/news/: ایجاد خبر جدید
GET /api/news/<id>/: مشاهده جزئیات خبر خاص
PUT /api/news/<id>/: ویرایش خبر
DELETE /api/news/<id>/: حذف خبر

_جستجو و فیلتر:

GET /api/news/?search=<query>: جستجو در اخبار
GET /api/news/?category=<category_id>: فیلتر بر اساس دسته‌بندی
برای اطلاعات بیشتر به مستندات Swagger در مسیر /swagger/ مراجعه کنید.


# منابع
- [مستندات Django REST Framework](https://www.django-rest-framework.org/)


# نویسنده پروژه
"زهرا گروسی"
