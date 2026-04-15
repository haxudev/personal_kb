---
description: "Convert files in inbox/ to Markdown and store them in workmemory/"
---

## /ingest

Ingest files from `inbox/` into your local knowledge base.

### Steps

1. Run `bash scripts/preflight.sh` to verify `markitdown` is installed
2. Scan `inbox/` recursively for supported file formats
3. For each file, call `markitdown` and write the output to `workmemory/`, preserving the relative path structure
4. Add YAML frontmatter to each output file (`source_path`, `ingested_at`)
5. Report summary: N succeeded, M failed, K skipped

### Supported Formats

All formats supported by markitdown: `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.xml`, `.json`, `.csv`, `.epub`, `.ipynb`, `.txt`

### Behavior

- Output filename: original name with `.md` extension (e.g., `report.pdf` → `report.pdf.md`)
- Subdirectory structure is preserved (`inbox/notes/todo.txt` → `workmemory/notes/todo.txt.md`)
- Already-existing output files are skipped unless `--force` is specified
- Single file failures do not block the rest of the batch
- If `inbox/` is empty, prompt the user to add files first

### Usage

```
/ingest
/ingest --force
```
