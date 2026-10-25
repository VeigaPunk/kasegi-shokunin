# RevCounters1 — C1 independent counter re-run (round 28, wave 1)

Seat: RevCounters1 (reviewer, read-only; no production edits made)
State: **PRE-STATE** — the impl had NOT landed at run time.
Evidence: `sha256sum corpus/instruments/anchorcheck.py` =
`c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748`
(the frozen pre-change digest) observed twice: 2026-10-25T17:22:55Z and
2026-10-25T17:24:12Z. Source scan confirms pre-change limbs: no
`FAIL_CLASSES`, no `--selftest` handling, CITE regex (line 104) lacks a
`~/Projects/bounties/` arm; 283 lines total.

All four frozen counter commands were executed verbatim from the lane root
(`/home/vgpnk/Projects/shokunin/kasegi-shokunin`) against the committed
pre-change bytes and the committed round-27 fixtures. After-values below are
from `.ufo/waves/round-28/claims.json` (frozen). Verdicts compare observed
values to the frozen after-values AND to the frozen before-values.

---

## Counter 1 — bad-fixture exit

Command (verbatim):
```
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo $?
```
Output: `0` (exit of the pipeline: 0)
Timestamp: 2026-10-25T17:23:07Z
Frozen after-value: `1`. Frozen before-value: `0` (BASE-ABSENT printed, exit 0).

Verbatim verdict line (unfiltered run, for the record):
```
== .ufo/waves/round-27/c1-controls/bad-fixture.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1
BASE-ABSENT md:2 corpus/knowledge/zz-r27-anchorcheck-missing.md:99 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/corpus/knowledge/zz-r27-anchorcheck-missing.md)
```

Verdict: **PRE-STATE consistent** — before-value `0` reproduced exactly.
After-verdict (exit must become 1): **OWED** — unverifiable against
pre-change bytes; re-run required post-landing. Do-nothing control holds:
pre-change bytes do not reach the after-value.

## Counter 2 — bounties fixture BOUNTIES-ABSENT count

Command (verbatim):
```
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
```
Output: `0` (pipeline exit: 1 — grep's normal zero-match exit; the metric
line itself is `0`)
Timestamp: 2026-10-25T17:23:07Z
Frozen after-value: `1`. Frozen before-value: `0` (cite not matched by CITE).

Verbatim summary (unfiltered run, for the record):
```
== .ufo/waves/round-27/c1-controls/bounties-fixture.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```
The bounties cite is invisible to CITE pre-change — consistent with the
predicate (b).

Verdict: **PRE-STATE consistent** — before-value `0` reproduced.
After-verdict (must become `1`): **OWED** — requires the landed
`~/Projects/bounties/` CITE arm. Do-nothing control holds.

## Counter 3 — selftest receipt index + selftest exit

Command (verbatim):
```
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt && grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt && sha256sum corpus/instruments/anchorcheck.py | awk '{print "instrument_sha256="$1}' && python3 corpus/instruments/anchorcheck.py --selftest >/dev/null 2>&1; echo selftest_exit=$?
```
Output:
```
grep: .ufo/waves/round-28/c1-receipt-index.txt: No such file or directory (os error 2)
selftest_exit=2
```
Timestamp: 2026-10-25T17:23:07Z

Note on `selftest_exit=2`: the `&&` chain short-circuited on the first grep
(missing receipt index), so `python3 anchorcheck.py --selftest` never ran
inside the chain; `2` is the chain's exit, not the instrument's. Run
standalone at 2026-10-25T17:23:20Z:

Command:
```
python3 corpus/instruments/anchorcheck.py --selftest; echo selftest_exit=$?
```
Output:
```
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/anchorcheck.py", line 283, in <module>
    sys.exit(main(sys.argv[1:]))
  File "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/anchorcheck.py", line 135, in main
    for line in open(src):
FileNotFoundError: [Errno 2] No such file or directory: '--selftest'
selftest_exit=1
```

Frozen after-value: `1` receipt line at instrument_sha256 matching
`sha256sum corpus/instruments/anchorcheck.py`, `selftest cases=N failures=0`,
exit=0. Frozen before-value: `0` (`--selftest` crashes FileNotFoundError
exit 1).

Verdict: **PRE-STATE consistent** — receipt index absent (0 lines) and
`--selftest` crashes FileNotFoundError exit 1, both exactly the frozen
before-values. After-verdict: **OWED** — requires ExecReceiptCanonC1's
landed index at the post-change digest plus the landed `--selftest` limb.
Do-nothing control holds.

## Counter 4 — SKILL.md live no-harm (exit, bad, LOST-RECORDED)

Command (verbatim):
```
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo $? ; python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p' ; python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | sed -n 's/^== .*LOST-RECORDED=\([0-9]*\).*/lost=\1/p'
```
Output:
```
0

lost=306
```
(exit `0`; the `bad=` limb printed **nothing**; `lost=306`)
Timestamp: 2026-10-25T17:23:07Z

Frozen after-values: `skill_md_exit=0`, `skill_md_bad=0`,
`skill_md_lost_recorded=306`. Frozen before-values identical (this limb is a
no-harm invariant; before == after by design).

Verdict: **partially verifiable now.** exit=0 **PASS**; lost=306 **PASS**.
bad= **FAIL as specified** — the extractor emitted no `bad=` line at all
(see Finding F1). The underlying truth is checkable in the unfiltered
summary (line 2 of output):
```
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```
so bad really is 0 — the counter's sed simply cannot see it.

---

## Findings by severity

### F1 (medium, blocking the counter as frozen) — counter-4 `bad=` extractor can never emit `bad=0`

The frozen command greps with
`s/^== .*bad; \([0-9]*\) bad.*/bad=\1/p`, which requires a `bad` token
*after* the first semicolon. The instrument's actual summary format is
`== FILE: N in-range cite instances, M bad; K distinct anchors; LOST=…` —
the token after `bad;` is `K distinct anchors`, never `K bad`. Observed: the
limb prints nothing (empty output), exit 0, against both the round-27
pre-change bytes now and — per `.ufo/waves/round-27/c1-controls/skill-before.txt`
line 2 — the same summary format last round. The format has no `bad; N bad`
shape today, and the C1 predicate does not require the impl to change the
summary format, so unless ExecImplC1 deliberately alters it, this limb stays
empty post-landing and the counter can never evidence `bad=0` — exposing the
claim to the kill rule on a specification defect, not an instrument defect.
Recommendation: land a claims.json correction file (per the frozen
corrections rule) replacing that sed with e.g.
`sed -n 's/^== .*cite instances, \([0-9]*\) bad;.*/bad=\1/p'`, then re-run.

### F2 (low, specification clarity) — counter-3 chain's `selftest_exit` is ambiguous pre-landing

Inside the `&&` chain the first grep fails before `--selftest` exists, so
`selftest_exit` reports the chain exit (`2`), not the instrument's. Frozen
before-value calls it exit 1 — which is what the instrument itself produces
(verified standalone above). Harmless once the receipt index exists (all
greps then succeed and the real selftest exit flows through), but the
before-receipt semantics deserve the footnote this receipt provides.

## Do-nothing control check (kill-rule limb)

Pre-change bytes on committed fixtures reproduce every frozen before-value
(exit 0, 0 BOUNTIES lines, no receipt index, selftest FileNotFoundError
exit 1, SKILL exit 0, LOST=306) and reach **no** after-value. The
do-nothing control behaves as designed. Round-28 fresh before-receipts
already exist at `.ufo/waves/round-28/c1-controls/` (written by another
seat; consistent with these observations, not re-verified line-by-line).

## Owed at close — exact re-run for the L1 post-landing

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/anchorcheck.py   # must differ from c2a9e6c6...
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo $?                                        # expect 1
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT                      # expect 1
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt && grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt && sha256sum corpus/instruments/anchorcheck.py | awk '{print "instrument_sha256="$1}' && python3 corpus/instruments/anchorcheck.py --selftest >/dev/null 2>&1; echo selftest_exit=$?   # expect 1 line, sha match, cases=N failures=0, exit 0
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo $? ; python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p' ; python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | sed -n 's/^== .*LOST-RECORDED=\([0-9]*\).*/lost=\1/p'   # expect 0, bad=0 (see F1), lost=306
```

## Scope and tooling notes

- Wrote only this receipt. Read-only otherwise; no VCS writes, no scratch
  outside my receipt path.
- Tools installed/upgraded: none (everything needed was already present).
- Timing per the hard rule: impl not landed at 17:22–17:24Z; counters run
  anyway against pre-change bytes; after-verdicts owed as listed above.
