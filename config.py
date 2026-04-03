from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY        = os.environ["GOOGLE_API_KEY"]
LANGCHAIN_API_KEY     = os.environ.get("LANGSMITH_API_KEY")
GOOGLE_SHEET_ID       = os.environ["GOOGLE_SHEET_ID"]
GOOGLE_CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON", "./credentials.json")
NOTION_TOKEN          = os.environ["NOTION_TOKEN"]
NOTION_TEMPLATE_ID    = os.environ["NOTION_BRIEF_TEMPLATE_ID"]
NOTION_PARENT_ID      = os.environ["NOTION_PARENT_PAGE_ID"]
SLACK_WEBHOOK_URL     = os.environ["SLACK_WEBHOOK_URL"]
AIRTABLE_API_KEY      = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID      = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE_NAME   = os.environ["AIRTABLE_TABLE_NAME"]