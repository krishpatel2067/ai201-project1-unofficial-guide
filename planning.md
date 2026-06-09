# Project 1 Planning: The Unofficial Guide

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Student reviews of CS professors at the New Jersey Institute of Technology (NJIT). Official course descriptions or other university materials don't reflect professor personality, teaching styles, difficulty, etc. Furthermore, the sites that do exist to handle professor reviews, namely Rate My Professors (RMP), often contain tens if not hundreds of reviews, which would be too many to read to try to find an answer to a specific question (e.g. "Does [professor] offer any extra credit?").

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source | Description                                       | URL or location                          |
| --- | ------ | ------------------------------------------------- | ---------------------------------------- |
| 1   | RMP    | Overall ratings and reviews of Bassel Arafeh      | `documents/clean/bassel-arafeh.txt`      |
| 2   | RMP    | Overall ratings and reviews of Samaneh Berenjian  | `documents/clean/samaneh-berenjian.txt`  |
| 3   | RMP    | Overall ratings and reviews of James Calvin       | `documents/clean/james-calvin.txt`       |
| 4   | RMP    | Overall ratings and reviews of Abdul-Rahman Itani | `documents/clean/abdul-rahman-itani`.txt |
| 5   | RMP    | Overall ratings and reviews of Martin Kellogg     | `documents/clean/martin-kellogg.txt`     |
| 6   | RMP    | Overall ratings and reviews of Kumar Mani         | `documents/clean/kumar-mani.txt`         |
| 7   | RMP    | Overall ratings and reviews of Kamlesh Naik       | `documents/clean/kamlesh-naik.txt`       |
| 8   | RMP    | Overall ratings and reviews of Marvin Nakayama    | `documents/clean/marvin-nakayama.txt`    |
| 9   | RMP    | Overall ratings and reviews of Michael Renda      | `documents/clean/michael-renda.txt`      |
| 10  | RMP    | Overall ratings and reviews of Andrew Sohn        | `documents/clean/andrew-sohn.txt`        |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

This project will allow users to toggle between structure-based chunking (default) and fixed size chunking.

### Structure-based Chunking

**Chunk size:** Max 1000 characters

**Overlap:** 0 characters

**Reasoning:**

- **Overall Ratings**: RMP overall ratings are strictly structured. For example, each raw overall rating starts with the numeric rating in the first line, contains the professor's full name on Line 4, and ends with a distribution of ratings.
- **Individual Reviews**: RMP reviews are strictly structured, too. Each review body is max 350 characters long. The additional aspects of the review (e.g. rating, tags, upvotes, downvotes) can vary in character length but are still strict in structure. For example, each full raw review (body and additional aspects) can be separated by a blank line and starts with the line "Quality".

The raw docs were used as examples even though those won't be going into the RAG pipeline themselves. But because the raw docs themselves have structure, the cleaned docs derieved from then will also have structure.

### Fixed Size Chunking

The overall chunk from structured chunking is instead written continuously with the other review chunks in fixed chunking. Also unlike structured chunking, fixed chunking only allows for much metadata to be reliably extracted and stored: namely the source file itself and the professor name.

**Chunk size**: 650 characters (350 max words per review body + review info such as date, upvotes, etc.)

**Overlap**: 75 characters

**Reasoning:** RMP review bodies are capped at 350 characters, giving a stable starting value for chunk size. The metadata (review date, tags, upvotes, etc.) may vary in length, but from eyeballing the docs, they generally don't exceed 300-400 characters. Thus, the final chunk size reflects this: 350 + 300 = 650. The overlap of 75 is chosen to ensure that if a review get cut off, there is a good chance that it is wholly intact in the next chunk.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Top-k:** 10 (cap to 5 after single-file filtering)

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
| 5   | Which professors offer extra credit?                | Some professors that have offered extra credit before are James Calvin, Samaneh Berenjian, and Andrew Sohn.                                   |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The docs may contain roughly an equal number of conflicting reviews and sentiments, throwing the retriever off and leading to a cherry-picked answer. Reviews can vary a lot depending on which student wrote it (e.g. a failed student would tend to exaggerate a professor's negative qualities). A more well-tuned RAG pipeline would handle and express an even split of opinions in the final response, offering nuance necessary to ensure accuracy and reliability.

2. The reviews may include inconsistences in spelling, grammar, punctuation, wording, etc. For instance, the strict 350-character limit may cause students to abbreviate certain words, perhaps creating separate embeddings for abbreviations and full forms. A spelling mistake could render an entire review un-retrievable against a properly spelled user query. An advanced RAG pipeline could use an LLM in the cleaning process to conservatively normalize such inconsistences.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
      Document Ingestion         (clean raw docs; vanilla Python)
             V
          Chunking               (structure-based or fixed size; store metadata; vanilla Python)
             V
   Embedding + Vector Store      (all-MiniLM-L6-v2 via sentence transform + ChromaDB; both offline)
             V
         Retrieval               (semantic-only or hybrid; top-10, filter to single-file - keep max 5; vanilla Python)
             V
        Generation               (Groq: llama-3.3-70b-versatile; API-based)
```

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

I will give Claude Code access to my `documents/raw/` directory as well as my Documents section in this file so that it can learn the raw doc format and produce the correct code to create clean docs from raw docs. I'll manually read line-by-line to verify that the code matches my expectations and that the clean docs follow a clean format that can be easily chunked.

I will use Claude Code again in the chunking stage, surfacing the human-reviewed clean docs and Chunking Strategy section of this file. I will verify that my plan is sound and that I understand everything before continuing. I expect it to produce correct and well-structured code to chunk the docs based on the strategy given in the Chunking Strategy section. I'll confirm that the chunks match my spec via line-by-line code reivew and by printing a few chunks to the console.

**Milestone 4 — Embedding and retrieval:**

I will give Claude Code info from my Retrieval Approach section of this file and surface my intended tech stack (namely `all-MiniLM-L6-v2` via `sentence transformer` for embedding). I will use the AI tool to pressure-test my decisions and assumptions, verifying that everything is sound before moving on. I expect it to produce clean and correct Python code to embed the chunks and retrieve them as per my spec. On top of the usual line-by-line code review, I will verify the retrieval works by inputting a few queries and seeing the list of retrieved chunks.

**Milestone 5 — Generation and interface:**

I will give Claude code info from my `spec/` directory that has more detailed info on the generation phase (namely the system prompt and grounding requirements) and the interface. I expect it to generate accurate and readable code to call the LLM with the retrieved chunks and show the output on the interface that it will create as per my spec in the aforementioned directory. I will verify the code it generated line-by-line and use the interface to test the end-to-end experience, including the RAG itself and any interface elements.
