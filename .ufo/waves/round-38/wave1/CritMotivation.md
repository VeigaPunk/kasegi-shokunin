# CritMotivation — round 38, do-nothing and cheapest-skip controls

Seat: CritMotivation · role: critic · axes: depth:verifiability, coverage · milestone: round-38
Item: run the do-nothing and cheapest-skip controls — (1) base counters miss the C2 targets;
(2) a junk-row commit control (F21 row + junk S055 row + junk entry, no capture/manifest); (3) the
C1 cheapest skip (Correction lines + a fake all-gates receipt) and say which G-checks still fail.

Receipt-only: **no landable bytes** (no `## DELIVERABLE` block — this seat delivers findings, not
text the L1 pastes; round-37 defect D-A is not repeated here).

| tag | ref | note |
|---|---|---|
| BASE | `a173b0c2b98c5ae39599fa9be76027fbbead0b9e` | round-38 base, exported for every measurement |
| FREEZE | `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b` | claims freeze |
| TIP | `700153593eb586c70a6499c8ca225ee4d673bc9b` | lane HEAD at measurement (wave1 spec + dispatch) |
| R37J | `2387dcf6ccfefcfb703783387b9aade8fc82abfa` | r37 judged head |
| R37Y | `83975acc83df4bd8d5eaf463182ae615f2b64546` | r37 lane tip |
| SUITE | `.ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh` | landed during this seat's run; 61159 bytes, sha256 `85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6` (wave-1 deliverable, not yet committed to `corpus/instruments/`) |

Method. Every counter ran on a `git archive` export or a scratch fixture under
`/fast/scratch/hyaku/kasegi-r38/CritMotivation/` (TMPDIR bound there; work dirs `--work` under
it). The lane, the fleet root and `~/Projects/shokuknow` were never written: the only git calls
were read-only (`archive`, `diff`, `cat-file`, `merge-base`, `rev-parse`, `log`, `show`, `ls-tree`)
plus four `git init` fixtures whose `rev-parse --show-toplevel` was verified equal to the fixture
path before any commit. No package installs, no pacman, no service changes.

Tooling: `python3` (3.13), `git`, `bash`, `sha256sum` — already present; nothing installed.

---

## 1. Control 1 — do-nothing at BASE

### 1.1 C2 counters

```
$ git -C LANE archive a173b0c2 | tar -x -C base
$ cd base; TMPDIR=$S
frontier=20            registry=54        S055rows=0        knowledge=49      citeS055=0
python3 corpus/instruments/frontier-recheck-count.py --root base
  -> entries=23 pass=23 exit=0            (RC 0)
python3 corpus/instruments/capture-binding-check.py --root base
  -> records=44 bound=44 unbound=0        (RC 0)
python3 corpus/instruments/recheck-audit.py --root base --quiet
  -> strict pass=1/49 cdroot_fail=48 ... expect=present expected=49 missing=0 unexpected=0 exit=1
python3 corpus/instruments/recheck-audit.py --root base --cdroot LANE --quiet
  -> strict pass=49/49 ... expect=present expected=49 missing=0 unexpected=0 exit=0
bash scripts/sources-census.sh validate --file base/corpus/SOURCES.md
  -> W04 S028, W04 S029, ok; exit=0
ls base/corpus/source-snapshots/round-38 -> No such file or directory
grep -rliE 'CSAF|Common Security Advisory Framework|\bVEX\b' base/corpus/knowledge base/corpus/README.md base/corpus/SOURCES.md base/SKILL.md base/PROVINCE.md | wc -l -> 0
```

| C2 target (frozen) | BASE | met? |
|---|---|---|
| frontier 21 | 20 | no |
| registry 55 (S055 present, NF=13) | 54 / 0 | no |
| entry citing `source: S055` 1 | 0 | no |
| knowledge 50 | 49 | no |
| harness entries=24 pass=24 exit=0 | 23 / 23 | no |
| binding 45/45 | 44 / 44 (exit 0) | no — the *count* is 44, not 45 |
| audit expected=50 missing=0 unexpected=0 | expected=49, missing=0, unexpected=0 | no |
| census exit 0 (W04 S028/S029 only) | exit 0, W04 S028/S029 | **yes — already true at BASE** |

So the do-nothing run misses 7 of 8 C2 limbs; the one it satisfies (census exit 0) is a property
the base already had, i.e. it discriminates nothing. Note also that `recheck-audit.py` is
root-scoped: run inside an export it exits 1 on `cdroot_fail=48` although `expected=49` is
correct; the claim's command is only meaningful from the lane root (`--cdroot LANE` or cwd).

### 1.2 C1 at BASE

```
$ bash SUITE                      -> exit 2
  r38-closure: refusing to run against the live worktree: this suite is export-mode only.
$ bash SUITE --export-ref a173b0c2 --lane LANE --work $S/suitework-base
  G1 payload=province-correction=0,readme-correction=0,province-fence=closed,readme-fence=open,declared-blocks=0,declared-ok=0 closed=0
  G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,digest-match=0,run-lines=0,closed-line=0,selftest-lines=0,selftest-summary=0,scorecard-ref=0,shonen-ref=0,head-token-lines=0 closed=0
  G3 payload=resolutions-section=0,line-tokens=0,added-pending=0,added-placeholders=0,diff-read=ok closed=0
  G4 payload=dispatches=0,pairs=0,seats-ok=0,read=fail closed=0
  G5 payload=round38-section=0,final-lane-commit-lines=0,correction=0,f3246559=1,anchor-ancestor=1 closed=0
  G6 payload=r36=absent,r37=absent,r38=present,work=inside,tolerated=none,read=ok closed=0
  G7 payload=filled-section=0,correction=0,proposal-rows=0,missing=0 closed=0
  G8 payload=r37-suite=1,r37-closed=0,r37-exit=1 closed=0
  closed=0/8 exit=1
```

Do-nothing C1 = 0/8. Note G8: at freeze the before-control measured `closed=14/14` for the r37
suite; at my measurement the same command is **13/14** because r37 E9 reads the *live* lane:

```
$ bash corpus/instruments/r37-closure.sh --export-ref a173b0c2 --lane LANE --work $S/r37work
  E9 payload=status-read=ok,status-dirty=17,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent closed=0
  closed=13/14 exit=1
```

(G8's carry-over is therefore an ordering property, not a byte property — see F3.)

---

## 2. Control 2 — junk-row commit (no capture/manifest)

Fixture `junk/` = BASE export plus exactly three additions, nothing else:

1. `corpus/README.md`: one `| F21 | OASIS CSAF v2.0 … | admitted | knowledge/junk-csaf-vex-product-status.md | S055 | … |` row.
2. `corpus/SOURCES.md`: one `| S055 | OASIS CSAF v2.0 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html | docs | A | … | not captured | the VEX product-status categories | watch | 2026-10-26 | 90d | corpus/knowledge/junk-csaf-vex-product-status.md |` row, NF=13 (verified: `len(row.split('|'))==14` for 11 columns).
3. `corpus/knowledge/junk-csaf-vex-product-status.md`: `source: S055`, a `recheck:` line naming a
   manifest path that does not exist, no snapshot directory, no manifest.

```
frontier=21  registry=55  S055rows=1  knowledge=50  citeS055=1
harness  -> FAIL F21 knowledge/junk-csaf-vex-product-status.md ids=S055 exit=- problems=selection-not-cited-by-entry,manifest-unreadable
            entries=24 pass=23 exit=1
binding  -> records=44 bound=44 unbound=0 exit=0        (unchanged: it walks manifests, not registry rows)
audit    -> lines=50 total=50 pass=49 fail-closed=25 ... expect=present expected=49 missing=0 unexpected=1 exit=1
census   -> file E07 S055 status=watch ; exit=1
```

| counter | frozen target | junk (no capture) | met? |
|---|---|---|---|
| frontier rows | 21 | 21 | **yes** |
| registry rows / S055 | 55 / NF=13 | 55 / 1 | **yes** |
| entry citing S055 | 1 | 1 | **yes** |
| knowledge files | 50 | 50 | **yes** |
| harness | entries=24 pass=24 exit=0 | 24 / **23** / 1 | no |
| binding | 45/45 | **44**/44 | no |
| audit | expected=50, unexpected=0, exit 0 | expected=**49**, unexpected=**1**, exit 1 | no |
| census | exit 0, no new W/E | **E07** exit 1 | no |

The frozen kill rule rejects this commit on four independent limbs. Two structural facts behind
the numbers: (a) `capture-binding-check.py` counts manifest records, so a registry row alone can
never move 44→45; (b) the audit's committed `knowledge-expected.txt` (49 entries) makes a new
knowledge file an `unexpected` drift until the L1 edits the list.

### 2.1 Extension — the same junk with a 105-byte fabricated capture (2b)

Because the claim's C2 coverage is measured entirely by these instruments, I probed the boundary:
`junk2/` adds (i) a one-line, 105-byte `corpus/source-snapshots/round-38/S055.txt`
(`sha256 80dea24d…9174`) that I wrote myself, (ii) a schema-valid `manifest.json` whose single
record binds that file to the S055 URL with a strict `fetched_utc` and a quote taken from my own
line, (iii) the entry's recheck line prefixed `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`,
(iv) the entry appended to `knowledge-expected.txt`, (v) the row status `watch`→`mined`.

```
harness  -> PASS F21 ... ids=S055 ; entries=24 pass=24 exit=0
source-recheck --manifest junk2/…/round-38/manifest.json --source S055 -> S055:sha256 OK ; S055:Q1 OK occurrences=1 anchor=1-ok ; exit=0
binding  -> records=45 bound=45 unbound=0 exit=0
audit    -> lines=50 total=50 pass=50 ... expect=present expected=50 missing=0 unexpected=0 exit=0
census   -> W04 S028, W04 S029, ok ; exit=0
frontier=21 registry=55 knowledge=50 citeS055=1
```

**Every frozen C2 counting target is met by a capture I fabricated in one line.** This is not a
failure of the L1's work (the real capture is being fetched independently), it is a statement
about what the counters prove: `capture-binding-check.py` binds id ↔ URL-text ↔ file name and a
strict timestamp, never the bytes to the documented URL; `source-recheck.py` pins quotes against
*whatever capture the manifest names*; the registry row's `capture … (sha256 …)` pin (the shape
S051–S054 rows use) is read by no instrument. The only frozen limb that can reject fabricated
*content* is the junk twin (4 statements rejected against the independently fetched page). The
C2 after-state must therefore be reported as "surface admitted + capture fetched", not as
"capture authenticated by the counters", and the fetch transcript has to ride in the receipt.

---

## 3. Control 3 — C1 cheapest skip

Fixture built on the TIP export (the realistic pre-J parent), three scratch git repos with
verified toplevels:

* `repoA` — the literal cheapest skip: one commit = TIP + `Correction (round 38)` lines in
  `PROVINCE.md` (`… L79-L152 … misplaced …`) and `corpus/README.md` (`… L399-L454 … misplaced …`)
  + `.ufo/waves/round-38/final-gates/all-gates.txt` containing only the "right header"
  (`all-gates v2`, `export-ref=<parent>`, `suite-sha256=<64 hex>`, `run-utc=…`) and a
  `closed=8/8 exit=0` line. `REF=S1`.
* `repoB` — split into `J2` (corrections) + `Y2` (receipt naming `J2`); `diff J2..Y2` =
  `.ufo/waves/round-38/final-gates/all-gates.txt` only.
* `repoC` — `J3` (corrections + the two judged-head prose lines) + `Y5` (forged receipt carrying
  **the real suite digest** `85d33ea9…` and 8 forged `G<n> payload=… closed=1` lines + 8
  `selftest case=G<n>` lines + `closed=8/8 exit=0` + `selftest cases=8 failures=0`).

### 3.1 The literal cheapest skip, scored by the landed suite

```
$ bash SUITE --export-ref S1 --lane $S/repoA --work $S/suitework-A
G1 ... province-correction=1,readme-correction=1,province-fence=closed,readme-fence=open,declared-blocks=0 closed=0
G2 ... receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=0,digest-match=0,run-lines=0,closed-line=1,selftest-lines=0,selftest-summary=0,scorecard-ref=0,shonen-ref=0,head-token-lines=0 closed=0
G3 ... resolutions-section=0,line-tokens=0,added-pending=0,added-placeholders=0,diff-read=fail closed=0
G4 ... dispatches=1,pairs=0,seats-ok=0,read=ok closed=0
G5 ... round38-section=0,final-lane-commit-lines=0,correction=0,f3246559=1,anchor-ancestor=1 closed=0
G6 ... r36=absent,r37=absent,r38=present,work=outside,tolerated=none,read=ok closed=0
G7 ... filled-section=0,correction=0,proposal-rows=0,missing=0 closed=0
G8 ... r37-suite=1,r37-closed=0,r37-exit=1 closed=0
closed=0/8 exit=1
```

Two-step variant (`REF=Y2`, receipt naming `J2`, diff = receipt only):

```
G2 ... receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,digest-match=0,run-lines=0,closed-line=1,selftest-lines=0,selftest-summary=0,scorecard-ref=0,shonen-ref=0 closed=0
closed=0/8 exit=1
```

**Which G-checks still fail, and why** (all eight, in the fixture; the G8 fixture red is an
artifact, see below):

| check | limb that stays red under the cheapest skip |
|---|---|
| G1 | `declared-blocks=0` (file absent) and `readme-fence=open` — the appended Correction line sits *inside* the unclosed fence opened at L426; PROVINCE fences are already closed |
| G2 | at `REF=J` the receipt is absent from the export (`receipt=0`); at `REF=Y` the receipt is present but has 0 run lines, 0 selftest lines and a digest that is not the suite's |
| G3 | `resolutions-section=0`, `line-tokens=0` — no `## Pending-marker resolutions (round 38)` heading/rows |
| G4 | `pairs=0` — `wave1-dispatch.json` has no `wave1-results.json` sibling (73 seats) |
| G5 | `round38-section=0`, `correction=0` — no round-38 SCORECARD section and no `f3246559` + `anchor ancestor` Correction line (the base already carries `f3246559` at `SCORECARD.md:1509` on the r37 `Final lane commit:` line, so that limb is one prose line away) |
| G6 | live limb only: at measurement `/fast/scratch/hyaku/kasegi-r38` holds 17 entries (r36/r37 absent). The landed suite on the same fixture prints `r38=present,work=outside,tolerated=none` (red); a scratch re-implementation of the frozen G6 predicate (`gcheck.py`, written before the suite landed) measured the discrimination: clean root (`kasegi-r38/<work>` only) → `closed=1`, a stray under `kasegi-r36` → `r36-entries=['stray-file']` red, a sibling seat dir under `kasegi-r38` → `r38-other=['CritMotivation']` red |
| G7 | `filled-section=0`, `proposal-rows=0` — ledger section still empty |
| G8 | fixture-only red: the fixture's nested r37 run is lane-bound (E1/E9/E10 ancestry). In the real lane G8 is the one check that is green without any round-38 work *if* HEAD==REF and the tree is clean (F3) |

So the cheapest skip closes **0/8** as committed, and at most G8 (+G6 at a clean moment) — both
of which are carry-over/live properties that the round-38 defect fixes do not touch. C1 is not
reachable by pasting the two correction lines and a receipt header.

### 3.2 The two counterexamples the cheapest skip exposed

**(a) The frozen counting command names the wrong ref.** Claims `C1.counting_commands[0]` says
`bash corpus/instruments/r38-closure.sh --export-ref <J> -> closed=8/8 exit=0`, and
`judged_head_rule` defines J as "the lane commit that carries every round-38 change except that
receipt; the lane tip Y adds only the receipt file". G2 reads the receipt from the **export**
(`receipt=0` at `REF=J3`, measured above). At `REF=J` the receipt is absent, so the first counting
command can never print 8/8; at `REF=Y` G2's `diff-clean` limb is satisfied precisely because
`diff J..Y` is the receipt alone (measured `diff-clean=1` at `REF=Y2`/`Y5`). The r37 precedent is
the same shape: the committed `all-gates.txt` at `9492c77` names `2735e93`, and
`git diff --name-only 2735e93 9492c77` is the receipt alone. The green ref is the **receipt
commit**, and the receipt names its parent. Smallest safe correction: state the counting command
as `--export-ref <Y>` (with the receipt's `export-ref=<J>`), and have the report name J and Y;
otherwise the kill rule ("the judged-head export prints closed != 8/8") kills a correct
implementation.

**(b) G2's receipt is forgeable — the digest is the only binding.** `repoC/Y5` (zero corpus work,
no fence fix, no declared blocks, no resolutions, no results.json, no ledger rows) scores:

```
$ bash SUITE --export-ref Y5 --lane $S/repoC --work $S/suitework-forge2
G1 ... declared-blocks=0,readme-fence=open closed=0
G2 payload=receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,digest-match=1,run-lines=1,closed-line=1,selftest-lines=1,selftest-summary=1,scorecard-ref=1,shonen-ref=1,head-token-lines=0 closed=1
G3..G8 closed=0
closed=1/8 exit=1
```

G2 is green because the suite digest is public once the instrument is committed (I substituted the
landed suite's own sha256) and the two judged-head prose lines are two lines of text. r37's E10
carried a `crossrun=1` limb precisely against this ("for every id but E10 … the recorded line is
compared against the live lines", `r37-closure.sh:687-692`); the r38 G2 contract has no such limb,
so a receipt can attest a run that never happened. The total stays red (the other checks read the
corpus bytes), so this is not a laundering route for the claim — but "digest bound" must not be
presented as "the receipt was produced by the run that verifies it". Smallest safe correction:
restore the cross-run comparison (each `G<n> payload=` in the receipt byte-equal to the live run's
`G<n> payload=` line for n≠2, and the 8 `closed=1` set equal to the live set).

---

## 4. Findings (for the L1's ledger / mistake rows)

| id | axis | finding | smallest safe correction |
|---|---|---|---|
| F1 | depth:verifiability | The first C1 counting command runs at J, but G2 needs the receipt inside the export; measured `receipt=0` at `REF=J3`, `diff-clean=1` only at the receipt commit. The claim as frozen cannot print 8/8 at J. | Count at Y (`--export-ref <Y>`), receipt names J; report both hashes. Mirror the r37 `9492c77`/`2735e93` shape. |
| F2 | depth:verifiability | G2 is forgeable with the public suite digest + two prose lines (measured `G2 closed=1`, total 1/8). The r38 contract dropped r37's E10 `crossrun` limb. | Add the cross-run payload comparison to G2. |
| F3 | depth:verifiability | G8 (nested r37 E9) requires `HEAD==REF` and a clean lane; live base run = 13/14 (`status-dirty=17, head-match=0`). Running the suite at J while Y is committed makes G8 red as well. G6 additionally requires every r38 scratch entry gone but the suite's own work dir. | Run the final gate last: at HEAD==Y, clean porcelain, scratch cleaned; record the live-state payload (E9/G6) in the receipt. |
| F4 | coverage | The whole frozen C2 counter set is reachable with a fabricated 105-byte capture + three edits (harness 24/24, source-recheck exit 0, binding 45/45, audit expected=50 exit 0, census exit 0). Instruments bind shape, not bytes; the registry row's sha256 pin is read by nothing. | Receipt must carry the fetch transcript (HTTP status/bytes/sha256/UTC/UA) and state `S055.txt` sha256 == fetched sha256; bind the registry-row `capture … (sha256 …)` pin to the manifest record (and note the row is prose). Keep the junk twin as the only content guard. |
| F5 | coverage | Do-nothing satisfies exactly one C2 limb — census exit 0 — which BASE already had; the other seven are strict increases. The junk commit (no capture) is rejected by harness/audit/census, so the kill rule's instrument limbs do discriminate. | No action; keep the census limb out of the evidence-of-work list. |

Limits of this seat's evidence: (i) the suite was measured as the wave-1 deliverable
`ExecSuiteBuild.r38-closure.sh` (sha256 `85d33ea9…`); if the L1 lands different bytes the digest
and the G payloads move, and the F1/F2 consequences are structural (they follow from the frozen
G2 text, not from this file's bytes). (ii) Fixture G8 reds are lane-bound artifacts and are
disclosed as such; the real-lane G8 was measured on BASE (13/14 live, 14/14 at freeze per the
before-control). (iii) My own scratch dir is an entry under `kasegi-r38` for the duration of the
wave, so G6 is red until every seat — including this one — is cleaned up.

---

## 5. Cleanup

Scratch `S=/fast/scratch/hyaku/kasegi-r38/CritMotivation/` held every export, fixture, repo,
work dir and transcript above. Removed with `rm -rf -- "$S"` after this receipt was written;
verified at 2026-10-26T18:48:57Z with `[ -d "$S" ]` -> **absent**. Surviving entries under
`/fast/scratch/hyaku/kasegi-r38/` at that check belong to other live seats
(`CritC2Kill ExecSuiteBuild L1 MutC2Entry MutG1G2 MutG3G4 RevSpotCheckReadiness SentSecrets`);
this seat contributes none.
