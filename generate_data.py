import pandas as pd
from datetime import datetime, timedelta
import random

def generate_data():
    # --- 1. INVENTORY (The "Stock Reality") ---
    inventory_data = {
        "product_id": ["P001", "P002", "P003", "P004"],
        "product_name": ["High-End Laptop", "Basic Mouse", "Noise-Cancel Headphones", "Mech Keyboard"],
        "cost_price": [800, 5, 50, 40],
        "selling_price": [1200, 15, 110, 80],
        "current_stock": [5, 600, 45, 120],  # Laptop: SCARCE. Mouse: DEAD STOCK.
        "min_stock_threshold": [10, 50, 20, 30]
    }
    pd.DataFrame(inventory_data).to_csv("inventory.csv", index=False)
    print("✅ inventory.csv created (Laptop=Scarce, Mouse=Overstock)")

    # --- 2. FINANCIALS (The "Cash Limits") ---
    financial_data = {
        "metric": ["cash_balance", "monthly_burn_rate", "fixed_costs"],
        "value": [12000, 5000, 3000] # Low cash runway (~2.5 months)
    }
    pd.DataFrame(financial_data).to_csv("financials.csv", index=False)
    print("✅ financials.csv created (Cash is TIGHT)")

    # --- 3. COMPETITORS (The "Market Pressure") ---
    competitor_data = {
        "product_id": ["P001", "P002", "P003", "P004"],
        "competitor_price": [1150, 10, 120, 75], # Competitor undercutting Laptop & Mouse
        "competitor_promo": [True, True, False, False]
    }
    pd.DataFrame(competitor_data).to_csv("competitors.csv", index=False)
    print("✅ competitors.csv created")

    # --- 4. SALES TRENDS (The "Context") ---
    # Generating 7 days of sales
    sales_data = {
        "date": [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(7)],
        "P001_sales": [1, 0, 1, 0, 0, 1, 0], # Laptop: Slow
        "P002_sales": [2, 1, 2, 1, 1, 2, 1], # Mouse: VERY Slow (Dead stock risk)
        "P003_sales": [5, 8, 6, 7, 9, 8, 7], # Headphones: HOT SELLER
        "P004_sales": [3, 2, 3, 4, 3, 2, 3]
    }
    pd.DataFrame(sales_data).to_csv("sales_history.csv", index=False)
    print("✅ sales_history.csv created")

if __name__ == "__main__":
    generate_data()