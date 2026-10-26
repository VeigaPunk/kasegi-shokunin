# RevClaimsFreeze — round-38 claims satisfiability & honesty review (receipt only)

Seat: RevClaimsFreeze (leaf, no dispatch). Reviewed 2026-10-26T18:44:36Z.
Scope: re-ran every before-measurement in `.ufo/waves/round-38/{c1-controls,c2-controls}/before.txt`
and `census-before.txt`; checked every frozen literal against the lane bytes at the claims-freeze
commit `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b` (and base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`);
flagged unsatisfiable / self-referential / do-nothing-reachable predicate clauses. Receipt only — no
deliverable file.

## Method

- Read-only git against the lane only (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin`):
  log, status, diff, ls-tree, ls-files-equivalents, archive, cat-file, merge-base. No mutating git.
- Base and freeze exported read-only into scratch: `git -C <lane> archive <hash> | tar -x -C <S>/base|frz`
  (`S=/fast/scratch/hyaku/kasegi-r38/RevClaimsFreeze`). `git diff --stat base freeze` = the 4 control
  files only (107 insertions, 0 deletions) ⇒ every corpus literal is byte-identical at base and freeze
  (spot-check: `sha256sum PROVINCE.md` identical in both exports: `3e9e66b2448d61b6…`).
- Freeze-state fixture for live-limb re-runs: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`, toplevel
  verified `== $D`, fetched the lane's refs into the fixture, `checkout --detach a173b0c2…` ⇒ clean
  tree, `HEAD=a173b0c2…`, full history. All fixture git writes stayed inside the verified fixture.
- Instruments were re-run from the base export / fixture with their documented scratch-copy flags
  (`recheck-audit.py --root <base> --cdroot <lane>`; see Method note M-1).

## A. c1-controls/before.txt — per-line re-run (18 lines)

| # | before.txt line (value) | my re-run | verdict |
|---|---|---|---|
| 1 | header: measured 18:16:23Z at base, "live lane == base, porcelain empty" | historical; consistent: `git diff --name-only base 9a10b02f` = the 4 control files only, so the lane was base-plus-controls at freeze | agree (historical) |
| 2 | `ls corpus/instruments/r38-closure.sh` → exit=2 | base export and live lane: `No such file or directory`, exit=2 | agree |
| 3 | `grep -c '^Correction (round 38)' PROVINCE.md` → 0 | 0 (exit=1) | agree |
| 4 | same on corpus/README.md → 0 | 0 (exit=1) | agree |
| 5 | fence lines PROVINCE.md → `81:\`\`\` 96:\`\`\`text 124:\`\`\`` | `grep -n '^```'` → `81:```  96:```text  124:``` `; CommonMark walk (opener ``` optional info; closer ``` no info) ⇒ open-at-EOF=0 | agree |
| 6 | fence lines corpus/README.md → `426:\`\`\`` opener never closed, open-at-EOF=1 | `grep -n '^```'` → `426:``` ` only; walk ⇒ open-at-EOF=1 | agree |
| 7 | r37 appends: PROVINCE.md L79-L152 (74 lines), corpus/README.md L399-L454 (56 lines) | `git diff -U0 b56a41680cef… a173b0c2… -- PROVINCE.md` → single hunk `@@ -78,0 +79,74 @@`; corpus/README.md → `@@ -398,0 +399,56 @@`; no other hunks in either file | agree |
| 8 | `ls .ufo/waves/round-38/declared-blocks.txt` → exit=2 | base + freeze exports: absent, exit=2 (live tree now has it untracked — in-round landing, expected) | agree |
| 9 | `ls .ufo/waves/round-38/final-gates/all-gates.txt` → exit=2 | base + freeze + live: absent, exit=2 | agree |
| 10 | `grep -c '⟨pending' corpus/lessons/round-37.md` → 7 (lines 10 90 95 216 265 300 320) | `grep -n` → exactly `10: 90: 95: 216: 265: 300: 320:`, count 7 | agree (exact line list) |
| 11 | `grep -c 'Pending-marker resolutions (round 38)'` → 0 | 0 | agree |
| 12 | L85 'is not landed' → 1 | `grep -c 'is not landed'` on L85 → **0**; L85 bytes: `…but is **not landed**.` (bold markers between "is" and "not"); `grep -c 'not landed'` → 1 | **disagree as written / agree in substance** (see F-2) |
| 13 | `git ls-tree -r --name-only 2387dcf6 -- .ufo/waves/round-37/ \| grep -c results.json` → 0 | 0 (grep exit=1); full ls-tree shows `wave1-dispatch.json` present, no `*-results.json` | agree |
| 14 | round-37 SCORECARD section `Final lane commit:` → 1 | awk over `## Round 37 result` (L1496) to EOF → 1; the line: `Final lane commit: f3246559bed2fd085dde860e00247ce394f02bad (round-37 wave-evidence ancestor; the round's final head is named in the report).` | agree |
| 15 | `grep -c '^Correction (round 38)' SCORECARD.md` → 0 | 0; also `grep -c '^## Round 38' SCORECARD.md` → 0 (no round-38 section at base) | agree |
| 16 | G6: `find kasegi-r36 kasegi-r37 -mindepth 1 \| wc -l` → 1 (`kasegi-r37/build-spec.py`) | now **0 real entries**: both dirs absent (`find` prints only 2 stderr lines) — cleaned mid-wave, improving direction; satisfies G6's "zero entries (or are absent)" | disagree now, drift explained (see F-3) |
| 17 | G7: ledger heading at L37, empty L38-L39, 0 rows | L37 = `## Round-37 dispositions (appended 2026-10-26, R31 home)`; L38/L39 empty; `awk 'NR>=38 && /^\|/'` → 0 rows (file is 43 lines; L41-43 are a separate `## Re-pin note` section, not rows) | agree |
| 18 | G8: `r37-closure.sh --export-ref a173b0c2…` → closed=14/14 exit=0 (run at freeze by L1) | live-lane re-run now: **closed=13/14 exit=1** (E9 red: `status-dirty=3` from in-flight untracked wave1 receipts, `head-match=0` since HEAD=7001535); freeze-state fixture re-run: **closed=14/14 exit=0**, all E1-E14 closed=1 | agree under freeze conditions (see F-4) |

## B. c2-controls/before.txt — per-line re-run (13 lines)

| # | before.txt line (value) | my re-run | verdict |
|---|---|---|---|
| 1 | header: measured 18:16:23Z at base | historical; consistent with the 4-file freeze diff | agree (historical) |
| 2 | frontier rows → 20 | base + freeze: 20 (live tree now 21 — C2 landing in flight, expected) | agree |
| 3 | registry rows → 54 | base + freeze: 54 (live now 55) | agree |
| 4 | S055 row → 0 | base + freeze: 0 (live now 1, shape verified below) | agree |
| 5 | `grep -rlE '^source: S055' corpus/knowledge \| wc -l` → 0 | base + freeze: 0 (live now 1) | agree |
| 6 | `ls corpus/knowledge/*.md \| wc -l` → 49 | base + freeze: 49 (live now 50) | agree |
| 7 | `frontier-recheck-count.py` → entries=23 pass=23 exit=0 | base export: `entries=23 pass=23 exit=0` (23 PASS lines F01-F20, F09/F10/F11 double-row) | agree |
| 8 | `capture-binding-check.py` → records=44 bound=44 unbound=0 | base export: `records=44 bound=44 unbound=0` (13 manifests; pre-existing `orphans=1 orphan=S040-live.txt` informational, not claimed) | agree |
| 9 | `recheck-audit.py --quiet` → expect=present expected=49 missing=0 unexpected=0 exit=0 | base export **with `--cdroot <lane>`**: `strict pass=49/49 cdroot_fail=0 … expected=49 missing=0 unexpected=0 exit=0` | agree (see method note M-1) |
| 10 | uncovered-ground sweep → 0 | base export: `grep -rliE 'CSAF|Common Security Advisory Framework|\bVEX\b' …` → 0 | agree |
| 11 | sibling sweep → 1 file: kake-shokunin/corpus/knowledge/security-txt-publishing.md:63 | 21 `*-shokunin` repos, 20 siblings excluding kasegi; exactly 1 hit: `./kake-shokunin/corpus/knowledge/security-txt-publishing.md`; L63 = `be ignored (S078); securitytxt.org already lists one extension, \`CSAF\` (S079).` | agree |
| 12 | `ls corpus/source-snapshots/round-38` → exit=2 | base + freeze: absent, exit=2 (live now has S055.txt + manifest.json untracked) | agree |
| 13 | junk twin `c2-controls/junk-f21.md` absent (built in-round) | base + freeze: absent; live now has `junk-f21.md` + `junk-f21-recheck.txt` untracked (in-round build, as the line itself notes) | agree |

## C. census-before.txt — per-line re-run (4 lines)

Re-ran `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`:

| # | before line | my re-run | verdict |
|---|---|---|---|
| 1 | `kasegi W04 S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes` | identical line | agree |
| 2 | `kasegi W04 S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes` | identical line | agree |
| 3 | `kasegi ok <lane>/corpus/SOURCES.md` | identical line | agree |
| 4 | `exit=0` | exit=0 — even with the in-flight S055 row in the working tree, no new W/E code (pre-validates the C2 after-claim "census exit 0 (W04 S028/S029 only)") | agree |

## D. Literal checks at 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b

Freeze = base + the 4 control files only, so corpus bytes are identical in both; all counts verified
in both exports:

- **L79-L152 / L399-L454 (r37 append ranges)**: hunks `@@ -78,0 +79,74 @@` (PROVINCE.md) and
  `@@ -398,0 +399,56 @@` (corpus/README.md) between r37 base `b56a41680cef…` and r38 base `a173b0c2…` —
  exactly the claimed ranges/line counts. Content spot-check confirms the D-A characterization:
  PROVINCE L80-152 carries `[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6]…`
  plus property tables and a `Harness on the same mirror (HYAKU_SCRATCH=<scratch> …)` receipt block;
  README L399-454 carries the same receipt prose/tables (L450-452 literally measure
  "`PROVINCE.md` 80, `corpus/README.md` 425" — the pre-paste sizes) and ends inside the unclosed
  fence opened at L426. "Misplaced receipt scaffolding" is grounded.
- **Pending-marker lines L10, L90, L95, L216, L265, L300, L320**: `grep -n '⟨pending'` hits exactly
  those 7 lines, count 7 — matches claims G3 and the spot-check §5 D-C verbatim.
- **L85 not-landed sentence**: present (`…but is **not landed**.`) — grounded (pattern nuance in F-2).
- **f3246559**: `git cat-file -t f3246559` → commit; `f3246559bed2fd085dde860e00247ce394f02bad` =
  "round-37: wave evidence — spec/plan/dispatch (kasegi-r37-build, 64 seats v2)";
  `git merge-base --is-ancestor f3246559 2387dcf6…` → true (ancestor of the r37 judged head); named
  with the full hash in the SCORECARD round-37 section's `Final lane commit:` line. G5's correction
  target is a real, resolvable ancestor — honest, not self-referential.
- **Counts 20/54/49/23/44/49** (frontier / registry / knowledge / harness / binding / audit-expected):
  20, 54, 0-S055, 0-citing, 49 files in base AND freeze exports; harness `entries=23 pass=23 exit=0`;
  binding `records=44 bound=44 unbound=0`; audit `expected=49 missing=0 unexpected=0 exit=0`
  (with `--cdroot`). All six before-counts reproduce exactly.
- **Ledger `## Round-37 dispositions`**: heading at L37 (full text `## Round-37 dispositions
  (appended 2026-10-26, R31 home)`), L38-L39 empty, 0 table rows — D-F's "empty heading" is grounded.
- **G7's "proposals 1-7"**: `considerthese/2026-10-26.md` § Self-improvement suggestions has exactly
  7 numbered items (1-7); item 3 is the quiescence gate — matches claims
  `non_claim_frontier_items.considerthese` ("proposal 3 … mined into C1 G4/G6").
- **G4's field path**: `.ufo/waves/round-38/wave1-dispatch.json` (committed at tip 7001535, an
  ancestor of any J) parses; `taskCall.tasks` exists with **73** tasks — the check's JSON path is
  real, and G4 is non-vacuous at J (at the freeze commit there are no round-38 dispatch files, but
  the dispatch lands before J by construction).
- **"NF=13"**: not a SOURCES.md column (header: `id|source|kind|tier|scope|anchor|teaches|status|
  opened|recheck|used-by`, 11 cells). It is the lane's row-shape convention: `awk -F'|'` field count
  13 = 11 cells with no `|` inside a cell (round-31 lesson L82, round-33 L79, round-35 L67, r36/r37
  spot-checks "S05x row shape … NF=13"). Kill rule "NF != 13" is checkable via awk — grounded.
- **Saturation "9/10 per owned axis, window N=3"**: grounded in SCORECARD §Saturation (L309+):
  "Round-22 declaration. Saturation line: **9/10 on each owned axis** (depth:density,
  depth:verifiability, coverage). Stagnation window: **N = 3**".
- **Routing honesty**: `corpus/lessons/round-37-verifier-spotcheck.md` §5 ("Routed defects") contains
  exactly D-A (L159), D-B (L165), D-C (L169), D3 (L175), D-D, D-E — and no D-F, matching "D-F is
  L1-found". The G1↔D-A … G6↔D-E, G7↔D-F, G8↔carry-over mapping in the C1 predicate is coherent with
  §5's text (D-A's own remedy "add a check that an amendment append equals its declared block
  bytes/sha" is what G1's declared-blocks.txt clause implements; D-B's remedy "state that the receipt
  grades an ancestor and list the post-receipt diff" is what G2's export-ref≤REF + diff⊆{receipt}
  clause implements).

## E. Findings by severity

**F-1 (HIGH — satisfiability tension inside C1; resolvable, must be pinned before ExecSuiteBuild finalizes).**
C1 counting command #1 says `bash corpus/instruments/r38-closure.sh --export-ref <J> -> closed=8/8
exit=0`, and the C1 `after` line says "closed=8/8 exit=0 **at J**". But G2 requires
`.ufo/waves/round-38/final-gates/all-gates.txt` **"in the export"**, and `judged_head_rule` defines
J as the commit that carries every round-38 change **except that receipt**, with the lane tip Y
adding only the receipt (`git diff --name-only J Y` = the receipt path). Under the literal reading,
the export of J cannot contain the receipt, so G2 cannot close at `--export-ref J` ⇒ the suite
prints closed=7/8 at J ⇒ the kill rule ("the judged-head export prints closed != 8/8") false-kills an
honest suite. The dispatch's ExecSuiteBuild task text repeats the same "in the export" wording and
does not resolve it. Two consistent resolutions; the frozen text under-determines which one:
  - (a) the suite, finding the receipt absent from the export of REF, reads it from the live lane at
    the same path and requires `export-ref` ≤ REF with `git diff --name-only <export-ref> REF` ⊆
    {receipt} — this makes counting command #1 literally true at J and is exactly the spot-check's
    D-B remedy ("the receipt grades an ancestor and lists the post-receipt diff"); or
  - (b) the green run is `--export-ref Y` (the only ref whose export contains the receipt), and
    counting command #1 should read `<Y>` (erratum).
  Either preserves discrimination (base and r37-head exports stay red: G1/G3/G5/G7 fail there on
  bytes that exist at those heads). What is NOT acceptable: a suite that skips G2 when the receipt
  is absent — that would make `--export-ref J` green with the receipt binding never tested, i.e. the
  vacuous pass the kill rule's forgery clause guards against. Related wording note: `judged_head_rule`'s
  "Lane files never name J by hash" is loose — the receipt itself names J by hash (G2 requires it);
  the precise rule is "no lane file labels J (or any hash) as the final head; the receipt binds J as
  `export-ref=` from Y, where J ≠ Y, so no commit contains its own hash".

**F-2 (LOW — before-log pattern abbreviation).** c1 before line 12 logs the L85 probe as
`'is not landed' -> 1`; the L85 bytes are `is **not landed**` (bold markers), so the quoted pattern
scores 0 and only `not landed` scores 1. Substance true, logged pattern not verbatim. Cosmetic.

**F-3 (INFO — G6 live drift, improving).** The before value (1 entry: `kasegi-r37/build-spec.py`)
was true at freeze (the spot-check §5 D-E documents exactly that path); at re-run both
`kasegi-r36` and `kasegi-r37` are absent — cleaned mid-wave, which satisfies G6's "zero entries (or
are absent)". Note for the r38 suite: the before-control measured ANY entry (`find -mindepth 1`),
while r37's E9 scratch limb used `-type d` (dirs only) — that is why E9 passed at freeze despite the
file. The claims' G6 wording ("hold zero entries") is the stricter any-entry reading; the r38 suite
should implement the stricter one (the dispatch's G6 wording — "absent or empty … no entry other
than the suite's own --work dir … unreadable dir is RED" — already does).

**F-4 (INFO — G8 re-run needs freeze conditions).** Live-lane re-run of G8 now prints closed=13/14
(E9 live limbs: `status-dirty=3` from in-flight untracked wave1 receipts; `head-match=0` since HEAD
moved to 7001535; `scratch-root=absent` since kasegi-r37 was cleaned). In a verified fixture clone
(clean tree, HEAD=base, full history) the same suite byte-reproduces `closed=14/14 exit=0`. The
before value is honest; the divergence is mid-wave drift, and it usefully demonstrates that E9's
live limbs are load-bearing (a do-nothing control cannot keep them green across a wave).

**F-5 (INFO — method note M-1, audit cdroot).** `recheck-audit.py --quiet` exits 0 at base only when
the cd targets baked into the entries match the audit root: run in a tar export or a fixture clone
without `--cdroot`, it prints `cdroot_fail=48 … exit=1`; with `--root <base> --cdroot <lane>` it
prints `strict pass=49/49 … expected=49 missing=0 unexpected=0 exit=0` (the instrument's own
`--cdroot` help says to set it "when --root is a scratch copy of the corpus"). The before line's
exit=0 is honest under the in-lane invocation; future verifiers re-running from copies must pass
`--cdroot` or they will false-flag this line. (Live lane today, mid-wave: `strict pass=50/50 …
expected=50 … exit=0` — the C2 landing is already materializing consistently.)

**F-6 (INFO — G4 non-vacuity timing).** At the freeze commit there are no round-38 `*-dispatch.json`
files, so G4 would be vacuous if evaluated at freeze; it is evaluated at J, where the dispatch
(committed at 7001535, `taskCall.tasks` = 73) is necessarily present, so the check is non-vacuous
and requires a tracked, seat-count-equal `*-results.json` (r37 precedent:
`kasegi-r37-build-results.json`, 64/64, landed at 83975acc after `complete` — the exact D3 defect
G4 closes). No action needed; recorded so the vacuity question is answered with evidence.

**F-7 (MINOR — fence-walk spec precision).** G1's walk rule ("closing fence = ``` with no info
string") under-specifies CommonMark length matching (a closing fence must be at least as long as its
opener; a 4-tick opener is not closed by a 3-tick closer). No 4-tick fence lines exist at base
(verified: only the 3-tick lines listed above), so every base measurement is unaffected; the r38
suite should implement the length rule anyway to stay CommonMark-faithful on future appends.

**F-8 (MINOR — kill-rule grep presupposition).** The C1 kill rule's
`grep -c '⟨pending' corpus/lessons/round-38.md` presupposes the file exists; on a missing file grep
prints no count and exits 2. The round-38 lesson will exist in-round, but the suite should treat an
absent file as RED (fail-closed), not as a skipped check.

## F. Do-nothing-control and self-reference analysis

- **C1 is not do-nothing-reachable.** The kill rule requires the base export AND the r37-judged-head
  export to print closed<8/8 while J prints 8/8. At base, G1 (Corrections 0/0, declared-blocks
  absent), G2 (all-gates absent), G3 (7 pending markers, no resolutions section), G4 (no round-38
  dispatch/results), G5 (Final-lane-commit 1, Correction 0), G7 (ledger 0 rows) all fail on bytes I
  verified — the base red is real, so the green at J requires the actual work.
- **C2 is not do-nothing-reachable.** Every before count must move (20→21, 54→55, 0→1 citing,
  49→50, 23→24, 44→45, expected 49→50) and the predicate requires the junk twin to exist and be
  rejected (live tree already carries `junk-f21.md` + `junk-f21-recheck.txt` untracked). No count
  moves without the S055 work.
- **No self-referential clause.** The one structural risk — a commit naming its own hash — is
  explicitly routed around by `judged_head_rule` (lane files name J only by reference; the report
  names J and Y; the receipt at Y names J where J ≠ Y). Verified non-self-naming bindings: the
  receipt's `suite-sha256=` hashes the suite (a different file); `declared-blocks.txt` hashes
  PROVINCE/README end-of-file blocks (not itself); SCORECARD's f3246559 line names an ancestor of
  the commit containing it. The only wording looseness is F-1's related note.
- **C2 live satisfiability probes (read-only, mid-wave)**: S055 row landed in the working tree with
  `NF=13`, `kind spec`, tier `A`, status `mined`, opened `2026-10-26`, the claimed URL
  `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`; `capture-binding-check.py` →
  `records=45 bound=45 unbound=0`; `frontier-recheck-count.py` → `entries=24 pass=24 exit=0` incl.
  `PASS F21 knowledge/csaf-vex-product-status-and-justifications.md ids=S055`;
  `source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055` →
  exit 0 (Q2/Q3/Q4 OK lines). The C2 predicate is satisfiable and is being satisfied by the bytes
  now in flight.

## G. Tooling record

No tools installed or upgraded (pacman never invoked; existing bash/git/python3 sufficient).

## H. Scratch

`S=/fast/scratch/hyaku/kasegi-r38/RevClaimsFreeze/` (base/frz/r37h exports, fixture clone, work dirs)
removed before yield; no other scratch created; nothing written outside the receipt path and scratch.
