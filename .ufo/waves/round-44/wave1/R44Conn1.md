# R44Conn1 — cross-claim/source overlap: the invariant C1 and C2 both lean on

Seat: `R44Conn1` (connector, leaf — no subagent dispatch). Axes: `depth:verifiability`, `coverage`.
Read-only seat: no lane byte written except this report. No git/jj mutation, no commit, no install,
no pacman. Required policy read first: `/home/vgpnk/.omp/agent/RULES.md` (no install performed, so
nothing to record under the tooling directive).

State pinned for every measurement below (snapshot saved to scratch, then removed):

```
2026-10-28T16:02:57-03:00
HEAD=66314015122b9aa32dc40f2f1815df56624c26d1   git rev-parse --abbrev-ref HEAD -> HEAD (detached)
 M PROVINCE.md  M SCORECARD.md  M corpus/README.md  M corpus/SOURCES.md
 M corpus/instruments/knowledge-expected.txt      (+ untracked r44 artifacts, listed in Limitations)
```

The tree was being written by other seats while I measured; counts below are a timestamped snapshot,
not the final revision.

## Finding

**C1's eight routed defects and C2's candidate share one adversarial invariant, and at this snapshot
both claims violate it in the same shape.** The invariant is already law in this lane — `corpus/QUALITY.md:353`
(R41: a counted value is read as a whole token and *the counter prints the token it read*) and
`corpus/QUALITY.md:369` (R43: a record reporting a run is graded by a committed counter over *that
record's own bytes*) — and it can be stated in one line:

> **A claim is certified only by a counter that (i) reads the revision the claim names, (ii) reads the
> artifact's own bytes rather than a union or a draft, and (iii) prints a value that differs between
> the do-nothing world and the after world.**

C1's eight items are four failure shapes of that one invariant (§1 below). C2's candidate reproduces
two of those shapes in its own new artifacts: its **frozen counter reads `0` in both worlds** (§2a), and
its **new capture record was unbound against the lane's own landed binding gate** for the whole drafting
window (§2b — red `unbound=1` at 16:02:57, repaired by another seat at ~16:06–16:12, green `bound=58`
at 16:12:31) while every counter C2 freezes stayed green throughout. The kill rule of C2 tests
*reachability* of F26, not *discrimination*, so C2 can satisfy its frozen predicate set with a red gate
in the tree — that is the cross-claim hole, and §2b is the instance that actually happened this round.

## 1. C1's eight items are four shapes of one invariant

The lane already carries a named seven-family taxonomy — `F-EVID / F-TOKEN / F-TABLE / F-DECL /
F-SCAN / F-BIND / F-FLIP` (`.ufo/waves/round-42/wave1/ScoutPrecedent.md:8`, family meanings at
`.ufo/waves/round-42/wave1/ScoutDefeatsR41.md:11`). Mapping §6 onto it (`corpus/lessons/round-43-verifier-spotcheck.md:101-108`):

| §6 item | defect | lane family | invariant shape |
|---|---|---|---|
| 1 | `closed=13/19` unbacked at `ab98fac9` | F-TOKEN + F-EVID | **I1** literal with no run at the named revision |
| 2 | K18 excludes `SCORECARD.md`; K17 reads only `claims-erratum*.md` | detector scope (R10) | **I2** detector narrower than the claim's surface |
| 3 | "29-character prefix" vs measured 26 | F-TOKEN | **I1** |
| 4 | planner=L1 mapping and L2-floor line absent from the report | contract field absent | **I4** no field, so no detector can exist |
| 5 | `names=` empty beside `seats=73`; transcript without `export-ref`; aborted `.tmp` | F-DECL + F-SCAN + identity | **I3** record loses the identity that would make I1 checkable |
| 6 | `SHONEN.md` lost one base byte | append-only | **I3** |
| 7 | SHONEN bullet points at `corpus/instruments/README.md`, 0 hits | F-BIND | **I2/I3** dangling pointer |
| 8 | `127` asserted, cited control prints `exit=2` | F-TOKEN (control token) | **I1** |

I1 is four of the eight items; I2/I3 cover three more; I4 the last. The round-42 queue had the same
centre of mass — RD42-1 (stale number), RD42-5 (receipt granularity) are I1;
`corpus/lessons/round-42-verifier-spotcheck.md:173-177`.

## 2. C2's candidate, measured against the same invariant

C2's candidate at this snapshot is landed in the working tree: `corpus/README.md:628` (F26 `admitted`,
cells `| F26 | … | admitted | knowledge/google-cloud-vrp-customer-resource-boundary.md | S069 | … |`),
`corpus/SOURCES.md:75` (S069 `mined`, tier A), `corpus/SOURCES.md:76` (S070 `rejected`, the recorded
reject), `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` (new entry),
`corpus/source-snapshots/round-44/{S069.txt,manifest.json}`, and
`corpus/instruments/knowledge-expected.txt` gained the entry.

Measured: `26` admitted F rows, `70` SOURCES rows, `63` knowledge files.

```
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md   -> 26
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 70
$ find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l          -> 63
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi -> ok, exit=0
```

So the coverage movement is real. What is not real is the *evidence chain*, in four places.

### 2a. C2's frozen counter cannot discriminate (shape I1 + F-TABLE)

The counter frozen in `.ufo/waves/round-44/claims.json:23` is
`grep -cE '^\| F[0-9]+ \| admitted \|'` — it assumes column 2 is the status, but the frontier table's
column 2 is the title and column 3 is the status (`.ufo/waves/round-44/wave1/R44Review10.md` measured
the same table). The frozen do-nothing control uses a *different* regex (`.ufo/waves/round-44/controls/do-nothing.txt:10`,
`^\| F[0-9]+ \| .* \| admitted \|`), so the claim and its own control disagree about how to measure
the same predicate.

| world | claims.json:23 counter | control:10 counter |
|---|---|---|
| frozen base export (`git archive 5ab3a60`) | **0** | 25 |
| HEAD export (`git archive 6631401`) | **0** | 25 |
| live tree 16:02 (F26 present) | **0** | 26 |
| synthetic after-row in scratch | **0** | 1 |

```
$ grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md ; echo rc=$?   -> 0 / rc=1
$ printf '| F26 | … | admitted | knowledge/… | S069 | … |\n' > f26.txt
$ grep -cE '^\| F[0-9]+ \| admitted \|' f26.txt                        -> 0
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' f26.txt                  -> 1
```

The claim's own counter returns the same value in the do-nothing world and in the after world, so it
satisfies the C2 kill rule's *shape* (`a do-nothing replay cannot reach F26`) by never reaching 26 at
all — it cannot certify the after-state either. This is C1-D8's shape (a cited token the cited command
does not print) reproduced inside C2's own instrument, and it is F-TABLE, the family whose r41 mutants
(D03/D04) survived the suite (`ScoutDefeatsR41.md:11`).

### 2b. The new capture record was unbound against a landed, selftested gate (shape I3, F-BIND)

`corpus/instruments/capture-binding-check.py` rule B5 (`:52-55`) requires a manifest record's `url` to
equal, byte-for-byte, the `https://` token of its own row's source cell.

**Observed red at 16:02:57, on the manifest as drafted:**

```
$ python3 corpus/instruments/capture-binding-check.py            # live tree, 16:02:57
MANIFEST round-44 records=1 url_bound=0 fetched=1 archival=0
FAIL rule=url-mismatch record=S069 row=S069 dir=round-44
records=58 bound=57 unbound=1
exit=1
```

The mismatch was one token wide: the record's `url` was the REST endpoint
(`https://bughunters.google.com/rest/v1/articles/…`) while the row's source cell carried the human page
(`https://bughunters.google.com/about/rules/…`). Precedent S067 binds both to the same token
(`https://curl.se/docs/CVE-2025-9086.html`).

**Repaired by another seat while I measured; re-verified green at 16:12:31:**

```
$ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-44 records=1 url_bound=1 fetched=1 archival=0
records=58 bound=58 unbound=0
exit=0
```

The repair is exactly one cell: `url` now equals the row token, and the API endpoint moved to
`capture_url` + `http.final_url` in `corpus/source-snapshots/round-44/manifest.json:7-14`.

Two things survive the repair. First, the regression was real for the drafting window and **none of
C2's frozen counters could see it**: the census checks duplicate URLs, not capture binding, and it was
`exit=0` throughout; the F/S/knowledge counters moved 25→26, 68→70, 62→63 regardless. Second, the gate
was green at base (`57/57`) and the round-43 verifier recorded `records=57`
(`corpus/lessons/round-43-verifier-spotcheck.md:63`), so the C2 candidate had made a green gate red and
the frozen predicate set would have certified the round anyway. That is the coverage/depth coupling the
invariant exists to prevent.

### 2c. The pin is still not reproducible from the URL the row publishes (shape I1)

`corpus/source-snapshots/round-44/manifest.json` pins `sha256 0932279c…`, `bytes 45681`, `lines 1132`;
`url` is now the human page and `capture_url` the REST endpoint. Neither returns those bytes:

```
$ curl -sS -o api.json -w 'http=%{http_code} bytes=%{size_download}\n' <capture_url>
http=200 bytes=48657
$ head -c 120 api.json   -> {"title":"Cloud Vulnerability Reward Program Rules", "body":"…
$ sha256sum api.json     -> f7dbb8c9b00d6dab2edc5295f40c84441b33355eed6b9acddaa0dd19311e4c69
recon raw  .ufo/waves/round-44/source-recon/S069.txt   -> 1 line, 47136 B, sha 7e2004ba…
recon body .ufo/waves/round-44/source-recon/S069-body.txt -> 1132 lines, 45681 B, sha 0932279c…
pinned     corpus/source-snapshots/round-44/S069.txt    -> identical to recon body (`cmp` -> identical)
```

Three different byte counts for one source: 48657 now, 47136 at recon, 45681 pinned. The API serves
`{"title": …, "body": …}` JSON; the pinned file is the **unescaped `body` value**, i.e. the product of a
`json→body-text` extraction. That step is not declared anywhere: `grep -rn 'S069-body'` over the lane
hits nothing outside this report, no script consumes it, and the manifest records `bytes 45681` /
`snapshot_bytes 45681` — so it states the *stored* size as if it were the fetched one, while the fetched
response was 47136 B at recon. The S069 row declares no transformation and no raw byte count:

```
$ grep -E '^\| S069 ' corpus/SOURCES.md | grep -ciE 'normaliz|extract|raw bytes'   -> 0
```

Precedent says the opposite: S067's row carries `3822 bytes; fetched …; 10455 raw bytes`, and S068's row
carries the normalization disclosure (`the pin is the instrument-normalized text, 191 lines`).
`corpus/QUALITY.md` Q8 requires the receipt to name the transformation it applied. So the new row is a
literal whose derivation is unrecorded — exactly C1-D1's shape. (The provenance *URL* chain is now
documented: `url`/`capture_url`/`http.final_url` satisfy rule E3, `capture-binding-check.py:119-123`,
precedent S057. It is the byte-level transformation that is missing.)

### 2d. The recheck detector covers 3 of the entry's 5 quoted spans (shape I2)

The entry's `recheck:` line runs `source-recheck.py --manifest …/round-44/manifest.json --source S069`,
which is executable and green:

```
S069:sha256 OK
S069:Q1 OK normalized=markup-whitespace occurrences=1 anchor=61-ok
S069:Q2 OK normalized=markup-whitespace occurrences=1 anchor=62-ok
S069:Q3 OK normalized=markup-whitespace occurrences=1 anchor=70-ok
```

But the manifest carries three quotes (Q1–Q3, anchors 61/62/70) while the entry publishes five quoted
spans. The unchecked one is the entry's scope claim — "In principle, any Google Cloud product or web
service that handles reasonably sensitive user data is intended to be in scope"
(`knowledge/google-cloud-vrp-customer-resource-boundary.md:9`, `S069.txt:9-11`, 21 words). S067's
manifest carries six quotes. So the one claim a reader would lean on hardest is outside the detector —
C1-D2's shape ("no check can see defect 1") on the C2 surface, and R10's fixture-matrix caveat.

Credit where due, measured: every locator the entry does cite resolves —
`sed -n '9,11p;61,63p;68,69p;70,72p;78,86p' corpus/source-snapshots/round-44/S069.txt` prints the quoted
text at those lines, and the quoted spans measure 21/13/12/18 words, all ≤ Q3's 25.

### 2e. Both claims' `control` cells dangle

`claims.json:15` cites `.ufo/waves/round-44/controls/c1-do-nothing.txt`; `claims.json:24` cites
`.ufo/waves/round-44/controls/c2-do-nothing.txt`. Neither file exists (`ls` → `No such file or
directory`); the frozen control that does exist is `controls/do-nothing.txt`. That is C1-D7's shape
(dangling pointer) and C1-D8's (a citation that does not resolve to the cited artifact) inside the
frozen claims themselves.

## 3. Discrimination matrix (the do-nothing test, run properly)

I built the worlds with `git archive … | tar -x -C <scratch>` (read-only on git; no worktree, no index
touch) and ran the same commands in each:

| world | C1 counter (`r44-routed-defects.py`) | C2 F-row counter: claim / control | SOURCES | knowledge | binding gate |
|---|---|---|---|---|---|
| base `5ab3a60` export | instrument absent at base | 0 / 25 | 68 | 62 | exit 0, `bound=57 unbound=0` |
| HEAD `6631401` export | `fixed=0 unresolved=8 exit=1` | 0 / 25 | 68 | 62 | exit 0, `bound=57 unbound=0` |
| live tree 16:02 | `fixed=3 unresolved=5 exit=1` | 0 / 26 | 70 | 63 | exit 1, `bound=57 unbound=1` |
| live tree 16:13 | `fixed=5 unresolved=3 exit=1` | 0 / 26 | 70 | 63 | exit 0, `bound=58 unbound=0` (repaired) |

Two things fall out.

1. **The C1 counter reads the working tree, not committed evidence.** The same instrument, same
   `--baseline`, gives `fixed=3`/`fixed=5` against the live tree (it moved between 16:02 and 16:13 as
   other seats wrote) and `fixed=0` against the HEAD export — at the committed revision, every credited
   fix lives in untracked files (`git ls-files .ufo/waves/round-43/claims-erratum-6.md
   .ufo/waves/round-44/controls/missing-suite-base.txt` → 0). C1's after-state says "proven by one
   committed read-only counter over committed lane evidence" (`claims.json:12`); the instrument does not
   enforce "committed" and cannot tell a landed fix from a drafted one. Between 16:03 and 16:13 the
   instrument gained an `export-unavailable` check on `--baseline` (a partial repair), but `--root`
   still grades whatever tree it is pointed at, committed or not.
2. **The C1 counter as frozen does not run.** `claims.json:14` declares
   `--root <lane-export> --baseline <frozen-base>`; the instrument also requires `--report`
   (`argparse: error: the following arguments are required: --report`, `exit=2`). Same shape as C1-D8.

Both claims therefore have the same defect at the same layer: **the instrument named in the claim does
not measure what the claim's `after` says it measures.** That is the shared adversarial invariant, and
it is testable in one place instead of eight.

## 4. Recent kasegi and sibling themes — the invariant is lane-general

The same failure has been found independently outside kasegi, and codified inside it:

- kotoba, round 74: "The counter does not discriminate the one judged change (the carry-forward world
  also reads 20 of 20, as the lane itself reports)" — `kotoba-shokunin/corpus/lessons/round-74-verifier-spotcheck.md:80`.
- kaidoku, round 38: "author: met by counter; counter non-discriminating" —
  `kaidoku-shokunin/corpus/lessons/round-38-verifier-spotcheck.md:61`.
- kasegi's own round 39 records a `(non-discriminating)` counter — `corpus/lessons/round-39.md:59`.
- the fix is already written as law: `corpus/QUALITY.md:353` (R41, whole token + prints the token) and
  `corpus/QUALITY.md:369` (R43, counter over the record's own bytes).

So this is not a new class. What is new in round 44 is that C2's counter, both `control` pointers and
the capture pin were frozen *before* R41/R43 were applied to them — and C1's own repair counter inherited
the same gap.

## 5. Proposed move (one bounded move)

**Land one discrimination receipt over both claims' own counters, run against two `git archive`
exports, and require the printed values to differ.**

Concretely, one control file `.ufo/waves/round-44/controls/counter-discrimination.txt` produced by one
command shape:

```
for claim in C1 C2; do
  base=$(eval "<claims.json:$claim counter>" against the 5ab3a60 export)
  tip=$(eval  "<claims.json:$claim counter>" against the round-tip export)
  echo "$claim base=$base tip=$tip discriminate=$([ "$base" != "$tip" ] && echo 1 || echo 0)"
done
```

with three required properties: the counter string is taken verbatim from `claims.json` (so the claim is
graded, not a paraphrase); each side prints the token it read; and `discriminate=1` is required on both.
Add one limb running `capture-binding-check.py` on both exports and requiring `exit=0` on both.

Red-before, today, without any implementation: C2 reads `base=0 tip=0 discriminate=0`; C1's declared
invocation exits 2 (and its corrected form reads `tip=5` against the working tree while the committed
tip reads `0`); the binding limb was `base=exit 0 tip=exit 1` at 16:02 and is `exit 0` on both since the
16:06–16:12 repair — which is exactly why the receipt must be generated at the final revision, not once.
The receipt turns green only when the C2 counter reads 26 at the tip *export*, the C1 fixes are
committed (so tip=0 unresolved), and the binding limb is green on both exports.

Why this is the right size: it does not widen C1's frozen list or C2's frozen target (freeze integrity
holds — `claims.json` is not edited; the corrected counter string and the S069 URL/transformation
disclosure go into an appended `claims-erratum` block, the route C1-D2's own repair already uses), it
reuses instruments that already exist and are selftested, and it converts the eight narrative defects
into one executable property plus the existing per-artifact gates.

## 6. Risks (stated, not smoothed)

1. **Drift can satisfy a discrimination check for the wrong reason** — a knowledge file added by an
   unrelated commit moves a count. The receipt must print the token *and* stay paired with the
   per-artifact gates (binding, `knowledge-expected.txt` diff, frontier harness); discrimination is a
   necessary condition, never sufficient.
2. **Freeze integrity.** Editing `claims.json` after freeze would repeat the kaidoku r38 M38-1 failure
   (`kaidoku-shokunin/corpus/lessons/round-38.md:32`). The erratum must keep the original string visible
   and name it `superseded`.
3. **A moving tip.** The tip export is HEAD only until L1 commits; a receipt run mid-round is stale by
   construction and must record `export-ref` (the r43 J8 lesson).
4. **The S069 fix landed mid-seat and carries a residual.** The URL repair satisfied the gate (16:12),
   but the byte-transformation is still undeclared: the row must state `api-json→body-text` plus the raw
   byte count (47136 at recon, 48657 at my re-fetch, stored 45681) as S067/S068 do, or the next spot-check
   routes it as D-1-shaped. If the lane later moves the REST URL into the row's source cell it risks
   `FAIL rule=double-https-row` (rule B4, `capture-binding-check.py:48-51`); if it instead pins the
   page-rendered text it must re-capture. Either way the raw byte count must be stated.
5. **Live-API non-stability.** My single re-fetch returned 48657 B / `f7dbb8c9…`; the API is not
   byte-stable, so a "pin must reproduce from its URL" rule needs the declared transformation or it is
   unimplementable.
6. **Concurrency.** This report was written while siblings edited the same tree; the S069 URL repair,
   the counter's new `export-unavailable` guard and the `fixed=3→5` drift all happened inside one hour.
   Every timestamped claim above is true as measured; a re-run may show a cleaner tree, which changes
   which limbs are red, not the invariant.

## 7. Verification (commands a reviewer can re-run)

```
git rev-parse HEAD                                                  # 66314015122b9aa32dc40f2f1815df56624c26d1
grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md              # 0  (claim's counter)
grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md        # 26 (control's counter)
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md # 70
find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l              # 63
python3 corpus/instruments/capture-binding-check.py                 # 16:02: FAIL url-mismatch S069, exit 1; 16:12: bound=58, exit 0
python3 corpus/instruments/capture-binding-check.py --root <5ab3a60 export>  # 57/57, exit 0
python3 corpus/instruments/capture-binding-check.py --selftest      # cases=33 failures=0
python3 corpus/instruments/r44-routed-defects.py --root . --baseline <base>  # argparse: --report required
python3 corpus/instruments/r44-routed-defects.py --root . --baseline <base> --report .ufo/reports/round-44/kasegi.md
                                                                    # 16:03 fixed=3; 16:13 fixed=5 (untracked fixes)
python3 corpus/instruments/r44-routed-defects.py --root <HEAD export> --baseline <base> --report <absent>
                                                                    # fixed=0 unresolved=8 exit=1
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069
                                                                    # Q1-Q3 OK (three quotes only)
ls .ufo/waves/round-44/controls/c1-do-nothing.txt .ufo/waves/round-44/controls/c2-do-nothing.txt  # both absent
```

## 8. Limitations

- One live fetch of the REST endpoint (16:03 local); non-byte-stability is shown by one sample, not a
  distribution.
- The working tree was under concurrent edit by other seats (5 modified tracked files, untracked
  `claims-erratum-6.md`, `controls/{missing-suite-base,round43-registry-correction*,fix-hash-count,census-invocation-error}.txt`,
  `wave1/R44Review*.md`, `wave1/R44Scout*.md`, `source-recon/`, the knowledge entry and the round-44
  snapshot). Every number above is timestamped to 16:02–16:13 and may differ at the final revision.
- `corpus/instruments/r44-routed-defects.py` is untracked and changed during the seat (it gained an
  `export-unavailable` guard between 16:03 and 16:13); its final bytes may differ.
- I did not execute the r43 suite or any of its 19 limbs, and did not run census adversarial rows.
- I did not attempt to determine whether the live API body actually contains the pinned text at the same
  offsets; the pin binds the stored extract, and `source-recheck.py` verified quotes against that extract.

## 9. Boundaries observed

No lane/fleet production write except this report. No git/jj mutation, no index touch, no commit, no
push, no sibling or domain source tree touched, no operator config touched, no install, no pacman. All
worlds were built with `git archive | tar -x` into scratch. Scratch root: `$HYAKU_SCRATCH` was **unset**
(`printf` → empty), so I used the existing convention root `/home/vgpnk/.cache/hyaku-scratch/kasegi-r44/R44Conn1/`
(never `/tmp`); it held the state snapshot, the two exports, the gate outputs and the synthetic F26 row,
and was removed on exit — removal verified.
