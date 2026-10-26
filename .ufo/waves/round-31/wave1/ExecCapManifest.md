# ExecCapManifest receipt — round 31, C2/F15 capture + manifest for S048

Answering model: devin/deepseek-v4-1-flash (route table default; no model passed).
Write scope exercised: `corpus/source-snapshots/round-31/S048.txt`, `corpus/source-snapshots/round-31/manifest.json`, this receipt. Nothing else written; scratch lived in `mktemp -d` under /tmp and was deleted.
Pre-state: `corpus/source-snapshots/round-31/` did not exist at base b374febbb (`grep -n normaliz corpus/source-snapshots/*/manifest.json` reported `corpus/source-snapshots/round-31/manifest.json: No such file or directory`); the recheck below is an AFTER column only, never compared to a PRE-STATE number.

## 1. Capture (lane instrument, no curl fallback)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && mkdir -p corpus/source-snapshots/round-31 && python3 corpus/instruments/capture-source.py --id S048 --url https://www.microsoft.com/en-us/msrc/msvr --kind html --out corpus/source-snapshots/round-31/S048.txt; echo "capture_exit=$?"
```
```
S048 status=200 fetched_bytes=81802 snapshot_bytes=3755 sha256=2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55 utc=2026-10-25T23:29:53Z out=corpus/source-snapshots/round-31/S048.txt
capture_exit=0
```
- HTTP status 200, no redirect (final URL = requested URL).
- exit 0; fetched_bytes=81802; snapshot_bytes=3755; UTC timestamp 2026-10-25T23:29:53Z.
- Committed sha256 pin `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`, re-measured on the committed bytes:
```
$ sha256sum corpus/source-snapshots/round-31/S048.txt
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
$ wc -lc corpus/source-snapshots/round-31/S048.txt
  97 3755 corpus/source-snapshots/round-31/S048.txt
```

### Capture non-determinism (measured, not assumed)
A second capture to a temp path differs only on line 2:
```
S048 status=200 fetched_bytes=81802 snapshot_bytes=3755 sha256=9062897607751e89d02859849edebb4c8640ea0ff35529ec469360b41adf7be9 utc=2026-10-25T23:32:21Z out=/tmp/tmp.ScRGUr7bSg/S048b.txt
recapture_exit=0
$ diff corpus/source-snapshots/round-31/S048.txt /tmp/tmp.ScRGUr7bSg/S048b.txt
2c2
< This is the Trace Id: f97e6b1cb578f714d23850f80f018bb3
---
> This is the Trace Id: 031abc7c024b6fb75c793cd4d34a257d
```
Line 2 is a per-request Trace Id. Consequence recorded in the manifest `purpose`: the pin binds the committed bytes, not a refetch; line 2 is never quoted. `source-recheck.py` reads only local files, so exit 0 does not depend on refetch stability.

## 2. Assertions (8, all exactly-once; normalization declared per Q8)

Normalization: `capture-source.py` `html_to_text()` output compared under `source-recheck.py` `normalize()` — capture markup (`<u>…</u>`) stripped, whitespace collapsed. Every quote was measured `occ=1` under that normalization before being written, so no assertion carries an `anchor` (Q9: anchor is required only for non-unique quotes).

| id | quote (≤25 words) | words | line | covers | raw substring | occ |
|---|---|---|---|---|---|---|
| Q1 | `MSVR learns about vulnerabilities in third-party products in three ways` | 10 | L31 | the three intake routes sentence | yes | 1 |
| Q2 | `These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue.` | 19 | L32 | route 1 (internal engineers) | yes | 1 |
| Q3 | `These issues are coordinated by MSVR.` | 6 | L33 | route 2 (external MSRC reports) + third-party findings coordinated | yes | 1 |
| Q4 | `Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices.` | 14 | L34 | route 3 (internal research projects) | yes | 1 |
| Q5 | `as a vendor affected by vulnerabilities in its products and services` | 11 | L35 | role 1 of the three roles | yes | 1 |
| Q6 | `as a finder of new vulnerabilities in third-party products and services` | 11 | L35 | role 2 of the three roles | yes | 1 |
| Q7 | `as a coordinator of vulnerabilities that affect multiple vendors` | 9 | L35 | role 3 of the three roles | yes | 1 |
| Q8 | `This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach.` | 11 | L35 | statement that third-party findings are coordinated (CVD framing) | yes | 1 |

Word counts and occurrence counts measured in one pass with `source-recheck.py`'s own `normalize()`:
```
occ=1 raw_in=True words=10 nchars=71 :: MSVR learns about vulnerabilities in third-party products in
occ=1 raw_in=True words=19 nchars=112 :: These vulnerabilities are reported to the MSVR team, which t
occ=1 raw_in=True words=6 nchars=37 :: These issues are coordinated by MSVR.
occ=1 raw_in=True words=14 nchars=109 :: Any issues are reported to the affected vendor under accepte
occ=1 raw_in=True words=11 nchars=68 :: as a vendor affected by vulnerabilities in its products and
occ=1 raw_in=True words=11 nchars=71 :: as a finder of new vulnerabilities in third-party products a
occ=1 raw_in=True words=9 nchars=64 :: as a coordinator of vulnerabilities that affect multiple ven
occ=1 raw_in=True words=11 nchars=100 :: This coordination takes place under Microsoft's Coordinated
```
No quote touches volatile page chrome (nav L3-L27, footer L36-L97). L30 carries U+2019 (curly apostrophe) and is not quoted; Q8 uses L35's ASCII `'`. L33's source typo ("third-party product of affects both", sic) is inside no assertion, so nothing is silently corrected.

## 3. Recheck (target predicate)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048; echo "recheck_exit=$?"
```
```
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
recheck_exit=0
```
Full-manifest run (no `--source` selector) also exits 0 with the same eight OK lines: `full_manifest_exit=0`.

## 4. Negative controls (the manifest can fail)

Run on a temp copy in `mktemp -d` (never in the lane tree), each a one-field mutation of the landed manifest:
```
--- negative quote control ---
S048:Q1 MISMATCH reason=quote-not-found
neg_quote_exit=1
--- negative sha control ---
S048:sha256 MISMATCH expected=0000000000000000000000000000000000000000000000000000000000000000 actual=2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55
neg_sha_exit=1
--- negative stem control ---
S048:manifest MISMATCH reason=stem-mismatch
neg_stem_exit=1
```
(A control that drops one word from Q1 fails; a wrong pin fails; a `path` whose stem is not `S048` fails — Q9's three bindings are all live on this record.)

## 5. Schema conformance

Same shape as `corpus/source-snapshots/round-30/manifest.json`: `schema_version` 1, `purpose` string, `sources` array of `{id, path, sha256, quotes:[{id, quote, location}]}`; one record, `id: S048`, `path: S048.txt` (stem == id), the capture's sha256 pin, 8 quote assertions. The extra `purpose` sentence carries the declared normalization (Q8) and the Trace-Id caveat; `load_manifest` ignores keys beyond `schema_version`/`sources`, so the record is read exactly as round-30's is.

## 6. Risks / notes for downstream seats

- The pin is bound to these bytes; any recapture of S048 changes line 2 and therefore the sha. Do not recapture — cite the committed file.
- Page-level evidence only: this page states that MSVR coordinates third-party findings under CVD and names the three roles, but carries no timelines, contact addresses, or per-vendor process. Claims beyond L31-L35 need another source.
- `corpus/SOURCES.md` S048 row and the F15/knowledge-entry side are other seats' paths (ExecRegistryAppend, ExecEntryF15); not touched here.

## 7. Tooling

No install or upgrade performed this seat (python3 stdlib instrument only); no pacman transaction; no network fetch beyond the two documented capture runs of the named public URL under the instrument UA.
