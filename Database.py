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
            low REAL,close REAL, volume INT, stock_long_name TEXT UNIQUE, stock_currency TEXT, stock_industry TEXT ,\
            stock_headquarter TEXT)")

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS symbols (id INTEGER PRIMARY KEY, symbol TEXT UNIQUE, name TEXT UNIQUE, \
            country TEXT,ipo_year INTEGER, sector TEXT, industry TEXT)")

        self.conn.commit()

    def insert_link(self, date, link, stock_name):
        self.cur.execute(
            "INSERT OR IGNORE INTO links VALUES (NULL, ?, ?, ?)", (date, link, stock_name))
        self.conn.commit()

    def insert_stockdata(self, date, open, high, low, close, volume, stock_long_name, stock_currency, stock_industry, stock_headquarter):
        self.cur.execute(
            "INSERT OR IGNORE INTO stock_data VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date, open, high, low, close, volume, stock_long_name, stock_currency, stock_industry, stock_headquarter))
        self.conn.commit()

    def insert_symbol(self, symbol, name, country, ipo_year, sector, industry):
        self.cur.execute(
            "INSERT OR IGNORE INTO symbols VALUES (NULL, ?, ?, ?, ?, ?, ?)", (symbol, name, country, ipo_year, sector, industry))
        self.conn.commit()


    def search_symbol(self, name=""):

        self.cur.execute(
            "SELECT * FROM symbols WHERE name like ?", [str("%"+name+"%")])

        rows = self.cur.fetchall()
        return rows



    def __del__(self):
        self.conn.close()
