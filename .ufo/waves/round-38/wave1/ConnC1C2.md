# ConnC1C2 — C1×C2 interdependence trace and integration order (round 38)

Seat: ConnC1C2 (connector, leaf; no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Lane head at work:
`700153593eb586c70a6499c8ca225ee4d673bc9b` (base `a173b0c2…` and claims freeze `9a10b02f…` are
its ancestors — verified). Item: trace interdependence between C1 (depth:verifiability) and C2
(coverage) and define the integration order; receipt only. No lane file was written by this seat
except this receipt; all composition was done on `git archive` exports and scratch copies.

## 1. Files both claims touch (wave-1 draft map)

| file | C1 bytes | C2 bytes | author seat | nature |
|---|---|---|---|---|
| `corpus/README.md` | G1 limb: correction line + fence closed at EOF + declared suffix | F21 row + admission block | ScribeFrontierBlocks.readme-eof.md (C2) | **one joint append** — the 32-line EOF block closes the L426 fence (line 1), names L399-L454 as misplaced (correction line), and carries the F21 table + count paragraph. C1's G1 consumes exactly this block; `declared-blocks.txt` binds it. There is no separate C1 append. |
| `PROVINCE.md` | G1 limb: correction line (L79-L152) | F21 amendment | ScribeFrontierBlocks.province-eof.md (C2) | **one joint append** (4 lines: blank, correction, blank, r38 F21 frontier sentence). Adds no fence line; PROVINCE stays fence-closed. |
| `SCORECARD.md` | correction line (f3246559) + `## Round 38 result` section | none (coverage row inside the section is C1 scribe recording C2 outcomes) | ScribeScorecard.* (C1) | C1-only edit; the section must name J only by reference (G2/G5). |
| `LOG.md` | C1 bullet | C2 bullet | ScribeLOG.block.md | one joint entry, one append; no per-claim conflict. |
| `SHONEN.md` | G2: round-38 lines name J only by reference | none | **no wave-1 draft exists** — integration must add the round-38 lines (ScribeScorecard §5 defers them; ExecRefChecker scopes G2 to `round[- ]38` lines) | C1-gated; open responsibility. |
| `corpus/lessons/round-37.md` | G3 pending-marker resolutions section | none | ScribePendingResolutions.block.md (C1) | C1-only. |
| `corpus/lessons/round-38.md` | Mistakes section (C1) | (assimilation record) | ScribeMistakes / ScribeAssimilation / ScribeConsiderthese / others | shared lesson file, disjoint sections; kill rule forbids `⟨pending` in it. |
| `corpus/knowledge/considerthese-proposals-ledger.md` | G7 filled section | none | ScribeConsiderthese.block.md → G7 fill | C1-only; must not gain a `^source: S055` line (C2 counter 3) — verified 0. |
| `corpus/QUALITY.md` | R32/R33 | none | ScribeQualityRows.block.md | C1-side; append is the round's largest undeclared markdown append (recommended to declare). |
| `SKILL.md` | r38-closure.sh registry row | none | ScribeSkillRegistry.row.md | C1-side (density guard). |
| `corpus/SOURCES.md`, `corpus/knowledge/csaf-vex-product-status-and-justifications.md`, `corpus/source-snapshots/round-38/{S055.txt,manifest.json}` | none | S055 row, entry, capture/manifest | C2 seats | C2-only. |
| `.ufo/waves/round-38/declared-blocks.txt` | G1 declaration file | none | ExecDeclaredBlocks.gen.sh | C1-only; suffix-anchored, `tail -n <lines> | sha256sum` == declared digest, optional `# base` guards. |

## 2. Evidence (commands actually run, outputs)

Scratch `S=/fast/scratch/hyaku/kasegi-r38/ConnC1C2`; mirror = `git -C <lane> archive HEAD PROVINCE.md corpus SCORECARD.md SHONEN.md LOG.md SKILL.md | tar -x -C $S/mirror`.

- Lane state: `git rev-parse HEAD` → `70015359…`; `merge-base --is-ancestor a173b0c2 HEAD` and `… 9a10b02f HEAD` both exit 0; porcelain: only `?? .ufo/waves/round-38/wave1{,.ready,.ready.dispatched}/`.
- Base: `PROVINCE.md` 152 lines / `corpus/README.md` 454 lines; knowledge files 49; registry rows 54; frontier rows 20; expected list 49 entries.
- Fence walks (ExecFenceWalk.sh): base `PROVINCE.md` → `closed`, `corpus/README.md` → `open` (L426 opener). After appending the two C2 blocks → `closed` / `closed`. Trace of composed README L454-478: L454-455 `code` (the L426 fence closes on the block's first line), L456+ `text` — the F21 row is **outside** the fence.
- Frontier/self after compose: `grep -cE '^\| F[0-9]+ \|'` → `21`; `^\| F21 \|` → `1`; `21/21 admitted` → `1`; corrections: README names `L399-L454` (1) + `misplaced` (1); PROVINCE names `L79-L152` (1) + `misplaced` (1).
- Declared-blocks (ExecDeclaredBlocks.gen.sh, run from compose root):
  `gen corpus/README.md <readme-eof>` → `corpus/README.md 32 f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff` (pre_lines=454, post_lines=486, tail_view=exact); `gen PROVINCE.md <province-eof>` → `PROVINCE.md 4 797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf` (pre_lines=152, post_lines=156). Both match the scribe draft byte-for-byte. `check` → `declared=2 ok=2 fail=0 base=0 exit=0`; with `# base` guards → `base=2 exit=0`; one stray line appended after the README block → `FAIL corpus/README.md … fail=1 exit=1`.
- Full C2 compose (no C1 artifacts): frontier 21; registry 55; S055 rows 1; knowledge 50; expected 50. Harness: `entries=24 pass=24 exit=0` incl. `PASS F21 … ids=S055 exit=0`. Census: `census_rc=0`, only `W04 S028`/`W04 S029`. Capture-binding: `records=45 bound=45 unbound=0` (base control: `44/44`; `multi_row_url=2` and orphan `S040-live.txt` are pre-existing at base). Audit: `expect=present expected=50 missing=0 unexpected=0` (entry's `source:` line is the only `^source: S055` in knowledge).
- Composed SCORECARD (correction + section appended): G5/A `Final lane commit:` lines in the round-38 section → `0`; G5/B `^Correction (round 38)` → `1` naming `f3246559`; G2/D forbidden labeled-hash regex `(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}` in section → `0` hits; G2/C `judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt` present.
- Append-only: diff base→compose over the 10 protected files → deletions 0 everywhere (PROVINCE +4, SOURCES +1, README +32, others +0). G3 widened-vocabulary sweep: 0 hits in every drafted deliverable block (14 files) and 0 hits in added lines of the protected-file deltas.

## 3. Integration order (required chain)

1. **Freeze C2 facts first**: capture `corpus/source-snapshots/round-38/S055.txt` (sha256 `63c8ad52…`) + `manifest.json`; entry `knowledge/csaf-vex-product-status-and-justifications.md`; registry row inserted **after the S054 row** (not EOF — census `E12`). The row alone without the entry makes census red `E11`; land row + entry + capture + manifest in the same content window.
2. **Land the two front-door EOF blocks last on `corpus/README.md` and `PROVINCE.md`** — one append per file (the C2 blocks, containing both claims' bytes: fence closure, correction lines, F21 admission). Nothing may append to either file afterward: the declared-block suffix (and `# base` guards, if used) reds, and the correction line's L399/L426/L454 references go stale.
3. **Generate `.ufo/waves/round-38/declared-blocks.txt` after step 2** from the final frozen blocks (gen measures, never predicts), optionally with `# base corpus/README.md 454` / `# base PROVINCE.md 152`. Build `r38-closure.sh` + fixtures against this declared contract and ExecRefChecker semantics; `--selftest` must reject mutants.
4. **Land the remaining C1 edits** (scorecard correction+section; lesson pending-resolutions; ledger G7 fill; QUALITY R32/R33; SKILL row; LOG entry; SHONEN round-38 lines by reference). All appends; no in-place edits.
5. **Commit the integration tree as J** — every round-38 change except the gate receipt; include `wave1-results.json` (G4: tracked sibling results with equal seat count) in J, before the report.
6. **Gate at J on a clean lane** (G6 scratch quiescent, no untracked wave files): `r38-closure.sh --export-ref J` → `closed=8/8 exit=0`; `--selftest --export-ref J` → `cases=8 failures=0`; base `a173b0c2` and r37 judged head `2387dcf6` exports red; carry-over `r37-closure.sh --export-ref REF` → `closed=14/14 exit=0` (r37 E9 reads the **live** worktree — a dirty tree reds it, verified by ExecBaseRed).
7. **Write all-gates v2 receipt; commit Y = J + receipt only**. Report names J and Y; lane files (SCORECARD/SHONEN) name J only by reference — the drafted section already does.

Why this satisfies the three stated invariants:

- **G1 declared-blocks equality holds**: the declaration is generated after the final EOF block is composed (step 3 after step 2); the suffix assertion then matches, and step 2's "no further appends" keeps it true at the gate.
- **README F21 row insertion does not break the EOF block**: the row is **not** inserted into the head frontier table (which keeps 20 rows and its line numbers); it lives inside the new EOF admission block, after the fence is closed, so it is normal text, the corrections' line refs hold, and the suffix declaration is unaffected.
- **C2 counters unaffected by C1 edits**: the only input file C2 counters share with C1's edit set is `corpus/README.md`, and C1 contributes nothing to it beyond the byte-identical joint block (counter 1 measured 21 on the compose); every other C2 counter reads C2-only files (SOURCES.md, knowledge entry is snapshots, knowledge-expected.txt, instruments). C1's edits to SCORECARD/SHONEN/LOG/lessons/ledger/SKILL/QUALITY/declared-blocks/all-gates are read by none of the nine C2 counting commands. Verified by running all nine counters on a compose containing zero C1 artifacts: all green.

## 4. Causal separability

- **C2 verifiable with C1 reverted: yes.** The full C2 compose (no C1 bytes anywhere) passes all nine C2 counters — harness 24/24, census exit 0, binding 45/45, audit expected=50, frontier 21, registry 55, knowledge 50.
- **C1 verifiable with C2 reverted: no — G1 depends on C2-authored bytes.** The correction lines, fence closure and the declared suffixes physically live inside C2's front-door blocks; with C2 reverted, G1 reds (no correction lines, README open-at-EOF, no declared block). The dependency is one-directional and contained to `README.md`/`PROVINCE.md`; G2/G3/G4/G5/G6/G7/G8 are C1-internal (G4/G6 also touch wave mechanics).

## 5. Second-order effects and risks

- Declared-blocks staleness: any post-declaration edit to either front-door file voids G1 (mutant proven). Two the correction line inside C2's block as the *single* D-A marker; do not add a second correction block.
- Census `E11`: S055 row ↔ entry must land together; row-first is red.
- Harness F21 `recheck:` executes `cd <lane> && …` (committed convention): run the harness in the real lane after the manifest lands, else F21 exits 2 and the harness prints `pass=23` (reproduced on mirror; root-relative variant passes).
- G8/r37 E9 reads the live worktree: gate run requires a clean, fully committed lane (also satisfies the "working tree clean at filing" kill rule).
- SHONEN round-38 lines have no wave-1 draft owner; integration must produce them in the reference-only form (G2 carrier scope: `round[- ]38` lines; historical r37 lines out of scope per ExecRefChecker).
- QUALITY R32/R33 append is outside G1's declared set; declaring it (14 lines) is recommended and measured green.
- Sibling ruling (deferred to this connector seat by `c2-controls/before.txt`): kake-shokunin's only CSAF mention (`corpus/knowledge/security-txt-publishing.md:63`, "securitytxt.org already lists one extension, `CSAF` (S079)") is a security.txt extension-field registry fact in kake's own domain — it states no CSAF product-status categories and no VEX justification flags, so it does not cover F21 and does not affect C2's coverage claim.

## 6. Scratch/tooling

All work under `S=/fast/scratch/hyaku/kasegi-r38/ConnC1C2` (`mkdir -p`); read-only git only (`archive/rev-parse/merge-base/status`); no tool install, no network fetch, no mutating git, no writes outside `$S` and this receipt. `S` removed with `rm -rf` before yield (verified absent).
