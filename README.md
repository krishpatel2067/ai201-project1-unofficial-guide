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

| #   | Source | Type    | URL or file path                      |
| --- | ------ | ------- | ------------------------------------- |
| 1   | RMP    | Reviews | documents/clean/bassel-arafeh.txt     |
| 2   | RMP    | Reviews | documents/clean/samaneh-berenjian.txt |
| 3   | RMP    | Reviews | documents/clean/james-calvin.txt      |
| 4   | RMP    | Reviews | documents/clean/abdul-rahman-itani    |
| 5   | RMP    | Reviews | documents/clean/martin-kellogg.txt    |
| 6   | RMP    | Reviews | documents/clean/kumar-mani.txt        |
| 7   | RMP    | Reviews | documents/clean/kamlesh-naik.txt      |
| 8   | RMP    | Reviews | documents/clean/marvin-nakayama.txt   |
| 9   | RMP    | Reviews | documents/clean/michael-renda.txt     |
| 10  | RMP    | Reviews | documents/clean/andrew-sohn.txt       |

Note: each professor's reviews have their own online page on RMP (easily searchable via Google), but since reviews can be added, changed, or deleted, this project's docs are strictly local to ensure a stable corpus.

- **Origin**: [Rate My Professors](https://www.ratemyprofessors.com/) for NJIT. Ten random professors were selected, each comprising a pair of documents: `professor-overall.txt` (overall ratings) and `professor-reviews.txt` (individual reviews). Each review on RMP is strictly 350 characters or under.
- **Raw Docs** (`documents/raw/`): Manual copy-pastes of all the overall and individual reviews directly from the website. [Example: [andrew-sohn-overall.txt](./documents/raw/andrew-sohn-overall.txt) and [andrew-sohn-reviews.txt](./documents/raw/andrew-sohn-reivews.txt)]
- **Clean Docs** (`documents/clean/`): Structured versions of the raw docs, combining the overall stats and reviews into one file. [Example: [andrew-sohn.txt](./documents//clean/andrew-sohn.txt)]

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunking strategy**: Document structure-based chunking

**Chunk size:** N/A (document structure)

**Overlap:** 0 (none needed due to strict, consistent structure)

**Why these choices fit your documents:** Raw RMP reviews are highly structured to begin with. Cleaning the raw docs further solidifies a structure that can easily be chunked accordingly without having to resort to estimated character counts (though it is good to know that RMP reviews are capped at 350 characters).

**Final chunk count:** 759 (10 overall, one for each proffesor + 749 reviews)

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` because it is lightweight and on-device, suitable for project purposes.

**Production tradeoff reflection:**

If this project were deployed for real users and cost wasn't a constraint, I would consider opting for a more advanced model that offers more accurate embeddings especially for domain-specific text (vital for edge-case queries in this CS-professor-oriented RAG) and/or multilingual support (necessary for students whose first language isn't English). An example of an offline model satisfying the latter is `EmbeddingGemma (300M)` that can support 100+ languages. A larger context window wouldn't a big priority for this project because student questions about professors tend to be short and direct. One scenario it could be useful is with conversation history, but even then it is reasonable to assume most students wouldn't end up having long chats with the RAG about the same professor.

I would even consider online embedding models, which may be more capable than offline ones and are not constrained by the user's hardware. However, online models often have a small monetary cost based on token use. Plus, moving from offline to online would introduce latency, perhaps slowing down the end-to-end operation. This tradeoff would be acceptable for a better, user-hardware-agnostic model, but it should be offered alongside local models as an option, depending on the user's preferences and needs.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

```
You are a Q/A assistant answering college students' questions about CS professors at the New Jersey Institute of Technology. You will be given a user query along with a few chunks of text as sources. Decide which chunk(s) is/are the most relevant to the user query and generate a concise response (1-3 sentences) using only the chunks provided. If the relevant chunks from one file disagree (e.g. some students found a professor easy and others hard), reflect that disagreement rather than presenting only one side.

Do NOT use information outside of the provided chunks. Do NOT use any prior knowledge about these professors. If the answer to the user's query doesn't appear in the provided chunks, do NOT guess or fill in the gaps. Instead, reply with exactly "I can't find the answer to that question." and do NOT include any citation or source when you give that response.

If you are able to answer the user query, you must cite exactly one source using the name of the file that your chosen chunks come from. Each chunk is labeled with the source file it came from. Use that file name for the citation. Each citation must follow the format "[file-name.extension]" (e.g. "[james-calvin.txt]") and must be placed all the way at the end of your response. However, if you cannot find the answer, do NOT include a citation at all.

"Tags:" are short labels attached to a review (e.g. "Lecture heavy"). They are NOT part of the actual review body.
```

**How source attribution is surfaced in the response:**

The source attribution is added to the end of an answer. If the model cannot answer (due to low relevance), then the source attribution is simply omitted.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question                                            | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
| --- | --------------------------------------------------- | --------------- | ---------------------------- | ----------------- | ----------------- |
| 1   | Does professor Berenjian offer extra credit?        | [1]             | [6]                          |                   |                   |
| 2   | Are Professor Kellogg's classes difficult?          | [2]             | [7]                          |                   |                   |
| 3   | Is it a good idea to skip Professor Naik's classes? | [3]             | [8]                          |                   |                   |
| 4   | Does Professor Bassel give good lectures?           | [4]             | [9]                          |                   |                   |
| 5   | Which professors offer extra credit?                | [5]             | [10]                         |                   |                   |

Expected answers:

1. Yes, Professor Berenjian offers extra credit.
2. Yes, Professor Kellogg's classes, especially that on compilers, is difficult and requires a lot of time.
3. No, it is not a good idea to skip Professor Naik's classes as he often puts lecture material on exams and does not fully follow the textbook.
4. No, Professor Bassel does not give good lectures. Many students find his lectures boring and difficult to understand.
5. Some professors that have offered extra credit before are James Calvin, Samaneh Berenjian, and Andrew Sohn.

System response:

6.
7.

```
Professor Kellogg's class, CS485, is considered challenging, requiring a significant amount of time and effort, but it is also a very rewarding experience. Students can expect to learn a lot, despite the class being demanding. [martin-kellogg.txt]
```

8.

```
It's not a good idea to skip Professor Naik's classes, as multiple students have advised against it, warning that skipping class will make it harder to pass. According to the students, attending classes and doing the homework makes things easier, and Professor Naik is transparent about what will be on the exams. [kamlesh-naik.txt]
```

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

## BM25 Keyword-Matching vs Semantic Only

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

From the beginning, I knew I wanted to include all the stretch features in the project. By including this intention in the spec, my Claude Code was able to implement the various stages of the pipeline in a way that allowed these stretch features to be added later easily. For example, \_\_\_\_.

**One way your implementation diverged from the spec, and why:**

I originally wanted the LLM to

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

- _What I gave the AI:_ I asked the AI to create a cleaning and ingestion script to convert raw docs into clean docs and ingest / chunk the docs.
- _What it produced:_ it created `ingest.py` initially with the code to clean the raw docs. However, it was much longer than I had anticipated.
- _What I changed or overrode:_ Thus, I asked it to split the cleaning and chunking code into two separate files: `clean.py` and `chunk.py` to keep the functions seperate and the files short.

**Instance 2**

- _What I gave the AI:_ I asked the AI to store as much metadata as possible about each reivew, which could be useful for future filtering features.
- _What it produced:_ It did what I asked, but it also curiously added a `date_num` (e.g. 20260421) and `date_str` ("Apr 21st, 2026") field for review dates - a duplication that didn't exist for any other metadata field.
- _What I changed or overrode:_ I asked it to only keep `date_num` since the `date_str` could be derived from the former in the UI anyway, so storing both seemed redundnat.

## Notes

- Aggregate stats kept as a chunk with N other reivew chunks.
- Aggregate stats often require a separate classifer that route to structured lookups - regular semantic search isn't good with numbers.
- Embedded data vs metadata split:
  - Review metadata: source, professor, type, quality, difficulty, course, date_num, grade?, would_take_again?, online?, for_credit, thumbs_up, thumbs_down
  - Stats metadata:
- AI use: Asked it to create cleaning and ingestion in one script, created ingest.py with cleaning, but I changed it to clean.py
- AI use: asked it to store all reivew metadata, it stored date_num and date_str, I said to only keep date_num
- AI use: `"extra credit": "EXTRA CREDIT"` -> `"extra credit": "Extra Credit"` in `clean.py`
- Failure: Berenjian extra credit -> none of the 5 results contained extra credit even tho tags existed -> a few tags only diluted in dense embedding -> need BM25
- Spec diverge: orig plan - have LLM choose from one professor's reviews - unreliable -> manual filtering to only matching source sof top result
