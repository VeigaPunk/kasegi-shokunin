# CritC2Kill — C2 kill-rule robustness review (round 30, wave 1)

Seat: `CritC2Kill-3` (UFO-FSD critic, leaf). Scope: attack claim C2's predicate
("reach frontier 14 + entries citing S046/047 = 1 + rows 47 + census 0 + harness
17/17 + recheck 0") **without a real entry or captures** — empty/stub/wrong
entry, row-only append, duplicate source row, entry pointing at an existing
capture, and sourceless fixtures. Verdict: **the kill rule is robust against
structural/arithmetic forgery, not robust against content-fidelity forgery — the
claim can be driven fully green with a stub entry, reused wrong captures, or a
decoy citation file.**

## Axes
- `coverage` (owned, C2): score_after "held 7" — the axes the counter gates live on.
- `depth:verifiability` (owned): the same gates double as the verifiability
  instrument; content-fidelity gaps here are shared.

## Basis (bytes measured)
- Frozen claims: `.ufo/waves/round-30/claims.json` (C2 kill rule + counter
  commands); before receipts `.ufo/waves/round-30/c2-controls/before.txt`
  (frontier=13, entries=0, rows=45), `census-before.txt`, `c1-controls/before.txt`.
- Instruments read in full: `corpus/instruments/frontier-recheck-count.py`
  (sha256 c8a62888…) and `corpus/instruments/source-recheck.py` (sha256
  9fe6a4a0…), `scripts/sources-census.sh` (validate E01–E12/W01–W04).
- Real round-30 capture digests: S046.txt 884481f3…, S047.txt bcf4f605…,
  S041.txt e18acbf9…; round-30/manifest.json 2a3256d9…; reused round-29
  S043.txt d3b815ed…, round-28 S042.txt b432ec165….
- Current working tree (M0 mirror, counters all green) confirms the real F14
  landing: frontier=14, entries_citing=1, rows=47, census=0, harness 17/17, recheck=0.

## Attack experiments (each run in an isolated mirror under
`.ufo/waves/round-30/wave1/CritC2Kill-lab/M*`; only working-tree scratch copies,
no lane mutation)

### A. Empty/stub entry + real captures — **NOT CAUGHT (all six counters green)**
Stub F14 entry `japanese-severity-vocabulary-and-impact-model.md` containing
only header lines (`source: S046/S047/S041` + chained `recheck:` line to the
real round-30 manifest), zero prose, zero claims.
Results: frontier=14; entries_citing=1; rows=2 (total 47); census_exit=0;
harness 17/17 exit=0; recheck_exit=0 (S046/S047/S041 all OK, occurrences=1).
Proof: the harness contract is A–D (source/recheck/manifest bookkeeping) + exit
code; it never reads the entry body. `source-recheck.py` verifies capture bytes
against manifest assertions only.

### B. Reused/wrong captures (point the entry at existing captures) — **NOT CAUGHT**
S046.txt replaced with byte-copy of round-29 S043.txt (HackerOne policy), S047.txt
replaced with round-28 S042.txt (IPA intake-process page); manifest rewritten with
those documents' own sha256 pins and quotes. Stub entry identical to A.
Results: frontier=14; entries_citing=1; rows=2 (47); census_exit=0; harness
17/17 exit=0; recheck_exit=0 (S046 Q1–Q4 OK anchor=31/40/170/92-ok; S047
Q1–Q6 OK). No check anywhere ties `S046.txt`/`S047.txt` bytes to the IPA JVN
URLs the registry rows claim — capture provenance is self-attested by the manifest.

### C. Row-only append (no entry) — **CAUGHT**
F14 README row + S046/S047 rows, no entry file: harness `FAIL F14 problems=missing-entry`,
entries=17 pass=16 exit=1; census also reports E11 (used-by missing) exit=1.
Kill rule fires.

### D. Duplicate source row — **CAUGHT**
Two S046 rows: `rows_s046_047=3` and `total_s_rows=48` (both violate the exact
counts) and census `E03 duplicate id` + `E04 duplicate url` exit=1. Kill rule fires.

### E. F14 row pointing at an existing entry (F13's file) — **CAUGHT**
Harness prints `DUPLICATE-ENTRY F13,F14` exit=1. Kill rule fires.

### F. Sourceless fixture counted by the citations counter — **NOT CAUGHT**
Decoy orphan file `corpus/knowledge/zz-sourceless-fixture.md` containing only
`source: S046 …`; F14 stub cites S041 only; registry rows S046/S047 untouched.
Results: frontier=14; entries_citing=1 (**the decoy, not the entry**); rows=2
(47); census_exit=0; harness 17/17 exit=0; recheck_exit=0. The
`grep -lE '^source: S04[6-7] ' corpus/knowledge/*.md` counter counts any header
line in any file — nothing binds it to the registry, the frontier, or a capture.

## Verdict
- Kill rule **robust** against: missing entry (harness E), duplicate entry
  realpath (harness F), duplicate/manipulated source rows (census E01/E03/E04 +
  exact row counts), malformed/unreadable manifests and stem mismatch
  (source-recheck B1), non-unique/unanchored quotes (B2), and count inflation
  beyond the exact figures (14/1/47/17/17/0 are all hard-switch).
- Kill rule **not robust** against content-fidelity forgery: A (stub), B (false
  provenance), F (sourceless fixture) each satisfy **all six counter commands**
  (the very commands the kill rule runs) while zero real knowledge, zero genuine
  captures, or zero actual S046/S047 grounding exist. The claim's "measured"
  status would be held on artifacts whose substance no instrument checks.

## Smallest safe corrections (ordered)
1. **Bind predicate 2 to admitted entries** — count only files referenced by
   admitted frontier rows (or parse a first-class `cites:`/registry-backed
   field), eliminating decoy header files (fixes F).
2. **Capture provenance pin** — `source-recheck.py` should validate a per-record
   `url` (+ `fetched_by`/`fetched_at`) against the SOURCES registry row URL and
   reject a capture whose bytes are identical to another round's different-URL
   capture (fixes B).
3. **Entry ⇄ assertion binding** — `frontier-recheck-count.py` should require
   each manifest quote (or its `location` anchor) to appear in the entry body,
   turning the documented "recheck coverage only" caveat into a prose check
   (fixes A).
4. Cheapest stopgap: tighten the citation regex to require the S-id followed by
   ` — ` and the same file to carry a `recheck:` line (hardens F without a new
   instrument).

## Evidence and hygiene
- All counters (awk/grep/census/harness/recheck) run verbatim on mirrors; key
  outputs captured above. Mirror trees retained at
  `.ufo/waves/round-30/wave1/CritC2Kill-lab/` (M0 baseline; Mbase-Stub;
  Mfake-Cap; MrowOnlyB; MrowOnly; Mcopy-Dup; Mdecoy) for reproduction.
- No tool installs were made (tooling authorization read; none needed). No
  write outside the lane repo; no git/jj mutation; no live target contact.
