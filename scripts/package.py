#!/usr/bin/env python3
"""Package explicit public paths, never personal runtime data or Git history."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = {"README.md", "LICENSE", "CONTRIBUTING.md", ".gitignore", "catalog.json"}
TOP_DIRS = {"skills", "scripts", "docs", "examples", "evals", "tests", ".github"}
SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml"}


def public_files():
    result = {}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "__pycache__"} for part in relative.parts) or path.suffix == ".pyc":
            continue
        if relative.parts[0] not in TOP_FILES | TOP_DIRS:
            continue
        if path.is_symlink():
            raise ValueError(f"Refusing symlink: {relative}")
        if not path.is_file():
            continue
        if relative.as_posix() not in TOP_FILES and path.name != "LICENSE" and path.suffix not in SUFFIXES:
            raise ValueError(f"Unexpected public file type: {relative}")
        result[relative.as_posix()] = path.read_bytes()
    return result


def write_zip(path, files):
    if path.exists():
        raise ValueError(f"Output already exists: {path}")
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED, strict_timestamps=False) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def package(output):
    output = Path(output).expanduser().resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Output must be outside the source tree.")
    source = public_files()
    catalog = json.loads(source["catalog.json"])
    output.mkdir(parents=True, exist_ok=True)
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in source.items()}
    full = {f"exobrain-skill/{name}": data for name, data in source.items()}
    full["exobrain-skill/SHA256SUMS.txt"] = "".join(f"{sha}  {name}\n" for name, sha in manifest.items()).encode()
    archives = [(f"exobrain-skill-v{catalog['version']}.zip", full)]
    for entry in catalog["skills"]:
        name, prefix = entry["name"], entry["path"] + "/"
        files = {name + "/" + path.removeprefix(prefix): data
                 for path, data in source.items() if path.startswith(prefix)}
        if f"{name}/SKILL.md" not in files:
            raise ValueError(f"Incomplete skill: {name}")
        files[f"{name}/LICENSE"] = source["LICENSE"]
        archives.append((f"{name}-skill-v{entry['version']}.zip", files))
    if any((output / name).exists() for name, _ in archives) or (output / "manifest.json").exists():
        raise ValueError("Release output already exists; select a fresh directory.")
    for name, files in archives:
        write_zip(output / name, files)
    report = {"version": catalog["version"], "public_file_count": len(source), "files": manifest,
              "archives": {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                           for name, _ in archives}}
    (output / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="Output directory outside the public source tree")
    args = parser.parse_args()
    report = package(args.output)
    print(json.dumps({"public_file_count": report["public_file_count"], "archives": report["archives"]}, indent=2))


if __name__ == "__main__":
    main()
