from pathlib import Path
from project_init.runner import run_module


def test_base_creates_git_repo(tmp_project):
    run_module("base", tmp_project, "test-project")
    assert (tmp_project / ".git").exists()


def test_base_creates_dispatcher(tmp_project):
    run_module("base", tmp_project, "test-project")
    dispatcher = tmp_project / ".git" / "hooks" / "pre-commit"
    assert dispatcher.exists()
    assert dispatcher.stat().st_mode & 0o111


def test_base_creates_precommit_d(tmp_project):
    run_module("base", tmp_project, "test-project")
    assert (tmp_project / ".git" / "hooks" / "pre-commit.d").is_dir()


def test_base_creates_agents_symlink_or_copy(tmp_project):
    run_module("base", tmp_project, "test-project")
    agents = tmp_project / "agents.md"
    assert agents.exists()
    content = agents.read_text()
    assert "pre-commit.d contract" in content


def test_base_creates_reference(tmp_project):
    run_module("base", tmp_project, "test-project")
    ref = tmp_project / "reference.md"
    assert ref.exists()
    assert "<!-- module:base -->" in ref.read_text()


def test_base_creates_output_and_data(tmp_project):
    run_module("base", tmp_project, "test-project")
    assert (tmp_project / "output" / ".gitkeep").exists()
    assert (tmp_project / "data" / ".gitkeep").exists()