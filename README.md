# RAG Cyber Frameworks

This repository organizes reference materials from cybersecurity frameworks and methodologies that will be used in future retrieval and question-answering stages.

## Python compatibility

This repository currently requires Python `>=3.12,<3.14`.

- Preferred version: `3.13`
- Not supported for the full stack: `3.14+`

The current Chroma-based vector store stack is not compatible with Python 3.14, so create the project virtual environment with Python 3.13.

Suggested setup on Windows:

```bash
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Data organization

The project separates source documents from processed artifacts:

```text
data/
  raw/
    nist/
    osstmm/
    ptes/
  processed/
    chunks/
    documents/
    embeddings/
    manifests/
  vectorstore/
    chroma/
```

- `data/raw/` stores the original documents committed to the repository.
- `data/processed/manifests/` stores generated catalog artifacts derived from the raw corpus.
- `data/processed/documents/` stores one processed JSON file per source document.
- `data/processed/chunks/` stores chunked representations derived from `clean_text`.
- `data/processed/embeddings/` stores chunk embeddings generated locally with Ollama.
- `data/vectorstore/chroma/` stores the persistent local Chroma index built from chunk embeddings.

## Current sources

The repository currently includes:

- `PTES` materials in Markdown format.
- `OSSTMM` material in PDF format.
- `NIST` materials in PDF format.

These files are treated as the canonical raw inputs for the ingestion pipeline.

## Objective of this stage

The project currently has eight completed ingestion stages:

1. inventory and manifest generation for raw files
2. source loading and conversion into processed document JSON files
3. conservative text cleaning and normalization
4. chunk generation with overlap from cleaned text
5. local embedding generation from chunks with Ollama
6. local vector indexing with Chroma and semantic top-k search
7. retrieval of ranked chunks and formatting of context for generation
8. grounded answer generation with retrieved context and Ollama

The generated manifest is written to:

`data/processed/manifests/documents_manifest.json`

The processed documents are written to:

`data/processed/documents/`

The generated chunks are written to:

`data/processed/chunks/chunks.jsonl`

The generated embeddings are written to:

`data/processed/embeddings/chunk_embeddings.jsonl`

The generated vector index is written to:

`data/vectorstore/chroma/`

## Pipeline status

Implemented in this stage:

- raw document discovery
- metadata cataloging
- manifest generation
- manifest loading primitives
- source loading for PDF, HTML, TXT, and Markdown
- processed document JSON generation
- conservative text cleaning with `clean_text`
- chunk generation using `clean_text`
- local embedding generation with Ollama
- persistent vector indexing with Chroma
- semantic top-k search over indexed chunks
- retrieval-ready context assembly from ranked chunks
- grounded answer generation from retrieved context

Not implemented yet:

- API layer

## Generate the manifest

Run:

```bash
python scripts/inventory_data.py
```

This scans `data/raw/` and regenerates the manifest in `data/processed/manifests/`.

## Load source documents

Run:

```bash
python scripts/load_sources.py
```

This reads the manifest, loads each source document, extracts raw text, and writes one processed JSON file per document to `data/processed/documents/`.

Each processed JSON preserves the manifest metadata and adds:

- `text`
- `clean_text`
- `processing_status`
- `loader_type`
- `processed_at`
- `error`
- `output_path`

The `text` field preserves the extracted content as loaded from the source. The `clean_text` field stores a conservative normalized version for downstream processing.

## Clean processed documents

Run:

```bash
python scripts/clean_documents.py
```

This reads the JSON files in `data/processed/documents/`, applies deterministic normalization to the existing `text` field, and writes the result back into `clean_text` without changing the original `text`.

## Build chunks

Run:

```bash
python scripts/build_chunks.py
```

This reads the processed documents, uses `clean_text` as the chunking source, generates character-based chunks with overlap, and writes the output to `data/processed/chunks/chunks.jsonl`.

Each chunk record includes:

- `chunk_id`
- `document_id`
- `title`
- `framework`
- `source_type`
- `source_path`
- `chunk_index`
- `char_count`
- `text`

## Build embeddings with Ollama

Start the local Ollama server:

```bash
ollama serve
```

Pull the default embedding model:

```bash
ollama pull nomic-embed-text
```

Optional environment variables:

```bash
set OLLAMA_BASE_URL=http://127.0.0.1:11434
set OLLAMA_EMBED_MODEL=nomic-embed-text
set OLLAMA_GENERATE_MODEL=qwen3.5:4b
set OLLAMA_EMBED_TIMEOUT_SECONDS=30
set OLLAMA_GENERATE_TIMEOUT_SECONDS=300
```

Run:

```bash
python scripts/build_embeddings.py
```

This reads `data/processed/chunks/chunks.jsonl`, requests embeddings from the local Ollama API, and writes the results to `data/processed/embeddings/chunk_embeddings.jsonl`.

Each embedding record preserves the chunk metadata and adds:

- `embedding_model`
- `embedding`
- `error`

## Build the vector index

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python scripts/build_vector_index.py
```

This reads `data/processed/embeddings/chunk_embeddings.jsonl`, indexes all records with valid embeddings, and persists the Chroma database in `data/vectorstore/chroma/`.

Indexed records store:

- chunk ids
- embeddings
- chunk texts
- chunk metadata

## Search indexed chunks

Make sure Ollama is running locally because the query embedding is generated at search time.

Run:

```bash
python scripts/search_chunks.py "nist cybersecurity framework" --top-k 5
```

This loads the persistent Chroma index, embeds the query with Ollama, and prints the top-k semantic matches with chunk metadata and text previews.

## Retrieve formatted context

Use the retrieval layer when you want structured results plus a context block that can feed the next generation step.

Run:

```bash
python scripts/retrieve_context.py "nist cybersecurity framework" --top-k 3
```

Or print the formatted context as well:

```bash
python scripts/retrieve_context.py "penetration testing reporting" --top-k 3 --show-context
```

This step:

- generates an embedding for the query with Ollama
- consults the persistent Chroma index
- uses fast retrieval by default for lower latency
- returns structured retrieval results with metadata and distance
- optionally formats the retrieved chunks into a single text context block

For harder queries, use expanded retrieval:

```bash
python scripts/retrieve_context.py "how to use gobuster looking for subdomain" --top-k 3 --retrieval-mode expanded
```

## Ask the full RAG pipeline

Pull a local generation model:

```bash
ollama pull qwen3.5:4b
```

Run the full retrieval + generation flow:

```bash
python scripts/ask_rag.py "What does CSF 2.0 describe?" --top-k 3
```

Or include the grounded context used for the answer:

```bash
python scripts/ask_rag.py "What does CSF 2.0 describe?" --top-k 3 --show-context
```

This step:

- retrieves the top-k relevant chunks
- formats the retrieved context
- builds a grounded prompt
- generates an answer with Ollama
- prints the answer and the retrieved sources

The generator is instructed to answer only from the retrieved context. When a question mentions a specific tool that is not present in the corpus, it should say that clearly and only provide technique-level guidance supported by the retrieved context.

The default `ask_rag.py` path is optimized for latency:

- fast retrieval mode by default
- streaming generation by default
- smaller generation context by default

For harder retrieval problems, switch to expanded mode:

```bash
python scripts/ask_rag.py "How to use gobuster looking for subdomain?" --top-k 3 --retrieval-mode expanded
```

RAG will always be slower than asking the local model directly because it first embeds the query, searches the vector index, and builds a grounded prompt with retrieved evidence before generation.

## Commit guidance

Recommended to commit:

- source code under `app/` and `scripts/`
- `README.md`
- `requirements.txt`
- `pyproject.toml`
- `.python-version`
- deterministic processed JSON artifacts if you want reproducible snapshots of each stage

Recommended to keep out of Git:

- `.venv/`
- temporary local folders such as `.tmp/`
- `data/vectorstore/chroma/` because the Chroma database is a local binary index that can be rebuilt from `data/processed/embeddings/chunk_embeddings.jsonl`

## Next steps

Planned next pipeline stages:

1. API layer
