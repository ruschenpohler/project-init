# Agent SWE Playbook

## 0. Response Style and Format

- Be direct and honest. Truth over confirmation. Never adjust answers to avoid offending.
- Minimize token use. Do not explain a point more than once per question.
- Be terse in execution. Show reasoning only when prompted to explain.
- Be technically precise. Use equations where they help make a point (render in LaTeX for readability and define all parameters for clarity).
- Prefer fundamental fixes over workarounds. Don't propose quick fixes or technical debt unprompted.
- A substantive answer to an intellectual question typically includes three things: technical explanation, intuition, and a single illustrative example.
- Define abbreviations on first use (full term [abbreviation]). Explain unfamiliar jargon briefly.
- Use jargon alongside explanations so new concepts become associated and can be googled.
- When queried for a summary of a source, read it fully. First list main sections, then summarize each, then answer the query.
- State uncertainty explicitly. If confidence is below the median for your training data, express degree in percent ("I am more uncertain than about XX% of topics.")

---

## 1. Git & Version Control

### Basic function principle
- Every commit must leave the repo in a working state: tests pass, scripts run.

### Commit best practices
- Commit autonomously. Do not ask the user for permission to commit routine, well-scoped changes.
- Commit chunks of logically associated work. A commit should be precise enough that undoing it reverts a single, specific change.
- Commit after each item in your todo list, and before starting the next. If you have completed a logical unit of work (a function, a module, a test suite, a config change), commit it immediately. Do not accumulate uncommitted changes across multiple logical units.

### Commit format
- Use format: `[commit-type]: [commit-description] [severity-level]`
- Use the following set of commit types:

| Label | Scope |
|-------|-------|
| `feat:` | New research or product capability |
| `output:` | New research output, figures, tables, etc. |
| `fix:` | Bug fix |
| `refactor:` | Code restructuring with no behavioural change |
| `style:` | Formatting, lint, whitespace only |
| `chore:` | Maintenance, dependency changes, config updates, file moves |
| `test:` | New or updated tests |
| `docs:` | Documentation, README, docstrings |
| `data:` | Dataset changes, schema migrations |
| `infra:` | Tooling, build system, CI/CD, deployment, platform setup |
| `revert:` | Reverts a previous commit |

- Produce legible, informative, and concise commit descriptions:
  1. First line: imperative mood, ≤72 chars, no period.
  2. Body: explain why, not what. The diff shows what changed. Can be empty if trivial.
  3. Git history is a decision log. Non-obvious choices belong in the commit body.

### Severity scale
Used for commits and log entries alike.

| Score | Definition | Example |
|-------|------------|---------|
| 0/10 | Zero runtime impact. Cannot break anything. | `style: ruff format src/ [0]` |
| 1/10 | Zero runtime impact. Mechanical change. | `chore: update .gitignore for output/ [1]` |
| 2/10 | Low risk. Existing tooling, version bumps. | `chore: bump pandas 2.0.0 → 2.0.1 [2]` |
| 3/10 | Low risk. Moves or renames with no logic change. | `chore: move spark_pipeline.py to src/legacy/ [3]` |
| 4/10 | Moderate risk. Adds or updates tests/docs. | `test: add fixture for CLI stacking [4]` |
| 5/10 | Moderate risk. Standard research parameter change. | `feat: expand GBT grid to max_depth ∈ {3,4,5,6} [5]` |
| 6/10 | Structural. Touches core logic but preserves interface. | `refactor: extract feature_groups() by target_key [6]` |
| 7/10 | Substantial. New feature with downstream consumers. | `feat: add target-specific GDP lags for Y/Y [7]` |
| 8/10 | Critical. Fixes a bug that affects published results. | `fix: use Y/Y lags instead of Q/Q for yy target [8]` |
| 9/10 | High stakes. Changes experimental protocol or data source. | `feat: switch from truncated panel to bridge-equation fill [9]` |
| 10/10 | Existential. Could invalidate prior analysis or paper claims. | `feat: replace sklearn GBT with EM-DFM frontier [10]` |

### Gitignore standards
- Add the following to `.gitignore`. Do not commit them unprompted:
  1. `AGENTS.md`, `impl-log.md`, `impl-plan_*.md`, or any other implementation logging files.
  2. Generated artefacts: `.parquet`, `.jsonl`, `.csv`, `.png`, `.xlsx`, `__pycache__/`, `*.pyc`.
  3. Data directories: `data/`, `output/`.
  4. Environment directories: `.venv/`, `.uvcache/`.
  5. Secrets or credentials: `.env`, `credentials.json`, API keys, tokens.
  6. Notebook checkpoints and Spark artefacts: `.ipynb_checkpoints/`, `metastore_db/`, `derby.log`, `spark-warehouse/`.
  7. Scratch notebooks: `notebooks/` (learning material, not portfolio code).

---

## 2. Environment & Dependencies

### uv is the single source of truth
- Never `pip install` inside the project. Always `uv sync` or `uv sync --extra dev`.
- `pyproject.toml` owns dependencies; `uv.lock` is committed as the reproducibility contract.
- Use `uv add <pkg>` so `uv.lock` updates automatically. Do not edit `pyproject.toml` by hand for deps.
- Always commit `uv.lock` when dependencies change. An out-of-date lockfile breaks reproducibility.

### Dependency minimalism
- Upper-bound dependencies: `pandas>=2.0.0,<3.0.0`. The lockfile pins exact; bounds communicate intent.
- Do not add a dependency for trivial stdlib functionality (<20 lines).
- Separate runtime / dev / optional groups:
  - **Runtime:** minimal
  - **Dev:** pytest, ruff, mypy
  - **Optional:** legacy code, heavy viz, notebook-only tools

### Python version
- Pin `.python-version`. uv respects it.
- Document minimum version in `requires-python`.

---

## 3. Code Quality & Linting

### Lint before commit
- Run `uv run ruff check src/ tests/` and `uv run ruff format src/ tests/` before staging.
- Fix errors, then stage, then commit.

### Ruff configuration
- Set `line-length`, `target-version`, `exclude` once in `pyproject.toml`.
- Exclude directories you do not own (e.g., `src/legacy/`).

### Type hints
- Use them on function signatures.
- If a function returns `pd.DataFrame | None`, state it explicitly.

---

## 4. Testing

### Unit tests
- Fast, deterministic, no external dependencies.
- Use synthetic fixtures in `conftest.py`. ~100 rows is enough.
- Every non-trivial pure function gets a unit test. That includes every file in `src/`.
- Test edge cases: empty input, single row, NaN, identical values, zero variance.
- Tests must be independent. No test should rely on another test's output or files.
- Use `tmp_path` for all file I/O in tests. Never write to `output/` or `data/` from a test.

### Integration tests
- Run on real artefacts but skip if absent: `@pytest.mark.skipif(not PATH.exists())`.
- Validate end-to-end plumbing, not model quality.

### Fixture design
- Deterministic RNG: `np.random.default_rng(42)`.
- Match real data formats exactly (e.g., `"YYYY-QQ"` with hyphen).
- Include structural properties: cold-start countries, missing data, staggered time ranges.

### Test naming
- State the expected outcome: `test_drops_countries_below_threshold`, not `test_filter_min_obs_1`.

### Test the contract, not the implementation
- Bad: `assert model.named_steps["regressor"].max_depth == 3`
- Good: `assert predictions.isna().sum() == 0`

### No flaky tests
- Any test that fails intermittently due to RNG, timing, or races will be ignored.
- Seed everything, mock time, avoid concurrency in unit tests.

---

## 5. Code Structure & Modularity

### Function design
- A function should either compute something or perform an action, never both. `fit_and_plot_and_save()` couples model logic to I/O and visualization, making it untestable and unreusable.

### No module-level mutable state
- `OUTPUT_PATH = "output/predictions.parquet"` at module scope prevents test redirection and thread safety. Use function arguments and factories. Constants are fine; mutable globals are bugs.

### Configuration is not code
- Magic numbers (`min_obs=8`, `lag_depth=4`) belong in a single config dict or dataclass. When an agent changes a threshold, they should touch exactly one line.

### No orphaned code
- If a module is not imported by any active script, delete it or document it prominently as unused. Dead code misleads the next agent.

### Python module naming
- Never start a Python filename with a digit. `02_feature_engineering.py` is unimportable via standard `import`, breaks pytest discovery, IDE navigation, and type checking. Use `feature_engineering.py` or prefix with a letter if ordering matters: `p02_feature_engineering.py`.

---

## 6. Data Handling (Python / pandas)

### Never mutate inputs in-place
- `def compute_lags(df): df["lag1"] = df["x"].shift(1); return df` mutates the caller's DataFrame, causing Heisenbugs in tests and pipelines. Default to `df = df.copy()` at the top of every transform. The memory cost is negligible; the debugging cost is enormous.

### Type stability
- A function that returns `pd.DataFrame | None` forces callers to handle two paths forever. Better: return an empty DataFrame with correct columns and schema.

### Validate at every boundary
- After every `pd.read_parquet()`, assert expected columns and dtypes.
- After every merge/join, assert row count is expected.
- After regex extract, assert no NaNs from mismatches.
- Example: `pd.Period("2010Q4")` produces `"2010Q4"`; data uses `"2010-Q4"`. A silent filter failure produces empty results with no error. Assert: `df["year_quarter"].str.match(r"\d{4}-Q\d").all()` after load.

---

## 7. Reproducibility & Determinism

### Seed all randomness
- `np.random.normal()`, `pd.DataFrame.sample()`, sklearn internals — all need explicit seeds. The seed should be a parameter, not hardcoded deep in a function: `fit_model(X, y, random_state=42)`.

### No absolute paths
- `"/Users/alice/projects/data/file.csv"` kills portability. Use `Path(__file__).resolve().parent.parent / "data" / "file.csv"` or environment variables with sensible defaults.

### Create output directories programmatically
- `Path("output/tables").mkdir(parents=True, exist_ok=True)` before every write. Do not assume a directory exists because it was created once manually.

### Restartable long-running jobs
- Any job >5 minutes must be designed for interruption. Append-only checkpointing (JSONL, SQLite) beats read-rewrite (parquet). Log progress after every iteration. Maintain `existing_combos()` or equivalent: never recompute what is already done.

### Hyperparameter persistence
- Every model fit should log what was actually used, not just what was in the grid. JSONL sidecars for long jobs are cheap and invaluable for debugging.

---

## 8. Defensive Programming & Error Handling

### Fail loud, fail early
- Silent `return None` when training data is empty creates a downstream `TypeError` 20 minutes later. Raise `ValueError("Training set empty after filtering")` immediately. Assertions are executable documentation: `assert len(train) >= 20, f"Too small: {len(train)}"`.

### Rename safety
- Renaming a column or function is a breaking change. Search the entire codebase for the old name before committing. Better: add the new name, migrate downstream code, then drop the old in a follow-up commit.

### Smoke test before full run
- Before kicking off a 90-minute job, run one iteration manually and inspect the output. Before running the full test suite, run one test: `uv run pytest tests/test_x.py::test_y -v`.

---

## 9. Scope Discipline

### Don't start creating files unprompted
- Only start producing a new file with explicit confirmation from the user. Do not create new modules, scripts, or documentation files unprompted.

### Do not introduce abstractions prematurely
- Do not create a base class, utility module, or helper function until the same pattern appears three times. A 50-line script is often clearer than a refactored 5-file architecture.

### Assert specific values, not just shapes and types
- Code that compiles and passes superficial inspection can still have off-by-one errors, silent type coercion, or incorrect pandas axis semantics. Countermeasure: assert specific values in tests and at runtime boundaries.

### Do not rewrite code you do not understand
- Legacy code is often messy because it learned edge cases through bugs. Understand why it is messy before cleaning it. If you cannot explain every line, do not delete it.

### Limit change scope
- If a change touches >5 files, it is probably two changes. Split by concern: "add feature" and "refactor for readability" should not be in the same commit stream.

---

## 10. Logging

### Format
- Append-only JSONL: one line per event.
- File: `impl-log.jsonl` (or project-specific name).

### Schema
| Field | Type | Explanation |
|-------|------|-------------|
| `timestamp` | string (ISO 8601) | Exact date and time: `YYYY-MM-DDTHH:MM:SS` |
| `impl-stage` | string | Project-specific stage: `"Phase 1.3, Rolling eval"` or `"Step 1b"` |
| `headline` | string | One-line summary, readable without opening `notes` |
| `notes` | string | Full narrative: what, why, blockers, decisions |
| `metrics` | object (JSON dict) | Structured data for queryability. See below. |
| `commit-ids` | string | Comma-separated git hashes linked to this entry. Empty if none. |
| `status` | string | One of: `started`, `in-progress`, `completed`, `halted`, `failed`, `handover` |
| `severity` | integer [0,10] | Load-bearing score. Same scale as commits (Section 1). |

### What goes in `metrics`
`metrics` is not regex bait. It is structured data extracted at write-time. Put anything you might later sum, average, or filter on. If a future analyst asks a quantitative question and the number is not in `metrics`, the answer requires reading English prose.

Example:
```json
{
  "timestamp": "2026-05-06T14:00:00",
  "impl-stage": "Phase 1.3, Rolling eval",
  "headline": "Rewrote rolling eval with sklearn, 61 origins",
  "notes": "Rewrote src/05_rolling_eval.py with sklearn...",
  "metrics": {"predictions": 23383, "origins": 61, "duration_min": 90, "restarts": 7},
  "commit-ids": "377d674",
  "status": "completed",
  "severity": 6
}
```

### Status definitions
| Status | Meaning |
|--------|---------|
| `started` | Work has begun. No output yet. |
| `in-progress` | Work ongoing. Partial output may exist. |
| `completed` | Work finished. Output validated. |
| `halted` | Blocked by external dependency or decision. |
| `failed` | Attempted and did not succeed. Error documented. |
| `handover` | Ready for next agent. Includes status quo and next steps. |
