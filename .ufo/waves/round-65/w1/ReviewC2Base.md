# ReviewC2Base — independent base measurement (C2) + S098 source screen

Round 65 predata, seat ReviewC2Base (leaf). Base `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`
(`git rev-parse HEAD` in the lane at measurement time). Read-only: no production file
edited, no commit, no mutating git/jj command, no tool installed, no pacman transaction.
Artifacts: `w1/ReviewC2Base/before.txt`, `w1/ReviewC2Base/source-check.md`,
`w1/ReviewC2Base/NOTES.md`; scratch `/fast/scratch/hyaku/kasegi-r65/ReviewC2Base/`
(base export, captures, generator script).

## BEFORE numbers (every value is the literal output of the command printed above it in `before.txt`)

| counter | value |
|---|---|
| `frontier-recheck-count.py` (lane root) | `FRONTIER-CENSUS rows=43 admitted=43 closed=43 problem-rows=0 registry=97`; `entries=46 pass=46 exit=0` |
| `capture-binding-check.py` (lane root) | `AUDIT records=78 with_url=78 with_fetched_utc=40 with_archival=38 snapshot_dirs=38 manifest_dirs=38 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt`; `records=78 bound=78 unbound=0 exit=0` |
| `recheck-audit.py` (lane root) | `strict pass=72/81 cdroot_fail=0 instrument_fail=0 own_fail=0`; `executes=59 gated=22 broken=0`; `lines=81 total=81 pass=72 fail-closed=22 parse_fail=0 cwd_fail=9 paths_fail=0 exit=1`; `expect=present expected=81 missing=0 unexpected=0 exit=1` |
| `wc -l corpus/instruments/knowledge-expected.txt` | 83 (2 `#` lines + 81 `corpus/knowledge/` paths) |
| `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` | exit 0 |
| `ls corpus/knowledge/*.md \| wc -l` | 81 |
| `grep -c '^\| S[0-9]' corpus/SOURCES.md` | 97 |
| `grep -c '^\| F[0-9]' corpus/README.md` | 45 (but the census's row set is 43 — see R2) |

Instrument digests measured: `frontier-recheck-count.py 010897bc…`, `capture-binding-check.py
ebc206d4…`, `recheck-audit.py 451047ea…`, `knowledge-expected.txt a8833bb1…`.

## Findings

### R1 — HIGH (blocks any "base is green" or "delta" claim on `recheck-audit`)

`recheck-audit.py` **exits 1 at base**: `pass=72/81`, `cwd_fail=9`, `paths_fail=0`,
`parse_fail=0`. The nine are the frozen-`cwd`-limb entries that also carry `foreign=2`
(round 64 named them: cisa-vulnrichment-adp-enrichment, cisa-vulnrichment-record-list,
github-repository-security-advisories-rest-api, nvd-api-2.0-response-schema,
nvd-api-2.0-retrieval-interface, openssf-scorecard-checks, osv-affected-range-events,
project-zero-big-sleep-sqlite-variant-analysis, project-zero-fuzzilli-vs-bigsleep-comparison
— `w1/ScopeConnect.md:70`). C2 must not present `recheck-audit` as green-before, and no
C2 claim may sell this round as closing the `cwd` limb.

Second limb of the same finding — **the copy run is not a base measurement**:
`recheck-audit.py --root <export>` prints `strict pass=1/81 cdroot_fail=71 … exit=1`,
because strict limb (d) requires the `cd <path> &&` target to equal the audited root
(`corpus/instruments/recheck-audit.py:27`, `:143`). Only the lane-root run (72/81,
`cdroot_fail=0`) is quotable; `before.txt` keeps the export figure labelled
`BEFORE export_recheck_strict_pass 1` and nothing else.

### R2 — HIGH (blocks the coverage arithmetic)

Two different "frontier row" numbers exist at base: `grep -c '^| F[0-9]' corpus/README.md`
→ **45**, `grep -cE '^\| F[0-9]+ \|'` → **45**, while the census's row set is **43**
(`FRONTIER-CENSUS rows=43 admitted=43 closed=43`). The two extra matches are not frontier
rows — they are continuation rows for existing entries:

```
README.md:699  | F02 coordinator case: ZDI's conditional disclosure timelines, unknown 120-day clock start and acquired-finding disposition | `corpus/knowledge/zdi-disclos…
README.md:700  | F29 current capture provenance | `corpus/knowledge/github-repository-security-advisories.md` | S076 supersedes S074 …
```

So F44 makes the frontier **44**, not 46. Any receipt that quotes the grep's 45 as the
base overstates coverage by 2 (and would let a single landing look like two).

### R3 — HIGH (blocks the S098 capture from binding correctly)

The document is served at two HTTPS spellings that resolve to **different page paths**:

```
.../psirt_services_framework_v1.1   -> final .../psirt_services_framework_v1.1   229255 B  sha256 3a1b5c1a…
.../psirt_services_framework_v1.1/  -> final .../psirt_services_framework_v1-1   229255 B  sha256 cf58a500…
http://.../psirt_services_framework_v1.1 -> redirects to the https dot form
```

Raw diff between the two spellings is two lines (the `og:url` meta and a per-response
script nonce), and **the text snapshots are byte-identical**
(`cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`). Because
`capture-binding-check.py` rule B5 compares the record `url` to the row's `https://` token
byte-for-byte, the registry row must carry the **dot, no-trailing-slash** spelling and
exactly one `https://` token. A trailing-slash row would bind a URL that resolves to
`v1-1`; the digest would still match, so nothing else would catch it.

### R4 — HIGH (landing-order defect, measured live)

A sibling seat captured S098 into `corpus/source-snapshots/round-65/` **before** the
registry row existed. The counter then reads:

```
MANIFEST round-65 records=1 url_bound=0 fetched=1 archival=0
FAIL rule=no-row record=S098 dir=round-65
AUDIT records=79 … orphans=1 orphan=S040-live.txt
records=79 bound=78 unbound=1        [exit=1]
$ grep -c '^| S098 ' corpus/SOURCES.md
0
```

So the capture-binding counter goes red purely on ordering: base `records=78 bound=78
unbound=0 exit=0` → intermediate `records=79 bound=78 unbound=1 exit=1`. The registry row
and the manifest must land in the same change (row first is safest), or the round's own
gate fails on a correctly renamed file.

**Resolved at the landed HEAD** (`1c36d72`): row and manifest landed together —
`MANIFEST round-65 records=1 url_bound=1 fetched=1`, `records=79 bound=79 unbound=0`,
exit 0 (see "Post-landing verification" below). The finding stands as a landing-order
requirement, not as a defect in the landed tree.

### R5 — MEDIUM (anchor hygiene, measured)

The FIRST site chrome is byte-identical across every FIRST capture in the lane:

```
$ for f in round-24/S001 round-24/S002 round-36/S053 cap1/S098; do sed -n '198,206p' "$f" | sha256sum; done
bac145c2bf99e8cf8930f0e7649991dce48001ea76a61c5b5db43e8e9ec30ca4   (all four)
```

and the title string already occurs in three published snapshots (`S001:201`, `S002:201`,
`S053:201` → `grep -rn 'PSIRT Services Framework' corpus/source-snapshots/ | wc -l` → 3).
Anchor lines taken from L1–L215 or L1537–L1573 therefore identify FIRST's navigation, not
this document. The document body is **L216–L1536** (H1 L1, content-column title L216,
`Also available in PDF.` L217, `Purpose` L218, Service Area 1 L402 … Service Area 6
L1309, last reference L1536, footer nav L1537). The sibling manifest's `body_lines`
`[216, 1450]` is inside that span and is consistent with it.

### R6 — MEDIUM (what the digest can and cannot mean)

`Last-Modified: Mon, 26 Jan 2026 14:43:46 GMT`, no `ETag`, no publication or revision
date in the text, and a rolling copyright line (`L1573 Copyright © 2015—2026 …`). Raw
bytes carry a per-response script nonce, so the raw sha256 is not a content digest (it was
stable across four fetches in ~3 min, and identical for the dot form on repeat). The
honest claim is "snapshot `cfa42e23…`, 170137 bytes, 1573 lines, captured
`2026-11-04T19:26:49Z`", never "the page says X today". Offline re-parse of the saved raw
bytes reproduces the pinned digest (`matches_capture=True`), so the transform is
deterministic independently of the network.

### R7 — MEDIUM (F44 must attribute, not repeat, superseded ISO editions)

The framework cites `ISO/IEC 30111:2013` (L1444, L1514, L1522, L1523) and
`ISO/IEC 29147:2014` (L1445, L1513, L1515–L1517). The lane's F38 rows already record the
current editions — `S089` = `ISO/IEC 29147:2018` (`https://www.iso.org/standard/72311.html`),
`S090` = `ISO/IEC 30111:2019` (`https://www.iso.org/standard/69725.html`). An F44 entry
that restates 2013/2014 as current contradicts F38; it may quote them only as the
framework's own citations.

### R8 — LOW (identifier is free but not historically virgin)

Registry rows end at `S097` (`grep -oE '^\| S[0-9]{3} ' | sort -u | tail -3` → S095, S096,
S097); `S098` appears in no current document (`grep -n 'S098' LOG.md SKILL.md SCORECARD.md
PROVINCE.md corpus/README.md` → empty; `grep -rn '055110' … corpus/` → empty). But three
in-tree round-24/28 receipts used `S098` for a different, never-landed staged row
(`www.055110.com`; `.ufo/waves/round-24/wave1/ScoutCensus.md:65`, `ScoutMergeOther.md:53`,
`.ufo/waves/round-28/wave1/ConnStagedCensus.md:131`). Reuse is correct; the receipt should
say so, so two different S098s in `.ufo/waves` are explained rather than discovered.

### R9 — INFO (three correct numbers that are easy to misquote)

`knowledge-expected.txt` is 83 physical lines = 2 comments + 81 paths; `sort -c` exit 0;
`corpus/knowledge/*.md` = 81; the audit prints `expected=81 missing=0 unexpected=0`. The
`expected=` value is the post-comment count, not the `wc -l` value.

### R10 — INFO (do not "fix" the declared orphan)

`capture-binding-check.py` prints `orphans=1 orphan=S040-live.txt` at base and **still
exits 0**, because the manifest declares it with a reason (rule A2). It is not a defect
introduced by this round and must not be counted as one.

### R11 — INFO (independent corroboration of the S098 digest)

Two independent capture runs produced the same snapshot: the sibling's at
`2026-11-04T19:26:27Z` and mine at `19:26:49Z` — `cmp` printed
`CMP_WITH_MY_CAPTURE=identical`. That is the strongest stability evidence available here
and is separate from my own repeat-fetch evidence.

## Coverage screen for F44 (C2 axis)

The candidate is distinguishable **on subject**, not on publisher:

* **This source** — a PSIRT service taxonomy: `SERVICE AREAS – SERVICES – FUNCTIONS –
  SUB-FUNCTIONS` (L226–L227), 6 service areas (`grep -c '^Service Area [0-9]'` → 6),
  84 `Function` headings, 81 `Sub-function` headings, an explicit PSIRT-vs-CSIRT section
  (L243) and organisational models (`Distributed Model` L249, `Centralized Model` L259).
* **F43 / S095** — CERT/CC's phase-to-five-role responsibility matrix
  (`corpus/SOURCES.md:104`); object = phases × roles. Not a service catalogue.
* **F06 / S018** — FIRST multi-party coordination guidelines (`corpus/SOURCES.md:24`);
  object = multi-party coordination practice. S098 is single-organisation capability
  design.
* `coordinated disclosure` occurs **4** times in 1573 lines (L477, L480, L731, L1197), so
  the disclosure process is one sub-function here, not the document's subject.

No URL, title, or scope duplicate exists in `corpus/SOURCES.md` or `corpus/knowledge/`
(`grep -c 'psirt_services_framework' corpus/SOURCES.md` → 0; `grep -rin 'psirt services
framework' corpus/knowledge/ corpus/SOURCES.md corpus/README.md | wc -l` → 0; the registry
holds four other FIRST URLs: S001, S002, S018, S053).

## Post-landing verification (HEAD `1c36d724c91cdd8585219798ea7cf60bb4f24b5b`; labelled, not the base)

The integrator landed the round during this seat (`round-65: land signal-fail-closed derive
gate and F44 PSIRT services catalogue`). Re-running the same read-only commands at that HEAD
yields **base + 1 on every C2 counter**, i.e. the landing moved exactly its own row/entry:

| counter | base `a283189` | landed `1c36d72` |
|---|---|---|
| capture-binding `records/bound/unbound` | 78/78/0, exit 0 | 79/79/0, exit 0; `MANIFEST round-65 records=1 url_bound=1 fetched=1` |
| frontier `entries= pass=` | 46/46, census rows 43 | 47/47, census rows 44, `PASS F44 … ids=S098` |
| recheck `strict pass` | 72/81, exit 1 | 73/82, exit 1 (`cwd_fail=9` unchanged) |
| `knowledge-expected.txt` lines / paths | 83 / 81 | 84 / 82 (`sort -c` exit 0) |
| `corpus/knowledge/*.md` | 81 | 82 |
| registry rows (`grep '^| S[0-9]'`) | 97 | 98 |
| `grep -c '^| F[0-9]'` README | 45 (census 43) | 46 (census 44) |
| recheck `executes / gated` | 59 / 22 | 60 / 22 |

Verification of the landed artefacts against my independent capture:

* **R3 honoured** — the S098 row carries the dot spelling and exactly one `https://` token
  (`grep '^| S098 ' corpus/SOURCES.md | awk -F'|' '{print $3}' | grep -o 'https://' | wc -l`
  → 1; counter `url_bound=1`, `bound=79 unbound=0`).
* **Row figures supported** — `grep -cE '^Service [0-9]+\.[0-9]+' cap1/S098.txt` → 28
  (`sort -u` → 28), plus 6 service areas and 84 functions, matching the row's "six service
  areas, 28 services and 84 functions".
* **Entry is bound** — its `recheck:` line invokes
  `source-recheck.py --manifest corpus/source-snapshots/round-65/manifest.json --source S098`
  and the audit moves from `gated=22`/`executes=59` to `executes=60` with one more pass.
* **Cited anchors exist** — `PSIRT Framework Structure` L226, `Service 2.1` L680,
  `Service 3.1` L849, `Service 3.3` L904.
* **R1 unchanged** — the audit still exits 1 on `cwd_fail=9`; this landing neither claims
  nor achieves a green verifiability counter.

## Residual risk

* The page is mutable; only the snapshot-bound claim survives. A re-capture on another day
  may legitimately differ (year roll, nonce, site rebuild) — pin the snapshot, not the host.
* `recheck-audit` remains red at base on the `cwd` limb (9 entries). If the round touches
  `recheck-audit.py` or `knowledge-expected.txt` for other reasons, the 72/81 value must be
  re-measured and re-labelled by date, not carried forward.
* The `S098` id remains free in the registry but historically carries a different, unlanded
  round-24 staged source; an unqualified `S098` in a future receipt may be read either way
  unless the reuse is stated.

## Verification gaps (what I did not check, stated plainly)

* I did **not** run the C1 work: `figure-audit.py`, its selftests, or the
  `upstream-python-signal-ignored` case. That is C1's counter; this receipt measures only
  the four C2 counters plus the source screen.
* I did **not** review `w1/EntryS098/` draft anchors/quotes or `w1/ScopeF44/screen.md`;
  those are other seats' artifacts and are unread by me.
* I did **not** verify that the round's F44 row, entry, expected-list sync, and recheck
  line land correctly — predata only; nothing here is admitted.
* Raw-byte stability was sampled over ~25 s plus repeated fetches; I did not wait hours.
  The two-runner digest identity (R11) is the stronger evidence, not the time window.
* `git status --porcelain` gained `?? corpus/source-snapshots/round-65/` from a sibling
  during the session; my writes are confined to `w1/ReviewC2Base*`.

Report: .ufo/waves/round-65/w1/ReviewC2Base.md
