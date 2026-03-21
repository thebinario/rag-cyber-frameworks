# RAG Cyber Frameworks

This repository organizes reference materials from cybersecurity frameworks and methodologies that will be used in future retrieval and question-answering stages.

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
```

- `data/raw/` stores the original documents committed to the repository.
- `data/processed/manifests/` stores generated catalog artifacts derived from the raw corpus.
- `data/processed/documents/` stores one processed JSON file per source document.
- `data/processed/chunks/` stores chunked representations derived from `clean_text`.
- `data/processed/embeddings/` stores chunk embeddings generated locally with Ollama.

## Current sources

The repository currently includes:

- `PTES` materials in Markdown format.
- `OSSTMM` material in PDF format.
- `NIST` materials in PDF format.

These files are treated as the canonical raw inputs for the ingestion pipeline.

## Objective of this stage

The project currently has five completed ingestion stages:

1. inventory and manifest generation for raw files
2. source loading and conversion into processed document JSON files
3. conservative text cleaning and normalization
4. chunk generation with overlap from cleaned text
5. local embedding generation from chunks with Ollama

The generated manifest is written to:

`data/processed/manifests/documents_manifest.json`

The processed documents are written to:

`data/processed/documents/`

The generated chunks are written to:

`data/processed/chunks/chunks.jsonl`

The generated embeddings are written to:

`data/processed/embeddings/chunk_embeddings.jsonl`

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

Not implemented yet:

- vector indexing
- retrieval
- answer generation
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

## Next steps

This stage intentionally does not implement vector storage, retrieval, answer generation, or an API. Embeddings are generated locally and saved as JSONL only.

## Next steps

Planned next pipeline stages:

1. vector database indexing
2. retrieval and response orchestration
