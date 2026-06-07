# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Student reviews of CS professors at the New Jersey Institute of Technology (NJIT). Official course descriptions or other university materials don't reflect professor personality, teaching styles, difficulty, etc. Furthermore, the sites that do exist to handle professor reviews, namely Rate My Professors (RMP), often contain tens if not hundreds of reviews, which would be too many to read to try to find an answer to a specific question (e.g. "Does [professor] offer any extra credit?").

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source | Description                   | URL or location                   |
| --- | ------ | ----------------------------- | --------------------------------- |
| 1   | RMP    | Reviews of Bassel Arafeh      | docs/clean/bassel-arafeh.txt      |
| 2   | RMP    | Reviews of Samaneh Berenjian  | docs/clean/samaneh-berenjian.txt  |
| 3   | RMP    | Reviews of James Calvin       | docs/clean/james-calvin.txt       |
| 4   | RMP    | Reviews of Adrian Ionescu     | docs/clean/adrian-ionescu.txt     |
| 5   | RMP    | Reviews of Abdul-Rahman Itani | docs/clean/abdul-rahman-itani.txt |
| 6   | RMP    | Reviews of Martin Kellogg     | docs/clean/martin-kellogg.txt     |
| 7   | RMP    | Reviews of Kumar Mani         | docs/clean/kumar-mani.txt         |
| 8   | RMP    | Reviews of Kamlesh Naik       | docs/clean/kamlesh-naik.txt       |
| 9   | RMP    | Reviews of Michael Renda      | docs/clean/michael-renda.txt      |
| 10  | RMP    | Reviews of Andrew Sohn        | docs/clean/andrew-sohn.txt        |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunking strategy**: Structure-based chunking

**Chunk size:** Max 1000 characters

**Overlap:** 0 characters

**Reasoning:**

- **Overall Ratings**: RMP overall ratings are strictly structured. For example, each raw overall rating starts with the numeric rating in the first line, contains the professor's full name on Line 4, and ends with a distribution of ratings.
- **Individual Reviews**: RMP reviews are strictly structured, too. Each review body is max 350 characters long. The additional aspects of the review (e.g. rating, tags, upvotes, downvotes) can vary in character length but are still strict in structure. For example, each full raw review (body and additional aspects) can be separated by a blank line and starts with the line "Quality".

The raw docs were used as examples even though those won't be going into the RAG pipeline themselves. But becasue the raw docs themselves have structure, the cleaned docs derieved from then will also have structure.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-va` via `sentence-transformers`

**Top-k:** 5

**Production tradeoff reflection:**

If this project were deployed for real users and cost wasn't a constraint, I would consider opting for a more advanced model that offers more accurate embeddings especially for domain-specific text (vital for edge-case queries in this CS-professor-oriented RAG) and/or multilingual support (necessary for students whose first language isn't English). An example of an offline model satisfying the latter is `EmbeddingGemma (300M)` that can support 100+ languages. A larger context window wouldn't a big priority for this project because student questions about professors tend to be short and direct. One scenario it could be useful is with conversation history, but even then it is reasonable to assume most students wouldn't end up having long chats with the RAG about the same professor.

I would even consider online embedding models, which may be more capable than offline ones and are not constrained by the user's hardware. However, online models often have a small monetary cost based on token use. Plus, moving from offline to online would introduce latency, perhaps slowing down the end-to-end operation. This tradeoff would be acceptable for a better, user-hardware-agnostic model, but it should be offered alongside local models as an option, depending on the user's preferences and needs.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question                                            | Expected answer                                                                                                                               |
| --- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Does Professor Berenjian offer extra credit?        | Yes, Professor Berenjian offers extra credit.                                                                                                 |
| 2   | Does Professor Bassel give good lectures?           | No, Professor Bassel does not give good lectures. Many students find his lectures boring and difficult to understand.                         |
| 3   | Is it a good idea to skip Professor Naik's classes? | No, it is not a good idea to skip Professor Naik's classes as he often puts lecture material on exams and does not fully follow the textbook. |
| 4   | Are Professor Kellogg's classses difficult?         | Yes, Professor Kellogg's classes, especially that on compilers, is difficult and requires a lot of time.                                      |
| 5   | Which professors offer extra credit?                | Some professors that have offered extra credit before are James Calvin, Samaneh Berenjian, Adrian Ionescu, and Andrew Sohn.                   |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The docs may contain roughly an equal number of conflicting reviews and sentiments, throwing the retriever off and leading to a cherry-picked answer. Reviews can vary a lot depending on which student wrote it (e.g. a failed student would tend to exaggerate a professor's negative qualities). A more well-tuned RAG pipeline would handle and express an even split of opinions in the final response, offering nuance necessary to ensure accuracy and reliability.

2. The reviews may include inconsistences in spelling, grammer, punctuation, wording, etc. For instance, the strict 350-character limit may cause students to abbreviate certain words, perhaps creating separate embeddings for abbreviations and full forms. A spelling mistake could render an entire review un-retrievable against a properly spelled user query. An advanced RAG pipeline could use an LLM in the cleaning process to conservatively normalize such inconsistences.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
