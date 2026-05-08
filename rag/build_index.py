"""Build a FAISS index over markdown release notes."""
import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CORPUS_DIR = Path(__file__).parent / "corpus"
INDEX_PATH = Path(__file__).parent / "index.faiss"
CHUNKS_PATH = Path(__file__).parent / "chunks.json"
MODEL_NAME = "all-MiniLM-L6-v2"


def chunk_markdown(text: str, max_chars: int = 800) -> list[str]:
    """Split markdown by paragraph, then merge until each chunk is <max_chars."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for p in paragraphs:
        if len(current) + len(p) < max_chars:
            current = f"{current}\n\n{p}".strip()
        else:
            if current:
                chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    return chunks


def main():
    print(f"Loading model {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)

    chunks_meta = []  # list of {source, chunk_idx, text}
    all_texts = []

    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        text = md_file.read_text()
        for i, chunk in enumerate(chunk_markdown(text)):
            chunks_meta.append({
                "source": md_file.name,
                "chunk_idx": i,
                "text": chunk,
            })
            all_texts.append(chunk)

    print(f"Embedding {len(all_texts)} chunks...")
    embeddings = model.encode(all_texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))
    CHUNKS_PATH.write_text(json.dumps(chunks_meta, indent=2))
    print(f"Wrote index: {INDEX_PATH}")
    print(f"Wrote chunks: {CHUNKS_PATH}")


if __name__ == "__main__":
    main()