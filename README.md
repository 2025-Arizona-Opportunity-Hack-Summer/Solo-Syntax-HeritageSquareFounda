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
Rename files using:
```

rename \<old\_name> to \<new\_name>

```

### 📁 Move Files
```

move \<file\_name> to \<folder\_name>

````

### 🏷️ Tag Files
Auto-tagging based on file content.

### 🧠 Categorize Files
Categorization using AI-powered prompts.

### 📝 Summarize Files
Summarize long text files instantly.

### 📃 List Files
List available files in the connected Google Drive.

### 📤 Upload Files
Upload local files directly to Google Drive using the UI.

---

## 📌 Use Cases

Here’s how different teams can benefit from the AI assistant:

- **Nonprofits**: Quickly organize donation forms, event flyers, grant applications, and compliance documents.
- **Marketing Teams**: Categorize, tag, and move content assets into the right campaigns without technical steps.
- **Academic Institutions**: Help faculty or admin staff manage departmental files or categorize research data.
- **Small Businesses**: Upload invoices, summarize financial reports, and retrieve contracts on demand.
- **Event Planning**: Upload, rename, and tag itineraries, checklists, and brochures efficiently.

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

Project Lead: [Bhavagna Shreya Bandaru](mailto:bbandar5@asu.edu)

---

## 📜 License

MIT License – see `LICENSE.md` for usage details.

```

