import pytest
from django.test import Client
from django.contrib.auth.models import User, Permission, ContentType
from bread.models import Grain, Flour, FlourInBread, FlourInLeaven, Bread, Leaven


@pytest.fixture
def Client():
    client = Client
    return client


@pytest.fixture
def user():
    user = User.objects.create(username='Kowalski')
    user.set_password('dziendobry')
    user.save()
    return user


@pytest.fixture()
def grains():
    grain_list = []
    for x in 'abcde':
        a = Grain.objects.create(name=x)
        grain_list.append(a)
    return grain_list
