import stat
from pathlib import Path

SELF_DIR = Path(__file__).resolve().parent


def install(project_root: Path, project_name: str):
    tmpl = (SELF_DIR / "pyproject.toml.tmpl").read_text()
    rendered = tmpl.replace("{{PROJECT_NAME}}", project_name)
    (project_root / "pyproject.toml").write_text(rendered)

    (project_root / ".python-version").write_text("3.11\n")

    src_pkg = project_root / "src" / project_name.replace("-", "_")
    src_pkg.mkdir(parents=True)
    (src_pkg / "__init__.py").touch()
    tests_dir = project_root / "tests"
    tests_dir.mkdir()
    (tests_dir / "__init__.py").touch()
    (tests_dir / "conftest.py").write_text(CONFTEST_CONTENT)

    hook = project_root / ".git" / "hooks" / "pre-commit.d" / "20-ruff.sh"
    hook.write_text(RUFF_HOOK)
    hook.chmod(hook.stat().st_mode | stat.S_IEXEC)

    hook = project_root / ".git" / "hooks" / "pre-commit.d" / "30-pytest.sh"
    hook.write_text(PYTEST_HOOK)
    hook.chmod(hook.stat().st_mode | stat.S_IEXEC)

    from project_init.utils import append_fragment

    append_fragment(project_root / "reference.md", SELF_DIR / "ref-python.md", "python")


CONFTEST_CONTENT = """\
import pytest
import random


@pytest.fixture
def rng():
    random.seed(42)
    return random
"""

RUFF_HOOK = """\
#!/bin/bash
# 20-ruff.sh: lint and format check
uv run ruff check src/ tests/ || exit 1
uv run ruff format --check src/ tests/ || exit 1
"""

PYTEST_HOOK = """\
#!/bin/bash
# 30-pytest.sh: run test suite
uv run pytest tests/ -q || exit 1
"""