import gspread
from google.oauth2.service_account import Credentials

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
    Get sales figures input from the user
    """
    #Instruct the user to provide the sales data
    print("Please enter sales data from the last market.")
    print("Data should be six numbers separated by commas.")
    print("Example: 10,20,30,40,50,60\n") #\n backslash to add an extra line

    data_str = input("Enter your data here: ")
    #check if we are getting a value --> print(f"The data provided is {data_str}")
    
    sales_data = data_str.split(",") #This will remove the commas from the string.
    #print(sales_data) -- sales_data values are strings

    #Call the validate_data function here
    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try converts all string values into integers.
    Raises ValueErrors if strings cannot be converted into integers
    or if there aren't exactly 6 values
    """
    #print(f"Values to be validated: {values}")

    #check if there are exactly 6 values in the data
    try:
        if len(values) !=6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")

    #check if these 6 values can be converted into integers



#Since the code is inside the function, do not forget to call it
get_sales_data()