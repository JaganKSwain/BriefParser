# run_once/build_index.py
# Builds the FAISS brand similarity index from data/brand_profiles.json.
# Safe to re-run any time brand_profiles.json is updated.
import json, faiss, pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Resolve paths relative to this script — works regardless of CWD
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR   = ROOT / "data"
INDEX_DIR  = DATA_DIR / "faiss_index"
PROFILES_FILE = DATA_DIR / "brand_profiles.json"

model    = SentenceTransformer("all-MiniLM-L6-v2")
profiles = json.loads(PROFILES_FILE.read_text())

print(f"Loaded {len(profiles)} brand profiles:")
for p in profiles:
    print(f"  • {p['brand_name']} ({p['category']})")

texts = [
    f"{p['brand_name']} {p['category']} {p['tone_of_voice']} {' '.join(p['past_themes'])}"
    for p in profiles
]

embeddings = model.encode(texts).astype("float32")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

INDEX_DIR.mkdir(parents=True, exist_ok=True)
faiss.write_index(index, str(INDEX_DIR / "brands.index"))
with open(INDEX_DIR / "profiles.pkl", "wb") as f:
    pickle.dump(profiles, f)

print(f"\nIndex built: {index.ntotal} vectors, dim={embeddings.shape[1]}")
print(f"Saved to: {INDEX_DIR}")