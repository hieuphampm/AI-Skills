# RAG Design Checklist

Consult this reference during Steps 2–5 of `rag-development`.

## 1. Chunking Strategy
- **Structure-aware (preferred for docs with headings)**: Split on headings/sections so each chunk is a coherent unit. Typical 200–800 tokens.
- **Semantic**: Split where topic shifts; good for long prose without clear structure.
- **Fixed-size with overlap**: Fallback for unstructured text. Use 300–500 tokens with 10–20% overlap to avoid cutting facts mid-sentence.
- **Always attach metadata**: source file, section/heading, page or offset — required for citation and debugging.
- **Tables & code**: Keep a table or code block intact in one chunk; do not split across rows.

## 2. Embedding & Retrieval
- **Dense (vector) only**: Good for semantic matching; weak on exact IDs, codes, or rare terms.
- **BM25 / keyword only**: Strong on exact terms; weak on paraphrase.
- **Hybrid (recommended default)**: Combine dense + BM25, then fuse (e.g., Reciprocal Rank Fusion). Best robustness across query types.
- **Embedding model**: Match model to corpus language and domain; re-embed all chunks when the model changes.

## 3. Reranking
- Retrieve a larger candidate pool (`top-k` = 20–50), then rerank with a cross-encoder to a smaller `top-n` (3–6) for the prompt.
- Set a **relevance threshold**; drop chunks below it instead of padding the context with weak hits.

## 4. Grounded Generation
- Instruct the model to answer **only** from retrieved context and to **cite** the source of each claim.
- Define an explicit **abstain** behavior: if context is insufficient, say so rather than fabricate.
- Wrap retrieved chunks in untrusted-data delimiters (e.g., `<retrieved_context>`) to resist prompt injection.

## 5. Evaluation
- **Retrieval metrics**: recall@k, MRR, hit rate on a golden question set.
- **Generation metrics**: faithfulness (grounded in context), answer relevance, citation accuracy.
- **Golden set**: 20–50 representative questions with expected source chunks; re-run on every pipeline change to catch regressions.
