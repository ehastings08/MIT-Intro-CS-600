########## Problem Set 1, Problem 2

balance = float(raw_input('Outstanding balance: '))
annual_interest_rate = float(raw_input('Annual interest rate: '))
monthly_interest_rate = annual_interest_rate / 12

for pmt in range(int(round(balance/12,-1)),int(round(balance/5,-1)),10):
    
    for month in range(1,13):
        if month ==1:
            remaining_balance = balance
        
        # Compound interest for start of month
        interest_added = monthly_interest_rate * remaining_balance
        
        # Pay off minimum payment pmt
        remaining_balance -= pmt
        
        # Add compound interest
        remaining_balance += interest_added
        
        if remaining_balance <= 0:
            months_number = month
            break
            
    if remaining_balance <= 0:
        print 'Monthly payment to pay off debt in 1 year:',pmt
        print 'Number of months needed: ',months_number
        print 'Balance: ',remaining_balance
        break