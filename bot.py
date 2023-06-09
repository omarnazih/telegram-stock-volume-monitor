import telebot
import time
import config as cfg
from core import get_performing_stocks

from core_old import *
from util import get_filtered_symbols

# Initialize the bot with your bot token
bot = telebot.TeleBot(cfg.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Bot started. Please enter the interval in minutes (e.g., 30) for sending messages.")

    bot.register_next_step_handler(message, handle_interval_input)


def handle_interval_input(message):
    try:
        interval = int(message.text)
        if interval <= 0:
            bot.send_message(message.chat.id, "Invalid interval. Please enter a positive value.")
        else:
            bot.send_message(message.chat.id, f"Interval set to {interval} minutes. Please enter the volume threshold increase percentage.")

            bot.register_next_step_handler(message, handle_threshold_input, interval)
    except ValueError:
        bot.send_message(message.chat.id, "Invalid interval. Please enter a valid number.")


def handle_threshold_input(message, interval):
    try:
        threshold = int(message.text)
        if threshold < 0:
            bot.send_message(message.chat.id, "Invalid threshold. Please enter a non-negative value.")
        else:
            bot.send_message(message.chat.id, f"Volume threshold set to {threshold}. I will refresh my stock information every {interval} minutes.")
            bot.send_message(message.chat.id, f"Started monitoring stocks... \n If any stocks meet the threshold, I will send you a message.")
            try:
                while True:
                    # tickers = ["BTCUSD", "MCOUSD", "FAIRUSD"]
                    tickers = ["BTCUSD"]
                    # stock_generator = get_performing_stocks( """get_filtered_symbols()""", volume_threshold=threshold)
                    threshold=100 #!todo remove this
                    stock_generator = get_performing_stocks(tickers, volume_threshold=threshold)

                    while True:
                        try:
                            stock_info = next(stock_generator)
                            bot.send_message(message.chat.id, stock_info)
                        except StopIteration:
                            bot.send_message(message.chat.id, "No more stocks to monitor.")
                            break
                    
                    bot.send_message(message.chat.id, "Interval Finished Waiting for next Interval!")
                    # Sleep for the specified interval in minutes
                    time.sleep(interval * 60) #!todo remove, this interval is deprecated as I am using the new core.py
            except Exception as e:
                # Handling the exception
                print("An error occurred:", str(e))
                bot.send_message(message.chat.id, "There was an error! \n the Developer 👨🏻‍💻 has been notified!")        
    except ValueError:
        bot.send_message(message.chat.id, "Invalid threshold. Please enter a valid number.")



if __name__ == "__main__":
    # Start the bot
    bot.polling()