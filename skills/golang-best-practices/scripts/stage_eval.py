#!/usr/bin/env python3
"""Stage isolated eval inputs without exposing grader criteria to the agent."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", dest="case_ids", help="Case ID; repeat to select several. Defaults to all.")
    parser.add_argument("--output", type=Path, help="New staging directory; must not already exist.")
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[1]
    suite = json.loads((skill / "evals/evals.json").read_text())
    cases = suite["cases"]
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        parser.error("Evaluation case IDs must be unique")
    selected = set(args.case_ids or ids)
    unknown = selected.difference(ids)
    if unknown:
        parser.error("Unknown case IDs: " + ", ".join(sorted(unknown)))
    cases = [case for case in cases if case["id"] in selected]
    for case in cases:
        if not case["id"] or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in case["id"]):
            parser.error("Case IDs must contain lowercase letters, digits, or hyphens")
        for name in case["files"]:
            path = PurePosixPath(name)
            if not name or path.is_absolute() or ".." in path.parts or "\\" in name or not path.parts:
                parser.error(f"Unsafe fixture path: {name!r}")
    if args.output:
        root = args.output.resolve()
        root.mkdir(parents=True, exist_ok=False)
    else:
        root = Path(tempfile.mkdtemp(prefix="golang-skill-eval-"))
    instructions = [skill / "SKILL.md"] + sorted((skill / "references").rglob("*.md"))
    hashes = {str(path.relative_to(skill)): hashlib.sha256(path.read_bytes()).hexdigest() for path in instructions}
    for case in cases:
        target = root / case["id"]
        workspace = target / "workspace"
        workspace.mkdir(parents=True)
        for name, content in case["files"].items():
            path = workspace / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        for instruction in instructions:
            destination = target / instruction.relative_to(skill)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(instruction, destination)
        (target / "task.txt").write_text(case["prompt"] + "\n")
    metadata = {
        "case_ids": [case["id"] for case in cases],
        "instruction_files": hashes,
        "instruction_snapshot_sha256": hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(),
        "eval_suite_sha256": hashlib.sha256((skill / "evals/evals.json").read_bytes()).hexdigest(),
    }
    (root / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(root)


if __name__ == "__main__":
    main()
