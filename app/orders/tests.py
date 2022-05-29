from django.test import TestCase
from django.urls import reverse
from customers.models import Customers
import pytest


def test_menu_access():
    url = reverse('menu')
    assert url == "/show_menu"

@pytest.fixture
def new_customer(db):
    c = Customers.objects.create(
            firstname='usr01',
            lastname='usr01',
            username='user001',
            password='pwd',
            address='address001',
            phone='0001234567'
    )
    return c

def test_search_users(new_customer):
    assert Customers.objects.filter(id=1).exists()


# Create your tests here.
