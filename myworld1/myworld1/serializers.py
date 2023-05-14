from django.db.models import fields
from rest_framework import serializers
from .models import Employees

class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employees
		fields ='__all__'

