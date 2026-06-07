# Project Requirements Spec

Colleges have two kinds of knowledge: the official kind (course catalogs, housing handbooks, university websites) and the real kind — the stuff students actually share with each other to survive - namely, Rate My Professor reviews.

In this project, you'll help me build The Unofficial Guide: a RAG (Retrieval-Augmented Generation) system that makes this kind of student-generated knowledge searchable and answerable. A user asks a plain-language question - "Which CS professor gives the most useful feedback?" - and gets a grounded, cited answer drawn from real documents collected.

## Required Features

- [] **Document Ingestion**:
  - [] There are 20 raw docs under `documents/raw/`, 2 per professor, copy-pasted from Rate My Professors. One raw doc for a professor is the overall ratings (e.g. `james-calvin-overall.txt`), and the other one is the list of individual ratings (e.g. `james-calvin-reviews.txt`).
  - [] Load the raw docs, identify the structure, clean or preprocess them as needed (remove unnecessary info like "I'm professor [professor]" from overall ratings), and produce structured text ready for chunking.
  - [] Each pair of raw docs should produce a single clean doc (e.g. `james-calvin-overall.txt` and `james-calvin-reviews.txt` produce `james-calvin.txt`). Store the clean docs in `documents/clean/`.
  - [] Use vanilla Python.
- [] **Chunking Strategy**:
  - [] Split the clean docs into chunks using document structure-based chunking.
  - [] The clean docs should have structure to exploit for chunking, so don't focus on character counts (though each review body is capped at 350 characters FYI).
- [] **Vector Store and Semantic Search**:
  - [] Embed the chunks using `all-MiniLM-L6-v2` and store them in a ChromaDB vector database.
  - [] Given a user query, retrieve the top k relevant chunks using semantic similarity search (let k = 5 for reviews).
  - [] The retrieved chunks must be sorted in ascending order according to cosine distance (most relevant at the top).
  - [] The user queries are assumed to be about a single professor only (e.g. no cross-professor comparison).
- [] **Grounded Response Generation**:
  - [] Use the Groq LLM `llama-3.3-70b-versatile` to generate an answer to the user's query using only the retrieved chunks as context.
  - [] Use the LLM system prompt:

    ```
    You are a Q/A assistant answering college students' questions about CS professors at the New Jersey Institute of Technology. You will be given a user query along with a few chunks of text as sources. Decide which chunk(s) is/are the most relevant to the user query and generate a short response using only the chunks provided. All of your chosen chunks must come from the same file. Do NOT use chunks from different files in your response.

    Do NOT use information outside of the provided chunks. If the answer to the user's query doesn't appear in the provided chunks, do NOT guess or fill in the gaps - instead, say "I can't find the answer to that question."

    If you are able to answer the user query, you must cite exactly one source using the name of the file that your chosen chunks come from. Each citation must follow the format "[file-name.extension]" (e.g. "[james-calvin.txt]") and must be placed all the way at the end of your response.
    ```

- **Query Interface**:
  - [] Build a basic interface using Gradio to test the end-to-end system.
  - [] On top of basic chatting interface with the RAG, include debug features to see the retrieved chunks in full, their cosine distances, where they come from.

## Stretch Features

- [] **Hybrid Search**:
  - [] Combine semantic search with keyword (BM25) search and compare results to semantic-only.
  - [] Include a toggle in the interface to switch between semantic with keyword search and semantic-only for easy testing.
- [] **Chunking Strategy**
  - [] Include a toggle in the interface to switch between 2 chunking strategies: the default structure-based chunking and fixed-size (500-750 characters each with 50-100 characters of overlap or your best judgement from the clean docs).
- [] **Metadata Filtering**:
  - [] Allow users to filter by document source (e.g. file name), date, and rating.
  - [] Users should be able to combine multiple filters.
- [] **Conversational Memory**:
  - [] Support multi-turn queries where the system remembers context from the previous question.
  - [] Include a toggle in the home page of the interface for this functionality for the next chat. That chat would then show whether or not conversational history is enabled.
