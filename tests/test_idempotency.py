from project_init.runner import run_module


def test_base_idempotent(tmp_project):
    run_module("base", tmp_project, "my-project")
    run_module("base", tmp_project, "my-project")
    content = (tmp_project / "reference.md").read_text()
    assert content.count("<!-- module:base -->") == 1


def test_python_idempotent(tmp_project):
    run_module("base", tmp_project, "my-project")
    run_module("python", tmp_project, "my-project")
    run_module("python", tmp_project, "my-project")
    content = (tmp_project / "reference.md").read_text()
    assert content.count("<!-- module:python -->") == 1
