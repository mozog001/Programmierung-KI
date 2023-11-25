import yfinance as yf  # https://pypi.org/project/yfinance/
import pandas as pd


def read_symbols(filepath):
    with open(filepath) as file:  # csv aus https://www.nasdaq.com/market-activity/stocks/screener exportiert
        return file.read()  # csv als Vorschlagewerte in GUI einbauen


def get_stock_data(start, end):
    data = stock.history(start=start, end=end, actions=None)  # Startwert sollte aus der Datenbank kommen
    return data  # End Wert über GUI oder aktuelle Datum


def get_stock_info():  # Zuordnung der Aktienkurse zum Unternehmen sowie allgemeine Infos
    long_name = stock.info["longName"]
    currency = stock.info["currency"]
    industry = f'{stock.info["industry"]} {stock.info["sector"]}'
    headquarter = f'{stock.info["address1"]} {stock.info["zip"]} {stock.info["city"]} {stock.info["country"]}'
    return long_name, currency, industry, headquarter


def get_stock_news(date):  # Links in GUI anzeigen mit Vorschau? Doppelte Links in Datenbank löschen
    news = stock.news  # Überprüfen in Datenbank, dass Link nicht doppelt vorkommt
    long_name = stock.info["longName"]
    stock_news_links = [link["link"] for link in news]
    news_date = [date] * len(stock_news_links)
    s_news = pd.DataFrame({"Date": news_date, "Link": stock_news_links, "Stock_name": long_name})
    return s_news


def get_data(data, long_name, currency, industry, headquarter):
    s_data = pd.DataFrame(data)
    long_name = [long_name] * len(data)
    currency = [currency] * len(data)
    industry = [industry] * len(data)
    headquarter = [headquarter] * len(data)
    s_data["stock_long_name"] = long_name
    s_data["stock_currency"] = currency
    s_data["stock_industry"] = industry
    s_data["stock_headquarter"] = headquarter
    return s_data


if __name__ == "__main__":
    symbols = read_symbols("symbols.csv")
    stock_name = "AAPL"
    try:
        if stock_name not in symbols:
            print("Aktien-Symbol nicht gefunden")
            raise ValueError
    except ValueError:
        print("Aktie nicht gefunden")
    stock = yf.Ticker(stock_name)
    start_date = "2020-10-01"
    end_date = "2023-11-25"
    stock_data = get_stock_data(start_date, end_date)
    stock_long_name, stock_currency, stock_industry, stock_headquarter = get_stock_info()
    stock_news = get_stock_news(end_date)
    stock_data_base = get_data(stock_data, stock_long_name, stock_currency, stock_industry, stock_headquarter)
    stock_data_base.to_csv("stock_data.csv")  # Datenbank Tabelle 1
    stock_news.to_csv("links.csv", index=False)  # Datenbank Tabelle 2 (Verknüpfung über Unternehmensnamen)
