from websocket import create_connection
import simplejson as json
ws = create_connection("wss://api.tiingo.com/iex")

subscribe = {
        'eventName':'subscribe',
        'authorization':'eb139cbdeb7f6fcea982996ea60db725654dcaa7',
        'eventData': {
            'thresholdLevel': 5
    }
}

ws.send(json.dumps(subscribe))
while True:
    print(ws.recv())
# import requests
# import config as cfg

# from datetime import datetime

# def get_stock_volume(symbol):
#     api_key = cfg.IEX_API_KEY
#     url = f'https://cloud.iexapis.com/stable/stock/{symbol}/chart/1d?token={api_key}'

#     try:
#         response = requests.get(url)
#         data = response.json()

#         # Get the latest and previous volume
#         latest_data = data[-1]
#         previous_data = data[-2]

#         latest_volume = latest_data['volume']
#         previous_volume = previous_data['volume']

#         # Get the timestamps
#         latest_timestamp = datetime.fromtimestamp(latest_data['date'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
#         previous_timestamp = datetime.fromtimestamp(previous_data['date'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

#         print(latest_timestamp, latest_volume, previous_timestamp, previous_volume)
#         return latest_timestamp, latest_volume, previous_timestamp, previous_volume

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return None


# def check_stock_volume(symbol, threshold, increase_percentage):
#     latest_timestamp, latest_volume, previous_timestamp, previous_volume = get_stock_volume(symbol)

#     if latest_timestamp is not None:
#         if latest_volume > threshold:
#             increase_percentage = (latest_volume - previous_volume) / previous_volume * 100

#             print(f"Latest Timestamp: {latest_timestamp}")
#             print(f"Latest Volume: {latest_volume}")
#             print(f"Previous Timestamp: {previous_timestamp}")
#             print(f"Previous Volume: {previous_volume}")
#             print(f"Increase Percentage: {increase_percentage:.2f}%")

#         else:
#             print(f"The stock volume for {symbol} is not greater than the threshold.")


# check_stock_volume('MSFT', 100, 10)


# # check_stock_volume('MSFT', 100)
# # import websocket
# # import json

# # def on_message(ws, message):
# #     data = json.loads(message)
# #     if 'data' in data:
# #         for item in data['data']:
# #             if 's' in item and item['s'] == 'AAPL':
# #                 volume = item['v']
# #                 print(f"Real-time Volume for AAPL: {volume}")

# # def on_error(ws, error):
# #     print(error)

# # def on_close(ws):
# #     print("Connection closed")

# # def on_open(ws):
# #     # Subscribe to real-time trades for AAPL
# #     ws.send(json.dumps({"type": "subscribe", "symbol": "AAPL", "trade": True}))

# # websocket.enableTrace(True)
# # ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=chftkk9r01qhsjlal1ggchftkk9r01qhsjlal1h0",
# #                             on_message=on_message,
# #                             on_error=on_error,
# #                             on_close=on_close)
# # ws.on_open = on_open
# # ws.run_forever()