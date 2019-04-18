import pytest

from django.test import TestCase
from channels.testing import HttpCommunicator, WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase
from .consumers import SyncAinaConsumer
from mysite.routing import application
from django.contrib.auth.models import User, Group

# Create your tests here.

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.asyncio]


async def test_consumer_successful_login():
    """Test if we can login successfully."""
    communicator = WebsocketCommunicator(application, "ws/connect/")
    connected, subprotocol = await communicator.connect()
    user = User.objects.create_user(username='admin', password='kandidat11')
    Group.objects.create(name="test_group")
    Group.objects.get(name="test_group").user_set.add(user)
    assert connected
    await communicator.send_json_to({
        'type':'authorization',
        'username':'admin',
        'password':'kandidat11'
    })
    response = await communicator.receive_json_from()
    print(response['message'])
    assert response['type'] == 'success'
    assert response['message'] == 'User logged in.'

    await communicator.disconnect()


async def test_consumer_fail_login():
    """Test that a user that doesn't exist can't perform a login."""
    communicator = WebsocketCommunicator(application, "ws/connect/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_json_to({
        'type':'authorization',
        'username':'imaginary_user',
        'password':'imgainary_password'
    })
    response = await communicator.receive_json_from()
    assert response['type'] == 'error'
    assert response['message'] == \
        'Wrong credentials supplied, closing connection...'

    await communicator.disconnect()


async def test_sending_invalid_type():
    communicator = WebsocketCommunicator(application, "ws/connect/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_json_to({
        'type':'invalid type'
    })
    response = await communicator.receive_json_from()
    assert response['type'] == 'error'
    assert response['message'] == \
        'Invalid type sent, closing connection... ' + 'invalid type'

    await communicator.disconnect()
