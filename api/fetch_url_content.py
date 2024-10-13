import requests
from notion_client import Client
import os

# Notion APIクライアントの初期化
notion = Client(auth=os.getenv("NOTION_API_KEY"))

def handler(request):
    try:
        # リクエストの内容を取得
        data = request.json
        notion_page_id = data.get("notionPageId")
        url = data.get("url")
        
        # URLからコンテンツを取得
        response = requests.get(url)
        content = response.text
        
        # Notionのページを更新
        notion.pages.update(
            page_id=notion_page_id,
            properties={
                "Content": {
                    "rich_text": [{
                        "text": {
                            "content": content[:2000]  # 最初の2000文字のみ保存
                        }
                    }]
                }
            }
        )
        
        return {
            "statusCode": 200,
            "body": "Notion page updated successfully"
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Internal server error: {str(e)}"
        }
