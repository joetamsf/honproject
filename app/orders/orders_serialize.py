from rest_framework import serializers
from .models import Orders

class OrderSerialize(serializers.ModelSerializer):
    class Meta:
        models=Orders
        fields = ['customer']