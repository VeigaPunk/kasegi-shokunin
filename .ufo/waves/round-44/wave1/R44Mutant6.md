# R44Mutant6 — registry-pointer mutant probe

seat: `R44Mutant6` (mutation-tester, leaf) · lane: kasegi round 44 · role: read-only
base revision: `66314015122b9aa32dc40f2f1815df56624c26d1` (HEAD `round-44: freeze claims and validated wave`)
scratch: `/fast/scratch/hyaku/kasegi-r44/R44Mutant6/` (`HYAKU_SCRATCH` unset in the session; the lane default root `/fast/scratch/hyaku` was used, never `/tmp`) — removed on exit, see §8.
no production/shared file was created, modified or deleted by this seat; no git/jj/index mutation, no commit, no pacman, no tool install.

Item: **design a registry-pointer mutant that accepts a nonexistent/wrong registry row.**

## 1. Target surface (what "registry pointer" means here)

`corpus/instruments/frontier-recheck-count.py` (566 lines, sha256 `010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6`) rule G binds every admitted frontier row's source pointer to a `corpus/SOURCES.md` row:

- `read_registry_ids()` (L138–148) returns the id set parsed by `REGISTRY_ROW = re.compile(r"^\|\s*(S\d{3,})\s*\|", re.MULTILINE)` (L106), or `None` when the root has no registry;
- `frontier_census()` (L310–) emits `source-id-absent:<id>` for `bound - registry` (L337–340).

This is the limb that would certify C2's "F26 + its newly opened tier-A registry row all land": the round-44 C2 diff adds F26 → `S069` (`corpus/README.md`, uncommitted) and S069 to `corpus/SOURCES.md`; rule G is what binds that pointer to a row.

## 2. Mutant (one expression, one line)

```
--- pristine/frontier-recheck-count.py
+++ mutant/frontier-recheck-count.py
@@ -145,7 +145,7 @@
     except OSError:
         return None
-    return set(REGISTRY_ROW.findall(text))
+    return set(re.findall(r"S\d{3,}", text))
```

sha256 pristine `010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6` → mutant `ed20d7ade9c18cc71deb340405c5de767ab5e7369d846eeaf1dbb886972e55c6`. The mutant resolves a pointer to *any* `S\d{3,}` token in the registry file instead of to a table row, so an id that exists only in the registry's prose — a staged/mapped id, a rejection note, a superseded id — counts as a registered row.

## 3. Detector fixture (scratch, synthetic)

`fixture/`: `corpus/README.md` F26 `admitted` → `knowledge/phantom.md`, sources cell `S080`; `knowledge/phantom.md` declares `source: S080` + evidence bullet + `recheck: … --source S080`; `corpus/source-snapshots/fixture/manifest.json` record `S080`; stub `corpus/instruments/source-recheck.py` (exit 0); `corpus/SOURCES.md` = one real row `S001` plus two note lines naming `S080`, `S081`, `S082`. `S080` has **no row**.

## 4. Verdict — SURVIVED

| state | command | stdout (decisive lines) | exit |
|---|---|---|---|
| pristine | `python3 pristine/frontier-recheck-count.py --root fixture` | `FRONTIER-CENSUS rows=1 admitted=1 closed=0 problem-rows=1 registry=1` / `FRONTIER-FAIL F26 status=admitted ids=S080 problems=source-id-absent:S080` | **1** |
| mutant | `python3 mutant/frontier-recheck-count.py --root fixture` | `FRONTIER-CENSUS … closed=1 problem-rows=0 registry=4` / `FRONTIER-PASS F26 ids=S080` | **0** |
| restored | `cp pristine → mutant`; rerun | `FRONTIER-FAIL F26 … problems=source-id-absent:S080` | **1** |

The detector's own six selftest cases do not see the mutant:

```
pristine: selftest cases=6 failures=0   exit=0
mutant:   selftest cases=6 failures=0   exit=0
```

Cause, from the code: every selftest fixture (`build_fixture`, L392–429) writes `corpus/README.md`, `knowledge/`, a manifest and a stub, but **never `corpus/SOURCES.md`**; `read_registry_ids` therefore hits the `except OSError: return None` path and the mutated line is unreachable in all six cases. The registry limb has no graded case at all.

### Committed-registry replay (not a synthetic registry)

`fixture-live/` is the same fixture with `corpus/SOURCES.md` = `git show 6631401:corpus/SOURCES.md` (68 rows):

```
pristine: FRONTIER-CENSUS … registry=68 ; FRONTIER-FAIL F26 … problems=source-id-absent:S080 ; exit=1
mutant:   FRONTIER-CENSUS … registry=71 ; FRONTIER-PASS F26 ids=S080                          ; exit=0
```

`S080` appears twice in the **committed** registry (L93, L122, prose only: "staged `S080` → landed `S048`"); it has no row. The mutant therefore accepts, on committed lane bytes, a frontier pointer to a row that was never opened — exactly the C2 hazard ("a newly opened tier-A source row" claimed against a staged-id mention).

### On the live lane the mutant is invisible

`--root .` at probe time: pristine and mutant stdout are byte-identical except the census count (`registry=70` → `registry=73`); both exit 1. (`diff` of the two outputs = one line, the `registry=` token.) No committed gate asserts that token — `grep -rn 'registry=[0-9]' corpus/instruments/*.sh` finds only `r40-closure.sh:1368` (`'registry=0'`, a different instrument's negative). The instrument's digest is recorded in `corpus/instruments/README.md:477` but no committed check recomputes it.

## 5. Cross-detector (bounded escape, not a corpus-wide false accept)

`corpus/instruments/capture-binding-check.py --root fixture-live`:

```
FAIL rule=no-row record=S080 dir=fixture
records=1 bound=0 unbound=1          exit=1
```

Rule B1 (`no-row`) independently rejects the phantom pointer **when a capture record exists for it**. C2 requires a captured source, so on the C2 path the mutant is caught by the sibling gate; it survives the frontier gate alone. The escape is real for any pointer that has no manifest record (e.g. an F-row `sources` cell citing an id whose capture was not landed) and for every pointer whose *content* is wrong (§6).

## 6. Secondary observation — the "wrong row" half is already a pristine gap (no mutation)

Rule G tests **membership only**: it never checks the row's `status` or that the entry's `source:` URL equals the row's URL. With committed registry bytes and a pointer to `S068` (a `rejected` row), the pristine instrument says:

```
FRONTIER-CENSUS … closed=1 problem-rows=0 registry=68 ; FRONTIER-PASS F27 ids=S068 ; exit=0
```

while `capture-binding-check.py` on the same fixture: `FAIL rule=rejected-row-anchor record=S068 row=S068` exit 1. So a frontier/knowledge pointer to a refused or wrong row passes the frontier gate today; only a capture record's presence lets the sibling gate catch it. This is a coverage finding about the frozen predicate, not permission to widen it, and not part of the mutant verdict above.

## 7. Expected kill (what a detector must do to kill this mutant)

One graded case in `frontier-recheck-count.py --selftest` that (a) writes a `corpus/SOURCES.md` with one row, (b) binds a frontier row to an id absent from it, (c) expects `FRONTIER-FAIL … problems=source-id-absent:<id>` and exit 1. The mutant then fails that case (it would print `FRONTIER-PASS`). Optional second case: pointer to a `rejected` row, and (if the lane wants URL agreement) an entry `source:` URL differing from the row's URL — both currently pass pristine.

## 8. Restoration + cleanup evidence

- restored bytes: `sha256sum pristine/… mutant/…` → both `010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6`; rerun on `fixture` → `source-id-absent:S080`, exit 1.
- scratch removed on exit: `rm -rf /fast/scratch/hyaku/kasegi-r44/R44Mutant6` → `removed`; `ls -d /fast/scratch/hyaku/kasegi-r44/R44Mutant6` → `No such file or directory` (no failure to report).
- `S080` in committed `corpus/SOURCES.md` at L93 and L122 (verified with `git show 6631401:corpus/SOURCES.md | grep -n S080`).

## 9. Limitations

- Synthetic fixture + stub `source-recheck.py`: the probe isolates rule G; it does not execute a real recheck.
- The lane working tree was **moving** during the probe: at the first read `corpus/SOURCES.md` was 68 rows, later 70 rows (uncommitted S069/S070), `corpus/README.md` +19 (F26), one new untracked knowledge entry, and the in-flight F26 entry fails its recheck limb (`recheck-exit-127`) — another seat's uncommitted work, not this seat's. All mutant evidence is pinned to `6631401` bytes (instrument from `git show HEAD:`, registry from `git show HEAD:`), so it does not depend on that drift.
- The mutant is a designed defect, not a lane change; nothing was written outside scratch and this report.
- Verdict scope: **SURVIVED** for `frontier-recheck-count.py` (no selftest case, no lane-visible delta, no executable digest pin); **KILLED** only by `capture-binding-check.py` rule B1 and only when a manifest record exists for the phantom id. Not a claim about C2's truth — C2's "registry row lands" limb rests on this ungraded predicate.
