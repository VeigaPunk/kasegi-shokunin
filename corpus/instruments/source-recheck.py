#!/usr/bin/env python3
"""Recheck pinned quotes against checked-in source snapshots.

Usage: python3 corpus/instruments/source-recheck.py --manifest PATH [--source ID]
       python3 corpus/instruments/source-recheck.py --selftest

Manifest paths are relative to the manifest directory. This instrument reads
only local files; a successful check verifies captured bytes, not current
upstream availability or freshness.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA_VERSION = 1
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
MARKUP_RE = re.compile(r"</?u>")


def normalize(text):
    """Collapse whitespace and drop capture markup (<u>/</u>) before matching."""
    return " ".join(MARKUP_RE.sub("", text).split())


def emit(out, stable_id, status, detail=""):
    line = f"{stable_id} {status}"
    if detail:
        line += f" {detail}"
    print(line, file=out)


def valid_id(value):
    return isinstance(value, str) and ID_RE.fullmatch(value) is not None


def load_manifest(path, out):
    try:
        manifest_path = Path(path).resolve(strict=True)
        raw = manifest_path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
    except FileNotFoundError:
        emit(out, "manifest", "UNAVAILABLE", "reason=missing")
        return None, None
    except (OSError, UnicodeError, json.JSONDecodeError):
        emit(out, "manifest", "UNAVAILABLE", "reason=unreadable-or-invalid")
        return None, None

    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != SCHEMA_VERSION:
        emit(out, "manifest", "UNAVAILABLE", "reason=unsupported-schema")
        return None, None
    records = data.get("sources")
    if not isinstance(records, list) or not records:
        emit(out, "manifest", "UNAVAILABLE", "reason=missing-sources")
        return None, None

    seen = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict) or not valid_id(record.get("id")):
            emit(out, f"manifest:record-{index}", "UNAVAILABLE", "reason=invalid-source-id")
            return None, None
        if record["id"] in seen:
            emit(out, "manifest", "UNAVAILABLE", "reason=duplicate-source-id")
            return None, None
        seen.add(record["id"])

    return manifest_path, records


def check_source(manifest_path, record, out):
    source_id = record["id"]
    path = record.get("path")
    if not isinstance(path, str) or not path or Path(path).is_absolute():
        emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=invalid-path")
        return 2

    expected = record.get("sha256")
    if not isinstance(expected, str) or SHA256_RE.fullmatch(expected) is None:
        emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=invalid-sha256")
        return 2

    quotes = record.get("quotes")
    if not isinstance(quotes, list) or not quotes:
        emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=missing-quotes")
        return 2
    quote_ids = set()
    for index, assertion in enumerate(quotes, start=1):
        if not isinstance(assertion, dict) or not valid_id(assertion.get("id")):
            emit(out, f"{source_id}:quote-{index}", "UNAVAILABLE", "reason=invalid-quote-id")
            return 2
        if assertion["id"] in quote_ids:
            emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=duplicate-quote-id")
            return 2
        quote_ids.add(assertion["id"])
        if not isinstance(assertion.get("quote"), str) or not assertion["quote"]:
            emit(out, f"{source_id}:{assertion['id']}", "UNAVAILABLE", "reason=empty-quote")
            return 2

    base = manifest_path.parent
    try:
        base = base.resolve(strict=True)
        resolved = (base / path).resolve(strict=True)
        if os.path.commonpath((str(base), str(resolved))) != str(base):
            emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=outside-manifest-directory")
            return 2
        source_bytes = resolved.read_bytes()
    except FileNotFoundError:
        emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=missing")
        return 2
    except (OSError, RuntimeError, ValueError):
        emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=unreadable")
        return 2

    actual = hashlib.sha256(source_bytes).hexdigest()
    if actual != expected:
        emit(out, f"{source_id}:sha256", "MISMATCH", f"expected={expected} actual={actual}")
        return 1

    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError:
        emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=not-utf8")
        return 2

    emit(out, f"{source_id}:sha256", "OK")
    status = 0
    for assertion in sorted(quotes, key=lambda item: item["id"]):
        quote_id = assertion["id"]
        if assertion["quote"] in source_text:
            emit(out, f"{source_id}:{quote_id}", "OK")
        elif normalize(assertion["quote"]) and normalize(assertion["quote"]) in normalize(source_text):
            # Declared normalization (considerthese/2026-10-24 proposal 1):
            # reader captures carry markup such as <u>…</u>; the receipt names
            # the transformation instead of forcing the entry to quote tags.
            emit(out, f"{source_id}:{quote_id}", "OK", "normalized=markup-whitespace")
        else:
            emit(out, f"{source_id}:{quote_id}", "MISMATCH", "reason=quote-not-found")
            status = 1
    return status


def recheck(manifest_arg, source_id, out=sys.stdout):
    if source_id is not None and not valid_id(source_id):
        emit(out, "manifest:selection", "UNAVAILABLE", "reason=invalid-source-id")
        return 2

    manifest_path, records = load_manifest(manifest_arg, out)
    if records is None:
        return 2

    if source_id is not None:
        records = [record for record in records if record["id"] == source_id]
        if not records:
            emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=not-listed")
            return 2

    status = 0
    for record in sorted(records, key=lambda item: item["id"]):
        result = check_source(manifest_path, record, out)
        if result == 2:
            status = 2
        elif result == 1 and status == 0:
            status = 1
    return status


def selftest(out=sys.stdout):
    script = Path(__file__).resolve()
    payload = b"Captured fixture supports a verifiable local rule.\n"
    snapshot_digest = hashlib.sha256(payload).hexdigest()
    with tempfile.TemporaryDirectory(prefix="source-recheck-") as directory:
        root = Path(directory)
        manifest_path = root / "manifest.json"
        source_path = root / "S900.txt"
        source_path.write_bytes(payload)
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "sources": [{
                "id": "S900",
                "path": source_path.name,
                "sha256": snapshot_digest,
                "quotes": [{
                    "id": "Q1",
                    "quote": "verifiable local rule",
                    "location": "fixture line 1",
                }],
            }],
        }
        manifest_path.write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")

        cases = []

        def run_case(name, manifest_arg, expected_status, expected_ids):
            try:
                result = subprocess.run(
                    [sys.executable, str(script), "--manifest", str(manifest_arg), "--source", "S900"],
                    cwd=str(root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                )
                observed_ids = [line.split(maxsplit=1)[0] for line in result.stdout.splitlines() if line.strip()]
                passed = (result.returncode == expected_status and observed_ids == expected_ids and not result.stderr)
                observed_status = result.returncode
            except OSError:
                passed = False
                observed_ids = []
                observed_status = "unavailable"
            state = "PASS" if passed else "FAIL"
            print(
                f"SELFTEST {name} {state} expected-exit={expected_status} observed-exit={observed_status} "
                f"expected-ids={','.join(expected_ids)} observed-ids={','.join(observed_ids)}",
                file=out,
            )
            cases.append(passed)

        run_case("clean", manifest_path, 0, ["S900:sha256", "S900:Q1"])

        source_path.write_bytes(payload + b"corruption\n")
        run_case("corrupt", manifest_path, 1, ["S900:sha256"])

        source_path.unlink()
        run_case("missing-source", manifest_path, 2, ["S900:source"])

        run_case("missing-manifest", root / "absent.json", 2, ["manifest"])

    return 0 if all(cases) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Recheck exact quotes in pinned local source snapshots.")
    parser.add_argument("--manifest", help="JSON manifest with local source paths, SHA-256 pins, and quote assertions")
    parser.add_argument("--source", help="check one source ID from the manifest")
    parser.add_argument("--selftest", action="store_true", help="run isolated clean, corrupt, and missing-file controls")
    args = parser.parse_args(argv)

    if args.selftest:
        if args.manifest is not None or args.source is not None:
            emit(sys.stdout, "manifest:selection", "UNAVAILABLE", "reason=selftest-takes-no-manifest-or-source")
            return 2
        return selftest()
    if args.manifest is None:
        emit(sys.stdout, "manifest", "UNAVAILABLE", "reason=missing-required-argument")
        return 2
    return recheck(args.manifest, args.source)


if __name__ == "__main__":
    sys.exit(main())
