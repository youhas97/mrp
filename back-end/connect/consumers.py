from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.auth import login, get_user, logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

class SyncAinaConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_node):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        if text_data_json['type'] == 'authorization':
            user = authenticate(
                username=text_data_json['username'],        password=text_data_json['password'])

            if user is not None:
                async_to_sync(login)(self.scope, user)
                self.scope["session"].save()
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
                        'message':'User logged in.'
                    }))
                    print("Logged in")
            else:
                self.send(text_data=json.dumps({
                    'type':'error',
                    'message':'Wrong credentials supplied, closing connection...'
                }))
                self.close()
        
        else:
            self.send(text_data=json.dumps({
                'type':'error',
                'message':'Invalid type sent, closing connection...'
            }))
            self.close()