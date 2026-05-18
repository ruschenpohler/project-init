from pathlib import Path


def assert_dispatcher_exists(project_root: Path):
    dispatcher = project_root / ".git" / "hooks" / "pre-commit"
    if not dispatcher.exists():
        raise RuntimeError(
            f"Dispatcher not found at {dispatcher}. Run base module first."
        )


def append_fragment(ref_path: Path, fragment_path: Path, module_name: str):
    sentinel = f"<!-- module:{module_name} -->"
    content = ref_path.read_text()
    if sentinel in content:
        return
    fragment = fragment_path.read_text()
    with ref_path.open("a") as f:
        f.write(f"\n{sentinel}\n")
        f.write(fragment)
        f.write("\n")