from marketing_agent import MarketingAgent
import pandas as pd

def test_agent():
    print("Testing MarketingAgent with expanded data...")
    agent = MarketingAgent()
    
    # helper to check if product exists in agent's memory
    df_inv = agent.inventory.df_inv
    print(f"Agent loaded inventory with {len(df_inv)} rows.")
    
    # Try to analyze the last product
    last_id = df_inv.iloc[-1]['product_id']
    print(f"Attempting to analyze product: {last_id}")
    
    try:
        result = agent.inventory.analyze_product(last_id)
        print("✅ Success! Result:", result)
    except IndexError:
        print("❌ Failed: IndexError (Stale Data?)")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_agent()
