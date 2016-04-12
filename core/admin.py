from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': (
			'username', 'password', 'email', 'chat_id', 'is_active', 'is_staff', 'is_superuser',
			'groups', 'user_permissions')}),
	)

	list_display = ('username',)
	ordering = ('email',)

admin.site.register(User, CustomUserAdmin)