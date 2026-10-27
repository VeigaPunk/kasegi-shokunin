# RevCorrections — receipt (round 41, wave 1)

Seat: RevCorrections (reviewer, leaf). Item: review the I1 correction-block drafts against the verifier's
exact D1/D2 wording; deliverable is this receipt (per-requirement verdict). No lane files were edited; no
mutating git/jj run; no installs/upgrades; no network fetches.

## Review targets

1. `.ufo/waves/round-41/claims.json` (line 26, C1 predicate) — the authoritative I1 wording, reviewed
   first (fallback clause) and kept as the grading contract.
2. `ScribeCorrections.full-blocks.txt` — landed in wave1 during this seat; reviewed in full below.
   `ExecI1Blocks` had not landed a draft at receipt time; the same checklist was sent to it.

## Ground truth re-derived (commands + observed output)

1. D1 targets say "verified" — reads of the three records:
   - `SCORECARD.md` `## Round 40 result` C1 row: `| depth:verifiability | 4 | **4 (held; verified)** | ... At Y d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5: closed=10/10 exit=0; graded --selftest cases=10 failures=0 exit 0; ... Receipt .ufo/waves/round-40/final-gates/all-gates.txt at Y is the teed transcript ...`.
   - `LOG.md` L1728: `- C1 (depth:verifiability, 4 held, verified): ... at Y d0fe34d3... closed=10/10 exit=0, graded selftest cases=10 failures=0 ... receipt = teed transcript (time-basis=ref-commit).`
   - `SHONEN.md` L219 (`Correction (round 40)` line under Box 3): `... the final round-40 receipt values are recorded in .ufo/waves/round-40/final-gates/all-gates.txt at Y d0fe34d3...: closed=10/10 exit=0, graded selftest cases=10 failures=0, suite sha256 bdbd18a3..., time-basis=ref-commit, run-utc=2026-10-26T22:32:37Z. ...`
2. Final r40 receipt truth — `cat .ufo/waves/round-40/final-gates/all-gates.txt` (16 lines, `all-gates v4`):
   `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd` (J7), `suite-sha256=bdbd18a3...`,
   `time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`, H1–H10 each `closed=1`,
   last line `closed=10/10 exit=0`. `grep -n "selftest" .ufo/waves/round-40/final-gates/all-gates.txt | wc -l` -> `0` — the receipt carries NO selftest line, so D2's "SHONEN.md L219 says the receipt 'records' the selftest values, but it does not" re-derives exactly.
3. Receipt digest — `sha256sum .ufo/waves/round-40/final-gates/all-gates.txt` ->
   `7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b`.
4. D2's lane criterion — `corpus/QUALITY.md` L323 (R37): a record quoting a run result carries a committed transcript or says `report-only`; a receipt is only the unedited tee of one observed run.
5. Firing evidence files exist at the D1 paths — `ls -la` on
   `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` (7,978 B),
   `.ufo/waves/round-40/wave2/CritKillRule.md` (12,042 B),
   `.ufo/waves/round-40/wave2/CritKillRule.h6-escapes.sh` (4,377 B, executable),
   `.ufo/waves/round-40/wave2/MutH6H10.md` (15,615 B). `MutH6H10.md` L132: `## Defect D2 (H8 survivor): the negative-control acceptance predicate is unkillable, and pristine H8 already accepts a leaf-capped green base`.
6. Pre-landing state — `grep -rn "Correction (round 41)" SCORECARD.md LOG.md SHONEN.md | wc -l` -> `0`.

## Per-requirement verdict — claims.json I1 wording (fallback review)

1. NOT-verified grade — PASS. I1 requires lines that "grade round-40 C1 NOT verified on the frozen
   counter": the exact grade D1 demands, stronger than the `4 (held; verified)` overclaim it repairs.
2. Firing evidence with paths — PASS WITH CAVEAT. Tokens `RevC1Counters.defeats.txt`, `CritKillRule.md`,
   `MutH6H10.md` are named and all exist (item 5 above). Caveat carried to drafters: D1's sharpest
   clause fires on `CritKillRule.h6-escapes.sh`; name it alongside `CritKillRule.md`.
3. Receipt truth named — GAP IN I1 WORDING (draft-side must). The wording does not itself compel the
   receipt values; the blocks must state them or the correction overcorrects.
4. D2 gap + r41 closure — GAP IN I1 WORDING (draft-side must); I2 is the r41 closure (receipt at Y tees
   BOTH the suite run and the graded selftest, `time-basis=ref-commit`).
5. Plain prose / line-anchored / no fences / <=5 lines — CONSISTENT (draft-side discipline; I4 backs the
   fence limb).
6. Exactly 3 records + evidence tokens — PASS. `SCORECARD.md`, `LOG.md`, `SHONEN.md`; tokens required.

## Per-requirement verdict — ScribeCorrections.full-blocks.txt (draft review)

Review chain (the peer iterated mid-wave under L1 direction; each snapshot re-verified):
`4784 B / 44a3bc80...` (peer draft, never landed) -> `5087 B / 2aeffe50cf7c...` (first landed
snapshot; full six-requirement PASS recorded below) -> `4949 B / 53af656b82aa...` (current; L1
CORRECTIONS-L1.md item 2 alignment: "eight committed escape states F1–F8"). Verdict below is re-pointed
at the current snapshot; the chain is recorded so no stale digest is cited as current.

Current byte checks (run in scratch S): `sha256sum` -> `53af656b82aa0d47ad0c4b55e50fd6e70d81690ee09e5eaffc3f4bfb6203c886`;
`stat -c %s` -> `4949` B; `wc -l` -> `12`; `grep -c '^Correction (round 41):'` -> `10` content lines, all
anchored at column 0; `grep -c '^```'` -> `0` fences; `awk` block split -> `4/3/3` lines per block;
`grep -in 'seven'` -> zero occurrences; `grep -c 'eight committed escape states F1–F8'` -> `3` (one per
block); `awk` per-block token scan -> every block carries `RevC1Counters.defeats.txt`,
`CritKillRule.md`, `MutH6H10.md` and the phrase `NOT verified`; `awk` per-block limb scan -> every block
has exactly one receipt-truth line (digest `7f55d540...` + `closed=10/10 exit=0`), one D2-gap line
(no `selftest` line / report-only) and one I2-closure line.

Eight-state grounding: `grep -c '^### F' .ufo/waves/round-40/wave2/CritKillRule.md` -> `8`
(F1 L41, F2 L58, F3 L80, F4 L94, F5 L107, F6 L127, F7 L142, F8 L152), so "eight committed escape
states F1–F8" matches the committed headings; the file's intro prose "7 distinct escape states
reproduced" (L9) is the stale literal, superseded by the authoritative L1 freeze note
`.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` item 2 (committed headings authoritative; I11 payload
`escapes=8 red=8`). The blocks' parenthetical "(L1 freeze correction 2)" cites that note accurately.

1. NOT-verified grade — PASS (all 3 blocks; unchanged from first snapshot).
2. Firing evidence with paths — PASS (all 3 blocks, tokens intact; escape-state phrase now reads
   "eight committed escape states F1–F8" — accurate against the committed headings, per grounding above).
3. Receipt truth named — PASS (every block: Y `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5`,
   `.ufo/waves/round-40/final-gates/all-gates.txt`, digest `7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b` matching the live file, `closed=10/10 exit=0`, H1–H10 `closed=1`, `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd` (J7), `time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`, no `selftest` line, plus the "green suite run is not claim admission" calibration).
4. D2 gap + r41 closure — PASS (each block: Y receipt holds no `selftest` line; only committed graded
   tally is scratch Y′ `wave2/RevC1Counters.md` R7, report-only; I2 tees BOTH transcripts at Y with
   `time-basis=ref-commit` and `run-utc` = the ref's committer instant).
5. Plain prose, line-anchored, no fences, <=5 lines — PASS (10 column-0 lines, zero fences, blocks 4/3/3).
6. Exactly 3 records + evidence tokens — PASS (blocks map 1:1 to SCORECARD.md, LOG.md, SHONEN.md;
   per-block token scan confirms all three evidence tokens in every block).

Minor notes (non-blocking, unchanged from first review): (a) the SHONEN block's phrase "also quoted by
the round-40 correction above" reads correctly only when the block is appended after SHONEN.md L219 —
true for a tail append, the L1's landing pattern; (b) the parenthetical "(L1 freeze correction 2)"
references a wave artifact (CORRECTIONS-L1.md) that is a committed lane file under `.ufo/`, so the
reference resolves; acceptable provenance garnish, not a limb defect.

## Per-requirement verdict — ExecI1Blocks.blocks.txt (draft review)

Review chain (the peer iterated twice under review + L1 alignment; each snapshot re-verified):
`34654ec5...` (first landed; six-requirement PASS recorded below) -> `9a92113601cadc1e5...` (current;
two changes: (a) the competing "7 distinct escape states reproduced" numeral dropped — disclosure kept
as "the file's own intro prose counts them differently" citing CORRECTIONS-L1.md — so zero seven-count
literals remain while the contradiction stays on record; (b) the byte-accuracy gaps its earlier message
overstated are now actually closed: receipt sha256 `7f55d540...` + "16 lines", "H1–H10 all `closed=1`",
and the R7 pointer `.ufo/waves/round-40/wave2/RevC1Counters.md` all present in every block).
Verdict below is re-pointed at the current snapshot.

Current byte checks (run in scratch S): `sha256sum` -> `9a92113601cadc1e5ac35ecc9b1339d133befffaabde07a7a07abc9a03e68f89`;
`stat -c %s` -> `6385` B; `wc -l` -> `11`; `grep -c '^## BLOCK'` -> `3` organizational headings (L1
strips these when landing, landing only the three `Correction (round 41):` lines); `grep -c '^```'` ->
`0` fences; each block is one physical column-0 line; `grep -in 'seven|7 distinct'` -> zero hits;
`grep -c 'F1–F8'` -> `3`; per-line limb scan (`awk` over the three `Correction` lines) -> every line:
defeats=1, `CritKillRule.md`=1, `CritKillRule.h6-escapes.sh`=1, `MutH6H10.md`=1, R7 pointer=1,
sha256=1, NOT-verified=1, report-only=1, I2=1.

1. NOT-verified grade — PASS. SCORECARD line: "round-40 C1 is NOT verified on the frozen counter and its
   claim admission is withdrawn"; LOG line: "on the frozen counter round-40 C1 is not verified — NOT
   verified"; SHONEN line: re-grades box 3, "box 3 stays `[~]`, not independently verified".
2. Firing evidence with paths — PASS. All three tokens on every line, with full
   `.ufo/waves/round-40/wave2/` paths and accurate one-clause case labels (T2 substring-value, T4
   fenced pseudo-row, T7 symlinked declaration, T13 mention-only row, T14 case/separator escape);
   F1–F8 wording matches the committed headings per the grounding above and cites CORRECTIONS-L1.md.
3. Receipt truth named — PASS. Every line names the path, Y40 `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5`,
   the blob sha256 `7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b`, "16 lines",
   `closed=10/10 exit=0`, H1–H10 all `closed=1`, `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd`,
   `time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`, and "that receipt carries no `selftest`
   line". (The earlier message-overstates-bytes note is resolved: the bytes now carry what the message
   claimed.)
4. D2 gap + r41 closure — PASS. Every line: no `selftest` line in the receipt; the only committed graded
   tally is scratch Y′ with its R7 pointer `.ufo/waves/round-40/wave2/RevC1Counters.md`, marked
   report-only and withdrawn as evidence (D2's own fix ask); "round 41 re-derives the closure with
   `corpus/instruments/r41-closure.sh` (I1–I12) and tees both the run transcript and the graded
   selftest into the round-41 receipt (I2)".
5. Plain prose, line-anchored, no fences, <=5 lines — PASS. Three single physical lines, column 0,
   zero fences, zero seven-count literals, 1 line per block (<=5). Same note as above: the `## BLOCK`
   headings are organizers, not landable bytes.
6. Exactly 3 records + evidence tokens — PASS. Blocks map 1:1 to SCORECARD.md, LOG.md, SHONEN.md with
   all three tokens in every line.

Ruling on the peer's open question from the first snapshot (kept vs hard-coded "eight"): RESOLVED by the
peer's second edit in the direction I ruled — the disclosure is kept, the competing numeral is dropped.
The current phrasing "eight committed headings; the file's own intro prose counts them differently, and
the round-41 freeze correction CORRECTIONS-L1.md makes the committed headings authoritative" is the best
of both: zero seven-count literals, full contradiction disclosure, authority attribution intact.

## Findings

- No blocking defect in the claims.json I1 wording (requirements 1, 2, 5, 6 PASS; 3 and 4 are wording
  gaps the drafts must cover — both covered by both drafts).
- `ScribeCorrections.full-blocks.txt` PASSES all six seat requirements at the current snapshot
  (`53af656b...`, 4949 B); landable as-is. First-landed snapshot (`2aeffe50...`) also passed; the
  delta between them was the L1-mandated F1–F8 alignment, which I independently grounded
  (`^### F` count = 8 in the committed `CritKillRule.md`).
- `ExecI1Blocks.blocks.txt` PASSES all six seat requirements at the current snapshot
  (`9a92113601cadc1e5...`, 6385 B); landable as-is once the L1 strips the `## BLOCK` organizers and
  lands only the three `Correction (round 41):` lines. Both drafts are conforming; the L1 may choose
  either (or merge), subject to the strip note.
- Open item raised by ExecI1Blocks — "claims.json still says seven" — re-checked against the live file
  and already handled: `.ufo/waves/round-41/claims.json` carries the L1's appended `correction`
  annotations at line 72 (base hash: 38-char `5b29ea1439450b712581edf5f0bf98dfb262ab` corrected to the
  40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab`; the stale form survives only inside the
  annotation's quote, working literals use the 40-char form, 5 occurrences) and line 78 (I11: "claims.json
  says 'the seven committed CritKillRule escape states' but the committed wave2/CritKillRule.md carries
  EIGHT '### F' headings (F1-F8; its own intro prose says 7). I11's target is the eight committed states;
  I11 payload must read escapes=8 and red=8, naming F1-F8."). The three remaining "seven" literals live
  in the frozen predicate/kill_rule text (lines 26–27) plus the line-78 quote — superseded, not live
  spec. Instrument builders must read the annotations (CORRECTIONS-L1.md states the same); this matches
  the peer's conclusion, no further seat action.

## Hygiene

- Scratch: `/fast/scratch/hyaku/kasegi-r41/RevCorrections` created with `mkdir -p`, bound as cwd for all
  verification commands; removed before yield. No scratch under 50 MB touched /tmp.
- Writes: this receipt only. No lane/fleet/source-tree file edited; no MANIFEST/templates/scripts/
  .ufo/state writes; read-only git only (none needed beyond `cat`/`grep`/`ls`/`sha256sum`/`stat`).
- Tools: no installs/upgrades this seat; disk guard not needed (no heavy pass; /fast at 25%).
- Receipt path: `.ufo/waves/round-41/wave1/RevCorrections.md` (this file). No byte-exact landable
  deliverable is named by this item beyond the receipt.
