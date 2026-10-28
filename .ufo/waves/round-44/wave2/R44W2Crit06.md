# R44W2Crit06 — frontier-step attack (§2b: census pair, mined mistake, sourced claim)

Tree under attack: `8063547d0ce647d6f9eafc3c8d0a502616685218` (= lane HEAD; working tree identical for every file cited below — `git diff --stat 8063547 -- <cited files>` is empty). Base: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`. All evidence below is from committed bytes re-extracted with `git archive` into seat scratch and from read-only commands in the lane/fleet repos.

## Verdicts

| §2b item | Verdict |
|---|---|
| 1. Census before → after pair | **PARTIALLY FALSIFIED** — the after half is real; the before half is theatre (uncommitted, post-commit, false provenance sentence, and zero discriminating power) |
| 2. One mined mistake | **HOLDS** — could not falsify; 8 mistakes, every checked receipt and instrument reproduces on committed bytes |
| 3. ≥1 sourced claim on a row opened this round | **HOLDS** — could not falsify; S069 row, entry, capture, and reconstruction all verify |

---

## Item 1 — census before/after pair: PARTIALLY FALSIFIED

**What is genuine.** The receipt-exact command re-run on the real tree reproduces the committed after-receipt byte-for-byte:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

identical to committed `.ufo/waves/round-44/controls/sources-census-after.txt`.

**Falsification F1 — the before half cited by the committed tree does not exist in it.** Committed `corpus/lessons/round-44.md:135-138` (§Frontier step) claims "exit 0 at both ends of the round (receipts `controls/sources-census-before.txt` and `controls/sources-census-after.txt`)". But:
- `git cat-file -e 8063547:.ufo/waves/round-44/controls/sources-census-before.txt` → fails; `git ls-tree -r 8063547 -- .ufo/waves/round-44/controls/` does not list it.
- `git log --all --oneline -- .ufo/waves/round-44/controls/sources-census-before.txt` → empty: **no commit ever carried it**. It is untracked in the working tree.
- LOG.md:1972 claims a before/after pair for attempt 1 too; no successful before-census receipt for attempt 1 exists in any commit either. The only committed before-half artifact is `controls/census-invocation-error.txt`, an exit-2 wrong-root run that validated no registry.

**Falsification F2 — the on-disk before receipt's provenance sentence is false against committed bytes.** Untracked `controls/sources-census-before.txt:8` says: "The same command, re-run at the start of attempt 2 (the registry had not moved since attempt 1's commit 6631401)". Committed bytes contradict the parenthetical:
- `git show 6631401:corpus/SOURCES.md | grep -c S069` → **0** (68-row registry, no S069/S070).
- `git ls-tree 6631401 --name-only -- corpus/source-snapshots/round-44/` → empty; `git show 6631401:corpus/README.md | grep -c F26` → 0.
- The entire corpus movement (S069, S070, snapshot, manifest, entry, F26 row, 68→70 rows, 62→63 entries) lands **first in 8063547** — the very commit carrying the lesson. A census validating a registry "unchanged since 6631401" cannot also describe the registry that this round committed.

**Falsification F3 — sequencing.** Commit 8063547: `2026-10-28T16:58:53-03:00`. `sources-census-before.txt` mtime: `2026-10-28 17:02:34 -0300` — written ~4 min **after** the landing commit, between `wave2-spec.json` (16:59:57) and `wave2-dispatch.json` (17:00:31)+3 min, i.e. during wave-2 dispatch, labelled "BEFORE (attempt-2 round start)". (mtime proves last write, not first creation; but F1 already makes the before half unauditable from the committed tree regardless.)

**Falsification F4 — the pair has zero discriminating power even if fully committed.** Re-ran the census on `git archive` exports of base and commit (synthetic root: fleet `shokunin.conf` copy + `kasegi-shokunin` symlink to each export):

```
$ sources-census.sh validate --root <root-of-5ab3a60-export> kasegi   → W04 S028, W04 S029, ok, exit=0
$ sources-census.sh validate --root <root-of-8063547-export> kasegi   → W04 S028, W04 S029, ok, exit=0
```

Byte-identical except the path echoed in the `ok` line. Validate-mode output is invariant across the 68→70 movement (both W04 rows are pre-existing), so **no** census pair of this shape could witness the round's source work; both halves were guaranteed to print the same three lines.

**Smallest safe correction:** commit the before receipt with a corrected provenance sentence (or drop the before-half claim from the lesson/LOG), and record that the census validates shape, not movement — the movement's witnesses are the row-count greps (68→70, 62→63) and `frontier-recheck-count.py`, which do discriminate and do reproduce (below).

## Item 2 — mined mistake: HOLDS (not falsified)

Committed `corpus/lessons/round-44.md` carries `## Mistakes` (M44-1…M44-6) and attempt-2 `### Mistakes` (M44-7, M44-8), each with captured-by, correction, and a fail-closed-evidence column. Every cited artifact exists at 8063547 and the instruments reproduce on the committed export:

- M44-1: `controls/census-invocation-error.txt` committed; wrong-root invocation re-run → `ERROR: config not found`, exit 2 ✓ (second ERROR line wording differs from the receipt — my scratch root does not end in `*-shokunin`, which the script's lane detection keys on; exit code and first error identical; fleet script unchanged since `f47ad6ba` 2026-10-25).
- M44-3: re-ran the frozen C2 greps: base `0 68 62`, after `0 70 63` — exactly what committed `controls/c2-frozen-counter-replay.txt` records ✓.
- M44-4/M44-7: draft counter absent from `corpus/instruments/` at 8063547; `controls/r44-counter-trial-disposition.txt` committed ✓.
- M44-5: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069` → `sha256 OK`, Q1–Q5 OK, exit 0, matching committed `controls/S069-source-recheck.txt` ✓.
- M44-2/M44-6: entry `recheck:` line has the cadence after the command; `frontier-recheck-count.py --root <export>` → `entries=29 pass=29 exit=0` ✓; `wave1/R44Critic2.md` is 137 lines, so the cited `:21-93` span exists ✓.

Minor conformance nit (not theatre): template §2b.3 asks for "class · evidence pointer · captured-by · fix"; the table has no explicit class field — pointers are embedded in the Error/fail-closed columns. Substantively met.

## Item 3 — sourced claim on a row opened this round: HOLDS (not falsified)

- `corpus/SOURCES.md:75` (committed): S069, kind docs, **tier A**, teaches-cell, quote-cell, used-by `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`, status `mined`, **opened 2026-10-28** (= round day; claims frozen 2026-10-28), recheck `180d`; NF=13 (well-formed). Row is an append: `git diff 5ab3a60 8063547 -- corpus/SOURCES.md` shows additions only; **no pre-existing row's status/recheck/used-by changed** ✓.
- The C2 claim rests on it: the entry's first line is `source: S069 — https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules — …` ✓.
- Gate quote: "The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services." = 13 words (≤25), located at `corpus/source-snapshots/round-44/S069.txt:61-62` ✓ (verified in capture bytes).
- Capture authenticity: capture sha256 `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2`, 45,681 B / 1,132 lines — matches the registry row; and the lesson's reconstruction command reproduces it **byte-identically** from the committed raw API JSON:
  `jq -r '.body' .ufo/waves/round-44/source-recon/S069.txt | sha256sum` → same digest, `cmp` IDENTICAL ✓.
- Every entry line-citation resolves: 10-11 (scope sentence), 61-62 (strict limit), 62-63 (prohibition), 65-72 (written authorization / ineligibility), 68-69 (customer domains), 76-77 (customer IP ranges: "Finding a Google-owned asset inside a customer IP block … still considered unauthorized testing within customer space" — counted: exactly the 21 words the entry claims), 78-87 (local reproduction, not live multi-tenant) ✓. The README:632 correction's novel-ground claim is accurate to those lines.
- Live drift honestly disclosed in committed `controls/S069-live-drift.txt` (live 200/47,203 B vs pin 45,681 B, formatting-only diff), the row, and the lesson.

Minor note: `S069-live-drift.txt` cites the live-body half by a scratch path (`/fast/scratch/hyaku/kasegi-r44/round44-l1-source-live/live-body.txt`) that is not committed, so the drift comparison's live side is not auditable from the tree; the disclosure is conservative and the pin side fully verifies.

## Limits

- I could not determine when the before-census command was first executed (receipts record output, not time); my findings are about what the committed tree can audit, which is: not the before half.
- Validate-mode invariance (F4) means no census pair could ever witness the movement; I did not audit whether other §2b obligations outside my three-item scope (e.g. S070's flip condition wording) are optimal.
- No tool installed or updated; no pacman usage. Scratch `/fast/scratch/hyaku/kasegi-r44/R44W2Crit06` removed before yield.
