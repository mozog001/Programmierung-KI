import Database as db

# Test Database
db = db.StockDatabase()


stockHistoryData = db.getStockHistoryData("AMZN", beginDate=None, endDate="2023-12-02")
for row in stockHistoryData:
    print(row, end="\n")
print(len(stockHistoryData))

help(db.getStockHistoryData)
db.conn.close()




