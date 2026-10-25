# RevRegistryC2 — registry edit review (corpus/SOURCES.md), round 28 wave 1

- Seat: RevRegistryC2 (reviewer, leaf; no dispatches, no installs)
- Reviewed: 2026-10-25T17:26:17Z (UTC), lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, working tree `94f387cb` + uncommitted seat edits
- Base for diff: `c9f8b115a098c65356e4b3b6048af45a37ab8395` (claims freeze, per dispatch)
- State timeline: at first observation (~17:25Z) `git diff c9f8b115… -- corpus/SOURCES.md` was empty (PRE-STATE); ScribeRegistryC2 landed between my two check batches; every check below was (re-)run against the landed bytes at 17:26:17Z. No polling was done — the landing was observed in already-issued parallel calls.

## Verdict

Registry edit **PASS on every grammar item the registry controls**. One open item, not a registry defect: census exit 1 because the F12 entry file (`corpus/knowledge/japanese-domestic-disclosure-workflow.md`, owned by ScribeEntryC2) is not yet on disk. Must be exit 0 at round end (C2 kill rule).

## Frozen grammar checks (all commands run by me, from lane root)

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | 11 columns on the new row (awk NF check) | PASS | `awk -F'|' '/^\| S042 /{print NF}' corpus/SOURCES.md` → `NF=13` = 11 columns (leading/trailing split artifacts are cells 1/13). All 42 data rows: `13` ×42, so no row swallows a pipe. |
| 2 | No literal/escaped pipes in cells | PASS | NF=13 on every row excludes literal pipes; `grep -nE '\\\|' corpus/SOURCES.md` → no matches (no escaped pipe). |
| 3 | kind enum `docs` | PASS | cell[4] = `docs` (census fires no kind E-code). |
| 4 | tier A scoped | PASS | cell[5] = `A`; scope cell[6] is row-specific ("IPA and JPCERT/CC's own intake process … software-product flow (10 steps …), the web-application flow (7 steps) and the vendor own-product flow"), not generic. |
| 5 | status mined | PASS | cell[9] = `mined`. |
| 6 | opened 2026-10-25 | PASS | cell[10] = `2026-10-25` (today, matches frozen claim). |
| 7 | used-by exactly the one entry | PASS | cell[12] = `corpus/knowledge/japanese-domestic-disclosure-workflow.md` — single path, no comma/second entry, exactly the claims-declared F12 entry path. |
| 8 | used-by path exists | **FAIL (mid-wave)** | `test -f corpus/knowledge/japanese-domestic-disclosure-workflow.md` → absent at 17:26:17Z. Owner: ScribeEntryC2 (pending). See Open item. |
| 9 | S042 id not reused (dup check) | PASS | `grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md` → `1`; full-row id scan → `NO_DUP_IDS`. (`.ufo/` round-24/25/26 mentions of S042 are prior-round staged-id history, not registry rows.) |
| 10 | S041 cells byte-identical to base except used-by | PASS | Per-cell diff of row S041 (base vs current): only `cell[12]` differs. old → new: `corpus/knowledge/iso-29147-and-30111-division-of-labour.md, corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` → same + `, corpus/knowledge/japanese-domestic-disclosure-workflow.md`. Cells 1–11,13 byte-identical. |
| 11 | Diff shape: exactly one added row + one used-by cell change + log lines | PASS | `git diff --numstat c9f8b115… -- corpus/SOURCES.md` → `4 1`; 2 hunks. Hunk 1 `@@ -44,7 +44,8 @@`: −old S041 row, +new S041 row (used-by only), +S042 row. Hunk 2 `@@ -74,3 +75,5 @@`: exactly 2 `## Registry changes` log bullets ("- S042 row added: …", "- S041 used-by cell old → new: …"); the log's old-value prefix matches the verified cell diff. No other line touched. |

## Census CLI (paste, 2026-10-25T17:26:17Z)

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	E11	S041 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
kasegi	E11	S042 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
census_exit=1
```

- W04 ×2 are the pre-existing baseline (S028/S029 rows untouched by this diff; known since round 23/24 receipts).
- E11 ×2: census script line 566–568 fires E11 when `! -e "$dir/$path"` — both errors name the same missing file, the F12 entry (ScribeEntryC2's file). This is the only failing grammar item and it is outside the registry writer's control.

## Open item (severity: blocker for C2 round-end, owner ScribeEntryC2)

1. `corpus/knowledge/japanese-domestic-disclosure-workflow.md` absent on disk at 17:26:17Z → census exit 1, E11 on S041 and S042. C2 kill rule fires if census exit ≠ 0 at round end.

Exact re-run command for L1 after the entry lands:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
```

Expected post-landing: only the two pre-existing W04 lines, `census_exit=0`, rows 42.

## Residual risk / verification gaps

- I reviewed the registry edit only; manifest Q9 quote assertions, recheck executability, README F12 row, and harness 15/15 are other seats and were not judged here.
- The diff's log bullets were verified by line classification + 200-char prefix; the S041 old→new recorded above comes from the authoritative per-cell diff, which the log bullet prefix matches.
- One intermediate S041 cell-diff attempt errored on a lost temp file (`diff: /tmp/tmp.Pr3T5d7n6V/cur.txt: No such file or directory`, exit 2 — shell glitch, not a data finding); rerun via process substitution succeeded and is the evidence cited.
- Tooling: nothing installed or upgraded (pacman untouched).
- No edits made to any production file; this receipt is my only write.
