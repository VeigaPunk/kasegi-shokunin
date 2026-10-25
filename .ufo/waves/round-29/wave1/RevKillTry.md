# RevKillTry — round 29, wave 1 — cheap-side attacks on the C1/C2 kill rules

Seat: `RevKillTry` (reviewer, leaf). UTC window: 2026-10-25T18:2x–18:5xZ.
Assignment: attempt to satisfy the frozen C1 and C2 targets (`.ufo/waves/round-29/claims.json`,
frozen) **without doing the claimed work**, and confirm the frozen counters + kill rules
discriminate. Every attack was executed, not derived; every result below is a measured exit
code or grep over the bytes named. Tooling installed/upgraded: **none** (stdlib + committed
instruments only). Model route: not load-bearing for this item (all checks are local
instruments); no model was passed by hand.

## Lab, fidelity, and state labels

All attacks ran in a scratch lab under this wave: `.ufo/waves/round-29/wave1/killtry-lab/`
(172 KB after trim; receipts retained, corpus copies regenerable — see §Reproduction).
Lab = byte copies of the landed tree plus per-attack mutations; frozen counter *shapes* run
unchanged except `cd <lane>` points at the lab lane and the census is invoked as
`--root <lab-fleet> kasegi` against a `shokunin.conf` naming the lab lane.

Snapshot digests (pinned; `anchorcheck.py` was non-stationary early in my window — the M28-4
pattern — and had settled by battery time; every C1 run below is at this digest):

```
anchorcheck.py             68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97
frontier-recheck-count.py  c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261
source-recheck.py          9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96
README.md 67d94e80…, SOURCES.md fa54ba52…, manifest.json 910608e6…
```

**Fidelity proof (S0)**: before any mutation the lab reproduced the landed after-column —
frontier admitted 13, entries citing S04[3-5] = 1, S043–45 rows = 3, census validate exit 0
(W04 S028/S029 only), harness `entries=16 pass=16 exit=0`, per-id recheck exit 0 all
`occurrences=1` (`s0-base.txt`, re-confirmed after restores in `s0-prime.txt`). The C1 base
variant reproduced `selftest cases=12 failures=0 / limbs=9 covered=9 / nogit_exit=0`
(`c1-battery.txt`), matching the canonical receipt `c1-receipt-index.txt` (18:17Z).

**State label**: the C2 subject was already landed when I started (ExecCanonC2 AFTER at
18:22Z), so C2 counter runs above are at the landed bytes; C1 had just landed (canonical
receipt 18:16–18:17Z) and `anchorcheck.py` was mid-rewrite during my first reads — all C1
attacks are labelled **at the settled digest 68e1bdc6**, which is also the digest the
canonical receipt pins (verified matching at battery time).

One lab-fidelity disclosure: in the C2 lab, entries other than F13 execute their `recheck:`
lines with their own absolute `cd` into the **live lane**, so their PASS rows exercise live
bytes; F13's line was repointed at the lab lane (Q10 `cd <lane-root> &&` form preserved) and
is the row under test in every C2 attack.

## Findings by severity

### F1 · HIGH (C1) — a print-only selftest passes every frozen C1 condition, receipt clause included

Attack (`c1-printonly/`): `main()`'s `--selftest` branch replaced by two prints and
`return 0`; no fixture is built, no case runs, `_selftest` never invoked.

Measured (`c1-battery.txt`):

```
selftest cases=12 failures=0
limbs=9 covered=9
selftest_exit=0
grep: both lines match, grep_exit=0
nogit_exit=0
receipt clause: instrument_sha256 line of the print-only file itself → satisfied
```

All five kill conditions hold with **zero claimed work**. The receipt clause binds
*identity, not honesty*: it compares the receipt digest to the committed file's digest, and a
degenerate instrument in place at canon time records its own digest (direction-B demo in
`receipt-test.txt`: re-canonicalizing after a tamper also passes). The clause's real teeth are
post-canon tamper detection — direction A shows a one-line post-receipt edit fires the
mismatch (`receipt-test.txt`).

The executed mutation battery (`c1-controls/mutant-m1..m4.txt`) kills: removed limb case (m1),
missing limbs line (m2), skip-as-covered with git present (m3), GIT_* env leak (m4). It does
**not** contain a full print-only mutant. Discrimination against F1 currently rests entirely
on seat review (RevC1Instrument / CritC1Kill), not on anything frozen.

### F2 · HIGH (C1) — a duplicated fixture silently un-isolates a limb while every counter stays green

Attack (`c1-sharedfix/`): the `base-absent-origin` case's fixture replaced by the mirror
arm's fixture (`absent=('mirror',)`), and — to make the blind spot consequential — the origin
`BASE-ABSENT` classification disabled (`elif False and ORIGIN_ABSENT:`). This re-creates the
round-28 CritC1Kill gap ("ORIGIN BASE-ABSENT has no failing fixture") **invisibly**:

```
selftest cases=12 failures=0
limbs=9 covered=9        ← covered counts the case NAME executing, not the limb exercised
selftest_exit=0 ; nogit_exit=0
```

Control (`c1-deadlimb/`): the same classification break with the **real** fixture in place →
`selftest FAIL base-absent-origin: MISSING-FILE: want 0, got 1; BASE-ABSENT: want 1, got 0`,
`cases=12 failures=1`, `nogit_exit=1` — killed. So the isolating-fixture design (R13) works
*when the fixture is real*; the counters count `covered` by case name and cannot see which
arm a fixture exercises. m1–m4 contain no shared-fixture mutant either.

### F3 · HIGH (C2) — stem-swap forgery passes all seven frozen C2 conditions (M28-8, still open at kill-rule level)

Attack (S9, `s7-s9-quotegames.txt`): manifest record `id: "S043"` rewritten to
`path: "S044.txt"` + S044's sha256 + S044's quotes — i.e. "S043" now rechecks **Bugcrowd**
bytes while the registry row and entry still say S043 = HackerOne policy capture, and
`S043.txt` is referenced by no record at all.

```
c1 admitted=13 ; c2 entries=1 ; c3 rows=3 ; census_exit=0
c5 harness: PASS F13 … entries=16 pass=16 exit=0
c6 --source S043: S043:sha256 OK, Q1–Q4 all OK occurrences=1, recheck_exit=0
```

Nothing in the frozen chain compares `basename(path)` to the record id: no stem check in
`source-recheck.py` (verified by read: path validity, sha256, quote assertions only; zero
`splitext`/`stem` occurrences in it or in `frontier-recheck-count.py`), none in the harness,
none in the census, none in the kill-rule text. This is the executed end-to-end confirmation
of the gap CritC2Kill §1 derives from committed bytes ("Path-stem ≠ id … carried into round 29
unfixed"), routed as M28-8; the landed manifest itself has seat-level stem evidence only
(RevC2Manifest §binding-table: `stem=ok … verdict=PASS` per assertion — a receipt, not a
counter).

### F4 · HIGH (C2) — meter doctoring: a stub `source-recheck.py` passes counters 5+6 once any schema-valid manifest exists; no C2 instrument is digest-bound

Attack (S10b, `s10b-doctored-manifest.txt`): `source-recheck.py` replaced by a stub that
reads nothing and prints `occurrences=1` lines, exit 0 (`instrument-doctored.py`, kept in the
lab); real round-29 manifest + captures left in place.

```
c5 harness: PASS F13 … entries=16 pass=16 exit=0
c6: recheck_exit=0 for S043/S044/S045
```

The kill rule has an `instrument_sha256` clause binding **anchorcheck.py** (C1) but no
corresponding clause for either C2 instrument named in its own counter commands — the
asymmetry is the gap. **Positive finding**: the lazy variant (S10, stub + manifest deleted)
is killed by the harness itself — `problems=manifest-unreadable, entries=16 pass=15 exit=1`
(`s10-doctored.txt`) — because check B re-reads the manifest independently of the meter. So
the harness has real teeth; they bind *form*, not the meter's *identity* or honesty.

### F5 · MEDIUM (C2) — the coverage counter counts rows, not topics: a fabricated F13 title passes

Attack (S11, `s11-s12.txt`): F13's topic cell replaced with a fabricated one
("Intigriti reward table folklore"), evidence cells untouched → `admitted` count still 13,
harness 16/16, all frozen conditions pass. The awk counter reads the status cell only. A
coverage claim "F13 = program severity ladders admitted" is falsifiable only by a seat that
reads `corpus/README.md:264` (ScribeReadmeC2 / RevC2Entry class), not by anything frozen.

### F6 · MEDIUM (C2) — an unanchored twice-occurring quote passes both exit-code counters; only the kill rule's `occurrences=1` reading fires

Attack (S8, `s7-s9-quotegames.txt`): added assertion S044:Q5, quote
`vulnerability-rating-taxonomy` (occurs exactly 2× in the capture), no anchor:

```
S044:Q5 OK occurrences=2 anchor=MISSING
recheck_exit=0
c5 harness: entries=16 pass=16 exit=0
```

Both executable counters pass; the kill fails **only** because its text reads per-assertion
occurrence counts, not exit codes ("any manifest assertion not occurrences=1"). This is the
r28 M28-2 lesson still live: any after-column built from `recheck_exit` alone certifies this
forgery. The occurrences clause is load-bearing and was exercised — but it is a *reading
discipline*, not an instrument.

## Attacks the frozen rules killed (discrimination confirmed)

| # | Cheap route | Killed by (measured) |
|---|---|---|
| A1 | Sourceless rows: S043–45 registered + entry + F13 admitted, manifest+captures deleted (S1) | c5 `FAIL F13 problems=manifest-unreadable, pass=15 exit=1`; c6 `manifest UNAVAILABLE reason=missing` exit 2 (`s1-sourceless.txt`). Text counters 1–4 all pass first — they are the gameable layer by design; 5/6 are the teeth. |
| A2 | `recheck: true` (S2) | harness `not-a-recheck-invocation,no-source-selection,no-manifest`, pass=15 (`s2-s5-recheckforms.txt`) |
| A3 | Whole-manifest recheck, no `--source` (S3) | `no-source-selection`, pass=15 |
| A4 | `… source-recheck.py --selftest` as the recheck line (S4) | `not-a-recheck-invocation,no-source-selection,no-manifest`, pass=15 |
| A5 | Cross-entry credit: recheck points at round-28 manifest `--source S041` (S5) | `header-sources-not-rechecked`, pass=15 (R12 binding works) |
| A6 | Sub-floor quote `"P1 to P5"` (normalized 8 < 12) (S7) | `S044:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence` exit 2; harness `recheck-exit-2` (r24 forgery route still closed) |
| A7 | Duplicate S043 registry row to farm the row count (S12) | c3 counts 4 lines ≠ 3 → kill; census `E03 S043 duplicate id` exit 1 |
| A8 | Dead limb with real fixtures (control for F2) | `failures=1`, `nogit_exit=1` — the selftest's vector check kills a broken classification |
| A9 | Stub meter with no manifest (control for F4) | harness check B `manifest-unreadable`, pass=15 |
| A10 | Post-receipt instrument tamper (C1 receipt clause) | digest mismatch → clause fires (`receipt-test.txt` direction A) |

## What this means for the two claims

- **C2's execution layer is genuinely discriminating** against every no-capture and
  wrong-binding-form route tried (A1–A7, A9): rows, entries, frontier admissions, census
  shape, harness binding (A–D), and per-assertion occurrence reading together leave no
  *sourceless* path to the target. The open holes are *identity* holes: which bytes a record
  points at (F3), which meter verifies them (F4), and which topic a row claims (F5) — plus
  the known provenance boundary (§Residual risk).
- **C1's counters verify the selftest's *summary*, not its *work***: both degenerate
  implementations (F1 print-only, F2 shared fixture) print the exact frozen strings and pass,
  receipt clause included. The r28→r29 gap-closure claim ("every declared verdict limb has an
  isolating failing fixture") is enforced today by the selftest's own vector check — which is
  real and kills broken limbs (A8) — but nothing frozen verifies the fixtures are real,
  distinct, and per-arm.

## Recommendations (cheap, concrete)

1. Add two mutants to the C1 battery: **print-only selftest** (F1) and **shared-fixture limb**
   (F2); both currently survive instrument + frozen counters (m1–m4 do not cover them).
2. Extend the canonical receipt clause: `instrument_sha256` lines for
   `frontier-recheck-count.py` **and** `source-recheck.py` (and their digests re-checked at
   close), mirroring the anchorcheck clause — closes F4's identity gap for the cost of two
   hash lines.
3. Land the M28-8 fix in the instrument or the counter: fail (or gate) on
   `basename(path) != record id` — closes F3; concur with CritC2Kill's minimum corrections.
4. Keep the per-assertion `occurrences=1` reading in every after-column (F6): exit codes are
   demonstrably insufficient; a receipt that quotes only `recheck_exit` should be treated as
   PRE-STATE-grade evidence for Q9.

## Residual risk and verification gaps

- **Capture provenance is unfalsifiable locally.** A forger who fabricates *consistent*
  snapshot bytes (writes any `.txt`, quotes from it, pins its sha256) passes every frozen
  counter by construction — F3 is that forgery executed with reused bytes; fully fabricated
  bytes are strictly easier. The round's actual provenance rests on the ExecCapS043/44/45
  fetch receipts, the staged package, and reviewer seats — appropriate, but the kill rules
  should not be cited as covering it.
- **F5-class mislabeling of any other row** (titles, `next` prose, entry headers) is invisible
  to every counter; only census shape and harness bindings are frozen.
- My lab executed non-F13 entries against live-lane bytes (disclosed above); their PASS rows
  here re-verify form, not a second full recheck of rounds 24–28.
- `anchorcheck.py` was non-stationary early in the window (two re-reads showed 531→561-line
  generations); all C1 evidence here is at the settled 68e1bdc6, which the canonical receipt
  pins and which still matched the live file at battery time (re-verified in
  `receipt-test.txt`). Any later edit re-opens the receipt clause (it fires — direction A).
- Not re-run live: the C1 counters on the live lane (canonical receipt 18:17Z + my base-lab
  run at the same digest agree; no independent third run added).

## Reproduction

Everything regenerates from the lane bytes at the pinned digests: copy
`corpus/{README.md,SOURCES.md}`, the 16 F01–F13 entries,
`corpus/source-snapshots/round-*/manifest.json` (+ round-29 captures, round-28 S041/S042),
the three instruments; repoint the F13 entry's `cd` prefix at the copy; apply the per-attack
mutations kept in `killtry-lab/` (`c1-printonly/`, `c1-sharedfix/`, `c1-deadlimb/`,
`instrument-doctored.py`, `entry.base.md`, `manifest.base.json`); re-run the frozen counter
shapes. Receipts: `c1-battery.txt`, `s0-base.txt`, `s0-prime.txt`, `s1-sourceless.txt`,
`s2-s5-recheckforms.txt`, `s7-s9-quotegames.txt`, `s10-doctored.txt`,
`s10b-doctored-manifest.txt`, `s11-s12.txt`, `receipt-test.txt`.

## Assimilation cross-check (by-document, owed by the claims block)

Staged → adopted ids verified by document, not arithmetic: package
`shokuknow/merge/kasegi/SOURCES.append.md` S031/S032/S033 URLs byte-match lane rows
S043 (`https://hackerone.com/security/policy_versions`), S044 (`…/vulnerability-rating-taxonomy/master/README.md`),
S045 (`…/mappings/cwe/cwe.json`). Consistent with `staged_rows_adopted` in the frozen claims.
