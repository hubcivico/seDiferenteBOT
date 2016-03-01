from django.conf import settings

import requests


def send_message(user, text):
	requests.post(settings.TELEGRAM_URL + '/sendMessage', data={'chat_id': user.chat_id, 'text': text})