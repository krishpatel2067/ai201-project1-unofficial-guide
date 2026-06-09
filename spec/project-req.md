# Project Requirements Spec

Colleges have two kinds of knowledge: the official kind (course catalogs, housing handbooks, university websites) and the real kind — the stuff students actually share with each other to survive - namely, Rate My Professor reviews.

In this project, you'll help me build The Unofficial Guide: a RAG (Retrieval-Augmented Generation) system that makes this kind of student-generated knowledge searchable and answerable. A user asks a plain-language question - "Which CS professor gives the most useful feedback?" - and gets a grounded, cited answer drawn from real documents collected.

## Required Features

- [x] **Document Ingestion**:
  - [x] There are 20 raw docs under `documents/raw/`, 2 per professor, copy-pasted from Rate My Professors. One raw doc for a professor is the overall ratings (e.g. `james-calvin-overall.txt`), and the other one is the list of individual ratings (e.g. `james-calvin-reviews.txt`).
  - [x] Load the raw docs, identify the structure, clean or preprocess them as needed (remove unnecessary info like "I'm professor [professor]" from overall ratings), and produce structured text ready for chunking.
  - [x] Each pair of raw docs should produce a single clean doc (e.g. `james-calvin-overall.txt` and `james-calvin-reviews.txt` produce `james-calvin.txt`). Store the clean docs in `documents/clean/`.
  - [x] Use vanilla Python.
- [x] **Chunking Strategy**:
  - [x] Split the clean docs into chunks using document structure-based chunking.
  - [x] The clean docs should have structure to exploit for chunking, so don't focus on character counts (though each review body is capped at 350 characters FYI).
- [x] **Vector Store and Semantic Search**:
  - [x] Embed the chunks using `all-MiniLM-L6-v2` and store them in a ChromaDB vector database.
  - [x] Given a user query, retrieve the top k relevant chunks using semantic similarity search (let k = 5 for reviews).
  - [x] The retrieved chunks must be sorted in ascending order according to cosine distance (most relevant at the top).
  - [x] The user queries are assumed to be about a single professor only (e.g. no cross-professor comparison).
  - ~~[] User queries can ask about stats (separate from natural-language reviews), like overall ratings, the total number of reviews, how many students gave the highest rating, etc.~~
- [x] **Grounded Response Generation**:
  - [x] Use the Groq LLM `llama-3.3-70b-versatile` to generate an answer to the user's query using only the retrieved chunks as context.
  - [x] Use the LLM system prompt:

    ```
    You are a Q/A assistant answering college students' questions about CS professors at the New Jersey Institute of Technology. You will be given a user query along with a few chunks of text as sources. Decide which chunk(s) is/are the most relevant to the user query and generate a concise response (1-3 sentences) using only the chunks provided. If the relevant chunks from one file disagree (e.g. some students found a professor easy and others hard), reflect that disagreement rather than presenting only one side.

    Do NOT use information outside of the provided chunks. Do NOT use any prior knowledge about these professors. If the answer to the user's query doesn't appear in the provided chunks, do NOT guess or fill in the gaps. Instead, reply with exactly "I can't find the answer to that question." and do NOT include any citation or source when you give that response.

    If you are able to answer the user query, you must cite exactly one source using the name of the file that your chosen chunks come from. Each chunk is labeled with the source file it came from. Use that file name for the citation. Each citation must follow the format "[file-name.extension]" (e.g. "[james-calvin.txt]") and must be placed all the way at the end of your response. However, if you cannot find the answer, do NOT include a citation at all.

    "Tags:" are short labels attached to a review (e.g. "Lecture heavy"). They are NOT part of the actual review body.
    ```

- **Query Interface**:
  - [x] Build a basic interface using Gradio to test the end-to-end system.
  - [x] On top of basic chatting interface with the RAG, include debug features to see the retrieved chunks in full, their cosine distances, where they come from.

## Stretch Features

Although these are stretch features, I would like to implement all of them for the practice and points.

- [x] **Hybrid Search**:
  - [x] Combine semantic search with keyword (BM25) search and compare results to semantic-only.
  - [x] Include a toggle in the interface to switch between semantic with keyword search and semantic-only for easy testing.
- [x] **Chunking Strategy**
  - [x] Include a toggle in the interface to switch between 2 chunking strategies: the default structure-based chunking and fixed-size (500-750 characters each with 50-100 characters of overlap or your best judgement from the clean docs).
- [x] **Metadata Filtering**:
  - [x] Allow users to filter by document source (e.g. file name), date, and rating.
  - [x] Users should be able to combine multiple filters.
- [x] **Conversational Memory**:
  - [x] Support multi-turn queries where the system remembers context from the previous question.
  - [x] Include a toggle in the home page of the interface for this functionality for the next chat. That chat would then show whether or not conversational history is enabled.
