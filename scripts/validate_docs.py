#!/usr/bin/env python3
"""Validate public benchmark documentation and metadata consistency."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - CI normally has PyYAML
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS = ROOT / "benchmarks"
REQUIRED = {
    "title", "family", "difficulty", "estimated_minutes", "capabilities",
    "entrypoint", "public_ports", "milestones", "public_objective",
    "operator_evaluator",
}
SECTIONS = [
    "Overview", "Capability under evaluation", "Difficulty and estimated duration",
    "Starting conditions", "Target topology", "Exposed ports", "Objective",
    "Milestones and scoring categories", "Running locally", "Health checks",
    "Reset and cleanup", "Safety notes", "Related evaluator",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_yaml(path: Path) -> dict:
    if yaml:
        with path.open() as handle:
            return yaml.safe_load(handle) or {}
    # Minimal fallback for the flat metadata fields used here.
    data = {}
    active_list = None
    for line in path.read_text().splitlines():
        if line.startswith("  - ") and active_list:
            data[active_list].append(line[4:].strip().strip("'\""))
            continue
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if value == "[]":
                data[key] = []
                active_list = key
            elif value:
                data[key] = value
                active_list = None
            else:
                data[key] = []
                active_list = key
    return data


def compose_ports(path: Path) -> set[int]:
    ports = set()
    if not path.is_file():
        return ports
    for line in path.read_text().splitlines():
        match = re.search(r'[- ]+["\']?(\d+):\d+["\']?', line)
        if match:
            ports.add(int(match.group(1)))
    return ports


def public_markdown() -> list[Path]:
    return [*BENCHMARKS.rglob("README.md"), *(ROOT / "docs").glob("*.md"), ROOT / "README.md"]


def main() -> int:
    errors: list[str] = []
    metadata: list[tuple[Path, dict]] = []
    ids: dict[str, Path] = {}
    for challenge in sorted(BENCHMARKS.rglob("challenge.yaml")):
        data = load_yaml(challenge)
        metadata.append((challenge, data))
        missing = REQUIRED - set(data)
        if missing:
            fail(errors, f"{challenge}: missing metadata fields: {', '.join(sorted(missing))}")
        ident = data.get("id")
        if ident in ids:
            fail(errors, f"duplicate benchmark ID {ident!r}: {ids[ident]} and {challenge}")
        ids[ident] = challenge
        readme = challenge.parent / "README.md"
        if not readme.exists():
            fail(errors, f"{challenge.parent}: missing README.md")
        else:
            text = readme.read_text()
            for section in SECTIONS:
                if f"## {section}" not in text:
                    fail(errors, f"{readme}: missing section {section!r}")
        compose = challenge.parent / str(data.get("compose", ""))
        expected = set(int(p) for p in data.get("public_ports", []) or [])
        actual = compose_ports(compose)
        if compose.is_file() and expected != actual:
            fail(errors, f"{challenge}: public_ports {sorted(expected)} != Compose host ports {sorted(actual)}")
        if not compose.exists() and expected:
            fail(errors, f"{challenge}: documents ports but Compose file is absent")

    public_text = "\n".join(path.read_text(errors="replace") for path in public_markdown() if path.exists())
    leaked = sorted(set(re.findall(r"FLAG\{[^}\n]+\}", public_text)))
    if leaked:
        fail(errors, "exact flag values found in public documentation: " + ", ".join(leaked))

    for document in public_markdown():
        if not document.exists():
            continue
        for link in re.findall(r"\]\(([^)]+)\)", document.read_text(errors="replace")):
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (document.parent / link.split("#", 1)[0]).resolve()
            if not target.exists():
                fail(errors, f"{document}: broken link {link}")

    catalog = ROOT / "docs" / "benchmark-catalog.md"
    if not catalog.exists():
        fail(errors, f"missing catalog: {catalog}")
    else:
        catalog_text = catalog.read_text()
        for ident, challenge in ((data.get("id"), path) for path, data in metadata):
            if ident not in catalog_text:
                fail(errors, f"{catalog}: missing benchmark ID {ident}")
        for link in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", catalog_text):
            target = (catalog.parent / link).resolve()
            if not target.exists():
                fail(errors, f"{catalog}: broken link {link}")

    if errors:
        print("Documentation validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Documentation validation passed for {len(metadata)} benchmarks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
