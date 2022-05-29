from django.db import models

# Create your models here.
class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=200)
    lastname= models.CharField(max_length=200)
    password = models.CharField(max_length=200, default='password001')
    ssn = models.CharField(max_length=11, blank=False)
    staff_type = models.CharField(max_length=2)
    role = models.CharField(max_length=10, default='member')
