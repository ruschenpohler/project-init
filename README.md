# project-init

Scaffolding CLI for new projects. Installs git, tooling, agent protocols, and domain modules
in one command.

## Install

```bash
git clone https://github.com/ruschenpohler/project-init
cd project-init
uv sync
```

## Usage

```bash
# Minimal (base + python)
project-init my-project

# Non-python project (base only)
project-init my-project --no-python

# ML research project
project-init my-project --profile ml-research

# Custom flag combination
project-init my-project --cas --exptracking --security

# Specify parent directory
project-init my-project --path ~/projects/
```

## Modules

| Module | Flag | Always? | Contents |
|---|---|---|---|
| base | — | yes | git, dispatcher, agents.md, reference.md, .gitignore, output/, data/ |
| python | default-on | `--no-python` to skip | uv, ruff, pytest, src/ structure |
| cas | `--cas` | no | content-addressed storage, SHA-256 hashing |
| exptracking | `--exptracking` | no | MLflow wrapper, project_standards.yaml |
| security | `--security` | no | pip-audit, bandit, audit.log |

## Profiles

Profiles are flag bundles in `profiles/`. Current profiles:
- `ml-research`: `--cas --exptracking --security`

## Adding a module

1. Create `modules/<name>/install.py` with an `install(project_root, project_name)` function.
2. Create `modules/<name>/ref-<name>.md` with a reference fragment.
3. Add the module name to `MODULE_ORDER` in `runner.py`.
4. Add a `--<name>` flag in `cli.py`.
5. Write tests in `tests/test_<name>.py`.

## Windows note

On Windows, the `agents.md` symlink falls back to a file copy if symlinks require
admin privileges. Edit `modules/base/agents.md.tmpl` in the `project-init` repo to
propagate changes to scaffolded projects.

## Pre-commit hooks

Hooks are installed into `.git/hooks/` which is not committed. If a project is cloned
fresh, hooks must be reinstalled by re-running `project-init` or manually.