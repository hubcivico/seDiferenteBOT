from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Create your models here.


class AbstractCreatedAt(models.Model):
	created_at = models.DateTimeField('Fecha', default=now)

	class Meta:
		abstract = True


class UserStatus(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,)
	status = models.IntegerField(default=0)
	page = models.IntegerField(default=0)

	class Meta:
		verbose_name = 'Estado'
		verbose_name_plural = 'Estados'


class Message(AbstractCreatedAt):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', related_name='messages')
	body = models.TextField(blank=True, null=False, max_length=150)
	checked = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Mensaje'
		verbose_name_plural = 'Mensajes'