import requests
import schedule
import time

import config as cfg

from config import ValidIntervals as INTERVALS



def check_stock_volume(stock_symbol:str, interval:str=INTERVALS.DEFAULT, volume_threshold:int=100):    
    """Checks If certain stock volume is meeting inputed critirea

    Args:
        stock_symbol (str): stock symbol
        interval (str, optional): _description_. Defaults to INTERVALS.DEFAULT.
        volume_threshold (int, optional): _description_. Defaults to 100.

    Returns:
        stock_symbol, latest_volume, volume_increase, volume_percentage_increase
    """
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": stock_symbol,
        "interval": interval,
        "apikey": cfg.ALPHA_V_API_KEY
    }

    data = None

    try:
        response = requests.get(cfg.API_ENDPOINT, params=params)
        response.raise_for_status()  # Optional: Raise an exception if the request was not successful
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", str(e))
        return None
    except ValueError:
        print("Invalid JSON response received.")   
        return None

    if f"Time Series ({interval})" not in data: return None  # Failed to retrieve data

    print("Checking...", stock_symbol)

    time_series = data[f"Time Series ({interval})"]

    # Retrieve the latest two data points
    latest_time = max(time_series.keys())
    print(latest_time)
    latest_volume = int(time_series[latest_time]["5. volume"])
    print(latest_volume)

    previous_time = sorted(time_series.keys())[-2]
    print(previous_time)
    previous_volume = int(time_series[previous_time]["5. volume"])
    print(previous_volume)

    volume_increase = latest_volume - previous_volume
    volume_percentage_increase = (volume_increase / previous_volume) * 100
    volume_percentage_increase = f"{round(volume_percentage_increase, 2)}%"

    if volume_increase > volume_threshold:
        return (stock_symbol, latest_volume, volume_increase, volume_percentage_increase)
    else:
        return None



def get_performing_stocks(stocks_to_monitor, interval:str=INTERVALS.DEFAULT, volume_threshold:int=100):    
    print(interval)
    for stock in stocks_to_monitor:
        print(stock)
        result = check_stock_volume(stock, interval, volume_threshold)
        if result:
            symbol, latest_volume, volume_increase, volume_percentage_increase = result
            text = f"Stock: {symbol} \n"\
                    f"Latest Volume: {latest_volume}\n"\
                    f"Volume Increase: {volume_increase}\n"\
                    f"Increase Percentage: {volume_percentage_increase}\n"\
                    "------------------------"
            print(text)
            yield text