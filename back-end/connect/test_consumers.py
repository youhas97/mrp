import pytest
import asyncio
import os
import mysite.settings

from mysite.settings import BASE_DIR
from django.test import TestCase
from channels.testing import HttpCommunicator, WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase
from .consumers import SyncAinaConsumer
from mysite.routing import application
from django.contrib.auth.models import User, Group

pytestmark = [pytest.mark.asyncio, pytest.mark.django_db(transaction=True)]

# Create your tests here.


@pytest.fixture(scope="function")
async def create_and_connect_users(create_user):
    """ Create user objects we can use for testing. 
    
    This fixture will create two users and log them in to the backend
    via websockets. Yields two communicators that can be used by test
    functions. """
    user1 = create_user("test_dummy1", "test_group")
    user2 = create_user("test_dummy2", "test_group")

    communicator1 = WebsocketCommunicator(application, "ws/connect/")
    communicator2 = WebsocketCommunicator(application, "ws/connect/")

    connected1, _ = await communicator1.connect()
    connected2, _ = await communicator2.connect()

    assert connected1
    assert connected2

    # After connection, log in the users to the backend
    await communicator1.send_json_to({
        'type':'authorization',
        'username':'test_dummy1',
        'password':'kandidat11'
    })
    response1 = await communicator1.receive_json_from()

    await communicator2.send_json_to({
        'type':'authorization',
        'username':'test_dummy2',
        'password':'kandidat11'
    })
    response2 = await communicator2.receive_json_from()

    assert response1['type'] == 'success'
    assert response2['type'] == 'success'

    yield communicator1, communicator2

    await communicator1.disconnect()
    await communicator2.disconnect()


@pytest.fixture(scope="function")
def create_user():

    def _create_user(uname, group):
        user = User.objects.create_user(
            username=uname,
            password='kandidat11'
        )
        group, _ = Group.objects.get_or_create(name=group)
        group.user_set.add(user)

        return user
    
    return _create_user


async def test_consumer_successful_login(create_user):
    """Test if we can login successfully."""
    communicator = WebsocketCommunicator(application, "ws/connect/")
    connected, subprotocol = await communicator.connect()
    assert connected

    user = create_user("test_dummy1", "test_group")

    await communicator.send_json_to({
        'type':'authorization',
        'username':'test_dummy1',
        'password':'kandidat11'
    })
    response = await communicator.receive_json_from()
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
    """ Test sending an invalid type. """
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


async def test_consumer_send_gps(create_and_connect_users):
    """ Test sending gps data to other users.

    Uses the create_and_connect_users fixture to create two users,
    each with their own communicator. """

    communicator1, communicator2 = create_and_connect_users

    await communicator1.send_json_to({
        'type': 'gps',
        'position': 'Flen'
    })
    response2 = await communicator2.receive_json_from()


    await communicator2.send_json_to({
        'type': 'gps',
        'position':'Linköping'
    })
    response1 = await communicator1.receive_json_from()

    # test_dummy1 should receive gps data from test_dummy2
    # test_dummy2 should receive gps data from test_dummy1
    client_data1 = response1['test_dummy2']
    client_data2 = response2['test_dummy1']

    assert client_data1['type'] == 'gps_data'
    assert client_data1['position'] == 'Linköping'

    assert client_data2['type'] == 'gps_data'
    assert client_data2['position'] == 'Flen'

