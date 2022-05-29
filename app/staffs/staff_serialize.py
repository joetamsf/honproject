from rest_framework import serializers
from .models import Staffs

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staffs
        fields = ['firstname', 'lastname', 'staff_type', 'ssn']