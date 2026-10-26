# RevCensus — round-34 final census verification

Seat: RevCensus (reviewer, leaf of the L2 wave; no delegation). Assignment: verify the final census —
the frozen validate command, the six contract commands, registry 50→51, frontier 16→17 — and give a
verdict. This seat authored none of the measured changes; every command below was run by this seat
and outputs are quoted verbatim.

## Report

### 0. Method and timeline

- All commands run from the lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless stated.
- Timeline (UTC, 2026-10-26): first battery on the **pre-landing** tree (~05:2x–05:3xZ — SOURCES.md
  then byte-identical to the freeze commit, frontier 16); S051 row observed landed mid-verification;
  final battery after both the S051 row and the F17 frontier row had landed; bookend re-run
  byte-identical (VALIDATE-OUTPUT-IDENTICAL, SIX-COMMANDS-IDENTICAL).
- Frozen-claims integrity: `sha256sum .ufo/waves/round-34/claims.json` →
  `dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850`, byte-identical to
  `git show 29f606dbdd28aff6fd4573ab4b90788bbb90af13:.ufo/waves/round-34/claims.json | sha256sum`
  → same digest. The claims verified against are the committed frozen bytes.
- Read-only git plumbing only (`show`, `diff`, `status`, `log`); no `git add/commit/push`, no jj
  mutations, no writes outside this receipt and the scratch dir, no subagents, no `agent://all`.

### 1. Primary census validate command (frozen contract text)

Pre-landing run and final run print the same three lines:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "validate_exit=$?"
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
validate_exit=0
```

- exit 0; stderr empty; **exactly** `W04 S028` + `W04 S029` + `ok` — no `E` finding, no new `W` finding.
- The three content lines are byte-identical to the frozen `.ufo/waves/round-34/census-before.txt`.
- The S051 row introduced no new warning: its URL is unique across scopes (no other row in any fleet
  lane registry carries `immunefi-vulnerability-severity`; W04 fires on the same normalized URL with
  a different scope key, `scripts/sources-census.sh:643-645`).
- Bookend: second run byte-identical.

### 2. Six contract commands (canonical CORPUS.md:133-149 forms, run from the lane root)

Command text transcribed verbatim from `/home/vgpnk/Projects/shokunin/CORPUS.md` §"Census — run from
the lane root" into a battery script; replayed on the freeze-commit bytes first:

```
$ git show 29f606db:corpus/SOURCES.md > $S/SOURCES-freeze.md && bash six-commands.sh $S/SOURCES-freeze.md
rows=50
malformed=0
tier=A=47 B=1 C=2
status=mined=38 queued=9 rejected=3
dups=
enum_violations=
missing_usedby=
```

(matches the frozen `census-before.txt` before-state and the round-33 after-state; the pre-landing
working tree reproduced it exactly — `diff` empty, REPRO-IDENTICAL)

Final (landed) values:

```
$ bash six-commands.sh corpus/SOURCES.md
rows=51
malformed=0
tier=A=48 B=1 C=2
status=mined=39 queued=9 rejected=3
dups=
enum_violations=
missing_usedby=
```

| command | expected (assignment) | measured (final) | verdict |
|---|---|---|---|
| rows | 51 | 51 | match |
| malformed | 0 | 0 | match |
| tier histogram | A=48 B=1 C=2 | A=48 B=1 C=2 | match |
| status histogram | mined=39 queued=9 rejected=3 | mined=39 queued=9 rejected=3 | match |
| duplicate ids | empty | empty | match |
| enum violations / tier inflation | empty | empty | match |
| missing used-by | empty | empty | match |

Tier sums 48+1+2=51; status sums 39+9+3=51. Bookend: second run byte-identical.

### 3. Registry 50→51

- Base `014ee2d` and freeze `29f606d`: `git show <c>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **50** each.
- Pre-landing working tree: 50, and `git show 29f606d:corpus/SOURCES.md | diff -q - corpus/SOURCES.md`
  → identical (the tree still carried the freeze bytes at first measure).
- Final: **51**; `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` → **1**.
- Landed diff vs freeze: `git diff --numstat 29f606d -- corpus/SOURCES.md` → `5 0` (5 added, 0
  deleted), exactly these lines:
  - `corpus/SOURCES.md:57` — the S051 registry row (11 cells / NF=13; kind `docs`, tier `A`, status
    `mined`, opened `2026-10-26`, recheck `90d`, used-by
    `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, anchor pinned to
    `corpus/source-snapshots/round-34/S051.txt` sha256 `4fd8ed98…b325a5`, 175 lines, with line
    locators L45–L96);
  - `corpus/SOURCES.md:77` — the `## Search log` bullet "Immunefi severity-classification sweep
    (round 34); question: does the lane already hold a Web3 or smart-contract bounty
    severity-classification source …";
  - `corpus/SOURCES.md:103-105` — the three `## Registry changes` R8 lines, ending
    "No status/recheck/used-by cell changed on any pre-existing row; S001–S050 untouched (logged).
    Registry 50 rows pre-append → 51 post-append (R8)."
- The row's used-by path exists (the F17 entry, untracked working-tree file pending the L1 commit);
  the census E11 check confirms it (`missing_usedby` empty).

### 4. Frontier 16→17

- Base `014ee2d` and freeze `29f606d`: `git show <c>:corpus/README.md | grep -cE '^\| F[0-9]+ \|'` → **16** each.
- Pre-landing working tree: 16 (README.md unmodified; digest `3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932`).
- Final: **17**; `grep -cE '^\| F17 \||^\| F17  \|' corpus/README.md` → **1** — the F17 row at
  `corpus/README.md:361`, status `admitted`, entry
  `knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, sources `S051`.
- Landed diff vs freeze: `git diff --numstat 29f606d -- corpus/README.md` → `26 0` (26 added, 0
  deleted): the `## Round-34 admission — coverage map row and Frontier F17 (appended 2026-10-26)`
  section (coverage-map row + F17 frontier row + the r34 amendment paragraph "at round 34 the
  frontier stands at **17/17 admitted** — … F16 at round 33, F17 at round 34").
- Harness corroboration (ExecHarnessAfter's instrument, run by this seat as a cross-check):
  `python3 corpus/instruments/frontier-recheck-count.py` → `PASS F17
  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051`, `entries=20 pass=20 exit=0`.
- Entries citing `source: S051 `: `grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l` → **1**;
  knowledge entries `ls corpus/knowledge/*.md | wc -l` → **46** (claim before 45 → after 46).

### 5. Instrument soundness (the measuring tool itself)

- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` → **exit 0**; 96 `killed`
  lines, 0 `SURVIVED` — the census instrument passes its own 96-case selftest.
- Quiescent input: bookend digests stable across the final battery —
  `corpus/SOURCES.md` `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6`,
  `corpus/README.md` `876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29`
  (pre-landing digests for the record: SOURCES `b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b`
  = the freeze-commit bytes; README `3779e77f…` unchanged pre-landing).

### 6. Findings and observations

1. **Frontier-row ownership gap (resolved by landing; recorded for the lesson).** No wave1 seat's
   task text in `wave1-spec.json` owns the `corpus/README.md` F17 frontier row / Round-34 admission
   section — searched all 65 items' task segments for `frontier row|README|admission section|16→17`:
   zero owners; the counting seats (ExecCensusAfter, ExecRegressionC2, RevCensus) only measure it.
   Round-33 precedent matches: the F16 row landed in the L1 integration commit `9f98488`, not by a
   wave seat. The row did land during this verification window (README digest `3779e77f…` →
   `876be9cc…`); the L1 should confirm at integration whether it authored this append or which seat
   did, so the lesson's landed-changes table attributes it.
2. **Landed text vs the ScribeSOURCESRow draft**: the appended search-log bullet and R8 lines differ
   in wording from the draft at `.ufo/waves/round-34/wave1/ScribeSOURCESRow.md` (e.g. the draft's
   bullet carried "captured under the instrument UA into corpus/source-snapshots/round-34/S051.txt:
   8502 bytes, 175 lines, sha256 4fd8ed98…b325a5" while the landed bullet phrases the capture
   differently; the draft's third R8 bullet read "an uncommitted fetch … lists v2.3 ahead of the
   v2.2 page" while the landed `:104` reads "the index fetch of 2026-10-26 (no committed capture;
   observation only) marks v2.3 and v2.2 both Currently in Use"). The shape (1 row + 1 bullet + 3
   R8 lines) is preserved and ExecRegistryAppend was instructed "do not proceed with a different
   shape"; whether the wording deltas are within that instruction is **RevRowS051's verdict scope**
   (row + bullet + R8 truthfulness), not this seat's. Recorded here so the L1 can reconcile the two
   receipts.
3. No other census-visible defect: no `E` code fired (validate E-code scan empty), no new `W` code,
   and the FLEET block equals the lane block (rows 51; tier 48/1/2; status queued=9 mined=39
   rejected=3; missing 0; invalid 0).
4. **F-3 (verified first-hand; outside census scope — recorded so this PASS is not read past the
   census; reported independently by ExecCensusAfter-2):** two adjacent C2 cells are defective at
   the landed bytes:
   - **Recheck claim wording.** `source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json
     --source S051` exits 0, but of its 18 assertion lines 16 print `occurrences=1` and **two print
     `occurrences=2`** (`S051:Q9 OK occurrences=2 anchor=77-ok`, `S051:Q17 OK occurrences=2
     anchor=96-ok`); sha256 OK. The frozen claims.json C2 "after" sentence "every assertion
     occurrences=1" is therefore FALSE as worded — the pass is legitimate via the QUALITY Q9
     anchor-disambiguation path, so the defect is the claim wording, not the recheck or the entry.
     The kill rule ("source-recheck S051 exit != 0") does not fire. Correction lands as an appended
     claims-correction file per the freeze rules; the L1 decides.
   - **Junk-twin rejection is reviewer-limb only.** `c2-controls/junk-f17.md` (committed at the
     freeze commit) carries the real S051 URL verbatim (`:9`), a `recheck:` line whose command is
     byte-identical to the real entry's (`--manifest …/round-34/manifest.json --source S051` →
     exit 0), and a quoted fragment that exists in the capture (`Direct theft of any user funds` →
     1 hit in the capture, `S051.txt:75`; the string also occurs once in the manifest's `quotes`
     array, so the capture+manifest pair holds it in 2 files — the capture-side count is the one
     the rejection argument turns on); only its synthetic phrase is absent (`five severity levels for
     smart-contract exploits` → grep 0). `check_r9`'s junk limb asserts only that the twin FILE
     EXISTS plus nine case-name greps in capture-binding-check.py — it never executes a rejection.
     Sub-block anchors at the bytes verified by this seat (sha256 `2a635bf575c38e04b028dd26ecbeff73c3b909add892ab727c2ab6b1c821dcfc`,
     742 lines): nine case-name greps `:433-438`, twin-presence test `:441-445`; rule A's
     behavioural mirror/reverse fixtures `:446-472` are a separate limb of the same check, not the
     junk rejection. The limb's logic is unchanged across the file's landed states (688→742 lines
     during the wave; re-read at both digests by ExecCensusAfter-2), so the finding is
     state-independent — only the anchors move, which is why they are pinned to the digest here.
     (Earlier line cites in play — this seat's first draft `:432-444`,
     ExecCensusAfter-2's `:424-436`/`:437-463` — matched earlier/different byte states of this
     still-uncommitted file; anchors into it are valid only against the digest named.) No
     executable counter distinguishes the twin; rejection rests on the non-author reviewer REFUSE
     record. Residual gap for the lesson's Gate/boundary section.

### 7. Verdict

**PASS.** The final census verifies end to end on the landed bytes:

- the frozen validate command exits 0 with exactly `W04 S028` + `W04 S029` + `ok` (no E findings,
  no new warnings);
- all six contract commands match the claimed after-state (rows=51, malformed=0, tier A=48 B=1 C=2,
  status mined=39 queued=9 rejected=3, dups empty, enum violations empty, missing used-by empty);
- registry rows **50→51** with exactly one S051 row (append-only, 5 lines, 0 deletions);
- frontier **16→17** with exactly one F17 row admitted (append-only, 26 lines, 0 deletions), bound
  by the harness (`entries=20 pass=20 exit=0`, `PASS F17 ids=S051`).

The before-state (rows=50, frontier=16) was independently reproduced at the freeze commit `29f606db`
and on the pre-landing working tree before the landing, so the 50→51 and 16→17 transitions are
measured, not asserted. Residual (non-census, for the L1): finding 1 (frontier-row attribution) and
finding 2 (draft-vs-landed wording, RevRowS051's scope).

**Scope boundary on this PASS** — two adjacent C2 cells were measured defective by
ExecCensusAfter-2 (`.ufo/waves/round-34/wave1/ExecCensusAfter.md`) and re-verified first-hand by
this seat (F-3 below); they are outside the census battery above and this PASS does not extend to
them.

### 8. Scratch and hygiene

- Scratch root `/fast/scratch/hyaku/kasegi-r34/RevCensus/` — deleted before yield (`rm -rf`).
- Writes outside scratch: this receipt only. No production file touched; no git/jj mutation; no
  writes outside the lane; `/home/vgpnk/Projects/shokuknow` and `/home/vgpnk/Projects/bounties`
  never touched.
- Tools installed: none (existing coreutils/gawk/python3 sufficient; no tooling authorization
  exercised).
