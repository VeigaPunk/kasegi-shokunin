# ExecC1Indep — independent re-derivation of C1's numbers (round-96 w1)

Seat: ExecC1Indep · 2026-11-07 · lane kasegi, base d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6, C1 landing 3c0581e2616df7a10af494a785b479d5e5293749, freeze 804e7bc344df0808c880815dde077c28be5db18a.

Method note: I did not run or import the lane's counter (`knowledge-meter.py`, pinned fadd0ede…). I read its docstring and `corpus/instruments/resolve.py` only to learn the meter's *semantics* (scope, path-like rule, class names, rate = non-GONE/total distinct), then implemented my own extractor and classifier from scratch (`/fast/scratch/hyaku/kasegi-r96/ExecC1Indep/census.py`, removed with the seat scratch). All rates below were produced by my code.

## Item 1 — own census of distinct backticked path-like tokens: AGREE

**Extraction rules (mine).** Over `corpus/knowledge/*.md` (104 files at both revs): take every backticked span per line; strip trailing `.,;:`; keep the token iff it is path-like: ends in a code/doc extension (.mjs .md .json .jsonl .yml .yaml .py .sh .txt .git .gitignore, case-insensitive), or ends `/`, or starts `~/` or `/`, or contains `/`, `<`, `{`, `~`, `..`, or ends in a `:NN` / `:NN-MM` line anchor whose anchor-stripped remainder ends in an extension. Reject empty, space-without-slash, and `http`/`xd://`/`skill://` heads. Dedup to one global distinct set per revision.

**Classification rules (mine).** Strip the `:NN`/`:NN-MM` (or `::symbol`) anchor → BASE. Bounty domain (exact `~/Projects/bounties` or `/home/vgpnk/Projects/bounties` root or `/`-descendant): literal host existence → RESOLVES, else mirror suffix (confined) → MIRROR-EQUIVALENT, else GONE. Mirror-alias domain (exact mirror-candidate root or `/`-descendant): exists under the selected mirror, realpath-confined → RESOLVES else GONE. Other absolute (`~`/`/`): host-exists → RESOLVES else GONE. Relative: exists under a full `git archive` extract of the measured revision → INTERNAL, else mirror (confined) → MIRROR-EQUIVALENT, else GONE. Existence test: literal, then brace expansion (≤64, sorted), then `<...>`→`*` glob; first existing wins. Rate = (#class ≠ GONE) / (#tokens).

Environment: `~/Projects/bounties`, `~/Projects/the-bounty-hunter`, `~/Projects/origin-work/the-bounty-hunter` all absent on this host (matches the control receipt's `mirror_absent=True`), so classification is tree-existence-driven.

**My numbers** (receipts `census-base.txt`, `census-landing.txt`, `census-delta-final.txt`):
- base d8a2bb0: **1030/2027** (GONE 997, INTERNAL 1007, RESOLVES 23)
- landing 3c0581e: **1032/2028** (GONE 996, INTERNAL 1009, RESOLVES 23)
- Set delta: added {`SKILL.md:182-185` → INTERNAL, `corpus/source-snapshots/round-30/S041.txt:1680-1681` → INTERNAL}; removed {`S041.txt:1680-1681`, classified GONE at base}; 2026 common tokens with **no class flips**.

**Comparison with the meter.** Numerator delta +2 and denominator delta +1 — identical to the meter's 1030/2027 → 1032/2028, and my absolute rates equal the meter's on both revs. Mechanics, independently derived: `SKILL.md:182-184` survives the landing as a distinct token (kept on triage-thresholds.md lines 89, 433–435; INTERNAL at both revs), so `SKILL.md:182-185` is a pure INTERNAL addition (+1); the qualified snapshot token is a second pure INTERNAL addition (+1); the bare `S041.txt:1680-1681` (its only scope occurrence was iso-29147:13) leaves the set as a removed GONE token (−1 denominator, 0 numerator) → 1030+2 / 2027+1.

Two non-obvious exclusions my census confirms: the comma-combined `SKILL.md:182-184,255-257` / `SKILL.md:182-185,255-257` are not path-like under the extraction rule (no `/`, no terminating `:NN[-NN]` anchor), so they sit in neither denominator; the two iso-29147:36 prose pointers are unbackticked, so they are census-invisible — their binding is M4's `part` rule, not the rate.

Caveat (qualifier, no verdict change): the census consults the host filesystem for absolute/bounty/mirror tokens (23 RESOLVES at base and landing). Host drift under those roots since the meter's pre-freeze run would move the absolutes; the corpus-relative structure (INTERNAL/GONE delta) is host-independent.

## Item 2 — repair map applied to base extract vs landing: AGREE

Applying the 5 rows of `.ufo/waves/round-96/c1/repair-map.tsv` (sha256 7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f, matches the frozen pin; each row replaces every occurrence of its literal `old` on its site line) to a `git archive d8a2bb0a…` extract yields files **byte-identical** to `git archive 3c0581e2…`:

- `corpus/knowledge/triage-thresholds.md`: applied sha256 ab98d2b0a5f5af2145f409f6793effe68c91cd4d348a6ee6b68096dc5114c671 == landing sha256 (cmp clean)
- `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`: applied sha256 edceed23c622870bedd1e8bc7cbbd58479ca2f8d67e0d64dd26208475010b54f == landing sha256 (cmp clean)

Honesty note: my first application attempt reported DIFFER — that was a bug in my own throwaway apply script (it re-read the pristine base per row, so a second row on the same file clobbered the first row's replacement). After fixing my script to compose rows per file, both files compare byte-identical. The lane artifacts were never at fault.

## Item 3 — numstat and the "five edits" reading: AGREE

`git diff --numstat d8a2bb0a… 3c0581e2… -- corpus/knowledge` (receipt `step3-numstat.txt`):
```
2	2	corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md
2	2	corpus/knowledge/triage-thresholds.md
```
4 changed lines carrying the 5 edits: triage-thresholds.md:88 (`SKILL.md:182-184`→`SKILL.md:182-185`) and :90 (`SKILL.md:182-184,255-257`→`SKILL.md:182-185,255-257`); iso-29147…md:13 (bare `S041.txt:1680-1681`→`corpus/source-snapshots/round-30/S041.txt:1680-1681`) and :36 (two edits on one line: `(L1832-1834)`→`(L1832-1833)` for d) and `(L1835)`→`(L1834)` for e) only; f) stays `(L1835)`). Line counts unchanged (triage 487→487, iso 67→67), so the two-lines-per-file numstat is exactly five substring substitutions across four lines. Whole-tree numstat confirms the landing touches no other content file: only these two knowledge files plus additions under `.ufo/waves/round-96/` (counter, map, labels, generator, harness, receipt, claims, C2 artifacts). Scope-wide `.ufo` citation sets are identical at base and landing (receipts `ufo-cites-*.txt`) — no knowledge file cites a round-96 wave path, so the landing's own artifacts do not perturb the rate.

## Verdict

AGREE on all three items. My independent census reproduces the meter's rates exactly (base 1030/2027, landing 1032/2028; numerator +2 via two INTERNAL additions, denominator +1 via one GONE removal, no class flips); the frozen map applied to the base extract is byte-identical to the landing for both files; the diff is exactly five edits on four lines in two knowledge files. Nothing here re-scores C1 beyond its frozen predicate; the observations below are routed qualifiers.

Observations (qualifiers, not verdicts):
1. The controls receipt (`controls/c1-controls-r96.txt`) header names `freeze=179deaaa…` and `candidate=f60c11a3…`; neither commit resolves in this repo today (pre-freeze scratch revs, receipt written before the freeze commit that contains it existed). All pin surfaces that the kill rule keys on — counter sha fadd0ede…, map sha 7d9bb49f…, labels sha 757894d1…, harness sha d47328ae… — do resolve and match the worktree files I hashed.
2. The landing's +2 numerator includes `SKILL.md:182-185` whose resolution is path-existence (SKILL.md is 1251 lines at both revs); the semantic claim that the omitted term completes on 185 is label evidence, not census output — the census verifies the delta mechanics, M5 owns range truth.
3. Tools installed: none. Credentials read: none.

## Receipts

All paths relative to /home/vgpnk/Projects/shokunin/kasegi-shokunin; outputs in `.ufo/waves/round-96/w1/ExecC1Indep-receipts/`.

1. `git rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; `git cat-file -t` on base/landing/freeze → `commit` ×3 (rc 0).
2. `sha256sum` of repair-map.tsv, labels.tsv, knowledge-meter.py, c1-controls-r96.py → 7d9bb49f…, 757894d1…, fadd0ede…, d47328ae… — all four equal the frozen pins (`sha256-pins.txt`).
3. `git archive <rev> -- corpus/knowledge/triage-thresholds.md corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md | tar -x` for both revs (rc 0; `sha256-pins.txt`).
4. `git diff --numstat` / `git diff` base→landing, scope and whole tree → 2/2 + 2/2; whole tree adds only `.ufo/waves/round-96/*` (`step3-numstat.txt`, `step3-rawdiff.txt`). rc 0.
5. Occurrence greps: bare `S041.txt…` in scope — base exactly one (iso:13), landing none (`bare-s041-*.txt`); `SKILL.md:182…` tokens on triage lines 88/89/90/433/434/435 base vs landing (`skill182-*.txt`). rc 0.
6. Host-dir probe: all three bounty/mirror roots absent (`host-dirs.txt`). `wc -l SKILL.md` → 1251 both revs.
7. `.ufo` citation grep over scope at both revs → identical sets, no round-96 citations (`ufo-cites-base.txt`, `ufo-cites-landing.txt`). rc 0.
8. Own census runs: `census.py tree-base scope-base` → `CENSUS … rate=1030/2027 mirror_absent=True`; `census.py tree-landing scope-landing` → `rate=1032/2028` (`census-base.txt`, `census-landing.txt`). rc 0.
9. Census set-delta + class-flip check → removed [`S041.txt:1680-1681`], added [`SKILL.md:182-185`, `corpus/source-snapshots/round-30/S041.txt:1680-1681`], flips NONE, key-token classes tabulated (`census-delta-final.txt`). rc 0.
10. Map application (own `apply_map.py`, 5 rows, each `old` found exactly once on its site line) → `APPLY-MAP rows=5 ok` (`step2-apply.txt`); `cmp` byte-identical ×2, applied sha256s == landing sha256s (`step2-cmp.txt`). rc 0.
11. `git cat-file -t 179deaaa…` / `f60c11a3…` → not present in repo; `git rev-parse` re-confirms base/landing/freeze full shas (`receipt-revs.txt`).

Scratch `/fast/scratch/hyaku/kasegi-r96/ExecC1Indep` removed; nothing of the seat outlives it besides the report and receipts.
