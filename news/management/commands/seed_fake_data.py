import random
from faker import Faker
from django.core.management.base import BaseCommand
from news.models import User, News, Category, Keyword, Advertising, Post, Role
from django.contrib.auth import get_user_model


fake = Faker()

class Command(BaseCommand):
    help = 'Seed fake data into the database'

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()  # استفاده از get_user_model برای بارگذاری صحیح مدل User
        categories = list(Category.objects.all())  # تبدیل QuerySet به لیست

        
        # ایجاد 5 کاربر
        for _ in range(5):
            user = User.objects.create_user(username=fake.user_name(), password=fake.password())
            self.stdout.write(f"User {user.username} created")

        # ایجاد 5 دسته‌بندی
        for category_name in ['week', 'guy', 'trouble', 'design', 'decide']:
            category = Category.objects.create(
                title=category_name,
                name=fake.word(),
                description=fake.text()
            )
            self.stdout.write(f"Category {category.title} created")
            
       # ایجاد 10 خبر
        for _ in range(10):
            reporter = random.choice(User.objects.all())  # انتخاب یک کاربر به عنوان خبرنگار
            if reporter:
                news = News.objects.create(
                    title=fake.sentence(),
                    content=fake.text(),
                    reporter=reporter,  # اختصاص کاربر به فیلد reporter
                    is_approved=random.choice([True, False])
                )
                news.categories.set(random.sample(categories, 2))  # انتساب 2 دسته‌بندی به هر خبر
                news.save()
                self.stdout.write(f"News {news.title} created")

                # اضافه کردن کیورد‌ها
                for _ in range(3):  # 3 کیورد به هر خبر اضافه کنید
                    keyword = Keyword.objects.create(word=fake.word(), category=random.choice(categories))
                    news.keywords.add(keyword)

                self.stdout.write(f"Keywords added to News {news.title}")
            else:
                self.stdout.write(self.style.ERROR('No reporter found'))
                
        # ایجاد تبلیغات
        for _ in range(3):  # ایجاد 3 تبلیغ
            ad = Advertising.objects.create(
                title=fake.word(),
                link=fake.url(),
                banner=fake.image_url(),
                location=random.choice(['header', 'sidebar', 'footer']),
                start_date=fake.date_this_year(),
                expiration_date=fake.date_this_year(),
                status=random.choice([True, False])
            )
            self.stdout.write(f"Advertising {ad.title} created")

        # ایجاد پست‌ها
        for _ in range(5):  # ایجاد 5 پست
            post = Post.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                author=random.choice(User.objects.all())
            )
            self.stdout.write(f"Post {post.title} created")

        self.stdout.write(self.style.SUCCESS('Successfully seeded fake data!'))
