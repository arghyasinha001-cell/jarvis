"""
Utility script to list all Gemini models available for your API key.
Run this once to verify your key works and see which models you can use.

Usage:
    python test_import.py
"""

import google.generativeai as genai

try:
    import config
    genai.configure(api_key=config.GEMINI_API_KEY)
except ImportError:
    print("[ERROR] config.py not found.")
    print("        Copy config.py.example → config.py and add your Gemini API key.")
    raise SystemExit(1)

print("Scanning for available Gemini models...")

try:
    found = 0
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"  FOUND: {m.name}")
            found += 1
    print(f"\nDone. {found} model(s) available.")
except Exception as e:
    print(f"[ERROR]: {e}")
