from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class AbstractCreatedAt(models.Model):
	created_at = models.DateTimeField('Fecha', default=now)

	class Meta:
		abstract = True


class Message(AbstractCreatedAt):
	user = models.ForeignKey(User, verbose_name='Usuario', related_name='messages')
	body = models.TextField(blank=True, null=False)
	checked = models.BooleanField(default=False)

	def __str__(self):
		return '{} ({})'.format(self.external_id, self.provider)

	class Meta:
		verbose_name = 'Mensaje'
		verbose_name_plural = 'Mensajes'