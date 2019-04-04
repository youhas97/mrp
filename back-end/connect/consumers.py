from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.auth import login, get_user, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser


"""
SyncAinaConsumer is a channels websocket consumer that is used when clients want to connect to the back-end. Front-end will need to authenticate before they can send other information. Any information sent before user has authenticated will result in the connection closing. Likewise, any invalid type for a socket message will result in the connection closing.

This websocket consumer will mostly be used as a means to communicate GPS locations between other websocket connections to the back-end. For every GPS location received from a client, the consumer will broadcast it to every other client connected. 

Types:
'authorization'
'success'
'error'
'gps'
"""
GPS_VALUES = {}


class SyncAinaConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_node):
        pass

    def receive(self, text_data=None, bytes_data=None):
        # serialize json string to python dictionary
        text_data_json = json.loads(text_data)

        """
        If client wants to authenticate, they send authorization as the type together with credentials.
        """
        if text_data_json['type'] == 'authorization':

            # authenticate with django models
            user = authenticate(
                username=text_data_json['username'],        password=text_data_json['password'])

            if user is not None:
                # login the user
                async_to_sync(login)(self.scope, user)
                self.scope["session"].save()

                # Check if user has a session
                if isinstance(async_to_sync(get_user)(self.scope),
                    AnonymousUser):
                    self.send(text_data=json.dumps({
                        'type':'error',
                        'message':'Could not login user, closing connection...'
                    }))
                    self.close()
                else:
                    self.send(text_data=json.dumps({
                        'type':'success',
                        'message':'User logged in.',
                        'id' : User.objects.get(username__exact=text_data_json['username']).id,
                        'pos' : None,
                        'name' : text_data_json['username'],
                        'group' : 14,
                        'needHelp' : False
                    }))
                    print("Logged in")
            else:
                self.send(text_data=json.dumps({
                    'type':'error',
                    'message':'Wrong credentials supplied, closing connection...'
                }))
                self.close()
        elif text_data_json['type'] == 'gps':
            name = text_data_json['name']
            id = text_data_json['id']
            pos = text_data_json['pos']
            group = text_data_json['group']
            need_help = text_data_json['needHelp']
            GPS_VALUES[id] = {'pos' : pos, 'name' : name, 'group' : group, 'needHelp' : need_help}
            self.send(text_data=json.dumps({
                'type': 'gps_values',
                'gps_list': GPS_VALUES
                }))

        elif text_data_json['type'] == 'message':
            print(text_data_json['message'])
        
        else:
            self.send(text_data=json.dumps({
                'type':'error',
                'message':'Invalid type sent, closing connection... ' + text_data_json['type']
            }))
            self.close()