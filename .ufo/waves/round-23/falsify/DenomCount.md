# DenomCount — frontier denominator / count audit (round-23 FALSIFY)

**Seat:** L1Kasegi23.DenomCount-2 (leaf; no dispatch).
**Axes attacked:** `depth:verifiability` (is the count an instrument or an assertion?) and `coverage` (8/8, 3/3, duplication, entry existence).
**Mode:** read-only on production bytes. Mutations only in `/tmp/kasegi-r23-falsify-DenomCount/`. No installs, no commits, no index writes.
**Verdict on the measured claim:** the counts **reproduce on landed bytes** (8 admitted of 8, 3 of 3 for F06–F08, zero duplicates, 8/8 entry files present and bound). The defects found are in the *evidence instrument named by the task*, not in the corpus state. No admission or score movement is claimed.

## 1. Exact commands and outputs

Run in `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

```
$ grep -cE '^\| F0[1-8] .*\| admitted \|' corpus/README.md
8
```
```
$ grep -cE '^\| F0[6-8] .*\| admitted \|' corpus/README.md
3
```

Field-exact cross-check (status read as column 3, not as a substring anywhere in the row):

```
$ awk -F'|' '$2 ~ /^ F0[1-8] $/ {s=$4; gsub(/^ +| +$/,"",s); if (s=="admitted") print NR": "$2" -> "s}' corpus/README.md | wc -l
8
$ awk -F'|' '$2 ~ /^ F0[6-8] $/ {s=$4; gsub(/^ +| +$/,"",s); if (s=="admitted") c++} END{print c+0}' corpus/README.md
3
```

The header at `corpus/README.md:193` is `| id | topic | status | entry | sources | next |`, so `status` is field 4 under `-F'|'`; both instruments agree.

Duplication (grep cannot answer this; the ID set can):

```
$ grep -E '^\| F0[1-8] .*\| admitted \|' corpus/README.md | awk -F'|' '{gsub(/^ +| +$/,"",$2); print $2}' | sort | uniq -d
(no output)
dup_count=0  unique_count=8
$ ... | sort -u | diff - <(printf 'F0%d\n' 1 2 3 4 5 6 7 8 | sort)
SET-IDENTICAL
```

Table census: `grep -nE 'F0[1-9]' corpus/README.md` returns exactly `README.md:5` (prose), and rows `195–202`. No `F09+` token exists anywhere under `corpus/README.md` or `.ufo/waves/round-23/`. The table body is bounded by `195–202`; line 203 is blank and 204 is prose (verified with `sed -n '203,214p' | cat -A`), so there is no hidden ninth row and no second frontier table (`grep -rnE '^\| F0[1-8] ' --include=*.md corpus/ .ufo/waves/round-23/claims.json` outside README → empty).

Entry existence and row→entry binding (all 8 rows, `corpus/` as base = README's own directory):

```
rows = 8
F01  status=admitted exists=True  table_src=S001  file_src=S001  bind=True
F02  status=admitted exists=True  table_src=S003  file_src=S003  bind=True
F03  status=admitted exists=True  table_src=S006  file_src=S006  bind=True
F04  status=admitted exists=True  table_src=S009  file_src=S009  bind=True
F05  status=admitted exists=True  table_src=S013  file_src=S013  bind=True
F06  status=admitted exists=True  table_src=S018  file_src=S018  bind=True
F07  status=admitted exists=True  table_src=S030  file_src=S030  bind=True
F08  status=admitted exists=True  table_src=S029  file_src=S029  bind=True
ALL_EXIST_AND_BIND = True
distinct entry paths = 8
```

Sizes/content are not stubs: `3993–5034 B`, `44–77` lines, `540–732` words, and eight distinct `md5sum`s (no row points at another row's content). Each opens with QUALITY.md Q1's three header lines (`source:`, `verified-at:`, `recheck:`) under its H1.

`grep -cE '^\| S0(18|22|24|29|30) ' corpus/SOURCES.md` → all five rows present (30 S-rows total). S018/S029/S030 are `mined` with `used-by` equal to the same entry files the README rows name; S022 and S024 are `queued` with `used-by —`, and S029/S030 each begin `supersedes S024/S022` — internally consistent with the README `sources` cells.

Denominator definition confirmed against the frozen claim, not assumed: `.ufo/waves/round-23/claims.json` C2 says *"Frozen frontier denominator is eight public-practice surfaces: 5/8 to 8/8"* and *"F06-F08 admitted 3/3"*. Measured 8/8 and 3/3 match that after-state; the `before` value `0/3` and the 5/8 baseline are receipts I did not re-execute.

## 2. Findings (severity order)

### D-1 (Medium, verifiability) — the specified regex is column-agnostic and spacing-brittle, so `grep -c = 8` is neither necessary nor sufficient for "8 rows whose *status* is admitted"

Mutations on copies in `/tmp/kasegi-r23-falsify-DenomCount/` (production untouched):

| id | mutation | specified regex | field-exact truth |
|---|---|---|---|
| M1 | `201s/| admitted |/| candidate |/` (demote F07) | 7 | 7 |
| M3 | `200s/| admitted |/|admitted|/` (drop spaces) | 7 | 8 |
| M4 | `195s/| admitted |/| admitted  |/` (extra space) | 7 | 8 |
| M5b | F02 status→`candidate`, `next` cell→`admitted` | **8** | **7** |

M5b row as written: `| F02 | Coordinated-disclosure timelines | candidate | knowledge/coordinated-disclosure-timelines.md | S003, S004, S005 | admitted |`. The regex `^\| F0[1-8] .*\| admitted \|` matches because `.*` spans columns; it never reads the status column. The inverse (M3/M4) shows a genuinely admitted row can be silently dropped from the count by a spacing change. On the current bytes both instruments return 8/3, so the claim is *true* — but any report that offers only the `grep -c` output as proof is offering an instrument that can be wrong in both directions. Load-bearing instrument should be the field-exact read (`awk -F'|' '$4'` trimmed), with the regex as a cheap proxy only.

### D-2 (Medium, coverage) — `grep -c` cannot establish the "no frontier row is duplicated" sub-claim; that sub-claim needs a separate ID-set check

M2: appending `sed -n '202p' corpus/README.md` to a copy yields regex count **9** while unique IDs remain **8**. So a count of 8 does not prove absence of duplication (a duplicate plus a demotion nets back to 8), and a count of 9 does not by itself demonstrate a *distinct* ninth surface. The dedup evidence I published above (`uniq -d` empty, `unique_count=8`, set-identical to `{F01..F08}`, plus 8 distinct content hashes) is the part that actually closes this sub-claim. It passes.

### D-3 (Low, verifiability of the invariant) — the 8/8 property is ungated

`grep -rlnE 'Frontier|admitted|F0[1-8]' corpus/instruments/` returns nothing: no instrument in `corpus/instruments/` (`resolve.py`, `anchorcheck.py`, `density.py`, `source-recheck.py`, `mirror-containment-check.py`, `test_resolve.py`) parses README frontier rows. The "8/8" therefore exists only as a point-in-time manual receipt with no regression detector: a future edit adding `| F09 | … | admitted | knowledge/missing.md |` would not fail any local check. This is a gap in durability, not a defect in the current state.

## 3. Controls that passed — and why they are not defects

- `corpus/README.md:5` names "the five round-22 entries (Frontier F01–F05)". That sentence is scoped to the *round-22 entries' provenance* (S001–S015, 2026-10-19); it is not an admitted-count claim and stays true after F06–F08 admission. Not stale.
- `corpus/README.md:186` ("No new domain knowledge is admitted by this index addition") sits inside the round-21 "Interactive cutover evidence" section and describes that index addition; the round-23 Frontier table does not contradict it. The adjacent correction note at `:191` covers only the QUALITY.md-absence sentence.
- `corpus/QUALITY.md:21` ("the 25 admitted before round 22") concerns legacy entries, not frontier rows.
- No competing frontier table or second copy of F06–F08 rows exists anywhere under `corpus/` or in `claims.json`.

## 4. Residual risk and verification gaps

- **Content adequacy is out of scope here.** Q1 header presence, entry existence and source-ID binding were checked; Q2 (tier support), Q3 (≤25-word located quotes), Q4 (attribution), Q5 (falsifiable rule + rejected over-generalization) and Q6 (documentation-only) for F06–F08 were not re-derived by this seat — sibling seats hold those.
- **`admitted` is a self-declared string.** Nothing validates its vocabulary or requires the row's entry to exist at edit time (D-3); the binding check above is manual.
- **"Entry exists and binds" ≠ "entry is correct."** The md5/size/lines numbers prove non-stub, distinct content, not accuracy of the knowledge.
- **Baseline claim not re-executed.** `c1-baseline.json`'s escape 0/6 and the C2 `before=0/3` were not rerun here (C1 seats own that); the 5/8→8/8 delta's left side is accepted only as the frozen claim text.

## 5. Scope limits

Assessed: `corpus/README.md` frontier table (lines 193–202), the eight `corpus/knowledge/*.md` entry headers/hashes/sizes, `corpus/SOURCES.md` rows S018/S022/S024/S029/S030, `corpus/QUALITY.md`, `corpus/instruments/` inventory, and `.ufo/waves/round-23/claims.json` C2 wording. Not assessed: C1 resolver/mirror containment, source-capture fidelity, lesson/erratum content, other wave receipts.

## 6. Tooling

No installs or updates were made; no package transactions (pacman paused host-wide was not touched). Scratch confined to `/tmp/kasegi-r23-falsify-DenomCount/`.

Scratch durability: this report references **no** `.ufo/waves/round-35/scratch/` path and **no** in-repo scratch file; the only external locus is the `/tmp` directory above, which is ephemeral by nature. Every mutation is reproducible from the `sed`/Python commands recorded in §2 verbatim, and the essential outcomes (regex vs field-exact counts, the M5b row as written) are inlined here rather than left to the copies. Re-validated at `2026-10-25T03:47` while an unrelated external sweep removed `.ufo/waves/round-35/scratch/`: `m1=7/7, m2=9/9, m3=7/8, m4=7/8, m5b=8/7` (regex/field-exact), unchanged from the values reported.
