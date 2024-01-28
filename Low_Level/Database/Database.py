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
        6. delete_stockdata: Löscht alle Einträge in der Tabelle stock_data

        In Pycharm kann die Datenbank mit dem Plugin "DB Browser for SQLite" betrachtet werden.
    """
    # ------------------------------------------------------------------------------------------------------------------
    # Initialisierung der Datenbank und Erstellung der Tabellen
    def __init__(self):
        try:
            # Stellt eine Verbindung zur lokalen Datenbank "StockDatabase.db her
            self.conn = sqlite3.connect('StockDatabase.db')
            self.cur = self.conn.cursor()

            # Erstelle notwendige Tabellen "Datenmodellierung" --> stock_data, symbols
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS stock_data (id INTEGER PRIMARY KEY, date TEXT, open REAL, high REAL, \
                low REAL,close REAL, volume INT, symbol TEXT ,stock_long_name TEXT , stock_currency TEXT, \
                stock_industry TEXT , stock_headquarter TEXT, UNIQUE(date, stock_long_name))")

            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS symbols (id INTEGER PRIMARY KEY, symbol TEXT UNIQUE, name TEXT UNIQUE, \
                country TEXT,ipo_year INTEGER, sector TEXT, industry TEXT)")

            self.conn.commit()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite ", error)
    # ------------------------------------------------------------------------------------------------------------------
    # Löscht alle Einträge in der Tabelle stock_data
    def delete_stockdata(self):
        """
          Funktion:        delete_stockdata: Löscht alle Einträge in der Tabelle stock_data.

          Rückgabewert:    Kein Rückgabewert
          """
        try:
            self.cur.execute("DELETE FROM stock_data")
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to delete data from sqlite table ", error)

    # ------------------------------------------------------------------------------------------------------------------
    # Fügt die historischen Daten einer Aktie in die Tabelle stock_data ein
    def insert_stockdata(self, data):
        """
        Funktion:        insert_stockdata: Fügt die historischen Daten einer Aktie in die Tabelle stock_data ein.


        Parameter:       data(List of dictonaries):  Dictornary (key: value) mit den historischen Daten der Aktie
                            z.B. [{'Date': '2020-01-01'}, {'Open': 300.0, 'High': 400.0, 'Low': 200.0, 'Close': 350.0,
                            'Volume': 1000, 'symbol': 'AAPL', 'stock_long_name': 'Apple Inc.', 'stock_currency': 'USD',
                            'stock_industry': 'Technology', 'stock_headquarter': 'Cupertino, California'}}]

        Rückgabewert:    Kein Rückgabewert
        """
        try:
            for DataDate, dataValues in data.items():
                self.cur.execute(
                    "INSERT OR IGNORE INTO stock_data VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        str(DataDate), dataValues['Open'], dataValues['High'], dataValues['Low'], dataValues['Close'],
                        dataValues['Volume'], dataValues['symbol'], dataValues['stock_long_name'],
                        dataValues['stock_currency'], dataValues['stock_industry'], dataValues['stock_headquarter']))
                self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table ", error)

    # ------------------------------------------------------------------------------------------------------------------
    # Fügt die Symbole der Aktien in die Tabelle symbols ein
    # - deprecated -
    def insert_symbol_(self, symbol, name, country, ipo_year, sector, industry):
        try:
            self.cur.execute(
                "INSERT OR IGNORE INTO symbols VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                (symbol, name, country, ipo_year, sector, industry))
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table ", error)

    # ------------------------------------------------------------------------------------------------------------------
    # Fügt die Symbole der Aktien in die Tabelle symbols ein
    def insert_symbol(self, data):
        """
        Funktion:        insert_symbol: Fügt die Symbole der Aktien in die Tabelle symbols ein.


        Parameter:       data(List of dictonaries): Dictornary (key: value) mit den Symbolen der Aktien
                            z.B. [{'symbol': 'AAPL', 'name': 'Apple Inc.', 'country': 'United States', 'ipo year': 1980,
                            'sector': 'Technology', 'industry': 'Consumer Electronics'}]

        Rückgabewert:    Kein Rückgabewert
        """
        try:
            for dataValues in data.values():
                self.cur.execute(
                    "INSERT OR IGNORE INTO symbols VALUES (NULL, ?, ?, ?, ?, ?, ?)", (
                        dataValues['symbol'], dataValues['name'], dataValues['country'], dataValues['ipo year'],
                        dataValues['sector'], dataValues['industry']))
                self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table ", error)

    # ------------------------------------------------------------------------------------------------------------------
    def getStockHistoryData(self, symbol, beginDate="1900-01-01", endDate=str(sqlite3.Date.today())):
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
            beginDate = "1900-01-01"  # Beginn der Aktienkurse wird auf 1900-01-01 gesetzt

        if endDate == None:
            endDate = str(sqlite3.Date.today())  # Ende der Aktienkurse wird auf das aktuelle Datum gesetzt

        if type(beginDate) == str and type(endDate) == str:

            # Check date format  YYYY-MM-DD
            #if re.search(r'^\d{4}-\d{2}-\d{2}$', beginDate) and re.search(r'^\d{4}-\d{2}-\d{2}$', endDate):

            try:
                self.cur.execute(
                    "SELECT * FROM stock_data WHERE symbol = ? and  Date >= ? and Date <= ? ORDER BY Date ASC",
                    [symbol, beginDate, endDate])

                rows = self.cur.fetchall()
                retValue = rows

            except sqlite3.Error as error:
                print("Failed to select data from sqlite table ", error)

            #else:  # Date format not correct
                #raise ValueError("Date format not correct, expected YYYY-MM-DD")

        else:  # Date format not correct
            raise TypeError("String expected: beginDate, endDate")

        return retValue
    # ------------------------------------------------------------------------------------------------------------------
    def getStockCloseData(self, symbol):
        rows = []
        try:
            self.cur.execute(
                "SELECT Date, close FROM stock_data WHERE symbol = ? ORDER BY Date ASC", [symbol])
            rows = self.cur.fetchall()
        except sqlite3.Error as error:
            print("Failed to select data from sqlite table ", error)

        return rows
    # ------------------------------------------------------------------------------------------------------------------
    # Sucht nach einem Symbol in der Tabelle symbols, es wird eine Liste mit den gefundenen Symbolen zurückgegeben
    def search_symbol(self, name=""):
        """
        Funktion:        search_symbol: Sucht nach einem Ausdruck in der Tabelle symbols in der Spalte name.
                         Es wird eine Liste mit den gefundenen Symbolen zurückgegeben.

        Parameter:       name(string):              String, der in der Spalte name gesucht wird. z.B. "Apple"

        Rückgabewert:    Liste der gefundenen Symbole. Die Liste ist leer, wenn keine Symbole gefunden wurden.
        """
        rows = []
        try:
            self.cur.execute(
                "SELECT * FROM symbols WHERE name like ?", [str("%" + name + "%")])

            rows = self.cur.fetchall()

        except sqlite3.Error as error:
            print("Failed to select data from sqlite table ", error)
        return rows
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_symbols(self):
        """
        Funktion:        get_all_symbols: Es wird eine Liste mit allen Symbolen zurückgegeben.


        Rückgabewert:    Liste aller in der Tabelle gespeicherten Symbole. Die Liste ist leer, wenn keine Symbole
                         gefunden wurden.
        """
        rows = []
        try:
            self.cur.execute(
                "SELECT * FROM symbols")

            rows = self.cur.fetchall()
        except sqlite3.Error as error:
            print("Failed to select data from sqlite table ", error)

        return rows
    # ------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        try:
            self.conn.close()
        except sqlite3.Error as error:
            print("Failed to close database connection ", error)
