#You should modify initialize()
def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global is_disabled
    
    is_disabled = False #If the card is disabled, this is True. Otherwise, it is False
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day, last_update_month = -1, -1
    
    last_country = None
    last_country2 = None    
    
    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    #Check if the first input date is the same or after the second input date
    #Return True iff the above statement is true
    return((day1 >= day2 and month1 == month2) or month1 > month2)
    
def all_three_different(c1, c2, c3):
    #Check congruency between all combinations of two of the three varibles.
    #Return True iff all three variables are different
    return(c1 != c2 and c2 != c3 and c1 != c3)

def purchase(amount, day, month, country):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global is_disabled
    if is_disabled:
        return("error, card disabled")
    elif all_three_different(country, last_country, last_country2):
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
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global is_disabled
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return("error, date")
    else:
        return(cur_balance_owing_recent + cur_balance_owing_intst)
    
def pay_bill(amount, day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global is_disabled
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return("error, date")
    elif amount < cur_balance_owing_intst:
        amount -= cur_balance_owing_intst
        cur_balance_owing_intst = 0
        cur_balance_owing_recent -= amount
        last_update_day = day
        last_update_month = month
    else:
        cur_balance_owing_intst -= amount
        last_update_day = day
        last_update_month = month
        
def interest(day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    if month - last_update_month = 1:
        cur_balance_owing_intst *= 1.05
        cur_balance_owing_intst += cur_balance_owing_recent
        last_update_day = day
        last_update_month = month
        break
    elif month - last_update_month > 1:
        cur_balance_owing_intst *= 1.05
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_intst *= (1.05)**(month - last_update_month - 1)
        last_update_day = day
        last_update_month = month
        break
    else:
        last_update_day = day
        last_update_month = month
        break

#Initialize all global variables outside the main block.
initialize()		
    
if __name__ == '__main__':
    #Describe your testing strategy and implement it below.
    #What you see here is just the simulation from the handout, which
    #doesn't work yet.
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      #80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      #30.0     (=80-50)
    print("Now owing:", amount_owed(6, 3))      #31.5     (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      #71.5     (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      #41.5     (=71.5-30)
    print("Now owing:", amount_owed(1, 5))      #43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      #83.65375 
    print(purchase(50, 3, 5, "United States"))  #error    (3 diff. countries in 
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      #83.65375 (no change, purchase
                                                #          declined)
    print(purchase(150, 3, 5, "Canada"))        #error    (card disabled)
    print("Now owing:", amount_owed(1, 6))      #85.8364375 
                                                #(43.65375*1.05+40)