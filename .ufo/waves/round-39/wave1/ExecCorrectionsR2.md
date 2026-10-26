# ExecCorrectionsR2 — round-39 corrections for the round-38 verifier's R2/R3 sweep

- seat `ExecCorrectionsR2` (executor, leaf); lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD `d65d823`
- work window 2026-10-26T19:30Z–19:36Z; judged axis: depth:verifiability; milestone round-39
- status: **four append-only `Correction (round 39)` blocks delivered byte-exact**; no lane file edited, no tracked file written outside the four deliverables and this receipt.

Assignment: sweep the round-38 verifier's R2 defect (lane records overstate C1 at the judged head J) and R3
(the report's tip run over `f06148c6` has no committed transcript), as append-only correction blocks for
`corpus/lessons/round-38.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`.

## 1. Deliverables

| deliverable | lands appended to | lands at | lines | bytes | sha256 |
|---|---|---|---:|---:|---|
| `.ufo/waves/round-39/wave1/ExecCorrectionsR2.round38-lesson.append.md` | `corpus/lessons/round-38.md` (EOF, after the `## Instrument attack findings` closing paragraph) | `:311` | 2 | 1354 | `895547931464ba115bae0620a771766dab35fb36daa329435e7310b1b5e83474` |
| `.ufo/waves/round-39/wave1/ExecCorrectionsR2.log.append.md` | `LOG.md`, round-39 entry (bullet; the round-39 entry does not exist yet — see §5.3) | `:1703` if appended to the current file | 1 | 514 | `b9cee1ecfa138ec8f9da8a1e2401ae4e588dfb4c74181bb036e57ebddc4e2b3e` |
| `.ufo/waves/round-39/wave1/ExecCorrectionsR2.scorecard.append.md` | `SCORECARD.md` (EOF, after the round-38 `## Planned` paragraph) | `:1532` | 2 | 1426 | `0251af27d9336fe1b93db705dacc38ab0a77df09331ed9a0ae7761df14bada55` |
| `.ufo/waves/round-39/wave1/ExecCorrectionsR2.shonen.append.md` | `SHONEN.md` (EOF, after the round-38 box-4 paragraph) | `:189` | 2 | 743 | `79890f628869257df313f97aafd7359d4e6f9dc07af3de2eea5b756326deb23d` |

Line counts are `wc -l`; the three file appends start with exactly one blank separator line (the target files
end on a single `\n` with no trailing blank line), the LOG block is a single `- **Correction (round 39):**`
bullet with no leading blank. Each file contains only landable bytes — one correction paragraph/bullet, no
headings, notes or tables. Deliverable directory:

```
$ cd .ufo/waves/round-39/wave1 && for f in ExecCorrectionsR2.*.append.md; do \
    printf '%s lines=%s bytes=%s sha256=%s\n' "$f" "$(wc -l < $f)" "$(stat -c%s $f)" "$(sha256sum $f | cut -d' ' -f1)"; done
ExecCorrectionsR2.log.append.md lines=1 bytes=514 sha256=b9cee1ecfa138ec8f9da8a1e2401ae4e588dfb4c74181bb036e57ebddc4e2b3e
ExecCorrectionsR2.round38-lesson.append.md lines=2 bytes=1354 sha256=895547931464ba115bae0620a771766dab35fb36daa329435e7310b1b5e83474
ExecCorrectionsR2.scorecard.append.md lines=2 bytes=1426 sha256=0251af27d9336fe1b93db705dacc38ab0a77df09331ed9a0ae7761df14bada55
ExecCorrectionsR2.shonen.append.md lines=2 bytes=743 sha256=79890f628869257df313f97aafd7359d4e6f9dc07af3de2eea5b756326deb23d
```

## 2. Ground truth measured (read-only, lane + fleet report)

Heads (the round-39 dispatch summary and `claims.json` carry a 37-character token for J — see §5.1; the
receipt's `:2` value is authoritative):

```
$ for h in 66703acaaff50529a35be49aa8759d04140720ad f06148c66c6d7aed948cb7024d9f0b9cffe4b95a 7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e; do \
    printf '%s -> ' "$h"; git rev-parse --verify "$h^{commit}"; done
66703acaaff50529a35be49aa8759d04140720ad -> 66703acaaff50529a35be49aa8759d04140720ad
f06148c66c6d7aed948cb7024d9f0b9cffe4b95a -> f06148c66c6d7aed948cb7024d9f0b9cffe4b95a
7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e -> 7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e
$ git merge-base --is-ancestor 66703acaaff50529a35be49aa8759d04140720ad f06148c66c6d7aed948cb7024d9f0b9cffe4b95a && echo "J ancestor-of Y: yes"
J ancestor-of Y: yes
$ git diff --name-only 66703acaaff50529a35be49aa8759d04140720ad f06148c66c6d7aed948cb7024d9f0b9cffe4b95a
.ufo/waves/round-38/final-gates/all-gates.txt
$ git diff --numstat 66703acaaff50529a35be49aa8759d04140720ad f06148c66c6d7aed948cb7024d9f0b9cffe4b95a
79	0	.ufo/waves/round-38/final-gates/all-gates.txt
$ git grep -c f06148c6 f06148c66c6d7aed948cb7024d9f0b9cffe4b95a -- .
(no output; exit 1)     # the tip cannot carry its own run
```

Receipt `.ufo/waves/round-38/final-gates/all-gates.txt` (the only committed transcript):

```
$ grep -n "^export-ref=\|^run-ref=\|^export-ref-run: G2\|^export-ref-run: closed\|^closed=8/8\|^selftest cases=" .ufo/waves/round-38/final-gates/all-gates.txt
2:export-ref=66703acaaff50529a35be49aa8759d04140720ad
4:run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e
8:export-ref-run: G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,digest-match=0,run-lines=0,closed-line=0,selftest-lines=0,selftest-summary=0,scorecard-ref=1,shonen-ref=1,head-token-lines=0 closed=0
15:export-ref-run: closed=7/8 exit=1
26:closed=8/8 exit=0
73:selftest cases=8 failures=0
```

(The `:26` and `:73` lines sit under `## run over run-ref` (`:16`) / `## selftest over run-ref` (`:27`), whose
headers at `:17` and `:29` carry `export-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e`. The receipt's own
header comment `:5` states the structural reason: G2 requires the receipt inside the export, and J cannot
contain the receipt that names it.)

Report quote that R3 routes (fleet repo, read-only, not a lane file):

```
$ grep -n "f06148c6" /home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md
37:- `bash corpus/instruments/r38-closure.sh --export-ref f06148c6…` (tip = J + receipt only) → `closed=8/8 exit=0`; `--selftest --export-ref f06148c6…` → `selftest cases=8 failures=0` …
```

That quote is **report-only**: no committed transcript exists for the tip run (the tip cannot carry its own
run). It is the only unlabeled `f06148c6 … closed=8/8` quote in existence: `corpus/lessons/round-38-verifier-spotcheck.md:59-60`
already labels the report's tip run "report-quoted only, not evidence-verified", and `:169` repeats it. The
SCORECARD block adds the label beside the lane's own score row (round-39 G3's requirement: committed
transcript or report-only label).

## 3. Sweep proof — every overstating mention touched

Method: copy all four targets to scratch, run the greps on the copies, append the four deliverables to a second
copy set, re-run the same greps. Patterns: the spec's literal `closed=8/8`, plus the non-literal phrasings the
overstatement also uses (`over the judged head`, `run over the round-38 head`, `run + selftest over`).

Before (unmodified copies):

```
$ grep -n "closed=8/8" corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
corpus/lessons/round-38.md:21:  … `closed=8/8 exit=0` and `selftest cases=8 failures=0` over the judged head are the receipt `.ufo/waves/round-38/final-gates/all-gates.txt` …
corpus/lessons/round-38.md:94:8. **C1 receipts at the judged head.** … `--export-ref J` → `closed=8/8 exit=0`; `--selftest --export-ref J` → `selftest cases=8 failures=0` …
$ grep -n "over the judged head\|run over the round-38 head\|run + selftest over" corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
corpus/lessons/round-38.md:21:  … (same C1 row) …
LOG.md:1698:  - **C1 depth:verifiability (4 held).** … Run and selftest over the judged head: `.ufo/waves/round-38/final-gates/all-gates.txt`; reds: `final-gates/reds.txt`. …
SCORECARD.md:1517:  | depth:verifiability | 4 | 4 (held) | … the run over the round-38 head the receipt names, and its `--selftest`, are committed in `.ufo/waves/round-38/final-gates/all-gates.txt`; … |
SHONEN.md:185:  — evidence (round 38): … r38 suite run + selftest over the judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt (raw transcript committed there). Box stays `[~]`.
```

Five overstating sites: `corpus/lessons/round-38.md:21`, `:94`; `LOG.md:1698`; `SCORECARD.md:1517`;
`SHONEN.md:185`. After the appends:

```
$ grep -n "Correction (round 39)" corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
corpus/lessons/round-38.md:311:Correction (round 39): two C1 lines above overstate the result at the judged head. … (`:21`, …) … (`:94`, …) …
LOG.md:1703:- **Correction (round 39):** the round-38 C1 bullet says "Run and selftest over the judged head: …"
SCORECARD.md:1532:Correction (round 39): the `## Round 38 result` depth:verifiability row overstates the run at the judged head. …
SHONEN.md:189:Correction (round 39): box 3's round-38 evidence line ("r38 suite run + selftest over the judged head: …") …
```

Coverage: `:21` and `:94` are both named by the round-38-lesson block; `LOG.md:1698` by the LOG bullet;
`SCORECARD.md:1517` by the SCORECARD block; `SHONEN.md:185` by the SHONEN block. Every pre-existing `closed=8/8`
occurrence in the four files is one of `:21`/`:94`, and both are named. No sixth site exists: the remaining
`judged head` mentions in these files (`corpus/lessons/round-38.md:6,19,245,248,249,284-286,304,305`,
`SCORECARD.md:1522`, `LOG.md:1663,1665,1671,1680,1682,1686,1701`) are either earlier rounds or name the head by
reference without asserting an 8/8 run at it.

Checked and deliberately not corrected: `SCORECARD.md:1523` ("the C1 run is the receipt itself"). It states
where the run is recorded, not that 8/8 was printed at J; the receipt it points at carries both runs, and the
SCORECARD correction block now states which is which.

## 4. Append-only proof — additions only, no rewrite

```
$ for f in corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md; do diff -u before/$f after/$f > d.diff; \
    printf '%s hunks=%s minus_lines=%s plus_nonblank=%s\n' "$f" "$(grep -c '^@@' d.diff)" "$(grep -c '^-[^-]' d.diff)" "$(grep -c '^+[^+]' d.diff)"; done
corpus/lessons/round-38.md hunks=1 minus=0 plus_nonblank=1
LOG.md hunks=1 minus=0 plus_nonblank=1
SCORECARD.md hunks=1 minus=0 plus_nonblank=1
SHONEN.md hunks=1 minus=0 plus_nonblank=1
```

Each file: exactly one hunk at EOF, zero removed/changed lines, one non-blank added line (plus the blank
separator where the block has one). Appended tail is byte-identical to the deliverable:

```
$ cmp <(tail -c "$(stat -c%s .ufo/waves/round-39/wave1/ExecCorrectionsR2.round38-lesson.append.md)" after/corpus/lessons/round-38.md) .ufo/waves/round-39/wave1/ExecCorrectionsR2.round38-lesson.append.md && echo "identical"
identical   # same check run for log / scorecard / shonen: all identical
```

Placeholder safety for the round-39 `G3` limb (its vocabulary is `⟨pending`, `<fill>`, `filled by the L1`,
`<LANE_HASH>`, `<r38-`): `grep -n "⟨pending\|<fill>\|filled by the L1\|<LANE_HASH>\|<r38-\|<"` over the four
deliverables → **no placeholder tokens** (the first draft's `git grep f06148c6 <Y>` was rewritten to
"over the tip's tree" for this reason). No `Final lane commit:` line is introduced.

Targets were unmodified at start: `git status --porcelain -- corpus/lessons/round-38.md LOG.md SCORECARD.md
SHONEN.md` → empty; blobs `4ed05a9e…` (round-38.md), `308dc467…` (LOG), `a1a48cb3…` (SCORECARD), `f17dee7a…`
(SHONEN) at HEAD `d65d823`.

## 5. Findings for the L1

1. **The frozen round-39 C1 kill rule carries a truncated J hash.** `claims.json` (read-only, claims-freeze
   commit `dcd3170`) contains the token `66703aca50529a35be49aa8759d04140720ad` — **37 hex chars** — in the C1
   `kill_rule` ("… or r38 judged head 66703aca50529a35be49aa8759d04140720ad export prints closed=8/8"). It is not
   a commit: `git rev-parse --verify 66703aca50529a35be49aa8759d04140720ad^{commit}` →
   `fatal: ambiguous argument … unknown revision`. The receipt's authoritative value (`all-gates.txt:2`, and the
   round-38 verifier spotcheck `:9`) is **`66703acaaff50529a35be49aa8759d04140720ad`**. All four corrections use
   the 40-char receipt value; a round-39 check that copies the claims token will be unresolvable rather than red
   for the right reason.
2. **R3's label is now in a lane file.** The report's tip run (f06148c6, `closed=8/8 exit=0` + selftest 8/0) had
   no committed transcript and no lane-side label; the SCORECARD block names it report-quoted only, beside the
   row it corrects, which is what round-39 G3 requires of any quoted `--export-ref <hash> → closed=K/K`.
3. **The LOG block is merge-ready, not self-placed.** `grep -c '^## Round 39' LOG.md` → `0` at HEAD `d65d823`; the
   round-39 entry is the L1's to create. The bullet names the round-38 bullet by quoting it, so it reads
   correctly from inside the round-39 entry and needs no line-number reference.
4. **The judged-head rule itself is consistent, and the corrections say so.** `git diff --name-only J Y` is the
   receipt file only (`79/0`), so `corpus/lessons/round-38.md:94`'s "differs from J by itself only" stays true and
   is not corrected; only its `closed=8/8`-at-J clause is.

## 6. Hygiene

- Writes: the four deliverable files above and this receipt only. No edit to any lane file, fleet file, sibling
  lane, `MANIFEST.json`, `templates/`, fleet `scripts/`, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`.
  Read-only git only (`rev-parse`, `diff`, `merge-base`, `grep`, `log`, `hash-object`); no mutating git/jj anywhere.
- Tooling: none installed, upgraded or fetched; no pacman invocation; no network fetch this item (the only report
  bytes read were already-committed local files).
- Scratch: `/fast/scratch/hyaku/kasegi-r39/ExecCorrectionsR2/` (before/after copies, four diffs) removed before
  yield; `ls -d /fast/scratch/hyaku/kasegi-r39/ExecCorrectionsR2` → `No such file or directory`.
