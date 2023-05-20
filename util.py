import os
import csv
import requests
import config as cfg

from stocks_scraper import generate_csv

CSV_FILE = cfg.CSV_FILENAME
API_KEY = cfg.RAPID_API_KEY


def get_filtered_symbols():
    """Return Filterd Stock Symbols
    """

    "If csv files doesn't exist then generate it"
    if not os.path.exists(CSV_FILE): generate_csv()
        
        
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        
        symbols_list = [row['Ticker'] for row in reader]
        
        # Get the count of rows
        symbols_count = reader.line_num - 1

    print(f"Fetched ({symbols_count}) stock symbols!.")
    return symbols_list

 
def get_all_symbols():
    """Get Trending stock symbols"""
    url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/tr/trending"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    data_count = data[0]["count"]
    print(f"Fetched ({data_count}) stocks symbols from api")
    print("===============================================")
    

    if not data:
        return None
    
    return [symbol for symbol in data[0]["quotes"]]