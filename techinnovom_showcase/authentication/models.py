# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    has_business = models.BooleanField(default=False)
    host_buisness = models.BooleanField(default=False)
    display = models.BooleanField(default=False)
    plan = models.CharField(max_length=200, blank=True, null=True)
    total = models.IntegerField(default=0)
    totalproduct = models.IntegerField(default=0)
    ref = models.CharField(max_length=200, blank=True, null=True)#the person that referredd you
    points = models.IntegerField(default=0)


class UserUpload(models.Model):

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('NGN', 'Nigerian Naira'),
        # Add more currency options as needed
    ]


    img = models.ImageField(upload_to='uploads/')
    link = models.URLField()
    days = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    end_date = models.DateField(null=True, blank=True)
    is_live = models.BooleanField(default=False)

    def calculate_end_date(self):
        if self.days:
            self.end_date = timezone.now() + timezone.timedelta(days=self.days)
            self.save()

