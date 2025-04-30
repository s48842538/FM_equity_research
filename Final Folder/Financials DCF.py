import pandas as pd
import os

def get_financials_table(file_path, sheet_name="Sheet2"):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None  # Return None if the file doesn't exist
    
    # Load Excel without assuming any header
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # Select the specific rows (e.g., 42 to 46 in Excel = 41 to 45 in pandas)
    important_rows = [2, 4, 5, 6, 8, 9]  

    # Select columns C to I (columns 5 to 9 inclusive) based on your example
    financials_table = df.iloc[important_rows, 5:10]  # Note: column 4 = column E in pandas (starts at 0)

    # Assign row and column names
    financials_table.index = [
        "Sales Revenue ($'000)", 
        "Free Cash Flow", 
        "Discount Factor", 
        "Discounted Free Cash Flows", 
        "Free Cash Flow Estimate 2", 
        "Discounted Free Cash Flow 2"
    ]
    
    financials_table.columns = ["FY2025", "FY2026", "FY2027", "FY2028", "FY2029"]

    return financials_table

# Make sure you provide the correct file path here
file_path = "CIP DCF.xlsx"  # Modify this path if the file is in a different location
table = get_financials_table(file_path)

# If table is None, it means there was an error loading the file
if table is not None:
    print(table)