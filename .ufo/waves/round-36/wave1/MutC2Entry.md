# MutC2Entry — round-36 mutation probe: the drafted F19 entry vs its own detectors

Seat: `MutC2Entry` (leaf, mutation-tester). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`).
Axis judged: coverage (C2's F19 pipeline). Milestone: round-36. All runs: 2026-10-26.
Report path: `.ufo/waves/round-36/wave1/MutC2Entry.md`.

This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r36/MutC2Entry/`
(removed before this receipt was finalized). No lane, fleet, sibling-lane or source-tree file was
edited; the only git operations were read-only `archive`/`log`/`ls-tree`/`status`/`rev-parse`.
No tool was installed (`python3`, `bash`, `git`, `grep`, `tar`, `sha256sum` only); `pacman` untouched.
`agent://all` was not messaged; no subagent was spawned.

---

## 1. Verdict table

| mutant | smallest behavior-bearing point mutated | expected detector | actual detector output (verbatim lines) | verdict |
|---|---|---|---|---|
| **M1** | entry: delete the `source: S053 — …` header line (line 3 of the draft) | harness prints `no-source-line`, exit 1 | `FAIL  F19  knowledge/epss-exploit-prediction-scoring.md  ids=-  exit=-  problems=no-source-line` + `entries=22 pass=21 exit=1`; harness rc=**1** | **KILLED** — exactly the expected print and exit |
| **M2a** | entry: paraphrase the entry's own pinned Q2 blockquote (line 39) to `EPSS publishes a probability between zero and one (with ranking percentiles)` | `quote-not-found` | harness `PASS F19 … exit=0` + `entries=22 pass=22 exit=0`, rc=**0**; recheck-audit rc=**0** | **SURVIVED** — coverage finding, see §4 |
| **M2b** | manifest: paraphrase pinned Q2 in `corpus/source-snapshots/round-36/manifest.json` (the pin the entry mirrors), recheck run against the mutated tree | `quote-not-found` | harness: `FAIL F19 … ids=S053 exit=1 problems=recheck-exit-1` + `entries=22 pass=21 exit=1`, rc=**1**; embedded recheck stdout: `S053:Q2 MISMATCH reason=quote-not-found` (Q1/Q3/Q4 `OK`, `sha256 OK`); direct `source-recheck.py --manifest … --source S053` rc=**1** | **KILLED** — the expected string `quote-not-found` is real and fires |
| **M3** | entry: recheck line `--source S053` → `--source S052` | exit 1 | harness: `FAIL F19 … problems=header-sources-not-rechecked,selection-not-declared-by-entry,manifest-missing-ids` + `entries=22 pass=21 exit=1`, rc=**1**; direct `source-recheck.py --manifest … --source S052`: `S052:source UNAVAILABLE reason=not-listed`, rc=**2** | **KILLED** at the harness (exit 1 as tasked); the bare instrument's own verdict is rc=2 (`not-listed`), recorded so nobody misreads the pair |
| **M4** | entry: delete the whole `recheck: cd … && python3 corpus/instruments/source-recheck.py …` line | recheck-audit fails closed | harness: `FAIL F19 … problems=no-recheck-line,no-source-selection,no-manifest`, rc=**1**; audit: `strict pass=47/48 …`, `lines=47 total=48 pass=47 … exit=1`, `expect=present expected=48 missing=0 unexpected=0 exit=1`, audit rc=**1** | **KILLED** — fails closed via the completeness limb (audited lines 47 ≠ 48 files), not by misnaming the entry |

4 of 5 mutants killed outright; M2 splits into a killed half (M2b, manifest pin) and a surviving half
(M2a, entry text) that is a genuine coverage finding, not a defect to fix by mutating the contract.

## 2. Baseline (pristine draft) — green, measured before every mutant set

Scratch tree = `git archive` of the claims-freeze commit `b47f2cdf…` + the F19 additions exactly as
drafted by siblings: the entry `corpus/knowledge/epss-exploit-prediction-scoring.md` extracted
byte-for-byte from `.ufo/waves/round-36/wave1/ScribeEntryF19.md` between its `---BEGIN/END ENTRY---`
markers (263 lines / 17,374 bytes, sha256 `36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641`
— matches that receipt's own "263 lines / 17,374 bytes" claim; the receipt's current revision already
carries the corrected capture digest, so 0 digest fixes were needed); the S053 registry row, search-log
bullet and Paths line from `ScribeRowS053.md` §1.1–1.3; `manifest.json` + `S053.txt` from
`ExecC2Capture.md` §3/§6 (extracted capture hashed back to `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`
= the manifest's declared sha256, 244 lines / 8,448 bytes — byte-perfect); a probe Frontier row `| F19 | … | admitted | knowledge/epss-exploit-prediction-scoring.md | S053 | … |`
inserted after the F18 row in `corpus/README.md` (probe scaffolding; the L1 lands the real drafted row);
`knowledge-expected.txt` + the entry (47→48, sorted). All of it scratch-only.

Measured on that tree (canonical `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` kept in the
recheck line; the real lane working tree holds the L1's landed round-36 capture, so the line resolves):

```
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
entries=22 pass=22 exit=0                       # frontier-recheck-count.py, rc=0
S053:sha256 OK                                   # source-recheck.py --manifest … --source S053, rc=0
S053:Q1 OK occurrences=1 anchor=216-ok
S053:Q2 OK occurrences=1 anchor=217-ok
S053:Q3 OK occurrences=1 anchor=217-ok
S053:Q4 OK occurrences=1 anchor=235-ok
strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0    # recheck-audit.py --root <tree> --cdroot <lane>, rc=0
lines=48 total=48 pass=48 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=48 missing=0 unexpected=0 exit=0
records=43 bound=43 unbound=0                    # capture-binding-check.py, rc=0
```

A green baseline is what makes the kill verdicts above meaningful (role rule: a baseline failure would
have made every mutant inconclusive). The F19 audit row at baseline: `frozen=111 strict=111111 lane=0 foreign=0 executes PASS`.

## 3. Restoration evidence

After each mutant the pristine entry bytes were copied back and re-hashed; the hash was required to
equal the pristine digest, else the probe aborted. Observed after each of the five restorations:
`restored OK sha=36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641` (five times, byte-exact).
The M2b manifest mutant lived only in the disposable `treeB` copy, which was deleted with the scratch
dir. The M2a/M2b probe re-verified the baseline green immediately before mutating (M2b baseline:
`entries=22 pass=22 exit=0`, rc=0), so the kill is attributable to the paraphrase alone.

## 4. Coverage findings (surviving half of M2)

- **No committed instrument compares the entry's quoted spans with the capture.** M2a paraphrased a
  pinned quote inside the entry and both detectors stayed green (harness rc=0, audit rc=0). The binding
  instruments police the *manifest↔capture* edge (M2b: killed) and the *entry↔recheck* edge (M1/M3/M4:
  killed); the *entry-quote↔capture* edge is policed only by the entry's own FC-1/FC-2 manual loops.
  This is a known, documented design limit — ScribeEntryF19 finding #2 says exactly that its seven
  non-manifest cited spans have "FC-2 … as the only guard" — and the probe now demonstrates it as
  measured fact rather than prose. A surviving mutant is a coverage finding, not permission to change
  the contract: pinning the remaining seven spans is a manifest revision (new record fields), not an
  entry edit, and is the L1's call.
- **M3's expected "exit 1" is a harness-level verdict.** The bare `source-recheck.py` answers a
  not-listed id with `S052:source UNAVAILABLE reason=not-listed` and **rc=2** (its UNAVAILABLE class),
  not 1. The tasked detector (`frontier-recheck-count.py`) still fails the entry at the binding limbs
  before execution and exits 1 — the claim as written holds at the level it was written for. Anyone
  scripting the direct instrument should assert rc∈{1,2} with the reason string, not rc=1.

## 5. Observations handed to the L1 (found while assembling, not mutants)

1. **Landed manifest is not byte-identical to the capture receipt's manifest.** The real lane's
   `corpus/source-snapshots/round-36/manifest.json` hashes `dd591cd4743b148d…`, the receipt-embedded
   manifest `f9590c2bbc26244a…`; parsed `sources[0]` is key-for-key identical (no differing keys), and
   `S053.txt` IS byte-identical (`4ec61c59b0e9aedf…83e9` measured on both). ExecC2Capture's receipt
   asks the L1 to land the two artifacts "byte-identically"; the manifest half of that is currently
   met only semantically (formatting/serialization drift). The instruments do not care; the byte claim
   does.
2. **Mid-probe scratch sweeps.** `/fast/scratch/hyaku/kasegi-r36/*` was wiped by a concurrent
   quiescence sweep at 12:57 (destroying this seat's first probe mid-run) and again between two tool
   calls. Every number in this receipt comes from one tight re-run after the second wipe; where the
   first pass had already produced output (baseline, M1, M3, M4, M2a), its values were identical.
   Scratch hygiene note for round-36 lessons: quiescence enforcement that deletes seat dirs while wave
   seats still run races those seats' probes.
3. Assembly details that could bite a re-run: the Frontier F19 row this probe used is scaffolding
   (marked as such in its note cell); the entry draft's `ground: F19` line and prose S-id mentions
   (`S052`, the `record S053` mention in "Scope and limits of the pin") are load-bearing for the
   harness's citation limb — the M3 mutant therefore shows `selection-not-cited-by-entry` *not* firing
   (S052 is legitimately cited in prose), which is correct behavior, not a missed limb.

## 6. Bounds

No lane file was created or modified (receipt only); no sibling scratch was touched; the real lane was
only read (plus executing its committed instruments and the landed captures through the recheck lines,
which the corpus's own `cd <lane> &&` convention requires). The claims file was not edited. Scratch
`/fast/scratch/hyaku/kasegi-r36/MutC2Entry/` was removed after this receipt was written.
