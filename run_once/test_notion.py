# run_once/test_notion.py
from notion_client import Client
import os
from dotenv import load_dotenv
load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])

# 1. Check your identity
me = notion.users.me()
print(f"Connected as: {me['name']}")

# 2. Fetch the template page — should return page metadata
template = notion.pages.retrieve(os.environ["NOTION_BRIEF_TEMPLATE_ID"])
print(f"Template page found: {template['url']}")

# 3. Create a test child page to confirm write access
new_page = notion.pages.create(
    parent={"page_id": os.environ["NOTION_PARENT_PAGE_ID"]},
    properties={
        "title": {
            "title": [{"text": {"content": "TEST — delete me"}}]
        }
    },
    children=[
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": "Write access confirmed."}}]
            }
        }
    ]
)
print(f"Test page created: {new_page['url']}")
print("All Notion checks passed.")