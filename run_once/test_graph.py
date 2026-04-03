# run_once/test_graph.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()  # must happen before importing nodes that init LLM at module level

from graph import pipeline
from schemas import AgentState, RawBrief

print("\n--- TEST 1: Happy path ---")
state = AgentState(raw_brief=RawBrief(
    row_id="row_001",
    brand_name="GlowSkin",
    content_type="reel",
    topic="SPF myths",
    key_message="SPF is not just for summer, everyone needs it daily",
    target_audience="Women 25-40 interested in skincare",
    mandatory_inclusions="Mention dermatologist tested",
    reference_urls="",
    free_text_notes="Keep it fun and educational"
))
result = AgentState(**pipeline.invoke(state))
print("Flagged:", result.flagged)
print("Scriptwriter:", result.assigned_scriptwriter)
print("Notion URL:", result.notion_page_url)
print("Airtable ID:", result.airtable_record_id)

print("\n--- TEST 2: Incomplete brief (blank key_message) ---")
state2 = AgentState(raw_brief=RawBrief(
    row_id="row_002",
    brand_name="GlowSkin",
    content_type="reel",
    topic="SPF myths",
    key_message="",
    target_audience="tbd",
    mandatory_inclusions="",
    reference_urls="",
    free_text_notes=""
))
result2 = AgentState(**pipeline.invoke(state2))
print("Flagged:", result2.flagged)
print("Reason:", result2.flag_reason)

print("\n--- TEST 3: Unknown brand ---")
state3 = AgentState(raw_brief=RawBrief(
    row_id="row_003",
    brand_name="RandomBrandXYZ",
    content_type="reel",
    topic="product launch",
    key_message="New product is amazing",
    target_audience="everyone",
    mandatory_inclusions="",
    reference_urls="",
    free_text_notes=""
))
result3 = AgentState(**pipeline.invoke(state3))
print("Flagged:", result3.flagged)
print("Reason:", result3.flag_reason)