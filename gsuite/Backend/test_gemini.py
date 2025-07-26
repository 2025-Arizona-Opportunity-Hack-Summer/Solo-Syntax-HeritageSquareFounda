import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your .env file
load_dotenv()

# Fetch the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

print(f"🔑 Loaded API Key (partial): {api_key[:10]}..." if api_key else "❌ API Key not found!")

# Check if the key is present
if not api_key:
    exit("❌ GEMINI_API_KEY is missing from your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

# Attempt to call Gemini
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say hello in one sentence.")
    print("Gemini is working!")
    print("Response:", response.text.strip())

except Exception as e:
    print("Gemini API Error:")
    print(e)
