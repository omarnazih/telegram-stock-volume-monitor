import requests
import time

from datetime import datetime
from multiprocessing import Pool

import config as cfg


def track_stock_volume(ticker:str):
    api_key = cfg.FMP_API_KEY
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"

    print("Started Tracking...")
    
    # Get initial stock volume, price, and timestamp
    response = requests.get(url)
    data = response.json()    
        
    data = data[0]
    initial_volume = data['volume']
    initial_price = data['price']

    while True:

        # Wait for the specified interval
        time.sleep(interval_minutes * 60)
                
        # Get current stock volume, price, and timestamp
        response = requests.get(url)
        data = response.json()

        current_volume = data['volume']
        current_price = data['price']
        current_timestamp = data['timestamp']

        # Calculate percentage change in volume
        percentage_change = ((current_volume - initial_volume) / initial_volume) * 100

        # Check if the volume increase exceeds the threshold
        if percentage_change >= threshold_percentage:
            print(f"Stock volume for {ticker} increased by {percentage_change}%")
            print(f"Timestamp of increase: {current_timestamp}")
            print(f"Time of increase: {datetime.fromtimestamp(current_timestamp)}")
            print(f"Price before increase: {initial_price}")
            print(f"Price after increase: {current_price}")
            print(f"Volume before increase: {initial_volume}")
            print(f"Volume after increase: {current_volume}")
            print("-----------------------------------")

        # Update initial volume, price, and timestamp for the next iteration
        initial_volume = current_volume
        initial_price = current_price


# List of tickers to track
tickers = ["AAPL", "GOOGL", "MSFT", "AMZN"]  # Add more tickers as needed

# Set the threshold percentage and interval
threshold_percentage = 0.05
interval_minutes = 1

# Create a multiprocessing pool with the number of desired processes
num_processes = 1000  # Adjust the number of processes as needed
pool = Pool(num_processes)

# Track stock volume concurrently for each ticker
pool.map(track_stock_volume, tickers)
