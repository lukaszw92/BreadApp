import pytest
from django.urls import reverse

from bread.models import Grain


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
    response




