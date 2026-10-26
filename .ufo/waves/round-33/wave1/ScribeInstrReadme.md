# ScribeInstrReadme — `corpus/instruments/README.md` round-33 append

Seat: ScribeInstrReadme (round 33, wave 1, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`. Answering model: `opencode-go/deepseek-v4.1-flash`
(session route; no model passed). Tools installed/upgraded: **none**. Write scope exercised:
`corpus/instruments/README.md` (append only) plus this receipt and its evidence directory
`.ufo/waves/round-33/wave1/ScribeInstrReadme/`. No other lane file written; no git/jj mutation
(read-only `git show`/`git status` only); no `/home/vgpnk/Projects/shokuknow` access; no live target contacted.

## 1. What landed

| fact | measured value |
|---|---|
| file | `corpus/instruments/README.md` |
| before (HEAD blob, = this seat's pre-edit digest) | `ad2abebd3ad88b70fbfd00a8e89e8fab6d1c53d7254ae285939649ac95756fa2`, 511 lines |
| after | `15dd603ec3cb47fa9dc181f2010790a858c437dedc2184ffcd1fe0eae40139ba`, 656 lines |
| appended section | `## Round-33 additions — \`capture-binding-check.py\` (C1 capture-manifest binding)`, starts at line 513 |
| append-only proof | `git show HEAD:corpus/instruments/README.md` vs `head -n 511` of the working file → `cmp` exit 0 (`PREFIX_IDENTICAL`) |

```
$ sha256sum corpus/instruments/README.md
15dd603ec3cb47fa9dc181f2010790a858c437dedc2184ffcd1fe0eae40139ba  corpus/instruments/README.md
$ wc -l corpus/instruments/README.md
656
$ git show HEAD:corpus/instruments/README.md > .base && head -n 511 corpus/instruments/README.md > .prefix && cmp .base .prefix
prefix_cmp_exit=0
```

Disclosure: the first append edit unintentionally reordered one word on the last pre-existing line
(510, `The other four digests` → `The four other digests`) and then extended the section; it was reverted
within the same minute, before any measurement in this receipt, and the `cmp` above is the final state —
every line 1–511 is byte-identical to HEAD. No other pre-existing line was touched (R6).

Existing anchored citations into this file (`corpus/instruments/citation-survival.md:146`,
`corpus/knowledge/citation-bases.md:25`/`:100`, `corpus/lessons/round-22.md:19`,
`.ufo/waves/round-23/build/FixtureSafety.md:11`/`:23`) all target lines ≤ 511 and therefore still hold
their lines unchanged.

## 2. Instrument facts the section records (all measured by this seat)

Inputs at the measurement instant, on quiescent bytes (instrument mtime 01:23:14, unchanged across 8
consecutive 15 s checks; `corpus/SOURCES.md` stable across 3 checks):

```
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py   (492 lines)
fe89b17a2e059ef0d6e934157fef7c72508f1421e87a82a4aafefad40bc68c3c  corpus/SOURCES.md  (50 S0xx rows)
```

Live run, twice, byte-identical stdout (2026-10-26T04:26:53Z / 04:26:57Z; `diff` of the two bodies exit 0;
sha256 of the 12-line body `5cac3ea71553ea102cbfcf83760a5a798750694bdc2979d02cea057cefb201d9`):

```text
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
binding_exit=0
```

`--selftest` at the same digest: eleven `selftest case=… verdict=pass` lines, `selftest cases=11
failures=0`, `selftest_exit=0`; the scratch root was empty after the run (fixture trees removed at exit).

Second measurement after the registry moved again (`corpus/SOURCES.md`
`b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b`, 50 rows, 2026-10-26T04:29Z;
instrument and round-32 manifest digests unchanged): two runs, byte-identical, same twelve lines, same
body sha256 `5cac3ea7…`, `binding_exit=0`. The registry's Search-log/R8 appends therefore do not move the
verdict; only the two row URLs matter to rule B.

Exit 2 measured, not assumed:

```
--- exit2: root without corpus/source-snapshots
UNAVAILABLE reason=no-snapshot-tree /fast/scratch/hyaku/kasegi-r33/ScribeInstrReadme/e2/nothing
exit=2
--- exit2: snapshot tree present, SOURCES.md absent
UNAVAILABLE reason=read-error [Errno 2] No such file or directory: '/fast/scratch/hyaku/kasegi-r33/ScribeInstrReadme/e2/nosources/corpus/SOURCES.md'
exit=2
```

Registry token shape the section's limit bullet leans on, measured over the 50 rows:

```
rows=50 https_token_count_distribution=[(1, 50)]
```

No-write property: `git status --porcelain corpus/instruments corpus/source-snapshots corpus/SOURCES.md`
before and after every run above lists only the peers' in-flight files (eight ` M` manifests, ` M
corpus/SOURCES.md`, `?? corpus/instruments/capture-binding-check.py`, `?? corpus/source-snapshots/round-32/manifest.json`)
— identical sets, so the checker wrote nothing.

## 3. Manifest-schema note (recorded in the section, re-measured here)

```
$ python3 -c "…walk corpus/source-snapshots/*/manifest.json…"
records=40 url=40 archival=38 fetched=2
distinct archival_note values=1
'pre-round-32 capture; fetch instant not recorded'
```

Per-record fields added: `url` (byte-exact own-row `https://` token), `archival: true` + `archival_note`
(one value across all 38 pre-round-32 records), `fetched_utc` (`2026-10-25T23:14:00-03:00`) on the two
round-32 records only, which carry no `archival` key. The section also pins the nine manifest digests at
the measured state (`round-23` `1f6d4fb5…`, `round-24` `77b158ca…`, `round-25` `251cb5b2…`, `round-26`
`1c913132…`, `round-28` `89f51e05…`, `round-29` `b24a485f…`, `round-30` `8aacf77c…`, `round-31`
`5fa37fd7…`, `round-32` `6e4e719a…`).

"That the legacy manifests gained only fields" is verified, not assumed: for each of the eight
pre-round-32 manifests, the HEAD blob and the working file are compared with the four added keys
(`url`, `archival`, `archival_note`, `fetched_utc`) removed — `hdr_same=True top_extra=[]
records_identical_minus_added=True` for all eight, so `schema_version`, `purpose`, every record's
`id`/`path`/`sha256` and every `quotes` array are byte-identical to base, and the added keys sit between
`path` and `sha256` (`key order ['id','path','url','archival','archival_note','sha256','quotes']`).
Evidence: `schema-delta.txt`.

## 4. Findings

- **F1 — digest provenance, resolved (no defect).** At this seat's first read (01:21) the executor
  receipt's header still showed `4bc7aed3…` / 491 lines; its finalised version
  (`.ufo/waves/round-33/wave1/ExecCaptureBinding.md`, mtime 01:29) carries
  `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` / 492 lines in the header plus a
  digest-history line `bcabe76a…` → `4bc7aed3…` → **`b4182665…`** explaining that the last step is a
  docstring-only correction of the fixture count (`ten` vs the eleven `CASES`). The README section says
  exactly that, and notes that the executor's §3–§7 runs were executed at `4bc7aed3…` with only the
  selftest re-run at `b4182665…`. The landed digest this seat measured twice, quiescent, is `b4182665…`.
- **F2 — contract text vs landed rule B (for the canonical judge).** This seat's dispatch contract says
  rule B requires the `url` to `match EXACTLY ONE corpus/SOURCES.md registry-row URL (grep for the URL text
  in the row's source cell; 0 or 2+ matches = failure)`. The landed instrument and
  `.ufo/waves/round-33/claims-erratum-1.md` §4 use id-scoped binding: a URL that also appears in a
  different row (S024/S029, S006/S028) is **not** a failure and is reported as the informational
  `multi_row_url=2`. Under the literal contract wording, records S029 and S006 could never bind and
  `unbound=0` would be unattainable. The README documents the erratum reading, not the literal one; the
  divergence is recorded here rather than resolved.
- **F3 — PRE-STATE figures, kept apart.** Before ExecRegistryAppend landed rows S049/S050 (48 registry
  rows), the same instrument printed `MANIFEST round-32 records=2 url_bound=0 …`, `FAIL rule=no-row
  record=S049`, `FAIL rule=no-row record=S050`, `records=40 bound=38 unbound=2`, `live_exit=1` (two runs,
  identical). Those numbers are **PRE-STATE** and are not the after column; the post-append run above is.
  The transition is the registry append alone — no manifest or instrument byte changed between the two
  measurements (instrument digest identical, manifest digests identical).
- **F4 — one field beyond the frozen schema.** Legacy records carry `archival_note` in addition to
  `archival`; the checker reads only `archival` and ignores the note. Harmless, recorded in the section
  table so a later reader does not mistake the note for a checked field.
- **F5 — the round-32 capture instant is a commit instant.** `fetched_utc` for S049/S050 is the capture
  commit `288ea9ac…` author timestamp, not a measured HTTP instant (ExecManifest32 §8; quoted in the
  README's limits block). `bound=40` therefore says "40 records name their own documented row and carry
  provenance", not "40 captures were fetched at the recorded instant".

## 5. Out of scope / not done

- Not edited: the instrument, any manifest, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `QUALITY.md`,
  `PROVINCE.md`, `SKILL.md`, `corpus/lessons/round-33.md`, the read-only instrument set, any
  `.ufo/waves/round-33/` control file. The `capture-binding-check` row in the SCORECARD capabilities table
  is ScribeScorecard's item, not this seat's.
- Not run: build/lint/test gates, any network fetch, any campaign tool in `/home/vgpnk/Projects/shokuknow`.
  No claim is authored here; the section reports measurements, it does not assert a score move.
- Known limit of this receipt: the live figures are working-tree measurements — the L1 has not committed
  this round, so no commit-pinned figure is claimed.

## 6. Artifacts

`.ufo/waves/round-33/wave1/ScribeInstrReadme/`: `selftest-run1.txt`, `live-postappend-A.txt`,
`live-postappend-B.txt` (registry `fe89b17a…`), `live-postappend-C.txt`, `live-postappend-D.txt`
(registry `b22c7f01…`), `digests.txt` (instrument + nine manifests + registry), `schema-delta.txt`
(HEAD-vs-working manifest comparison with the added keys removed), `exit2.txt`, `append-only.txt`
(base/prefix `cmp`, registry token distribution, pre-existing anchors), plus the earlier PRE-STATE
captures `live-run1.txt` and `live-run2.txt` (48 registry rows, `bound=38 unbound=2`).
Scratch `$HYAKU_SCRATCH/kasegi-r33/ScribeInstrReadme/` was created empty and removed before this receipt
was finalised; nothing of this seat remains on disk outside the lane.

Re-run (from the lane root):

```
sha256sum corpus/instruments/README.md corpus/instruments/capture-binding-check.py
python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"
python3 corpus/instruments/capture-binding-check.py --selftest; echo "selftest_exit=$?"
```

Targets: README `15dd603e…` / 656 lines (or a later append that keeps lines 1–511 identical);
instrument `b4182665…`; `records=40 bound=40 unbound=0` exit 0; `selftest cases=11 failures=0` exit 0.
