VERDICT: BROKEN

# R46W2CritControlsV11 — Controls critic for counters v1.1 (round 46, falsify wave 2)

Scope: the two v1.1 counters (`corpus/instruments/r46-c1-gate.py`, `corpus/instruments/r46-c2-gate.py`) against the integrated tree at `5437afeaf9b642c267bba3c31f00ae701e49da68`. Counter runs were made from the lane (`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c1-gate.py ...`), against exported trees, with `--work` in scratch. The lane was not written to; no git mutation was run.

Setup, re-run by me:
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` printed `0d121a201fe7cc3d0604ceb7666d1a85a5bbc174`. That HEAD is `5437afe` plus one later commit (`0d121a2 round-46: wave 2 spec (33 seats, policy v1) and dispatch`). `git diff --stat 5437afe HEAD -- corpus .ufo/waves/round-46/claims.json` printed nothing, so the corpus and the frozen claims are byte-identical to `5437afe`. I exported `5437afe` with `git archive | tar -x` (tip).
- Base: a copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` (base). `git show 914ca0b:corpus/knowledge/claim-gates.md` and `corpus/README.md` `diff` clean against the copy.
- Integrated tip, run by me: `c1-gate fixed=7/7 exit=0` (`gated=22 broken=0`, `regrounded=2 claim-gates.md,claim-package-contract.md`, `mutants=46 survivors=none`) and `c2-gate fixed=7/7 exit=0` (`rows=28 admitted=28`, `table-rows=8 xrefs=4/4`, `spans=21 located=21`, `census-rc=0 ok-line=1`). So the integrated tree reads 7/7 under both counters, as stated in the errata.
- Do-nothing controls, re-run: base vs base `c1-gate fixed=1/7 exit=1`; base `c2-gate fixed=1/7 exit=1`.

Findings below each name the attacked thing, the command run, and the printed output (quoted). Every "7/7" is a re-run I performed. Probe trees are generated from the tip in scratch; the scratch is removed on exit, so each recipe is written out here in full.

---

## F1 — C1 (depth:verifiability): re-ground rows over one committed file via two spellings reads 7/7 — BROKEN

Attacked: `r46-c1-gate.py` limb L4 / `check_row` file counting. The frozen claim (`claims.json` line 12, C1 `after`) says each re-grounded entry carries rows "over >=2 committed files". The counter counts `files` as a set of raw path strings (`files.add(f)` at `r46-c1-gate.py:173-174`, the rel string returned by `check_row` at line 153; the rule `len(files) >= 2` at line 178). `check_row` never normalises the path, so `corpus/instruments/./claim-package-check.py` is a second "file" for the same bytes.

Recipe (tree P1 = tip with the `## Re-ground (round 46)` section of both entries replaced; the recheck and restoration lines untouched):
- claim-gates.md rows: six rows, anchors alternating `corpus/instruments/claim-package-check.py:<n>` and `corpus/instruments/./claim-package-check.py:<n>`, tokens = the stripped text of line n, for n in 101, 109, 116, 117, 119, 121 (single lines; each token is unique in the file, >= 8 chars, no backtick or pipe).
- claim-package-contract.md rows: the same construction over six lines taken from line 300 on.
- Probe rows as shipped (claim-gates.md, copied from the run):
```
| G1 | Entry claim restated for row 1 | `corpus/instruments/claim-package-check.py:101` | `SIX_FILES = (` |
| G2 | Entry claim restated for row 2 | `corpus/instruments/./claim-package-check.py:109` | `JSON_FILES = (` |
| G3 | Entry claim restated for row 3 | `corpus/instruments/claim-package-check.py:116` | `HEX64 = re.compile(r'^[0-9a-fA-F]{64}$')` |
| G4 | Entry claim restated for row 4 | `corpus/instruments/./claim-package-check.py:117` | `HEX_ANY = re.compile(r'^(?:[0-9a-fA-F]{7,64})$')` |
| G5 | Entry claim restated for row 5 | `corpus/instruments/claim-package-check.py:119` | `HTTPS_URL = re.compile(r'https://[^\s)\]<>"]+')` |
| G6 | Entry claim restated for row 6 | `corpus/instruments/./claim-package-check.py:121` | `NO_SUBMISSION = 'No submission performed'` |
```
Command: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c1-gate.py --root <P1> --baseline <base> --work <scratch>/tmp`

Output (printed):
```
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-exact=2
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
Per-entry (`r46-c1-gate.py --entry corpus/knowledge/claim-gates.md --root <P1>`): `reground entry=claim-gates.md rows=6 ok=6 files=2 distinct=1 exit=0`.

Discrimination: the same six rows, all on one spelling (`corpus/instruments/claim-package-check.py` only, tree P0), read `reground entry=claim-gates.md rows=6 ok=6 files=1 distinct=1 exit=1` and `c1-gate fixed=0/7 exit=1` (L1 `gated=24`, L2 `regrounded=0`). The one-spelling control is the freeze's `single-anchor-file` case; it fails; the two-spelling tree passes. The only difference between P0 and P1 is the spelling of one path.

Defect: one committed file is re-grounded as two anchor files. This violates the C1 `after` sentence ("over >=2 committed files"). The rows' tokens and anchors all come from one file.

Fix (for L1): normalise with `os.path.normpath` / `realpath` before `files.add`, and count distinct real files.

Limitation: the rows' claim text in P1 is placeholder; the file-count defect is structural and does not need the claim text.

---

## F2 — C1: rows whose only located token is a section heading (two real base captures) read 7/7 — BROKEN (semantic defect the counter cannot see)

Attacked: `check_row` / L6 accept any `<= 40`-line range that contains the token (`r46-c1-gate.py:145-153`). The base captures contain only headings in the range.

Recipe (tree P2b = tip, both entries re-grounded on heading lines, no spelling tricks):
- claim-gates.md: `corpus/source-snapshots/round-45/S071.txt` lines 3, 10, 73 (`Security bugs`, `Preparing your report`, `What qualifies as a security bug`) and `corpus/source-snapshots/round-44/S069.txt` lines 7, 29, 52 (`Services in scope`, `Qualifying vulnerabilities`, `Rules of Engagement: Disqualifying Actions & Boundaries`); each row `| G<n> | Entry claim restated for row <n> | `<file>:<line>` | `<token>` |`.
- claim-package-contract.md: S071 lines 109, 174, 254 and S069 lines 114, 231, 986.
- The S069 lines are markdown `## ` headings (`S069.txt:7` `## Services in scope`, line 29 `## Qualifying vulnerabilities`); S071 lines are RST-underlined headings (`S071.txt:3` `Security bugs`, line 10 `Preparing your report`).

Command: as F1, `--root <P2b> --baseline <base>`.

Output (printed):
```
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-exact=2
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
Per-entry: `reground entry=claim-gates.md rows=6 ok=6 files=2 distinct=1 exit=0`.

Discrimination: the base reads `c1-gate fixed=1/7 exit=1` (re-run). P2a (all six rows on S071 under two spellings) also reads 7/7, but it depends on the F1 spelling bypass. P2b (two real captures, no spelling variant) is the independent evidence and reads `c1-gate fixed=7/7 exit=0`. The per-entry line `row G6 ok=1 read=token-located` shows a heading token accepted as located.

Defect: every row's token is a section heading (no body sentence). The rows restate entry claims (for example "a claim-ready package contains six files") that a page title does not support. The counter accepts them. C1's kill rule assigns this judgment to a non-author reading ("the rows are the semantic check the counter cannot make"); the counter alone is not evidence of support.

Fix (mechanical part): reject tokens whose located lines are all headings (`^#`, or an underline line below), or require the token to lie in a non-heading line.

Limitation: the placeholder claim text makes the mismatch obvious. Against real claims the mismatch is semantic; the counter cannot detect it either way.

---

## F3 — C1 L7: a still-gated entry re-encoded to CRLF (body text unchanged) reads 7/7 — BROKEN

Attacked: L7 "entries gated at BASE and still gated at TREE are byte-identical to BASE" (docstring `r46-c1-gate.py:36`; the errata's E5 "still-gated entries are byte-identical to BASE"; the frozen C1 `after` ends "Entries still gated keep their BASE recheck line byte-identical."). L7 compares `read()` results (`r46-c1-gate.py:100-105`, `open(path, "r", encoding="utf-8")`, universal newlines), so `\r\n` is folded into `\n` (`gate_list`, L7 at lines 304-306).

Recipe (tree P3 = tip, `corpus/knowledge/citation-bases.md` (still gated at base and tip) rewritten with `b.replace(b"\n", b"\r\n")`; base copy has 0 CR bytes, P3 copy has 126):

Command: as F1.

Output (printed):
```
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-exact=2
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=46 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```

Discrimination (same tree, controls):
- body edit, one extra `\n` inserted into `citation-bases.md` (tree P3c): `gate L7 pass=0 read=still-gated=22 changed=citation-bases.md`, `c1-gate fixed=6/7 exit=1`. So L7 does catch body changes.
- BOM prepended to `citation-bases.md` (tree P8): `gate L7 pass=0 read=still-gated=22 changed=citation-bases.md`, `c1-gate fixed=6/7 exit=1`. Encoding change that keeps the BOM byte is caught.
- CRLF only (P3): `changed=none`, 7/7.

Defect: a still-gated entry's bytes changed (every line ending), and the counter reads it as unchanged. The sentence "byte-identical" is violated and the counter does not say so.

Fix: compare bytes (`open(path, "rb")`) in L7, not text-mode reads.

Limitation: the edit is line-endings only; the recheck line executes identically, so the L1 gate count is unaffected. The defect is the counter's claim, not an executed behaviour.

---

## F4 — C1 L7: a still-gated entry whose only change is the file mode reads 7/7 — INFO (not bytes; reported because the brief asked)

Recipe (tree P4 = tip, `chmod 755 corpus/knowledge/citation-bases.md`; base is 644). Output: `gate L7 pass=1 read=still-gated=22 changed=none`, `c1-gate fixed=7/7 exit=0`.

Note: "byte-identical" does not cover the mode bit, so this is not a violated sentence. It is undetected metadata. Record only.

---

## F5 — C2 (coverage): five-core, filler-padded F28 entry reads 7/7 — BROKEN

Attacked: G2 section check (`sect_words >= 25`, `r46-c2-gate.py:184-202`), G5 located-quote check (`r46-c2-gate.py:280-303`, `len(passed) >= 4` and five cores). Frozen C2 kill rule (`claims.json` line 30): "or if the entry restates the page without a decision rule a reporter can act on".

Recipe (tree P7 = tip, `corpus/knowledge/github-private-vulnerability-reporting.md` replaced by):
- Header (3 lines): `source: S073 — <canonical URL> — GitHub Docs, privately reporting a security vulnerability (capture corpus/source-snapshots/round-46/S073.txt)`, `verified-at: 2026-10-28`, `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073`.
- `## Scope and decision rule`: exactly five curly-quoted spans, each followed by its cite, located in capture lines 564, 573, 574, 577, 578 (the five frozen cores):
  - `“You can only report vulnerabilities privately for repositories where this feature is enabled.” (`S073.txt:564`)`
  - `“By default, you must provide a summary, details, proof of concept, and impact statement.” (`S073.txt:573`)`
  - `“Optionally, select I used AI assistance to find or write up this report.” (`S073.txt:574`)`
  - `“GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.” (`S073.txt:577`)`
  - `“only the repository maintainer can merge changes from that private fork into the parent repository” (`S073.txt:578`)`
- `## Overlap and novelty`, `## Limits`, `## Falsifiable package rule`: filler only. The filler sentence (repeated twice per section; the Falsifiable section once): "This paragraph restates the reporter flow in other words and adds no new claim and no new location, so the section is long enough to pass the word floor while saying nothing that the cited page does not already say, which is exactly the padding this probe measures in the coverage counter."
- A six-row 3-cell table with `S073.txt:<n>` in the middle cell and two-word cells, plus a line of cross-references to `corpus/knowledge/ai-assisted-finding-validation.md:1` and `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:1`.
- Size 3839 bytes, five curly quotes, zero straight quotes (`gen2.py` print).

Command: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c2-gate.py --root <P7>`

Output (printed):
```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```

Discrimination: the base reads `c2-gate fixed=1/7 exit=1` (re-run). The freeze's own controls (`controls/freeze-controls.txt`, quoted from its printed output, not re-run here) read `fixed=4/7` for the header-only junk-row entry and `fixed=5/7` for uncited 600-word filler. P7 is the only one of these that reaches 7/7: it clears G2's word floor and G5's five located cores with no uncited span, and it still has no decision rule.

Defect: the entry's three non-quote sections are filler; the entry has no decision rule a reporter can act on (the kill rule). The counter has no limb for section content; G2 counts words, and G5 counts located cores.

Fix: no mechanical limb fully closes this; a non-author reading must judge the entry (as C2's kill rule already says). A cheap mechanical tightening: require each section to carry at least one located quote or a sentence naming an action, and require distinct content across sections.

---

## F6 — C2 G1: relabelling the F27 frontier row as F29 reads 7/7 — BROKEN (count-only G1)

Attacked: G1 checks 28 rows, 28 admitted, no duplicate ids, the F28 row's entry. It does not check that F01-F27 survive. The C2 `after` sentence is "28 admitted frontier rows with F28 = ...", which implies F01-F27 kept.

Recipe (tree P9 = tip, `corpus/README.md` line 651: `| F27 |` changed to `| F29 |`, content unchanged):

Output (printed):
```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```
Evidence that F27 is gone: `grep -cE '^\| F(0[1-9]|1[0-9]|2[0-7]) \|'` on the probe README prints `26` (F01-F26 only); the tip has 28 `^\| F[0-9]+ \|` lines.

Defect: a previously admitted frontier move is removed and a relabelled row is counted in its place. This is a count-padding tree. Fix: pin the F01-F27 rows (ids and content) to the base README bytes, or require ids F01..F28 exactly.

---

## Closed candidates (the counter catches them; no finding)

- **F028 twin of F28 with the same entry, replacing the F27 row** (`probes/p5-f028twin`): `gate G1 pass=0 read=F28-entry-shared-with-another-row`; `c2-gate fixed=2/7 exit=1`. Closed by the shared-entry rule (`r46-c2-gate.py:162-163`).
- **Literal second F28 row** (`probes/p5c-dupF28-added`, rows become 29): `gate G1 pass=0 read=rows=29 admitted=29 dup=1`, `c2-gate fixed=2/7 exit=1`.
- **Literal second F28 row replacing F27** (`probes/p5d-dupF28-replaces-F27`): `gate G1 pass=0 read=rows=28 admitted=28 dup=1`, `c2-gate fixed=2/7 exit=1`. Closed by the duplicate-id check (`r46-c2-gate.py:171-172`).
- **S073 row under `## Registry changes`** (`probes/p6-registry-changes`: the table row moved from `## Registry` to a table under `## Registry changes`): the counter reads `gate G3 pass=1 read=row-S073=ok` (its `registry_lines` takes `## Registry changes` as registry, `r46-c2-gate.py:143`), but `gate G7 pass=0 read=census-rc=1 ok-line=0` and `c2-gate fixed=6/7 exit=1`. The fleet census reports, by re-run: `file	E12	S073 row outside Registry section` (rc=1). So G7 closes it. Note: G3's section match is looser than the census's exact `Registry`; G7 is what closes it, and it depends on the fleet-root census script (see limitations).
- **C1 one-spelling single-file re-ground** (freeze control, re-run as P0): `c1-gate fixed=0/7 exit=1`.
- **C1 marker-only / recheck-line variants**: not re-run (covered by the frozen controls; no new defect found by reasoning about L3, since L3 requires the exact `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<itself>.md` shape and `allowed()` rejects anything else).
- **Tip itself**: `grep` for spelling variants or `corpus/source-snapshots/` anchors in the two re-ground sections of the tip found no match (the integrated tree is not exploiting F1/F2; those gaps are latent in v1.1).

---

## Recipes (each probe rebuilt from the tip with the stated edit; scratch removed at exit)

Common: `cp -a <tip> <probe>` then the edit below. C1 probes: `python3 .../r46-c1-gate.py --root <probe> --baseline <base> --work <scratch>/tmp`. C2 probes: `python3 .../r46-c2-gate.py --root <probe>`. `<base>` is a copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure`.

- P1 (F1): for each of `claim-gates.md` (start line 100) and `claim-package-contract.md` (start line 300): keep the lines before `## Re-ground (round 46)`, then append the heading, a blank line, `| id | current claim | committed anchor | token |`, `|---|---|---|---|`, and six rows; anchor `corpus/instruments/claim-package-check.py:<n>` on even rows and `corpus/instruments/./claim-package-check.py:<n>` on odd rows; token = stripped text of line `<n>` (first six lines >= start with 12-60 characters, no backtick or pipe, unique in the file).
- P0 (control F1): same, every anchor on the first spelling only.
- P2b (F2): as described under F2 (S071 lines 3,10,73 / 109,174,254; S069 lines 7,29,52 / 114,231,986; token = heading text; anchor on the spelling given there).
- P3 (F3): `citation-bases.md` bytes `replace(b"\n", b"\r\n")`. P3c: `replace(b"\n", b"\n\n", 1)`. P8: prepend `b"\xef\xbb\xbf"`. P4 (F4): `chmod 755`.
- P7 (F5): as described under F5.
- P9 (F6): `corpus/README.md` line 651 `| F27 |` -> `| F29 |`.
- P5 / P5c / P5d / P6 (closed): as described under "Closed candidates".

## Limitations

- Probes isolate the counter. The row claim text is placeholder in F1 and F2; the defects in F1, F3, F6 are structural and do not depend on claim text. F2 and F5 are semantic defects the counter cannot see; they are reported because the frozen counter reads 7/7 with the defect present, and the kill rule's non-author reading is the only gate for them.
- I did not re-run the frozen `freeze-controls.py` suite in full; I re-ran the do-nothing controls (C1 1/7, C2 1/7) and the single-spelling control, and used the freeze's junk-row and uncited-filler numbers as printed in `controls/freeze-controls.txt`.
- C2 G7 depends on `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane and hard-coded in `r46-c2-gate.py:54` (`CENSUS`). A change there moves G7 with nothing in the lane changing.
- L7 and G6 read `corpus/knowledge` as text or bytes as stated above; I did not test Latin-1 or UTF-16 re-encodings (L7 would fail closed via a decode exception; not run).
- Observed, not mine: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/__pycache__/` holds `r46-c1-gate.cpython-314.pyc` (mtime 20:35:52) and `r46-c2-gate.cpython-314.pyc` (20:34:47), written before my classify import (run with `-B`) and not by my script-mode runs. I did not delete them.
- Scratch (`/fast/scratch/hyaku/kasegi-r46/R46W2CritControlsV11/`) is removed at exit; the probes are reproducible from the recipes above.
