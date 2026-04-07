import google.generativeai as genai
from google.api_core import exceptions

# ── Credentials loaded from config.py ──────────────────────
try:
    import config
    genai.configure(api_key=config.GEMINI_API_KEY)
    _configured = True
except ImportError:
    print("[WARNING] config.py not found. AI responses will be disabled.")
    print("          Copy config.py.example to config.py and fill in your Gemini API key.")
    _configured = False
except Exception as e:
    print(f"[WARNING] Failed to configure Gemini: {e}")
    _configured = False

model = genai.GenerativeModel('models/gemini-2.0-flash') if _configured else None


def ask_ai(query):
    if not _configured or model is None:
        return "AI is not configured. Please add your Gemini API key to config.py."

    try:
        prompt = (
            "You are Jarvis, a helpful and concise AI assistant. "
            "Answer the following query in 2 sentences or less. "
            "Do not use markdown like asterisks or bold text. "
            f"Query: {query}"
        )
        response = model.generate_content(prompt)
        return response.text.replace("*", "")

    except exceptions.ResourceExhausted:
        return "I am overloaded. Please ask again in a minute."

    except Exception as e:
        print(f"[AI ERROR]: {e}")
        return "I am having trouble connecting to the AI server."
