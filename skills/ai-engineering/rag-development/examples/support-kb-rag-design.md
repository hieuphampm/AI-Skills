# Example: Support Knowledge Base RAG Design

## Input
- `corpus_description`: "Approximately 4,000 Markdown help-center articles, 300–1,500 words each, organized by product area with H2/H3 headings. Some articles embed tables (pricing, error codes) and code snippets."
- `query_profile`: "End-user and support-agent questions like 'How do I reset my API key?' or 'Why does error E402 happen?'. Answers should be short, step-by-step, and cite the article. Latency target < 2s."
- `existing_pipeline`: "Current system uses fixed 512-token chunks with no overlap and dense-only retrieval; users report answers that miss the right article and occasional invented steps."

## Expected Output (`rag_design`)

# RAG Pipeline Design

## 1. Corpus & Query Profile
- **Source Documents**: 4,000 Markdown help articles (300–1,500 words), H2/H3 structured, with tables and code blocks.
- **Question Types**: How-to and error-diagnosis questions; short step-by-step answers with article citations.
- **Constraints**: < 2s latency; high faithfulness (no invented steps).

## 2. Ingestion & Chunking
- **Chunking Strategy**: Structure-aware — split on H2/H3 so each chunk is one coherent section.
- **Chunk Size / Overlap**: 300–600 tokens; keep tables and code blocks intact in a single chunk.
- **Metadata Preserved**: `source_article`, `section_heading`, `product_area`.

## 3. Retrieval & Reranking
| Stage | Choice | Parameters |
| :--- | :--- | :--- |
| Embedding | `<multilingual dense model>` | 1024-dim, English |
| Retrieval | Hybrid (dense + BM25, RRF fusion) | `top-k = 30` |
| Reranker | `<cross-encoder>` | `top-n = 4`, threshold `0.35` |

## 4. Grounded Generation
- **Grounding Rule**: Answer only from retrieved context; cite the article + section for each step.
- **Abstain Behavior**: If no chunk passes the threshold, respond "I couldn't find this in the help center" instead of guessing.
- **Injection Defense**: Chunks wrapped in `<retrieved_context>` delimiters; model instructed to treat them as data only.

## 5. Evaluation Plan
- **Retrieval Metrics**: `recall@4`, `MRR`
- **Generation Metrics**: `faithfulness`, `answer relevance`, `citation accuracy`
- **Golden Set**: 40 representative questions with expected source articles.

## 6. Assumptions & Trade-offs
- Hybrid retrieval + reranker adds ~150ms vs dense-only; acceptable within the 2s budget and directly addresses the "misses the right article" symptom.
- Assumed English corpus; if multilingual articles are added, re-select the embedding model and re-embed all chunks.
