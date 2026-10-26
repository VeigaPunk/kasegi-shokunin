# ConnPatterns — round 40 falsify wave 2 (cross-claim pattern finding)

Seat: ConnPatterns (leaf; no subagents). Scope: read the C1 suite (`corpus/instruments/r40-closure.sh`, H1-H10) and the C2 decisions (lesson Gate blocks, registry rows, knowledge entries, manifest), identify shared assumptions and interactions that could hide a defect, scan for pattern reuse (status-change logging, quote discipline) that could be folded into QUALITY/suite. No lane edits; only this receipt. All runs used fixture clones of the lane (toplevel verified = fixture before each commit); the real lane was only read (`git show/archive/ls-tree/rev-parse` + read-only instrument runs). No tool installs needed (bash/python3/git only).
Fixture Y = J + receipt only (clone of lane HEAD 3074c767…; committed `all-gates.txt` at `.ufo/waves/round-40/final-gates/all-gates.txt`; `git diff --name-only J Y` = that one path).
## 1. Reproduced counts at the verification ref (green evidence)

Fixture Y = J + receipt only (clone of lane HEAD 3074c767…; committed `all-gates.txt` at `corpus`… `.ufo/waves/round-40/final-gates/all-gates.txt`; `git diff --name-only J Y` = that one path).

| Item | Command (run at fixture Y) | Result |
|---|---|---|
| C1 suite | `bash corpus/instruments/r40-closure.sh --export-ref <Y> --lane <fixture> --work … --scratch-root <empty>` | `closed=10/10 exit=0`; transcript byte-identical to the committed all-gates (same header, `run-utc=2026-10-26T21:56:22Z` = ref committer instant, H1-H10 payloads) |
| C1 selftest | `bash … --selftest --export-ref <Y> …` | `selftest cases=10 failures=0`, one graded `case=H<n> positive=pass` line per check, 7 forged-report judge lines rejected, exit=0 |
| C1 negative controls | H8 in the same run | base a7af2ce… = 3/10 exit=1; r39 judged head 8371e7a… = 2/10 exit=1 |
| C1 plain-run refusal | `bash … ` (no flags) | exit=2 |
| C2 queued | `awk -F'|' …` count queued among the nine | 0 |
| C2 mined | same counter | 7 (`S016 S017 S019 S020 S021 S023 S025`) |
| C2 entries citing nine | `grep -rlE '^source: S0(16|17|19|20|21|22|23|24|25)' corpus/knowledge | wc -l` | 7 |
| C2 S060+ rows / entries | `grep -cE '^\|[[:space:]]*S06[0-9][[:space:]]*\|' corpus/SOURCES.md`; `grep -rlE '^source: S06[0-9]' corpus/knowledge | wc -l` | 3 rows (S060/S061/S062); 1 entry |
| C2 frontier | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 23 |
| C2 harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=26 pass=26 exit=0` |
| C2 census | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `W04 S028`, `W04 S029`, `ok`, exit=0 (same two pre-existing warnings as census-before) |
| C2 source-recheck | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S0NN` per mined row | all 8 rows: `sha256 OK` + every pinned quote `OK` with `occurrences=… anchor=N-ok`, exit=0 each |
| C2 capture binding | `python3 corpus/instruments/capture-binding-check.py --root .` | `records=54 bound=54 unbound=0`, exit=0 |
| Junk control | flipped all nine status cells to `rejected` (fixture clone) | queued=0 (passes), mined=0 (fails the ≥4 counter) → rejected as designed |

## 2. Cross-claim interactions that could hide a defect

### F1. H6's family scan is blind to the per-seat leftover layout it claims to police (live gap)
`check_h6` finds only **depth-1** entries of the scratch root (`find "$realroot" -mindepth 1 -maxdepth 1`), matches `kasegi-r39*|kasegi-r40*`, tolerates the one family dir containing `--work`, and counts anything else. The seat protocol puts every seat's scratch at `/fast/scratch/hyaku/kasegi-r40/<SEATNAME>/` — depth 2, **inside** the tolerated family dir. Demonstrated: scratch root with `kasegi-r40/LeftoverSeat/` (a leftover sibling that does not contain `--work`) + `--work` in `kasegi-r40/MyWork` → `H6 payload=strays=0,read=ok closed=1`, full `closed=10/10`. So the claim kill rule "any leftover kasegi-r39*/r40 scratch entry at filing other than the passed --work dir" is **not enforced** for the exact layout the round produces; a seat that leaves its scratch dir at yield sails through H6. (The 30 live wave-2 seat dirs under `/fast/scratch/hyaku/kasegi-r40/` were likewise invisible to a run with `--scratch-root /fast/scratch/hyaku` and `--work` inside the family dir: strays=0.) `@` the harness's separate live check still catches survivors; it is H6-as-claim-gate that is blind. Suggested fix: scan one level deeper (`-maxdepth 2`, matching `kasegi-r39*/kasegi-r40*` entries below the family dir) and tolerate only the subtree containing `--work`; the wave-1 fixture matrix (ExecH6ScratchFixtures) only exercises top-level entries, so this case was untested.

### F2. H2 anchors to fixed strings, not to the record it corroborates (latent, M39-2 shape)
`h2_scan` greps for lines starting `Correction (round 40)` containing both literal `closed=7/8` and `failures=1`. It never reads the round-39 final receipt (`.ufo/waves/round-39/final-gates/all-gates.txt` at 8371e7a…, v5, which is in the same tree). Demonstrated: in a fixture, rewrote the committed r39 receipt `closed=7/8 exit=1` → `closed=6/8 exit=1` and `selftest failures=1` → `failures=2`; H2 payload immutable (`corrections=8,named=5,missing=0,fences=closed closed=1`). The suite is still safe-by-construction on the *receipt* side (H7 went red via `diff-clean=0`), but the correction values are believed by echo, not by derivation — the exact failure shape M39-2 documented (records asserting values the receipt contradicts). The current record is true (7/8/1), so this is latent. Suggested fix: derive the expected strings from the committed r39 receipt inside the export (it is a tracked path) instead of constants.

### F3. H3 checks mention, not substance
`check_h3` counts mentions/rows of `M39-2` in `corpus/QUALITY.md`. Demonstrated: replaced the R37 criterion row's operative sentence ("A record whose stated head or tally contradicts the committed receipt …") with its opposite; H3 identical green (`mentions=1,rows=1 closed=1`). Same class as F2: a criterion row that stops meaning what it says still satisfies the gate. Latent (row is currently sound).

### F4. C2's frozen counting set is grep-level and omits the committed instruments
The C2 counting commands count status cells and grep files; the deep checks (source-recheck per-row, capture-binding, quote anchors) are committed instruments but are **not** in the counting set. A future regression in e.g. `source-recheck.py`'s anchor rule, or a drift between the round-40 lesson's prose quotes and the manifest anchors, would not trip any frozen counter. The same quote-discipline machine (H4's `h4_code`, ≤25 words + URL + date + location) is applied only to the **round-39** lesson Gate blocks; the round-40 Gate blocks/entries are not scanned by any committed check. Wave 1 verified them manually (seam check); nothing reproducible guards them. Suggested reuse: (a) add `source-recheck` + `capture-binding-check` exits to C2's counting commands (or one aggregate instrument), (b) run `h4_code`-style scan over round-40 Gate blocks (S016/S017/S019/S020/S021/S022/S023/S024/S025/S060/S061/S062) as a new suite limb or QUALITY criterion.

### F5. H9 byte-pins the C2 decision artifacts (coupling, not a defect)
`declared-blocks.txt` declares the tails of `corpus/lessons/round-40.md`, the eight knowledge entries and the eight captures. Demonstrated: appending one line to `round-40.md` (without refreshing declared-blocks) flips H9 red (`declared=172,valid=171,tail=171`) while H2/H3/H4 stay green and C2 counters are unaffected. Consequence: any post-filing correction to C2 lesson/entry/capture content requires a lockstep declared-blocks refresh (the round's own J2-J5 churn shows this friction already happened). Keep as a deliberate discipline; note it as a maintenance coupling in QUALITY so future rounds don't treat it as a flake.

### F6. H6 is temporally coupled to concurrent seats (scheduling coupling, not a defect)
With `--work` outside any family dir, a second top-level `kasegi-r40*` entry reddens H6 (`strays=1`). During the wave, sibling seats' dirs exist, so the suite cannot run green on the real root mid-wave; a green Y ( requires all seats to have removed scratch first. Documented in the suite header; retained as coordinated observation.

## 3. Pattern reuse suggested for QUALITY/suite

- **P1 (status-change log ↔ registry transitions):** the lesson's `Nine decided rows — status change log` is prose; no committed check ties its `queued -> mined/rejected` transitions to the `SOURCES.md` status cells. The census's E11 `used-by` limb already binds rows↔entries; a parallel limb (or an extension of `capture-binding-check.py`) that verifies the lesson log matches registry transitions would close the gap cheaply.
- **P2 (quote discipline):** port the H4 `h4_code` scan to the round-40 lesson Gate blocks (F4b). The manifest+`source-recheck` anchor machinery already exists per capture; only the lesson prose is unguarded.
- **P3 (value derivation):** for H2/H3, derive expectations from the committed records (r39 receipt; criterion row semantics) instead of literal strings, so the gates re-read the record they are meant to keep honest (F2/F3).

## 4. Notes

- No network fetches were needed for this seat (source re-open is other seats' items); committed captures/manifest were re-checked via `source-recheck`.
- No lane/fleet files were modified; fixture commits were confined to scratch clones with toplevel assertions. No installs performed (channel: n/a).
- Scratch `S=/fast/scratch/hyaku/kasegi-r40/ConnPatterns/` removed before yielding.
