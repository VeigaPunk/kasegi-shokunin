# ExecHarnessSync — round-41 wave-1 receipt (knowledge-expected list sync for the F24 / S063 admission)

Seat: executor, leaf. Item: deliver the full new `corpus/instruments/knowledge-expected.txt` bytes after the
round-41 F24 knowledge addition, and give the L1 the post-integration command sequence with the exact expected
output lines.
Axes: depth:verifiability (the audit's expected-set equality is a frozen C2 counter), coverage (the expected
count must rise 59 -> 60 with F24's one new entry).

## 1. Deliverable

`.ufo/waves/round-41/wave1/ExecHarnessSync.knowledge-expected.txt` — land at
`corpus/instruments/knowledge-expected.txt`.

- **62 lines: 2 comment lines (byte-identical to HEAD) + 60 entry lines.**
- **sha256 `f993d9f379efa1a53ef7d1feb488de70749bb1c8da245fb558ef33ed7faacbe1`**, 3,079 bytes.
- C-locale sorted, one lane-relative `corpus/knowledge/<entry>.md` path per line:
  `grep -v '^#' F | LC_ALL=C sort -c` -> exit 0.
- Header lines deliberately unchanged (they still read "round 30"). Nothing parses them — `recheck-audit.py`'s
  `load_expected()` skips `#` lines and the audit requires set equality, not the round number — and r31-r40 kept
  them, so the diff against HEAD is insertions only (0 deletions). The round-35 lesson item 10 records the stale
  stamp as a cosmetic issue, not a counter.
- Delta vs HEAD: **+1 insertion, 0 deletions**, at line 48:

```
47:corpus/knowledge/retirement-autopsies.md
48:corpus/knowledge/rfc-9116-security-txt.md     <- new
49:corpus/knowledge/root-loss-2026-10-12.md
```

## 2. Why this exact name, and why this position

The basename is not a guess: `ScribeC2Entry` (the sibling seat that owns the F24 entry) names
`corpus/knowledge/rfc-9116-security-txt.md` in its own deliverable and receipt
(`wave1/ScribeC2Entry.md` §1 and §7.5). The registry row's `used-by` cell must name the same path — the census's
E11 limb checks that the `used-by` path exists on disk, and the harness's `entry_contract()` resolves the README
F24 row's entry cell to the same file. Three independent artifacts (entry scribe, registry row, README F24 row)
therefore agree on one name, and it is the name this list must carry.

Position is the file's own convention, not a fresh one: the committed list is **C-locale** sorted, and the two
orderings differ in this lane. `evidence-dir.md` vs `ev-model.md` sorts differently under `LC_ALL=C` than under
the default locale, and the committed file follows C:

```
$ LC_ALL=C diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt) <(ls corpus/knowledge/*.md | LC_ALL=C sort)
(empty)
$ diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt) <(ls corpus/knowledge/*.md | sort)
24a25
> corpus/knowledge/evidence-dir.md
26d26
< corpus/knowledge/evidence-dir.md
```

So the default-locale sort is **wrong** for this file and C-locale is right. Under C, `rfc-9116-security-txt.md`
falls between `retirement-autopsies.md` and `root-loss-2026-10-12.md` (`reti` < `rfc-` < `root`).

### Byte-consistency check (the item's explicit requirement)

The delivered file was diffed against a scratch copy of the committed file with exactly one line inserted at the
right position:

```
$ awk 'NR==48{print "corpus/knowledge/rfc-9116-security-txt.md"}{print}' base.txt > base-plus-one.txt
$ diff base-plus-one.txt ExecHarnessSync.knowledge-expected.txt
(no output)   -> BYTE_CONSISTENT_WITH_ONE_LINE_INSERT
```

And against a **tree-derived** regeneration of the integration-state mirror (the 60-file tree, globbed and
C-locale sorted) — the deliverable is tree-derived, not hand-incremented:

```
$ { grep '^#' candidate.txt; ls full/corpus/knowledge/*.md | sed 's|^full/||' | LC_ALL=C sort; } > tree-derived.txt
$ diff tree-derived.txt candidate.txt
(no output)   -> DELIVERABLE_EQUALS_TREE_DERIVED_60
```

## 3. Post-integration command sequence for the L1 (exact expected output lines)

Run from the lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin` **after** the L1 lands the entry, the
capture, the manifest, the S063 registry row and the F24 README row. Every line below is the **measured** output
of the integration-state mirror, not a transcription.

**1. recheck-audit — expected 60**

```
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=60/60 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=36 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0
```
exit 0. The frozen line to check is `expect=present expected=60 missing=0 unexpected=0 exit=0`.

**2. frontier-recheck-count — 27/27**

```
$ python3 corpus/instruments/frontier-recheck-count.py
...
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
entries=27 pass=27 exit=0
```
exit 0.

**3. capture-binding-check — 55/55**

```
$ python3 corpus/instruments/capture-binding-check.py
...
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=55 with_url=55 with_fetched_utc=17 with_archival=38 snapshot_dirs=17 manifest_dirs=17 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=55 bound=55 unbound=0
```
exit 0. (`orphan=S040-live.txt` is the standing round-40 orphan, unchanged; `multi_row_url=3` is unchanged.)

**4. census — exit 0**

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```
exit 0, **W04 S028/S029 only** — byte-identical to `wave1/../census-before.txt`, so no new E/W code.

**5. source-recheck — S063 green**

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063
S063:sha256 OK
S063:Q1 OK normalized=markup-whitespace occurrences=1 anchor=330-ok
S063:Q2 OK normalized=markup-whitespace occurrences=1 anchor=270-ok
S063:Q3 OK normalized=markup-whitespace occurrences=1 anchor=235-ok
```
exit 0. (These are `ExecC2Capture`'s own three Gate pins; the capture itself passes source-recheck unchanged.)

**6. the other frozen C2 numbers, measured on the same mirror**

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md            -> 24      (23 -> 24)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   -> 63   (62 -> 63)
$ ls corpus/knowledge/*.md | wc -l                        -> 60     (59 -> 60)
$ grep -rlE '^source: S063' corpus/knowledge | wc -l      -> 1
r22 measure (20+F_admitted)/(20+F_total)                 -> 44/44 = 1.000, queued rows 0
```

## 4. Method (no lane writes; all work in scratch)

1. Baseline read-only runs on the **unmodified lane tree** at HEAD (5b29ea14), before any mirror was built:
   `recheck-audit.py --quiet` -> `expected=59 missing=0 unexpected=0 exit=0`; `frontier-recheck-count.py` ->
   `entries=26 pass=26 exit=0`; `capture-binding-check.py` -> `records=54 bound=54 unbound=0`;
   `sources-census.sh validate` -> exit 0 with W04 S028/S029 only. These are the discrimination baselines and
   they match `wave41/c2-controls/before.txt` exactly.
2. Mirror: `git -C <lane> archive HEAD | tar -x -C $S/full` (read-only git; the mirror is not a git repo and no
   commit was made anywhere).
3. F24/S063 artifacts placed in the mirror from the **sibling seats' own delivered bytes**, not from my own
   stand-ins: `ExecC2Capture.S063.txt` as the capture, `ExecC2Capture.manifest-record.json` as the manifest
   record, `ScribeC2Entry.entry.md` spliced per its §1/§5 contract (`<<<CAPTURE>>>` x3 and the 21
   `<<<CAPTURE:Lnnn>>>` markers in ascending capture-line order) as the entry, plus an F24 README row and an
   S063 registry row (kind `spec`, tier `A`, status `mined`, opened `2026-10-27`, `recheck: on-release`).
4. Each mirror entry's `recheck:` line was re-pointed from the lane's absolute path to the mirror path, so the
   mirror stands in for the lane exactly as it will be at Y (every line resolves its manifest inside the mirror).
   Without that the strict `cdroot` limb fails by construction — 59 `cdroot_fail` — and the audit measures the
   mirror's path rather than the lane's.
5. The delivered list was installed into the mirror and all four counters were run against it.

## 5. Negative controls — the list is a live counter, not decoration

Both directions are falsifiable, and both were measured:

```
# NEG-1: the OLD 59-line list against the 60-file integration tree
$ python3 recheck-audit.py --quiet --root $S/full --cdroot $S/full
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=59 missing=0 unexpected=1 exit=1
rc=1

# NEG-2: the NEW 60-line list against a 59-file tree (the entry removed)
lines=59 total=59 pass=59 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=60 missing=1 unexpected=0 exit=1
rc=1

# restored: the delivered list against the 60-file tree
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0
rc=0
```

Landing the entry **without** this file prints `unexpected=1` and exits 1 — the exact failure mode the file
prevents. Landing this file **without** the entry prints `missing=1` and exits 1. The do-nothing control at
`wave41/c2-controls/before.txt` cannot reach any of the after-state values.

## 6. Cross-seat defect found: the F24 entry as delivered fails the harness citation limb

**This is a defect in `ScribeC2Entry`'s delivered bytes, not in my deliverable, and it will make the L1's
`frontier-recheck-count` print `entries=27 pass=26 exit=1` instead of `27/27`.** It needs a decision at landing
time, so I report it here rather than silently fixing it.

Measured on the mirror with the sibling's entry spliced exactly per its own contract:

```
$ python3 frontier-recheck-count.py --root $S/full
FAIL     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=-    problems=selection-not-cited-by-entry
entries=27 pass=26 exit=1
rc=1
```

Cause: `frontier-recheck-count.py`'s citation limb requires the entry to cite its recheck'd source id **outside**
the `source:` declaration line and the `recheck:` line. `S063` appears in `ScribeC2Entry.entry.md` only on those
two lines (2 occurrences total), so the cited-id set is empty and the limb reds. The lane's convention is the
other attribution form: `cyclonedx-analysis-subtree.md` writes `— S060.txt:L4` on every quote, which puts the id
in the cited set. The sibling entry writes `— §2.5, L189` instead, and `S063.txt` never appears in prose.

This is a lane-wide invariant, not a one-off: all **33** existing entries that carry `--source <id>` satisfy
`recheck_ids ⊆ cited` today. The new entry would be the first to break it.

**Both fixes were measured green; the L1 picks:**

- **Fix A (lane-conventional — recommended).** Re-point the 17 quote attributions from `— §x, Lnnn` to
  `— S063.txt:Lnnn (§x)`, the form every other entry uses. Then:
  `PASS F24 knowledge/rfc-9116-security-txt.md ids=S063 exit=0` -> `entries=27 pass=27 exit=0`, rc 0.
- **Fix B (minimal, one line).** Add one evidence bullet in the `EVIDENCE_LINE` form, which falls through to the
  citation scan:
  `- S063, "RFC 9116 §2.5.5 — the Expires field is REQUIRED and single."`
  Then: `entries=27 pass=27 exit=0`, rc 0.

Fix A also satisfies the entry's own QUALITY Q1–Q10 shape (the F23 precedent's attribution form); Fix B is
smaller but leaves the entry's attributions in a form no other entry uses. Either one makes the harness green;
without either, the C2 claim's `harness entries=27 pass=27 incl PASS F24` leg fails.

Note this defect is **orthogonal to my deliverable**: the list is correct and green with the entry in either
state (the audit's `expect=present expected=60 missing=0 unexpected=0 exit=0` holds both ways), and it is the
harness, not the list, that reds.

## 7. Integration notes / risks

- Land the file as delivered. If the F24 entry lands under a different basename than
  `corpus/knowledge/rfc-9116-security-txt.md`, regenerate instead of trusting this list:
  `{ grep '^#' corpus/instruments/knowledge-expected.txt; ls corpus/knowledge/*.md | LC_ALL=C sort; } > /tmp/e && mv /tmp/e corpus/instruments/knowledge-expected.txt`
  then `python3 corpus/instruments/recheck-audit.py --quiet` must print `expected=<entries> missing=0 unexpected=0 exit=0`.
  Note `ls` must be `LC_ALL=C`-sorted to match this file's convention (see §2).
- The header stamp still reads "round 30" and will keep doing so unless the L1 changes it; the audit does not read
  it, and the r35-r40 precedent is to leave it.
- The S063 entry stays `gated` in the audit until `corpus/source-snapshots/round-41/manifest.json` exists in the
  lane (its `recheck:` line `cd`s to the lane, which lacks the manifest until the L1 lands it). That is the
  manifest dependency, not a list defect — `gated` still counts as a pass on every limb, so `pass=60` holds.
- `records=55 bound=55` requires the S063 manifest record to carry a `url` matching the registry row's source cell
  and a strict-UTC `fetched_utc` (round-41 >= MODERN_ROUND 32, so the archival exemption is closed). The sibling's
  record has both.

## 8. Tooling

Nothing installed or upgraded. Read-only git only (`archive`, `show`, `status`, `log`) — no mutating git/jj
command anywhere. Disk guard was green before the heavy steps (`/fast/scratch/hyaku` 24%, 610.8G free).

**Network fetch** (the RFC 9116 body, for my own cross-check of the sibling capture — not for the deliverable):

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o work/rfc9116.txt \
    -w 'HTTP_STATUS=%{http_code} BYTES=%{size_download} FINAL_URL=%{url_effective}\n' \
    https://www.rfc-editor.org/rfc/rfc9116.txt
HTTP_STATUS=200 BYTES=45129 FINAL_URL=https://www.rfc-editor.org/rfc/rfc9116.txt
fetch started 2026-10-27T08:28:22Z, finished 2026-10-27T08:28:22Z (UTC)
```
45,129 bytes, sha256 `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9` — identical to the
`raw_sha256` the sibling's manifest record already pins, so the two fetches agree.

## 9. Write scope / scratch

I wrote only this receipt and `ExecHarnessSync.knowledge-expected.txt` in the wave dir. No lane file was edited:
`git status --porcelain` shows my two files as the only additions from this seat, and
`git diff HEAD -- corpus/instruments/knowledge-expected.txt` is empty — the list is delivered, not landed. No
fleet-root file was written, no sibling lane was touched, and `/home/vgpnk/Projects/shokuknow` was never written
or run.

Scratch `/fast/scratch/hyaku/kasegi-r41/ExecHarnessSync/` (mirror, capture, splice scripts, negative-control
copies) was removed after the receipt and deliverable were in the wave dir.
