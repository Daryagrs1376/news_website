from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate fake data for the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating fake data...")
        # کد تولید داده‌های جعلی
        self.stdout.write(self.style.SUCCESS("Fake data generation completed!"))
