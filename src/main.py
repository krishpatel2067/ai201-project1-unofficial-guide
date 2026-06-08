"""
main.py — Stage 6 + stretch features: Gradio chat interface for The Unofficial Guide.

Wires the full pipeline behind a chat UI:

    question -> [condense w/ history] -> retrieve() -> filter_to_top_file() -> generate_answer()

Includes the spec's debug panel (retrieved chunks, cosine distances, sources) and
toggles for the stretch features: hybrid search, chunking strategy, metadata
filters, and conversational memory.

Run with:  python src/main.py
Then open the local URL it prints (default http://127.0.0.1:7860).
"""

from __future__ import annotations

from datetime import datetime

import gradio as gr

from clean import CLEAN_DIR
from generate import condense_query, generate_answer
from retrieve import filter_to_top_file, retrieve

# Make long lines in the debug code blocks wrap instead of scrolling sideways.
DEBUG_CSS = """
#debug-panel pre, #debug-panel code {
    white-space: pre-wrap !important;
    overflow-wrap: anywhere;
}
"""

# Source-file options for the metadata filters (stretch feature).
SOURCE_FILES = sorted(p.name for p in CLEAN_DIR.glob("*.txt"))


def _format_debug(retrieved: list[dict], used: list[dict],
                  search_query: str | None = None) -> str:
    """Render the retrieved chunks (distances, sources, full text) as markdown,
    flagging which ones survived the single-professor filter and fed the answer.
    ``search_query`` is shown when conversational memory rewrote the question."""
    if not retrieved:
        return "_No chunks retrieved._"
    answer_file = used[0]["metadata"]["source"] if used else "none"
    used_ids = {h["id"] for h in used}
    blocks = []
    if search_query:
        blocks.append(f"**Rewritten search query:** `{search_query}`\n")
    blocks.append(
        f"**Retrieved {len(retrieved)} chunks.** **Answer drawn from `{answer_file}`** "
        f"({len(used)} chunk(s) sent to the LLM).  "
        f"_✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap._"
    )
    for rank, h in enumerate(retrieved, start=1):
        m = h["metadata"]
        if h["id"] in used_ids:
            marker = "  ✅ used"
        elif m["source"] == answer_file:
            marker = "  📄 same file"
        else:
            marker = ""
        dist = f"{h['distance']:.4f}" if h.get("distance") is not None else "n/a"
        rrf = f" · rrf `{h['rrf']:.4f}`" if "rrf" in h else ""
        blocks.append(
            f"\n**#{rank}** · distance `{dist}`{rrf} · source `{m['source']}` "
            f"· {m['type']} · id `{h['id']}`{marker}\n\n"
            f"```\n{h['document']}\n```"
        )
    return "\n".join(blocks)


def _parse_date_input(text: str) -> int | None:
    """Parse a 'YYYY-MM-DD' string into a YYYYMMDD int (or None if blank/invalid)."""
    text = (text or "").strip()
    if not text:
        return None
    try:
        return int(datetime.strptime(text, "%Y-%m-%d").strftime("%Y%m%d"))
    except ValueError:
        return None  # unparseable -> treat as no date filter


def _build_where(source: str, min_rating: float, after_date: str):
    """Assemble a ChromaDB metadata filter from the UI controls (or None).

    Combines any active filters with $and. Applies to semantic search; the rating
    and date filters only match review chunks (overall chunks lack those fields).
    """
    clauses = []
    if source and source != "(any)":
        clauses.append({"source": source})
    if min_rating and min_rating > 0:
        clauses.append({"quality": {"$gte": float(min_rating)}})
    after_num = _parse_date_input(after_date)
    if after_num is not None:
        clauses.append({"date_num": {"$gte": after_num}})  # YYYYMMDD comparison
    if not clauses:
        return None
    return clauses[0] if len(clauses) == 1 else {"$and": clauses}


def chat(message: str, history: list, memory: bool, hybrid: bool, strategy: str,
         source: str, min_rating: float, after_date: str):
    """One chat turn: returns (updated_history, cleared_box, debug_markdown).

    ``history`` is the chatbot's list of chat-message dicts ({"role", "content"}).
    When ``memory`` is on we (1) rewrite the question into a standalone query for
    retrieval and (2) pass the prior turns to the LLM so it can resolve references.
    """
    message = (message or "").strip()
    history = history or []
    if not message:
        return history, "", ""

    # 1. Retrieval query: rewrite the follow-up with history when memory is on.
    search_query = condense_query(history, message) if (memory and history) else message

    # 2. Retrieve + collapse to a single professor.
    where = _build_where(source, min_rating, after_date)
    retrieved = retrieve(search_query, hybrid=hybrid, strategy=strategy, where=where)
    used = filter_to_top_file(retrieved)

    # 3. Generate, passing prior turns only when memory is on.
    try:
        answer = generate_answer(message, used, history=history if memory else None)
    except Exception as exc:  # surface API/key errors in the UI instead of crashing
        answer = f"⚠️ Generation failed: {exc}"

    new_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer},
    ]
    rewritten = search_query if (memory and search_query != message) else None
    return new_history, "", _format_debug(retrieved, used, rewritten)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="The Unofficial Guide") as app:
        gr.Markdown(
            "# The Unofficial Guide\n"
            "Ask about an NJIT CS professor. Answers are grounded only in Rate My "
            "Professors reviews and cite their source file."
        )
        chatbot = gr.Chatbot(label="Conversation", height=420)
        message = gr.Textbox(
            label="Your question",
            placeholder="e.g. Are Professor Kellogg's classes difficult?",
        )
        with gr.Row():
            ask = gr.Button("Ask", variant="primary")
            clear = gr.Button("Clear conversation")

        # --- Stretch-feature toggles ---
        memory = gr.Checkbox(label="Conversational memory (use previous turns)", value=False)
        memory_status = gr.Markdown("Conversational memory: **OFF**")
        hybrid = gr.Checkbox(label="Hybrid search (semantic + BM25 keyword)", value=False)
        strategy = gr.Radio(
            choices=["structured", "fixed"], value="structured",
            label="Chunking strategy (structured = per-review; fixed = 650-char windows)",
        )

        with gr.Accordion("Filters (optional, applied to semantic search)", open=False):
            source = gr.Dropdown(
                choices=["(any)"] + SOURCE_FILES, value="(any)",
                label="Source file (professor)",
            )
            min_rating = gr.Slider(
                0, 5, value=0, step=0.5, label="Minimum review rating (0 = any)",
            )
            after_date = gr.Textbox(
                label="Reviews on or after (YYYY-MM-DD, optional)",
                placeholder="e.g. 2024-01-01",
            )

        with gr.Accordion("Debug — retrieved chunks, distances, and sources", open=False):
            debug = gr.Markdown(elem_id="debug-panel")

        inputs = [message, chatbot, memory, hybrid, strategy, source, min_rating, after_date]
        outputs = [chatbot, message, debug]
        ask.click(chat, inputs=inputs, outputs=outputs)
        message.submit(chat, inputs=inputs, outputs=outputs)
        clear.click(lambda: ([], "", ""), outputs=[chatbot, message, debug])
        # Reflect the memory toggle's state in the UI (spec: "show whether enabled").
        memory.change(
            lambda on: f"Conversational memory: **{'ON' if on else 'OFF'}**",
            inputs=memory, outputs=memory_status,
        )
    return app


def main() -> None:
    build_app().launch(css=DEBUG_CSS)


if __name__ == "__main__":
    main()
