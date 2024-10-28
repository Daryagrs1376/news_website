import sys
import os
import random
from faker import Faker

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_website.settings")

import django
django.setup()

# ایجاد یک نمونه از Faker برای تولید داده‌های فیک
fake = Faker()

def create_fake_data(n=10):
    # واردات مدل‌ها درون تابع برای جلوگیری از واردات چرخشی
    from news.models import (
        News, Categories, Users, Advertisings, Dashboards, Features, Groupings, Keywords, 
        Locations, NewsSpecialAttributes, Newscategorys, Operations, PageViews, 
        ReporterProfiles, Roles, Settings, SpecialCategories, SpecialFeatures, UserProfiles
    )

    # ایجاد دسته‌بندی‌های فیک
    for _ in range(n):
        Categories.objects.get_or_create(name=fake.word())

    # ایجاد نویسنده فیک (Users)
    for _ in range(n):
        Users.objects.get_or_create(username=fake.user_name())

    # ایجاد اخبار فیک (News)
    for _ in range(n):
        category = Categories.objects.order_by('?').first()  # انتخاب دسته‌بندی تصادفی
        author = Users.objects.order_by('?').first()  # انتخاب نویسنده تصادفی

        News.objects.create(
            title=fake.sentence(),
            content=fake.paragraph(nb_sentences=5),
            author=author,
            category=category,
            published_date=fake.date_time_this_year(),
            status=random.choice(['published', 'draft'])
        )
    
    # ایجاد فیک دیتا برای مدل‌های دیگر (اختیاری)
    for _ in range(n):
        Advertisings.objects.get_or_create(description=fake.text(max_nb_chars=100))
        Dashboards.objects.get_or_create(name=fake.word())
        Features.objects.get_or_create(name=fake.word())
        Groupings.objects.get_or_create(name=fake.word())
        Keywords.objects.get_or_create(word=fake.word())
        Locations.objects.get_or_create(name=fake.city())
        NewsSpecialAttributes.objects.get_or_create(attribute=fake.word())
        Newscategorys.objects.get_or_create(name=fake.word())
        Operations.objects.get_or_create(operation_name=fake.word())
        PageViews.objects.get_or_create(page_url=fake.url())
        ReporterProfiles.objects.get_or_create(name=fake.name())
        Roles.objects.get_or_create(role_name=fake.job())
        Settings.objects.get_or_create(setting_name=fake.word())
        SpecialCategories.objects.get_or_create(name=fake.word())
        SpecialFeatures.objects.get_or_create(feature_name=fake.word())
        UserProfiles.objects.get_or_create(user=Users.objects.order_by('?').first())

# فراخوانی تابع برای ایجاد داده‌های فیک
create_fake_data(20)  # به تعداد دلخواه داده فیک ایجاد کنید
