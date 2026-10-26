# ExecCensusReplay — C2 census before→after mechanics (round 37)

Seat: ExecCensusReplay (leaf, coverage axis). Scope: establish the census before→after mechanics for
C2 by running the fleet census at base and validating the *planned* S054 row inside a faithful
pre-state mirror. Receipt only: no lane, fleet, or sibling-lane writes; no mutating git; no installs.

Verdict:

| measurement | result |
|---|---|
| base census (`validate --root … kasegi`) | exit **0**, W04 S028 + W04 S029 only |
| mirror registry (base + planned S054 row + knowledge entry) | exit **0**, E-codes **0**, W04 S028/S029 only |
| census rows | 53 → **54** |
| tier.A / tier.B / tier.C | 50/1/2 → **51/1/2** |
| status mined / queued / rejected | 41/9/3 → **42/9/3** |
| discriminating controls | E03, E04, E11, E12 each fire when the corresponding defect is injected |

Environment: GNU bash 5.3.20(1), GNU Awk 5.4.1, host
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` sha256
`3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`. Measured 2026-10-26T17:04Z.
All scratch under `/fast/scratch/hyaku/kasegi-r37/ExecCensusReplay/` (removed before yielding).

## 1. Base census (round-37 base state)

Lane corpus is byte-identical to base `b56a41680cefd391868c1c370dc063c69d827e7d` at measurement time,
so running against the live lane tree *is* the base measurement:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git diff --stat b56a41680cefd391868c1c370dc063c69d827e7d..HEAD -- corpus/     # (empty)
$ git status --porcelain corpus/ | wc -l
0
$ sha256sum corpus/SOURCES.md
2ff7818ad2179c1f8ecf89262e3f8a84a585dfb4f64bbc1fa0e7dbc3be2465fe  corpus/SOURCES.md
# same digest as: git show b56a41680cefd391868c1c370dc063c69d827e7d:corpus/SOURCES.md
```

Transcript (stdout + exit):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
$ echo $?
0
```

stderr empty. This reproduces the recorded `c2-controls/before.txt` / `census-before.txt` lines exactly
(exit 0; W04 S028, W04 S029; no E-codes). Registry rows at this state: **53**
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 53).

## 2. Mirror construction (pre-state + planned S054)

```
$ mkdir -p mirror/corpus
$ git -C <lane> show b56a4168…:corpus/SOURCES.md > mirror/corpus/SOURCES.md
$ cp -a <lane>/corpus/knowledge mirror/corpus/knowledge        # 48 files
$ printf 'source: S054\n' > mirror/corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
$ ls mirror/corpus/knowledge/*.md | wc -l
49
```

The row was inserted **as line 60**, i.e. at the end of the `## Registry` table, immediately after the
`S053` row (line 59) and before the blank line that precedes `## Paths` (which sits at line 61 of the
base file, line 62 after the insert).
Row bytes (`mirror/corpus/SOURCES.md` sha256
`4c0e7bc0781e5229dbe548053265adfa61caf3dac3aaaddad12c22e403ef2850`, 118 lines, 54 registry rows;
row bytes sha256 `9ca6c2f842438fb1969f83329da4deaf1e9f68c47de4acefb726e06676607a1d`):

```
| S054 | SSVC - Stakeholder-Specific Vulnerability Categorization (CERT/CC, Carnegie Mellon University) — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ | docs | A | CERT/CC's own SSVC overview: stakeholder-tailored vulnerability prioritization and the decision-point vocabulary it defines | capture corpus/source-snapshots/round-37/S054.txt: the "What is SSVC?" definition sentence, the stakeholder-tailored prioritization sentences, and the decision-point passages (Exploitation, Exposure, Automatability, Human Impact) | SSVC prioritizes vulnerability response by stakeholder-specific decision points and outcomes rather than a single technical severity score, so its outcome is a stakeholder-tailored priority distinct from CVSS severity, KEV listing and EPSS likelihood | mined | 2026-10-26 | 180d | corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md |
```

Cell shape verified: `NF=13` with 11 cells —
`S054 | docs | A | scope | anchor | teaches | mined | 2026-10-26 | 180d | knowledge path`.
URL literal is the erratum-1 corrected one (`…/tutorials/ssvc_overview/`, not the docs home page), and
it collides with no existing row (S004 is `certcc.github.io/certcc_disclosure_policy/`).

## 3. Mirror validate — the after state

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file /fast/scratch/hyaku/kasegi-r37/ExecCensusReplay/mirror/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r37/ExecCensusReplay/mirror/corpus/SOURCES.md
$ echo $?
0
$ grep -cP '\tE[0-9]{2}\t' mirror-validate.out
0
```

stderr empty. **No E-code of any kind** — in particular none of E03 (duplicate id) / E04 (duplicate
URL+scope), the two codes that would have made the freeze unsatisfiable.

## 4. Census-mode arithmetic (before → after)

```
$ bash …/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi      # exit 0
kasegi	rows	53          |  tier.A 50  tier.B 1  tier.C 2  |  mined 41  queued 9  rejected 3
$ bash …/sources-census.sh census --file <mirror>/corpus/SOURCES.md                # exit 0
file	rows	54          |  tier.A 51  tier.B 1  tier.C 2  |  mined 42  queued 9  rejected 3
FLEET	rows 54  tier.A 51  tier.B 1  tier.C 2  tier.invalid 0  queued 9  mined 42  rejected 3  status.invalid 0  missing 0
```

The single S054 row moves exactly `rows +1`, `tier.A +1`, `status.mined +1`; every other bucket is
unchanged, which is the arithmetic C2's "registry 53→54, tier A, mined" claim needs.

## 5. Discriminating controls (each a separate mirror copy)

| control | delta from §3 mirror | result |
|---|---|---|
| `ctl-norow` | S054 row **and** its entry removed (pure base re-validate through `--file`) | exit **0**, W04 S028/S029 only, 53 rows |
| `ctl-shallow` | row kept, `corpus/knowledge/` **not** mirrored | exit **1**, **47 × E11** (one per mined used-by cell, S001…S054) |
| `ctl-noentry` | row kept, only `ssvc-…categorization.md` removed | exit **1**, exactly `E11 S054 missing used-by corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` |
| `ctl-dup-id` | second, identical `S054` row appended | exit **1**, `E03 S054 duplicate id` **and** `E04 S054 duplicate url certcc.github.io/SSVC/tutorials/ssvc_overview within scope …` |
| `ctl-dup-url` | same row re-ided as `S055` (same URL + scope cell) | exit **1**, `E04 S055 duplicate url certcc.github.io/SSVC/tutorials/ssvc_overview within scope …` (no E03) |
| `ctl-eof` | same row appended at **end of file** instead of inside `## Registry` | exit **1**, `E12 S054 row outside Registry section` |

`ctl-shallow` is why a SOURCES.md-only mirror cannot be used: E11 resolves each used-by path against
`dirname(<registry file>)/..`, i.e. the mirror root, not the fleet root. `ctl-noentry` and `ctl-eof`
show the green in §3 is not vacuous — it depends on the knowledge entry existing and on the row living
inside the Registry table.

The census script's own fixture suite agrees (`bash …/sources-census.sh selftest` → `selftest ok`,
exit **0**, fixtures `killed E03-duplicate-id`, `killed E04-duplicate-url`,
`killed W04-does-not-fail-validation`, `killed E04-rejected-pair-exemption-mutant`).

## 6. Mechanics findings for integration (L1)

1. **Row + entry must land together.** The registry row alone is red: `ctl-noentry` → `exit 1`,
   `E11 S054`. Land `corpus/SOURCES.md` and
   `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (with header
   `source: S054`) in the same integration commit, then run the lane census.
2. **Placement is load-bearing.** The row must go at the end of the `## Registry` table (after S053,
   before the blank line that precedes `## Paths`). An end-of-file append is `E12` and exit 1.
3. **URL literal.** Use the erratum-1 value `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`
   in the row, the manifest record and it must equal the capture record's `url` (B5 binding); the
   frozen-claims predicate text still shows the home page — the erratum is the operative literal.
4. **W04 is warning-only.** S028/S029 pre-exist and do not change status (`W04-does-not-fail-validation`
   killed in selftest); the after-state "census exit 0 (W04 S028/S029 only)" is therefore satisfiable
   and was reproduced here.
5. **Expected after-state census lines** (what the integration should print):
   `rows 54 · tier.A 51 · tier.B 1 · tier.C 2 · mined 42 · queued 9 · rejected 3`,
   `validate` → the two W04 lines plus `ok`, exit 0.
6. **A lone SOURCES.md mirror is not a valid census target.** If any later seat mirrors only the
   registry, it will see ~47 E11 and may misread that as a defect; mirror `corpus/knowledge/` too, or
   point `--file` at the real lane file.

## 7. Risks and limits

- The S054 row bytes above are **my reconstruction** from the frozen C2 claim plus claims-erratum-1
  and the registry's own conventions (11 cells; `<name> — <url>` source cell; tier A; `mined`;
  `opened 2026-10-26`; cadence `180d`; used-by = the F20 entry path). Its `anchor` cell deliberately
  carries **no** invented `S054.txt` line numbers — those belong to the capture seat. No census
  E-check inspects anchor/capture prose, so the §3 green does not depend on the anchor wording; but
  the capture-binding / source-recheck instruments do, so the landed row's anchor must be reconciled
  with the real `corpus/source-snapshots/round-37/S054.txt` line numbers before the C2 gate.
- Census `validate` does not check that the anchor's cited capture path exists; a green census is
  necessary, not sufficient, for the capture binding (owned by the S054 capture/source-recheck seats).
- Scope of this measurement: census mechanics only (E03/E04 freedom, row arithmetic, exit codes).
  Knowledge-entry content (Q1–Q6), harness `entries=23 pass=23`, and `recheck-audit` sync are other
  seats' evidence and were not re-measured here.

## 8. Files changed

- This receipt only: `.ufo/waves/round-37/wave1/ExecCensusReplay.md`.
- No lane file, fleet file, or sibling tree was written; no git mutating command was run; no tool
  installed. Scratch `/fast/scratch/hyaku/kasegi-r37/ExecCensusReplay/` removed after copying these
  results here.
