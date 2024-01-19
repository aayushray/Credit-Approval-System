from rest_framework import serializers
from .models import Customer, Loan

class Registration(serializers.ModelSerializer):
    approval_limit = serializers.IntegerField(required=False)

    def to_internal_value(self, data):
        if 'monthly_income' in data:
            data['monthly_salary'] = data.pop('monthly_income')
        data.setdefault('monthly_salary', None)
        return data
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'monthly_salary', 'phone_number', 'approval_limit']

class Eligibility(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['customer_id', 'loan_amount', 'interest_rate', 'tenure']

class CreateLoan(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['customer_id', 'loan_amount', 'interest_rate', 'tenure']