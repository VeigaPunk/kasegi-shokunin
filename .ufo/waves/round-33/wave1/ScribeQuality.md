# ScribeQuality — round 33 (kasegi)

- Seat: `ScribeQuality`, role scribe, axes `depth:verifiability`, `coverage`, milestone round-33.
- Answering model (rule 10, from the session route table, not passed by me): `opencode-go/deepseek-v4.1-flash`.
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`; lane HEAD at seat start `a6a502351bb90c8cd6d9b8f45f55109b7848e0d1`.
- Write scope used: `corpus/QUALITY.md` (append-only) and this receipt. No other path written.
- Tooling: nothing installed, nothing upgraded (rule 5 unused).
- Scratch: none created — no clone, mirror, work tree or fixture was needed; every measurement below is `git`/`python3` read-only over the lane (rule 12 satisfied trivially).
- No git/jj mutation run (rule 4); read-only `git rev-parse`, `git show`, `git ls-tree`, `git cat-file`, `git diff --numstat`, `git status --porcelain` only. No `/home/vgpnk/Projects/shokuknow` write, no campaign tool, no network fetch. No live bounty target contacted (rule 8).

## 1. What landed

`corpus/QUALITY.md`: appended `## Round-33 additions — a capture snapshot ships with its manifest (append-only)` after the pre-existing last line (158). Two rows plus one replay block:

- **R20** — a capture snapshot directory ships its `manifest.json` in the same round/commit; every record carries a `url` matching exactly one `corpus/SOURCES.md` registry-row URL plus one provenance field (`fetched_utc` for round-32+, declared `archival: true` for older). Grounded in M33-1 and round-32 verifier spotcheck D5 (`corpus/lessons/round-32-verifier-spotcheck.md:93`), with the base measurement below.
- **R21** — a sourced claim's capture manifest carries the provenance that separates a fabricated capture from a real one (registry-named `url` + commit-dated fetch instant); shape-count counters are not a capture check. Grounded in `corpus/lessons/round-31.md:146` open item 4 and `.ufo/waves/round-31/wave1/CritC2Kill.md:232` §6 item 2.
- `### R20 / R21 — the base measurement both rows rest on (read-only, replayable)`: one `cd`-prefixed, `bash`-runnable block that prints the row's figures from any cwd, plus its measured base output.

Every figure quoted inside a row is produced by that cited block (R19): `manifest_records=38 with_url=0 with_fetched_utc=0 archival_true=0`, `snapshot_dirs_without_manifest=1`. The one inline figure that is not from that block — `git cat-file -e 690b69da:corpus/instruments/capture-binding-check.py` → exit 128 — is cited with its command in the same paragraph, and was re-run for this receipt (§2).

## 2. Measurement the rows rest on

`$ rev=690b69dae23ab9f4ccf056ba2d619cadc2abb3c4; python3 - "$rev" <<'PY' … PY` (the exact block now at `corpus/QUALITY.md:177-200`), run on the lane:

```
dirs=9 manifest_records=38 with_url=0 with_fetched_utc=0 archival_true=0 snapshot_dirs_without_manifest=1 names=corpus/source-snapshots/round-32
```

Independent cross-check (same facts, different code path — per-manifest counting at the base commit):

```
manifest_files 8 records 38 with_url 0 with_fetched_utc 0 archival_true 0
[('round-23', 4), ('round-24', 19), ('round-25', 5), ('round-26', 1), ('round-28', 2), ('round-29', 3), ('round-30', 3), ('round-31', 1)]
```

Snapshot dirs at base: `round-23, round-24, round-25, round-26, round-28, round-29, round-30, round-31, round-32` (9; no `round-27`). `git ls-tree --name-only 690b69da corpus/source-snapshots/round-32/` →

```
corpus/source-snapshots/round-32/S049.txt
corpus/source-snapshots/round-32/S050.txt
```

Checker absence at base:

```
$ git cat-file -e 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4:corpus/instruments/capture-binding-check.py; echo "cat_file_exit=$?"
fatal: path 'corpus/instruments/capture-binding-check.py' does not exist in '690b69dae23ab9f4ccf056ba2d619cadc2abb3c4'
cat_file_exit=128
$ test -e corpus/instruments/capture-binding-check.py; echo "worktree_test_e=$?"
worktree_test_e=1
```

Note: the second value is the working tree at 2026-10-26 during this seat's run (the C1 owner `ExecCaptureBinding` was live) — it is a snapshot, not a verdict; nothing in the rows depends on it.

Anchors cited by the two rows, re-opened before writing:

```
$ sed -n '93p' corpus/lessons/round-32-verifier-spotcheck.md | cut -c1-90
- **D5** `corpus/source-snapshots/round-32/S049.txt`/`S050.txt` are committed without a `r
$ sed -n '146p' corpus/lessons/round-31.md | cut -c1-80
4. **Gate caveat 1 fixes not landed** — manifest `url`/`fetched_utc` fields an
$ grep -n 'No URL↔capture binding' .ufo/waves/round-31/wave1/CritC2Kill.md
232:2. **No URL↔capture binding anywhere** (§4). Minimal: manifest `url` + `fetched_utc` per record and
```

Quotes used, each ≤25 words at the cited location: "are committed without a `round-32/manifest.json`" and "so the 38-record target is not silently moved" (`round-32-verifier-spotcheck.md:93`); "manifest `url`/`fetched_utc` fields and a census URL↔capture comparison" (`round-31.md:146`); "No URL↔capture binding anywhere" (`CritC2Kill.md:232`).

## 3. Append-only proof (R6)

```
$ git diff --numstat -- corpus/QUALITY.md
55	0	corpus/QUALITY.md
$ git show HEAD:corpus/QUALITY.md | sha256sum
300f9962e3017ca0846038d193cfe83f674989dccf78d4488caa59e578badaba  -
$ head -n 158 corpus/QUALITY.md | sha256sum
300f9962e3017ca0846038d193cfe83f674989dccf78d4488caa59e578badaba  -
$ wc -l corpus/QUALITY.md
213 corpus/QUALITY.md
```

55 insertions, 0 deletions; the committed 158-line prefix is byte-identical, so every pre-existing line keeps its number. File digest before `300f9962…`, after `00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087`. Row counts: `| Qn |` rows 10 → 10, `| Rn |` rows 19 → 21.

`anchorcheck.py` (read-only instrument, not edited) before and after:

```
before: PAST-EOF md:77 README.md:159 (file has 14 lines)
before: corpus/QUALITY.md: 3 in-range cite instances, 1 bad; 3 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
before exit=1
after:  PAST-EOF md:77 README.md:159 (file has 14 lines)
after:  corpus/QUALITY.md: 6 in-range cite instances, 1 bad; 6 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
after  exit=1
after added anchors: OK md:169 corpus/lessons/round-32-verifier-spotcheck.md:93
                     OK md:170 corpus/lessons/round-31.md:146
                     OK md:170 .ufo/waves/round-31/wave1/CritC2Kill.md:232
```

The three pre-existing in-range instances (`md:77 SCORECARD.md:502`, `md:95 SCORECARD.md:813`, `md:102 corpus/QUALITY.md:95`) print the same source lines before and after; the single bad verdict is unchanged and pre-existing (finding F1).

## 4. The appended block runs as filed

```
$ cd / && sed -n '178,199p' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md | bash; echo "embedded_block_exit=$?"
dirs=9 manifest_records=38 with_url=0 with_fetched_utc=0 archival_true=0 snapshot_dirs_without_manifest=1 names=corpus/source-snapshots/round-32
embedded_block_exit=0
```

Run from `/` (foreign cwd), not the lane root: the `cd … || exit 9` prefix carries it, and the printed line matches the row's quoted figures byte for byte.

## 5. Findings

- **F1 (pre-existing, routed, not fixed).** `corpus/QUALITY.md:77` (row R13) cites `README.md:159`; at the lane root `README.md` is 14 lines, so `anchorcheck.py` reports `PAST-EOF`. The intended file is `corpus/README.md` (316 lines, line 159 exists). This is inherited: the same verdict reads on the pre-append file (`before: … 3 in-range … 1 bad`). QUALITY is append-only and my ticket adds R20/R21, so the repair belongs to a superseding row or the L1 — no existing row was rewritten.
- **F2 (dependency, disclosed).** Both rows cite M33-1 at `corpus/lessons/round-33.md` § Mistakes. That file is absent at composition time (`test -e corpus/lessons/round-33.md` → absent) because `ScribeLesson` owns it; the rows also carry the frozen fallback pointer `.ufo/waves/round-33/claims.json` → `non_claim_frontier_items.mistake`, so the ground resolves today and the lesson reference resolves when that seat lands (same shape as the round-31 `round-32`/`round-31` self-reference noted in `corpus/lessons/round-31.md` § Open items 5).
- **F3 (non-comparative state, M30-3).** While this seat ran, eight `corpus/source-snapshots/round-*/manifest.json` files were dirty in the working tree (`ExecManifestUpgrade`) and `corpus/instruments/capture-binding-check.py` was absent from the tree at first check. No number in R20/R21 or in this receipt is taken from those in-flight bytes: every figure is measured at the claims base `690b69da…` through `git show`/`git ls-tree`. A post-wave measurement of `records=40 bound=40 unbound=0` is C1's counter run on quiescent landed bytes, not this seat's claim.

## 6. Out of scope this seat (not touched, not claimed)

`corpus/README.md`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `SOURCES.md`, `corpus/instruments/knowledge-expected.txt`, every `corpus/source-snapshots/*/manifest.json`, `corpus/knowledge/**`, `corpus/lessons/round-33.md`, `claims.json`, `c1-controls/`, `c2-controls/`, `census-before.txt`, `assimilation/`, `watchdog-digest.txt`, the round report, and every read-only instrument (`limb-mutation-check.py`, `limb-ledger.json`, `recheck-audit.py`, `source-recheck.py`, `frontier-recheck-count.py`, `anchorcheck.py`, `density.py`, `resolve.py`, `score-gap.py`). No C1/C2 predicate is asserted or re-derived here; no axis score is claimed. This seat edited no committed file other than `corpus/QUALITY.md` and did not commit (the L1 commits through the lane helper).

## 7. Limits

- The base measurement is a single-instant read of the lane's git object store at base `690b69da…`; it says nothing about rounds after 33 and is not a currency check of any source page (no network access was used).
- The `archival: true` count is `r.get('archival') is True` in the surface JSON, so a string `"true"` would not count; the base has 0 of either, and the C1 rule C text is the authority for the landed shape.
- The pre-existing `PAST-EOF` (F1) keeps `anchorcheck.py` at exit 1 for this file, so "anchorcheck exits 0" is not available as a QUALITY-wide gate this round; the append-only property is instead carried by the 55/0 numstat and the byte-identical 158-line prefix.
