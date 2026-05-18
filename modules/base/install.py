import stat
import subprocess
from pathlib import Path
from project_init.utils import append_fragment

SELF_DIR = Path(__file__).resolve().parent


def install(project_root: Path, project_name: str):
    subprocess.run(["git", "init", "-b", "main", str(project_root)], check=True)

    hooks_dir = project_root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    precommit_d = hooks_dir / "pre-commit.d"
    precommit_d.mkdir(exist_ok=True)
    dispatcher_src = SELF_DIR / "hooks" / "pre-commit"
    dispatcher_dst = hooks_dir / "pre-commit"
    dispatcher_dst.write_text(dispatcher_src.read_text())
    dispatcher_dst.chmod(dispatcher_dst.stat().st_mode | stat.S_IEXEC)

    agents_tmpl = SELF_DIR / "agents.md.tmpl"
    agents_link = project_root / "agents.md"
    try:
        agents_link.symlink_to(agents_tmpl)
    except OSError:
        agents_link.write_text(agents_tmpl.read_text())
        print(
            "  [warn] Could not create symlink for agents.md; "
            "fell back to copy. Symlinks may require admin privileges on Windows."
        )

    ref = project_root / "reference.md"
    ref.write_text("")
    append_fragment(ref, SELF_DIR / "ref-base.md", "base")

    gitignore = project_root / ".gitignore"
    gitignore.write_text(GITIGNORE_CONTENT)

    for d in ["output", "data"]:
        p = project_root / d
        p.mkdir()
        (p / ".gitkeep").touch()

    (project_root / "impl-log.jsonl").touch()


GITIGNORE_CONTENT = """\
# agents and implementation logs
agents.md
impl-log.jsonl
impl-log.md
impl-plan_*.md

# generated artefacts
*.parquet
*.jsonl
*.csv
*.png
*.xlsx
__pycache__/
*.pyc

# data and output
data/
output/

# environment
.venv/
.uvcache/

# secrets
.env
credentials.json

# notebooks
.ipynb_checkpoints/
notebooks/

# spark
metastore_db/
derby.log
spark-warehouse/
"""