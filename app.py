import base64
import json
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from utils.gdrive_helper import GoogleDriveHelper
from utils.notion_service import NotionDatabaseHandler
from utils.reciept_service import ReceiptParser
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

credential_json = json.loads(os.getenv("GOOGLE_OAUTH_SERVICE_ACCOUNT"))
gdrive_service = GoogleDriveHelper(credential_json)

drive_folder_id = gdrive_service.create_folder("test_notion_upload")

receipt_service = ReceiptParser(os.getenv("MINDEE_API_KEY"))

notion_db_id = os.getenv("NOTION_DB_ID")
category_db_id = os.getenv("CATEGORY_DB")
mode_db_id = os.getenv("EXPENSE_MODE_DB")
notion_service = NotionDatabaseHandler(
        api_key=os.getenv("NOTION_KEY"),
        database_id=notion_db_id,
        category_db_id=category_db_id,
        mode_db_id=mode_db_id,
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_bytes = file.read()
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')

        reciept_details = receipt_service.parse_reciept_from_base64(file_base64, filename)

        _, drive_url = gdrive_service.upload_file_obj(
            file, filename, drive_folder_id
        )
        reciept_details["Receipt"] = {"name": filename, "url": drive_url}

        # Create the payload from the user content
        entry_payload = notion_service.create_entry_payload(reciept_details)

        # Insert the entry into the database
        if entry_payload:
            notion_service.insert_entry(entry_payload)
        flash("Image uploaded and processed successfully!", "success")

        # Process the uploaded file here
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)