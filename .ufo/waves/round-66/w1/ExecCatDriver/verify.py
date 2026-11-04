#!/usr/bin/env python3
"""verify.py: kasegi round-66 C1 committed-input driver (seat ExecCatDriver, proposed).

Measures one revision of corpus/instruments/figure-audit.py against the cat-SIGPIPE predicate.

Inputs and their sources:
  * controls (probe battery, pin manifest): read as bytes from --controls-revision with
    `git show`, never from the worktree; the pin manifest names their digests.
  * measured tree: a checkout of --revision in ONE scratch shared clone under --work.
  * paired base gate: bytes of corpus/instruments/figure-audit.py at the manifest base revision.
  * --candidate PATH overlays the measured gate for a non-frozen trial only; its digest is
    recorded, labelled unpinned, and never compared with a base pin.

Usage:
  python3 -B verify.py --revision REV --controls-revision CREV --work DIR
      [--candidate PATH | --final] [--base-rev REV] [--source-repo PATH]
      [--pins-path REL] [--probes-path REL] [--timeout SEC] [--print-inputs]

Output: one `RESULT <name> PASS|FAIL <note>` per measurement, in the order of MEASUREMENTS,
then `VERIFY measurements=11 failures=N revision=REV mode=base|candidate|final` (12 with --cat-mutbat).
Exit: 0 every measurement passes; 1 any FAIL; 2 setup failure (`VERIFY-SETUP reason=...`,
no verdict is claimed).

Verdict authority: the gate's own FIG/exit lines on driver-generated ledgers (shape-identity),
not the probe battery's PROBE lines. A verdict that depends on the derive's spelling (probe ID,
held-out ID) fails. The measured gate is bound to committed bytes in final mode.

This driver is not a sandbox: it executes the measured gate, its selftest, the existing
mutation battery and the probe battery. Children run in their own process group under a
timeout and are killed as a group on expiry. Receipts for every child go to WORK/receipts.
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
SCRATCH_ROOT = "/fast/scratch/hyaku/kasegi-r66"
WAVE = ".ufo/waves/round-66"
DRIVER_REL = WAVE + "/w1/ExecCatDriver/verify.py"
PINS_REL = WAVE + "/controls/driver-pins.json"
PROBES_REL = WAVE + "/w1/ExecCatProbes/probes.py"
GATE_REL = "corpus/instruments/figure-audit.py"
LEDGER_REL = "corpus/instruments/figure-audit-ledger.json"
MUTBAT_REL = "corpus/instruments/figure-audit-mutbat.py"
SIGPIPE_REASON = "derive-upstream-signal-13"

MEASUREMENTS = ("driver-self-pin", "controls-pins", "ledger-closure", "probes-base-paired",
                "probes-measured", "shape-identity", "selftest", "mutbat-existing", "real-ledger",
                "red-wrong-want", "identity-guards")

# Independent expectation table (from the round-66 seat spec, not copied from probes.py).
# probe key -> (audit exit, reason or "-"). Probe mode "base" is the paired base read,
# probe mode "candidate" is the claim predicate and is always the measured-gate check.
PROBE_EXPECT = {
    "base": {"P1": (0, "-"), "P2": (0, "-"), "P3": (0, "-"), "P4": (0, "-"),
             "P5": (1, "derive-upstream-exit-1"), "P6": (0, "-"), "P7": (0, "-"), "P8": (0, "-")},
    "candidate": {"P1": (1, SIGPIPE_REASON), "P2": (1, SIGPIPE_REASON), "P3": (0, "-"),
                  "P4": (0, "-"), "P5": (1, "derive-upstream-exit-1"), "P6": (0, "-"),
                  "P7": (0, "-"), "P8": (1, SIGPIPE_REASON)},
}
# Native stage-0 status the real pipeline must show (premise check, independent of the gate).
NATIVE_STAGE0 = {"P1": -13, "P2": -13, "P3": -13, "P4": -13, "P5": 1, "P6": 1, "P7": 0, "P8": -13}

# Driver-owned shapes: key, fixture variant, derive (gate grammar), want, native stages, stdin file.
SHAPES = (
    ("P1", "big", "cat big.txt missing.txt | head -n 1", "alpha",
     [["cat", "big.txt", "missing.txt"], ["head", "-n", "1"]], None),
    ("P2", "big", "cat big.txt other.txt | head -n 1", "alpha",
     [["cat", "big.txt", "other.txt"], ["head", "-n", "1"]], None),
    ("P3", "big", "cat big.txt | head -n 1", "alpha",
     [["cat", "big.txt"], ["head", "-n", "1"]], None),
    ("P4", "big", "cat < big.txt | head -n 1", "alpha",
     [["cat"], ["head", "-n", "1"]], "big.txt"),
    ("P5", "big", "cat missing.txt | wc -l", "0",
     [["cat", "missing.txt"], ["wc", "-l"]], None),
    ("P6", "big", "grep absent big.txt | wc -l", "0",
     [["grep", "absent", "big.txt"], ["wc", "-l"]], None),
    ("P7", "small", "cat big.txt other.txt | head -n 1", "alpha",
     [["cat", "big.txt", "other.txt"], ["head", "-n", "1"]], None),
    ("P8", "big", "cat -- -- missing.txt | head -n 1", "alpha",
     [["cat", "--", "--", "missing.txt"], ["head", "-n", "1"]], None),
)

PROBE_RE = re.compile(r"^PROBE (\S+) rc=(\S+) expected=(\S+) reason=(\S+) pass=(true|false)$")
NATIVE_RE = re.compile(r"^NATIVE (\S+) stage0=(-?\d+) stage1=(-?\d+)")
PROBES_RE = re.compile(r"^PROBES probes=(\d+) failures=(\d+) mode=(\S+) instrument_sha256=([0-9a-f]{64})$")
SELFTEST_RE = re.compile(r"selftest cases=(\d+) failures=(\d+)")


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


def parse_probes(text, rc, probe_mode, instrument_sha):
    problems, seen, natives, summaries = [], {}, {}, []
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
    expect = PROBE_EXPECT[probe_mode]
    if sorted(seen) != sorted(expect):
        problems.append("probe-set=%s" % ",".join(sorted(seen)))
    for key in sorted(expect):
        if key not in seen:
            continue
        m = seen[key]
        erc, reason = expect[key]
        ok = m.group(2) == str(erc) and m.group(3) == str(erc) and m.group(4) == reason and m.group(5) == "true"
        if not ok:
            problems.append("%s rc=%s want=%d reason=%s want=%s pass=%s" % (
                key, m.group(2), erc, m.group(4), reason, m.group(5)))
        if natives.get(key) != NATIVE_STAGE0[key]:
            problems.append("%s native-stage0=%s want=%d" % (key, natives.get(key), NATIVE_STAGE0[key]))
    sm = PROBES_RE.match(summaries[0]) if len(summaries) == 1 else None
    if sm is None:
        problems.append("summary-missing-or-duplicated")
    elif (int(sm.group(1)) != len(expect) or int(sm.group(2)) != 0 or sm.group(3) != probe_mode
          or sm.group(4) != instrument_sha):
        problems.append("summary=%r" % summaries[0])
    if rc != 0:
        problems.append("rc=%s" % rc)
    return not problems, "mode=%s probes=%d rc=%s problems=%s" % (
        probe_mode, len(seen), rc, "; ".join(problems) or "none")


def expected_block(c):
    return (c.pins.get("expected") or {}).get(c.kind) or {}


def build_shape_fixtures(work):
    """Driver-owned fixture roots: 'big' (4 MiB+, first line alpha) and 'small' (one line)."""
    line = "x" * 63 + "\n"
    big = "alpha\n" + line * 66000
    roots = {}
    for variant, extra in (("big", True), ("small", False)):
        root = os.path.join(work, "shapes", variant)
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(root)
        body = big if extra else "alpha\n"
        for name in ("big.txt", "--") if extra else ("big.txt",):
            with open(os.path.join(root, name), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(body)
        with open(os.path.join(root, "other.txt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("beta\n")
        roots[variant] = root
    return roots


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
    """(verdict, reason, derived) from the gate's own FIG line for fid."""
    for ln in text.splitlines():
        if not ln.startswith("FIG %s " % fid):
            continue
        if " derived=UNAVAILABLE reason=" in ln and ln.endswith(" stale"):
            return "stale", ln.split(" derived=UNAVAILABLE reason=", 1)[1].rsplit(" stale", 1)[0], None
        m = re.search(r" derived=(\S+) ok$", ln)
        if m:
            return "ok", "-", m.group(1)
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


def m_probes_base_paired(c):
    if c.probes_local is None:
        return False, "probes absent at controls revision"
    return _probes(c, "base-paired", c.base_gate, "base")


def m_probes_measured(c):
    if c.probes_local is None:
        return False, "probes absent at controls revision"
    return _probes(c, "measured", c.gate, "candidate")


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
    for key, variant, derive, want, stages, stdin_name in SHAPES:
        root = roots[variant]
        nrc, _ = native_stages(stages, root, stdin_name, c.timeout)
        if nrc[0] != NATIVE_STAGE0[key]:
            problems.append("%s native-stage0=%s want=%d" % (key, nrc[0], NATIVE_STAGE0[key]))
        erc, ereason = PROBE_EXPECT["candidate"][key]
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
            want_verdict = "ok" if erc == 0 else "stale"
            if rc != erc or verdict != want_verdict or reason != ereason:
                problems.append("%s/%s rc=%s verdict=%s reason=%s want=%d/%s/%s" % (
                    key, label, rc, verdict, reason, erc, want_verdict, ereason))
            if verdict == "ok" and derived != want:
                problems.append("%s/%s derived=%s want=%s" % (key, label, derived, want))
        if len(set((g[1], g[2], g[3]) for g in got)) != 1:
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


def m_cat_mutbat(c):
    rel = c.a.cat_mutbat
    rc, data = git(c.src, "show", c.crev + ":" + rel)
    if rc:
        return False, "cat-mutbat %s absent at controls revision" % rel
    pinned = (c.pins.get("controls") or {}).get(rel)
    if pinned is None or sha_bytes(data) != str(pinned):
        return False, "cat-mutbat %s not pinned to its committed bytes" % rel
    local = os.path.join(c.work, "controls", "cat-mutbat.py")
    with open(local, "wb") as fh:
        fh.write(data)
    want = expected_block(c).get("cat_mutbat_summary")
    if c.probes_local is None:
        return False, "probes collector absent at controls revision"
    workdir = os.path.join(c.work, "cat-mutbat")
    shutil.rmtree(workdir, ignore_errors=True)
    rc, text = run_cmd(c, "cat-mutbat", [sys.executable, "-B", local, "--instrument", c.gate,
                                         "--collector", c.probes_local, "--work", workdir],
                       c.work, [local, c.gate, c.probes_local])
    ok = rc == 0 and want is not None and want in text.splitlines()
    return ok, "exit=%d want=%r sha256=%s" % (rc, want, sha_bytes(data))

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
    if a.final and not a.cat_mutbat:
        raise Setup("--final requires --cat-mutbat (the cat limb must be measured)")
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
    names = [n for n in MEASUREMENTS if n != "identity-guards"]
    if a.cat_mutbat:
        names.append("cat-mutbat")
    names.append("identity-guards")
    return names


def main(argv=None):
    ap = argparse.ArgumentParser(description="kasegi r66 C1 committed-input driver")
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
    ap.add_argument("--cat-mutbat", dest="cat_mutbat", default=None,
                    help="committed path (in the controls revision) of the cat-limb mutation battery")
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
        "cat-mutbat": m_cat_mutbat,
        "selftest": m_selftest,
        "mutbat-existing": m_mutbat,
        "real-ledger": m_real_ledger,
        "red-wrong-want": m_red_wrong_want,
        "identity-guards": m_identity_guards,
    }
    results = {}
    # identity-guards is evaluated last so it sees the tree state after every child ran.
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
