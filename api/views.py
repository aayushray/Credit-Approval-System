from django.shortcuts import render
from rest_framework.response import Response
from .models import Customer, Loan
from .serializers import Registration, Eligibility, CreateLoan
from rest_framework.decorators import api_view
from .checkEligibility import criteriaCheck

# Create your views here.
@api_view(['POST'])
def customer_registration(request):
    serializer = Registration(data=request.data)
    monthly_salary = request.data['monthly_income']
    approved_limit = round(36*(monthly_salary), -5)

    if serializer.is_valid():
        serializer.validated_data['approved_limit'] = approved_limit
        new_customer = serializer.save()
        new_customer.save()
        response = {
            'customer_id': new_customer.customer_id,
            'name': f'{new_customer.first_name} {new_customer.last_name}',
            'age': new_customer.age,
            'monthly_income': new_customer.monthly_salary,
            'approved_limit': new_customer.approved_limit,
            'phone_number': new_customer.phone_number
        }

        return Response(response, status=201)
    else:
        print(serializer.errors)
        return Response("Wrong Format of the API", status=400)

@api_view(['POST'])
def check_eligibility(request):
    approval, new_interest_rate, message = criteriaCheck(request.data['customer_id'])
    serializer = Eligibility(data=request.data)
    if serializer.is_valid():
        response = {
            'customer_id': request.data['customer_id'],
            'approval': approval,
            'interest_rate': serializer.validated_data['interest_rate'],
            'corrected_interest_rate': new_interest_rate,
            'tenure': serializer.validated_data['tenure'],
            'monthly_installment': round(calculate_emi(serializer.validated_data['loan_amount'], new_interest_rate, serializer.validated_data['tenure']), 2)
        }
        return Response(response, status=200)
    else:
        return Response("Wrong Format of the API", status=400)

def calculate_emi(loan_amount, annual_interest_rate, tenure_months):
    loan_amount = float(loan_amount)
    monthly_interest_rate = annual_interest_rate / (12 * 100)
    emi = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**tenure_months) / ((1 + monthly_interest_rate)**tenure_months - 1)
    return emi

@api_view(['POST'])
def create_new_loan(request):
    approval, new_interest, message = criteriaCheck(request.data['customer_id'])
    serializer = CreateLoan(data = request.data)
    if serializer.is_valid():
        pass