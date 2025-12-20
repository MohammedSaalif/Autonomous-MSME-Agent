import google.generativeai as genai
import os

# ⚠️ PASTE YOUR KEY HERE
API_KEY = "AIzaSyB5PHCdyqMCzx7VjdcQ9kcRTouxq_wfb64" 
genai.configure(api_key=API_KEY)

print("🔍 Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")