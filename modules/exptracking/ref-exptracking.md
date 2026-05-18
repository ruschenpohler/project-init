# Reference: Experiment Tracking

## MLflow
- Use `src/experiment.py:start_run()` wrapper. Do not call `mlflow` directly in scripts.
- Every model fit logs: params used, metrics produced, artefact hash (from CAS if installed).
- `mlruns/` is gitignored. Runs are local unless explicitly exported.

## project_standards.yaml
- All magic numbers (thresholds, seeds, paths) live here.
- When changing a threshold, change it here — one line, one place.
- Agents: read this file at the start of any task that touches model parameters.

## Schema enforcement
- Validate input DataFrames with Pydantic or explicit assert blocks at every pipeline boundary.
- A function that accepts a DataFrame must document expected columns and dtypes in its docstring.
- After every merge/join, assert row count matches expectation.