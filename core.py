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

    if f"Time Series ({interval})" not in data: return None  # Failed to retrieve data

    print("Checking...", stock_symbol)

    time_series = data[f'Time Series ({interval})']  # Adjust this based on the desired time interval

    time_points = list(time_series.keys())

    volume_values = [int(time_series[time_point]['5. volume']) for time_point in time_points]

    volume_before = volume_values[-2]
    volume_after = volume_values[-1]
    volume_increase = volume_after - volume_before
            
    volume_increase_percentage = volume_increase / volume_before * 100
    
    if volume_increase_percentage >= volume_threshold:
        time_before = time_points[-2]
        time_after = time_points[-1]        
        # print(f"Time Before: {time_before}")
        # print(f"Time After: {time_after}")
        return (stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage)
    else:
        return None



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