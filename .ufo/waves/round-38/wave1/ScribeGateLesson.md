# ScribeGateLesson — round 38 (lesson sections `## Frozen claims — before → after` and `## Gate`)

Seat: `ScribeGateLesson`, role scribe, axes `depth:verifiability` + `coverage`, milestone round-38.
Leaf seat, no dispatch. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only writes: the two
wave-1 paths named below and scratch). Base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; lane head
observed each time with read-only `git rev-parse`. Scratch
`/fast/scratch/hyaku/kasegi-r38/ScribeGateLesson/` (`TMPDIR` bound there; removed before yield).
Tooling: nothing installed or upgraded (no pacman, no `uv`, no `npx`, no binary downloads); `curl`,
`python3` 3.14.8, `sha256sum`, `cmp`, `tail`, `grep`, `awk` sufficed. No mutating git/jj command ran;
the only mutating git anywhere was none at all (no fixture was needed).

## Behavior

Drafted the two round-38 lesson sections, byte-exact, to `wave1/ScribeGateLesson.block.md`, modelled on
`corpus/lessons/round-37.md` (its `## Frozen claims — before → after` table and its `## Gate` with
Admitted / Rejected / Contested scope / Spot-check readiness). Every number in the block is either a
reading this seat took (base controls, its own fetch and normalization, the instrument outputs quoted
below) or is marked `[L1-MEASURE]` because it exists only at the judged head J.

## Deliverable

| deliverable | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-38/wave1/ScribeGateLesson.block.md` (whole file) | 80 | 27,761 | `fbe900d241edac4be6cf618e917f2712d361ec5a35474abce6e740a446b9c7d3` |

Structure (no fences, so nothing can be pasted twice; no scaffolding, no validation prose outside the
sections' own claims):

```
1:## Frozen claims — before → after          (table C1 / C2 / depth:density + 2 qualifications)
16:## Gate
18:### Admitted — F21 / S055 (OASIS CSAF v2.0, the VEX profile's product status and justification flags)
37:### Rejected
42:### Candidates considered and not taken this round
48:### Standing assimilation refusals — seven staged entries, no flip cleared
64:### Contested scope — kake's security.txt CSAF mention: adjacent, reported not absorbed
70:### Spot-check readiness (what a non-author can re-derive from committed bytes)
```

Vocabulary scans on the deliverable, in full:

```
$ for t in '⟨pending' '<fill>' 'filled by the L1' '<LANE_HASH>' '<r38-' 'TBD' 'TODO'; do \
    printf '%-18s %s\n' "$t" "$(grep -cF -- "$t" ScribeGateLesson.block.md)"; done
⟨pending            0
<fill>              0
filled by the L1    0
<LANE_HASH>         0
<r38-               0
TBD                 0
TODO                0
$ grep -o '<[A-Za-z_][^>]*>' ScribeGateLesson.block.md | sort | uniq -c   → (no output)
$ grep -c '^```' ScribeGateLesson.block.md                                → 0
```

(The `grep -cF '⟨pending'` above is the suite's own kill-rule pattern; the deliverable mentions the
round-37 markers as "the suite's pending markers" and never reproduces the token.)

## Evidence

### 1. Fetch ledger — this seat's own fetches

All with `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, times UTC, 2026-10-26.

| # | URL | HTTP | bytes | fetched UTC | body sha256 |
|---|---|---|---|---|---|
| 1 | https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html | 200 | 414,858 | 18:31:17Z | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` |
| 2 | https://docs.oasis-open.org/csaf/csaf/v2.1/os/ | 404 | 41,334 | 18:32:30Z | error page |
| 3 | https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex | 200 | 49,253 | 18:32:30Z | normalized 115 lines |
| 4 | https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html | 200 | 25,631 | 18:32:50Z | `05ce174dec889a785a8dce287d66cd0f757910336193d0b71453b5143b9f51de` |
| 5 | https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html | 200 | 1,231,332 | 18:32:50Z | normalized 12,240 lines |
| 6 | https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=csaf | 200 | 145,838 | 18:32:50Z | 1 redirect to `groups.oasis-open.org/communities/tc-home2?…` |
| 7 | https://docs.oasis-open.org/csaf/csaf/v2.0/errata01/os/csaf-v2.0-errata01-os.html | 200 | 25,631 | 18:33:34Z | `05ce174dec889a785a8dce287d66cd0f757910336193d0b71453b5143b9f51de` |

Fetch 1, verbatim:

```
http=200 bytes=414858 url=https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html redirects=0 ctype=text/html
fetched_utc=2026-10-26T18:31:17Z
fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b  raw.html
date: Mon, 26 Oct 2026 18:31:18 GMT
content-type: text/html
last-modified: Sun, 05 Apr 2026 13:17:09 GMT
server: cloudflare
```

Rows 4 and 7 are byte-identical: the v2.0 "Latest stage" URL serves the Errata 01 document. Row 2's
404 and row 5's `Committee Specification Draft 04 / 21 October 2026` header are the stage evidence the
deliverable's candidate rows cite.

### 2. Normalization and identity with the landed capture

`raw.html` normalized by importing the lane instrument's own converter (no reimplementation):

```
$ python3 - <<'PY'  # importlib load of corpus/instruments/capture-source.py, then html_to_text(raw)
snapshot_bytes=272441 lines=5146 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
PY
$ cmp S055.txt <wave1>/ExecC2Capture.S055.txt   → BYTE_EQUAL_TO_DELIVERED (before landing)
$ sha256sum corpus/source-snapshots/round-38/S055.txt  (after landing)
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
$ cmp corpus/source-snapshots/round-38/manifest.json <wave1>/ExecC2Capture.manifest.json → MANIFEST_IDENTICAL
```

The curl body's sha256 equals the manifest's `raw_sha256`; the normalized digest equals its `sha256`
and the landed file's. Raw-body variance between clients (414,858 curl vs 415,225 urllib, Δ = the
Cloudflare beacon script) is stripped by `SCRIPT_RE`, which is why the deliverable says to pin the
snapshot digest, never a `Content-Length`.

### 3. Quote pins — word counts and locations read by this seat

Own line reads in `S055.txt` (not copied from a peer): `L2135` Q1 (24 words), `L2844` Q2 (25),
`L2151`+`L2152` Q3 (23, the sentence split by the `For each item in` keyword), `L1767` Q4 (19),
`L1855` (the eight properties named in one sentence), `L1885`–`L1894` (their definitions), `L1757`–
`L1761` (five label enum values), `L1762` (the "reflect the VEX not affected justifications"
sentence), `L1763`–`L1769` (per-label MUST uses), `L2329` (pairwise-disjoint rule). Keyword census:
`MUST` 194, `SHALL` 54, `MUST be tested` 74, lines opening a `6.1.*` heading 88 (66 at `6.1.N`, 22
nested). Term bounds: `CVSS` 73, `KEV` 0, `EPSS` 0, `SSVC` 0, `FIRST` 3 (L435, L437, L1305).

`source-recheck.py` against the delivered manifest, then against the committed paths:

```
# scratch copy: manifest.json + S055.txt side by side
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-ok
S055:Q2 OK occurrences=1 anchor=2844-ok
S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok
S055:Q4 OK occurrences=1 anchor=1767-ok
exit=0

# committed path
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
(same six lines)  exit=0
```

The wave-1 filenames instead of the manifest's `S055.txt` produce `S055:source UNAVAILABLE
reason=missing` exit 2 — recorded in the deliverable as the "manifest and capture in one directory"
requirement.

### 4. Junk control (three runs, own manifests)

```
claims from c2-controls/junk-f21.md at anchor 1 against S055.txt →
S055:sha256 OK
S055:J1 MISMATCH reason=quote-not-found
S055:J2 MISMATCH reason=quote-not-found
S055:J3 MISMATCH reason=quote-not-found
S055:J4 MISMATCH reason=quote-not-found
junk_exit=1

Q1 verbatim, same manifest shape →
S055:Q1 OK occurrences=1 anchor=2135-ok   (exit 0, established by the manifest run in §3)

one-word paraphrase of Q1 (product → component), anchor 2135 →
S055:P1 MISMATCH reason=quote-not-found
paraphrase_exit=1
```

`c2-controls/junk-f21.md` (landed) and `wave1/ExecC2Junk.junk-f21.md` are the same bytes: 23 lines,
983 bytes, sha256 `6742705ec69537cfd949b1a7df506fe8446267c712aaec8b7e714d6cbdaa1630`. The round's own
transcript `c2-controls/junk-f21-recheck.txt` (18:40:48Z) records the same four MISMATCH lines.

### 5. Base controls (before-values in the table)

Own grep/instrument runs against the lane at base/`7001535` (corpus tree unchanged from base):

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                      → 20
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 54
grep -cE '^\|[[:space:]]*S055[[:space:]]*\|' corpus/SOURCES.md  → 0
ls corpus/knowledge/*.md | wc -l                                → 49
python3 corpus/instruments/frontier-recheck-count.py            → entries=23 pass=23 exit=0
python3 corpus/instruments/capture-binding-check.py             → records=44 bound=44 unbound=0
python3 corpus/instruments/recheck-audit.py --quiet             → expected=49 missing=0 unexpected=0 exit=0
```

`.ufo/waves/round-38/c2-controls/before.txt` and `census-before.txt` are the frozen controls for
everything else in the C1/C2 before cells (suite absent, D-A…D-F open, census `W04 S028`/`W04 S029`
only, exit 0); this seat re-read those files rather than re-running their commands.

### 6. Landed-state measurements (after-values), 18:41–18:42Z at head `7001535` + working tree

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                       → 21
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 55
awk -F'|' '/^\| S055 \|/{print "NF="NF}' corpus/SOURCES.md       → NF=13
grep -cE '^\|[[:space:]]*S055[[:space:]]*\|' corpus/SOURCES.md    → 1
ls corpus/knowledge/*.md | wc -l                                 → 50
grep -rlE '^source: S055' corpus/knowledge | wc -l               → 1
sha256sum corpus/source-snapshots/round-38/S055.txt              → 63c8ad52…e11cd42
sha256sum corpus/source-snapshots/round-38/manifest.json         → 95b3f46d…f9a9f
sha256sum corpus/knowledge/csaf-vex-product-status-and-justifications.md → 0343ef45…c5b0a
wc -lc corpus/knowledge/csaf-vex-product-status-and-justifications.md → 137 22887
grep '^| S055 ' corpus/SOURCES.md > landed.row; sha256sum landed.row → 901309af…f96cc  (= ScribeRowS055.row.md)
grep '^| F21 '  corpus/README.md  > landed.f21; sha256sum landed.f21 → 17743c05…d0c8488f (= readme-row.md)
python3 corpus/instruments/frontier-recheck-count.py  → PASS F21 … ids=S055 exit=0 ; entries=24 pass=24 exit=0
python3 corpus/instruments/capture-binding-check.py    → MANIFEST round-38 records=1 url_bound=1 fetched=1 ; records=45 bound=45 unbound=0
python3 corpus/instruments/recheck-audit.py --quiet   → lines=50 total=50 pass=50 … expect=present expected=50 missing=0 unexpected=0 exit=0
bash …/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
  kasegi W04 S028 … / kasegi W04 S029 … / kasegi ok … → census_exit=0
```

Entry identity: `cmp`/`diff -u` between `wave1/ScribeEntryF21.entry.md` and the landed entry is empty —
both 137 lines, 22,887 bytes, `0343ef45…`. Earlier in the wave the same path held 22,831 bytes /
`545303c7…`, and the row seat's mirror used `96899762…`; the deliverable records the drift so a census
claim names bytes, not a filename.

### 7. C1-side facts this seat measured

```
grep -c '^Correction (round 38)' PROVINCE.md corpus/README.md SCORECARD.md → 1 / 1 / 1 (L154, L457, L1511)
fence walk (open = bare or info-string ```; close = bare ```) →
  PROVINCE.md       fence_state_at_eof=closed last_open=81  last_close=124
  corpus/README.md  fence_state_at_eof=closed last_open=426 last_close=455
cat .ufo/waves/round-38/declared-blocks.txt
  corpus/README.md 32 f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff
  PROVINCE.md 4 797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf
tail -32 corpus/README.md | sha256sum → f0318ac8…fbbdff  (equal)
tail -4  PROVINCE.md      | sha256sum → 797666b9…d3acf  (equal)
```

Carry-over conditionality, measured:

```
$ bash corpus/instruments/r37-closure.sh --export-ref a173b0c2… --work "$S/g8/w2"
E1..E8, E10..E14 … closed=1
E9 payload=status-read=ok,status-dirty=3,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent closed=0
closed=13/14 exit=1
```

Cause, from the suite's own `check_e9()` (`corpus/instruments/r37-closure.sh:560-612`): it reads the
live lane's `git status --porcelain` (3 untracked round-38 wave paths), requires `HEAD == the exported
ref` (live head was `7001535`, ref `a173b0c2`, so `head-match=0`), the lane-root identity, and the
`/fast/scratch/hyaku/kasegi-r37` directory scan. The freeze's `closed=14/14` is the same suite with
the live head at the ref and a clean tree. `r38-closure.sh` and
`.ufo/waves/round-38/final-gates/` did not exist at this seat's last read, so every suite number in the
deliverable's C1 after cell is `[L1-MEASURE]`.

### 8. Sibling sweep and the kake hit

```
$ for d in */; do … grep -rliE '\bCSAF\b|Common Security Advisory Framework' --include=*.md \
    --exclude-dir=.ufo --exclude-dir=.git "$d" | wc -l; done
kake-shokunin files=1   (corpus/knowledge/security-txt-publishing.md, line 63)
(all other 19 sibling lanes: 0; kasegi itself: 0)
$ grep -n 'CSAF' kake-shokunin/corpus/knowledge/security-txt-publishing.md
63:  be ignored (S078); securitytxt.org already lists one extension, `CSAF` (S079).
$ grep -rliE 'CSAF|Common Security Advisory Framework|\bVEX\b' corpus/knowledge corpus/README.md corpus/SOURCES.md SKILL.md PROVINCE.md | wc -l  → 0 (lane, at base)
```

`wave1/ScoutF21Sibling.md` widens the pattern (case-insensitive, plus `product_status`,
`known_not_affected`, `openvex`, CycloneDX VEX, whole-repo, and all of `shokuknow/merge`) and finds the
same single site plus four classified false-positive families; the deliverable's contested-scope
ruling rests on that and on this seat's own narrower sweep.

## Gates / criteria touched

- **coverage (C2):** the Gate section carries all five elements the item names — an Admitted block with
  URL, access date, four ≤25-word located quotes with normalized-line numbers, kind/tier reasoning; a
  Rejected block for the junk twin with reasons and a content-specificity control; three candidates
  considered and not taken with reasons and flip conditions; seven standing assimilation refusals with
  reasons and flip conditions; and a contested-scope ruling for the kake security.txt mention.
- **depth:verifiability (C1):** the before/after table states each of G1–G8 with the base reading from
  the frozen controls, records the one C1 fact set measured here (corrections, fence state, declared
  blocks) and marks the suite's own verdicts `[L1-MEASURE]`; the G8 conditionality is stated with the
  measured `E9` payload rather than a claim of green.
- No lane file was edited by this seat; the deliverable is a wave-1 artifact for the L1 to place.

## Findings

1. **G8's `closed=14/14` is not ref-independent.** The r37 suite's E9 limb reads the live lane; at a
   head newer than the exported ref it reds on `head-match=0`/`status-dirty=N` with the thirteen carried
   checks green. Whichever limb `r38-closure.sh` uses for G8 must run with `HEAD == export-ref` and a
   clean tree, or accept the E9 payload as part of the record.
2. **The row-draft divergence resolved by landing.** Three drafts plus one search-log bullet described
   the S055 row with different prose and two different cadences; the landed line is the scribe's
   (`901309af…`), `NF=13`, recheck `180d`. The other drafts stay in wave-1 as evidence of the choice and
   are not what a spot-check should read.
3. **Entry digest drift across seats** (`96899762…` → `545303c7…` → `0343ef45…`) means a census or
   QUALITY verdict is only meaningful against the bytes it ran on; at this head the landed entry and its
   deliverable are byte-identical.
4. **Binding and content checks are disjoint, by design.** `capture-binding-check.py` never opens capture
   bytes: deleting `S055.txt` leaves `records=45 bound=45 unbound=0` exit 0 (`wave1/ExecC2Binding.md` M2).
   The URL/provenance/accounting verdict is the binding check's; the digest and quote verdict is
   `source-recheck.py`'s — the deliverable's spot-check list splits the two rather than merging them.
5. **The harness is a live-lane measurement.** `frontier-recheck-count.py` re-executes each row's
   `cd`-prefixed `recheck:` line, so `entries=24 pass=24` is only reproducible in a lane, not from an
   export. Recorded as a caveat, not a defect.
6. **The front-door corrections are checkable without the suite.** Both declared blocks re-hash to
   their declared digests from the file tails, both files' fence state at EOF is closed (last opener /
   closer pairs 81/124 and 426/455), and the three `Correction (round 38)` lines exist at L154 (PROVINCE),
   L457 (README), L1511 (SCORECARD) — the same facts G1 and G5 assert, measured independently here.
7. **The v2.0 stage has three artifacts, and the row binds one.** `csaf-v2.0-os.html` (OS, 18 Nov 2022)
   is the captured text; the header's latest-stage URL serves Errata 01 (26 Jan 2024, prose and
   conformance unchanged, only the aggregator schema); v2.1 exists only as CSD 04 (21 Oct 2026, public
   review 23 Oct–6 Nov 2026, `/os/` 404). The Gate names all three so a reader cannot mistake the
   latest-stage link for the pinned text.

## Out of scope

- The r38 suite and the final-gates receipt did not exist at this seat's last read; C1 verification was
  not this seat's item and was not attempted. Values that require J are marked `[L1-MEASURE]`.
- No QUALITY review of the landed entry, no registry or frontier edits, no census run at a committed
  head (the run above is the working tree), no assimilation adoption, no sibling-lane write, no
  shokuknow or fleet-root write, no service restart, no pacman transaction.

## Touched surfaces

- Wrote: `.ufo/waves/round-38/wave1/ScribeGateLesson.block.md` (deliverable),
  `.ufo/waves/round-38/wave1/ScribeGateLesson.md` (this receipt), and scratch under
  `/fast/scratch/hyaku/kasegi-r38/ScribeGateLesson/`.
- Read-only elsewhere: lane `corpus/` tree and instruments, wave-1 receipts and deliverables, frozen
  claims and controls, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
  `kake-shokunin/corpus/knowledge/security-txt-publishing.md`; read-only git only (`rev-parse`,
  `status`, `archive` was not needed).

## Artifact paths (lane-relative)

- `.ufo/waves/round-38/wave1/ScribeGateLesson.block.md` — 80 lines, 27,761 bytes, sha256
  `fbe900d241edac4be6cf618e917f2712d361ec5a35474abce6e740a446b9c7d3`
- `.ufo/waves/round-38/wave1/ScribeGateLesson.md` — this receipt
- scratch `/fast/scratch/hyaku/kasegi-r38/ScribeGateLesson/` — removed before yield
