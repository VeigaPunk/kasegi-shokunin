VERDICT: BROKEN

# R45RevGateG4 — C2 gate G4 attack (kasegi round 45)

Attacked: `corpus/instruments/r45-c2-gate.py` `def g4` (lines 156-166), against its docstring predicate (lines 18-19: "capture: source-recheck.py exits 0 on manifest S071 (sha256 OK and five quotes OK) and the manifest holds the five frozen quote cores") and claims.json C2 `after`.

## What G4 actually reads (code, lines 156-166)
- `man` = `<root>/corpus/source-snapshots/round-45/manifest.json` (existence only).
- `source-recheck.py` is executed from **`<root>/corpus/instruments/`** — the verifier is the tree's own copy, not a frozen one.
- `oks` = count of `^S071:Q\d+ OK ` lines; `rc == 0`; `"S071:sha256 OK" in out`; `"BROKEN" not in out`.
- `miss` = the five hard-coded `MANIFEST_CORES` (norm-substring) searched across the **whole raw manifest text**, not inside a `quotes` entry.
- G4 never reads: `url`, `capture_url`, `http`, `path` (beyond what recheck does), `fetched_utc`, the snapshot bytes directly, or the SOURCES row. Grep of the file: `url|http|capture|path|sha` hits at lines 47, 143-152 (G3/G2 only); no provenance read inside g4.
- source-recheck.py's own docstring (lines 7-9): "This instrument reads only local files; a successful check verifies captured bytes, not current upstream availability or freshness." G4 therefore verifies **self-consistency** (manifest sha == bytes in the manifest's own dir), not that the bytes or URL come from docs.kernel.org.

## Baseline (honest) — discriminating controls
Command (scratch, `g4` imported from the frozen gate file, `g4(root)`):
- Control T0 (pure base export `/fast/scratch/hyaku/kasegi-r45/L1/pure` copy, no manifest):
  `gate G4 pass=0 read=manifest-absent`
- Control T1 (copy of the committed round-45 manifest + S071.txt + S072.txt + both instruments):
  `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
  Full CLI `python3 r45-c2-gate.py --root <T1>` also printed `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`.

## Attack constructions (defect present: the cited S071 capture is not tied to docs.kernel.org / the manifest does not hold the checked quotes)
All run with the frozen `g4()`; every one printed pass=1.

1. **B — provenance swap (cheapest; real bytes kept).** Edit manifest only: `url`, `capture_url`, `http.final_url` -> `https://example.invalid/mirror/security-bugs.rst.txt`, `http.status` 404.
   `diff` output (`diff <real manifest> <B manifest>`):
   ```
   6,7c6,7
   <       "url": "https://docs.kernel.org/process/security-bugs.html",
   >       "url": "https://example.invalid/mirror/security-bugs.rst.txt",
   9,10c9,10
   <         "status": 200,
   >         "status": 404,
   ```
   G4 line: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
   Full CLI on B: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0` (other gates red only because the fixture is minimal: `c2-gate fixed=1/7 exit=1`; G4 is the only line in question).
2. **A — fabricated capture, sha re-pinned.** Replace `S071.txt` with the five cores as five lines; set record `sha256`/`bytes`/`lines` to match; quotes = cores with anchors 1-5.
   `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
   Full CLI: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`.
3. **C — path redirect to shadow capture.** Real `S071.txt` untouched (so a sha-vs-SOURCES-anchor check on the real file stays green); record `path` -> `shadow/S071.txt` (stem S071 satisfies B1), shadow file = fabricated cores, sha re-pinned.
   `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
4. **D — decoy quotes, cores in an unselected record.** S071 quotes = five real substrings ("A reproducer with low complexity", "Working exploits are extremely helpful", "our preference is to release fixes", "Note that a time-dependent version such as", "will be needed (source code, shell script"); added record `S099` (not `--source`-selected, `path` absent, sha zeros) whose quotes are the five cores.
   Recheck: `(0, 'S071:sha256 OK\nS071:Q1 OK occurrences=1\nS071:Q2 OK occurrences=1\nS071:Q3 OK occurrences=1\nS071:Q4 OK occurrences=1\nS071:Q5 OK occurrences=1\n')`
   G4 line: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
   Note: the checked S071 quotes do not contain the cores at all; the cores are only substring-present in an unchecked record.
5. **E — decoy quotes, cores in an unchecked key.** Same decoy S071 quotes; cores placed in a `notes` string of the S071 record (recheck ignores unknown keys).
   `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
6. **F — tree-local verifier stub, no snapshot at all.** `corpus/instruments/source-recheck.py` replaced by a 5-line stub that prints `S071:sha256 OK` and five `S071:Qn OK` lines and exits 0; `S071.txt` and `S072.txt` deleted; manifest holds the five cores in a `notes` string.
   `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0` (`S071.txt present? False`)

Six genuine constructions printed pass=1 with the real defect present (A, B, C, D, E, F); the requirement was >=5. Cross-check: G3 (`g3`, lines 132-153) reads the SOURCES.md row, not the manifest, so B/C/F leave G3 and G4 able to disagree; G4 cannot detect any of them.

## False-RED: correct-looking landings G4 rejects
Built from the honest T1 tree; `run_recheck` = source-recheck.py exit + output.
- FR1 quote ids lowercase (`q1`..`q5`; schema-valid by ID_RE): recheck rc=0 with `S071:q1 OK ...`; G4 `gate G4 pass=0 read=recheck-rc=0 quotes-ok=0 frozen-cores-missing=0` (regex `Q\d+` is case-sensitive, line 162).
- FR2 Q1 written as the suffix span `with an exceptional extension to 14 calendar days` (correct substring of the source): G4 `pass=0 ... quotes-ok=5 frozen-cores-missing=1` (line 164 requires the full 118-char core).
- FR3 Q3 without the trailing period `Binary-only executables are not accepted` (correct span): G4 `pass=0 ... frozen-cores-missing=1`.
- FR4 Q1 declared `anchor: 312` (last line of the 310-312 span; window is anchor..anchor+3, so the span's start line is excluded): recheck prints `S071:Q1 OK normalized=markup-whitespace occurrences=1 anchor=312-BROKEN`; G4 `pass=0 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0` — the red is silent: the read token shows no reason (`"BROKEN" not in out`, line 165).
- FR5 manifest with UTF-8 BOM: recheck `manifest UNAVAILABLE reason=unreadable-or-invalid` rc=2; G4 `pass=0 read=recheck-rc=2 ...` (recheck rejects it too; consistent but a format variant G4 cannot distinguish from corruption).
- FR6 `sha256` uppercase: recheck `S071:manifest UNAVAILABLE reason=invalid-sha256`; G4 `pass=0 read=recheck-rc=2 ...` (schema-rejected; consistent).
- Controls that should and do pass: FR7 Q2 wrapped in `**…**` markup -> `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`; FR8 formatting-only rewrite (json indent=4, ensure_ascii) -> `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`.

So G4 can false-RED on a correct landing for: lowercase/other-case quote ids; a shorter or differently-punctuated span of any core (the frozen full-string match is required); an anchor pointing at a multi-line quote's last line; BOM / uppercase sha (schema-rejected by recheck too). A diagnostic defect: FR4 red has no reason token.

## Limitations
- I did not fetch docs.kernel.org (no live-target testing; corpus is documentation-only). Whether the real S071.txt equals the live page is unverified; G4 cannot establish it either way.
- Fixtures are minimal, so full-CLI `fixed=1/7` on the scratch trees is a fixture artifact; only the G4 line is evidence here. Other gates were not attacked.
- The lane's C2 drafts (F27 row, knowledge entry, SOURCES S071 row) are not landed in the lane tree; I did not test a final landing.
- I did not re-run the lane's freeze controls (c2-fabricated-quote 5/7 etc.); I cannot say from my run whether G4 is green on them. [INFERENCE: since construction A passes G4, the fabricated-quote control's 5/7 likely includes G4=1; unverified.]
- Scratch trees were under `$HYAKU_SCRATCH/kasegi-r45/R45RevGateG4` with TMPDIR set explicitly; removed on exit. No git mutations, no commits, no shared files touched; pure base export only read (copied).

## Recommended repairs (for the L1; not applied by me)
- Bind G4 to the frozen source: require manifest record `url`/`capture_url` == the G2 URL, `path` == `S071.txt` in the frozen dir, `sha256` == `sha256(corpus/source-snapshots/round-45/S071.txt)` and equal to the SOURCES anchor (G3).
- Run `source-recheck.py` from the frozen tool dir (`{tool}`), not the tree copy.
- Check the five cores as text of `quotes[*].quote` for the S071 record (not whole-manifest substring), and accept case-insensitive ids.
- Emit a reason token on red (e.g., `anchor-broken`/`broken-output`).
