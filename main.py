import os
import time
from dotenv import load_dotenv

load_dotenv()

# LangSmith tracing controlled via .env (LANGCHAIN_TRACING_V2=false by default)

from graph import pipeline
from schemas import AgentState
from tools.sheets import fetch_new_briefs
from tools.slack import notify_error
from logger import log, log_error

POLL_INTERVAL = 15  # seconds — fast enough for live demo


def process_brief(brief) -> None:
    print()
    log(f"{'='*55}")
    log(f"NEW BRIEF DETECTED")
    log(f"  Row ID       : {brief.row_id}")
    log(f"  Brand        : {brief.brand_name}")
    log(f"  Content type : {brief.content_type}")
    log(f"  Topic        : {brief.topic}")
    log(f"{'='*55}")

    initial_state = AgentState(raw_brief=brief)

    try:
        log("[ 1/4 ] Running parser (LLM quality check)...")
        log("[ 2/4 ] Retrieving brand context (FAISS)...")
        log("[ 3/4 ] Interpreting brief (LLM)...")
        log("[ 4/4 ] Dispatching to Notion / Slack / Airtable...")
        result = AgentState(**pipeline.invoke(initial_state))

    except Exception as e:
        log_error(f"Pipeline crashed on {brief.row_id}: {e}", e)
        notify_error(
            context=f"Row {brief.row_id} — {brief.brand_name}",
            error=str(e)
        )
        return

    print()
    if result.flagged:
        log(f"⚠️  FLAGGED — coordinator review required")
        log(f"   Reason   : {result.flag_reason}")
        log(f"   Notion   : {result.notion_page_url or 'not created'}")
        log(f"   Airtable : {result.airtable_record_id or 'not created'}")
    else:
        log(f"✅ PROCESSED SUCCESSFULLY")
        log(f"   Scriptwriter : {result.assigned_scriptwriter}")
        log(f"   Notion page  : {result.notion_page_url}")
        log(f"   Airtable ID  : {result.airtable_record_id}")

    log(f"{'='*55}\n")


def run():
    print()
    log("╔══════════════════════════════════════════════════════╗")
    log("║       SCROLLHOUSE BRIEF AGENT — PS-02               ║")
    log("╚══════════════════════════════════════════════════════╝")
    log(f"Polling Google Sheets every {POLL_INTERVAL} seconds.")
    log("Fill in the Google Form to trigger the pipeline.")
    log("Press Ctrl+C to stop.\n")

    while True:
        try:
            briefs = fetch_new_briefs()

            if not briefs:
                log("Watching... (no new briefs)")
            else:
                log(f"Found {len(briefs)} new brief(s). Processing...")
                for brief in briefs:
                    process_brief(brief)

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print()
            log("Agent stopped. Goodbye.")
            break

        except Exception as e:
            log_error(f"Polling error: {e}", e)
            notify_error("Polling loop", str(e))
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()