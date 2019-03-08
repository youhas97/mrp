from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from base64 import b64decode
from django.contrib.auth.models import User
from django.db.models import When
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

# Create your views here.

# Return this response if login credentials do not match.
def unauth_access(reason = "None"):
    response = HttpResponse("Unauthorized access: " + reason)
    response['Access-Control-Allow-Origin'] = '*'
    response['WWW-Authenticate'] =  'Basic realm="Access to Aina website", charset="UTF-8"'
    response.status = 401
    return response

def login(request):
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'authorization'
        return response
    elif request.method == 'GET':
        if 'HTTP_AUTHORIZATION' in request.META:
            decoded_string = b64decode(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).decode("UTF-8")
            uname, pword = decoded_string.split(':')

            user = None
            try:
                user = User.objects.get(username__exact=uname)
            except ObjectDoesNotExist:
                print("No match found")
                return unauth_access("Username does not exist.")

            if not check_password(pword, user.password):
                print("Password didn't match")
                return unauth_access("Wrong password.")


            data = {'message':'Username logged in'}
            response = JsonResponse(data)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return unauth_access("Missing Authorization header.")