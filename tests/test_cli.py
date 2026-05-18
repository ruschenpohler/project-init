import subprocess
import sys


def test_cli_base_only(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_init.cli",
            "test-proj",
            "--path",
            str(tmp_path),
            "--no-python",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (tmp_path / "test-proj" / ".git").exists()


def test_cli_with_python(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_init.cli",
            "test-proj",
            "--path",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (tmp_path / "test-proj" / "pyproject.toml").exists()


def test_cli_refuses_existing_dir(tmp_path):
    (tmp_path / "test-proj").mkdir()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_init.cli",
            "test-proj",
            "--path",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
