from django.shortcuts import render, render_to_response
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse

import json

# Create your views here.


@csrf_exempt
def get_update(request):
	print('OK1')
	if request.method == 'POST':
		data = json.loads(request.body)
		print(data['message'])
		print(data['message']['chat'])

	return HttpResponse('OK')
