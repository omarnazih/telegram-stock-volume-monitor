import requests

def get_all_symbols():
    """Get Trending stock symbols"""
    url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/tr/trending"

    headers = {
        "X-RapidAPI-Key": "55efa72bb4mshe644238d11c5722p165df8jsnaed29d0f2305",
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