# RevCorrections — review of ExecCorrectionsR2's R2 correction blocks (round 39)

- seat `RevCorrections` (reviewer, leaf); lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD `d65d823e7c84813c192b20ee757a8761f878a61f` (base `480b1a505a2dfc14a4f718d16d63808247214d0a`, freeze `dcd31701720a6a4929a32471a62011ed87103421`)
- reviewed 2026-10-26T19:3x–19:5xZ against `.ufo/waves/round-39/wave1/ExecCorrectionsR2.{round38-lesson,log,scorecard,shonen}.append.md` + its receipt `ExecCorrectionsR2.md`
- method: independent re-measurement (own greps, diffs, cmp, git reads on scratch copies); the executor's receipt was cross-checked, not trusted.

## Verdict

**PASS — the four blocks satisfy the R2/R3 mandate; recommend one one-token pre-land fix (F1).**
Sweep complete (every overstating mention named by a `Correction (round 39)` line), truth named in every
block (judged-head run `closed=7/8 exit=1`; the `closed=8/8` run/selftest over run-ref `7dd2fcd6`, not J),
append-only verified byte-wise, all four blocks byte-exact landable. No correction rewrites existing bytes.

## 1. Deliverables reviewed (my own fingerprints; match the executor's receipt §1 exactly)

| deliverable | lands appended to | lines | bytes | sha256 |
|---|---|---:|---:|---|
| `ExecCorrectionsR2.round38-lesson.append.md` | `corpus/lessons/round-38.md` (EOF) | 2 | 1354 | `895547931464ba115bae0620a771766dab35fb36daa329435e7310b1b5e83474` |
| `ExecCorrectionsR2.log.append.md` | `LOG.md` round-39 entry (bullet; L1 merges) | 1 | 514 | `b9cee1ecfa138ec8f9da8a1e2401ae4e588dfb4c74181bb036e57ebddc4e2b3e` |
| `ExecCorrectionsR2.scorecard.append.md` | `SCORECARD.md` (EOF) | 2 | 1426 | `0251af27d9336fe1b93db705dacc38ab0a77df09331ed9a0ae7761df14bada55` |
| `ExecCorrectionsR2.shonen.append.md` | `SHONEN.md` (EOF) | 2 | 743 | `79890f628869257df313f97aafd7359d4e6f9dc07af3de2eea5b756326deb23d` |

Shape: the three file blocks are one blank separator line + one `Correction (round 39):` paragraph; the LOG
block is one `- **Correction (round 39):**` bullet. All end `\n`; no CRLF (`grep -nP '\r'` → none), no
trailing spaces, no fence-opening lines (`^```|^~~~` → none), no `Final lane commit:` line, no placeholder
vocabulary (`⟨pending`, `<fill>`, `filled by the L1`, `<LANE_HASH>`, `<r38-` → none). Pure landable bytes.

## 2. Sweep completeness — every overstating mention touched

Mandate grep, before (run verbatim in the lane, HEAD `d65d823`):

```
$ grep -n "closed=8/8" corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
corpus/lessons/round-38.md:21:| **C1** | … `closed=8/8 exit=0` and `selftest cases=8 failures=0` over the judged head are the receipt …
corpus/lessons/round-38.md:94:8. **C1 receipts at the judged head.** … `--export-ref J` → `closed=8/8 exit=0`; …
```

Exactly two literal mentions, both in `corpus/lessons/round-38.md`; LOG/SCORECARD/SHONEN carry the same
overstate in other words. Five overstate sites total, each named by its block:

| site | overstate | swept by |
|---|---|---|
| `corpus/lessons/round-38.md:21` | "8/8 … over the judged head" | lesson block (names `:21` + quotes it) |
| `corpus/lessons/round-38.md:94` | "`--export-ref J` → `closed=8/8 exit=0`" | lesson block (names `:94` + quotes it) |
| `LOG.md:1698` | "Run and selftest over the judged head" | LOG bullet (quotes the phrase) |
| `SCORECARD.md:1517` | "the run over the round-38 head the receipt names" | SCORECARD block (quotes the clause; section `## Round 38 result` at `:1513` named correctly) |
| `SHONEN.md:185` | "r38 suite run + selftest over the judged head" | SHONEN block (quotes box 3's line) |

No sixth site: I swept all `judged head` mentions in the four files myself — `round-38.md:6,19,245,248-249,284-286,304-305`
(rule text, Mistakes rows, attack findings), `LOG.md:1663-1701` (round-36/37 entries; `:1701` is the Wave
bullet about the results file, not a run claim), `SCORECARD.md:1424,1472,1500,1511,1522` (earlier rounds /
reference-only naming). `SCORECARD.md:1523` ("the C1 run is the receipt itself") checked and acceptably left
uncorrected: it states where the run is recorded, not that 8/8 printed at J, and the SCORECARD block now
states which run is which. The remaining `8/8` matches in LOG/SCORECARD are round-23-era frontier/density
counters, not the r38 C1 suite.

Post-append (simulated on scratch copies): mentions retained at `:21`/`:94` (append-only), correction lines
land at `corpus/lessons/round-38.md:311`, `LOG.md:1703` (if EOF-appended; the L1 merges into the round-39
entry — `grep -c '^## Round 39' LOG.md` → 0 at HEAD), `SCORECARD.md:1532`, `SHONEN.md:189`.

## 3. Truth named in every block — verified against the committed receipt

Each block contains `closed=7/8 exit=1`, the full run-ref hash `7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e`,
and the not-J contrast (lesson/log literally "not J"; scorecard/shonen by paraphrase: "holds only for the
receipt's `run-ref`" / "committed over the receipt's run-ref, with the run over J red on G2 alone").
Ground truth re-measured from `.ufo/waves/round-38/final-gates/all-gates.txt` (unchanged `f06148c6..HEAD`;
`git diff --name-only` empty):

```
2:export-ref=66703acaaff50529a35be49aa8759d04140720ad      <- judged head per the frozen r38 judged_head_rule ("J is the export-ref= value recorded in …all-gates.txt")
4:run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e
8:export-ref-run: G2 payload=receipt=0,… closed=0
15:export-ref-run: closed=7/8 exit=1
17:run-header: export-ref=7dd2fcd6…                        (run section)
26:closed=8/8 exit=0                                       (over run-ref)
28:selftest export-ref=7dd2fcd6…                           (selftest section)
73:selftest cases=8 failures=0
```

Structural claims verified: `git diff --name-only J 7dd2fcd6…` → the receipt file only (bootstrap = J plus a
receipt); `git merge-base --is-ancestor J f06148c6…` → yes; receipt header `:5` states the G2-at-J
structural reason. R3 label verified: the SCORECARD block names `f06148c66c6d7aed948cb7024d9f0b9cffe4b95a`
report-quoted only — `git diff --name-only J f06148c6…` → the receipt only, `--numstat` → `79 0`,
`git grep f06148c6 f06148c6…` → 0 hits exit 1, and the quote's source is the fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md:37` (read-only; no committed transcript for
that run exists in the lane — lane-wide grep shows `f06148c6` only in round-39 wave machinery and the
committed spotcheck lesson). Scores untouched ("corrects the evidence sentence, not the score") — matches
frozen `score_after: held 4`.

## 4. Append-only / no rewrite of existing bytes

Simulated `cat <deliverable> >> <copy>` per target, `diff -u` before/after:

```
corpus/lessons/round-38.md  added=2 removed=0   (blank separator + paragraph, one EOF hunk)
LOG.md                      added=1 removed=0
SCORECARD.md                added=2 removed=0
SHONEN.md                   added=2 removed=0
```

Appended tail byte-identical to the deliverable (`cmp <(tail -c <size> after) <deliverable>` → identical ×4).
Targets unmodified at start: blobs at HEAD `d65d823` — `4ed05a9e…` (round-38.md), `308dc467…` (LOG),
`a1a48cb3…` (SCORECARD), `f17dee7a…` (SHONEN); `git status --porcelain` on the four → empty.

## Findings

- **F1 — MINOR, fix before land.** `ExecCorrectionsR2.round38-lesson.append.md` cites the selftest run-ref
  anchor as `(:4, :17, :29)`; the anchor carrying `export-ref=7dd2fcd6…` in the selftest section is **`:28`**
  (`:29` is `selftest detail=G1 positive=pass …`, which names no ref). One-token fix `:29` → `:28` in the
  deliverable (byte count unchanged, sha256 changes — re-fingerprint and re-declare the tail). The executor's
  receipt §2 parenthetical ("headers at `:17` and `:29`") repeats the same off-by-one; do not propagate it into
  declared-blocks or the report. All other citations in all four blocks check out (`:2 :4 :5 :8 :15 :17 :26 :73`).
- **F2 — MATERIAL, outside the blocks (corroborates the executor's §5.1).** Frozen `claims.json` (C1
  `kill_rule` and counting command #4) carries `66703aca50529a35be49aa8759d04140720ad` — **37 hex chars, not
  an object** (`git cat-file -t` → fatal). The valid r38 judged head is `66703acaaff50529a35be49aa8759d04140720ad`
  (receipt `:2`). All four corrections correctly use the 40-char receipt value; the r39 suite's r38-head
  red-check and the final report must use the valid hash — the frozen counting command as written is
  unresolvable (R1-class: frozen command not dry-run satisfiable).
- **F3 — NIT.** The LOG bullet omits the `round-38-verifier-spotcheck.md §5 R2` citation the other three
  blocks carry. Truth fully named; non-blocking.
- Timing note (resolved, no defect): ExecCorrectionsR2's scratch dir was still present immediately after its
  receipt landed; absent at recheck minutes later (mid-cleanup race). Its §6 removal claim is now true.

## Verification gaps

- The r39 suite (`corpus/instruments/r39-closure.sh`) is not yet committed; I did not run it (not my item).
- The LOG bullet's final position is the L1's merge (no round-39 entry exists yet); I verified the bullet
  bytes and the EOF-append simulation only.
- I read the fleet report only at the R3 quote (`:37`) and its header lines; not a full audit of that report.

## Hygiene

Writes: this receipt only. Scratch `/fast/scratch/hyaku/kasegi-r39/RevCorrections/` (append-sim copies +
diffs) removed before yield. No tooling installed; no pacman; no network fetches; read-only git only
(`log`, `status`, `rev-parse`, `cat-file`, `diff`, `merge-base`, `ls-tree`, `grep`); no mutating git/jj anywhere.
