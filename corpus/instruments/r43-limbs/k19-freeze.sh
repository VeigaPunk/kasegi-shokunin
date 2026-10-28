#!/usr/bin/env bash
# ExecK19Freeze.sh -- K19 limb for corpus/instruments/r43-closure.sh.
#
# Sourceable: defines the shell function `check_k19 <export-root> [<commit-utc>]`,
# which prints exactly one line and returns its closed status:
#
#   K19 payload=freeze=<present|absent>,order=<ok|bad>,sha=<match|mismatch> closed=<0|1>
#
# Return status: 0 when closed=1, 1 when closed=0 (never exit: a sourced limb
# must not terminate the suite).
#
# RD42-6 class -- the freeze record must not predate the evidence it freezes.
# The limb reads only bytes under <export-root> (a `git archive` extraction of
# one commit); it never touches the lane work tree, so `committed` is carried
# by the export itself.
#
# Required relations, all over the same export:
#   claims  = .ufo/waves/round-43/claims.json
#   freeze  = .ufo/waves/round-43/freeze.txt
#   controls= claims.controls.c1 and claims.controls.c2 (relative paths inside
#             the export; absolute paths and `..` escapes are refused)
#
#   (0) the claims are the ones this check is about: claims.round is the JSON
#       integer 43 (43.0 and "43" are refused) and claims.lane is exactly
#       "kasegi" -- a round-42/44 or souji claims file with a regenerated digest
#       is not a pass;
#   (1) each control receipt carries exactly one `measured-at=<ISO-Z>` line and
#       that value parses as ISO 8601 UTC (`YYYY-MM-DDThh:mm:ssZ`), and the two
#       receipts are two distinct files: `controls.c2 := controls.c1` collapses
#       "the two committed controls" into one and is refused;
#   (2) claims.frozen_at_utc is not earlier than the latest of the two
#       measured-at values;
#   (3) claims.frozen_at_utc is not earlier than the committed freeze record's
#       `frozen-at=` label, and that label is equal to it -- a freeze record
#       written before the claims were frozen is the RD42-6 defect, and a
#       record whose label disagrees with the claims is not the record of those
#       claims;
#   (4) the freeze record is exactly four lines in the documented order
#       (frozen-at, measured-at-max, claims-sha256, base); both timestamps
#       parse as ISO 8601 Z, `measured-at-max` equals the latest control
#       measurement, and `base` equals claims.base (40 lowercase hex);
#   (5) `claims-sha256` is the SHA-256 of the claims.json bytes read here;
#   (6) when the caller supplies <commit-utc> (the ISO 8601 Z committer time of
#       the export's own commit), the label is not later than that instant: a
#       record cannot be frozen after the commit that contains it. A second
#       argument that is unparseable or explicitly empty is a red, never an
#       ignored bound.
#
# Payload fields:
#   freeze=present|absent   the freeze record exists in the export
#   order=ok|bad            relations (0)(1)(2)(3)(4)(6) all hold
#   sha=match|mismatch      relation (5) holds (an absent record cannot match,
#                           so `freeze=absent` always carries `sha=mismatch`)
# closed=1 only when freeze=present, order=ok, sha=match.

check_k19() {
    local export_root="${1:-}"
    local commit_utc="${2:-}"
    if [ -z "$export_root" ] || [ ! -d "$export_root" ]; then
        printf 'K19 payload=freeze=absent,order=bad,sha=mismatch closed=0\n'
        return 1
    fi
    python3 - "$export_root" "$commit_utc" "$#" <<'K19_PY'
import hashlib
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.abspath(sys.argv[1])
COMMIT_UTC = sys.argv[2] if len(sys.argv) > 2 else ""
ARGC = int(sys.argv[3]) if len(sys.argv) > 3 else 0
CLAIMS_ROUND = 43
CLAIMS_LANE = "kasegi"
CLAIMS_REL = ".ufo/waves/round-43/claims.json"
FREEZE_REL = ".ufo/waves/round-43/freeze.txt"
FREEZE_KEYS = ("frozen-at", "measured-at-max", "claims-sha256", "base")
ISO_Z_RX = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
HEX64_RX = re.compile(r"^[0-9a-f]{64}$")
HEX40_RX = re.compile(r"^[0-9a-f]{40}$")


def iso_z(value):
    """Parse an ISO 8601 UTC second-precision timestamp, or None."""
    if not isinstance(value, str) or not ISO_Z_RX.match(value):
        return None
    try:
        stamp = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
    return stamp if stamp.strftime("%Y-%m-%dT%H:%M:%SZ") == value else None


def inside(path):
    """True when path resolves to a location under ROOT (no symlink escape)."""
    real_root = os.path.realpath(ROOT)
    real = os.path.realpath(path)
    return real == real_root or real.startswith(real_root + os.sep)


def read_bytes(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path) or not inside(path):
        return None
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError:
        return None


def read_text(rel):
    raw = read_bytes(rel)
    if raw is None:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def parse_freeze(raw):
    """The exact four-line record, in order, or None."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    lines = text.split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    if len(lines) != len(FREEZE_KEYS):
        return None
    record = {}
    for key, line in zip(FREEZE_KEYS, lines):
        prefix = key + "="
        if not line.startswith(prefix):
            return None
        value = line[len(prefix):]
        if not value or "=" in value:
            return None
        record[key] = value
    return record


# --- claims -----------------------------------------------------------------
claims_bytes = read_bytes(CLAIMS_REL)
claims = None
if claims_bytes is not None:
    try:
        claims = json.loads(claims_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        claims = None
claims = claims if isinstance(claims, dict) else {}

# --- the two control receipts it names --------------------------------------
controls = claims.get("controls")
controls = controls if isinstance(controls, dict) else {}
measurements = []
control_paths = []
controls_ok = True
for name in ("c1", "c2"):
    rel = controls.get(name)
    if not isinstance(rel, str) or not rel or os.path.isabs(rel):
        controls_ok = False
        continue
    if ".." in rel.split("/"):
        controls_ok = False
        continue
    text = read_text(rel)
    if text is None:
        controls_ok = False
        continue
    hits = [line.strip() for line in text.splitlines()
            if line.strip().startswith("measured-at=")]
    if len(hits) != 1:                    # exactly one, never zero or two
        controls_ok = False
        continue
    stamp = iso_z(hits[0][len("measured-at="):])
    if stamp is None:
        controls_ok = False
        continue
    measurements.append(stamp)
    control_paths.append(os.path.realpath(os.path.join(ROOT, rel)))
# `controls.c2 := controls.c1` (or any spelling that resolves to one file) is
# not "the two committed control receipts": the pair must be two distinct files.
controls_distinct = (controls_ok and len(control_paths) == 2
                     and control_paths[0] != control_paths[1])
measured_max = max(measurements) if controls_distinct else None

# (0) the claims must be this round's claims in this lane.
identity_ok = (type(claims.get("round")) is int      # 43, never 43.0 or true
               and claims.get("round") == CLAIMS_ROUND
               and claims.get("lane") == CLAIMS_LANE)

# (6) an optional upper bound supplied by the caller: the committer instant of
# the export's own commit.  Supplied but unparseable -- including explicitly
# empty, `check_k19 <export> ""` -- is a red, never an ignored bound: a suite
# whose COMMIT_UTC computation failed must not silently lose the check.
commit_bound_supplied = ARGC >= 2
commit_bound = iso_z(COMMIT_UTC) if commit_bound_supplied else None
commit_bound_ok = (not commit_bound_supplied) or commit_bound is not None

# --- the committed freeze record -------------------------------------------
freeze_raw = read_bytes(FREEZE_REL)
present = freeze_raw is not None
record = parse_freeze(freeze_raw) if present else None

digest_match = False
order_ok = False
if record is not None:
    frozen_at = iso_z(record["frozen-at"])
    stated_max = iso_z(record["measured-at-max"])
    claims_frozen = iso_z(claims.get("frozen_at_utc"))
    claims_base = claims.get("base")
    digest_match = (
        claims_bytes is not None
        and HEX64_RX.match(record["claims-sha256"]) is not None
        and hashlib.sha256(claims_bytes).hexdigest() == record["claims-sha256"]
    )
    order_ok = (
        identity_ok                             # (0) round 43, lane kasegi
        and measured_max is not None            # (1) distinct controls, one stamp each
        and frozen_at is not None
        and stated_max is not None
        and claims_frozen is not None
        and frozen_at == claims_frozen          # (3) record label == claims label
        and frozen_at >= measured_max           # (2) label not earlier than controls
        and stated_max == measured_max          # (4) record states the real max
        and isinstance(claims_base, str)
        and HEX40_RX.match(claims_base) is not None
        and record["base"] == claims_base       # (4) record states the claims base
        and commit_bound_ok                     # (6) bound, when supplied, parses
        and (commit_bound is None or frozen_at <= commit_bound)
    )
    order_ok = bool(order_ok)

closed = 1 if (present and order_ok and digest_match) else 0
print("K19 payload=freeze=%s,order=%s,sha=%s closed=%d" % (
    "present" if present else "absent",
    "ok" if order_ok else "bad",
    "match" if digest_match else "mismatch",
    closed))
sys.exit(0 if closed else 1)
K19_PY
    return $?
}
