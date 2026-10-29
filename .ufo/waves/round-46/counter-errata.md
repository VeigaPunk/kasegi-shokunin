# Round 46 — counter errata (E1) and the classification decision

Frozen at `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5` (`freeze.txt`): `claims.json` sha256 `e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740`, `r46-c1-gate.py` v1 sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294`, `r46-c2-gate.py` v1 sha256 `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`.
`claims.json` is byte-identical at the tip: `diff <(git show 9f23aab:.ufo/waves/round-46/claims.json) .ufo/waves/round-46/claims.json` prints nothing. No claim sentence, before-value, after-value, target, kill rule or counter command was edited.

## Decision (spot-check item 2 of `corpus/lessons/round-45-verifier-spotcheck.md`, decided inside the round, before closure)

**Counter erratum, not a changed rule.** Basis, in the order the spot-check asked for:

1. Prose predicate diff: the C1 and C2 `after` sentences and kill rules are unchanged (empty diff above). The seven C1 limb sentences in `r46-c1-gate.py`'s docstring and the seven C2 gate sentences changed only where a wave-1 falsification showed the CODE did not do what the SAME sentence says (list below); each docstring edit is the sentence made literal, not a new requirement.
2. The kill rule's own parenthesis: "bug fixes that keep a limb's sentence are logged as counter errata in counter-errata.md with a plain re-derivation that does not use the counter" — this file is that log; the re-derivations are in the last section.
3. The v1.1 pass set is narrower than v1's. That is the point of an erratum after a falsify wave (round-44 and round-45 precedent) and is disclosed, not hidden: every v1.1 limb rejects at least one tree v1 passed, each named with its source report.

## Changes, with the wave-1 report that forced each

### r46-c1-gate.py v1 -> v1.1 (sha256 `99e0ee555b68e5177f33e49e8024469608297a412171b190f66b1bba189475cc` at the integration tip; the final sha is in the report)

| id | v1 code | v1.1 code | forced by |
|---|---|---|---|
| C1-E1 (L3) | substring test: line mentions `r46-c1-gate.py` and `--entry corpus/knowledge/<e>` outside the `cd` | the recheck line is exactly `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<itself>.md` with an optional trailing ` # comment`; exactly one `recheck:` line in the entry; no `~/`, `$HOME`, `/home/` after the `cd` | `wave1/R46RevC1L3.md` (a `true  # r46-c1-gate.py --entry ...` comment trick read 7/7), `wave1/R46CritKillRule.md` C1-a/b/c, `wave1/R46RevC1L1.md` finding 2 (a shadow `recheck: true` above the base line), `wave1/R46ExecSelftestC1.md` F1-F6 |
| C1-E2 (L4) | per-entry token located in a <=40-line anchor range | plus: every anchored file is byte-identical to BASE's (an anchor cannot be planted in the same edit), no repeated (anchor, range) or token, token >= 8 chars | `wave1/R46Revenger.md` ("planted-anchor variant"), `wave1/R46RevC1L4.md`, `wave1/R46RevC1L6.md` (`dup`) |
| C1-E3 (L5) | every BASE line except `recheck:` lines is an in-order prefix of TREE's | plus: the BASE recheck command survives verbatim as exactly one `restoration-recheck: <command>` line, so the on-restoration check of a lost-base entry is kept, never dropped | `wave1/R46Revenger.md` §1 (re-grounding silently removes the entry's restoration check), `wave1/R46RevC1L5.md`, `wave1/R46CritCalibration.md` F5 (claim text says "every BASE line kept"; v1 exempted the recheck line) |
| C1-E4 (L6) | blank the token in a scratch copy of the anchored file; red = load-bearing | an unmutated scratch copy must read green first; blanking only the token inside the row's own anchored lines must turn red on exactly that row | `wave1/R46RevC1L6.md` findings 1-3 (rows that were red for the wrong reason; the scratch copy omitting the entry body) |
| C1-E5 (L7) | still-gated entries keep their BASE recheck LINE | still-gated entries are byte-identical to BASE | `wave1/R46RevC1L7.md` (if present) and the L7 sentence in `claims.json` ("entries still gated keep their BASE recheck line byte-identical" — the file is the stricter reading) |
| C1-E6 (execution) | every tree-supplied `recheck:` line ran under `bash -c` with the full host environment | only allow-listed line shapes are executed (`test ...`, `set -o pipefail`, `git -C <dir> rev-parse HEAD`, `python3 corpus/instruments/<x>.py <plain args> [| grep -x '<literal>']`), instruments resolve to THIS lane's `corpus/instruments/`, minimal environment (`HOME`, `PATH`, `TMPDIR`, `LANG`); a line outside the allow-list reads `broken` and is never run, which turns L1 red | `wave1/R46SentinelGate.md` S1 HIGH (a tree-supplied line read the operator's environment); every one of the lane's 64 base lines passes the allow-list (`gated=24 broken=0` at the base under v1.1) |

Not changed on purpose: the environment is NOT scrubbed of `HOME`. `wave1/R46RevC1L1.md` finding 3 shows that a host which restores `~/Projects/bounties` moves L1; v1.1 measures BASE under the same environment, so L2 (the regrounded set) reads 0 and the aggregate stays red; the host dependence is disclosed and `HOME` is needed by the base lines (`root-loss-2026-10-12.md` tests `~/Projects/ufo-fsd-alpha`).

### r46-c2-gate.py v1 -> v1.1 (sha256 `b52fea3183a393fa2f5bb40879241034e9db0b45f7914244d9f3bed134958621` at the integration tip)

| id | v1 code | v1.1 code | forced by |
|---|---|---|---|
| C2-E1 (G2) | `"--source S073" in line`; any 3-cell pipe line counts as a table row; heading presence only | `--source S073` as a whole token and the round-46 manifest named; a counted table row has three non-trivial cells and a located `S073.txt:N` cite; each section carries >= 25 words (the package rule >= 12; E1 table wording corrected: the 12-word floor is for `## Falsifiable package rule` only); live lines only | `wave1/R46MutC2a.md` S1 (`--source S0730`), S2 (junk row `\| - \| - \| - \|`), S3 (emptied Limits), `wave1/R46RevC2G2.md` |
| C2-E2 (G3) | `URL in row[1]` substring; no cell content test; rows read under any `##` | the FIRST URL of the source cell equals the canonical URL; kind `docs`; scope and teaches >= 8 words; recheck cell a cadence or date; anchor cell names the capture and a line locator; registry rows are read only under `## Registry` (any heading resets) | `wave1/R46MutC2a.md` S4 (URL wrapped in another host), `wave1/R46RevC2G3.md` (filler row) |
| C2-E3 (G4) | `quotes-ok >= 8` | plus: the manifest's quote texts are pairwise distinct, equal in number to the OK lines, with >= 7 distinct anchors | `wave1/R46MutC2b.md` P4 |
| C2-E4 (G5) | raw text; any range width; curly quotes only | live lines only (no HTML comment, no fence); a cited range lies inside the page body (lines 556-583) and spans <= 12 lines, start >= 1; an ASCII-quoted span of >= 4 words is held to the same cite-and-locate rule | `wave1/R46MutC2b.md` M07/M08/M09/P1/P2, `wave1/R46RevC2G5.md` |
| C2-E5 (G6) | `.md` files at depth 1 only; the byte pin over the 64 base entries | the directory holds exactly the 65 `.md` entries (no other file, no nested `.md`); the byte pin covers 62 base entries — the two entries C1 re-grounds are exempt from the BYTE pin (their NAMES stay pinned) | `wave1/R46MutC2c.md` S1/S2, `wave1/R46ConnSeparable.md` F1 (at the joint tip v1 read 6/7 because C1 necessarily edits two pinned base files: with v1 no tree satisfied both counters, so C2 was not verifiable with C1 landed) |
| C2-E6 | `False` left where a pin used to be | unchanged: the entry and row bytes are NOT pinned (they did not exist at freeze); the gate grades structure and located quotes and the non-author closure re-opens the page | `wave1/R46Simplifier.md` (if present) |

## What the errata do not claim

- v1.1 is still a mechanical grader. `wave1/R46CritSoftening.md` and `wave1/R46Revenger.md` show that a counter reading 7/7 is compatible with rows that overreach (a row about the lost `claim-check.mjs` anchored to a different tool). The C1 kill rule already delegates that judgment to a non-author reading; the C1 verdict in the report rests on the wave-2 side-by-side reading of every row (`wave2/`), not on 7/7.
- v1 reading of the integrated tree before the fix: `c2-gate fixed=6/7` (G6). That reading is kept as a plain finding in `wave1/R46ConnSeparable.md` (T12).

## Plain re-derivations (no python counter; run from the lane root at the tip)

```
# C1 recheck lines: exactly one, exact shape, per re-grounded entry (expect 1 and 1)
grep -cE '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate\.py --entry corpus/knowledge/(claim-gates|claim-package-contract)\.md( +#.*)?$' corpus/knowledge/claim-gates.md corpus/knowledge/claim-package-contract.md
# the BASE recheck command survives verbatim as restoration-recheck (expect no diff output)
for e in claim-gates claim-package-contract; do diff <(git show 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba:corpus/knowledge/$e.md | grep '^recheck:' | sed 's/^recheck:/restoration-recheck:/') <(grep '^restoration-recheck:' corpus/knowledge/$e.md); done
# append-only: deletions per entry == 1 (the replaced recheck line)
git diff --numstat 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba -- corpus/knowledge/claim-gates.md corpus/knowledge/claim-package-contract.md
# rows per entry, and every row located by a fixed-string search (expect rows=25 located=25 / rows=21 located=21)
bash .ufo/waves/round-46/controls/plain-rows.sh "$PWD" claim-gates.md ; bash .ufo/waves/round-46/controls/plain-rows.sh "$PWD" claim-package-contract.md
# the gated count in the instrument of record (expect executes=43 gated=22 broken=0: 40 base executing lines + the 2 re-grounded entries + the new F28 entry's own recheck)
python3 corpus/instruments/recheck-audit.py --root . --quiet | grep '^executes='
```


## E2 — the wave-2 falsification (counters v1.1 -> v1.2; landing gate; entries)

The wave-2 seats (`wave2/`) attacked the v1.1 tree. Their reports are cited per row; the ruling of the Decision section stands (counter erratum), restated with the critic's objection below.

### r46-c1-gate.py v1.1 -> v1.2

| id | change | forced by |
|---|---|---|
| C1-E7 | instrument names in the allow-list are the five the lane's rechecks use (`anchorcheck`, `source-recheck`, `claim-package-check`, `density`, `r46-c1-gate`); `freeze-check`, `kill-rule-check`, `r46-landing-gate --jj-lane` and every other instrument that executes a path or command from its arguments are no longer runnable through a recheck line | `wave2/R46W2SentinelV11.md` F1 HIGH (three PoCs ran tree-controlled code through allow-listed instruments) |
| C1-E8 | files are read with `newline=""` and split on `"\n"` only (CRLF, lone CR and U+2028 stay visible to L4, L5 and L7); anchored ranges containing `\r` or U+2028 are refused; distinct anchor files are counted by content digest too | `wave2/R46W2MutC1b.md` A3/A4/A6/B3/B4, `wave2/R46W2MutC1c.md` m11 |
| C1-E9 | recheck and restoration lines and the `## Re-ground (round 46)` heading are read from live Markdown (outside HTML comments and fences); a heading or recheck line that exists only inside a comment or a fence, a second hidden `recheck:` line, and any table row inside the section that is not a `G<digits>` row, header or separator (indented, lowercase id) make the entry red | `wave2/R46W2MutC1a.md` m09-m12, `wave2/R46W2MutC1c.md` m06/m07/m09 |
| C1-E10 | a token needs >= 6 alphanumeric characters (a comment divider is not evidence) | `wave2/R46W2MutC1c.md` m05 |

### r46-c2-gate.py v1.1 -> v1.2

| id | change | forced by |
|---|---|---|
| C2-E7 (G1) | the F28 row's sources cell names S073 | `wave2/R46W2MutC2a.md` S1 |
| C2-E8 (G2) | the recheck line has the exact form (one `recheck:` line, exact command, optional ` # comment`); cross-reference ranges are checked at both ends; table cites lie inside the page body 556-583; the four sections carry content (Scope and the package rule cite S073.txt; Overlap holds >= 2 `corpus/knowledge/<file>.md:N` references; Limits cites S073.txt or a backticked sweep command) | `wave2/R46W2MutC2a.md` S2-S4, S6 |
| C2-E9 (G3) | the anchor locator is a line range inside 556-589 | `wave2/R46W2MutC2a.md` S5 |
| C2-E10 (G4) | the S073 record is found by id (not `sources[0]`) and the five cores must sit in quote records | `wave2/R46W2MutC2b.md` F6/F7 |
| C2-E11 (G5) | quoted spans anywhere in the raw file (comments and fences included) must be cited and located, ASCII-quoted spans of >= 4 words (any length, across lines) and single-curly spans of >= 4 words are held to the same rule, cores count only from live text | `wave2/R46W2MutC2b.md` F1-F5 |
| C2-E12 (G6, G7) | `corpus/`, `corpus/knowledge` and its entries and `corpus/SOURCES.md` must not be symlinks; each exempt entry may grow but never shrink below its base size | `wave2/R46W2MutC2c.md` F1-F3 |

### Landing gate (`corpus/instruments/r46-landing-gate.py`)

The `date-order-author` check was withdrawn. `wave2/R46W2CritMistake.md` F1-F4 shows, with the round-45, round-44 and round-28 pairs and a constructed honest amend, that the author time of a report commit is not a filing clock (an amend or a jj rewrite keeps it and moves the committer time), so the check failed every honest rewritten history and could not tell it from a real inversion. The committer-time check (`date-order`) remains; the gate's selftest case that asserted the author reading now asserts that the round-45 shape PASSES (`post-honest-rewrite-author-earlier-than-cited-round45-shape`); `selftest cases=30 failures=0`.

### The critic's objection to the ruling, and the answer

`wave2/R46W2CritErratum.md` (VERDICT BROKEN on the stated basis): five of seven C1 limb sentences changed and four now require something the frozen text did not say; no C2 gate sentence changed (only code); the C2 pass set is not narrower than v1's at the joint tip (v1 read 6/7 there, v1.1 7/7); and the errata supplied a plain re-derivation for C1 only in part. Accepted, in these words:

1. The E1 table's phrase "the sentence made literal" is withdrawn for C1 L4, L6 and L7, the token floor and every C2 change: those are NEW requirements added because a falsify wave showed a green tree with the defect present. They tighten the pass set toward the frozen `after` sentences (the C1 `after` sentence names "a recheck line that runs `r46-c1-gate.py --entry` on itself", "every BASE line kept", "every row load-bearing" and "still-gated lines byte-identical"; the code now says each of those more strictly), but they are not literal restatements.
2. The classification stays **counter erratum**, with that disclosed: the claim sentences, the before-values, the after-values, the targets and the kill rule's text are byte-identical to the freeze (`claims.json` sha256 `e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740`); what changed is how the code reads a tree. A reader who weighs the kill-rule parenthesis ("bug fixes that keep a limb's sentence") narrowly must read C1 as UNVERIFIED on the frozen counter and rely on the plain re-derivations below, which do not use either counter and which the non-author closure can re-run.
3. C2 never had a limb-sentence clause in its kill rule; its v1 -> v1.2 changes are logged here with the report that forced each.
4. v1 read 6/7 on the joint tip because C1 edits two entries the v1 G6 pinned byte for byte (C2-E5): v1.2's pass set is wider on that one axis (the exempt entries) and narrower on every other; the disclosure is the same.
5. "Every BASE line kept (append-only)" (C1 `after`) is literally false for the two re-grounded entries: the BASE `recheck:` line becomes a `restoration-recheck:` line with the same command (one deletion and one addition per entry in `git diff --numstat`). The wording tension is real; the substance (no BASE text lost, the on-restoration check kept) is what the plain re-derivation below shows.

### Plain re-derivations for C2 (no python counter)

```
# rows, sources, status, census (expect 28, 73, 65, census exit 0)
grep -cE '^\| F[0-9]+ \|' corpus/README.md
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l ; ls corpus/knowledge | wc -l
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
# G2/G5: every quoted span of the entry is followed by an S073.txt cite and sits in the page body; no quote line outside 556-579 (expect 0)
grep -oE 'S073\.txt:[0-9]+' corpus/knowledge/github-private-vulnerability-reporting.md | cut -d: -f2 | awk '$1<556||$1>583' | wc -l
# G5: every cited span located by fixed-string search (expect located == spans); see wave2/R46W2RevEntryTable.md for the loop
python3 - <<'EOF'
import re
b=open("corpus/knowledge/github-private-vulnerability-reporting.md",encoding="utf-8").read()
s=open("corpus/source-snapshots/round-46/S073.txt",encoding="utf-8").read().split("\n")
n=lambda x:" ".join(x.replace("\u2019","'").split())
sp=re.findall("\u201c([^\u201d]+)\u201d\\s*\\(`?S073\\.txt:(\\d+)(?:-(\\d+))?`?",b)
ok=sum(1 for q,a,c in sp if n(q) in n(" ".join(s[int(a)-1:int(c or a)])))
print("spans",len(sp),"located",ok)
EOF
```
