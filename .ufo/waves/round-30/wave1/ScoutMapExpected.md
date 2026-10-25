# ScoutMapExpected — round 30, wave 1 (kasegi)

Seat: L2 scout. Scope: `corpus/instruments/knowledge-expected.txt` + `recheck-audit.py`
state at the freeze commit, the round-28/29 count verification, regeneration mechanics, the
R6 appendix convention, and the exact F13 table shapes for F14. Read-only: no production file
was edited; nothing installed (no tooling needed).

## 1. Expected list at the freeze commit (measured)

| item | value |
|---|---|
| file | `corpus/instruments/knowledge-expected.txt` |
| freeze commit bytes (3c557354…) | sha256 `6d26f6d5…989a` |
| working-tree bytes (2026-10-25) | sha256 `6d26f6d5…989a` — byte-identical to freeze |
| total lines | **43** |
| comment lines (header, `#`) | **2** |
| entries (non-comment) | **41** |
| hygiene | 0 blank lines, 0 duplicates, 0 CR bytes |
| ordering | exact match to `LC_ALL=C sort` (ASCII byte order) |
| header | line 1 `# Expected knowledge entries for corpus/instruments/recheck-audit.py — round 29`; line 2 “Sorted list from the working tree … keep in sync with corpus/knowledge/.” |

Live audit at those bytes (run 2026-10-25, `recheck-audit.py` freeze sha `3fc0d751…`):
`expect=present expected=41 missing=0 unexpected=0 exit=0`, `lines=41 total=41 pass=41`,
`strict pass=41/41 cdroot_fail=0 instrument_fail=0 own_fail=0` (executes=17 gated=24 broken=0).
Green today.

## 2. Round-28/29 note verification (measured from git objects, read-only)

| state | commit | lines = entries + comments |
|---|---|---|
| pre-F12 (round-28 start) | `1265fe1^` | **41 = 39 + 2** |
| post-F12 (round-28 end = round-29 base) | `1265fe1`, `7a6591c1` | **42 = 40 + 2** |
| post-F13 (round-29 end) | `0ab89298` | **43 = 41 + 2** |
| round-30 base | `a94871315` | **43 = 41 + 2** |
| freeze | `3c55735` | **43 = 41 + 2** |

So the measured sequence is 39/41 → (F12) 40/42 → (F13) 41/43. The brief's phrasing
“expected=40 entries/42 lines pre-r28 → 41/43 after F12” swaps the labels: 40/42 is the
**post-F12** state (round-28 end / round-29 start), and 41/43 is the **post-F13** state
(round-29 end). r29 ends at 43 lines — confirmed. This also matches the round-29 lesson's
own “40 → 41 entries / 42 → 43 lines” and the README round-28 amendment's “41 lines = 39
entries + 2 comment lines” measured pre-F12.

## 3. How the list is regenerated

- Creation (round-26 wave-1 `ExecExpectedList`): `git ls-files corpus/knowledge/*.md | sort`
  (read-only) → one lane-relative `corpus/knowledge/<entry>.md` per line, plus a 2-line `#`
  header naming the owning instrument and the round; verified by
  `diff <(git ls-files corpus/knowledge/*.md | sort) <(grep -v '^#' corpus/instruments/knowledge-expected.txt)`.
- Round-26 reviewer parity spec: non-comment set == `ls corpus/knowledge/*.md | sort`;
  sorted; no blank/duplicate/CR; every name exists; exact count reported.
- Round-29 fix seat `ExecRecheckAudit` regenerated 40→41 entries / 42→43 lines (lesson).
- **Pitfall (grounded in round-26):** the audit's `expected_mismatch` compares against the
  **tree glob** (`corpus/knowledge/*.md`), not git-tracked files. `git ls-files` omits
  untracked files, so regenerating from `git ls-files` during a wave (before the L1 commits)
  reds the audit: round-26 wave-1 did exactly this (37 listed vs 39 in tree, `unexpected=2`,
  exit 1; fixed in wave-2 with the shell glob). Regeneration this round must use the tree
  glob — `printf '%s\n' corpus/knowledge/*.md | LC_ALL=C sort` (or `ls … | sort`) — so the
  new, still-untracked entry is included.
- Collation note: the committed list matches ASCII/C byte order. Under the current
  `en_US.UTF-8` locale, `sort` emits one inversion (`evidence-dir.md` before `ev-model.md`,
  locale-ignorable `-`), which the round-26 `AttackA6` recorded for the 39-entry state; the
  current 41-entry list is C-ordered. This never affects the audit (set equality, not order),
  but a locale-aware `diff` re-verification shows that one line.

## 4. What must change when `japanese-severity-vocabulary-and-impact-model.md` lands

1. The file `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` must exist in
   the tree (Q1 header `source:`/`verified-at:`/`recheck:` etc. — executor-owned).
2. `corpus/instruments/knowledge-expected.txt` gains exactly one line,
   `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`, inserted between
   `japanese-domestic-disclosure-workflow.md` (currently file line 21) and `mission-control.md`
   (line 22) — the sorted position in both C and locale collation. Result: **44 lines =
   42 entries + 2 comments**. Bump header line 1 to “round 30” (optional; `#` lines are
   ignored by `load_expected`).
3. Before the update the audit reds exactly as round-28 documented: `expect=present
   expected=41 missing=0 unexpected=1 exit=1`. After it: `expect=present expected=42
   missing=0 unexpected=0`; full exit 0 additionally requires the new entry's recheck line to
   pass all frozen + strict limbs (`strict pass=42/42`).

## 5. README appendix convention (R6) and F13 shapes for F14

- R6 (QUALITY.md): an edit to a file other files cite by line number keeps every existing line
  at its number — append at the end, or a same-line suffix. R9: corrections are appended to
  historical records, never silently rewritten. Round-28/29 amendments implement this: the
  coverage map is never edited in place; each round appends a dated section at the end of
  `corpus/README.md` containing the coverage-map row(s) and the frontier row(s) “on the same
  table shape as the frontier above”. F14 must be a new `## Round-30 admission` section
  appended **after** the round-29 section, not inserted into the main map/table.
- F13 appendix shapes (verbatim, read from README lines 258–264):

  Coverage-map block (entry cell uses backticks; row includes `(round 29)`):
  ```
  | Area | Entry | Source basis |
  |---|---|
  | Program severity ladders and reward scales (round 29) | `knowledge/program-severity-ladders-and-reward-scales.md` | S043, S044, S045 — public primary, opened 2026-10-25 |
  ```
  Frontier block (entry cell has **no** backticks; status literally `admitted`):
  ```
  | id | topic | status | entry | sources | next |
  ||---|---|---|---|
  | F13 | Program severity ladders and reward scales | admitted | knowledge/program-severity-ladders-and-reward-scales.md | S043, S044, S045 | Keep each platform's ladder as its own suggested baseline — distinct from CVSS-B and from other programs' reward ceilings; do not generalize a payout scale across programs. |
  ```
  F14 rows must replicate these shapes byte-for-byte: coverage row
  `| Japanese severity vocabulary and the handling-priority model (round 30) | `knowledge/japanese-severity-vocabulary-and-impact-model.md` | S046, S047, S041 — public primary, opened 2026-10-25 |`,
  frontier row `| F14 | Japanese severity vocabulary and the handling-priority model | admitted | knowledge/japanese-severity-vocabulary-and-impact-model.md | S046, S047, S041 | <next prose> |`
  (one space after each `|`; no trailing space; sources cell keeps “S046, S047, S041” order — the same order the harness prints).

## 6. Harness and counter expectations for F14 (context)

- C2 counter (awk) counts README rows with `$4 ~ /^ *admitted *$/`: 13 → 14.
- `frontier-recheck-count.py` at base: rows 16 (F09/F10/F11 each appear twice), `entries=16
  pass=16 exit=0`; with F14 admitted: **entries=17 pass=17 exit=0**, including
  `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S046,S047,S041 exit=0`.
  Harness contract (code-read): entry file must exist; header `source:` id set must equal the
  recheck `--source` id set and be a subset of body-cited ids; recheck line must be a
  `source-recheck.py` invocation with `--manifest` + `--source`; the named round-30 manifest
  must exist with `schema_version=1` and list S046/S047/S041; line must exit 0 from the lane
  root. The frontier row's entry cell may carry or omit backticks (regex ``?([^|`]+?)`?`).
- Sources: staged S049/S050 → lane S046 (IPA JVN activity report PDF) / S047 (IPA JVN
  quarterly registration report) per claims.json assimilation (`staged_rows_adopted`); registry
  rows 45 → 47; S041 already registered (JPCERT/CC 2026 guideline) and cited by F14; census
  stays W04 S028/S029 only (S046/S047 are new rows, no new warnings).

## 7. Observed / inferred split

- Observed (measured): all counts, digests, live audit output, README appendix bytes, harness
  contract lines, registry row count 45, census W04-only, harness 16/16 at base.
- Inferred, not re-verified: the future round-30 manifest content and the F14 entry body
  (executor-owned); adoption ids S046/S047 map (from claims.json `staged_rows_adopted` S049→S046,
  S050→S047).
- Remaining unknowns for the L1: none blocking — the expected-list work is fully specified;
  the new entry's recheck line must clear the strict limbs for the live audit to exit 0.
