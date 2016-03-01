from django.contrib import admin

# Register your models here.

from .models import UserStatus, Message

admin.site.register(UserStatus)
admin.site.register(Message)