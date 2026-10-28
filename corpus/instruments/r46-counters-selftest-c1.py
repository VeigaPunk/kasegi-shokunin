#!/usr/bin/env python3
"""r46-counters-selftest-c1.py - falsification harness for the frozen round-46 C1 counter
(corpus/instruments/r46-c1-gate.py).  Stdlib only; honours TMPDIR / --work; never edits the counter.

WHAT IT DOES
    1. copies the pure base export (--pure) twice: BASE (read-only baseline) and TIP (a COMPLETE
       synthetic tip: the counter is copied in, claim-package-contract.md and claim-gates.md get a
       real `## Re-ground (round 46)` section (8 and 7 rows over corpus/instruments/claim-package-check.py
       and the exemplar fixture; line numbers are LOCATED in the committed bytes at build time) and
       their recheck line becomes `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry ...`).
    2. asserts TIP reads `c1-gate fixed=7/7 exit=0`, a do-nothing control (tree = baseline = pure) reads
       1/7, and positive boundary controls (exactly 6 rows; an extra prose note) still read 7/7.
    3. applies one edit per mutant to a fresh copy of TIP and asserts (a) the targeted limb reads
       pass=0 and (b) fixed < 7.  A mutant the frozen counter does NOT reject is a FALSE-GREEN: it is
       printed `FALSE-GREEN` with its recipe, and counted as a failure.
OUTPUT
    one `case ...` line per case, `FALSE-GREEN ...`/`UNEXPECTED ...` detail lines, and last
    `selftest cases=<N> failures=<F>`.  Exit 0 only when F = 0.
USAGE
    python3 r46-counters-selftest-c1.py [--lane DIR] [--pure DIR] [--counter FILE] [--work DIR] [--jobs N] [--keep]
"""
from __future__ import annotations

import argparse
import atexit
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"
SECTION = "## Re-ground (round 46)"
CK = "corpus/instruments/claim-package-check.py"
FX = "corpus/instruments/fixtures/claim-package/exemplar"
INTRO = ("Rows re-ground the entry's current claims on committed bytes; every line above this "
         "section stays a historical observation of the lost tree.")
GATE = "corpus/instruments/r46-c1-gate.py"


def norm(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def rd(root: str, rel: str) -> str:
    with open(os.path.join(root, rel), "r", encoding="utf-8") as fh:
        return fh.read()


def wr(root: str, rel: str, text: str) -> None:
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


def loc(pure: str, rel: str, token: str, span: int = 1) -> str:
    """Return `rel:a[-b]` for the first line carrying the token (token may continue over `span` lines)."""
    lines = rd(pure, rel).splitlines()
    head = norm(token)[:18]
    for i, ln in enumerate(lines):
        if head in norm(ln) and norm(token) in norm(" ".join(lines[i:i + span])):
            return "%s:%d" % (rel, i + 1) if span == 1 else "%s:%d-%d" % (rel, i + 1, i + span)
    raise SystemExit("selftest setup: token %r not found in %s" % (token, rel))


# (claim in the entry's words, anchored file, token, span)
ROWS = {
    "claim-package-contract.md": [
        ("manifest carries schema_version evidence-manifest/v1", CK, "schema_version') != 'evidence-manifest/v1'", 1),
        ("six files: report, checklist, manifest, custodian receipts, provenance, status", CK, "'custodian-receipts.json',", 1),
        ("every custodian action: scope_signal exactly NO_SCOPE_OBJECTION", CK, "decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'", 1),
        ("report carries the literal No submission performed", CK, "NO_SUBMISSION = 'No submission performed'", 1),
        ("claim_review.hard_gates list the four hard gates", CK, "'no_duplicate_or_prior_submission',", 1),
        ("claim_review.reviewer must be a distinct identity", CK, "reviewer=not-distinct", 1),
        ("at least one positive-polarity artifact (exemplar manifest)", FX + "/evidence/manifest.json", '"polarity": "positive"', 1),
        ("custodian chain scope_signal (exemplar receipts)", FX + "/custodian-receipts.json", '"scope_signal": "NO_SCOPE_OBJECTION"', 1),
    ],
    "claim-gates.md": [
        ("per-file size cap 5 MiB", CK, "MAX_SCAN_BYTES = 5 * 1024 * 1024", 1),
        ("one permissive secret regex over credential words", CK, "(?i)\\b(?:api[_-]?key", 1),
        ("blanket symlink ban in the package tree", CK, "no symlink in the package tree", 1),
        ("hard gates include evidence_integrity", CK, "'evidence_integrity',", 1),
        ("head_sha256 = final decision digest = manifest expected head", CK, "head_sha256 equals the final decision digest", 2),
        ("subchecks no_secrets and operator_attribution", CK, "SUBCHECK_KEYS = ('no_secrets', 'operator_attribution')", 1),
        ("manifest carries expected_head_sha256 (exemplar)", FX + "/evidence/manifest.json", '"expected_head_sha256"', 1),
    ],
}


def row_line(gid: str, claim: str, anchor: str, token: str) -> str:
    return "| %s | %s | `%s` | `%s` |" % (gid, claim, anchor, token)


def build_rows(pure: str, name: str) -> list[str]:
    out = []
    for i, (claim, rel, tok, span) in enumerate(ROWS[name], 1):
        out.append(row_line("G%d" % i, claim, loc(pure, rel, tok, span), tok))
    return out


def section_text(rows: list[str]) -> str:
    return "\n".join(["", SECTION, "", INTRO, "", "| id | current claim | committed anchor | token |", "|---|---|---|---|"] + rows) + "\n"


def rec_line(name: str) -> str:
    return "recheck: cd %s && python3 %s --entry corpus/knowledge/%s" % (LANE, GATE, name)


def set_recheck(t: str, name: str, new: str | None) -> None:
    rel = "corpus/knowledge/" + name
    ls = rd(t, rel).split("\n")
    i = next(i for i, ln in enumerate(ls) if ln.startswith("recheck:"))
    if new is None:
        del ls[i]
    else:
        ls[i] = new
    wr(t, rel, "\n".join(ls))


def edit(t: str, rel: str, fn) -> None:
    old = rd(t, rel)
    new = fn(old)
    assert new != old, "mutation was a no-op on " + rel
    wr(t, rel, new)


def row_edit(t: str, name: str, gid: str, fn) -> None:
    def go(text: str) -> str:
        ls = text.split("\n")
        i = next(i for i, ln in enumerate(ls) if re.match(r"^\|\s*%s\s*\|" % gid, ln))
        ls[i] = fn(ls[i])
        return "\n".join(ls)
    edit(t, "corpus/knowledge/" + name, go)


def drop_rows(t: str, name: str, gids: list[str]) -> None:
    def go(text: str) -> str:
        return "\n".join(ln for ln in text.split("\n") if not any(re.match(r"^\|\s*%s\s*\|" % g, ln) for g in gids))
    edit(t, "corpus/knowledge/" + name, go)


def build_tip(pure: str, counter: str, dest: str) -> None:
    shutil.copytree(pure, dest, symlinks=True)
    shutil.copyfile(counter, os.path.join(dest, GATE))
    os.chmod(os.path.join(dest, GATE), 0o644)
    for name in ROWS:
        set_recheck(dest, name, rec_line(name))
        rel = "corpus/knowledge/" + name
        text = rd(dest, rel)
        wr(dest, rel, text.rstrip("\n") + "\n" + section_text(build_rows(pure, name)))


# ---------------------------------------------------------------- mutants
CP, CG = "claim-package-contract.md", "claim-gates.md"
EXEC_ENTRY = "ai-assisted-finding-validation.md"  # executes (exit 0) at BASE; not one of the 24 gated entries
BASE_LINE = {}  # entry -> BASE recheck line, filled in main


def m_lines_down(t):  # L1: one fewer recheck line (executing entry)
    set_recheck(t, EXEC_ENTRY, None)


def m_broken(t):  # L1: an executing entry's line stops parsing
    set_recheck(t, EXEC_ENTRY, "recheck: cd %s && python3 (" % LANE)


def m_new_gated(t):  # L1/L2: an executing entry becomes gated
    set_recheck(t, EXEC_ENTRY, "recheck: cd %s && false" % LANE)


def m_single_reground(t):  # L2: claim-gates back to its BASE (gated) line, section intact
    set_recheck(t, CG, BASE_LINE[CG])


def m_home_tilde(t):
    set_recheck(t, CP, rec_line(CP) + " && test -d ~/Projects")


def m_home_var(t):
    set_recheck(t, CP, rec_line(CP) + ' && test -d "$HOME"')


def m_wrong_entry(t):  # claim-gates' line runs the OTHER entry
    set_recheck(t, CG, rec_line(CP))


def m_true_line(t):  # softened to true, section intact
    set_recheck(t, CP, "recheck: cd %s && true" % LANE)


def m_comment_smuggle(t):  # line is `true`; the gate incantation sits in a comment
    set_recheck(t, CP, "recheck: cd %s && true  # python3 %s --entry corpus/knowledge/%s" % (LANE, GATE, CP))


def m_or_true(t):  # gate runs but its verdict is discarded
    set_recheck(t, CP, rec_line(CP) + " || true")


def m_semicolon_true(t):
    set_recheck(t, CG, rec_line(CG) + " ; true")


def m_echo(t):  # the incantation is only echoed
    set_recheck(t, CP, "recheck: cd %s && echo python3 %s --entry corpus/knowledge/%s" % (LANE, GATE, CP))


def m_cd_bogus(t):  # the lane path in `cd` is not the lane (counter strips it and runs at TREE)
    set_recheck(t, CP, "recheck: cd /fast/scratch/hyaku/kasegi-r46/no-such-dir && python3 %s --entry corpus/knowledge/%s" % (GATE, CP))


def m_root_override(t):  # the line is pointed at another tree by absolute path
    set_recheck(t, CP, rec_line(CP) + " --root " + SHADOW[0])


def m_anchor_moved(t):
    row_edit(t, CG, "G1", lambda ln: re.sub(r"`([^`:]+):(\d+)`", lambda m: "`%s:%d`" % (m.group(1), int(m.group(2)) + 30), ln, count=1))


def m_token_absent(t):
    row_edit(t, CG, "G2", lambda ln: ln.replace("key`", "keyX`"))


def m_pipe_token(t):  # a markdown-table token that contains `|` splits the row into 7 cells
    row_edit(t, CG, "G2", lambda ln: row_line("G2", "one permissive secret regex over credential words", loc(PUREX[0], CK, "api[_-]?key|secret", 1), "api[_-]?key|secret|token|password"))


def m_anchor_symlink(t):
    os.symlink("exemplar/custodian-receipts.json", os.path.join(t, "corpus/instruments/fixtures/claim-package/r46-link.json"))
    row_edit(t, CP, "G8", lambda ln: ln.replace("exemplar/custodian-receipts.json", "r46-link.json"))


def m_anchor_outside(t):
    row_edit(t, CP, "G1", lambda ln: re.sub(r"`corpus/instruments/claim-package-check.py:(\d+)`", "`corpus/knowledge/triage-thresholds.md:1`", ln))


def m_five_rows(t):
    drop_rows(t, CG, ["G1", "G2"])


def m_one_anchor_file(t):  # G7 re-anchored to the same file as every other row of that entry
    row_edit(t, CG, "G7", lambda ln: row_line("G7", "manifest carries expected_head_sha256", loc(PUREX[0], CK, "expected_head_sha256", 1), "expected_head_sha256"))


def m_dup_id(t):
    row_edit(t, CG, "G7", lambda ln: ln.replace("| G7 |", "| G6 |", 1))


def m_body_deleted(t):
    edit(t, "corpus/knowledge/" + CP, lambda s: s.replace("## Validation\n", "", 1))


def m_body_edited(t):
    edit(t, "corpus/knowledge/" + CG, lambda s: s.replace("Exit 1 + `claim-check: FAIL", "Exit 2 + `claim-check: FAIL", 1))


def m_still_gated_edited(t):
    set_recheck(t, "evidence-dir.md", rd(t, "corpus/knowledge/evidence-dir.md").split("\n")[next(i for i, ln in enumerate(rd(t, "corpus/knowledge/evidence-dir.md").split("\n")) if ln.startswith("recheck:"))] + " # edited")


def m_third_soft(t):
    set_recheck(t, "evidence-dir.md", "recheck: cd %s && true" % LANE)


def m_third_deleted(t):
    set_recheck(t, "evidence-dir.md", None)


def m_hash_token(t):  # L6: a token the blanking cannot change
    wr(t, "corpus/instruments/r46-hash-anchor.txt", "######\n")
    row_edit(t, CG, "G7", lambda ln: row_line("G7", "hash fixture", "corpus/instruments/r46-hash-anchor.txt:1", "######"))


def m_self_anchor(t):  # an anchor that reaches the entry itself through a symlinked directory
    os.symlink("../knowledge", os.path.join(t, "corpus/instruments/kn"))
    row_edit(t, CG, "G7", lambda ln: row_line("G7", "the entry's own title", "corpus/instruments/kn/claim-gates.md:1", "the complete gate list"))


def m_tautology(t):  # anchor file written for the purpose: it states the claims in prose
    wr(t, "corpus/instruments/r46-claim-note.txt",
       "\n".join(["the secrets gate caps every scanned file at five mebibytes",
                  "one permissive regex matches the credential words",
                  "any symlink in the package is refused without traversal",
                  "the hard gates include evidence integrity"]) + "\n")
    for gid, tok in (("G1", "caps every scanned file"), ("G2", "one permissive regex"), ("G3", "refused without traversal"), ("G4", "include evidence integrity")):
        n = {"G1": 1, "G2": 2, "G3": 3, "G4": 4}[gid]
        row_edit(t, CG, gid, lambda ln, n=n, tok=tok, gid=gid: row_line(gid, re.split(r"\s*\|\s*", ln.strip().strip("|"))[1], "corpus/instruments/r46-claim-note.txt:%d" % n, tok))


def m_fenced(t):  # the table sits inside a code fence (renders as code, not as rows)
    def go(s):
        ls = s.split("\n")
        first = next(i for i, ln in enumerate(ls) if ln.startswith("| id |"))
        return "\n".join(ls[:first] + ["```"] + ls[first:] + ["```"])
    edit(t, "corpus/knowledge/" + CP, go)


def m_six_rows_ok(t):  # POSITIVE: exactly the minimum
    drop_rows(t, CG, ["G1"])


def m_note_ok(t):  # POSITIVE: prose after the table
    with open(os.path.join(t, "corpus/knowledge/" + CG), "a", encoding="utf-8") as fh:
        fh.write("\nThe rows above are the only machine-checked part of this section.\n")


def m_section_only(t):  # both lines kept at BASE, sections present
    set_recheck(t, CP, BASE_LINE[CP])
    set_recheck(t, CG, BASE_LINE[CG])


def m_section_twice(t):  # section heading repeated
    with open(os.path.join(t, "corpus/knowledge/" + CP), "a", encoding="utf-8") as fh:
        fh.write("\n" + SECTION + "\n")


# kind: mut = must be rejected + targets 0; pos = must read 7/7
CASES = [
    ("L1-recheck-line-deleted", m_lines_down, {"L1"}, "mut", "delete the recheck line of citation-bases.md (an executing entry)"),
    ("L1-recheck-unparsable", m_broken, {"L1"}, "mut", "citation-bases.md recheck becomes `cd <lane> && python3 (`"),
    ("L1-new-gated-entry", m_new_gated, {"L1"}, "mut", "citation-bases.md recheck becomes `cd <lane> && false`"),
    ("L2-only-one-reground", m_single_reground, {"L2"}, "mut", "claim-gates.md recheck restored to the BASE line, section kept"),
    ("L3-line-has-tilde-path", m_home_tilde, {"L3"}, "mut", "contract recheck line + ` && test -d ~/Projects`"),
    ("L3-line-has-HOME-var", m_home_var, {"L3"}, "mut", "contract recheck line + ` && test -d \"$HOME\"`"),
    ("L3-line-names-other-entry", m_wrong_entry, {"L3"}, "mut", "claim-gates recheck runs `--entry` of claim-package-contract.md"),
    ("L3-line-softened-true", m_true_line, {"L3"}, "mut", "contract recheck becomes `cd <lane> && true`, section intact"),
    ("L3-gate-incantation-in-comment", m_comment_smuggle, {"L3"}, "mut", "contract recheck `... && true  # python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md`"),
    ("L3-gate-verdict-discarded-or-true", m_or_true, {"L3"}, "mut", "contract recheck = the real line + ` || true`"),
    ("L3-gate-verdict-discarded-semicolon", m_semicolon_true, {"L3"}, "mut", "claim-gates recheck = the real line + ` ; true`"),
    ("L3-gate-only-echoed", m_echo, {"L3"}, "mut", "contract recheck `... && echo python3 corpus/instruments/r46-c1-gate.py --entry ...`"),
    ("L3-cd-target-not-the-lane", m_cd_bogus, {"L3"}, "mut", "contract recheck `cd /fast/scratch/hyaku/kasegi-r46/no-such-dir && python3 ...--entry ...`"),
    ("L3-root-override-absolute", m_root_override, {"L3"}, "mut", "contract recheck = the real line + ` --root <absolute scratch tree>`"),
    ("L4-row-anchor-moved", m_anchor_moved, {"L4"}, "mut", "claim-gates row G1 anchor line +30"),
    ("L4-token-absent", m_token_absent, {"L4"}, "mut", "claim-gates row G2 token `...api[_-]?key` -> `...api[_-]?keyX`"),
    ("L4-pipe-in-token", m_pipe_token, {"L4"}, "mut", "claim-gates row G2 token = the literal alternation `api[_-]?key|secret|token|password` (a `|` inside the token cell)"),
    ("L4-anchor-is-symlink", m_anchor_symlink, {"L4"}, "mut", "contract row G8 anchored on a NEW symlink file fixtures/claim-package/r46-link.json -> exemplar/custodian-receipts.json"),
    ("L4-anchor-outside-dirs", m_anchor_outside, {"L4"}, "mut", "contract row G1 anchor path -> corpus/knowledge/triage-thresholds.md:1"),
    ("L4-five-rows", m_five_rows, {"L4"}, "mut", "claim-gates: delete rows G1,G2 (7 -> 5 rows)"),
    ("L4-one-anchor-file", m_one_anchor_file, {"L4"}, "mut", "claim-gates row G7 re-anchored on claim-package-check.py (every row of the entry then sits in one file)"),
    ("L4-duplicate-row-id", m_dup_id, {"L4"}, "mut", "claim-gates row G7 renamed G6"),
    ("L5-body-line-deleted", m_body_deleted, {"L5"}, "mut", "contract: delete the `## Validation` heading line"),
    ("L5-body-line-edited", m_body_edited, {"L5"}, "mut", "claim-gates: `Exit 1 +` -> `Exit 2 +` on line 4"),
    ("L6-token-blanking-is-a-noop", m_hash_token, {"L6"}, "mut", "new corpus/instruments/r46-hash-anchor.txt = `######`; claim-gates row G7 anchored there with token `######`"),
    ("L7-still-gated-line-edited", m_still_gated_edited, {"L7"}, "mut", "evidence-dir.md (still gated) recheck line + ` # edited`"),
    ("X-third-gated-softened-true", m_third_soft, {"L3"}, "mut", "evidence-dir.md (a third gated entry) recheck becomes `cd <lane> && true`"),
    ("X-third-gated-line-deleted", m_third_deleted, {"L1"}, "mut", "evidence-dir.md recheck line deleted outright"),
    ("X-section-heading-twice", m_section_twice, {"L4"}, "mut", "contract: `## Re-ground (round 46)` appears twice"),
    ("X-section-only-lines-kept", m_section_only, {"L1", "L2"}, "mut", "both sections present, both recheck lines left at BASE"),
    ("X-anchor-self-via-symlinked-dir", m_self_anchor, {"L6"}, "mut", "symlink dir corpus/instruments/kn -> ../knowledge; claim-gates row G7 anchored on corpus/instruments/kn/claim-gates.md:1 token `the complete gate list` (the entry itself)"),
    ("X-tautological-anchor-file", m_tautology, {"L4"}, "mut", "new corpus/instruments/r46-claim-note.txt restating claims in prose; claim-gates rows G1-G4 anchored there"),
    ("X-rows-inside-code-fence", m_fenced, {"L4"}, "mut", "contract: the row table wrapped in a ``` fence"),
    ("P-exactly-six-rows", m_six_rows_ok, set(), "pos", "claim-gates: delete row G1 (7 -> 6 rows)"),
    ("P-prose-after-table", m_note_ok, set(), "pos", "claim-gates: one prose line appended after the table"),
]

def stub_gate(t):  # the tree's own copy of the gate script is replaced by an always-green stub
    wr(t, GATE, "import sys\nsys.exit(0)\n")


def with_stub(fn):
    def go(t):
        fn(t)
        stub_gate(t)
    return go


ROWLEVEL = ["L4-row-anchor-moved", "L4-token-absent", "L4-pipe-in-token", "L4-anchor-is-symlink", "L4-anchor-outside-dirs",
            "L4-five-rows", "L4-one-anchor-file", "L4-duplicate-row-id", "X-section-heading-twice"]
_new = []
for _c in CASES:
    if _c[0] in ROWLEVEL:
        # a broken row turns the entry's own recheck line red, so the entry drops back into the gated set: L1/L2 (and L7) catch it
        _new.append((_c[0], _c[1], {"L1", "L2"}, _c[3], _c[4]))
        # with the tree's gate copy stubbed the recheck line stays green: only L4 (SELF bytes) can catch the bad rows
        _new.append((_c[0] + "+stubbed-gate-copy", with_stub(_c[1]), {"L4"}, _c[3], _c[4] + "; AND the tree copy of r46-c1-gate.py replaced by `sys.exit(0)`"))
    else:
        _new.append(_c)
CASES[:] = _new
_stub_only = ("X-stubbed-gate-copy-alone", stub_gate, set(), "pos", "only the tree copy of r46-c1-gate.py replaced by `sys.exit(0)` (rows all valid): the counter must still read 7/7 because L4 uses its own bytes")
CASES.append(_stub_only)

SHADOW = [""]
PUREX = [""]


def run_counter(counter: str, tree: str, base: str, work: str):
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ, TMPDIR=work)
    p = subprocess.run([sys.executable, counter, "--root", tree, "--baseline", base, "--work", work],
                       capture_output=True, text=True, timeout=900, env=env)
    limbs = {m.group(1): int(m.group(2)) for m in re.finditer(r"^gate (L\d) pass=(\d) ", p.stdout, re.M)}
    reads = {m.group(1): m.group(3) for m in re.finditer(r"^gate (L\d) pass=(\d) read=(.*)$", p.stdout, re.M)}
    m = re.search(r"^c1-gate fixed=(\d)/7 exit=(\d)", p.stdout, re.M)
    return limbs, reads, (int(m.group(1)) if m else -1), p.returncode, p.stdout


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--pure", default=PURE)
    ap.add_argument("--counter")
    ap.add_argument("--work")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    counter = os.path.abspath(a.counter or os.path.join(a.lane, GATE))
    base_dir = a.work or os.environ.get("TMPDIR") or os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kasegi-r46", "R46ExecSelftestC1")
    os.makedirs(base_dir, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="c1st-", dir=base_dir)
    if not a.keep:
        atexit.register(shutil.rmtree, scratch, True)
    log = []

    def out(s):
        print(s)
        sys.stdout.flush()

    pure = os.path.abspath(a.pure)
    PUREX[0] = pure
    base = os.path.join(scratch, "base")
    shutil.copytree(pure, base, symlinks=True)
    for name in ROWS:
        BASE_LINE[name] = next(ln for ln in rd(pure, "corpus/knowledge/" + name).split("\n") if ln.startswith("recheck:"))
    tip = os.path.join(scratch, "tip")
    build_tip(pure, counter, tip)
    SHADOW[0] = tip

    results = []  # (name, kind, targets, desc, limbs, reads, fixed, rc)

    def one(case):
        name, fn, targets, kind, desc = case
        d = os.path.join(scratch, "case-" + name)
        shutil.copytree(tip, d, symlinks=True)
        fn(d)
        limbs, reads, fixed, rc, _ = run_counter(counter, d, base, os.path.join(scratch, "w-" + name))
        shutil.rmtree(d, ignore_errors=True)
        return (name, kind, targets, desc, limbs, reads, fixed, rc)

    # tip + do-nothing control first (serial, cheap and they gate everything else)
    limbs, reads, fixed, rc, stdout = run_counter(counter, tip, base, os.path.join(scratch, "w-tip"))
    results.append(("TIP-7of7", "tip", set(), "complete synthetic tip: counter copied in; contract+gates re-grounded (8+7 rows)", limbs, reads, fixed, rc))
    limbs, reads, fixed, rc, _ = run_counter(counter, base, base, os.path.join(scratch, "w-null"))
    results.append(("CONTROL-do-nothing", "null", set(), "tree = baseline = pure export", limbs, reads, fixed, rc))
    with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        results.extend(ex.map(one, CASES))

    failures = 0
    notes = []
    for name, kind, targets, desc, limbs, reads, fixed, rc in results:
        order = " ".join("%s=%d" % (k, limbs.get(k, -1)) for k in ("L1", "L2", "L3", "L4", "L5", "L6", "L7"))
        if kind == "tip":
            ok = fixed == 7 and rc == 0
            verdict = "OK" if ok else "UNEXPECTED"
        elif kind == "null":
            ok = fixed == 1 and rc == 1 and limbs.get("L7") == 1
            verdict = "OK" if ok else "UNEXPECTED"
        elif kind == "pos":
            ok = fixed == 7 and rc == 0
            verdict = "OK" if ok else "UNEXPECTED"
        else:
            rejected = fixed < 7 or rc != 0
            hit = all(limbs.get(L) == 0 for L in targets)
            ok = rejected and hit
            verdict = "OK" if ok else ("FALSE-GREEN" if not rejected else "UNEXPECTED")
        failures += 0 if ok else 1
        out("case %-38s %s fixed=%d/7 exit=%d targets=%s verdict=%s" % (name, order, fixed, rc, ",".join(sorted(targets)) or "-", verdict))
        if not ok:
            notes.append("%s %s: recipe=%s | reads=%s" % (verdict, name, desc, "; ".join("%s:%s" % (k, v) for k, v in sorted(reads.items()))))
    for n in notes:
        out(n)
    out("selftest cases=%d failures=%d" % (len(results), failures))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
