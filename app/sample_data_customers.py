from faker import Faker
import random
import os
import sys
import django  
import random

faker = Faker()
sample_customers_rc = 10
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restapp.settings')
django.setup()


""" try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
    ) from exc """

from customers.models import Customers

for _ in range(0,sample_customers_rc):
    username = faker.first_name() + str(random.randint(0,9999))
    c = Customers(
    firstname=faker.first_name(), lastname=faker.last_name(), address=faker.address(), phone=faker.phone_number(),username=username, password=faker.password() 
    )
    c.save()
