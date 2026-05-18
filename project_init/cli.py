import argparse
from pathlib import Path
from project_init.runner import run


def main():
    parser = argparse.ArgumentParser(
        prog="project-init",
        description="Scaffold a new project with git, tooling, and agent protocols.",
    )
    parser.add_argument("name", help="Project directory name")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Parent directory for the new project (default: cwd)",
    )
    parser.add_argument(
        "--no-python", action="store_true", help="Skip the python module"
    )
    parser.add_argument("--cas", action="store_true")
    parser.add_argument("--exptracking", action="store_true")
    parser.add_argument("--security", action="store_true")
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="Load flags from profiles/<name>.flags",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()