#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
EXPECTED_CHAPTERS = 71


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def count_files(pattern: str) -> int:
    return sum(1 for _ in CHAPTERS.rglob(pattern))


def check_counts() -> None:
    readmes = count_files("README.md")
    exercises = count_files("exercises.md")
    solutions = count_files("solutions.md")
    examples = sum(1 for _ in CHAPTERS.glob("part_*/chapter_*/examples/Main.hs"))
    if readmes != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} chapter README files, found {readmes}")
    if exercises != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} exercise files, found {exercises}")
    if solutions != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} solution files, found {solutions}")
    if examples != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} runnable examples, found {examples}")


def check_links() -> None:
    missing: list[tuple[str, str]] = []
    markdown_files = [ROOT / "README.md", ROOT / "START_HERE.md", ROOT / "TUTORIAL.md", ROOT / "glossary.md", ROOT / "CHECKPOINTS.md", ROOT / "ADVANCED_PROJECTS.md"]
    markdown_files.extend((ROOT / "projects").rglob("*.md"))
    markdown_files.extend(CHAPTERS.rglob("*.md"))
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#")):
                continue
            if not (path.parent / target).exists():
                missing.append((str(path.relative_to(ROOT)), target))
    if missing:
        sample = "\n".join(f"{path} -> {target}" for path, target in missing[:10])
        fail(f"missing markdown links:\n{sample}")


def check_repeated_template_text() -> None:
    repeated_patterns = [
        "初心者はHaskellを「PythonやJavaScriptの別構文」",
        "この章では、目の前のコードを「何を実行するか」",
        "Q. Haskellのコードは短いのに、なぜ説明が長いのですか？",
        "この設計は ______ を防ぐために使う。",
        "この章の判断で使う語",
        "Q. まず実装を増やしてから型を考えてもよいですか？",
        "Q. 型が通れば設計として十分ですか？",
        "作って、次のコードを置きます。",
    ]
    hits: list[str] = []
    for path in CHAPTERS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for pattern in repeated_patterns:
            if pattern in text:
                hits.append(f"{path.relative_to(ROOT)} contains repeated template text: {pattern}")
    if hits:
        sample = "\n".join(hits[:20])
        fail(f"template text remains:\n{sample}")


def check_examples_have_main() -> None:
    missing_main = []
    for path in CHAPTERS.glob("part_*/chapter_*/examples/Main.hs"):
        text = path.read_text(encoding="utf-8")
        if "main :: IO ()" not in text:
            missing_main.append(str(path.relative_to(ROOT)))
    if missing_main:
        fail("examples missing main :: IO ():\n" + "\n".join(missing_main[:20]))


def check_philosophy_sections() -> None:
    required_readme_sections = [
        "## 背景と設計思想",
        "## なぜそうすべきなのか",
        "## 他言語的な発想との違い",
    ]
    required_solution_sections = [
        "## なぜこの設計判断を選ぶのか",
    ]
    missing: list[str] = []
    for path in CHAPTERS.glob("part_*/chapter_*/README.md"):
        text = path.read_text(encoding="utf-8")
        for section in required_readme_sections:
            if section not in text:
                missing.append(f"{path.relative_to(ROOT)} missing {section}")
    for path in CHAPTERS.glob("part_*/chapter_*/solutions.md"):
        text = path.read_text(encoding="utf-8")
        for section in required_solution_sections:
            if section not in text:
                missing.append(f"{path.relative_to(ROOT)} missing {section}")
    if missing:
        fail("philosophy sections missing:\n" + "\n".join(missing[:20]))


def check_root_learning_assets() -> None:
    required = [
        ROOT / "CHECKPOINTS.md",
        ROOT / "ADVANCED_PROJECTS.md",
        ROOT / "glossary.md",
        ROOT / "projects" / "capstone" / "README.md",
        ROOT / "src" / "Tutorial" / "Capstone.hs",
        ROOT / "app" / "Main.hs",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        fail("missing required learning assets:\n" + "\n".join(missing))

    cabal = (ROOT / "haskell-complete-tutorial.cabal").read_text(encoding="utf-8")
    for required_text in ["Tutorial.Capstone", "executable capstone", "test-suite tutorial-tests"]:
        if required_text not in cabal:
            fail(f"cabal file missing {required_text}")


def main() -> None:
    check_counts()
    check_links()
    check_repeated_template_text()
    check_examples_have_main()
    check_philosophy_sections()
    check_root_learning_assets()
    print("tutorial validation passed")


if __name__ == "__main__":
    main()
