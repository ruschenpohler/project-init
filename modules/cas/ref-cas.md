# Reference: CAS (Content-Addressed Storage)

## Purpose
CAS ensures that every artefact (model, dataset, output file) is identified by its content,
not its filename. If the file changes, the hash changes — silent overwrites are impossible.

## Structure
- `cas/store/` — immutable artefact store, keyed by SHA-256 hash
- `cas/shadow/` — staging area for artefacts not yet committed to store

## Usage
```python
from src.cas import hash_file, hash_directory, store_artefact
digest = store_artefact(Path("output/model.pkl"), Path("cas/store"))
```

## Rules
- Never delete files from `cas/store/` manually.
- Log the digest in `impl-log.jsonl` under `metrics.artefact_hash` for every stored artefact.
- `cas/` is gitignored by default (large binary files). Add digests to logs, not files to git.