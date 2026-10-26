# ExecGradedSelftestFixture — G2' graded case-line fixtures

Seat: ExecGradedSelftestFixture (leaf). Round 39, wave 1. Axes owned by this
seat's work: depth:verifiability. Item: build the G2' graded-case-line fixtures
for the round-39 G2 check (synthetic all-gates v3 receipt + case-line variants
(a)-(e), each with its expected `G2 payload=... closed=` line) and the mutant
list the suite author embeds for G2.

Frozen inputs read first: `.ufo/waves/round-39/claims.json` (C1 predicate line
24: G2 requires "exactly eight graded `selftest case=G<n> ... positive=pass ...
verdict=pass` lines plus `selftest cases=8 failures=0`, and no summary-only line
satisfies a case"); `corpus/lessons/round-38-verifier-spotcheck.md` (R1-R4);
`corpus/instruments/r38-closure.sh` (`check_g2`, `judge_selftest_report`).
Deliverable landed before this receipt.

## Deliverable

`ExecGradedSelftestFixture.fixtures/` (30 files, beside this receipt). Item-named
directory; every receipt inside it is byte-exact synthetic text.

| File | Lines | sha256 |
|---|---|---|
| `README.md` | 69 | `627b880ae1233511b0d691ad8e3f5a2c4daef71eb29cfbd5e2cb5924556f9b6b` |
| `judge-g2-cases.sh` | 84 | `73aa11f2e2e5554ed58d2ad8d4a2d201a02511aa690c6d26da592e09e6d245a9` |
| `run-fixtures.sh` | 32 | `33439f3e7a96141ba5e191bce6a653b46fd1e28cd95451f9a4856231f27ee96e` |
| `generate.py` | 274 | `2551b84fd46c1c9acad529f213c19e091fd2842f20cf20796c474b5fe79e7aee` |
| `expected.tsv` | 27 | `60d3b200c48ae07eb9943cd2423ebd61515e18252750cbc94c7805a12b57ec41` |
| `mutants.txt` | 28 | `766e3c7063d7ee379541c19c4064728a8782476da49328c9bae60c2b3820e02e` |
| `receipt-green.txt` (a) | 44 | `96f52210602e44424afbf40d46b280a5fb97343d36bb37619bac65ba42ea0d22` |
| `b-summary-only.txt` | 15 | `577181f80ae43059143e175ab7ec05f92ef6153b9581aa5bf4ef1c36bbbbf123` |
| `c-verdict-fail.txt` | 44 | `b0d9d510f7b13a8a8b8a91472ca4b217f63038b695189969e3058ee9416256df` |
| `d-missing-verdict.txt` | 44 | `72a87d0066da99e1421daa0f2d2aead756cc50e8f1722b135f129d15b03ffadc` |
| `e-seven-cases.txt` | 41 | `f7bf98eac6963059fcf96511a7b296d7ff15daedbaf9ed5e3290ea647657095c` |
| `m01-duplicate-id.txt` | 44 | `ba7c1a21f43f14bd030f22f48ec3b8fa5a7bc1545c9f0f66ff9c7dfc9eb523a3` |
| `m02-detail-free-0-0.txt` | 23 | `f0b1f408f73813986bd4a62737ae03423dd8cf94e6cf2a17db3082e089c88747` |
| `m03-details-removed.txt` | 23 | `937ddbcb24591ca30766fc9795d2a5a4d16f8ce6d5d7f9b01a2dd5ceee853c32` |
| `m04-detail-rejected-0.txt` | 44 | `f98f215d71dec1a102ac909592b97f952b61db00f3a06f681e4e78be4185df62` |
| `m05-detail-rejected-10.txt` | 44 | `d4fbca3cbd395ad3124aa4032cfd0e0d7f44d436748c1ef3c2afa4ee9e0c6fe7` |
| `m06-ninth-case-g9.txt` | 47 | `d6ee092d0b5b4e61c8489997e3256b94087b4b7715004fac844b643b0c9f89ab` |
| `m07-trailing-field.txt` | 44 | `baddab8eea7e6de0a2b3cd56c911b1e57ba170e5e9ebcefce21d7a066df76d75` |
| `m08-case-missing-mutants.txt` | 44 | `d7359d23dc6efedf18f9ae5475b5a6877a3430410e9628c230764fa1da6e85f5` |
| `m09-case-missing-positive.txt` | 44 | `39090ff1e5651e87b7b8f14d2805a50469110859aacb68a3f0b3b95f63b39be4` |
| `m10-summary-failures-1.txt` | 44 | `9c7d1f0b0a8df219f8d3cb5106a1cd75520e896e2bf38d8bca61978d8f893f69` |
| `m11-summary-duplicated.txt` | 45 | `7a42b6a94291ea5b9dc21d145f99799c9925dd97dc4c124a08f5c7619a700e33` |
| `m12-sentinel-v2.txt` | 44 | `809716697e21a39304ca6d93283094d2be970fc9fec412c75e4729362cc0b6a4` |
| `m13-closed-7of8.txt` | 44 | `2a95e161191ee1fd453118026aee5b8b8bc9af919b0d6a98e0e30cc29b988e1e` |
| `m14-run-line-closed-0.txt` | 44 | `f444d4b14bb4327e3b17a37f99664587249a869e0eda05d44681746b990b34be` |
| `m15-run-line-missing.txt` | 43 | `1baa78578866589f649895f9f2a0cc305e888adb834a6bde9987a5b9b429e8bc` |
| `m16-seven-cases-truthful-summary.txt` | 41 | `280d1101905ebde30bf786e44a838dc64a1e13924ca3254276fa13d9c4131688` |
| `m17-positive-fail.txt` | 44 | `d28230fa518611da36aab616a1d778777dc2ecc8485d3abfd5efbaef40036b1e` |
| `m18-bare-summary-only.txt` | 13 | `3e79ceb4530525e1d2144f6fa89d54a33cc64fefdb90a6b356b1c97b3a84ed5c` |
| `m19-eight-summary-lines.txt` | 21 | `aa48eb327ab15447a99eedf0eaacda1c5d46793ea44cb9babff8cded656f64de` |

24 of the 30 files are fixtures (1 positive control + 4 named variants + 19
mutants); the other 6 are the README contract, the judge, the driver, the
generator, the expectation table and the mutant list. No file outside the
deliverable directory and this receipt was written.

### Expected lines, per named variant (from `expected.tsv`, measured)

```
receipt-green.txt (a)   G2 payload=receipt=1,sentinel=1,run-lines=1,closed-line=1,cases=8,graded=8,detail-ok=1,summary=1,summary-only=0 closed=1   exit 0
b-summary-only.txt (b)  G2 payload=receipt=1,sentinel=1,run-lines=1,closed-line=1,cases=0,graded=0,detail-ok=0,summary=1,summary-only=1 closed=0   exit 1
c-verdict-fail.txt (c)  G2 payload=receipt=1,sentinel=1,run-lines=1,closed-line=1,cases=8,graded=7,detail-ok=1,summary=1,summary-only=0 closed=0   exit 1
d-missing-verdict.txt (d) G2 payload=receipt=1,sentinel=1,run-lines=1,closed-line=1,cases=8,graded=7,detail-ok=1,summary=1,summary-only=0 closed=0   exit 1
e-seven-cases.txt (e)   G2 payload=receipt=1,sentinel=1,run-lines=1,closed-line=1,cases=7,graded=7,detail-ok=1,summary=1,summary-only=0 closed=0   exit 1
```

## The rule the fixtures encode

`judge-g2-cases.sh RECEIPT` prints one line and exits 0 iff it ends `closed=1`.
Fields, in this order: `receipt`, `sentinel` (line 1 is exactly `all-gates v3`),
`run-lines` (eight distinct `G<n> payload=... closed=1`), `closed-line` (exactly
one `closed=8/8 exit=0`), `cases` (count of `^selftest case=G<digits> `),
`graded` (ids G1..G8 with exactly one case line matching the whole-line regex
`^selftest case=G<n> positive=pass mutants=<a>/<b> verdict=pass$`), `detail-ok`
(at least one graded id and every graded id has `b>=1`, `a==b`, exactly `b`
`selftest detail=G<n> mutant=` lines, exactly `a` of them ending `rejected=1`),
`summary` (count of `selftest cases=8 failures=0`), `summary-only` (selftest
lines present but zero case lines), `closed` (all of the above).

The high-value consequence for the suite author: the green receipt's own
`G2 payload=...` line literally contains `cases=8,graded=8,detail-ok=1,
summary=1,summary-only=0`. Every fixture keeps it, so a check that counts
unanchored tokens reads a pass out of the receipt's own claim about itself. The
fixtures kill that (see the weak-judge table below).

## Evidence (commands actually run, actual output)

### 1. Full fixture run, over the installed deliverable

`cd .../wave1/ExecGradedSelftestFixture.fixtures && ./run-fixtures.sh` — exit 0:

```
fixture=receipt-green.txt expected-rc=0 observed-rc=0 verdict=pass
fixture=b-summary-only.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=c-verdict-fail.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=d-missing-verdict.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=e-seven-cases.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m01-duplicate-id.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m02-detail-free-0-0.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m03-details-removed.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m04-detail-rejected-0.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m05-detail-rejected-10.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m06-ninth-case-g9.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m07-trailing-field.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m08-case-missing-mutants.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m09-case-missing-positive.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m10-summary-failures-1.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m11-summary-duplicated.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m12-sentinel-v2.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m13-closed-7of8.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m14-run-line-closed-0.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m15-run-line-missing.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m16-seven-cases-truthful-summary.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m17-positive-fail.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m18-bare-summary-only.txt expected-rc=1 observed-rc=1 verdict=pass
fixture=m19-eight-summary-lines.txt expected-rc=1 observed-rc=1 verdict=pass
fixtures=24 pass=24 failures=0
```

Spot checks of the two required behaviours, verbatim:

```
$ bash judge-g2-cases.sh receipt-green.txt
G2 payload=receipt=1,sentinel=1,run-lines=1,closed-line=1,cases=8,graded=8,detail-ok=1,summary=1,summary-only=0 closed=1
rc=0
$ bash judge-g2-cases.sh b-summary-only.txt
G2 payload=receipt=1,sentinel=1,run-lines=1,closed-line=1,cases=0,graded=0,detail-ok=0,summary=1,summary-only=1 closed=0
rc=1
```

### 2. The fixtures discriminate against weaker judges

Three deliberately weak judges were dropped in as `judge-g2-cases.sh` and run
over the same 24 fixtures (acceptance = judge exit 0). Intended acceptance set
is exactly `{receipt-green.txt}`.

| judge | accepted / 24 | false accepts (must be rejected, accepted instead) |
|---|---|---|
| this judge | 1 | none |
| shape-only, r38 `check_g2` class (8 `^selftest case=G[1-8] ` ids + summary) | 16 | c, d, m02-m09, m12-m15, m17 (15) |
| r38 `judge_selftest_report` class (case count + `verdict=pass$` count + summary) | 12 | m01-m05, m08, m09, m12-m15 (11) |
| unanchored token counter | 18 | c, d, m01-m09, m11-m15, m17 (17) |

Verbatim from the sweep (`for f in ...; do bash $judge "$f" >/dev/null 2>&1 && acc="$acc $b"; done`):

```
deliv          fixtures=24 accepted=1 [ receipt-green.txt ]
wk-shape       fixtures=24 accepted=16 [ c-verdict-fail.txt d-missing-verdict.txt m02-detail-free-0-0.txt m03-details-removed.txt m04-detail-rejected-0.txt m05-detail-rejected-10.txt m06-ninth-case-g9.txt m07-trailing-field.txt m08-case-missing-mutants.txt m09-case-missing-positive.txt m12-sentinel-v2.txt m13-closed-7of8.txt m14-run-line-closed-0.txt m15-run-line-missing.txt m17-positive-fail.txt receipt-green.txt ]
wk-r38         fixtures=24 accepted=12 [ m01-duplicate-id.txt m02-detail-free-0-0.txt m03-details-removed.txt m04-detail-rejected-0.txt m05-detail-rejected-10.txt m08-case-missing-mutants.txt m09-case-missing-positive.txt m12-sentinel-v2.txt m13-closed-7of8.txt m14-run-line-closed-0.txt m15-run-line-missing.txt receipt-green.txt ]
wk-unanchored  fixtures=24 accepted=18 [ c-verdict-fail.txt d-missing-verdict.txt m01-duplicate-id.txt m02-detail-free-0-0.txt m03-details-removed.txt m04-detail-rejected-0.txt m05-detail-rejected-10.txt m06-ninth-case-g9.txt m07-trailing-field.txt m08-case-missing-mutants.txt m09-case-missing-positive.txt m11-summary-duplicated.txt m12-sentinel-v2.txt m13-closed-7of8.txt m14-run-line-closed-0.txt m15-run-line-missing.txt m17-positive-fail.txt receipt-green.txt ]
```

This is the round-38 attack surface (R5: shape-only case counting; the receipt's
own payload line as a second source of truth) reproduced as failing controls.

### 3. Mutations are minimal and intentional (`diff receipt-green.txt <fixture>`)

```
b-summary-only.txt                   +0 -29   all case+detail lines removed
c-verdict-fail.txt                   +1 -1    G4 verdict=pass -> verdict=fail
d-missing-verdict.txt                +1 -1    G6 loses " verdict=pass"
e-seven-cases.txt                    +0 -3    G8 case+2 details removed, summary still cases=8
m01-duplicate-id.txt                 +1 -1    G3 line duplicated, G7 line removed
m02-detail-free-0-0.txt              +8 -29   details removed, every case line mutants=0/0
m03-details-removed.txt              +0 -21   case lines claim 2/2, no detail lines
m04-detail-rejected-0.txt            +1 -1    one G2 detail rejected=0
m05-detail-rejected-10.txt           +1 -1    one G5 detail rejected=10
m06-ninth-case-g9.txt                +3 -0    G9 detail pair + case line
m07-trailing-field.txt               +1 -1    " note=ok" after verdict=pass
m08-case-missing-mutants.txt         +1 -1    G3 loses mutants=
m09-case-missing-positive.txt        +1 -1    G5 loses positive=pass
m10-summary-failures-1.txt           +1 -1    summary failures=1
m11-summary-duplicated.txt           +1 -0    second summary line
m12-sentinel-v2.txt                  +1 -1    line 1 all-gates v2
m13-closed-7of8.txt                  +1 -1    closed=7/8 exit=1
m14-run-line-closed-0.txt            +1 -1    G5 run line closed=0
m15-run-line-missing.txt             +0 -1    G8 run line removed
m16-seven-cases-truthful-summary.txt +1 -4    G8 removed, summary cases=7
m17-positive-fail.txt                +1 -1    G7 positive=fail mutants=0/1 verdict=fail
m18-bare-summary-only.txt            +0 -31   selftest region is one bare summary line
m19-eight-summary-lines.txt          +7 -30   eight summary lines, zero case lines
```

### 4. Regeneration is byte-identical

`python3 generate.py <fresh-dir>` → `fixtures=24 out=<fresh-dir>`, then
`cmp` of every generated file against the delivered copy: 25 files (24 receipts
+ `mutants.txt`) identical, 0 differing. `mutants.txt` names exactly the 24
receipts (`diff` of the two sorted file lists: empty).

### 5. Guard and hygiene

- Disk guard before work: `/tmp` 3% (125.2G free), `/var/tmp` 35%, `/fast/scratch/hyaku` 24% (610.7G free) — green.
- Scratch `S=/fast/scratch/hyaku/kasegi-r39/ExecGradedSelftestFixture/` created with `mkdir -p`, all work bound there (no inherited `TMPDIR` used, no `--work` dir needed: no git fixture, no clone, no lane run).
- No mutating git command, no pacman, no tool install or upgrade (nothing was needed). No write to any PATH dir, fleet-root tracked file, `.ufo/state/`, `.ufo/watchdog.log`, `MANIFEST.json`, `templates/`, `scripts/`, or a sibling repo. Write set = the deliverable directory + this receipt + scratch (removed).
- Not run (leaf: parent owns post-integration gates): `corpus/instruments/r39-closure.sh` does not exist yet; no lane instrument, build, lint or test was executed.

## Embed list the suite author should take

`fixtures/mutants.txt` carries 24 tab-separated rows
`id<TAB>fixture<TAB>expected closed<TAB>mutation`:

- `P-G2-01` positive control, `receipt-green.txt`, `closed=1`.
- `M-G2-01` … `M-G2-23` negative controls, `closed=0`, one row per variant (b)-(e) plus 19 further mutants.

Embed pattern in `r39-closure.sh`:

1. Copy the receipt to `.ufo/waves/round-39/final-gates/all-gates.txt` inside a fresh mutant tree (`mut_reset`), as the other checks do.
2. Positive control: green fixture → `G2 payload=... closed=1` and `st_pos` passes.
3. Each negative: `st_neg G2 <mutation> <tree> ... 'closed=0'` **and** require the expected payload line from `expected.tsv`, so a check that rejects for the wrong reason still fails.
4. Record `mutants=<ok>/<n>` on G2's own case line and one `selftest detail=G2 mutant=<id> rejected=1` per mutant. The green receipt's case lines already show the required shape (`selftest case=G2 positive=pass mutants=2/2 verdict=pass` with two detail lines).

## Risks and open edges (not defects of this deliverable)

- The fixtures are receipts only: header hashes are placeholders (40/64 zeros), so `export-ref` existence/ancestry, the `git diff --name-only <export-ref> REF` scope test and the `suite-sha256` digest binding stay tested by the suite's real run against a real export. Nothing here may be bound to a lane head.
- The payload vocabulary and field order are fixed by this contract; if the suite author chooses different field names, `expected.tsv` must be regenerated with the same `judge-g2-cases.sh` (or the contract updated) so fixtures and check cannot drift apart silently.
- `m16` (truthful `cases=7` summary) and `e` (lying `cases=8` summary) are both covered on purpose: a check that only compares the summary against itself passes `m16`'s summary and must still go red on `cases!=8`.
- `detail-ok` is 0 when nothing is graded (`b`, `m18`); that is a reporting choice, not a second gate — `graded==8` already fails those.
- Adjacent seat overlap: `TabiR34` extracts the round-39 mutant list; this deliverable's mutant ids are G2-scoped (`M-G2-*`) and independent of that list.

## Result

Deliverable complete: 24 fixture receipts (1 GREEN, 23 RED), each with a
measured expected `G2 payload=... closed=` line, a judge implementing the
graded case-line rule, a driver proving `fixtures=24 pass=24 failures=0`, a
regeneration path proving byte-identity, and a 24-row mutant list ready to embed
under G2. Discrimination demonstrated: three weaker judges accept 12-18 of the
24 fixtures; this judge accepts only the green one.
