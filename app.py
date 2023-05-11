import requests
import config as cfg

from datetime import datetime


def check_stock_volume(stock_symbol, interval='5min', volume_threshold=100):
    api_key = cfg.ALPHA_V_API_KEY
    api_endpoint = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": stock_symbol,
        "interval": interval,
        "apikey": api_key
    }

    try:
        response = requests.get(api_endpoint, params=params)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", str(e))
        return None

    if "Time Series (5min)" not in data:
        return None

    print("Checking...", stock_symbol)

    time_series = data["Time Series (5min)"]

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_volume = None
    previous_volume = 0

    for time, values in time_series.items():
        if time > current_time:
            break
        current_volume = float(values["5. volume"])
        previous_volume = current_volume

    if current_volume is None:
        return None

    volume_increase = current_volume - previous_volume
    volume_percentage_increase = (volume_increase / previous_volume) * 100
    volume_percentage_increase = f"{round(volume_percentage_increase, 2)}%"

    if volume_increase > volume_threshold:
        return (stock_symbol, current_volume, volume_increase, volume_percentage_increase)
    else:
        return None


from util import get_all_symbols

for stock in get_all_symbols():        
    # result = check_stock_volume(stock, interval, volume_threshold)
    result = check_stock_volume(stock)
    if result:
        symbol, latest_volume, volume_increase, volume_percentage_increase = result
        text = f"Stock: {symbol} \n"\
                f"Latest Volume: {latest_volume}\n"\
                f"Volume Increase: {volume_increase}\n"\
                f"Increase Percentage: {volume_percentage_increase}\n"\
                "------------------------"
        print(text)