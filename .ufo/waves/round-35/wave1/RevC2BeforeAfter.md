# RevC2BeforeAfter — round-35 wave-1 receipt (C2 independent before→after verification)

Seat: RevC2BeforeAfter-2 (leaf, L1 = KasegiR35). I did not author any C2 change; every counter below was
re-derived with my own command from `.ufo/waves/round-35/claims.json` (C2 `counting_commands`), at the tip
and, for the before state, against a `git archive` of base `3266c9937b03062d9bbc2f436e20820115ed179c`
extracted to scratch. No writes outside the lane; no tool installed or upgraded (host `python3` 3.14.8,
`grep`/`awk`/`sha256sum` only).

## Report

Tree state verified: HEAD `da2d3c687f82a9814ee71c91c930cb733050d37c` (wave-1 spec + dispatch) on top of
freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9` on base `3266c993…`; the C2 corpus edits
(`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/cisa-kev-catalog.md`,
`corpus/instruments/knowledge-expected.txt`, `corpus/source-snapshots/round-35/`) landed in the working
copy uncommitted at 03:42 local while I was verifying; all after-state counters were re-run after that
landing. Verification window 03:33–03:43 local (-0300), 2026-10-26.

Instruments are byte-identical between base and tip (`cmp` clean for both `frontier-recheck-count.py` and
`source-recheck.py`), so the counter delta is purely corpus content, not tooling drift. Both instruments'
selftests pass at tip (`source-recheck.py --selftest` → `selftest cases=10 failures=0` exit 0;
`frontier-recheck-count.py --selftest` → `selftest cases=6 failures=0` exit 0).

### 1. Before state (base 3266c99, derived independently) — 7/7 match the frozen control

Base tree extracted with `git archive 3266c993… | tar -x -C $S/before`; greps run against those files,
scripts run inside the extracted tree. `$S` = `/fast/scratch/hyaku/kasegi-r35/RevC2BeforeAfter-2`.

| Counter (claims.json C2 before) | My command at base tree | Output | Frozen `c2-controls/before.txt` | Match |
|---|---|---|---|---|
| frontier_admitted=17 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `17` exit=0 | 17 | YES |
| registry rows=51 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `51` exit=0 | 51 | YES |
| S052_rows=0 | `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` | `0` exit=1 | 0 | YES |
| entries citing S052=0 | `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` | `0` | 0 | YES |
| harness entries=20 pass=20 exit=0 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=20 pass=20 exit=0` (F01–F17, 20 PASS lines) | `entries=20 pass=20 exit=0` | YES |
| source-recheck S052 exit 2 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` | `manifest UNAVAILABLE reason=missing` exit=2 | `manifest UNAVAILABLE reason=missing` / `recheck_exit=2` | YES |
| knowledge entries=46 | `ls corpus/knowledge/*.md \| wc -l` | `46` | 46 | YES |

Census on the base tree was not re-runnable (the fleet census validates the live lane in place; running it
against a scratch copy would misreport). The L1's frozen `census-before.txt`/`before.txt` control records
the before census; my independent tip census (§2) shows the same W04-only pattern, so the before→after
census delta is empty as claimed.

### 2. After state at tip — 8/8 counters match claims.json

All commands run from the lane root after the 03:42 landing.

1. **Frontier count 17 → 18.** `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `18` exit=0 (base: 17).
   All 18 rows carry `admitted`: `grep -cE '^\| F[0-9]+ \|[^|]*\| admitted \|' corpus/README.md` → `18`.
   The F18 row is `corpus/README.md:388`:
   `| F18 | CISA Known Exploited Vulnerabilities catalog — exploitation-status-based prioritization distinct from CVSS severity | admitted | knowledge/cisa-kev-catalog.md | S052 | Keep the catalog's remediation clock attached to the directive that binds it: … KEV listing is an exploitation-status signal, not a severity score — the feed carries no severity field (12 keys x 1756 records, cvss 0). |`
   It sits in an appended "Round-35 admission" section (R6/R9 append-only convention; `git diff
   corpus/README.md` shows additions only, zero deletions), and the harness binds it (item 5).
2. **Registry rows 51 → 52.** `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` →
   `52` exit=0 (base: 51). `git diff corpus/SOURCES.md` shows additions only (1 row + 6 changelog
   bullets); no pre-existing row edited.
3. **S052 row = 1, tier A, mined, opened 2026-10-26.** `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|'
   corpus/SOURCES.md` → `1` exit=0 (base: 0). Row at `corpus/SOURCES.md:58`, columns extracted with awk:
   id `S052`, kind `dataset`, tier `A`, status `mined`, opened `2026-10-26`, recheck `90d`, used-by
   `corpus/knowledge/cisa-kev-catalog.md`, capture column carries sha256
   `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` / 1479694 bytes / 27870 lines.
   Row URL vs manifest URL byte-equality checked programmatically: `BYTE-EQUAL:
   https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` (QUALITY R20).
4. **Entries citing S052 = 1.** `grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l` → `1`
   (base: 0); the file is `corpus/knowledge/cisa-kev-catalog.md`, whose `source:` line (entry :3) cites
   the same feed URL and capture digest, with a `recheck:` line (:6) naming the manifest and the five
   Q1–Q5 assertions.
5. **Harness 20/20 → 21/21 exit 0 incl. `PASS F18 ids=S052`.**
   `python3 corpus/instruments/frontier-recheck-count.py | grep -E 'F18|entries='` →
   `PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0` and
   `entries=21 pass=21 exit=0`, harness exit=0 (base: `entries=20 pass=20 exit=0`). 18 frontier rows +
   3 second entries (F09/F10/F11) = 21, consistent.
6. **source-recheck S052: exit 2 → exit 0, every assertion occurrences=1, sha256 OK.**
   `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` →
   `S052:sha256 OK` / `S052:Q1 OK occurrences=1 anchor=2-ok` / `S052:Q2 OK occurrences=1 anchor=3-ok` /
   `S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok` / `S052:Q4 OK
   normalized=markup-whitespace occurrences=1 anchor=15472-ok` / `S052:Q5 OK
   normalized=markup-whitespace occurrences=1 anchor=19165-ok`, exit=0 (base: exit=2 missing manifest).
7. **Census exit 0, W04 S028/S029 only (before and after).**
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` →
   `kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes` /
   `kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes` /
   `kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`, census_exit=0. Re-run
   after the S052 row landed: same two W04 lines, no new findings — the S052 row introduces no E-code
   and no new W04.
8. **Knowledge entries 46 → 47.** `ls corpus/knowledge/*.md | wc -l` → `47` (base: 46);
   `corpus/instruments/knowledge-expected.txt` grew 48 → 49 lines with
   `corpus/knowledge/cisa-kev-catalog.md` at :7.

### 3. Junk twin (c2-controls/junk-f18.md) — rejected, proven independently

The twin is a shape-identical fixture (H1, `source: S052`, `recheck:` line) whose two quoted strings are
fabrications. Its own `recheck:` line points at the real manifest, so the discriminating invocation must
recheck *the twin's own quotes*. I built that control myself in scratch
(`$S/junk/round-35/manifest.json`, schema 1, record id `S052` / path `S052.txt` — a byte-copy of the
committed capture, same sha256 — asserting the twin's two fabricated quotes):

```
python3 corpus/instruments/source-recheck.py --manifest $S/junk/round-35/manifest.json --source S052
S052:sha256 OK
S052:J1 MISMATCH reason=quote-not-found
S052:J2 MISMATCH reason=quote-not-found
exit=1
```

(First attempt with record id `S052JUNK` failed closed with `S052JUNK:manifest MISMATCH
reason=stem-mismatch` exit=1 — the instrument's B1 stem rule; corrected to id `S052`.) So the twin's
quotes fail the capture recheck: exit != 0 as the kill rule requires. Not admitted: `grep -c 'junk-f18'
corpus/README.md` → `0` exit=1, and the harness counts 21 entries (not 22) with no junk row. The
"non-author reviewer REFUSE on record" half of the after-state lives in the do-nothing seat's receipt
(`wave1/ExecDoNothingReject.md`), which had **not landed** at 03:43 local (seat still waiting for closure
readiness) — pending for the L1's final integration check, not a corpus defect.

### 4. Entry spot-checks (independent reproduction of the entry's own falsifiable checks)

Against the committed capture, all reproduce the entry's stated values exactly:

- FC-1: `keys 5 count 1756 records 1756`
- FC-8: `cvss=0 base score=0 risk rating=0 reward=0 bounty=0 severity+score=3`
- FC-9 (FCEB sentence, deliberately anchored in-entry, not a manifest assertion): `2`
- FC-10 (BOD 22-01 sentence, 327 identical records): `327`

The entry's two repeated sentences (occurrences 2 and 327) are correctly kept *out* of the manifest —
every manifest assertion is `occurrences=1` — and are anchored/counted in-entry instead (entry §Scope).
Claim 4b (BOD 26-04 live-page read) is explicitly labelled not-a-pinned-source in the entry; out of C2's
counter scope, noted as declared.

### 5. Digests at verification time (03:43 local)

```
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md
a5696dc057a7fb608f3d77f21f0101fb150de8f8d0455090fb6a4e4d9e58c838  corpus/knowledge/cisa-kev-catalog.md
d2e99ca60bc5acf109a60a26452379bc8d428ea0cb382f1e513696a7873347a8  corpus/instruments/knowledge-expected.txt
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176  .ufo/waves/round-35/c2-controls/junk-f18.md
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
```

### 6. Verdict

**C2: all 8 counters match claims.json at the tip, and the independently derived before state matches the
frozen before-control 7/7. No differences found. No kill-rule condition observed.** Junk twin rejected by
my own discriminating recheck (exit 1, `quote-not-found` ×2) and not admitted anywhere. Timing caveats for
the L1: (a) the C2 corpus edits landed uncommitted at 03:42 local, mid-verification — the after-state
numbers above are post-landing; (b) `wave1/ExecDoNothingReject.md` (REFUSE record) was still absent at
03:43 local; (c) everything verified is in the working copy — the L1's commit makes it durable.

Scratch `$S` deleted before yielding (verified absent); no defect from leftover trees.
