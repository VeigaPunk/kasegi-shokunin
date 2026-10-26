#!/usr/bin/env python3
"""ExecRefChecker.py — INDEPENDENT reference checker for the round-38 closure
contract (checks G1-G8).

This file is wave evidence, not a lane instrument. It is written from the frozen
round-38 claims contract (`.ufo/waves/round-38/claims.json`, claim C1) and shares
no code with `corpus/instruments/r38-closure.sh`: it is the cross-check the L1
diffs the bash suite against. It is Python 3 standard library only.

EXPORT MODE IS THE ONLY RUN MODE. `--export-ref <hash>` extracts the lane tree
with

    git -C <lane> archive <hash> | tar -x -C <work>/export

and every byte-reading check reads only under that export root. The only
ref-scoped git reads that cannot be answered from export bytes are G2's commit
existence/ancestry and receipt diff, G3's base..REF added-line diff, and G8's
carry-over suite run. A plain run (no --export-ref, no --selftest) refuses with
exit 2, because a suite that reads the working tree can be turned green by edits
that were never committed.

G6 is LIVE by construction (scratch-root quiescence cannot be answered from an
export) and G8 runs the export's own `corpus/instruments/r37-closure.sh`, whose
E9 limbs are live as well.

Work-dir discipline (mirrors the committed r37 suite): `--work` must resolve
outside the lane, is refused before anything is created if it would not, its
`export/` and `mut/` subdirectories are cleared before use, and an auto-created
work dir honours TMPDIR. Nothing is written under the lane.

Output (export mode), in this order:
    export-ref=<40 hex> mode=export lane=<dir> suite-sha256=<64 hex>
    G1 payload=<k=v,...> closed=0|1
    ...
    G8 payload=<k=v,...> closed=0|1
    closed=<k>/8 exit=<0|1>
Exit 0 only when k=8.

Output (selftest mode):
    export-ref=<40 hex> mode=selftest lane=<dir> suite-sha256=<64 hex>
    selftest case=G<n> positive=pass|fail mutants=<rejected>/<total> verdict=pass|fail
    selftest detail=G<n> mutant=<label> rejected=0|1
    ...
    selftest cases=8 failures=<k>
Exit 0 only when all eight cases ran and k=0. Every mutant reopens exactly one
clause of its check on a hardlink copy of the export; a check that cannot
discriminate a single-defect mutant fails its case. A summary-only forgery cannot
satisfy any check: each check reads the evidence bytes it names.

Usage:
    python3 ExecRefChecker.py --export-ref <hash> [--lane DIR] [--work DIR]
                              [--scratch-root DIR]
    python3 ExecRefChecker.py --selftest [--export-ref <hash>] [--lane DIR]
                              [--work DIR] [--scratch-root DIR]
    python3 ExecRefChecker.py -h

Defaults: --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin,
--scratch-root /fast/scratch/hyaku, work dir under TMPDIR.

The eight checks (round-38 defect routing):
    G1 (D-A) Front-door corrections and fence state. PROVINCE.md and
       corpus/README.md each carry >=1 line beginning `Correction (round 38)`
       that contains the round-37 append range (`L79-L152` in PROVINCE.md,
       `L399-L454` in corpus/README.md) and the word `misplaced`; a CommonMark
       fence walk over each whole file ends CLOSED (a line matching `^ {0,3}``` `
       opens a fence while closed, info string allowed; while open only a line
       matching `^ {0,3}```[[:space:]]*$` closes it); and
       `.ufo/waves/round-38/declared-blocks.txt` exists with >=1
       `<path> <lines> <sha256>` line per front-door file, each verified against
       the last `<lines>` lines of `<path>` in the export.
    G2 (D-B) All-gates v2 receipt. `.ufo/waves/round-38/final-gates/all-gates.txt`
       in the export: first line `all-gates v2`; one `export-ref=<40 hex>` whose
       commit exists in the lane and equals REF or is an ancestor of REF; the
       `git diff --name-only <export-ref> REF` list is nothing but the receipt;
       one `suite-sha256=` equal to the running suite's digest; exactly 8
       `G<n> payload=... closed=1` lines covering G1-G8; one `closed=8/8 exit=0`;
       8 `selftest case=G<n> ` lines covering G1-G8; one
       `selftest cases=8 failures=0`. The SCORECARD `^## Round 38` section must
       name the judged head BY REFERENCE (`judged head: export-ref of
       .ufo/waves/round-38/final-gates/all-gates.txt`) and neither that section
       nor any SHONEN.md line mentioning round 38 may label a head with a commit
       hash.
    G3 (D-C) Pending-marker resolutions. corpus/lessons/round-37.md carries a
       `## Pending-marker resolutions (round 38)` heading followed by table rows
       naming each of L10, L90, L95, L216, L265, L300, L320, L85 (8 distinct
       line tokens, each in some row inside that section); and the added lines
       (`+`, not `+++`) of the base..REF diff, excluding `.ufo`, the r38 suite and
       its fixtures, contain 0 matches of `⟨pending`, `<fill>`,
       `filled by the L1`, `<LANE_HASH>`, `<r38-` and 0 word-bounded `TBD`/`TODO`.
    G4 (D3) Dispatch/results parity. For every tracked
       `.ufo/waves/round-38/*-dispatch.json` in the export (>=1 required) the
       sibling `*-results.json` (or the dispatcher's `<wave>-results.json` in the
       same directory, if it lists the same wave) exists in the export, parses as
       JSON, and its seat-entry count equals `len(taskCall.tasks)`.
    G5 (D-D) Anchor-ancestor label. The SCORECARD `^## Round 38` section carries
       0 lines containing `Final lane commit:` and SCORECARD.md carries >=1 line
       beginning `Correction (round 38)` that contains `f3246559` and
       `anchor ancestor`.
    G6 (D-E) Live scratch quiescence under --scratch-root: kasegi-r36 and
       kasegi-r37 are absent or empty; kasegi-r38 is absent or carries no entry
       other than the resolved --work dir (or its top-level parent under
       kasegi-r38). An unreadable directory is RED, never empty.
    G7 (D-F) Ledger section filled. corpus/knowledge/considerthese-proposals-ledger.md
       carries `## Round-37 dispositions — filled (round 38)` AFTER
       `## Round-37 dispositions (appended 2026-10-26, R31 home)`; inside the
       filled section one line begins `Correction (round 38)` and >=7 table data
       rows start with the proposal numbers 1..7 (each present).
    G8 Carry-over: the export's own corpus/instruments/r37-closure.sh run with
       `--export-ref REF --lane <lane> --work <work>/r37` ends with
       `closed=14/14 exit=0`.

Documented limits (measured, not hidden):
    - G2 checks the receipt's SHAPE, digest, ancestry and the committed diff. It
      cannot prove the recorded VALUES were produced before the receipt was
      committed; that is why the judged head is named only by reference and the
      diff REF..receipt is empty but for the receipt. The digest rule keeps the
      recorded run bound to the instrument that produced it.
    - G2's carrier scope is the LAST `^## Round 38` section (the round appends
      one) plus every SHONEN.md line matching `round[- ]38` case-insensitively.
      Historical round-37 lines in SHONEN.md are out of scope by construction.
    - G3's added-line limb uses the commit diff on a real run. For a selftest
      mutant (a copied tree that is not a commit) it uses `git diff --no-index`
      of the base export against the mutant, with the same path exclusions; both
      compute "lines added relative to the base tree".
    - G6's kasegi-r38 allowance names the resolved --work dir and its top-level
      parent only; it deliberately does not exempt other seats' scratch dirs, so
      a live wave with nine concurrent seats reads RED. That is the intended
      live reading; the final gate must run after scratch cleanup.
    - G8 inherits the r37 suite's E9 limbs: E9(d) requires the exported ref to BE
      the lane's HEAD, so a historical export can never read quiescent now, and
      the base/r37-judged-head exports fail G8 for that live reason rather than
      for a byte defect. G8 passes only on a ref the runner has checked out.
    - G4's seat-entry count is `len(results)` of the results JSON (with the
      top-level `seats` count, where present, required to agree). A results file
      whose entries are named but empty still counts: G4 is a parity check, not a
      content check.

Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
2 harness error (bad or missing argument, unresolvable ref, unreadable lane,
archive failure, --work inside the lane). The plain-run refusal is exit 2.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE_DEFAULT = '/home/vgpnk/Projects/shokunin/kasegi-shokunin'
SCRATCH_ROOT_DEFAULT = '/fast/scratch/hyaku'
BASE = 'a173b0c2b98c5ae39599fa9be76027fbbead0b9e'
R38_DIR = '.ufo/waves/round-38'
RECEIPT = R38_DIR + '/final-gates/all-gates.txt'
DECLARED = R38_DIR + '/declared-blocks.txt'
R37_SUITE = 'corpus/instruments/r37-closure.sh'
CHECK_IDS = ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8')

FENCE_OPEN = re.compile(r'^ {0,3}```')
FENCE_CLOSE = re.compile(r'^ {0,3}```[ \t]*$')
HEX40 = re.compile(r'^[0-9a-f]{40}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
LABEL_HEX = re.compile(r'(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}',
                       re.IGNORECASE)
G2_REFERENCE = 'judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt'

FIXED_TOKENS = ('\u27e8pending', '<fill>', 'filled by the L1', '<LANE_HASH>', '<r38-')
WORD_TOKENS = re.compile(r'\b(?:TBD|TODO)\b')

G3_TOKENS = ('L10', 'L90', 'L95', 'L216', 'L265', 'L300', 'L320', 'L85')


class HarnessError(Exception):
    """A harness-level failure: exit 2, never a check verdict."""


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def read_bytes(path):
    try:
        with open(path, 'rb') as fh:
            return fh.read()
    except OSError:
        return None


def read_lines(path):
    data = read_bytes(path)
    if data is None:
        return None
    return data.decode('utf-8', 'replace').splitlines()


def run(argv, cwd=None, timeout=600):
    """Run argv; return CompletedProcess or None on spawn/timeout failure."""
    try:
        return subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None


def git(lane, *args, timeout=600):
    return run(['git', '-C', lane] + list(args), timeout=timeout)


def git_line(lane, *args):
    cp = git(lane, *args)
    if cp is None or cp.returncode != 0:
        return None
    return cp.stdout.strip()


def section_after(lines, start_re, last=True):
    """Return (index, lines-of-section) for the LAST (or first) heading matching
    start_re, closed by the next `^## ` heading or EOF."""
    idxs = [i for i, ln in enumerate(lines) if re.match(start_re, ln)]
    if not idxs:
        return None, None
    i = idxs[-1] if last else idxs[0]
    out = []
    for ln in lines[i:]:
        if out and re.match(r'^## ', ln):
            break
        out.append(ln)
    return i, out


def payload(**kwargs):
    return ','.join('%s=%s' % (k.replace('_', '-'), v) for k, v in kwargs.items())


def fence_state(lines):
    opened = False
    for ln in lines:
        if opened:
            if FENCE_CLOSE.match(ln):
                opened = False
        elif FENCE_OPEN.match(ln):
            opened = True
    return 'open' if opened else 'closed'


def split_cells(row):
    """Split a markdown table row on unescaped pipes."""
    sentinel = '\x01'
    cells = row.replace('\\|', sentinel).split('|')
    return [c.replace(sentinel, '|') for c in cells]


def last_n_lines(data, n):
    """Exactly `tail -n <n>`: the last n lines, terminators preserved."""
    if n <= 0:
        return b''
    return b''.join(data.splitlines(keepends=True)[-n:])


# ---------------------------------------------------------------------------
# context
# ---------------------------------------------------------------------------

class Ctx(object):
    def __init__(self, tree, ref, ref_resolved, lane, work, scratch_root,
                 base_tree=None, added_text=None):
        self.tree = tree
        self.ref = ref
        self.ref_resolved = ref_resolved
        self.lane = lane
        self.work = work
        self.scratch_root = scratch_root
        self.base_tree = base_tree
        self.added_text = added_text

    def clone(self, **over):
        c = Ctx(self.tree, self.ref, self.ref_resolved, self.lane, self.work,
                self.scratch_root, self.base_tree, self.added_text)
        for k, v in over.items():
            setattr(c, k, v)
        return c

    def path(self, rel):
        return os.path.join(self.tree, rel)


# ---------------------------------------------------------------------------
# G1 — D-A: front-door corrections, fence state, declared blocks
# ---------------------------------------------------------------------------

def correction_lines(lines, needles):
    if lines is None:
        return 0
    n = 0
    for ln in lines:
        if not ln.startswith('Correction (round 38)'):
            continue
        if all(nd in ln for nd in needles) and re.search(r'\bmisplaced\b', ln, re.IGNORECASE):
            n += 1
    return n


def check_g1(ctx):
    prov = read_lines(ctx.path('PROVINCE.md'))
    readme = read_lines(ctx.path('corpus/README.md'))
    prov_fence = fence_state(prov) if prov is not None else 'absent'
    readme_fence = fence_state(readme) if readme is not None else 'absent'
    prov_corr = correction_lines(prov, ('L79-L152',))
    readme_corr = correction_lines(readme, ('L399-L454',))

    declared_lines = read_lines(ctx.path(DECLARED))
    declared_total = 0
    declared_match = 0
    per_file = {}
    wellformed = True
    if declared_lines is not None:
        for ln in declared_lines:
            if not ln.strip():
                continue
            declared_total += 1
            parts = ln.split()
            if len(parts) != 3:
                wellformed = False
                continue
            rel, nstr, want = parts
            if not re.match(r'^[0-9]+$', nstr) or not HEX64.match(want):
                wellformed = False
                continue
            data = read_bytes(ctx.path(rel))
            if data is None:
                wellformed = False
                continue
            got = sha256_bytes(last_n_lines(data, int(nstr)))
            if got == want:
                declared_match += 1
                per_file[rel] = per_file.get(rel, 0) + 1
            else:
                wellformed = False
    covered = all(per_file.get(f, 0) >= 1 for f in ('PROVINCE.md', 'corpus/README.md'))
    closed = (prov_corr >= 1 and readme_corr >= 1
              and prov_fence == 'closed' and readme_fence == 'closed'
              and declared_lines is not None and covered and wellformed
              and declared_match == declared_total and declared_total >= 2)
    return closed, payload(
        province_correction=prov_corr,
        readme_correction=readme_corr,
        province_fence=prov_fence,
        readme_fence=readme_fence,
        declared_lines=declared_total,
        declared_match=declared_match,
        declared_covered=1 if covered else 0,
    )


# ---------------------------------------------------------------------------
# G2 — D-B: all-gates v2 receipt + judged head named by reference
# ---------------------------------------------------------------------------

def check_g2(ctx):
    lines = read_lines(ctx.path(RECEIPT))
    receipt = 'present' if lines is not None else 'missing'
    version = 'absent'
    xrefs = []
    xref_ok = 0
    anc = 0
    diff_extra = -1
    digests = []
    dig_ok = 0
    run_ids = []
    run_zero = 0
    closed_line = 0
    case_ids = []
    case_summary = 0
    carrier_count = 0
    carrier_ref = 0
    label_hits = 0
    section_count = 0

    if lines is not None:
        version = 'v2' if lines and lines[0].strip() == 'all-gates v2' else 'other'
        xrefs = [m.group(1) for m in (re.match(r'^export-ref=([0-9a-f]{40})$', ln) for ln in lines) if m]
        if len(xrefs) == 1:
            xref = xrefs[0]
            resolved = git_line(ctx.lane, 'rev-parse', '--verify', '--quiet', xref + '^{commit}')
            if resolved:
                xref_ok = 1
                ref_res = ctx.ref_resolved
                if ref_res:
                    if resolved == ref_res:
                        anc = 1
                    else:
                        cp = git(ctx.lane, 'merge-base', '--is-ancestor', resolved, ref_res)
                        if cp is not None and cp.returncode == 0:
                            anc = 1
                    cp = git(ctx.lane, 'diff', '--name-only', resolved, ref_res)
                    if cp is not None and cp.returncode == 0:
                        diff_extra = len([ln for ln in cp.stdout.splitlines()
                                          if ln.strip() and ln.strip() != RECEIPT])
                    else:
                        diff_extra = -1
        digests = [m.group(1) for m in (re.match(r'^suite-sha256=([0-9a-f]{64})$', ln) for ln in lines) if m]
        if len(digests) == 1 and digests[0] == suite_digest():
            dig_ok = 1
        run_ids = sorted(set(re.findall(r'^G([1-8]) payload=.* closed=1$', '\n'.join(lines), re.M)))
        run_zero = len([ln for ln in lines if re.match(r'^G[1-8] payload=.* closed=0$', ln)])
        closed_line = len([ln for ln in lines if ln.strip() == 'closed=8/8 exit=0'])
        case_ids = sorted(set(re.findall(r'^selftest case=G([1-8]) ', '\n'.join(lines), re.M)))
        case_summary = len([ln for ln in lines if ln.strip() == 'selftest cases=8 failures=0'])

    scorecard = read_lines(ctx.path('SCORECARD.md'))
    if scorecard is not None:
        idx, sec = section_after(scorecard, r'^## Round 38')
        section_count = len([i for i, ln in enumerate(scorecard) if re.match(r'^## Round 38', ln)])
        if sec is not None:
            carrier_count = len(sec)
            carrier_ref = len([ln for ln in sec if G2_REFERENCE in ln])
            label_hits += len([ln for ln in sec if LABEL_HEX.search(ln)])
    shonen = read_lines(ctx.path('SHONEN.md'))
    if shonen is not None:
        label_hits += len([ln for ln in shonen
                           if re.search(r'round[- ]38', ln, re.IGNORECASE)
                           and LABEL_HEX.search(ln)])

    closed = (receipt == 'present' and version == 'v2' and xref_ok == 1 and anc == 1
              and diff_extra == 0 and dig_ok == 1
              and run_ids == ['1', '2', '3', '4', '5', '6', '7', '8'] and run_zero == 0
              and closed_line >= 1
              and case_ids == ['1', '2', '3', '4', '5', '6', '7', '8'] and case_summary == 1
              and carrier_ref >= 1 and label_hits == 0)
    return closed, payload(
        receipt=receipt,
        version=version,
        export_ref=xrefs[0] if len(xrefs) == 1 else ('none' if not xrefs else 'many'),
        export_ref_exists=xref_ok,
        ancestor=anc,
        diff_extra=diff_extra,
        digest=dig_ok,
        run_lines=len(run_ids),
        run_open=run_zero,
        closed_line=closed_line,
        selftest_cases=len(case_ids),
        selftest_summary=case_summary,
        carrier_lines=carrier_count,
        carrier_reference=carrier_ref,
        label_hashes=label_hits,
    )


# ---------------------------------------------------------------------------
# G3 — D-C: pending-marker resolutions + zero widened placeholders in added lines
# ---------------------------------------------------------------------------

def g3_added_text(ctx):
    if ctx.added_text is not None:
        return ctx.added_text
    cp = git(ctx.lane, 'diff', BASE, ctx.ref_resolved or ctx.ref, '--', '.',
             ':!.ufo', ':!corpus/instruments/r38-closure.sh',
             ':!corpus/instruments/r38-fixtures')
    if cp is None or cp.returncode != 0:
        return None
    return cp.stdout


def g3_marker_rows(ctx):
    lesson = read_lines(ctx.path('corpus/lessons/round-37.md'))
    if lesson is None:
        return 0, 0, 0
    idx, sec = section_after(lesson, r'^## Pending-marker resolutions \(round 38\)\s*$')
    if sec is None:
        return 0, 0, 0
    rows = [ln for ln in sec if ln.startswith('|')]
    present = 0
    for tok in G3_TOKENS:
        pat = re.compile(r'(?<![0-9A-Za-z])' + tok + r'(?![0-9A-Za-z])')
        if any(pat.search(r) for r in rows):
            present += 1
    return 1, present, len(rows)


def check_g3(ctx):
    heading, markers, rows = g3_marker_rows(ctx)
    text = g3_added_text(ctx)
    if text is None:
        added_state = 'unavailable'
        fixed_hits = -1
        word_hits = -1
    else:
        added = [ln for ln in text.splitlines()
                 if ln.startswith('+') and not ln.startswith('+++')]
        added_state = 'read'
        fixed_hits = sum(1 for ln in added for tok in FIXED_TOKENS if tok in ln)
        word_hits = sum(1 for ln in added if WORD_TOKENS.search(ln))
    closed = (heading == 1 and markers == len(G3_TOKENS)
              and added_state == 'read' and fixed_hits == 0 and word_hits == 0)
    return closed, payload(
        lesson_section=heading,
        markers='%d/%d' % (markers, len(G3_TOKENS)),
        marker_rows=rows,
        added_scan=added_state,
        added_fixed_tokens=fixed_hits,
        added_word_tokens=word_hits,
    )


# ---------------------------------------------------------------------------
# G4 — D3: dispatch/results parity
# ---------------------------------------------------------------------------

def results_seat_count(obj):
    if not isinstance(obj, dict):
        return None
    results = obj.get('results')
    if isinstance(results, list):
        n = len(results)
        seats = obj.get('seats')
        if isinstance(seats, int) and seats != n:
            return None
        return n
    if isinstance(results, dict):
        return len(results)
    return None


def check_g4(ctx):
    ddir = ctx.path(R38_DIR)
    dispatches = []
    if os.path.isdir(ddir):
        dispatches = sorted(f for f in os.listdir(ddir) if f.endswith('-dispatch.json'))
    paired = 0
    seats_match = 0
    detail = []
    for name in dispatches:
        dpath = os.path.join(ddir, name)
        try:
            with open(dpath, 'r', encoding='utf-8') as fh:
                disp = json.load(fh)
        except (OSError, ValueError):
            detail.append('%s=bad-dispatch' % name)
            continue
        tasks = None
        if isinstance(disp, dict):
            tc = disp.get('taskCall')
            if isinstance(tc, dict) and isinstance(tc.get('tasks'), list):
                tasks = tc['tasks']
        if tasks is None:
            detail.append('%s=no-tasks' % name)
            continue
        stem = name[:-len('-dispatch.json')]
        cands = [stem + '-results.json']
        wave = disp.get('wave')
        if isinstance(wave, str) and wave and wave not in cands:
            cands.append(wave + '-results.json')
        found = False
        ok = False
        parseable = False
        notes = []
        for cand in cands:
            rpath = os.path.join(ddir, cand)
            if not os.path.isfile(rpath):
                continue
            found = True
            try:
                with open(rpath, 'r', encoding='utf-8') as fh:
                    res = json.load(fh)
            except (OSError, ValueError):
                notes.append('%s=unparsed' % cand)
                continue
            if isinstance(res, dict) and isinstance(res.get('wave'), str) and wave \
               and res['wave'] != wave:
                notes.append('%s=wave-mismatch' % cand)
                continue
            n = results_seat_count(res)
            if n is None:
                notes.append('%s=count-inconsistent' % cand)
                continue
            parseable = True
            if n == len(tasks):
                seats_match += 1
                ok = True
                break
            notes.append('%s=seats-%d-of-%d' % (cand, n, len(tasks)))
        if not found:
            detail.append('%s=results-missing' % name)
        else:
            if parseable:
                paired += 1
            if not ok:
                detail.extend(notes or ['%s=unpaired' % name])
    closed = bool(dispatches) and paired == len(dispatches) and seats_match == len(dispatches)
    return closed, payload(
        dispatches=len(dispatches),
        paired=paired,
        seats_match=seats_match,
        detail=';'.join(detail) if detail else 'none',
    )


# ---------------------------------------------------------------------------
# G5 — D-D: anchor-ancestor label instead of a final-lane-commit label
# ---------------------------------------------------------------------------

def check_g5(ctx):
    scorecard = read_lines(ctx.path('SCORECARD.md'))
    final_labels = -1
    section_count = 0
    correction = 0
    if scorecard is not None:
        idx, sec = section_after(scorecard, r'^## Round 38')
        section_count = len([i for i, ln in enumerate(scorecard) if re.match(r'^## Round 38', ln)])
        if sec is not None:
            final_labels = len([ln for ln in sec if 'Final lane commit:' in ln])
        else:
            final_labels = 0
        correction = len([ln for ln in scorecard
                          if ln.startswith('Correction (round 38)')
                          and 'f3246559' in ln and 'anchor ancestor' in ln])
    closed = (scorecard is not None and section_count >= 1
              and final_labels == 0 and correction >= 1)
    return closed, payload(
        round38_sections=section_count,
        final_lane_commit=final_labels,
        anchor_correction=correction,
    )


# ---------------------------------------------------------------------------
# G6 — D-E: live scratch quiescence
# ---------------------------------------------------------------------------

def scan_scratch(root, name, allowed):
    p = os.path.join(root, name)
    if not os.path.exists(p):
        return 'absent', 0
    try:
        entries = list(os.scandir(p))
    except OSError:
        return 'unreadable', -1
    if not entries:
        return 'empty', 0
    bad = 0
    for e in entries:
        try:
            real = os.path.realpath(e.path)
        except OSError:
            real = e.path
        if real in allowed:
            continue
        bad += 1
    return ('clean' if bad == 0 else 'stray'), bad


def check_g6(ctx):
    root = ctx.scratch_root
    allowed = set()
    if ctx.work:
        w = os.path.realpath(ctx.work)
        allowed.add(w)
        r38 = os.path.realpath(os.path.join(root, 'kasegi-r38'))
        if w == r38 or w.startswith(r38 + os.sep):
            rel = os.path.relpath(w, r38)
            allowed.add(os.path.join(r38, rel.split(os.sep)[0]))
    if not os.path.isdir(root):
        absent = 'absroot=absent'
        r36 = r37 = r38 = 'absent'
        bad = 0
    else:
        absent = 'absroot=present'
        r36, b36 = scan_scratch(root, 'kasegi-r36', allowed)
        r37, b37 = scan_scratch(root, 'kasegi-r37', allowed)
        r38, b38 = scan_scratch(root, 'kasegi-r38', allowed)
        bad = max(b36, 0) + max(b37, 0) + max(b38, 0)
    closed = (r36 in ('absent', 'empty') and r37 in ('absent', 'empty')
              and r38 in ('absent', 'empty', 'clean'))
    return closed, payload(r36=r36, r37=r37, r38=r38, offenders=bad)


# ---------------------------------------------------------------------------
# G7 — D-F: the round-37 ledger section is filled
# ---------------------------------------------------------------------------

def check_g7(ctx):
    ledger = read_lines(ctx.path('corpus/knowledge/considerthese-proposals-ledger.md'))
    if ledger is None:
        return False, payload(filled_heading=0, after_original=0, correction=0,
                              rows=0, proposals='0/7')
    orig_re = r'^## Round-37 dispositions \(appended 2026-10-26, R31 home\)\s*$'
    filled_re = r'^## Round-37 dispositions \u2014 filled \(round 38\)\s*$'
    orig_idx = next((i for i, ln in enumerate(ledger) if re.match(orig_re, ln)), None)
    fidx, sec = section_after(ledger, filled_re)
    filled = 1 if fidx is not None else 0
    after = 1 if (orig_idx is not None and fidx is not None and fidx > orig_idx) else 0
    corr = 0
    rows = 0
    proposals = set()
    if sec is not None:
        corr = len([ln for ln in sec if ln.startswith('Correction (round 38)')])
        for ln in sec:
            if not ln.startswith('|'):
                continue
            cells = split_cells(ln)
            if len(cells) < 3:
                continue
            first = cells[1].strip()
            m = re.match(r'^([0-9]+)[.)]', first)
            if not m:
                continue
            rows += 1
            proposals.add(int(m.group(1)))
    need = set(range(1, 8))
    closed = (filled == 1 and after == 1 and corr >= 1 and need <= proposals)
    return closed, payload(
        filled_heading=filled,
        after_original=after,
        correction=corr,
        rows=rows,
        proposals='%d/7' % len(need & proposals),
    )


# ---------------------------------------------------------------------------
# G8 — carry-over: the export's own r37 suite closes 14/14
# ---------------------------------------------------------------------------

def check_g8(ctx):
    suite = ctx.path(R37_SUITE)
    if not os.path.isfile(suite):
        return False, payload(r37='absent', last='none', closed=0, exit=0)
    work = os.path.join(ctx.work, 'r37')
    cp = run(['bash', suite, '--export-ref', ctx.ref_resolved or ctx.ref,
              '--lane', ctx.lane, '--work', work], timeout=900)
    if cp is None:
        return False, payload(r37='present', last='run-failed', closed=0, exit=2)
    lines = [ln for ln in cp.stdout.splitlines() if ln.strip()]
    last = lines[-1] if lines else 'none'
    m = re.match(r'^closed=([0-9]+)/14 exit=([0-9]+)$', last.strip())
    closed_n, code = (int(m.group(1)), int(m.group(2))) if m else (0, cp.returncode)
    closed = last.strip() == 'closed=14/14 exit=0' and cp.returncode == 0
    return closed, payload(r37='present', last='closed=%d/14' % closed_n,
                           exit=code, lines=len(lines))


CHECKS = {'G1': check_g1, 'G2': check_g2, 'G3': check_g3, 'G4': check_g4,
          'G5': check_g5, 'G6': check_g6, 'G7': check_g7, 'G8': check_g8}


# ---------------------------------------------------------------------------
# harness: arguments, work dir, export
# ---------------------------------------------------------------------------

HELP = __doc__.split('Exit codes:')[0]


def die(msg):
    sys.stderr.write('ExecRefChecker: %s\n' % msg)
    raise SystemExit(2)


def parse_args(argv):
    opts = {'export_ref': None, 'selftest': False, 'lane': LANE_DEFAULT,
            'work': None, 'scratch_root': SCRATCH_ROOT_DEFAULT}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ('-h', '--help'):
            sys.stdout.write(HELP)
            raise SystemExit(0)
        if a == '--selftest':
            opts['selftest'] = True
            i += 1
            continue
        for flag, key in (('--export-ref', 'export_ref'), ('--lane', 'lane'),
                          ('--work', 'work'), ('--scratch-root', 'scratch_root')):
            if a == flag:
                if i + 1 >= len(argv):
                    die('%s needs a value' % flag)
                opts[key] = argv[i + 1]
                i += 2
                break
        else:
            die('unknown argument: %s' % a)
    return opts


def suite_digest():
    try:
        data = read_bytes(os.path.realpath(__file__))
    except OSError:
        return 'unreadable'
    if data is None:
        return 'unreadable'
    return sha256_bytes(data)


def make_work(lane, work_arg):
    if work_arg:
        norm = os.path.realpath(work_arg)
        if norm == '/' or norm == lane or norm.startswith(lane + os.sep):
            die('--work must be outside the lane: %s' % norm)
        os.makedirs(norm, exist_ok=True)
        work = os.path.realpath(norm)
        if work == lane or work.startswith(lane + os.sep):
            die('--work resolves inside the lane: %s' % work)
        return work, False
    work = tempfile.mkdtemp(prefix='ExecRefChecker.')
    return os.path.realpath(work), True


def prepare_export(lane, ref, work, need_base=False):
    if not os.path.isdir(lane):
        raise HarnessError('lane is not a directory: %s' % lane)
    cp = git(lane, 'rev-parse', '--git-dir')
    if cp is None or cp.returncode != 0:
        raise HarnessError('lane is not a git repository: %s' % lane)
    resolved = git_line(lane, 'rev-parse', '--verify', '--quiet', ref + '^{commit}')
    if not resolved:
        raise HarnessError('cannot resolve export ref in %s: %s' % (lane, ref))
    export = os.path.join(work, 'export')
    mut = os.path.join(work, 'mut')
    for p in (export, mut):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p, exist_ok=True)
    cp = run(['bash', '-c', 'git -C "$1" archive --format=tar "$2" | tar -xf - -C "$3"',
              'archive', lane, resolved, export], timeout=900)
    if cp is None or cp.returncode != 0:
        raise HarnessError('git archive export failed for %s' % resolved)
    if not os.path.isfile(os.path.join(export, 'SCORECARD.md')):
        raise HarnessError('export has no SCORECARD.md (not a lane tree): %s' % resolved)
    base_tree = None
    if need_base:
        base_tree = os.path.join(work, 'base')
        if os.path.isdir(base_tree):
            shutil.rmtree(base_tree, ignore_errors=True)
        os.makedirs(base_tree, exist_ok=True)
        cp = run(['bash', '-c', 'git -C "$1" archive --format=tar "$2" | tar -xf - -C "$3"',
                  'archive', lane, BASE, base_tree], timeout=900)
        if cp is None or cp.returncode != 0:
            base_tree = None
    return resolved, export, base_tree


# ---------------------------------------------------------------------------
# selftest: single-defect mutants
# ---------------------------------------------------------------------------

def link_tree(src, dst):
    if os.path.isdir(dst):
        shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, copy_function=os.link, symlinks=True)


def put(tree, rel, data):
    """Write bytes, unlinking first so a hardlinked copy never mutates the source."""
    path = os.path.join(tree, rel)
    os.makedirs(os.path.dirname(path) or tree, exist_ok=True)
    if os.path.lexists(path):
        os.unlink(path)
    with open(path, 'wb') as fh:
        fh.write(data.encode('utf-8') if isinstance(data, str) else data)


def drop_line(tree, rel, pred):
    data = read_bytes(os.path.join(tree, rel))
    if data is None:
        return
    keep = [ln for ln in data.split(b'\n') if not pred(ln.decode('utf-8', 'replace'))]
    put(tree, rel, b'\n'.join(keep))


def no_index_added(base_tree, mut_tree, workdir):
    """+ lines of the base->mutant tree diff, with the G3 path exclusions."""
    os.makedirs(workdir, exist_ok=True)
    cp = run(['git', 'diff', '--no-index', '--no-color', '--no-ext-diff',
              '--', base_tree, mut_tree], cwd=workdir, timeout=900)
    if cp is None or cp.returncode not in (0, 1):
        return None
    out = []
    keep = True
    for ln in cp.stdout.splitlines():
        if ln.startswith('diff --git '):
            keep = True
            continue
        if ln.startswith('+++ '):
            rhs = ln[4:].strip()
            if rhs == '/dev/null':
                keep = False
                continue
            if rhs.startswith('b/'):
                rhs = rhs[2:]
            rel = os.path.relpath(rhs, mut_tree) if os.path.isabs(rhs) else rhs
            if (rel.startswith('.ufo' + os.sep) or rel == '.ufo'
                    or rel == 'corpus/instruments/r38-closure.sh'
                    or rel.startswith('corpus/instruments/r38-fixtures')):
                keep = False
            continue
        if keep and ln.startswith('+') and not ln.startswith('+++'):
            out.append(ln)
    return '\n'.join(out)


def mutant_tree(ctx, work, label):
    dst = os.path.join(work, 'mut', label, 'tree')
    d = os.path.dirname(dst)
    os.makedirs(d, exist_ok=True)
    link_tree(ctx.tree, dst)
    return dst


G1_MUTANTS = [
    ('drop-province-correction', lambda t, c: drop_line(
        t, 'PROVINCE.md', lambda ln: ln.startswith('Correction (round 38)'))),
    ('reopen-readme-fence', lambda t, c: put(
        t, 'corpus/README.md',
        (read_bytes(os.path.join(t, 'corpus/README.md')) or b'').decode() + '```\n')),
    ('declared-digest-flip', lambda t, c: _flip_declared(t)),
]


def _flip_declared(tree):
    data = read_bytes(os.path.join(tree, DECLARED))
    if data is None:
        raise RuntimeError('no declared-blocks.txt to mutate')
    text = data.decode()
    m = re.search(r'[0-9a-f]{64}', text)
    if not m:
        raise RuntimeError('no digest in declared-blocks.txt')
    repl = ('f' if m.group(0)[0] != 'f' else 'e') + m.group(0)[1:]
    put(tree, DECLARED, text[:m.start()] + repl + text[m.end():])


def _g2_receipt_set(tree, regex, repl):
    data = read_bytes(os.path.join(tree, RECEIPT))
    if data is None:
        raise RuntimeError('no receipt to mutate')
    text = data.decode()
    new, n = re.subn(regex, repl, text, count=1, flags=re.M)
    if n == 0:
        raise RuntimeError('receipt has no line matching %s' % regex)
    put(tree, RECEIPT, new)


def _g2_mut_ancestor(tree, ctx):
    ref = ctx.ref_resolved
    cp = git(ctx.lane, 'rev-list', '--all', '--max-count=200')
    cand = None
    if cp is not None and cp.returncode == 0:
        for h in cp.stdout.split():
            if h == ref:
                continue
            a = git(ctx.lane, 'merge-base', '--is-ancestor', h, ref)
            if a is not None and a.returncode != 0:
                cand = h
                break
    if cand is None:
        cand = 'deadbeef' * 5
    _g2_receipt_set(tree, r'^export-ref=[0-9a-f]{40}$', 'export-ref=' + cand)


def _g2_mut_diff(tree, ctx):
    _g2_receipt_set(tree, r'^export-ref=[0-9a-f]{40}$', 'export-ref=' + BASE)


def _g2_mut_label(tree, ctx):
    path = os.path.join(tree, 'SCORECARD.md')
    sc = read_lines(path)
    if sc is None:
        raise RuntimeError('no SCORECARD.md')
    out = []
    inserted = False
    for ln in sc:
        out.append(ln)
        if not inserted and re.match(r'^## Round 38', ln):
            out.append('Final head deadbeefdeadbeefdeadbeefdeadbeefdeadbeef (mutant).')
            inserted = True
    if not inserted:
        raise RuntimeError('no round-38 SCORECARD section')
    put(tree, 'SCORECARD.md', '\n'.join(out) + '\n')


G2_MUTANTS = [
    ('header-v1', lambda t, c: _g2_receipt_set(t, r'^all-gates v2$', 'all-gates v1')),
    ('export-ref-not-ancestor', _g2_mut_ancestor),
    ('extra-file-in-diff', _g2_mut_diff),
    ('digest-mismatch', lambda t, c: _g2_receipt_set(
        t, r'^suite-sha256=[0-9a-f]{64}$', 'suite-sha256=' + 'f' * 64)),
    ('final-head-label', _g2_mut_label),
]

G3_MUTANTS = [
    ('drop-L265-row', lambda t, c: drop_line(
        t, 'corpus/lessons/round-37.md',
        lambda ln: ln.startswith('|') and 'L265' in ln)),
    ('add-toggle-marker', lambda t, c: put(
        t, 'corpus/lessons/round-37.md',
        (read_bytes(os.path.join(t, 'corpus/lessons/round-37.md')) or b'').decode()
        + 'TODO: unresolved mutant line\n')),
]

G4_MUTANTS = [
    ('drop-results', lambda t, c: _drop_results(t)),
    ('drop-seat-entry', lambda t, c: _drop_seat(t)),
]


def _results_path(tree):
    ddir = os.path.join(tree, R38_DIR)
    for name in sorted(os.listdir(ddir)):
        if name.endswith('-results.json'):
            return os.path.join(ddir, name)
    raise RuntimeError('no results.json to mutate')


def _drop_results(tree):
    os.unlink(_results_path(tree))


def _drop_seat(tree):
    p = _results_path(tree)
    with open(p, 'r', encoding='utf-8') as fh:
        obj = json.load(fh)
    obj['results'] = obj['results'][:-1]
    put(tree, os.path.relpath(p, tree), json.dumps(obj, indent=1))


def _g5_mut_label(tree, ctx):
    path = os.path.join(tree, 'SCORECARD.md')
    sc = read_lines(path)
    if sc is None:
        raise RuntimeError('no SCORECARD.md')
    out = []
    inserted = False
    for ln in sc:
        out.append(ln)
        if not inserted and re.match(r'^## Round 38', ln):
            out.append('Final lane commit: abc1234 (mutant).')
            inserted = True
    if not inserted:
        raise RuntimeError('no round-38 SCORECARD section')
    put(tree, 'SCORECARD.md', '\n'.join(out) + '\n')


def _g5_mut_correction(tree, ctx):
    drop_line(tree, 'SCORECARD.md',
              lambda ln: ln.startswith('Correction (round 38)') and 'f3246559' in ln)


G5_MUTANTS = [('final-lane-commit-label', _g5_mut_label),
              ('drop-anchor-correction', _g5_mut_correction)]


def _g6_fixture(ctx, work, name, entry):
    root = os.path.join(work, 'mut', 'scratch-' + name, 'root')
    os.makedirs(os.path.join(root, 'kasegi-' + entry), exist_ok=True)
    put(root, os.path.join('kasegi-' + entry, 'Stray', 'leftover.txt'), 'stray\n')
    return root


G6_MUTANTS = [('stray-kasegi-r36', 'r36'), ('stray-kasegi-r38', 'r38')]

G7_MUTANTS = [
    ('drop-proposal-row-4', lambda t, c: drop_line(
        t, 'corpus/knowledge/considerthese-proposals-ledger.md',
        lambda ln: ln.startswith('|') and re.match(r'^\s*\|\s*4[.)]', ln))),
    ('drop-correction-line', lambda t, c: drop_line(
        t, 'corpus/knowledge/considerthese-proposals-ledger.md',
        lambda ln: ln.startswith('Correction (round 38)'))),
]


def _g8_mut_stub(tree, ctx):
    put(tree, R37_SUITE, '#!/bin/sh\n# single-defect mutant: failing carry-over\n'
                          'echo "corpus closed=13/14 exit=1"\necho closed=13/14 exit=1\n')


def run_case(ctx, gid, work):
    check = CHECKS[gid]
    positive = check(ctx)[0]
    rejected = 0
    total = 0
    details = []
    if gid == 'G6':
        for label, entry in G6_MUTANTS:
            total += 1
            root = _g6_fixture(ctx, work, label, entry)
            ok = not check(ctx.clone(scratch_root=root))[0]
            rejected += ok
            details.append((label, ok))
    elif gid == 'G8':
        for label, fn in (('mutant-stub-carry-over', _g8_mut_stub),
                          ('ref-with-red-r37', None)):
            total += 1
            if fn is None:
                ok = not check(ctx.clone(ref=BASE,
                                         ref_resolved=git_line(ctx.lane, 'rev-parse',
                                                               '--verify', '--quiet',
                                                               BASE + '^{commit}') or BASE))[0]
                details.append((label, ok))
                rejected += ok
                continue
            tree = mutant_tree(ctx, work, label)
            try:
                fn(tree, ctx)
            except RuntimeError:
                details.append((label, False))
                continue
            ok = not check(ctx.clone(tree=tree))[0]
            rejected += ok
            details.append((label, ok))
    else:
        muts = {'G1': G1_MUTANTS, 'G2': G2_MUTANTS, 'G3': G3_MUTANTS,
                'G4': G4_MUTANTS, 'G5': G5_MUTANTS, 'G7': G7_MUTANTS}[gid]
        for label, fn in muts:
            total += 1
            tree = mutant_tree(ctx, work, label)
            try:
                fn(tree, ctx)
            except RuntimeError:
                details.append((label, False))
                continue
            sub = ctx.clone(tree=tree)
            if gid == 'G3' and ctx.base_tree:
                sub.added_text = no_index_added(ctx.base_tree, tree,
                                                os.path.join(work, 'mut', label))
            ok = not check(sub)[0]
            rejected += ok
            details.append((label, ok))
    verdict = bool(positive) and total >= 2 and rejected == total
    return positive, rejected, total, verdict, details


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv):
    opts = parse_args(argv)
    if opts['selftest']:
        mode = 'selftest'
    elif opts['export_ref']:
        mode = 'export'
    else:
        die('plain run refused: --export-ref <hash> is required '
            '(or --selftest); a working-tree run can be turned green by '
            'uncommitted edits')
    lane = os.path.realpath(opts['lane'])
    want = opts['export_ref'] or 'HEAD'
    work = None
    auto_work = False
    try:
        work, auto_work = make_work(lane, opts['work'])
        resolved, export, base_tree = prepare_export(lane, want, work,
                                                     need_base=opts['selftest'])
        ctx = Ctx(export, want, resolved, lane, work,
                  os.path.realpath(opts['scratch_root']), base_tree)
        sys.stdout.write('export-ref=%s mode=%s lane=%s suite-sha256=%s\n'
                         % (resolved, mode, lane, suite_digest()))
        if mode == 'selftest':
            fails = 0
            ran = 0
            for gid in CHECK_IDS:
                positive, rejected, total, verdict, details = run_case(ctx, gid, work)
                ran += 1
                if not verdict:
                    fails += 1
                sys.stdout.write('selftest case=%s positive=%s mutants=%d/%d verdict=%s\n'
                                 % (gid, 'pass' if positive else 'fail',
                                    rejected, total, 'pass' if verdict else 'fail'))
                for label, ok in details:
                    sys.stdout.write('selftest detail=%s mutant=%s rejected=%d\n'
                                     % (gid, label, 1 if ok else 0))
            sys.stdout.write('selftest cases=%d failures=%d\n' % (ran, fails))
            return 0 if (ran == 8 and fails == 0) else 1
        results = []
        closed_n = 0
        for gid in CHECK_IDS:
            closed, pay = CHECKS[gid](ctx)
            if closed:
                closed_n += 1
            results.append('G%s payload=%s closed=%d' % (gid[1], pay, 1 if closed else 0))
        for line in results:
            sys.stdout.write(line + '\n')
        sys.stdout.write('closed=%d/8 exit=%d\n' % (closed_n, 0 if closed_n == 8 else 1))
        return 0 if closed_n == 8 else 1
    except HarnessError as exc:
        sys.stderr.write('ExecRefChecker: %s\n' % exc)
        return 2
    finally:
        # Mirror the committed r37 suite: the owned subdirectories are always
        # removed, and an auto-created work dir goes with them; a caller-supplied
        # work dir itself is left in place.
        if work and os.path.isdir(work):
            for sub in ('export', 'mut', 'base', 'r37'):
                shutil.rmtree(os.path.join(work, sub), ignore_errors=True)
            if auto_work:
                shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    try:
        raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        raise SystemExit(2)
