import pytest
from django.urls import reverse

from bread.models import Grain, Flour


def test_index_view(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_show_all_view(client):
    response = client.get(reverse('show_all_breads'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_grain_view(client, user):
    client.login(username='Kowalski', password='dziendobry')
    response = client.post(reverse('add_grain'), {'name': 'x'})
    assert response.status_code == 302
    assert Grain.objects.get(name='x')
    x = Grain.objects.get(name='x')
    response = client.post(reverse('remove_grain', args=(x.pk,)))
    assert response.status_code == 302
    assert len(Grain.objects.all()) == 0

@pytest.mark.django_db
def test_add_flour_view(client, user):
    client.login(username='Kowalski', password='dziendobry')
    Grain.objects.create(name='z')
    z = Grain.objects.get(name='z')
    response = client.post(reverse('add_flour'), {'name': 'x', 'brand': 'y',
                                                  'grain': z, 'wholegrain': True, 'type': 500})
    assert Flour.objects.get(name='x')










