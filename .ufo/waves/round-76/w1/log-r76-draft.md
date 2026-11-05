# DRAFT — LOG.md "## Round 76" block skeleton (ScribeLedger, not applied)
# Placement: end-of-file append after LOG.md line 2811 (the r75 block's last line). Every <FILL> is a number or hash the L1 measures at integration on the landed bytes; the freeze hash and base hash are real and go in as written. This header is not part of the text.
==========

## Round 76 — the recheck-cwd census forged-relabel kill, load-bearing RESULT limb and both-headers fixture (C1) and the OSV.dev API overview as F54 on S111 (C2)

- Declared two claims in `.ufo/waves/round-76/claims.json`. Freeze `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e`; base `a788021675873a96e09e91aa033d8c26ac2fe212`; controls committed at the freeze under `.ufo/waves/round-76/controls/`. C1 `depth:verifiability` (lowest non-retired axis, nominal 4 held per R58): `corpus/instruments/recheck-cwd-census.py` is amended for a neither-header file (counted only in `norecheck`), a load-bearing case-6 RESULT limb, and a both-headers fixture classed as a normal entry. C2 `coverage` (held at 8): Frontier F54, the OSV.dev API overview, on S111.
- Attempt 1, dispatched wave `w1`: one v1 wave of 13 seats (3 executors, 2 scouts, 2 scribes, 2 reviewers, 1 critic, 1 mutation-tester, 1 sentinel, 1 connector; counted from `.ufo/waves/round-76/w1-spec.json` `items`). Dead seats <FILL>. Reports `.ufo/waves/round-76/w1/`.
- Base controls (receipts at the freeze): base selftest `cases=6 failures=0` exit 0; base census `entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0`, conformant, exit 0; red-before: the three base-counter mutants m1-forged-relabel, m2-result-limb-removed, m3-restoration-forces each print `selftest cases=6 failures=0`, rc 0; base frontier `rows=53 admitted=53 closed=53 registry=110`, `entries=56 pass=56 exit=0`; capture `records=89 bound=89`; knowledge 91; expected 93 lines / 91 rows.
- C1 landing: commit <FILL>; amended counter sha256 <FILL>; `selftest cases=8 failures=0` exit <FILL>. Red-before mutants on the amended selftest: M-R1 forged relabel rc <FILL>; M-R2 case-6 RESULT limb removed rc <FILL>; M-R3 restoration-recheck: forces restoration_only rc <FILL>. Real-tree census `entries=91 … restoration_only=0` conformant, exit <FILL>; diff against `c1-donothing-realtree-r76.txt` <FILL: empty or not>. Exec surface: `"bash", "-c"` count <FILL> (base 1); `subprocess.run(` count <FILL> (base 1); writes outside `tempfile.mkdtemp` <FILL>.
- C2 landing: `corpus/source-snapshots/round-76/{S111.txt,manifest.json}`; registry row S111 (110 -> <FILL>; removed rows <FILL>); knowledge entry `corpus/knowledge/osv-api-surface-and-limits.md` (91 -> <FILL>); `knowledge-expected.txt` inserted at line 68 (93/91 -> <FILL>; `LC_ALL=C sort -c` exit <FILL>); README F54 block; PROVINCE amendment; the SOURCES.md Leads bullet for the OSV overview retired. Measured: `FRONTIER-CENSUS rows=<FILL> admitted=<FILL> … registry=<FILL>`, `FRONTIER-PASS F54 ids=S111`, `entries=<FILL> pass=<FILL> exit=<FILL>`; `capture-binding-check.py` `records=<FILL> bound=<FILL> unbound=<FILL>` exit <FILL>; `source-recheck.py --manifest … --source S111` exit <FILL>, with <FILL: N> quotes anchor-located. Measured before integration by ScribeLedger on the committed manifest: Q01 (`API (1.0)`, line 21) is UNAVAILABLE `reason=quote-too-short-to-be-evidence`, rc 2 (`MIN_QUOTE_CHARS = 12`, `source-recheck.py` line 33); the repair is an L1 or operator decision and is recorded in the lesson's routed defects. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit <FILL> (six inherited W04 warnings).
- Verdicts: C1 <FILL: VERIFIED or FAILED on A1-A5, kill rule applied as frozen>. C2 <FILL: VERIFIED or FAILED on B1-B7, kill rule applied as frozen>.
- Mistake mining: <FILL: M76-x ids and one-line summaries from corpus/lessons/round-76.md § Mistakes>.
- Non-claim work: the S111 registry row, the knowledge entry, the README and PROVINCE blocks, the LOG, SCORECARD and lesson drafts, the considerthese sweep verdict, and the assimilation collision re-derivation (merge/kasegi staged ids vs the lane registry; adoption stays closed while collisions persist; the r70/r71 L0 questions are the routing item).
- No capability row, retirement or split <FILL: confirm>. Predicates were not reworded after any seat scored.

### Round-76 counters (before → after)

| counter | before (base `a788021`, controls `5da54cd`) | after (landed tree) | command |
|---|---|---|---|
| recheck-cwd census selftest | `selftest cases=6 failures=0` exit 0 | <FILL> | `TMPDIR=<scratch> python3 -B corpus/instruments/recheck-cwd-census.py --selftest` |
| census on the real tree | `RECHECK-CWD entries=91 … restoration_only=0`, conformant, exit 0 | <FILL: byte-identical to base (A4)> | `python3 -B corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` from `/tmp` |
| registry rows | 110 | <FILL> | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` |
| knowledge entries | 91 | <FILL> | `ls corpus/knowledge/*.md \| wc -l` |
| frontier admitted | 53 (F01–F53) | <FILL> (F01–F54) | `python3 corpus/instruments/frontier-recheck-count.py` |
| capture records | `records=89 bound=89` | <FILL> | `python3 corpus/instruments/capture-binding-check.py` |

### Round-76 counting commands

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=/fast/scratch/hyaku/kasegi-r76/<L1>/tmp python3 -B corpus/instruments/recheck-cwd-census.py --selftest
cd /tmp && python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-cwd-census.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-76/manifest.json --source S111
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-binding-check.py && python3 corpus/instruments/frontier-recheck-count.py
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```
