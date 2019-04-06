from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.auth import login, get_user, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User


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
CHANNEL_GROUP_NAME = "MRP_GLOBAL"


class SyncAinaConsumer(WebsocketConsumer):
    def connect(self):
        # Join a channel group called "MRP_GLOBAL".
        async_to_sync(self.channel_layer.group_add)(
            CHANNEL_GROUP_NAME,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_node):
        # Leave the group on disconnect.
        async_to_sync(self.channel_layer.group_discard)(
            CHANNEL_GROUP_NAME,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        # serialize json string to python dictionary
        client_data = json.loads(text_data)

        """
        If client wants to authenticate, they send authorization as the type together with credentials.
        """
        if client_data['type'] == 'authorization':
            self._login_user(client_data)

        elif client_data['type'] == 'gps':
            self._receive_gps(client_data)
        elif client_data['type'] == 'message':
            print(client_data['message'])
        else:
            self.send(text_data=json.dumps({
                'type':'error',
                'message':'Invalid type sent, closing connection... ' + 
                client_data['type']
            }))
            self.close()

    
    def global_message(self, event):
        print(event)
        

    def _login_user(self, client_data):
        # authenticate with django models
        user = authenticate(
            username=client_data['username'],        
            password=client_data['password'])

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
                uname = client_data['username']
                self.send(text_data=json.dumps({
                    'type':'success',
                    'message':'User logged in.',
                    'id' : User.objects.get(username__exact=uname).id,
                    'pos' : None,
                    'name' : uname,
                    'group' : User.objects.get(username__exact=uname).groups.get(pk=1).name,
                    'needHelp' : False
                }))
        else:
            self.send(text_data=json.dumps({
                'type':'error',
                'message':'Wrong credentials supplied, closing connection...'
            }))
            self.close()


    def _receive_gps(self, client_data):
        name = client_data['name']
        id = client_data['id']
        pos = client_data['pos']
        group = client_data['group']
        need_help = client_data['needHelp']
        GPS_VALUES[id] = {
            'pos' : pos, 
            'name' : name, 
            'group' : group, 
            'needHelp' : need_help
            }
        self.send(text_data=json.dumps({
            'type': 'gps_values',
            'gps_list': GPS_VALUES
            }))

        async_to_sync(self.channel_layer.group_send)(
            CHANNEL_GROUP_NAME,
            {
                # type has to correspond to a method, global_message.
                'type':'global.message',
                'gps_list': GPS_VALUES
            }
        )