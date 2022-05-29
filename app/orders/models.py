from django.db import models

# Create your models here.

class Foods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    food = models.ManyToManyField(Foods,db_table='orders_and_foods')
    order_date = models.DateTimeField(auto_now_add=True)
    customers = models.ForeignKey('customers.Customers', on_delete=models.CASCADE)
    staffs = models.ManyToManyField('staffs.Staffs',db_table='cookingstaff')

