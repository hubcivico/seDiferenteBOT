from django.contrib import admin

# Register your models here.

from .models import UserStatus, Message

class MessageAdmin(admin.ModelAdmin):
	list_display = ('user', 'body', 'created_at', 'checked')
	list_filter = ('user', 'created_at', 'checked')

admin.site.register(UserStatus)
admin.site.register(Message, MessageAdmin)