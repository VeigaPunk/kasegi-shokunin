# R46W2ConnClaimsConsistency — cross-artifact consistency of the round-46 integrated tree

VERDICT: BROKEN

Scope: the tip commit 5437afeaf9b642c267bba3c31f00ae701e49da68 (export replayed in scratch; lane working tree tracked files equal it: `git status --porcelain | grep -v '^??'` printed nothing). Base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba (pure export `/fast/scratch/hyaku/kasegi-r46/L1/pure`, and a clean `git archive` of the same corpus used for the final replay). Freeze 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 (archive replayed for the freeze readings).

The numeric claims re-derive at the tip and at the base (section A). The text-level cross-artifact statements do not all agree (section B): one frozen claim names an artifact that does not exist at the tip, the committed control file is the v1 output and is not the v1.1 reading that wave-1 reports cite, two counter docstrings contradict their code or their own version label, and the errata's plain re-derivation covers only part of the limbs it rules on. None of these moves a counter reading; they are what the L1 must fix before closure.

## A. Re-derived (HOLDS)

Commands run in my scratch; output quoted.

A1. Frozen claims and counter bytes
```
e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740  .ufo/waves/round-46/claims.json      (tip)
e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740  claims.json at 9f23aab (git show | sha256sum)
b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294  r46-c1-gate.py at 9f23aab (v1)
0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6  r46-c2-gate.py at 9f23aab (v1)
99e0ee555b68e5177f33e49e8024469608297a412171b190f66b1bba189475cc  corpus/instruments/r46-c1-gate.py (tip, v1.1; errata matches)
b52fea3183a393fa2f5bb40879241034e9db0b45f7914244d9f3bed134958621  corpus/instruments/r46-c2-gate.py (tip, v1.1; errata matches)
66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  S073.txt (tip = freeze.txt S073-sha256 = S073 row = PINS)
01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34  manifest.json (tip = freeze.txt = PINS)
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  source-recheck.py (tip = PINS)
```
All of these agree with claims.json, freeze.txt, counter-errata.md and the counter PINS. The claims file is byte-identical at the tip (sha above).

A2. Freeze-check replayed at the base with the v1.1 counters (the requested command, base = clean archive of the base corpus):
```
claim C1 base_read=c1-gate fixed=1/7 exit=1 verdict=ok
claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok
freeze-check claims=2 base_ok=2 exit=0
```
(The same run against the pure export copy, which carries an extra untracked `corpus/instruments/__pycache__` that is not in the base commit, printed the same three lines.)

A3. Counters at the tip (run from the tip export, `--baseline` = base export):
```
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-exact=2
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=46 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```
Counters at the base (the do-nothing control): C1 `fixed=1/7 exit=1` (L1 `gated=24 broken=0 lines=64/base=64`), C2 `fixed=1/7 exit=1` (only G7). Counters on the freeze tree: C1 v1 and v1.1 both `c1-gate fixed=1/7 exit=1`; C2 v1 and v1.1 both `c2-gate fixed=2/7 exit=1` (G4 + G7), matching the claims' `freeze_tree_reading` for both.

A4. The v1 C2 counter on the tip tree reads `c2-gate fixed=6/7 exit=1` (`gate G6 pass=0 read=knowledge=65 base-names-intact=0 entry-bytes-ok=1`). This reproduces errata E1 and wave-1 `R46ConnSeparable.md` T12.

A5. Plain numbers (the claims' `plain` list and the errata's re-derivations), tip vs base:
```
base: grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l  -> 23
tip : same -> 21
base: recheck-audit.py --root . --quiet | grep '^executes='  -> executes=40 gated=24 broken=0
tip : -> executes=43 gated=22 broken=0      (errata: "executes=43 gated=22 broken=0")
base: score-gap.py | grep '^gap:' -> gap: 24 of 64 rechecks still gated on a lost base ...
tip : -> gap: 22 of 65 rechecks still gated on a lost base ...
base/tip: grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 27 / 28
base/tip: SOURCES S-rows -> 72 / 73
base/tip: knowledge *.md -> 64 / 65
base: grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md -> (no output)
tip : -> corpus/knowledge/github-private-vulnerability-reporting.md, corpus/SOURCES.md, corpus/README.md
tip : plain-rows.sh claim-gates.md -> rows=25 located=25 ; claim-package-contract.md -> rows=21 located=21
tip : grep -cE '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate\.py --entry corpus/knowledge/(claim-gates|claim-package-contract)\.md( +#.*)?$' -> 1 and 1
tip : restoration-recheck diff vs base recheck (sed-prefix-swapped): no output for both entries (identical)
tip : git diff --numstat base -- claim-gates.md claim-package-contract.md -> 36 1 / 30 1 (one deletion each = the replaced recheck line)
tip : r44-frontier-count.py --root <tip> --expect 28 -> "frontier rows=28 admitted=28", exit 0
base: r44-frontier-count.py --root <base> --expect 28 -> "frontier expected=28 admitted=27 verdict=SHORT exit=1"   (claims' secondary: rows=27 admitted=27 exit 1)
tip : source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 -> "S073:sha256 OK" + S073:Q1..Q8 OK, exit 0
```
Every number matches the claims' `before`, `after`, `plain` and `secondary` fields and the errata's re-derivation block.

A6. S073 capture and row (the line-number and sha claims):
```
wc -l -c S073.txt -> 589 15568
L556 "Privately reporting a security vulnerability"; L564 "...You can only report vulnerabilities privately for repositories where this feature is enabled."; L573 "By default, you must provide a summary, details, proof of concept, and impact statement."; L575 "At the bottom of the form, click Submit report..."; L578 "Optionally, click Start a temporary private fork ... only the repository maintainer can merge changes from that private fork..."; L583 "YesNo"
manifest: fetched_utc 2026-10-28T22:56:49Z, http {'status': 200, final_url == row URL}, bytes 577188, snapshot_bytes 15568, lines 589, quotes = 8 (anchors 560,563,564,566,573,574,577,578)
```
Matches the S073 row (`body lines 556-583`, `sha256 66c96a…1930`, `589 lines, 15568 bytes`, `manifest raw 577188 bytes`, `fetched 2026-10-28T22:56:49Z, HTTP 200`).

A7. The F28 entry's cross-references resolve in the cited sense: the entry cites `ai-assisted-finding-validation.md:7-8` for the reviewer-distinct rule (line 31); lines 7-8 of that file state "For Kasegi claim-ready status, the package must identify the reproducing evidence and a reviewer distinct from its producer". The entry's quote "anyone can submit a private vulnerability report to the repository maintainers" (cited `S073.txt:565`) is the verbatim sed 565 line.

A8. Controls (the kill rule's "any control grades 7/7"): I re-ran `controls/freeze-controls.py --lane <lane> --base 914ca0b6… --work <scratch>` at v1.1. Last line printed: `controls total=9 red=9 green=0` (EXIT=0). No control is green.

A9. Instruments vs knowledge directory: `knowledge-expected.txt` lists 65 `corpus/knowledge/*.md` lines; the set equals the tip's `ls corpus/knowledge/*.md` (the only diff is the order of `ev-model.md` vs `evidence-dir.md` under the locale sort, not a set difference). Base file: 64 lines. Its single tip change (`git diff --stat` 1 insertion) adds the F28 entry; the claims do not list this file, but the change is consistent.

## B. Disagreements and stale statements (each re-checked by a command above or below)

B1. (claims.json `frontier_step`) "mined mistake in corpus/lessons/round-46.md ## Mistakes". At the tip the file does not exist: `ls corpus/lessons/round-46.md` → `No such file or directory`; `git ls-tree --name-only 5437af… corpus/lessons/ | grep -i 46` → nothing; `ls corpus/lessons | grep 46` → nothing (only `round-45.md`, `round-45-verifier-spotcheck.md`). The other frontier_step references hold: `considerthese/2026-10-26.md` proposal 3 is "Add a quiescence gate before `complete`" (line 31), and the S072/S070 supersede note is in `corpus/SOURCES.md` (line 162). So a frozen claim cites a closure artifact that the tip does not yet have. Either write it at closure or state it as pending.

B2. `.ufo/waves/round-46/controls/freeze-controls.txt` is the v1 output (file mtime 20:02, labels `recheck-lines-clean`, `entry-mode-green`, `base-names-intact`), not a v1.1 reading. Diff of the committed file against my v1.1 re-run (`diff <(grep -E '^==|fixed=|controls total' committed) <(grep … rerun)`):
```
4c4  < c1-gate fixed=3/7 exit=1   ---  > c1-gate fixed=2/7 exit=1     (c1 marker-only)
10c10 < c1-gate fixed=6/7 exit=1  ---  > c1-gate fixed=0/7 exit=1     (c1 gutted-entry)
14c14 < c2-gate fixed=4/7 exit=1  ---  > c2-gate fixed=3/7 exit=1     (c2 junk-row)
16c16 < c2-gate fixed=4/7 exit=1  ---  > c2-gate fixed=3/7 exit=1     (c2 fabricated-quote)
18c18 < c2-gate fixed=5/7 exit=1  ---  > c2-gate fixed=4/7 exit=1     (c2 uncited-filler)
```
The kill rule still holds (9 red, 0 green). But `freeze.txt` and the wave-1 reports cite these numbers as the frozen controls: `R46CritCalibration.md:87` ("Negative controls (frozen, rerun): C1 marker-only fixed=3/7, gutted-entry fixed=6/7; C2 junk-row 4/7, fabricated-quote 4/7, uncited-filler 5/7") and `R46RevC2G3.md:55` (`c2 junk-row … c2-gate fixed=4/7`). Those are v1 readings; at v1.1 they are different. The committed control file needs regenerating or the reports need the v1 label. Note also the v1.1 marker-only control prints `gate L1 pass=0 read=gated=22 broken=2` (the `true` lines are now `broken`), which is the intended v1.1 behaviour but is not what the committed file records.

B3. C2 docstring, G6 sentence (r46-c2-gate.py line 30, unchanged since v1 — the v1 file has the identical line 30): "`find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 65 and the other 64 files are the round-46 tip's bytes." The v1.1 code does not pin tip bytes. It pins the BASE content hash (`PINS["base-knowledge-content"] = 5e0796…`) over `base_like` minus `CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md"}` (62 files). The errata C2-E5 says exactly this ("the byte pin covers 62 base entries"), so the errata and the code agree and the sentence does not. Under the errata's own rule (the sentence made literal), this change is not logged as a sentence change: the sentence was left as-is and the code departs from it. Reproduce: `diff <(git show 9f23aab:corpus/instruments/r46-c2-gate.py | sed -n '1,/^"""$/p') <(sed -n '1,/^"""$/p' corpus/instruments/r46-c2-gate.py)` prints only the header line (2c2), i.e. G6's sentence is byte-identical to v1's.

B4. C2 docstring line 8: "(the limbs carry the round-46 **v1.2** hardening: real tables only, pinned captures, …)". The file header, the claims and the errata say v1.1 (`grep -n "v1.1\|v1.2" corpus/instruments/r46-c2-gate.py` → lines 2 and 8). Stale version label.

B5. Errata C2-E1 (G2): "each section carries >= 25 words (the package rule >= 12)". Code: `full = sum(1 for sct in SECTIONS if sect_words(body, sct) >= (12 if sct.startswith("## Falsifiable") else 25))`. The Falsifiable section is held to 12, not 25. The errata sentence says every section is held to 25, so either the errata or the code is wrong. The code is what runs (`full=4/4` at tip).

B6. Errata "Decision" (point 1) says the C1 limb sentences "changed only where … the sentence made literal". Diff of the C1 docstring v1 → v1.1: L1 and L2 unchanged; L3, L4, L5, L6, L7 rewritten (e.g. v1 L5 "every BASE line except the recheck line is, in order, a prefix of TREE's" → v1.1 "… and the BASE recheck command survives verbatim as one `restoration-recheck:` line"; v1 L7 "keep their BASE recheck line byte-identical" → v1.1 "are byte-identical to BASE"). The kill rule's parenthesis covers "bug fixes that keep a limb's sentence" and requires "a plain re-derivation that does not use the counter". The errata's plain section covers L3 (shape, `1 and 1`), L5 (restoration identity, numstat deletion 1) and L1 (executes/gated). It does not re-derive L2 (regrounded set), L4 (anchors byte-identical to BASE), L6 (load-bearing, blanking tokens) or L7 (still-gated entries byte-identical). `plain-rows.sh` checks only that each token is a fixed substring of its range (`located`), which is weaker than L6's blank-and-red test. So the plain re-derivation the kill rule requires is partial for C1.

B7. Errata has no plain re-derivation for any C2 change. The C2 limb changes (G2 structure and words, G3 cell rules, G5 cite-range and body 556-583, G6 pin, C2-E1…E5) are logged with `forced by` columns but their plain section is absent; the claims' own `plain` list for C2 covers only G1 (rows), G3-count (S-rows), G4 (`source-recheck`), G6-count (65), and the F28 grep. G2, G5 and G7 have no plain check. The counter is the only grader of those limbs.

B8. Claim C1 `after`: "every BASE line kept (append-only)". The implementation keeps every non-recheck BASE line and rewrites the one BASE `recheck:` line to `restoration-recheck:` (numstat: one deletion per entry). The rewrite is deliberate (errata C1-E3), and the `restoration-recheck` text equals the base text after the prefix swap (`diff` printed nothing), so the substance holds. But "every BASE line kept" literally is not true of the two re-grounded entries. A non-author reading should decide whether the wording or the rewrite is the intended contract; the errata does not mention the wording tension.

B9. Claim C2 `after`: "a stated contrast with F27 (AI-assisted finds) and F04". The entry contrasts F27 at line 30 (`linux-kernel-security-bugs-reporting-process.md:23 (F27)`) and the F04 entry by path at line 31 (`ai-assisted-finding-validation.md:7-8`). The label `F04` does not appear in the entry (`grep -n "F04" …` → none). Holds by path, not by label. Minor.

B10. README admission heading: `## Round-46 admission - coverage map row and Frontier F28 (appended 2026-10-28)` uses an ASCII hyphen (`od -c` at line 655 shows `-`). The round-45 heading (line 634) uses an em dash (`342 200 224`). Style drift only.

B11. C1 docstring output line: says `reground entry=X rows=<n> ok=<k> exit=0|1`; the code prints `reground entry=%s rows=%d ok=%d files=%d distinct=%d exit=%d`. Also the module docstring's allow-list list omits `set -o pipefail` (which `allowed()` accepts). Doc drift only.

B12. C2 G7 depends on `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, a fleet-root path outside the lane (the constant is in the docstring and the code: `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`). The claims and errata say "census exit 0" with no mention that the census script lives outside the lane. The counter reads `census-rc=0` only because that fleet file exists on this host. Recorded as a dependency, not a fault.

B13. Lane root: an empty, untracked directory `x` (`ls -la x` → `total 0`, mtime 14:19) exists in the lane working tree. Not in the commit; not created by this seat. The claim "lane working tree equals it" is true for tracked files only.

## C. Limitations

- I did not run the non-author semantic closure (does each row support its claim). B6/B7 are about the mechanical re-derivation only.
- I did not run the wave-1 mutation or selftest suites; I checked that the wave-1 phrases the errata cites exist (`R46RevC1L3.md` has the `true  # r46-c1-gate` pattern three times; `R46Revenger.md:57` has "Planted-anchor variant"; `R46MutC2a.md` S1-S4, `R46MutC2b.md` M07-M09/P1/P2/P4, `R46RevC1L6.md` findings 1-5, `R46CritKillRule.md` C1-a/b/c, `R46ExecSelftestC1.md` F1-F6 exist). I did not re-read every cited wave-1 finding for content.
- The census script (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) is outside the lane; I read its exit through the counter only.
- Host dependence: C1 L1 under the grader's HOME reads the same at base and tip only while `~/Projects/bounties` stays absent. Not re-tested.
- Background job `bg_24135` (v1 C1 on base) and `bg_24178` (recheck-audit at tip) completed; their outputs are above. Controls re-run used the lane's live `corpus/instruments` as tool root (read-only); fixture trees were scratch only.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46W2ConnClaimsConsistency` is removed on exit; nothing was committed, pushed, or written outside this Report file.
