import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def generate_stock_prices(days, initial_price=100):
    stock_prices = [initial_price]

    for _ in range(1, days):
        # Simuliere eine zufällige prozentuale Änderung des Aktienkurses
        daily_change_percentage = random.uniform(-2, 2)  # Beispiel: Änderung zwischen -2% und 2%
        
        new_price = stock_prices[-1] * (1 + daily_change_percentage / 100)
        stock_prices.append(new_price)

    return stock_prices

def genGraph(ax, canvas):
    test_data = generate_stock_prices(350)
    return test_data

def calculate_sma(ax, canvas, test_data):
    sma_values = []
    window_size = 10
    for i in range(len(test_data) - window_size + 1):
        window = test_data[i : i + window_size]
        sma = sum(window) / window_size
        sma_values.append(sma)
    return sma_values