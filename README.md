# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Student reviews of CS professors at the New Jersey Institute of Technology (NJIT). Official course descriptions or other university materials don't reflect professor personality, teaching styles, difficulty, etc. Furthermore, the sites that do exist to handle professor reviews, namely Rate My Professors (RMP), often contain tens if not hundreds of reviews, which would be too many to read to try to find an answer to a specific question (e.g. "Does [professor] offer any extra credit?").

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

RMP = Rate My Professors

| #   | Source | Type    | URL or file path |
| --- | ------ | ------- | ---------------- |
| 1   | RMP    | Reviews |                  |
| 2   | RMP    | Reviews |                  |
| 3   | RMP    | Reviews |                  |
| 4   | RMP    | Reviews |                  |
| 5   | RMP    | Reviews |                  |
| 6   | RMP    | Reviews |                  |
| 7   | RMP    | Reviews |                  |
| 8   | RMP    | Reviews |                  |
| 9   | RMP    | Reviews |                  |
| 10  | RMP    | Reviews |                  |

Note: each professor's reviews have their own online page on RMP (easily searchable via Google), but since reviews can be added, changed, or deleted, this project's docs are strictly local to ensure a stable corpus.

- **Origin**: [Rate My Professors](https://www.ratemyprofessors.com/) for NJIT. Ten random professors were selected, each comprising a pair of documents: `professor-overall.txt` (overall ratings) and `professor-reviews.txt` (individual reviews). Each review on RMP is strictly 350 characters or under.
- **Raw Docs**: Manual copy-pastes of all the overall and individual reviews directly from the website. [Example: [andrew-sohn-overall](./documents/raw/andrew-sohn-overall.txt) and [andrew-sohn-reviews.txt](./documents/raw/andrew-sohn-reivews.txt)]
- **Cleaned Docs**:

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
| --- | -------- | --------------- | ---------------------------- | ----------------- | ----------------- |
| 1   |          |                 |                              |                   |                   |
| 2   |          |                 |                              |                   |                   |
| 3   |          |                 |                              |                   |                   |
| 4   |          |                 |                              |                   |                   |
| 5   |          |                 |                              |                   |                   |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_

**Instance 2**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_
