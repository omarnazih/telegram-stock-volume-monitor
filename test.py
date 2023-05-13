import requests
import config as cfg

def check_volume_increase(stock_symbol, time_interval, volume_increase_percentage):
    api_key = cfg.ALPHA_V_API_KEY

    # Make a request to the Alpha Vantage API to get the stock's intraday volume data
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval={time_interval}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if f'Time Series ({time_interval})' in data:  # Adjust this based on the desired time interval
        time_series = data[f'Time Series ({time_interval})']  # Adjust this based on the desired time interval

        time_points = list(time_series.keys())
        print(time_points)
        volume_values = [int(time_series[time_point]['5. volume']) for time_point in time_points]

        volume_before = volume_values[-2]
        volume_after = volume_values[-1]
        volume_increase = volume_after - volume_before
                
        volume_increase_perc = volume_increase / volume_before * 100

        time_before = time_points[-2]
        time_after = time_points[-1]
        
        if volume_increase_perc >= volume_increase_percentage:
            print(f"Stock Symbol: {stock_symbol}")
            print(f"Time Interval: {time_interval}")
            print(f"Volume Before: {volume_before}")
            print(f"Volume After: {volume_after}")
            print(f"Time Before: {time_before}")
            print(f"Time After: {time_after}")
            print(f"Volume Increase: {volume_increase}")
            print(f"Volume Increase Percentage: {volume_increase_perc:.2f}%")
            return (stock_symbol, volume_before, volume_after, volume_increase)
        else:
            print("Criteria not met: Volume increase percentage is below specified threshold.")
            return None
    else:
        print("Insufficient data available.")
        return None

# Example usage:
check_volume_increase('AAPL', '15min', 20)
