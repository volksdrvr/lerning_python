# Get the loan details
money_owed = float(input("Loan amount?\n"))
apr = float(input("APR?\n"))
payment = float(input("Payment?\n"))
months = int(input("Months?\n"))

monthly_rate = apr/100/12

for i in range (months):
    interest_paid = money_owed * monthly_rate
    money_owed = money_owed + interest_paid

    money_owed = money_owed - payment

    if (money_owed < 0):
        print ("The last patment is:", money_owed)
        print ("You paid off the loan in", i+1, "months")
        break
    
    print ("Paid", payment, "of which", interest_paid, "was interest", end=' ')
    print("Now i owe", money_owed)
