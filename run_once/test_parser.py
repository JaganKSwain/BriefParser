# run_once/test_parser.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from schemas import AgentState, RawBrief
from nodes.parser import parse_brief

# --- TEST 1: Complete brief (should pass through) ---
print("\n--- TEST 1: Complete brief ---")
state1 = AgentState(raw_brief=RawBrief(
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
result1 = parse_brief(state1)
print("Flagged:", result1.flagged)
print("Flag reason:", result1.flag_reason)

# --- TEST 2: Missing key_message ---
print("\n--- TEST 2: Blank key_message ---")
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
result2 = parse_brief(state2)
print("Flagged:", result2.flagged)
print("Flag reason:", result2.flag_reason)

# --- TEST 3: Meaningless content ---
print("\n--- TEST 3: Meaningless fields ---")
state3 = AgentState(raw_brief=RawBrief(
    row_id="row_003",
    brand_name="???",
    content_type="idk",
    topic="n/a",
    key_message="tbd",
    target_audience="everyone",
    mandatory_inclusions="",
    reference_urls="",
    free_text_notes=""
))
result3 = parse_brief(state3)
print("Flagged:", result3.flagged)
print("Flag reason:", result3.flag_reason)
