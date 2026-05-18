# Reference: Security

## Pre-commit checks
- `70-pip-audit.sh`: fails on high-severity dependency vulnerabilities. Runs before commit.
- `71-bandit.sh`: static analysis on `src/`. Fails on high-severity findings only.

## Audit log
- `audit.log` is append-only. Never truncate or delete it.
- Log format: one JSON line per event, same schema as `impl-log.jsonl`.
- Gitignored. Lives on disk only.

## Rules
- Never commit secrets, API keys, or credentials. `.env` and `credentials.json` are gitignored.
- If pip-audit or bandit fires, fix the issue before committing — do not use `--skip` flags.