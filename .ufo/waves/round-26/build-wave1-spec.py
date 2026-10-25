#!/usr/bin/env python3
"""Build wave-1 spec for kasegi round 26 (36 build seats)."""
import json, os

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SHOKU = "/home/vgpnk/Projects/shokuknow"
BASE = "1b076fa7f2fb5e7dd9d87449514eba526043421b"
W1 = ".ufo/waves/round-26/wave1"
R26 = ".ufo/waves/round-26"

CONTEXT = f"""# Round
kasegi-shokunin round 26, wave 1 (build), dispatched by the L1 (parent omp session). Fleet root
{FLEET}. Lane repo {LANE} — your only write scope. Lane base revision {BASE} (claims freeze commit).
Read before your item (absolute paths):
- {LANE}/.ufo/waves/round-26/claims.json (FROZEN claims C1/C2, predicates, counters, kill rules — do
  not edit; corrections land as separate appended files)
- {LANE}/SCORECARD.md (axes, saturation, planned rows)
- {LANE}/corpus/QUALITY.md (entry bar Q1-Q9, record bar R1-R12)
- {LANE}/corpus/README.md (coverage map, frontier)
- {LANE}/corpus/SOURCES.md (registry; S001-S040; S040 recheck cell, R25-5)
- {LANE}/corpus/lessons/round-25.md (Gate/verifier spotcheck routed defects R25-1..R25-5) and
  round-25-verifier-spotcheck.md
- {LANE}/corpus/instruments/recheck-audit.py (has 13 selftest fixtures + completeness for missing
  recheck lines; full-entry deletion STILL passes: the round's C1 soundness target)
- {LANE}/corpus/instruments/capture-source.py (supports --kind pdf via pdftotext)
- {LANE}/corpus/instruments/source-recheck.py (manifest sha256-pinned quote verification)

# The two frozen claims (do not widen, do not re-word; counter commands execute from lane root)
C1 depth:verifiability (lowest non-retired axis, score 4 held) — recheck-audit gate conformance:
(a) SKILL.md gains a gate|probe registry row for recheck-audit.py with verdict map, self-test spelling
(--selftest), pinned-value path, write scope, owner; (b) a committed selftest receipt line
`selftest cases=… failures=0` exists in .ufo/waves/round-26/c1-receipt-index.txt at the instrument's
own sha256 (fixes R25-2 cross-reference); (c) fix-control #3 is restated to exclude the retained
historical round-24.md:77 line and the restated grep returns 0 hits (R25-4); (d) deleting a whole
corpus/knowledge entry makes the audit exit 1 naming the missing entry (before: exit 0).
C2 coverage (score 7 held) — F11 frontier admitted in corpus/README.md (ISO/IEC 29147/30111
division-of-labour theme, assimilation package), >=1 knowledge entry cites a source row first
registered this round (S041 = JPCERT/CC 2026 P-guideline capture, staged S076/S064 by document),
sources census validates exit 0 at round end. Kill rule: a source row appended without an admitted
entry citing it.

# Hard rules (every seat)
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Use absolute
  paths in every command.
- You are a leaf: spawn nothing, start no background job, run no swarm of your own.
- Write ONLY your owned paths (named in your item). A read-only seat makes NO production edit; its
  output is its report file (and, where the item says so, files under {W1}/).
- Never write {FLEET} (fleet root), any sibling lane, {SHOKU} (READ-ONLY: no writes, never run
  renumber-staged.py / merge-plan.py / quote-lint.py / absent-defect-register.py there),
  {FLEET}/.ufo/state, {FLEET}/.scratch, MANIFEST.json, templates/ or fleet scripts/.
- Never run in the lane repo: git add/commit/push/checkout/switch/stash/reset/pull, any mutating jj
  command (commit/new/describe/squash/rebase/abandon/bookmark/undo/op restore), or any other VCS write.
  Read-only git (log/show/diff/status/ls-files/rev-parse) and `jj --ignore-working-copy` are fine.
  The L1 commits through the lane helper; you never do.
- Tooling: you may install or upgrade tools that help your item — read /home/vgpnk/.omp/agent/RULES.md
  first, official channels only, record tool/version/channel/reason in your report. ALL pacman
  transactions are PAUSED host-wide: use `uv tool` / `npx` / an official binary in ~/.local/bin only;
  never `pacman -S`, `-Sy`, `-Syu`, `-U`, `-R`.
- Honesty: an unrun check has not passed; never fabricate a verdict, a quote, a count or an exit code.
  Quote failures verbatim. If your item cannot be completed, report the exact blocker.
- Never edit claims.json, the round-25 lesson(s), or any round-25 wave receipt.
- Today is 2026-10-25. Use UTC in timestamps. Access dates in Gate blocks must be today.
"""

ITEM = {
    "s1": dict(role="scout", axes=["depth:verifiability", "coverage"], milestone="planner data-walk",
        task=f"""This seat carries the L1 planner's bounded data-walk. Verify and report:
1. Counter command availability from the lane root: the C1 counting commands in claims.json parse and
   run (grep -cE '^\\| [^|]+\\| gate\\|probe ' SKILL.md -> 0 now; grep -cE 'selftest cases='
   {R26}/c1-receipt-index.txt -> file absent now; the fix-control grep excluding round-24.md:77 -> 1
   hit now on the retained line). Run each, record exact current outputs.
2. Knowledge file census: `git ls-files corpus/knowledge/*.md | wc -l` and `glob` count (expect 37).
   Confirm no untracked knowledge files.
3. C2: corpus/README.md frontier rows current list (F1..F10) and their states; verify F11 is absent;
   verify `frontier-recheck-count.py` exists and how it counts entries per row.
4. Sources census CLI: run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin kasegi` and record exit.
5. SOURCES.md rows: confirm S040 row columns (id|title|source|category|grade|read|recheck|used-by)
   and exact current recheck cell; confirm S039 exists (Hitachi ISO mapping) for entry citation needs.
6. Confirm .ufo/waves/round-26/claims.json exists and is untouched (matches commit {BASE}).
Report: {W1}/s1-datawalk.txt (facts only; no edits)."""),
    "s2": dict(role="scout", axes=["depth:verifiability"], milestone="S040 live probe (R25-5)",
        task=f"""Record the live behavior of the Cisco security vulnerability policy URL for R25-5
(drift: final URL + UA requirement). Run BOTH probes:
- Browser UA: `curl -s -o /dev/null -L -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
  (KHTML, like Gecko) Chrome/126.0 Safari/537.36" -w "final=%{{url_effective}} code=%{{http_code}}
  num_redirects=%{{num_redirects}}\n" ...`
- Instrument UA (the lane's capture-source.py UA string): `curl -s -o /dev/null -L -A
  "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)" ...`
Record canonical URL, redirect chain, final URL, final code for both. Then capture the FINAL page
(not the canonical URL) through the lane instrument: `python3 {LANE}/corpus/instruments/capture-source.py
--id S040 --url https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html
--kind html --out {LANE}/corpus/source-snapshots/round-26/S040-live.txt` — record exit, sha256,
fetch time. Grep the captured snapshot for "ISO/IEC 29147" and "Disclosure of Security Vulnerabilities"
and report line numbers + first 120 chars of each hit. Do NOT edit SOURCES.md (scribe w1 owns it).
Report: {W1}/s040-probe.txt (include both curl outputs, capture log line, greps)."""),
    "s3": dict(role="scout", axes=["coverage"], milestone="staged package inventory",
        task=f"""Read-only inventory of the assimilation package at {SHOKU}/merge/kasegi/:
1. Confirm MERGE-REPORT.md and SOURCES.append.md exist; staged row count (94) and first/last staged
   ids; list ids S031-S040 (collide with lane registry) and S041-S124 (free).
2. Confirm the two target staged entries exist with current bytes:
   - corpus/knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md
   - corpus/knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md
3. Extract from each staged entry: its `ground:` line, `source:`/`verified-at:`/`recheck:` headers,
   every quoted claim and its location citation. Report whether the staged recheck lines would pass the
   lane's strict limb rules (parse/cwd/paths/cdroot/instrument/own) — say which do not.
4. Confirm reject candidates exist in the package: vendor-cvd-policy-crosswalk-2026-10-23.md and
   chinese-criminal-thresholds-and-authorisation.md (ground F20 vs F09 status).
No writes outside {W1}/s3-inventory.txt. Read-only on {SHOKU}."""),
    "s4": dict(role="scout", axes=["coverage"], milestone="quarantine slice hand-check",
        task=f"""Hand-check the kasegi quarantine slice rows (from
{SHOKU}/.ufo/waves/corpus-expansion-1/absent-defect-register.md): S037, S054 (payload-absent), S048,
S065, S068, S069, S070 (could-not-be-fetched). For EACH row: try to fetch its cited source with the
lane instrument UA (`curl -s -L -A "kasegi-shokunin/1.0 (documentation capture;
+https://shokunin.invalid/kasegi)"`), record HTTP code and bytes; if fetched, attempt to locate the
staged quote text in the body and report the first 80 chars of a contiguous match (or none). Verdicts
per row: `fetched quote-located` | `fetched no-quote` | `unfetchable` | `already-mined-legacy` (for
S068:Cisco — cite the round-25 verifier spotcheck's verified 301->200/UA note). For payload-absent
rows report what absence means for adoption. Write verdicts one row per line to
{W1}/quarantine-verdicts.txt. No production edits."""),
    "s5": dict(role="scout", axes=["coverage"], milestone="staged quote re-location",
        task=f"""Independently re-locate the quotes used by the two staged target entries in the
ORIGINAL source (not the lane capture). Fetch
https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf (instrument UA) to /tmp, run `pdftotext`
on pages 45-47 and 53-54. Report the exact extracted line numbers for:
- division-of-labour paragraph: "ISO/IEC 30111:2013 はベンダの社内での脆弱性取扱いのプロセス（脆弱性
  の検証、脆弱性対策の開発等）の指針を提供します。" (expect ~line 2009-2012 of full text)
- 図 1 caption "（出所：ISO/IEC 29147:2014 を元に作成）" occurrences
- §4 (2) divergence sentence "P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません"
- 7-day acknowledgement "受信した旨を 7 日以内に返信することが必要となります。"
- "6.2 Minimum policy aspects" / "6.3 Optional policy aspects" markers
- "参考 1 ISO/IEC 29147:2014 と情報セキュリティ早期警戒パートナーシップガ..." table
Also compute the sha256 of the fetched PDF bytes and of a pdftotext extraction. Output:
{W1}/s5-quote-relocation.txt. Report only facts, no production edits."""),
    "c1": dict(role="connector", axes=["coverage"], milestone="sibling overlap scan",
        task=f"""Scan sibling lanes' corpora for overlap with the planned F11 theme (ISO/IEC 29147 /
30111 division of labour; JPCERT/CC 2026 partnership guideline). For each repo under {FLEET}/*-shokunin/
(except kasegi) and {FLEET}/../kimi-shokunin/skills, grep for: "29147", "30111", "JPCERT", "jpcert",
"パートナーシップ", "partnership_guideline". Report per repo: hits, file names, and a verdict
(overlap|distinct|none). Also confirm no sibling holds an F11-equivalent frontier row. Output:
{W1}/c1-overlap.txt. Read-only."""),
    "c2": dict(role="connector", axes=["depth:verifiability"], milestone="round-25 metric continuity",
        task=f"""Reconstruct the round-25 frozen metric spans (read-only git history of the lane) to
give the revenger/no-harm baseline: (1) the C1 claim counters in .ufo/waves/round-25/claims.json
(lines=35 pass=6 fail-closed=23 exit=1 and the after=37 state); (2) the instrument digest
c1-instrument-digest.txt = c3c19adc... and the receipt index line 4 cross-reference (wave2/C1InstrumentDigest.md
claims it "matches c1-receipt-index.txt:4 exactly" — pull the actual line 4, which has no selftest
line: quote both); (3) d24-3 receipts (dispatch-mut8.json/contain-mut8.json) exist; (4) verify the
round-25 lesson's fix-control #3 text and the historical retained line corpus/lessons/round-24.md:77
("62 assertions" quote) causing the 1-hit grep. Output {W1}/c2-r25-continuity.md with exact quoted
strings and commit hashes. Read-only; no edits."""),
    "c3": dict(role="connector", axes=["coverage"], milestone="used-by edge map",
        task=f"""Compute the used-by edges for registry rows S039 (Hitachi), S040 (Cisco) and the
planned S041 (JPCERT/CC 2026 guideline): for each corpus/knowledge/*.md entry, find its `source:` ids.
Report per row: list of citing entries. Then confirm: (a) S040's used-by currently includes
vendor-disclosure-policy-commitments-crosswalk / vendor-disclosure-policies-as-corpus-objects (F10
entries); (b) adding S041 and having two new entries cite S041/S039/S040 does not orphan any row and
keeps census rule R9 (rows cited by >=1 entry) satisfied; (c) nothing else references S040's canonical
URL directly in a way that would break if the row's recheck cell gains the final-URL/UA note. Output
{W1}/c3-usedby.txt. Read-only."""),
    "c4": dict(role="connector", axes=["depth:verifiability"], milestone="ownership matrix preflight",
        task=f"""Build the ownership matrix for round-26 wave-1 outputs: map every planned owned path
(({W1}/*, corpus/instruments/recheck-audit.py, corpus/instruments/knowledge-expected.txt,
corpus/knowledge/iso-29147-and-30111-division-of-labour.md,
corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md, corpus/source-snapshots/round-26/*,
corpus/SOURCES.md, corpus/README.md, corpus/lessons/round-26.md, SCORECARD.md, LOG.md,
PROVINCE.md, SKILL.md, .ufo/waves/round-26/c1-receipt-index.txt, .ufo/waves/round-26/c1-controls/*)
to the seat that owns it (s2/s4/s5 read-only, w1-w7 writers, e1-e9 writers, m1-m3 read/write into
c1-controls only). Assert no path is owned by two seats and no seat writes outside its set. Output
{W1}/c4-ownership.txt. Read-only."""),
    "e1": dict(role="executor", axes=["depth:verifiability"], milestone="recheck-audit deletion soundness",
        task=f"""Extend {LANE}/corpus/instruments/recheck-audit.py (SOLE OWNER of this file) so that
deleting a whole corpus/knowledge entry fails the audit:
1. Add `--expect PATH` argument, defaulting to `<root>/corpus/instruments/knowledge-expected.txt` when
   it exists; when it exists, collect the expected entry filenames (one per line, sorted, relative to
   root), compare set equality with the audited tree's entries. On mismatch, print `missing=<name>` for
   entries in expected but absent, `unexpected=<name>` for extra entries, and make exit=1.
2. Add receipt JSON fields `expected_entries`, `missing_entries`, `unexpected_entries` (arrays).
3. When `--expect` is absent or its file missing, keep current behavior (completeness via glob) and
   add receipt field `expect=absent`.
4. Extend the selftest with TWO new fixtures (total 15): (i) a tree whose expected list names a file
   that is absent -> exit must be 1 and receipt shows missing_entries naming it; (ii) a tree with an
   unexpected extra file -> exit 1. Keep all existing 13 fixtures passing.
5. Update the module docstring: document the expected-list contract (committed alongside knowledge
   files; drift = red audit) and the exit semantics (0 clean / 1 failed).
Do NOT touch any other instrument or file. Run the full selftest (15 cases) and the audit against a
scratch copy; record outputs (selftest lines + exit) in {R26}/c1-controls/e1-selftest-live.txt. Do
not edit claims.json. Report your diff summary in the Report: trailer."""),
    "e2": dict(role="executor", axes=["depth:verifiability"], milestone="expected list artifact",
        task=f"""Create {LANE}/corpus/instruments/knowledge-expected.txt: the sorted list of current
committed knowledge entry filenames (relative paths under corpus/knowledge/), one per line, from
`git ls-files corpus/knowledge/*.md` (read-only) — exactly 37 entries. Add a two-line header comment
(naming the owning instrument recheck-audit.py and the round). After creating it, sanity-run:
`python3 {LANE}/corpus/instruments/recheck-audit.py --root {LANE} --cdroot {LANE}` only if e1's
change has landed; otherwise defer the run and only create the file, noting the deferral. Report the
file + count. Sole owner of this file."""),
    "e3": dict(role="executor", axes=["depth:verifiability"], milestone="gate receipt index + crossref fix",
        task=f"""Write {R26}/c1-receipt-index.txt — the committed gate receipt index for round 26 —
with lines:
1. `instrument_sha256=<sha256 of {LANE}/corpus/instruments/recheck-audit.py at write time>` (compute
   with sha256sum; also print the base digest c3c19adc... = pre-change bytes as a control line).
2. `selftest cases=15 failures=0 exit=0` after running `python3 {LANE}/corpus/instruments/recheck-audit.py
   --selftest` (must pass; if any fixture fails, quote the failing lines verbatim and do not claim 0).
3. The live lane audit line: `python3 {LANE}/corpus/instruments/recheck-audit.py --json {R26}/c1-live.json
   --cdroot {LANE}` output summary (lines/total/pass_strict/exit).
4. A note line correcting the round-25 cross-reference: the old index had no selftest line at :4
   (wave2/C1InstrumentDigest.md said otherwise); this index carries the selftest receipt at the new
   digest. Do NOT edit the round-25 files.
Also write {R26}/c1-instrument-digest.txt with the new sha256 (and the old digest note). Report the
receipt's exact lines."""),
    "e4": dict(role="executor", axes=["depth:verifiability"], milestone="SKILL.md gate registry row",
        task=f"""Add to {LANE}/SKILL.md (SOLE OWNER of SKILL.md edits this round) a section
`## Gates & probes registry` (place after the instruments/checklists area, before the final tables):
a table with columns | name | type | entry command | verdict map | self-test | pinned-value path |
write scope | owner |, and ONE row for recheck-audit.py: name `recheck-audit.py`, type `gate|probe`,
entry `python3 corpus/instruments/recheck-audit.py [--json <out>]`, verdict map `0 clean | 1 failed |
undeclared nonzero -> could-not-evaluate`, self-test `python3 corpus/instruments/recheck-audit.py
--selftest` (spelling `--selftest`), pinned-value path `.ufo/waves/round-26/c1-receipt-index.txt`,
write scope `corpus/` read-only + its own receipt dir, owner `kasegi`. Add one sentence noting the
expected-list contract (deletion = red audit). Do not touch any other section. Report the diff lines
added."""),
    "e5": dict(role="executor", axes=["coverage"], milestone="S041 capture",
        task=f"""Capture the JPCERT/CC 2026 partnership guideline into the lane snapshot tree:
`python3 {LANE}/corpus/instruments/capture-source.py --id S041 --url
https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf --out
{LANE}/corpus/source-snapshots/round-26/S041.txt`
Record exit, sha256, fetched_bytes, snapshot_bytes, utc. Verify the snapshot contains the division-of-
labour paragraph and the 図1 caption (grep for "社内での脆弱性取扱" and "出所：ISO/IEC 29147:2014 を元に作成")
and report line numbers. Sole owner of corpus/source-snapshots/round-26/S041.txt. Do not create the
manifest (e6 owns it). Report the capture log line verbatim."""),
    "e6": dict(role="executor", axes=["coverage"], milestone="manifest + quote recheck",
        task=f"""Build {LANE}/corpus/source-snapshots/round-26/manifest.json (SOLE OWNER): follow the
existing manifest schema used by `source-recheck.py` (read an existing manifest in
corpus/source-snapshots/round-25/ first). Include entries for S041 (snapshot S041.txt, sha256 from the
capture) and S040 (snapshot S040-live.txt if present, else skip and note). Then run quote verification:
`python3 {LANE}/corpus/instruments/source-recheck.py --manifest {LANE}/corpus/source-snapshots/round-26/manifest.json
--source S041` after adding to the manifest the exact quotes to check (≤70 chars each, taken from the
captured text lines):
- "ISO/IEC 30111:2013 はベンダの社内での脆弱性取扱いのプロセス（脆弱性の検証、脆弱性対策の開発等）の指針を提供します。"
- "脆弱性公開ポリシーには、ベンダへの連絡方法、セキュアな通信オプション" (verify which line exists; quote a shorter
  contiguous fragment if this exact one is absent — record what you used)
- "P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません"
- "受信した旨を 7 日以内に返信することが必要となります。"
- "6.2 Minimum policy aspects"
Record pass/fail per quote and the final exit status in {W1}/e6-recheck-results.txt. If any quote
fails, output the actual snapshot context line and correct the quote to the real bytes (report the
correction). Do not edit S041.txt."""),
    "e7": dict(role="executor", axes=["coverage"], milestone="mirror census gate (pre-append)",
        task=f"""Build a scratch mirror of the lane (copy corpus/ + SCORECARD.md + NOTHING under
.ufo/waves) to /tmp/kasegi-r26-mirror; run the sources census against it:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <mirror> kasegi` and record
exit. Also run the census against the live lane and record exit. Then create the do-nothing control
receipt for C2: `corpus/README.md` frontier count (awk from claims.json) and
`grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l` (expect 0) — write both to
{R26}/c2-controls/do-nothing.json (JSON with the two counts + census exits). Report all receipts."""),
    "e8": dict(role="executor", axes=["depth:verifiability"], milestone="frontier recheck integration check",
        task=f"""Verify `frontier-recheck-count.py` integrates the future F11 row without breaking:
read the script (corpus/instruments/frontier-recheck-count.py), explain how it counts entries per
frontier row, then simulate: on a scratch copy of corpus/README.md, add a temporary F11 row (copy of
an existing admitted row with a unique placeholder name) and run the script against the scratch; record
the before/after counts and exit. Do NOT modify the real corpus/README.md (scribe w4 owns it). Report
the simulation outputs in {W1}/e8-frontier-sim.txt. Also run the script on the live map and record its
exit and per-row counts."""),
    "w1": dict(role="scribe", axes=["coverage"], milestone="SOURCES append block",
        task=f"""Append to {LANE}/corpus/SOURCES.md (SOLE OWNER of SOURCES.md edits this round) the new
row for S041 = JPCERT/CC 2026 partnership guideline (title 情報セキュリティ早期警戒パートナーシップガイドライン
2026年10月; source https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf; category spec; grade A;
read = 付録6 §2 p.45 + §4 p.46-47 + 参考1 p.53-54; recheck = `180d — re-fetch with capture-source.py
instrument UA (browser UA 403s); canonical anchor is the PDF`; used-by = the two new F11 entries, both
drafted by w2/w3). Format must match the existing registry columns exactly (check row R9/R10 rules in
QUALITY.md). Also update the S040 row's recheck cell old->new (log the old value in a `## Registry
changes` note at the bottom: old recheck cell -> new cell including `final URL
https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html (2
redirects); instrument UA required (browser UA 403s)`). Do NOT alter any other row. Only append rows
that the admitted entries cite (S041). Report the exact appended lines."""),
    "w2": dict(role="scribe", axes=["coverage"], milestone="F11 entry: division of labour",
        task=f"""Create {LANE}/corpus/knowledge/iso-29147-and-30111-division-of-labour.md (SOLE OWNER)
satisfying QUALITY.md Q1-Q9: opens with headers `source: S041`, `verified-at: 2026-10-25`,
`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py
--manifest corpus/source-snapshots/round-26/manifest.json --source S041`. Content: the division of
labour between ISO/IEC 29147:2014 (vendor's outward-facing handling: receiving reports, advisory
distribution) and ISO/IEC 30111:2013 (internal verification/mitigation processes), grounded in quotes
(≤70 chars each) from the captured S041 snapshot (division paragraph line ~1670-1671; figure 1 caption
~1678), plus supporting evidence from already-mined lane rows: S039 (Hitachi's three-step mapping to
29147:2014/30111:2013) and S040 (Cisco citing 29147:2018). Include a `## Source` block with each
quote's location (`S041.txt:<line>`). Keep the entry focused and load-bearing: no invented claims, no
extra sources, no claims beyond the quotes + mined rows. Write a one-line `## Ground` note that this
adopts staged entry iso-29147-and-30111-division-of-labour-2026-10-23.md re-grounded. Report the file
created + line count."""),
    "w3": dict(role="scribe", axes=["coverage"], milestone="F11 entry: crosswalk",
        task=f"""Create {LANE}/corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md (SOLE OWNER)
satisfying Q1-Q9: headers `source: S041`, `verified-at: 2026-10-25`, `recheck:` = `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041`. Content: the JPCERT/CC P-guideline's own account of where it differs from ISO/IEC 29147:2014 — it does not require a vendor to adopt a disclosure policy (quote "P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません"), while 29147:2014 does (quote "ISO/IEC 29147:2014 では、脆弱性公開ポリシーを策定することや、その一部を公開することが必要"); the 7-day acknowledgement recommendation (quote "受信した旨を 7 日以内に返信することが必要となります。"), and the 6.2/6.3 minimum/optional policy aspects republication; note the 参考1 clause cross-reference table (p.53-54). Each quote located at `S041.txt:<line>`. Also reference S040 (Cisco's policy as a real-world example of a 29147:2018-aligned disclosure policy). One-line `## Ground` note: adopts staged entry iso-29147-divergence-and-clause-crosswalk-2026-10-23.md re-grounded. Report file + line count."""),
    "w4": dict(role="scribe", axes=["coverage"], milestone="corpus README map + F11 row",
        task=f"""Update {LANE}/corpus/README.md (SOLE OWNER): (1) add frontier row F11 (name: ISO/IEC 29147/30111 division-of-labour meta) to the coverage table with state `admitted` and entries linking to the two new knowledge entries; (2) update the frontier section per the repo's frontier rules (replace the decision text describing the next frontier with F11 as now admitted and the next frontier (F12) per the frontier logic — if the frontier logic requires the *next* frontier to be named, follow the pattern used in prior rounds; otherwise just mark F11 admitted). Do not change any other row. Report the diff lines. Verify the frontier counter from claims.json would now yield 11 after your edit (run the awk command on your own edited copy — record the result)."""),
    "w5": dict(role="scribe", axes=["depth:verifiability"], milestone="lesson round-26",
        task=f"""Compose {LANE}/corpus/lessons/round-26.md (SOLE OWNER), the round-26 lesson, matching
the house lesson format (see round-24/round-25 lessons). Required blocks:
1. ## Overview — round, date, base commit, claims C1/C2 and their counters.
2. ## Gate — admits: the two new knowledge entries (+ their staged adoption ids) and S041 row; rejects
   from the assimilation set: vendor-cvd-policy-crosswalk-2026-10-23.md (ground F20 absent, Q7 prose
   recheck, Q3 four-vs-two conditions — carry the round-25 verifier's reasons) and
   chinese-criminal-thresholds-and-authorisation.md (refused round 24; reason + flip retained); each
   reject carries a flip condition. Include the quarantine verdicts for the seven slice rows (from
   s4). Include the kill-rule status for C1/C2.
3. ## Mistakes — everything learned this round, including the R25-1..R25-5 routed defect fixes and how
   this round complied (claims.json frozen at commit 1b076fa7 BEFORE any measurement; corrections land
   as separate appended files).
4. ## Fixes that can fail — list each fix + a control that would catch its re-introduction; #3 must
   be the RESTATED fix-control: `grep -rnE '62 assertions\\|77 assertions' corpus/instruments/README.md
   SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l` → 0 hits (exclude the
   retained historical line; run it and record the 0). Include the deletion-mutant control (a deleted
   knowledge entry must make `recheck-audit.py` exit 1).
5. ## Appendix — counters with their exact commands; confirmation and kill rules; access-date evidence.
Do NOT relax any Q/R bar. Report the file + its line count; record the fix-control grep output."""),
    "w6": dict(role="scribe", axes=["depth:verifiability"], milestone="SCORECARD update",
        task=f"""Update {LANE}/SCORECARD.md (SOLE OWNER) per its house rules: (1) set depth:verifiability
score row evidence pointer to the round-26 gate receipt (.ufo/waves/round-26/c1-receipt-index.txt) and
last-change round 26 (score stays 4; the round proves gate conformance, not a higher score); (2) set
coverage row evidence pointer to the F11 admission (corpus/README.md) and last-change round 26 (score
7); (3) update `planned` rows: remove the executed r26 plans, add a plausible r27 plan row (do not
invent scope; a short placeholder honoring the frontier logic is fine — mark it as plan, not commit);
(4) if any capability row needs the new PDF capture path (capture-source.py --kind pdf already exists —
record as evidence only if not already), update accordingly. Report the diff lines and the exact
counter commands you used."""),
    "w7": dict(role="scribe", axes=["coverage"], milestone="LOG + PROVINCE maintenance",
        task=f"""Append to {LANE}/LOG.md (SOLE OWNER) the round-26 entry: date, commit base, claims
C1/C2, admitted F11, tools touched (recheck-audit.py expected-list contract; capture-source.py pdf
kind), and the gate/verdict lines. Also check {LANE}/PROVINCE.md: if its frontier sentence or surface
list mentions the F10 frontier only, append the F11 sentence (one line: `F11 — ISO/IEC 29147/30111
division-of-labour (JPCERT/CC 2026 guideline) — admitted round 26`). Do not alter anything else in
PROVINCE.md. Report the appended lines."""),
    "m1": dict(role="mutation-tester", axes=["depth:verifiability"], milestone="C1 deletion-mutant controls",
        task=f"""Build the C1 control receipts on the CURRENT (pre-fix) instrument bytes. Create scratch
fixture trees (copy of the lane's corpus) and run `python3 {LANE}/corpus/instruments/recheck-audit.py
--root <fixture> --cdroot {LANE}` on each:
- mutant A: delete one whole knowledge entry file (e.g. cnvd-canonical-advisory-cross-references-2026-10-23.md)
  from the fixture (keep everything else) → record exit + lines/total.
- mutant B: delete the recheck line from one entry (expected: exit 1 via completeness) → record.
- mutant C: rename one knowledge file (slug change) → record exit.
- mutant D: add a stray extra knowledge file without recheck line → record exit.
- mutant E: base copy with no changes → record exit (must be 0 if all lines pass; note any failures
  verbatim — if the base audit FAILS, say so: the base tree may have a non-passing line).
Write each run's raw output to {R26}/c1-controls/m1-*.txt and a JSON summary {R26}/c1-controls/m1-summary.json.
These are the do-nothing (pre-fix) receipts for C1. Also compute `sha256sum` of the CURRENT instrument
bytes and record (expect c3c19adc...).
Do not edit production files."""),
    "m2": dict(role="mutation-tester", axes=["depth:verifiability"], milestone="gate registry row mutants",
        task=f"""On a scratch copy of SKILL.md, mutate the planned registry row in ways a lazy writer
might ship: (a) row without verdict map; (b) type `gate` without `|probe`; (c) self-test flag spelled
`--self-test`; (d) missing pinned-value path; (e) row present but name typo'd. For each mutant, run the
counter command from claims.json (`grep -cE '^\\| [^|]+\\| gate\\|probe '`) and record whether the
counter still matches the row (determinism check). Output {R26}/c1-controls/m2-registry-mutants.txt
with per-mutant grep output. Read-only on the real SKILL.md."""),
    "m3": dict(role="mutation-tester", axes=["depth:verifiability"], milestone="counter gameability probes",
        task=f"""Attempt to satisfy each C1/C2 AFTER value with minimal cheat work (do this on scratch
copies / receipts only, never production): for C1, can you produce a `selftest cases=15 failures=0`
line without running selftest? Can `--expect` be pointed at an empty file to make `missing=[]` while
entries vanish? For C2, can `F11 admitted` be written while the new entries are empty shells citing
S041? For each probe report whether the frozen counter (as written in claims.json) would still catch it
or not, and note any counter weakness in {R26}/c1-controls/m3-gameability.txt + {R26}/c2-controls/m3-gameability.txt.
No production edits."""),
    "k1": dict(role="critic", axes=["depth:verifiability"], milestone="C1 vacuity attack",
        task=f"""Attack the C1 claim for vacuity: (1) Could the registry row appear without any real
gate behavior (i.e. is the AFTER counter (`grep -cE ...`) satisfied by a decorative row)? If yes, say
what additional committed evidence makes it non-vacuuous (e.g. the recipe must also run) — propose it
as a NOTE for the round report (do NOT change claims.json). (2) Is the deletion fixture robust: does
`lines/total` counting plus expected-set equality catch BOTH full deletion and rename? Trace the
predicted behavior of the e1 change (--expect) against mutants A/C/D from m1 and confirm or falsify.
(3) Does the fix-control #3 restatement interact correctly with the retained historical line? Run the
restated grep command yourself and record the output. Output {W1}/k1-vacuity.txt. Read-only/scratch
only."""),
    "k2": dict(role="critic", axes=["coverage"], milestone="C2 vacuity attack",
        task=f"""Attack the C2 claim for vacuity: (1) Could `F11 admitted` + `entries citing S04x`
be satisfied while the new entries contribute no actual learning (empty shells, quotes that duplicate an
existing entry)? Check the planned entries' stated content against the existing corpus for duplication
(vendor-disclosure-policy-commitments-crosswalk etc.). (2) Is `grep -lE '^source: S04[0-9] '` a fair
counter for `source row first registered this round`? Test the awk/grep command on a scratch registry
with two S04x rows and confirm behavior. (3) Does admitting F11 break any existing frontier row
counting (frontier-recheck-count.py)? Simulate on a scratch copy. Output {W1}/k2-vacuity.txt. No
production edits."""),
    "k3": dict(role="critic", axes=["depth:verifiability"], milestone="no-harm review",
        task=f"""Review the planned round-26 changes for harm to other axes and invariants: (1) does
the recheck-audit.py change (--expect) affect the round-25 claims' receipts retroactively (it must
not — the change is forward-only; verify the round-25 receipt files are untouched)? (2) does the
SOURCES.md S041 append + S040 recheck-cell update preserve the census invariant (run the census on a
scratch copy after simulating the append)? (3) does adding two knowledge entries + F11 row break any
README invariants (frontier row count, entries-per-row sums)? (4) check that no seat's write scope
overlaps another (consume c4's ownership matrix). Output {W1}/k3-noharm.txt with verdicts. No edits."""),
    "r1": dict(role="revenger", axes=["depth:verifiability"], milestone="r25 instrument digest lineage",
        task=f"""Reverse-engineer the round-25 receipt lineage to pin the exact digest mismatch:
1. Reconstruct the recheck-audit.py bytes at the round-25 tip (git show 41a77b8:corpus/instruments/recheck-audit.py
   or the r25 branch tip) and compute sha256 — compare with c1-instrument-digest.txt (c3c19adc...).
2. Show that the current working-tree bytes match the round-25 committed bytes (sha256 equal) — i.e.
   no silent drift before this round's e1 change.
3. Pull .ufo/waves/round-25/c1-receipt-index.txt line 4 and quote it; confirm it has no selftest line;
   note the wave2/C1InstrumentDigest.md cross-reference claim and its contradiction.
4. Summarize exactly what the round-26 receipt must contain to fix the cross-reference (index line
   carrying `selftest cases=15 failures=0 exit=0` + new digest) and which round-25 files must remain
   untouched.
Output {W1}/r1-digest-lineage.md with hashes, quoted lines, and commit ids. Read-only."""),
    "r2": dict(role="revenger", axes=["depth:verifiability"], milestone="S040 redirect fingerprint",
        task=f"""Reconstruct the S040 fetch history: pull the round-25 verifier spotcheck's record (the
301→200/UA note), the capture log line from round-25 (corpus/source-snapshots/round-25/capture-log.txt
if it exists — else find the S040 snapshot record), and today's s2 probe. Reconcile: canonical URL →
301 → final URL under instrument UA; browser UA → 403. Produce a one-page fingerprint file
{W1}/r2-s040-fingerprint.txt with the exact curl output lines and the final URL + UA requirement
phrasing that should appear in the S040 recheck cell (for w1) and in the round-26 lesson. Read-only."""),
    "n1": dict(role="sentinel", axes=["depth:verifiability"], milestone="scope sweep",
        task=f"""End-of-wave scope sweep (read-only): (1) list files modified/created in the lane since
base committed 1b076fa7 using `git status --porcelain` + `find .ufo/waves/round-26 -newer <claims-commit>`
(report the working-tree status), and check each changed path belongs to the ownership matrix (c4);
(2) confirm no writes under /home/vgpnk/Projects/shokunin (fleet root), /home/vgpnk/Projects/shokuknow,
or any sibling lane; (3) confirm no VCS mutation happened (git log unchanged: HEAD still 1b076fa7,
working tree has uncommitted expected files). (4) verify claims.json bytes match the freeze commit
(`git show 1b076fa7:.ufo/waves/round-26/claims.json | sha256sum` vs current file). Output
{W1}/n1-sweep.txt. Read-only — run this LAST in the wave."""),
    "n2": dict(role="sentinel", axes=["coverage"], milestone="contract compliance check",
        task=f"""Check the round deliverables contract: (1) presence of the promised artifacts — the
two new knowledge entries, SOURCES append block with S041, corpus/README.md F11 row, lesson round-26,
SCORECARD update, LOG entry, c1-receipt-index.txt, c1-controls/*, c2-controls/*, wave1 reports;
(2) for each, check it exists and is non-empty; (3) run the C2 counter commands as they stand
(`awk ... corpus/README.md` → expect 11 after w4; `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l`
→ expect >=1) and the C1 counter commands (SKILL.md registry row grep → expect >=1; selftest line grep
→ expect 1) and record outputs; (4) if any artifact is missing or counter fails, list it as a gap for
the L1 (no fixes). Output {W1}/n2-contract.txt."""),
    "x1": dict(role="simplifier", axes=["depth:verifiability"], milestone="YAGNI audit of wave artifacts",
        task=f"""Audit the wave-1 drafts for YAGNI (no production edits): scan the new files created by
the wave (knowledge entries, lesson, SOURCES append, SCORECARD diff, registry row, expected list) for
(1) duplicated/redundant blocks that add no load-bearing value, (2) placeholder or empty sections, (3)
over-wide claims that exceed the committed evidence, (4) reuse of prior round patterns that are now
dead (e.g. references to retired instruments). Produce a checklist with per-file suggestions —
{W1}/x1-yagni.txt. The L1 may apply your suggestions only if they keep the claims' counters intact.
Read-only."""),
}

if __name__ == "__main__":
    spec = {
        "wave": "kasegi-r26-build",
        "context": CONTEXT,
        "reportDir": W1,
        "maxLanes": 64,
        "axes": ["depth:verifiability", "coverage"],
        "milestone": "round-26 build wave: C1 gate conformance + C2 F11 assimilation",
        "items": [],
    }
    order = ["s1","s2","s3","s4","s5","c1","c2","c3","c4",
             "e1","e2","e3","e4","e5","e6","e7","e8",
             "w1","w2","w3","w4","w5","w6","w7",
             "m1","m2","m3","k1","k2","k3","r1","r2","n1","n2","x1"]
    camels = {"s1":"ScoutDatawalk","s2":"ScoutS040Probe","s3":"ScoutPackageInventory",
              "s4":"ScoutQuarantine","s5":"ScoutQuoteRelocation",
              "c1":"ConnOverlap","c2":"ConnR25Continuity","c3":"ConnUsedbyMap","c4":"ConnOwnership",
              "e1":"ExecAuditFix","e2":"ExecExpectedList","e3":"ExecReceiptIndex","e4":"ExecSkillRegistry",
              "e5":"ExecCaptureS041","e6":"ExecManifestRecheck","e7":"ExecMirrorCensus","e8":"ExecFrontierSim",
              "w1":"ScribeSourcesAppend","w2":"ScribeEntryDivision","w3":"ScribeEntryCrosswalk",
              "w4":"ScribeReadme","w5":"ScribeLesson","w6":"ScribeScorecard","w7":"ScribeLogProvince",
              "m1":"MutDeletionControls","m2":"MutRegistryRow","m3":"MutGameability",
              "k1":"CritVacuityC1","k2":"CritVacuityC2","k3":"CritNoHarm",
              "r1":"RevDigestLineage","r2":"RevS040Fingerprint",
              "n1":"SentScopeSweep","n2":"SentContract","x1":"SimplYagni"}
    for key in order:
        it = ITEM[key]
        spec["items"].append({
            "name": camels[key],
            "role": it["role"],
            "axes": it["axes"],
            "milestone": it["milestone"],
            "prompt": it["task"],
        })
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wave1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=1)
    print("wrote", out, "items:", len(spec["items"]))
