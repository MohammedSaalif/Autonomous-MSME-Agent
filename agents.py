import pandas as pd
import datetime
import hashlib
import csv
import os

# --- 1. FINANCE AGENT ---
class FinanceAgent:
    def __init__(self):
        self.df = pd.read_csv("financials.csv")
    
    def get_status(self):
        # Read Data
        cash = self.df[self.df['metric'] == 'cash_balance']['value'].values[0]
        burn = self.df[self.df['metric'] == 'monthly_burn_rate']['value'].values[0]
        
        # Calculate Logic
        runway_months = round(cash / burn, 1)
        
        status = "HEALTHY"
        if runway_months < 3:
            status = "CRITICAL"
        
        return {
            "cash": cash,
            "burn_rate": burn,
            "runway_months": runway_months,
            "status": status,
            "message": f"Cash Runway: {runway_months} months. Status: {status}"
        }

# --- 2. INVENTORY AGENT ---
class InventoryAgent:
    def __init__(self):
        self.df_inv = pd.read_csv("inventory.csv")
        self.df_sales = pd.read_csv("sales_history.csv")
    
    def analyze_product(self, product_id):
        # Get Product Data
        prod = self.df_inv[self.df_inv['product_id'] == product_id].iloc[0]
        name = prod['product_name']
        stock = prod['current_stock']
        
        # Calculate recent sales velocity (last 7 days)
        sales_col = f"{product_id}_sales"
        total_sales_7d = self.df_sales[sales_col].head(7).sum()
        
        # Logic: Overstock vs Low Stock
        status = "NORMAL"
        if stock > 100 and total_sales_7d < 10:
            status = "OVERSTOCK (Dead Inventory)"
        elif stock < 10:
            status = "LOW STOCK (Scarcity)"
        elif total_sales_7d > 30:
            status = "HIGH DEMAND"

        return {
            "product": name,
            "stock": stock,
            "7d_sales": total_sales_7d,
            "status": status
        }

# --- 3. COMPETITOR AGENT ---
class CompetitorAgent:
    def __init__(self):
        self.df_comp = pd.read_csv("competitors.csv")
        self.df_inv = pd.read_csv("inventory.csv")
        
    def compare_price(self, product_id):
        # Get our price vs theirs
        my_price = self.df_inv[self.df_inv['product_id'] == product_id]['selling_price'].values[0]
        comp_row = self.df_comp[self.df_comp['product_id'] == product_id].iloc[0]
        comp_price = comp_row['competitor_price']
        
        diff = my_price - comp_price
        
        position = "Competitive"
        if diff > 0:
            position = f"Overpriced by ${diff} (We are losing)"
        elif diff < 0:
            position = f"Underpriced by ${abs(diff)} (We are winning)"
            
        return {
            "my_price": my_price,
            "competitor_price": comp_price,
            "position": position
        }

# --- 4. AUDIT & COMPLIANCE AGENT ---
class AuditAgent:
    def __init__(self, log_file="audit_log.csv"):
        self.log_file = log_file
        # Ensure file exists with headers
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "agent_name", "product_id", "action_taken", "reasoning_hash", "status"])

    def log_event(self, agent_name, product_id, action, reasoning):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a hash of the reasoning for integrity (simulated blockchain-lite)
        reasoning_hash = hashlib.sha256(reasoning.encode()).hexdigest()[:16]
        
        status = "VERIFIED"
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, agent_name, product_id, action, reasoning_hash, status])
            
        return reasoning_hash

    def get_recent_logs(self):
        try:
            return pd.read_csv(self.log_file).tail(10).iloc[::-1] # Last 10, reversed
        except:
            return pd.DataFrame()