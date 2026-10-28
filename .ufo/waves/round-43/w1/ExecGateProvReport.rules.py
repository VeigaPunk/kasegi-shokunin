#!/usr/bin/env python3
"""Claim-package gate rules R-PROVENANCE, R-REPORT, R-NOSECRET.

Sourceable module for corpus/instruments/claim-package-check.py.  Each rule
function takes the package directory and returns the same result dict the
sibling rule modules return:

    {"id": "<RULE-ID>", "verdict": "pass"|"fail", "detail": "<short>",
     "counts": {...}, "reasons": [...]}

`detail` is `<key>=<value>` pairs joined by spaces, plus `fail=<reason,...>`
when the rule fails, so the CLI line

    RULE <id> verdict=<pass|fail> detail=<short>

can be printed as-is.  R-NOSECRET never puts a matched value anywhere in the
result: it reports the classes that fired, the hit count and the first
file:line only.

Fail-closed (R30): a missing, unreadable, non-UTF-8 or unparseable file fails
the rule that reads it.  Only regular non-symlink files under the package
directory are opened, and R-NOSECRET fails the package on any symlink entry or
on a file over 5 MiB (the walk's non-regex gates in claim-gates.md); package
containment of manifest artifact paths belongs to R-MANIFEST.

provenance.json shape (fields from the contract; this module fixes the key
names, and the alternate keys in parentheses are read too):

    agents[]:      identity (name), requested_model, resolved_model, and a
                   transition either inline (`transition`) or via transitions[]
    transitions[]: agent (identity) naming a declared agent, requested_model,
                   resolved_model; optional when every agent is inline-covered
    commands[]:    command (cmd), exit_code (exit) - integer, bool rejected
    pin:           remote (url), commit (sha) - 7-64 hex
    policy_sha256: 64 hex
    external_effects_performed: exactly the empty list
    secrets_attestation: object with "findings": 0 or "no_secrets": true
                   (optional non-empty "by"), or a non-empty string

Standalone: `rules.py <package-dir>` prints the three RULE lines, exit 0 only
when all three pass, 1 when any fails, 2 when the package directory is absent.
"""

import argparse
import json
import os
import re
import sys

RULE_PROVENANCE = "R-PROVENANCE"
RULE_REPORT = "R-REPORT"
RULE_NOSECRET = "R-NOSECRET"

PROVENANCE_REL = "provenance.json"
REPORT_REL = "report.md"
MANIFEST_REL = "evidence/manifest.json"

HEX64_RE = re.compile(r"\A[0-9a-fA-F]{64}\Z")
COMMIT_RE = re.compile(r"\A[0-9a-fA-F]{7,64}\Z")
# A 64-hex run not embedded in a longer hex run (whole token, R41).
CITED_DIGEST_RE = re.compile(r"(?<![0-9a-fA-F])([0-9a-fA-F]{64})(?![0-9a-fA-F])")
SCOPE_EXCERPT_RE = re.compile(r"scope excerpt", re.IGNORECASE)
PROGRAM_URL_RE = re.compile(r"https://[^\s<>\"')\]]+")
NO_SUBMISSION_MARKER = "No submission performed"
MAX_SCAN_BYTES = 5 * 1024 * 1024

SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:[A-Z0-9 ]{0,40})?PRIVATE KEY-----")),
    ("op-ref", re.compile(r"op://[A-Za-z0-9._\-]+")),
    ("bearer-token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=\-]{16,}")),
    ("authorization-token",
     re.compile(r"(?i)\bauthorization\b[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=\-]{16,}")),
    ("labelled-hex",
     re.compile(r"(?i)\b(?:token|secret|password|passwd|api[_-]?key)\b"
                r"[\"']?\s*[:=]\s*[\"']?[0-9a-f]{32,}")),
    ("session-cookie",
     re.compile(r"(?i)\b(?:set-cookie|cookie)\s*:[^\n]{0,200}?"
                r"(?:session|sess|auth|sid)=[A-Za-z0-9%._\-]{16,}")),
    ("session-cookie",
     re.compile(r"(?i)\b(?:session|session_cookie|sessionid|jsessionid|phpsessid|connect\.sid)\b"
                r"[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9%._\-]{16,}")),
)

AGENT_ID_KEYS = ("identity", "name")
TRANSITION_AGENT_KEYS = ("agent", "identity")
COMMAND_KEYS = ("command", "cmd")
EXIT_KEYS = ("exit_code", "exit")
PIN_REMOTE_KEYS = ("remote", "url")
PIN_COMMIT_KEYS = ("commit", "sha")


class _Missing:
    """Sentinel: the caller did not hand us a parsed manifest."""


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


def _package_root(root):
    return os.path.realpath(os.fspath(root))


def _text_path(root, rel):
    """Join a '/'-separated relative path under ROOT without escaping it."""
    return os.path.join(root, *[part for part in rel.split("/") if part])


def _nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def _int_not_bool(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _pick(item, keys):
    for key in keys:
        if key in item:
            return item[key]
    return None


def _load_json(root, rel):
    """Return (object, reason_or_None); reads only inside ROOT."""
    path = _text_path(root, rel)
    if os.path.islink(path) or not os.path.isfile(path):
        return None, "missing"
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError:
        return None, "unreadable"
    try:
        return json.loads(raw.decode("utf-8")), None
    except (UnicodeDecodeError, ValueError):
        return None, "unparseable"


def _load_manifest(root, manifest):
    if not isinstance(manifest, _Missing):
        if not isinstance(manifest, dict):
            return None, "not-object"
        return manifest, None
    data, error = _load_json(root, MANIFEST_REL)
    if error:
        return None, error
    if not isinstance(data, dict):
        return None, "not-object"
    return data, None


def rule_provenance(root, manifest=_UNSET):
    """R-PROVENANCE: agents+models per transition, commands+exit codes, a pin,
    policy_sha256, `external_effects_performed: []`, secrets attestation."""
    counts = {"agents": 0, "transitions": 0, "commands": 0}
    try:
        root = _package_root(root)
        data, error = _load_json(root, PROVENANCE_REL)
    except (TypeError, ValueError):
        data, error = None, "package-unreadable"
    if error:
        return _result(RULE_PROVENANCE, [error], counts, _detail(counts, [error]))
    if not isinstance(data, dict):
        return _result(RULE_PROVENANCE, ["not-object"], counts,
                       _detail(counts, ["not-object"]))

    reasons = []
    agents = data.get("agents")
    agent_ids = []
    inline_transitions = set()
    if not isinstance(agents, list) or not agents:
        reasons.append("agents-empty")
    else:
        for agent in agents:
            if not isinstance(agent, dict):
                reasons.append("agent-not-object")
                continue
            ident = _pick(agent, AGENT_ID_KEYS)
            if not _nonempty_str(ident):
                reasons.append("agent-identity-empty")
                continue
            if ident in agent_ids:
                reasons.append("agent-duplicate")
            agent_ids.append(ident)
            for field in ("requested_model", "resolved_model"):
                if not _nonempty_str(agent.get(field)):
                    reasons.append("agent-%s-empty" % field)
            if _nonempty_str(agent.get("transition")):
                inline_transitions.add(ident)

    transitions = data.get("transitions")
    covered = set()
    if isinstance(transitions, list) and transitions:
        for trans in transitions:
            if not isinstance(trans, dict):
                reasons.append("transition-not-object")
                continue
            ref = _pick(trans, TRANSITION_AGENT_KEYS)
            if not _nonempty_str(ref) or ref not in agent_ids:
                reasons.append("transition-agent-unknown")
            else:
                covered.add(ref)
            for field in ("requested_model", "resolved_model"):
                if not _nonempty_str(trans.get(field)):
                    reasons.append("transition-%s-empty" % field)
        for ident in agent_ids:
            if ident not in covered and ident not in inline_transitions:
                reasons.append("agent-without-transition")
    elif transitions is None or (isinstance(transitions, list) and not transitions):
        if not agent_ids or any(ident not in inline_transitions
                                for ident in agent_ids):
            reasons.append("transitions-empty")
    else:
        reasons.append("transitions-shape")

    commands = data.get("commands")
    if not isinstance(commands, list) or not commands:
        reasons.append("commands-empty")
        commands = []
    else:
        for command in commands:
            if not isinstance(command, dict):
                reasons.append("command-not-object")
                continue
            if not _nonempty_str(_pick(command, COMMAND_KEYS)):
                reasons.append("command-text-empty")
            if not _int_not_bool(_pick(command, EXIT_KEYS)):
                reasons.append("command-exit-code-invalid")

    pin = data.get("pin")
    if not isinstance(pin, dict):
        reasons.append("pin-missing")
    else:
        if not _nonempty_str(_pick(pin, PIN_REMOTE_KEYS)):
            reasons.append("pin-remote-empty")
        commit = _pick(pin, PIN_COMMIT_KEYS)
        if not (isinstance(commit, str) and COMMIT_RE.match(commit)):
            reasons.append("pin-commit-invalid")

    policy = data.get("policy_sha256")
    if not (isinstance(policy, str) and HEX64_RE.match(policy)):
        reasons.append("policy-sha256-invalid")

    if "external_effects_performed" not in data:
        reasons.append("external-effects-absent")
    elif (not isinstance(data["external_effects_performed"], list)
          or data["external_effects_performed"]):
        reasons.append("external-effects-not-empty-list")

    attestation = data.get("secrets_attestation")
    if isinstance(attestation, str):
        if not _nonempty_str(attestation):
            reasons.append("attestation-empty")
    elif isinstance(attestation, dict):
        if not attestation:
            reasons.append("attestation-empty")
        else:
            findings = attestation.get("findings", _UNSET)
            no_secrets = attestation.get("no_secrets", _UNSET)
            clean = (no_secrets is True
                     or (_int_not_bool(findings) and findings == 0))
            if not clean:
                reasons.append("attestation-not-clean")
            if "by" in attestation and not _nonempty_str(attestation.get("by")):
                reasons.append("attestation-by-empty")
    else:
        reasons.append("attestation-missing")

    counts["agents"] = len(agent_ids)
    counts["transitions"] = (len(transitions) if isinstance(transitions, list)
                             else len(inline_transitions))
    counts["commands"] = len(commands)
    return _result(RULE_PROVENANCE, reasons, counts, _detail(counts, reasons))


def _manifest_digests(manifest):
    digests = set()

    def add(value):
        if isinstance(value, str) and HEX64_RE.match(value):
            digests.add(value.lower())

    add(manifest.get("expected_head_sha256"))
    for artifact in manifest.get("artifacts") or []:
        if isinstance(artifact, dict):
            add(artifact.get("sha256"))
    for receipt in manifest.get("redactions") or []:
        if isinstance(receipt, dict):
            for key in ("artifact_sha256", "scanned_artifact_sha256", "sha256"):
                add(receipt.get(key))
    return digests


def rule_report(root, manifest=_UNSET):
    """R-REPORT: `Scope excerpt`, literal `No submission performed`, a program
    URL, and every cited 64-hex digest present in evidence/manifest.json."""
    counts = {"cited": 0, "manifest": 0, "absent": 0}
    try:
        root = _package_root(root)
    except (TypeError, ValueError):
        root = ""
    path = _text_path(root, REPORT_REL)
    if os.path.islink(path) or not os.path.isfile(path):
        return _result(RULE_REPORT, ["report-missing"], counts,
                       _detail(counts, ["report-missing"]))
    try:
        with open(path, "rb") as handle:
            report = handle.read().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return _result(RULE_REPORT, ["report-unreadable"], counts,
                       _detail(counts, ["report-unreadable"]))

    manifest_data, error = _load_manifest(root, manifest)
    if error:
        reason = "manifest-" + error
        return _result(RULE_REPORT, [reason], counts, _detail(counts, [reason]))

    reasons = []
    if not SCOPE_EXCERPT_RE.search(report):
        reasons.append("scope-excerpt-absent")
    if NO_SUBMISSION_MARKER not in report:
        reasons.append("no-submission-marker-absent")
    if not PROGRAM_URL_RE.search(report):
        reasons.append("program-url-absent")

    cited = sorted({digest.lower() for digest in CITED_DIGEST_RE.findall(report)})
    known = _manifest_digests(manifest_data)
    absent = [digest for digest in cited if digest not in known]
    if absent:
        reasons.append("cited-digest-absent")
    if not cited:
        reasons.append("no-cited-digest")

    counts["cited"] = len(cited)
    counts["manifest"] = len(known)
    counts["absent"] = len(absent)
    return _result(RULE_REPORT, reasons, counts, _detail(counts, reasons))


def _scan_text(text):
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                hits.append((label, lineno))
    return hits


def rule_nosecret(root, manifest=_UNSET):
    """R-NOSECRET: secret-shaped-token scan over the package text plus the
    walk's non-regex gates (no symlink entry, nothing over 5 MiB).  Reports the
    classes that fired and where, never the matched value."""
    counts = {"files": 0, "hits": 0, "symlinks": 0, "oversize": 0,
              "classes": "none"}
    try:
        root = _package_root(root)
    except (TypeError, ValueError):
        return _result(RULE_NOSECRET, ["package-unreadable"], counts,
                       _detail(counts, ["package-unreadable"]))
    reasons = []
    hits = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        kept = []
        for name in sorted(dirnames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                counts["symlinks"] += 1
            else:
                kept.append(name)
        dirnames[:] = kept
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                counts["symlinks"] += 1
                continue
            if not os.path.isfile(path):
                continue
            try:
                if os.path.getsize(path) > MAX_SCAN_BYTES:
                    counts["oversize"] += 1
                    continue
                with open(path, "rb") as handle:
                    raw = handle.read()
            except OSError:
                reasons.append("unreadable-file")
                continue
            counts["files"] += 1
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            for label, lineno in _scan_text(raw.decode("utf-8", "replace")):
                hits.append((rel, lineno, label))

    if counts["symlinks"]:
        reasons.append("symlink-entry")
    if counts["oversize"]:
        reasons.append("oversize-file")
    counts["hits"] = len(hits)
    if hits:
        counts["classes"] = "+".join(sorted({hit[2] for hit in hits}))
        counts["at"] = "%s:%d" % (hits[0][0].replace(" ", "_"), hits[0][1])
        reasons.append("secret-shaped-token")
    return _result(RULE_NOSECRET, reasons, counts, _detail(counts, reasons))


RULES = ((RULE_PROVENANCE, rule_provenance),
         (RULE_REPORT, rule_report),
         (RULE_NOSECRET, rule_nosecret))


def run(root, manifest=_UNSET):
    """The three rule results for ROOT, in gate order."""
    return [rule(root, manifest) for _rule_id, rule in RULES]


def emit(result):
    """Print one CLI line: RULE <id> verdict=pass|fail detail=<short>."""
    print("RULE %s verdict=%s detail=%s"
          % (result["id"], result["verdict"], result["detail"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("package", help="claim-package directory")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.package):
        print("package=%s verdict=ERROR" % args.package)
        return 2
    results = run(args.package)
    for result in results:
        emit(result)
    passed = sum(1 for result in results if result["verdict"] == "pass")
    failed = len(results) - passed
    print("package=%s rules=%d pass=%d fail=%d verdict=%s"
          % (args.package, len(results), passed, failed,
             "WELL-FORMED" if failed == 0 else "DEFECT"))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
