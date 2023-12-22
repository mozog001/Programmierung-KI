import re
import sqlite3




class StockDatabase:

    """ Database for stock data

        Die Datenbank wird in der Datei StockDatabase.db gespeichert.
        Die Datenbank enthält 2 Tabellen:


        1. stock_data: Enthält die historischen Daten der Aktien
        2. symbols: Enthält die Symbole der Aktien

        Die Datenbank wird mit der Klasse StockDatabase erstellt.
        Die Klasse enthält folgende Methoden:


        1. insert_stockdata: Fügt die historischen Daten einer Aktie in die Tabelle stock_data ein
        2. insert_symbol: Fügt die Symbole der Aktien in die Tabelle symbols ein
        3. search_symbol: Sucht nach einem Symbol in der Tabelle symbols
        4. get_all_symbols: Liefert alle Symbole aus der Tabelle symbols
        4. getStockHistoryData: Liefert die historischen Daten einer Aktie aus der Tabelle stock_data
        5. getStockCloseData: Liefert die historischen Schlusskurse einer Aktie aus der Tabelle stock_data

        In Pycharm kann die Datenbank mit dem Plugin "DB Browser for SQLite" betrachtet werden.
    """

    def __init__(self):
        # Stellt eine Verbindung zur lokalen Datenbank "StockDatabase.db her
        self.conn = sqlite3.connect('StockDatabase.db')
        self.cur = self.conn.cursor()
        # Erstelle notwendige Tabellen "Datenmodellierung" --> stock_data, symbols

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS stock_data (id INTEGER PRIMARY KEY, date TEXT, open REAL, high REAL, \
            low REAL,close REAL, volume INT, symbol TEXT ,stock_long_name TEXT , stock_currency TEXT, stock_industry TEXT ,\
            stock_headquarter TEXT, UNIQUE(date, stock_long_name))")

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS symbols (id INTEGER PRIMARY KEY, symbol TEXT UNIQUE, name TEXT UNIQUE, \
            country TEXT,ipo_year INTEGER, sector TEXT, industry TEXT)")

        self.conn.commit()


    # Fügt die historischen Daten einer Aktie in die Tabelle stock_data ein
    def insert_stockdata(self, data):
        for DataDate, dataValues in data.items():
            self.cur.execute(
                "INSERT OR IGNORE INTO stock_data VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    str(DataDate), dataValues['Open'], dataValues['High'], dataValues['Low'], dataValues['Close'], dataValues['Volume'], dataValues['symbol'], dataValues['stock_long_name'],
                    dataValues['stock_currency'], dataValues['stock_industry'], dataValues['stock_headquarter']))
            self.conn.commit()


    # Fügt die Symbole der Aktien in die Tabelle symbols ein
    def insert_symbol_(self, symbol, name, country, ipo_year, sector, industry):
        self.cur.execute(
             "INSERT OR IGNORE INTO symbols VALUES (NULL, ?, ?, ?, ?, ?, ?)",(symbol, name, country, ipo_year, sector, industry))
        self.conn.commit()

    def insert_symbol(self, data):
        for dataValues in data.values():
            self.cur.execute(
                "INSERT OR IGNORE INTO symbols VALUES (NULL, ?, ?, ?, ?, ?, ?)", (
                    dataValues['symbol'], dataValues['name'], dataValues['country'], dataValues['ipo year'], dataValues['sector'], dataValues['industry']))
            self.conn.commit()


    def getStockHistoryData(self, symbol, beginDate="1900-01-01" , endDate=str(sqlite3.Date.today())):
        """
        Funktion:        getStockHistoryData: Liefert die historischen Daten einer Aktie aus der Tabelle stock_data
                         Die Daten werden nach dem Datum sortiert ausgegeben.

        Parameter:       symbol(string):              Symbol der Aktie z.B. "AAPL"
                         beginDate(string), optional: Beginn der Aktienkurse, Format: YYYY-MM-DD  z.B. "2020-01-01" oder None
                         endDate(string), optional:   Ende der Aktienkurse, Format: YYYY-MM-DD  z.B. "2020-01-01" oder None

        Rückgabewert:    Liste mit den historischen Daten der Aktie. Die Liste ist leer, wenn keine Daten gefunden wurden.
                         Die Liste enthält Tupel, die die Daten der Aktie enthalten
                         z.B. [(1, '2020-01-01', 300.0, 400.0, 200.0, 350.0, 1000, 'AAPL', 'Apple Inc.', 'USD', 'Technology', 'Cupertino, California')]
                         Die Liste wird nach dem Datum sortiert zurückgegeben.
        """
        retValue = []

        if beginDate == None:
            beginDate = "1900-01-01"    # Beginn der Aktienkurse wird auf 1900-01-01 gesetzt

        if endDate == None:
            endDate = str(sqlite3.Date.today())     # Ende der Aktienkurse wird auf das aktuelle Datum gesetzt


        if type(beginDate)== str and type(endDate)== str:

            #Check date format  YYYY-MM-DD
            if re.search(r'^\d{4}-\d{2}-\d{2}$', beginDate) and re.search(r'^\d{4}-\d{2}-\d{2}$', endDate):

                self.cur.execute(
                    "SELECT * FROM stock_data WHERE symbol = ? and  Date >= ? and Date <= ? ORDER BY Date ASC", [symbol, beginDate, endDate])

                rows = self.cur.fetchall()
                retValue = rows

            else:  # Date format not correct
                raise ValueError("Date format not correct, expected YYYY-MM-DD")

        else:   # Date format not correct
                raise TypeError("String expected: beginDate, endDate")

        return retValue

    def getStockCloseData(self, symbol):
        self.cur.execute(
            "SELECT Date, close FROM stock_data WHERE symbol = ? ORDER BY Date ASC", [symbol])

        rows = self.cur.fetchall()
        return rows

    # Sucht nach einem Symbol in der Tabelle symbols, es wird eine Liste mit den gefundenen Symbolen zurückgegeben
    def search_symbol(self, name=""):

        self.cur.execute(
            "SELECT * FROM symbols WHERE name like ?", [str("%"+name+"%")])

        rows = self.cur.fetchall()
        return rows

    def get_all_symbols(self):
        self.cur.execute(
            "SELECT * FROM symbols")
        
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
