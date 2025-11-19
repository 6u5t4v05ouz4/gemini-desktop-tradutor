import google.generativeai as genai
import config_manager
import os

api_key = config_manager.get_api_key()
if not api_key:
    print("No API Key found in config.")
else:
    genai.configure(api_key=api_key)
    try:
        print("Listing available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error: {e}")
