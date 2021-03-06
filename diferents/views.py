#coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

from core.utils import get_user
from core.telegram import TelegramBot
from diferentes.models import UserStatus, Message
from django.utils.timezone import now

import json
from datetime import timedelta

# Create your views here.

bot = TelegramBot(settings.TELEGRAM_BOT_TOKEN_DIFERENTS)

# Command register pool
commands = [
	('/start', 'start_command'),
	('/soc_diferent', 'diferente_command'),
	('/gent_diferent', 'gente_diferente_command'),
	('/seguent', 'siguiente_command'),
	('/anterior', 'anterior_command'),
	('/eixir', 'salir_command'),
	('/descarrega', 'descarga_command'),
]

force_status = [
	(1, 'diferente_command')
]

# Main view
@csrf_exempt
def get_update(request):
	if request.method == 'POST':
		data = json.loads(request.body)

		user = get_user(data['message']['chat'])

		# Check if is plain text
		try:
			text = data['message']['text']
			result = process_update(user, text)
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
			return call_method(st[1])

	# Auto-detect command
	for command in commands:
		if text == command[0]:
			return call_method(command[1])


#Commands
def start_command(user, text):
	return bot.send_message(user, 'Benvingut/da %s a diferentsBOT, el canal per a enviar y coneixer característiques que ens fan ser persones diferents.' % str(user.username))


def diferente_command(user, text):
	status = get_status(user)

	if status == 0:
		user.userstatus.status = 1
		user.userstatus.save()
		return bot.send_message(user, 'Que característica et diferència de les demés persones (ex. aspectes físics, rasgs de personalitat, idees polítiques, etc.)?')
	elif status == 1:
		user.userstatus.status = 0
		user.userstatus.save()
		if text != '/cancel_lar':
			Message.objects.create(user=user, body=str(text))
			return bot.send_message(user, 'Gràcies per participar! Ultilitza el comandament /gent_diferent per a saver que ens fa diferents.')


def render_messages_message(user, messages):
	total_messages = Message.objects.filter(checked=True)
	total_pages = total_messages.count() / 5.0

	text = ''
	for m in messages:
		text += m.body + '\n'
	text += '\nUltilitza el comandament /soc_diferent per a aportar la teua caracteristica.'

	buttons = []
	if user.userstatus.page > 0:
		buttons.append('/anterior')
	if user.userstatus.page < total_pages - 1:
		buttons.append('/seguent')
	buttons.append('/eixir')

	return text, [buttons]

def gente_diferente_command(user, text):
	user.userstatus.page = 0
	user.userstatus.save()

	message, buttons = render_messages_message(user, Message.objects.filter(checked=True).order_by('-created_at')[:5])

	return bot.send_keyboard(user, message, buttons)


def siguiente_command(user, text):
	total_messages = Message.objects.filter(checked=True).order_by('-created_at')
	total_pages = total_messages.count() / 5.0

	if user.userstatus.page < total_pages - 1:
		user.userstatus.page += 1
		user.userstatus.save()

		message, buttons = render_messages_message(user, total_messages[user.userstatus.page * 5:user.userstatus.page * 5 + 5])

		return bot.send_keyboard(user, message, buttons)
	else:
		return gente_diferente_command(user, text)


def anterior_command(user, text):
	total_messages = Message.objects.filter(checked=True).order_by('-created_at')

	if user.userstatus.page > 0:
		user.userstatus.page -= 1
		user.userstatus.save()

		message, buttons = render_messages_message(user, total_messages[(user.userstatus.page + 1) * 5 - 5:(user.userstatus.page + 1) * 5])

		return bot.send_keyboard(user, message, buttons)
	else:
		return gente_diferente_command(user, text)


def salir_command(user, text):
	user.userstatus.page = 0
	user.userstatus.save()

	bot.send_message(user, '/gent_diferent quan vulgues!')


def descarga_command(user, text):
	with open('/tmp/se_diferente.txt', 'w') as f:
		messages = Message.objects.filter(checked=True)

		for m in messages:
			f.write('%d/%d/%d' % (m.created_at.day, m.created_at.month, m.created_at.year) + ' ' + m.body + '\n')
		f.close()

		user.userstatus.last_download = now()
		user.userstatus.save()

		return bot.send_document(user, open('/tmp/se_diferente.txt', 'r'))

def get_status(user):
	try:
		return UserStatus.objects.get(user=user).status
	except UserStatus.DoesNotExist:
		return UserStatus.objects.create(user=user).status