from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from core.utils import get_user
from core.telegram import send_message, send_keyboard
from .models import UserStatus, Message

import json
import csv

# Create your views here.

# Command register pool
commands = [
	('/start', 'start_command'),
	('/se_diferente', 'diferente_command'),
	('/gente_diferente', 'gente_diferente_command'),
	('/siguiente', 'siguiente_command'),
	('/anterior', 'anterior_command'),
	('/descarga', 'descarga_command'),
]

force_status = [
	(1, 'diferente_command')
]

# Main view
@csrf_exempt
def get_update(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))

		print(data)

		user = get_user(data['message']['chat'])

		# Check if is plain text
		try:
			text = data['message']['text']
			process_update(user, text)
		except KeyError:
			pass

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
		if text == command[0]:
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


def descarga_command(user, text):
	messages = Message.objects.all()

	file = open('test.csv', 'w')
	writer = csv.writer(file)

	for m in messages:
		writer.writerow([m.body])


def render_messages_message(user, messages):
	total_messages = Message.objects.all().order_by('-created_at')
	total_pages = total_messages.count() / 5.0

	text = ''
	for m in messages:
		text += m.body + '\n'

	text += '\n/se_diferente para aportar tu granito de arena!'

	buttons = []
	if user.userstatus.page > 0:
		buttons.append('/anterior')
	if user.userstatus.page < total_pages - 1:
		buttons.append('/siguiente')

	return text, [buttons]

def gente_diferente_command(user, text):
	user.userstatus.page = 0
	user.userstatus.save()

	message, buttons = render_messages_message(user, Message.objects.all().order_by('-created_at')[:5])

	send_keyboard(user, message, buttons)


def siguiente_command(user, text):
	total_messages = Message.objects.all().order_by('-created_at')
	total_pages = total_messages.count() / 5.0

	if user.userstatus.page < total_pages - 1:
		user.userstatus.page += 1
		user.userstatus.save()

		message, buttons = render_messages_message(user, total_messages[user.userstatus.page * 5:user.userstatus.page * 5 + 5])

		send_keyboard(user, message, buttons)
	else:
		gente_diferente_command(user, text)


def anterior_command(user, text):
	total_messages = Message.objects.all().order_by('-created_at')

	if user.userstatus.page > 0:
		user.userstatus.page -= 1
		user.userstatus.save()

		message, buttons = render_messages_message(user, total_messages[(user.userstatus.page + 1) * 5 - 5:(user.userstatus.page + 1) * 5])

		send_keyboard(user, message, buttons)
	else:
		gente_diferente_command(user, text)


def get_status(user):
	try:
		return UserStatus.objects.get(user=user).status
	except UserStatus.DoesNotExist:
		return UserStatus.objects.create(user=user).status