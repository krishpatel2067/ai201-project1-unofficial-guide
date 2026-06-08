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

import re
import sys

import chromadb
from chromadb.utils import embedding_functions

from chunk import build_chunks
from clean import PROJECT_ROOT

# --- Shared config -----------------------------------------------------------
CHROMA_DIR = PROJECT_ROOT / "chroma_db"   # on-disk persistence (git-ignored)
COLLECTIONS = {"structured": "rmp_structured", "fixed": "rmp_fixed"}
DEFAULT_STRATEGY = "structured"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5
RRF_K = 60   # Reciprocal Rank Fusion constant (standard default)

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


def get_collection(strategy: str = DEFAULT_STRATEGY):
    """Open (or create) the collection for a chunking strategy, wired to the
    embedding function and configured for cosine distance."""
    return _client().get_or_create_collection(
        name=COLLECTIONS[strategy],
        embedding_function=_embedding_fn,
        metadata={"hnsw:space": "cosine"},  # default is L2; we want cosine
    )


# --- Stage 3: build the index ------------------------------------------------
def build_index() -> dict[str, int]:
    """Embed all chunks and (re)load them into Chroma — one collection per
    chunking strategy (structured + fixed), so the UI can toggle between them
    instantly without re-embedding.

    Run once (and again whenever the source docs change). Returns {strategy:
    count} so the caller can sanity-check.
    """
    client = _client()
    counts: dict[str, int] = {}
    for strategy, name in COLLECTIONS.items():
        # Drop any existing collection first so a rebuild can't leave behind
        # stale/duplicate chunks. The not-found exception type varies across
        # Chroma versions, so we guard broadly.
        try:
            client.delete_collection(name)
        except Exception:
            pass
        collection = client.get_or_create_collection(
            name=name,
            embedding_function=_embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )
        chunks = build_chunks(strategy)
        collection.add(
            ids=[c["id"] for c in chunks],
            documents=[c["document"] for c in chunks],
            metadatas=[c["metadata"] for c in chunks],
        )
        counts[strategy] = collection.count()
    return counts


# --- Stage 4: retrieve -------------------------------------------------------
def retrieve(query: str, k: int = TOP_K, hybrid: bool = False,
             strategy: str = DEFAULT_STRATEGY, max_distance: float | None = None,
             where: dict | None = None) -> list[dict]:
    """Return the ``k`` most relevant chunks for ``query``.

    ``hybrid=False`` (default): pure semantic search — embed the query and rank
    by cosine distance. ``hybrid=True``: fuse semantic + BM25 rankings with
    Reciprocal Rank Fusion (see ``_retrieve_hybrid``). ``strategy`` selects the
    chunking collection ('structured' or 'fixed').

    Each hit is a dict (id, document, metadata, distance; plus ``rrf`` in hybrid
    mode), most-relevant first. ``max_distance`` optionally drops weak matches and
    ``where`` is an optional Chroma metadata filter (both semantic mode only).
    """
    if hybrid:
        return _retrieve_hybrid(query, k, strategy)

    collection = get_collection(strategy)
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


# --- Stretch feature: hybrid (semantic + BM25) retrieval --------------------
_bm25_cache: dict[str, tuple] = {}   # strategy -> (BM25Okapi index, chunks)


def _tokenize(text: str) -> list[str]:
    """Lowercase the text and split into alphanumeric word tokens for BM25."""
    return re.findall(r"[a-z0-9]+", text.lower())


def _get_bm25(strategy: str = DEFAULT_STRATEGY):
    """Build (once per strategy) and return (bm25_index, chunks).

    rank-bm25 is imported lazily so semantic-only usage doesn't require it. The
    corpus is small, so we keep each strategy's index in memory rather than
    persisting it.
    """
    if strategy not in _bm25_cache:
        from rank_bm25 import BM25Okapi
        chunks = build_chunks(strategy)
        _bm25_cache[strategy] = (
            BM25Okapi([_tokenize(c["document"]) for c in chunks]), chunks
        )
    return _bm25_cache[strategy]


def _rrf(rankings: list[list[str]]) -> dict[str, float]:
    """Reciprocal Rank Fusion: merge ranked id-lists into one score map.

    A chunk's score is the sum of 1/(RRF_K + rank) over each list it appears in
    (rank is 0-based; higher = better). It uses ranks only, so the retrievers'
    incompatible score scales (cosine distance vs BM25) never need reconciling —
    which is why RRF is the go-to fusion method for hybrid search.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, id_ in enumerate(ranking):
            scores[id_] = scores.get(id_, 0.0) + 1.0 / (RRF_K + rank)
    return scores


def _retrieve_hybrid(query: str, k: int, strategy: str = DEFAULT_STRATEGY) -> list[dict]:
    """Fuse semantic + BM25 rankings with RRF and return the top-k chunks.

    Both retrievers rank ALL chunks; each returned chunk keeps its cosine
    distance (for the debug panel) alongside its fused RRF score.
    """
    bm25, chunks = _get_bm25(strategy)
    id_to_chunk = {c["id"]: c for c in chunks}
    n = len(chunks)

    # Semantic ranking over all chunks (ids + cosine distances; skip docs/meta).
    collection = get_collection(strategy)
    sem = collection.query(query_texts=[query], n_results=n, include=["distances"])
    sem_ids = sem["ids"][0]
    sem_distance = dict(zip(sem_ids, sem["distances"][0]))

    # BM25 ranking over all chunks (best score first).
    bm25_scores = bm25.get_scores(_tokenize(query))
    bm25_ids = [chunks[i]["id"]
                for i in sorted(range(n), key=lambda i: bm25_scores[i], reverse=True)]

    # Fuse the two rankings and take the top-k by RRF score.
    fused = _rrf([sem_ids, bm25_ids])
    top_ids = sorted(fused, key=fused.get, reverse=True)[:k]

    return [
        {
            "id": id_,
            "document": id_to_chunk[id_]["document"],
            "metadata": id_to_chunk[id_]["metadata"],
            "distance": sem_distance.get(id_),
            "rrf": fused[id_],
        }
        for id_ in top_ids
    ]


def _print_hits(query: str, hits: list[dict]) -> None:
    """Debug view of retrieved chunks — the basis for the Gradio debug panel."""
    print(f"\nQuery: {query!r}")
    print(f"Top {len(hits)} chunks:\n")
    for rank, h in enumerate(hits, start=1):
        m = h["metadata"]
        dist = f"{h['distance']:.4f}" if h.get("distance") is not None else "n/a"
        rrf = f"  rrf={h['rrf']:.4f}" if "rrf" in h else ""
        print(f"#{rank}  distance={dist}{rrf}  "
              f"source={m['source']}  type={m['type']}  id={h['id']}")
        indented = h["document"].replace("\n", "\n    ")
        print(f"    {indented}\n")


def _build_and_report() -> None:
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print("Building indexes — the first run downloads the model (~80 MB), "
          "so it may take a minute...")
    counts = build_index()
    for strategy, count in counts.items():
        print(f"  {strategy:<11} -> collection '{COLLECTIONS[strategy]}': {count} chunks")
    print(f"Stored at {CHROMA_DIR.relative_to(PROJECT_ROOT)}/")


def main() -> None:
    # Flags (any order): --rebuild (build the indexes), --hybrid, --fixed.
    args = sys.argv[1:]
    if "--rebuild" in args:
        _build_and_report()
        return
    hybrid = "--hybrid" in args
    strategy = "fixed" if "--fixed" in args else DEFAULT_STRATEGY
    query = " ".join(a for a in args if not a.startswith("--"))
    if not query:
        print('Usage:\n'
              '  python src/retrieve.py --rebuild                        # (re)build the indexes\n'
              '  python src/retrieve.py [--hybrid] [--fixed] "question"  # search')
        return
    _print_hits(query, retrieve(query, hybrid=hybrid, strategy=strategy))


if __name__ == "__main__":
    main()
