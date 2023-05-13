import requests
import schedule
import time

import config as cfg

from config import ValidIntervals as INTERVALS

def check_stock_volume(stock_symbol: str, interval:str = INTERVALS.DEFAULT,volume_threshold: int = 100):
    """Checks if a certain stock's volume meets the specified criteria.

    Args:
        stock_symbol (str): Stock symbol.
        volume_threshold (int, optional): Minimum volume increase threshold. Defaults to 100.

    Returns:
        tuple: (stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage)
               Returns None if the volume criteria is not met or an error occurs.
    """
    url = "https://twelve-data1.p.rapidapi.com/time_series"

    querystring = {"symbol":str(stock_symbol),"interval":interval}

    headers = {
        "X-RapidAPI-Key": cfg.RAPID_API_KEY,
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }

    
    print(stock_symbol)
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", str(e))
        return None
    except ValueError:
        print("Invalid JSON response received.")
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

    if "values" not in data:
        return None  # Failed to retrieve data

    print("Checking...", stock_symbol)

    values = data["values"]

    if len(values) < 2:
        return None  # Insufficient data points

    volume_before = int(values[-2]["volume"])
    volume_after = int(values[-1]["volume"])
    volume_increase = volume_after - volume_before

    if volume_before == 0:
        volume_increase_percentage = 0
    else:
        volume_increase_percentage = (volume_increase / volume_before) * 100

    if volume_increase_percentage >= volume_threshold:
        time_before = values[-2]["datetime"]
        time_after = values[-1]["datetime"]
        print(f"Time Before: {time_before}")
        print(f"Time After: {time_after}")
        return (
            stock_symbol,
            volume_before,
            volume_after,
            volume_increase,
            volume_increase_percentage,
        )
    else:
        return None
# def check_stock_volume(stock_symbol: str, interval:str=INTERVALS.DEFAULT,volume_threshold: int = 100):
#     """Checks if a certain stock's volume meets the specified criteria.

#     Args:
#         stock_symbol (str): Stock symbol.
#         volume_threshold (int, optional): Minimum volume increase threshold. Defaults to 100.

#     Returns:
#         tuple: (stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage)
#                Returns None if the volume criteria is not met or an error occurs.
#     """
#     endpoint = f"https://api.polygon.io/v2/aggs/ticker/{stock_symbol}/range/1/minute/2023-05-13/2023-05-13"

#     params = {
#         "unadjusted": True,
#         "sort": "asc",
#         "limit": 2,
#         "apiKey": cfg.POLYGON_API_KEY,
#     }

#     data = None

#     try:
#         response = requests.get(endpoint, params=params)
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

#     if "results" not in data:
#         return None  # Failed to retrieve data

#     print("Checking...", stock_symbol)

#     results = data["results"]

#     volume_before = results[0]["v"]
#     volume_after = results[1]["v"]
#     volume_increase = volume_after - volume_before

#     volume_increase_percentage = (volume_increase / volume_before) * 100

#     if volume_increase_percentage >= volume_threshold:
#         print(results[0])
#         time_before = results[0]["t"]
#         time_after = results[1]["t"]
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

# def check_stock_volume(stock_symbol:str, interval:str=INTERVALS.DEFAULT, volume_threshold:int=100):    
#     """Checks If certain stock volume is meeting inputed critirea

#     Args:
#         stock_symbol (str): stock symbol
#         interval (str, optional): _description_. Defaults to INTERVALS.DEFAULT.
#         volume_threshold (int, optional): _description_. Defaults to 100.

#     Returns:
#         stock_symbol, latest_volume, volume_increase, volume_percentage_increase
#     """
#     params = {
#         "function": "TIME_SERIES_INTRADAY",
#         "symbol": stock_symbol,
#         "interval": interval,
#         "apikey": cfg.ALPHA_V_API_KEY
#     }

#     data = None

#     try:
#         response = requests.get(cfg.API_ENDPOINT, params=params)
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

#     if f"Time Series ({interval})" not in data: return None  # Failed to retrieve data

#     print("Checking...", stock_symbol)

#     time_series = data[f'Time Series ({interval})']  # Adjust this based on the desired time interval

#     time_points = list(time_series.keys())

#     volume_values = [int(time_series[time_point]['5. volume']) for time_point in time_points]

#     volume_before = volume_values[-2]
#     volume_after = volume_values[-1]
#     volume_increase = volume_after - volume_before
            
#     volume_increase_percentage = volume_increase / volume_before * 100
    
#     if volume_increase_percentage >= volume_threshold:
#         time_before = time_points[-2]
#         time_after = time_points[-1]
#         print(time_points)
#         print(f"Time Before: {time_before}")
#         print(f"Time After: {time_after}")
#         return (stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage)
#     else:
#         return None


 

# def check_stock_volume(stock_symbol:str, interval:str=INTERVALS.DEFAULT, volume_threshold:int=100):
#     """Checks if a certain stock's volume meets the specified criteria.

#     Args:
#         stock_symbol (str): Stock symbol.
#         volume_threshold (int, optional): Minimum volume increase threshold. Defaults to 100.

#     Returns:
#         tuple: (stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage)
#                Returns None if the volume criteria is not met or an error occurs.
#     """
#     params = {
#         "function": "TIME_SERIES_DAILY",
#         "symbol": stock_symbol,
#         "apikey": cfg.ALPHA_V_API_KEY
#     }

#     data = None

#     try:
#         response = requests.get(cfg.API_ENDPOINT, params=params)
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

#     if "Time Series (Daily)" not in data:
#         return None  # Failed to retrieve data

#     print("Checking...", stock_symbol)

#     time_series = data["Time Series (Daily)"]

#     time_points = list(time_series.keys())

#     volume_values = [int(time_series[time_point]["5. volume"]) for time_point in time_points]

#     volume_before = volume_values[-2]
#     volume_after = volume_values[-1]
#     volume_increase = volume_after - volume_before

#     volume_increase_percentage = (volume_increase / volume_before) * 100

#     if volume_increase_percentage >= volume_threshold:
#         print(time_points)
#         time_before = time_points[-2]
#         time_after = time_points[-1]
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


def get_performing_stocks(stocks_to_monitor, interval:str=INTERVALS.DEFAULT, volume_threshold:int=100):    
    print(interval)
    for stock in stocks_to_monitor:
        result = check_stock_volume(stock, interval, volume_threshold)
        if result:
            stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage = result
            text = f"Stock: {stock_symbol} \n"\
                    f"Volume Before: {volume_before}\n"\
                    f"Volume After: {volume_after}\n"\
                    f"Volume Increase: {volume_increase}\n"\
                    f"Increase Percentage: {volume_increase_percentage:.2f}%\n"\
                    "------------------------"
            print(text)
            yield text