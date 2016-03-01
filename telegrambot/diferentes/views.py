from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from core.utils import get_user
from core.telegram import send_message
from .models import UserStatus, Message

import json

# Create your views here.

# Command register pool
commands = [
	('/start', 'start_command'),
	('/se_diferente', 'diferente_command'),
	('/gente_diferente', 'more_diferente_command'),
]

force_status = [
	(1, 'diferente_command')
]

# Main view
@csrf_exempt
def get_update(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		user = get_user(data['message']['chat'])
		process_update(user, data['message']['text'])

	return HttpResponse('')


# Process the incoming message
def process_update(user, text):
	def call_method(method_name):
		possibles = globals().copy()
		possibles.update(locals())
		method = possibles.get(method_name)
		if not method:
			raise NotImplementedError("Method %s not implemented" % method_name)
		method(user, text)

	status = get_status(user)

	# Cast determinated status
	for st in force_status:
		if status == st[0]:
			call_method(st[1])

	# Auto-detect command
	for command in commands:
		if text in command[0]:
			call_method(command[1])


#Commands
def start_command(user, text):
	send_message(user, 'Bienvenido a SeDiferente, ¿Qué te hace diferente?')


def diferente_command(user, text):
	status = get_status(user)

	if status == 0:
		send_message(user, 'Dinos ahora que es lo que te hace diferente ;D')
		user.userstatus.status = 1
		user.userstatus.save()
	elif status == 1:
		Message.objects.create(user=user, body=text)
		send_message(user, 'Gracias por participar! /gente_diferente para nuevas experiencias!')
		user.userstatus.status = 0
		user.userstatus.save()


def more_diferente_command(user, text):
	messages = Message.objects.all().order_by('-created_at')[:5]

	text = ''
	for m in messages:
		text += m.body + '\n'
	text += '/se_diferente para aportar tu granito de arena!'

	send_message(user, text)


def get_status(user):
	try:
		return UserStatus.objects.get(user=user).status
	except UserStatus.DoesNotExist:
		return UserStatus.objects.create(user=user).status