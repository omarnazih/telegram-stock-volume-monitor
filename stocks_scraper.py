from finviz.screener import Screener
import config as cfg


CSV_FILE = cfg.CSV_FILENAME


def generate_csv():
    # Filters From website finviz : https://finviz.com/screener.ashx?v=111&f=cap_micro,sh_float_u100,sh_price_u20
    filters = ['cap_micro', 'sh_float_u100','sh_price_u10']  # Shows companies Thas has cap micro,float under 100mil and price under20$

    # Get the performance table and sort it by price ascending
    stock_list = Screener(filters=filters, table='Performance', order='price') 

    # Export the screener results to .csv
    stock_list.to_csv(CSV_FILE)
    

if __name__ == "__main__":
    # !todo Create a cron job to run the scraper every day
    generate_csv()