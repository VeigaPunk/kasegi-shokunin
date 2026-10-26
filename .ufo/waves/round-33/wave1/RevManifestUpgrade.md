# RevManifestUpgrade — round-33 wave-1 receipt

- Seat: RevManifestUpgrade (reviewer, leaf). Scope: verify ExecManifestUpgrade's legacy manifest upgrade (round-23/24/25/26/28/29/30/31 manifest.json vs base 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4).
- Date: 2026-10-26. Answering model: zai/glm-5.3-flash. No tool installs (bound 5: none needed).
- All commands run read-only in the lane except the receipt write and the `$HYAKU_SCRATCH` fixture.

## Verdict: lands

ExecManifestUpgrade's diff is exactly the contract upgrade: additions-only, all 38 legacy records keep `id`/`path`/`sha256`/`quotes` (incl. per-quote `id`/`quote`/`location`) byte-identical to base, each gains exactly `url` (byte-exact with its own-id SOURCES.md registry row) + `archival: true` + `archival_note`, no `fetched_utc` anywhere, no records added or removed. The real `capture-binding-check.py` on a scratch copy of the upgraded manifests fails rule A only (round-32 dir, pre-ExecManifest32) with `records=38 bound=38 unbound=0`, as my item predicted.

## Check 1 — `git diff -U0` shows additions only

```
$ git diff --numstat 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 -- corpus/source-snapshots/round-{23,24,25,26,28,29,30,31}/manifest.json
12	0	corpus/source-snapshots/round-23/manifest.json
57	0	corpus/source-snapshots/round-24/manifest.json
15	0	corpus/source-snapshots/round-25/manifest.json
3	0	corpus/source-snapshots/round-26/manifest.json
6	0	corpus/source-snapshots/round-28/manifest.json
9	0	corpus/source-snapshots/round-29/manifest.json
9	0	corpus/source-snapshots/round-30/manifest.json
3	0	corpus/source-snapshots/round-31/manifest.json
$ git diff -U0 <base> -- <same 8 paths> | grep -cE '^-[^-]'   # deleted content lines
0
$ git diff -U0 <base> -- <same 8 paths> | grep -cE '^\+[^+]'  # added content lines
114
```
114 = 38 records x 3 added lines (`url`, `archival`, `archival_note`) exactly. Sample hunk (`git diff -U0 <base> -- corpus/source-snapshots/round-31/manifest.json`, @@ -7,0 +8,3 @@):
```
+   "url": "https://www.microsoft.com/en-us/msrc/msvr",
+   "archival": true,
+   "archival_note": "pre-round-32 capture; fetch instant not recorded",
```

## Check 2 — fields unchanged, provenance exactly-one

Kernel cell (condensed): for each of the 8 paths, `git show <base>:<path>` vs worktree JSON; per record compare every base key, flag any non-{url,archival,archival_note} new key, require exactly one of `fetched_utc`/`archival` and `archival is True`.

```
base record keys observed: ['id', 'path', 'quotes', 'sha256']
round-23: base=4 cur=4 issues=0      round-28: base=2 cur=2 issues=0
round-24: base=19 cur=19 issues=0    round-29: base=3 cur=3 issues=0
round-25: base=5 cur=5 issues=0      round-30: base=3 cur=3 issues=0
round-26: base=1 cur=1 issues=0      round-31: base=1 cur=1 issues=0
legacy records compared: 38
defects: 0
```
All 38 records: `fetched_utc` absent, `archival: true` present. 4+19+5+1+2+3+3+1 = 38, matching C1's "38 pre-round-32 records".

## Check 3 — added `url` byte-exact with the SOURCES.md registry row

Kernel cell (condensed): parse `^\|\s*(S\d{3})\s*\|` rows of corpus/SOURCES.md (48 rows at review time, pre-S049/S050 append), extract each row source-cell URL tokens (`https?://\S+`), per record require (a) the record `url` appears in exactly one row's source cell (rule-B cross-row count) and (b) `url` equals a URL token of its own-id row (byte-exact).

```
legacy records with own-row byte-exact url: 38/38
cross-row match counts: 36 records hits=1; 2 records hits=2:
  S029 r23 hits=2 rows=[S024,S029] https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng
  S006 r24 hits=2 rows=[S006,S028] https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq
```
Both hits=2 cases are the registry's pre-existing duplicate-URL row pairs (the known base W04 census warnings); in both, the record `url` is byte-exact with its own-id row (S029's row, S006's row). Not a manifest defect: SOURCES.md is not ExecManifestUpgrade's file and its rows predate this round.

## Check 4 — real checker on scratch copy (PRE-STATE, bound 6)

Fixture: `S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kasegi-r33/RevManifestUpgrade`; `cp -r corpus/source-snapshots $S/corpus/ && cp corpus/SOURCES.md $S/corpus/ && rm -f $S/corpus/source-snapshots/round-32/manifest.json`. This is the pre-ExecManifest32 state (labeled PRE-STATE; the after-state counter is C1's `records=40 bound=40 unbound=0`, runnable only once ExecManifest32's manifest is in the tree).

```
$ python3 corpus/instruments/capture-binding-check.py --root "$S"; echo "binding_exit=$?"
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
AUDIT records=38 with_url=38 with_fetched_utc=0 with_archival=38 snapshot_dirs=9 manifest_dirs=8 missing_manifest=1 multi_row_url=2
FAIL rule=missing-manifest dir=round-32
records=38 bound=38 unbound=0
binding_exit=1
```
Rule-A-only failure exactly as predicted (round-32 dir, no manifest yet); all 38 upgraded legacy records bound. Re-run named for the C1 verifier on final bytes: `python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"` (expect records=40 bound=40 unbound=0 exit 0).

`--selftest` at review time: `selftest cases=11 failures=0`, selftest_exit=0 (contract asks >=6 cases; all six named cases present, plus url-mismatch, no-row, shared-url-not-a-failure, round-32-with-fetched_utc-passes, pre-round-32-archival-passes).

## Check 5 — quiescence (bound 6)

Aggregate stamp `sha256sum <8 manifests> corpus/SOURCES.md | sha256sum` = `8d06ebe4807b7c2a282b5c7471c0d96f938102e96c14543387b22927d296239b` at fixture creation and again after the checker run; `cmp` of all 9 fixture files vs worktree: identical. The bytes I cite were quiescent across the whole review.

## Findings by severity

- Critical/High/Medium: none against ExecManifestUpgrade's diff.
- Low / cross-seat (needs L1 adjudication, not a manifest defect): rule-B multi-row semantics. The frozen contract text says a url matching "0 or 2+" registry rows is a failure, and C1's kill rule repeats "matches zero or two+ registry-row URLs". The landed checker instead bounds a record by its own-id row and reports cross-row duplicates informationally: `multi_row_url=2` in AUDIT (evidence: Check 4 output), with selftest `case=shared-url-not-a-failure exit=0 want=0 verdict=pass` alongside `case=url-matching-two-rows exit=1 want=1 verdict=pass`. Under a strict cross-row reading of C1's predicate ("matches exactly one registry-row URL"), records S029 (round-23) and S006 (round-24) would be unbound and C1 could be killed despite `bound=40`. The checker's own-row reading is self-consistent and the duplicate rows are the registry's known base W04 warnings (frozen file, not upgradeable by this seat) — but the divergence between the frozen text and the implemented rule should be settled by the L1 before the C1 verifier runs.
- Note: `corpus/source-snapshots/round-32/manifest.json` appeared untracked (`??` in `git status`) while this review was in flight (ExecManifest32 landing). Check 4 is labeled PRE-STATE accordingly; no after-state number is claimed here.

## Residual risk / verification gaps

- I did not re-verify `sha256` pins against snapshot bytes; the pins are untouched by the upgrade (additions-only diff, Check 1/2) and pin verification is source-recheck's instrument domain.
- The instrument landed during this review (`corpus/instruments/capture-binding-check.py`, 21527 bytes); I verified its behavior at that instant only.
- Scratch fixture removed at yield (bound 12): `$S` deleted after this receipt was written; no lane writes outside this receipt.
