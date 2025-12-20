import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

def generate_data():
    print("Generating expanded dataset...")
    
    num_products = 50
    num_days = 60
    
    # 1. Generate Products (Inventory)
    products = []
    # Sample names to mix and match for variety
    adjectives = ["Pro", "Slim", "Ultra", "Gaming", "Office", "Smart", "Wireless", "Ergo", "Mechanical", "HD"]
    nouns = ["Laptop", "Mouse", "Keyboard", "Headphones", "Monitor", "Webcam", "Speaker", "Tablet", "Phone", "Charger"]
    
    inventory_data = {
        "product_id": [],
        "product_name": [],
        "cost_price": [],
        "selling_price": [],
        "current_stock": [],
        "min_stock_threshold": [],
        "vendor_email": []
    }
    
    # Pre-define some existing ones to keep continuity if desired, but we can just overwrite all P001-P050
    for i in range(1, num_products + 1):
        pid = f"P{i:03d}"
        pname = f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(100, 900)}"
        
        # Random pricing logic
        cost = random.randint(10, 500)
        margin = random.uniform(1.2, 2.0)
        selling = int(cost * margin)
        
        stock = random.randint(0, 200)
        threshold = random.randint(5, 30)

        # Force some scenarios
        if i % 10 == 0:
            # Overstock (High Stock > 100, we will force low sales later)
            stock = random.randint(120, 300)
            pname = f"Old Gen {pname}" # Mark it visually
        elif i % 10 == 1:
            # Low Stock (Stock < 10)
            stock = random.randint(0, 5)
        
        # Fake email
        v_email = f"vendor.{random.choice(['abc', 'xyz', 'global', 'tech', 'supply'])}.{random.randint(1,99)}@example.com"
        
        inventory_data["product_id"].append(pid)
        inventory_data["product_name"].append(pname)
        inventory_data["cost_price"].append(cost)
        inventory_data["selling_price"].append(selling)
        inventory_data["current_stock"].append(stock)
        inventory_data["min_stock_threshold"].append(threshold)
        inventory_data["vendor_email"].append(v_email)
        
    df_inventory = pd.DataFrame(inventory_data)
    df_inventory.to_csv("inventory.csv", index=False)
    print(f"✅ Generated inventory.csv with {len(df_inventory)} rows.")

    # 2. Generate Competitors
    competitor_data = {
        "product_id": [],
        "competitor_price": [],
        "competitor_promo": []
    }
    
    for i in range(len(inventory_data["product_id"])):
        pid = inventory_data["product_id"][i]
        our_price = inventory_data["selling_price"][i]
        
        # Competitor price variation (+- 15%)
        variation = random.uniform(0.85, 1.15)
        comp_price = int(our_price * variation)
        promo = random.choice([True, False])
        
        competitor_data["product_id"].append(pid)
        competitor_data["competitor_price"].append(comp_price)
        competitor_data["competitor_promo"].append(promo)
        
    df_competitors = pd.DataFrame(competitor_data)
    df_competitors.to_csv("competitors.csv", index=False)
    print(f"✅ Generated competitors.csv with {len(df_competitors)} rows.")
    
    # 3. Generate Sales History
    # Columns: date, P001_sales, P002_sales, ...
    
    dates = [datetime.today() - timedelta(days=x) for x in range(num_days)]
    dates.sort() # Oldest to newest
    date_strings = [d.strftime("%Y-%m-%d") for d in dates]
    
    sales_data = {"date": date_strings}
    
    for pid in inventory_data["product_id"]:
        # Generate random daily sales patterns
        
        # Check if we forced this product to be Overstock (ID ends in 0 for our logic above?)
        # Let's map back from the PID string "P010", "P020" etc.
        idx = int(pid[1:]) # P001 -> 1
        
        avg_daily = random.randint(0, 15)
        
        if idx % 10 == 0:
            # Force LOW sales for Overstock candidates (Avg < 1)
            avg_daily = 0.5 
            
        pattern = np.random.poisson(avg_daily, num_days)
        sales_data[f"{pid}_sales"] = pattern
        
    df_sales = pd.DataFrame(sales_data)
    # Sort by date descending as per original file style (usually newest first is better for view, but original was newest first? Let's check original...
    # Original sales_history.csv had 2025-12-20 at top. So descending.)
    df_sales = df_sales.sort_values(by="date", ascending=False)
    
    df_sales.to_csv("sales_history.csv", index=False)
    print(f"✅ Generated sales_history.csv with {len(df_sales)} rows and {len(df_sales.columns)} columns.")

if __name__ == "__main__":
    generate_data()
