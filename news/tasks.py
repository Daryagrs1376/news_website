from celery import shared_task
from .models import Article
from django.utils.timezone import now

@shared_task
def publish_scheduled_articles():
    articles = Article.objects.filter(is_published=False, publish_date__lte=now())
    for article in articles:
        article.is_published = True
        article.save()
