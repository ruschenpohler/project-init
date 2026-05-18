from pathlib import Path
import subprocess

SELF_DIR = Path(__file__).resolve().parent


def install(project_root: Path, project_name: str):
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        # uv add modifies pyproject.toml and generates/updates uv.lock.
        # Both are picked up by the initial commit in runner.py. This is correct.
        subprocess.run(
            ["uv", "add", "--optional", "dev", "mlflow>=2.0.0,<3.0.0"],
            cwd=str(project_root),
            check=False,
        )

    src_dir = project_root / "src"
    src_dir.mkdir(exist_ok=True)
    (src_dir / "experiment.py").write_text(EXPERIMENT_MODULE)

    (project_root / "project_standards.yaml").write_text(STANDARDS_CONTENT)

    from project_init.utils import append_fragment

    append_fragment(
        project_root / "reference.md", SELF_DIR / "ref-exptracking.md", "exptracking"
    )


EXPERIMENT_MODULE = '''\
"""
MLflow experiment tracking wrapper.
Provides a thin, opinionated interface over mlflow.start_run().
"""
import mlflow
from pathlib import Path
from typing import Any


def start_run(
    experiment_name: str,
    run_name: str,
    params: dict[str, Any],
    tags: dict[str, str] | None = None,
):
    """
    Start a tracked MLflow run. Logs all params immediately.
    Returns the active run context manager.
    """
    mlflow.set_experiment(experiment_name)
    run = mlflow.start_run(run_name=run_name, tags=tags or {})
    mlflow.log_params(params)
    return run
'''

STANDARDS_CONTENT = """\
# project_standards.yaml
# Single source of truth for project-wide configuration.
# Agents: change thresholds here, not in source code.

random_seed: 42
min_observations: 20
output_dir: output/
data_dir: data/
log_file: impl-log.jsonl
"""
