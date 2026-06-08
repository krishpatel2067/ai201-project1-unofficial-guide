---
name: dense-retrieval-misses-tag-only-signals
description: Both dense-only AND hybrid (BM25+RRF) retrieval fail the Berenjian "extra credit" query (tag-only signal); accepted as a documented system limitation / README failure case.
metadata:
  type: project
---

The eval query "Does Professor Berenjian offer extra credit?" fails under BOTH retrieval modes — none of her `Extra credit`-tagged reviews reach the top-5, so generation correctly refuses ("I can't find the answer…").

Root cause: the extra-credit signal lives ONLY in the chunk's tag line; the review *bodies* never mention extra credit. So:
- **Dense:** the 2-word tag is diluted within the whole-chunk embedding; generic Berenjian reviews ("caring/respected") that also match "professor/berenjian" rank higher.
- **Hybrid (BM25 + RRF):** verified via `temp.md` — still all-generic top-5. RRF (fused over the FULL 759-chunk corpus) rewards chunks strong on *both* axes; the generic chunks are semantic-top AND match "professor"/"berenjian" on BM25, so they out-score the BM25-only extra-credit chunks. (Hybrid did help professor coherence, though: it displaced an off-topic Itani chunk that semantic-only ranked #5.)

**Why:** A realistic fix (fuse each retriever's top-N instead of the whole corpus) risks floating a *different* professor's extra-credit chunk to #1, which `filter_to_top_file` would then lock onto → wrong-professor answer. Fixing that needs query-aware professor filtering = scope creep for a class project.

**Decision:** accept as a documented limitation. Use it as the README "Failure Case Analysis" example (root cause = retrieval stage; tag-only signal diluted in both dense embedding and RRF fusion). Evidence: `samples/` + `temp.md`.
