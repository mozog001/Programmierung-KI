import sqlite3




class StockDatabase:

    """ Database for stock data
        Um die Datenbank zu testen, kann die Datei TestDatabase.py ausgeführt werden.
        Die Datenbank wird dann mit Testdaten gefüllt.
        Die Datenbank wird in der Datei StockDatabase.db gespeichert.
        Die Datenbank enthält 3 Tabellen:

        1. links: Enthält die Links zu den einzelnen Aktien
        2. stock_data: Enthält die historischen Daten der Aktien
        3. symbols: Enthält die Symbole der Aktien

        Die Datenbank wird mit der Klasse StockDatabase erstellt.
        Die Klasse enthält folgende Methoden:

        1. insert_link: Fügt einen Link in die Tabelle links ein
        2. insert_stockdata: Fügt die historischen Daten einer Aktie in die Tabelle stock_data ein
        3. insert_symbol: Fügt die Symbole der Aktien in die Tabelle symbols ein
        4. search_symbol: Sucht nach einem Symbol in der Tabelle symbols
        5. getStockHistoryData: Liefert die historischen Daten einer Aktie aus der Tabelle stock_data

        In Pycharm kann die Datenbank mit dem Plugin "DB Browser for SQLite" betrachtet werden.
    """

    def __init__(self):
        # Stellt eine Verbindung zur lokalen Datenbank "StockDatabase.db her
        self.conn = sqlite3.connect('StockDatabase.db')
        self.cur = self.conn.cursor()
        # Erstelle notwendige Tabellen "Datenmodellierung" --> links, stock_data, symbols
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, date TEXT, link TEXT, stock_name TEXT UNIQUE)")

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS stock_data (id INTEGER PRIMARY KEY, date TEXT, open REAL, high REAL, \
            low REAL,close REAL, volume INT, symbol TEXT ,stock_long_name TEXT , stock_currency TEXT, stock_industry TEXT ,\
            stock_headquarter TEXT, UNIQUE(date, stock_long_name))")

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS symbols (id INTEGER PRIMARY KEY, symbol TEXT UNIQUE, name TEXT UNIQUE, \
            country TEXT,ipo_year INTEGER, sector TEXT, industry TEXT)")

        self.conn.commit()

    # Fügt einen Link in die Tabelle links ein
    def insert_link(self, date, link, stock_name):
        self.cur.execute(
            "INSERT OR IGNORE INTO links VALUES (NULL, ?, ?, ?)", (date, link, stock_name))
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
    def insert_symbol__(self, symbol, name, country, ipo_year, sector, industry):
        self.cur.execute(
             "INSERT OR IGNORE INTO symbols VALUES (NULL, ?, ?, ?, ?, ?, ?)",(symbol, name, country, ipo_year, sector, industry))
        self.conn.commit()
    def insert_symbol(self, data):
        for dataValues in data:
            self.cur.execute(
                "INSERT OR IGNORE INTO symbols VALUES (NULL, ?, ?, ?, ?, ?, ?)", (
                    dataValues['symbol'], dataValues['name'], dataValues['country'], dataValues['ipo_year'], dataValues['sector'], dataValues['industry']))
            self.conn.commit()



    # Liefert die historischen Daten einer Aktie aus der Tabelle stock_data, es wird eine Liste mit den gefundenen Daten zurückgegeben
    # Die Daten werden nach Datum sortiert ausgegeben
    def getStockHistoryData(self, symbol, beginDate, endDate):
        self.cur.execute(
            "SELECT * FROM stock_data WHERE symbol = ? and  Date >= ? and Date <= ? ORDER BY Date ASC", [symbol, beginDate, endDate])

        rows = self.cur.fetchall()
        return rows

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
