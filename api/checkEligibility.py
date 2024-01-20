from .models import Customer, Loan
import datetime

def criteriaCheck(customer_id):
    loans = Loan.objects.filter(customer_id=customer_id)
    current_date = datetime.date.today()

    past_loan_paid_on_time = 0
    total_past_loans = 0
    current_year_monthly_installments = 0
    loan_approved_volume = len(loans)
    total_loan_amount = 0

    for loan in loans:
        loan_end_date = loan.end_date
        total_past_loans += 1
        emis_paid_this_year = 0
        
        if (loan_end_date <= current_date) and (loan.emi_paid_on_time == loan.tenure):
            past_loan_paid_on_time += 1
        
        if (loan_end_date.year >= current_date.year):
            emis_paid_this_year = loan.monthly_payment
        
        current_year_monthly_installments += emis_paid_this_year
        total_loan_amount+= loan.loan_amount

    #setting CRITERIA 1:
    criteria1 = round(past_loan_paid_on_time / total_past_loans, 2) * 100


    #setting CRITERIA 2:
    if (total_past_loans >= 6):
        criteria2 = 100
    elif (total_past_loans >= 4):
        criteria2 = 75
    elif (total_past_loans >= 2):
        criteria2 = 50
    else:
        criteria2 = 30


    #setting CRITERIA 3:
    monthly_salary = Customer.objects.get(customer_id=customer_id).monthly_salary

    if (current_year_monthly_installments <= 0.20*(monthly_salary)):
        criteria3 = 100
    elif (current_year_monthly_installments <= 0.35*(monthly_salary)):
        criteria3 = 75
    elif (current_year_monthly_installments <= 0.5*(monthly_salary)):
        criteria3 = 50
    else:
        criteria3 = 0

    
    #setting CRITERIA 4:
    if (loan_approved_volume >= 5):
        criteria4 = 100
    elif (loan_approved_volume >= 3):
        criteria4 = 70
    else:
        criteria4 = 30
    

    # Calculating the CREDIT SCORE
    if ((total_loan_amount > Customer.objects.get(customer_id=customer_id).approved_limit) or (criteria3 == 0)):
        credit_score = 0
    else:
        credit_score = round((criteria1 + criteria2 + criteria3 + criteria4)/4, 2)
    
    if credit_score >= 50:
        return True, None, None
    elif credit_score >= 30 and credit_score < 50:
        return True, 12, None
    elif credit_score >= 10 and credit_score < 30: 
        return True, 16, None
    else:
        if criteria3:
            return False, None, 'Your sum of all current loans have exceded the Approved Limit'
        else:
            return False, None, f'Your Credit Score is {credit_score}(Below 10)'