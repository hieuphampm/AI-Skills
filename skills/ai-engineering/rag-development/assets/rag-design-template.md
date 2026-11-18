# RAG Pipeline Design

## 1. Corpus & Query Profile
- **Source Documents**: `<formats, scale, structure>`
- **Question Types**: `<typical queries and expected answer style>`
- **Constraints**: `<latency, accuracy, cost targets>`

## 2. Ingestion & Chunking
- **Chunking Strategy**: `<structure-aware | semantic | fixed-size+overlap>`
- **Chunk Size / Overlap**: `<tokens>` / `<overlap %>`
- **Metadata Preserved**: `<source, section, page/offset>`

## 3. Retrieval & Reranking
| Stage | Choice | Parameters |
| :--- | :--- | :--- |
| Embedding | `<model>` | `<dimension, language>` |
| Retrieval | `<dense | bm25 | hybrid>` | `top-k = <n>` |
| Reranker | `<cross-encoder model>` | `top-n = <n>`, threshold `<value>` |

## 4. Grounded Generation
- **Grounding Rule**: Answer only from retrieved context; cite each claim.
- **Abstain Behavior**: `<what to do when context is insufficient>`
- **Injection Defense**: Retrieved chunks wrapped in `<retrieved_context>` delimiters.

## 5. Evaluation Plan
- **Retrieval Metrics**: `recall@<k>`, `MRR`
- **Generation Metrics**: `faithfulness`, `answer relevance`, `citation accuracy`
- **Golden Set**: `<size>` questions with expected source chunks

## 6. Assumptions & Trade-offs
- `<explicit assumptions made and accuracy/latency/cost trade-offs>`
