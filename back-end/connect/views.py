from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from base64 import b64decode
from django.contrib.auth.models import User
from django.db.models import When
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
import json, re
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Return this response if login credentials do not match.
def unauth_access(reason = "None"):
    response = HttpResponse("Unauthorized access: " + reason, status=401)
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

            if not User.objects.filter(username__exact=uname).exists():
                print("No match found")
                return unauth_access("Username does not exist.")
                
            user = User.objects.get(username__exact=uname)
            if not check_password(pword, user.password):
                print("Password didn't match")
                return unauth_access("Wrong password.")


            data = {'message':'Username logged in'}
            response = JsonResponse(data)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return unauth_access("Missing Authorization header.")


"""
Return a 400 Bad Request if request contains invalid username and/or password.
"""
def invalid_credentials(reason="Invalid username and/or password."):
    response['Access-Control-Allow-Origin'] = '*'
    response = HttpResponse(reason)
    response.status = 400
    return response

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uname=data['username']
        pword=data['password']
        print("Username: " + uname + "\nPassword: " + pword)
        # TODO: Check username and password for validity before creating a user.
        """if not re.match("^[a-zA-Z]+[a-zA-Z0-9_+-.@]*$", uname) \
            or len(uname) < 8 \
            or len(uname) > 150 \
            or len(pword) < 8 \
            or 
            return invalid_credentials()"""


        User.objects.create(
            username=data['username'], 
            password=make_password(data['password'])
            )
        return HttpResponse()