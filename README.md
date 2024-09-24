 # Bill Tracker Application - Open Source Project

 Welcome to the **Bill Tracker Application**! This open-source project is designed to help individuals and organizations track, manage, and organize their bills for both personal and corporate use, with a specific focus on **tax and expense management**. The application allows users to upload bill images, which are processed by an AI/ML model to extract important details such as supplier name, invoice number, date, tax, net amount, and category. The extracted details are then stored in a Notion database, and the bill images are saved to Google Drive for easy access.

 ## Key Features

 - **Bill Image Upload**: Users can upload images of their bills through a simple and secure Flask web interface.
 - **AI/ML Bill Parsing**: A custom AI/ML model is used to extract essential bill details such as supplier name, invoice number, date, tax, net amount, and category.
 - **Google Drive Integration**: Uploaded bill images are automatically saved in Google Drive for backup and easy retrieval.
 - **Notion Integration**: The parsed bill details are stored in a Notion database, allowing users to track and manage their bills efficiently.
 - **Secure and Cost-Free**: Built with security and privacy in mind, using open-source tools and APIs to avoid costly third-party services.

 ## Technology Stack

 - **Flask**: A lightweight and flexible Python web framework for building the web application.
 - **Custom AI/ML Model**: A machine learning model for parsing bill images and extracting information.
 - **Google Drive API**: For uploading and managing bill images in Google Drive.
 - **Notion API**: For creating and updating entries in a Notion database with the extracted bill details.
 - **Mindee API** (optional): To enhance OCR capabilities for complex bill structures.

 ## Prerequisites

 To run this project, ensure you have the following tools installed:

 - **Python 3.x**
 - **Flask**
 - **Google Drive API credentials** (OAuth 2.0)
 - **Notion API credentials** (API token and database ID)
 - **An AI/ML model** trained to recognize and extract bill details
 - **Optional: Mindee API** for additional OCR support

 ## Installation and Setup

 1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-repo/bill-tracker-app.git
    cd bill-tracker-app
    ```

 2. **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

 3. **Install required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

 4. **Set up Google Drive API credentials:**

    - Follow the [Google Drive API setup guide](https://developers.google.com/drive/api/v3/quickstart/python) to create your OAuth 2.0 credentials.
    - Download the `credentials.json` file and place it in the project directory.

 5. **Set up Notion API credentials:**

    - Sign up for the [Notion API](https://www.notion.so/my-integrations) and create a new integration.
    - Copy your **Notion API token** and **database ID** and set them as environment variables in your project.

    ```bash
    export NOTION_TOKEN='your_notion_api_token'
    export NOTION_DATABASE_ID='your_notion_database_id'
    ```

 6. **Add your trained AI/ML model:**

    - Ensure that your trained model is placed in the project and accessible via the `extract_bill_details` function.
    - Modify the path to the model and adjust the prediction logic if necessary.

 7. **Run the Flask application:**

    ```bash
    flask run
    ```

 8. **Upload bills** via the web interface at `http://localhost:5000`.

 ## Code Snippets

 Here’s a brief overview of how key components work:

 ### File Upload in Flask

 ```python
 @app.route('/upload', methods=['POST'])
 def upload_file():
     if 'file' not in request.files:
         return redirect(request.url)
     file = request.files['file']
     if file.filename == '':
         return redirect(request.url)
     if file:
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         # Process the uploaded file here
         return redirect(url_for('index'))
 ```

 ### AI/ML Model Integration

 ```python
 def extract_bill_details(image_path):
     # Process the image through your ML model
     result = model.predict(image_path)
     details = {
         'supplier_name': result['supplier_name'],
         'invoice_number': result['invoice_number'],
         'date': result['date'],
         'tax': result['tax'],
         'net_amount': result['net_amount'],
         'category': result['category']
     }
     return details
 ```

 ### Google Drive Upload

 ```python
 def upload_to_drive(file_path):
     file = drive.CreateFile({'title': os.path.basename(file_path)})
     file.SetContentFile(file_path)
     file.Upload()
     print(f'Uploaded {file_path} to Google Drive')
 ```

 ### Notion API Integration

 ```python
 def create_notion_entry(details):
     headers = {
         "Authorization": f"Bearer {NOTION_TOKEN}",
         "Content-Type": "application/json",
         "Notion-Version": "2021-05-13"
     }
     data = {
         "parent": {"database_id": NOTION_DATABASE_ID},
         "properties": {
             "Supplier Name": {"title": [{"text": {"content": details['supplier_name']}}]},
             "Invoice Number": {"rich_text": [{"text": {"content": details['invoice_number']}}]},
             "Date": {"date": {"start": details['date']}},
             "Tax": {"number": details['tax']},
             "Net Amount": {"number": details['net_amount']},
             "Category": {"select": {"name": details['category']}}
         }
     }
     response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
     if response.status_code == 200:
         print('Notion entry created successfully')
     else:
         print(f'Failed to create Notion entry: {response.content}')
 ```

 ## Benefits of the Project

 - **Automated Expense Management**: Automatically categorize, store, and track bills.
 - **Tax Preparation**: Easily retrieve and organize bills for tax purposes.
 - **Cost-Free**: Avoid the expense of third-party solutions by building and customizing this app using free open-source tools.
 - **Cloud Storage**: Store bill images in Google Drive for easy access and backup.
 - **Centralized Database**: Use Notion as a powerful and flexible database for tracking all your financial data.

 ## Contributing

 Feel free to fork this repository and make improvements! If you encounter any issues or have suggestions for new features, please open an issue or submit a pull request. Your contributions are welcome.


