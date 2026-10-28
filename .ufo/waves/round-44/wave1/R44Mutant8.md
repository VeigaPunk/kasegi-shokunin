# R44Mutant8 — C2 counter mutant: junk F26 row / knowledge entry without source provenance

- lane-round: kasegi 44, wave 1, mutation-tester seat (leaf; no dispatch).
- assigned item: *Design a C2 counter mutant accepting a junk F26 row or knowledge entry without source provenance.*
- frozen base measured: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` (the revision named by
  `.ufo/waves/round-44/controls/do-nothing.txt`). All mutant measurements are on a `git archive`
  export of that commit; the live lane worktree was **not** used because it carries sibling
  in-flight edits (`git status --porcelain | grep -v '^??'` → `M PROVINCE.md SCORECARD.md SHONEN.md
  SKILL.md corpus/README.md corpus/SOURCES.md corpus/instruments/knowledge-expected.txt`).
- scratch: `/fast/scratch/hyaku/kasegi-r44/R44Mutant8/` (`HYAKU_SCRATCH` unset in this shell;
  default per `scripts/hyaku/lane-addendum.md:529`). Created, used, deleted — §8.
- no production, lane, git/jj/index, fleet or operator-config writes. No tool installs (none
  needed); `pacman` never invoked.

## 0. Method and pinning

The pristine copy is a `git archive` of the frozen base, and its three measured files hash equal
to the committed blobs, so the baseline is the frozen base byte-for-byte:

```
$ for f in corpus/README.md corpus/SOURCES.md corpus/instruments/knowledge-expected.txt; do
    a=$(git show 5ab3a60:$f | sha256sum | cut -d' ' -f1)
    b=$(sha256sum /fast/scratch/.../base/$f | cut -d' ' -f1); ... done
corpus/README.md committed=82dedcea2055d9425179addd11fe17ef0a5abdc17be5f9cb4322e9fe742f40b6 base=82dedcea… MATCH
corpus/SOURCES.md committed=fd96d38b03585db8952740958e87db6aa0a4b54f0abb30d9ca3f9a7a1b60c358 base=fd96d38b… MATCH
corpus/instruments/knowledge-expected.txt committed=4624d47e155af21ebe35280188f650af8557f97e3760df358466bd196739f142 base=4624d47e… MATCH
```

Each mutant is a `cp -a` of that export; the pristine export was never mutated (post-run hashes
above are identical to the pre-run committed digests). Mutants are disposable scratch copies per
tasking; their exact bytes are recorded as digests in §1 so the recipe is reproducible.

Detectors run on every tree, in this order: the **frozen C2 counter** exactly as written in
`claims.json`; the **do-nothing control's** variant of that counter (the command that actually
produced 25/68/62); `frontier-recheck-count.py --root <tree>`; `recheck-audit.py --root <tree>
--cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin`; `anchorcheck.py <entry>`;
`capture-binding-check.py --root <tree>`; `sources-census.sh validate --file <tree>/corpus/SOURCES.md`.

## 1. Mutant design

Baseline counters at the frozen base reproduce the do-nothing control exactly:

```
$ grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md        → 0
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md  → 25
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 68
$ find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l        → 62
$ python3 corpus/instruments/frontier-recheck-count.py --root base → entries=28 pass=28 exit=0
$ python3 corpus/instruments/recheck-audit.py --root base --cdroot <lane> → expect=present expected=62 missing=0 unexpected=0 exit=0
```

Four arms, each the smallest behavior-bearing edit that could satisfy the C2 after-state without
real provenance:

**M1 — junk F26 row + provenance-free entry, no `source:`/`recheck:` line.**
- appended after the last frontier row (`corpus/README.md:591`):
  `| F26 | Junk row with no source provenance | admitted | knowledge/junk-f26-no-provenance.md | — | Nothing; this row cites no source. |`
- new `corpus/knowledge/junk-f26-no-provenance.md` (title + `verified-at` + unsupported claim, **no**
  `source:` line, **no** `recheck:` line, **no** quote, **no** anchor); expected list synced.
- hashes: README `28c375692dc5f28ce72adcf074408d4f0e83dec33d56ca736a0a28655ee10357`,
  entry `7e6bcd5c88275163b31daea52d5762cb6d45c65d00fcacd9acf7b1a7596b4718`,
  expected `78fa1f8b36ddd6ca5cc08a2b1b18826a89f07643613d56ccb70964158072e780`.

**M2 — provenance-free entry only** (no frontier row): same entry and expected-list sync as M1;
`corpus/README.md` unchanged (`82dedcea…`).

**M3 — laundered provenance:** same entry, but it declares a *real* id for an unrelated topic and a
working recheck line, and the F26 row names that id:
`source: S001 — https://www.first.org/cvss/v4.0/user-guide` + `recheck: … source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S001`;
F26 `sources` cell `S001`. Entry body still has no quote and no anchor. Entry hash `bb089f014b53ffbdb30e04fbb0c9864d69e5e9c528e61f6e4136ea1a99b95ea5`,
README `f1540e1f359286978e674666052b547c66d6f11271cd5621c75a631ced9c2bb0`.

**M4 — fabricated source end-to-end:** new registry row inside the table after S068
(`| S069 | Fabricated policy source — https://example.invalid/fabricated-policy | docs | A | … | mined | 2026-10-28 | 180d | corpus/knowledge/junk-f26-no-provenance.md |`),
a hand-written `corpus/source-snapshots/round-44/S069.txt` (9 lines, self-described fabricated),
a matching `manifest.json` (`fetched_utc`, `http.final_url`, `sha256`, one quote), an entry citing
`corpus/source-snapshots/round-44/S069.txt:6` and `:8`, and F26 `sources` cell `S069`.
Hashes: README `ab9f7d8ab4a94093b1ee38168e7bf79730ee208b691080a7128505a2737ca364`,
SOURCES `7eca273eee8cd47d99e09ab2014293c97506d452aa2f01caabaeabdcd185b226`,
entry `e6fb7942b055b64eb3d2af354cdf9426fed10d4201d3712a921c61a3c8b4f0ea`,
manifest `561de9d69ff7bbf9addc43aa86a2f0dc680d191fa020c27b07ccfd651b28a254`,
capture `a6d8b76f98659436efa495d9f6984f27af57c2773a77bd6b1a9b75422cf5a113`.

## 2. Actual outputs

| detector | pristine base | M1 junk F26 | M2 entry only | M3 laundered | M4 fabricated source |
|---|---|---|---|---|---|
| C2 counter **as frozen in `claims.json`** (`'^\| F[0-9]+ \| admitted \|'`) | **0** | **0** | **0** | **0** | **0** |
| do-nothing-control frontier regex (`'^\| F[0-9]+ \| .* \| admitted \|'`) | 25 | **26** | 25 | **26** | **26** |
| SOURCES rows | 68 | 68 | 68 | 68 | **69** |
| knowledge `*.md` count | 62 | **63** | **63** | **63** | **63** |
| `frontier-recheck-count.py` | `entries=28 pass=28 exit=0` | `FRONTIER-FAIL F26 status=admitted ids=- problems=missing-pass-line` / `entries=29 pass=28 exit=1` | `entries=28 pass=28 exit=0` | `FRONTIER-PASS F26 ids=S001` / `entries=29 pass=29 exit=0` | `FRONTIER-PASS F26 ids=S069` / `entries=29 pass=29 exit=0` |
| `recheck-audit.py` | `lines=62 total=62 … exit=0` | `lines=62 total=63 … exit=1` | `lines=62 total=63 … exit=1` | `lines=63 total=63 … exit=0` | `lines=63 total=63 … exit=0`; `expect=present expected=63 missing=0 unexpected=0 exit=0` |
| `anchorcheck.py <entry>` | n/a | n/a | n/a | `0 in-range cite instances … exit=0` | `2 in-range cite instances, 0 bad` / `OK … S069.txt:6` / `OK … S069.txt:8`, exit=0 |
| `capture-binding-check.py` | — | — | — | — | `AUDIT records=58 … records=58 bound=58 unbound=0`, exit=0 |
| `sources-census.sh validate --file` | — | — | — | — | `file ok <tree>/corpus/SOURCES.md`, exit=0 (W04 S028/S029 unchanged) |

Exact quoted lines (copy from the run receipts, which lived in scratch and are quoted here because
scratch is removed):

```
M1: FRONTIER-FAIL F26 status=admitted ids=- problems=missing-pass-line
M1: entries=29 pass=28 exit=1
M1: lines=62 total=63 pass=62 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
M1: expect=present expected=63 missing=0 unexpected=0 exit=1
M2: entries=28 pass=28 exit=0
M2: lines=62 total=63 pass=62 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
M3: FRONTIER-PASS F26 ids=S001
M3: PASS     F26  knowledge/junk-f26-no-provenance.md  ids=S001  exit=0
M3: lines=63 total=63 pass=63 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
M3: expect=present expected=63 missing=0 unexpected=0 exit=0
M4: FRONTIER-PASS F26 ids=S069
M4: entries=29 pass=29 exit=0
M4: AUDIT records=58 with_url=58 with_fetched_utc=20 with_archival=38 snapshot_dirs=20 manifest_dirs=20 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1
M4: records=58 bound=58 unbound=0
M4: == corpus/knowledge/junk-f26-no-provenance.md: 2 in-range cite instances, 0 bad; 2 distinct anchors; … BASE-ABSENT=0
M4: OK md:11 corpus/source-snapshots/round-44/S069.txt:6  [Section 1. A fabricated rule: "Researchers must never test customer-owned resources without written …]
M4: OK md:11 corpus/source-snapshots/round-44/S069.txt:8  [Section 2. A fabricated timeline: "Acknowledge within two business days and disclose within forty-…]
```

## 3. Verdicts

- **M1 — killed** by two independent committed detectors: `frontier-recheck-count.py` Rule G
  (`missing-pass-line` on F26, exit 1) and `recheck-audit.py` completeness (`total=63 > lines=62`,
  exit 1). The frozen *count* still reads 26/68/63, so the counter alone accepts it.
- **M2 — killed** by `recheck-audit.py` completeness only (exit 1); `frontier-recheck-count.py`
  is blind to it (`entries=28 pass=28 exit=0`). It meets the knowledge-count token (63) while
  adding no source.
- **M3 — survived** every committed detector, with a source line naming an unrelated registered
  id and a recheck line that runs green. Counters read 26/68/63 — the frozen after-state.
- **M4 — survived** every committed detector end-to-end: fabricated registry row, fabricated
  capture, fabricated manifest, in-range anchors, F26 PASS. Counters read 26/69/63, i.e. **every
  C2 after-state number plus the "newly opened tier-A source row"**, with zero real provenance.

## 4. Finding 1 — the counter of record cannot measure its own after-state

`claims.json` C2's first command is `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md`.
Against the actual frontier table (`| id | topic | status | entry | sources | next |`) it returns
**0 at the frozen base and 0 in all four mutants**, because `admitted` is the third cell, not the
second. The command that produced the frozen 25/68/62 (do-nothing control, and every historical
receipt) is `grep -cE '^\| F[0-9]+ \| .* \| admitted \|'`. So the frozen counter of record would
report 0→0 for C2, and a lane that trusted it could neither show the 26 target nor distinguish a
junk row from a real one. This is a depth:verifiability defect in the *frozen counter text*, not
in the lane's implementation; I did not change it (contract is frozen).

## 5. Finding 2 — coverage boundary: C2's predicate is a count/structural witness, not a provenance witness

The surviving M4 shows the after-state is reachable by construction: a row, a registry id, a
capture, a manifest, a quote and two in-range anchors can all be authored locally, and every
committed instrument checks only *internal consistency* (`capture-binding-check.py` B–E binds
record→row→digest→stamp; `source-recheck.py` binds manifest quotes→captured bytes;
`anchorcheck.py` binds cites→capture lines; census validates row shape, not reachability). None
of them fetches the URL or attests that the capture came from it, and none requires an entry's
prose to derive from the source it declares. The claim already says this is where the
**non-author gate** is load-bearing ("no coverage credit unless … the non-author gate agrees"),
so the mutant is a *coverage finding*, not a contradiction of the contract: the C2 counter is
necessary and insufficient, and a green counter must never be reported as coverage credit on its
own. A future amendment that wanted content binding would need a limb such as "the F26 entry
contains at least one quote that occurs in the newly opened source's capture" — I am not
proposing it as a change here, only recording that no current limb has that shape.

Discrimination against do-nothing: do-nothing reads 25/68/62 and `entries=28 pass=28`;
M1/M3/M4 read 26 and 63 (M4 69) — so the counters do separate do-nothing from an *attempt*, but
they do not separate real work from M3/M4.

## 6. Limitations

- Gates were run offline on a scratch export; `capture-binding-check.py` and `source-recheck.py`
  verify captured bytes and manifest assertions, never upstream authenticity (documented
  behaviour, not a defect claim).
- I did not run the round-43 closure suite (`corpus/instruments/r43-closure.sh`) — it grades
  round-43 receipts, not C2 provenance, and the PROTOCOL gate rule forbids replaying a sibling's
  gate as evidence.
- `anchorcheck.py` classifies a bare capture name (`S069.txt:6`) as mirror-relative and reported
  `BASE-ABSENT`; only the lane-relative form (`corpus/source-snapshots/round-44/S069.txt:6`)
  resolved IN-RANGE. Recorded as an observation about citation form, not routed as a defect.
- Mutant receipts lived in scratch and are quoted inline; the report is the durable record. The
  mutant trees are deleted, so re-running requires re-applying §1's exact text (digests given).
- The live lane worktree was already dirty with sibling round-44 edits during this seat; nothing
  here is a statement about those edits.

## 7. Lane cleanliness

- `git rev-parse --show-toplevel` in the lane → `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
  no git/jj command that mutates was run (only `rev-parse`, `archive`, `show`, `status`, `log`).
- The pristine export's measured files hash equal to `5ab3a60`'s blobs after all probes (§0).

## 8. Scratch removal

`/fast/scratch/hyaku/kasegi-r44/R44Mutant8/` (base + mutA–mutD + receipts) was removed before
yield; the empty parent `kasegi-r44` is left for the L1 to purge per `lane-addendum.md:535`.
