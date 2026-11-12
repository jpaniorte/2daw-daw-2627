from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from common import HOME_DIR

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
TOKEN = HOME_DIR / "drive_token.json"


def _service(client_secret):
    creds = Credentials.from_authorized_user_file(TOKEN, SCOPES) if TOKEN.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES).run_local_server(port=0)
        HOME_DIR.mkdir(exist_ok=True)
        TOKEN.write_text(creds.to_json())
    return build("drive", "v3", credentials=creds)


def upload_mp3(mp3_path, folder_id, client_secret):
    """Sube el mp3, lo comparte con enlace (lector) y devuelve el file_id."""
    svc = _service(client_secret)
    media = MediaFileUpload(mp3_path, mimetype="audio/mpeg", resumable=True)
    meta = {"name": Path(mp3_path).name, "parents": [folder_id]}
    file_id = svc.files().create(body=meta, media_body=media, fields="id").execute()["id"]
    svc.permissions().create(fileId=file_id, body={"type": "anyone", "role": "reader"}).execute()
    return file_id
