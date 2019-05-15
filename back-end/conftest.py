import os
import django
import pytest
import mysite.settings
import asyncio

from mysite.settings import BASE_DIR
from manage import DEFAULT_SETTINGS_MODULE

@pytest.yield_fixture(scope='module')
def event_loop(request):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop

"""
https://stackoverflow.com/questions/39137339/django-exception-django-core-exceptions-improperlyconfigured

Channels tests can't be executed the 'Django way', so we need to run pytest in order to test Channels sockets.
"""
def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
    django.setup()
