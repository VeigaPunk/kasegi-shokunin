# kasegi round 36 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure of lane-round kasegi 36. The judge did not author the round, dispatched no lane work, and edited no
lane-authored file. Inputs: report `.ufo/reports/round-36/kasegi.md` (fleet repo), prompt
`.ufo/prompts/kasegi-round-36.md`, lane base `cc692008b0cfd58d18275aa6c4aed79620120799` (B), judged head
`a23dc4788aa7c98831eed6db953434034ce5ae8d` (A). Branch tip at closure: `c20300df516eb5575d8db2aaad1f0cf4913e7981`
(a later commit that touches `.ufo/waves/round-36/` only; see §5 D3).

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 1527/1532 at read time):

    2026-10-26T12:31:14-03:00 launch kasegi round=36 pgid=14809 driver=hyaku-inline attempt=1
    2026-10-26T13:02:47-03:00 complete kasegi round=36; hyaku-inline attempt=1

`grep -c 'lane-dead-no-report kasegi round=36' .ufo/watchdog.log` → `0`.

Measurement method: `git -C <lane> archive <ref> | tar -x` into scratch trees for B and A, then plain
`grep`/`awk`/`ls`/`git ls-tree`/`sha256sum` over the extracted committed bytes. No lane gate or instrument
was executed (PROTOCOL §Gate standard, Closure consequence).

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an %H %s' -- .ufo/reports/round-36/kasegi.md` | `kasegi-shokunin dd1ad9cf94065ef8a20f41eb10faf85f62e3c750 round-36: kasegi report`; erratum `kasegi-shokunin 1c43fd8f2d6c8648b25600d14a04f512dda87cbe` (appended 4 lines, no rewrite) | conformant |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` on the report; `SHONEN.md` box count | `1`; four `[~]` lines against the four `SHONEN.md` boxes | conformant |
| Cited lane commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `cc692008`, `b47f2cdf`, `caa314625`, `e666d902`, `2c26a97e`, `e9c57c43`, `274fa9ae`, `a23dc478` | all eight resolve; all `anc=0` (ancestor) | conformant |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `state branch=master local=c20300df… remote=c20300df… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | conformant |
| Prompt carries the template contract | read `.ufo/prompts/kasegi-round-36.md` §1–§5 | MISSION/AXES binding, 1–3 claims, frontier step §2b, L2 floor §3, report path + sections + SHONEN §4, commit/push scope/L0 §5, hyaku addendum §6 | conformant |
| Report is not a marker | report names claims, commits, commands | real committed work | status `ok` |

Defects recorded (status-neutral): report filed with an open "wave results not finalised" item, then an
erratum and a further lane commit after `complete` (§5 D3).

## 2. Claims — re-derived at A

### C1 — depth:verifiability (held 4): VERIFIED (re-measured by plain reads + evidence-verified)

Predicate (frozen `claims.json`): `r36-closure.sh --export-ref <final head>` → `closed=9/9 exit=0`;
`--selftest` → `cases=9 failures=0`; r35 base `3266c993` → `closed=0/9 exit=1`; r35 judged head `0aee0ef` →
`closed<9/9 exit=1`.

Suite bytes: `sha256sum corpus/instruments/r36-closure.sh` at A →
`4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (894 lines), equal to the digest the
suite prints in its run header and that the receipts cite. Absent at B (`ls` exit 2).

Each check's limbs, re-derived from the suite's own definitions (header lines 54–106) with plain reads
over A — not by running the suite:

| Check | Plain command at A | Observed | Closed? |
|---|---|---|---|
| E1 | `grep -cF 'filled by the L1' SCORECARD.md`; `grep -cF '<LANE_HASH>' SCORECARD.md`; every 40-hex on/after a `Final lane commit:` line → `git cat-file -e` + `merge-base --is-ancestor <h> A` | `0`; `0`; five hashes (`274fa9ae`, `7963976e`, `9f984881`, `c1c6a5f8`, `e666d902`) all exist and are ancestors | yes |
| E2 | `grep -cF 'round-34 depth:density row' SCORECARD.md`; `grep -cF '201.2' SCORECARD.md` | `1`; `7` | yes |
| E3 | rows in `## …Gates & probes registry…` sections whose first cell is the exact basename | `r35-defect-closure.sh` `1`, `r36-closure.sh` `1` (B: `0`/`0`) | yes |
| E4 | `git ls-tree -r --name-only A -- .ufo/waves/round-35/wave1-results.json \| wc -l`; provenance note present | `1`; `1` | yes |
| E5 | `ls .ufo/waves/round-35/claims-erratum-d5.md` | present | yes |
| E6 | `grep -rlF 'Correction (round 35)' .ufo/waves/round-34` | `.ufo/waves/round-34/wave1/L1Integration.md` | yes |
| E7 | QUALITY table rows whose 3rd column begins `supersedes R22` / `supersedes R23` | `1` / `1` | yes |
| E8 | `grep -cF M36 corpus/lessons/round-36.md`; `grep -cF source-recheck` (same); `grep -cF 'source-recheck exit 0 on committed bytes' corpus/lessons/round-35.md` | `4`; `3`; `0` (file present) | yes |
| E9 | live limbs now: `git rev-parse HEAD`; `git status --porcelain \| wc -l`; `find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d \| wc -l` | HEAD `c20300df…` = branch tip; `0`; `0` (root present) | yes at `c20300df` |

E9 is live by design: an export of A now reads `head-match=0` because the branch moved to `c20300df`.
`git diff --name-only A c20300df | grep -vc '^.ufo/waves/round-36/'` → `0`, so E1–E8's inputs are
byte-identical at `c20300df`, and the lane's erratum statement (`--export-ref c20300df…` → `closed=9/9`)
is consistent with every limb re-derived above.

Committed gate evidence (verified, not executed): `.ufo/waves/round-36/final-gates/all-gates.txt` at A
carries `closed=0/9 exit=1` (r35 base) and `closed=3/9 exit=1` (r35 judged head) — both required reds.
The `--selftest` tally is evidenced by `wave1/RevC1Selftest.md` (`selftest cases=9 failures=0`, exit 0, 9
case lines, mutants 4/4,3/3,5/5,1/1,1/1,1/1,2/2,4/4,4/4, header `suite-sha256=4db1ae70…`) on a fixture head,
and by `SimplC1.md` (same tally). Evidence gap: `all-gates.txt` carries neither the positive
`--export-ref <head>` run nor the selftest summary/case lines (its `== selftest ==` section holds three
`judge=forged-* rejected=1` lines only); the real-head `closed=9/9` and `cases=9 failures=0` exist only as
assertions in the SCORECARD "Round-36 measured closure" line and the report erratum. Because every limb
re-derives closed by plain reads, the claim verifies; the receipt gap is routed (§5 D1).

Reported vs re-derived: report `closed=9/9`, `cases=9 failures=0`, `0/9`, `3/9` — consistent;
`grep -cF 'r35-defect-closure.sh' SKILL.md` B→A `0→1`, `r36-closure.sh` `0→1` — match;
`grep -cF 'filled by the L1' SCORECARD.md` `0→0` — match.

### C2 — coverage (held 7): VERIFIED (re-measured)

| Counter | Reported B→A | Re-measured B→A |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 18→19 | 18→19 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 52→53 | 52→53 |
| `grep -cE '^\|[[:space:]]*S053[[:space:]]*\|' corpus/SOURCES.md` | 0→1 | 0→1 |
| `grep -rlE '^source: S053 ' corpus/knowledge \| wc -l` | 0→1 | 0→1 |
| `ls corpus/knowledge/*.md \| wc -l` | 47→48 | 47→48 |
| S053 row shape (`awk -F'\|' … NF`) | — | `NF=13`; tier `A`, kind `docs`, status `mined`, opened `2026-10-26`, recheck `90d`, used-by `corpus/knowledge/epss-exploit-prediction-scoring.md` (exists) |
| capture `sha256sum`/`wc` | `4ec61c59…`, 244 lines, 8448 B | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`, 244 lines, 8448 B |
| Q1–Q4 `grep -nF` in `S053.txt` | L216/217/217/235, `occurrences=1` | L216 / L217 / L217 / L235, one hit each; Q1 = 25 words |
| uncovered-ground sweep at B: `grep -rliE 'EPSS\|exploit prediction' corpus/knowledge corpus/README.md corpus/SOURCES.md SKILL.md \| wc -l` | 0 | 0 |
| census `scripts/sources-census.sh validate --root … kasegi` | exit 0, W04 S028/S029 | exit 0, W04 S028/S029 only |

Harness/recheck-audit/binding-check outputs are evidence-verified from `final-gates/all-gates.txt`:
`PASS F19 … ids=S053`, `entries=22 pass=22 exit=0`, `S053:sha256 OK` + Q1–Q4 `OK occurrences=1`,
`expected=48 missing=0 unexpected=0 exit=0`, `records=43 bound=43 unbound=0`.

### Owned-axis harm check

`git diff --numstat B A`: `SKILL.md 7/0`, `PROVINCE.md 3/0`, `corpus/QUALITY.md 14/0`, `corpus/SOURCES.md 5/0`,
`corpus/README.md 2/0`, `LOG.md 16/0`, `SCORECARD.md 90/0` — append-only, zero deletions. `SCORECARD.md`
diff adds only the `## Round 36` section; no axis score row changes (C1 held 4, C2 held 7, depth:density 9
"no move claimed"). The `SKILL.md` append is one registry section (two rows) after `:1106`, so every
density-bearing base line is byte-identical; density not re-run (lane instrument), no harm by construction.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | suite absent at B → nine routed/closure-order defects re-derived closed at A; required reds committed; score held at 4 by the lane |
| coverage | improved | frontier 18→19, registry 52→53 (tier A, mined), knowledge 47→48 on EPSS ground absent at B; score held at 7 |
| depth:density | unchanged | append-only `SKILL.md`/`PROVINCE.md`; no claim |

## 3. Discernment spot-check (`corpus/lessons/round-36.md` `## Gate`, at A)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| F19 / S053 FIRST EPSS page | admit | `curl -sSL https://www.first.org/epss/` (2026-10-26) → `status=200 bytes=26804`, no redirect; tag-stripped text contains the Q1 span, Q2, Q3, and both Q4 sentences once each | agree | live page reproduces the 26804-byte served size the manifest records and every pinned quote; tier A is right for FIRST's statements about its own model; the entry scopes the claim to FIRST's self-description |
| `c2-controls/junk-f19.md` | reject | `grep -cF 'EPSS guarantees exploitation within 30 days for every scored CVE.' S053.txt` → `0`; `grep -cF guarantee` on the live HTML → `0`; the twin's "scores CVSS severity rather than exploitation likelihood" → `0` | agree | the fabricated sentences exist in neither the capture nor the live page |
| Quarantine row S048 (`https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3`, full URL from the read-only register `absent-defect-register.md:322`) | reject (unreachable, 0 adopted) | `curl -sS` → `status=404 bytes=748`, body `404 - 未找到`, sha256 prefix `95cd25d80d88cce1` | agree | byte-identical to the `ScoutQuarantine.md:45` receipt (748 B, `95cd25d8…`); no quote can be checked, so non-adoption is correct |

New `SOURCES.md` row re-opened: S053 (above). Its `## Gate` quote is ≤25 words (Q1 = 25 by `wc -w`), located
(`S053.txt` L216), and present live.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` →
`W04 S028`, `W04 S029` (standing duplicate-URL warnings), `ok`, exit 0.

## 4. Trend verdicts

- **expansion: improved** — one admitted entry (`epss-exploit-prediction-scoring.md`) on ground B did not
  hold (sweep 0 at B), citing mined tier-A `S053`; F18→F19.
- **quality: improved** — the round-35 verifier's routed defects close by plain re-derivation (E1–E8 at A,
  E9 live); the false round-35 lesson line is gone (`0`) with M36-2 recording it; S053 re-opens live with
  identical served size and quotes; no admitted entry failed a re-check here. Offsetting defects (D1, D2)
  are evidence/record defects, not a false or stale knowledge entry left unmarked.
- **discernment: improved** — the non-author spot-check agrees with the gate on the admit and on both
  rejects sampled.

## 5. Routed defects (kasegi owes these next round)

- **D1 — C1 positive-limb receipt missing.** `.ufo/waves/round-36/final-gates/all-gates.txt` carries the two
  red controls but not the `--export-ref <head>` run or the `--selftest` summary and case lines; commit the
  raw transcript (header with `suite-sha256=`, nine `E<n> payload=` lines, `closed=9/9 exit=0`; nine
  `selftest case=` lines + `cases=9 failures=0`) for the head it names.
- **D2 — false path in append-only LOG.** `LOG.md` round-36 C1 bullet says `corpus/instruments/r36-fixtures/`
  landed; `git ls-tree -r --name-only c20300df | grep -c r36-fixtures` → `0` (also absent at A). Append a
  named correction entry.
- **D3 — closure-order recurrence (M36-1/M36-4 class).** Lane commit `c20300df` (13:41:37) and report erratum
  `1c43fd8f` (13:41:38) landed after `complete kasegi round=36` (13:02:47); the report was filed with WAVE-DONE
  pending. The erratum form is correct; the order is the class this round's C1 targeted.
- **D4 — "final lane commit" label.** `corpus/lessons/round-36.md:3` and `SCORECARD.md`'s
  `Final lane commit: e666d902…` name an intermediate ancestor, not the round's final head (`a23dc478`, then
  `c20300df`). Label it as the anchor ancestor.
- **D5 — registry row completeness.** `SKILL.md` row `r36-closure.sh`: type cell `gate\|probe` is not a choice
  (`grep -cF 'gate\|probe' SKILL.md` → `6` lines), and the verdict map omits exit `2` (plain-run refusal / harness error) →
  `could-not-evaluate`.
- **D6 — E9 limb (b) fail-open.** `r36-closure.sh:465-466` maps a failing `git status` read to `0` dirty lines
  (`2>/dev/null`, `${porcelain:-0}`); make the limb fail closed.

Promotion note for the operator: SHONEN box 2 (end-to-end domain task) remains `[~]` with "none new", so the
checklist is not fully checkable by a non-author this round.
