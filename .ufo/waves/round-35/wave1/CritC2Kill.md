# CritC2Kill — falsifying C2 as declared (round 35)

Seat: attack critic, C2 (coverage) kill attempt. Write scope: lane repo only; all work trees under
`/fast/scratch/hyaku/kasegi-r35/CritC2Kill/` (removed before yield). No lane edit, no git/jj mutation,
no subagent, no peer broadcast.

## Report

### Mandate

Build four junk constructions that satisfy the C2 shape counters (frontier=18, registry rows=52, S052
row present, harness entries=21 pass=21) without a real capture or a real admission, run the landed
checks against each, and state which checks catch which and what remains.

### Verdict (short)

C2 **is not falsified as an artifact claim**, and one part of it **is falsified as a verifiability
claim**.

- Not falsified on substance: the landed S052 capture is byte-identical, after the declared `collapse()`
  normalization, to a live fetch of the KEV feed made by this seat at 2026-10-26T03:41Z
  (1,807,090 served bytes → 1,479,694 normalized bytes → sha256 `d69349e8…8826`, `IDENTICAL`); the
  landed entry's own FC-1/FC-3/FC-6/FC-9/FC-10 claims re-compute true; all six C2 counting commands hold
  at the measurement instant.
- Falsified on verifiability: the only automated "admission gate" is `frontier-recheck-count.py`, which
  binds an entry to its own `recheck:` line and the manifest that line names. It never reads the entry's
  assertions. Three of the four constructions below therefore pass **every** landed check, and the
  **declared junk-twin control is false as built**: `c2-controls/junk-f18.md`'s recheck line is the same
  S052 selection the real entry runs and **exits 0**, and the same bytes pass the harness as an admitted
  row.

Per the frozen kill rule ("junk twin passes source-recheck or is admitted"), the *control artifact*
triggers the clause. Round judgment stays with the L1; the measurable statement is: no landed check
rejects the junk twin, and the after-condition `junk twin rejected: source-recheck exit != 0` is not
reproducible from the committed bytes.

### Measurement instant and live artifacts

`date -u` → `2026-10-26T06:42:44Z`. Counters at that instant (commands verbatim from claims.json):

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                                  -> 18
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        -> 52
grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md              -> 1
grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l                     -> 1
ls corpus/knowledge/*.md | wc -l                                            -> 47
python3 corpus/instruments/frontier-recheck-count.py                        -> PASS F18 knowledge/cisa-kev-catalog.md ids=S052 exit=0
                                                                              entries=21 pass=21 exit=0   (harness_exit=0)
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
  S052:sha256 OK / Q1..Q5 OK (Q3,Q4,Q5 normalized=markup-whitespace, occurrences=1, anchors 2,3,4,15472,19165) -> exit=0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <live>/corpus/SOURCES.md --today 2026-10-26
  W04 S028, W04 S029, ok                                                        -> census_exit=0
python3 corpus/instruments/capture-binding-check.py --root .
  AUDIT records=42 with_url=42 with_fetched_utc=4 with_archival=38 snapshot_dirs=11 manifest_dirs=11
        missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
  records=42 bound=42 unbound=0                                                  -> exit=0
python3 corpus/instruments/recheck-audit.py
  strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0
  lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
  expect=present expected=47 missing=0 unexpected=0 exit=0
```

File digests at that instant (`sha256sum`):

```
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md
a5696dc057a7fb608f3d77f21f0101fb150de8f8d0455090fb6a4e4d9e58c838  corpus/knowledge/cisa-kev-catalog.md   [at 06:42:44Z]
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
d2e99ca60bc5acf109a60a26452379bc8d428ea0cb382f1e513696a7873347a8  corpus/instruments/knowledge-expected.txt
0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176  .ufo/waves/round-35/c2-controls/junk-f18.md
```

Re-measured at 2026-10-26T06:44:21Z: `corpus/README.md`, `corpus/SOURCES.md` and the round-35
`manifest.json` carry the same digests; `corpus/knowledge/cisa-kev-catalog.md` moved from `a5696dc0…`
to `0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74` (a peer seat's edit between the
two instants). The substance was re-verified at the newer bytes: `PASS F18 … ids=S052 exit=0`,
`entries=21 pass=21 exit=0`, `source-recheck S052` exit 0, and FC-9/FC-10 still present at the entry's
lines 36/38 with their runnable checks at lines 96/97. `corpus/source-snapshots/round-35/S052.txt`
measures 27,870 lines / 1,479,694 bytes (`wc -c -l`), matching the manifest `purpose` and the entry
header at both instants.

Out-of-band authenticity control (network, read-only, `/fast/scratch` only):

```
curl -sS -o S052-live.json https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
  -> 1807090 bytes, curl_exit=0
collapse(live) -> 1479694 bytes sha256 d69349e8…8826
snapshot        -> 1479694 bytes sha256 d69349e8…8826
-> IDENTICAL        (capture-source.py collapse(): BLANK_RE per line + strip + drop blank lines)
```

So the landed capture is the real document, not an error page. That is **external** evidence: no
landed instrument performs this comparison (gap G2 below).

### Constructions, with runs

Scratch lane: `cp -a corpus /fast/scratch/hyaku/kasegi-r35/CritC2Kill/lane/corpus` (5.7 MB); the
builder is `/fast/scratch/hyaku/kasegi-r35/CritC2Kill/build.py`. Four junk registry rows S090–S093
were inserted inside the `## Registry` table (an EOF append is `E12 row outside Registry section`, exit 1
— placement matters and was measured first), and frontier rows F90–F93 were appended to the scratch
`corpus/README.md`. All instrument runs below are `--root .` from the scratch lane root.

**J1 — entry quoting a fabricated string with a fake manifest record.** Invented quote
`"this sentence was invented by the attack seat and never appeared in any real document"` asserted at
anchor 2 of a 3-line fabricated capture `round-35/junk1/S091.txt`, sha256 over those bytes, registry row
S091 whose https token equals the record `url`, entry `knowledge/junk1-fabricated.md` quoting it.

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/junk1/manifest.json --source S091
  S091:sha256 OK
  S091:Q1 OK occurrences=1 anchor=2-ok                                           exit=0
python3 corpus/instruments/frontier-recheck-count.py --root .
  PASS     F90  knowledge/junk1-fabricated.md                        ids=S091           exit=0
  entries=23 pass=23 exit=0                                                      exit=0
python3 corpus/instruments/capture-binding-check.py --root .
  MANIFEST round-35/junk1 records=1 url_bound=1 fetched=1 archival=0
  records=46 bound=46 unbound=0                                                  exit=0
```

→ **not caught**: self-consistent fabrication is indistinguishable from a capture at every landed check.

Sub-cases that *are* caught (the discriminating half of the same construction):

```
J1b assertion quote absent from its own capture (S093)
  python3 corpus/instruments/source-recheck.py --manifest …/junk1b/manifest.json --source S093
    S093:sha256 OK
    S093:Q1 MISMATCH reason=quote-not-found                                      exit=1
J1c fabricated assertion appended to an otherwise real manifest over the real S052 capture
  Q6 "five exploited vulnerabilities to the catalog every Tuesday"
  python3 corpus/instruments/source-recheck.py --manifest …/junk3/manifest.json --source S052
    S052:Q1..Q5 OK …  S052:Q6 MISMATCH reason=quote-not-found                    exit=1
  python3 corpus/instruments/frontier-recheck-count.py --root .
    FAIL     F91  knowledge/junk3-s052-never-opened.md ids=S052 exit=1 problems=recheck-exit-1
    entries=24 pass=23 exit=1                                                    exit=1
```

**J1d — the entry's own quote and its stated digest are never read.** `source-recheck.py`'s CLI takes
`--manifest`, `--source`, `--selftest` only (`main()`, lines 393-415) — there is no way to assert a quote
from an entry. `anchorcheck.py` on the junk entry *and* on the landed F18 entry:

```
python3 corpus/instruments/anchorcheck.py corpus/knowledge/junk5-junktwin.md
  == … junk5-junktwin.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; …            exit=0
python3 corpus/instruments/anchorcheck.py corpus/knowledge/cisa-kev-catalog.md
  == … cisa-kev-catalog.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; …          exit=0
```

Bare `L2`, `L5423`, `L15472` refs are not anchored tokens, so the F18 entry's extra quotes (the FCEB
sentence `L5423`, the BOD 22-01 sentence `L2246` — deliberately outside the manifest) and its header
digest claim are machine-unchecked. Proof: stamping a 64-zero sha256 into the junk entry's `source:`
line leaves the harness verdict untouched:

```
PASS     F90  knowledge/junk1-fabricated.md                        ids=S091           exit=0
```

**J2 — a row with no opened source.** S090: `status mined`, `opened 2026-10-26`, `used-by —`, no
capture, no manifest record anywhere.

```
sources-census.sh validate --file <scratch>/corpus/SOURCES.md --today 2026-10-26
  W04 S028, W04 S029, W03 S090 mined but unused, W04 S092 …, ok                  exit=0
```

Sharpened variant S093 (`mined`, `opened 2026-10-26`, `used-by corpus/knowledge/junk1-fabricated.md`
— a real path — still no capture): validate prints **no line for S093 at all**. `capture-binding-check`
sees only manifests (`records=46` against 56 rows) and passes. A non-date `opened` cell *is* caught —
`E08 S090 opened=—`, and with that defect `census_exit=1` — so census checks the cell's shape, not that
an opening occurred.

Live-tree magnitude: 52 registry rows vs 40 distinct manifest record ids → **12 rows carry no capture**
(`S016,S017,S019–S028`); **0 of them are `mined`**. The invariant "mined ⇒ capture record" holds today
and is enforced by nothing (gap G3).

**J3 — an entry citing S052 that never opened the KEV JSON.** `knowledge/junk3-s052-never-opened.md`:
header `source: S052`, prose citation, `recheck:` line = the real round-35 manifest selection, body
quoting `"five exploited vulnerabilities to the catalog every Tuesday"` and `"scores each entry with a
CVSS v4 vector rather than a due-date"` — both absent from `S052.txt`.

```
PASS     F91  knowledge/junk3-s052-never-opened.md                 ids=S052           exit=0
entries=23 pass=23 exit=0                                                          exit=0
source-recheck --manifest corpus/source-snapshots/round-35/junk3/manifest.json --source S052 -> exit=0
```

→ **not caught**. "PASS F18 ids=S052" licenses exactly: *this entry's recheck line re-runs a manifest
that lists S052 and whose own five assertions re-verify*. The landed entry happens to do much more —
FC-1/FC-3/FC-6/FC-9/FC-10 re-computed true by this seat:

```
FC-1 keys 5 count 1756 records 1756        FC-3 keysets 1 keys 12
FC-6 bod22 340 bod26 139 both 0 neither 1277
FC-9 grep -c FCEB-sentence -> 2            FC-10 grep -c BOD-22-01-sentence -> 327
sed -n '2246p;5423p' -> both lines carry the quoted text
```

— but those FC lines are prose: nothing runs them, so the gate would have passed the entry with every
FC line false (J4 demonstrates that shape).

**J4 — the KEV capture is an HTML error page renamed `.txt`, with a self-consistent manifest.**
`round-35/junk4/S092.txt` = `<html><head><title>502 Bad Gateway</title>…<p>CISA Catalog of Known Exploited
Vulnerabilities is temporarily unavailable.</p>…`; manifest sha256 over those bytes, assertion Q1 from
line 3, `fetched_utc 2026-10-26T09:00:00Z`, record `url` byte-equal to a registry row carrying the KEV
URL.

```
python3 corpus/instruments/source-recheck.py --manifest …/junk4/manifest.json --source S092
  S092:sha256 OK
  S092:Q1 OK occurrences=1 anchor=3-ok                                           exit=0
python3 corpus/instruments/capture-binding-check.py --root .
  MANIFEST round-35/junk4 records=1 url_bound=1 fetched=1 archival=0
  records=46 bound=46 unbound=0                                                  exit=0
python3 corpus/instruments/frontier-recheck-count.py --root .
  PASS     F92  knowledge/junk4-kev-errorpage.md                     ids=S092           exit=0   exit=0
python3 -c 'import json;json.load(open("corpus/source-snapshots/round-35/junk4/S092.txt"))'
  json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)        exit=1
```

→ **not caught by any landed check**; only the unrun JSON parse and an external fetch separate an error
page from the feed (G2).

### The declared junk-twin control is false as built

`c2-controls/junk-f18.md` (digest `0abec359…`) says it "declares no manifest record" and that "the
admission gate must reject this entry", but its `recheck:` line selects **S052**, which the manifest
lists, and the selection is byte-identical in effect to the real entry's:

```
cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
  S052:sha256 OK / Q1..Q5 OK                                                     exit=0     (run twice, 06:38Z and 06:42Z)
```

Admitted as a Frontier row in the scratch lane (same bytes, F93), the harness passes it:

```
PASS     F93  knowledge/junk5-junktwin.md                          ids=S052           exit=0
entries=24 pass=24 exit=0
```

The L1's own dispatch step (`ExecDoNothingReject` step 3: "exit 0 on the real entry, exit != 0 on the
junk twin") is therefore unsatisfiable with the committed twin. `source-recheck.py` has no ad-hoc quote
input, so "run source-recheck on the junk twin's fabricated quote" is not a reachable command; only a
manifest assertion can express it.

Corrected control, demonstrated (select an id the manifest does not list, the reading `MutJunkTwin`
step 2 names — "a twin not listed in the manifest must exit != 0"):

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S053
  S053:source UNAVAILABLE reason=not-listed                                      exit=2
# twin repointed at --source S053, admitted as F93:
FAIL     F93  knowledge/junk5-junktwin.md                          ids=S052           exit=-
         problems=header-sources-not-rechecked,selection-not-declared-by-entry,
                  selection-not-cited-by-entry,manifest-missing-ids
entries=24 pass=22 exit=1                                                        exit=1
```

So the rejection limb works when the control is written to be falsifiable. A stronger (quote-level)
twin: header `source: S053`, a `round-35/junk-twin/manifest.json` whose single assertion is the
fabricated sentence, capture that lacks it → `MISMATCH reason=quote-not-found`, exit 1, as measured in
J1b.

### Catch matrix

| construction | source-recheck | harness | capture-binding | census | recheck-audit | anchorcheck |
|---|---|---|---|---|---|---|
| J1 fabricated capture + fabricated record (self-consistent) | PASS 0 | PASS | PASS | n/a | PASS (form only) | 0 anchors, 0 bad |
| J1b assertion absent from its own capture | **MISMATCH 1** | FAIL | PASS | n/a | PASS | 0 |
| J1c fabricated assertion appended to a real manifest | **MISMATCH 1** | FAIL | PASS | n/a | PASS | 0 |
| J1d entry body quote / stated digest fabricated | PASS 0 | PASS | PASS | n/a | PASS | 0 |
| J2 row mined, no capture, used-by present | n/a | n/a | invisible (42 records / 52 rows) | PASS 0 (no line) | n/a | n/a |
| J2 row `opened` not a date | n/a | n/a | invisible | **E08 exit 1** | n/a | n/a |
| J3 cites S052, never opened the feed | PASS 0 | PASS | PASS | PASS | PASS | 0 |
| J4 error page as KEV capture (self-consistent) | PASS 0 | PASS | PASS (url+utc only) | PASS | PASS | 0 |
| committed junk twin `c2-controls/junk-f18.md` | **PASS 0** | **PASS as a row** | PASS | n/a | PASS | 0 |
| corrected twin (`--source S053`) | **exit 2** | **FAIL (4 problems)** | n/a | n/a | PASS | 0 |

### Residual gaps (measured)

- **G1 — entry bodies are unverified.** No instrument reads an entry's assertions; `anchorcheck.py`
  reports 0 anchors on both the junk and the landed F18 entry (bare `L…` refs), and a zeroed digest in
  the entry's `source:` line changes no verdict. The landed entry's FC-1…FC-11 are human-run prose.
- **G2 — captures are bound by name and URL string, not by content or provenance.** `capture-binding`
  rule B compares `url` to the row's https token and rule C checks the `fetched_utc` *shape*; a renamed
  error page with a self-consistent manifest passes (J4). `source-recheck` verifies sha256 against a
  manifest the same author writes, so it proves internal consistency only. Nothing fetches; the only
  thing that separated the real capture from J4 here was this seat's out-of-band `curl` + `collapse()`.
- **G3 — no "mined ⇒ capture" rule.** 12 live rows carry no capture (0 mined today); census warns only
  when such a row is also unused (`W03`), and is silent when it names a used-by path (S093 measured).
- **G4 — the committed junk-twin control is not falsifiable** (exits 0; passes as a row), so the C2
  after-condition "source-recheck exit != 0 on the junk twin" is not reproducible.
- **G5 — the harness verdict is narrower than its name.** `PASS F18 ids=S052` means binding + recheck
  exit; it does not mean the entry's claims were checked, and a `ground: F18` header is unbound to the
  README row's topic (any entry citing S052 passes).
- **G6 — the shape counters are pure text shapes.** `frontier=18`, `rows=52`, `S052_row=1`,
  `cite=1` are satisfiable with no capture (J2) and with no reading (J1, J3).

### Smallest safe correction (for the L1; not applied)

1. Rewrite `c2-controls/junk-f18.md`'s `recheck:` line to select an id the manifest does not list
   (`--source S053`, exit 2) **and** add a second twin whose twin-specific manifest asserts the
   fabricated sentence against a capture that lacks it (exit 1); record both outputs and a non-author
   REFUSE. This makes the kill-rule clause measurable. (Demonstrated above.)
2. State the F18 admission as reviewer-verified rather than gate-verified, and name the reviewer; or
   add a small entry-body gate: assert each manifest `quote` appears in the entry (the five Q1–Q5
   strings), plus set-equality between the entry's stated sha256 and the manifest's — both are one-pass
   text checks over existing bytes.
3. Record G1/G2 as declared limits of `frontier-recheck-count.py` and `capture-binding-check.py` (their
   docstrings already disclaim content binding; the claim's wording should inherit that disclaimer).
4. Optional, cheap, and decisive for J4: a `--kind text` capture-typing assertion in the manifest
   (`"content_type": "application/json"` plus a declared `parser: json` check) — source-recheck would
   then fail an error page without any network access.

### Scratch, cleanup, tooling

- Scratch root `/fast/scratch/hyaku/kasegi-r35/CritC2Kill/` (lane copy 5.7 MB, four fixture manifests,
  four captures, five junk entries, `build.py`, `S052-live.json`). Removed before yield; receipt first.
- No tool installed or upgraded (no `pacman`/`uv`/`npx` transaction). Network used once, read-only:
  `curl` of the KEV feed into scratch, used only to compare normalized bytes.
- No lane file written; no git/jj command run; fleet root, sibling lanes, shokuknow, bounties untouched.
