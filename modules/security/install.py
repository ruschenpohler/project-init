import stat
from pathlib import Path

SELF_DIR = Path(__file__).resolve().parent


def install(project_root: Path, project_name: str):
    hooks_d = project_root / ".git" / "hooks" / "pre-commit.d"
    hooks_d.mkdir(exist_ok=True)

    pip_audit_hook = hooks_d / "70-pip-audit.sh"
    pip_audit_hook.write_text(PIP_AUDIT_HOOK)
    pip_audit_hook.chmod(pip_audit_hook.stat().st_mode | stat.S_IEXEC)

    bandit_hook = hooks_d / "71-bandit.sh"
    bandit_hook.write_text(BANDIT_HOOK)
    bandit_hook.chmod(bandit_hook.stat().st_mode | stat.S_IEXEC)

    audit_log = project_root / "audit.log"
    audit_log.touch()

    gitignore = project_root / ".gitignore"
    content = gitignore.read_text()
    if "audit.log" not in content:
        with gitignore.open("a") as f:
            f.write("\n# security audit log\naudit.log\n")

    from project_init.utils import append_fragment

    append_fragment(
        project_root / "reference.md", SELF_DIR / "ref-security.md", "security"
    )


PIP_AUDIT_HOOK = """\
#!/bin/bash
# 70-pip-audit.sh: fail on high-severity vulnerabilities only
uv run pip-audit --severity high --exit-code 1 || exit 1
"""

BANDIT_HOOK = """\
#!/bin/bash
# 71-bandit.sh: static security analysis, high severity only
uv run bandit -r src/ --severity-level high -q || exit 1
"""