# RevCensus receipt — round 40, FALSIFY wave 2 (hyaku run 9)

Seat: RevCensus (leaf; no subagent dispatch). Dispatched by L1 (KasegiR40).
Item attacked: **the sources registry at Y** — `corpus/SOURCES.md` and the census gate that
vouches for it: the frozen census command, every CORPUS.md manual check, the C2 registry
counting commands, the new rows' captures/locators re-opened live, and mutation tests of the
census gate itself.

## What Y is at attack time

- Lane tip commit: `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (J5). Working tree tracked files
  are clean (`git status --porcelain` shows only untracked `.ufo/waves/round-40/final-gates/`,
  the two `kasegi-r40-falsify.ready*` files, and `wave2/`).
- The receipt `.ufo/waves/round-40/final-gates/all-gates.txt` (1062 B) exists on disk but is
  **untracked**; `git log -- .ufo/waves/round-40/final-gates/all-gates.txt` is empty, so no
  commit contains it and a Y-as-commit does not exist yet. `git diff --name-only 94abbff
  3074c76` = `.ufo/waves/round-40/declared-blocks.txt` (1 deletion), not the receipt.
- Registry impact: none — `git archive 3074c76` export's `corpus/SOURCES.md` is byte-identical
  to the worktree file (`cmp` clean), so every registry check below is valid for Y as defined
  (J + the untracked receipt). Observation O-3 records the state for the integrator.

## 1. Frozen census command — REPRODUCED

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
(run 2026-10-26 ~22:12 UTC, scratch cwd):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

Exit 0; warnings exactly W04 S028 and W04 S029 — matches the frozen claim, `census-before.txt`,
and the round-40 lesson's Census line. No new W/E code.

## 2. CORPUS.md manual checks on an export of Y — ALL CLEAN

Export: `git -C <lane> archive 3074c76` → scratch `y-export/`; checks run from the export root
(so `used-by` repo-relative paths resolve). Results:

| check | result |
|---|---|
| rows `grep -cE '^\|…S[0-9]{3,}…\|'` | **62** (59 at base + S060/S061/S062) |
| malformed rows NF!=13 | **0** |
| tier histogram | A=57 B=3 C=2 (base: A=55 B=2 C=2) |
| status histogram | mined=52 rejected=10 queued=0 |
| duplicate ids | none |
| enum violations (kind/tier/status) | none |
| tier-inflation (community at A) | none |
| mined rows' used-by paths missing | none (all exist) |

First run of the used-by check from `corpus/` (not the root) printed 58 false "missing" lines —
my pathing error, re-run clean from the root; noted here so nobody mistakes it for a defect.

## 3. C2 counting commands from claims.json, re-run on committed bytes — 8/8 GREEN

| command (on the 3074c76 export) | claimed | observed |
|---|---|---|
| queued among the nine rows | 9 → 0 | **0** |
| mined among the nine | 0 → ≥4 | **7** |
| entries `^source: S0(16|17|19|20|21|22|23|24|25)` | = mined count | **7** (the seven mined rows' entries, one each) |
| S060+ rows | 0 → ≥1 | **3** (S060, S061, S062) |
| entries `^source: S06[0-9]` | 0 → ≥1 | **1** (`cyclonedx-analysis-subtree.md` → S060) |
| frontier rows `^\| F[0-9]+ \|` in README.md | 22 → 23 | **23** |
| `frontier-recheck-count.py` | 25/25 → 26/26 | **entries=26 pass=26 exit=0** (PASS F23 ids=S060) |
| census validate | exit 0 | **exit 0** (§1) |

Before-controls honesty, verified against a base `a7af2ce` export: frontier 22 ✓; base
`validate --file base-export/corpus/SOURCES.md` prints the same W04 S028/S029 + `ok`, exit 0 ✓;
base `capture-binding-check.py` = `records=46 bound=46` ✓ (lesson says "up from 46").

## 4. New rows re-opened live (curl -sS -L --max-time 90 -A kasegi-shokunin/1.0)

Fetch time 2026-10-26T22:15:09–15Z (≈1 h after the ledger's 21:16 fetches). Every byte-level
claim in the three new rows reproduced:

- **S060** (mined, tier A, `supersedes S059 —` opens its teaches ✓). Re-capture via the
  committed `corpus/instruments/capture-source.py --id S060 --url https://cyclonedx.org/docs/1.7/json/ --kind html`:
  HTTP 200, 6,420,268 raw bytes; **full-page normalized sha256 `ffe8c0b6…ba7f4` = manifest
  claim**; slice (L1 + page-text L16060–L16169) **byte-identical to committed
  `S060.txt`** (`d6862622…e6779`, 4889 B, 111 lines = row's anchor claim). Locators L7/L15/L50
  hold the manifest quotes verbatim. REPRODUCED.
- **S061** (rejected; anchor cites committed ledger `wave1/ScoutS060Leads.txt`, sha256
  `96dc0c26…3695c5` = declared-blocks.txt ✓). Live: lead URL 404 / 46,957 B / `ec8e69c7…` ✓;
  publication page 200 / 56,383 B / `2cb3a40b…` ✓ with "Publish Date June 01, 2022" and
  "Archived Content" ✓; PDF 200 / 313,386 B / `9a4027c6…` ✓; `pdftotext -layout -enc UTF-8`
  sha256 `2b480ac8…8df4e6` ✓; locators L46-47 ("…status justification in an optional,
  machine-readable field.") and L208-209 (§3.7.3 "…are similar, but with some key…") ✓.
  REPRODUCED (one count nit → D-2).
- **S062** (rejected; round-39 flip monitor correctly NOT fired). Live: v2.1 page 200 /
  1,231,332 B / `fdb4bf01…` byte-identical to csd04 ✓; directory listing 1,097 B / `5e59949c…`
  ✓ showing csd01 28-May-2025 → csd04 21-Oct-2026, `schema/`, **no `os/`** ✓; parent listing
  392 B / `64a94196…` (v2.0/, v2.1/ only) ✓; both `os/` probes 404 / 41,334 B / `e416b400…` ✓.
  Both quoted spans present in the fetched bytes ("Edited by Stefan Hagen and Thomas Schmidt.
  21 October 2026. OASIS Committee Specification Draft 04."; "The nine defined properties are
  First affected…"). SHALL-drift monitor note verified: csd04 §3.2.4.8 reads "Group IDs … and
  Product IDs … **SHALL** be present" where S055 (v2.0) L1737 reads "**MUST** be present" ✓.
  REPRODUCED (locator nits → D-3).

## 5. Lane instruments re-run over the eight round-40 captures — GREEN

- `source-recheck.py --manifest …/round-40/manifest.json --source {S016,S017,S019,S020,S021,S023,S025,S060}`:
  **8/8 exit=0**, every pinned quote OK with `anchor=N-ok` (S019 quotes report occurrences=2 —
  the manifest's "recurs at L83" note is accurate).
- All **18/18 manifest quotes** verify at their declared anchors under whitespace-normalized
  matching; S020 Q1 (L142–L145), S025 Q1 (L31–L34) and S025 Q2 (L506–L510) are multi-line spans
  whose start sits mid-line exactly as the manifest locations state.
- `capture-binding-check.py`: **records=54 bound=54 unbound=0, exit=0** (54 = 46 + 8 new) —
  matches the lesson. `orphan=S040-live.txt` in the AUDIT line is pre-existing (present at
  base, inside round-26 control fixtures), not a round-40 item.

## 6. Append-only discipline on the nine decided rows — CLEAN

Cell-by-cell diff base→tip across S016/S017/S019/S020/S021/S022/S023/S024/S025: changed cells
are `status` ×9 and `used-by` ×7 only; `source/kind/tier/scope/anchor/teaches/opened/recheck`
untouched; no row removed; no id reused. The lesson's status-change log (7 queued→mined,
2 queued→rejected) matches. S061/S062 teaches follow the `REJECTED: …; flip: …` shape; S061
honestly records "no lane capture or manifest record exists this round" (true — manifest has
exactly 8 records, none for S061/S062).

## 7. Census-gate mutation tests (scratch fixture root; lane untouched)

Pristine control: exit 0, W04×2. Each mutant is the tip registry with one injected defect:

| mutant | result |
|---|---|
| E01 row truncated to 12 fields | killed — exit 1, E01 |
| E02 id `X016` | killed — exit 1, E02 |
| E03 duplicate id in-registry | killed — exit 1, E03 (+E04, correct) |
| E04 duplicate URL+scope in-registry (S063) | killed — exit 1, E04 |
| E05 kind `blog` | killed — exit 1, E05 |
| E06 tier `D` | killed — exit 1, E06 |
| E07 status `watch` | killed — exit 1, E07 |
| E08 opened `2027-01-01` | killed — exit 1, E08 |
| E09 recheck `soon` | **SURVIVED — exit 0, no code** (see O-1) |
| E10 community at tier A | killed — exit 1, E10 |
| E11 dangling used-by | killed — exit 1, E11 |
| W01 tier-C mined with used-by | warning W01, exit 0 (correct W semantics) |

The frozen CORPUS.md manual awk checks independently kill the NF!=13, duplicate-id, tier-D,
status-watch and community-at-A mutants (exact expected outputs). The gate is not vacuous.

## Defects found

All are minor; none breaks a frozen claim or a gate.

- **D-1 (minor, number-drift, `corpus/lessons/round-40.md` L27).** The Census line reads
  "tier A **+3?**mined S016/…/S060, rejected S061/S062…". Observed tier delta base→tip is
  **A +2** (55→57: S060, S061) and **B +1** (S062); no row changed tier. The "+3" is wrong as
  written and the "?" is a stray character. The registry itself is correct; the lesson's
  summary line is not.
- **D-2 (minor, count-method, S061 anchor + `wave1/ScoutS060Leads.txt`).** "pdftotext -layout
  text **274 lines** sha256 2b480ac8…": the byte-identical file (same sha256) is **273** lines
  by `wc -l`. The sha256 (the binding claim) is correct; the line count is off by one under
  the ordinary counter.
- **D-3 (minor, locator drift, S062 anchor + ledger).** Locators "L498" / "L7611" do not
  reproduce: raw HTML has the quotes at **L495 / L4162**, the lane's own capture normalization
  (`capture-source.py html_to_text`) at **L65 / L3022**, and a tag→newline collapse at
  **L497 / L7610** (consistent off-by-one from the claim). The quoted text and every
  byte-level claim verify; only the named line numbers are not reproducible by any method
  tried (raw, lane normalization, tag→newline±blanks; pandoc/lynx/w3m not installed).
- **D-4 (minor, cosmetic, `corpus/lessons/round-40.md` L29+L31).** Duplicated `## Gate`
  heading (two consecutive `## Gate` lines).

## Observations (not defects)

- **O-1 (tool looseness).** `sources-census.sh` `symbolic()` = `^[A-Za-z][A-Za-z0-9 _-]*$`
  accepts **any** word-like recheck token in validate mode (mutation E09: `soon` → exit 0,
  no code). Such values are surfaced only by `overdue` mode (`cadence <id> recheck=<x>`). The
  lane registry at Y is unaffected — every recheck is an ISO date, `NNd`, `on-release`, `365d`
  or `30d`. Flagged for the tool owner, not the lane.
- **O-2 (metadata).** Manifest records for S023/S060 say `user_agent: kasegi-shokunin/1.0`
  while their `tool` fields attribute the fetch to `capture-source.py`, whose hardcoded UA is
  `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`. The record
  names a UA prefix, not the exact string sent. Content unaffected (S060 re-capture with the
  instrument's real UA reproduced the identical normalized text).
- **O-3 (state, for the integrator).** At attack time the receipt `all-gates.txt` is untracked
  and no commit contains it, so claims C1's "`git diff --name-only J Y` = all-gates.txt" is
  not yet evaluable as a commit diff; Y-as-commit does not exist. Registry bytes are identical
  tip↔worktree, so this census attack is unaffected. Expected to resolve when the round-close
  receipt commit lands.

## Verdict

**Registry at Y: CONFORMANT — the census claims reproduce.** The frozen census command exits 0
with exactly the two declared W04 warnings; every CORPUS.md manual check is clean on the
committed bytes; all eight C2 counting commands reproduce (queued 0, mined-among-nine 7 with
7 matching entries, S060+ = 3 with 1 mined citing entry, frontier 23, harness 26/26, binding
54/54, recheck 8/8); all three new rows' captures and ledger claims re-open byte-exact live;
append-only discipline holds on the nine decided rows; the census gate kills every injected
defect class except the by-design symbolic-cadence looseness (O-1). Four minor defects filed
(D-1..D-4), none of which falsifies a frozen claim.

lsp device: no LSP server answered in this session (shell/data review; text-level checks only).

Scratch `/fast/scratch/hyaku/kasegi-r40/RevCensus/` removed at yield (disk-guard status taken
before the heavy pass: 613 GB free).
