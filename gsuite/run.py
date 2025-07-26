# gsuite/run.py
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from gsuite.Backend import chat_api
import uvicorn

if __name__ == "__main__":
    print("🤖 Starting Heritage Square Chatbot...")
    uvicorn.run(chat_api.app, host="127.0.0.1", port=8000)
