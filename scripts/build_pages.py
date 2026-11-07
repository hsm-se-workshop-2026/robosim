"""Assemble the static GitHub Pages site and its browser-side Python modules."""

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_FILES = ("index.html", "app.js", "styles.css")
PYTHON_FILES = (
    "src/__init__.py",
    "src/browser_api.py",
    "src/adapters/__init__.py",
    "src/adapters/keyboard_control.py",
    "src/adapters/line_follower.py",
    "src/application/__init__.py",
    "src/application/ports.py",
    "src/application/simulation.py",
    "src/domain/__init__.py",
    "src/domain/robot.py",
    "src/domain/track.py",
)


def build_pages(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name in SITE_FILES:
        shutil.copy2(ROOT / "site" / name, output / name)
    for name in PYTHON_FILES:
        destination = output / "python" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, destination)
    (output / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "pages",
        help="directory for the generated static site",
    )
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build_pages(output)
    print(f"GitHub Pages site generated in {output}")


if __name__ == "__main__":
    main()
