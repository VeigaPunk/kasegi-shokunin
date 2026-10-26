# RevClaimsFreeze — round-37 frozen claims satisfiability at base (QUALITY R22/R25)

Seat: RevClaimsFreeze-2 · Round 37 · Lane kasegi-shokunin · 2026-10-26
Base `b56a41680cefd391868c1c370dc063c69d827e7d` · freeze `224df74db2a46d627ae1475a72ca48796bbd177c`
Rules applied: `corpus/QUALITY.md:226` (R22 — every literal constant and regex in predicate/kill rule run against the base tree) and `:229` (R25 — literals checked against base bytes **plus the round's declared after-adds**; a literal true at base but false at the declared after-state is fixed before data).

## Method

All measurements against base bytes, read-only. Two vehicles:

1. **Base export** — `git archive b56a4168 | tar -x` into scratch (`/fast/scratch/hyaku/kasegi-r37/RevClaimsFreeze-2/base`, 7200 files); greps and instrument runs executed inside it.
2. **Scratch clone fixtures** (needed because three instruments key on a real git checkout): `git clone --no-hardlinks` of the lane into scratch, `checkout` pinned at `b56a4168` (and at `a23dc478` for one run), toplevel verified before use. No mutating git command touched the lane, fleet, or any source tree.

Deviations from the literal counting commands, both forced by the instruments' design and both recorded per row below: (a) `recheck-audit.py` run as `--root <base-clone> --cdroot <lane>` (see Finding F1); (b) census run as `sources-census.sh validate --root <scratch-fleet> kasegi` where `<scratch-fleet>/kasegi-shokunin` symlinks the base clone and `shokunin.conf` is copied read-only into scratch.

## C1 (depth:verifiability) — per-literal verdicts at base

| # | Literal (source) | Expected at base | Measured | Verdict |
|---|---|---|---|---|
| C1-1 | `corpus/instruments/r37-closure.sh` absent (before; kill `ls_exit=2`) | absent, ls exit 2 | absent, exit 2 | **TRUE** |
| C1-2 | `.ufo/waves/round-37/final-gates/all-gates.txt` absent (D1 open) | absent | absent | **TRUE** |
| C1-3 | D2: LOG.md round-36 C1 bullet cites `corpus/instruments/r36-fixtures/` | present | `LOG.md:1665` — "Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`" | **TRUE** |
| C1-4 | D2: `git ls-tree -r base` r36-fixtures count | 0 | 0 | **TRUE** |
| C1-5 | D4: SCORECARD labels `Final lane commit: e666d902` | 1 | 1 — `SCORECARD.md:1492`, inside the `## Round 36` section (starts :1406, last section at base) | **TRUE** |
| C1-6 | D4: round-36 lesson labels e666d902 as final lane commit | present | `corpus/lessons/round-36.md:3` — "final lane commit `e666d902337a…` (filled at closure)" | **TRUE** |
| C1-7 | D5: SKILL.md `r36-closure.sh` registry row type cell is literal `gate\|probe` | present | `SKILL.md:1111`, first cell exact `r36-closure.sh`, type cell `gate\|probe` | **TRUE** |
| C1-8 | D5: that row's verdict map omits exit 2 / `could-not-evaluate` | absent in row | `could-not-evaluate` occurs exactly once in SKILL.md — `:981`, the `recheck-audit.py` row; absent from the r36-closure.sh row | **TRUE** |
| C1-9 | D6: `grep -cF 'porcelain:-0' corpus/instruments/r36-closure.sh` ≥ 1 | 1 | 1 | **TRUE** |
| C1-10 | D6: status read swallows failure (`2>/dev/null`) | present | `r36-closure.sh:465` — `porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)` then `porcelain=${porcelain:-0}` (:466) | **TRUE** |
| C1-11 | `grep -c 'filled by the L1' SCORECARD.md` (counting cmd #5; kill ≠0) | 0 | 0 | **TRUE** |
| C1-12 | `grep -c '<LANE_HASH>' SCORECARD.md` (kill ≠0) | 0 | 0 | **TRUE** |
| C1-13 | worktree clean 0 at base (before) | 0 | **RECORDED-ONLY** — measured 0 in `c1-controls/before.txt` at 16:31Z; a historical worktree state is not re-verifiable post-freeze. Live tree is now dirty (6 entries: wave1 dir, assimilation/, run err files, one modified r36 scribe receipt) — expected mid-round; the frozen `claims.json` itself is byte-identical to 224df74d (`git diff --stat` empty) | RECORDED |
| C1-14 | scratch leftovers 0 at base (before) | 0 | **RECORDED-ONLY** — before.txt measured 0; live `/fast/scratch/hyaku/kasegi-r37` now holds running seats' dirs (this seat's included until cleanup) — expected mid-round; kill rule binds at filing | RECORDED |
| C1-15 | E1–E9 inputs present at base (carried checks E2 erratum, E3 both registry rows, E4 tracked+provenance, E5 `.ufo/waves/round-35/claims-erratum-d5.md`, E6 `.ufo/waves/round-34/wave1/L1Integration.md` 'Correction (round 35)', E7 QUALITY supersedes-R22/R23 rows, E8 round-36 lesson correction) | all green | **LIVE**: `r36-closure.sh --export-ref b56a4168` (from base clone, `--lane/--scratch-root/--work` overrides) → E1–E9 all `closed=1`, `closed=9/9 exit=0` | **TRUE (live run)** |
| C1-16 | "(E10-E14 open there)" implies E1–E9 green at r36 judged head `a23dc478` | green | **LIVE**: same suite at `--export-ref a23dc478…` → `closed=9/9 exit=0` | **TRUE (live run)** |
| C1-17 | Required-red achievability: round-37 inputs absent at `cc692008` and `a23dc478` | absent | `ls-tree` 'round-37' matches: 0 at both heads → E10/E11/E12 red there; E13 red (row `gate\|probe` at a23dc478 / row absent at cc692008); E14 red (r37-closure.sh absent) → `closed<14/14 exit=1` reachable at both | **TRUE** |

## C2 (coverage) — per-literal verdicts at base

| # | Literal (source) | Expected at base | Measured | Verdict |
|---|---|---|---|---|
| C2-1 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 19 | 19 | **TRUE** |
| C2-2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 53 | 53; ids exactly S001–S053 contiguous, S054 free | **TRUE** |
| C2-3 | S054 registry row | 0 | 0 | **TRUE** |
| C2-4 | `grep -rlE '^source: S054 ' corpus/knowledge \| wc -l` | 0 | 0 | **TRUE** |
| C2-5 | `frontier-recheck-count.py` | entries=22 pass=22 exit=0 | entries=22 pass=22 exit=0 (22 PASS lines, F01–F19) | **TRUE** |
| C2-6 | `capture-binding-check.py` | records=43 bound=43 unbound=0 | records=43 bound=43 unbound=0, exit 0 (12 manifest dirs; pre-existing quirks multi_row_url=2, orphan=S040-live.txt do not affect the literals) | **TRUE** |
| C2-7 | `recheck-audit.py --quiet` | strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0; expected=48 missing=0 unexpected=0 exit=0 | reproduced exactly: `strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0 … expected=48 missing=0 unexpected=0 exit=0` — via `--root <base-clone> --cdroot <lane>` (see F1); bare invocation in any non-lane cwd fails cdroot 47/48 | **TRUE (with documented deviation)** |
| C2-8 | `ls corpus/knowledge/*.md \| wc -l` | 48 | 48 | **TRUE** |
| C2-9 | `knowledge-expected.txt` in sync (48 entry lines) | 48 | `corpus/instruments/knowledge-expected.txt`: 50 lines = 2 `#` comments + 48 entry paths; audit set-equality passed | **TRUE** |
| C2-10 | `c2-controls/junk-f20.md` absent (control not yet built) | absent | absent | **TRUE** |
| C2-11 | `corpus/source-snapshots/round-37` absent/empty | absent | absent | **TRUE** |
| C2-12 | census: exit 0, W04 S028/S029 only | reproduced | `W04 S028 duplicate url docs.hackerone.com/…`, `W04 S029 duplicate url eur-lex.europa.eu/…`, `ok …/SOURCES.md`, exit 0 — via scratch fleet root (see Method) | **TRUE (with documented deviation)** |
| C2-13 | Kill-rule "S054 row malformed (NF != 13)" satisfiable | NF=13 is the well-formed shape | census contract header: "one registry table, 11 columns => NF=13"; S053 row measures `awk -F'|'` NF=13 | **TRUE** |
| C2-14 | After-add collision guard: `certcc.github.io/SSVC` absent at base | 0 | 0 (the one base `certcc` row is S004, url `certcc.github.io/certcc_disclosure_policy/` — different URL, no W04/multi-row collision for the S054 after-add) | **TRUE** |

## R25 — after-state consistency (base + declared after-adds)

Every after literal is a +1 delta over a verified base count, driven by exactly the declared after-adds (one F20 row, one S054 row, one knowledge entry, one manifest record, one expected line, one harness entry):

- frontier 19→20; registry 53→54; `source: S054`-citing entries 0→1 (existing convention `source: S053 — <url> — capture …` matches the `^source: S054 ` regex); knowledge 48→49; harness 22→23 (harness entries map knowledge entries to frontier rows); binding 43→44 (SSVC url unique at base → record binds, no multi-row growth); audit expected 48→49 (expected-file sync declared); junk-f20 0→rejected; census W04 set unchanged (S054 url introduces no duplicate across scopes).
- C1 after-adds (r37-closure.sh, final-gates/all-gates.txt, LOG round-37 correction, round-37 lesson + SCORECARD section, SKILL row edit) are all new/appended text; the E1–E9 inputs they must not break are verified green at base and at a23dc478, and the required reds are reachable (C1-17). E10's self-referential digest (sha of the suite bytes) is well-defined. E13's `could-not-evaluate` vocabulary already exists in the registry (`SKILL.md:981`), so the exit-2 verdict addition introduces no new convention.

**No literal was found false at base, and none true at base but false at the declared after-state. R22 and R25 both SATISFIED — no pre-data correction required.**

## Findings

- **F1 (MEDIUM, final-gate fragility — pre-existing instrument property, not a freeze defect):** the C2 counting command `python3 corpus/instruments/recheck-audit.py --quiet` is environment-bound: every knowledge entry's `recheck:` line bakes the absolute lane path in a `cd <path> &&` prefix, so the strict cdroot limb passes only when the audit runs at the real lane root. Bare invocation in any export/clone fails `cdroot_fail=47/48, exit=1` (fail-closed, substance untouched). The L1's final gate must run it at the live lane root; any export-based rerun of this command reads red for venue, not for defect. Reproduction here needed `--root <base-clone> --cdroot <lane>`.
- **F2 (LOW, id-reuse ambiguity):** `S054` already names a *different* source in base history — the staged 内閣府 vulnerability-information PDF, refused `payload-absent`/`prose-class-unverifiable` (`corpus/lessons/round-33.md:61`, `round-34.md:166`, `round-35.md:120,135,460`). C2 mints registry S054 for SSVC, and the round-37 quarantine slice will again print "S054 payload-absent" beside the admitted SSVC row. Claim literals are count-based and unaffected, but the round-37 lesson should disambiguate (e.g. "staged S054 (内閣府)" vs "registry S054 (SSVC)") so a future verifier cannot read the coexisting verdicts as a contradiction. The round's own id-collision study (registry 53 × staged 94) shows awareness; this row is a live instance of it.
- **F3 (LOW, E9 live-state coupling):** the closure suite's E9 reads the *live* lane worktree and the live `/fast/scratch/hyaku/kasegi-r37` root (r36-closure.sh:448-485 shape, carried into r37 fail-closed). Mid-round runs are red while any seat dir exists; the final gate is only green after scratch cleanup with a clean worktree — the kill rule already binds this at filing. Seats (this one included) must remove scratch before yield.
- **F4 (INFO):** `F20` appears in base lessons only as dated history of a rejected entry whose `ground:` named a then-nonexistent frontier id (`round-25.md:115`); no conflict with the after-state F20 row.
- **F5 (INFO):** base binding quirks `multi_row_url=2` and `orphan=S040-live.txt` pre-date this round and do not interact with any claim literal.

## Verification gaps

- C1-13/C1-14 (base-time worktree and scratch cleanliness) rest on the committed before-controls' own 16:31Z measurements; not independently re-verifiable after the fact.
- After-state greens (`closed=14/14`, `cases=14 failures=0`, harness 23/23, audit 49/49, junk rejected) are achievability findings, not measurements — the round-37 artifacts they quantify do not exist yet. The r37 suite's own mutant fixtures (kill rule: "any single E-check's committed fixture proves the check can pass while its defect is present") are a design requirement on the suite author, unverifiable at base.

## Tooling record

No installs or upgrades performed (operator 2026-10-19 authorization unused): system `git`, `bash`, `python3`, coreutils only. Scratch `/fast/scratch/hyaku/kasegi-r37/RevClaimsFreeze-2/` removed after this receipt was written.
