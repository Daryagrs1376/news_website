import os
import django
import random
from faker import Faker
from django.core.management.base import BaseCommand
from news.models import News, Category  # اصلاح ایمپورت به Category

# تنظیمات برای اجرای اسکریپت
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_website.settings")  # نام پروژه خود را جایگزین کنید
django.setup()

class Command(BaseCommand):
    help = 'Populate fake data'

    # تابع ایجاد دسته‌بندی‌های جعلی
    def populate_categories(self, n=5):
        fake = Faker()
        for _ in range(n):
            name = fake.word().capitalize()
            description = fake.sentence(nb_words=10)

            # افزودن داده به مدل Category
            Category.objects.create(
                name=name,
                description=description
            )

    # تابع ایجاد اخبار جعلی
    def populate_news(self, n=10):
        fake = Faker()
        categories = Category.objects.all()

        for _ in range(n):
            title = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=10)
            published_date = fake.date_time_this_year()
            category = random.choice(categories)

            # افزودن داده به مدل News
            News.objects.create(
                title=title,
                content=content,
                published_date=published_date,
                category=category
            )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("در حال ایجاد داده‌های جعلی..."))
        
        # ابتدا دسته‌بندی‌ها را ایجاد کنید تا در مرحله بعدی برای اخبار استفاده شوند
        self.populate_categories(5)  # تعداد دسته‌بندی‌های جعلی
        self.populate_news(20)  # تعداد اخبار جعلی
        
        self.stdout.write(self.style.SUCCESS("ایجاد داده‌های جعلی به پایان رسید."))
