#!/usr/bin/env python3
"""verify.py: kasegi round-67 C1 committed-input driver (seat ExecMultiHeadDriver, proposed).

Measures one revision of corpus/instruments/figure-audit.py against the multi-head
SIGPIPE input-completeness predicate (per-head input-count rule; round-66 cat rows
P1/P2 frozen; P5/P15 unchanged; P12..P18 fixed). The five repair shapes P9 (cut),
P10 (wc), P11 (grep), P19/P20 (mid-argv `--` dash-file operands) are
FACE-CONDITIONAL per the L1 ruling on
controls/dispatch-addendum-r67.md: this host's grep/cut/wc race their downstream
close, so a shape's native stage0 is -13 (SIGPIPE face) or 1/2 (error face) run to
run. The driver replays each repair shape's pipeline itself, up to 20 attempts,
drives BOTH the base and the measured gate on every attempt, and prints one
`FACE <probe> stage0=<n> base=<verdict> candidate=<verdict>` line per attempt
(receipts faces-<label>.txt). Assertions, per repair shape: the replay must hit
the -13 face at least once; every BASE-gate run must read ok or stale with an
error-face reason (the ok runs ARE the masked -13 faces, and at least one per
shape is required -- that is the false green the claim is about; a base
stale:derive-upstream-signal-13 would be a contradiction); every MEASURED-gate
run must read stale with reason in {derive-upstream-signal-13,
derive-upstream-exit-1, derive-upstream-exit-2}, and at least one run per shape
must show the SIGPIPE-face refusal (derive-upstream-signal-13). A shape that
never reaches the -13 face in 20 attempts fails its measurement (a failed
measurement, not a pass). probes-base-paired judges the base column,
probes-measured the candidate column.

Inputs and their sources:
  * controls (probe battery, multi-head mutation battery, pin manifest, L1 claim
    evidence): read as bytes from --controls-revision with `git show`, never from
    the worktree; the pin manifest names their digests.
  * measured tree: a checkout of --revision in ONE scratch shared clone under --work.
  * paired base gate: bytes of corpus/instruments/figure-audit.py at the manifest base revision.
  * --candidate PATH overlays the measured gate for a non-frozen trial only; its digest is
    recorded, labelled unpinned, and never compared with a base pin.

Usage:
  python3 -B verify.py --revision REV --controls-revision CREV --work DIR
      [--candidate PATH | --final] [--base-rev REV] [--source-repo PATH]
      [--pins-path REL] [--probes-path REL] [--timeout SEC] [--print-inputs]

Output: one `RESULT <name> PASS|FAIL <note>` per measurement, in the order of MEASUREMENTS,
then `VERIFY measurements=12 failures=N revision=REV mode=base|candidate|final`.
Exit: 0 every measurement passes; 1 any FAIL; 2 setup failure (`VERIFY-SETUP reason=...`,
no verdict is claimed).

Verdict authority: the gate's own FIG/exit lines on driver-generated ledgers (shape-identity),
not the probe battery's PROBE lines. A verdict that depends on the derive's spelling (probe ID,
held-out ID) fails. The measured gate is bound to committed bytes in final mode.

This driver is not a sandbox: it executes the measured gate, its selftest, the existing
mutation battery, the multi-head limb battery and the probe battery. Children run in their
own process group under a timeout and are killed as a group on expiry. Receipts for every
child go to WORK/receipts.
"""
import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import types

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SCRATCH_ROOT = "/fast/scratch/hyaku/kasegi-r67"
WAVE = ".ufo/waves/round-67"
DRIVER_REL = WAVE + "/w1/ExecMultiHeadDriver/verify.py"
PINS_REL = WAVE + "/controls/driver-pins.json"
PROBES_REL = WAVE + "/w1/ExecMultiHeadProbes/probes.py"
MULTIHEAD_MUTBAT_REL = WAVE + "/w1/MutationMultiHead/multihead-mutbat.py"
GATE_REL = "corpus/instruments/figure-audit.py"
LEDGER_REL = "corpus/instruments/figure-audit-ledger.json"
MUTBAT_REL = "corpus/instruments/figure-audit-mutbat.py"
SIGPIPE_REASON = "derive-upstream-signal-13"
EXIT1_REASON = "derive-upstream-exit-1"
DERIVE_EXIT1_REASON = "derive-exit-1"
EXIT2_REASON = "derive-upstream-exit-2"
# L1 ruling (face-conditional repairs): the repair shapes' native stage0 races
# between -13 and 1/2 on this host, so neither a reason nor a base verdict is
# frozen for them. On a -13 face the candidate's stale reason may be any of:
FACE_REASONS = (SIGPIPE_REASON, EXIT1_REASON, EXIT2_REASON)
REPAIR_KEYS = ("P9", "P10", "P11", "P19", "P20")

MEASUREMENTS = ("driver-self-pin", "controls-pins", "ledger-closure", "probes-base-paired",
                "probes-measured", "shape-identity", "selftest", "mutbat-existing",
                "multihead-mutbat", "real-ledger", "red-wrong-want", "identity-guards")

# Independent expectation table (from the L1 measured base matrix
# controls/base-matrix-r67.txt, the wave spec and dispatch-addendum-r67.md --
# not copied from probes.py). Probe key -> (audit exit, reason) for the FIXED
# rows; the repair rows P9/P10/P11 are face-conditional (_expect) and are never
# frozen here. P18 (grep single positive control) is rc0 in BOTH modes; the
# collector reports its native -13 but does not enforce it as a premise.
BASE_EXPECT = {
    "P1": (1, SIGPIPE_REASON), "P2": (1, SIGPIPE_REASON), "P3": (0, "-"), "P4": (0, "-"),
    "P5": (1, DERIVE_EXIT1_REASON), "P6": (0, "-"), "P7": (0, "-"), "P8": (0, "-"),
    "P12": (0, "-"), "P13": (0, "-"), "P14": (0, "-"),
    "P15": (1, EXIT1_REASON), "P16": (0, "-"), "P17": (0, "-"), "P18": (0, "-"),
}
CAND_EXPECT = {
    "P1": (1, SIGPIPE_REASON), "P2": (1, SIGPIPE_REASON), "P3": (0, "-"), "P4": (0, "-"),
    "P5": (1, DERIVE_EXIT1_REASON), "P6": (0, "-"), "P7": (0, "-"), "P8": (0, "-"),
    "P12": (0, "-"), "P13": (0, "-"), "P14": (0, "-"), "P15": (1, EXIT1_REASON),
    "P16": (0, "-"), "P17": (0, "-"), "P18": (0, "-"),
}

# Native stage-0 faces the real pipelines may show (L1 controls
# native-statuses-r67.txt / base-matrix-r67.txt / donothing-multihead-r67.txt and
# the ruling: grep races -13/2, cut/wc race -13/1, P10 was measured both ways).
# Premise check, independent of the gate; the repair shapes' faces are judged
# verdict-per-face by the driver's own FACE loop. P16 sort buffers its whole
# output, so its single write can lose the race on either side; both outcomes
# leave the single-input verdict green. P18's native status is noted, never
# enforced (positive control, collector ruling).
NATIVE_STAGE0 = {
    "P1": (-13,), "P2": (-13,), "P3": (-13,), "P4": (-13,), "P5": (1,), "P6": (0,),
    "P7": (0,), "P8": (0,), "P9": (-13, 1), "P10": (-13, 1, 2), "P11": (-13, 1, 2),
    "P12": (-13,), "P13": (0,), "P14": (0,), "P15": (1,), "P16": (0, -13), "P17": (0,),
    "P18": (-13, 0),
    # P19/P20 (L1 freeze wiring): mid-argv `--` repair shapes; the -13 face is the
    # expected native premise (the CUTDASH differential shows exit 1 only without
    # the separator). `-missing.txt` must stay absent.
    "P19": (-13,), "P20": (-13,),
}

# Driver-owned shapes: key, derive (gate grammar), want (derived when ok), native
# stages, stdin file. Fixtures are deterministic (build_shape_fixtures); IDs are
# opaque per spelling so an id-keyed oracle cannot pass.
BIG_LINE = "x" * 1023
BIG_CONTENT = "alpha\n" + (BIG_LINE + "\n") * 4095
BIG_SHA = hashlib.sha256(BIG_CONTENT.encode("utf-8")).hexdigest()

SHAPES = (
    ("P1", "cat big.txt missing.txt | head -n 1", "alpha",
     [["cat", "big.txt", "missing.txt"], ["head", "-n", "1"]], None),
    ("P2", "cat big.txt other.txt | head -n 1", "alpha",
     [["cat", "big.txt", "other.txt"], ["head", "-n", "1"]], None),
    ("P3", "cat big.txt | head -n 1", "alpha",
     [["cat", "big.txt"], ["head", "-n", "1"]], None),
    ("P4", "cat < big.txt | head -n 1", "alpha",
     [["cat"], ["head", "-n", "1"]], "big.txt"),
    ("P5", "cat missing.txt", "alpha",
     [["cat", "missing.txt"]], None),
    ("P6", "head -n 5 big.txt | head -n 1", "alpha",
     [["head", "-n", "5", "big.txt"], ["head", "-n", "1"]], None),
    ("P7", "wc -l < big.txt | head -n 1", "4096",
     [["wc", "-l"], ["head", "-n", "1"]], "big.txt"),
    ("P8", "grep -c alpha big.txt | head -n 1", "1",
     [["grep", "-c", "alpha", "big.txt"], ["head", "-n", "1"]], None),
    ("P9", "cut -f1 -d: big.txt missing.txt | head -n 1", "alpha",
     [["cut", "-f1", "-d:", "big.txt", "missing.txt"], ["head", "-n", "1"]], None),
    ("P10", "wc -l big.txt missing.txt | head -n 1", "4096 big.txt",
     [["wc", "-l", "big.txt", "missing.txt"], ["head", "-n", "1"]], None),
    ("P11", "grep x xlines.txt missing.txt | head -n 1", "xlines.txt:x",
     [["grep", "x", "xlines.txt", "missing.txt"], ["head", "-n", "1"]], None),
    ("P12", "cut -f1 -d: big.txt | head -n 1", "alpha",
     [["cut", "-f1", "-d:", "big.txt"], ["head", "-n", "1"]], None),
    ("P13", "wc -l big.txt | head -n 1", "4096 big.txt",
     [["wc", "-l", "big.txt"], ["head", "-n", "1"]], None),
    ("P14", "sha256sum big.txt | head -n 1", BIG_SHA + "  big.txt",
     [["sha256sum", "big.txt"], ["head", "-n", "1"]], None),
    ("P15", "head -n 5 big.txt missing.txt | head -n 1", "alpha",
     [["head", "-n", "5", "big.txt", "missing.txt"], ["head", "-n", "1"]], None),
    ("P16", "sort big.txt | head -n 1", "alpha",
     [["sort", "big.txt"], ["head", "-n", "1"]], None),
    ("P17", "ls big.txt | head -n 1", "big.txt",
     [["ls", "big.txt"], ["head", "-n", "1"]], None),
    ("P18", "grep x big.txt | head -n 1", BIG_LINE,
     [["grep", "x", "big.txt"], ["head", "-n", "1"]], None),
    # P19/P20 (L1): mid-argv `--` repair shapes; `-missing.txt` is a dash-named
    # ABSENT operand counted only because of the separator.
    ("P19", "cut -f1 -d: big.txt -- -missing.txt | head -n 1", "alpha",
     [["cut", "-f1", "-d:", "big.txt", "--", "-missing.txt"], ["head", "-n", "1"]], None),
    ("P20", "grep x xlines.txt -- -missing.txt | head -n 1", "xlines.txt:x",
     [["grep", "x", "xlines.txt", "--", "-missing.txt"], ["head", "-n", "1"]], None),
)

PROBE_RE = re.compile(r"^PROBE (\S+) rc=(\S+) expected=(\S+) reason=(\S+) pass=(true|false)(?: repeats=(\d+))?$")
NATIVE_RE = re.compile(r"^NATIVE (\S+) stage0=(-?\d+) stage1=(-?\d+|-)")
PROBES_RE = re.compile(r"^PROBES probes=(\d+) failures=(\d+) mode=(\S+) instrument_sha256=([0-9a-f]{64})$")
SELFTEST_RE = re.compile(r"selftest cases=(\d+) failures=(\d+)")
MUTBAT_RE = re.compile(r"^MUTBAT killed=(\d+)/(\d+) survivors=(\d+) equivalents=(\d+) invalid_rejected=(\d+) failures=(\d+)$")


class Setup(Exception):
    """Harness or setup failure: no measurement verdict is produced."""


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, "rb") as fh:
        return sha_bytes(fh.read())


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout


def git_text(repo, *args):
    rc, out = git(repo, *args)
    return rc, out.decode("utf-8", "replace").strip()


def commit_of(repo, spec):
    rc, out = git_text(repo, "rev-parse", "--verify", "--quiet", spec + "^{commit}")
    return out if rc == 0 and out else None


def object_of(repo, spec):
    rc, out = git_text(repo, "rev-parse", "--verify", "--quiet", spec)
    return out if rc == 0 and out else None


def resolve(repo, spec):
    sha = commit_of(repo, spec)
    if sha is None:
        raise Setup("revision %r does not resolve to a commit" % spec)
    return sha


def status_lines(repo):
    rc, out = git(repo, "status", "--porcelain", "--untracked-files=all")
    return sorted(out.decode("utf-8", "replace").splitlines())


def closure_entries(repo, rev, figs):
    """Committed inputs each derive reads, keyed by `commit:path` and resolved to object ids.

    Heuristic enumeration over shlex tokens: `REV:PATH` resolves at REV; a bare path resolves
    at the derive's commit context (its first commit token) or at --revision. A `REV:PATH`
    whose commit exists but whose path does not is an unresolved gap and fails the closure.
    """
    entries, unresolved = {}, []
    for fig in figs:
        fid = fig.get("id") if isinstance(fig, dict) else None
        try:
            toks = shlex.split(fig["derive"])
        except (KeyError, TypeError, ValueError):
            unresolved.append("derive-unparsed:%s" % fid)
            continue
        ctx = None
        for t in toks:
            if t.startswith("-"):
                continue
            sha = commit_of(repo, t)
            if sha:
                entries["commit %s" % sha] = sha
                ctx = ctx or sha
        for t in toks:
            if t.startswith("-"):
                continue
            rspec, sep, path = t.partition(":")
            rsha = commit_of(repo, rspec) if sep and path else None
            if rsha:
                sha = object_of(repo, "%s:%s" % (rsha, path.rstrip("/")))
                if sha is None:
                    unresolved.append(t)
                else:
                    entries["%s:%s" % (rsha, path)] = sha
                continue
            base = ctx or rev
            sha = object_of(repo, "%s:%s" % (base, t.rstrip("/")))
            if sha:
                entries["%s:%s" % (base, t)] = sha
    return entries, unresolved


def closure_digest(entries):
    text = "".join("%s\t%s\n" % (k, entries[k]) for k in sorted(entries))
    return sha_bytes(text.encode("utf-8")), text


def run_cmd(c, name, argv, cwd, inputs=()):
    """One child in its own session; killed as a process group on timeout; receipt written."""
    p = subprocess.Popen(argv, cwd=cwd, env=c.env, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    timed_out = False
    try:
        out, _ = p.communicate(timeout=c.timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _ = p.communicate()
    rc = 124 if timed_out else p.returncode
    text = out.decode("utf-8", "replace")
    head = "".join("input sha256=%s %s\n" % (sha_file(i), i) for i in inputs if os.path.isfile(i))
    with open(os.path.join(c.rec, name + ".txt"), "w", encoding="utf-8") as fh:
        fh.write("%s$ %s\n(cwd=%s)\n%s%s[exit=%d]\n" % (
            head, shlex.join(argv), cwd, text,
            ("[timeout=%ss]\n" % c.timeout) if timed_out else "", rc))
    return rc, text


def _expect(key, probe_mode):
    """(allowed exit set, allowed reason set, face-conditional?) for one probe.

    Fixed rows: exact (rc, reason) from the table. Repair rows (P9/P10/P11):
    face-conditional -- the battery's own row is RECORDED, not verdict-bearing
    (its frozen expectation may miss a flipped face); acceptance is any face-
    consistent outcome, and the verdict authority is the driver's FACE loop:
    base accepts the green row or stale with any face reason; candidate must
    refuse (rc 1) with reason in FACE_REASONS under every face.
    """
    if key in REPAIR_KEYS:
        if probe_mode == "base":
            return {0, 1}, {"-"} | set(FACE_REASONS), True
        return {1}, set(FACE_REASONS), True
    erc, reason = (BASE_EXPECT if probe_mode == "base" else CAND_EXPECT)[key]
    return {erc}, {reason}, False


def parse_probes(text, rc, probe_mode, instrument_sha):
    problems, seen, natives, summaries, face_rows = [], {}, {}, [], []
    for ln in text.splitlines():
        m = PROBE_RE.match(ln)
        if m:
            key = m.group(1).split("-", 1)[0]
            if key in seen:
                problems.append("dup-%s" % key)
            seen[key] = m
            continue
        m = NATIVE_RE.match(ln)
        if m:
            natives[m.group(1).split("-", 1)[0]] = int(m.group(2))
            continue
        if ln.startswith("PROBES "):
            summaries.append(ln)
    expect_keys = sorted(NATIVE_STAGE0)
    if sorted(seen) != expect_keys:
        problems.append("probe-set=%s" % ",".join(sorted(seen)))
    battery_misses = 0
    for key in expect_keys:
        if key not in seen:
            continue
        m = seen[key]
        rcs, reasons, face_ok = _expect(key, probe_mode)
        got_rc, got_exp, got_reason = m.group(2), m.group(3), m.group(4)
        if m.group(5) != "true":
            battery_misses += 1
        if got_rc not in set(str(r) for r in rcs):
            problems.append("%s rc=%s want=%s" % (key, got_rc, sorted(rcs)))
        elif got_reason not in reasons:
            problems.append("%s reason=%s want=%s" % (key, got_reason, sorted(reasons)))
        elif not face_ok and (m.group(5) != "true" or got_exp != got_rc):
            # fixed rows pin pass=true and their expected rc in the battery's own field
            problems.append("%s expected-field=%s rc=%s pass=%s" % (key, got_exp, got_rc, m.group(5)))
        allowed = NATIVE_STAGE0[key]
        if natives.get(key) not in allowed:
            problems.append("%s native-stage0=%s want=%s" % (key, natives.get(key), sorted(allowed)))
        if face_ok:
            face_rows.append("%s=rc%s/%s" % (key, got_rc, got_reason))
    sm = PROBES_RE.match(summaries[0]) if len(summaries) == 1 else None
    if sm is None:
        problems.append("summary-missing-or-duplicated")
    elif (int(sm.group(1)) != len(expect_keys) or int(sm.group(2)) != battery_misses
          or sm.group(3) != probe_mode or sm.group(4) != instrument_sha):
        problems.append("summary=%r" % summaries[0])
    if rc not in (0, 1) or (rc == 0 and battery_misses):
        # rc 1 is legitimate only as the recorded face misses the battery's own
        # frozen repair-row expectations; a setup error (rc 2) is never a verdict.
        problems.append("rc=%s misses=%d" % (rc, battery_misses))
    note = "mode=%s probes=%d rc=%s problems=%s" % (
        probe_mode, len(seen), rc, "; ".join(problems) or "none")
    if face_rows:
        note += " face-recorded=%s" % ",".join(face_rows)
    return not problems, note


def expected_block(c):
    return (c.pins.get("expected") or {}).get(c.kind) or {}


def build_shape_fixtures(work, name="shapes"):
    """Driver-owned fixture root 'big': big.txt/other.txt/xlines.txt; missing.txt absent.

    big.txt is byte-identical to the L1 no-work control fixture (4193286 bytes,
    sha256 %s); other.txt starts beta; xlines.txt is 200000 lines of 'x'.
    """ % BIG_SHA
    root = os.path.join(work, name, "big")
    shutil.rmtree(os.path.join(work, name), ignore_errors=True)
    os.makedirs(root)
    for fname, body in (("big.txt", BIG_CONTENT),
                        ("other.txt", "beta\n" + ("y" * 1023 + "\n") * 4095),
                        ("xlines.txt", "x\n" * 200000)):
        with open(os.path.join(root, fname), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
    # missing.txt and -missing.txt (P19/P20 operand) must stay absent.
    for absent in ("missing.txt", "-missing.txt"):
        if os.path.exists(os.path.join(root, absent)):
            raise Setup("fixture %s must be absent in %s" % (absent, root))
    return {"big": root}


def native_stages(stages, root, stdin_name, timeout):
    """Replay the pipeline with plain Popen (no shell); parent closes its pipe ends."""
    procs, prev = [], None
    for i, argv in enumerate(stages):
        stdin = prev
        fh = None
        if i == 0 and stdin_name:
            fh = open(os.path.join(root, stdin_name), "rb")
            stdin = fh
        p = subprocess.Popen(argv, cwd=root, stdin=stdin, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL)
        procs.append(p)
        if prev is not None:
            prev.close()
        if fh is not None:
            fh.close()
        prev = p.stdout
    out, _ = procs[-1].communicate(timeout=timeout)
    for p in procs[:-1]:
        p.wait(timeout=timeout)
    return [p.returncode for p in procs], out.decode("utf-8", "replace")


def parse_fig(text, fid):
    """(verdict, reason, derived) from the gate's own FIG line for fid.

    FIG line shapes: `FIG <id> recorded=<rec> derived=<derived> ok` (or with a
    `want=<want>` marker), and `FIG <id> recorded=<rec>
    derived=UNAVAILABLE reason=<reason> stale`. derived/want may contain
    spaces, so the line is split on its markers and its terminal verdict
    token -- never on a single \\S+ token.
    """
    for ln in text.splitlines():
        if not ln.startswith("FIG %s " % fid):
            continue
        if " derived=UNAVAILABLE" in ln and ln.endswith(" stale"):
            body = ln.split(" derived=UNAVAILABLE reason=", 1)
            if len(body) == 2:
                return "stale", body[1].rsplit(" stale", 1)[0].split(" want=")[0], None
        if ln.endswith(" ok") and " derived=" in ln:
            derived = ln.split(" derived=", 1)[1].rsplit(" ok", 1)[0].split(" want=")[0]
            return "ok", "-", derived
        return "stale", "-", None
    return None, None, None


# ---- measurements: each returns (ok, note) -------------------------------------------------

def m_driver_self_pin(c):
    running = sha_file(os.path.abspath(__file__))
    pinned = c.pins.get("driver_sha256")
    rc, committed = git(c.src, "show", c.crev + ":" + DRIVER_REL)
    cm = "absent" if rc else sha_bytes(committed)
    ok = pinned == running and (c.mode != "final" or cm == running)
    return ok, "running=%s pinned=%s committed-at-controls=%s mode=%s" % (
        running, pinned, cm, c.mode)


def m_controls_pins(c):
    pinned = c.pins.get("controls") or {}
    problems = []
    if c.a.probes_path not in pinned:
        problems.append("probes-unpinned")
    if MULTIHEAD_MUTBAT_REL not in pinned:
        problems.append("multihead-mutbat-unpinned")
    for rel in sorted(pinned):
        rc, data = git(c.src, "show", c.crev + ":" + rel)
        if rc:
            problems.append("%s=absent" % rel)
        elif sha_bytes(data) != str(pinned[rel]):
            problems.append("%s=mismatch" % rel)
    tree_pins = c.pins.get("tree_inputs") or {}
    if not {LEDGER_REL, MUTBAT_REL} <= set(tree_pins):
        problems.append("ledger-or-existing-battery-unpinned")
    for rel, digest in sorted(tree_pins.items()):
        if rel not in (LEDGER_REL, MUTBAT_REL) or sha_file(os.path.join(c.tree, rel)) != digest:
            problems.append("%s=tree-input-mismatch" % rel)
    return not problems, "pinned=%d problems=%s" % (len(pinned), "; ".join(problems) or "none")


def m_ledger_closure(c):
    # Diagnostic only: the full checkout's ledger closure is the ground truth. Revision-keyed
    # closure pins are NOT enforced, so the frozen driver never demands future-revision pins.
    entries, unresolved = closure_entries(c.repo, c.rev, c.figs)
    digest, text = closure_digest(entries)
    with open(os.path.join(c.rec, "closure.tsv"), "w", encoding="utf-8") as fh:
        fh.write(text)
    problems = ["unresolved=%s" % ",".join(unresolved)] if unresolved else []
    return not problems, "entries=%d unresolved=%d sha256=%s (diagnostic) problems=%s" % (
        len(entries), len(unresolved), digest, "; ".join(problems) or "none")


FACE_ATTEMPTS = 20


def _face_verdict(text, fid):
    verdict, reason, derived = parse_fig(text, fid)
    if verdict == "ok":
        return "ok", derived
    if verdict == "stale":
        return "stale:%s" % reason, None
    return "harness", None


def _run_gate_once(c, name, gate, ledger, root):
    """One gate child: own session, group-killed on timeout; compact receipt line."""
    argv = [sys.executable, "-B", gate, "--ledger", ledger, "--root", root]
    p = subprocess.Popen(argv, cwd=root, env=c.env, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    timed_out = False
    try:
        out, _ = p.communicate(timeout=c.timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _ = p.communicate()
    text = out.decode("utf-8", "replace")
    with open(os.path.join(c.rec, name + ".txt"), "a", encoding="utf-8") as fh:
        fh.write("$ %s\n%s%s[exit=%d]\n" % (shlex.join(argv), text,
                                            ("[timeout=%ss]\n" % c.timeout) if timed_out else "",
                                            124 if timed_out else p.returncode))
    return (124 if timed_out else p.returncode), text


def _repair_faces(c, label):
    """Face-conditional attempts for the repair shapes (L1 ruling).

    Replays each repair shape's native pipeline up to FACE_ATTEMPTS times,
    drives BOTH gates on every attempt, and writes one
    `FACE <probe> stage0=<n> base=<verdict> candidate=<verdict>` line per
    attempt to receipts/faces-<label>.txt. The gate re-executes the derive
    itself, so the replay's stage0 and a gate run's internal face can desync;
    the verdict-per-face judgement therefore attributes each gate run's face by
    its own observable (its stale reason), while the replay loop proves the
    -13 face is reachable at all. A shape must show the replay -13 face at
    least once; ledger ids are opaque digests, never the probe key.
    Returns (rows, problems, summary) where rows[key] = {"sig": [...], "other": [...]}
    with (stage0, base_verdict, cand_verdict) tuples.
    """
    shapes = {key: (derive, want, stages, stdin) for key, derive, want, stages, stdin in SHAPES}
    roots = build_shape_fixtures(c.work, "faces-" + label)
    root = roots["big"]
    lines, rows, problems = [], {}, []
    for key in REPAIR_KEYS:
        derive, want, stages, stdin = shapes[key]
        rows[key] = {"sig": [], "other": []}
        for attempt in range(1, FACE_ATTEMPTS + 1):
            nrc, _ = native_stages(stages, root, stdin, c.timeout)
            stage0 = nrc[0]
            fid_b = "f-" + sha_bytes(("b|%s|%s|%d" % (label, key, attempt)).encode())[:16]
            fid_c = "f-" + sha_bytes(("c|%s|%s|%d" % (label, key, attempt)).encode())[:16]
            verdicts = []
            for gate, fid, tag in ((c.base_gate, fid_b, "b"), (c.gate, fid_c, "c")):
                ledger = os.path.join(c.work, "faces-" + label, "%s%d.json" % (tag, attempt))
                if os.path.exists(ledger):
                    os.unlink(ledger)
                with open(ledger, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump({"figures": [{"id": fid, "record": "face.txt:1", "recorded": want,
                                             "derive": derive, "want": want}]}, fh)
                    fh.write("\n")
                rc, text = _run_gate_once(c, "face-%s-%s-%d-%s" % (label, key, attempt, tag),
                                          gate, ledger, root)
                if rc != 0 and rc != 1:
                    problems.append("%s/%s gate-rc=%d" % (key, tag, rc))
                verdicts.append(_face_verdict(text, fid)[0])
            face = "sig" if stage0 == -13 else "other"
            rows[key][face].append((stage0, verdicts[0], verdicts[1]))
            lines.append("FACE %s stage0=%d base=%s candidate=%s" % (key, stage0, verdicts[0], verdicts[1]))
            if _base_masked(rows[key]) and _cand_sig_refused(rows[key]) and rows[key]["other"]:
                break
        if not rows[key]["sig"]:
            problems.append("%s no-sigpipe-face-in-%d-attempts" % (key, FACE_ATTEMPTS))
    lines.append("FACES %s attempts=%s" % (label, " ".join(
        "%s:sig%d/other%d" % (k, len(rows[k]["sig"]), len(rows[k]["other"])) for k in REPAIR_KEYS)))
    with open(os.path.join(c.rec, "faces-%s.txt" % label), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return rows, problems, lines[-1]


def _base_masked(bucket):
    return any(v == "ok" for _s, v, _c in bucket["sig"] + bucket["other"])


def _cand_sig_refused(bucket):
    return any(c == "stale:" + SIGPIPE_REASON for _s, _b, c in bucket["sig"] + bucket["other"])


def _judge_base_faces(rows):
    """Base column: the false green is the claim's premise. A base run whose own
    face was the error face reads stale exit-N; a run on the -13 face reads ok
    (the masking). The gate re-runs the derive, so `ok` runs are exactly the
    masked -13 faces; requiring at least one per shape re-derives the false
    green on the SIGPIPE face. A base stale:derive-upstream-signal-13 would be
    a contradiction (base exempts every non-cat head blindly) and fails."""
    problems = []
    for key in REPAIR_KEYS:
        for stage0, base_v, _cand in rows[key]["sig"] + rows[key]["other"]:
            if base_v == "ok" or base_v.startswith("stale:"):
                reason = base_v[6:] if base_v.startswith("stale:") else None
                if reason is not None and reason not in (EXIT1_REASON, EXIT2_REASON):
                    problems.append("%s base=%s want=ok or stale-exit-face" % (key, base_v))
            else:
                problems.append("%s base=%s want=ok or stale-exit-face" % (key, base_v))
        if not _base_masked(rows[key]):
            problems.append("%s no-masked-sigpipe-base-run-in-%d-attempts" % (key, FACE_ATTEMPTS))
    return problems


def _judge_candidate_faces(rows):
    """Candidate column: every run must refuse (stale, reason in FACE_REASONS)
    whatever face its own execution saw, and at least one run per shape must
    show the SIGPIPE-face refusal (stale:derive-upstream-signal-13) so the
    repair is observed on the face the claim is about."""
    problems = []
    for key in REPAIR_KEYS:
        for stage0, _base, cand_v in rows[key]["sig"] + rows[key]["other"]:
            reason = cand_v[6:] if cand_v.startswith("stale:") else None
            if reason not in FACE_REASONS:
                problems.append("%s candidate=%s want=stale in %s" % (
                    key, cand_v, sorted(FACE_REASONS)))
        if not _cand_sig_refused(rows[key]):
            problems.append("%s no-sigpipe-refusal-in-%d-attempts" % (key, FACE_ATTEMPTS))
    return problems


def m_probes_base_paired(c):
    if c.probes_local is None:
        return False, "probes absent at controls revision"
    ok, note = _probes(c, "base-paired", c.base_gate, "base")
    rows, problems, summary = _repair_faces(c, "base-paired")
    problems += _judge_base_faces(rows)
    return ok and not problems, "%s %s %s" % (note, summary,
                                              "; ".join(problems) or "faces-clean")


def m_probes_measured(c):
    if c.probes_local is None:
        return False, "probes absent at controls revision"
    ok, note = _probes(c, "measured", c.gate, "candidate")
    rows, problems, summary = _repair_faces(c, "measured")
    problems += _judge_candidate_faces(rows)
    return ok and not problems, "%s %s %s" % (note, summary,
                                              "; ".join(problems) or "faces-clean")


def _probes(c, label, instrument, probe_mode):
    workdir = os.path.join(c.work, "probes-" + label)
    shutil.rmtree(workdir, ignore_errors=True)
    argv = [sys.executable, "-B", c.probes_local, "--instrument", instrument,
            "--work", workdir, "--mode", probe_mode]
    rc, text = run_cmd(c, "probes-" + label, argv, c.work, inputs=[instrument, c.probes_local])
    return parse_probes(text, rc, probe_mode, sha_file(instrument))


def m_shape_identity(c):
    """The gate's own verdict on driver-owned ledgers, under two spellings of the figure ID."""
    roots = build_shape_fixtures(c.work)
    ledgers = os.path.join(c.work, "shapes", "ledgers")
    os.makedirs(ledgers, exist_ok=True)
    problems, rows = [], []
    for key, derive, want, stages, stdin_name in SHAPES:
        root = roots["big"]
        nrc, _ = native_stages(stages, root, stdin_name, c.timeout)
        if nrc[0] not in NATIVE_STAGE0[key]:
            problems.append("%s native-stage0=%s want=%s" % (key, nrc[0], sorted(NATIVE_STAGE0[key])))
        rcs, reasons, flaky_ok = _expect(key, "candidate")
        want_verdict = "ok" if rcs == {0} else "stale"
        got = []
        for label, fid in (("probe", key + "-probe-spelling"), ("held", "held-" + sha_bytes(key.encode())[:10])):
            ledger = os.path.join(ledgers, "%s-%s.json" % (key, label))
            with open(ledger, "w", encoding="utf-8", newline="\n") as fh:
                json.dump({"figures": [{"id": fid, "record": "shape.txt:1", "recorded": want,
                                         "derive": derive, "want": want}]}, fh)
                fh.write("\n")
            rc, text = run_cmd(c, "shape-%s-%s" % (key, label), [
                sys.executable, "-B", c.gate, "--ledger", ledger, "--root", root], root, [c.gate])
            verdict, reason, derived = parse_fig(text, fid)
            got.append((fid, rc, verdict, reason, derived))
            if rc not in rcs or verdict != want_verdict:
                problems.append("%s/%s rc=%s verdict=%s want=%d/%s" % (
                    key, label, rc, verdict, sorted(rcs)[0] if len(rcs) == 1 else sorted(rcs),
                    want_verdict))
            elif (reason not in reasons) if flaky_ok else (reason != sorted(reasons)[0]):
                problems.append("%s/%s reason=%s want=%s" % (key, label, reason, sorted(reasons)))
            if verdict == "ok" and derived != want:
                problems.append("%s/%s derived=%s want=%s" % (key, label, derived, want))
        id_fields = (1, 2) if flaky_ok else (1, 2, 3)
        if len(set(tuple(g[i] for i in id_fields) for g in got)) != 1:
            problems.append("%s spelling-dependent" % key)
        rows.append("%s rc=%s verdict=%s reason=%s native0=%s" % (
            key, got[0][1], got[0][2], got[0][3], nrc[0]))
    return not problems, "shapes=%d %s problems=%s" % (
        len(SHAPES), " | ".join(rows), "; ".join(problems) or "none")


def m_selftest(c):
    rc, text = run_cmd(c, "selftest", [sys.executable, "-B", c.gate, "--selftest"], c.tree, [c.gate])
    hits = SELFTEST_RE.findall(text)
    want = expected_block(c).get("selftest_cases")
    cases, fails = hits[-1] if hits else (None, None)
    ok = rc == 0 and cases is not None and str(want) == cases and fails == "0"
    return ok, "cases=%s failures=%s want=%s exit=%d kind=%s" % (cases, fails, want, rc, c.kind)


def m_mutbat(c):
    want = expected_block(c).get("mutbat_summary")
    mutbat = os.path.join(c.tree, MUTBAT_REL)
    rc, text = run_cmd(c, "mutbat", [sys.executable, "-B", mutbat, "--instrument", c.gate],
                       c.work, [mutbat, c.gate])
    lines = [ln for ln in text.splitlines() if ln.startswith("mutbat killed=")]
    ok = rc == 0 and len(lines) == 1 and lines[0] == want
    return ok, "exit=%d summary=%s want=%s" % (rc, lines[-1] if lines else None, want)


def m_multihead_mutbat(c):
    """Run the committed multi-head limb battery against the measured gate.

    The battery is a pinned control (read from the controls revision, never the
    worktree) and drives the REAL probes collector. Expectations are
    kind-explicit: at candidate kind the battery must exit 0 with the pinned
    green summary; at base kind its red IS the pinned expectation -- exit 1
    with the measured baseline-failure summary (killed=0/7, invalid_rejected
    counted, no kills). An ignored shared collector (COLLECTOR ignored=...)
    is a FAILED sub-assertion with its reason, never a silent pass.
    """
    rel = MULTIHEAD_MUTBAT_REL
    rc, data = git(c.src, "show", c.crev + ":" + rel)
    if rc:
        return False, "multihead-mutbat %s absent at controls revision" % rel
    pinned = (c.pins.get("controls") or {}).get(rel)
    if pinned is None or sha_bytes(data) != str(pinned):
        return False, "multihead-mutbat %s not pinned to its committed bytes" % rel
    if c.probes_local is None:
        return False, "probes collector absent at controls revision"
    local = os.path.join(c.work, "controls", "multihead-mutbat.py")
    with open(local, "wb") as fh:
        fh.write(data)
    want = expected_block(c).get("multihead_mutbat_summary")
    workdir = os.path.join(c.work, "multihead-mutbat")
    shutil.rmtree(workdir, ignore_errors=True)
    rc, text = run_cmd(c, "multihead-mutbat", [sys.executable, "-B", local, "--instrument", c.gate,
                                               "--collector", c.probes_local, "--work", workdir],
                       c.work, [local, c.gate, c.probes_local])
    lines = [ln for ln in text.splitlines() if MUTBAT_RE.match(ln)]
    collector = [ln for ln in text.splitlines() if ln.startswith("COLLECTOR ")]
    # Erratum 1 (round 67): a COLLECTOR line is not by itself a failure.  `COLLECTOR
    # fixtures=ok` proves the collector's fixtures were built and `COLLECTOR unstable=<ids>`
    # is the collector's own legitimate finding (P10's native face is flaky); only
    # `COLLECTOR ignored=` means the battery did not consume the shared table.  The binding
    # is required to be visible as a `probes=collector:` line.
    ignored = [ln for ln in collector if " ignored=" in ln]
    findings = [ln for ln in collector if " ignored=" not in ln]
    bound = [ln for ln in text.splitlines() if ln.startswith("probes=collector:")]
    ok = want is not None and len(lines) == 1 and lines[0] == want
    ok = ok and rc == (1 if c.kind == "base" else 0)
    ok = ok and bool(bound) and not ignored
    note = "exit=%d want=%r sha256=%s" % (rc, lines[-1] if lines else None, sha_bytes(data))
    if ignored:
        note += " collector-ignored-FAIL %s" % ignored[0]
    if findings:
        note += " collector-findings=%s" % "|".join(f.replace(" ", "_") for f in findings)
    if not bound:
        note += " collector-not-bound"
    return ok, note


def m_real_ledger(c):
    want = c.pins.get("expected", {}).get("ledger_summary")
    rc, text = run_cmd(c, "real-ledger", [sys.executable, "-B", c.gate, "--ledger", LEDGER_REL,
                                           "--root", "."], c.tree, [c.gate, c.ledger_path])
    ok = rc == 0 and want in text.splitlines()
    return ok, "exit=%d want=%r ledger_sha256=%s" % (rc, want, c.ledger_sha)


def m_red_wrong_want(c):
    red = os.path.join(c.work, "red")
    shutil.rmtree(red, ignore_errors=True)
    os.makedirs(red)
    with open(os.path.join(red, "g.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("35\n")
    doc = {"figures": [
        {"id": "red-wrong-want", "record": "g.txt:1", "recorded": "34", "derive": "cat g.txt", "want": "34"},
        {"id": "green-right-want", "record": "g.txt:1", "recorded": "35", "derive": "cat g.txt", "want": "35"},
    ]}
    ledger = os.path.join(red, "ledger.json")
    with open(ledger, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh)
        fh.write("\n")
    rc, text = run_cmd(c, "red-wrong-want", [sys.executable, "-B", c.gate, "--ledger", ledger,
                                              "--root", red], red, [c.gate])
    lines = text.splitlines()
    want = {"FIG red-wrong-want recorded=34 derived=35 want=34 stale",
            "FIG green-right-want recorded=35 derived=35 ok",
            "FIGURE-AUDIT figures=2 ok=1 stale=1 exit=1"}
    fig_lines = [ln for ln in lines if ln.startswith("FIG ")]
    ok = rc == 1 and want <= set(lines) and len(fig_lines) == 2
    return ok, "exit=%d red-stale-line=%s" % (rc, "yes" if want <= set(lines) else "no")


def m_identity_guards(c):
    problems = []
    rc, head = git_text(c.tree, "rev-parse", "HEAD")
    if head != c.rev:
        problems.append("head=%s" % head[:12])
    post = status_lines(c.tree)
    if post != c.pre:
        problems.append("tree-changed-by-run")
    changed = sorted(set(ln[3:] for ln in post))
    allowed = [GATE_REL] if c.a.candidate else []
    if changed != sorted(allowed):
        problems.append("dirty=%s" % ",".join(changed))
    tree_gate = sha_file(c.gate)
    rc, committed = git(c.tree, "show", c.rev + ":" + GATE_REL)
    if not c.a.candidate and (rc or sha_bytes(committed) != tree_gate):
        problems.append("gate-not-committed-bytes")
    if sha_bytes(c.base_bytes) != str(c.pins.get("base_gate_sha256")):
        problems.append("base-gate-pin")
    measured = c.pins.get("measured") or {}
    if not c.a.candidate and (c.mode == "final" or measured.get("revision") == c.rev) \
            and measured.get("gate_sha256") != tree_gate:
        problems.append("measured-gate-pin")
    if c.mode == "final" and git(c.src, "merge-base", "--is-ancestor", c.crev, c.rev)[0] != 0:
        problems.append("final-controls-not-ancestor-of-revision")
    return not problems, "head=%s mode=%s gate=%s candidate=%s(unpinned) base=%s problems=%s" % (
        head[:12], c.mode, tree_gate, c.cand_sha or "-", sha_bytes(c.base_bytes),
        "; ".join(p for p in problems if p) or "none")


def inputs_json(c):
    entries, unresolved = closure_entries(c.repo, c.rev, c.figs)
    digest, _ = closure_digest(entries)
    return {
        "driver_sha256": sha_file(os.path.abspath(__file__)),
        "controls_revision": c.crev,
        "controls": {c.a.probes_path: sha_bytes(c.probes_bytes) if c.probes_bytes else None},
        "base": {"revision": c.base, "gate_sha256": sha_bytes(c.base_bytes)},
        "measured": {"revision": c.rev, "gate_sha256": sha_file(c.gate), "ledger_sha256": c.ledger_sha,
                     "mutbat_sha256": sha_file(os.path.join(c.tree, MUTBAT_REL)),
                     "closure_entries": len(entries), "closure_sha256": digest,
                     "unresolved": unresolved},
    }


def setup(a):
    if a.candidate and a.final:
        raise Setup("--final refuses --candidate")
    mode = "final" if a.final else ("candidate" if a.candidate else "base")
    work = os.path.realpath(a.work)
    if not work.startswith(SCRATCH_ROOT + "/") or work.startswith(LANE):
        raise Setup("--work must be a directory under %s/ and outside the lane" % SCRATCH_ROOT)
    src = os.path.realpath(a.source_repo)
    if mode == "final" and src != LANE:
        raise Setup("--final reads only the lane repo %s" % LANE)
    rc, top = git_text(src, "rev-parse", "--show-toplevel")
    if rc or os.path.realpath(top) != src:
        raise Setup("source-repo is not its own toplevel: %s" % src)
    rev = resolve(src, a.revision)
    crev = resolve(src, a.controls_revision)
    rc, pins_raw = git(src, "show", crev + ":" + a.pins_path)
    if rc:
        if not a.print_inputs:
            raise Setup("pin manifest %s absent at controls revision %s" % (a.pins_path, crev))
        pins = {}
    else:
        try:
            pins = json.loads(pins_raw.decode("utf-8"))
        except ValueError as exc:
            raise Setup("pin manifest unparsable: %s" % exc)
    base_spec = a.base_rev or pins.get("base")
    if not base_spec:
        raise Setup("no base revision: pass --base-rev or pin base in the manifest")
    base = resolve(src, base_spec)
    rc, base_bytes = git(src, "show", base + ":" + GATE_REL)
    if rc:
        raise Setup("base gate %s absent at %s" % (GATE_REL, base))
    rc, probes_bytes = git(src, "show", crev + ":" + a.probes_path)
    probes_bytes = None if rc else probes_bytes

    os.makedirs(work, exist_ok=True)
    tmp = os.path.join(work, "tmp")
    rec = os.path.join(work, "receipts")
    for d in (tmp, rec, os.path.join(work, "base"), os.path.join(work, "controls")):
        os.makedirs(d, exist_ok=True)
    repo = os.path.join(work, "repo")
    if not os.path.isdir(os.path.join(repo, ".git")):
        p = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", src, repo],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode:
            raise Setup("clone failed: %s" % p.stderr.decode("utf-8", "replace").strip())
    rc, origin = git_text(repo, "config", "--get", "remote.origin.url")
    if rc or origin != src:
        raise Setup("scratch clone origin is not the source repo")
    if commit_of(repo, rev) is None:
        p = subprocess.run(["git", "-C", repo, "fetch", "-q", "--no-tags", src, rev],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode or commit_of(repo, rev) is None:
            raise Setup("revision %s not reachable from the scratch clone" % rev)
    rc, _ = git(repo, "checkout", "-q", "-f", "--detach", rev)
    if rc:
        raise Setup("cannot check out %s in the scratch clone" % rev)
    git(repo, "clean", "-q", "-f", "-d", "-x")
    rc, head = git_text(repo, "rev-parse", "HEAD")
    if head != rev:
        raise Setup("scratch HEAD %s differs from revision %s" % (head, rev))

    gate = os.path.join(repo, GATE_REL)
    cand_sha = None
    if a.candidate:
        cand = os.path.realpath(a.candidate)
        if not os.path.isfile(cand):
            raise Setup("candidate is not a file: %s" % cand)
        shutil.copyfile(cand, gate)
        cand_sha = sha_file(cand)
    pre = status_lines(repo)

    base_gate = os.path.join(work, "base", "figure-audit.py")
    with open(base_gate, "wb") as fh:
        fh.write(base_bytes)
    probes_local = None
    if probes_bytes is not None:
        probes_local = os.path.join(work, "controls", "probes.py")
        with open(probes_local, "wb") as fh:
            fh.write(probes_bytes)
    ledger_path = os.path.join(repo, LEDGER_REL)
    with open(ledger_path, "rb") as fh:
        ledger_raw = fh.read()
    figs = json.loads(ledger_raw.decode("utf-8"))["figures"]

    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", ""),
           "TMPDIR": tmp, "HYAKU_SCRATCH": work, "PYTHONDONTWRITEBYTECODE": "1"}
    kind = "base" if mode == "base" else "candidate"
    return types.SimpleNamespace(
        a=a, mode=mode, kind=kind, work=work, rec=rec, env=env, timeout=a.timeout,
        src=src, rev=rev, crev=crev, base=base, base_bytes=base_bytes, base_gate=base_gate,
        pins=pins, probes_bytes=probes_bytes, probes_local=probes_local,
        repo=repo, tree=repo, gate=gate, cand_sha=cand_sha, pre=pre,
        ledger_path=ledger_path, ledger_sha=sha_bytes(ledger_raw), figs=figs)


def measurement_names(a):
    # Round-67 battery is unconditional: exactly the 12 committed measurements,
    # identity-guards last (it sees the tree state after every child ran).
    return list(MEASUREMENTS)


def main(argv=None):
    ap = argparse.ArgumentParser(description="kasegi r67 C1 committed-input driver")
    ap.add_argument("--revision", required=True, help="measured revision (full or short)")
    ap.add_argument("--controls-revision", dest="controls_revision", required=True,
                    help="committed revision supplying the probe battery and pin manifest")
    ap.add_argument("--work", required=True, help="scratch dir under %s/" % SCRATCH_ROOT)
    ap.add_argument("--candidate", help="uncommitted gate overlay (trial only; never --final)")
    ap.add_argument("--final", action="store_true", help="frozen mode: lane source, pins required")
    ap.add_argument("--base-rev", dest="base_rev", help="base revision (default: manifest base)")
    ap.add_argument("--source-repo", dest="source_repo", default=LANE)
    ap.add_argument("--pins-path", dest="pins_path", default=PINS_REL)
    ap.add_argument("--probes-path", dest="probes_path", default=PROBES_REL)
    ap.add_argument("--timeout", type=int, default=900, help="seconds per child")
    ap.add_argument("--print-inputs", dest="print_inputs", action="store_true",
                    help="print input digests as JSON and exit 0 (pin-manifest construction)")
    a = ap.parse_args(argv)
    try:
        c = setup(a)
    except Setup as exc:
        print("VERIFY-SETUP reason=%s" % exc)
        return 2
    if a.print_inputs:
        print("INPUTS " + json.dumps(inputs_json(c), indent=2, sort_keys=True))
        return 0

    fns = {
        "driver-self-pin": m_driver_self_pin,
        "controls-pins": m_controls_pins,
        "ledger-closure": m_ledger_closure,
        "probes-base-paired": m_probes_base_paired,
        "probes-measured": m_probes_measured,
        "shape-identity": m_shape_identity,
        "selftest": m_selftest,
        "mutbat-existing": m_mutbat,
        "multihead-mutbat": m_multihead_mutbat,
        "real-ledger": m_real_ledger,
        "red-wrong-want": m_red_wrong_want,
        "identity-guards": m_identity_guards,
    }
    results = {}
    names = measurement_names(a)
    for name in names:
        if name == "identity-guards":
            continue
        try:
            results[name] = fns[name](c)
        except Exception as exc:  # a broken measurement is a FAIL, never a silent pass
            results[name] = (False, "harness-error %s: %s" % (type(exc).__name__, exc))
    try:
        results["identity-guards"] = m_identity_guards(c)
    except Exception as exc:
        results["identity-guards"] = (False, "harness-error %s: %s" % (type(exc).__name__, exc))

    failures = 0
    for name in names:
        ok, note = results[name]
        failures += 0 if ok else 1
        print("RESULT %s %s %s" % (name, "PASS" if ok else "FAIL", note))
    index = {"driver_sha256": sha_file(os.path.abspath(__file__)),
             "pins_sha256": sha_bytes(json.dumps(c.pins, sort_keys=True).encode("utf-8")),
             "mode": c.mode, "revision": c.rev, "controls_revision": c.crev, "base": c.base,
             "receipts": {n: sha_file(os.path.join(c.rec, n)) for n in sorted(os.listdir(c.rec))
                          if os.path.isfile(os.path.join(c.rec, n))}}
    with open(os.path.join(c.rec, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("VERIFY measurements=%d failures=%d revision=%s mode=%s" % (
        len(names), failures, c.rev, c.mode))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
