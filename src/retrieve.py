"""
retrieve.py — Stages 3 & 4: Embedding + Vector Store, and Retrieval.

This module owns the two ends of the same pipe (see spec/stages.md for why they
live together):

    build_index()    -- run ONCE, offline. Embeds every chunk from chunk.py and
                        stores the vectors + metadata in a ChromaDB collection.
    retrieve(query)  -- run PER QUERY, online. (Added in Stage 4.) Embeds the
                        query and returns the most similar chunks.

The two share a single embedding model and a single Chroma collection. That
shared contract is the whole reason they belong in one file: change the model
or collection here and both sides stay consistent. Embedding the query with a
*different* model than the documents would make cosine distance meaningless.
"""

from __future__ import annotations

import sys

import chromadb
from chromadb.utils import embedding_functions

from chunk import build_all_chunks
from clean import PROJECT_ROOT

# --- Shared config -----------------------------------------------------------
CHROMA_DIR = PROJECT_ROOT / "chroma_db"   # on-disk persistence (git-ignored)
COLLECTION_NAME = "rmp_reviews"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

# The embedding function converts text -> vectors with all-MiniLM-L6-v2.
# By attaching it to the collection, ChromaDB uses it automatically for BOTH
# the documents (when we add them) and the query (when we search) — which is
# exactly how we guarantee both land in the same vector space.
_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)


def _client() -> chromadb.api.ClientAPI:
    """A persistent Chroma client backed by CHROMA_DIR (survives across runs)."""
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection():
    """Open (or create) our collection, wired to the embedding function and
    configured for cosine distance. Used by both indexing and querying."""
    return _client().get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_embedding_fn,
        metadata={"hnsw:space": "cosine"},  # default is L2; we want cosine
    )


# --- Stage 3: build the index ------------------------------------------------
def build_index() -> int:
    """Embed all chunks and (re)load them into the Chroma collection.

    Run this once (and again whenever the source docs change). Returns the
    number of chunks indexed so the caller can sanity-check the count.
    """
    chunks = build_all_chunks()
    client = _client()

    # Drop any existing collection first so a rebuild can't leave behind stale
    # or duplicate chunks. delete_collection raises if it doesn't exist yet, and
    # the exception type varies across Chroma versions, so we guard broadly.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )

    # One add() call: Chroma embeds each document with our embedding function
    # and stores it alongside its id and metadata.
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["document"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )
    return collection.count()


# --- Stage 4: retrieve -------------------------------------------------------
def retrieve(query: str, k: int = TOP_K, max_distance: float | None = None,
             where: dict | None = None) -> list[dict]:
    """Embed ``query`` and return the ``k`` most similar chunks.

    Returns a list of dicts (id, document, metadata, distance) sorted ascending
    by cosine distance — most relevant first. ``max_distance`` optionally drops
    weak matches; ``where`` is an optional Chroma metadata filter (used later by
    the metadata-filtering stretch feature).
    """
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k, where=where)

    # Chroma wraps each result list one-per-query; we sent a single query -> [0].
    hits: list[dict] = []
    for id_, doc, meta, dist in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        if max_distance is not None and dist > max_distance:
            continue
        hits.append({"id": id_, "document": doc, "metadata": meta, "distance": dist})
    return hits


def _print_hits(query: str, hits: list[dict]) -> None:
    """Debug view of retrieved chunks — the basis for the Gradio debug panel."""
    print(f"\nQuery: {query!r}")
    print(f"Top {len(hits)} chunks by ascending cosine distance:\n")
    for rank, h in enumerate(hits, start=1):
        m = h["metadata"]
        print(f"#{rank}  distance={h['distance']:.4f}  "
              f"source={m['source']}  type={m['type']}  id={h['id']}")
        indented = h["document"].replace("\n", "\n    ")
        print(f"    {indented}\n")


def _build_and_report() -> None:
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print("Building index — the first run downloads the model (~80 MB), "
          "so it may take a minute...")
    n_indexed = build_index()
    expected = len(build_all_chunks())
    print(f"Indexed {n_indexed} chunks (expected {expected}) into collection "
          f"'{COLLECTION_NAME}' at {CHROMA_DIR.relative_to(PROJECT_ROOT)}/")
    print("OK" if n_indexed == expected else "WARNING: count mismatch!")


def main() -> None:
    # No args -> (re)build the index. With args -> treat them as a search query.
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        _print_hits(query, retrieve(query))
    else:
        _build_and_report()


if __name__ == "__main__":
    main()
