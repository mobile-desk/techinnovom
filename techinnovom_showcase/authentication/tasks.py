# tasks.py
from celery import shared_task
from datetime import date
from .models import UserUpload

@shared_task
def delete_expired_ads():
    today = date.today()
    expired_ads = UserUpload.objects.filter(end_date=today)
    expired_ads.delete()
