import markdown_it
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

# Helper function to convert inline children to Notion rich_text
def inline_children_to_rich_text(children):
    """Convert markdown-it inline children to Notion rich_text array"""
    rich_text = []
    if not children:
        return rich_text
    
    # Track current formatting state
    bold = False
    italic = False
    code = False
    strikethrough = False
    
    for child in children:
        if child.type == "strong_open":
            bold = True
        elif child.type == "strong_close":
            bold = False
        elif child.type == "em_open":
            italic = True
        elif child.type == "em_close":
            italic = False
        elif child.type == "code_inline":
            rich_text.append({
                "type": "text",
                "text": {"content": child.content},
                "annotations": {
                    "bold": bold,
                    "italic": italic,
                    "code": True,
                    "strikethrough": strikethrough,
                    "underline": False,
                    "color": "default"
                }
            })
        elif child.type == "s_open":
            strikethrough = True
        elif child.type == "s_close":
            strikethrough = False
        elif child.type == "text":
            rich_text.append({
                "type": "text",
                "text": {"content": child.content},
                "annotations": {
                    "bold": bold,
                    "italic": italic,
                    "code": code,
                    "strikethrough": strikethrough,
                    "underline": False,
                    "color": "default"
                }
            })
        elif child.type == "softbreak":
            rich_text.append({
                "type": "text",
                "text": {"content": "\n"},
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "code": False,
                    "strikethrough": False,
                    "underline": False,
                    "color": "default"
                }
            })
    
    return rich_text

def markdown_to_notion_blocks(md_text):
    md = markdown_it.MarkdownIt()
    tokens = md.parse(md_text)

    blocks = []
    current_block_type = None  # Track what block we're building
    in_list = False
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.type == "heading_open":
            level = int(token.tag[1])  # Extract heading level (e.g., h1 -> 1)
            # Notion only supports heading_1, heading_2, heading_3
            level = min(level, 3)
            current_block_type = f"heading_{level}"
            blocks.append({
                "type": current_block_type,
                current_block_type: {"rich_text": []}
            })
        
        elif token.type == "heading_close":
            current_block_type = None
        
        elif token.type == "paragraph_open":
            if not in_list:
                current_block_type = "paragraph"
                blocks.append({"type": "paragraph", "paragraph": {"rich_text": []}})
        
        elif token.type == "paragraph_close":
            if not in_list:
                current_block_type = None
        
        elif token.type == "bullet_list_open":
            in_list = True
        
        elif token.type == "bullet_list_close":
            in_list = False
        
        elif token.type == "ordered_list_open":
            in_list = True
        
        elif token.type == "ordered_list_close":
            in_list = False
        
        elif token.type == "list_item_open":
            current_block_type = "bulleted_list_item"
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": []}
            })
        
        elif token.type == "list_item_close":
            current_block_type = None
        
        elif token.type == "inline":
            # Convert inline children to rich_text with proper formatting
            rich_text = inline_children_to_rich_text(token.children)
            
            # Add rich_text to the current block
            if blocks and current_block_type:
                blocks[-1][current_block_type]["rich_text"].extend(rich_text)
        
        elif token.type == "fence" or token.type == "code_block":
            # Code blocks
            blocks.append({
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": token.content.rstrip()}}],
                    "language": token.info if token.info else "plain text"
                }
            })
        
        i += 1

    return blocks

def add_markdown_to_notion(page_id, md_text):
    blocks = markdown_to_notion_blocks(md_text)
    
    # Send blocks to Notion
    notion.blocks.children.append(
        block_id=page_id,
        children=blocks
    )

def create_notion_page(page_title, markdown_content):

    # Create a new page
    page = notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties={"title": {"title": [{"text": {"content": page_title}}]}}
    )
    print(page)
    # Add the markdown text to the page
    add_markdown_to_notion(page["id"], markdown_content)
    return "Page created successfully"