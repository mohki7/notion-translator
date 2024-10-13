import { Client } from "@notionhq/client";
import axios from 'axios';

const notion = new Client({ auth: process.env.NOTION_API_KEY });

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { notionPageId, url } = req.body;

    // URLからコンテンツを取得
    const response = await axios.get(url);
    const content = response.data;

    // Notionに書き込む
    await notion.pages.update({
      page_id: notionPageId,
      properties: {
        Content: {
          rich_text: [
            {
              text: {
                content: content.substring(0, 2000) // 最初の2000文字を保存
              }
            }
          ]
        }
      }
    });

    res.status(200).json({ message: 'Notion page updated successfully' });
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
