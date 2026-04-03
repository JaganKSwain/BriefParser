# run_once/test_slack.py
import requests, os
from dotenv import load_dotenv
load_dotenv()

payload = {
    "text": "Scrollhouse Agent is live. Slack connection verified."
}

r = requests.post(os.environ["SLACK_WEBHOOK_URL"], json=payload)
print("Status:", r.status_code)
print("Response:", r.text)