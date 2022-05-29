# from tkinter import CASCADE
from django.db import models

# Create your models here.
class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    address = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=40, null=False)

class Tokens(models.Model):
    token = models.CharField(max_length=200,unique=True)
    expire_time = models.IntegerField()
    customers = models.ForeignKey(Customers, on_delete=models.CASCADE)