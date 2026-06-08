"""
generate.py — Stage 5: Grounded Response Generation.

Takes a user query plus the chunks retrieved in Stage 4 and asks the Groq LLM
(llama-3.3-70b-versatile) to answer using ONLY those chunks, citing a single
source file. The grounding rules live in SYSTEM_PROMPT, copied verbatim from
spec/project-req.md — do NOT paraphrase it; the exact wording is the spec.

Run with:  python src/generate.py "your question here"
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from groq import Groq

from clean import PROJECT_ROOT

# Load GROQ_API_KEY from the project-root .env (which is git-ignored).
load_dotenv(PROJECT_ROOT / ".env")

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a Q/A assistant answering college students' questions about CS professors at the New Jersey Institute of Technology. You will be given a user query along with a few chunks of text as sources. Decide which chunk(s) is/are the most relevant to the user query and generate a concise response (1-3 sentences) using only the chunks provided. If the relevant chunks from one file disagree (e.g. some students found a professor easy and others hard), reflect that disagreement rather than presenting only one side.

Do NOT use information outside of the provided chunks. Do NOT use any prior knowledge about these professors. If the answer to the user's query doesn't appear in the provided chunks, do NOT guess or fill in the gaps. Instead, reply with exactly "I can't find the answer to that question." and do NOT include any citation or source when you give that response.

If you are able to answer the user query, you must cite exactly one source using the name of the file that your chosen chunks come from. Each chunk is labeled with the source file it came from. Use that file name for the citation. Each citation must follow the format "[file-name.extension]" (e.g. "[james-calvin.txt]") and must be placed all the way at the end of your response. However, if you cannot find the answer, do NOT include a citation at all.

"Tags:" are short labels attached to a review (e.g. "Lecture heavy"). They are NOT part of the actual review body."""


def _format_context(hits: list[dict]) -> str:
    """Render retrieved chunks into the source block the LLM sees.

    Each chunk is labeled with its source filename so the model can produce the
    [filename] citation. (Chunks are pre-filtered to a single file upstream by
    filter_to_top_file, so they all share one source.)
    """
    blocks = []
    for i, h in enumerate(hits, start=1):
        source = h["metadata"]["source"]
        blocks.append(f"Chunk {i} (source file: {source}):\n{h['document']}")
    return "\n\n".join(blocks)


def filter_to_top_file(hits: list[dict]) -> list[dict]:
    """Keep only the chunks from the top-ranked hit's source file.

    Retrieval returns the top-k across ALL professors, but a single-professor
    answer must draw from one file. Since hits are sorted by ascending distance,
    the #1 hit's file is the best-matching professor; we drop chunks from any
    other file before generation. This structurally guarantees the one-file /
    one-citation rule instead of relying on the LLM to obey it.
    """
    if not hits:
        return hits
    top_source = hits[0]["metadata"]["source"]
    return [h for h in hits if h["metadata"]["source"] == top_source]


def generate_answer(query: str, hits: list[dict]) -> str:
    """Call the Groq LLM to answer ``query``, grounded only in ``hits``."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(free at https://console.groq.com)."
        )
    client = Groq(api_key=api_key)

    user_message = f"User query: {query}\n\nSources:\n{_format_context(hits)}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        # Low temperature keeps the answer faithful to the sources and reduces
        # run-to-run variance — what we want for grounded Q/A, not creativity.
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python src/generate.py "your question here"')
        return

    # Imported here so that merely importing generate.py (e.g. from main.py)
    # doesn't eagerly load the embedding model that retrieve.py pulls in.
    from retrieve import retrieve

    query = " ".join(sys.argv[1:])
    retrieved = retrieve(query)
    used = filter_to_top_file(retrieved)
    answer = generate_answer(query, used)

    print(f"\nQuery: {query!r}\n")
    print("Answer:")
    print(answer)
    # Debug: what semantic search returned (across files) vs. the single file the
    # answer was actually drawn from after filtering to the top hit's source.
    retrieved_sources = sorted({h["metadata"]["source"] for h in retrieved})
    answer_file = used[0]["metadata"]["source"] if used else "none"
    print(
        f"\n(Debug: retrieved {len(retrieved)} chunks spanning "
        f"{len(retrieved_sources)} file(s): {', '.join(retrieved_sources)}.\n"
        f" Answer drawn from {answer_file} ({len(used)} chunk(s)).)"
    )


if __name__ == "__main__":
    main()
