import logging
import mimetypes

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


class GoogleDriveHelper:
    SCOPES = [
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    VALID_EXTENSIONS = [".pdf", ".png", ".jpeg", ".jpg"]

    def __init__(self, credentail_json):
        self.credentail_json_file = credentail_json
        self.connect_using_service_account()

    def connect_using_service_account(self):
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            self.credentail_json, self.SCOPES
        )
        self.drive_service = build(
            "drive", "v3", credentials=creds, cache_discovery=False
        )

    def get_sharable_link(self, file_id):
        permission = {"role": "reader", "type": "anyone"}
        self.drive_service.permissions().create(
            fileId=file_id, body=permission
        ).execute()

        # Get the sharable link for the file
        file = (
            self.drive_service.files()
            .get(fileId=file_id, fields="webViewLink, webContentLink")
            .execute()
        )

        sharable_link = file.get("webViewLink")  # Link to view the file
        print(f"Sharable link: {sharable_link}")
        return sharable_link

    def upload_file_obj(self, file_obj, filename, parent_folder_id=None):
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = "application/octet-stream"  # Default fallback MIME type
        file_metadata = {
            "name": filename,
            "parents": [parent_folder_id] if parent_folder_id else [],
        }
        print(mime_type)

        # Upload the file object using MediaIoBaseUpload
        media = MediaIoBaseUpload(file_obj, mimetype=mime_type, resumable=True)

        # Upload the file to Google Drive
        drive_file = (
            self.drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        file_id = drive_file.get("id")
        print(f"File uploaded successfully. File ID: {file_id}")
        sharablelink = self.get_sharable_link(file_id)
        return drive_file.get("id"), sharablelink

    def create_folder(self, folder_name, parent_folder_id=None):
        """Create a folder in Google Drive and return its ID."""
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"

        # Add parent folder condition if specified
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        # Searching for existing folders with the specified name
        results = (
            self.drive_service.files()
            .list(q=query, spaces="drive", fields="files(id, name)", pageSize=10)
            .execute()
        )

        items = results.get("files", [])
        if items:
            print(f"Folder '{folder_name}' already exists in Google Drive.")
            return items[0]["id"]

        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_folder_id] if parent_folder_id else [],
        }

        created_folder = (
            self.drive_service.files()
            .create(body=folder_metadata, fields="id")
            .execute()
        )

        print(f'Created Folder ID: {created_folder["id"]}')
        return created_folder["id"]
