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

@pytest.fixture
def user2():
    user = User.objects.create(username='Zielinski')
    user.set_password('dobrydzien')
    user.save()
    return user



@pytest.fixture()
def grains():
    grain_list = []
    for x in 'abcde':
        a = Grain.objects.create(name=x)
        grain_list.append(a)
    return grain_list

@pytest.fixture()
def flours():
    Grain.objects.create(name='z')
    z = Grain.objects.get(name='z')
    flour_list = []
    for name in 'abcde':
        flour = Flour.objects.create(name=name, brand='y', grain=z, wholegrain=True, type=500)
        flour_list.append(flour)
    return flour_list


@pytest.fixture()
def leaven():
    g = Grain.objects.create(name='g')
    y = Flour.objects.create(name='a', brand='b', grain=g, wholegrain=True, type=500)
    leaven = Leaven.objects.create(name='x', sourdough=1, water=1, proofing='01:00:00')
    FlourInLeaven.objects.create(leaven=leaven, flour=y, grams=150)
    return leaven




