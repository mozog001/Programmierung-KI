import display_data

test_data = display_data.get_stocks_list("AAPL", "2020-01-01", "2020-03-01")

def calculate_sma(stock_data, window_size):
    sma_values = []
    for i in range(len(stock_data) - window_size + 1):
        window = stock_data[i:i + window_size]        
        # Liste mit Daten generieren
        timestamp = window[-1][0]        
        # Liste mit Preisen generieren
        prices = [item[1] for item in window]        
        sma = sum(prices) / len(prices)        
        sma_values.append((timestamp, sma))    
    return sma_values