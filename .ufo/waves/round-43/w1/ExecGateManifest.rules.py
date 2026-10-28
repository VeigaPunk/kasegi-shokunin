#!/usr/bin/env python3
"""R-FILES, R-MANIFEST, R-REDACT: the package-shape half of the claim-package gate.

Sourceable fragment for corpus/instruments/claim-package-check.py (round 43).
Contract: corpus/knowledge/claim-package-contract.md ("A claim-ready package
lives at claims/<program>/<slug>/ and contains: ...") and
corpus/knowledge/claim-gates.md (the recovered ops/claim-check.mjs gate list).
The contract file is authoritative; claim-gates.md supplies the byte-level
semantics the lost executable used.

INTERFACE (splice-safe, no side effects on import)
    rule_files(root)                -> result
    rule_manifest(root[, manifest]) -> result
    rule_redact(root[, manifest])   -> result

    result = {"id": "R-FILES", "verdict": "pass"|"fail",
              "detail": "<space-separated k=v tokens>",
              "counts": {...}, "reasons": [<short codes>]}

    emit(result)        prints one `RULE <id> verdict=<v> detail=<...>` line
    run(root)           returns the three results in gate order
    main(argv)          standalone CLI: `python3 <this file> <package-dir>`

The rule functions never print and never trust package content: a manifest
digest is only ever compared against sha256 recomputed from the artifact
bytes. Every rule fails CLOSED (R30): an unreadable, unparsable or malformed
input is a FAIL, never a pass, and a raising rule becomes a FAIL, not a
traceback.

R-FILES (contract: the six-file row set)
    report.md, claim_checklist.md, evidence/manifest.json,
    custodian-receipts.json, provenance.json, status.json
  Each must be a regular file directly under the package root (not a
  directory, not a symlink -- claim-check.mjs banned blanket symlinks in its
  walk loop, and a symlinked contract file is not a file the package owns).
  Detail: files=<k>/6 missing=<n> notregular=<n>

R-MANIFEST (contract: evidence/manifest.json row)
    schema_version == "evidence-manifest/v1"; expected_head_sha256 present
    (its VALUE is R-CUSTODIAN's three-way binding); artifacts[] non-empty;
    per artifact: path is a non-empty relative path resolved against
    evidence/, with no `..` component, no absolute path, no symlink anywhere
    on the traversed chain, and a realpath that stays inside the package
    root; sha256 recomputed over the artifact bytes and compared to the
    declared digest; polarity in {positive, negative}; at least one positive.
  Detail: artifacts=<n> positive=<p> negative=<g> digest-bad=<d> escape=<e>
          missing=<m> shape=<s>

R-REDACT (contract: manifest redactions[] row)
    redactions[] is a non-empty list (`redactions: []` is never claim-ready);
    every artifact has at least one receipt whose artifact_sha256 equals the
    artifact's declared digest (and whose scanned_artifact_sha256, when
    present, equals it too -- claim-gates.md bound both to a.sha256); every
    receipt's producer and verifier identities are non-empty and distinct;
    every receipt binds a digest that some manifest artifact declares.
  Detail: redactions=<n> artifacts=<n> covered=<c> unbound=<u>
          identity-bad=<d> digest-bad=<b>

Standalone exit: 0 all three pass, 1 any fail, 2 the package dir is missing
or is not a directory. When splicing into the gate CLI, drop main() and the
__main__ block; call run()/rule_* and let the CLI own printing and exit codes.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

MANIFEST_SCHEMA = "evidence-manifest/v1"
POLARITIES = ("positive", "negative")
REQUIRED_FILES = (
    "report.md",
    "claim_checklist.md",
    "evidence/manifest.json",
    "custodian-receipts.json",
    "provenance.json",
    "status.json",
)
PRODUCER_KEYS = ("producer", "producer_identity")
VERIFIER_KEYS = ("verifier", "verifier_identity")


class _Missing:
    """Sentinel: caller did not hand us a parsed manifest."""


_UNSET = _Missing()


def _result(rule_id, reasons, counts, detail):
    reasons = sorted(set(reasons))
    return {
        "id": rule_id,
        "verdict": "fail" if reasons else "pass",
        "detail": detail,
        "counts": counts,
        "reasons": reasons,
    }


def _detail(counts, reasons):
    parts = ["%s=%s" % (key, counts[key]) for key in counts]
    reasons = sorted(set(reasons))
    if reasons:
        parts.append("fail=" + ",".join(reasons))
    return " ".join(parts)


def _is_sha256(value):
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(c in "0123456789abcdef" for c in value.lower())


def _package_root(root):
    return os.path.realpath(os.fspath(root))


def _text_path(root, rel):
    """Join a '/'-separated relative path under root without escaping it."""
    return os.path.join(root, *[part for part in rel.split("/") if part])


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_target(root, evidence, rel):
    """Resolve one artifact path. Returns (absolute_target, reason_or_None)."""
    if not isinstance(rel, str) or not rel.strip():
        return None, "empty-path"
    if os.path.isabs(rel) or rel.startswith("\\"):
        return None, "absolute-path"
    parts = [part for part in rel.split("/") if part not in ("", ".")]
    if not parts:
        return None, "empty-path"
    if ".." in parts:
        # Rejected outright: `sub/../a` resolves inside evidence/ yet still
        # walks the tree, and claim-check.mjs required the resolved path to
        # be prefixed by the package root, never a traversal.
        return None, "dotdot"
    target = os.path.join(evidence, *parts)
    walk = evidence
    for part in parts:
        walk = os.path.join(walk, part)
        if os.path.islink(walk):
            return None, "symlink"
    real_target = os.path.realpath(target)
    if real_target != root and not real_target.startswith(root + os.sep):
        return None, "outside-package"
    if not os.path.isfile(real_target):
        return None, "missing"
    return real_target, None


def _load_manifest(root, manifest):
    """Return (manifest_object, error_code). Fails closed on any read error."""
    if manifest is not _UNSET:
        if not isinstance(manifest, dict):
            return None, "manifest-unreadable"
        return manifest, None
    path = _text_path(root, "evidence/manifest.json")
    try:
        with open(path, "rb") as handle:
            payload = json.loads(handle.read().decode("utf-8"))
    except OSError:
        return None, "manifest-unreadable"
    except (UnicodeDecodeError, ValueError):
        return None, "manifest-unparsable"
    if not isinstance(payload, dict):
        return None, "manifest-shape"
    return payload, None


def rule_files(root):
    """R-FILES: the six contract files exist as regular files in the package."""
    counts = {"files": "0/6", "missing": len(REQUIRED_FILES), "notregular": 0}
    try:
        root = os.path.realpath(os.fspath(root))
        if not os.path.isdir(root):
            raise ValueError("not a directory")
    except (TypeError, ValueError):
        return _result("R-FILES", ["package-unreadable"], counts,
                       _detail(counts, ["package-unreadable"]))
    missing = []
    notregular = []
    for rel in REQUIRED_FILES:
        path = _text_path(root, rel)
        if os.path.islink(path) or (os.path.exists(path) and not os.path.isfile(path)):
            notregular.append(rel)
            if not os.path.isfile(path):
                missing.append(rel)
        elif not os.path.isfile(path):
            missing.append(rel)
    reasons = []
    if missing:
        reasons.append("missing-file")
    if notregular:
        reasons.append("not-regular-file")
    counts = {"files": "%d/%d" % (len(REQUIRED_FILES) - len(missing), len(REQUIRED_FILES)),
              "missing": len(missing),
              "notregular": len(notregular)}
    return _result("R-FILES", reasons, counts, _detail(counts, reasons))


def rule_manifest(root, manifest=_UNSET):
    """R-MANIFEST: schema, recomputed per-artifact digests, polarity coverage."""
    counts = {"artifacts": 0, "positive": 0, "negative": 0,
              "digest-bad": 0, "escape": 0, "missing": 0, "shape": 0}
    try:
        root = _package_root(root)
        manifest, error = _load_manifest(root, manifest)
    except (TypeError, ValueError):
        manifest, error = None, "package-unreadable"
    reasons = []
    if error:
        reasons.append(error)
        return _result("R-MANIFEST", reasons, counts, _detail(counts, reasons))
    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        reasons.append("schema-version")
    head = manifest.get("expected_head_sha256")
    if not isinstance(head, str) or not head.strip():
        reasons.append("head-missing")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        reasons.append("artifacts-empty")
        artifacts = []
    evidence = os.path.join(root, "evidence")
    if os.path.islink(evidence) or not os.path.isdir(evidence):
        reasons.append("evidence-dir")
        counts["escape"] = len(artifacts)
        artifacts = []
    counts["artifacts"] = len(artifacts)
    for entry in artifacts:
        if not isinstance(entry, dict):
            counts["shape"] += 1
            continue
        polarity = entry.get("polarity")
        if polarity in POLARITIES:
            counts[polarity] += 1
        else:
            counts["shape"] += 1
        declared = entry.get("sha256")
        target, path_error = _artifact_target(root, evidence, entry.get("path"))
        if path_error == "empty-path":
            counts["shape"] += 1
            continue
        if path_error == "missing":
            counts["missing"] += 1
            continue
        if path_error:
            counts["escape"] += 1
            continue
        if not _is_sha256(declared):
            counts["digest-bad"] += 1
            continue
        try:
            swept = _sha256_file(target)
        except OSError:
            counts["digest-bad"] += 1
            continue
        if swept != declared.lower():
            counts["digest-bad"] += 1
    if counts["shape"]:
        reasons.append("artifact-shape")
    if counts["escape"]:
        reasons.append("path-escape")
    if counts["missing"]:
        reasons.append("artifact-missing")
    if counts["digest-bad"]:
        reasons.append("digest-mismatch")
    if artifacts and counts["positive"] == 0:
        reasons.append("no-positive")
    return _result("R-MANIFEST", reasons, counts, _detail(counts, reasons))


def _identity(entry, keys):
    for key in keys:
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def rule_redact(root, manifest=_UNSET):
    """R-REDACT: one same-digest receipt per artifact, two distinct identities."""
    counts = {"redactions": 0, "artifacts": 0, "covered": 0,
              "unbound": 0, "identity-bad": 0, "digest-bad": 0}
    try:
        root = _package_root(root)
        manifest, error = _load_manifest(root, manifest)
    except (TypeError, ValueError):
        manifest, error = None, "package-unreadable"
    reasons = []
    if error:
        reasons.append(error)
        return _result("R-REDACT", reasons, counts, _detail(counts, reasons))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        artifacts = []
    declared = []
    for entry in artifacts:
        if isinstance(entry, dict) and _is_sha256(entry.get("sha256")):
            declared.append(entry["sha256"].lower())
    counts["artifacts"] = len(declared)
    receipts = manifest.get("redactions")
    if not isinstance(receipts, list):
        reasons.append("redactions-shape")
        receipts = []
    counts["redactions"] = len(receipts)
    if not receipts:
        reasons.append("empty-redactions")
    covered = set()
    for receipt in receipts:
        if not isinstance(receipt, dict):
            counts["identity-bad"] += 1
            continue
        digest = receipt.get("artifact_sha256")
        scanned = receipt.get("scanned_artifact_sha256")
        digest = digest.lower() if _is_sha256(digest) else ""
        if not digest:
            counts["digest-bad"] += 1
        if scanned is not None:
            scanned = scanned.lower() if _is_sha256(scanned) else ""
            if not scanned or scanned != digest:
                counts["digest-bad"] += 1
        bound = digest in declared
        if not bound:
            counts["unbound"] += 1
        producer = _identity(receipt, PRODUCER_KEYS)
        verifier = _identity(receipt, VERIFIER_KEYS)
        if not producer or not verifier or producer == verifier:
            counts["identity-bad"] += 1
            continue
        if bound:
            covered.add(digest)
    counts["covered"] = sum(1 for digest in declared if digest in covered)
    uncovered = counts["artifacts"] - counts["covered"]
    if counts["digest-bad"]:
        reasons.append("receipt-digest")
    if counts["unbound"]:
        reasons.append("unbound-receipt")
    if counts["identity-bad"]:
        reasons.append("identity")
    if uncovered > 0:
        reasons.append("uncovered-artifact")
        counts["uncovered"] = uncovered
    return _result("R-REDACT", reasons, counts, _detail(counts, reasons))


def run(root):
    """Run the three rules in gate order over one package dir."""
    return [rule_files(root), rule_manifest(root), rule_redact(root)]


def emit(result):
    """Print one CLI line: RULE <id> verdict=pass|fail detail=<short>."""
    print("RULE %s verdict=%s detail=%s"
          % (result["id"], result["verdict"], result["detail"]))


def main(argv):
    if len(argv) != 1:
        sys.stderr.write("usage: %s <package-dir>\n" % os.path.basename(sys.argv[0]))
        return 2
    root = argv[0]
    if not os.path.isdir(root):
        print("package=%s verdict=ERROR" % root)
        return 2
    results = run(root)
    for result in results:
        emit(result)
    return 0 if all(result["verdict"] == "pass" for result in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
