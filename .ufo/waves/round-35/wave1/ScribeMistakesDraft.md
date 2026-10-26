# ScribeMistakesDraft — round-35 `## Mistakes` draft (rows only; the L1 integrates)

Seat: `ScribeMistakesDraft` (scribe, leaf). Lane `kasegi-shokunin`, round 35, wave `kasegi-r35-build`
(64 seats). Lane base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze commit
`617496b9c6e92bc671e7e78b83df69a04470d0e9`; wave-1 dispatch commit
`da2d3c687f82a9814ee71c91c930cb733050d37c` (lane `HEAD` unless a command names another revision).

This file is the **draft** of `corpus/lessons/round-35.md` `## Mistakes`. It is not the lesson and it
carries no round verdict. Field order follows `.ufo/waves/round-34/mistakes-erratum-1.md:6-7`
(class · evidence pointer · captured-by · fix · fix shown able to fail) with the corrected
`captured-by` semantics of `.ufo/waves/round-34/wave1/CritMistakes.md:126-127`: `captured-by` is a
seat or `none`, and a criterion goes in its own **Criterion missed:** field.

**Numbering contract** (CritMistakes-3, `.ufo/waves/round-35/wave1/CritMistakes.md:275-280`): M35-1 is
pre-numbered by the frozen claim; **rows beyond M35-1 are provisional** and must be minted in a
separate appended `.ufo/waves/round-35/mistakes-erratum-1.md` before any surface cites `M35-2+`.
Draft ids below are the L1's to renumber, merge or drop.

Snapshot: **58** files were present in `.ufo/waves/round-35/wave1/` at `2026-10-26T06:54Z` (57 seats'
plus this draft) of 64 spec names; `ExecDoNothingReject` and `SentScopeFinal` were still absent, and
`ConnSibling`'s seat filed under a non-spec name (M35-14). The set grew during composition: the late
`MutJunkTwin` (D5 **KILLED**), `ExecRegressionC2` (all seven C2 after-values match; no new row) and
`SimplifierCleanup` (no cleanup defect) were swept and added nothing; `SimplifierDocs` produced M35-3's
limbs (6)-(7) and M35-17. Every row states its own measurement instant where the state is
time-sensitive, and §4 lists what a later receipt can still overturn.

---

## 1. Method — what was swept, and what each pass can and cannot see

**(a) Vocabulary sweep** (triage only: it names files, it does not judge them; no row rests on it):

```
$ cd .ufo/waves/round-35/wave1
$ L=$(ls *.md | grep -v '^ScribeMistakesDraft.md$')      # exclude this draft; it quotes the word list
$ for w in FAIL exit=1 REFUSE REJECT BLOCKED SURVIVOR traceback UNVERIFIED 'no git'; do
    printf '%-11s files=%s hits=%s\n' "$w" "$(grep -l -F -- "$w" $L | wc -l)" \
      "$(grep -o -F -- "$w" $L | wc -l)"; done
FAIL        files=5  hits=13
exit=1      files=30 hits=251
REFUSE      files=8  hits=29
REJECT      files=1  hits=4
BLOCKED     files=0  hits=0
SURVIVOR    files=0  hits=0
traceback   files=0  hits=0
UNVERIFIED  files=0  hits=0
no git      files=17 hits=21
```

The exclusion is not cosmetic: without it the draft matches its own word list (`BLOCKED … 1/2`,
`SURVIVOR 1/2`, `traceback 1/2`, `UNVERIFIED 1/2`), which is a small instance of the same
self-reading trap the lane's instruments guard against (`corpus/instruments/README.md` on `resolve.py`
ingesting its own census).

Each receipt that tripped a word was **read at the cited lines** before any row was written; the
counts above are not evidence of a defect: `FAIL`/`exit=1` are dominated by mutation fixtures and gate
output that is *supposed* to fail, and none was counted as a defect without reading the line.

**(b) Structure sweep** — per receipt: `## Report`, an `exit=` token, a scratch path, a `Report:`
trailer. Pointers only; `exitcodes=0` is legitimate for a seat that ran only `ls`/`grep`.

**(c) Claim → disk cross-checks** — every receipt that asserts a landing was re-run read-only:
`git ls-files`, `git ls-tree`, `git diff --numstat`, `grep -c`, `sha256sum`, the frozen counting
commands, and `bash corpus/instruments/r35-defect-closure.sh` (plain, and `--root` over fixtures this
seat built). The suite was **not** run as a verdict; every suite run quoted below is a cross-check of
a receipt claim or a fixture demonstration.

Digest cross-checker (catches a wrong abbreviation — row M35-7):

```
$ python3 - <<'PY'
import re,pathlib
t=pathlib.Path('corpus/SOURCES.md').read_text()
fulls=set(re.findall(r'\b[0-9a-f]{64}\b',t))
bad=[(t[:m.start()].count('\n')+1,m.group(0)) for m in
     re.finditer(r'\b([0-9a-f]{6,64})…([0-9a-f]{4,64})\b',t)
     if not any(h.startswith(m.group(1)) and h.endswith(m.group(2)) for h in fulls)]
print('full_digests_in_file=%d abbrev=%d invalid=%d'%(len(fulls),
      len(re.findall(r'\b[0-9a-f]{6,64}…[0-9a-f]{4,64}\b',t)),len(bad)),bad)
PY
full_digests_in_file=5 abbrev=2 invalid=1 [(79, 'd69349e8…77e8826')]
```

**What this seat did not do:** it did not re-run any network fetch, the census, the harness or
`source-recheck.py` for the round's claims, did not run the suite's `--selftest`, and did not treat a
mid-wave suite run as a verdict. It read the fleet root only where a receipt's claim required it
(`.ufo/watchdog.log` via the citing receipt, never re-derived).

---

## 2. Rows

### M35-1 — round 34's wave wrote its results file after the round was declared `complete`, so the file was never committed

Class: landing / closure-order (a rendered wave is not a committed round). **Evidence:**
`corpus/lessons/round-34-verifier-spotcheck.md:30` (§1 row "No uncommitted round work":
`?? .ufo/waves/round-34/wave1-results.json`, 312874 B, `sha256 3afa3581…`) and `:183` (§6 D4, both
limbs); the offset and its two inputs are measured in `wave1/ExecD4ResultsTrack.md:57` (driver line
`1488:2026-10-26T03:19:31-03:00 complete kasegi round=34`), `:61` ("written **3 min 48 s after** the
closure line"), `:188-190` (mtime `06:23:19Z`), and the same window's transient rewrite of the
committed `wave1/ExecRegressionC1.md` (`:198-199`). **Captured by:** `none` — the writer was the wave
dispatcher and no round-34 seat receipt names the file
(`grep -rln 'wave1-results.json' .ufo/waves/round-34/wave1/ | wc -l` → `0`, re-run by
`CritMistakes.md:35-49`). **Criterion missed:** R4 (`corpus/QUALITY.md:38`: "a round counts only with
a resolvable work commit … a rendered wave is not execution"). **Routed by:** round-34 verifier
spot-check. **Fix:** lane side — `check_d4` requires the results file *and* the provenance note tracked,
one mutant per limb (`corpus/instruments/r35-defect-closure.sh`, `sha256 0ae4b484…`); the note landed
(`.ufo/waves/round-34/wave1-results.json.provenance.md`, 5639 B, `e1c44301…`, `wave1/ExecD4ResultsTrack.md`
§3). Harness side — no post-`complete` writes, owner the wave dispatcher, check
`git status --porcelain` empty at closure start. **Fix shown able to fail:** at the freeze commit both
`git cat-file -e 617496b9:<path>` calls exit `128`; the live tree reads
`D4 check=tracked=0,provenance=1 open=1` (measured `06:47Z`). The provenance limb **cannot** fail on
the shape it names — see M35-2.

### M35-2 — the D4 provenance limb counts file existence, so the defect closes with the note untracked

Class: closure clause satisfiable by an uncommitted artefact. **Evidence:**
`corpus/instruments/r35-defect-closure.sh:207` (at `sha256 0ae4b484…`):
`if [ -f .ufo/waves/round-34/wave1-results.json.provenance.md ]; then prov=1; else prov=0; fi` —
`[ -f ]` never consults the index, although D4's own sentence is about a *committed* note.
**Captured by:** `CritMistakes-3` (`wave1/CritMistakes.md:50-70`, fixture B); reproduced here.
**Criterion missed:** R4 / R14 ("wave evidence is receipts and digests in git"). **Fix:** one line —
`prov=$(git ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l)` — and keep the
per-limb mutant. **Fix shown able to fail, measured by this seat** (fixture
`/fast/scratch/hyaku/kasegi-r35/ScribeMistakesDraft/d4provenance`: a fresh `git init` tree with the
results JSON committed and the note present but **untracked**):

```
$ git ls-files -- .ufo/waves/round-34/wave1-results.json | wc -l                 → 1
$ git ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l  → 0
$ bash corpus/instruments/r35-defect-closure.sh --root …/d4provenance
D4 check=tracked=1,provenance=1 open=0
```

`open=0` with the note untracked is the defect; with the `git ls-files` limb the same tree reads
`provenance=0 open=1`.

### M35-3 — the closure clauses for D1, D2 and D6 are bare, unscoped greps: a marker *quotation* fails D1, a *repudiation* satisfies it, the prose spelling D1 was routed to catch is not read, and the placeholder class lives on in the report where no check looks

Class: counter discrimination / clause satisfiable by non-corrective prose. **Evidence:** seven
independent measurements inside this wave —

1. `wave1/ScoutDatawalk.md:70` (F-1): `grep -c 'LANE_HASH' SCORECARD.md` → `0` **at freeze**, so that
   kill-rule term is satisfied before any work (`git show 617496b9:SCORECARD.md | grep -c -F --
   '<LANE_HASH>'` → `0`, re-measured here).
2. `wave1/ScribeIntegrationNotes.md:340-341,358-359`: the literal read `1` at `06:35Z` inside D1's own
   correction prose and was rewritten to `0` at `06:36:18Z` ("angle-bracket lane-hash marker").
3. `wave1/CritC1Kill.md:215-232`: a tree whose only `c1c6a5f` mention is "the round-34 tip c1c6a5f
   **could not be confirmed** by this seat" reads `D1 … correction-c1c6a5f=1 open=0`.
4. `wave1/CritOverclaim.md:190` (P1): with `**Final lane commit: the L1 fills this line in the closing
   commit.**` restored, the suite reads
   `D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0` — green with the
   placeholder present; the routed fix is "widen the R1 check to placeholder prose"
   (`corpus/lessons/round-34-verifier-spotcheck.md:145-148`) and `check_d1` has no such limb.
   `wave1/CritOverclaim.md:156` (O5) adds that `SCORECARD.md:1259-1261` attributes a three-spelling
   fact to a two-literals check.
5. `wave1/CritMistakes.md:190-217` (F4): D2's erratum limbs are global greps
   (`round-34 depth:density row` and `201.2` anywhere), so an unrelated sentence carrying `201.2`
   reads `D2 … open=0` with no correction present.
6. `wave1/SimplifierDocs.md:157-175` (C-3): D6's predicate **forbids quoting the sentence it
   corrects** — `grep -c -F 'did not file a receipt (dead seat' L1Integration.md` must be `0` *and*
   `Correction (round 35)` present in the same file, so the correction cannot name what it fixes.
7. `wave1/SimplifierDocs.md:108-118` (P5): the placeholder class recurred **outside the counter's
   scope** — the report draft carried `⟨from the wave registry / L1: names and counts⟩` at `:394`
   (`:385` at SimplifierDocs' read),
   and `check_d1` greps only `SCORECARD.md` (`sed -n '/^check_d1()/,/^}/p'
   corpus/instruments/r35-defect-closure.sh`), so no closure check scans the report.

**Captured by:** `ScoutDatawalk`, `ScribeIntegrationNotes`, `CritC1Kill`, `CritOverclaim`,
`CritMistakes-3`, `SimplifierDocs` (six seats, all non-authors of the clauses). **Criterion missed:** R22
(satisfiability against base bytes) for the vacuous marker term; R11/R13 (a counter publishes its
discrimination, each limb load-bearing) for the rest. **Fix:** bind each clause to its slot and
conjoin it — `sed -n '/^## Round 34 /,$p' SCORECARD.md | grep -A1 'Final lane commit:' | grep -c c1c6a5f`
(`CritC1Kill`'s slot-bound probe), `grep -cE 'round-34 depth:density row.*201\.2'` for D2, plus a third
limb `grep -c -F 'the L1 fills this line' == 0` with one mutant each; escape or strip marker quotations
before counting. For D6, count the stale sentence only outside the appended `Correction (round 35)`
block (or drop the zero-count limb and require the correction to name the committed receipt
`wave1/ExecRegressionC1.md`), so the correction may quote what it closes. **Fix shown able to fail,
measured by this seat** (fixture
`/fast/scratch/hyaku/kasegi-r35/ScribeMistakesDraft/d1prose` = a byte copy of the live `SCORECARD.md`
plus one line `Prose about a marker (not a placeholder): the literal `<LANE_HASH>` appears here only as
a quotation.`):

```
$ bash corpus/instruments/r35-defect-closure.sh --root …/d1prose
D1 check=placeholders=0,lane-hash-markers=1,correction-c1c6a5f=3 open=1
$ bash corpus/instruments/r35-defect-closure.sh --root …/d1clean      # same copy, no added line
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
```

A quotation of the marker turns a green tree red, and a repudiation of the hash turns a red tree green.

### M35-4 — the round's own gate has no Gates & probes registry row, and D3's literal is satisfied by a near-name sibling

Class: gate registration (the D3 defect class, one round after D3 was routed). **Evidence:**
`grep -c -F 'r35-defect-closure' SKILL.md` → `0` while `r-defect-closure` → `4` and
`kill-rule-check` → `4` (`SKILL.md:1097-1098`); the suite the C1 claim actually runs is
`corpus/instruments/r35-defect-closure.sh`; `check_d3` greps `r-defect-closure`, which is **not** a
substring of `r35-defect-closure`, so the round's own counter passes D3 while having no registry row.
Measured at `06:44Z`: `bash corpus/instruments/r35-defect-closure.sh` →
`D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0`. **Captured by:**
`ExecD3SkillRegistry` (`wave1/ExecD3SkillRegistry.md` §Findings 1, "Name split inside claim C1 … that
file still has no registry row"), `ExecScoreGap` (`wave1/ExecScoreGap.md:57-59,64` — `BASE-ABSENT=1` on `SKILL.md:1097`; the same row's
anchor red), and `CritMistakes-3` (`wave1/CritMistakes.md:127-161`, which calls it the strongest row
of the round). **Criterion missed:** the gate standard quoted at
`corpus/lessons/round-34-verifier-spotcheck.md:180` — "not graded conformant until registered".
**Fix:** append an eight-field registry row for `r35-defect-closure.sh` (name, gate|probe, entry
command, verdict map, selftest spelling, pinned-value path, write scope, owner) and add
`registry-r35-defect-closure` as its own D3 clause with a `filter_out` mutant (the construction exists:
`D3:-registry-r-defect-closure`). **Fix shown able to fail:** `grep -c 'r35-defect-closure' SKILL.md`
→ `0` today with D3 `open=0`; the filter-out mutant must print `registry-r35-defect-closure=0 …
open=1` after the row lands and `open=0` when the row is deleted.

### M35-5 — the uncommitted plan edit rewrote the C2 task around a URL that 404s, contradicts the landed capture, and has no author

Class: dispatch literal not verified before dispatch / plan artifact carrying a false provenance.
**Evidence:** `wave1/CritBoundary.md:80-102` (F2) — `git diff` of
`.ufo/waves/round-35/build-spec.py` (mtime `03:32:50`, `sha256 a56179ca…`) replaces the `ExecC2Capture`
task with "…the JSON endpoint … returns HTTP 404 …, so the official CSV distribution is the primary
data source"; `wave1/ExecC2Capture.md:11-22` measures the `404` on three user agents (`size=46916`,
HTML), `:44` records that the L1's interim CSV steer was itself wrong ("that steer's premise is false
one path over"), and the landed manifest/row pin the long JSON feed
(`corpus/source-snapshots/round-35/manifest.json`, `url=…/feeds/known_exploited_vulnerabilities.json`;
`corpus/SOURCES.md:58`). The committed `wave1-spec.json` still names the dead short URL; the edit has
**no consumer** (`wave1-dispatch.json` mtime `03:29:04`, never regenerated) and no receipt declares
editing `build-spec.py` (`wave1/CritBoundary.md:80-102`). **Captured by:** `CritBoundary-3` (F2) and
`ExecC2Capture` (§1, §7.1). **Criterion missed:** none — R22 covers frozen claim predicates, not
dispatch prompts; the freeze procedure has no URL-probe limb. **Fix:** revert `build-spec.py` to the
dispatch-time bytes or narrow the sentence to the short URL; state authorship in the lesson; probe each
dispatch URL under the instrument UA before the freeze. **Fix shown able to fail:** `git diff --
.ufo/waves/round-35/build-spec.py` is non-empty today and empty after the revert; the manifest's `url`
is a live JSON feed while the spec's is the 404 path. Caveat: the 404 is receipt-pinned (a live-network
fact), not re-runnable offline. **Conflict recorded verbatim** — `CritMistakes-3` (`wave1/CritMistakes.md:253-260`,
F7) recommends **not** minting this row: "External drift, not lane behaviour, and the artefact choice is
already recorded in the committed manifest; a mistake row would cite a live-network fact that cannot be
re-run offline. Keep it as a lesson caveat under C2." The row as drafted survives that objection only
through the *uncommitted, unconsumed* plan edit and the dead literal in the committed spec; the L1
decides which form it takes.

### M35-6 — C2's frozen junk-twin rejection limb repeats the defect the round's own D5 erratum repairs

Class: frozen predicate with no discriminating invocation. **Evidence:** `claims.json` C2 predicate
("the junk F18 twin … is rejected by the admission gate") and `after[6]` ("source-recheck exit != 0 and
non-author reviewer REFUSE on record"); `wave1/ScoutDatawalk.md:73` (F-4: the twin carries "the same
command the real entry will carry … exactly the round-34 D5 finding"); `wave1/CritOverclaim.md:167`
(O7: "C2 `after[6]` is literally false as frozen"); the round-35 repair is
`.ufo/waves/round-35/claims-erratum-d5.md:26-29,41-81`, which restates the *round-34* sentence and
records that "source-recheck exit != 0 on the twin … has no executable form as frozen". **Captured by:**
`ScoutDatawalk` (F-4) and `CritOverclaim` (O7). **Criterion missed:** the D5 erratum's own restated rule,
applied to the round-35 claim at freeze. **Fix:** state the twin's rejection as the capture comparison
(the twin's two fabricated sentences occur `0` times in the pinned `S052.txt`) and append a C2 erratum
in the D5 form. **Fix shown able to fail, measured by this seat:** the twin's `recheck:` line
(`.ufo/waves/round-35/c2-controls/junk-f18.md:11`) re-runs the live manifest —
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json
--source S052` → `exit=0`, i.e. the frozen clause reads *pass* on a fabricated twin; the quote
comparison separates them.

### M35-7 — the landed S052 search-log bullet carries two wrong facts: a count and a digest abbreviation

Class: unverified literal in landed bytes. **Evidence:** `corpus/SOURCES.md:79` — "CISA 2 knowledge
files and **7 SOURCES rows** …" and, on the same line, `sha256 d69349e8…77e8826`. The capture's digest
is `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`
(`corpus/SOURCES.md:58`, `manifest.json`), whose last 8 are `779e8826`; `'77e8826' in <digest>` is
`False`, `'779e8826' in <digest>` is `True`. Base registry rows mentioning CISA (case-insensitive) are
`5` (`S003 S008 S021 S023 S026`), not `7`. **Captured by:** `ScribeSOURCESRow`
(`wave1/ScribeSOURCESRow.md:100-110`, F2/F8 with the same computation; a peer seat, not a criterion).
**Criterion missed:** none — the census validates row shape and URL binding, not prose counts or
abbreviated digests. **Fix:** an R9-style appended correction naming both facts (never a rewrite of
`:79`), plus the §1(c) abbreviation check in the census or the recheck audit. **Fix shown able to fail:**
the §1(c) command prints `abbrev=2 invalid=1 [(79, 'd69349e8…77e8826')]` today and `invalid=0` after the
correction; `git show 3266c99:corpus/SOURCES.md | awk -F'|' '/^\| *S[0-9]+ *\|/ && tolower($0) ~ /cisa/
{n++} END{print n}'` → `5`.

### M35-8 — two live seats share one id across rounds, so a peer's coordination reached the wrong agent and the landed row's author is "unnamed"

Class: dispatch / identity collision. **Evidence:** `wave1/ExecRegistryAppend.md:3` names itself
`ExecRegistryAppend-3` and claims authorship ("Author of record: this seat … authorised to author the
three blocks"); `wave1/ScribeSOURCESRow.md:7-15` records the split from the other side —
"ExecRegistryAppend — the agent I addressed as that executor — replied that it holds only the round-33
item and disclaims the round-35 write, so the appending seat is unnamed in my evidence". The spec's item
name is `ExecRegistryAppend`; the roster carries both `ExecRegistryAppend-3` and a round-34
`ScribeSOURCESRow-2` family. **Captured by:** `ScribeSOURCESRow` (recorded the ambiguity and resolved it
wrongly); `none` as a gate. **Criterion missed:** none — no clause binds a receipt's declared seat id to
the spec name. **Fix:** round-prefix seat ids (`r35-ExecRegistryAppend`) so a live prior-round identity
cannot answer for the current one, and require a substitute's receipt to quote the authorizing message
id. **Fix shown able to fail:** the on-disk contradiction is the red state — the author's receipt and the
peer's record disagree about who wrote `corpus/SOURCES.md:58`; a name-uniqueness check against the
registry is red on this wave and green after the prefix.

### M35-9 — the report draft asserted the two do-nothing controls were "committed at the freeze" while both were absent from the freeze and untracked

Class: false provenance in a landing surface. **Evidence:** `wave1/CritOverclaim.md:135-155` (O4)
quotes the pre-fix text at `ScribeReportDraft.md:53-56` (digest `dc267907bb5bf07a…`) — "**Do-nothing
controls committed at the freeze:** …" — and the measured facts:
`git ls-tree -r --name-only 617496b9 -- .ufo/waves/round-35/` lists exactly four files
(`c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`, `claims.json`) and
`git status --porcelain | grep -c 'c1-controls/fake-suite.sh\|c2-controls/junk-f18.md'` → `2` (both
`??`). This seat read the same sentence independently at `06:41Z`
(`wave1/ScribeReportDraft.md:62-65` at mtime `03:34:36`). **Captured by:** `CritOverclaim` (O4).
**Criterion missed:** R4 again (a claim of commit state without `git ls-tree`). **Fix: landed in flight
at `06:52Z`** — the line now reads "**Do-nothing controls (untracked at draft time)**"
(`wave1/ScribeReportDraft.md:61`, digest `c1a6871d5e6a0416…`). **Fix shown able to fail:** the
`git ls-tree` and `git status` commands above are red on the pre-fix sentence and green on the corrected
one; a check that every "committed" claim in a draft is followed by a `git ls-tree`/`ls-files` proof is
red today on `ScribeReportDraft.md` as it stood at `03:34Z` (receipt-pinned).

### M35-10 — the LOG draft asserted three C1 after-values as measured while the receipt it cited said otherwise; corrected in flight

Class: summarization past measured evidence (M34-1's class). **Evidence:**
`wave1/CritOverclaim.md:112-131` (O1–O3) — at `06:37Z` the draft (digest `585c8f2a…`) read "plain run
`closed=7/7 exit=0` … `--selftest` `cases=7 failures=0` ⟨`ExecClosureSuite.md`⟩" while that receipt's
§3 reads `closed=4/7 exit=1` and §6 `selftest cases=7 failures=3`; it asserted the QUALITY supersession
rows land ("both counts 0" measured); and it wrote D4 "tracked 0 → 1" while `git ls-files … | wc -l` →
`0`. All three were corrected at `06:46Z` (`w=585c8f2a…` current). **Captured by:** `CritOverclaim`
(O1–O3). **Criterion missed:** R19/R18 (a quoted figure is produced by a command the row cites).
**Fix: landed in flight** — the draft now quotes the tree label with each suite number. **Fix shown able
to fail:** the rule that produced all three errors is itself checkable — a draft sentence citing
`ExecClosureSuite.md` without its tree label (live / all-fixed / base) can be grepped; the pre-fix text
is receipt-pinned at `585c8f2a…`.

### M35-11 — a receipt asserted its own scratch was deleted while the tree existed for ~200 s, and attempt suffixes collapse two attempts into one directory

Class: durable record as prediction / scratch hygiene. **Evidence:** `wave1/ExecClosureSuite.md:390-398`
(quoted `rm -rf` + `ls … || echo scratch-absent` + "No work tree of mine is left on disk"), contradicted
in `wave1/CritBoundary.md:45-79` (F1): writes at `03:42:59`, `03:43:36`, `03:43:43` and `ls -d` at
`03:44:26` → **PRESENT**; absent again at `03:45:57`, with no second cleanup in the receipt. The seat
now records the correction itself at `wave1/ExecClosureSuite.md:381` ("`CritBoundary-3` caught an earlier
version of this paragraph claiming `scratch-absent` while a later …"); the second, milder instance is
`ScribeEntryF18` (`wave1/CritBoundary.md:45-79`). The naming limb: `wave1/CritBoundary.md:103-111` (F3)
— receipts address the un-suffixed path, so `ExecNoHarmFinal/` holds attempt-1 and attempt-3 fixtures in
one directory and `RevC2BeforeAfter-2/` nests a second copy of itself. **Captured by:** `CritBoundary-3`.
**Criterion missed:** R1 (a liveness/absence assertion carries an as-of `test -e`). **Fix:** make the
cleanup block the seat's **last** act and phrase it as executed output (or prospectively, verified by
the L1 gate); scratch dir = full seat id; the L1 close adds
`find /fast/scratch/hyaku/kasegi-r35 -mindepth 1 -maxdepth 1 -type d -printf '%f\n'` and lists only
dirs whose seat has no receipt. **Fix shown able to fail:** `ls -d …/ExecClosureSuite` → PRESENT at
`03:44:26` against a receipt saying absent (CritBoundary's measurement); today it is ABSENT, so the
ordering defect is invisible to a single end-state check — which is exactly why the gate is a
directory-vs-receipt comparison, not a `test -e`.

### M35-12 — a seat ran `jj st`, which snapshots the working copy; the wave rules forbid jj mutations

Class: overstatement / VCS mutation (M34-5's class, recurring). **Evidence:**
`wave1/ScoutPackageThemes.md:106` — "one `jj st` was run once to see lane state (it snapshots the
working copy; …)"; `wave1/CritBoundary.md:118-124` (F5) matches it to the op log's
`snapshot working copy` entries and records that the lane has no seat-made commit, bookmark move,
`describe` or staged entry. **Captured by:** `CritBoundary-3`. **Criterion missed:** none — no check
reads the op log. **Fix:** `jj --ignore-working-copy st` (or plain `git status`); record the op id in
the receipt when a jj read is unavoidable. **Fix shown able to fail:** `jj --ignore-working-copy op log`
shows `snapshot working copy` ops from the wave window (CritBoundary's measurement; not re-run here to
avoid adding another snapshot).

### M35-13 — the claims declare a freeze instant 62 min after the freeze commit and still in the future

Class: unbound provenance literal (R22/R25 applied to a timestamp). **Evidence:**
`.ufo/waves/round-35/claims.json:6` `"frozen_at_utc": "2026-10-26T07:30:00Z"`;
`git log -1 --format='%h author=%aI committer=%cI' 617496b9` →
`committer=2026-10-26T03:28:03-03:00` (= `06:28:03Z`); `date -u` at composition `06:41:12Z` →
declared freeze is `+48.8 min` ahead of the wall clock. Round 34's field (`05:00:00Z`) sat before its
own commit (`05:28:39Z`), so the sign is the anomaly. **Captured by:** `none`. **Criterion missed:**
R22's satisfiability limb, extended to dates. **Fix:** set `frozen_at_utc` from the freeze commit's
committer date and assert `declared <= now`. **Fix shown able to fail:** the difference is negative
today and non-negative once bound.

### M35-14 — one seat's receipt is filed under a name the spec does not carry, so the name-vs-file coverage count shows one missing seat and one extra file

Class: evidence naming (the round-34 `ScribeReportDraft-2` observation, which was prose and not a row,
recurring). **Evidence:** `ls .ufo/waves/round-35/wave1/Conn*` → only `ConnSibling-ruling-draft.md`; the
spec item is `ConnSibling`; the file carries no `## Report` (structure sweep: `report=0`), so it is a
draft ruling rather than the seat's receipt. **Captured by:** `none` — the L1's composition computes the
coverage count, no gate does. **Criterion missed:** none. **Fix:** file under the spec name (or record
the alias in the wave manifest) and require `## Report` in every file under the wave dir. **Fix shown
able to fail:** the set difference between `wave1-spec.json` names and `ls wave1/*.md` stems is
non-empty on both sides today and empty after the rename; `grep -c '^## Report'
.ufo/waves/round-35/wave1/ConnSibling-ruling-draft.md` → `0`.

### M35-15 — C1's counter set carries a C2-owned counter and leaves five of its seven defects without an independent counter

Class: claim measurement mis-scoping. **Evidence:** `claims.json` C1 `counting_commands` = suite plain,
suite `--selftest`, `grep 'filled by the L1'`, `grep -cE '^\| *S…'` → 52, `git ls-files …
wave1-results.json`; the third and fifth cover D1/D4, the second is the whole suite, and the
registry-row counter belongs to C2 — measured and reported as F-2/F-6 by `wave1/ScoutDatawalk.md:71`.
**Captured by:** `ScoutDatawalk` (F-2). **Criterion missed:** R13 (each limb load-bearing, each claim
measured by its own instrument). **Fix:** move the SOURCES counter to C2 and add one counter per D item
(D2, D3, D5, D6, D7). **Fix shown able to fail:** a per-item coverage table over the seven D clauses has
`2/7` independent counters today; the mis-scoped counter fails C1 when C2 misses.

### M35-16 — the registry row that closes D3 first carried a citation that failed the lane's own anchor gate

Class: register-a-gate-by-writing-a-file-that-fails-a-gate. **Evidence:**
`wave1/ExecScoreGap.md:57-59` measured `python3 corpus/instruments/anchorcheck.py SKILL.md` → **exit 1**
with `BASE-ABSENT=1` because `SKILL.md:1097` carried a bare `S050.txt:70`; the addendum re-ran after the
fix (`wave1/ExecScoreGap.md:339`): "16 in-range, 0 bad, LOST-RECORDED=306, BASE-ABSENT=0, exit 0". **Captured by:** `ExecScoreGap`.
**Criterion missed:** R12/R1 (a citation resolves at its written path). **Fix: landed** — the token is
now `corpus/source-snapshots/round-32/S050.txt:70`. **Fix shown able to fail:** `anchorcheck.py SKILL.md`
exit `1` on the pre-fix bytes, `0` after; **caveat** the pre-fix bytes are transient (digest-pinned in
the receipt, not in the tree), so a re-runnable red needs the bare token planted in a fixture.

### M35-17 — the report draft's headline verdict counts five closed defects while its own parenthetical accounts for four closed, one commit-pending and two unlanded

Class: numeric overclaim in a landing surface. **Evidence:** `wave1/SimplifierDocs.md:143-151` (C-1)
quoting `wave1/ScribeReportDraft.md:282-284` (`:275-278` at SimplifierDocs' read): "**quality: `improved`** — five of the seven routed
defects are closed and measured (D1, D2, D3, D5 closed; D4's record is digest-verifiable but its
`tracked` clause is the L1's commit; D6/D7 are drafted and measured on copies, not landed)". The
parenthetical sums to `4+1+2=7` while the first clause says **five**; the live suite the same draft
quotes reads `closed=4/7`. **Captured by:** `SimplifierDocs` (C-1). **Criterion missed:** R19 (a quoted
figure is produced by a command the row cites). **Fix:** one word — "four", or "five closed or
commit-pending". **Fix shown able to fail:** the tally is arithmetic against the draft's own
parenthetical and against `bash corpus/instruments/r35-defect-closure.sh` → `closed=4/7 exit=1`
(measured `06:47Z`); the corrected sentence reads the same number as the counter.

---

## 3. Cleared on re-check, and candidates deliberately not minted

| observation | disposition |
|---|---|
| `wave1/ExecRegistryAppend.md` briefly asserted "S052 row added" while `corpus/SOURCES.md` read 51 rows, and its `## Report` was a two-line stub with zero `exit=` (this seat's `06:39Z` read) | **not a row**: the seat was still running — by `06:44Z` the append had landed (`52` rows, `:58` present) and the Report section carried 103 lines and 4 exit codes. It is why §2 rows date their measurements. |
| `capture-binding-check.py` prints `multi_row_url=2`, `orphans=1 orphan=S040-live.txt` | **not a row**: declared informational by the instrument (`corpus/instruments/capture-binding-check.py:59`); the two URLs are `S006/S028` and `S024/S029`, not S052. |
| `wave1/CritC1Kill.md:227` "the round-34 tip c1c6a5f could not be confirmed by this seat" | **not a row**: it is the inside of a demonstration fixture proving M35-3's repudiation gap. |
| before-controls remain output-only for the fourth round (`wave1/ExecBeforeReceipts.md:211-223`; `grep -rln 'before.txt' corpus/instruments/` → README prose only) | **not minted**, on `CritMistakes-3`'s reasoning (`wave1/CritMistakes.md:236-252`, F6): a row whose fix never lands is the prose-without-check the schema forbids. Recorded as a standing open item, with the fix owner named. |
| `claims-erratum-d5.md` §3 prescribes `/fast/scratch/kasegi-d5/S051`, outside the mandated root (`wave1/CritBoundary.md:112-117`, F4) | **not a row**: hygiene note; the citing seat's own runs used the mandated root (`wave1/RevD5D6D7.md:73`). One-line rewrite. |
| `wave1/ScoutPackageThemes.md` names `anthropic/claude-sonnet-5-5` where most seats name another model | **not a row**: model attribution is not a round criterion. |
| `ScribeSOURCESRow` and `ExecRegistryAppend-3` both describe the S052 landing | **not a row on its own**: the ids differ (M35-8), the bytes are the same, and `capture-binding-check.py` reads `round-35 records=1 url_bound=1`. |

## 4. Limits of this draft

1. **Snapshot, not quiescence.** 58 files / 57 seats' receipts at `06:54Z`; the absent ones
   (`ExecDoNothingReject`, `ExecRegressionC2`, `MutJunkTwin`, `SentScopeFinal`, `SimplifierCleanup`,
   `SimplifierDocs`, `ConnTrends`, …) can add rows or overturn §3. The L1 must re-run §1 and the §5
   commands at quiescence; the rows whose subject is a landed file (M35-2, M35-4, M35-7, M35-9, M35-14)
   need only a re-read of that file and its git state.
2. **Two rows rest on receipt-pinned red states** — M35-5's 404 and M35-16's pre-fix digest — and say so;
   every other row's red state is re-runnable from committed bytes or a scratch fixture.
3. **M35-13 and M35-14 are small.** Filed because the assignment asks for every swept defect, not
   because they move an axis; the L1 may merge them into one provenance/naming row.
4. **This seat's scratch is deleted before yielding** (§5 R7), including the two fixture trees; their
   construction is given inline so both can be re-made in one command each.

---

## 5. Report

All commands ran in `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only git plumbing:
`log`, `show`, `ls-files`, `ls-tree`, `diff`, `cat-file`) unless a scratch path is named. No `git
add/commit/push`, no `jj` command, no `pacman`/tool install, no subagent, no write outside the wave
dir. Wall clock at composition: `2026-10-26T06:54Z`.

### R1 — snapshot and receipt set

```
$ ls -1 .ufo/waves/round-35/wave1/*.md | wc -l
58                                                              exit 0   # 57 seats + this file
$ git log --oneline -1
da2d3c6 round-35: wave-1 spec + dispatch (64 seats, v2)          exit 0
$ git status --short | wc -l
19                                                              exit 0
$ sha256sum corpus/instruments/r35-defect-closure.sh
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f   exit 0
```

Suite evolution observed while composing (each a different instrument, so every suite quote in §2 names
its digest): `d7ad8438…` (773 lines) → `0ae4b484…` (`check_d1/d4` unchanged across the two reads of this
seat). The critic's own read was at `a4f80067…` (`wave1/CritMistakes.md` §Report); nothing in §2 depends
on the intermediate digest.

### R2 — live suite state (`06:47Z`, cross-check, not a verdict)

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 … open=0   D2 … open=0   D3 … open=0
D4 check=tracked=0,provenance=1 open=1
D5 … open=0   D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
```

### R3 — the two fixtures that make M35-2 and M35-3 able to fail

```
$ bash corpus/instruments/r35-defect-closure.sh --root /fast/scratch/hyaku/kasegi-r35/ScribeMistakesDraft/d1prose
D1 check=placeholders=0,lane-hash-markers=1,correction-c1c6a5f=3 open=1          exit 0 (suite); D1 open
$ bash corpus/instruments/r35-defect-closure.sh --root …/d1clean
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
$ bash corpus/instruments/r35-defect-closure.sh --root …/d4provenance
D4 check=tracked=1,provenance=1 open=0                                           # the defect: note untracked
$ git -C …/d4provenance ls-files -- .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l
0
```

### R4 — claim-to-disk checks quoted in §2

```
$ grep -c -F 'r35-defect-closure' SKILL.md                              → 0     exit 1
$ grep -c -F 'r-defect-closure' SKILL.md                                → 4     exit 0
$ git ls-tree -r --name-only 617496b9 -- .ufo/waves/round-35/            → 4 files, no controls
$ git ls-files --error-unmatch .ufo/waves/round-35/c1-controls/fake-suite.sh   → exit 1 (untracked)
$ git ls-files --error-unmatch .ufo/waves/round-35/c2-controls/junk-f18.md     → exit 1 (untracked)
$ git diff --numstat 3266c99 -- SCORECARD.md                            → 33 15
$ git show 3266c99:SCORECARD.md | grep -n 'mean \*\*201\.7\*\*, 25 blocks, 710 path-citation' → 1145
$ grep -n 'mean \*\*201\.7\*\*, 25 blocks, 710 path-citation' SCORECARD.md                    → 1146
$ git show 617496b9:SCORECARD.md | grep -c -F -- '<LANE_HASH>'          → 0     exit 1
$ grep -n 'frozen_at_utc' .ufo/waves/round-35/claims.json               → 6:"2026-10-26T07:30:00Z"
$ git log -1 --format='%h author=%aI committer=%cI' 617496b9            → committer=2026-10-26T03:28:03-03:00
$ date -u                                                               → 2026-10-26T06:41:12Z
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
  (all OK)                                                              → exit 0
$ ls .ufo/waves/round-35/wave1/Conn*                                     → ConnSibling-ruling-draft.md only
$ python3 corpus/instruments/capture-binding-check.py                    → round-35 records=1 url_bound=1, multi_row_url=2, orphans=1
```

### R5 — digests of bytes this seat wrote

| path | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-35/wave1/ScribeMistakesDraft.md` (this file) | — | not self-pinned (a file cannot carry its own final digest) |

Digests of the bytes the rows assert about, so a re-verifier can bind a row to a revision (measured
`06:55Z`; every one of these files except `SCORECARD.md`/`SOURCES.md` may move again before the L1
commits — re-take before citing):

| path | sha256 |
|---|---|
| `corpus/instruments/r35-defect-closure.sh` | `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` (834 lines) |
| `.ufo/waves/round-35/claims.json` | `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982` |
| `corpus/SOURCES.md` | `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba` |
| `SCORECARD.md` | `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` |
| `corpus/QUALITY.md` | `807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` (freeze bytes: D7 rows still absent) |
| `.ufo/waves/round-35/wave1/ScribeReportDraft.md` | `546e38a5d6b998c15b1855cab0cc33778a9264f2442846da8360fb6de94bc31a` (moved after the O4 fix) |
| `.ufo/waves/round-35/c1-controls/fake-suite.sh` | `292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121` |
| `.ufo/waves/round-35/c2-controls/junk-f18.md` | `0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176` |
| `corpus/source-snapshots/round-35/S052.txt` | `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` |
| `.ufo/waves/round-35/claims-erratum-d5.md` | `eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6` |

No other file was created or modified. The file is **not** `corpus/lessons/round-35.md`; that lesson is
`ScribeLesson`'s surface and the L1's decision.

### R6 — scratch gate at composition

```
$ for d in /fast/scratch/hyaku/kasegi-r35/*/; do n=$(basename "$d")
    [ -f .ufo/waves/round-35/wave1/$n.md ] && echo "$n"; done
RevD5D6D7                                                       # receipt 03:42:38, scratch mtime 03:43:38 — seat still live (its §Verdict is "pending")
$ ls -d /fast/scratch/hyaku/kasegi-r35/*/ | wc -l
7                                                               # the rest belong to live seats; this seat's own dir is deleted below
```

That is M35-11's gate, run once: no finished seat except the live `RevD5D6D7` holds a tree at this
instant.

### R7 — scratch

Work tree: `/fast/scratch/hyaku/kasegi-r35/ScribeMistakesDraft/` (`sweep.sh`, `digestcheck.py`,
`sweep-s1.txt`, `d1prose/`, `d1clean/`, `d4provenance/`) and was removed as this seat's last act:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r35/ScribeMistakesDraft
$ test -d /fast/scratch/hyaku/kasegi-r35/ScribeMistakesDraft && echo PRESENT || echo ABSENT
ABSENT                                                          exit 0
```

The fixtures are reconstructed by the commands in R3/R4 above (one `cp` + one `printf` each). No
`/tmp` file was written. No tool install or upgrade was made (host `python3`, `git`, `coreutils` only;
no `pacman` transaction was attempted).

Report: .ufo/waves/round-35/wave1/ScribeMistakesDraft.md
