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
    manifests/
```

- `data/raw/` stores the original documents committed to the repository.
- `data/processed/manifests/` stores generated catalog artifacts derived from the raw corpus.

## Current sources

The repository currently includes:

- `PTES` materials in Markdown format.
- `OSSTMM` material in PDF format.
- `NIST` materials in PDF format.

These files are treated as the canonical raw inputs for the ingestion pipeline.

## Objective of this stage

This stage establishes the document inventory layer for the project. The goal is to scan the files already present in `data/raw/`, normalize a minimal set of metadata, and generate a manifest that can be loaded by application code in later commits.

The generated manifest is written to:

`data/processed/manifests/documents_manifest.json`

## Pipeline status

Implemented in this stage:

- raw document discovery
- metadata cataloging
- manifest generation
- manifest loading primitives

Not implemented yet:

- document parsing beyond file-level metadata
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

## Next steps

Planned next pipeline stages:

1. richer document normalization and content extraction
2. chunk generation per document
3. embedding creation
4. vector database indexing
5. retrieval and response orchestration
