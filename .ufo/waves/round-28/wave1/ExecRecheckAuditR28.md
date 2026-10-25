# ExecRecheckAuditR28 — round 28, wave 1

Seat: leaf executor (leaf member; no dispatch, no background job).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `94f387cbee71a532a51ce075f01701a557231e85`
(dispatch base `c9f8b115` is an ancestor).
Item: run `corpus/instruments/recheck-audit.py` over the corpus after `corpus/knowledge/` lands, record the
summary line; then run the new F12 entry's `recheck:` line standalone from a foreign cwd **and** from the
lane root, both exit 0, and paste.
Receipt: `.ufo/waves/round-28/receipts/ExecRecheckAuditR28.txt` (536 lines, sha256
`7d320e42261ee093ad67f905738515e509df458a131cd955c4ba444291ea691e`).

## State: POST-STATE reached (PRE-STATE baseline preserved)

The F12 entry was absent at 17:25:38Z and landed while the seat was running. Both sides are measured.

| Obs | UTC | entries | anchorcheck.py (12) | audit exit | executes/gated | refreshed-list exit |
|---|---|---|---|---|---|---|
| O1 PRE | 17:25:38Z | 39 | `c2a9e6c60880` (r27 byte) | 0 | 16/23 | n/a |
| O2 POST | 17:26:55Z | 40 | `2f7070466fba` (intermediate) | 1 | 17/23 | 0 |
| O3 POST | 17:27:13Z | 40 | `982d720776f1` (intermediate) | 1 | 17/23 | 0 |
| O4 POST | 17:28:15Z | 40 | `c36292292ec0` (intermediate) | 1 | 16/24 | 0 |
| **O5 FINAL** | **17:29:06Z** | **40** | **`95333e29ee5a` (C1 landed)** | **1** | **16/24** | **0** |

`recheck-audit.py` sha256 `3fc0d751f2a5…`, `source-recheck.py` `9fe6a4a07fdb…`,
`knowledge-expected.txt` `30ba586029f6…` (unchanged since 09:48Z, still the 39-line file),
round-28 manifest `e62ddad133ff…`, S041 `e18acbf99d13…`, S042 `b432ec165693…`,
entry at O5 `a0f8e6172110…` (churned `55cf660f` → `0261f315` → `a0f8e617` during the wave).

## The two deliverables

**1. Audit summary line (lane root, `python3 corpus/instruments/recheck-audit.py`), exit 1 at O5:**

```text
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=39 missing=0 unexpected=1 exit=1
unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md
```

The exit 1 is **one stale owned file**, not the entry: `corpus/instruments/knowledge-expected.txt` still has
39 lines (ExecExpectedList's file; not edited here — probe E measured that a missing expected line alone
reds the audit with `unexpected=…`). With that list at 40 entries via `--expect`:

```text
python3 corpus/instruments/recheck-audit.py --expect /tmp/r28-kexp40.txt   -> exit 0
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=24 broken=0
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=40 missing=0 unexpected=0 exit=0
```

F12 row in both runs:
`japanese-domestic-disclosure-workflow.md  frozen=111 strict=111111 lane=0  foreign=0  executes  PASS`

**2. The entry's own `recheck:` line, standalone — exit 0 from both cwds, identical output (14 OK lines):**

```text
cwd=/tmp                                       exit=0
cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin  exit=0
S041:sha256 OK
S041:Q1 OK occurrences=1   ...  S041:Q6 OK occurrences=1
S042:sha256 OK
S042:Q1 OK occurrences=1   ...  S042:Q6 OK occurrences=1
```

Entry contract also holds: declared `source:` ids `S041 S042` == line `--source` ids `S041 S042`; `cd`
target is the lane root; both path tokens resolve; line runs `source-recheck.py` with
`--manifest corpus/source-snapshots/round-28/manifest.json`.

## Findings (measured, not inferred)

1. **The F12 entry passes every limb the audit has**, at every entry digest observed (O2–O5), and its
   standalone line is cwd-independent (exit 0 from `/tmp` and from the lane root). The audit's own exit 1
   is attributable solely to the stale expected list; refreshed, the round's exit 0 is reached.

2. **Gap class — `recheck-audit.py` is sound on FORM, blind on EVIDENCE STATE.** `class` is `gated` for
   *any* nonzero line exit that still parses, and `gated` counts as PASS. Nine-probe matrix on the real
   manifest/capture bytes (registry in the receipt):
   - `--source S999` (id not in the manifest) → source-recheck exit 2 → `gated` PASS, audit exit 0
   - line pointed at `round-26/manifest.json`, which does not list S042 → exit 2 → `gated` PASS, audit exit 0
   - one byte appended to the S042 capture → `S042:sha256 MISMATCH` exit 1 → `gated` PASS, audit exit 0
   - headers declare S041+S042 but the line checks only S041 → `executes` PASS, audit exit 0
     (declared-vs-line id equality is not an audit limb)
   Consequence: post-landing `recheck-audit.py` exit 0 is **necessary, not sufficient** for C2's
   "entry's recheck line exits 0 on its ids". That kill rule is enforced by
   `corpus/instruments/frontier-recheck-count.py` rules A/B (ExecHarnessC2's counter) and by the
   standalone runs above. Limbs that do bite: missing manifest file (`paths_fail=1`, exit 1) and
   expected-list drift (`unexpected=1`, exit 1).

3. **C1 cross-evidence (corpus side):** under the landed `anchorcheck.py 95333e29`, `citation-bases.md`
   flips exit 0 → 1 (`10 in-range cite instances, 0 bad; … BASE-ABSENT=1`, driven by
   `BASE-ABSENT md:31 …/the-bounty-hunter/ops/rank.mjs:55-58`). BASE-ABSENT is a declared C1 FAIL_CLASS,
   so this is intended fail-closed; the audit reclassifies the row `gated` and still counts it PASS.
   This — not the F12 entry — is why `executes` is 16, not 17. ExecImplC1 confirmed the reading and the
   landed digest. (Neither `executes` value is a stable acceptance number; key on the F12 row.)

4. Round-28 manifest and captures already satisfy every mechanical limb: 2 sources, 12 assertions, each
   `OK occurrences=1`, no anchor needed, both capture sha256 match the pins, exit 0 per id and whole-manifest.

## Risks / blockers

- **Blocker (owned by another seat):** `corpus/instruments/knowledge-expected.txt` is still 39 lines, so the
  canonical audit exits 1 at round end. ExecExpectedList was messaged with the measured basis
  (post-refresh `expected=40`, `lines=40 total=40 pass=40`); its receipt already records those numbers.
  I did not edit that file (ownership map).
- Entry digest churned four times during the wave (`55cf660f` → `0261f315` → `a0f8e617` → `a22d2321`);
  numbers are pinned to the stated digests, and the final bytes `a22d2321` were re-measured at 17:31:01Z
  (receipt §O6) with the same outcome: row `executes PASS`, standalone exit 0 from both cwds, refreshed
  audit exit 0 `expected=40`. If the entry moves again, re-run R1+R2.
- The three intermediate `anchorcheck.py` digests appear in the receipt body as measured; O5 supersedes
  them and names the landed digest.

## L1 re-run (post-landing acceptance)

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/recheck-audit.py                     # expect exit 0 once the expected list is 40
CMD=$(sed -n 's/^recheck:[[:space:]]*//p' corpus/knowledge/japanese-domestic-disclosure-workflow.md)
( cd /tmp && bash -c "$CMD" ); echo foreign_exit=$?            # expect 0
bash -c "$CMD"; echo lane_exit=$?                              # expect 0
```

Accept: F12 row `frozen=111 strict=111111 lane=0 foreign=0 executes PASS`; `strict pass=40/40`;
`lines=40 total=40 pass=40`; `expect=present expected=40 missing=0 unexpected=0 exit=0`;
both standalone exits 0 with 14 OK lines. Do not gate on `executes` (16 now, 17 pre-C1).

## Writes / tooling

No production file edited by this seat. Written: this report and
`.ufo/waves/round-28/receipts/ExecRecheckAuditR28.txt`. Scratch under `/tmp`
(`/tmp/r28-audit-probe-*`, `/tmp/r28-audit-dryrun-*`, `/tmp/r28-kexp40.txt`); nothing bulky committed
(QUALITY R14 wave-evidence economy). No tool installed or upgraded, so no tool/version/channel row applies.
