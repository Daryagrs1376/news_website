from django.core.management.base import BaseCommand
from faker import Faker
from myapp.models import News, Category, Keyword  # اپ و مدل‌ها را تنظیم کنید

class Command(BaseCommand):
    help = 'Populate database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(10):
            category = Category.objects.create(
                title=fake.word(),
                name=fake.word(),
                description=fake.text()
            )
            keyword = Keyword.objects.create(
                word=fake.word(),
                category=category
            )
            News.objects.create(
                title=fake.sentence(),
                content=fake.paragraph(),
                short_description=fake.sentence(),
                news_text=fake.text(),
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
                status=True,
            )
        self.stdout.write(self.style.SUCCESS('Successfully populated database with fake data'))
