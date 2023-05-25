import concurrent.futures
import requests
import time

from datetime import datetime

import config as cfg


def get_stock_quote(ticker):
    api_key = cfg.FMP_API_KEY            
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]  # Return the first quote from the response
    return None

def track_stocks_parallel(tickers, interval=0.2, target_percentage_increase=100):
    target_percentage_increase = 0.05  # Define the target percentage increase per minute
    INTERVAL = interval
    
    print(INTERVAL)
    # Create a dictionary to store the last volume and price values for each stock
    last_volumes = {ticker: None for ticker in tickers}
    last_prices = {ticker: None for ticker in tickers}
    
    while True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the API requests for each stock in parallel
            futures = [executor.submit(get_stock_quote, ticker) for ticker in tickers]

            # Process the results as they become available
            for future in concurrent.futures.as_completed(futures):
                quote = future.result()
                print("Data: ", quote)
                if quote is not None:
                    ticker = quote['symbol']
                    current_volume = float(quote['volume'])
                    current_price = float(quote['price'])
                    current_timestamp = quote['timestamp']
                    
                    # Check if the last volume and price values are available
                    if last_volumes[ticker] is not None and last_prices[ticker] is not None:
                        initial_volume = last_volumes[ticker]
                        initial_price = last_prices[ticker]
                        
                        percentage_change = (current_price - initial_price) / initial_price * 100
                        change_percentage = (current_volume - initial_volume) / initial_volume * 100
                        
                        print(change_percentage)  
                        print(target_percentage_increase)                 
                        if change_percentage >= target_percentage_increase:
                            yield (
                                ticker,
                                percentage_change,
                                initial_price,
                                current_price,
                                change_percentage,
                                initial_volume,
                                current_volume,
                                current_timestamp,
                            )

                    last_volumes[ticker] = current_volume
                    last_prices[ticker] = current_price

        time.sleep(INTERVAL * 60)  # Wait for X minutes before checking again

# Example usage
# tickers = ["AAPL", "GOOGL"]
tickers = ["BTCUSD", "MCOUSD", "FAIRUSD"]

def get_performing_stocks(tickers, volume_threshold=100):
    for result in track_stocks_parallel(tickers, interval=5,target_percentage_increase=volume_threshold):
        ticker, percentage_change, initial_price, current_price, change_percentage, initial_volume, current_volume, current_timestamp = result
        
        text = f"Stock volume for `{ticker}` increased by {change_percentage:.2f}% \n"\
                f"Price before increase: 💰{initial_price} \n"\
                f"Price after increase: 💰{current_price} \n"\
                f"Change Percentage: 📈{percentage_change:.2f}%\n"\
                f"Volume before increase: {initial_volume}\n"\
                f"Volume after increase: {current_volume}\n"\
                f"Time of increase: 🕒{datetime.fromtimestamp(current_timestamp)}\n"\
                "-----------------------------------"
        yield text       
    print(f"Stock: {ticker}")
    print(f"Percentage Change: {percentage_change}%")
    print(f"Initial Price: {initial_price}")
    print(f"Current Price: {current_price}")
    print(f"Change Percentage: {change_percentage}%")
    print(f"Initial Volume: {initial_volume}")
    print(f"Current Volume: {current_volume}")
    print(f"Timestamp: {current_timestamp}")
    
    
# get_performing_stocks(tickers)   