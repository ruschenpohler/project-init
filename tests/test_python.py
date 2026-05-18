from project_init.runner import run_module


def test_python_creates_pyproject(tmp_project):
    run_module("base", tmp_project, "my-project")
    run_module("python", tmp_project, "my-project")
    pyproject = tmp_project / "pyproject.toml"
    assert pyproject.exists()
    assert "my-project" in pyproject.read_text()


def test_python_substitutes_project_name(tmp_project):
    run_module("base", tmp_project, "my-project")
    run_module("python", tmp_project, "my-project")
    content = (tmp_project / "pyproject.toml").read_text()
    assert "{{PROJECT_NAME}}" not in content


def test_python_creates_src_structure(tmp_project):
    run_module("base", tmp_project, "my-project")
    run_module("python", tmp_project, "my-project")
    assert (tmp_project / "src" / "my_project" / "__init__.py").exists()


def test_python_installs_hooks(tmp_project):
    run_module("base", tmp_project, "my-project")
    run_module("python", tmp_project, "my-project")
    hooks_d = tmp_project / ".git" / "hooks" / "pre-commit.d"
    assert (hooks_d / "20-ruff.sh").exists()
    assert (hooks_d / "30-pytest.sh").exists()


def test_python_appends_reference(tmp_project):
    run_module("base", tmp_project, "my-project")
    run_module("python", tmp_project, "my-project")
    content = (tmp_project / "reference.md").read_text()
    assert "<!-- module:python -->" in content