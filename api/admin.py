from django.contrib import admin
from .models import Loan, Customer

# Register your models here.

admin.site.register(Customer)
admin.site.register(Loan)