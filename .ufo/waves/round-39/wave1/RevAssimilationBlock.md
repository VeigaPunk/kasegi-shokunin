# RevAssimilationBlock — review of ExecAssimilationIds assimilation evidence (round 39)

Seat: `RevAssimilationBlock` (reviewer, leaf; no subagent dispatch). Axes: `depth:verifiability`.
Reviewed: `.ufo/waves/round-39/wave1/ExecAssimilationIds.{reg-ids,staged-ids,collisions,quarantine-slice,quarantine-verdicts.md}` + receipt `ExecAssimilationIds.md`. Frozen claims read first; nothing edited.

## Verdict: PASS — evidence is honest, protocol-shaped, and independently reproducible; adoption zero stands

Every checkable claim in the receipt and verdict table reproduced under my own commands (listed below with outputs). No blocking defect. Three minor notes for the L1, none requiring rework of the deliverables.

## 1. reg-ids / staged-ids / collisions — byte-identical to my independent derivation

I re-derived all three from the primary sources at base `480b1a505a2dfc14a4f718d16d63808247214d0a` (lane registry via `git show`, staged package read-only) with the frozen 0–3-space extractor before opening the peer's files:

```
reg-ids 55 (S001–S055), staged-ids 94 (S031–S124), collisions 25 (S031–S055)
my.collisions: S031 S032 ... S053 S054 S055
cd5ee2d942f27a618c6a7066e663c2012e914454c5b1eb4e218bbddb1a355df9  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
0875ecb42ce8beede45a9278071690029d86da04a687d0ad1b2e572f1fa203a1  collisions
```

`cmp` against the landed deliverables: **reg-ids, staged-ids, collisions all BYTE-IDENTICAL**. The exact frozen pattern `'^ {0,3}\|[[:space:]]*S[0-9]{3,}'` and a stricter trailing-`|` variant produce identical id sets (cmp clean), so the extractor transcription in receipt §2 is faithful. `staged-ids` digest equals the committed round-31 artifact `550a0129…` (I re-hashed `.ufo/waves/round-31/assimilation/*`: 47/94/17 lines, `ab66f54a…`/`550a0129…`/`ac78cd56…` as the receipt records) — the package did not move and the cross-round control is real.

## 2. Guard proof (indented-row fixture) — reproduced, load-bearing

My own fixture run: registry `| S001 | x |` + `  | S002 | y |` against staged `| S002 | y |`:

```
guard (0-3 spaces):  fixture collisions [S002] count=1
column-zero control: count=0
```

Same discriminating result as receipt §3 (nonempty under the guard, empty under `^\|`). I also re-checked the known blind spot: `grep -cE '^ {4,}\|[[:space:]]*S[0-9]'` on both real inputs → **0** in each, so 4+ space indented rows (which the extractor misses) do not exist in either input — the r38 honesty note still holds.

## 3. Quarantine slice — every line carries an S-id; extraction reproduces across rounds

Frozen awk re-run by me on the register → 7 lines, 417 B, sha256 `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862` — **byte-identical to the landed `ExecAssimilationIds.quarantine-slice`** and to the committed r30 artifact (I hashed `.ufo/waves/round-30/assimilation/quarantine-slice` → same digest; r37/r38 lessons record the same). 7/7 lines carry `S[0-9]{3}`. Register itself byte-stable: sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines / 83,621 B, exactly the r38-recorded values. Verdict table covers exactly the seven slice ids (S037 S048 S054 S065 S068 S069 S070; no extras).

## 4. Every slice verdict is supported by measured fetch evidence — re-measured all seven independently

Same mandated method (`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`), 2026-10-26T19:36–19:37Z:

| id | my measurement | peer's claim | agreement |
|---|---|---|---|
| S037 | 200, 24,131 B, sha `add55637…fa3737`; whole quote 0× (ws-normalized); `发布日期：`/`实施日期：` 0 line-hits; all tokens located (`标准状态：`, `现行`, `发布日期`, `2020-11-19`, `实施日期`, `2021-06-01`, `GB/T 30279-2020`) | 200/24,131 B, same sha; quote 0×; tokens located | payload byte-identical; **quote-defective supported** |
| S054 | 200, 513,648 B, sha `0150c9d1…2b88`; pdftotext 139 lines; full recorded quote 0×; trailing clause `の悪用が確認されたもの又は疑われるもの` exactly 1× (L42→L43) | same bytes/sha; 0× and 1× | payload byte-identical; **quote-defective supported** (definition elided without marker) |
| S048 | 404, 748 B, sha `95cd25d8…2436` | same, retry-deterministic | body byte-identical (also equals r36/r38 recorded failure); **unreachable supported** |
| S065 | HEAD 200, Content-Length 7,465,472, application/pdf | 200/7,465,472 B, sha `e33b0f67…` | size exact; row has no quote cell → **unverifiable, nothing credited — supported and honest** |
| S068 | 403, 465 B, `Access Denied`, sha `b77a05f8…` (≠ peer's `dd13cbcc…`/`1defe6a2…` at same 465 B) | 403/465 B, per-request `Reference #` id varies | my differing digest at identical size **confirms** the peer's per-request-digest explanation; **unreachable supported** |
| S069/S070 | 200, 0 B; sha equals `sha256sum /dev/null` = `e3b0c442…b855` | same; one measurement covers both (identical URL), not double-counted | **unreachable (0-byte payload) supported** under the pre-declared vocabulary |

The verdict vocabulary was fixed before payloads were read (stated at the top of the verdicts file) — correct protocol shape.

## 5. No fabrication-class claim without basis

Neither the table nor the receipt labels any row `fabrication`. Both `quote-defective` rows carry located splice evidence (S037: field concatenation with two added colons, quote 0× while every factual token occurs; S054: elided statutory parenthetical, trailing clause 1×). The receipt explicitly offers the stricter mapping (→ unreachable) with the same action: non-adoptable. S065's contradiction of the register's "could not be fetched" note is disclosed, not smoothed. The five rows whose register class cell reads "could not be fetched" are shown as candidate notes, re-measured live, not treated as verdicts.

## 6. Round-38 standing refusals carry — package byte-identical (full sha verified), flips still unmet

```
sha256(shokuknow/merge/kasegi/SOURCES.append.md)
  = 4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb   (100 lines, 89,718 B)
  = the r38-recorded digest 4fe049cb…73eb — byte-identical, refusals carry
package: 70 files, every mtime 2026-10-24 23:33:20 (find | uniq)
```

The three r38 verifier-sampled flip conditions re-measured by me, all still unmet: (1) `program-severity-ladders-and-reward-scales.md` lane `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6` vs staged `35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87` (50 lines, at `merge/kasegi/knowledge/corpus/knowledge/`) — no byte identity; (2) `grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt` → 0 (`newsType_21` → 1) — anchor still absent; (3) `grep -c sse.com.cn corpus/SOURCES.md` → 0 — S047 still unregistered. The registry's 9 `supersed` hits are historical bullet/row prose (round-35 search-log supersession note etc.), none a supersedes row for severity-ladders. So all seven round-35 refusal reasons stand and 0 of 7 flips is met — the receipt's "adopts nothing" conclusion is evidence-backed.

## 7. Receipt claims verified

Base blob `git show 480b1a5…:corpus/SOURCES.md` → 122 lines / 75,948 B / `88bcd8c6bfbdca2180a113a60f0c7c3869ace3fd331d8118b65a39cbbf29ae61` (exact match). Ancestry: base and claims-freeze are `merge-base --is-ancestor` of the receipt's measurement HEAD `d65d823e…` (both rc=0). Worktree registry rows now: 55, matching the base blob. Verdicts deliverable: 170 lines / 11,128 B / `28a721d30fdbc38139fa942bb68d11518d32532a951645331286081f2e290cfd` (exact match to receipt §6). No tools installed; no mutating git/jj command run by me.

## Findings (all minor, non-blocking)

1. **Verdict-class delta vs the round-38 lesson (flag for L1 prose, not a defect).** r38 recorded S065/S068/S069/S070 as "present-and-located (carried, round 37)" — an overcount that included rows with no quote cell. r39's stricter vocabulary reclassifies them (S065 `unverifiable`, S068 `unreachable` via edge denial, S069/S070 `unreachable` 0-byte) on fresh measurement; the delta is evidence-driven (register and package byte-stable; only live reachability moved). The round-39 lesson should note the reclassification so the two rounds read as a correction, not a contradiction.
2. **Register-class column is paraphrase.** The verdicts table shows `never checked` where the register cell literally reads "the cited source could not be fetched, so no quote was checked". The S065 evidence section discloses the contradiction explicitly, so honesty is preserved; exact-cell quoting would have been tighter.
3. **Anchor line numbers are method-relative.** My tag-strip of S037 (378 non-empty lines) locates the same cells at L297–L313 where the peer's 52-line normalization puts them at L14–L30. Same tokens, same verdict; the deliverable could state that anchors are relative to its own extraction.

## Residual risk and verification gaps

- S065: I corroborated size/type via HEAD (Content-Length exactly 7,465,472) but did not re-download 7.4 MB to check the peer's payload sha `e33b0f67…586d83`; the reachable-again fact and the no-quote-cell → unverifiable logic do not depend on that digest.
- S037/S054/S048/S068/S069 payloads: byte-level agreement between my fetches and the peer's within ~5 minutes; site-side drift after that is possible but the verdicts record payloads by digest, so any drift is detectable.
- G6 note: my own scratch `/fast/scratch/hyaku/kasegi-r39/RevAssimilationBlock` is removed immediately after this receipt is written; the seat's live evidence lives in this file.
