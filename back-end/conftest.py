import os
import django
from manage import DEFAULT_SETTINGS_MODULE


"""
https://stackoverflow.com/questions/39137339/django-exception-django-core-exceptions-improperlyconfigured

Channels tests can't be executed the 'Django way', so we need to run pytest in order to test Channels sockets.
"""
def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
    django.setup()