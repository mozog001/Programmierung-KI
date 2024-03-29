import yfinance as yf
import pandas as pd
from Low_Level.Database import Database as StockDB

""" 
Diese Skript erstellt über das Package yfinance (https://pypi.org/project/yfinance/)eine Verbindung zur 
Yahoo Finance API (https://legal.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.html). 
Es werden Aktiendaten, Unternehmensinformationen und Links von aktuellen Finanznachrichten zum abgefragten 
Unternehmen abzurufen. Die gesammelten Daten werden in einem Pandas-DataFrame gespeichert und zur Datenbank geschickt
"""


class StockData:
    def __init__(self):  # Definition Klassenattribute
        self.stockname = None
        self.stock = None
        self.start = None
        self.end = None
        self.symbol = None
        self.long_name = None
        self.currency = None
        self.industry = None
        self.headquarter = None
        self.news = None
        self.stock_news_links = None
        self.news_date = None
        self.s_news = None
        self.s_data = None

    def get_stock_data(self, stockname, start, end):
        """
        Ruft die historischen Aktienkurse auf. Bei der Erstellung des Ticker-Objekts muss der symbolische Stockname von
        Yahoo-Finance (https://de.finance.yahoo.com/) angegeben werden.
        :param stockname: Beispiel: Apple = AAPL
        :param start: Startdatum der Aktienkurse im Format YYYY-MM-DD
        :param end: Enddatum der Aktienkurse im Format YYYY-MM-DD
        :return: Pandas-DataFrame mit den historischen Aktienkursen
        """
        try:
            self.stockname = stockname
            self.stock = yf.Ticker(stockname)
            self.start = start
            self.end = end
            data = self.stock.history(start=start, end=end, actions=None)
            data = data.reset_index()  # Dataframe Index Datum wird gelöst
            data['Date'] = data['Date'].dt.date  # Anpassung Datumsformat YYYY-MM-DD ohne Uhrzeit
            data = data.set_index("Date")  # Datum wieder als Index
            return data
        except Exception as e:
            print(f"Ticker-Symbol konnte nicht erstellt werden {e}")

    def get_stock_info(self, stockname):
        """
        Allgemeine Informationen zum betrachteten Unternehmen werden abgerufen.
        :param stockname: Symbolischer Stockname
        :return Tuple mit den Informationen zum Unternehmen
        """
        try:
            self.stockname = stockname
            self.stock = yf.Ticker(stockname)
            self.long_name = self.stock.info["longName"]
            self.currency = self.stock.info["currency"]
            self.industry = f'{self.stock.info["industry"]} {self.stock.info["sector"]}'
            self.headquarter = (
                f'{self.stock.info["address1"]} {self.stock.info["zip"]} '
                f'{self.stock.info["city"]} {self.stock.info["country"]}'
            )
            return self.long_name, self.currency, self.industry, self.headquarter
        except Exception as e:
            print(f"Unternehmensinformationen konnten nicht abgerufen werden {e}")

    def get_stock_news(self, stockname, date):
        """
        Es werden aktuelle Links, die zu Finanznachrichten des betrachteten Unternehmens abgerufen. Es ist nicht
        möglich Finanznachrichten der Vergangenheit abzurufen. Das Datum wird nur verwendet, um den Links das
        Abrufdatum zuzuordnen. Links mit Datum werden in einem Pandas-DataFrame abgelegt
        :param stockname: symbolischer Stockname
        :param date: Datum des Abrufs im Format YYYY-MM-DD
        :return: Pandas-DataFrame mit den Links zu den Finanznachrichten
        """
        try:
            self.stockname = stockname
            self.stock = yf.Ticker(stockname)
            self.news = self.stock.news
            self.long_name = self.stock.info["longName"]
            self.stock_news_links = [link["link"] for link in self.news]
            self.news_date = [date] * len(self.stock_news_links)  # Jeder Link bekommt eine Zeile und ein Datum
            self.s_news = pd.DataFrame(
                ({"Date": self.news_date, "Link": self.stock_news_links, "Stock_name": self.long_name})
            )
            return self.s_news
        except Exception as e:
            print(f"Finanznachrichten konnten nicht abgerufen werden {e}")

    def get_data(self, data, long_name, currency, industry, headquarter, stockname):
        """
        Zusammenführung von Aktienkursen und Informationen und Aufbereitung für die Datenbank.
        :param data: Pandas-DataFrame mit den historischen Aktienkursen
        :param long_name: Unternehmensnahme
        :param currency: Währung des Unternehmens
        :param industry: Branche des Unternehmens
        :param headquarter: Sitz des Unternehmens
        :param stockname: symbolischer Stockname
        :return: Pandas-DataFrame mit den historischen Aktienkursen und Informationen
        """
        self.stockname = stockname
        self.s_data = pd.DataFrame(data)
        self.long_name = [long_name] * len(data)
        self.currency = [currency] * len(data)
        self.industry = [industry] * len(data)
        self.headquarter = [headquarter] * len(data)
        self.s_data["symbol"] = [self.stockname] * len(data)
        self.s_data["stock_long_name"] = long_name
        self.s_data["stock_currency"] = currency
        self.s_data["stock_industry"] = industry
        self.s_data["stock_headquarter"] = headquarter
        return self.s_data


if __name__ == "__main__":
    stockDB = StockDB.StockDatabase()
    stock_name = "AAPL"
    start_date = "2015-12-01"
    end_date = "2016-12-04"
    stock = StockData()
    stock_data = stock.get_stock_data(stock_name, start_date, end_date)
    stock_long_name, stock_currency, stock_industry, stock_headquarter = stock.get_stock_info(stock_name)
    stock_news = stock.get_stock_news(stock_name, end_date)
    stock_data_base = stock.get_data(stock_data, stock_long_name, stock_currency, stock_industry, stock_headquarter,
                                     stock_name)
    stockDataDict = stock_data_base.to_dict('index')
    stockDB.insert_stockdata(stockDataDict)
