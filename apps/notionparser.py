from datetime import datetime

from flask import render_template, Blueprint
import requests
import html
from pageindex import pageindex, notionindex
from config import NOTION_TOKEN

from pytz import timezone

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')
more_bp = Blueprint('more', __name__, url_prefix='/more')

ts = datetime.now()
timezone = timezone('Etc/GMT-3')
ts_msk = ts.astimezone(timezone)

@knowledge_bp.route('/<page_name>', methods=['GET'])
def knowledge_page(page_name):
    notion_page = notionindex[f"{page_name}"]
    blocks = notion_integration(notion_page)
    title = pageindex[f"{page_name}"]
    return render_template(f'knowledge/{page_name}.html', title=title, active_page=page_name,  route='knowledge',  blocks=blocks, ts=ts_msk)


@more_bp.route('/<page_name>', methods=['GET'])
def more_pages(page_name):
    notion_page = notionindex[f"{page_name}"]
    blocks = notion_integration(notion_page)
    title = pageindex[f"{page_name}"]
    return render_template(f'more/{page_name}.html', title=title, active_page=page_name,  route='more',  blocks=blocks, ts=ts_msk)



def notion_integration(NOTION_PAGE_ID):
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
            elif block_type == 'code':
                content = block['code']['text'][0]['text']['content']
                blocks.append({'type': 'code', 'content': content})
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
            elif block_type == 'video':
                video_data = block.get('video', {})
                video_type = video_data.get('type', '')
                if video_type == 'external':
                    video_url = video_data.get('external', {}).get('url', '')
                    if video_url:
                        blocks.append({'type': 'video', 'source': video_url})

            elif block_type == 'callout':
                print(block)
                if 'text' in block[block_type]:
                    text_list = block[block_type]['text']
                    content = '\n'.join([text.get('plain_text', '') for text in text_list])
                    if content:
                        blocks.append({'type': 'callout', 'content': content})
        # Добавьте обработку других типов блоков Notion по мере необходимости.
    print(blocks)

    combined_blocks = []
    current_block = None
    for item in blocks:
        if item['type'] == 'heading_3':
            if current_block is not None:
                combined_blocks.append(current_block)
            current_block = {'type': 'combined', 'content': []}
            combined_blocks.append(item)
        else:
            if current_block is not None:
                current_block['content'].append(item)
    if current_block is not None:
        combined_blocks.append(current_block)

    print(combined_blocks)

    if len(combined_blocks) > 0:
        return combined_blocks
    else:
        return blocks

def parse_paragraph(text_list):
    content = ""
    for text in text_list:
        if text.get('href'):
            content += f'<a href="{html.escape(text["href"])}">{html.escape(text["plain_text"])}</a>'
        else:
            content += html.escape(text.get('plain_text', ''))
    print(content)
    return content

