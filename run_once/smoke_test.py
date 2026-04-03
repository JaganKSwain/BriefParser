# run_once/smoke_test.py
import os
from dotenv import load_dotenv
load_dotenv()

# 1. Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
print("Gemini:", llm.invoke("Say OK").content)

# 2. Notion
from notion_client import Client
notion = Client(auth=os.environ["NOTION_TOKEN"])
me = notion.users.me()
print("Notion user:", me["name"])

# 3. Slack
import requests
r = requests.post(os.environ["SLACK_WEBHOOK_URL"],
                  json={"text": "Smoke test — agent is live"})
print("Slack:", r.status_code)

# 4. Airtable
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_API_KEY']}"}
base = os.environ["AIRTABLE_BASE_ID"]
table = os.environ["AIRTABLE_TABLE_NAME"]
r = requests.get(f"https://api.airtable.com/v0/{base}/{table}?maxRecords=1", headers=headers)
print("Airtable:", r.status_code)