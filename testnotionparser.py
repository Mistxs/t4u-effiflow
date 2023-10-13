from flask import Flask, render_template
import requests
import html


app = Flask(__name__)

NOTION_TOKEN = ''
NOTION_PAGE_ID = ''

@app.route('/')
def notion_integration():
    headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-05-13'
    }

    response = requests.get(f'https://api.notion.com/v1/blocks/{NOTION_PAGE_ID}/children', headers=headers)
    data = response.json()

    blocks = []
    for block in data['results']:
        block_type = block.get('type', None)
        if block_type:
            if block_type == 'paragraph':
                content = parse_paragraph(block[block_type]['text'])
                blocks.append({'type': 'paragraph', 'content': content})
            elif block_type.startswith('heading'):
                text_list = block[block_type]['text']
                content = '\n'.join([text.get('plain_text', '') for text in text_list])
                if content:
                    blocks.append({'type': block_type, 'content': content})
            elif block_type == 'to_do':
                text_list = block[block_type]['text']
                content = '\n'.join([text.get('plain_text', '') for text in text_list])
                checked = block[block_type].get('checked', False)
                if content:
                    blocks.append({'type': 'to_do', 'content': content, 'checked': checked})
            elif block_type in ['bulleted_list_item', 'numbered_list_item']:
                text_list = block[block_type]['text']
                content = '\n'.join([text.get('plain_text', '') for text in text_list])
                if content:
                    blocks.append({'type': block_type, 'content': content})
            elif block_type == 'image':
                source = block.get('image', {}).get('file', {}).get('url', '')
                if source:
                    blocks.append({'type': 'image', 'source': source})
            elif block_type == 'callout':
                print(block)
                if 'text' in block[block_type]:
                    text_list = block[block_type]['text']
                    content = '\n'.join([text.get('plain_text', '') for text in text_list])
                    if content:
                        blocks.append({'type': 'callout', 'content': content})
        # Добавьте обработку других типов блоков Notion по мере необходимости.

    return render_template('notion_template.html', blocks=blocks)

def parse_paragraph(text_list):
    content = ""
    for text in text_list:
        if text.get('href'):
            content += f'<a href="{html.escape(text["href"])}">{html.escape(text["plain_text"])}</a>'
        else:
            content += html.escape(text.get('plain_text', ''))
    print(content)
    return content

if __name__ == '__main__':
    app.run(debug=True)
