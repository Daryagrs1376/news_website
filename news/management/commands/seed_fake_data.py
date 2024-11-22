from faker import Faker
import random
from django.core.management.base import BaseCommand
from news.models import (  # نام مدل‌ها را به اپلیکیشن خود تغییر دهید
    Tokens, Groups, Users, Advertisings, Categories, Dashboards, Features,
    Groupings, Keywords, Locations, NewsSpecialAttributes, Newscategorys,
    News, PageViews, ReporterProfiles, Roles, Settings, SpecialCategories,
    SpecialFeatures, Subtitles
)

fake = Faker("fa_IR")  # تنظیم زبان فارسی

class Command(BaseCommand):
    help = "تولید داده‌های جعلی فارسی برای سایت خبرگذاری"

    def handle(self, *args, **kwargs):
        self.stdout.write("در حال تولید داده‌های جعلی...")

        # تولید داده برای مدل‌های مختلف
        # Tokens
        for _ in range(10):
            Tokens.objects.create(key=fake.uuid4(), user_id=random.randint(1, 100))

        # Groups
        for _ in range(5):
            Groups.objects.create(name=fake.word())

        # Users
        for _ in range(20):
            Users.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_staff=fake.boolean(),
            )

        # Advertisings
        for _ in range(10):
            Advertisings.objects.create(
                title=fake.sentence(nb_words=3),  # عنوان تبلیغ
                content=fake.text(max_nb_chars=300),  # متن تبلیغ
            )

        # Categories
        for _ in range(10):
            Categories.objects.create(name=fake.word())

        # Dashboards
        for _ in range(5):
            Dashboards.objects.create(name=fake.sentence(nb_words=2))

        # Features
        for _ in range(10):
            Features.objects.create(feature_name=fake.word())

        # Groupings
        for _ in range(10):
            Groupings.objects.create(name=fake.word())

        # Keywords
        for _ in range(10):
            Keywords.objects.create(keyword=fake.word())

        # Locations
        for _ in range(10):
            Locations.objects.create(city=fake.city(), country="ایران")

        # News Special Attributes
        for _ in range(10):
            NewsSpecialAttributes.objects.create(attribute=fake.sentence(nb_words=4))

        # Newscategorys
        for _ in range(10):
            Newscategorys.objects.create(name=fake.word())

        # News
        for _ in range(20):
            News.objects.create(
                headline=fake.sentence(nb_words=6),  # تیتر خبر
                content=fake.text(max_nb_chars=500),  # محتوای خبر
                author=fake.name(),  # نویسنده
                published_date=fake.date_time_this_year(),  # تاریخ انتشار
            )

        # Page Views
        for _ in range(10):
            PageViews.objects.create(page_name=fake.word(), views=random.randint(0, 10000))

        # Reporter Profiles
        for _ in range(10):
            ReporterProfiles.objects.create(
                name=fake.name(),  # نام خبرنگار
                email=fake.email(),  # ایمیل خبرنگار
                profile_bio=fake.text(max_nb_chars=200),  # بیوگرافی
            )

        # Roles
        for _ in range(5):
            Roles.objects.create(role_name=fake.job())

        # Settings
        for _ in range(10):
            Settings.objects.create(setting_key=fake.word(), setting_value=fake.word())

        # Special Categories
        for _ in range(10):
            SpecialCategories.objects.create(name=fake.word())

        # Special Features
        for _ in range(5):
            SpecialFeatures.objects.create(name=fake.sentence(nb_words=2))

        # Subtitles
        for _ in range(10):
            Subtitles.objects.create(subtitle_text=fake.sentence(nb_words=5))

        self.stdout.write(self.style.SUCCESS("تولید داده‌های جعلی فارسی با موفقیت انجام شد!"))
