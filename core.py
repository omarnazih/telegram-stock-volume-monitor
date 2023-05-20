import requests
import schedule
from datetime import datetime
import time

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


def track_stock_volume(ticker:str, threshold_percentage:int=100):
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
        # time.sleep(interval_minutes * 60)
                
        # Get current stock volume, price, and timestamp
        response = requests.get(url)
        data = response.json()
        data = data[0]
        current_volume = data['volume']
        current_price = data['price']
        change_percentage = data['changesPercentage']
        current_timestamp = data['timestamp']

        # Calculate percentage change in volume
        percentage_change = ((current_volume - initial_volume) / initial_volume) * 100

        # Check if the volume increase exceeds the threshold
        if percentage_change >= threshold_percentage:
            yield(
                ticker,
                percentage_change,
                initial_price,
                current_price,
                change_percentage,
                initial_volume,
                current_volume,
                current_timestamp,
            )        


        # Update initial volume, price, and timestamp for the next iteration
        initial_volume = current_volume
        initial_price = current_price
        # !Rmove
        time.sleep(1 * 60)


def get_performing_stocks(stocks_to_monitor, interval:str=INTERVALS.DEFAULT, volume_threshold:int=100):    

    for stock in stocks_to_monitor:

        volume_generator = track_stock_volume(stock)

        while True:
            try:
                result = next(volume_generator)
                if result:
                    ticker, percentage_change, initial_price, current_price, change_percentage, initial_volume, current_volume, current_timestamp = result
                    text = f"Stock volume for `{ticker}` increased by {percentage_change:.2f}% \n"\
                            f"Price before increase: 💰{initial_price} \n"\
                            f"Price after increase: 💰{current_price} \n"\
                            f"Change Percentage: 📈{change_percentage}\n"\
                            f"Volume before increase: {initial_volume}\n"\
                            f"Volume after increase: {current_volume}\n"\
                            f"Time of increase: 🕒{datetime.fromtimestamp(current_timestamp)}\n"\
                            "-----------------------------------"
                    yield text                
                
            except StopIteration:
                print("No more data!")
                break        


if __name__ == "__main__":
    gen = get_performing_stocks(["AAPL"])
    for g in gen:
        print(g)