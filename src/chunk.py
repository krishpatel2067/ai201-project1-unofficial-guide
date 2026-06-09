"""
chunk.py — Stage 2: Chunking for The Unofficial Guide.

Reads the clean docs produced by ``clean.py`` (``documents/clean/<slug>.txt``)
and turns each one into the atomic units we will embed and search over:

    * 1 "overall" chunk per professor  -> the aggregate-stats summary
    * 1 "review" chunk per individual review

Each chunk is a dict with three parts, mirroring how it will be stored in
ChromaDB later:

    {
        "id":       "<unique string>",
        "document": "<the text that gets embedded>",
        "metadata": {<structured, filterable fields — never embedded>},
    }

The document/metadata split is the whole point of this stage: prose and concise
meaning (review body + tags + course) go into ``document`` so semantic search
can match them, while numbers/dates/flags go into ``metadata`` so they can be
displayed and filtered without polluting the embedding.

(Note: this module shadows Python's deprecated stdlib ``chunk`` module. That's
harmless here — we never import the stdlib one.)

Run with:  python src/chunk.py
"""

from __future__ import annotations

import random
import re
import sys
from datetime import datetime

# Reuse the path constants from clean.py so the pipeline stays in sync.
from clean import CLEAN_DIR

# --- Clean-doc parsing -------------------------------------------------------
# chunk.py treats the clean docs as its input "contract": it re-parses the
# structured text clean.py wrote. Keeping stages decoupled through a persisted
# artifact (rather than sharing in-memory objects) mirrors how real indexing
# pipelines hand off between steps.


def parse_clean_doc(text: str) -> tuple[dict, list[dict]]:
    """Split a clean doc into (overall stats dict, list of review dicts)."""
    overall_block, _, reviews_block = text.partition("=== REVIEWS ===")
    return _parse_overall(overall_block), _parse_reviews(reviews_block)


def _key_values(block: str) -> dict[str, str]:
    """Turn 'Key: value' lines into a dict, skipping separators/blanks.

    Partitions on the *first* colon only, so values that themselves contain a
    colon (e.g. a review body) stay intact.
    """
    kv: dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("===") or line.startswith("---"):
            continue
        key, sep, value = line.partition(":")
        if sep:
            kv[key.strip()] = value.strip()
    return kv


def _parse_overall(block: str) -> dict:
    kv = _key_values(block)
    quality, num_ratings = re.match(
        r"([\d.]+)/5 \(based on (\d+) ratings\)", kv["Overall Quality"]
    ).groups()
    distribution = {
        int(star): int(count)
        for star, count in re.findall(r"\((\d)\): (\d+)", kv["Rating Distribution"])
    }
    return {
        "professor": kv["Professor"],
        "overall_quality": float(quality),
        "num_ratings": int(num_ratings),
        "would_take_again_pct": int(kv["Would Take Again"].rstrip("%")),
        "difficulty": float(kv["Level of Difficulty"]),
        "distribution": distribution,
    }


def _parse_reviews(block: str) -> list[dict]:
    """Split the reviews block on the '--- Review N ---' markers and parse each."""
    parts = re.split(r"--- Review \d+ ---", block)
    return [_key_values(part) for part in parts if part.strip()]


# --- Chunk construction ------------------------------------------------------
def _date_to_num(date_str: str) -> int:
    """'Apr 21, 2026' -> 20260421 (a sortable, range-filterable int)."""
    return int(datetime.strptime(date_str, "%b %d, %Y").strftime("%Y%m%d"))


def _overall_chunk(slug: str, overall: dict) -> dict:
    """Build the aggregate-stats chunk for one professor.

    The document is a *natural-language rendering* of the stats so that a
    semantic query like "how many gave the highest rating?" has a chance to
    match — embeddings handle meaning, not raw tables.
    """
    prof = overall["professor"]
    d = overall["distribution"]
    document = (
        f"Overall quality rating: {overall['overall_quality']} out of 5, "
        f"based on {overall['num_ratings']} ratings.\n"
        f"{overall['would_take_again_pct']}% of students would take {prof} again.\n"
        f"Average level of difficulty: {overall['difficulty']} out of 5.\n"
        f"Rating distribution: {d.get(5, 0)} students rated Awesome (5 stars), "
        f"{d.get(4, 0)} Great (4 stars), {d.get(3, 0)} Good (3 stars), "
        f"{d.get(2, 0)} OK (2 stars), {d.get(1, 0)} Awful (1 star)."
    )
    metadata = {
        "source": f"{slug}.txt",
        "professor": prof,
        "type": "overall",
        "overall_quality": overall["overall_quality"],
        "num_ratings": overall["num_ratings"],
        "would_take_again_pct": overall["would_take_again_pct"],
        "difficulty": overall["difficulty"],
        "dist_5": d.get(5, 0),
        "dist_4": d.get(4, 0),
        "dist_3": d.get(3, 0),
        "dist_2": d.get(2, 0),
        "dist_1": d.get(1, 0),
    }
    return {"id": f"{slug}-overall", "document": document, "metadata": metadata}


def _review_chunk(slug: str, professor: str, n: int, kv: dict) -> dict:
    """Build one review chunk: embed course + body + tags; everything else
    structured/numeric becomes metadata."""
    course = kv["Course"]
    body = kv.get("Review", "")
    tags = kv.get("Tags", "")

    # Embedded text: course code + opinion prose + tag words.
    doc_lines = [f"Course: {course}"]
    if body:
        doc_lines.append(body)
    if tags:
        doc_lines.append(f"Tags: {tags}")
    document = "\n".join(doc_lines)

    # Always-present, scalar metadata.
    metadata = {
        "source": f"{slug}.txt",
        "professor": professor,
        "type": "review",
        "quality": float(kv["Quality"]),
        "difficulty": float(kv["Difficulty"]),
        "course": course,
        "date_num": _date_to_num(kv["Date"]),
        "thumbs_up": int(kv.get("Thumbs Up", 0)),
        "thumbs_down": int(kv.get("Thumbs Down", 0)),
    }
    # Optional fields — only add when present (ChromaDB rejects None values).
    if "For Credit" in kv:
        metadata["for_credit"] = kv["For Credit"].lower() == "yes"
    if "Would Take Again" in kv:
        metadata["would_take_again"] = kv["Would Take Again"].lower() == "yes"
    if "Online Class" in kv:
        metadata["online"] = kv["Online Class"].lower() == "yes"
    if kv.get("Grade"):
        metadata["grade"] = kv["Grade"]

    return {"id": f"{slug}-review-{n}", "document": document, "metadata": metadata}


def build_all_chunks() -> list[dict]:
    """Build every chunk across all clean docs. This is the function the Stage 3
    indexer (``retrieve.build_index``) will import and feed to ChromaDB."""
    chunks: list[dict] = []
    for path in sorted(CLEAN_DIR.glob("*.txt")):
        slug = path.stem
        overall, reviews = parse_clean_doc(path.read_text(encoding="utf-8"))
        chunks.append(_overall_chunk(slug, overall))
        for n, kv in enumerate(reviews, start=1):
            chunks.append(_review_chunk(slug, overall["professor"], n, kv))
    return chunks


# --- Stretch feature: fixed-size chunking -----------------------------------
# An alternative to structure-based chunking: slice each clean doc into
# overlapping fixed-length character windows, ignoring review boundaries. This
# is the naive baseline the interface toggles against. Fixed chunks carry only
# source/professor metadata (a window can straddle several reviews, so per-review
# fields like quality/date don't apply).
FIXED_CHUNK_SIZE = 650  # characters per window (within the 500-750 spec)
FIXED_OVERLAP = 75  # characters shared between consecutive windows


def build_all_chunks_fixed() -> list[dict]:
    """Build fixed-size, overlapping character-window chunks from the clean docs."""
    step = FIXED_CHUNK_SIZE - FIXED_OVERLAP
    chunks: list[dict] = []
    for path in sorted(CLEAN_DIR.glob("*.txt")):
        slug = path.stem
        text = path.read_text(encoding="utf-8")
        name_match = re.search(r"^Professor:\s*(.+)$", text, re.MULTILINE)
        professor = name_match.group(1).strip() if name_match else slug
        n = 0
        for start in range(0, len(text), step):
            window = text[start : start + FIXED_CHUNK_SIZE].strip()
            if not window:
                continue
            n += 1
            chunks.append(
                {
                    "id": f"{slug}-fixed-{n}",
                    "document": window,
                    "metadata": {
                        "source": f"{slug}.txt",
                        "professor": professor,
                        "type": "fixed",
                    },
                }
            )
    return chunks


def build_chunks(strategy: str = "structured") -> list[dict]:
    """Dispatch to the chosen chunking strategy: 'structured' (default) or 'fixed'."""
    return build_all_chunks_fixed() if strategy == "fixed" else build_all_chunks()


# --- Driver / sanity check ---------------------------------------------------
def main() -> None:
    args = sys.argv[1:]
    if "--help" in args:
        print("Usage: python src/chunk.py [--fixed]")
        return

    strategy = "fixed" if "--fixed" in args else "structured"

    # If using structured chunking, print one random chunk of each kind so repeated runs
    # surface different professors/reviews to eyeball the document/metadata split broadly.
    if strategy == "fixed":
        chunks = build_all_chunks_fixed()
        n_overall = 0
        n_review = sum(1 for _ in chunks)
        sample_overall = None
        sample_review = random.choice([c for c in chunks])
    else:
        chunks = build_all_chunks()
        n_overall = sum(c["metadata"]["type"] == "overall" for c in chunks)
        n_review = sum(c["metadata"]["type"] == "review" for c in chunks)
        sample_overall = random.choice(
            [c for c in chunks if c["metadata"]["type"] == "overall"]
        )
        sample_review = random.choice(
            [c for c in chunks if c["metadata"]["type"] == "review"]
        )

    print(f"Built {len(chunks)} chunks: {n_overall} overall + {n_review} reviews\n")

    for label, c in [("OVERALL", sample_overall), ("REVIEW", sample_review)]:
        if not c:
            continue
        print(f"===== SAMPLE {label} CHUNK: {c['id']} =====")
        print("--- document (embedded text) ---")
        print(c["document"])
        print("--- metadata ---")
        for k, v in c["metadata"].items():
            print(f"  {k}: {v!r}")
        print()


if __name__ == "__main__":
    main()
