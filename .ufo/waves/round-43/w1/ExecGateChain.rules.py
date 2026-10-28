"""R-CUSTODIAN and R-STATUS rules for the claim-package gate.

Sourceable module (round-43 C2).  The gate execs these bytes -- importlib
`spec_from_file_location`, `exec(compile(...))`, or any namespace load works,
and the delivery name (`*.rules.py`) is never imported by module name -- and
calls, per package directory:

    rule_custodian(pkg)  -> (verdict: bool, detail: str)
    rule_status(pkg)     -> (verdict: bool, detail: str)
    RULE_IDS             -> ["R-CUSTODIAN", "R-STATUS"]
    run(pkg)             -> [(rule_id, verdict, detail), ...]

`detail` is a short space-separated field list carrying the counts the gate
prints after `detail=`.  Neither rule raises: a missing, unreadable or
non-JSON file, a wrong container type and a failed path-confinement check all
return `(False, "error=<short>")`, so a corrupt package fails closed.

Scope, exactly the contract text the two rules own
(`corpus/knowledge/claim-package-contract.md`):

R-CUSTODIAN
  * non-empty decision chain of {action, input_sha256, decision_sha256,
    matched_grant_id, scope_signal} objects;
  * every action: non-empty `matched_grant_id`, `scope_signal` exactly
    "NO_SCOPE_OBJECTION";
  * `head_sha256` == final `decision_sha256` ==
    `manifest.expected_head_sha256` (three-way binding).

R-STATUS
  * `manifest_sha256` binds the manifest bytes (recomputed here, never
    trusted from the file);
  * `claim_review` holds `hard_gates`, `subchecks` and a `reviewer` with
    non-empty identity, requested/resolved model, boolean fallback flag and
    an identity distinct from every producer/verifier identity in the
    manifest;
  * `claimable: true` requires every hard gate and subcheck PASS and
    `finding_count >= 1`;
  * `claimable: false` must name a blocker (`blockers` / `residual_gates`
    non-empty, or a non-empty `verdict` string).

Only files beneath the package directory are read; symlinks and paths that
resolve outside the root are refused.  The rules do not scan secrets, recheck
provenance, grade report prose or recompute artifact digests: those are the
other six rules' scope, listed so this module cannot be mistaken for a full
gate.
"""
import hashlib
import json
import os
import re
import sys

RULE_IDS = ["R-CUSTODIAN", "R-STATUS"]

_SCOPE_OK = "NO_SCOPE_OBJECTION"
_CHAIN_KEYS = (
    "action",
    "input_sha256",
    "decision_sha256",
    "matched_grant_id",
    "scope_signal",
)
_PASS_TOKENS = ("PASS", "PASSED", "OK", "TRUE")
_HEX64 = re.compile(r"\A[0-9a-fA-F]{64}\Z")


# --------------------------------------------------------------------------
# path-confined reads
# --------------------------------------------------------------------------
def _pkg_root(pkg):
    root = os.path.realpath(os.path.abspath(pkg))
    if not os.path.isdir(root):
        raise ValueError("no-package-dir")
    return root


def _read_bytes(pkg, rel):
    """Read PKG/REL, refusing symlinks and anything resolving outside PKG."""
    root = _pkg_root(pkg)
    if os.path.isabs(rel):
        raise ValueError("absolute-path")
    parts = rel.replace("\\", "/").split("/")
    if not parts or ".." in parts or "" in parts:
        raise ValueError("unsafe-path")
    target = os.path.join(root, rel)
    if os.path.islink(target):
        raise ValueError("symlink")
    real = os.path.realpath(target)
    if real != root and os.path.commonpath((root, real)) != root:
        raise ValueError("escape")
    if not os.path.isfile(real):
        raise ValueError("missing:%s" % rel)
    with open(real, "rb") as fh:
        return fh.read()


def _load_json(pkg, rel):
    return json.loads(_read_bytes(pkg, rel).decode("utf-8"))


# --------------------------------------------------------------------------
# small predicates
# --------------------------------------------------------------------------
def _nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def _is_pass(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().upper() in _PASS_TOKENS
    return False


def _gate_counts(container):
    """Return (total, non-PASS) for a hard_gates/subchecks container.

    Accepts a mapping {name: verdict}, a list of {name, verdict|status|
    result|pass} objects, or a list of verdict scalars.  A container of the
    wrong type reports (0, 1) so it fails closed.
    """
    if isinstance(container, dict):
        items = list(container.values())
        return len(items), sum(0 if _is_pass(v) else 1 for v in items)
    if isinstance(container, list):
        bad = 0
        for entry in container:
            if isinstance(entry, dict):
                probe = None
                for key in ("verdict", "status", "result", "state", "outcome",
                            "pass", "value"):
                    if key in entry:
                        probe = entry[key]
                        break
                if not _is_pass(probe):
                    bad += 1
            elif not _is_pass(entry):
                bad += 1
        return len(container), bad
    return 0, 1


def _manifest_identities(manifest):
    """Folded producer/verifier identities recorded in the manifest."""
    found = set()

    def add(value):
        if _nonempty_str(value):
            found.add(value.strip().casefold())

    for key in ("producer_identity", "verifier_identity", "producer",
                "verifier", "reviewer_identity"):
        if isinstance(manifest, dict):
            add(manifest.get(key))
    redactions = manifest.get("redactions") if isinstance(manifest, dict) else None
    if isinstance(redactions, list):
        for receipt in redactions:
            if isinstance(receipt, dict):
                for key in ("producer", "verifier", "producer_identity",
                            "verifier_identity", "scanned_by", "produced_by"):
                    add(receipt.get(key))
    return found


def _blocker_named(status, review):
    """True when a not-claimable package names why it is not claimable."""
    for holder in (status, review):
        if not isinstance(holder, dict):
            continue
        for key in ("blockers", "residual_gates", "remaining_gates",
                    "blocker_codes"):
            value = holder.get(key)
            if isinstance(value, str) and value.strip():
                return True
            if isinstance(value, (list, tuple, dict)) and len(value) > 0:
                if isinstance(value, dict):
                    if any(_nonempty_str(v) or v for v in value.values()):
                        return True
                else:
                    return True
        verdict = holder.get("verdict")
        if _nonempty_str(verdict):
            return True
    return False


# --------------------------------------------------------------------------
# R-CUSTODIAN
# --------------------------------------------------------------------------
def rule_custodian(pkg):
    try:
        manifest = _load_json(pkg, "evidence/manifest.json")
        receipts = _load_json(pkg, "custodian-receipts.json")
    except (ValueError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return False, "error=%s" % (str(exc).split(":")[0] or "unreadable")

    chain = None
    if isinstance(receipts, dict):
        for key in ("chain", "decisions", "custodian_chain"):
            if isinstance(receipts.get(key), list):
                chain = receipts[key]
                break
    if chain is None:
        chain = []

    grant_bad = 0
    scope_bad = 0
    fields_bad = 0
    for action in chain:
        if not isinstance(action, dict):
            fields_bad += 1
            continue
        if any(not _nonempty_str(action.get(key)) for key in _CHAIN_KEYS):
            fields_bad += 1
        if not _nonempty_str(action.get("matched_grant_id")):
            grant_bad += 1
        if action.get("scope_signal") != _SCOPE_OK:
            scope_bad += 1

    head = receipts.get("head_sha256") if isinstance(receipts, dict) else None
    final_digest = None
    if chain and isinstance(chain[-1], dict):
        final_digest = chain[-1].get("decision_sha256")
    expected = (manifest.get("expected_head_sha256")
                if isinstance(manifest, dict) else None)

    if not _nonempty_str(head):
        head_state = "absent"
    elif not _nonempty_str(final_digest) or head != final_digest:
        head_state = "bad"
    else:
        head_state = "ok"

    expected_state = ("ok" if _nonempty_str(expected) and head == expected
                      else ("absent" if not _nonempty_str(expected) else "bad"))

    verdict = (len(chain) > 0 and grant_bad == 0 and scope_bad == 0
               and fields_bad == 0 and head_state == "ok"
               and expected_state == "ok")
    detail = ("actions=%d grant-bad=%d scope-bad=%d fields-bad=%d "
              "head=%s expected-head=%s"
              % (len(chain), grant_bad, scope_bad, fields_bad, head_state,
                 expected_state))
    return verdict, detail


# --------------------------------------------------------------------------
# R-STATUS
# --------------------------------------------------------------------------
def rule_status(pkg):
    try:
        manifest_bytes = _read_bytes(pkg, "evidence/manifest.json")
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        status = _load_json(pkg, "status.json")
    except (ValueError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return False, "error=%s" % (str(exc).split(":")[0] or "unreadable")
    if not isinstance(status, dict):
        return False, "error=status-not-object"

    recorded = status.get("manifest_sha256")
    recomputed = hashlib.sha256(manifest_bytes).hexdigest()
    if not _nonempty_str(recorded):
        bind_state = "absent"
    elif recorded.strip().lower() != recomputed:
        bind_state = "bad"
    else:
        bind_state = "ok"

    review = status.get("claim_review")
    review = review if isinstance(review, dict) else {}
    gates_total, gates_bad = _gate_counts(review.get("hard_gates"))
    subs_total, subs_bad = _gate_counts(review.get("subchecks"))

    reviewer = review.get("reviewer")
    reviewer = reviewer if isinstance(reviewer, dict) else {}
    reviewer_fields_ok = (
        _nonempty_str(reviewer.get("identity"))
        and _nonempty_str(reviewer.get("requested_model"))
        and _nonempty_str(reviewer.get("resolved_model"))
        and isinstance(reviewer.get("fallback"), bool)
    )
    identities = _manifest_identities(manifest)
    collide = 0
    if _nonempty_str(reviewer.get("identity")):
        if reviewer["identity"].strip().casefold() in identities:
            collide = 1

    claimable = status.get("claimable")
    finding_count = status.get("finding_count")
    finding_ok = (isinstance(finding_count, int)
                  and not isinstance(finding_count, bool)
                  and finding_count >= 1)

    if claimable is True:
        claim_state = "true"
        blocker_state = "n/a"
        verdict = (bind_state == "ok" and gates_total > 0 and gates_bad == 0
                   and subs_total > 0 and subs_bad == 0 and finding_ok
                   and reviewer_fields_ok and collide == 0)
    elif claimable is False:
        claim_state = "false"
        blocker = _blocker_named(status, review)
        blocker_state = "yes" if blocker else "no"
        verdict = (bind_state == "ok" and reviewer_fields_ok and collide == 0
                   and blocker)
    else:
        claim_state = "absent"
        blocker_state = "n/a"
        verdict = False

    detail = ("manifest-bind=%s gates=%d gates-fail=%d subchecks=%d "
              "subchecks-fail=%d finding_count=%s reviewer-fields=%s "
              "reviewer-collide=%d claimable=%s blocker=%s"
              % (bind_state, gates_total, gates_bad, subs_total, subs_bad,
                 finding_count if isinstance(finding_count, int)
                 and not isinstance(finding_count, bool) else "absent",
                 "ok" if reviewer_fields_ok else "bad", collide,
                 claim_state, blocker_state))
    return verdict, detail


# --------------------------------------------------------------------------
# convenience: both rules in gate printing order
# --------------------------------------------------------------------------
def run(pkg):
    return [
        ("R-CUSTODIAN",) + rule_custodian(pkg),
        ("R-STATUS",) + rule_status(pkg),
    ]


def _main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: %s <package-dir>\n" % os.path.basename(argv[0]))
        return 2
    pkg = argv[1]
    results = run(pkg)
    passed = 0
    for rule_id, ok, detail in results:
        passed += 1 if ok else 0
        print("RULE %s verdict=%s detail=%s"
              % (rule_id, "pass" if ok else "fail", detail))
    print("package=%s rules=%d pass=%d fail=%d"
          % (pkg, len(results), passed, len(results) - passed))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
