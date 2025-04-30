import yfinance as yf
import pandas as pd
import os

def get_financial_ratios(ticker):
    stock = yf.Ticker(ticker)
    
    # Extract relevant financial data
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow
    income_statement = stock.financials
    shares_outstanding = stock.info.get('sharesOutstanding', None)  # Shares outstanding

    # Function to safely get value or None if not found
    def safe_get_value(dataframe, row_name):
        try:
            value = dataframe.loc[row_name].values[0]  # Get the first (and only) value from the row
            return value
        except KeyError:
            return None
    
    # Extract financial values based on available keys
    current_assets = safe_get_value(balance_sheet, 'Cash And Cash Equivalents') + \
                     safe_get_value(balance_sheet, 'Receivables') + \
                     safe_get_value(balance_sheet, 'Other Current Assets')
    
    current_liabilities = safe_get_value(balance_sheet, 'Current Liabilities')
    total_debt = safe_get_value(balance_sheet, 'Total Debt')
    total_equity = safe_get_value(balance_sheet, 'Stockholders Equity')
    total_assets = safe_get_value(balance_sheet, 'Total Assets')
    net_income = safe_get_value(income_statement, 'Net Income')
    revenue = safe_get_value(income_statement, 'Total Revenue')

    # Calculate ratios
    if current_assets is None or current_assets == 0:
        current_ratio = None
        quick_ratio = None
    else:
        # Calculate Current Ratio
        current_ratio = current_assets / current_liabilities if current_liabilities else None
        # Calculate Quick Ratio
        quick_ratio = (current_assets - safe_get_value(balance_sheet, 'Cash And Cash Equivalents')) / current_liabilities if current_liabilities else None

    # Calculate Debt to Equity and Return on Equity (ROE)
    debt_to_equity = total_debt / total_equity if total_equity else None
    roe = net_income / total_equity if total_equity else None
    
    # Return on Assets (ROA)
    roa = net_income / total_assets if total_assets else None
    
    # Earnings Per Share (EPS)
    eps = net_income / shares_outstanding if shares_outstanding and net_income else None
    
    # Liquidity Ratio
    liquidity_ratio = (safe_get_value(balance_sheet, 'Cash And Cash Equivalents') + 
                       safe_get_value(balance_sheet, 'Receivables')) / current_liabilities if current_liabilities else None
    
    # Profitability Ratios (Profit Margin)
    profit_margin = net_income / revenue if revenue else None

    # Organize the ratios and their components into a DataFrame
    ratios = {
        "Ratio": ["Current Ratio", "Quick Ratio", "Debt to Equity", "Return on Equity", "Return on Assets", 
                  "Earnings Per Share", "Liquidity Ratio", "Profit Margin"],
        "Value": [current_ratio, quick_ratio, debt_to_equity, roe, roa, eps, liquidity_ratio, profit_margin],
        "Current Assets": [current_assets, current_assets, None, None, None, None, None, None],  # Adding current assets to the table
        "Current Liabilities": [current_liabilities, current_liabilities, None, None, None, None, None, None],  # Adding current liabilities to the table
        "Cash And Cash Equivalents": [safe_get_value(balance_sheet, 'Cash And Cash Equivalents'), 
                                      safe_get_value(balance_sheet, 'Cash And Cash Equivalents'), 
                                      None, None, None, None, None, None],  # Adding cash and cash equivalents to the table
        "Total Debt": [None, None, total_debt, None, None, None, None, None],  # Only debt to equity uses total debt
        "Total Equity": [None, None, total_equity, total_equity, None, None, None, None],  # Only debt to equity and ROE use total equity
        "Net Income": [None, None, None, net_income, net_income, net_income, None, None],  # Only ROE, ROA, and EPS use net income
        "Shares Outstanding": [None, None, None, None, None, shares_outstanding, None, None],  # Only EPS uses shares outstanding
        "Total Assets": [None, None, None, None, total_assets, None, None, None],  # Only ROA uses total assets
        "Revenue": [None, None, None, None, None, None, None, revenue]  # Only profit margin uses revenue
    }
    
    ratios_df = pd.DataFrame(ratios)
    
    # Save to CSV
    save_folder = "Graphs"
    os.makedirs(save_folder, exist_ok=True)
    output_file = os.path.join(save_folder, f"{ticker}_financial_ratios_with_components.csv")
    ratios_df.to_csv(output_file, index=False)
    
    print(f"Financial ratios and components saved at: {output_file}")
    
    # Also save as 'ratios.csv' as requested
    ratios_output_file = os.path.join(save_folder, "ratios.csv")
    ratios_df.to_csv(ratios_output_file, index=False)
    print(f"Ratios table saved as: {ratios_output_file}")
    
    return ratios_df

# Example usage
ticker = "CIP.AX"
ratios_df = get_financial_ratios(ticker)

if ratios_df is not None:
    print(ratios_df)
else:
    print("Failed to generate financial ratios.")

