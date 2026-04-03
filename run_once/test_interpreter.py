# run_once/test_interpreter.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()  # must happen before importing nodes that init LLM at module level

from schemas import AgentState, RawBrief, BrandContext
from nodes.interpreter import interpret_brief

state = AgentState(
    raw_brief=RawBrief(
        row_id="row_001",
        brand_name="GlowSkin",
        content_type="reel",
        topic="SPF myths",
        key_message="SPF is not just for summer, everyone needs it daily",
        target_audience="Women 25-40 interested in skincare",
        mandatory_inclusions="Mention dermatologist tested",
        reference_urls="",
        free_text_notes="Keep it educational but fun"
    ),
    brand_context=BrandContext(
        tone_of_voice="warm, conversational, science-backed but accessible",
        past_themes=["ingredient education", "before/after", "founder story"],
        client_rules=["Never use the word cheap", "Always mention dermatologist tested"],
        similarity_score=0.3
    )
)

result = interpret_brief(state)
if result.flagged:
    print("Flagged:", result.flag_reason)
else:
    ib = result.interpreted_brief
    print("Summary:", ib.one_line_summary)
    print("Hooks:")
    for i, h in enumerate(ib.hook_options):
        print(f"  {i+1}. {h}")
    print("Confidence:", ib.confidence_score)