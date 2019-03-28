from django.conf.urls import url

from . import consumers

"""
channels uses routing.py instead of django's urls.py
"""

websocket_urlpatterns = [
    url(r'^ws/connect/$', consumers.SyncAinaConsumer)
]