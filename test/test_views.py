import pytest
from django.urls import reverse

from bread.models import Grain, Flour, Leaven, FlourInLeaven, FlourInBread, Bread


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
    for x in 'abcde':
        response = client.post(reverse('add_grain'), {'name': x})
    assert response.status_code == 302
    assert Grain.objects.get(name='a')
    a = Grain.objects.get(name='a')
    response = client.post(reverse('remove_grain', args=(a.pk,)))
    assert response.status_code == 302
    assert len(Grain.objects.all()) == 4


@pytest.mark.django_db
def test_flour_view(client, user, grains):
    client.login(username='Kowalski', password='dziendobry')
    z = grains[0]
    a = grains[1]
    response = client.post(reverse('add_flour'), {'name': 'x', 'brand': 'y',
                                                  'grain': z.id, 'wholegrain': True, 'type': 500})
    assert response.status_code == 302
    assert Flour.objects.get(name='x', brand='y', grain=z, wholegrain=True, type=500)
    x = Flour.objects.get(name='x')
    response = client.post(reverse('edit_flour', args=(x.pk,)), {'name': 'f', 'brand': 'b',
                                                                 'grain': a.id, 'wholegrain': False, 'type': 1500})

    x = Flour.objects.get(name='f', brand='b', grain=a.id, wholegrain=False, type=1500)
    response = client.post(reverse('remove_flour', args=(x.pk,)))
    assert response.status_code == 302
    assert len(Flour.objects.all()) == 0


@pytest.mark.django_db
def test_leaven_view(client, user):
    client.login(username='Kowalski', password='dziendobry')
    response = client.post(reverse('add_leaven'), {'name': 'x', 'sourdough': 1, 'water': 1, 'proofing': '01:00:00'})
    assert response.status_code == 302
    assert Leaven.objects.get(name='x', sourdough=1, water=1, proofing='01:00:00', user=user.id)
    example_leaven = Leaven.objects.get(name='x')
    response = client.post(reverse('remove_leaven', args=(example_leaven.pk,)))
    assert response.status_code == 302
    assert len(Leaven.objects.all()) == 0


@pytest.mark.django_db
def test_flour_in_leaven_view(client, user, flours):
    flour = flours[0]
    client.login(username='Kowalski', password='dziendobry')
    response = client.post(reverse('add_leaven'), {'name': 'x', 'sourdough': 1, 'water': 1, 'proofing': '01:00:00'})
    assert response.status_code == 302
    example_leaven = Leaven.objects.get(name='x')
    response = client.post(reverse('flour_in_leaven', args=(example_leaven.pk,)), {'flour': flour.id, 'grams': 200})
    example_flour_in_leaven = FlourInLeaven.objects.get(pk=1)
    assert response.status_code == 302
    assert FlourInLeaven.objects.get(leaven=example_leaven.id)
    response = client.post(reverse('remove_flour_leaven', args=(example_flour_in_leaven.pk,)))
    assert len(example_leaven.flourinleaven_set.all()) == 0


@pytest.mark.django_db
def test_bread_view(client, user, leaven):
    client.login(username='Kowalski', password='dziendobry')
    for a, b, c in zip('abcd', range(1, 5), range(1, 5)):
        response = client.post(reverse('add_bread'), {'name': a, 'date': '2020-09-30', 'water': b, 'salt': c,
                                                      'leaven': leaven.id, 'baking_time': '01:00:00',
                                                      'baking_temperature': 210, 'rating': 5})
        assert response.status_code == 302
    assert len(Bread.objects.all()) == 4
    a = Bread.objects.get(name='a')
    response = client.post(reverse('remove_bread', args=(a.pk,)))
    assert response.status_code == 302
    assert len(Bread.objects.all()) == 3




@pytest.mark.django_db
def test_flour_in_bread_view(client, user, leaven, flours):
    client.login(username='Kowalski', password='dziendobry')
    response = client.post(reverse('add_bread'), {'name': 'a', 'date': '2020-09-30', 'water': 150, 'salt': 10,
                                                  'leaven': leaven.id, 'baking_time': '01:00:00',
                                                  'baking_temperature': 210, 'rating': 5})
    assert response.status_code == 302
    assert Bread.objects.get(name='a')
    example_bread = Bread.objects.get(name='a')
    for flour in flours:
        response = client.post(reverse('flour_in_bread', args=(example_bread.pk,)), {'flour': flour.id,
                                                                                     'bread': example_bread.id,
                                                                                     'grams': 200})
    assert response.status_code == 302
    assert len(example_bread.flourinbread_set.all()) == 5
    example_flour_in_bread = FlourInBread.objects.get(pk=1)
    response = client.post(reverse('remove_flour_bread', args=(example_flour_in_bread.pk,)))
    assert len(example_bread.flourinbread_set.all()) == 4


@pytest.mark.django_db
def test_my_breads_view(client, user, user2, flours, leaven):
    client.login(username='Zielinski', password='dobrydzien')
    for a, b, c in zip('abc', range(1, 4), range(1, 4)):
        response = client.post(reverse('add_bread'), {'name': a, 'date': '2020-09-30', 'water': b, 'salt': c,
                                                      'leaven': leaven.id, 'baking_time': '01:00:00',
                                                      'baking_temperature': 210, 'rating': 5})
        assert response.status_code == 302
    assert len(Bread.objects.filter(user__username="Zielinski")) == 3
    client.logout()

    client.login(username='Kowalski', password='dziendobry')
    for a, b, c in zip('xy', range(1, 3), range(1, 3)):
        response = client.post(reverse('add_bread'), {'name': a, 'date': '2020-09-30', 'water': b, 'salt': c,
                                                      'leaven': leaven.id, 'baking_time': '01:00:00',
                                                      'baking_temperature': 210, 'rating': 5})
        assert response.status_code == 302
    assert len(Bread.objects.filter(user__username="Kowalski")) == 2
    assert len(Bread.objects.filter(user__username="Zielinski")) == 3








