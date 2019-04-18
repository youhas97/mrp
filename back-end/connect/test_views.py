from django.test import RequestFactory
import json
from django.contrib.auth.models import User, Group
import pytest
from .views import register

pytestmark = pytest.mark.django_db(transaction=True)

def test_successful_register():
    factory = RequestFactory()

    requestData = {
        'username':'test_subject',
        'password':'kandidat11',
        'groupnum':'alpha_squad',
        'name':'Bond, James Bond'
    }
    request = factory.post(
        'connect/register', 
        data=json.dumps(requestData),
        content_type='application/json;charset=UTF-8'
    )

    Group.objects.create(name='alpha_squad')

    response = register(request)

    assert response.status_code == 200

    