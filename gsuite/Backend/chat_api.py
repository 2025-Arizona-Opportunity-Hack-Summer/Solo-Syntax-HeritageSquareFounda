from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
import traceback

from gsuite.Backend.agent import (
    find_file_by_name,
    read_file,
    rename_file,
    move_file,
    categorize_file,
    extract_tags,
    list_files
)

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Heritage Square File Assistant API is running."}

@app.post("/chat")
def chat_handler(message: Message):
    user_input = message.text.strip().lower()

    try:
        if user_input.startswith("read "):
            name = user_input[5:].strip()
            file = find_file_by_name(name)
            if not file:
                return {"response": f"File '{name}' not found."}
            mime = file.get("mimeType", "")
            if mime in ["text/plain", "application/json", "text/csv"]:
                return {"response": read_file(file["id"])}
            return {"response": f"Cannot display file '{name}' (type: {mime}) as plain text."}

        elif user_input.startswith("rename "):
            parts = user_input[7:].split(" to ")
            if len(parts) != 2:
                return {"response": "Usage: rename <old_name> to <new_name>"}
            old_name, new_name = parts[0].strip(), parts[1].strip()
            file = find_file_by_name(old_name)
            if not file:
                return {"response": f"File '{old_name}' not found."}
            return {"response": rename_file(file['id'], new_name)}

        elif user_input.startswith("move "):
            parts = user_input[5:].split(" to ")
            if len(parts) != 2:
                return {"response": "Usage: move <file_name> to <folder_name>"}
            file_name, folder_name = parts[0].strip(), parts[1].strip()
            file = find_file_by_name(file_name)
            folder = find_file_by_name(folder_name, is_folder=True)
            if not file:
                return {"response": f"File '{file_name}' not found."}
            if not folder:
                return {"response": f"Folder '{folder_name}' not found."}
            return {"response": move_file(file['id'], folder['id'])}

        elif user_input.startswith("categorize "):
            name = user_input[11:].strip()
            file = find_file_by_name(name)
            if not file:
                return {"response": f"File '{name}' not found."}
            content = read_file(file['id'])
            category = categorize_file(content)
            return {"response": f"Suggested category: {category}"}

        elif user_input.startswith("tag "):
            name = user_input[4:].strip()
            file = find_file_by_name(name)
            if not file:
                return {"response": f"File '{name}' not found."}
            content = read_file(file['id'])
            tags = extract_tags(content)
            return {"response": f"Tags: {', '.join(tags)}"}

        elif user_input.startswith("summarize "):
            name = user_input[10:].strip()
            file = find_file_by_name(name)
            if not file:
                return {"response": f"File '{name}' not found."}
            content = read_file(file['id'])
            return {"response": interpret_with_gemini(f"Summarize this:\n{content}")}

        elif user_input in ["list", "list files", "show my files"]:
            files = list_files()
            if isinstance(files, str):
                return {"response": files}
            file_names = [f"{f['name']}" for f in files]
            return {"response": "\n".join(file_names)}

        else:
            return {"response": interpret_with_gemini(user_input)}

    except Exception as e:
        return {"response": f"Internal server error: {str(e)}"}

def interpret_with_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(f"You are an AI file assistant. {prompt}")
        return response.text.strip()
    except Exception as e:
        traceback.print_exc()
        return f"Gemini error: {str(e)}"
