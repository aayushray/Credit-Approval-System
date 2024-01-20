from django.urls import path
from .views import customer_registration, check_eligibility, create_new_loan, view_by_loan_id, view_by_customer_id

urlpatterns = [
    path('register', customer_registration, name='register'),
    path('check-eligibility', check_eligibility, name='check-eligibility'),
    path('create-loan', create_new_loan, name='create_loan'),
    path('view-loan/<int:pk>', view_by_loan_id, name='view_by_loan_id'),
    path('view-loans/<int:pk>', view_by_customer_id, name='view_by_customer_id')
]
