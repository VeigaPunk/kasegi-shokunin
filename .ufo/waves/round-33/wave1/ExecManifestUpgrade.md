# ExecManifestUpgrade — legacy manifest provenance upgrade (round 33)

Seat: ExecManifestUpgrade (leaf executor). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin.
Base: 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4. Claims freeze: 6e55c8d.
Scope owned: `corpus/source-snapshots/{round-23,round-24,round-25,round-26,round-28,round-29,round-30,round-31}/manifest.json` only.
Answering model: this seat ran on the session's configured model route (no model passed by the seat).

Task: for every record in the eight legacy manifests add `url` (byte-exact copy of the record's OWN
SOURCES.md registry-row URL), `"archival": true` and an `archival_note`; do not alter `id`, `path`,
`sha256`, `quotes` or `location`. Then run `corpus/instruments/capture-binding-check.py` after
ExecCaptureBinding's receipt and report the measured state.

## 1. Record inventory at base (all 38 legacy records; 9 snapshot dirs)

```
round-23 4  [S018, S029, S030, S031]
round-24 19 [S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S032 S033 S034 S035]
round-25 5  [S036, S037, S038, S039, S040]
round-26 1  [S041]
round-28 2  [S041, S042]
round-29 3  [S043, S044, S045]
round-30 3  [S046, S047, S041]
round-31 1  [S048]
total 38
```

Every id resolves to exactly one registry row; no record lacks a row, so the "STOP and report the id"
branch did not fire. `round-26/S040-live.txt` holds no manifest record and none was added (matches
ScoutManifestAudit's note; the file is not a record and rule A is satisfied by the dir's manifest).

## 2. Registry-URL derivation (byte-exact, single source)

The URL for each record was read out of `corpus/SOURCES.md` column 2 of the row whose id equals the
record id — never retyped, never taken from prose. Derivation command and its per-id output:

```
$ python3 -c "import re,json; ids={}; [ids.setdefault(m.group(1),[]).extend(re.findall(r'https?://[^\s|]+',m.group(2))) for line in open('corpus/SOURCES.md') for m in [re.match(r'^\|\s*(S\d{3,})\s*\|(.*)$',line)] if m]; print(json.dumps(ids,indent=1,ensure_ascii=False))"
{ "S001": ["https://www.first.org/cvss/v4.0/user-guide"], ... "S048": ["https://www.microsoft.com/en-us/msrc/msvr"] }
```
(full 48-row map emitted; each id carried exactly one `https://` token in its source cell.)

### Shared-URL rows (informational, per claims-erratum-1)

```
$ python3 dupcheck.py   # counts rows whose source cell carries the record's URL
GLOBAL-URL-OCCURRENCES round-23 S029 -> 2 rows: ['S024', 'S029']
GLOBAL-URL-OCCURRENCES round-24 S006 -> 2 rows: ['S006', 'S028']
```

Those are the only two records of 38 whose URL text sits in more than one registry row, i.e.
`multi_row_url=2` under the L1's erratum. Each record still takes its URL from the row with its OWN id
(S029 from row S029, S006 from row S006), which is what the erratum requires. S048's URL also occurs in
one Search-log bullet (SOURCES.md line 72) — prose, not a row cell, so it is not a multi-row URL.

I read `.ufo/waves/round-33/claims-erratum-1.md` (L1 ruling, commit 53bfa59) and messaged
ExecCaptureBinding with the coordinates before/after the ruling; the data side was already
erratum-compliant.

## 3. Upgrade applied (insertion only, format-preserving)

Method: textual insertion after each record's `"path": "<file>"` line, reusing that line's own
indentation, so every pre-existing byte in the eight files survives. Serialising the parsed JSON was
rejected because round-30 carries compact one-line quote objects and round-25/26/28/31 use 1-space
indent — a re-dump would have rewritten unrelated lines. Insert transform (scratch script, removed
after the run):

```python
pat = re.compile(r'^(\s*)"path":\s*' + re.escape(json.dumps(path)) + r',\s*$')
idxs = [i for i, l in enumerate(lines) if pat.match(l.rstrip("\r\n"))]   # must be exactly 1
lines[i+1:i+1] = ['%s"url": %s,%s' % (indent, json.dumps(url, ensure_ascii=False), eol),
                  '%s"archival": true,%s' % (indent, eol),
                  '%s"archival_note": %s,%s' % (indent, json.dumps(NOTE, ensure_ascii=False), eol)]
```
NOTE = `pre-round-32 capture; fetch instant not recorded`.
Guards inside the script: unique path anchor per record; no pre-existing `url`/`archival`/
`archival_note`; `json.loads(after)` parses; deep-equality of the parsed document with the three new
keys stripped (structural drift check); record count per file unchanged; per-record `r["url"] ==
registry[r["id"]]`; `archival is True` and no `fetched_utc`.

```
$ python3 apply.py
upgraded round-23 records= 4
upgraded round-24 records= 19
upgraded round-25 records= 5
upgraded round-26 records= 1
upgraded round-28 records= 2
upgraded round-29 records= 3
upgraded round-30 records= 3
upgraded round-31 records= 1
```

## 4. Per-file sha256 before / after

| manifest | sha256 before | sha256 after |
|---|---|---|
| round-23 | c3de25caef46fe4780f01aa7f0885a41c3d6e77bf84287ffabb923dcb78a3f2f | 1f6d4fb50491354d1347676bb3f9a03884ee46f1178d62f3ff11f0b31b8d8e70 |
| round-24 | c94c0ae95e1e7df0bb2ea78e853b38c60edb5b5204eed1298351daa336ce8923 | 77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3 |
| round-25 | 6b8739dc3878b177cc80984d643af7d60e66cb595ed0eaffa22f036771ca4ebe | 251cb5b2c1bacb5ba47758fb60e41aaf1e367ae11df05ed19886361b35f7aea2 |
| round-26 | 5890f03d62035a071d15476cee30c08973dbaff1201b7e541fa161b2c6f68675 | 1c9131326106eca5860f5c650b2c9c4efa860da52a701b039b457aba619e3247 |
| round-28 | e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d | 89f51e052eaefcb56a880d48e6778ee88b46e55cafde1275c69992304e7ef75e |
| round-29 | 910608e6bba69b32423a260332853e28f737affeaeb9011f6c9faef6702fb16a | b24a485ff3d2d03abe3ef2022e211c7092bcf7509f3913cfa44145216e2c8d15 |
| round-30 | dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6 | 8aacf77cf2f3d9c7912eea419a05e10604959b2faacb4ae3b0e097f8ab81f94b |
| round-31 | 9693fa3c8a164c97aab3b58f694aaa2644e716a32b31194d55ee744e4cbc8410 | 5fa37fd7249d043af1e36f98a549ee4ac8d6181e29f5def78116d3c637cb50e8 |

## 5. Diff is additions only

```
$ git diff --stat -- corpus/source-snapshots/
 corpus/source-snapshots/round-23/manifest.json | 12 ++++++
 corpus/source-snapshots/round-24/manifest.json | 57 ++++++++++++++++++++++++++
 corpus/source-snapshots/round-25/manifest.json | 15 +++++++
 corpus/source-snapshots/round-26/manifest.json |  3 ++
 corpus/source-snapshots/round-28/manifest.json |  6 +++
 corpus/source-snapshots/round-29/manifest.json |  9 ++++
 corpus/source-snapshots/round-30/manifest.json |  9 ++++
 corpus/source-snapshots/round-31/manifest.json |  3 ++
 8 files changed, 114 insertions(+)

$ git diff -U0 -- corpus/source-snapshots/ | grep -cE '^-[^-]'
0
$ git diff -U0 -- corpus/source-snapshots/ | grep -cE '^\+[^+]'
114
$ git diff -U0 -- corpus/source-snapshots/ | grep -E '^\+\s*"(url|archival|archival_note)"' | wc -l
114     # 38 url + 38 archival + 38 archival_note = 114, i.e. 3 x 38 with no other added line
```

Sample hunks (note the per-file indentation is preserved: 6 spaces in round-23, 3 in round-31):
```
@@ -7,0 +8,3 @@
+      "url": "https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1",
+      "archival": true,
+      "archival_note": "pre-round-32 capture; fetch instant not recorded",
@@ -38,0 +42,3 @@
+      "url": "https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng",
...
@@ -7,0 +8,3 @@            (round-31)
+   "url": "https://www.microsoft.com/en-us/msrc/msvr",
+   "archival": true,
+   "archival_note": "pre-round-32 capture; fetch instant not recorded",
```
Zero deletion lines in `-U0` proves `id`, `path`, `sha256`, `quotes` and `location` values are untouched
byte-for-byte, not merely equal after parsing.

## 6. Independent post-check over all 38 records

```
$ python3 verify.py
records 38 violations 0
```
verify.py re-reads `corpus/SOURCES.md` itself (own row only), takes column 2 of the row for the record
id, and asserts: exactly one row carries the id; `url` is a substring of that cell AND the cell's sole
`https://` token equals `url`; `id`/`path`/`sha256`/`quotes` still present; `archival is True`;
`archival_note` equals the exact note string; no `fetched_utc` (legacy records must not claim one).

Per-file provenance counts after the upgrade:
```
round-23 records=4  url=4  arch=4  fetched=0
round-24 records=19 url=19 arch=19 fetched=0
round-25 records=5  url=5  arch=5  fetched=0
round-26 records=1  url=1  arch=1  fetched=0
round-28 records=2  url=2  arch=2  fetched=0
round-29 records=3  url=3  arch=3  fetched=0
round-30 records=3  url=3  arch=3  fetched=0
round-31 records=1  url=1  arch=1  fetched=0
round-32 records=2  url=2  arch=0  fetched=2   (ExecManifest32's file, not mine)
```

`git status --porcelain` shows only these eight manifests modified by this seat (no other lane path
touched, no capture file rewritten).

## 7. capture-binding-check.py runs

### 7.1 PRE-STATE run (instrument still global-grep; round-32 registry rows not yet appended)

Labeled PRE-STATE / in-flight (M30-3): taken while ExecCaptureBinding's rule B was still the global
grep and ExecRegistryAppend had not yet appended S049/S050, so these numbers are not comparable to a
post-fix column.

```
$ sha256sum corpus/instruments/capture-binding-check.py
5fa7868bf91941d8d9d39c71ba00492d347459ef875fa7d930fb244d01510837  corpus/instruments/capture-binding-check.py
$ python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"
MANIFEST round-23 records=4 url_bound=3 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=18 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=0 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0
FAIL rule=url-ambiguous record=S029 dir=round-23 rows=S024,S029
FAIL rule=url-ambiguous record=S006 dir=round-24 rows=S006,S028
FAIL rule=url-unbound record=S049 dir=round-32
FAIL rule=url-unbound record=S050 dir=round-32
records=40 bound=36 unbound=4
binding_exit=1
```

Read-out: the only two legacy-side failures are the erratum's `multi_row_url` records — rule B was
still binding by URL rather than by id at that sha. The S049/S050 failures are the not-yet-appended
registry rows (an ExecRegistryAppend dependency, not a manifest defect). Rule A passes at this point:
`missing_manifest=0`, `manifest_dirs=9` for `snapshot_dirs=9`.

### 7.2 POST-FIX runs at the final instrument digest (erratum-1 rule B, id-scoped)

ExecCaptureBinding's receipt (`.ufo/waves/round-33/wave1/ExecCaptureBinding.md`) reports the final
instrument; I re-ran it twice on my landed manifests at that digest, byte-identical. The instrument was
later bumped to **b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9** (492 lines,
docstring-only change: fixture-count and summary-field prose) and I re-ran there too: exit 1 twice,
byte-identical, and the output digest is unchanged from the 4bc7aed3… run
(`5b02ec0cf611d640e95ca45e060cca737af9b5a75e8f085ae4f342abe6f4ba9a`), i.e. behaviour-identical.

```
$ sha256sum corpus/instruments/capture-binding-check.py
4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79  (first post-fix digest)
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  (final; docstring-only bump)
$ grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md
48
$ for i in 1 2; do python3 corpus/instruments/capture-binding-check.py > final-run$i.txt 2>&1; echo "exit$i=$?"; done
exit1=1
exit2=1
$ cmp final-run1.txt final-run2.txt && echo IDENTICAL
IDENTICAL
$ sha256sum final-run1.txt final-run2.txt          # same digest at both instrument shas
5b02ec0cf611d640e95ca45e060cca737af9b5a75e8f085ae4f342abe6f4ba9a  final-run1.txt
5b02ec0cf611d640e95ca45e060cca737af9b5a75e8f085ae4f342abe6f4ba9a  final-run2.txt

MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=0 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
FAIL rule=no-row record=S049 dir=round-32
FAIL rule=no-row record=S050 dir=round-32
records=40 bound=38 unbound=2
binding_exit=1
```

Read-out: **all 38 legacy records bind** (url_bound equals records in every one of my eight files);
`multi_row_url=2` is the informational count the erratum mandates (S029, S006) and produces no FAIL;
rule A passes (`snapshot_dirs=9`, `manifest_dirs=9`, `missing_manifest=0`). The only two failures are
`no-row` for S049/S050 — those registry rows are ExecRegistryAppend's pending deliverable
(`grep -c` shows the registry still at 48 rows), not a manifest defect. With those two rows landed the
instrument reaches `records=40 bound=40 unbound=0` (ExecCaptureBinding reproduced that on a scratch
copy of the registry and reported it as simulated, not landed bytes).

Byte stability of my eight files confirmed again after the peer edits landed: same eight sha256 values
as §4 and `git diff -U0` still `0` deletions / `114` additions.

## 8. Status, risks, blockers

- Data side: complete and independently verified (§6, 0 violations over 38 records); every record has
  exactly one of `fetched_utc` / `archival` (legacy: `archival: true`).
- Interface risk raised and resolved by the L1: byte-exact URLs cannot satisfy a global
  "exactly one row" rule for S029/S006 because rows S024 and S028 carry the same URL text. I did not
  alter SOURCES.md (not mine, R8) and did not shade the URLs; the L1 ruled per-id row binding
  (claims-erratum-1.md) and the data already complies.
- Resolved during the round: `capture-binding-check.py` now implements the id-scoped rule B
  (ExecCaptureBinding, digest 4bc7aed3…), and my 38 records bind with 0 rule-B and 0 rule-C failures
  (§7.2).
- One dependency still open at receipt time, and it is not mine: `S049`/`S050` must reach
  `corpus/SOURCES.md` (owner ExecRegistryAppend) before ExecRegressionC1 can measure
  `records=40 bound=40 unbound=0`; until then the instrument's only failures are
  `FAIL rule=no-row record=S049|S050 dir=round-32`.
- Correction I owed the record: my first read of the frozen rule B was the global reading, which is
  unreachable on this registry (two shared URLs). I reported it rather than shading data or editing
  SOURCES.md; the L1's erratum settled the semantics and no manifest byte changed as a consequence.
- No `/tmp` path is used by anything committed here; the transform/verify scripts ran from
  `$HYAKU_SCRATCH/kasegi-r33/ExecManifestUpgrade/` (HYAKU_SCRATCH unset in this shell → default
  `/fast/scratch/hyaku`) and that scratch dir was removed before yield. No clone/worktree was created
  (no git fixture needed: the lane's own read-only `git diff` was sufficient).
- No git/jj mutation was run by this seat; no tool install was needed (python3 stdlib only).
