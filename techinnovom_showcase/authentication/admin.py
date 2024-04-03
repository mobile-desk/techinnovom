from django.contrib import admin
from .models import CustomUser, UserUpload

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserUpload)