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


# Used by conversational memory: rewrite a follow-up into a standalone query so
# retrieval (which has no memory) still finds the right professor.
CONDENSE_SYSTEM_PROMPT = """You rewrite a student's follow-up question into a standalone question for searching a database of NJIT CS professor reviews.

Given the conversation so far and the latest question, rewrite the latest question so it is fully self-contained: resolve pronouns and references (e.g. "he", "she", "that class") by inserting the specific professor or course named earlier in the conversation. If the latest question is already self-contained, return it unchanged.

Output ONLY the rewritten question — no preamble, explanation, or quotation marks."""


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


def generate_answer(query: str, hits: list[dict], history: list | None = None) -> str:
    """Call the Groq LLM to answer ``query``, grounded only in ``hits``.

    ``history`` (optional) is a list of prior chat messages ({"role", "content"}
    dicts, the Gradio chatbot format). When given, they're spliced in as prior
    messages so the model can resolve references like "he"/"that class" — i.e.
    conversational memory. The grounding rules still apply to the current ``hits``.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(free at https://console.groq.com)."
        )
    client = Groq(api_key=api_key)

    # history is in Gradio chat-message format, which can carry extra keys
    # (metadata/options) that the Groq API rejects — keep only role + content.
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(
        {"role": m["role"], "content": m["content"]} for m in (history or [])
    )
    messages.append(
        {
            "role": "user",
            "content": f"User query: {query}\n\nSources:\n{_format_context(hits)}",
        }
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        # Low temperature keeps the answer faithful to the sources and reduces
        # run-to-run variance — what we want for grounded Q/A, not creativity.
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def condense_query(history: list, question: str) -> str:
    """Rewrite a follow-up ``question`` into a standalone search query using the
    conversation ``history``.

    ``history`` is a list of prior chat messages ({"role", "content"} dicts).
    Returns ``question`` unchanged when there's no history to resolve. This is a
    cheap extra LLM call (same Groq client/key, deterministic) so that follow-ups
    like "does he offer extra credit?" retrieve against the right professor.
    """
    if not history:
        return question
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return question  # no key -> can't condense; fall back to the raw question
    client = Groq(api_key=api_key)
    convo = "\n".join(
        f"{'Student' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in history
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": CONDENSE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Conversation so far:\n{convo}\n\nLatest question: {question}",
            },
        ],
        temperature=0.0,  # deterministic rewrite
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    from main import build_where
    from retrieve import get_parser, print_hits, filter_to_top_file, retrieve

    parser = get_parser(desc="Generation CLI parsing")
    parser.add_argument(
        "--show-retrieved",
        action="store_true",
        help="Show all the retrieved chunks passed to the LLM",
    )
    args = parser.parse_args()
    query = args.query
    hybrid = args.hybrid
    strategy = "fixed" if args.fixed else "structured"

    where = build_where(
        source=args.src,
        min_rating=args.min_rating,
        after_date=(args.start_date and args.start_date.isoformat()),
    )
    retrieved = retrieve(query, hybrid=hybrid, strategy=strategy, where=where)
    used = filter_to_top_file(retrieved)
    answer = generate_answer(query, used)

    print(f"\nQuery: {query!r}  (hybrid={hybrid}, strategy={strategy})\n")
    print("Answer:")
    print(answer)

    if args.show_retrieved:
        print_hits(query, retrieved, filter_to_top_file(retrieved))
    else:
        # Short debug: what search returned (across files) vs. the single file the answer
        # was actually drawn from after filtering to the top hit's source.
        retrieved_sources = sorted({h["metadata"]["source"] for h in retrieved})
        answer_file = used[0]["metadata"]["source"] if used else "none"
        print(
            f"\n(Debug: retrieved {len(retrieved)} chunks spanning "
            f"{len(retrieved_sources)} file(s): {', '.join(retrieved_sources)}.\n"
            f" Answer drawn from {answer_file} ({len(used)} chunk(s)).)"
        )


if __name__ == "__main__":
    main()
