def initialize(): #Initialize the global variables used in this program
    
    #cur_balance_owing_intst stores the part of the balance that is currently
    #accruing interest as an integer
    #cur_balance_owing_recent stores the part of the balance that is not
    #accruing interest as an integer
    global cur_balance_owing_intst, cur_balance_owing_recent
    
    #last_update_day and last_update_month stores the date and month, 
    #respectively, of the last time the card was accessed as integers
    global last_update_day, last_update_month 
    
    #last_coutry and last_country2 store the most recent and second most recent
    #countries from which the card was accessed, respectively, as strings
    global last_country, last_country2 
    
    #is_disabled stores whether or not the card is disabled as a boolean 
    #variable (ie. if the card is disabled, is_disable is True)
    global is_disabled 
    
    #The default values for the global variables are set below
    is_disabled = False
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day, last_update_month = -1, -1
    
    last_country = None
    last_country2 = None    
    
    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    '''
    Check if the integer value of the first input day (day1) is the 
    same or bigger than the integer value of the second input day (day2), 
    while the integer valuse of month1 and month2 are equal.
    Check if the integer value of month1 is greater than the integer
    value of month2.
    Return True if either of the above statements is true.
    '''
    return((day1 >= day2 and month1 == month2) or month1 > month2)
    
def all_three_different(c1, c2, c3):
    '''
    Check congruency between all combinations of two of the three strings.
    Return True iff all three variables are different.
    '''
    return(c1 != c2 and c2 != c3 and c1 != c3)

def purchase(amount, day, month, country):
    '''
    Run the interest function and, if the purchase succeeds, add amount to 
    cur_balance_owing_recent and update the variables last_country2, 
    last_country, last_update_day, and last_update_month.
    
    The purchase fails if the card is disabled, fraud is detected,
    or if the purchase date is before the last date the card was accessed.
    If the purchase fails, return an error string.
    '''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global is_disabled
    if is_disabled:
        return("error, card disabled, purchase declined")
    interest(day, month)
    if all_three_different(country, last_country, last_country2):
        is_disabled = True
        return("error, fraud")
    elif date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return("error, date")
    else:
        last_country2 = last_country
        last_country = country
        last_update_day = day
        last_update_month = month
        cur_balance_owing_recent += amount
    
def amount_owed(day, month):
    '''
    Runs the interest function and then returns the total amount of money owed
    as an integer. If the inputted date is after the last date the card was 
    accessed, return an error string.
    '''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global is_disabled
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return("error, date")
    interest(day, month)
    return(cur_balance_owing_recent + cur_balance_owing_intst)
    
def pay_bill(amount, day, month):
    '''
    Runs the interest function, then deducts an amount from the amount owed, 
    first from the portion accruing interest, then from the recent owings.
    
    If the inputted date is after the last date the card was accessed, or if 
    the card is disabled, return an error string.
    '''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global is_disabled
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return("error, date")
    interest(day, month)
    if is_disabled:
        return("error, card disabled, payment declined")
    elif amount > cur_balance_owing_intst:
        amount -= cur_balance_owing_intst
        cur_balance_owing_intst = 0
        cur_balance_owing_recent -= amount
    else:
        cur_balance_owing_intst -= amount
        
def interest(day, month):
    '''
    Transfer the recent balance into the balance accruing interest if the last 
    date the card was accessed was of or before the previous month.
    Also updates the balance accruing interest for each month passed since the 
    last date the card was accessed.
    '''
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return()
    elif cur_balance_owing_intst + cur_balance_owing_recent < 0:
        return()
    elif month - last_update_month == 1:
        cur_balance_owing_intst *= 1.05
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_recent = 0
        last_update_day = day
        last_update_month = month
    elif month - last_update_month > 1:
        cur_balance_owing_intst *= 1.05
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_intst *= (1.05) ** (month - last_update_month - 1)
        cur_balance_owing_recent = 0
        last_update_day = day
        last_update_month = month
    else:
        last_update_day = day
        last_update_month = month

initialize()		
    
if __name__ == '__main__':
    initialize()
    #This is the default test block, it tests adding and subtracting from the
    #balance, interest, and disabling the card when fraud is detected.
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      #80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      #30.0     (=80-50)
    print("Now owing:", amount_owed(6, 3))      #31.5     (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      #71.5     (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      #41.5     (=71.5-30)
    print("Now owing:", amount_owed(1, 5))      #Testing multi-month interest
                                                #43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      #83.65375 
    print(purchase(50, 3, 5, "United States"))  #error    (3 diff. countries in 
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      #83.65375 (no change, purchase
                                                #          declined)
    print(purchase(150, 3, 5, "Canada"))        #error    (card disabled)
    print("Now owing:", amount_owed(1, 6))      #85.8364375 
                                                #(43.65375*1.05+40)
    #Further testing for paying bills when the card is disabled
    print(pay_bill(30, 2, 6))                   #error    (card disabled)
    print("Now owing:", amount_owed(2, 6))      #85.8364375 (same as before)
   
    #Reseting variables
    is_disabled = False
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day, last_update_month = -1, -1
    
    last_country = None
    last_country2 = None 
    
    #Testing what happens when invalid dates are used
    #Everything should give errors
    last_update_day, last_update_month = 20, 12
    print(purchase(60, 10, 2, "Canada"))
    print(pay_bill(50, 2, 1))
    print(amount_owed(1, 5))
    is_disabled = True
    print(purchase(60, 11, 2, "Canada"))
    print(pay_bill(50, 12, 12))
    print(amount_owed(5, 2))
    #Now using valid dates
    is_disabled = False
    print(purchase(60, 21, 12, "Canada"))       #Prints nothing because the 
                                                #function works
    print(pay_bill(50, 22, 12))                 #Again, prints nothing
    print(amount_owed(30, 12))                  #Now, you owe 10
    
    #Reseting variables
    is_disabled = False
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day, last_update_month = -1, -1
    
    last_country = None
    last_country2 = None  
    
    #Testing what happens when you pay more than the balance
    #Should return balance of -40.0 as float
    purchase(10, 1, 1, "Canada")
    pay_bill(50, 2, 1)
    print(amount_owed(3, 1))
    print(amount_owed(3, 3)) #Interest shouldn't effect negative balance
    #Now switching back to positive balance
    purchase(100, 1, 4, "Canada")
    print(amount_owed(3, 4))                    #Should be up to 60.0
    print(amount_owed(3, 5))                    #No interest on first month 
                                                #after payment
    print(amount_owed(3, 6))                    #60.0 * 1.05 = 63.0