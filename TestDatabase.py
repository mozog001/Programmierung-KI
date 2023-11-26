import Database as db

# Test Database
db = db.StockDatabase()
db.insert_link("2023-11-25","https://finance.yahoo.com/news/buy-apple-inc-nasdaq-aapl-110103890.html",
               "Apple Inc.")

db.insert_stockdata("2020-10-12 00:00:00-04:00", 0.0, 0.0, 0.0, 0.0, 0, "Apple Inc.",
                    "USD", "Technology", "Cupertino, California")

db.insert_symbol("AAPL", "Apple Inc.", "US", 1980, "Technology",
                 "Consumer Electronics")




