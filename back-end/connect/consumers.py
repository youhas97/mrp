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
        elif client_data['type'] == 'gps_alert':
            self._receive_alert(client_data)
        elif client_data['type'] == 'gps_cancel_alert':
            self._receive_alert(client_data)
        else:
            self.send(text_data=json.dumps({
                'type':'error',
                'message':'Invalid type sent, closing connection... ' + 
                client_data['type']
            }))
            self.close()
        

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
                uname =  self.scope["user"].username
                self.send(text_data=json.dumps({
                    'type':'success',
                    'message':'User logged in.',
                    'id' : User.objects.get(username__exact=uname).id,
                    'pos' : None,
                    'fname' : User.objects.get(username__exact=uname).first_name,
                    'group' : User.objects.get(username__exact=uname).groups.all()[0].name,
                    'needHelp' : False,
                    'username': uname,
                }))
        else:
            self.send(text_data=json.dumps({
                'type':'error',
                'message':'Wrong credentials supplied, closing connection...'
            }))
            self.close()


    def _receive_gps(self, client_data):
        client_data['type'] = 'gps_data'
        data = {
            self.scope["user"].username: client_data
        }

        async_to_sync(self.channel_layer.group_send)(
            CHANNEL_GROUP_NAME,
            {
                # type has to correspond to a method, global_message.
                'type': 'broadcast.event',
                'sent_from': self.scope["user"].username,
                'client_data': data
            }
        )

    def _receive_alert(self, client_data):
        async_to_sync(self.channel_layer.group_send)(
            CHANNEL_GROUP_NAME,
            {
                'type': 'broadcast.event',
                'sent_from': self.scope["user"].username,
                'client_data': client_data
            }
        )


    def broadcast_event(self, event):
        client_data = event['client_data']
        print(client_data)
        # Don't broadcast to self.
        if(self.scope["user"].username != event['sent_from']):
            self.send(text_data=json.dumps(client_data))