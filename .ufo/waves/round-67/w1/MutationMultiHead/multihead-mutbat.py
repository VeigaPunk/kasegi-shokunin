#!/usr/bin/env python3
"""multihead-mutbat.py — R67 limb battery for the per-head SIGPIPE input-count rule.

One limb = ONE text replacement at the smallest behaviour-bearing point of the
candidate gate.  A limb is killed only by a NAMED detector: either the candidate's
own `--selftest` turning red, or one of the named ledger probes whose expected
ok/stale+reason differs from the mutant's.  Semantically equivalent mutants are
recorded as EQUIVALENT and never counted as kills.  Invalid mutants (anchor not
exact-once, syntax error, setup failure) are rejected and never counted.

Usage:
  python3 -B multihead-mutbat.py --instrument /abs/figure-audit.py --work /abs/scratch
                                 [--collector /abs/probes.py] [--keep] [--dump-anchors]

--work must be owned scratch (created if missing, removed on exit unless --keep).
--collector is optional: a Python file defining `probe_table(root)` may supply the
named probes; otherwise the built-in table is used (the `probes=` line records
which).  This battery is not a sandbox: it executes the selected instrument's
selftest and its probes.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BIG_LINES = 4096          # 4 MiB fixtures: far past the 64 KiB pipe buffer
LINE = 1023


# ---------------------------------------------------------------- fixtures
def build_root(root):
    """Deterministic fixtures: big.txt/other.txt start alpha/beta, 4 MiB each."""
    root = Path(root)
    (root / "corpus" / "instruments").mkdir(parents=True, exist_ok=True)
    big = "alpha\n" + ("x" * LINE + "\n") * (BIG_LINES - 1)
    (root / "big.txt").write_text(big, encoding="utf-8", newline="\n")
    (root / "other.txt").write_text("beta\n" + ("y" * LINE + "\n") * (BIG_LINES - 1),
                                    encoding="utf-8", newline="\n")
    (root / "xlines.txt").write_text(("x" + "z" * (LINE - 1) + "\n") * BIG_LINES,
                                     encoding="utf-8", newline="\n")
    (root / "small.txt").write_text("7\n", encoding="utf-8", newline="\n")
    # Dash-named operands: reachable only after a leading `--` separator.
    (root / "-a").write_text(big, encoding="utf-8", newline="\n")
    (root / "-c").write_text("gamma\n" + ("r" * LINE + "\n") * (BIG_LINES - 1),
                             encoding="utf-8", newline="\n")
    (root / "corpus" / "instruments" / "pipe.py").write_text(
        "import signal, sys\n"
        "signal.signal(signal.SIGPIPE, signal.SIG_DFL)\n"
        "sys.stdout.write(('x' * 1023 + '\\n') * 4096)\n"
        "sys.stdout.flush()\n", encoding="utf-8", newline="\n")
    return root


def sha_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- probes
# (id, derive, expectation): ("ok", literal) or ("stale", reason) where reason may
# be a tuple of accepted reasons.
def probe_table(root):
    big_sha = sha_of(Path(root) / "big.txt")
    return [
        # multi-input read-only heads: the stage dies of SIGPIPE before the later
        # named operand is opened.  Correct rule: stale.  Base: false green.
        ("P1-cut-multi-missing", "cut -f1 -d: big.txt missing.txt | head -n 1",
         ("stale", "derive-upstream-signal-13")),
        ("P2-wc-multi-missing", "wc -l big.txt missing.txt | head -n 1",
         ("stale", ("derive-upstream-signal-13", "derive-upstream-exit-1"))),
        ("P3-grep-multi-missing", "grep x xlines.txt missing.txt | head -n 1",
         ("stale", "derive-upstream-signal-13")),
        ("P4-grep-two-existing", "grep x xlines.txt big.txt | head -n 1",
         ("stale", "derive-upstream-signal-13")),
        # single-input controls stay benign
        ("P5-cut-single", "cut -f1 -d: big.txt | head -n 1", ("ok", "alpha")),
        ("P6-wc-single", "wc -l big.txt | head -n 1", ("ok", "4096 big.txt")),
        ("P7-sha-single", "sha256sum big.txt | head -n 1",
         ("ok", "%s  big.txt" % big_sha)),
        ("P8-grep-single-sigpipe", "grep x big.txt | head -n 1",
         ("ok", "x" * LINE)),
        # round-66 cat behaviour must stay byte-identical
        ("P9-cat-single", "cat big.txt | head -n 1", ("ok", "alpha")),
        ("P10-cat-multi", "cat big.txt missing.txt | head -n 1",
         ("stale", "derive-upstream-signal-13")),
        # end-of-options: the candidate splits argv at the FIRST `--` anywhere, so
        # everything after it counts as an operand — including grep's pattern, which
        # makes the single-file `grep -- pattern file` a SAFE false stale (native -13).
        # The limb-4 mutant (leading-only drop) exempts it instead, so this probe kills it.
        ("P11-dashdash-leading", "grep -- x big.txt | head -n 1",
         ("stale", "derive-upstream-signal-13")),
        # unknown heads (python/git) keep the old benign SIGPIPE rule
        ("P12-unknown-head-sigpipe",
         "python3 corpus/instruments/pipe.py | head -n 1 | wc -l", ("ok", "1")),
        # existing status path for head: multi-input is an ordinary exit-1 stale
        ("P13-head-multi-exit1", "head -n 5 big.txt missing.txt | head -n 1",
         ("stale", "derive-upstream-exit-1")),
        # wc with its first operand first (no option token to absorb the skip):
        # two existing inputs, 4 MiB each, measured 141 on 30/30 repeats.
        ("P14-wc-two-existing", "wc small.txt big.txt | head -n 1",
         ("stale", "derive-upstream-signal-13")),
    ]


def classify(out):
    """Return ('ok', value) / ('value', derived) / ('stale', reason) / ('harness', text).

    ('value', ...) means the derive SUCCEEDED but the recorded want differed (the
    battery records a sentinel for probes that must be stale), so it is not a stale.
    """
    for line in out.splitlines():
        if line.startswith("FIG "):
            m = re.search(r"derived=UNAVAILABLE reason=(\S+) stale", line)
            if m:
                return ("stale", m.group(1))
            if line.endswith(" ok"):
                return ("ok", line.split(" derived=", 1)[1].rsplit(" ok", 1)[0])
            if " derived=" in line:
                return ("value", line.split(" derived=", 1)[1].split(" want=", 1)[0])
            return ("harness", line[:200])
    return ("harness", out.strip()[-200:])


def run_probe(gate, root, derive, want, tmpdir):
    literal = want[1] if want[0] == "ok" else "SENTINEL"
    ledger = {"figures": [{"id": "p", "record": "probe", "recorded": literal,
                           "derive": derive, "want": literal}]}
    lp = os.path.join(tmpdir, "probe-ledger.json")
    with open(lp, "w", encoding="utf-8") as f:
        json.dump(ledger, f)
    try:
        p = subprocess.run([sys.executable, "-B", str(gate), "--ledger", lp,
                            "--root", str(root)], cwd=str(root),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, timeout=300)
    except subprocess.SubprocessError as exc:
        return ("harness", "%s: %s" % (type(exc).__name__, exc))
    return classify(p.stdout)


def matches(got, want):
    if got[0] != want[0]:
        return False
    if want[0] == "ok":
        return got[1].strip() == want[1]
    reasons = want[1] if isinstance(want[1], tuple) else (want[1],)
    return got[1] in reasons


def selftest(gate, tmp):
    env = dict(os.environ, HYAKU_SCRATCH=str(tmp), TMPDIR=str(tmp))
    try:
        p = subprocess.run([sys.executable, "-B", str(gate), "--selftest"],
                           cwd=str(tmp), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, timeout=900, env=env)
    except subprocess.SubprocessError as exc:
        return None, "harness:%s" % type(exc).__name__
    lines = (p.stdout or "").strip().splitlines()
    return p.returncode, lines[-1] if lines else ""


# ---------------------------------------------------------------- limbs
# Each limb: (id, sites, kill_case).  A site is (regex, replacement) where the
# replacement may be a string or a callable(match)->str.  Every regex must match
# exactly once; otherwise the limb is invalid.
def _set_group(idx, text):
    """Replacement callable: substitute capture group `idx` with `text`."""
    def f(m):
        return m.group(0)[:m.start(idx) - m.start(0)] + text + \
            m.group(0)[m.end(idx) - m.start(0):]
    return f


LIMBS = [
    # (1) grep base 1 -> 0
    ("L1-grep-base-1-to-0",
     [(r'(["\'])grep\1\s*:\s*(1)\b', _set_group(2, "0"))],
     "P8-grep-single-sigpipe"),
    # (2) grep base 1 -> 2
    ("L2-grep-base-1-to-2",
     [(r'(["\'])grep\1\s*:\s*(1)\b', _set_group(2, "2"))],
     "P4-grep-two-existing"),
    # (3) cat/cut/wc base 0 -> 1 (explicit entries; base is `.get(head, 0)`)
    ("L3-catcutwc-base-0-to-1",
     [(r'SIGPIPE_REQUIRED_NONFILE_ARGS = \{"grep": 1\}',
       'SIGPIPE_REQUIRED_NONFILE_ARGS = {"grep": 1, "cat": 1, "cut": 1, "wc": 1}')],
     "P14-wc-two-existing"),
    # (4) drop the end-of-options handling: replace the first-`--`-anywhere split with
    # the old leading-only drop (the pre-L1-defect-3 shape)
    ("L4-drop-dashdash",
     [(r'(?m)^([ \t]*)tokens = list\(argv\[1:\]\)\n[ \t]*for i, t in enumerate\(tokens\):\n[ \t]*if t == "--":\n[ \t]*pre, post = tokens\[:i\], tokens\[i \+ 1:\]\n[ \t]*break\n[ \t]*else:\n[ \t]*pre, post = tokens, \[\]\n',
       "\\1tokens = list(argv[1:])\n\\1if tokens and tokens[0] == \"--\":\n\\1    tokens = tokens[1:]\n\\1pre, post = tokens, []\n")],
     "P11-dashdash-leading"),
    # (5) count option tokens as operands
    ("L5-count-options-as-operands",
     [(r'return sum\(1 for t in pre if not \(t\.startswith\("-"\) and t != "-"\)\) \+ len\(post\)',
       'return len(pre) + len(post)')],
     "P5-cut-single"),
    # (6) treat every unknown head as stale
    ("L6-unknown-head-stale",
     [(r'(?m)^([ \t]*)if head_name in READ_ONLY_HEADS:\n[ \t]*return sigpipe_input_count\(head_name, stage_argv\) > 1\n[ \t]*return False\n',
       "\\1if head_name in READ_ONLY_HEADS:\n\\1    return sigpipe_input_count(head_name, stage_argv) > 1\n\\1return True  # MUTANT: unknown head stale\n")],
     "P12-unknown-head-sigpipe"),
    # (7) exempt everything on SIGPIPE (old head-blind rule)
    ("L7-headblind-sigpipe-exempt",
     [(r'(?m)^([ \t]*)if head_name == "cat":\n[ \t]*return not cat_sigpipe_exempt\(stage_argv\)\n[ \t]*if head_name in READ_ONLY_HEADS:\n[ \t]*return sigpipe_input_count\(head_name, stage_argv\) > 1\n[ \t]*return False\n',
       "\\1return False  # MUTANT: head-blind SIGPIPE exemption\n")],
     "P1-cut-multi-missing"),
]

# Probes whose native face is timing-dependent on this host (wc's per-file write races
# the downstream close): the pristine face is captured twice and mutants must reproduce
# it, but it is never counted in the contract `failures`.
DIFFERENTIAL = ("P2-wc-multi-missing", "P14-wc-two-existing")

EQUIVALENTS = [
    ("E1-trailing-space-control",
     [(r'(return sum\(1 for t in pre if not \(t\.startswith\("-"\) and t != "-"\)\) \+ len\(post\))\n',
       "\\1  \n")],
     "trailing-space control: two bytes added, no behavioural change"),
    ("E2-le-one-vs-lt-two", [(r'<= 1\b', "< 2")],
     "len(x) <= 1 and len(x) < 2 are the same predicate over integers"),
    ("E3-sigpipe-constant", [(r'-signal\.SIGPIPE', "-13")],
     "signal.SIGPIPE is 13 on this host and the status is negated"),
]


def apply_sites(text, sites):
    out = text
    for pat, repl in sites:
        rx = re.compile(pat)
        hits = list(rx.finditer(out))
        if len(hits) != 1:
            return None, "sites=%d" % len(hits)
        m = hits[0]
        new = repl(m) if callable(repl) else m.expand(repl)
        out = out[:m.start()] + new + out[m.end():]
    return out, None


def _norm_want(want):
    if not isinstance(want, (tuple, list)) or len(want) != 2:
        return None
    kind = str(want[0])
    if kind not in ("ok", "stale"):
        return None
    val = want[1]
    if kind == "stale":
        val = tuple(str(x) for x in val) if isinstance(val, (tuple, list)) else str(val)
    return (kind, val)


def load_collector(path, builtin_root, work, gate, tmp):
    """Consume an optional shared collector; returns (extra_probes, label, notes, mismatch).

    extra_probes are 4-tuples (id, derive, want, root) with ids prefixed 'C:' so they
    never collide with the built-in P-ids.  Two shapes are supported:

    * `probe_table(root)` -> [(id, derive, ("ok", want)|("stale", reason))]: the
      declared expectations are used for mutant detection; a pristine mismatch is
      reported as COLLECTOR-BASE and counted separately, never as a built-in failure;
    * a `PROBES` dict {name: (derive, ...)}: expectations are CAPTURED from the
      pristine instrument (two agreeing runs), so the collector acts as a
      differential detector for the exact bytes under test.

    `build_fixtures(work)` is called when present so collector derives run against
    the collector's own pinned fixtures.  Any probe whose pristine result is not
    stable across two runs is dropped (reported as COLLECTOR unstable=...).
    """
    if path is None:
        return [], "builtin", [], 0
    notes = []
    try:
        spec = importlib.util.spec_from_file_location("collector", str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as exc:  # noqa: BLE001 - a broken collector is reported, not hidden
        return [], "builtin", ["COLLECTOR ignored=%s reason=%s" % (
            path, type(exc).__name__)], 0

    croot = work / "collector-root"
    croot.mkdir(exist_ok=True)
    has_fixtures = hasattr(mod, "build_fixtures")
    if has_fixtures:
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                err = mod.build_fixtures(str(croot))
        except Exception as exc:  # noqa: BLE001
            err = "build_fixtures raised %s" % type(exc).__name__
        if err:
            notes.append("COLLECTOR fixtures=fail detail=%s" % err)
            return [], "builtin", notes, 0
        notes.append("COLLECTOR fixtures=ok root=%s" % croot)
    root = croot if has_fixtures else builtin_root

    declared, shape = [], None
    if hasattr(mod, "probe_table"):
        try:
            table = mod.probe_table(str(root))
            declared = [(str(a), str(b), _norm_want(c)) for a, b, c in table]
            shape = "probe_table"
        except Exception as exc:  # noqa: BLE001
            notes.append("COLLECTOR probe_table=fail reason=%s" % type(exc).__name__)
            declared = []
    if not declared and hasattr(mod, "PROBES"):
        shape = "PROBES-capture"
        order = list(getattr(mod, "PROBE_ORDER", ())) or list(mod.PROBES)
        declared = [(str(n), str(mod.PROBES[n][0]), None) for n in order]
    if not declared:
        notes.append("COLLECTOR ignored=%s reason=no-probe_table-or-PROBES" % path)
        return [], "builtin", notes, 0
    # Conditional rows whose acceptance is reason any-of (the collector says so in its
    # own docstring); never pin them to a single frozen reason.
    reason_sets = {
        "P10": getattr(mod, "P10_REASON_SET", None),
        "P19": getattr(mod, "P1920_REASON_SET", None),
        "P20": getattr(mod, "P1920_REASON_SET", None),
    }
    declared = [(cid, derive,
                 (want[0], tuple(reason_sets[cid]))
                 if want and want[0] == "stale" and cid in reason_sets and reason_sets[cid]
                 else want)
                for cid, derive, want in declared]

    extra, unstable, mismatch = [], [], 0
    for cid, derive, want in declared:
        first = run_probe(gate, root, derive, want if want else ("stale", "?"), str(tmp))
        second = run_probe(gate, root, derive, want if want else ("stale", "?"), str(tmp))
        if first[0] == "harness" or second[0] == "harness":
            notes.append("COLLECTOR harness-error=%s detail=%r" % (cid, first))
            continue
        if first != second:
            unstable.append(cid)
            continue
        if want is None:
            want = first  # captured differential expectation
        elif not matches(first, want):
            mismatch += 1
            notes.append("COLLECTOR-BASE mismatch=%s got=%r want=%r" % (
                cid, first, want))
        extra.append(("C:" + cid, derive, want, root))
    if unstable:
        notes.append("COLLECTOR unstable=%s" % ",".join(unstable))
    return extra, "collector:%s(%s)" % (sha_of(path), shape), notes, mismatch


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--instrument", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--collector", type=Path, default=None)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--dump-anchors", action="store_true")
    args = ap.parse_args()

    instrument = args.instrument.resolve()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    tmp = work / "tmp"
    tmp.mkdir(exist_ok=True)
    root = build_root(work / "root")

    pristine = instrument.read_text(encoding="utf-8")
    print("instrument=%s sha256=%s bytes=%d" % (
        instrument, hashlib.sha256(instrument.read_bytes()).hexdigest(), len(pristine)))

    if args.dump_anchors:
        for lid, sites, _ in LIMBS + EQUIVALENTS:
            for pat, _r in sites:
                print("%-28s sites=%d pattern=%r" % (
                    lid, len(re.findall(pat, pristine)), pat))
        return 0

    builtin = [("P" + pid[1:], derive, want, root)
               for pid, derive, want in probe_table(root)]
    extra, probe_label, notes, collector_mismatch = load_collector(
        args.collector, root, work, instrument, tmp)
    for line in notes:
        print(line)
    probes = builtin + extra
    print("probes=%s count=%d builtin=%d collector=%d" % (
        probe_label, len(probes), len(builtin), len(extra)))

    failures = 0
    print("--- pristine baseline")
    resolved = []
    for pid, derive, want, proot in probes:
        got = run_probe(instrument, proot, derive, want, str(tmp))
        if pid in DIFFERENTIAL:
            # wc's SIGPIPE face is timing-dependent on this host (measured -13 and
            # exit-1): pin the face the pristine instrument actually shows, twice,
            # and require mutants to reproduce it.  Never counted in `failures`.
            again = run_probe(instrument, proot, derive, want, str(tmp))
            if got != again:
                print("DIFFERENTIAL %s unstable=%r/%r dropped=1" % (pid, got, again))
                continue
            print("DIFFERENTIAL %s captured=%r" % (pid, got))
            resolved.append((pid, derive, got, proot))
            continue
        good = matches(got, want)
        if not pid.startswith("C:"):
            failures += 0 if good else 1
        print("BASE %s got=%r want=%r verdict=%s" % (
            pid, got, want, "pass" if good else "FAIL"))
        resolved.append((pid, derive, want, proot))
    probes = resolved
    st_rc, st_last = selftest(instrument, tmp)
    st_ok = st_rc == 0 and str(st_last).startswith("selftest cases=")
    failures += 0 if st_ok else 1
    print("BASE selftest exit=%r last=%r" % (st_rc, st_last))

    if failures:
        # A baseline failure is inconclusive, never a killed mutant.
        for lid, _s, _k in LIMBS + EQUIVALENTS:
            print("MUTANT %s invalid by=pristine-baseline-not-satisfied" % lid)
        print("MUTBAT killed=0/%d survivors=0 equivalents=0 invalid_rejected=%d failures=%d" % (
            len(LIMBS), len(LIMBS) + len(EQUIVALENTS), failures))
        if collector_mismatch:
            print("COLLECTOR-BASE mismatches=%d" % collector_mismatch)
        if not args.keep:
            shutil.rmtree(work, ignore_errors=True)
        return 1

    killed = survivors = invalid = 0
    equiv_held = 0
    for lid, sites, kill in LIMBS:
        text, why = apply_sites(pristine, sites)
        if text is None:
            print("MUTANT %s invalid by=anchor-%s" % (lid, why))
            invalid += 1
            failures += 1
            continue
        try:
            compile(text, lid + ".py", "exec")
        except SyntaxError as exc:
            print("MUTANT %s invalid by=syntax-%s" % (lid, str(exc).split("(")[0]))
            invalid += 1
            failures += 1
            continue
        path = work / (lid + ".py")
        path.write_text(text, encoding="utf-8", newline="\n")
        st_rc, st_last = selftest(path, tmp)
        st_killed = st_rc == 1 and str(st_last).startswith("selftest cases=")
        dev = []
        harness = False
        for pid, derive, want, proot in probes:
            got = run_probe(path, proot, derive, want, str(tmp))
            if got[0] == "harness":
                harness = True
                dev.append((pid, got))
            elif not matches(got, want):
                dev.append((pid, got))
        if harness:
            print("MUTANT %s invalid by=probe-harness-error detail=%r" % (lid, dev))
            invalid += 1
            failures += 1
            continue
        by = None
        if kill in [d[0] for d in dev]:
            by = kill
        elif dev:
            by = dev[0][0]
        elif st_killed:
            by = "selftest"
        if by is not None:
            killed += 1
            print("MUTANT %s killed by=%s selftest_exit=%r deviations=%r" % (
                lid, by, st_rc, [(d[0], d[1]) for d in dev]))
        else:
            survivors += 1
            print("MUTANT %s survived by=- selftest_exit=%r deviations=[]" % (lid, st_rc))

    print("--- equivalents")
    for lid, sites, reason in EQUIVALENTS:
        text, why = apply_sites(pristine, sites)
        if text is None:
            print("MUTANT %s invalid by=anchor-%s" % (lid, why))
            invalid += 1
            failures += 1
            continue
        try:
            compile(text, lid + ".py", "exec")
        except SyntaxError as exc:
            print("MUTANT %s invalid by=syntax-%s" % (lid, str(exc).split("(")[0]))
            invalid += 1
            failures += 1
            continue
        path = work / (lid + ".py")
        path.write_text(text, encoding="utf-8", newline="\n")
        st_rc, st_last = selftest(path, tmp)
        same = st_rc == 0 and all(
            matches(run_probe(path, proot, d, w, str(tmp)), w)
            for _p, d, w, proot in probes)
        if same:
            equiv_held += 1
            print("MUTANT %s equivalent by=%s" % (lid, reason))
        else:
            print("MUTANT %s invalid by=not-equivalent selftest_exit=%r" % (lid, st_rc))
            invalid += 1
            failures += 1

    print("MUTBAT killed=%d/%d survivors=%d equivalents=%d invalid_rejected=%d failures=%d" % (
        killed, len(LIMBS), survivors, equiv_held, invalid, failures))
    if collector_mismatch:
        print("COLLECTOR-BASE mismatches=%d" % collector_mismatch)
    if not args.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 0 if failures == 0 and survivors == 0 and killed == len(LIMBS) \
        and collector_mismatch == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError) as exc:
        print("mutbat unavailable=%s detail=%s" % (type(exc).__name__, exc),
              file=sys.stderr)
        sys.exit(2)
