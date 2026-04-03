import requests
from config import SLACK_WEBHOOK_URL


def _post(message: str) -> bool:
    r = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message},
        timeout=10
    )
    return r.status_code == 200


def notify_scriptwriter(
    scriptwriter_name: str,
    brand_name: str,
    content_type: str,
    one_line_summary: str,
    notion_url: str,
    deadline: str,
    flagged: bool = False,
    flag_reason: str = None
) -> bool:

    if flagged:
        message = "\n".join([
            ":warning: *Brief flagged — coordinator review needed*",
            "",
            f"*Brand:* {brand_name}",
            f"*Content type:* {content_type}",
            f"*Flag reason:* {flag_reason}",
            f"*Notion page:* {notion_url}" if notion_url else "*Notion page:* not created",
            "",
            "Please review and assign manually."
        ])
    else:
        message = "\n".join([
            ":memo: *New brief ready for scriptwriting*",
            "",
            f"*Assigned to:* {scriptwriter_name}",
            f"*Brand:* {brand_name}",
            f"*Content type:* {content_type}",
            f"*Summary:* {one_line_summary}",
            f"*Deadline:* {deadline}",
            f"*Notion page:* {notion_url}",
        ])

    return _post(message)


def notify_error(context: str, error: str) -> bool:
    """Posts a system error alert to the channel."""
    message = "\n".join([
        ":red_circle: *Agent error — manual intervention needed*",
        "",
        f"*Context:* {context}",
        f"*Error:* {error}",
    ])
    return _post(message)