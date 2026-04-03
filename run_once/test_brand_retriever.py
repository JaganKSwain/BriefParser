# run_once/test_brand_retriever.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import AgentState, RawBrief
from nodes.brand_retriever import retrieve_brand_context

# Known brand
state = AgentState(raw_brief=RawBrief(
    row_id="row_001",
    brand_name="GlowSkin",
    content_type="reel",
    topic="SPF myths",
    key_message="SPF is not just for summer",
    target_audience="Women 25-40",
    mandatory_inclusions="",
    reference_urls="",
    free_text_notes=""
))
result = retrieve_brand_context(state)
print("Brand found:", result.brand_context.tone_of_voice if result.brand_context else "None")
print("Flagged:", result.flagged)

# Unknown brand
state2 = state.model_copy(update={
    "raw_brief": state.raw_brief.model_copy(update={"brand_name": "RandomBrandXYZ"})
})
result2 = retrieve_brand_context(state2)
print("Unknown brand flagged:", result2.flagged)
print("Reason:", result2.flag_reason)