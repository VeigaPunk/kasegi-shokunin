# AttackI1 — kill-rule recheck against the final state (round 26, wave 2)

Seat: `L1Kasegi26.AttackI1` (read-only leaf). Date: 2026-10-25 UTC.
Attacked: the frozen kill rules (`.ufo/waves/round-26/claims.json`, frozen 2026-10-25T12:27:41Z)
re-evaluated against the **final** landed state — C1 (all four counters green after regeneration)
and C2 (census exit 0; every new row cited; precise counter ≥1).
Falsification target: any failure mode that would fire a kill rule now.

## 1. Kill rules as frozen (claims.json)

- **C1 kill rule** (depth:verifiability): *"any counter misses its after value, or the
  do-nothing control hits any after value."* Four counters: (a) SKILL.md `gate|probe`
  registry row ≥1; (b) selftest receipt line in `c1-receipt-index.txt` =1; (c) restated
  fix-control #3 excluding the retained historical line =0; (d) deletion fixture exits 1
  naming the deleted entry (before: exit 0).
- **C2 kill rule** (coverage): *"a source row is appended without an admitted entry citing
  it; or census exit != 0 at round end."* (Two limbs only; no do-nothing limb. Counter
  after values: frontier admitted 11; entries citing a row first registered this round ≥1.)
- C1 do-nothing control: unchanged committed bytes → deletion exit 0, registry row 0,
  selftest lines 0, fix-control hits 1 (recorded `c1-controls/m1-e.txt`: 37/37 exit 0).

## 2. Final-state measurements (all run fresh this seat, 2026-10-25 UTC)

| Check | Command (exact) | Result | After value |
|---|---|---|---|
| C1(a) | `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` | **1** (row SKILL.md:981: recheck-audit.py, verdict map `0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate`, `--selftest`, pinned-value path `c1-receipt-index.txt`, write scope, owner) | ≥1 ✓ |
| C1(b) | `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` | **1**; index pins `instrument_sha256=3fc0d751…`, `selftest cases=15 failures=0 exit=0`; `sha256sum corpus/instruments/recheck-audit.py` = **3fc0d751…** (match — regeneration at landed digest closed M26-1) | 1 ✓ |
| C1(c) | `grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l` | **0**; proper ERE `grep -rnE '62 assertions|77 assertions' …` prints only the single retained historical `round-24.md:77` (excluded by the pipeline — M26-6 satisfied) | 0 ✓ |
| C1(d) | `python3 corpus/instruments/recheck-audit.py --root <scratch-with-one-entry-deleted> --cdroot <lane-root>` (fresh /tmp scratch: corpus/knowledge + knowledge-expected.txt, deleted `multiparty-vulnerability-coordination.md`) | **exit 1**, prints `missing=corpus/knowledge/multiparty-vulnerability-coordination.md`, tail `expect=present expected=39 missing=1 unexpected=0 exit=1` | exit 1 naming deleted entry ✓ |
| C1 do-nothing | pre-change bytes control `c1-controls/m1-e.txt` | 37/37 exit 0; no after value reachable | control not hit ✓ |
| C2 frontier | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | **11** (F11 row admitted; entry cells name the actual unsuffixed filenames) | 11 ✓ |
| C2 entries-citing (frozen grep) | `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l` | **3** — S040 F10 entry + two S041 F11 entries (**overmatch**, M26-4; before value is 1, not 0) | ≥1 ✓ (but vacuous, see §4) |
| C2 precise counter | `grep -l '^source: S041 ' corpus/knowledge/*.md | wc -l` | **2** — `iso-29147-and-30111-division-of-labour.md`, `iso-29147-divergence-and-clause-crosswalk.md` | ≥1 ✓ |
| C2 every new row cited | S041 `used-by` cell = both F11 entries (SOURCES.md:47); no other row first registered this round | **no orphan** | ✓ |
| C2 census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **exit 0** (only pre-existing W04 warnings S028/S029; no E09) | 0 ✓ |
| C2 recheck-cell form | S040/S041 `recheck:` cells (SOURCES.md:46-47, raw) | exactly `180d` cadence-only; final-URL/UA prose moved to `## Registry changes` (M26-5 closed) | E09-free ✓ |
| C2 frontier harness | `python3 corpus/instruments/frontier-recheck-count.py` | **exit 0, entries=14 pass=14**; both F11 rows `ids=S041`, entry names actual (M26-3 closed) | ✓ |
| Instrument selftest | `python3 corpus/instruments/recheck-audit.py --selftest` | zero FAIL lines; receipt pins 15 cases / 0 failures | ✓ |

## 3. Failure mode → kill rule that would fire

| Known failure mode | Kill rule that would fire | Why | Fires now? |
|---|---|---|---|
| **Deletion pass** (entry-file deletion shrinks the audited set while passing — lane-declared debt) | **C1** — counter (d) misses its after value | (d)'s after is "exit 1 naming the deleted entry"; a deletion pass (exit 0, set shrinks) would miss it → "any counter misses its after value" fires. The landed `--expect` expected-list equality (committed `knowledge-expected.txt`, 39 entries) is what closes this: missing → `missing=<name>` + exit 1; extra → `unexpected` + exit 1; absent `--expect` → prior glob-only behavior. Verified fresh: exit 1 naming `multiparty-vulnerability-coordination.md`. | **No** |
| **Census E09** (S040/S041 recheck cells carrying prose "180d — <prose>" break the census grammar) | **C2** — limb "census exit ≠ 0 at round end" | E09 on either cell made the census exit 1 at compose (recorded round-26 lesson M26-5, §Gate). Smallest safe correction applied: cells restored to bare `180d`, prose recorded under `## Registry changes`. Census now exits 0. | **No** (was firing at compose; closed) |
| **Orphan row** (a source row appended without an admitted entry citing it) | **C2** — limb "a source row is appended without an admitted entry citing it" | Fires directly by construction. This round's only newly appended row is S041 (staged S076/S064 renumbered by document into S041; staged S068 already lane S040, not appended). S041 is cited by **both** admitted F11 entries (precise counter = 2). | **No** |
| **Counter overmatch** (frozen C2 grep matches S040's round-25 entry, so the before value is 1 not 0 and an empty shell satisfies ≥1) | **No kill rule fires** — this is a counter-discrimination defect, not a kill-rule trigger | C2's kill rule has exactly two limbs (orphan row; census exit ≠ 0); neither references the counter's power. Overmatch (M26-4) is a false-positive hazard: the C2 do-nothing control ("no adoption") would still report ≥1 because of S040, and the frozen counters (awk 11, grep ≥1, census, frontier harness) are all satisfied by empty shells. The round therefore records it and treats the **precise** S041 counter (2) plus the two entries' Q1–Q9 conformance and manifest-pinned quotes (`source-recheck.py --source S041` exit 0) as the substantive gate. This is the one residual verifiability caveat, documented, not hidden; it does not fire a kill rule. | **No** (documented caveat) |

## 4. Verdict

**No kill rule fires in the final state.** C1: all four counters green (a=1, b=1 with
receipt regenerated at the landed digest 3fc0d751…, c=0 with the exclusion load-bearing,
d=exit 1 naming the deleted entry), and the do-nothing control (pre-change bytes) stays
37/37 exit 0 without reaching any after value. C2: frontier 11, every newly appended row
(S041, the only one) cited by admitted entries (precise counter 2), census exit 0 — both
kill-rule limbs satisfied. The C1/C2 kill rules as frozen are satisfied; the failure-mode
matrix above maps each known failure to the exact rule that would fire and confirms none
fires now.

## 5. Evidence trail (files read / runs)

- Reads: claims.json (frozen), SCORECARD.md, QUALITY.md, corpus/README.md (F11 row),
  SOURCES.md (S040/S041 rows + Registry changes), lessons/round-26.md, recheck-audit.py,
  knowledge-expected.txt (39), c1-receipt-index.txt, c1-instrument-digest.txt, c1-live.json
  (expect=present 39/39), c1-controls/m1-e.txt (do-nothing), c1-controls/m1-d.txt
  (pre-expected-list deletion control), source-snapshots/round-26/manifest.json,
  both iso-29147 knowledge entries.
- Runs (read-only, lane root; cwd = lane root): the exact counter commands in §2, plus
  `sha256sum corpus/instruments/recheck-audit.py` (3fc0d751…), proper-ERE content check,
  frontier harness, census validate, fresh /tmp deletion fixture, `--selftest`.
- Nothing installed (no tool installs recorded; no VCS mutation; no writes outside
  `.ufo/waves/round-26/wave2/`).
- Honesty notes: the scratch deletion fixture produces limb noise (paths/instrument fail
  because snapshot paths resolve against the scratch root, not the lane root); the deletion
  verdict (`missing=<name>`, exit 1) is independent of that noise. The frozen fix-control #3
  command's `\|` is a literal pipe under `-E`; the 0 is meaningful only via the exclusion
  pipeline — verified by the proper-ERE content check showing the single retained historical
  line. The "precise counter ≥1" is measured as the S041-citing count (2), not the frozen
  overmatching S04x grep (3).
