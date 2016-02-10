## Problem Set 1, Problem 1

## Paying Off Credit Card Debt
## Find the remaining balance after a year assuming 5000 purchase, 18% annual interest rate, and 2% minimum monthly payment rate

# Ask user for input
balance = float(raw_input('Balance: '))
annual_interest_rate = float(raw_input('Annual interest rate: '))
min_monthly_pmt_rate = float(raw_input('Minimum monthly payment: '))

# For each month, print data
for month in range(1,13):
    if month == 1:
        remaining_balance = balance

    min_monthly_pmt = min_monthly_pmt_rate * remaining_balance
    interest_paid = annual_interest_rate / 12 * remaining_balance
    principal = min_monthly_pmt - interest_paid
    remaining_balance = remaining_balance - principal
    
    print 'Month '+str(month)+':'
    print 'Minimum monthly payment: ', min_monthly_pmt
    print 'principal paid: ', principal
    print 'Remaining balance: ', remaining_balance

## Paying the Minimum

## Paying Debt Off In a Year