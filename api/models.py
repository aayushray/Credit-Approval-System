from collections.abc import Iterable
from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.IntegerField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    current_debt = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self) -> str:
        return str(self.customer_id)
    
    def save(self, *args, **kwargs):
        if not self.customer_id and self.id:
            self.customer_id = self.id
        super().save(*args, **kwargs)
    
class Loan(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.IntegerField(null=True, blank=True)
    loan_amount = models.DecimalField(max_digits=20, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=20, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=20, decimal_places=2)
    emi_paid_on_time = models.IntegerField(default=0)
    date_of_approval = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return str(self.customer_id) + " - " + str(self.loan_id)
    
    def save(self, *args, **kwargs):
        if not self.loan_id and self.id:
            self.loan_id = self.id
        super().save(*args, **kwargs)