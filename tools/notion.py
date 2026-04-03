from notion_client import Client
from notion_client.errors import APIResponseError
from config import NOTION_TOKEN, NOTION_PARENT_ID
from schemas import InterpretedBrief, RawBrief
from datetime import date

notion = Client(auth=NOTION_TOKEN)


def _build_body_blocks(raw: RawBrief, interpreted: InterpretedBrief) -> list:
    """Builds the Notion block content for a clean interpreted brief."""

    ambiguity_text = (
        "\n".join(f"- {f}" for f in interpreted.ambiguity_flags)
        if interpreted.ambiguity_flags
        else "None"
    )

    hooks_text = "\n".join(
        f"{i+1}. {h}" for i, h in enumerate(interpreted.hook_options)
    )

    sections = [
        ("Brand",               raw.brand_name),
        ("Content type",        raw.content_type),
        ("Submitted",           str(date.today())),
        ("",                    ""),
        ("One-line summary",    interpreted.one_line_summary),
        ("",                    ""),
        ("Hook options",        hooks_text),
        ("",                    ""),
        ("Tone direction",      interpreted.tone_direction),
        ("",                    ""),
        ("Visual treatment",    interpreted.visual_treatment),
        ("",                    ""),
        ("Scriptwriter notes",  interpreted.scriptwriter_notes),
        ("",                    ""),
        ("Ambiguity flags",     ambiguity_text),
        ("",                    ""),
        ("Confidence score",    str(round(interpreted.confidence_score, 2))),
        ("",                    ""),
        ("Status",              "Awaiting scriptwriter"),
    ]

    blocks = []
    for label, value in sections:
        if label == "":
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            })
            continue

        text = f"{label}: {value}" if value else label
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": text[:2000]}  # Notion 2000 char limit
                }]
            }
        })

    return blocks


def _build_flag_blocks(raw: RawBrief, flag_reason: str) -> list:
    """Builds the Notion block content for a flagged brief."""
    lines = [
        f"Brand: {raw.brand_name}",
        f"Content type: {raw.content_type}",
        f"Topic: {raw.topic}",
        f"Submitted: {date.today()}",
        "",
        "STATUS: FLAGGED — coordinator review required",
        "",
        f"Flag reason: {flag_reason}",
        "",
        "Raw submission:",
        f"Key message: {raw.key_message or 'not provided'}",
        f"Target audience: {raw.target_audience or 'not provided'}",
        f"Mandatory inclusions: {raw.mandatory_inclusions or 'not provided'}",
        f"Notes: {raw.free_text_notes or 'not provided'}",
    ]

    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": line[:2000]}
                }]
            }
        }
        for line in lines
    ]


def create_brief_page(
    raw: RawBrief,
    interpreted: InterpretedBrief = None,
    flagged: bool = False,
    flag_reason: str = ""
) -> str:
    """
    Creates a Notion page for the brief.
    Returns the page URL.
    Raises on API failure — let the dispatcher handle the error.
    """

    title = (
        f"[FLAGGED] {raw.brand_name} — {raw.content_type} — {date.today()}"
        if flagged
        else f"{raw.brand_name} — {raw.content_type} — {date.today()}"
    )

    blocks = (
        _build_flag_blocks(raw, flag_reason)
        if flagged or interpreted is None
        else _build_body_blocks(raw, interpreted)
    )

    try:
        page = notion.pages.create(
            parent={"page_id": NOTION_PARENT_ID},
            properties={
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
            children=blocks
        )
        return page["url"]

    except APIResponseError as e:
        raise RuntimeError(f"Notion page creation failed: {e.code} — {e.message}")