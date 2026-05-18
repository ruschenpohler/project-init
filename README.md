# `project-init`: A CLI Scaffolding Tool to Initializes Project Environments

A CLI scaffolding tool that initializes new projects with a complete, opinionated environment: version control, dependency management, code quality tooling, agent behavioral protocols, and optional domain modules. Designed for use by humans and agentic collaborators. Every project produced by `project-init` is git-backed from the start, has pre-commit hooks enforcing quality gates, carries an `agents.md` behavioral protocol, and builds a `reference.md` from the modules installed. Automating the basic setup of a new projects effectively sidesteps forgetting and configuration drift between projects.

---

## Install

```bash
git clone https://github.com/ruschenpohler/project-init
cd project-init
uv sync
```

Requires Python 3.11+ and [uv](https://github.com/astral-sh/uv).

---

## Usage

```bash
# base + python (default)
project-init my-project

# base only, no Python tooling
project-init my-project --no-python

# named profile (flag bundle)
project-init my-project --profile ml-research

# explicit flags
project-init my-project --cas --exptracking --security

# specify parent directory
project-init my-project --path ~/projects/
```

---

## What gets scaffolded

Every project receives the following, regardless of flags:

```
my-project/
├── .git/
│   └── hooks/
│       ├── pre-commit          # dispatcher: never overwritten by modules
│       └── pre-commit.d/       # modules drop numbered hook scripts here
├── agents.md                   # symlink to project-init/modules/base/agents.md.tmpl
├── reference.md                # built at init time by appending module fragments
├── .gitignore
├── impl-log.jsonl              # append-only JSONL audit log
├── output/
│   └── .gitkeep
└── data/
    └── .gitkeep
```

With the `python` module (default):

```
├── pyproject.toml              # project name substituted from template
├── .python-version
├── src/
│   └── my_project/
│       └── __init__.py
└── tests/
    └── conftest.py
```

The initial commit is made automatically with `--no-verify`, since hooks should not fire on the scaffold itself. Every subsequent commit goes through the full hook chain.

---

## Modules

### `base` (mandatory)

- Initializes a git repo with `main` as the default branch.
- Installs the pre-commit dispatcher into `.git/hooks/pre-commit`. This file is owned by `base` and never overwritten. Modules add checks by dropping numbered scripts into `.git/hooks/pre-commit.d/` -- naming convention `NN-description.sh`, where lower numbers run first.
- Creates `agents.md` as a symlink to `modules/base/agents.md.tmpl` in the `project-init` repo. Updating the template propagates to all symlinked projects immediately.
- Creates `reference.md` and appends the base reference fragment. Subsequent modules append their own fragments.
- Writes a standard `.gitignore` covering generated artefacts, data directories, secrets, and environment files.

### `python` (default-on, skip with `--no-python`)

- Writes `pyproject.toml` from a template, substituting the project name.
- Pins `.python-version` to 3.11.
- Creates `src/<project_name>/` and `tests/` with a `conftest.py` stub.
- Installs two pre-commit hooks: `20-ruff.sh` (lint and format check) and `30-pytest.sh` (full test suite). Both run via `uv run` to ensure the project's own environment is used.

### `cas` (optional, `--cas`)

- Creates `cas/store/` and `cas/shadow/` directories.
- Writes `src/cas.py` with SHA-256 helpers: `hash_file`, `hash_directory`, and `store_artefact`.
- Content-addressed storage makes silent overwrites of artefacts impossible: a changed file produces a different hash and is stored separately.

### `exptracking` (optional, `--exptracking`)

- Adds MLflow to the project's dev dependencies via `uv add`.
- Writes `src/experiment.py`, a thin wrapper over `mlflow.start_run` that logs all params immediately.
- Writes `project_standards.yaml` as the single source of truth for project-wide configuration (seeds, thresholds, paths). Agents and scripts read this file; magic numbers do not live in source code.
- Includes Pydantic-style schema enforcement conventions via the reference fragment.

### `security` (optional, `--security`)

- Installs `70-pip-audit.sh` and `71-bandit.sh` into `pre-commit.d/`. Both fail on high-severity findings only, keeping the signal-to-noise ratio high.
- Creates `audit.log` (append-only, gitignored) for file-based audit logging outside the git history.

---

## Profiles

Profiles are flat files in `profiles/` containing one flag per line. They allow named configurations without requiring the caller to remember individual flags.

```
# profiles/ml-research.flags
--cas
--exptracking
--security
```

```bash
project-init my-project --profile ml-research
```

Profiles and explicit flags can be combined. Explicit flags take precedence.

---

## Design notes

**Dispatcher pattern.** A git repo supports exactly one `.git/hooks/pre-commit` file. Without coordination, each module would overwrite the previous module's hook. The dispatcher solves this: `base` installs a single hook that iterates over `pre-commit.d/*.sh` in numeric order. Modules never touch the dispatcher -- they only add scripts to the directory. Installation order is irrelevant; execution order is controlled by the numeric prefix.

**Append-on-install for `reference.md`.** Each module ships a `ref-<name>.md` fragment. At install time, the fragment is appended to the project's `reference.md` behind an idempotency sentinel (`<!-- module:name -->`). Re-running a module does not duplicate its section. The result is a single reference file in every project, scoped exactly to what is installed, built from authoritative per-module sources.

**Symlink for `agents.md`.** Rather than copying `agents.md` into each project, `base` creates a symlink pointing to `modules/base/agents.md.tmpl` in the `project-init` repo. Edits to the template propagate to all projects immediately, with no per-project update step. On Windows without Developer Mode, the symlink falls back to a file copy with a printed warning -- changes to the template will not propagate automatically in that case.

**`uv` as the single environment layer.** `pyproject.toml` owns dependencies. `uv.lock` is committed as the reproducibility contract. No `pip install`, no `requirements.txt`, no manual environment management. Pre-commit hooks invoke tooling via `uv run` to ensure the project environment is always used.

**Initial commit.** The scaffold makes the first commit automatically using `--no-verify`. This prevents the ruff and pytest hooks from firing against an empty or partial project state. Every commit after the first goes through the full hook chain.

---

## Adding a module

1. Create `modules/<name>/install.py` with a function `install(project_root: Path, project_name: str)`.
2. Create `modules/<name>/ref-<name>.md` with the reference content for this module.
3. In `install.py`, append the fragment to `reference.md`:
   ```python
   from project_init.utils import append_fragment
   append_fragment(project_root / "reference.md", SELF_DIR / "ref-<name>.md", "<name>")
   ```
4. If the module installs a pre-commit hook, write it to `pre-commit.d/` with a numeric prefix. Do not touch `.git/hooks/pre-commit`.
5. Add the module name to `MODULE_ORDER` in `runner.py`.
6. Add a `--<name>` flag in `cli.py` and wire it into `resolve_flags`.
7. Write tests in `tests/test_<name>.py`. Cover: files created, reference fragment appended, idempotency.

---

## Windows

`agents.md` is created as a symlink on Unix. On Windows, symlinks require either Developer Mode or administrator privileges. If neither is available, `base` falls back to copying `agents.md.tmpl` into the project as a regular file with a printed warning. In that case, changes to `modules/base/agents.md.tmpl` in the `project-init` repo must be manually propagated to existing projects.

Pre-commit hooks use bash. On Windows, Git Bash or WSL is required for hooks to execute.

---

## Pre-commit hooks and cloned projects

Pre-commit hooks live in `.git/hooks/`, which git does not commit or transfer on clone. If a scaffolded project is cloned to a new machine, the hooks must be reinstalled. The simplest approach is to re-run `project-init` against the cloned directory, or to copy the `pre-commit.d/` scripts manually.
