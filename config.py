from dotenv import dotenv_values

config = dotenv_values(".env")

API_ENDPOINT = "https://www.alphavantage.co/query"
BOT_TOKEN = config["BOT_TOKEN"]
API_KEY = config["API_KEY"]
RAPID_API_KEY = config["RAPID_API_KEY"]

class ValidIntervals:    
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    MIN_60 = "60min"

    # Default value
    DEFAULT= MIN_5