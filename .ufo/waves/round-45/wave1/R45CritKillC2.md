VERDICT: BROKEN

Seat R45CritKillC2 (critic, leaf). Item: falsify C2's kill rule and after-state (claims.json C2, freeze 8cf62c879e6e6b031e67412f8fac1fba0bd378cf). Attacked: counter `corpus/instruments/r45-c2-gate.py` (G1–G7), `.ufo/waves/round-45/claims.json` C2 kill_rule/after, `controls/freeze-controls.py` C2 controls, the "non-author closure re-opens S071" clause, and the coverage criterion in `SCORECARD.md:1547-1562`. Cross-check instrument: `corpus/instruments/frontier-recheck-count.py` (the instrument SCORECARD:1551 already requires for admitted rows; the frozen C2 gate does not call it).

Summary: the frozen kill rule does not fire on a landing that adds four verbatim source sentences and nothing else. Such a landing reaches 7/7, 27 admitted rows and 64 entries, and also passes the frontier-recheck instrument. A verbatim copy of the existing F02 entry with its source ids scrubbed also reaches 7/7 and passes that instrument. The counter grades only the form of quote citations, not whether the entry adds analysis. The closure clause is satisfiable offline by no one, and online by anyone with network access; it is not run by any counter.

Scratch: `$HYAKU_SCRATCH/kasegi-r45/R45CritKillC2/` (default `/fast/scratch/hyaku`), removed on exit. Fixtures were built by copying the pure base export `/fast/scratch/hyaku/kasegi-r45/L1/pure` (not edited) and copying the three committed round-45 snapshot files from the lane. Nothing committed, nothing mutated in git, no lane file touched except this report. Tools installed: none (python3 stdlib and curl only).

## Re-runs of the frozen controls (reproduced)

Command: `python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export $SCR/base --lane <lane> --work $SCR/controls`
Printed (C2 lines):
```
control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED
control c2-junk-row counter=C2 c2-gate fixed=4/7 exit=1 expect=RED got=RED
control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 expect=RED got=RED
```
Matches freeze-controls.txt. The three controls are the only C2 controls; none of the landings below is among them.

Base gate on the pristine base copy: `gate G1 pass=0 read=rows=26 admitted=26 dup=0` ... `gate G7 pass=1 read=census-rc=0` ... `c2-gate fixed=1/7 exit=1`.

## Finding 1 — A boilerplate-only landing reaches 7/7 and passes the score's own recheck instrument (kill rule does not fire)

Fixture A2 = base + F27 row inserted after the F26 row in `corpus/README.md` (`| F27 | Linux kernel security-bugs reporting process | admitted | knowledge/linux-kernel-security-bugs.md | S071 | ... |`) + S071 row appended to `corpus/SOURCES.md` (11 cells, tier A, mined, 2026-10-28, sha256 0918dcfa… in the anchor cell) + new `corpus/knowledge/linux-kernel-security-bugs.md` whose body is exactly: a title line, the `source: S071 — https://docs.kernel.org/process/security-bugs.html — capture corpus/source-snapshots/round-45/S071.txt` line, `verified-at: 2026-10-28`, a real `recheck: cd … && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071` line, then four curly-quoted sentences each followed by a citation: the 7-day ceiling (`S071.txt:310-311`), AI-found bugs (`:95-96`), binary-only (`:39-40`), reproduction (`:41-43`). Nothing else. Non-quote prose words in the entry: 0.

Command and output:
```
$ python3 corpus/instruments/r45-c2-gate.py --root $SCR/fx/A2-boilerplate-real-recheck
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
gate G3 pass=1 read=row-S071=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4
gate G6 pass=1 read=knowledge=64
gate G7 pass=1 read=census-rc=0
c2-gate fixed=7/7 exit=0      (direct exit code 0)

$ python3 corpus/instruments/frontier-recheck-count.py --root $SCR/fx/A2-boilerplate-real-recheck
FRONTIER-PASS F27 ids=S071
PASS     F27  knowledge/linux-kernel-security-bugs.md  ids=S071  exit=0
entries=30 pass=30 exit=0      (direct exit code 0)
```
So the after-state in claims.json (“27 admitted frontier rows … one new knowledge entry (64 total) whose curly quotes are each located in snapshot lines and which cites the four frozen cores”) is literally satisfied by an entry with no analysis. The kill rule (fixed<7/7; any control 7/7; closure not locating quotes) does not fire on it. Novelty of the topic is real: `grep -rniE "kernel" corpus/knowledge` prints nothing at base. Novelty of content is not shown: the four cores are the only text, and nothing in the claim or gate requires any.

Discrimination against the do-nothing control: base 1/7 vs A2 7/7; the difference is the header, the two pointer rows and four verbatim sentences. Analysis content difference: 0 words.

## Finding 2 — A verbatim copy of the existing F02 entry, ids scrubbed, reaches 7/7 and passes the instrument

Fixture D3 = new file `knowledge/linux-kernel-security-bugs.md` whose body is the body of the existing `knowledge/coordinated-disclosure-timelines.md` (the F02 entry) with its `source:`/`verified-at:`/`recheck:` lines removed and `S003`/`S004`/`S005` replaced by the phrase "the cited policy"; then the same S071 header, real recheck line and four cores as A2. Share of the entry's 8-word shingles that occur verbatim in the F02 entry: 0.72 (D2, same copy without the id scrub: 0.85, `D2 new-entry lines: 55 8-gram shingles: 631 shared-with-F02: 538 share=0.85`).

```
$ r45-c2-gate.py --root $SCR/fx/D3-F02-copy-scrubbed-ids   ->  c2-gate fixed=7/7 exit=0
$ frontier-recheck-count.py --root $SCR/fx/D3-F02-copy-scrubbed-ids
PASS F27 ids=S071 ; entries=30 pass=30 exit=0  (direct exit 0)
```
The copy without the scrub (D2) is caught by the instrument only because the copied body still names S003–S005: `FRONTIER-FAIL F27 status=admitted ids=S003,S004,S005,S071 problems=missing-pass-line` (exit 1). So the instrument's protection is a side effect of source ids in the text, not a novelty check.

## Finding 3 — Repointing an existing entry plus a count pad reaches 7/7 with zero new entries

Fixture D: F27 row points at the existing `knowledge/coordinated-disclosure-timelines.md` (F02's entry), the two S071 header lines are inserted at lines 2–3, four cores are appended as a section, and an empty `knowledge/zz-count-pad.md` (0 bytes) is added so G6 counts 64.
```
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/coordinated-disclosure-timelines.md
gate G6 pass=1 read=knowledge=64
c2-gate fixed=7/7 exit=0
frontier-recheck-count: DUPLICATE-ENTRY F02,F27 knowledge/coordinated-disclosure-timelines.md ; entries=30 pass=28 exit=1
```
G1 does not require the F27 entry path to be unique; G6 counts files, not entries. The instrument detects the duplicate path but the frozen C2 gate does not call it.

## Finding 4 — Fabricated snapshot: 7/7 on content the live page does not hold

Fixture C: the author appends one sentence to the snapshot (`Reports naming a public CVE are triaged within 30 calendar days by the on-call maintainer.`, now line 374), re-pins the manifest sha256 and the SOURCES anchor sha, and cites that sentence with `(`S071.txt:374`)`.
```
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4
c2-gate fixed=7/7 exit=0
```
Independent check (web, no snapshot): `curl` of `https://docs.kernel.org/_sources/process/security-bugs.rst.txt` gives sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40` (equal to the pinned file); the fabricated snapshot has sha `8532a8cb…`. `grep -c "triaged within 30 calendar days"` on the live RST and live HTML: `0` and `0`. So the gate's truth anchor is the author's own file and manifest; nothing binds them to the upstream page. Manifest `bytes` (20152) and `lines` (372) are stale after the append (file now 20244 bytes) and G4 still passes: `grep -n '"bytes"' manifest.json` → `16: "bytes": 20152`, `wc -c S071.txt` → `20244`. `source-recheck.py` docstring (lines 8–9) states it "verifies captured bytes, not current upstream availability or freshness".

## Finding 5 — What the counter grades is grammar, not quotes (false negative and false positive)

- False negative: fixture E = an accurate house-style entry (blockquotes `> "…" — S071.txt:L310-L311`, the form used by 16 existing entries via `grep -lE '^> "' corpus/knowledge/*.md | wc -l` → 16) with a real recheck line. `gate G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4`, `c2-gate fixed=6/7 exit=1`. Meanwhile the instrument passes it (`PASS F27 ids=S071`, `entries=30 pass=30 exit=0`).
- False positive: G5 only grades curly spans followed immediately by a backticked citation. Fixture B adds an uncited curly fabricated sentence (`“the security team answers fax reports within one business day”`), an uncited prose claim (`The kernel triages reports on a 48-hour on-call rotation.`), and cites every core as `(`S071.txt:1-372`)` (whole file). `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4`; `c2-gate fixed=7/7 exit=0`. The 1–372 range makes the "located in snapshot lines N..M" check vacuous.
- G2 accepts `recheck: tbd` (length > 10): fixture A (with that recheck line) gives `gate G2 pass=1 read=source=1 verified-at=1 recheck=1`.
- The counter's quote-level result is also strictly coupled to line wrap: the cores wrap (`treat it as` / `public`, lines 95–96; `up to 7 calendar days` on line 310), so the G5 window must span two lines; a one-line citation would fail even when the text is right.

## Finding 6 — The after-state's coverage claim is not moved by the SCORECARD formula at all

SCORECARD.md:1551 defines coverage as `(20 + F_admitted) / (20 + F_total)` with `F_total` = frontier rows plus `queued` registry rows. Measured on the pristine base (`awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}'`):
```
base F_admitted=26 F_rows=26 queued_rows=0 ratio=1.0
fx/A-boilerplate-only F_admitted=27 F_rows=27 queued_rows=0 ratio=1.0
```
`grep -c "| queued |" corpus/SOURCES.md` → `0`. The ratio is 1.000 before F27 and after it; the formula cannot discriminate the landing. C2's "coverage" movement can only be an expansion count (+1 frontier row), not the SCORECARD coverage score.

## Finding 7 — Non-author closure ("re-opens S071") — answer

- Satisfiable without the pinned snapshot? Yes, by anyone with network access, and not offline. I performed that re-open: the live RST (sha `0918dcfa…`, 372 lines) is byte-identical to the pinned snapshot today, and the live HTML at the SOURCES URL `https://docs.kernel.org/process/security-bugs.html` (33,621 bytes) contains all five manifest quotes after tag stripping and whitespace normalisation (`Q1 7-day located-in-html-text`, `Q2 AI public located-in-html-text`, `Q3 binary located-in-html-text`, `Q4 repro located-in-html-text`, `Q5 version located-in-html-text`). Re-opening via the SOURCES URL works, and so does the manifest capture_url.
- But the closure catches only fabricated quotes (Finding 4). It passes A2 and D3 identically, because their quotes are real. It does not measure novelty, analysis or the entry's own prose.
- It is not run by any counter; `r45-c2-gate.py` has no network step, and no command or receipt for the closure is specified in claims.json. Its outcome depends on the live page at the time it is run; the kill rule gives no procedure for upstream drift (a drift would fail the claim for reasons unrelated to the entry).
- Round 44's own closure (`corpus/lessons/round-44-verifier-spotcheck.md` §4) re-opened the S069 document through a different URL (the REST article API) because the HTML was a shell. The same route choice would be needed here if the HTML ever becomes a shell; the frozen rule names no route.

## What an honest C2 claim needs that the gate does not check

1. Novelty floor against other entries: a shingle-overlap bound (D3 is 0.72, D2 0.85) or a rule that a new F-row's entry path is unique and its body is not a copy of another entry.
2. An analysis floor: non-quote prose that states a rule and is itself located or cited (A2 has 0 non-quote words and passes; B has uncited prose and passes).
3. Claim-to-citation binding for every rule sentence, not only curly spans with citations (B; E shows house-style spans are ungraded).
4. Citation precision: a bounded window (e.g. ≤3 lines) that contains the quote at its stated line (B's `1-372` passes).
5. Source binding: recompute manifest `bytes`/`lines` and check `fetched_utc`/`http` fields (C: stale bytes pass), and record an independent re-fetch receipt with its own sha; a self-pinned snapshot is circular (C: 7/7 against the live page's absence of the sentence).
6. Recheck binding inside the frozen gate: run `frontier-recheck-count.py` (already required by SCORECARD:1551) and reject `recheck: tbd`-type lines (A, G2).
7. Count binding: every knowledge file referenced by exactly one admitted row and every admitted row referencing a unique file (D's pad file and repointing both pass).
8. A coverage denominator that can move: at base the formula is 1.000 (Finding 6), so claim "coverage improved" only as "+1 frontier row" and say so.
9. Grammar neutrality: grade the house blockquote form too, or fail loudly on any entry with zero graded spans (E, 6/7 with the instrument passing it).

## Limitations

- Fixtures are hand-built in scratch and the scratch is removed on exit. The construction is fully described above (A2: header + recheck + four cores + F27 row + S071 row; D3: F02 body with S003–S005 replaced + S071 header/recheck + four cores; C: appended line 374 + re-pinned manifest and SOURCES sha; D: F02 repointed + empty pad file). Re-running needs the same description, not the files.
- The 8-word shingle share is a proxy for "copied", and "no analysis" is my reading of 0 non-quote words, not a machine-checked criterion.
- The live check is a one-time read on 2026-10-28 (`curl` 200 for both URLs). A later kernel-doc change could make the closure fail regardless of the entry.
- I did not run the executor's freeze-check draft (`wave1/R45ExecFreezeA.draft/freeze-check.py`) or the C1 counter beyond the freeze-controls re-run; the R45ScribeRowsB draft is empty. No F27 landing exists in the lane yet, so all landings tested are my fixtures.
- The census (G7) runs the fleet-root `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`r45-c2-gate.py:46`), outside the lane; it passed for every fixture but is not part of the lane tree.
- The `rc` values in one early run printed the exit code of `tail`; all exit codes reported above were re-taken without a pipe.
