from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def login(request):
    if 'Authentication' in request.META:
        data = {'message:':'success'}
        return JsonResponse(data)
    else:
        data = {'message':'401 Unauthorized access'}
        response = JsonResponse(data)
        response['Access-Control-Allow-Origin'] = '*'
        return response