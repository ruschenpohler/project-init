import sys
from pathlib import Path

from project_init.runner import run_module

MODULES_DIR = Path(__file__).resolve().parent.parent / "modules"


def test_base_creates_git_repo(tmp_project):
    run_module("base", tmp_project, "test-project")
    assert (tmp_project / ".git").exists()


def test_base_creates_dispatcher(tmp_project):
    run_module("base", tmp_project, "test-project")
    dispatcher = tmp_project / ".git" / "hooks" / "pre-commit"
    assert dispatcher.exists()
    if sys.platform != "win32":
        assert dispatcher.stat().st_mode & 0o111


def test_base_creates_precommit_d(tmp_project):
    run_module("base", tmp_project, "test-project")
    assert (tmp_project / ".git" / "hooks" / "pre-commit.d").is_dir()


def test_base_creates_agents_symlink_or_copy(tmp_project, capsys):
    run_module("base", tmp_project, "test-project")
    agents = tmp_project / "agents.md"
    assert agents.exists()
    tmpl = MODULES_DIR / "base" / "agents.md.tmpl"
    assert agents.read_text() == tmpl.read_text()
    if sys.platform == "win32":
        assert not agents.is_symlink()
        assert "Could not create symlink" in capsys.readouterr().out
    else:
        assert agents.is_symlink()


def test_base_creates_reference(tmp_project):
    run_module("base", tmp_project, "test-project")
    ref = tmp_project / "reference.md"
    assert ref.exists()
    assert "<!-- module:base -->" in ref.read_text()


def test_base_creates_output_and_data(tmp_project):
    run_module("base", tmp_project, "test-project")
    assert (tmp_project / "output" / ".gitkeep").exists()
    assert (tmp_project / "data" / ".gitkeep").exists()
