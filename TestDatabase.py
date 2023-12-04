import Database as db

# Test Database
db = db.StockDatabase()

# Lese Symbol.csv ein und füge die Symbole in die Datenbank ein
fhandle = open("symbols.csv")
for line in fhandle:
    line = line.rstrip()
    if line.startswith("Symbol"):
        continue
    symbol, name, country, ipo_year, sector, industry = line.split(";")
    db.insert_symbol(symbol, name, country, ipo_year, sector, industry)

symbollist = db.search_symbol("Apple")
print(symbollist)
db.conn.close()




