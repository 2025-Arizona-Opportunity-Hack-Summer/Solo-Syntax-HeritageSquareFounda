import os
import io
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pdfminer.high_level import extract_text_to_fp

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYFILE_PATH = os.path.join(BASE_DIR, "credentials", "gcp-oauth.keys.json")
GDRIVE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials", ".gdrive-server-credentials.json")
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

def authenticate_drive():
    if os.path.exists(GDRIVE_CREDENTIALS_PATH):
        return
    flow = InstalledAppFlow.from_client_secrets_file(KEYFILE_PATH, DRIVE_SCOPES)
    creds = flow.run_local_server(port=0)
    os.makedirs(os.path.dirname(GDRIVE_CREDENTIALS_PATH), exist_ok=True)
    with open(GDRIVE_CREDENTIALS_PATH, "w") as f:
        f.write(creds.to_json())
    print("Authenticated and saved credentials.")

def get_drive_client():
    authenticate_drive()
    creds = Credentials.from_authorized_user_file(GDRIVE_CREDENTIALS_PATH, DRIVE_SCOPES)
    return build("drive", "v3", credentials=creds)

def find_file_by_name(name, is_folder=False):
    drive = get_drive_client()
    mime_filter = " and mimeType = 'application/vnd.google-apps.folder'" if is_folder else ""
    query = f"name contains '{name}' and trashed = false{mime_filter}"
    try:
        results = drive.files().list(
            q=query,
            pageSize=1,
            fields="files(id, name, mimeType)",
            corpora="user",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True
        ).execute()
        files = results.get("files", [])
        return files[0] if files else None
    except Exception:
        return None

def read_file(file_id):
    drive = get_drive_client()
    try:
        file = drive.files().get(fileId=file_id, fields="mimeType, name").execute()
        mime_type = file["mimeType"]

        export_mime_types = {
            "application/vnd.google-apps.document": "text/plain",
            "application/vnd.google-apps.spreadsheet": "text/csv",
            "application/vnd.google-apps.presentation": "text/plain"
        }

        # Prepare request
        if mime_type in export_mime_types:
            request = drive.files().export_media(fileId=file_id, mimeType=export_mime_types[mime_type])
        elif mime_type.startswith("application/vnd.google-apps.folder"):
            return "This is a folder. Cannot read directly."
        else:
            request = drive.files().get_media(fileId=file_id)

        # Download content
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.seek(0)

        if mime_type == "application/pdf":
            output = io.StringIO()
            extract_text_to_fp(fh, output)
            return output.getvalue()

        return fh.read().decode("utf-8", errors="ignore")

    except Exception as e:
        return f"Error reading file: {e}"

def rename_file(file_id, new_name):
    drive = get_drive_client()
    try:
        updated = drive.files().update(fileId=file_id, body={"name": new_name}).execute()
        return f"File renamed to: {updated['name']}"
    except Exception as e:
        return f"Rename failed: {e}"

def move_file(file_id, folder_id):
    drive = get_drive_client()
    try:
        file = drive.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents', []))
        drive.files().update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        return "File moved to folder."
    except Exception as e:
        return f"Move failed: {e}"

def list_files():
    drive = get_drive_client()
    try:
        results = drive.files().list(
            q="trashed = false",
            pageSize=50,
            fields="files(id, name, mimeType)",
            corpora="user",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True
        ).execute()
        return results.get("files", [])
    except Exception as e:
        return f"Error listing files: {e}"

def categorize_file(content):
    if "grant" in content.lower():
        return "Grants"
    elif "marketing" in content.lower() or "social media" in content.lower():
        return "Marketing"
    elif "budget" in content.lower() or "logistics" in content.lower():
        return "Operations"
    elif "human resource" in content.lower() or "recruitment" in content.lower():
        return "HR"
    else:
        return "Uncategorized"

def extract_tags(content):
    words = content.lower().split()
    keywords = [w.strip(".,!?()[]{}<>:;\"'") for w in words if len(w) > 5 and words.count(w) == 1]
    return list(set(keywords[:5]))
