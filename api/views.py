from django.shortcuts import render
from rest_framework.response import Response
import datetime
from dateutil.relativedelta import relativedelta
from .models import Customer, Loan
from .serializers import Registration, Eligibility, CreateLoan, LoanSerializer, LoanByCustomerId
from rest_framework.decorators import api_view
from .checkEligibility import criteriaCheck
from decimal import Decimal

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
    try:
        customer = Customer.objects.get(customer_id=request.data['customer_id'])
    except Customer.DoesNotExist:
        return Response(f"Customer with customer id {request.data['customer_id']} Does not exists", status=404)

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

@api_view(['POST'])
def create_new_loan(request):
    try:
        customer = Customer.objects.get(customer_id=request.data['customer_id'])
    except Customer.DoesNotExist:
        return Response(f"Customer with customer id {request.data['customer_id']} Does not exists", status=404)
    
    approval, new_interest, message = criteriaCheck(request.data['customer_id'])

    serializer = CreateLoan(data = request.data)
    if serializer.is_valid():
        monthly_installment = round(calculate_emi(serializer.validated_data['loan_amount'], serializer.validated_data['interest_rate'], serializer.validated_data['tenure']), 2)
        customer_id = serializer.validated_data['customer_id']
        loan_amount = serializer.validated_data['loan_amount']
        tenure = serializer.validated_data['tenure']
        interest_rate = new_interest     # Taking the new_interest Rate, based on the eligibility criteria,  
        loan_id = None

        if approval:
            loan = Loan.objects.create(
                customer_id = Customer.objects.get(customer_id=customer_id),
                loan_amount = loan_amount,
                tenure = tenure,
                interest_rate = interest_rate,
                monthly_payment = monthly_installment,
                date_of_approval = datetime.date.today(),
                end_date = datetime.date.today()+relativedelta(months=tenure)
            )
            loan.save()
            loan_id = loan.loan_id

        response = {
            'loan_id': loan_id,
            'customer_id': customer_id,
            'loan_approvded': approval,
            'message': message,
            'monthly_installment': monthly_installment
        }
        return Response(response, status=201)
    return Response(f'Wrong API Format', status=400)


@api_view(['GET'])
def view_by_loan_id(request, pk):
    try:
        loan = Loan.objects.get(loan_id=pk)
    except Loan.DoesNotExist:
        return Response(f"Loan with loan id {pk} Does not exists", status=404)
    
    customer_id = loan.customer_id.customer_id
    customer = Customer.objects.get(customer_id= customer_id)
    serializer = LoanSerializer(loan)

    response = {
        'loan_id': serializer.data['loan_id'],
        'customer': {
            'customer_id': customer.customer_id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'phone_number': customer.phone_number,
            'age_of_customer': customer.age
        },
        'loan_amount': serializer.data['loan_amount'],
        'interest_rate': serializer.data['interest_rate'],
        'monthly_installment': serializer.data['monthly_payment'],
        'tenure': serializer.data['tenure']
    }

    return Response(response, status=200)


@api_view(['GET'])
def view_by_customer_id(request, pk):
    try:
        customer = Customer.objects.get(customer_id = pk)
    except Customer.DoesNotExist:
        return Response(f"Customer with customer id {pk} Does not exists", status=404)
    
    loans = Loan.objects.filter(customer_id = customer)
    serializer = LoanByCustomerId(loans, many=True)

    for data in serializer.data:
        loan = Loan.objects.get(loan_id = data['loan_id'])
        data['monthly_installment'] = data.pop('monthly_payment')
        data['repayments_left'] = loan.tenure - loan.emi_paid_on_time

    return Response(serializer.data, status=200)

def calculate_emi(loan_amount, annual_interest_rate, tenure_months):
    loan_amount = Decimal(loan_amount)
    monthly_interest_rate = Decimal(annual_interest_rate) / (12 * 100)
    emi = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**tenure_months) / ((1 + monthly_interest_rate)**tenure_months - 1)
    return emi