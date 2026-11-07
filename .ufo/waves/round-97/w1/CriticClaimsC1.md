# CriticClaimsC1 — round-97 w1 — C1 attack (tranche 12, 33 qualify-lane rows)

Seat: CriticClaimsC1 (leaf). Working dir `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; scratch `/fast/scratch/hyaku/kasegi-r97/CriticClaimsC1` (removed after the seat). Base `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`, freeze `daf7fc6a627d615178c27594110e956e592e4cd9`, C1 landing `75a471809cba265c8981ece1c0ed29c7895d9308`.

Pins observed in the lane working tree and at the freeze, all equal to `claims.json`:

| artifact | sha256 |
|---|---|
| `.ufo/waves/round-97/c1/knowledge-meter.py` | `a56198d00505cb81cb971b959aa32f4c917c74c48bf1f482521d7c50e8bb57da` |
| `.ufo/waves/round-97/c1/repair-map.tsv` | `f4ed7387ca08146e1426e22d7ad3a3c60082a53ae77b9556351ffaade0783c0c` |
| `.ufo/waves/round-97/c1/labels.tsv` (also at `daf7fc6`) | `5155959d4cea88bde7f44c0590f007731700a3072faa93f8ecbbd16410ffc853` |
| `.ufo/waves/round-97/controls/c1-controls-r97.py` | `471feda7032ffb28c666c6c6c1b22e4e0a0d9fd9052dcdb7dea386bd88cbe1fb` |

`corpus/instruments/resolve.py` is byte-identical at base and landing (blob `4d578e5592f8f8fe1661ed03daca09fffb818cb0`), so the census semantics are revision-stable.

## Verdict

**C1 STANDS on P1, P2 and P3 — re-derived independently, not merely re-run.** P1: the frozen meter prints `KNOWLEDGE-METER-RESULT pass rc=0` with M0 `1040/2041`, M1 `1043/2035`, M3 `same_files=True bad_lines=0 old_not_once=0 dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M9 `rows=33 unbound=none`, M10 `labelled=33 want=33 mapped=33 kinds=qualify-lane=33 unknown=none unapplied=none unlabelled=none`, M6 the frozen map sha, `after_rev=75a4718…`. My own census (fresh implementation, own token extraction, own classification driver) reproduces `1040/2041 -> 1043/2035`; my own map application reproduces all 16 landing files byte-for-byte; my own label binding reproduces all 33 rows. P2: the 14-control harness, re-run at the landing, prints `C1-CONTROLS-RESULT pass controls=14` and `ATTRIBUTION pass fixtures=13`, and every `CONTROL` line's `limbs=` equals its `declared=` (14/14, including the `candidate` positive with `declared=-`). P3: `git diff --name-only base..landing -- corpus/knowledge` prints exactly the sixteen files the map names; `SKILL.md` is byte-identical base..landing; the landing commit itself changes only those sixteen files (30 insertions / 30 deletions).

**P4 is not in `claims.json`.** The C1 `predicate` string contains P1, P2 and P3 only; the seat spec's "P1-P4 are in claims.json" is not satisfied. I cannot score a predicate that is not frozen. Routed as Q3 below; the round-94 P4 concern (a control before-fixture cloning the mutable live lane) is structurally addressed by the round-97 harness, whose `fixture(cand, …)` clones the candidate, not `LANE`.

Per-limb: **P1 STANDS** (M0 `1040/2041`, M1 `1043/2035`, M3 `bad_lines=0 old_not_once=0 dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M9 `rows=33 unbound=none`, M10 `labelled=33 want=33 mapped=33 kinds=qualify-lane=33`); **P2 STANDS** (14 controls, 13 attribution fixtures, every `limbs=` equals its `declared=`, 14/14); **P3 STANDS** (exactly the sixteen `corpus/knowledge` files; `SKILL.md` byte-identical); **P4 NOT-VERIFIED** (absent from `claims.json`; routed Q3, not a claim failure).

**One counter defect is routed, not a verdict change.** The frozen data satisfies the claim's statement (I verified the same-name binding independently: every label is exactly `corpus/instruments/<key>`), but the counter's M4 qualify-lane branch does not enforce that binding. A fixture that qualifies `resolve.py` to `corpus/instruments/density.py` — the wrong instrument — passes every limb with rc=0. See "Counterexample" below. This is a fixable counter-completeness defect; it does not re-score C1 because the landing's 33 labels are all same-name and I verified them myself.

## P1 — per-limb, my own numbers

Meter command (receipt `01-meter-landing.txt`, rc=0):

```
python3 -B .ufo/waves/round-97/c1/knowledge-meter.py --lane <clone-landing> \
  --base-rev b06af5e07efbd961a8449f7de6b57eeea62c6bd3 \
  --after-rev 75a471809cba265c8981ece1c0ed29c7895d9308 \
  --map .ufo/waves/round-97/c1/repair-map.tsv --labels-rev daf7fc6a627d615178c27594110e956e592e4cd9 \
  --base-target 1040/2041 --target 1043/2035 \
  --map-sha256 f4ed7387ca08146e1426e22d7ad3a3c60082a53ae77b9556351ffaade0783c0c --work <scratch>
```

Observed: `LIMB M0 pass base=1040/2041`, `M1 pass after=1043/2035`, `M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0`, `M4 pass bad=none`, `M5 pass out_of_range=none`, `M9 pass rows=33 unbound=none`, `M10 pass labelled=33 want=33 mapped=33 kinds=qualify-lane=33 unknown=none unapplied=none unlabelled=none`, `M6 pass sha256=f4ed7387…`, `KNOWLEDGE-METER-RESULT pass rc=0`.

### M0/M1 — independent resolver census (receipt `02-independent-census.txt`)

I extracted both trees with `git archive`, re-implemented the token rule from `resolve.py`'s source (`TOKEN`/`is_pathlike`), counted distinct tokens over `corpus/knowledge/*.md` (105 files at both revisions), and classified each with the pinned `resolve.py` loaded from the base tree (mirror absent). My numbers:

```
CENSUS base=1040/2041 after=1043/2035
COLLECT base mine=2041 collect=2041 equal=True
COLLECT after mine=2035 collect=2035 equal=True
GONE base=1001 after=992
REMOVED 9   (all nine bare basenames, all GONE at base)
ADDED 3     (corpus/instruments/{density,resolve,source-recheck}.py, all INTERNAL)
FLIPS 0
```

Removed (occurrences in the base scope): `anchorcheck.py` 6, `capture-secret-scan.py` 2, `capture-source.py` 5, `claim-package-check.py` 1, `density.py` 2, `r35-defect-closure.sh` 1, `r36-closure.sh` 2, `resolve.py` 5, `source-recheck.py` 9 — **33 occurrences, exactly the 33 map rows**. Added: `corpus/instruments/density.py` 2, `corpus/instruments/resolve.py` 5, `corpus/instruments/source-recheck.py` 9. The six other qualified targets (`anchorcheck.py`, `capture-secret-scan.py`, `capture-source.py`, `claim-package-check.py`, `r35-defect-closure.sh`, `r36-closure.sh`) were already INTERNAL tokens in the base scope, so they contribute 0 to the denominator. Arithmetic: `2041 − 9 + 3 = 2035`; `1040 + 3 = 1043`; `1001 − 9 = 992`. The claim's "+3 new / six already existed" decomposition is exact. My token set equals `resolve.collect` restricted to the knowledge files at both revisions (`equal=True`), so the census is not an artifact of my extractor.

### M3 — map applied by hand (receipts `02`, `03`, `11`)

I applied `repair-map.tsv` to my base extract line-by-line (`old` -> `new` per mapped line) and compared bytes to my landing extract: `APPLY bad_lines=0 old_not_once=0 rows=33`. Shape: `rows=33 lines=30 files=16 keys=9 targets=9`; the file set equals the `git diff --name-only base..landing -- corpus/knowledge` set (`file_set_equal_diff=True`, no missing, no extra). Per-row multiplicity: every `old` occurs exactly once on its base line (`multiplicity_bad=0`), so the 33 rows are 33 edits, not a replace-all over-count. The three two-row lines are `capture-intake-gate.md:11`, `considerthese-proposals-ledger.md:125`, `root-loss-2026-10-12.md:54` — all with different keys.

### M9/M10 — label binding (receipts `06`, `12`)

`labels=33 map_rows=33`; `unmapped_labels=0`; `BINDING bad=0`. For every row: `old == "`<key>`"`, `new == "`<label>`"`, `label == "corpus/instruments/" + key`, `key` has no `/` or `:`. All 33 `fix` cells are exactly `Qualify to <label>` (`fix_mismatch=0`), and every evidence cell names its target (`evidence_no_target=0`). This is the same-name binding the counter's M4 does **not** enforce — see the counterexample.

### P2 — controls re-run at the landing (receipts `05`, `15`)

Harness command (rc=0):

```
python3 -B .ufo/waves/round-97/controls/c1-controls-r97.py <clone-landing> \
  daf7fc6a627d615178c27594110e956e592e4cd9 \
  .ufo/waves/round-96/c1/knowledge-meter.py <scratch>/ctl <scratch>/out
```

Observed: `C1-CONTROLS candidate=75a4718… base=b06af5e… freeze=daf7fc6…`, then 14 `CONTROL` lines, then `ATTRIBUTION pass fixtures=13`, `C1-CONTROLS-RESULT pass controls=14`. I compared the 14 `(name, rc, want, PASS/FAIL, limbs, declared, attribution)` tuples against the committed receipt `.ufo/waves/round-97/controls/c1-controls-r97.txt`: `CONTROL-LINE-MATCH True` (14/14); `ATTRIBUTION-FIXTURES 13`; `ALL-LIMBS-EQ-DECLARED True`. The negative fixtures' failing sets are exactly the declared sets: `do-nothing M1,M3`; `wrong-map-sha M6`; `extra-unlisted-edit M3`; `r96-no-qualify-branch M4,M5,M9,M10`; `qualify-target-missing M4,M5`; `qualify-key-not-bare M4,M5`; `map-not-label M4,M5,M9`; `unknown-kind-row M10`; `unlabelled-only M9,M10`; `unapplied-only M10`; `duplicate-row M3`; `snapshot-missing-only M4,M5`. The `missing-labels` control is rc=2 with no declared set (not an attribution fixture). The `candidate` positive has `declared=-` and no failing limb. The harness's fixtures clone the candidate (`fixture(cand, …)` -> `clone(cand, dest)`), so the round-94 live-lane-clone concern does not recur; the only live-lane reads are the pinned map, labels, meter and r96 paths.

### P3 — path set (receipt `14`)

`git diff --name-only base..landing -- corpus/knowledge` prints exactly the 16 files the map names (`count=16`, set equality checked in receipt `11`); `git diff --quiet base..landing -- SKILL.md` rc=0 (byte-identical); `git show --stat 75a4718` is 16 files, 30 insertions, 30 deletions, all under `corpus/knowledge/`; the freeze (`b06af5e..daf7fc6`) and redaction (`daf7fc6..b3c2aff`) commits change 0 knowledge files, so the base-to-landing knowledge delta is exactly the tranche.

## Semantic core — is each bare token the lane's instrument at its site?

I dumped all 33 base lines with two lines of context (receipt `04`) and the token neighbourhoods (receipt `07`). Every one of the 33 sites is Markdown prose or a table cell; **none is inside a fenced code block** (`fenced=False` for all 33). The nine basenames are the lane's instruments, not lost-tree paths and not quoted fields:

- `capture-source.py` / `capture-secret-scan.py` — the capture writer and the scanner; the sites say "normalized by the lane's …", "the scanner whose shapes are imported", "the gate inherits each through `patterns()` without a change to …". `capture-secret-scan.py` imports `SECRET_PATTERNS` from `claim-package-check.py` (`return tuple(mod.SECRET_PATTERNS)`, `def patterns()`), matching the `cloud-signed-url…:69` site.
- `anchorcheck.py` — the verdict printer; the sites say "`LOST-RECORDED` under …", "prints `0 bad`", "reports `BASE-ABSENT`". The instrument contains `LOST-RECORDED` and `BASE-ABSENT`.
- `resolve.py` — the census; the sites say "GONE+synthetic under …", "SKILL.md resolvability", "lane total". The instrument has `collect`/`classify`/`MIRROR`.
- `source-recheck.py` — the manifest re-checker; the sites say "reports 54/54 OK", "accepts one `--source` per invocation", "prints `occurrences=2 anchor=N-ok`". The instrument has `--source` and the quote checks.
- `density.py` — the density measurement; the two sites are table rows under an `instrument` header ("file mean over `SKILL.md`", "path-citation instances"). The instrument prints `mean dens`.
- `claim-package-check.py` — the `SECRET_PATTERNS` source; the site says "imported from … beside the instrument". The file defines `SECRET_PATTERNS`.
- `r35-defect-closure.sh` / `r36-closure.sh` — the quiescence gate and its porcelain half; the sites say "prints `closed=7/7 exit=0`" and "E9(b)". The scripts carry `closed=K/7 exit=0|1` and the E9 checks.

No site is a lost-tree path: the lost-tree/lost-base tokens in the same sentences (`docs/*`, `claims/*`, `status.json`, `INGESTION.md`, `fleets/*`, the `[lost-tree]`/`[lost-base]` prefixes) are untouched. The one quotation is `first-psirt-maturity-document.md:68`, which quotes line 11 in the present tense; line 11 was edited in the same commit, and I verified the quoted substring `"`corpus/instruments/source-recheck.py` reports 54/54 OK (S100 44, S101 10)"` is present on both lines at the landing — the quote still matches its target, and the superseded count is unchanged.

Targets: all nine `corpus/instruments/<name>` paths are tracked at the landing, outside `.ufo/`, classify `INTERNAL`, and each basename is **unique** among tracked non-`.ufo` paths (`same_basename=[corpus/instruments/<name>]`), so there is no duplicate-authority ambiguity (receipt `06`). The bare tokens are `GONE` at base for all nine; the qualified paths are `INTERNAL` at base and landing (receipt `08`).

Cross-file quotations: I searched all 6,243 tracked `.md` files outside `corpus/knowledge` for a 45-character window around each edited token. 147 hits, **all under `.ufo/`** (historical wave receipts and fixture copies), **0 in live corpus files** (receipt `10`). The landing does not break a live quotation. The tracked generated report `corpus/instruments/citation-survival.md` is unchanged base..landing (same blob `9175840c…`) and was last updated at round-57 (`e300ad5`); its staleness is pre-existing, not caused by this landing, and it is excluded from the meter's `collect`.

## Counterexample — the counter accepts a wrong-instrument label (routed, not a verdict change)

The claim's statement says "Each edit replaces one bare backticked lane-instrument basename with its tracked `corpus/instruments/<name>` path". The counter's M4 qualify-lane branch checks only `old == "`<key>`"`, `new == <label>`, `key` bare, target not `.ufo/`, target tracked, target `INTERNAL`; M9 checks only that the map row equals the label's named edit. Neither checks `label == "corpus/instruments/" + key`.

I built the strongest local counterexample: a clone of the landing with one label and its map row changed from `corpus/instruments/resolve.py` to `corpus/instruments/density.py` for `citation-bases.md:65`, and the landing line changed to match (`resolve.py` -> `corpus/instruments/density.py`). The fixture commit is `bfdfae1aeac16090acb931f7663044df84854a6d`; the meter was run with `--after-rev bfdfae1… --labels-rev bfdfae1… --map <fixture map> --target 1043/2035`.

Result (receipts `09`, `16`): **`KNOWLEDGE-METER-RESULT pass rc=0`**, with M0 `1040/2041`, M1 `1043/2035`, M3 `bad_lines=0 old_not_once=0 dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M9 `rows=33 unbound=none`, M10 `labelled=33 want=33 mapped=33 kinds=qualify-lane=33`. The rate is unchanged because `corpus/instruments/resolve.py` is still added by the other four `resolve.py` rows and `corpus/instruments/density.py` by the two `density.py` rows, so the token set is identical. The fixture's evidence cell even still says "the tracked instrument is corpus/instruments/resolve.py" — the counter ignores the evidence column.

This is a **counter-completeness defect**, not a false claim: the landing's 33 labels are all same-name (my receipt `06`), so the landing's statement is true. But the frozen predicate would not catch a wrong-instrument label, and no existing negative fixture exercises that shape (`qualify-target-missing` uses a nonexistent target; `qualify-key-not-bare` uses a key with a separator; `map-not-label` uses a map/label mismatch).

Impacted axes: `depth:verifiability` (counter strength); `coverage` is not affected by C1. Smallest safe correction: in `knowledge-meter.py`'s M4 qualify-lane rejection condition add `or target != "corpus/instruments/" + key` (equivalently `os.path.basename(target) != key`), and add a negative control fixture "qualify-wrong-instrument" (label names a different tracked instrument) with `declared=M4` (M5 follows M4). The correction would not change the landing's verdict — every frozen label satisfies the added check — so it is a hardening for a future freeze, not a re-score. Because the counter is frozen at `a56198d0…`, the correction cannot be applied to this claim's counter after landing; it is routed for the next freeze.

Secondary code observation (not demonstrated with a fixture): M3's forward substitution uses `b.replace(old, new)` (replace-all) and only checks `b.count(old) < 1` (absence), not multiplicity. The frozen data is safe — my per-row check shows every `old` occurs exactly once on its base line — but a map row could under-count a line with two occurrences of the same token and M3 would still pass. The same-name hole above is the stronger finding.

## Routed qualifiers (no verdict change)

- **Q1 — `claims.json` C1.surface says "12 corpus/knowledge files"; the statement, map, diff and landing stat say sixteen.** I confirmed the surface string contains "in 12 corpus/knowledge files" and the map/diff have 16 distinct files. The predicate does not read the surface field. Routed defect: the surface text should say sixteen (or "tranche 12" if the 12 is a tranche number).
- **Q2 — the statement's "(-6 denominator)" parenthetical mis-attributes the arithmetic.** Measured decomposition: base scope 2041 = 2032 common + 9 bare GONE; landing scope 2035 = 2032 common + 3 new INTERNAL; 0 class flips. The −6 is the net of −9 bare rows leaving and +3 qualified rows entering; the six already-existing qualified targets contribute 0, not −6. The net numbers (`1043/2035`) are right; the causal phrasing is compressed. Routed textual qualifier.
- **Q3 — P4 is absent from `claims.json`.** The C1 predicate has P1-P3 only; the seat spec's "P1-P4" is not satisfied. The round-94 P4 concern (before-fixture cloning the mutable live lane) is structurally addressed by the round-97 harness's `fixture(cand, …)`; the harness's live-lane reads are the pinned map, labels, meter and r96 paths. If the intended P4 was "the controls reproduce after the landing", P2's re-run covers it (14/14, 13 attribution). Routed spec/claims mismatch.
- **Q4 — the committed control receipt's `candidate=f410e91f…` and `freeze=2059fcb…` are scratch objects absent from the lane object store.** I could not replay the pre-freeze candidate at those exact revs; the post-landing replay at `75a4718`/`daf7fc6` is the reproducible half, and its 14 `CONTROL` lines match the receipt's tuples exactly. Provenance caveat, not a predicate failure.
- **Q5 — the meter's rate is host-dependent if the bounty mirror is present.** The meter prints `mirror_absent=True`; both mirror candidates are absent on this host and `KASEGI_MIRROR` is unset. The predicate does not pin `mirror_absent`, so a host with the mirror would need the same `mirror_absent=True` note to reproduce `1040/2041 -> 1043/2035`. Reproducibility caveat; the recorded reading is self-describing.
- **Q6 — row 12's evidence says "the instrument whose header comment is quoted"; the sentence states the pin-declaration form (`pin: SKILL.md fc6d398` inside an HTML comment), not a quoted header comment.** Instrument identity is right; cosmetic evidence wording.
- **Q7 — `corpus/instruments/citation-survival.md` is not regenerated.** It is unchanged base..landing and was last updated at round-57; its counts are pre-existing stale, not a C1 regression, and it is excluded from the meter's scope. Noted for completeness, not routed as a C1 defect.

## Receipts

All under `.ufo/waves/round-97/w1/CriticClaimsC1-receipts/`. Commands were run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` with `TMPDIR=/fast/scratch/hyaku/kasegi-r97/CriticClaimsC1`; the lane git state was read-only; fixture clones were asserted with `git rev-parse --show-toplevel` before any commit.

| # | command | observed | file |
|---|---|---|---|
| 01 | `python3 -B .ufo/waves/round-97/c1/knowledge-meter.py --lane <clone-landing> --base-rev b06af5e… --after-rev 75a4718… --map .ufo/waves/round-97/c1/repair-map.tsv --labels-rev daf7fc6… --base-target 1040/2041 --target 1043/2035 --map-sha256 f4ed7387… --work <scratch>/work` | rc=0; 12 lines; M0-M10 pass; `KNOWLEDGE-METER-RESULT pass rc=0` | `01-meter-landing.txt` |
| 02 | `python3 -B <scratch>/census.py <clone> <base-extract> <landing-extract> .ufo/waves/round-97/c1/repair-map.tsv` | rc=0; `CENSUS base=1040/2041 after=1043/2035`; removed 9, added 3, flips 0; `APPLY bad_lines=0 old_not_once=0 rows=33` | `02-independent-census.txt` |
| 03 | per-row `old` occurrence count on the base line | rc=0; `rows=33 multiplicity_bad=0` | `03-map-multiplicity.txt` |
| 04 | base site lines with ±2 context, all 33 rows | rc=0; 30 site headers, 180 lines | `04-site-lines.txt` |
| 05 | `python3 -B .ufo/waves/round-97/controls/c1-controls-r97.py <clone-landing> daf7fc6… .ufo/waves/round-96/c1/knowledge-meter.py <scratch>/ctl <scratch>/out` | rc=0; 14 `CONTROL` lines all PASS; `ATTRIBUTION pass fixtures=13`; `C1-CONTROLS-RESULT pass controls=14` | `05-controls-landing.txt` |
| 06 | label/map/target binding check (33 labels, 33 rows; tracked/non-.ufo/INTERNAL; basename uniqueness) | rc=0; `BINDING bad=0`; nine targets tracked, non-.ufo, INTERNAL, unique | `06-label-binding.txt` |
| 07 | token neighbourhoods + fence state for all 33 rows | rc=0; 33 rows, `fenced=False` on every one | `07-site-neighborhoods.txt` |
| 08 | nine-token table: bare/qualified presence and classification at base/landing | rc=0; bare GONE at base, absent at landing; qualified INTERNAL at base and landing | `08-nine-token-table.txt` |
| 09 | meter on the wrong-instrument fixture (`--after-rev bfdfae1… --labels-rev bfdfae1… --map <fixture map>`) | rc=0; all limbs pass; `KNOWLEDGE-METER-RESULT pass rc=0` | `09-wrong-instrument-fixture.txt` |
| 10 | cross-file quotation scan (6,243 non-knowledge `.md`, 45-char windows) | rc=0; 147 hits, all `.ufo/`, 0 live | `10-cross-file-quotes.txt` |
| 11 | map shape and file-set equality vs `git diff --name-only base..landing -- corpus/knowledge` | rc=0; `rows=33 lines=30 files=16 keys=9 targets=9`; `file_set_equal_diff=True` | `11-map-shape.txt` |
| 12 | label `fix`/evidence consistency | rc=0; `rows=33 fix_mismatch=0 evidence_no_target=0` | `12-label-fix-evidence.txt` |
| 13 | `sha256sum` of counter/map/labels/harness; `git show daf7fc6:labels.tsv \| sha256sum`; `git cat-file -t` of the three revs | rc=0; all four pins equal claims.json; labels at freeze equal the pin; three revs are commits | `13-pins.txt` |
| 14 | `git diff --name-only b06af5e..75a4718 -- corpus/knowledge`; `git diff --quiet … -- SKILL.md`; `git show --stat 75a4718`; freeze/redaction knowledge diffs | rc=0; 16 files; SKILL.md rc=0; 16 files/30+/30−; freeze=0, redaction=0 | `14-p3-paths.txt` |
| 15 | compare the 14 `CONTROL` tuples with the committed receipt | rc=0; `CONTROL-LINE-MATCH True`; `ATTRIBUTION-FIXTURES 13`; `ALL-LIMBS-EQ-DECLARED True` | `15-control-line-compare.txt` |
| 16 | wrong-instrument fixture diff vs the landing + meter output | rc=0; 3 files changed (labels, map, one knowledge line); meter pass | `16-wrong-instrument-diff.txt` |

Scratch `/fast/scratch/hyaku/kasegi-r97/CriticClaimsC1` (clones, extracts, fixture, work dirs, census script) was removed after the receipts were written; nothing of this seat outlives it. No tools were installed or upgraded. No credential values appear in this report or its receipts.
