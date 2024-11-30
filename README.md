# پروژه API بک‌اند خبرگذاری

- این پروژه یک API برای سایت خبرگذاری است که به کاربران اجازه می‌دهد خبرها را مشاهده کنند و اطلاعات مختلفی از اخبار را دریافت کنند.


# ویژگی‌های پروژه
- مشاهده لیست اخبار
- جستجوی اخبار
- دسته‌بندی اخبار بر اساس موضوعات
- احراز هویت کاربران


# پیش‌نیازها
- Python 3.8 یا بالاتر
- Django 3.x
- Django REST framework
- rest_framework
- rest_framework.authtoken
- corsheaders
- drf_yasg
- django_extensions


# نصب و راه‌اندازی

۱. ابتدا مخزن پروژه را کلون کنید یا فایل‌های پروژه را دانلود کنید:

``bash
- git clone git@github.com:Daryagrs1376/ne
ws_website.gi

# بعد از طریق دستور زیر وارد پوشه پروژه شوید
- cd news_website/

# بهد محیط مجازی بسازید
- python -m venv env

# مرحله بعد محیط مجازی را فعال کنید

# فعال سازی محیط مجازی در لینوکس
- source env/bin/activate 

# فعال سازی محیط مجازی در ویندوز
- env\Scripts\activate


# با اجرای دستور زیر تمام پکیج های روی پروژه را نصب کن
- pip install -r requirements.txt


# با اجرای این دستور پایگاه داده را ایجاد کنید و مهاجرت‌ها را اجرا کن
- python manage.py migrate


# با دستور زیر پروژه را اجرا کن
- python manage.py runserver


#### ۶. استفاده از API (Usage)
مثال‌هایی از درخواست‌هایی که کاربران می‌توانند به API بفرستند، به همراه پاسخ‌های احتمالی آن‌ها را ذکر کنید.

```markdown
## استفاده از API

- **مشاهده لیست اخبار**:

  `GET /api/news/`

- **جستجو در اخبار**:

  `GET /api/news/?search=<keyword>`

- **دریافت جزئیات یک خبر خاص**:

  `GET /api/news/<id>/`


# منابع
- [مستندات Django REST Framework](https://www.django-rest-framework.org/)


# نویسنده پروژه
"زهرا گروسی"
