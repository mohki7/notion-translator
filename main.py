import PyPDF2
import requests
import os
from flask import Flask, request

app = Flask(__name__)

# Notion APIの設定
NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

def send_to_notion(text):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "title": {
                "title": [{"text": {"content": "Extracted PDF Text"}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": text}}]
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

@app.route('/upload', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['file']
    extracted_text = extract_text_from_pdf(pdf_file)
    status = send_to_notion(extracted_text)
    return f"Uploaded to Notion with status code {status}"

if __name__ == '__main__':
    app.run(debug=True)
