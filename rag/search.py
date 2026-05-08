"""Query the FAISS index."""
import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = Path(__file__).parent / "index.faiss"
CHUNKS_PATH = Path(__file__).parent / "chunks.json"
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
_index = None
_chunks = None


def _lazy_load():
    global _model, _index, _chunks
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
        _index = faiss.read_index(str(INDEX_PATH))
        _chunks = json.loads(CHUNKS_PATH.read_text())


def search(query: str, k: int = 5) -> list[dict]:
    _lazy_load()
    q_emb = _model.encode([query]).astype("float32")
    distances, indices = _index.search(q_emb, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        chunk = _chunks[idx]
        results.append({
            "source": chunk["source"],
            "text": chunk["text"],
            "score": float(dist),
        })
    return results


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "bond0 dhcp regression"
    for r in search(query):
        print(f"\n[{r['source']}] (score={r['score']:.3f})")
        print(r["text"][:200] + "...")