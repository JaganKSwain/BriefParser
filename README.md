# Scrollhouse Brief Agent — PS-02

An agentic AI pipeline that automates the **Content Brief to Script Pipeline** for Scrollhouse. When a client submits a brief via Google Forms (captured in Google Sheets), the agent reads it, validates it, retrieves brand context, interprets the creative intent using an LLM, creates a formatted Notion page, notifies the assigned scriptwriter on Slack, and updates the Airtable tracker — all without any manual intervention.

---

## Architecture

```
Google Sheets (polling)
        │
        ▼
   [Parser Node]          ← LLM decides: is the brief complete?
        │
   (flagged?) ──────────────────────────────────┐
        │                                        │
        ▼                                        ▼
[Brand Retriever Node]                    [Dispatcher Node]
  FAISS semantic search                   (flagged path:
  on brand name                            Notion + Slack
        │                                   alert + Airtable
   (unknown brand?) ──────────────────────→  "Flagged")
        │
        ▼
 [Interpreter Node]       ← LLM interprets brief, generates hooks,
        │                    tone, visual treatment, confidence score
   (low confidence?) ─────────────────────────────┘
        │
        ▼
 [Dispatcher Node]
   → Create Notion brief page
   → Notify scriptwriter on Slack
   → Update Airtable (Brief Processed)
```

---

## Setup

### Prerequisites

- Python 3.10+
- A virtual environment (recommended)
- API keys for: Google AI Studio (Gemini), Notion, Slack (Incoming Webhook), Airtable
- A Google Cloud service account with Sheets + Drive API enabled (`credentials.json`)

### 1. Clone and install

```bash
git clone <your-fork-url>
cd submission_TeamLuminary

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.example .env
```

Open `.env` and set:

```env
# LLM
GOOGLE_API_KEY=your_google_ai_studio_key

# Google Sheets (brief intake)
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_CREDENTIALS_JSON=./credentials.json   # path to service account JSON

# Notion
NOTION_TOKEN=your_notion_integration_token
NOTION_BRIEF_TEMPLATE_ID=your_template_page_id
NOTION_PARENT_PAGE_ID=your_parent_page_id

# Slack (Incoming Webhook)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Airtable
AIRTABLE_API_KEY=your_airtable_personal_access_token
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_NAME=Briefs

# LangSmith tracing (optional — set to true only if you have a valid key)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=scrollhouse-ps02
```

### 3. Set up Google Sheets

Your Google Sheet must have **Sheet1** with this header row (Row 1):

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| brand_name | content_type | topic | key_message | target_audience | mandatory_inclusions | reference_urls | free_text_notes |

Add test rows from Row 2 onward. The agent processes new rows only — already-seen rows are tracked in `data/processed_rows.json`.

Share the Google Sheet with your service account email (found in `credentials.json` → `client_email`).

### 4. Build the FAISS brand index

Run this once (and again whenever you update `data/brand_profiles.json`):

```bash
python run_once/build_index.py
```

Expected output:
```
Loaded 3 brand profiles:
  • GlowSkin (skincare)
  • FinTrack (fintech)
  • PeakFit (fitness)

Index built: 3 vectors, dim=384
```

### 5. Run the smoke test

Confirms all API credentials are working before starting the agent:

```bash
python run_once/smoke_test.py
```

Expected output:
```
Gemini: OK
Notion user: <your workspace name>
Slack: 200
Airtable: 200
```

### 6. Run the agent

```bash
python main.py
```

The agent polls Google Sheets every 30 seconds. Add a row to the sheet and watch it process end-to-end.

To stop: `Ctrl+C`

---

## Sample Input (Google Sheet Row)

| Field | Value |
|---|---|
| brand_name | GlowSkin |
| content_type | reel |
| topic | SPF myths |
| key_message | SPF is not just for summer, everyone needs it daily |
| target_audience | Women 25-40 interested in skincare |
| mandatory_inclusions | Mention dermatologist tested |
| reference_urls | |
| free_text_notes | Keep it fun and educational |

---

## Running Individual Tests

```bash
# Parser node
python run_once/test_parser.py

# Brand retriever (FAISS)
python run_once/test_brand_retriever.py

# Interpreter (LLM)
python run_once/test_interpreter.py

# Full end-to-end graph
python run_once/test_graph.py

# All tools (Sheets, Notion, Slack, Airtable)
python tools/test_tools.py
```

---

## Adding a New Brand

1. Add an entry to `data/brand_profiles.json`:
```json
{
  "brand_name": "YourBrand",
  "category": "your_category",
  "tone_of_voice": "describe the tone",
  "past_themes": ["theme1", "theme2"],
  "client_rules": ["Rule 1", "Rule 2"]
}
```

2. Rebuild the index:
```bash
python run_once/build_index.py
```

---

## Project Structure

```
submission_TeamLuminary/
├── main.py                    # Entry point — polling loop
├── graph.py                   # LangGraph pipeline definition
├── schemas.py                 # Pydantic data models
├── config.py                  # Environment variable loading
├── logger.py                  # Timestamped logging
├── nodes/
│   ├── parser.py              # Node 1: LLM brief quality check
│   ├── brand_retriever.py     # Node 2: FAISS brand context retrieval
│   ├── interpreter.py         # Node 3: LLM creative interpretation
│   └── dispatcher.py          # Node 4: Notion + Slack + Airtable
├── tools/
│   ├── sheets.py              # Google Sheets reader
│   ├── notion.py              # Notion page creator
│   ├── slack.py               # Slack webhook notifier
│   └── airtable.py            # Airtable CRUD
├── data/
│   ├── brand_profiles.json    # Brand knowledge base
│   ├── scriptwriters.json     # Scriptwriter roster with leave status
│   └── faiss_index/           # Built by build_index.py
│       ├── brands.index
│       └── profiles.pkl
└── run_once/
    ├── smoke_test.py           # API connectivity check
    ├── build_index.py          # FAISS index builder
    └── test_*.py               # Individual component tests
```

---

## Known Limitations

- Reference URL validation is not implemented — broken URLs are passed through to Notion as-is.
- Content type precedent checking is not implemented — new content types for a client are not flagged.
- Notion pages are created under a single parent page, not linked to per-client hub pages.
- Scriptwriter assignment uses "first available" logic; speciality matching is not implemented.
- The agent uses polling (every 30 seconds) rather than a webhook trigger from Google Forms.
