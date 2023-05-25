import finnhub

def check_stock_volume(stock_symbol: str, interval: str = "1", volume_threshold: int = 100):
    """Checks if a certain stock's volume meets the specified criteria.

    Args:
        stock_symbol (str): Stock symbol.
        interval (str, optional): Time interval for the volume data. Defaults to "1".
        volume_threshold (int, optional): Minimum volume increase threshold. Defaults to 100.

    Returns:
        tuple: (stock_symbol, volume_before, volume_after, volume_increase, volume_increase_percentage)
               Returns None if the volume criteria is not met or an error occurs.
    """
    finnhub_client = finnhub.Client(api_key="chftkk9r01qhsjlal1ggchftkk9r01qhsjlal1h0")  # Replace with your Finnhub API key

    try:
        # Retrieve historical price data
        res = finnhub_client.stock_candles(stock_symbol, interval, 2)
    except Exception as e:
        print("An error occurred:", str(e))
        return None

    if "c" not in res or "v" not in res:
        return None  # Failed to retrieve data

    print("Checking...", stock_symbol)

    close_prices = res["c"]
    volumes = res["v"]

    if len(close_prices) < 2 or len(volumes) < 2:
        return None  # Insufficient data points

    volume_before = volumes[-2]
    volume_after = volumes[-1]
    volume_increase = volume_after - volume_before

    if volume_before == 0:
        volume_increase_percentage = 0
    else:
        volume_increase_percentage = (volume_increase / volume_before) * 100

    if volume_increase_percentage >= volume_threshold:
        return (
            stock_symbol,
            volume_before,
            volume_after,
            volume_increase,
            volume_increase_percentage,
        )
    else:
        return None
    
    
print(check_stock_volume("AAPL"))    
