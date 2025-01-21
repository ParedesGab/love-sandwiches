import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

#Check if the API is working
# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data) 


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers
    separated by commas. The loop will repeatedly request data until it is valid.
    """
    while True:
        #Instruct the user to provide the sales data
        print("Please enter sales data from the last market.")
        print("Data should be six numbers separated by commas.")
        print("Example: 10,20,30,40,50,60\n") #\n backslash to add an extra line

        data_str = input("Enter your data here:\n")
        #check if we are getting a value --> print(f"The data provided is {data_str}")
        
        sales_data = data_str.split(",") #This will remove the commas from the string.
        #print(sales_data) -- sales_data values are strings

        #Call the validate_data function here
        #validate_data(sales_data)

        #(1.3) If there is no error in the validate data, then the 
        # while will be broken, with a printed message
        if validate_data(sales_data) == True:
            print("Data is valid!\n")
            break
    
    #The function will return the sales_data value!
    return sales_data
        

def validate_data(values):
    """
    Inside the try converts all string values into integers.
    Raises ValueErrors if strings cannot be converted into integers
    or if there aren't exactly 6 values
    """
    print(f"Validated sales data: {values}\n")

    #check if there are exactly 6 values in the data
    #check if these 6 values can be converted into integers
    try:
        [int(value) for value in values]

        if len(values) !=6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False  #(1.2)return False in case there is an error
    
    #(1.1)Return True if our function runs without any errors
    return True

# def update_sales_worksheet(data):
#     '''
#     Update sales excel worksheet, add new row with the list data provided.
#     '''
#     print("Updating sales worksheet...\n") #give user some feedback in the terminal
#     sales_worksheet = SHEET.worksheet("sales") #SHEET = GSPREAD_CLIENT.open('love_sandwiches')
#     sales_worksheet.append_row(data)
    
#     print("Sales worksheet updated successfully.\n")

# def update_surplus_worksheet(data):
#     '''
#     Update surplus excel worksheet, add new row with the list data provided.
#     '''
#     print("Updating surplus worksheet...\n") #give user some feedback in the terminal
#     surplus_worksheet = SHEET.worksheet("surplus") #SHEET = GSPREAD_CLIENT.open('love_sandwiches')
#     surplus_worksheet.append_row(data)
    
#     print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    '''
    Receives a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided 
    '''
    print(f"Updating {worksheet} worksheet...") 
    worksheet_to_update = SHEET.worksheet(worksheet) 
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
     """
     Compare sales with stock and calculate the surplus for each item type.
     The surplus is defined as the sales figure subtracted from the stock:
     - Positive surplus indicates waste
     - Negative surplus indicates extra made when stock was sold out.
     """
     print("Calculating surplus data...\n")
     stock = SHEET.worksheet("stock").get_all_values()
     #pprint(stock)

     stock_row = stock[-1]
     #print(stock_row) #['28', '31', '33', '29', '22', '31'] string values 

     #stock_row_num = [int(num) for num in stock_row]
     #print(stock_row_num)

     #print(f"sales row: {sales_row}\n") #[1, 2, 3, 4, 5, 6]

     surplus_data = []
     for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
     #print(surplus_data)
     return surplus_data

def get_last_5_entries_sales():

    """
    Collects columns of data from sales worksheet, 
    collecting the last 5 entries for each sandwich,
    and returns the data as a list of lists
    """

    #get the sales sheet
    sales = SHEET.worksheet("sales")

    #Code to access all columns:
    # 1 - Create a new empty list
    columns = []
    #2 - Create a for loop 6x times (1 for each column in my data)
    #to create a range of numbers from 1 to 6 (ind = index)
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    #pprint(columns)
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data ...\n")

    new_stock_data = []

    #Iterate through each column in the data (remember that the list values are strings)
    for column in data:
        #Iterate through each value and convert it into integers
        int_column = [int(num) for num in column]
        
        #calculate average in each column
        average_column = sum(int_column) / len(int_column)
        #print(average_column)

        # stock + 10 %
        stock_num = average_column*1.1
        #print(round(stock_num))

        new_stock_data.append(round(stock_num))
        
    return new_stock_data

def get_stock_values(data):
    """
    Get stock values
    """

    print("Make the following numbers of sandwiches for next")
    stock = SHEET.worksheet("stock")

    #One way to do it:
    # headings = []

    # for ind in range(1,7):
    #     column = stock.col_values(ind)
    #     headings.append(column[0])
    # pprint(headings)
    # #return columns

    #Shorter way:
    headings = stock.row_values(1)
    return headings

def create_dictionary(key, data):
    return dict(zip(key,data))


def main():

    '''
    Run all program functions
    '''

    #Call the get_sales_data function
    data = get_sales_data()
    #print(data)

    sales_data = [int(num) for num in data]
    #print(sales_data)

    #Call the update_sales_worksheet function
    #update_sales_worksheet(sales_data)
    update_worksheet(sales_data,"sales")

    #update_surplus_worksheet(new_surplus_data)

    #Call the calculate_surplus function
    new_surplus_data = calculate_surplus_data(sales_data)
    #print(new_surplus_data)
        
    update_worksheet(new_surplus_data,"surplus")

    sales_columns = get_last_5_entries_sales()
    #pprint(sales_columns)

    stock_data = calculate_stock_data(sales_columns)
    #print(stock_data)

    update_worksheet(stock_data,"stock")

    stock_values = get_stock_values(stock_data)
    #print(stock_values)

    my_dictionary = create_dictionary(stock_values, stock_data)
    print(my_dictionary)

print("Welcome to love sandwiches data automation\n")
main()


