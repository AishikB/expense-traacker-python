import csv
from datetime import datetime

expenditureDetails = []
fieldNames=["date", "category", "amount", "description"]
amount = 0

########### Helper functions #####################

def isDateInvalid(dateText):
    """Helper function to validate the input date"""
    try:
        if dateText is None:
            return True
        datetime.fromisoformat(dateText)
        return False
    except:
        print("Error: Incorrect data format, should be YYYY-MM-DD")
        return True

def isInvalidNum(numString):
    """Helper function to validate if the input date is a number"""
    try:
        if numString is None:
            return True
        int(numString)
        return False
    except:
        print("Error: plese enter a valid number")
        return True

def isInvalidMonth(month):
    """Validates if the entered month is valid"""
    if month == None:
        return True
    if isInvalidNum(month) or int(month) > 12 or int(month) < 1:
        print("Error!!! Enter a valid month")
        return True
    return False

def isInvalidYear(year):
    """Validates if the entered year is valid"""
    if year == None:
        return True
    currentYear = datetime.now().year
    if isInvalidNum(year):
        print("Error!!! Enter a valid year")
        return True
    if int(year) > currentYear:
        print ("Error!! Entered error cannot be more than current year")
        return True
    if int(year) <  1:
        print("Lets stay in the period after christ was born :)")
        return True
    return False
        
def populateExpenditureDetailsIfEmpty():
    """This function is used to load the global variable expenses with the expenses stored in the excel file when empty. It is used to initialize the expense details variable"""
    if len(expenditureDetails) == 0:
        expenses = readFromCsv()
        expenditureDetails.extend([expense for expense in expenses])

    
def addExpense():
    """This function is used to add a expense. This prompts the uer to enter date, amount, category and description of the expense"""
    dateOfExpense = None
    populateExpenditureDetailsIfEmpty()
    while isDateInvalid(dateOfExpense):
        dateOfExpense = input('Enter date of expense in YYYY-MM-DD format: ')
    category = input("Enter the category of expense: ")
    amount = None
    while isInvalidNum(amount):
        amount = input("Enter the amount spent: ")
    description = input("Enter a breif description of the expense: ")
    expenditure={'date': dateOfExpense, 'category': category, 'amount':amount, 'description': description}
    expenditureDetails.append(expenditure)

### Display of expense ###

def displayExpenses():
    """This function is used to display all the expenses"""
    populateExpenditureDetailsIfEmpty()
    for expenditure in expenditureDetails:
        print(expenditure)

### Track budget ####

def enterMonthlyBudget():
    """This method promts the user to enter budget"""
    budget = None
    while isInvalidNum(budget):
        budget = input('Enter monthly budget: ')
    return budget

def calculateExpenseForTheMonth(year, month):
    """This method calculates the expenses for the month"""
    totalExpense = 0
    global expenditureDetails
    populateExpenditureDetailsIfEmpty()
    for expenditure in expenditureDetails:
        date = expenditure['date']
        dateObj = datetime.fromisoformat(date)
        if(dateObj.year == int(year) and dateObj.month == int(month)):
            totalExpense += int(expenditure["amount"])
    return totalExpense

def compareExpenseWithMonthlyBudget(year, month):
    """This method compares the expense for the month with the given monthly budget"""
    try:
        budget = int(enterMonthlyBudget())
        expense = calculateExpenseForTheMonth(year, month)
        print("Budget:: ",budget)
        print("Expense::", expense)
        if(expense > budget):
            print("Warning!!! you are spending more than your budget")
        else:
            print("Your available budget for the month is ", (budget - expense))
    except Exception as error:
        print(error)
        
def writeExpenseToFile(expenses):
    """writes expenses into CSV file"""
    writeIntoCsv('expense.csv', expenses, True, 'w+')
    print("Expense saved successfully")


def writeIntoCsv(filename, expenses, printHeader, operation='w'):
    """Generic method to write data into file if exists otherwise create a new file and write the data"""
    with open(filename, operation, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        if printHeader:
            writer.writeheader()
        writer.writerows(expenses)
        csvfile.close()

def readFromCsv():
    """Read expenses from csv"""
    try:
        rows=[]
        with open('expense.csv', "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)
            csvfile.close()
            return rows
    except:
        return []
    
    
#### main method. Execution starts from here ###########    
def run():
    while True:
        choice = input('Select the option of your choice: \n1. Add Expense\n2. View Expense\n3. Track Budget\n4. Save Expense To File\n5. Save Expense and exit.\n')
        match choice:
            case '1':
                print("..........Adding Expense............")
                addExpense()
            case '2':
                print("............Viewing expense............")
                displayExpenses()
            case '3':
                print("........Generating budget expense comparison.......")
                month = None
                while isInvalidMonth(month):
                    month = input("Enter the month for which you want to evaluate your expenses: ")
                year = None
                while isInvalidYear(year):
                    year = input("Enter the year for which you want to evaluate your expenses: ")
                compareExpenseWithMonthlyBudget(year, month)
            case '4':
                print(".......Saving Expense To File...........")
                writeExpenseToFile(expenditureDetails)
            case '5':
                print(".......Saving Expense To File and exiting the process...........")
                writeExpenseToFile(expenditureDetails)
                break
            case _:
                print("Please select a valid input")
    
run()