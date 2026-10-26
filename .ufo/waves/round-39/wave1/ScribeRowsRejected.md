# ScribeRowsRejected — round-39 receipt

Seat: ScribeRowsRejected (scribe, leaf, no subagent dispatch). Round: kasegi-shokunin 39, claim C2 (coverage). Item: draft the three REJECTED SOURCES rows for S056 / S058 / S059 as byte-exact one-line deliverables plus the `## Registry changes` bullet lines. Read-only against the lane corpus: `corpus/SOURCES.md` is byte-unchanged (`git status --porcelain corpus/SOURCES.md` prints nothing). Tools installed or upgraded: none (python3, bash, git already present). Scratch `/fast/scratch/hyaku/kasegi-r39/ScribeRowsRejected` removed before yield. Disk guard green at start. All dates and times UTC, 2026-10-26.

## 0. Answer in one paragraph

The three rejected rows are delivered byte-exact (one line, NF=13, 11 cells, no `|` inside any cell) with `teaches` cells byte-identical to the three mandated strings, `status` = `rejected`, `used-by` = `—`, and anchor cells that carry the round-38 `ScoutVexLeads.md` fetch digests (six 64-hex digests; each one verified to occur verbatim in that receipt) plus its line locators. A scratch fleet mirror of `corpus/SOURCES.md` with only these three rows inserted after S055 validates clean: `exit 0`, warnings `W04 S028` and `W04 S029` only, i.e. the two pre-existing warnings and no new E/W code; a deliberately invalid probe row in the same mirror is reported (`E06 S900 tier=Z`, exit 1), proving the mirror is what the checker read. One conflict is routed to the judge and not resolved here: the frozen C2 text names four appended rows and the total 58, but 55 existing rows + 4 appends = 59; the three rejected rows alone take the frozen `grep -cE` count from 55 to exactly 58.

## 1. Deliverables

Paths are relative to the lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

| # | path | lines | bytes | sha256 |
|---|---|---|---|---|
| 1 | `.ufo/waves/round-39/wave1/ScribeRowsRejected.S056.row.md` | 1 | 1281 | `e3b789f2f7c249c82a71b498ef498cdf8afa43407a3eae59895ad0da86a69ceb` |
| 2 | `.ufo/waves/round-39/wave1/ScribeRowsRejected.S058.row.md` | 1 | 1202 | `57f1ab24f58bc512301226d7fe8e8e48ca4bd759474db249c90d6909ea3f87bb` |
| 3 | `.ufo/waves/round-39/wave1/ScribeRowsRejected.S059.row.md` | 1 | 1044 | `faf60f0194690c91a6db77d8c6523e4f71034e886426619059ff3b0b80d5cb47` |
| 4 | `.ufo/waves/round-39/wave1/ScribeRowsRejected.registry-changes.md` | 4 | 2205 | `86c4ab729473481226184e197c77919432836e5c8367960bca4ac30f9b39488c` |

Each file ends with one `\n`; file 4 is the four `## Registry changes` bullet lines (three `row added` bullets plus the `no cell changed` count bullet), nothing else.

## 2. Row cells as landed

Header shape (SOURCES.md L5): `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

| id | kind | tier | status | opened | recheck | used-by | scope chars | anchor chars | teaches chars |
|---|---|---|---|---|---|---|---|---|---|
| S056 | docs | A | rejected | 2026-10-26 | `on-release` | `—` | 173 | 589 | 256 |
| S058 | docs | B | rejected | 2026-10-26 | `180d` | `—` | 205 | 572 | 266 |
| S059 | spec | A | rejected | 2026-10-26 | `on-release` | `—` | 136 | 482 | 256 |

Source cells carry exactly the item-spec names and URLs (MINIMUM-requirements page; `github.com/openvex/spec/blob/main/OPENVEX-SPEC.md`; `cyclonedx.org/docs/1.7/json/`), one `https://` token each. Anchor digests, all re-verified against `.ufo/waves/round-38/wave1/ScoutVexLeads.md` §1:

| id | digests cited in the anchor | r38 ledger rows | locators |
|---|---|---|---|
| S056 | `67bafe172cb7ba5cee8938235abce59ca2a0069d96c65fa1078dc42f05a8eab8` (page 49253 B), `1e73325c674aa55c5665e3d2b647201acc46ee1fa9c8ee8bf88e4ff044f975c8` (PDF 1047967 B) | #1, #2 | L83 (v1.0.0), L408-L413 (four statuses), L435 (`[justification] MUST`), L127-L128 (CSAF/CycloneDX/OpenVEX cross-format statement) |
| S058 | `9375415ccb351260a998864cbeebbaff1808d1b09a306919b79cc75e5519f884` (raw 30580 B), `1dd123a88ebcae4703a1462bc772a47d5773949ae2e369964022ceb8cc2059db` (repo landing 312251 B) | #6, #7 | L1 (H1 v0.2.0), L205-L219, L343-L356, L362-L377, revisions table L635-L650 ending 2023-07-18 (no v0.2.0 date) |
| S059 | `afb22b46d49ad68a648cfb1b9ec3f0f47028cc6170a8ad133603fac30e88f3f9` (v1.7 6419901 B), `ff875e45809ad8e881fa62395490acbcf4f0f7d5ee87b1c516b2cbb226f6f588` (v1.6 5575098 B) | #10, #9 | `analysis.state` L24562-L24582, `analysis.justification` L24589-L24605 |

Why each stays rejected, in one line each (the ground is §2 of the round-38 receipt, not re-derived here): Minimum Requirements restates the vocabulary S055 already pins (S055 L1762: "The given values reflect the VEX not affected justifications.") and adds only lineage plus tool-neutral metadata rules; OpenVEX repeats the same four statuses and five labels at a mutable `main` ref with no standards-body approval and no established v0.2.0 date; CycloneDX `analysis` is a genuinely different vocabulary (six states including `false_positive`, nine justifications) that needs a scoped analysis-subtree capture before any quote can be pinned, so it belongs to a separate frontier. Each anchor ends "no lane capture, so no manifest record can anchor this row" — binding rule B3 bars a rejected row from anchoring a record.

## 3. Gates run (commands and actual output)

### G1 shape — one line, NF=13, 11 cells, no pipe inside a cell

Read off the delivered bytes:

```
S056 lines=1 bytes=1281 NF=13 cells=11 id=S056 kind=docs tier=A status=rejected opened=2026-10-26 recheck=on-release usedby=— pipe_in_cell=False trailing_nl=True sha256=e3b789f2f7c249c82a71b498ef498cdf8afa43407a3eae59895ad0da86a69ceb
S058 lines=1 bytes=1202 NF=13 cells=11 id=S058 kind=docs tier=B status=rejected opened=2026-10-26 recheck=180d usedby=— pipe_in_cell=False trailing_nl=True sha256=57f1ab24f58bc512301226d7fe8e8e48ca4bd759474db249c90d6909ea3f87bb
S059 lines=1 bytes=1044 NF=13 cells=11 id=S059 kind=spec tier=A status=rejected opened=2026-10-26 recheck=on-release usedby=— pipe_in_cell=False trailing_nl=True sha256=faf60f0194690c91a6db77d8c6523e4f71034e886426619059ff3b0b80d5cb47
```

### G2 teaches cells are byte-identical to the mandate

The three mandated strings were extracted programmatically from the frozen item spec (`.ufo/waves/round-39/wave1-spec.json`, item `ScribeRowsRejected`, prompt sha256 `2204c4f40db0938b8bcd40dc897345884635734f4833112e7fe5c0dde617f120`, 9025 bytes) and compared with the delivered cell:

```
S056 teaches_bytes_equal_mandate= True (256 chars)
S058 teaches_bytes_equal_mandate= True (266 chars)
S059 teaches_bytes_equal_mandate= True (256 chars)
```

Not merely a prefix match: the whole cell equals the mandated string (a trailing period was not added).

### G3 anchor provenance

Every 64-hex token inside each delivered row was looked up in the round-38 receipt:

```
S056 67bafe17…a8eab8  in_row=True  in_r38_receipt=True ; 1e73325c…f975c8 in_row=True in_r38_receipt=True
S058 9375415c…19f884  in_row=True  in_r38_receipt=True ; 1dd123a8…2059db in_row=True in_r38_receipt=True
S059 afb22b46…88f3f9  in_row=True  in_r38_receipt=True ; ff875e45…f6f588 in_row=True in_r38_receipt=True
```

No digest, byte count, HTTP status, fetch time or line locator was invented here; the two round-38 times that receipt prints as `18:36:0xZ` are carried as `18:36:0xZ` rather than inflated into false precision.

### G4 census over a scratch mirror with only these three rows appended

Mirror built as `<scratch>/mirror/kasegi-shokunin/`: `corpus/SOURCES.md` = lane bytes with the three rows inserted directly after the S055 row (inside `## Registry`, not at EOF) and `corpus/knowledge/` copied so `E11` used-by paths resolve. 58 registry rows in the mirror.

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-26 <scratch>/mirror/kasegi-shokunin
kasegi-shokunin	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-shokunin	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-shokunin	ok	<scratch>/mirror/kasegi-shokunin/corpus/SOURCES.md
exit 0
```

Mirror-read proof (same mirror plus one invalid probe row `S900` at tier `Z`):

```
kasegi-shokunin	E06	S900 tier=Z
exit 1
```

So the three rows add no `E` code and no `W` code: `E04` did not fire (no duplicate URL+scope), `E05` kind and `E06` tier are inside the enum, `E07` status `rejected`, `E08` opened is today, `E09` accepts the symbolic cadence `on-release` and `180d`, `E10` not applicable, `E12` did not fire (rows sit in `## Registry`), `W02` did not fire (each `teaches` is 256-266 chars, far past the 8-char thin-reason threshold), `W04` unchanged.

### G5 the frozen counting command

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        # lane, rows unlanded
55
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' <mirror>/corpus/SOURCES.md  # these three rows appended
58
```

And the frozen post-landing census check, run read-only on the real lane at its current (unlanded) state:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit 0
```

What this does **not** prove: it is the before state. The after state must be re-run once S057 and these three rows are actually landed; I did not land anything and did not edit `corpus/SOURCES.md`.

### G6 write surface

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain corpus/SOURCES.md
(empty)
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Only the four deliverable files above and this receipt were written inside the lane; no product file, no fleet-root file, no sibling lane, no source tree, no mutating git command.

## 4. The `## Registry changes` bullets

`ScribeRowsRejected.registry-changes.md` holds four lines in the section's established shape (`- S0NN row added: new row (id `S0NN`, kind …, tier …, status `rejected`, opened 2026-10-26, recheck …, used-by `—`), anchor pinned to the round-38 `ScoutVexLeads.md` fetch ledger: …`):

- S056 bullet — records kind/tier/status/opened/recheck/used-by, the page and PDF digests (abbreviated `67bafe17…a8eab8`, `1e73325c…f975c8` in the section's existing abbreviation style), the four locator groups, and that no manifest record may anchor the row.
- S058 bullet — same shape; records the `main`-ref volatility, the revisions table ending 2023-07-18, and the missing v0.2.0 date.
- S059 bullet — same shape; records both the v1.7 and v1.6 digests and the `analysis.state` / `analysis.justification` locators.
- Count bullet — `S001–S055 untouched (logged)`, then `Registry 55 rows pre-append → 59 post-append (R8): the mined S057 row plus the rejected S056, S058 and S059 rows; the three rejected rows alone take the registry-row count from 55 to 58.`

That last sentence is the arithmetic, not a hedge: see F1.

## 5. Findings

**F1 (HIGH, for the judge — not resolvable in my write scope). Frozen registry total 58 is inconsistent with the four rows the same claim requires.** Verbatim, `claims.json` C2 `after[0]`: `frontier 22; registry 58 (S057 mined + S056/S058/S059 rejected); …`. Verbatim, C2 `counting_commands`: ``grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58``. Verbatim, my item spec: `Also draft the `## Registry changes` bullet lines for these appends (old→new: registry 55 → 58).` Verbatim, `.ufo/waves/round-39/c2-controls/before.txt` line 3: `registry rows: 55`. The claim simultaneously requires all four rows (`kill_rule`: `S057 row absent or NF != 13; S056/S058/S059 rows absent as rejected rows; …`) and a total of 58; 55 + 4 = 59, so once the four rows are landed the counting command prints 59, not 58, and the frozen check fails through no defect in the rows. The measured coincidence is exact: the three rejected rows alone take the count 55 → 58 (G5). The likeliest derivation is the round-38 arithmetic carried forward — `ScoutVexLeads.md` §4 states "the frozen C2 before-controls count … (54 at base, 55 expected after S055)", and 54 + 4 = 58 — but I cannot establish the drafter's intent. Either the frozen figure is corrected to 59, or one row is withheld and the rejected-row kill rule fires. My deliverable states the true arithmetic (59 with S057, 58 with the rejected rows alone) and leaves the adjudication to the canonical judge.

**F2 (instrument trap, observed, non-mutating).** `sources-census.sh validate --root <scratch-root> <bare-lane-id>` does **not** read a scratch mirror: with `--root` set, a bare lane id skips the directory branch, `build_roster` finds no `shokunin.conf` at the scratch root (`stderr: ERROR: config not found: <scratch>/fleet/shokunin.conf`) and resolves the id from the real fleet roster — the run then validates the real lane and prints its real path in the `ok` line. Proof: with an invalid probe row at tier `Z` in the scratch mirror, that invocation still printed `exit 0` and only the two real-lane `W04` warnings, while the same mirror passed as an absolute directory argument reported `E06 S900 tier=Z` and `exit 1`. A verifier that writes "census exit 0 on the mirror" from the first form has proven nothing. I discarded my first two runs for exactly that reason and rebuilt the evidence on absolute-dir and `--file` invocations. Worth a line in the round-39 lesson's spot-check readiness list.

**F3 (note, verified harmless).** The S056 URL string already occurs once in `corpus/SOURCES.md` (`grep -n 'minimum-requirements' corpus/SOURCES.md` → line 86), inside the round-38 `## Search log` prose bullet — not a registry row. `W04` compares row URLs only, and the mirror run reports `W04` at S028/S029 alone, so the append introduces no duplicate-URL warning.

**F4 (dependency, not a defect).** The `## Registry changes` count bullet names the mined S057 row, whose deliverable belongs to seat `ScribeRowS057` and was not present in `wave1/` when I wrote this. If that row is withheld or reshaped (its item demands NF=13 and `status mined`), the count bullet needs the L1's final registry total, not mine.

**F5 (scope boundary, recorded).** `capture-binding-check.py` rule B3 forbids a rejected row from anchoring a capture record, so none of these three rows may appear in `corpus/source-snapshots/round-39/manifest.json`; each anchor says so explicitly. Binding should stay 46/46 and recheck-audit `expected=51` with these rows alone.

## 6. Out of scope (not done, by design)

No S057 row, no registry edit, no `corpus/README.md` frontier row, no knowledge entry, no capture, no manifest, no harness run, no binding or audit run, no census-after claim. I did not edit `corpus/SOURCES.md`, the round-39 lesson, PROVINCE, SCORECARD, LOG, or any fleet or sibling file, and I ran no mutating git command. Scratch was removed after the deliverables were copied.

## 7. Artifact paths

- Deliverables: `.ufo/waves/round-39/wave1/ScribeRowsRejected.S056.row.md`, `.S058.row.md`, `.S059.row.md`, `.registry-changes.md` (line counts and sha256 in §1).
- This receipt: `.ufo/waves/round-39/wave1/ScribeRowsRejected.md`.
- Read for provenance: `.ufo/waves/round-39/claims.json`, `.ufo/waves/round-39/wave1-spec.json`, `.ufo/waves/round-39/c2-controls/before.txt`, `.ufo/waves/round-38/wave1/ScoutVexLeads.md`, `corpus/SOURCES.md` (rows S026-S028 for the rejected-row shape, L5 header, L93 `## Registry changes`), `scripts/sources-census.sh`.

## 8. Scratch

`/fast/scratch/hyaku/kasegi-r39/ScribeRowsRejected/` (mirrors, probe copies, teach-string extraction) removed before yield; no `/tmp` residue was created.
