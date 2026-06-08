---
name: dense-retrieval-misses-tag-only-signals
description: Dense-only retrieval fails the Berenjian "extra credit" query (tag-only signal); BM25/hybrid is the fix; ideal README failure case.
metadata:
  type: project
---

Dense-only semantic retrieval (all-MiniLM-L6-v2, cosine, top-5) FAILS the eval query "Does Professor Berenjian offer extra credit?" — none of her `Extra credit`-tagged reviews surface (top-5 are generic "caring/respected/good teacher" reviews). Root cause: the extra-credit signal lives ONLY in the chunk's tag line ("Tags: Extra credit, …"); the review *bodies* never mention extra credit, so the 2-word tag is diluted within the whole-chunk embedding, and the query's strong "Professor Berenjian" terms pull in name-bearing but off-topic chunks. Dense embeddings are inherently weak at rare/exact-term matching.

**Why:** This is the textbook motivation for the BM25 / hybrid-search stretch feature — BM25's IDF rewards rare discriminative terms like "extra credit" via exact lexical match, so the tagged chunks rank high. Contrast: the "skip Naik's class" query worked under dense retrieval because the review bodies reinforced the tag's meaning.

**How to apply:** (1) Use this as the README "Failure Case Analysis" example — root cause tied to the retrieval stage (tag-only signal diluted in a dense embedding). (2) When building hybrid search, A/B test on this exact query to demonstrate BM25 fixing it. Raw evidence is in `samples/berenjian-extra-credit.txt`.
