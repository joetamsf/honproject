from rest_framework import serializers
from .models import Customers, Tokens

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers 
        fields = ['username', 'password', 'firstname', 'lastname', 'address', 'phone']


class TokenSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = ['token', 'expire_time', 'customers']