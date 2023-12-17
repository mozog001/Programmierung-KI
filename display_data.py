import API as api
import Database as db
from datetime import datetime

class DisplayData:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol

    def fetch_stocks(self, start_date, end_date):
        try:
            data = api.StockData(self.stock_symbol)

            #parse dates
            parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S%z')
            parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S%z')
            stock_data = data.get_stock_data(parsed_start_date, parsed_end_date)

            # Turn data into a list of tuples [(date timestamp, open price, close price)]
            data_list = []
            for index_timestamp, row in stock_data.iterrows():
                parsed_tstamp = index_timestamp.strftime('%Y-%m-%d %H:%M:%S%z')
                data_list.append((parsed_tstamp , row["Open"], row["Close"]))
            return data_list
        except Exception as e:
            return f"Error fetching stock data: {str(e)}"

    def get_stocks_list(self, start_date, end_date):
        try:
            # Fetch stock data from Database
            test_db = db.StockDatabase()
            db_data = test_db.getStockHistoryData(self.stock_symbol, start_date, end_date)

            # Turn DB data into a list of tuples [(date timestamp, open price, close price)]
            stocks = []
            for stock in db_data:
                stocks.append((stock[1], stock[2], stock[5]))

            # Check if DB data is empty
            if len(stocks) <= 0:
                fetched_stocks = self.fetch_stocks(start_date, end_date)
                return fetched_stocks

            # Check if fetch_stocks is needed for start_date
            if stocks[0][0] > start_date:
                fetched_stocks = self.fetch_stocks(start_date, stocks[0][0])
                if fetched_stocks:
                    stocks = fetched_stocks + stocks

            # Check if fetch_stocks is needed for end_date
            if stocks[-1][0] < end_date:
                fetched_stocks = self.fetch_stocks(stocks[-1][0], end_date)
                if fetched_stocks:
                    stocks = stocks + fetched_stocks
            return stocks
        except Exception as e:
            return f"Error getting stock list: {str(e)}"

    def get_stock_news(self, date):
        try:
            # Fetch stock News
            data = api.StockData(self.stock_symbol)
            stock_news = data.get_stock_news(date)

            # Turn data into a list of links [link1, link2, ...]
            links = stock_news["Link"].tolist()
            return links
        except Exception as e:
            return f"Error getting stock news: {str(e)}"

display = DisplayData("TYEKF")
print(display)
print(display.get_stocks_list("2023-11-28 00:00:00-05:00", "2023-12-30 00:00:00-05:00"))#print(display.fetch_stocks("2023-11-28 00:00:00-05:00", "2023-12-30 00:00:00-05:00"))
print(display.get_stock_news("2023-11-28 00:00:00-05:00"))
