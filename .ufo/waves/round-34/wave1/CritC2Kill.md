# CritC2Kill — round-34 wave1 receipt (critic leaf)

Seat: `CritC2Kill`, critic, leaf of the L2 wave. Assignment: **falsify C2 (coverage) as declared** by building
junk constructions that pass the C2 shape counters (frontier=17, rows=51, S051 row present, harness
entries=20 pass=20) without a real capture or a real admission, and state which landed checks catch each and
which do not. Read-only over the lane; no lane file other than this receipt was written. All fixtures live
under `/fast/scratch/hyaku/kasegi-r34/CritC2Kill/` (deleted before yield; see § Scratch).

## Report

### Method and environment

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `014ee2d7…`, claims freeze `29f606db…`.
- Measurements: 2026-10-26T05:36Z–05:45Z. The lane was **moving under this seat** (siblings landing): the
  harness bytes I copied into fixtures at 05:36:44Z were `87b14892…`; at 05:42Z the tip was `8a79010d…`; at
  05:43:44Z it was `1be79af6…`. Every fixture result below was **re-run with the tip bytes `1be79af6…`**
  (`source-recheck.py` `fd2e01e8…` and `capture-binding-check.py` `3d9e5e0d…` were stable all session).
- Frozen claims read: `.ufo/waves/round-34/claims.json`, sha256
  `dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850` (matches the freeze commit per
  `RevC2BeforeAfter`).
- Fixtures: full copies of `corpus/` (no `__pycache__`), one tree per construction:
  `t1` (fabricated capture+manifest), `t1e` (same, entry recheck keeps the absolute `cd`), `t2b`/`t2c`/`t2d`
  (captureless rows), `t3` (fabricated entry body), `t3c` (twin-quote manifests). In `t1`/`t2*`/`t3` the
  entries' recheck lines were rewritten `…/kasegi-shokunin` → `…/CritC2Kill/<fixture>/kasegi-shokunin`
  (45 files) so the harness tests the fixture; that rewrite is a relocation, not a semantic change.
- Digests at tip (`sha256sum`):

```
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  .ufo/waves/round-34/claims.json
2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026  .ufo/waves/round-34/c2-controls/junk-f17.md
```

### 1. Landed C2 battery at the tip — all declared measurements hold

Commands and verbatim outputs (exit codes shown as `exit=`):

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                      -> 17   exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 51 exit=0
$ grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md  -> 1    exit=0
$ grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l         -> 1    exit=0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
… 16 assertions print `occurrences=1 … anchor=N-ok`; Q9 and Q17 print `occurrences=2 anchor=77-ok` / `anchor=96-ok`
exit=0
$ python3 corpus/instruments/capture-binding-check.py | tail -2
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
exit=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

The declared C2 counters (frontier 17, rows 51, S051 row 1, entry 1, harness 20/20, source-recheck exit 0,
census exit 0) are reproduced. Note on the predicate wording, "every assertion occurrences=1": measured
**16 × occurrences=1 plus 2 × occurrences=2 with a verified anchor** — the anchors are the declared Q9 path
and the claim's own `after` list records them; the literal "every" is a wording defect, not an exit-status
failure (already flagged by `RevC2BeforeAfter`).

### 2. The real capture is genuine — independent live re-capture

```
$ date -u +%Y-%m-%dT%H:%M:%SZ                                    -> 2026-10-26T05:42:45Z
$ python3 corpus/instruments/capture-source.py --id S051 --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ --out $S/live/S051.txt
S051 status=200 fetched_bytes=219383 snapshot_bytes=8502 sha256=4fd8ed98…b325a5 utc=2026-10-26T05:42:46Z
$ sha256sum $S/live/S051.txt corpus/source-snapshots/round-34/S051.txt
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  (both)
$ cmp $S/live/S051.txt corpus/source-snapshots/round-34/S051.txt -> BYTE-IDENTICAL, exit=0
```

This is a second independent fetch (the first was `ScoutImmunefiLive` at 05:35:45Z, same sha). The committed
S051 capture is not fabricated; C2's landed material is real. **This evidence lives in receipts, not in an
instrument** — see gap G1.

### 3. Construction 1 — entry quoting a fabricated string with a fake manifest record

Procedure (`t1`): replace `corpus/source-snapshots/round-34/S051.txt` with 5 fabricated lines containing the
marker "This fabricated capture was never fetched from immunefi.com." and "Fabricated clause: smart-contract
severity is decided by a coin flip."; rewrite the manifest's S051 record `sha256` to the new bytes and replace
its 18 quotes with 3 fabricated quotes; keep `url` and `fetched_utc` unchanged so registry binding still holds.
Fake capture sha256 `a078700e60af1522c4512276e42f7efcfb9896829e6fc7516b2da1782a042ea4`.

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                       -> 17  exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 51 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=2-ok
S051:Q2 OK occurrences=1 anchor=4-ok
S051:Q3 OK occurrences=1 anchor=5-ok
exit=0
$ python3 corpus/instruments/capture-binding-check.py | tail -1
records=41 bound=41 unbound=0                                     exit=0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051  exit=0
entries=20 pass=20 exit=0
```

**Result: every C2 counter passes on a wholly fabricated capture.** 16 of the entry's 17 blockquotes no
longer occur in the capture (measured: 1/17, only "Critical High Medium Low None" survives) and nothing
fails. `source-recheck.py` cannot detect a fabricated capture: it compares the capture to a sha256 **carried
in the same manifest**, and the quotes to that capture — self-consistency, not provenance. `capture-binding`
binds id→row→url and checks a strict-UTC `fetched_utc`, all of which the fabricator copies. This is the
instrument's documented limit (docstring, "Known limits": "a record whose id names a row but whose capture
bytes came from a different document is bound by this instrument").

**Construction 1e — the harness is not root-confined.** With the entry's original absolute recheck line
(`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 …`), a fixture whose capture is
fabricated still prints:

```
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F17  … ids=S051  exit=0
entries=20 pass=20 exit=0
```

The harness's rule B reads the **fixture** manifest (id listing only, never bytes) while rule D executes the
line, whose `cd` walks back to the live lane and rechecks the real capture. So a base-tree or reviewer-copy
run of the harness does not necessarily test that tree; here the pass is attributable to the live lane.

### 4. Construction 2 — a registry row with no opened source

`t2c`: flip the queued row `S016` to `mined` and point its `used-by` at the F17 entry, with **no manifest
record and no capture** anywhere; rows stay 51.

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 51  exit=0
$ sources-census.sh validate --root /home/vgpnk/Projects/shokunin --file <t2c>/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	<fixture>/corpus/SOURCES.md
exit=0
$ python3 corpus/instruments/capture-binding-check.py | tail -1   -> records=41 bound=41 unbound=0  exit=0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2  -> entries=20 pass=20 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest … --source S051 -> exit=0
```

(`--file` labels the lane `file` instead of `kasegi`; the W04 pair and the `ok` line are substantively the
claimed census output, exit 0.) `capture-binding` only binds records→rows, never rows→records, so a mined row
with no capture is invisible; census `W03` ("mined but unused") is only a warning and does not fire once a
`used-by` path exists (E11 checks existence, not semantics). **Result: a mined, used registry row with no
opened source passes every C2 counter.** The current lane happens to satisfy `mined ⇒ record` (39 mined rows,
39 record ids, measured), but no instrument enforces it.

`t2b`: remove the rejected row `S028` and insert a phantom `S052` (unique URL, `—` used-by, no capture) —
rows stay 51; census `exit=0` with `W03 S052` + `W04 S029`, capture-binding `records=41 bound=41` exit 0.

`t2d`: a captureless row **cited** by an entry is caught — header `source: S016` + recheck `--source S016`
(manifest does not list S016):

```
FAIL F17 … ids=S016  exit=-  problems=selection-not-cited-by-entry,manifest-missing-ids
entries=20 pass=19 exit=1
$ source-recheck --source S016 -> S016:source UNAVAILABLE reason=not-listed  exit=2
```

So the uncaught surface is exactly the uncited row, not a cited one.

### 5. Construction 3 — entry citing S051 without ever opening the page

**3a — fabricated body quote, real capture untouched (`t3`).** Inject
`> "Immunefi pays a fixed $50,000 bounty for every Critical smart-contract finding." — S051.txt:46`
(occurs 0 times in the capture):

```
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2 -> F17 PASS, entries=20 pass=20 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest … --source S051 -> exit=0
$ python3 corpus/instruments/anchorcheck.py corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
== …: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
```

`anchorcheck` sees 0 cite instances because the entry's `S051.txt:NN` anchors are **not backticked** and its
matcher only consumes backticked tokens; `source-recheck` never reads the entry body (it reads the manifest's
`quotes`). The entry body is unbounded by every landed check.

**3b — entire body fabricated.** Replace everything after the header with invented claims ("$50,000",
"CVSS maps 1:1", `S051.txt:999`, `S051.txt:1000`): harness `entries=20 pass=20 exit=0`, source-recheck
`exit=0`, anchorcheck `0 bad exit=0`, and the shape counter still returns `1`. The harness binds only ids
(header `source:` ↔ `recheck --source` ↔ manifest id list); it never compares entry content to capture bytes.

**3c — the junk twin's own recheck does not reject the twin.** The committed twin
(`.ufo/waves/round-34/c2-controls/junk-f17.md:11`) points at the **real** manifest:

```
$ sed -n 's/^recheck: //p' .ufo/waves/round-34/c2-controls/junk-f17.md | bash
S051:sha256 OK … 18 × OK …                                          exit=0
$ python3 .ufo/waves/round-34/c2-controls/junk-checker.py
junk_twin h1=True source_line=True recheck_line=True
shape_counters=3/3                                                   exit=0
```

The rejection is real only under the reviewer's manufactured-manifest procedure (the twin's quote built into
a manifest, run against the committed capture):

```
twin quote vs REAL capture:              S051:Q1 MISMATCH reason=quote-not-found   exit=1
twin quote vs SELF-CONSISTENT fake capture: S051:Q1 OK occurrences=1               exit=0
```

So "junk twin rejected" is true for the committed twin against the committed capture, and false in general:
give the twin a capture its own quote lives in and it passes (construction 1).

### 6. The real entry is honest (so C2's content, not its gate, is at issue)

Against the genuine capture: the entry's FC checks all reproduce — 15 level headings / 0 "Severe|Moderate";
`v2.2`=2, `v2.3`=0; `CVSS`=0; `reward`=0, `$`=0; `Permanent freezing of funds`=2, `Temporary freezing`=1;
`Execute arbitrary system commands`=1; `1. None- Best practices`=2. All **17/17** blockquotes are covered by
the manifest's 18 quotes (normalized), and 17 distinct `S051.txt:NN` cites are present. The landed C2 claim is
supported; only the gate's discriminating power is limited.

### 7. Catch matrix — which landed check catches which construction

| construction | shape counters | harness | source-recheck | capture-binding | census | anchorcheck |
|---|---|---|---|---|---|---|
| 1 fabricated capture + self-consistent manifest | pass (17/51/1/1) | pass 20/20 | **pass exit 0** | **pass 41/41** | not applicable | — |
| 1e fabricated capture, absolute `cd` in entry | pass | **pass 20/20 (rechecks live lane)** | pass (fixture) | pass | — | — |
| 2 uncited mined row, no capture (`t2c`, `t2b`) | pass (51) | pass 20/20 | not consulted | **pass 41/41** | **exit 0** | — |
| 2 cited captureless row (`t2d`) | pass | **FAIL manifest-missing-ids exit 1** | **exit 2 not-listed** | pass | — | — |
| 3a fabricated body quote, real capture | pass | **pass 20/20** | **pass (manifest unchanged)** | pass | pass | **pass 0 instances** |
| 3b fabricated entry body | pass | **pass 20/20** | **pass** | pass | pass | **pass 0 instances** |
| 3c twin quote vs real capture | — | — | **exit 1 quote-not-found** | — | — | — |
| 3c twin quote vs fake capture | — | — | **pass exit 0** | — | — | — |

### 8. Residual gaps (measured, with the smallest safe correction)

- **G1 — no provenance binding.** `source-recheck` pins local bytes to a sha256 in the same manifest; no
  instrument ties the bytes to a fetch of the registry URL. Smallest correction: store `capture-source.py`'s
  fetch line (`status`, `fetched_bytes`, `snapshot_bytes`, UA, `fetched_utc`) as manifest fields and add one
  `capture-binding` rule that `fetched_bytes`/`snapshot_bytes` match the capture size and the log's sha/UTC
  match the record; keep the live re-capture as a receipt obligation for new admissions (done twice this
  round: `ScoutImmunefiLive`, this seat).
- **G2 — entry body unbound.** `frontier-recheck-count.py` binds ids only; `source-recheck` reads manifest
  quotes. Smallest correction: in the harness's per-entry contract, require every blockquote
  `> "…" — S<id>.txt:NN` to occur (normalized) in the named capture within a small line window around `NN`.
  Real entry: 17/17 pass; injection 3a would fail on 0 occurrences.
- **G3 — `mined` is not bound to a capture.** `capture-binding` walks records→rows only. Smallest correction:
  one rule "every row with `status=mined` has ≥1 manifest record, or is declared in an explicit no-capture
  list"; currently 39/39 satisfy it, and `t2c` would fail.
- **G4 — harness rule D can leave the tested root.** Entries carry `cd /home/vgpnk/Projects/shokunin/…`; on a
  relocated tree rule B reads the tree's manifest while D rechecks the live lane. Smallest correction:
  reject a `cd` prefix in `recheck:` lines (or require the line to be root-relative and execute it with the
  root as cwd); F17's line currently violates this.
- **G5 — "junk twin passes source-recheck" is ambiguous in the kill rule.** The twin's own `recheck:` line
  exits 0 (it names the real manifest); rejection depends on a reviewer building a manifest from the twin's
  quote. Smallest correction: append an erratum that defines the gate invocation and records both measurements
  (`exit=1` vs committed capture, `exit=0` via its declared line).

### 9. Other observed discrepancies for the L1 (not C2 kills)

- **C2 predicate wording:** "every assertion occurrences=1" vs measured 16×1 + 2×2 anchored (exit 0 holds).
- **C1 counting command staleness:** `claims.json` C1 lists `capture-binding-check.py -> records=40
  bound=40 unbound=0 (unchanged C1 instrument baseline)`; the tip prints **records=41 bound=41** (the
  round-34 S051 record). The count is correct for the after-tip; "unchanged" is not.
- **Lane moved during review** (harness digest `87b14892` → `8a79010d` → `1be79af6`); final measurements and
  all fixture re-runs are against `1be79af6`.

### Verdict

**C2 holds as declared for the landed tree, and the gate is not provenance-sound.** Every C2 counter and the
`PASS F17 ids=S051` line reproduce at the tip; the committed S051 capture is byte-identical to two independent
live re-captures; the real entry's 17/17 blockquotes and all FC checks hold; the committed twin is rejected
when its fabricated quote is checked against the committed capture (`exit=1`). But the landed checks cannot
distinguish a fabricated capture (construction 1: 17/51/1/1, harness 20/20, source-recheck exit 0,
capture-binding 41/41 exit 0), a fabricated entry body (3a/3b: harness and source-recheck still pass,
anchorcheck sees 0 cites), or an uncited mined row with no source (2: census exit 0, capture-binding 0). The
gaps are G1–G5 above; the smallest safe corrections are listed with each. C2's *evidence* is real this round;
its *gate* would not catch the same construction committed with a self-consistent capture.

### Scratch

`/fast/scratch/hyaku/kasegi-r34/CritC2Kill/` (fixtures + evidence files) is deleted after this receipt is
written; `ls -d` of the seat scratch verified `No such file or directory`. No tool was installed or upgraded.
No lane file other than this receipt was written; no git/jj mutation was run.
