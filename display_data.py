import API as api
import Database as db
from datetime import datetime, timedelta

class DisplayData:
    def __init__(self):
        self.api_data = api.StockData()
        self.db_data = db.StockDatabase()

    def fetch_stocks(self, stock_symbol, start_date, end_date):
        try:
            #parse dates
            #parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S%z')
            parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            stock_data = self.api_data.get_stock_data(stock_symbol, start_date, parsed_end_date)

            # Turn data into a list of tuples [(date, open price, close price)]
            data_list = []
            for index_timestamp, row in stock_data.iterrows():
                parsed_tstamp = index_timestamp.strftime('%Y-%m-%d')
                data_list.append((parsed_tstamp , row["Open"], row["Close"]))
            return data_list
        except Exception as e:
            return f"Error fetching stock data: {str(e)}"

    def get_stocks_list(self, stock_symbol, start_date, end_date):
        try:
            # Fetch stock data from Database
            db_data = self.db_data.getStockHistoryData(stock_symbol, start_date, end_date)

            # Turn DB data into a list of tuples [(date, open price, close price)]
            stocks = []
            for stock in db_data:
                stocks.append((stock[1], stock[2], stock[5]))

            # Check if DB data is empty
            if len(stocks) <= 0:
                fetched_stocks = self.fetch_stocks(stock_symbol, start_date, end_date)
                return fetched_stocks

            # Check if fetch_stocks is needed for start_date
            if start_date is None or stocks[0][0] > start_date:
                fetched_stocks = self.fetch_stocks(stock_symbol, start_date, stocks[0][0])
                if fetched_stocks:
                    stocks.extend(fetched_stocks)

            # Check if fetch_stocks is needed for end_date
            if stocks[-1][0] < end_date:
                fetched_stocks = self.fetch_stocks(stock_symbol, stocks[-1][0], end_date)
                if fetched_stocks:
                    stocks.extend(fetched_stocks)
            return stocks
        except Exception as e:
            return f"Error getting stock list: {str(e)}"

    def get_stock_news(self, stock_symbol, date):
        try:
            # Fetch stock News
            stock_news = self.api_data.get_stock_news(stock_symbol, date)

            # Turn data into a list of links [link1, link2, ...]
            links = stock_news["Link"].tolist()
            return links
        except Exception as e:
            return f"Error getting stock news: {str(e)}"

def main():
    display = DisplayData()
    stock_symbol = "AMZN"
    start_date = "2023-12-11"
    end_date = "2023-12-15"
    print('get_stocks_list:')
    print(display.get_stocks_list(stock_symbol, start_date, end_date))
    #print('fetch_stocks:')
    #print(display.fetch_stocks(stock_symbol, start_date, end_date))
    #print('get_stock_news:')
    #print(display.get_stock_news(stock_symbol, start_date))

if __name__ == "__main__":
    main()