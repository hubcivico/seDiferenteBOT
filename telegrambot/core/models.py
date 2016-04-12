from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=100)
	email = models.CharField(max_length=765, unique=True, null=True)
	chat_id = models.IntegerField(unique=True, null=True)
	first_name = models.TextField()
	date_joined = models.DateTimeField(default=timezone.now)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = UserManager()

	def get_short_name(self):
		return self.username

	def __unicode__(self):
		return self.user

	def __str__(self):
		return str(self.chat_id) + ' - ' + str(self.username)