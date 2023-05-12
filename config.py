from dotenv import dotenv_values, load_dotenv


config = load_dotenv()

if not config:
    config = dotenv_values(".env")

# Bot
BOT_TOKEN = config["BOT_TOKEN"]

# API Keys
ALPHA_V_API_KEY = config["ALPHA_V_API_KEY"]
IEX_API_KEY = config["IEX_API_KEY"]
RAPID_API_KEY = config["RAPID_API_KEY"]

# API End Points
API_ENDPOINT = "https://www.alphavantage.co/query"

# CSV
CSV_FILENAME = "stocks.csv"

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