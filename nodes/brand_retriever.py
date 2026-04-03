import faiss, pickle, os
import numpy as np
from sentence_transformers import SentenceTransformer
from schemas import AgentState, BrandContext

_model = SentenceTransformer("all-MiniLM-L6-v2")
_index = faiss.read_index("data/faiss_index/brands.index")
with open("data/faiss_index/profiles.pkl", "rb") as f:
    _profiles = pickle.load(f)

SIMILARITY_THRESHOLD = 1.2  # L2 distance — lower is more similar

def retrieve_brand_context(state: AgentState) -> AgentState:
    if state.flagged:
        return state  # don't process flagged briefs

    brand_name = state.raw_brief.brand_name
    query = _model.encode([brand_name]).astype("float32")
    distances, indices = _index.search(query, k=1)

    distance = distances[0][0]
    idx = indices[0][0]

    if distance > SIMILARITY_THRESHOLD:
        return state.model_copy(update={
            "flagged": True,
            "flag_reason": f"Unrecognised brand '{brand_name}' — not found in brand database. Possible new client or data entry error."
        })

    profile = _profiles[idx]
    context = BrandContext(
        tone_of_voice=profile["tone_of_voice"],
        past_themes=profile["past_themes"],
        client_rules=profile["client_rules"],
        similarity_score=float(distance)
    )

    return state.model_copy(update={"brand_context": context})