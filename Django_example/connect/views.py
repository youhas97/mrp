from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.

def login(request):
    if request.method == 'OPTIONS':
        print("in options")
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'authorization'
        return response
    elif request.method == 'GET':
        if 'HTTP_AUTHORIZATION' in request.META:
            print("in auth")
            data = {
                'message:':'success',
                'creds':request.META['HTTP_AUTHORIZATION'],
            }
            
            response = JsonResponse(data)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            print("in else")
            data = {'message':'401 Unauthorized access'}
            response = JsonResponse(data)
            response['Access-Control-Allow-Origin'] = '*'
            return response