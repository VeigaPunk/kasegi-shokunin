#!/usr/bin/env python3
"""Generate the G2' graded-selftest fixtures from one canonical green receipt.

Every fixture is a byte-exact all-gates v3 receipt.  The green receipt is
accepted by judge-g2-cases.sh; each mutant differs from it in exactly one
respect and must be rejected.  Header hashes are placeholders (40 zeros /
64 zeros): a fixture is never bound to a lane head, so the header-binding
fields of the real G2 stay out of scope here.
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

Z40 = '0' * 40
Z64 = '0' * 64

CHECKS = [
    ('G1', 'blocks=3,declared=3,fence=closed,corrections=2,paths=3',
     ['declared-lines-drift', 'fence-open-at-eof']),
    ('G2', 'receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,'
           'digest-match=1,run-lines=1,closed-line=1,cases=8,graded=8,'
           'detail-ok=1,summary=1,summary-only=0,scorecard-ref=1,shonen-ref=1,'
           'head-token-lines=0',
     ['summary-only-pass', 'seven-cases-pass']),
    ('G3', 'quoted=6,transcripts=6,report-only=0', ['uncommitted-quote']),
    ('G4', 'dispatch=1,tasks=73,seats=73,distinct=73,zero-task=0',
     ['duplicate-seat-identity', 'zero-task-dispatch']),
    ('G5', 'final-lane-commit=0,round-39-head-tokens=0,by-reference=2',
     ['final-lane-commit-token']),
    ('G6', 'r37=absent,r38=absent,r39=own-work-only,unreadable=0',
     ['stale-scratch-entry', 'unreadable-scratch-dir']),
    ('G7', 'section=1,rows=1,correction=1', ['empty-dispositions']),
    ('G8', 'pinned=1,suite-sha256-match=1,r37-closed=1',
     ['unpinned-bytes', 'r37-red']),
]


MUTANTS = """\
# G2' mutant list — embed each row as a negative control under G2.
# Columns: id<TAB>fixture<TAB>expected closed<TAB>mutation
# The exact expected `G2 payload=... closed=` line per fixture is expected.tsv;
# judge-g2-cases.sh must print it byte-for-byte.
P-G2-01\treceipt-green.txt\t1\tunmutated all-gates v3 receipt (positive control): eight graded case lines, detail-backed, one summary
M-G2-01\tb-summary-only.txt\t0\tvariant (b): all `selftest case=`/`selftest detail=` lines removed, `selftest cases=8 failures=0` kept — a summary-only line must satisfy no case
M-G2-02\tc-verdict-fail.txt\t0\tvariant (c): G4 case line `positive=pass ... verdict=pass` -> `verdict=fail`
M-G2-03\td-missing-verdict.txt\t0\tvariant (d): G6 case line loses its ` verdict=pass` field
M-G2-04\te-seven-cases.txt\t0\tvariant (e): G8 case+detail lines removed, summary still claims `cases=8` — a lying summary must not rescue a 7-case run
M-G2-05\tm01-duplicate-id.txt\t0\tG3 case line duplicated, G7 case line removed: eight case lines, seven graded ids, one id twice
M-G2-06\tm02-detail-free-0-0.txt\t0\tevery case line rewritten to `mutants=0/0`, detail lines removed — shape-only pass
M-G2-07\tm03-details-removed.txt\t0\tcase lines claim 2/2 but all `selftest detail=G<n> mutant=` lines are gone
M-G2-08\tm04-detail-rejected-0.txt\t0\tone G2 mutant detail flipped to `rejected=0`
M-G2-09\tm05-detail-rejected-10.txt\t0\tone G5 mutant detail changed to `rejected=10` — `rejected=1` must be a whole token
M-G2-10\tm06-ninth-case-g9.txt\t0\ta ninth graded-looking `selftest case=G9 ... verdict=pass` line with its detail line
M-G2-11\tm07-trailing-field.txt\t0\tG1 case line gains ` note=ok` after `verdict=pass` — the verdict field must terminate the line
M-G2-12\tm08-case-missing-mutants.txt\t0\tG3 case line loses its `mutants=<a>/<b>` field
M-G2-13\tm09-case-missing-positive.txt\t0\tG5 case line loses its `positive=pass` field
M-G2-14\tm10-summary-failures-1.txt\t0\tsummary rewritten to `selftest cases=8 failures=1`
M-G2-15\tm11-summary-duplicated.txt\t0\ttwo `selftest cases=8 failures=0` lines — exactly one is required
M-G2-16\tm12-sentinel-v2.txt\t0\tfirst line `all-gates v2` with a perfect case region — the case region alone must not close G2
M-G2-17\tm13-closed-7of8.txt\t0\t`closed=8/8 exit=0` -> `closed=7/8 exit=1`
M-G2-18\tm14-run-line-closed-0.txt\t0\tG5 run line reports `closed=0`
M-G2-19\tm15-run-line-missing.txt\t0\tthe `G8 payload=... closed=1` run line is absent (seven run lines)
M-G2-20\tm16-seven-cases-truthful-summary.txt\t0\tseven case lines plus `selftest cases=7 failures=0` — a truthful summary cannot close a short run
M-G2-21\tm17-positive-fail.txt\t0\tG7 case line `positive=fail mutants=0/1 verdict=fail`
M-G2-22\tm18-bare-summary-only.txt\t0\tthe selftest region is one bare `selftest cases=8 failures=0` line, no selftest header, no case lines
M-G2-23\tm19-eight-summary-lines.txt\t0\teight summary lines and zero case lines — repetition does not manufacture cases
"""

def green():
    """The canonical all-gates v3 receipt: header, eight run lines, receipt
    close line, selftest region (header, per-check details then case lines),
    selftest summary."""
    L = ['all-gates v3',
         'export-ref=' + Z40,
         'suite-sha256=' + Z64,
         'run-ref=' + Z40]
    for cid, payload, _ in CHECKS:
        L.append('%s payload=%s closed=1' % (cid, payload))
    L.append('closed=8/8 exit=0')
    L.append('selftest export-ref=%s lane=kasegi-shokunin suite-sha256=%s'
             % (Z40, Z64))
    for cid, payload, mutants in CHECKS:
        L.append('selftest detail=%s positive=pass payload=%s' % (cid, payload))
        for m in mutants:
            L.append('selftest detail=%s mutant=%s rejected=1 payload=red'
                     % (cid, m))
        n = len(mutants)
        L.append('selftest case=%s positive=pass mutants=%d/%d verdict=pass'
                 % (cid, n, n))
    L.append('selftest cases=8 failures=0')
    return L


def idx(L, prefix, start=0):
    for i in range(start, len(L)):
        if L[i].startswith(prefix):
            return i
    raise SystemExit('missing line: ' + prefix)


def case_line(L, cid):
    return idx(L, 'selftest case=%s ' % cid)


def drop_detail(L, cid):
    """Delete every `selftest detail=<cid> mutant=` line."""
    return [x for x in L if not x.startswith('selftest detail=%s mutant=' % cid)]


def drop_case(L, cid):
    i = case_line(L, cid)
    return L[:i] + L[i + 1:]


def set_line(L, cid, text):
    L = list(L)
    L[case_line(L, cid)] = text
    return L


def replace_one(L, old, new):
    L = list(L)
    i = L.index(old)
    L[i] = new
    return L


def build():
    g = green()
    fx = {}

    # P-G2-01 / variant (a): the green receipt.
    fx['receipt-green.txt'] = g

    # M-G2-01 / variant (b): summary-only — no per-case lines at all.
    fx['b-summary-only.txt'] = [
        x for x in g
        if not (x.startswith('selftest case=') or x.startswith('selftest detail='))]

    # M-G2-02 / variant (c): positive=pass but verdict=fail.
    fx['c-verdict-fail.txt'] = set_line(
        g, 'G4', 'selftest case=G4 positive=pass mutants=1/1 verdict=fail')

    # M-G2-03 / variant (d): the verdict= field is absent.
    fx['d-missing-verdict.txt'] = set_line(
        g, 'G6', 'selftest case=G6 positive=pass mutants=2/2')

    # M-G2-04 / variant (e): seven graded cases; the summary still claims 8.
    L = drop_detail(drop_case(g, 'G8'), 'G8')
    fx['e-seven-cases.txt'] = L

    # M-G2-05: duplicate id — G3 appears twice, G7 never.
    L = list(g)
    i = case_line(L, 'G3')
    L.insert(i + 1, L[i])
    L = drop_case(L, 'G7')
    fx['m01-duplicate-id.txt'] = L

    # M-G2-06: detail-free pass — every case line claims mutants=0/0 and no
    # detail line stands behind it.
    L = [x for x in g if not x.startswith('selftest detail=')]
    out = []
    for x in L:
        for cid, _, _ in CHECKS:
            if x.startswith('selftest case=%s ' % cid):
                x = 'selftest case=%s positive=pass mutants=0/0 verdict=pass' % cid
        out.append(x)
    fx['m02-detail-free-0-0.txt'] = out

    # M-G2-07: case lines claim 1/1, the detail lines are gone.
    fx['m03-details-removed.txt'] = [x for x in g
                                     if not x.startswith('selftest detail=')]

    # M-G2-08: one mutant detail says rejected=0.
    fx['m04-detail-rejected-0.txt'] = replace_one(
        g, 'selftest detail=G2 mutant=summary-only-pass rejected=1 payload=red',
        'selftest detail=G2 mutant=summary-only-pass rejected=0 payload=red')

    # M-G2-09: rejected=10 must not read as rejected=1.
    fx['m05-detail-rejected-10.txt'] = replace_one(
        g, 'selftest detail=G5 mutant=final-lane-commit-token rejected=1 payload=red',
        'selftest detail=G5 mutant=final-lane-commit-token rejected=10 payload=red')

    # M-G2-10: a ninth check line (G9) on top of the green eight.
    L = [x for x in g if not x.startswith('selftest cases=')]
    L += ['selftest detail=G9 positive=pass payload=extra',
          'selftest detail=G9 mutant=extra rejected=1 payload=red',
          'selftest case=G9 positive=pass mutants=1/1 verdict=pass',
          'selftest cases=8 failures=0']
    fx['m06-ninth-case-g9.txt'] = L

    # M-G2-11: text after verdict=pass breaks the anchored field tail.
    fx['m07-trailing-field.txt'] = set_line(
        g, 'G1', 'selftest case=G1 positive=pass mutants=2/2 verdict=pass note=ok')

    # M-G2-12: the mutants= field is absent.
    fx['m08-case-missing-mutants.txt'] = set_line(
        g, 'G3', 'selftest case=G3 positive=pass verdict=pass')

    # M-G2-13: the positive= field is absent.
    fx['m09-case-missing-positive.txt'] = set_line(
        g, 'G5', 'selftest case=G5 mutants=1/1 verdict=pass')

    # M-G2-14: summary claims a failure.
    fx['m10-summary-failures-1.txt'] = replace_one(
        g, 'selftest cases=8 failures=0', 'selftest cases=8 failures=1')

    # M-G2-15: two summary lines (exactly one is required).
    L = [x for x in g if not x.startswith('selftest cases=')]
    L += ['selftest cases=8 failures=0', 'selftest cases=8 failures=0']
    fx['m11-summary-duplicated.txt'] = L

    # M-G2-16: v2 sentinel with a perfect case region.
    L = list(g)
    L[0] = 'all-gates v2'
    fx['m12-sentinel-v2.txt'] = L

    # M-G2-17: closed line says 7/8 exit=1.
    fx['m13-closed-7of8.txt'] = replace_one(
        g, 'closed=8/8 exit=0', 'closed=7/8 exit=1')

    # M-G2-18: one run line is a red check.
    fx['m14-run-line-closed-0.txt'] = replace_one(
        g, 'G5 payload=final-lane-commit=0,round-39-head-tokens=0,by-reference=2 closed=1',
        'G5 payload=final-lane-commit=0,round-39-head-tokens=0,by-reference=2 closed=0')

    # M-G2-19: one run line is missing.
    L = [x for x in g if not x.startswith('G8 payload=')]
    fx['m15-run-line-missing.txt'] = L

    # M-G2-20: seven cases plus a truthful cases=7 summary.
    L = drop_detail(drop_case(g, 'G8'), 'G8')
    fx['m16-seven-cases-truthful-summary.txt'] = replace_one(
        L, 'selftest cases=8 failures=0', 'selftest cases=7 failures=0')

    # M-G2-21: positive=fail with verdict=fail.
    fx['m17-positive-fail.txt'] = set_line(
        g, 'G7',
        'selftest case=G7 positive=fail mutants=0/1 verdict=fail')

    # M-G2-22: the selftest region is the bare summary line only.
    fx['m18-bare-summary-only.txt'] = (
        ['all-gates v3',
         'export-ref=' + Z40,
         'suite-sha256=' + Z64]
        + ['%s payload=%s closed=1' % (cid, payload) for cid, payload, _ in CHECKS]
        + ['closed=8/8 exit=0',
           'selftest cases=8 failures=0'])

    # M-G2-23: eight summary lines, zero case lines.
    L = [x for x in g
         if not (x.startswith('selftest case=') or x.startswith('selftest detail=')
                 or x.startswith('selftest cases=') or x.startswith('selftest export-ref='))]
    L += ['selftest cases=8 failures=0'] * 8
    fx['m19-eight-summary-lines.txt'] = L

    return fx


def main():
    os.makedirs(OUT, exist_ok=True)
    fx = build()
    for name in sorted(fx):
        body = '\n'.join(fx[name]) + '\n'
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
            fh.write(body)
    with open(os.path.join(OUT, 'mutants.txt'), 'w', encoding='utf-8') as fh:
        fh.write(MUTANTS)
    print('fixtures=%d out=%s' % (len(fx), OUT))


if __name__ == '__main__':
    main()
