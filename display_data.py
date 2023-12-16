import API as api
import Database as db
from datetime import datetime

# try catches
# class form

# # get a list of stock prices
# def get_stocks_list(stock_symbol, start_date, end_date):
#     # Fetch stock data
#     data = api.StockData(stock_symbol)
#     stock_data = data.get_stock_data(start_date, end_date)

#     # Turn data into a list of tuples [(date timestamp, open price, close price)]
#     data_list = []
#     for index_timestamp, row in stock_data.iterrows():
#         parsed_date = index_timestamp.strftime('%Y-%m-%d')
#         data_list.append((parsed_date , row["Open"], row["Close"]))
#     return data_list

# print(get_stocks_list("TYEKF", "2020-01-01", "2020-01-10"))

# Fetch fresh stock data from API
def fetch_stocks(stock_symbol, start_date, end_date):
    data = api.StockData(stock_symbol)

    # print(start_date, end_date)
    parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S%z')
    parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S%z')

    # print(parsed_start_date, parsed_end_date)

    stock_data = data.get_stock_data(parsed_start_date, parsed_end_date)

    # Turn data into a list of tuples [(date timestamp, open price, close price)]
    data_list = []
    for index_timestamp, row in stock_data.iterrows():
        parsed_tstamp = index_timestamp.strftime('%Y-%m-%d %H:%M:%S%z')
        data_list.append((parsed_tstamp , row["Open"], row["Close"]))
    return data_list

# print(fetch_stocks("TYEKF", "2023-12-01 00:00:00-05:00", "2023-12-02 00:00:00-05:00"))
# print(fetch_stocks("TYEKF", "2020-12-01 00:00:00-0500", "2020-12-02 00:00:00-0500"))
# print(fetch_stocks("TYEKF", "2020-12-01", "2023-12-02"))
# print(fetch_stocks("TYEKF", "2023-11-28 00:00:00-05:00", "2023-12-30 00:00:00-05:00"))

# get a list of stock prices
def get_stocks_list(stock_symbol, start_date, end_date):
    # Fetch stock data from Database
    test_db = db.StockDatabase()
    db_data = test_db.getStockHistoryData(stock_symbol, start_date, end_date)

    # Turn DB data into a list of tuples [(date timestamp, open price, close price)]
    stocks = []
    for stock in db_data:
        stocks.append((stock[1], stock[2], stock[5]))

    # Check if DB data is empty
    if len(stocks) <= 0:
        print("empty")
        fetched_stocks = fetch_stocks(stock_symbol, start_date, end_date)
        return fetched_stocks

    # Check if fetch_stocks is needed for start_date
    if stocks[0][0] > start_date:
        print("before")
        fetched_stocks = fetch_stocks(stock_symbol, start_date, stocks[0][0])
        if fetched_stocks:
            stocks = fetched_stocks + stocks

    # Check if fetch_stocks is needed for end_date
    if stocks[-1][0] < end_date:
        print("after")
        fetched_stocks = fetch_stocks(stock_symbol, stocks[-1][0], end_date)
        if fetched_stocks:
            stocks = stocks + fetched_stocks
    return stocks

# print(get_stocks_list("TYEKF", "2020-07-26", "2023-11-09"))
# get_stocks_list("TYEKF", "2023-12-01", "2023-12-02")
# print(get_stocks_list("TYEKF", "2022-10-15 00:00:00-05:00", "2023-12-03 00:00:00-05:00"))
print(get_stocks_list("TYEKF", "2023-11-28 00:00:00-05:00", "2023-12-30 00:00:00-05:00"))

# #get a list of stock news links
# def get_stock_news(stock_symbol, date):
#     # Fetch stock News
#     data = api.StockData(stock_symbol)
#     stock_news = data.get_stock_news(date)

#     # Turn data into a list of links [link1, link2, ...]
#     links = stock_news["Link"].tolist()
#     return links

# print(get_stock_news("TYEKF", "2020-01-01"))


# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx

# import API as api

# # get a list of stock prices
# def get_stocks_list(stock_symbol, start_date, end_date):
#     # Fetch stock data
#     data = api.StockData(stock_symbol)
#     stock_data = data.get_stock_data(start_date, end_date)

#     # Turn data into a list of tuples [(date timestamp, open price, close price)]
#     data_list = []
#     for index_timestamp, row in stock_data.iterrows():
#         timestamp_to_str = index_timestamp.strftime('%Y-%m-%d %H:%M:%S%z')
#         data_list.append((timestamp_to_str, row["Open"], row["Close"]))
#     return data_list

# # print(get_stocks_list("TYEKF", "2023-12-01 00:00:00-05:00", "2023-12-02 00:00:00-05:00"))
# # print(get_stocks_list("TYEKF", "2020-12-01 00:00:00-0500", "2020-12-02 00:00:00-0500"))
# # print(get_stocks_list("TYEKF", "2020-12-01", "2023-12-02"))

# # #get a list of stock news links
# # def get_stock_news(stock_symbol, date):
# #     # Fetch stock News
# #     data = api.StockData(stock_symbol)
# #     stock_news = data.get_stock_news(date)

# #     # Turn data into a list of links [link1, link2, ...]
# #     links = stock_news["Link"].tolist()
# #     return links

# # #print(get_stock_news("TYEKF", "2020-01-01"))