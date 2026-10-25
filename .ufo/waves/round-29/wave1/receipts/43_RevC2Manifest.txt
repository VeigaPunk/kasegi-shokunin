# RevC2Manifest — Q9 binding-table re-run on the round-29 manifest

Seat: RevC2Manifest (reviewer, leaf). Round: kasegi-shokunin 29, wave 1 (hyaku run 7).
Answering model actually run on: zai/glm-5.3-flash (config route; no model passed by hand).
Tooling installs: none (no install or upgrade was needed; nothing to record under bound 5).
LSP: no `lsp` device is mounted in this session, so caller/definition checks are not semantic-server-backed; every load-bearing claim below is a direct execution or byte measurement, not grep-as-proof.

## 1. Canonical bytes reviewed (frozen set, verified by me, not taken on trust)

| file | sha256 | bytes |
|---|---|---|
| corpus/source-snapshots/round-29/manifest.json | `910608e6bba69b32423a260332853e28f737affeaeb9011f6c9faef6702fb16a` | 3,857 |
| corpus/source-snapshots/round-29/S043.txt | `d3b815ed75e3e32b2ae363b9f612c3d25b9c8c585df2c4cd797296f2ded69199` | 7,298 |
| corpus/source-snapshots/round-29/S044.txt | `8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf` | 8,187 |
| corpus/source-snapshots/round-29/S045.txt | `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86` | 14,575 |
| corpus/instruments/source-recheck.py (instrument under test) | `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` | 291 lines |
| .ufo/waves/round-29/wave1/q9-binding-table.py (my table) | `b7d438ef95f911ec8749f000ec1eaf8fcf202661b61057ca650985dcc0d8a7a7` | — |
| .ufo/waves/round-29/wave1/q9-failure-state-probes.py (my probes) | `f0f3048ffe2cca646a16c79f826c9065c37674f336502e40c5b43cef8144cc76` | — |

Everything below is measured at this frozen set. ExecManifestC2 declared the freeze
(manifest `910608e6…`, S043 `d3b815ed…`, S044/S045 unchanged) after my freeze request; I
re-hashed all four files myself before running and re-hashed after the battery (no drift).

## 2. What Q9 binds and how this receipt judges it

QUALITY Q9: an assertion binds (a) record `path` stem == `id`; (b) the quote exactly-once
in the capture **or** a declared `anchor` the instrument verifies; (c) the check prints the
observed occurrence count. The item adds three failure states that must fail closed:
stem≠id, unanchored twice-quote, broken anchor. Fail-closed here means the binding table
exits nonzero and the row reads FAIL. The table (committed beside this receipt) prints
`raw=` and `norm=` counts per row (limb c) and mirrors `anchor_verdict()` from
source-recheck.py byte-for-byte in `anchor_note()`. `--require-exactly-once` implements the
frozen C2 kill-rule bar ("any manifest assertion not occurrences=1"), which is stricter
than Q9's anchor fallback — the distinction mattered mid-wave (§5 F1).

## 3. Binding table on the real manifest (canonical run)

```
S043:Q1 stem=ok sha=ok raw=1 norm=1 bind=once anchor=31-ok verdict=PASS
S043:Q2 stem=ok sha=ok raw=1 norm=1 bind=once anchor=40-ok verdict=PASS
S043:Q3 stem=ok sha=ok raw=1 norm=1 bind=once anchor=170-ok verdict=PASS
S043:Q4 stem=ok sha=ok raw=1 norm=1 bind=once anchor=92-ok verdict=PASS
S044:Q1 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
S044:Q2 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
S044:Q3 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
S044:Q4 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
S045:Q1 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
S045:Q2 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
S045:Q3 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
S045:Q4 stem=ok sha=ok raw=1 norm=1 bind=once verdict=PASS
q9-binding manifest=910608e6bba6 sources=3 assertions=12 exactly-once=12 anchored-ok=0 failed=0 exit=0
```
`--require-exactly-once`: identical — `exactly-once=12 failed=0 exit=0`.

Independent cross-checks I ran beside the table (not trusted from any other seat):
- All 3 stems == ids; all 3 capture sha256s match their manifest pins.
- raw count == norm count == 1 for all 12 assertions (exactly-once both ways, no anchor
  fallback needed anywhere).
- Each S043 anchor line (31/40/170/92) equals the actual line where the quote sits
  (computed from byte offsets, not from the anchor field): no vacuous anchors.
- S044 quotes sit at lines 10/11/33/34-38, matching their `location` strings.
- S045 `location` JSON-path documentation verified against the parsed capture:
  idor = `$.content[5].children[2]`, ai_application_security = `$.content[0]`,
  excessive_jwt_lifetime = `$.content[6].children[8]`, 36 top-level content entries —
  all match the manifest locations and the SOURCES.md row text.

## 4. Instrument runs at the frozen set (the C2 counter form)

```
--source S043: S043:sha256 OK; Q1 OK occurrences=1 anchor=31-ok; Q2 …=1 anchor=40-ok;
               Q3 …=1 anchor=170-ok; Q4 …=1 anchor=92-ok          exit=0
--source S044: sha OK; Q1–Q4 OK occurrences=1                     exit=0
--source S045: sha OK; Q1–Q4 OK occurrences=1                     exit=0
full manifest: 12× OK occurrences=1                               exit=0
```
Every assertion prints its occurrence count (Q9 limb c) — satisfied by the instrument at
digest `9fe6a4a0…`.

## 5. Failure states — probes and results

Probe runner: `q9-failure-state-probes.py` (`f0f3048f…`). Each probe copies the frozen
manifest + captures into a mktemp fixture and applies ONE mutation, re-pinning whatever
digest the mutation invalidates so only the limb under test differs. C0 is the unmutated
control. Canonical output (final tool bytes), verbatim key lines:

| case | mutation | instrument (source-recheck `9fe6a4a0…`) | table (`b7d438ef…`) |
|---|---|---|---|
| C0 control | none | exit 0, all occurrences=1 | exit 0, 12 PASS |
| P1 stem≠id | S044.path→`VRT-README.txt` (bytes identical) | **exit 0, clean OK lines — blind** (no stem rule exists in the instrument) | **exit 1**; S044:Q1–Q4 `verdict=FAIL stem!=id`, other 8 PASS |
| P2 unanchored twice-quote | S044:Q1 line duplicated, manifest sha256 re-pinned | **exit 0**, prints `S044:Q1 OK occurrences=2 anchor=MISSING` (visible, not fatal) | **exit 1**; only S044:Q1 `raw=2 norm=2 bind=unanchored-multi verdict=FAIL` |
| P3 broken anchor | S044:Q1.anchor 20 (quote on line 10) | **exit 0**, prints `S044:Q1 OK occurrences=1 anchor=20-BROKEN` | **exit 1**; only S044:Q1 `bind=anchor-broken verdict=FAIL` (fails even though the quote is exactly-once — a declared anchor the instrument disproves is a false pin claim) |

Runner summary line: `summary control_exit=0 p1_exit=1 p2_exit=1 p3_exit=1` → probes_exit=0
(all expectations met). Single-limb discrimination held in every probe: exactly the targeted
rows flipped, 11 or 8 of 12 stayed PASS (R11-style: each limb shown load-bearing).

The instrument-vs-table split is the honest posture, not a defect discovered new: the
instrument's docstring says anchor notes are "visible, not fatal", and Q9's stem conjunct
is the documented unlanded one. Measured consequence at `9fe6a4a0…`: **exit 0 from
source-recheck alone proves none of the three Q9 failure states**; only a binding table
(or future instrument limbs) closes them.

## 6. Findings by severity

**F1 · HIGH (process; resolved at the frozen bytes, recorded because it tripped a frozen kill-rule clause mid-wave).**
The manifest was declared "final" twice while bytes kept moving. Digest states I observed
on manifest.json in sequence: `3a0dec1b` (3,806 B) → `79b32d50` (announced final) →
`54a36f4f` (mid-rework) → `910608e6` (frozen after my request). Two measured intermediate
states, both PRE-STATE, neither comparable to any after column:
- At `79b32d50`: S043 was the full policy_versions API array (1,220,741 B, 1 line,
  sha `02ecb500…`); S043 Q1/Q2/Q4 measured **raw=12 norm=12 occurrences=12**, Q3 =1; all
  four carried `anchor=1`, which the instrument verified `-ok` **vacuously** — a 1-line
  capture makes the anchor window the whole file, so any in-range anchor "holds". The
  instrument exited 0. Under Q9's letter that manifest was legal (once-or-verified-anchor);
  under the frozen C2 kill rule it tripped "any manifest assertion not occurrences=1" as
  written. The occurrence counts (12/12) came from the same policy text recurring across 12
  of the 153 API records (record ids 3787452, 3783214, 3783116, 3782850, 3782849, 3781738,
  3781166, 3780809, 3780417, 3779541, 3779257, 3779255) — real cross-version duplication,
  not a capture bug.
- At `54a36f4f`: S043.txt had been rewritten but the manifest still pinned `02ecb500…`
  (all four S043 rows sha=MISMATCH) and anchors were stale (`anchor=1-BROKEN`).
Resolution: the frozen set replaces the array capture with the extracted record-3787452
policy text (7,298 B, 204 lines), re-anchors Q1–Q4 at 31/40/170/92, and every C2-bar
assertion is exactly-once (§3). The defect that remains is the discipline one: two "final"
announcements preceded the actual freeze, and consumers (me included) started counters
against moving bytes. For the lesson: a manifest seat should freeze digests first and
announce once; reviewer/counters seats should refuse unfrozen bytes (I re-ran rather than
publishing the mid-flight states as canonical).

**F2 · MEDIUM (instrument boundary, unchanged upstream — disclosure with digests).**
At instrument digest `9fe6a4a0…`: source-recheck.py has no stem==id rule (P1 passes it
clean) and anchor notes do not move the exit code (P2 `OK occurrences=2 anchor=MISSING`
exit 0; P3 `OK occurrences=1 anchor=20-BROKEN` exit 0). Consequence: any receipt that cites
only `recheck_exit=0` as evidence of Q9 binding is over-reading the exit code at this
digest. The fail-closed posture for the three failure states currently lives in the
committed binding table (`b7d438ef…`), not in the instrument. This is the Q9 "unlanded
conjunct" state as documented; no regression vs round-24/25 behavior is claimed or
measured here.

**F3 · LOW (my own table, caught and fixed inside this review).**
The first table bytes passed P3: a broken declared anchor on an exactly-once quote took the
`once` fast-path and the row PASSed (probe-matrix exit summary `p3_exit=0`). Fixed so a
declared-but-disproved anchor fails the row regardless of uniqueness; canonical battery
re-run at the fixed bytes `b7d438ef…`. Recorded because R11's point cuts both ways: the
probe matrix is what makes the table trustworthy, and the first table was lenient on
exactly the state the item names. The lenient bytes were never published as canonical.

**F4 · LOW-MEDIUM (adjacent surface, for the row owner — not edited by me).**
The landed SOURCES.md S043 row (line 49) and its changelog line (line 83) still describe
the capture as "policy_versions API array of 153 records; record id 3787452, timestamp
2026-10-16T15:34:59.854Z". The frozen capture at the pinned path is now the extracted
record-3787452 policy text (`d3b815ed…`, 7,298 B, 204 rendered lines) — no array, and the
row's L31/L40/L92/L170 section language matches the new capture while the "153 records"
and timestamp language describes bytes that no longer exist there. R8-adjacent: log the
anchor-cell old→new (append a changelog line; do not silently rewrite). The row's other
cells ("quotes Q1–Q4 pinned in the round-29 manifest", used-by the F13 entry) remain true.

## 7. Adjacent coherence measured (context only; counters not re-owned here)

- The F13 entry `corpus/knowledge/program-severity-ladders-and-reward-scales.md` exists; its
  `source:` line for S043 names In Scope L31, Out of Scope L40, reward L92, DoS L170 —
  exactly the frozen manifest's four anchors, all verified -ok (§3). S044/S045 `source:`
  line ranges (10–11, 33–38; metadata.default, content[5].children[2], content[0],
  content[6].children[8]) match my independent checks (§3).
- Frontier F13 row present at corpus/README.md:264 (`admitted`, sources S043, S044, S045);
  registry rows S043–S045 at corpus/SOURCES.md:49–51 (changelog 83–86). I did not re-run
  the C2 counters (census, harness, admission tallies) — those belong to the counter seats.

## 8. Residual risk and verification gaps

- No upstream re-fetch: the sha pins bind manifest↔capture bytes only. Whether
  hackerone.com / raw.githubusercontent.com still serve the captured bytes is unverified
  here (that is capture-source/source-recheck's declared boundary, and the 90d recheck
  cadence's job).
- The reviewed bytes are working-tree (uncommitted). If the commit that lands them differs
  by so much as a byte, this receipt's digests stop matching and the table must be re-run.
- The probe matrix exercises the three named states plus the control; the instrument's
  `anchor=OUT-OF-RANGE` variant and stem≠id on a *record whose id is valid but path
  absolute* are adjacent states I did not probe (the table fails both by inspection of its
  verdict matrix, but inspection is not a measurement).
- S043's evidence value rests on the extracted record: the capture is one policy version's
  text with no embedded fetch provenance (status/byte-count header is not part of the file);
  the manifest `location` strings are the only record-id/timestamp trace now. F4's erratum
  is where that trace belongs.
- Model note per bound 8: all verdicts above are tool-measured; the answering model
  (zai/glm-5.3-flash) authored prose and the two committed helper tools only.

## 9. Reproduction

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/source-snapshots/round-29/manifest.json corpus/source-snapshots/round-29/S04{3,4,5}.txt
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json
python3 .ufo/waves/round-29/wave1/q9-binding-table.py --manifest corpus/source-snapshots/round-29/manifest.json
python3 .ufo/waves/round-29/wave1/q9-binding-table.py --manifest corpus/source-snapshots/round-29/manifest.json --require-exactly-once
python3 .ufo/waves/round-29/wave1/q9-failure-state-probes.py   # mktemp fixtures; read-only over the lane
```
Expected: recheck exit 0 with 12× occurrences=1; table exit 0 (12 exactly-once) both modes;
probes `control_exit=0 p1_exit=1 p2_exit=1 p3_exit=1`.

## Postscript (same session, after §6 was written)

**F4 resolved by the row owner.** ExecManifestC2 appended the R8 old→new correction at
`corpus/SOURCES.md:83` ("…anchor originally described the raw `policy_versions` API array
(153 records…) → the final record-scoped capture … 204 lines; quote locations Q1–Q4 at
lines 31, 40, 170, 92…"), verified by me in the working tree. Manifest and capture digests
are unchanged (`910608e6…` / `d3b815ed…` / `8adfca61…` / `f583a396…`), so §3–§5 remain the
canonical runs; §6 F4 now records a closed defect, not an open one. F1's freeze-discipline
point and F2's instrument boundary stand as written.
