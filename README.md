
# Heritage Square File Assistant 🗂️🤖

A smart document assistant that integrates AI with Google Drive, enabling natural language control over your cloud files. Designed for non-technical users and teams to interact with Drive using a simple, intuitive chatbot UI powered by **FastAPI**, **React**, **Google Drive API**, and **Gemini 1.5**.

---

## 🌟 Key Features

### ✅ Natural Language Commands
Interact with your files using plain English commands such as:
- `read Grants Document`
- `rename Annual Report to 2024 Budget`
- `move Brochure to Marketing Folder`
- `tag Volunteer Roster`
- `summarize Proposal Final`
- `categorize Tax Records`

### 📚 Read File Contents
Supports reading and displaying:
- `.txt`, `.json`, `.csv`

### ✏️ Rename Files  
### 📁 Move Files  
### 🏷️ Tag Files  
### 🧠 Categorize Files  
### 📝 Summarize Files  
### 📃 List Files  
### 📤 Upload Files  

---

## 📌 Use Cases

Here’s how different teams can benefit from the AI assistant:

- **Nonprofits**: Organize donation forms, event flyers, grant applications, and compliance docs.
- **Marketing**: Categorize and manage campaign assets.
- **Academia**: Sort and retrieve research or departmental files.
- **Small Business**: Upload, rename, and read invoices or contracts.
- **Event Planners**: Tag and manage itineraries and logistics documents.

---

## 📂 Project Structure

```

heritage-file-assistant/
│
├── frontend/                       # React-based chatbot UI
│   ├── public/
│   ├── src/
│   │   ├── App.js                 # Main UI logic and message handling
│   │   └── ...
│   └── package.json
│
├── backend/
│   └── gsuite/
│       ├── Backend/
│       │   ├── chat\_api.py       # FastAPI app with Gemini and Google Drive logic
│       │   └── agent.py          # Utility functions to access Drive (read, move, tag, etc.)
│       └── credentials/
│           └── .gdrive-server-credentials.json  # Google service account JSON
│
├── .env                           # Contains GEMINI\_API\_KEY
├── requirements.txt               # Python dependencies
├── README.md

````

---

## ⚙️ Tech Stack

| Layer        | Technology                      |
|--------------|----------------------------------|
| Frontend     | React.js, CSS                   |
| Backend      | FastAPI, Python, Pydantic       |
| AI Model     | Gemini 1.5 Flash (Google AI)    |
| File System  | Google Drive API (v3)           |
| Auth         | Google Service Account OAuth2   |

---

## 🏁 Getting Started

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
````

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Place your service account credentials at:

```
gsuite/credentials/.gdrive-server-credentials.json
```

Run the backend:

```bash
uvicorn gsuite.Backend.chat_api:app --reload
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## 📬 Contact

Project Lead: [Bhavagna Shreya Bandaru]

---

## 📜 License

MIT License – see `LICENSE.md` for usage details.

```

