# Project Stages

> Working checklist for **The Unofficial Guide** — a RAG over Rate My Professors reviews of
> 10 NJIT CS professors. This file captures the agreed design decisions and the staged plan
> so any agent (or future-you) can pick up without re-deriving context. Check boxes as work
> is completed. Decisions here were agreed during planning; update this file if they change.

---

## Key Design Decisions (read first)

- **Scope:** User queries are about a **single professor** at a time. Queries may be about
  natural-language opinions *or* aggregate stats (overall rating, # of ratings, distribution).
- **Clean docs:** One clean doc per professor at `documents/clean/<name>.txt`, produced by
  merging the `*-overall.txt` + `*-reviews.txt` pair and stripping UI noise
  (`Rate`, `Arrow Icon`, `Compare`, `I'm Professor X`, the standalone `Helpful` button label,
  stray `Reviewed: <date>` lines).
- **Chunking = structure-based.** Per professor:
  - **1 aggregate-stats chunk** (the overall ratings, kept whole).
  - **1 chunk per individual review.**
- **What gets embedded (the Chroma `document` text):**
  - *Review chunk:* `Course: <code>` + review body prose + `Tags: <comma-joined tags>`.
  - *Stats chunk:* a **natural-language rendering** of the overall stats (so semantic search
    can reach numeric questions, e.g. "how many gave the highest rating?").
- **Metadata (Chroma scalars only — `str`/`int`/`float`/`bool`; no lists/None; omit missing keys):**
  - *Review chunk:* `source` (filename, used for citation + filter), `professor`,
    `type="review"`, `quality` (float), `difficulty` (float), `course` (str,
    upper-cased, no spaces), `date_num` (int `YYYYMMDD`), `grade` (str, if present),
    `would_take_again` (bool, if present), `for_credit` (bool),
    `online` (bool, if present), `thumbs_up` (int), `thumbs_down` (int).
  - *Stats chunk:* `source`, `professor`, `type="overall"`, `overall_quality` (float),
    `num_ratings` (int), `would_take_again_pct` (int), `difficulty` (float),
    `dist_5`…`dist_1` (int counts).
  - *Dates:* store `date_num` only; derive any display string with `datetime` at render time.
  - *Tags* live in the embedded text (Chroma can't store lists), not in metadata.
- **Embedding/Retrieval:** `all-MiniLM-L6-v2` via `sentence-transformers`; ChromaDB;
  **cosine distance**; **top-k = 5**; results sorted **ascending by distance** (most relevant first);
  optional distance cutoff.
- **Generation:** Groq `llama-3.3-70b-versatile` with the fixed system prompt in
  `spec/project-req.md`; grounded to retrieved chunks; exactly one citation `[<name>.txt]`.
- **Code layout (`src/`):** `clean.py` (load + clean), `chunk.py` (chunking), `retrieve.py`
  (embed + build store + retrieve), `generate.py` (LLM call + grounding), `main.py`
  (Gradio interface + pipeline wiring).

---

## Stage 0 — Environment & Dependencies
- [ ] Confirm `.venv` has deps from `requirements.txt` (sentence-transformers, chromadb, groq, python-dotenv).
- [ ] Enable `gradio` in `requirements.txt` (currently commented) for the interface.
- [ ] Add `rank-bm25` (or chosen lib) for the hybrid-search stretch feature.
- [ ] Confirm `GROQ_API_KEY` is set in `.env` (not committed).

## Stage 1 — Document Ingestion & Cleaning  (`src/clean.py`)  [Milestone 3]
- [x] Load each `*-overall.txt` / `*-reviews.txt` pair from `documents/raw/`.
- [x] Parse + clean the **overall** doc: extract rating, # ratings, would-take-again %,
      difficulty, and the rating distribution; strip UI noise.
- [x] Parse + clean the **reviews** doc: split into review blocks (each starting with
      `Quality`); extract per-review fields, body, and tags; strip noise.
- [x] Normalize dates (strip ordinal suffixes) to a clean, parseable form; the `YYYYMMDD`
      int is derived in Stage 2.
- [x] Write one merged, chunk-ready clean doc per professor to `documents/clean/<name>.txt`
      (includes a `Professor:` header line for downstream metadata).
- [x] **Verify:** human line-by-line review of clean docs against raw (user-driven).

## Stage 2 — Chunking  (`src/chunk.py`)  [Milestone 3]
- [ ] From each clean doc, build **1 stats chunk + N review chunks** per the design above.
- [ ] For each chunk, assemble the embedded `document` text and the `metadata` dict.
- [ ] Assign stable unique `id`s.
- [ ] **Verify:** print a few chunks (text + metadata) to console for review.

## Stage 3 — Embedding & Vector Store  (`src/retrieve.py`)  [Milestone 4]
- [ ] `build_index()`: embed all chunks with `all-MiniLM-L6-v2` and add to a ChromaDB
      collection configured for **cosine** distance, with metadata attached. (Run once.)
- [ ] **Verify:** collection count matches total chunk count.

## Stage 4 — Retrieval  (`src/retrieve.py`)  [Milestone 4]
- [ ] `retrieve(query, k=5)`: semantic search, return chunks sorted ascending by distance.
- [ ] Optional distance cutoff to drop weak matches.
- [ ] **Verify:** run sample queries, inspect retrieved chunks + distances + sources.

## Stage 5 — Grounded Generation  (`src/generate.py`)  [Milestone 5]
- [ ] Format retrieved chunks (with source filenames) into the LLM context.
- [ ] Call Groq `llama-3.3-70b-versatile` with the fixed system prompt.
- [ ] Enforce grounding: refusal string when unsupported; single `[<name>.txt]` citation.
- [ ] **Verify:** answers are grounded + correctly cited; refusals fire when expected.

## Stage 6 — Query Interface  (`src/main.py`)  [Milestone 5]
- [ ] Gradio chat UI wiring ingest → retrieve → generate.
- [ ] Debug panel: retrieved chunks in full, cosine distances, source files.
- [ ] **Verify:** end-to-end run of the 5 eval questions from `planning.md`.

## Stage 7 — Stretch Features (all planned — see `spec/project-req.md`)
- [ ] **Hybrid search:** semantic + BM25 keyword; UI toggle vs semantic-only; compare results.
- [ ] **Chunking toggle:** structure-based (default) vs fixed-size (500–750 chars, 50–100 overlap).
- [ ] **Metadata filtering:** filter by source filename, date, and rating; combinable filters.
- [ ] **Conversational memory:** multi-turn context; home-page toggle; chat shows enabled state.

## Stage 8 — Evaluation & Write-up
- [ ] Run the 5 eval questions; record retrieval quality + response accuracy.
- [ ] Identify ≥1 failure case with root cause tied to a pipeline stage.
- [ ] (User writes the graded `README.md` / `planning.md` sections — agent assists/advises only.)
