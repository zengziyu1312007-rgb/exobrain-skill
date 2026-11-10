#!/usr/bin/env python3
"""Install the complete local skill without downloading or replacing existing files."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "my-exobrain"


def skill_sources():
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return {entry["name"]: ROOT / entry["path"] for entry in catalog["skills"]}


def inventory(folder):
    result = {}
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError("技能包含符号链接，已停止。")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def install(destination, dry_run=False, skill="my-exobrain"):
    sources = skill_sources()
    if skill not in sources:
        raise ValueError(f"未知技能：{skill}")
    source = sources[skill]
    if source.parent != ROOT / "skills" or source.name != skill:
        raise ValueError("技能路径与目录不一致。")
    raw = Path(destination).expanduser().absolute()
    if any(p.is_symlink() for p in [raw, *raw.parents]):
        raise ValueError("目标或上级目录是符号链接，请指定实际路径。")
    target = raw.resolve()
    expected = inventory(source)
    if not expected or not (source / "SKILL.md").is_file():
        raise ValueError("完整技能源文件缺失。")
    if target == source or source in target.parents or target in source.parents:
        raise ValueError("安装目标与源目录重叠。")
    if target.exists():
        if target.is_dir() and inventory(target) == expected:
            return "already-installed", target
        raise ValueError("目标已存在且内容不同；保留原文件，不自动覆盖。请先检查并备份旧版。")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if inventory(target) != expected:
            raise ValueError("安装后校验未通过；文件保留在目标目录，请检查。")
    return "preview" if dry_run else "installed", target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("codex", "claude"), default="codex")
    parser.add_argument("--skill", choices=tuple(skill_sources()), default="my-exobrain")
    parser.add_argument("--dest", help="自定义完整技能目录（不是个人外脑目录）")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    default = Path.home() / (".agents" if args.target == "codex" else ".claude") / "skills" / args.skill
    try:
        status, destination = install(args.dest or default, args.dry_run, args.skill)
    except (ValueError, OSError) as error:
        print(f"停止：{error}", file=sys.stderr)
        return 1
    print(f"{status}: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
