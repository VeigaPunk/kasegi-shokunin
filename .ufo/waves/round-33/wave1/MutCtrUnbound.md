# MutCtrUnbound — rule-B url-missing one-limb mutant (round 33)

Model: devin/glm-5-3-flash-1m (config route). Tooling installed: none.

Assigned mutation: count a record as bound even when it has no `url` (rule B skipped). Kill rule (frozen C1, as tasked): the mutant must fail (exit 1 or `unbound>0`) when unbound records exist; if it exits 0 with `unbound=0` while records lack url, it is a survivor.

The lane file `corpus/instruments/capture-binding-check.py` was NEVER written by this seat. All mutation happened on scratch copies under `/fast/scratch/hyaku/kasegi-r33/MutCtrUnbound/`. The lane bytes changed once mid-probe (ExecCaptureBinding's in-flight erratum-1 rewrite of rule B), so the probe was run against both pinned generations; verdicts below are per generation, each on the bytes named.

## Mutant definition

### Generation 1 — lane bytes `5fa7868bf91941d8d9d39c71ba00492d347459ef875fa7d930fb244d01510837`

Exact-once find/replace over the instrument's own bytes (occurrences of find string: 1, verified by count before replace; `py_compile` ok):

```python
# find  (pristine.py line 186, the url-missing branch of check()):
                failures.append("FAIL rule=url-missing record=%s dir=%s" % (label, name))
# replace:
                url_ok = True
```

Effect: a record with no `url` no longer appends a failure and is counted bound (rule B skipped for it); records carrying a `url` still go through registry matching.

- pristine sha256 = `5fa7868bf91941d8d9d39c71ba00492d347459ef875fa7d930fb244d01510837`
- mutant sha256   = `8bac695213191c51e79a90240ab48b3afe6a814048aa9585e9ed3a3ec6822792`

```diff
--- /fast/scratch/hyaku/kasegi-r33/MutCtrUnbound/pristine.py	2026-10-26 01:18:33.985059077 -0300
+++ /fast/scratch/hyaku/kasegi-r33/MutCtrUnbound/mutant.py	2026-10-26 01:19:46.062902608 -0300
@@ -183,7 +183,7 @@
             url = record.get("url")
             url_ok = False
             if not (isinstance(url, str) and url.strip()):
-                failures.append("FAIL rule=url-missing record=%s dir=%s" % (label, name))
+                url_ok = True
             else:
                 totals["with_url"] += 1
                 matches = binding_rows(registry, url)
```

### Generation 2 — lane bytes `4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79` (as-of 2026-10-26T04:20:13Z and again 04:20:41Z)

Mid-probe the lane bytes changed to the erratum-1 id-scoped rule B (docstring section B now reads "B. URL BINDING (claims-erratum-1, the L1's id-scoped ruling)." — pristine2.py lines 16-31): url-less records fail as `FAIL rule=url-mismatch record=<id> detail=absent` inside `bind_record()`, and a URL shared across DIFFERENT row ids became informational (`multi_row_url=N` on the AUDIT line). Same semantic limb re-mutated:

Exact-once find/replace (occurrences: 1; `py_compile` ok):

```python
# find  (pristine2.py line 178, the url-absent branch of bind_record()):
        return False, ["rule=url-mismatch record=%s detail=absent" % record_id]
# replace:
        return True, []
```

- pristine2 sha256 = `4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79`
- mutant2 sha256   = `4bc62ccf6e0fae1290833cc3d6e194352198aa5679c7e31eee17a37733d663b3`

```diff
--- /fast/scratch/hyaku/kasegi-r33/MutCtrUnbound/pristine2.py	2026-10-26 01:20:17.200056232 -0300
+++ /fast/scratch/hyaku/kasegi-r33/MutCtrUnbound/mutant2.py	2026-10-26 01:20:33.137458178 -0300
@@ -175,7 +175,7 @@
         return False, ["rule=dup-id record=%s rows=%d" % (record_id, len(own))]
     url = record.get("url")
     if not (isinstance(url, str) and url.strip()):
-        return False, ["rule=url-mismatch record=%s detail=absent" % record_id]
+        return True, []
     if url not in row_tokens(own[0]):
         return False, ["rule=url-mismatch record=%s row=%s" % (record_id, record_id)]
     return True, []
```

## Fixture trees (built in scratch; not lane bytes)

Fixture v1 (for generation 1, where rule B matched a url against ALL registry rows): one snapshot dir `round-23`, record S001 bound (url `https://fixture.example/doc-a`, `archival: true`), record S002 with NO `url` field (`archival: true`); registry has exactly one row carrying `https://fixture.example/doc-a` (so S001 matches exactly one row) and no S002 row. Under generation-1 rule B, S002's only failing limb is the missing url.

`fixture/corpus/source-snapshots/round-23/manifest.json` sha256 `b4cc8dc4f27446b8f5d159b1c29f995ca58b2c3eaef9c96342b3af5ff98cc697`:

```json
{
  "schema_version": 1,
  "purpose": "Mutation-probe fixture (round-33 seat MutCtrUnbound): one bound record (S001) and one record with no url field (S002) to exercise capture-binding-check rule B.",
  "sources": [
    {
      "id": "S001",
      "path": "S001.html",
      "url": "https://fixture.example/doc-a",
      "archival": true,
      "archival_note": "fixture record; not a real capture",
      "sha256": "20b881ddf1e7fcbed85b9dafb270f393bc02783ab47a38ae9451d4d574bcf7f6",
      "quotes": []
    },
    {
      "id": "S002",
      "path": "S002.html",
      "archival": true,
      "archival_note": "fixture record; not a real capture",
      "sha256": "e7a0badd6e23b1616c3c1d3f88671d4cc45b194f2e18057f1940b17cc46c1ce5",
      "quotes": []
    }
  ]
}
```

`fixture/corpus/SOURCES.md` sha256 `2e7272dd90d5caa77c495d03622b4ce43d5ead13c229be5dd2fe39dc553eb132` (registry row line):

```
| S001 | Fixture Doc A — https://fixture.example/doc-a | docs | A | fixture scope cell | fixture anchor cell | Fixture teaching sentence. | mined | 2026-10-26 | on-release | — |
```

Fixture v2 (for generation 2, where rule B binds by id): same manifest (S002 still has no `url` field), but the registry now also has an S002 row (`https://fixture.example/doc-b`), so B1 (row exists) and B2 (unique id) pass and B3's `url-mismatch detail=absent` is the ONLY failing limb. `fixture2/corpus/SOURCES.md` sha256 `002c2e5da098d130acf75be669029ac7157e307dadf2b530535c538361753e73`; `fixture2/.../manifest.json` sha256 `d81fd6cdc98ab7ce95bc311af5596f3d01cdad7c652ee0a967a2168dfe4d46d1`.

## Commands and output

### 1. Pristine baseline on fixture v1 (generation-1 bytes) — detector sound

```
$ python3 $S/pristine.py --root $S/fixture
MANIFEST round-23 records=2 url_bound=1 fetched=0 archival=2
AUDIT records=2 with_url=1 with_fetched_utc=0 with_archival=2 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0
FAIL rule=url-missing record=S002 dir=round-23
records=2 bound=1 unbound=1
exit=1
```

Baseline fails exactly the assigned limb (url-missing, S002 named) — not inconclusive.

### 2. Mutant (generation 1) on fixture v1 — the verdict leg

```
$ python3 $S/mutant.py --root $S/fixture
MANIFEST round-23 records=2 url_bound=2 fetched=0 archival=2
AUDIT records=2 with_url=1 with_fetched_utc=0 with_archival=2 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0
records=2 bound=2 unbound=0
exit=0
```

Mutant exits 0 with `unbound=0` while record S002 carries no `url` → **SURVIVOR** under the frozen kill rule.

### 3. Mutant (generation 1) `--selftest` — supplementary leg

```
$ python3 $S/mutant.py --selftest --scratch $S/selftest-scratch
selftest case=record-without-url exit=0 want=1 verdict=fail
selftest problem=exit=0 want=1 case=record-without-url
selftest problem=missing='FAIL rule=url-missing record=S002 dir=round-30' case=record-without-url
selftest problem=missing='records=2 bound=1 unbound=1' case=record-without-url
[... 8 further cases pass ...]
selftest cases=9 failures=1
exit=1
```

The instrument's own embedded `record-without-url` case discriminates the mutant.

### 4. Pristine baseline on fixture v2 (generation-2 bytes) — detector sound

```
$ python3 $S/pristine2.py --root $S/fixture2
MANIFEST round-23 records=2 url_bound=1 fetched=0 archival=2
AUDIT records=2 with_url=1 with_fetched_utc=0 with_archival=2 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=url-mismatch record=S002 detail=absent dir=round-23
records=2 bound=1 unbound=1
exit=1
```

### 5. Mutant2 (generation 2) on fixture v2 — the verdict leg

```
$ python3 $S/mutant2.py --root $S/fixture2
MANIFEST round-23 records=2 url_bound=2 fetched=0 archival=2
AUDIT records=2 with_url=1 with_fetched_utc=0 with_archival=2 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
records=2 bound=2 unbound=0
exit=0
```

Same survivor signature on the erratum-1 bytes.

### 6. Mutant2 `--selftest` — supplementary leg

```
$ python3 $S/mutant2.py --selftest --scratch $S/selftest-scratch2
selftest case=record-without-url exit=0 want=1 verdict=fail
selftest problem=exit=0 want=1 case=record-without-url
selftest problem=missing='FAIL rule=url-mismatch record=S002 detail=absent dir=round-30' case=record-without-url
selftest problem=missing='records=2 bound=1 unbound=1' case=record-without-url
[... 10 further cases pass ...]
selftest cases=11 failures=1
exit=1
```

### 7. Real-manifests leg (generation 2 bytes), both arms on the same pinned bytes

```
$ rm -rf $S/real3 && mkdir -p $S/real3/corpus && cp -r <lane>/corpus/source-snapshots $S/real3/corpus/ && cp <lane>/corpus/SOURCES.md $S/real3/corpus/
$ echo "as_of=$(date -u +%Y-%m-%dT%H:%M:%SZ); live_S049_rows=$(grep -c '^| S049 ' .../SOURCES.md); live_S050_rows=$(grep -c '^| S050 ' .../SOURCES.md)"
as_of=2026-10-26T04:20:38Z
live_S049_rows=0 live_S050_rows=0
pinned_bytes_sha256=6ef8f10b293d16ccdb9b11c0eccfabeec0c98c0505530af614fc1a0be2b48b43
$ python3 $S/pristine2.py --root $S/real3 ; echo exit=$?
[9 MANIFEST lines: round-23 4/4, round-24 19/19, round-25 5/5, round-26 1/1, round-28 2/2, round-29 3/3, round-30 3/3, round-31 1/1, round-32 0/2 bound]
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
FAIL rule=no-row record=S049 dir=round-32
FAIL rule=no-row record=S050 dir=round-32
records=40 bound=38 unbound=2
exit=1
$ python3 $S/mutant2.py --root $S/real3 ; echo exit=$?
<output byte-identical to pristine2's — `diff` of the two output files: OUTPUTS_IDENTICAL>
```

On url-bearing records the mutation is invisible (faithful one-limb mutation: no crash, no collateral output change on real data). This leg is PRE-STATE — see below; the verdict does not rest on it.

## Verdict

**SURVIVOR** under the frozen C1 kill rule as tasked (plain run): on a fixture whose S002 record has no `url`, the mutant prints `records=2 bound=2 unbound=0` and exits 0 — on both pinned generations of the instrument (`5fa7868b…` and `4bc7aed3…`).

## Coverage finding (recorded, not judged into the contract)

- The plain-run kill rule (exit 1 / `unbound>0`) does not pin the url-missing limb: `bound` is incremented from `url_ok` alone, and the only carrier of the url-missing failure is the FAIL append that this mutation removes. Nothing else in the plain run fails on a url-less record.
- The discriminating signal IS printed by the instrument itself: on every mutant run the AUDIT line shows `with_url=1` against `records=2` (with_url < records). The frozen kill rule does not read the AUDIT line.
- The instrument's own `--selftest` DOES discriminate this mutant on both generations (`failures=1`, exit 1; its `record-without-url` case expects exit 1 plus the FAIL line plus `records=2 bound=1 unbound=1`). C1's claim text already asserts "`--selftest` failures=0" as a claim property, so an instrument carrying this mutation would fail that clause even though the plain-run clause passes. Closing the plain-run hole is the integrator's call (e.g. a kill rule that also requires `--selftest` failures=0, or reading the with_url/records consistency); this seat changed nothing.

## PRE-STATE labels (bound 6)

- Real-manifests leg, generation 1, pinned bytes sha256 `f92dcbc7c3774e92249ac5f5ef3eb5f13e70339ea4cbc4a3b866b2bdb64759f1` (copied ~2026-10-26T04:18Z): pristine exits 1 — `FAIL rule=url-ambiguous record=S029 dir=round-23 rows=S024,S029`, `FAIL rule=url-ambiguous record=S006 dir=round-24 rows=S006,S028`, `FAIL rule=url-unbound record=S049 dir=round-32`, `FAIL rule=url-unbound record=S050 dir=round-32`, `records=40 bound=36 unbound=4`. The generation-1 mutant was NOT run on real bytes (bytes drifted to erratum-1 first; re-based instead).
- Real-manifests leg, generation 2, pinned bytes sha256 `6ef8f10b293d16ccdb9b11c0eccfabeec0c98c0505530af614fc1a0be2b48b43`, as_of 2026-10-26T04:20:38Z: `live_S049_rows=0 live_S050_rows=0` — the S049/S050 registry rows had not landed, so pristine itself exits 1 (`records=40 bound=38 unbound=2`, two `rule=no-row` failures). Non-comparative for the C1 `bound=40 unbound=0` target. Re-run condition: after ExecRegistryAppend lands the S049/S050 rows, re-run both arms on quiescent bytes before citing any real-tree bound figure.
- On both pinned real copies the manifest upgrades had landed: `with_archival=38 with_fetched_utc=2`, `missing_manifest=0`, 9 manifest dirs, 40 records — matching C1's 38/2 split.
- Erratum-1 drift note (factual): under generation-1 bytes the S024/S029 and S006/S028 duplicate-URL rows were rule-B failures; under generation-2 bytes they pass with `multi_row_url=2` informational. My tasking's contract text says rule B requires the url to "match EXACTLY ONE `corpus/SOURCES.md` registry-row URL"; the landed generation-2 bytes implement the id-scoped erratum-1 reading instead. Recorded as byte-level drift between generations; not judged here.

## Restoration evidence

- Mutated bytes lived only in scratch (`mutant.py`, `mutant2.py`); the lane instrument was never written by this seat.
- Lane instrument sha256 at probe start `5fa7868b…0837`; after the mid-probe erratum-1 edit `4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79` (as-of 2026-10-26T04:20:13Z), unchanged at probe end (as-of 2026-10-26T04:20:41Z) — the generation-2 verdict applies to bytes still current at 04:20:41Z.
- Restored-bytes runs: `mutant.py` overwritten with `pristine.py` (sha256 back to `5fa7868b…0837`) and `mutant2.py` overwritten with `pristine2.py` (sha256 back to `4bc7aed3…f79`); detector on restored bytes reproduces the pristine baseline (fixture v1: exit 1, `records=2 bound=1 unbound=1`; fixture v2: exit 1, `FAIL rule=url-mismatch record=S002 detail=absent dir=round-23`, `records=2 bound=1 unbound=1`). Each mutant differs from its pristine by exactly the one-line diff shown above.
- Scratch copy is disposable per tasking (lives under `$HYAKU_SCRATCH/kasegi-r33/MutCtrUnbound/`, removed at cleanup below).

## Cleanup

Scratch dir `/fast/scratch/hyaku/kasegi-r33/MutCtrUnbound/` removed after this receipt was written (receipt lives in the wave dir; nothing else needed preserving — all outputs are quoted above).
