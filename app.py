import requests
import config as cfg

# Replace 'YOUR_API_KEY' with your actual API key from IEX Cloud
API_KEY = cfg.IEX_API_KEY

# Define the base URL for the IEX Cloud API
BASE_URL = f'https://cloud.iexapis.com/stable'

# Define the endpoint for fetching stocks
SYMBOLS_ENDPOINT = f'{BASE_URL}/ref-data/symbols'

# Make the API request to fetch the symbols
response = requests.get(SYMBOLS_ENDPOINT, params={'token': API_KEY})
data = response.json()

# Filter stocks based on criteria
filtered_stocks = []
for stock in data:
    if stock['isEnabled'] and stock['type'] == 'cs':
        symbol = stock['symbol']
        name = stock['name']

        # Fetch additional stock information using the symbol
        STOCK_ENDPOINT = f'{BASE_URL}/stock/{symbol}/quote'
        response = requests.get(STOCK_ENDPOINT, params={'token': API_KEY})
        stock_data = response.json()

        # Extract the desired fields from the stock data
        market_cap = stock_data['marketCap']
        price = stock_data['latestPrice']

        # Skip if no values
        if market_cap == None: continue
        if price == None: continue
        
        # Filter based on criteria
        if (50e6 <= market_cap <= 300e6) and (1 <= price <= 20):
            print(symbol, name, market_cap, price)
            filtered_stocks.append(stock)

# Print the filtered stocks
for stock in filtered_stocks:
    print(f"Symbol: {stock['symbol']}, Name: {stock['name']}, Market Cap: {stock_data['marketCap']}, Price: {stock_data['latestPrice']}")


# import requests
# import csv
# import config as cfg

# from datetime import datetime


# # Replace 'YOUR_API_KEY' with your actual API key from Alpha Vantage
# API_KEY = cfg.ALPHA_V_API_KEY

# # Define the URL for the API endpoint
# URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey={API_KEY}'

# # Make the API request
# with requests.Session() as s:
#     download = s.get(URL)
#     decoded_content = download.content.decode('utf-8')

# # Parse the CSV data
# cr = csv.reader(decoded_content.splitlines(), delimiter=',')
# data = list(cr)

# print(data)
# # Skip the header row
# data = data[1:]

# # Filter stocks based on criteria
# filtered_stocks = []
# for row in data:
#     # Assuming the CSV columns are in a specific order, modify the indices accordingly
#     symbol = row[0]
#     name = row[1]
#     market_cap = float(row[2])
#     price = float(row[3])
#     stock_float = float(row[4])
    
#     if 50e6 <= market_cap <= 300e6 and stock_float < 100e6 and 1 <= price <= 20:
#         filtered_stocks.append(row)

# # Print the filtered stocks
# for stock in filtered_stocks:
#     print(f"Symbol: {stock[0]}, Name: {stock[1]}, Market Cap: {stock[2]}, Price: {stock[3]}, Float: {stock[4]}")