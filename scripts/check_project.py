#!/usr/bin/env python3
"""Check portable skill resources, local Markdown links and catalog references."""
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check():
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    errors = []
    names = set()
    categories = {entry["id"]: entry for entry in catalog["categories"]}
    for entry in catalog["skills"]:
        name = entry["name"]
        if name in names or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"Invalid or duplicate skill: {name}")
        names.add(name)
        if entry["path"] != f"skills/{name}":
            errors.append(f"Nonportable skill path: {name}")
        node = categories.get(entry["category"][0])
        for category in entry["category"][1:]:
            node = next((c for c in (node or {}).get("children", []) if c["id"] == category), None)
        if node is None:
            errors.append(f"Unknown category: {name}")
        skill = ROOT / entry["path"]
        if not (skill / "LICENSE").is_file() or (skill / "LICENSE").read_bytes() != (ROOT / "LICENSE").read_bytes():
            errors.append(f"Missing or inconsistent portable license: {name}")
        entrypoint = skill / "SKILL.md"
        if not entrypoint.is_file():
            errors.append(f"Missing SKILL.md: {name}")
            continue
        content = entrypoint.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        if not frontmatter or f"name: {name}\n" not in frontmatter.group(1) + "\n":
            errors.append(f"Frontmatter name mismatch: {name}")
        for path in skill.rglob("*"):
            if path.is_symlink():
                errors.append(f"Symlink in portable skill: {path.relative_to(ROOT)}")
            if path.suffix == ".md":
                for destination in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                    parsed = urlsplit(destination.strip('<>'))
                    if not parsed.scheme and parsed.path:
                        target = (path.parent / unquote(parsed.path)).resolve()
                        if target != skill and skill not in target.parents:
                            errors.append(f"Skill requires sibling/repo file: {path.relative_to(ROOT)} -> {destination}")
    actual = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir() and p.name != "__pycache__"}
    if names != actual:
        errors.append(f"Catalog differs from installed directories: {names ^ actual}")
    for path in ROOT.rglob("*.md"):
        if ".git" in path.relative_to(ROOT).parts:
            continue
        for destination in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            parsed = urlsplit(destination.strip('<>'))
            if not parsed.scheme and parsed.path and not (path.parent / unquote(parsed.path)).exists():
                errors.append(f"Broken local link: {path.relative_to(ROOT)} -> {destination}")
    roster = json.loads((ROOT / "skills/exobrain-council/references/roster.json").read_text(encoding="utf-8"))
    members = {member["id"]: member for member in roster["members"]}
    if len(members) != roster["count"]:
        errors.append("Council member count mismatch")
    used = []
    for group in roster["functions"]:
        for member in group["member_ids"]:
            used.append(member)
            if member not in members or members[member]["function_id"] != group["id"]:
                errors.append(f"Invalid council group reference: {member}")
    if len(used) != len(set(used)) or set(used) != set(members):
        errors.append("Council primary assignments do not cover each member exactly once")
    return errors


if __name__ == "__main__":
    problems = check()
    for problem in problems:
        print(problem)
    if not problems:
        print("Catalog, portable resources, local links and 24 council assignments passed.")
    raise SystemExit(bool(problems))
