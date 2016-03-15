from core.models import User


def get_user(chat):
	try:
		return User.objects.get(chat_id=chat['id'])
	except User.DoesNotExist:
		return User.objects.create(chat_id=chat['id'], username=chat['first_name'])