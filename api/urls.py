from django.urls import path
from .views import customer_registration, check_eligibility, create_new_loan

urlpatterns = [
    path('register/', customer_registration, name="register"),
    path('check-eligibility/', check_eligibility, name="check-eligibility"),
    path('create-loan/', create_new_loan, name='create_loan')
]
