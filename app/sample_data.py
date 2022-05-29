from faker import Faker
import random
import os
import sys
import django  

faker = Faker()
sample_staff_rc = 50
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restapp.settings')
django.setup()


try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
    ) from exc

from staffs.models import Staffs

def randomize_staff_member():
    for _ in range(0,sample_staff_rc):
        s = Staffs(
        firstname=faker.first_name(), lastname=faker.last_name(), staff_type=random.choice(['pt', 'ft']), ssn=faker.ssn(), role='member')
        s.save()

def set_password():
    s = list(Staffs.objects.all())
    
    for i in range(len(s)):
        s[i].password = faker.password()
        s[i].save()

def set_manager():
    #Filter Full time staff
    s = Staffs.objects.filter(staff_type='ft')
    #Randomly pick 2 staffs as manager
    temp_list = list(s)
    rand_id = random.randint(0,len(s))
    first_manager = temp_list[rand_id]
    temp_list.pop(rand_id)
    rand_id = random.randint(0,len(s))
    second_manager = temp_list[rand_id]

    first_manager.role = 'manager'
    first_manager.save()

    second_manager.role = 'manager'
    second_manager.save()
    
    print(f'{first_manager.id} , {first_manager.password}')
    print(f'{second_manager.id} , {second_manager.password}')
    
randomize_staff_member()
set_password()
set_manager()