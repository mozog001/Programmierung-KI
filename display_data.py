import API as api

# get a list of stock prices
def get_stocks_list(stock_symbol, start_date, end_date):
    # Fetch stock data
    data = api.StockData(stock_symbol)
    stock_data = data.get_stock_data(start_date, end_date)

    # Turn data into a list of tuples [(date timestamp, open price, close price)]
    data_list = []
    for index_timestamp, row in stock_data.iterrows():
        timestamp_to_str = index_timestamp.strftime('%Y-%m-%d %H:%M:%S%z')
        data_list.append((timestamp_to_str, row["Open"], row["Close"]))
    return data_list

print(get_stocks_list("AAPL", "2020-01-01", "2020-01-10"))

#get a list of stock news links
def get_stock_news(stock_symbol, date):
    # Fetch stock News
    data = api.StockData(stock_symbol)
    stock_news = data.get_stock_news(date)

    # Turn data into a list of links [link1, link2, ...]
    links = stock_news["Link"].tolist()
    return links

print(get_stock_news("AAPL", "2020-01-01"))
