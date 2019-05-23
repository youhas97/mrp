from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from base64 import b64decode
from django.contrib.auth.models import User, Group
from django.db.models import When
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
import json, re
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

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


def invalid_credentials(reason):
    """Return a 400 Bad Request if request contains invalid username and/or password."""

    response = HttpResponse(reason, status=400)
    response['Access-Control-Allow-Origin'] = '*'
    response.status = 400
    return response


@csrf_exempt
def register(request):
    """This function will try and register a new account to the database.
    
    It will first check for correct request method. It will then check for 
    invalid credentials, and if no error has occured, an attempt will be made to create
    the user and add it to an existing group using a transaction commit. 
    In case of error, an appropriate response will be returned to the client. """

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'accept, content-type, charset'
        response['Access-Control-Allow-Methods'] = 'POST'
        return response
    if request.method == 'POST':
        data = json.loads(request.body)
        uname = data['username']
        pword = data['password']
        group = data['groupname']
        name = data['name']

        response = check_for_invalid_credentials(uname, pword, group, name)
        if response is not None:
            return response

        """ 
        Create user using a transaction commit and add it to a group. If error occurs 
        inside the transaction, all changes to the database will be rolled back.
        """
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=uname, password=pword, first_name=name)
                db_group = Group.objects.get(name=group)
                db_group.user_set.add(user)
        except DatabaseError:
            response = HttpResponse(
                "Server encountered database error while trying to create user.",
                status=500
                )
            response['Access-Control-Allow-Origin'] = '*'
            return response


        response = HttpResponse("User created!", status=200)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else: 
        response = HttpResponse("Method not allowed.", status=405)
        response.status = 405
        return response

def check_for_invalid_credentials(uname, pword, group, name):
    """ Checks for invalid credentials.

    If invalid credentials are discovered, function will call invalid_credentials()
    which will send a 400 http response to the client. 
    This function returns a http  response if invalid credentials have been detected,
    or None if successful. """

    if not re.match("^[a-zA-Z]+[a-zA-Z0-9_+-.@]*$", uname):
        return invalid_credentials("Invalid characters in username.")
    elif len(uname) < 4:
        return invalid_credentials("Username has to contain at least 4 characters.")
    elif len(uname) > 150:
        return invalid_credentials("Username can max be of length 150.")

    if not re.match("^[a-zA-Z0-9]*$", pword):
        return invalid_credentials("Invalid characters in password.")
    elif len(pword) < 8:
        return invalid_credentials("Password has to contain at least 8 characters.")
    elif len(pword) > 150:
        return invalid_credentials("Password can max be of length 150.")

    if(User.objects.filter(username__exact=uname).exists()):
        return invalid_credentials("Username already exists.")
    elif not (Group.objects.filter(name__exact=group).exists()):
        return invalid_credentials(
            "Group does not exist, please select another group."
            )

    return None
