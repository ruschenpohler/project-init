# Reference: Python

## uv discipline
- Never `pip install`. Always `uv sync` or `uv add <pkg>`.
- `pyproject.toml` owns deps. `uv.lock` is the reproducibility contract — always commit it.
- Upper-bound dependencies: `pandas>=2.0.0,<3.0.0`.
- Separate runtime / dev / optional groups.

## Ruff
- Config lives in `pyproject.toml` under `[tool.ruff]`. Do not duplicate elsewhere.
- Pre-commit hook runs automatically. Do not skip it.

## pytest
- Every non-trivial pure function in `src/` gets a unit test.
- Fixtures in `conftest.py`. Use `random.seed(42)` for determinism.
- Use `tmp_path` for all file I/O in tests.
- Test naming: state the outcome — `test_drops_countries_below_threshold`, not `test_filter_1`.