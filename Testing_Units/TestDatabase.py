from Low_Level.Database import Database as db

# Test Database
db = db.StockDatabase()

#db.delete_stockdata()



stockHistoryData = db.getStockHistoryData("AMZN","2016-12-01", "2016-12-06")
for row in stockHistoryData:
    print(row, end="\n")
print(len(stockHistoryData))

#help(db.getStockHistoryData)
db.conn.close()




