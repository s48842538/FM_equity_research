import pandas as pd
import yfinance as yf
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
    import pandas as pd
import os

def save_valuation_table_from_excel(excel_file="CIP DCF.xlsx", sheet_name="Sheet2", output_file="valuation_table.csv", save_folder="Graphs"):
    # Ensure the save folder exists
    os.makedirs(save_folder, exist_ok=True)

    try:
        # Load the Excel file and extract the relevant sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)

        # Extract relevant rows and columns (B = Column 1, C = Column 2)
        rows_of_interest = [3, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 29]
        extracted_data = df.iloc[rows_of_interest, [1, 2]]  # Column B (1) and Column C (2)

        # Rename the columns for clarity
        extracted_data.columns = ["Metric", "Value"]

        # Drop rows where both Metric and Value are empty
        extracted_data.dropna(how='all', inplace=True)

        # Save the DataFrame as a CSV file
        output_path = os.path.join(save_folder, output_file)
        extracted_data.to_csv(output_path, index=False)
        print(f"Valuation table saved at: {output_path}")

    except FileNotFoundError:
        print(f"Error: '{excel_file}' file not found.")
        return
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return

    return extracted_data

# Example usage
valuation_table = save_valuation_table_from_excel()

if valuation_table is not None:
    print("\nValuation Table:")
    print(valuation_table)
else:
    print("Failed to generate the valuation table.")
