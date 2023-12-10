import yfinance as yf  # https://pypi.org/project/yfinance/
import pandas as pd


class StockData:
    def __init__(self, stockname):
        self.stockname = stockname
        self.stock = yf.Ticker(stockname)
        self.filepath = None
        self.start = None
        self.end = None
        self.long_name = None
        self.currency = None
        self.industry = None
        self.headquarter = None
        self.news = None
        self.stock_news_links = None
        self.news_date = None
        self.s_news = None
        self.s_data = None

    def get_stock_data(self, start, end):
        self.start = start
        self.end = end
        data = self.stock.history(start=start, end=end, actions=None)  
        return data 

    def get_stock_info(self):  # Zuordnung der Aktienkurse zum Unternehmen sowie allgemeine Infos
        self.long_name = self.stock.info["longName"]
        self.currency = self.stock.info["currency"]
        self.industry = f'{self.stock.info["industry"]} {self.stock.info["sector"]}'
        self.headquarter = (
            f'{self.stock.info["address1"]} {self.stock.info["zip"]} '
            f'{self.stock.info["city"]} {self.stock.info["country"]}'
        )
        return self.long_name, self.currency, self.industry, self.headquarter

    def get_stock_news(self, date):  # Links in GUI anzeigen mit Vorschau? Doppelte Links in Datenbank löschen
        self.news = self.stock.news  
        self.long_name = self.stock.info["longName"]
        self.stock_news_links = [link["link"] for link in self.news]
        self.news_date = [date] * len(self.stock_news_links)
        self.s_news = pd.DataFrame(
            ({"Date": self.news_date, "Link": self.stock_news_links, "Stock_name": self.long_name})
        )
        return self.s_news

    def get_data(self, data, long_name, currency, industry, headquarter):
        self.s_data = pd.DataFrame(data)
        self.long_name = [long_name] * len(data)
        self.currency = [currency] * len(data)
        self.industry = [industry] * len(data)
        self.headquarter = [headquarter] * len(data)
        self.s_data["stock_long_name"] = long_name
        self.s_data["stock_currency"] = currency
        self.s_data["stock_industry"] = industry
        self.s_data["stock_headquarter"] = headquarter
        return self.s_data


if __name__ == "__main__":
    stock_name = "AAPL"
    start_date = "2020-10-01"
    end_date = "2023-12-04"
    with open("symbols.csv") as file:  # csv aus https://www.nasdaq.com/market-activity/stocks/screener exportiert 23.11.2023
        symbols = file.read()  # csv als Vorschlagewerte in GUI einbauen
    if stock_name not in symbols:
        raise ValueError("Aktien-Symbol falsch oder nicht in Liste vorhanden.")
    stock = StockData(stock_name)
    stock_data = stock.get_stock_data(start_date, end_date)
    stock_long_name, stock_currency, stock_industry, stock_headquarter = stock.get_stock_info()
    stock_news = stock.get_stock_news(end_date)
    stock_data_base = stock.get_data(stock_data, stock_long_name, stock_currency, stock_industry, stock_headquarter)
    stock_data_base.to_csv("stock_data.csv")  # Datenbank Tabelle 1
    stock_news.to_csv("links.csv", index=False)  # Datenbank Tabelle 2 (Verknüpfung über Unternehmensnamen)