import pytest
from django.urls import reverse

from bread.models import Grain, Flour, Leaven, FlourInLeaven, FlourInBread


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
def test_flour_view(client, user, grains):
    client.login(username='Kowalski', password='dziendobry')
    z = grains[0]
    response = client.post(reverse('add_flour'), {'name': 'x', 'brand': 'y',
                                                  'grain': z.id, 'wholegrain': True, 'type': 500})
    assert response.status_code == 302
    assert Flour.objects.get(name='x', brand='y', grain=z, wholegrain=True, type=500)
    x = Flour.objects.get(name='x')
    response = client.post(reverse('remove_flour', args=(x.pk,)))
    assert response.status_code == 302
    assert len(Flour.objects.all()) == 0


@pytest.mark.django_db
def test_leaven_view(client, user):
    client.login(username='Kowalski', password='dziendobry')
    response = client.post(reverse('add_leaven'), {'name': 'x', 'sourdough': 1, 'water': 1, 'proofing': '01:00:00'})
    assert response.status_code == 302
    assert Leaven.objects.get(name='x', sourdough=1, water=1, proofing='01:00:00', user=user.id)
    x = Leaven.objects.get(name='x')
    response = client.post(reverse('remove_leaven', args=(x.pk,)))
    assert response.status_code == 302
    assert len(Leaven.objects.all()) == 0

@pytest.mark.django_db
def test_flour_in_leaven_view(client, user, flour):
    client.login(username='Kowalski', password='dziendobry')
    response = client.post(reverse('add_leaven'), {'name': 'x', 'sourdough': 1, 'water': 1, 'proofing': '01:00:00'})
    assert response.status_code == 302
    x = Leaven.objects.get(name='x')
    response = client.post(reverse('flour_in_leaven', args=(x.pk,)), {'flour': flour.id, 'grams': 200})
    assert response.status_code == 302
    assert FlourInLeaven.objects.get(leaven=x.id)
## delete
