import Database as db

# Test Database
db = db.StockDatabase()


stockHistoryData = db.getStockHistoryData("AMZN","2021-01-31")
for row in stockHistoryData:
    print(row, end="\n")
print(len(stockHistoryData))

help(db.getStockHistoryData)
db.conn.close()




