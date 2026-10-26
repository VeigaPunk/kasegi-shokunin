# RevSpotCheckReadiness — round 37 non-author spot-check readiness contract

Seat: RevSpotCheckReadiness-2 · Round: kasegi-shokunin 37 (hyaku run 9) · Scanned 2026-10-26.
Axes judged: depth:verifiability, coverage. Receipt only; no lane file edited; no tool installed
(stdlib `python3` + `git` + `bash` sufficed; no pacman run).

## Scan-time state (all observed live, read-only)

- Lane HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0` = claims-erratum-1 (S054 capture URL corrected,
  filed before any seat scored). Freeze `224df74db2a46d627ae1475a72ca48796bbd177c`; base
  `b56a41680cefd391868c1c370dc063c69d827e7d`. All five round-relevant hashes verified `commit` via
  `git cat-file -t`: base, freeze, HEAD, r36 base `cc692008…`, r36 judged `a23dc478…`, r36 lane head
  `c20300df…`.
- The wave is MID-FLIGHT: the C1 suite `corpus/instruments/r37-closure.sh`, the capture
  `corpus/source-snapshots/round-37/`, and `.ufo/waves/round-37/final-gates/all-gates.txt` do not
  exist yet (before-state, recorded at freeze in `.ufo/waves/round-37/c1-controls/before.txt` and
  `c2-controls/before.txt`; re-confirmed live today). Every checklist item below names the
  **committed file/command that must exist at the round-37 judged head** and its **expected output**.
- Live before-state re-confirmations (these are the numbers a fresh reviewer must see move):
  `frontier-recheck-count.py` → `entries=22 pass=22 exit=0`; `capture-binding-check.py` →
  `records=43 bound=43 unbound=0` exit 0; `recheck-audit.py --quiet` → `strict pass=48/48 …
  expected=48 missing=0 unexpected=0 exit=0`; census → exit 0, W04 S028/S029 only; frontier rows 19;
  SOURCES rows 53; entries citing S054 → 0; `ls corpus/knowledge/*.md | wc -l` → 48.
- D1–D6 defect states are OPEN in committed bytes today (baselines for the E10–E14 greps):
  D1 final-gates receipt absent; D2 false path `corpus/instruments/r36-fixtures/` claimed landed at
  `LOG.md:1665` (round-36 C1 bullet; `git ls-tree` shows 0); D4 stale label `Final lane commit:
  e666d902337a49dcbfc77880939874f39c6f477b` at `SCORECARD.md:1492` (Round-36 section); D5
  `SKILL.md:1111` r36-closure.sh row type cell is the literal `gate\|probe` and its verdict map has
  no exit-2 row; D6 `corpus/instruments/r36-closure.sh:466` `porcelain=${porcelain:-0}` (fail-open).
  Routing of record: `corpus/lessons/round-36-verifier-spotcheck.md` §5, lines 144–160.

**URL authority for every S054 item below:** `.ufo/waves/round-37/claims-erratum-1.md` (commit
`b362068`) supersedes the frozen claims.json literal `https://certcc.github.io/SSVC/` with
`https://certcc.github.io/SSVC/tutorials/ssvc_overview/` (the "What is SSVC?" overview tutorial
page). The frozen file is never edited; the erratum is the appended correction. A reviewer who
checks the old home-page URL is reading a superseded literal.

---

## Readiness checklist — what a fresh reviewer re-opens

Scratch convention for all commands: `S=/fast/scratch/hyaku/kasegi-r37/<reviewer-seat>` (mkdir -p,
removed after); `/tmp` only for files <50 MB. `<JUDGED>` = the round-37 final lane head hash named
in the round-37 SCORECARD section. Run everything **after** the wave-integration commit, when the
lane tree is quiescent.

### 1. S054 capture page (URL / quote / occurrences) — closes C2 capture-binding clauses

Must exist at `<JUDGED>`: `corpus/source-snapshots/round-37/S054.txt`,
`corpus/source-snapshots/round-37/manifest.json`,
`corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (header `source:
S054`), and an S054 row in `corpus/SOURCES.md`.

| # | Command | Expected |
|---|---|---|
| 1a | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054` | exit 0; sha256 of `S054.txt` matches the manifest's declared value; every declared quote prints `occurrences=N` with N ≥ 1; declared `anchor` line verified (round-24 checker behavior); any quote < 12 normalized chars would have been rejected `quote-too-short-to-be-evidence` |
| 1b | `python3 corpus/instruments/capture-binding-check.py` | `records=44 bound=44 unbound=0`, exit 0 (43→44: the new round-37 record). Rule B5: record `url` equals, byte-for-byte, the S054 row's exactly-one `https://` token — i.e. the corrected tutorial URL. Rule C: strict-UTC `fetched_utc` mandatory (round-32+ dirs; `Z` or `+00:00`, real calendar instant; `pending`/local-offset/malformed all fail) |
| 1c | `grep -c 'https://certcc.github.io/SSVC/tutorials/ssvc_overview/' corpus/SOURCES.md` | ≥ 1 (the S054 row's source cell); the row carries exactly one `https://` token (rule B4) |
| 1d | `grep -rlE '^source: S054 ' corpus/knowledge | wc -l` | 1 (the SSVC entry; 0 today) |

### 2. Junk twin rejection — closes C2 kill rule "junk-f20 accepted by source-recheck or harness"

Must exist at `<JUDGED>`: `.ufo/waves/round-37/c2-controls/junk-f20.md` (3–4 fabricated sentences
NOT on the SSVC page — spec examples: "SSVC guarantees a fixed remediation deadline for every
vulnerability", "SSVC replaces CVSS severity scoring", "SSVC is maintained by FIRST") and the
rejection transcript in `.ufo/waves/round-37/wave1/ExecC2JunkControl.md`.

- Reviewer re-run: copy `corpus/instruments/source-recheck.py` to scratch, build a scratch manifest
  asserting each fabricated sentence against the round-37 capture, run it → expect exit 1 with
  `quote-not-found` per sentence (or `not-listed`). The committed harness must also refuse it:
  `python3 corpus/instruments/frontier-recheck-count.py` stays `entries=23 pass=23 exit=0` with no
  junk row admitted.

### 3. Census exits — closes C2 kill rule "census exit != 0"

Committed before-receipt: `.ufo/waves/round-37/census-before.txt` (frozen). Reviewer re-run:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

Expected: exit 0 and exactly three output lines — `W04 S028 duplicate url
docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes`, `W04 S029 duplicate
url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes`, `ok …/kasegi-shokunin/corpus/SOURCES.md`.
No E-codes; the new S054 row must not add a duplicate-id/duplicate-URL E-code (pre-proven on a
mirror by `.ufo/waves/round-37/wave1/ExecCensusReplay.md`). Re-confirmed live today: exit 0, W04
S028/S029 only.

### 4. r37 suite reds + selftest — closes C1

Must exist at `<JUDGED>`: `corpus/instruments/r37-closure.sh` — fourteen checks E1–E14, export-only
mode (same mechanics as r36-closure.sh: `git -C <lane> archive <ref> | tar -x -C $S/export`; a plain
run without `--export-ref` refuses exit 2; nothing written under the lane).

| # | Command | Expected |
|---|---|---|
| 4a | `bash corpus/instruments/r37-closure.sh --export-ref <JUDGED>` | fourteen `E<n> payload=… closed=1` lines, then `closed=14/14 exit=0` |
| 4b | `bash corpus/instruments/r37-closure.sh --export-ref cc692008b0cfd58d18275aa6c4aed79620120799` | `closed<14/14 exit=1` (r36 base red) |
| 4c | `bash corpus/instruments/r37-closure.sh --export-ref a23dc4788aa7c98831eed6db953434034ce5ae8d` | `closed<14/14 exit=1`, with E10–E14 the open checks there (r36 judged head red) |
| 4d | `bash corpus/instruments/r37-closure.sh --selftest --export-ref <JUDGED>` | fourteen `selftest case=E<i> positive=… mutants=<ok>/<n> verdict=…` lines + `selftest cases=14 failures=0`, exit 0 |
| 4e | `bash corpus/instruments/r37-closure.sh` (no flag) | refused, exit 2 |

### 5. E10–E14 defect-state greps (run inside a scratch export of `<JUDGED>`)

Export once: `mkdir -p $S/export && git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive
<JUDGED> | tar -x -C $S/export`, then:

- **E10 (D1)** — `.ufo/waves/round-37/final-gates/all-gates.txt` in the export:
  `head -1 $S/export/.ufo/waves/round-37/final-gates/all-gates.txt` → `suite-sha256=<sha>` and
  `sha256sum $S/export/corpus/instruments/r37-closure.sh` → the same `<sha>` (header binds the suite
  bytes); `grep -cE '^E[0-9]+ payload=' <receipt>` → 14; `grep -c 'closed=14/14 exit=0' <receipt>`
  → 1; `grep -c 'selftest case=' <receipt>` → 14; `grep -c 'cases=14 failures=0' <receipt>` → 1.
  Today: file absent (D1 open).
- **E11 (D2)** — `git show <JUDGED>:LOG.md | grep -n 'r36-fixtures'`: the round-37 entry must carry
  a named CORRECTION of the round-36 C1 bullet's false `corpus/instruments/r36-fixtures/` path (the
  false claim itself remains at LOG.md:1665 in the round-36 entry — append-only log; the correction
  is new round-37 text). A round-37 entry that never names the false path fails.
- **E13 (D5)** — `grep -nE '^\| `?r36-closure\.sh`?[[:space:]]*\|' $S/export/SKILL.md`: the row's
  type cell is a single choice (`gate` or `probe`), NOT the literal `gate\|probe` visible at
  SKILL.md:1111 today, AND the same row's verdict cell maps exit `2` → `could-not-evaluate` (scope
  the grep to this row — the recheck-audit.py row at SKILL.md:981 already carries that token).
- **E14 (D6)** — `grep -cF 'porcelain:-0' $S/export/corpus/instruments/r37-closure.sh` → 0 AND
  `grep -n 'git status' $S/export/corpus/instruments/r37-closure.sh | grep -c '2>/dev/null'` → 0
  (a failed status read is red, never defaulted to clean). Baseline defect:
  r36-closure.sh:466 `porcelain=${porcelain:-0}`.
- **E12 (D4)** — see item 6.

### 6. Anchor-ancestor label — closes D4

Must exist at `<JUDGED>`: the round-37 lesson (`corpus/lessons/round-37*.md`) and a round-37
SCORECARD section (`## Round 37 — …`).

- `grep -n 'anchor ancestor' $S/export/corpus/lessons/round-37*.md` → ≥ 1, naming the r36 lane head
  `c20300df516eb5575d8db2aaad1f0cf4913e7981` as anchor ancestor.
- `sed -n '/^## Round 37/,$p' $S/export/SCORECARD.md | grep -c 'Final lane commit: e666d902'` → 0
  (stale label confined to the Round-36 section at SCORECARD.md:1492 today; must not recur in the
  round-37 section). The round-37 section's own `Final lane commit:` hash must resolve and be an
  ancestor of `<JUDGED>` (E1's binding limb proves this from the export).
- Kill-rule placeholder greps: `grep -c 'filled by the L1' SCORECARD.md` → 0;
  `grep -c '<LANE_HASH>' SCORECARD.md` → 0 (both 0 today).

### 7. No-harm diff — closes the no-harm invariant (RevNoHarm command set)

- `git -C <lane> diff --numstat b56a41680cefd391868c1c370dc063c69d827e7d..<JUDGED>`: for
  `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
  `corpus/README.md` — additions > 0, **deletions = 0** (append-only; existing line numbers
  preserved). Changed paths confined to lane-internal areas: `SKILL.md`, `LOG.md`, `SCORECARD.md`,
  `PROVINCE.md`, `corpus/**` (README, SOURCES, QUALITY, `instruments/r37-closure.sh`,
  `instruments/knowledge-expected.txt`, `knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`,
  `source-snapshots/round-37/**`, `lessons/round-37*`, `considerthese-ledger.md`),
  `.ufo/waves/round-37/**` (claims-erratum-1.md, final-gates/**, wave1/**). No path outside the lane
  repo.
- SKILL.md prefix integrity (registry rows appended only after the r36 rows, ~:1106):
  `git show <JUDGED>:SKILL.md | head -n $(git show b56a4168…:SKILL.md | wc -l) | sha256sum` must
  equal `git show b56a4168…:SKILL.md | sha256sum`.
- Baselines measured live today (must not move except by append): `density.py SKILL.md` → mean dens
  **225.3**, 751 path-citation instances across 27 blocks; `anchorcheck.py SKILL.md` → `16 in-range
  cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0
  OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0.
- Expected-list sync (part of the same no-harm/audit closure):
  `grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` → 49 (48 today, verified)
  and `python3 corpus/instruments/recheck-audit.py --quiet` → `strict pass=49/49 … expected=49
  missing=0 unexpected=0 exit=0`. The sync is load-bearing: with the entry but without the sync the
  audit reads `unexpected=1 exit=1` (negative control in
  `.ufo/waves/round-37/wave1/ExecExpectedListSync.md`).

---

## Reviewer cautions

1. **Quiescence items are red mid-wave by design.** `git status --porcelain` is nonempty today (6
   untracked wave entries) and seat scratch dirs exist under `/fast/scratch/hyaku/kasegi-r37/` while
   the wave runs. E9's quiescence limbs (`git status --porcelain` empty; `find
   /fast/scratch/hyaku/kasegi-r37 -mindepth 1 -maxdepth 1 -type d | wc -l` → 0) are judged at
   filing time, after integration and scratch cleanup — not at scan time.
2. **Export-only suite.** Never accept a green from a worktree-reading run; the plain run must
   refuse exit 2 (r36 precedent, r36-closure.sh header).
3. **Erratum precedence.** claims.json is frozen and never edited; `.ufo/waves/round-37/claims-erratum-1.md`
   (b362068) is the operative S054 URL. Any checklist variant still carrying
   `https://certcc.github.io/SSVC/` for the capture is stale.
4. **Occurrence discipline.** source-recheck prints `occurrences=N` on every pass (round-24 rule);
   a pass without a printed occurrence count is not the committed checker's pass shape.

## Residual risk / verification gaps

- The r37 suite bytes, the capture, and the final-gates receipt do not exist at scan time; every
  expected output above is specified from the frozen claims + committed checker semantics
  (r36-closure.sh mechanics, source-recheck/capture-binding-check rules), not from a live green run.
  The judged-head run (4a/4d) and the two reds (4b/4c) remain to be executed by the reviewer at
  `<JUDGED>`.
- `<JUDGED>` itself is unknown until integration; E1's ancestry limb is the check that binds it.
- Scratch dir `/fast/scratch/hyaku/kasegi-r37/RevSpotCheckReadiness-2/` removed before this receipt
  was finalized; no lane or fleet file was written except this receipt.
