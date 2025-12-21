import google.generativeai as genai
import os
from agents import FinanceAgent, InventoryAgent, CompetitorAgent, AuditAgent

# ⚠️ PASTE YOUR KEY HERE
API_KEY = "#" 
genai.configure(api_key=API_KEY)

class MarketingAgent:
    def __init__(self):
        self.finance = FinanceAgent()
        self.inventory = InventoryAgent()
        self.competitor = CompetitorAgent()
        self.audit = AuditAgent()
        # ✅ Using the model you confirmed works
        self.model = genai.GenerativeModel('gemini-2.5-flash') 

    def generate_strategy(self, product_id, crisis_mode=False):
        # 1. GATHER INTELLIGENCE
        fin_status = self.finance.get_status()
        inv_status = self.inventory.analyze_product(product_id)
        comp_status = self.competitor.compare_price(product_id)

        # 🚨 CRISIS SIMULATION LOGIC 🚨
        if crisis_mode:
            fin_status['message'] = "CRITICAL: Cash runway is < 2 weeks. BANKRUPTCY IMMINENT."
            fin_status['status'] = "EMERGENCY"
            # Force the prompt to realize we are dying

        # 2. CONSTRUCT THE PROMPT
        prompt = f"""
        You are an Autonomous Marketing Agent. Make a strategic decision based on the data below.
        
        --- BUSINESS CONTEXT ---
        💰 CASH STATUS: {fin_status['message']}
        📦 INVENTORY: {inv_status['status']} (Stock: {inv_status['stock']}, 7-Day Sales: {inv_status['7d_sales']}).
        🕵️ COMPETITOR: {comp_status['position']} (My Price: {comp_status['my_price']}, Theirs: {comp_status['competitor_price']}).
        
        --- PRODUCT ---
        Product Name: {inv_status['product']}
        
        --- MISSION ---
        Decide the immediate marketing action.
        
        CRITICAL INSTRUCTION: 
        If CASH STATUS is CRITICAL/EMERGENCY, you MUST choose "LIQUIDATION" or "HOLD". Do not spend money on Ads.
        If INVENTORY is OVERSTOCK, you MUST clear it.
        
        OUTPUT FORMAT:
        **DECISION:** [Aggressive Push / Liquidation / Hold / Price Match]
        **REASONING:** [Short explanation]
        **ACTION:** [Specific tactic]
        """

        # 3. GET AI DECISION
        try:
            response = self.model.generate_content(prompt)
            decision_text = response.text
            
            # 4. 📜 AUDIT LOGGING
            self.audit.log_event(
                agent_name="MarketingAgent",
                product_id=product_id,
                action="Strategy Generation",
                reasoning=decision_text
            )
            
            return decision_text
        except Exception as e:
            return f"Error connecting to AI: {e}"

if __name__ == "__main__":
    agent = MarketingAgent()
    print("Normal Mode:", agent.generate_strategy("P001", crisis_mode=False))
    print("\n🚨 Crisis Mode:", agent.generate_strategy("P001", crisis_mode=True))