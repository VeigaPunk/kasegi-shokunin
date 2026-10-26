# ScribeFrontierBlocks — round-38 front-door blocks (README row + both end-of-file blocks)

Seat: scribe, round 38, wave 1. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, lane head at work
time `700153593eb586c70a6499c8ca225ee4d673bc9b` (base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`).
Nothing was committed, landed, or edited outside the three deliverable files, this receipt, and scratch.

## Deliverables (byte-exact, landable bytes only)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-38/wave1/ScribeFrontierBlocks.readme-row.md` | 1 | 1267 | `17743c05a1451d2cf5c505deb71a66f86c7131d0556638a4d5ba7245d0c8488f` |
| `.ufo/waves/round-38/wave1/ScribeFrontierBlocks.readme-eof.md` | 32 | 4041 | `f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff` |
| `.ufo/waves/round-38/wave1/ScribeFrontierBlocks.province-eof.md` | 4 | 900 | `797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf` |

Each file contains only the bytes that land — no tables, notes, or headings outside the landed text.

### Landing (one append per file)

```
cat .ufo/waves/round-38/wave1/ScribeFrontierBlocks.readme-eof.md >> corpus/README.md     # 454 -> 486 lines
cat .ufo/waves/round-38/wave1/ScribeFrontierBlocks.province-eof.md >> PROVINCE.md       # 152 -> 156 lines
```

`readme-row.md` is **not** a second append: it is byte-identical to line 23 of
`readme-eof.md` (verified with `cmp`, below) and is delivered separately because the item names it.
Appending it again would make the frontier 22 rows and trip the C2 kill rule. One append per file is
what the suffix-anchored declaration requires.

### `.ufo/waves/round-38/declared-blocks.txt` (measured, not predicted)

```
# base corpus/README.md 454
corpus/README.md 32 f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff
# base PROVINCE.md 152
PROVINCE.md 4 797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf
```

The two `# base` guards are optional and were verified to hold (file line counts 486 and 156). The two
declaration lines are the output of the wave-1 `ExecDeclaredBlocks.gen.sh` (see evidence 3).

## What the blocks contain

### `readme-eof.md` (32 lines, appended at README EOF)

| line | content |
|---|---|
| 1 | `` ``` `` — closes the fence opened at README L426 (README walked *open* at EOF before) |
| 2 | blank |
| 3 | `Correction (round 38): …` — one line naming `corpus/README.md L399-L454` as misplaced receipt scaffolding from `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md` (receipt property and validation tables, the "Validation on a scratch mirror" section with its check table, the stray fence at L426), the intended 27-line round-37 block and its sha256 `2ebd8cd2…`, the receipt §3 "Deliverable B — `corpus/README.md` end-of-file block" it came from, the lost `## Round-37 admission …` heading at L399 (only L400-L425 landed unchanged), and that the L426 fence is closed by this block |
| 4 | blank |
| 5 | `## Round-38 admission — coverage map row and Frontier F21 (appended 2026-10-26)` |
| 6 | blank |
| 7-15 | coverage-map note in the shape of the round-37 paragraph's intended text: R6, entry `knowledge/csaf-vex-product-status-and-justifications.md`, Frontier F21, source S055, source basis (CSAF 2.0 OASIS Standard document, not a summary page), capture `2026-10-26T18:25:51Z`, HTTP 200, 272441 bytes / 5146 lines, sha256 `63c8ad52…`, under `corpus/source-snapshots/round-38/` |
| 16 | blank |
| 17-19 | coverage-map row (`Area \| Entry \| Source basis`) naming the entry and `S055 — public primary, opened 2026-10-26` |
| 20 | blank |
| 21-23 | frontier table header, separator, and the **F21 row** (= `readme-row.md`) |
| 24 | blank |
| 25-31 | `[r38 amendment, appended 2026-10-26]` count paragraph: `**21/21 admitted**`, F01-F08 r23 … F20 r37, F21 r38, 0/18 sentence declared untouched |
| 32 | blank (the file's terminal blank line, as in the r37 intended block) |

The F21 row quotes the capture verbatim at `S055.txt:2135` (VEX purpose), `:2844` (the four
`product_status` categories of the mandatory test), `:2152` (impact statement as machine readable flag),
`:1762` ("reflect the VEX not affected justifications") and `:1767`
(`vulnerable_code_not_in_execute_path`), and keeps F21 distinct from CVSS severity, KEV status, EPSS
likelihood and SSVC decisions.

### `province-eof.md` (4 lines, appended at PROVINCE EOF)

| line | content |
|---|---|
| 1 | blank (paragraph break after L152's truncated receipt sentence; the r37 block also began with a blank line) |
| 2 | `Correction (round 38): …` — one line naming `PROVINCE.md L79-L152` as the round-37 append, the intended 2-line amendment at L79-L80 (blank + the r37 F20 line, sha256 `cdfe44e3…`), and misplaced receipt scaffolding at L81-L152 (duplicated F20 row, property tables, "Validation on a scratch mirror", stray fences), read as not part of the province |
| 3 | blank |
| 4 | `[r38 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F21 — OASIS CSAF v2.0 (Common Security Advisory Framework) VEX product-status categories and not-affected justification flags — admitted round 38; entry \`corpus/knowledge/csaf-vex-product-status-and-justifications.md\` (source S055)` |

The block adds no fence line, so PROVINCE keeps its measured state: fences L81 / L96 (` ```text `, content)
/ L124 walk **closed** at EOF both before and after the append.

## Evidence (commands run, observed output)

All scratch under `S=/fast/scratch/hyaku/kasegi-r38/ScribeFrontierBlocks` (`TMPDIR=$S`); the mirror is
`git -C <lane> archive HEAD PROVINCE.md corpus | tar -x -C $S/mirror`, blocks appended to the **export
copies only**. `git archive`, `rev-parse`, `diff --numstat`, `cat-file` were read-only; the one `git init`
fixture was `$S/nh` and `rev-parse --show-toplevel` printed `$S/nh` (evidence 7).

1. **Fence walks.** Before append: `ExecFenceWalk.sh corpus/README.md` → `open`,
   `ExecFenceWalk.sh PROVINCE.md` → `closed` (README L426 opener; PROVINCE L81 opens, L96 ```` ```text ````
   is content, L124 closes). After append on the mirror: `closed` / `closed`;
   `ExecFenceWalk.sh --selftest` → `selftest cases=10 failures=0`. The suite's simpler rule (a line
   matching `^ {0,3}` + three backticks opens when closed; only `^ {0,3}` + three backticks + spaces
   closes) was also run in Python over both mirror files → `README closed`, `PROVINCE closed`.

2. **Correction-line predicate (suite G1 wording).** On the mirror:
   `grep -E '^Correction \(round 38\)' corpus/README.md | grep -c 'L399-L454'` → `1`;
   `… | grep -cw misplaced` → `1`; `grep -E '^Correction \(round 38\)' PROVINCE.md | grep -c 'L79-L152'`
   → `1`; `… | grep -cw misplaced` → `1`.

3. **Declared blocks.** `bash .ufo/waves/round-38/wave1/ExecDeclaredBlocks.gen.sh gen corpus/README.md
   $S/ScribeFrontierBlocks.readme-eof.md` →

   ```
   corpus/README.md 32 f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff
   ExecDeclaredBlocks.gen.sh: target=corpus/README.md pre_lines=454 post_lines=486 block_bytes=4041 block_newlines=32 declared_lines=32 tail_view=exact
   ExecDeclaredBlocks.gen.sh: optional base guard: # base corpus/README.md 454
   ```

   and for `PROVINCE.md` → `PROVINCE.md 4 797666b9…` with `pre_lines=152 post_lines=156
   block_bytes=900 declared_lines=4 tail_view=exact`. `check` on the mirror →
   `declared=2 ok=2 fail=0 base=0 exit=0`; with the two `# base` guards added →
   `declared=2 ok=2 fail=0 base=2 exit=0`. Negative controls on the same declarations: `printf 'junk\n' >>
   mirror-mut1/corpus/README.md` → `declared=2 ok=1 fail=2 base=2 exit=1`; appending a lone ` ``` ` to
   `mirror-mut2/corpus/README.md` → fence walk `open`.

4. **Frontier counts on the mirror.** `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `21`;
   `grep -cE '^\| F21 \|'` → `1`; `grep -c 'frontier stands at \*\*21/21 admitted\*\*'` → `1`;
   `wc -l` → `486 corpus/README.md`, `156 PROVINCE.md`.

5. **Row identity.** `sed -n '23p' $S/ScribeFrontierBlocks.readme-eof.md | cmp - $S/ScribeFrontierBlocks.readme-row.md`
   → identical (both 1 line / 1267 bytes). Row cell count from pipe split: 6 cells (F20 shape).

6. **Append-only.** `diff orig mirror` → `0` deletion lines in each file (`32` and `4` addition lines).
   `ExecNoHarm.sh` on fixture commits of `$S/nh` (export of base `a173b0c2`, blocks appended, committed):
   `4 0 PROVINCE.md`, `32 0 corpus/README.md`, `numstat files=10 deletions=0 violations=0`,
   `PROVINCE.md base-lines=152 ref-lines=156 prefix=identical`,
   `corpus/README.md base-lines=454 ref-lines=486 prefix=identical`, `no-harm: OK`, exit `0`.

7. **Placeholder vocabulary (G3 limb on my added lines).** The `>` lines of both mirror diffs →
   `0` matches for `⟨pending|<fill>|filled by the L1|<LANE_HASH>|<r38-`, `0` word-bounded `TBD|TODO`. No
   trailing whitespace or tabs in any of the three files (`grep -nP '[ \t]+$|\t'` rc=1).

8. **Row quotes are verbatim in the capture.** Against
   `.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt` (5146 lines, sha256 `63c8ad52…`): each of the five
   quoted/summarised passages matches once, and `awk 'NR==2135|NR==2844|NR==2152|NR==1762|NR==1767'`
   contains the cited text (each `1`).

9. **Harness parses the row (entry not yet landed).** On the mirror,
   `python3 corpus/instruments/frontier-recheck-count.py --root $S/mirror` →
   `FAIL F21 knowledge/csaf-vex-product-status-and-justifications.md ids=- exit=- problems=missing-entry`,
   `entries=24 pass=23 exit=1`. That is the fail-closed row→entry binding working: the entry file is
   another seat's round-38 deliverable and is absent at lane head `70015359`. With it landed the row is
   the 24th admitted entry.

## Facts the correction lines assert (measured, not inferred)

- `git diff --numstat b56a4168… a173b0c2… -- PROVINCE.md corpus/README.md` → `74 0 PROVINCE.md`,
  `56 0 corpus/README.md`; `152-79+1 = 74` and `454-399+1 = 56`, so L79-L152 and L399-L454 are exactly
  the round-37 appends.
- Intended round-37 README block = receipt lines 68-94: `27` lines / `2947` bytes /
  `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` (matches the r37 receipt's own
  property table). PROVINCE block = receipt lines 50-51: `2` lines / `295` bytes / `cdfe44e3…`.
- `diff -u` of the intended README block against landed L399-L425 shows one delta — intended line 1
  (`## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)`) is a blank line in
  the file; `sed -n '2,27p'` of the intended block `cmp`s identical to L400-L425. L399 is exactly `\n`.
- Landed scaffolding, by line: L426 ` ``` `, L428-L434 F20 property table, L436 `## 4. Validation on a
  scratch mirror (append, not edit)`, L442-L451 check table, L438-L440/L453-L454 fixture prose.
- PROVINCE scaffolding, by line: L81 fence, L83-L88 F20 property table, L90-L94 the receipt's
  `## 3. Deliverable B` prose, L96-L124 the fenced README block (its own duplicated F20 row at L114),
  L126-L132 a second property table, L134-L152 the §4 validation section.
- S055 capture numbers in the README paragraph: `fetched_utc=2026-10-26T18:25:51Z`, `status=200`,
  `snapshot_bytes=272441`, `lines=5146`, `sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`,
  read from `.ufo/waves/round-38/wave1/ExecC2Capture.manifest.json` and re-hashed from the capture file.

## Touched surfaces

- Wrote: the three files above and this receipt, all under `.ufo/waves/round-38/wave1/`; scratch under
  `$S` (removed before yield).
- Read-only: the lane tree (`git archive`/`diff`/`rev-parse`/`sha256sum`), wave-1 sibling deliverables
  (`ExecFenceWalk.sh`, `ExecDeclaredBlocks.gen.sh`, `ExecNoHarm.sh`, `ExecC2Capture.S055.txt`,
  `ExecC2Capture.manifest.json`, `ScribeRowS055.row.md`), the round-37 receipt, and the round-37
  verifier spot-check.
- `git status --porcelain` at lane head shows only the untracked `.ufo/waves/round-38/` wave dir: no
  tracked file in the lane was modified by this seat.

## Out of scope (not done, by item bounds)

- Did not land either block, did not create `.ufo/waves/round-38/declared-blocks.txt`, did not touch
  `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/lessons/round-37.md`, the ledger, the knowledge entry, the capture, or any instrument.
- Did not run `corpus/instruments/r38-closure.sh` (not built yet) and did not run
  `source-recheck.py`/`capture-binding-check.py`/`recheck-audit.py`/census (C2 seats own those).
- Did not restore the missing `## Round-37 admission` heading: D-A's fix is an append-only named
  correction (R6), so the heading loss is named, not edited back in.
- No tool installed or upgraded (nothing needed); no `pacman` invocation; no host service touched.

## Findings and risks for the L1

1. **Do not append `readme-row.md` separately.** It already sits at line 23 of `readme-eof.md`; a second
   append yields 22 frontier rows and fails C2's `grep -cE '^\| F[0-9]+ \|' ... -> 21`.
2. **One append per file.** Both declarations are suffix-anchored: any round-38 append to
   `corpus/README.md` or `PROVINCE.md` after these blocks voids them (negative control 3 shows `fail=2`,
   exit 1).
3. **Both correction lines are single physical lines** (905 and 580 bytes) so the suite's
   line-scoped predicate (`^Correction (round 38)` containing `L399-L454` / `L79-L152` and
   `misplaced`) cannot be broken by wrapping. They are longer than surrounding prose but shorter than
   the existing F20 frontier row (1216 bytes).
4. **Ordering within README.** The correction line necessarily refers to line numbers that only hold
   once this block is the last append: L455 ` ``` `, L457 the correction, L459 the `## Round-38 admission`
   heading, L475-L477 the F21 table (header/separator/row), L479-L485 the count paragraph, L486 the
   terminal blank. If another file change shifts
   README's head, the L399/L426/L454 references in the correction prose go stale while the declarations
   still hold; nothing before L399 may be edited (append-only).
5. **Citation dependency.** The F21 row cites `S055.txt:2135/2844/2152/1762/1767`, correct for the
   capture whose sha256 is `63c8ad52…`; if the landed `corpus/source-snapshots/round-38/S055.txt`
   differs, both the citations and the README paragraph's byte counts/sha go stale. The capture and the
   entry are the C2 seats' deliverables, not this seat's.
6. **At lane head the recheck harness reports `problems=missing-entry` for F21** (evidence 9). That is
   expected until `corpus/knowledge/csaf-vex-product-status-and-justifications.md` lands; it is not a
   README defect.
