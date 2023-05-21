import time
from datetime import datetime

import requests
from requests.exceptions import RequestException

import schedule

import config as cfg
from config import ValidIntervals as INTERVALS


# def check_stock_volume(stock_symbol: str, interval:str = INTERVALS.DEFAULT,volume_threshold: int = 100):
#     """Checks if a certain stock's volume meets the specified criteria.

#     Args:
#         stock_symbol (str): Stock symbol.
#         volume_threshold (int, optional): Minimum volume increase threshold. Defaults to 100.

#     Returns:
#         tuple: (stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage)
#                Returns None if the volume criteria is not met or an error occurs.
#     """
#     url = "https://twelve-data1.p.rapidapi.com/time_series"

#     querystring = {"symbol":str(stock_symbol),"interval":interval}

#     headers = {
#         "X-RapidAPI-Key": cfg.RAPID_API_KEY,
#         "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
#     }

    
#     print(stock_symbol)
#     try:
#         response = requests.get(url, headers=headers, params=querystring)
#         data = response.json()
#     except requests.exceptions.RequestException as e:
#         print("An error occurred during the request:", str(e))
#         return None
#     except ValueError:
#         print("Invalid JSON response received.")
#         return None
#     except Exception as e:
#         print("An error occurred:", str(e))
#         return None

#     if "values" not in data:
#         return None  # Failed to retrieve data

#     print("Checking...", stock_symbol)

#     values = data["values"]

#     if len(values) < 2:
#         return None  # Insufficient data points

#     volume_before = int(values[-2]["volume"])
#     volume_after = int(values[-1]["volume"])
#     volume_increase = volume_after - volume_before

#     if volume_before == 0:
#         volume_increase_percentage = 0
#     else:
#         volume_increase_percentage = (volume_increase / volume_before) * 100

#     if volume_increase_percentage >= volume_threshold:
#         time_before = values[-2]["datetime"]
#         time_after = values[-1]["datetime"]
#         print(f"Time Before: {time_before}")
#         print(f"Time After: {time_after}")
#         return (
#             stock_symbol,
#             volume_before,
#             volume_after,
#             volume_increase,
#             volume_increase_percentage,
#         )
#     else:
#         return None


# def get_stock_data(ticker: str):
#     api_key = cfg.FMP_API_KEY
#     url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"

#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for non-successful status codes
#         data = response.json()
#         return data[0]
#     except RequestException as e:
#         print(f"An error occurred: {e}")
def get_stock_data(ticker: str):
    if ticker == "AAPL":
        return {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": 175.16,
    "changesPercentage": 0.0628,
    "change": 0.11,
    "dayLow": 174.95,
    "dayHigh": 176.29,
    "yearHigh": 176.29,
    "yearLow": 124.17,
    "marketCap": 2755039164867,
    "priceAvg50": 164.0296,
    "priceAvg200": 152.09656,
    "exchange": "NASDAQ",
    "volume": 50895166,
    "avgVolume": 58266351,
    "open": 176.39,
    "previousClose": 175.05,
    "eps": 5.9,
    "pe": 29.69,
    "earningsAnnouncement": "2023-07-26T20:00:00.000+0000",
    "sharesOutstanding": 15728700416,
    "timestamp": 1684526404
  }
    else:
        return {
        "symbol": "NOT AAPL",
        "name": "Apple Inc.",
        "price": 175.16,
        "changesPercentage": 0.0628,
        "change": 0.11,
        "dayLow": 174.95,
        "dayHigh": 176.29,
        "yearHigh": 176.29,
        "yearLow": 124.17,
        "marketCap": 2755039164867,
        "priceAvg50": 164.0296,
        "priceAvg200": 152.09656,
        "exchange": "NASDAQ",
        "volume": 50895166,
        "avgVolume": 58266351,
        "open": 176.39,
        "previousClose": 175.05,
        "eps": 5.9,
        "pe": 29.69,
        "earningsAnnouncement": "2023-07-26T20:00:00.000+0000",
        "sharesOutstanding": 15728700416,
        "timestamp": 1684526404
    }


def calculate_percentage_change(initial_volume: float, current_volume: float):
    return ((current_volume - initial_volume) / initial_volume) * 100

def track_stock_volume(ticker: str, threshold_percentage: int = 100):
    print("Started Tracking...")
    
    stock_data = get_stock_data(ticker)
    initial_volume = stock_data['volume']
    initial_price = stock_data['price']

    while True:
        # time.sleep(1 * 60)  # Wait for the specified interval
                
        stock_data = get_stock_data(ticker)
        current_volume = stock_data['volume']
        current_price = stock_data['price']
        change_percentage = stock_data['changesPercentage']
        current_timestamp = stock_data['timestamp']

        percentage_change = calculate_percentage_change(initial_volume, current_volume)

        # if percentage_change >= threshold_percentage:
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
        
        initial_volume = current_volume
        initial_price = current_price

# def get_performing_stocks(stocks_to_monitor, interval:str=INTERVALS.DEFAULT, volume_threshold:int=100):    

#     for stock in stocks_to_monitor:

#         volume_generator = track_stock_volume(stock)

#         while True:
#             try:
#                 result = next(volume_generator)
#                 if result:
#                     ticker, percentage_change, initial_price, current_price, change_percentage, initial_volume, current_volume, current_timestamp = result
#                     text = f"Stock volume for `{ticker}` increased by {percentage_change:.2f}% \n"\
#                             f"Price before increase: 💰{initial_price} \n"\
#                             f"Price after increase: 💰{current_price} \n"\
#                             f"Change Percentage: 📈{change_percentage}\n"\
#                             f"Volume before increase: {initial_volume}\n"\
#                             f"Volume after increase: {current_volume}\n"\
#                             f"Time of increase: 🕒{datetime.fromtimestamp(current_timestamp)}\n"\
#                             "-----------------------------------"
#                     yield text                
                
#             except StopIteration:
#                 print("No more data!")
#                 break        


if __name__ == "__main__":
    tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "FB"]
    generator = track_stock_volume(tickers, num_processes=5)

    for data in generator:
        print(data)