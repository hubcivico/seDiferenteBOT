from django.conf import settings

import requests
import json


class TelegramBot:
	def __init__(self, token):
		self.TOKEN = token

	def send_message(self, user, text):
		json_keyboard = json.dumps({"hide_keyboard": True})
		return requests.post(
			settings.TELEGRAM_BOT_WEB + self.TOKEN + '/sendMessage',
			data={
				'chat_id': user.chat_id,
				'text': text,
				'reply_markup': json_keyboard
			}
		)


	def send_keyboard(self, user, text, buttons):
		json_keyboard = json.dumps({
			'keyboard': buttons,
			'one_time_keyboard': True,
			'resize_keyboard': True
		})

		return requests.post(
			settings.TELEGRAM_BOT_WEB + self.TOKEN + '/sendMessage',
			data={
				'text': text,
				'chat_id': user.chat_id,
				'reply_markup': json_keyboard
			}
		)


	def send_document(self, user, file):
		return requests.post(
			settings.TELEGRAM_BOT_WEB + self.TOKEN + '/sendDocument',
			files={'document': file},
			data={'chat_id': user.chat_id},
		)