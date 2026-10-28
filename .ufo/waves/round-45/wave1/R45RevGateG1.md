VERDICT: BROKEN

# R45RevGateG1 — C2 gate G1 attack (corpus/instruments/r45-c2-gate.py, `def g1`)

Scope: G1 only. Read-only seat; fixtures in scratch (removed on exit). Counter tested = working copy of corpus/instruments/r45-c2-gate.py, sha256 5e0796168cfe09f1e7db1b270a4f563cb40516c676d2c5c7921b46cd70730082 (tracked; `git status --short` on the file and corpus/README.md is clean). Base tree = `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd corpus`.

## What G1 actually checks (read: r45-c2-gate.py:107-118, docstring :10-12)
- `frontier()` (:85-91) counts every line matching `^\| F\d+ \|` anywhere in corpus/README.md. No section, no fence/comment awareness, no header check.
- `g1` passes iff that count == 27, count of 3rd cell == `admitted` == 27, no duplicate id, and F27's 4th cell contains a `knowledge/[A-Za-z0-9._-]+\.md` path where `corpus/<path>` `isfile()` (:94-104).
- G1 never reads the entry file's content, never checks the entry is unique to F27, and never checks it is the Linux-kernel process. Content is left to G2 (header trio) and G5 (quotes).

## Control (do-nothing)
Command: `python3 r45-c2-gate.py --root <pure base>`
Output: `gate G1 pass=0 read=rows=26 admitted=26 dup=0` ... `c2-gate fixed=1/7 exit=1`
(matches claims.json C2 expect_before). Adding only the F27 row with a missing entry (T0): `gate G1 pass=0 read=F27-entry-missing`.

## Finding 1 — G1 can print pass=1 with no real F27 entry (cheapest recipe: T1)
Recipe: copy base; insert ONE line after corpus/README.md:628 (after the F26 row):
`| F27 | Linux kernel security-bugs reporting process | admitted | knowledge/cvss-v4-severity-and-vector.md | S071 | probe |`
(the entry points at the existing F01 entry file; no new knowledge file, no SOURCES row).
Printed:
`gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/cvss-v4-severity-and-vector.md`
Same tree, rest of counter: `gate G2 pass=0 read=source=0 verified-at=0 recheck=1`, `gate G3 pass=0 read=row-S071=absent-or-malformed`, `gate G4 pass=0 read=manifest-absent`, `gate G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4`, `c2-gate fixed=2/7 exit=1`.

## Finding 2 — six distinct genuine constructions, each G1 pass=1 with the defect present
All six: no new Linux-kernel entry, no S071 row/snapshot use, G2 and G3 both fail. Each printed G1 line (verbatim):
- T1 existing unrelated entry (F01 file) as F27's entry: `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/cvss-v4-severity-and-vector.md`
- T2 zero-byte new entry `corpus/knowledge/linux-kernel-security-bugs.md` (created with `: >`; G6 then prints `knowledge=64`): `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs.md`
- T3 symlink `linux-kernel-security-bugs.md -> cvss-v4-severity-and-vector.md`: `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs.md`
- T4 duplicate-looking table: F27 row ONLY inside an HTML comment (README:629-631 `<!--` / `| F27 | ... | admitted | knowledge/linux-kernel-security-bugs.md | S071 | probe |` / `-->`), rendered table still F01-F26. `grep -cE '^\| F[0-9]+ \|'` gives 27 on T4 vs 26 on base; `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs.md`
- T5 duplicate-looking table: second table appended at README end under `## Round 45 frontier summary` containing only the F27 admitted row, pointing at F01's entry: `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/cvss-v4-severity-and-vector.md`
- T6 entry cell = missing path first, existing decoy second (`knowledge/linux-kernel-security-bugs.md, knowledge/cvss-v4-severity-and-vector.md`): `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/cvss-v4-severity-and-vector.md`

Root causes: (a) existence-only entry check (T1-T3); (b) row counting includes HTML comments and any table in the file (T4, T5); (c) first-existing-path-wins with no uniqueness across rows (T1, T5, T6).

Limitation on "defeats C2": none of T1-T6 reaches 7/7 (max observed fixed=3/7 for T2-T4). G1 alone is passable; the counter still rejects these trees through G2/G3/G4/G5.

## Finding 3 — G1+G2 are jointly satisfiable by a 3-line file (T7)
Recipe: T1 row with the entry file holding only the three header lines `source: S071 — https://docs.kernel.org/process/security-bugs.html`, `verified-at: 2026-10-28`, `recheck: probe`.
Printed:
`gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs.md`
`gate G2 pass=1 read=source=1 verified-at=1 recheck=1`
`gate G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4`
`c2-gate fixed=4/7 exit=1`
So G5 (quotes) is the only limb carrying content; G1/G2 do not.

## Finding 4 — G1 false-REDs on correct-looking landings (format variants)
Built on base with the row inserted at README:628 and a real-looking entry file present. G1 printed:
- REJECTED (should a correct landing be written this way?):
  - status bold `| **admitted** |` → `rows=27 admitted=26 dup=0`
  - status `Admitted` → `rows=27 admitted=26 dup=0`
  - status `admitted (round 45)` → `rows=27 admitted=26 dup=0`
  - no spaces `|F27|…|admitted|…|` → `rows=26 admitted=26 dup=0` (row silently not counted)
  - two-space indent `  | F27 | …` → `rows=26 admitted=26 dup=0`
  - no outer pipes `F27 | … | probe` → `rows=26 admitted=26 dup=0`
  - pipe inside a backticked name cell (`` `security|bugs` ``) → `rows=27 admitted=26 dup=0` (naive `split("|")`, frontier():90)
  - zero-padded `| F027 |` → `exception-IndexError` (g1 line 115 `[0]` runs before the `p is None` check at :116; verdict still RED, but the reason is an exception)
  - entry in nested dir `knowledge/kernel/security-bugs.md` (file exists) → `F27-entry-missing` (regex :99 forbids `/`)
  - entry with parentheses `knowledge/linux-kernel-security-bugs(1).md` (exists) → `F27-entry-missing`
  - entry with non-ASCII `knowledge/linux-kernel-security-bugs-é.md` (exists) → `F27-entry-missing`
  - a legitimate non-admitted candidate row elsewhere, e.g. `| F28 | … | rejected | … |` → `rows=28 admitted=27 dup=0`
- ACCEPTED (positive controls): backticked entry as in the existing F26 row `` `knowledge/…md` `` → `pass=1`; `corpus/knowledge/…md` prefix → `pass=1`; markdown link `[linux](knowledge/…md)` → `pass=1`.

Assessment: the bold/case/suffix status, no-space/no-outer-pipe/indented rows, pipe-in-cell, nested/parenthesised/non-ASCII filenames, and any extra non-admitted F-row are all rejected though a correct landing could reasonably use them. Only the exact existing convention passes.

## Recommendations (predicate-preserving errata, per claims.json C2 kill_rule)
- Parse the frontier table with a markdown-aware reader: skip HTML comments and fenced blocks; require one F27 row in the rendered frontier table.
- Require the F27 entry path to be unique across rows and non-empty; require exactly one path in the entry cell.
- Keep G1 a count/structure check; move content checks to G2/G5 as now. Do not change the predicate sentence after scoring.

## Limitations
- Tested the working-copy counter (tracked, clean); tested the frozen base export and fixtures only. No change to the lane was made.
- Fixtures are minimal README/knowledge edits; G2-G5 results are reported only as context for G1.
- Format-variant list is what I tried; not exhaustive (e.g., CRLF, tabs, NBSP not tested).
- Scratch removed on exit; all fixture outputs above were printed by re-runs in this session.
