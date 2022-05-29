import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restapp.settings')
django.setup()

from orders.models import Foods, Orders
from customers.models import Customers
from staffs.models import Staffs
from django.db.models import Max

def add_foods():
    food_list = ['Steak', 'PorkChop', 'IceTea', 'IceCoffee','ChickenWings']

    for _ in range(len(food_list)):
        f = Foods(name=food_list[_])
        f.save()

def add_customers():
    c = Customers(firstname="usr01", lastname="usr02", address="addr1", phone="0001234567",username="user01", password="password01")
    c.save()

add_foods()
add_customers()