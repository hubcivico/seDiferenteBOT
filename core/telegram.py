from django.conf import settings

import requests
import json


def send_message(user, text):
	json_keyboard = json.dumps({"hide_keyboard": True})
	return requests.post(
		settings.TELEGRAM_URL + '/sendMessage',
		data={
			'chat_id': user.chat_id,
			'text': text,
			'reply_markup': json_keyboard
		}
	)


def send_keyboard(user, text, buttons):
	json_keyboard = json.dumps({
		'keyboard': buttons,
		'one_time_keyboard': True,
		'resize_keyboard': True
	})

	return requests.post(
		settings.TELEGRAM_URL + '/sendMessage',
		data={
			'text': text,
			'chat_id': user.chat_id,
			'reply_markup': json_keyboard
		}
	)