from pathlib import Path
import subprocess
import importlib.util

MODULES_DIR = Path(__file__).resolve().parent.parent / "modules"
PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles"

MODULE_ORDER = ["base", "python", "cas", "exptracking", "security"]


def resolve_flags(args) -> dict:
    flags = {
        "python": not args.no_python,
        "cas": args.cas,
        "exptracking": args.exptracking,
        "security": args.security,
    }
    if args.profile:
        profile_path = PROFILES_DIR / f"{args.profile}.flags"
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {profile_path}")
        for line in profile_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line == "--no-python":
                flags["python"] = False
            else:
                key = line.lstrip("-")
                flags[key] = True
    return flags


def run(args):
    project_root = Path(args.path) / args.name
    if project_root.exists():
        raise FileExistsError(f"Directory already exists: {project_root}")
    project_root.mkdir(parents=True)
    print(f"Created project directory: {project_root}")

    flags = resolve_flags(args)
    installed_modules = []

    run_module("base", project_root, args.name)
    installed_modules.append("base")

    dispatcher = project_root / ".git" / "hooks" / "pre-commit"
    if not dispatcher.exists():
        raise RuntimeError("base module failed to install dispatcher. Aborting.")

    for module in MODULE_ORDER[1:]:
        if flags.get(module, False):
            run_module(module, project_root, args.name)
            installed_modules.append(module)

    commit_msg = (
        f"infra: scaffold project-init with modules "
        f"[{', '.join(installed_modules)}] [1]"
    )
    subprocess.run(["git", "-C", str(project_root), "add", "-A"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(project_root),
            "commit",
            "--no-verify",
            "-m",
            commit_msg,
        ],
        check=True,
    )
    print(f"\nDone. Project scaffolded at: {project_root}")
    print(f"Modules installed: {', '.join(installed_modules)}")


def run_module(module_name: str, project_root: Path, project_name: str):
    install_path = MODULES_DIR / module_name / "install.py"
    if not install_path.exists():
        raise FileNotFoundError(f"No install.py for module: {module_name}")
    spec = importlib.util.spec_from_file_location(
        f"install_{module_name}", install_path
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.install(project_root=project_root, project_name=project_name)
    print(f"  [ok] {module_name}")
