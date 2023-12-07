import random
import display_data

stock_data = display_data.get_stocks_list("AAPL", "2020-01-01", "2020-01-10")

def calculate_sma(stock_data):
    sma_values = []
    window_size = 3
    for i in range(len(stock_data) - window_size + 1):
        window = stock_data[i : i + window_size]
        sma = sum(window) / window_size
        sma_values.append(sma)
    return sma_values