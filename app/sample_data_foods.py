import os
from xml.dom.minidom import Identified
import django
import random

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

def add_orders():
    orders_count = 10
    max_customer_id = int(Customers.objects.aggregate(Max('id'))['id__max'])
    max_staff_id = int(Staffs.objects.aggregate(Max('id'))['id__max']) / 2

    for _ in range(orders_count):
        ran_cid = Customers.objects.get(id=random.randint(1,max_customer_id))
        ran_sid = Staffs.objects.get(id=random.randint(1,max_staff_id))
        ran_fid = Foods.objects.get(id=random.randint(1,5))
        o = Orders(customers=ran_cid)
        o.save()
        o.staffs.add(ran_sid)
        o.food.add(ran_fid)
        
add_foods()
add_orders()




