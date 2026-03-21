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
    documents/
    manifests/
```

- `data/raw/` stores the original documents committed to the repository.
- `data/processed/manifests/` stores generated catalog artifacts derived from the raw corpus.
- `data/processed/documents/` stores one processed JSON file per source document.

## Current sources

The repository currently includes:

- `PTES` materials in Markdown format.
- `OSSTMM` material in PDF format.
- `NIST` materials in PDF format.

These files are treated as the canonical raw inputs for the ingestion pipeline.

## Objective of this stage

The project currently has two completed ingestion stages:

1. inventory and manifest generation for raw files
2. source loading and conversion into processed document JSON files

The generated manifest is written to:

`data/processed/manifests/documents_manifest.json`

The processed documents are written to:

`data/processed/documents/`

## Pipeline status

Implemented in this stage:

- raw document discovery
- metadata cataloging
- manifest generation
- manifest loading primitives
- source loading for PDF, HTML, TXT, and Markdown
- processed document JSON generation

Not implemented yet:

- chunking
- embeddings
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
- `processing_status`
- `loader_type`
- `processed_at`
- `error`
- `output_path`

## Next steps

This stage intentionally does not implement chunking, advanced text cleaning, embeddings, retrieval, or answer generation.

## Next steps

Planned next pipeline stages:

1. richer normalization and cleanup of extracted text
2. chunk generation per document
3. embedding creation
4. vector database indexing
5. retrieval and response orchestration
