#AI used to assist intuition associated with combining both y-axis
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

#Import Centuria Industrial REIT Price Targets
centuria_price_targets = pd.read_csv('Tprice.csv',
    parse_dates=['Date'],   #converts the Date column to datetime
    dayfirst=True,          #dates are in D/M/YYYY format
    index_col='Date'        # make Date the DataFrame index
)

#Download last 10 years of price data from Yahoo Finance
centuria_price_history = yf.download("CIP.AX", start = '2015-4-25', end = '2025-4-25')
asx_price_history = yf.download("^AXJO", start = '2015-4-25', end = '2025-4-25')

#Define graph structure
plt.figure(figsize=(10,6))
plt.title("Centuria Industrial REIT Price and Price Targets vs ASX200 Index", fontsize = 16)
plt.grid(True)
plt.xlabel("Date")

#There will be 2 y-axis for the graph
#[0] is necessary to enable the combined legend as default labels (centuria_price/centuria_price_targets_plot in matplotlib) can interfere with retrieving the correct label for plotting (AI debug).
#Plot the primary y-axis (Centuria price and price targets)
plt.ylabel("Centuria Industrial REIT Price / Price Targets ($AUD)")
centuria_price = plt.plot(centuria_price_history['Close'], color = 'blue', linewidth = 1, label = 'Centuria Price')[0]
centuria_price_targets_plot = plt.plot(centuria_price_targets['12M Target Price'], color = 'red', linewidth = 1, label = 'Centuria Industrial REIT Price Targets')[0]

#Plot the secondary y-axis (ASX200 index)
#[0] is necessary to enable the combined legend as default labels (asx_price in matplotlib) can interfere with retrieving the correct label for plotting (AI debug).
plt.twinx()
plt.ylabel("ASX200 Index")
asx_price = plt.plot(asx_price_history['Close'], color = 'black', linewidth = 1, label = 'ASX200')[0]

#Combined Legend
combined_legend = [asx_price, centuria_price, centuria_price_targets_plot]
labels = [price.get_label() for price in combined_legend]
plt.legend(combined_legend, labels)

#Display Graph
plt.show()