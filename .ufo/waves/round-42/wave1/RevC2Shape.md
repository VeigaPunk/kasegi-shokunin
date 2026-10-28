# RevC2Shape — do the C2 counting commands discriminate? (receipt-only)

Seat: RevC2Shape-2 (reviewer, leaf). Axes judged: depth:verifiability, coverage. Frozen claims read first: `.ufo/waves/round-42/claims.json` (C2 counting_commands, nine of them; kill_rule enumerates the after-state elements). Nothing in the lane or fleet was written; no mutating git/jj; no tool installed.

## Verdict (one paragraph)
All nine frozen C2 counting commands print the before-values at base and every one of the ten after-values is reachable (shown on a synthetic after-state fixture A). Each of the three required single-value mutations is distinguished by at least one frozen command: **fake F25 row without entry** → harness (`entries=28 pass=27`, `FAIL F25 … problems=missing-entry`; the F25-row grep alone is FOOLED, it prints 25); **fake S064 row `mined` without capture** → harness (`recheck-exit-2`; the registry-row, S064-mined, entry, knowledge, binding, audit and census commands are all fooled when the entry+manifest exist); **entry without the provenance trio** → distinguished for `source:` (harness `no-source-line`) and `recheck:` (harness `no-recheck-line`) but **NOT for `verified-at:`** — a missing `verified-at:` line passes all nine frozen commands. Two further after-state elements named in the claim have no frozen counting command at all (details in "Gaps" with a one-line supplementary command each, verified to discriminate).

## Method
Base tree: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 5053a7f46de35784cff4b56756906e9014a38276 | tar -x` into `S=/fast/scratch/hyaku/kasegi-r42/RevC2Shape/base` (read-only git use). The nine counting commands, run from the copy root, via `counts.sh <copy>` (unchanged claim commands; only the three census/harness invocations are pointed at the copy: `frontier-recheck-count.py` and `capture-binding-check.py` default to their own lane root; `recheck-audit.py --quiet --cdroot <copy>`; `sources-census.sh validate --file <copy>/corpus/SOURCES.md` instead of `--root fleet kasegi`, because the census can only see the real lane by lane id). Entry `recheck:` lines in the copy are relocated (`cd <real lane>` → `cd <copy>`) so rechecks execute against the copy — otherwise `recheck-audit` cdroot limb fails 59/61 and the rechecks would run against the real lane.

After-state fixture A is SYNTHETIC (stand-in 4-line capture at `corpus/source-snapshots/round-42/S064.txt`, manifest record with sha256 + one quote, F25 row after F24, `[r42 Frontier amendment]` line appended to PROVINCE.md, S064 row `mined` after S063, entry `corpus/knowledge/osv-fixture.md` with `source:`/`verified-at:`/`recheck:`/`ground: F25`, knowledge-expected.txt line). It is not a real fetch and says nothing about the real F25/S064 content; its purpose is to prove which command moves on which defect. Each mutant = A with ONE element withheld/corrupted (`build.py <dest> A-<defect>`), or base plus one element (`base+f25row`, `base+s064row`).

counts.sh (verbatim commands):
```
k1 grep -cE '^\| F[0-9]+ \|' corpus/README.md
k2 grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
k3 awk -F'|' '/^\|[[:space:]]*S064[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if(s=="mined") n++} END{print n+0}' corpus/SOURCES.md
k4 grep -rlE '^source: S064' corpus/knowledge | wc -l
k5 ls corpus/knowledge/*.md | wc -l
k6 python3 corpus/instruments/frontier-recheck-count.py            (+ count of `PASS +F25` lines)
k7 python3 corpus/instruments/capture-binding-check.py
k8 python3 corpus/instruments/recheck-audit.py --quiet --cdroot <copy>
k9 bash scripts/sources-census.sh validate --file <copy>/corpus/SOURCES.md
```

## Base values (all nine print the before-values; match c2-controls/before.txt)
```
k1 frontier rows        : 24
k2 registry rows        : 63
k3 S064 mined rows      : 0
k4 entries citing S064  : 0
k5 knowledge files      : 60
k6 harness              : entries=27 pass=27 exit=0 | PASS-F25 lines=0
k7 binding              : records=55 bound=55 unbound=0 exit=0
k8 audit                : expect=present expected=60 missing=0 unexpected=0 exit=0
k9 census(validate)     : exit=0 codes=      2 W04 
```
census at base prints W04 ×2 (pre-existing, same in A: no new W/E code). before.txt: frontier 24, registry 63, S064+ 0, knowledge 60, harness 27/27, binding 55/55/0, audit expected=60 — all identical.

## After-target fixture A (every after-value reachable)
```
k1 frontier rows        : 25
k2 registry rows        : 64
k3 S064 mined rows      : 1
k4 entries citing S064  : 1
k5 knowledge files      : 61
k6 harness              : entries=28 pass=28 exit=0 | PASS-F25 lines=1
k7 binding              : records=56 bound=56 unbound=0 exit=0
k8 audit                : expect=present expected=61 missing=0 unexpected=0 exit=0
k9 census(validate)     : exit=0 codes=      2 W04 
```

## Mutation matrix — which commands move off the after-target
Format: mutant / frozen-9 commands whose output differs from A / supplementary commands (X1-X3, my proposals) / evidence lines. "NOTHING" = the defect is invisible to that set.
```
BASE  0/0/0 9 (r42: 0) 24
A     0/0/0 10 (r42: 1) 25
### A-f25row
  frozen-9 detect: F-rows, harness | supplementary: X3 F-admitted
   harness: entries=27 pass=27  | PASS-F25 lines=0
   X3 F-admitted: 24
### A-entry
  frozen-9 detect: entries-S064, knowledge, harness, audit, census | supplementary: -
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=- exit=- problems=missing-entry
   audit: expect=present expected=61 missing=1 unexpected=0
   census: exit=1 codes=      1 E11       2 W04
### A-capture
  frozen-9 detect: harness | supplementary: -
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=S064 exit=2 problems=recheck-exit-2
### A-manifest
  frozen-9 detect: harness, binding | supplementary: -
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=S064 exit=- problems=manifest-unreadable
   binding: records=55 bound=55 unbound=0 exit=1 || FAIL rule=missing-manifest dir=round-42
### A-no-source
  frozen-9 detect: entries-S064, harness | supplementary: X1 lacking-trio(src/ver/rech)
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=- exit=- problems=no-source-line
   X1 lacking-trio(src/ver/rech): 1/0/0
### A-no-verified
  frozen-9 detect: NOTHING | supplementary: X1 lacking-trio(src/ver/rech)
   X1 lacking-trio(src/ver/rech): 0/1/0
### A-no-recheck
  frozen-9 detect: harness | supplementary: X1 lacking-trio(src/ver/rech)
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=S064 exit=- problems=no-recheck-line,no-source-selection,no-manifest
   X1 lacking-trio(src/ver/rech): 0/0/1
### A-expected
  frozen-9 detect: audit | supplementary: -
   audit: expect=present expected=60 missing=0 unexpected=1
### A-province
  frozen-9 detect: NOTHING | supplementary: X2 PROVINCE-amend
   X2 PROVINCE-amend: 9 (r42: 0)
### A-s064row
  frozen-9 detect: reg-rows, S064-mined, binding | supplementary: -
   binding: records=56 bound=55 unbound=1 exit=1 || FAIL rule=no-row record=S064 dir=round-42
### A-capture-drift
  frozen-9 detect: harness | supplementary: -
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=S064 exit=1 problems=recheck-exit-1
### A-status-queued
  frozen-9 detect: S064-mined | supplementary: -
### A-f25-status
  frozen-9 detect: harness | supplementary: X3 F-admitted
   harness: entries=27 pass=27  | PASS-F25 lines=0
   X3 F-admitted: 24
### A-f25-wrongsrc
  frozen-9 detect: NOTHING | supplementary: -
### base+f25row
  frozen-9 detect: reg-rows, S064-mined, entries-S064, knowledge, harness, binding, audit | supplementary: X2 PROVINCE-amend
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=- exit=- problems=missing-entry
   binding: records=55 bound=55 unbound=0 exit=0
   audit: expect=present expected=60 missing=0 unexpected=0
   X2 PROVINCE-amend: 9 (r42: 0)
### base+s064row
  frozen-9 detect: F-rows, entries-S064, knowledge, harness, binding, audit, census | supplementary: X2 PROVINCE-amend, X3 F-admitted
   harness: entries=27 pass=27  | PASS-F25 lines=0
   binding: records=55 bound=55 unbound=0 exit=0
   audit: expect=present expected=60 missing=0 unexpected=0
   census: exit=1 codes=      1 E11       2 W04
   X2 PROVINCE-amend: 9 (r42: 0)
   X3 F-admitted: 24
### base+f25row+s064row
  frozen-9 detect: entries-S064, knowledge, harness, binding, audit, census | supplementary: X2 PROVINCE-amend
   harness: entries=28 pass=27  | PASS-F25 lines=0 || FAIL F25 knowledge/osv-fixture.md ids=- exit=- problems=missing-entry
   binding: records=55 bound=55 unbound=0 exit=0
   audit: expect=present expected=60 missing=0 unexpected=0
   census: exit=1 codes=      1 E11       2 W04
   X2 PROVINCE-amend: 9 (r42: 0)
```

Supplementary commands (run in the same loop; X1/X2/X3 base→A values shown at the top of the matrix: `0/0/0 → 0/0/0`, `9 (r42: 0) → 10 (r42: 1)`, `24 → 25`):
- X1 `for k in source: verified-at: recheck:; do grep -L "^$k" corpus/knowledge/*.md | wc -l; done` → 0/0/0 at base and A; 1 in the matching field per defect (A-no-source `1/0/0`, A-no-verified `0/1/0`, A-no-recheck `0/0/1`).
- X2 `grep -c '^\[r42 Frontier amendment' PROVINCE.md` → 0 → 1 (A-province prints 0).
- X3 `awk -F'|' '/^\| F[0-9]+ \|/{s=$4;gsub(/[[:space:]]/,"",s);if(s=="admitted")n++}END{print n+0}' corpus/README.md` → 24 → 25 (A-f25-status prints 24 where k1 still prints 25).
- X4 (F25 sources cell): `awk -F'|' '/^\| F25 \|/{s=$6;gsub(/[[:space:]]/,"",s);print s}' corpus/README.md` → `S064` on A, `S063` on A-f25-wrongsrc (verified; base F24 prints `S063`, so the column-6 selector is the sources cell).

## Per-required-mutation answer
1. **Fake F25 row without entry.** Variant `base+f25row` (and `A-entry`). Frozen commands that move: harness `entries=28 pass=27 exit=1`, `FAIL F25 … problems=missing-entry`, no `PASS F25`; also k4/k5 (entry count 0/60), k8 (`A-entry`: `missing=1`) and k9 (`A-entry`: census E11 used-by path missing). The row-count grep k1 prints 25 = the after-value → it is fooled by this mutant alone; k2/k3/k4/k5/k7 stay at base values too. Distinguisher: harness.
2. **Fake S064 row (`mined`) without capture.** Variant `A-capture` (row + manifest record + entry present, capture file deleted): ONLY the harness moves (`FAIL F25 … ids=S064 exit=2 problems=recheck-exit-2`). k2,k3,k4,k5 print after-values; k7 binding still `records=56 bound=56 unbound=0` (binding checks record↔registry row, never the capture bytes); k8 audit still `expected=61 missing=0` (the line runs and fails closed, not counted); k9 census 0 (E11 checks only `used-by` paths). Variant `base+s064row` (row only): k3=1 and k2=64 are fooled (these are the after-values) while k4 (0), k5 (60), k7 (55/55), k8 (60), k9 (E11, exit 1) and the harness (27/27, no PASS F25) move. Distinguisher: harness (capture-absent and capture-drift both only the harness: `A-capture-drift` → `recheck-exit-1`).
3. **Entry without the provenance trio.** `A-no-source` → harness `no-source-line` (k4 also 0); `A-no-recheck` → harness `no-recheck-line,no-source-selection,no-manifest`; **`A-no-verified` → NOTHING in the nine frozen commands** (all of k1-k9 equal A; `verified-at:` is not read by any instrument — `grep -rn verified-at corpus/instruments/*.py` prints no match; only a fixture dir mentions it). Only supplementary X1 detects it (`0/1/0`).

## Gaps (claim-vs-counter drift) for the L1 / C2 executors
G1. **`verified-at:` is uncounted.** The kill_rule says the kill fires when "the entry … lack[s] the provenance trio", but no counting command checks `verified-at:` (nor, strictly, that the three lines exist: harness covers source and recheck only). Add X1 to the receipt commands or the kill clause cannot be evidenced by the nine.
G2. **PROVINCE F25 amendment is uncounted.** The predicate requires "an appended F25 amendment in PROVINCE.md"; `A-province` (amendment absent) passes all nine. Add X2 (`^\[r42 Frontier amendment` → 0→1, grep -c `^\[r[0-9]* Frontier amendment` 9→10 at base).
G3. **F25 `status = admitted` is not counted** (k1 counts rows regardless of status; kill_rule names "status cell not `admitted`"). `A-f25-status` (row status `queued`) is caught only because the harness skips non-admitted rows (`entries=27`, no PASS F25); k1 still prints 25. Add X3.
G4. **F25 row's sources cell can disagree with the entry/registry.** `A-f25-wrongsrc` (row cites S063, entry and registry say S064) passes everything — no instrument cross-checks README row sources against the entry header. Add X4 (S064 on A, S063 on the mutant) if the L1 wants the row bound to S064.
G5. **Capture-absence/drift is detected only by the harness's embedded recheck line** (k7 binding and k8 audit pass). The harness count (`entries=28 pass=28`, `PASS F25`) is therefore the single load-bearing C2 command for the O4 junk-twin class; the recheck line must name `--manifest corpus/source-snapshots/round-42/manifest.json --source S064` and the harness cd target must be the real lane. A direct `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-42/manifest.json --source S064` (exit 0, printed `S064:sha256 OK` + quotes) in the receipt would make that second detector independent of the harness.
G6. `knowledge-expected.txt` omitted is caught only by k8 (`unexpected=1`, `expected=60`) — keep k8 in the receipt; it is the only counter of that class.
G7. Census k9 reports `exit 0` with W04×2 at base and in A; the criterion "no new W/E code" needs the code list (not just the exit code) printed: `bash scripts/sources-census.sh validate … | grep -oE '[WE][0-9]{2}' | sort | uniq -c` → `2 W04` at base.

## Limits of this check (honest)
- Fixture content is synthetic; the real F25/S064 capture, quotes and entry were not examined (items not yet landed at time of review; the working tree HEAD 0566bd6 carries only wave scaffolding over the base).
- census was run with `--file <copy>/SOURCES.md`; the frozen command uses `--root <fleet> kasegi` (real lane) and was not run against the fixture. E11 appeared because the fixture row's used-by path was absent in `base+s064row`; it is the census's used-by check, not a capture check.
- Mutant set covers single-element defects only; combined defects were not exhaustively enumerated (`base+f25row+s064row` shown).
- No measure (45/45 = 1.000) command was exercised: it is not in the nine counting commands and its tool is not named in the C2 claim.

## Artifacts
Scratch (`/fast/scratch/hyaku/kasegi-r42/RevC2Shape`: base copy, build.py, counts.sh, reloc.sh, per-variant outputs) removed before yield; the matrix above is the retained record. Disk guard was green (`/fast/scratch/hyaku` 27% used) before the run.
