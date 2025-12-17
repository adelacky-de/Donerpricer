import sys
from PySide6.QtWidgets import QApplication
from main import MainWindow
import ml_model
import pandas as pd

# Mock database.get_prices to return some data
import database
def mock_get_prices_by_item_and_brand(item_name, brand_name=None):
    # Return a dummy DataFrame
    data = {
        "date": ["2023-10-27", "2023-10-28", "2023-10-29"],
        "price": [5.00, 5.50, 5.20],
        "brand_name": ["BrandA", "BrandA", "BrandA"],
        "supermarket": ["SuperA", "SuperA", "SuperA"], # Added supermarket
        "location": ["LocA", "LocA", "LocA"],
        "weight_grams": [200, 200, 200],
        "price_volatility": [0.1, 0.1, 0.1] # Added volatility column
    }
    return pd.DataFrame(data)

database.get_prices_by_item_and_brand = mock_get_prices_by_item_and_brand

app = QApplication(sys.argv)
window = MainWindow()

# Simulate search
print("Simulating search for 'Döner'...")
window.search_input.setCurrentText("Döner")
window.search_item()

# Check labels
print(f"Best Day Label: {window.best_day_val.text()}")
print(f"Price Label: {window.price_val.text()}")
print(f"Confidence Label: {window.confidence_val.text()}")

sys.exit(0)
