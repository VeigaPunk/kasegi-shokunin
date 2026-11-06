#!/usr/bin/env python3
"""G6 tie-limb mutation driver for the frozen r83 entry gate.

For every mutant: build from pristine bytes, --selftest, c2-controls with GATES['r83']
repointed at the mutant, and a tied_ok/gate probe battery. Compare with pristine.
Writes $S/driver.json and prints a table.
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = "/fast/scratch/hyaku/kasegi-r83/MutEntryGate"
GATE = os.path.join(LANE, ".ufo/waves/round-83/c2/entry-gate.py")
CTRL = os.path.join(LANE, ".ufo/waves/round-83/controls/c2-controls-r83.py")
FROZEN_RECEIPT = os.path.join(LANE, ".ufo/waves/round-83/controls/c2-g6-controls-r83.txt")
os.makedirs(S, exist_ok=True)
TMP = os.path.join(S, "tmp")
os.makedirs(TMP, exist_ok=True)
ENV = dict(os.environ, TMPDIR=TMP)


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


with open(GATE, encoding="utf-8", newline="") as fh:
    SRC = fh.read()
PRIS = os.path.join(S, "gate-pristine.py")
if not os.path.exists(PRIS) or sha(PRIS) != sha(GATE):
    shutil.copyfile(GATE, PRIS)


def find_line(prefix):
    hits = [l for l in SRC.split("\n") if l.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]


ANYLINE = find_line("    return any(n in by_line and")
WORDSLINE = find_line("    return {w[:5]")
STOPBLOCK = ('STOP = frozenset("that this with from have will when they them their there which what were "\n'
             '                 "been into than then also only must does each such some more most other "\n'
             '                 "about over under page text rule claim".split())')
assert SRC.count(STOPBLOCK) == 1, STOPBLOCK

MUTANTS = [
    ("tie2to1", [("TIE_WORDS = 2", "TIE_WORDS = 1")],
     "TIE_WORDS 2 -> 1 (one shared stem ties)"),
    ("tie2to0", [("TIE_WORDS = 2", "TIE_WORDS = 0")],
     "TIE_WORDS 2 -> 0 (any located cited line ties)"),
    ("any_to_all", [(ANYLINE, ANYLINE.replace("return any(", "return all(", 1))],
     "any() -> all() over cited lines"),
    ("stem5to3", [(WORDSLINE, WORDSLINE.replace("w[:5]", "w[:3]", 1))],
     "stem cut 5 -> 3 letters"),
    ("stem5to20", [(WORDSLINE, WORDSLINE.replace("w[:5]", "w[:20]", 1))],
     "stem cut 5 -> 20 (no truncation)"),
    ("stop_empty", [(STOPBLOCK, "STOP = frozenset()")],
     "STOP emptied"),
    ("stop_plus_withdrawn",
     [('"about over under page text rule claim".split())',
       '"about over under page text rule claim withdrawn".split())')],
     "STOP gains 'withdrawn'"),
    ("membership_dropped", [(ANYLINE,
                             "    return any(len(rw & by_line.get(n, set())) >= TIE_WORDS for n in cited)")],
     "cited-line membership check dropped (absent line -> empty stem set)"),
    ("membership_union", [(ANYLINE,
                           "    union = set().union(*by_line.values()) if by_line else set()\n"
                           "    return bool(cited) and len(rw & union) >= TIE_WORDS")],
     "cited line ignored: tie against union of the section's span stems"),
    ("cite_not_stripped",
     [(find_line("    rw = words(re.sub("), "    rw = words(rule)")],
     "cite token not stripped from rule text before stemming"),
    ("nocite_true", [(find_line("    cited = [int(n)"),
                      find_line("    cited = [int(n)") + "\n    if not cited:\n        return True")],
     "tied_ok returns True when the rule cites nothing"),
    ("untied_out_of_ok",
     [(find_line("          and claimless == 0"),
       find_line("          and claimless == 0").replace(" and untied == 0", ""))],
     "untied excluded from the ok conjunction"),
    ("untied_not_printed",
     [('            "unpinned=%d ruleless=%d untied=%d header=%s"',
       '            "unpinned=%d ruleless=%d header=%s"'),
      ('               unpinned, ruleless, untied, "ok" if header else "bad"))',
       '               unpinned, ruleless, "ok" if header else "bad"))')],
     "untied counted but dropped from the ENTRY-GATE profile line"),
    ("ge_to_gt", [(ANYLINE, ANYLINE.replace(">= TIE_WORDS", "> TIE_WORDS", 1))],
     "ties needed becomes TIE_WORDS+1 (>= -> >)"),
    ("word_min3", [(WORDSLINE, WORDSLINE.replace("len(w) >= 4", "len(w) >= 3", 1))],
     "content-word minimum length 4 -> 3"),
    ("word_min5", [(WORDSLINE, WORDSLINE.replace("len(w) >= 4", "len(w) >= 5", 1))],
     "content-word minimum length 4 -> 5"),
]

Q = "alpha beta gamma delta"
ENTRY = ('# t\n\nsource: S9 \u2014 u\nverified-at: 2026-11-06\n'
         'recheck: cd /lane && python3 corpus/instruments/source-recheck.py --manifest m.json --source S9\n\n'
         '## Claim 1 \u2014 c\n\n"alpha beta gamma delta" (S9.txt:2)\n\n'
         'Falsifiable rule: one omega and four unrelated tokens here today (S9.txt:2)\n\n'
         'Rejected over-generalization: some filler sentence of at least eight words total.\n')
SNAP = ["", "alpha beta gamma delta", "x"]
MAN = {"_path": "m.json",
       "sources": [{"id": "S9", "path": "S9.txt", "quotes": [{"quote": Q}]}]}


def cbody(span, rule, line=2):
    return ('## Claim 1 \u2014 c\n\n"%s" (S9.txt:%d)\n\nFalsifiable rule: %s\n\n'
            'Rejected over-generalization: filler filler filler filler filler filler filler filler.\n'
            % (span, line, rule))


BODIES = {
    "tie0": cbody("alpha beta gamma delta", "one omega and four unrelated tokens here today (S9.txt:2)"),
    "tie1": cbody("alpha beta gamma delta", "one delta and four unrelated tokens here today (S9.txt:2)"),
    "tie2": cbody("alpha beta gamma delta", "one delta gamma and four unrelated tokens here (S9.txt:2)"),
    "tie3": cbody("alpha beta gamma delta", "one delta gamma alpha and four unrelated tokens (S9.txt:2)"),
    "nocite": cbody("alpha beta gamma delta",
                    "one delta gamma alpha and four unrelated tokens here today no citation"),
    "absentcite": cbody("alpha beta gamma delta",
                        "one delta gamma alpha and four unrelated tokens here (S9.txt:9)"),
    "twocites": cbody("alpha beta gamma delta",
                      "one delta gamma alpha and four unrelated tokens (S9.txt:2) and (S9.txt:9)"),
    "stem": cbody("imported records withdrawn",
                  "imports record withdrawal and four unrelated tokens here (S9.txt:2)"),
    "stop": cbody("this rule claims that text",
                  "that text with this and more unrelated tokens here (S9.txt:2)"),
    "withdrawn": cbody("withdrawn imports",
                       "withdrawn imports and more filler words here (S9.txt:2)"),
    "stem35": cbody("import records",
                    "improve recipe and four unrelated tokens here (S9.txt:2)"),
    "len3": cbody("sky ice",
                  "ice sky and more filler words here (S9.txt:2)"),
}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def probes(path, name):
    mod = load(path, name)
    out = {}
    for cname, body in BODIES.items():
        cs = re.findall(mod.SPAN_RE % re.escape("S9"), body)
        try:
            out[cname] = mod.tied_ok(body, "S9", cs)
        except Exception as exc:  # noqa: BLE001
            out[cname] = "ERR:%s" % type(exc).__name__
    try:
        ok, line = mod.gate(ENTRY, MAN, "S9", "/lane", SNAP)
        out["gate_ok"] = ok
        out["gate_line"] = line
    except Exception as exc:  # noqa: BLE001
        out["gate_ok"] = "ERR:%s" % type(exc).__name__
        out["gate_line"] = ""
    return out


def selftest(py):
    r = subprocess.run([sys.executable, "-B", py, "--selftest"], capture_output=True,
                       text=True, env=ENV, cwd=LANE)
    first = (r.stdout.strip().splitlines() or [""])[0]
    return r.returncode, first, r.stderr.strip()[-400:]


def controls(py, tag):
    cpath = os.path.join(S, "controls-%s.py" % tag)
    text = open(CTRL, encoding="utf-8").read()
    old = '"r83": ".ufo/waves/round-83/c2/entry-gate.py"'
    assert text.count(old) == 1
    text = text.replace(old, '"r83": %r' % py)
    with open(cpath, "w", encoding="utf-8") as fh:
        fh.write(text)
    work = os.path.join(S, "work-%s" % tag)
    r = subprocess.run([sys.executable, "-B", cpath, "--lane", LANE, "--work", work],
                       capture_output=True, text=True, env=ENV)
    lines = [l for l in r.stdout.splitlines() if l.startswith("CONTROL")]
    return r.returncode, lines, r.stderr.strip()[-400:]


def register_lines(lines):
    return [l for l in lines if " gate=r83 " in l]


def main():
    res = {"gate_sha256": sha(GATE), "gate_bytes": len(SRC.encode()),
           "mutants": [], "baselines": {}}

    b_inlane_rc, b_inlane, b_inlane_err = controls(os.path.join(LANE, ".ufo/waves/round-83/c2/entry-gate.py")
                                                   if False else GATE, "frozen")
    # the frozen controls script itself, unmodified, for the true baseline
    r = subprocess.run([sys.executable, "-B", CTRL, "--lane", LANE,
                        "--work", os.path.join(S, "work-inlane")],
                       capture_output=True, text=True, env=ENV)
    inlane = [l for l in r.stdout.splitlines() if l.startswith("CONTROL")]
    base_rc, base_lines, base_err = controls(PRIS, "pristine")
    base_st_rc, base_st_line, _ = selftest(PRIS)
    base_probes = probes(PRIS, "pristine")

    frozen = [l for l in open(FROZEN_RECEIPT, encoding="utf-8").read().splitlines()
              if l.startswith("CONTROL") and " gate=r83 " in l]
    res["baselines"] = {
        "pristine_selftest": {"rc": base_st_rc, "line": base_st_line},
        "controls_rc": base_rc,
        "r83_lines": register_lines(base_lines),
        "frozen_receipt_r83_lines": frozen,
        "matches_frozen_receipt": register_lines(base_lines) == frozen,
        "unmodified_controls_r83_lines": register_lines(inlane),
        "unmodified_controls_rc": r.returncode,
        "unmodified_matches_copied_baseline": register_lines(inlane) == register_lines(base_lines),
        "stderr": base_err + " | " + b_inlane_err,
    }
    print("BASELINE gate_sha256=%s bytes=%d" % (res["gate_sha256"], res["gate_bytes"]))
    print("BASELINE selftest rc=%d %s" % (base_st_rc, base_st_line))
    print("BASELINE controls_rc=%d r83_lines=%d matches_frozen_receipt=%s unmodified_matches=%s"
          % (base_rc, len(register_lines(base_lines)), res["baselines"]["matches_frozen_receipt"],
             res["baselines"]["unmodified_matches_copied_baseline"]))
    print("BASELINE probes=%s" % json.dumps(base_probes, sort_keys=True))

    for name, subs, note in MUTANTS:
        mut = SRC
        for old, new in subs:
            assert mut.count(old) == 1, (name, old, mut.count(old))
            mut = mut.replace(old, new)
        path = os.path.join(S, "gate-%s.py" % name)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(mut)
        msha = sha(path)

        st_rc, st_line, st_err = selftest(path)
        c_rc, c_lines, c_err = controls(path, name)
        mp = probes(path, name)
        diff = [(b, m) for b, m in zip(register_lines(base_lines), register_lines(c_lines)) if b != m]
        if len(register_lines(c_lines)) != len(register_lines(base_lines)):
            diff.append(("LINE-COUNT", len(register_lines(c_lines))))
        pchanged = {k: [base_probes.get(k), mp.get(k)] for k in mp
                    if base_probes.get(k) != mp.get(k)}
        if st_rc != 0:
            verdict = "KILLED-selftest"
        elif diff:
            verdict = "KILLED-controls"
        elif not pchanged:
            verdict = "SURVIVED-equivalent-on-exercised-points"
        else:
            verdict = "SURVIVED-undetected"
        rec = {"name": name, "note": note, "mutant_sha256": msha, "mutant_bytes": len(mut.encode()),
               "selftest": {"rc": st_rc, "line": st_line, "stderr": st_err},
               "controls": {"rc": c_rc, "diff": diff, "stderr": c_err},
               "probe_changes": pchanged, "verdict": verdict,
               "ok_flips": [k for k in pchanged if k in ("gate_ok", "tie0", "tie1", "tie2",
                                                          "tie3", "nocite", "stem", "stop",
                                                          "withdrawn", "twocites", "absentcite")]}
        res["mutants"].append(rec)
        print("MUTANT %s bytes=%d sha=%s" % (name, rec["mutant_bytes"], msha))
        print("  selftest rc=%d %s" % (st_rc, st_line))
        print("  controls rc=%d r83_diffs=%d" % (c_rc, len(diff)))
        for b, m in diff[:4]:
            print("    - %s" % b)
            print("    + %s" % m)
        print("  probes_changed=%s" % json.dumps(pchanged, sort_keys=True))
        print("  VERDICT %s" % verdict)

    r_rc, r_lines, r_err = controls(PRIS, "restored")
    res["restored_baseline"] = {"controls_rc": r_rc,
                                "same_as_first_baseline": register_lines(r_lines) == register_lines(base_lines),
                                "stderr": r_err}
    print("RESTORED-RUN controls_rc=%d same_as_first_baseline=%s"
          % (r_rc, res["restored_baseline"]["same_as_first_baseline"]))
    res["restored_gate_sha256"] = sha(GATE)
    res["gate_bytes_unchanged"] = (res["restored_gate_sha256"] == res["gate_sha256"]
                                   and os.path.getsize(GATE) == res["gate_bytes"])
    print("RESTORED lane_gate_sha256=%s unchanged=%s" % (res["restored_gate_sha256"],
                                                          res["gate_bytes_unchanged"]))
    with open(os.path.join(S, "driver.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
