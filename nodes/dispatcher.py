import json, requests
from datetime import date, timedelta
from schemas import AgentState
from tools.notion import create_brief_page
from tools.slack import notify_scriptwriter
from tools.airtable import create_brief_record
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME
from pathlib import Path

def load_scriptwriters():
    return json.loads(Path("data/scriptwriters.json").read_text())

def assign_scriptwriter(brand_context) -> str:
    writers = load_scriptwriters()
    available = [w for w in writers if not w["on_leave"]]
    if not available:
        return "Backup Writer"
    # simple match: return first available (extend with smarter matching later)
    return available[0]["name"]

def dispatch(state: AgentState) -> AgentState:
    raw        = state.raw_brief
    interpreted = state.interpreted_brief
    deadline   = (date.today() + timedelta(days=2)).strftime("%d %b %Y")

    if state.flagged:
        # Still create a Notion page and notify — but as a flag, not an assignment
        try:
            notion_url = create_brief_page(raw, interpreted) if interpreted else None
        except Exception:
            notion_url = None

        notify_scriptwriter(
            scriptwriter_name="",
            brand_name=raw.brand_name,
            content_type=raw.content_type,
            one_line_summary="",
            notion_url=notion_url or "Not created",
            deadline=deadline,
            flagged=True,
            flag_reason=state.flag_reason
        )

        record_id = create_brief_record(
            brand_name=raw.brand_name,
            content_type=raw.content_type,
            topic=raw.topic,
            status="Flagged",
            scriptwriter="",
            notion_link=notion_url or "",
            flag_reason=state.flag_reason
        )

        return state.model_copy(update={
            "notion_page_url": notion_url,
            "airtable_record_id": record_id
        })

    # Happy path
    writer = assign_scriptwriter(state.brand_context)

    notion_url = create_brief_page(raw, interpreted)

    notify_scriptwriter(
        scriptwriter_name=writer,
        brand_name=raw.brand_name,
        content_type=raw.content_type,
        one_line_summary=interpreted.one_line_summary,
        notion_url=notion_url,
        deadline=deadline,
        flagged=False
    )

    record_id = create_brief_record(
        brand_name=raw.brand_name,
        content_type=raw.content_type,
        topic=raw.topic,
        status="Brief Processed",
        scriptwriter=writer,
        notion_link=notion_url,
        flag_reason=""
    )

    return state.model_copy(update={
        "assigned_scriptwriter": writer,
        "notion_page_url": notion_url,
        "airtable_record_id": record_id
    })