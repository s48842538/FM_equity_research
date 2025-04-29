import pandas as pd

def get_financials_table(file_path, sheet_name="Sheet1"):
    # Load Excel without assuming any header
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
   
    # Select the specific rows (e.g., 42 to 46 in Excel = 41 to 45 in pandas)
    important_rows = [41, 42, 43, 44, 45]  

    # Select columns C to I (columns 2 to 8 inclusive)
    financials_table = df.iloc[important_rows, 2:9]  # Note: 2 = column C, 9 is exclusive (so stops at I)

    # Assign row and column names
    financials_table.index = ["Sales Revenue", "EBIDTA", "EBIT", "EBIAT", "FCF"]
    financials_table.columns = ["FY2012", "FY2013", "FY2014", "FY2015", "FY2016", "FY2017", "FY2018"]

    return financials_table
table = get_financials_table("CIP DCF.xlsx")
print(table)
