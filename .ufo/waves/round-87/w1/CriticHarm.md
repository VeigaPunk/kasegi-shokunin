# CriticHarm — round 87, attempt 1, wave `kasegi-r87-w1` (ONE v1 wave, 12 seats)

Seat: attack (harm check of the landing commits on every axis and gate). Leaf; no delegation, no
lane edits. Scope owner of nothing; this file routes findings only.

Round shape: 2 frozen claims (C1 `depth:verifiability` knowledge-scope tranche 2, C2 `coverage`
capability `capture-secret-scan`), base `cd1f568a6be2656b5f5dc479eb90ef99b91131b5`, freeze
`afb13a88e6fbc8e2f8a0c11f9cfbfde77e907e69`, C1 landing `d87b1b55a51d78411438e962a9abbebdd17930cd`,
C2 landing `132e16c588a2424c06b5ca15ea01fce1ee9a396d` (`.ufo/waves/round-87/landing.json`).

## Verdict (headline)

**HARM: 1 — and it is a claim-fatal gate record, not a measurement regression.** The C1 landing
commit carries three out-of-scope files, so frozen C1 predicate **P3 is FALSE** at `d87b1b55`; by the
frozen kill rule C1 is **NOT VERIFIED** as frozen. Every *measured* axis/gate reading I could take is
**NO-HARM**: byte-identical at base and landing, or strictly improved (provenance now resolves).

No other verdict anywhere flips for the worse between base and the landings.

## Method (all absolute paths; scratch `/fast/scratch/hyaku/kasegi-r87/CriticHarm`)

Three `git clone --shared` checkouts under scratch (`base`, `c1`, `c2`) plus a fourth at `252df0c9`
for the C2 r86-freeze limb; `git -C <clone> rev-parse --show-toplevel` asserted each; `TMPDIR` passed
explicitly; `python3 -B` everywhere. The knowledge-meter ran on the clone (census-of-record root), not
at the lane path, per the lane's +1 warning (r86 CriticRoot). No `resolve.py` lane census was run
(contract ban); no lane write, no git write in the lane, no `pacman`.

## Per-gate table: base vs landings

`L1` = C1 landing `d87b1b55`, `L2` = C2 landing `132e16c5`. Commands are run with cwd = the clone root.

| # | gate / reading | command | base `cd1f568a` | L1 | L2 | change |
|---|---|---|---|---|---|---|
| 1 | depth:density | `python3 -B corpus/instruments/density.py SKILL.md --label x` | rc 0, mean dens **273.2**, 932 cites / 38 blocks | identical | identical | **none** (`diff` empty; SKILL.md untouched by both landings) |
| 2 | claim-package `curl-h1-1913733` | `python3 -B corpus/instruments/claim-package-check.py corpus/practice/curl-h1-1913733` | 8/8 `WELL-FORMED exit=0` | identical | identical | **none** |
| 3 | claim-package `curl-ibb-h1-1997312` | `... corpus/practice/curl-ibb-h1-1997312` | 8/8 `WELL-FORMED exit=0` | identical | identical | **none** |
| 4 | claim-package selftest | `python3 -B corpus/instruments/claim-package-selftest.py` | `cases=10 failures=0` rc 0 | identical | identical | **none** |
| 5 | source-recheck r87 manifest | `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-87/manifest.json` | rc 2 `manifest UNAVAILABLE reason=missing` | rc 0 (all S124/S125 records OK, anchors 85/303/331/332/409) | rc 0 | **expected**: the manifest is added by the freeze commit; no pre-existing reading is lost |
| 6 | source-recheck selftest | `python3 -B corpus/instruments/source-recheck.py --selftest` | `cases=10 failures=0` rc 0 | identical | identical | **none** |
| 7 | capture-source selftest | `python3 -B corpus/instruments/capture-source.py --selftest` | `normalize=ok deterministic=ok` rc 0 | identical | identical | **none** |
| 8 | sources census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md` | rc 0, `file ok`, 4 pre-existing `W04 duplicate url` warnings | — | identical except the file-path token | **none** |
| 9 | knowledge meter | `python3 -B .ufo/waves/round-87/c1/knowledge-meter.py --lane <clone> --measure-rev <rev> --work <scratch>` | **596/1720** = 34.65 % | **678/1719** = 39.44 % | **678/1719** | **+82 citations / −1 distinct** (target hit exactly) |
| 10 | C1 counter (frozen) | `python3 -B .ufo/waves/round-87/c1/knowledge-meter.py --lane <c1 clone> --base-rev cd1f568a… --map .ufo/waves/round-87/c1/repair-map.json --target 678/1719 --map-sha256 7db928c7… --work <scratch>` | n/a (no map at base) | `KNOWLEDGE-METER-RESULT pass rc=0`, M1–M7 pass | same (files unchanged) | P1 true |
| 11 | anchorcheck, 5 changed knowledge files | `python3 -B corpus/instruments/anchorcheck.py corpus/knowledge/<f>.md` | **4 of 5 rc 1**: `BASE-ABSENT` 1 / 1 / 12 / 83 cites | **5 of 5 rc 0**, `BASE-ABSENT=0` | same | **improvement** (the repoint resolves the anchors; content spot-checked below) |
| 12 | citation-ground-check | `python3 -B corpus/instruments/citation-ground-check.py --root .` | rc 1, `verdict=failed`, 2 pre-existing `blocked blocked-protected-lane-bare` | identical | identical | **none** |
| 13 | gate-quote-audit | `python3 -B corpus/instruments/gate-quote-audit.py --root .` | rc 1, `annotated=10 ok=8 erratum-on-record=2 failures=2` | identical | identical | **none** |
| 14 | C2 capability counter | `python3 -B .ufo/waves/round-87/c2/capability-check.py --lane . --rev 132e16c5… --work <scratch> --instrument-sha256 b2bf9d65… --gate-sha256 8b6f8493…` | K1 FAIL (instrument absent), K2–K5 FAIL (executed control) | — | **K1–K5 pass**, `K3 summary=scanned=1319,hits=0,files=0,allowed=18,unused_allow=0` | **capability enters** |
| 15 | scanner selftest | `python3 -B corpus/instruments/capture-secret-scan.py --selftest` | absent | absent | `SELFTEST-RESULT pass cases=19` | new |
| 16 | independent r86 leak scan | `capture-secret-scan.py --lane <252df0c9 clone> --rev 252df0c9 --allow corpus/instruments/capture-secret-allow.tsv` | (r86 freeze `252df0c9`) **files=2 hits=6** | — | — | matches K2's file oracle; the 2 files are exactly those `git grep -l X-Amz-Security-Token` finds |
| 17 | instrument pins (13) | `git show <rev>:<path>` + sha256 vs `claims.json` | base: freeze-added paths ABSENT as expected | **all PIN** | **all PIN** | no post-freeze byte drift |

Executed at L1 and L2 both; receipt copies in `CriticHarm-receipts/` (21 files, all summary/verdict
lines, no matched values — re-scanned with the new instrument: 0 credential-shaped hits).

### C2 predicate P2 (byte equality), verified independently
`sha256sum corpus/instruments/capture-secret-scan.py` = `b2bf9d65…c6d1` and
`corpus/instruments/capture-secret-allow.tsv` = `f9fbd7e7…fc82` at `132e16c5`, equal to
`.ufo/waves/round-87/c2/candidate/*`. K1–K5 pass at the landing; the counter's control battery shows
the limbs are load-bearing (forged always-clean scanner → K2/K4 FAIL; path+shape-only allowlist → K3
FAIL `unused_allow=13`; widened scope → K3 FAIL; empty allowlist → K3 FAIL; wrong pin → K1 FAIL).

## C1 knowledge files render the same sentences apart from the repointed tokens

Independent reverse-apply of `repair-map.json` over the C1 landing files and `diff` against base:
all five **byte-identical after reverse substitution** — 83 distinct map values, **98 replacement
occurrences**, same file set, same line counts (89 / 69 / 36 / 173 / 134). No prose, table cell,
punctuation or wrapping change; only the backticked citation token lengthens.

Map integrity, re-derived (not taken from the counter): 83/83 keys have anchor-equal value, a target
that exists at base, a basename held by **exactly one** tracked file under `corpus/source-snapshots/`,
and an in-range anchor; 5 target files (round-23 S029, round-25 S040, round-44 S069, round-67 S100,
round-68 S102).

`1720 → 1719` is explained, not hidden: `corpus/source-snapshots/round-25/S040.txt` already exists as
a backticked token at base, so that key's repoint merges two distinct tokens into one (−1 distinct
while +83 −83 tokens move, M2 `stray_added=0`).

### Provenance spot-check (does the repointed path carry the quoted text?)
Sampled 13 anchors, all content-correct, so the repoint is not laundering a wrong reference:
`round-68/S102.txt` 9 `"https"`, 11 `"swagger": "2.0"`, 13 description, 14 `"title": "OpenSSF
Scorecard API"`, 19 `/projects/{platform}/{org}/{repo}`, 28 `^[0-9a-fA-F]{40}$`, 30 SHA1-commit
description, 31–32 `commit`/`query`, 139 VCS-platform description; `round-44/S069.txt` 10–11
"…is intended to be in scope", 61–62 "strictly limited to Google-owned infrastructure and services",
70–72 ineligibility sentence; `round-67/S100.txt:462` `Training & Education`; `round-23/S029.txt:20`
"…in any event within 24 hours of the manufacturer becoming aware of it" (and line 10 carries the same
phrase, which is exactly what the knowledge sentence asserts).

## Credential hygiene of the landing (this round's subject)

- No credential-shaped value entered the lane by either landing: `--files` over all **704** `corpus/`
  files at `132e16c5` reports **4 hits in 2 files**, and both are deliberate needles (the scanner's own
  selftest fixtures, and the pre-existing claim-package `defect-9-secret` fixture that the r87 selftest
  depends on). Nothing in `corpus/knowledge/` or the practice packages.
- The r86 leak is remediated under the new instrument: `round-86/S122.txt` at the landing contains no
  `X-Amz-Security-Token=` at all, and the scan of that file alone is `hits=0`.
- The allowlist holds only path+shape+digest+reason rows; no value is stored, and `aws-sts-session-token`
  rows are refused (K4 `sts_allow_rc=2`).
- `--rev` at the landing: `hits=0, unused_allow=0` — no stale row is masking a live capture.

## Routed findings (evidence + re-runnable command)

**DF-87-H1 — HARM, claim-fatal (frozen P3 false).** The C1 landing commit contains three files outside
`corpus/knowledge/`:
```
git diff --name-only afb13a88e6fbc8e2f8a0c11f9cfbfde77e907e69 d87b1b55a51d78411438e962a9abbebdd17930cd
.ufo/waves/round-87/w1-dispatch.json
.ufo/waves/round-87/w1-spec.json
.ufo/waves/round-87/w1/swarm-registry.json
corpus/knowledge/cra-manufacturer-reporting-duties.md
corpus/knowledge/first-psirt-maturity-document.md
corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
corpus/knowledge/openssf-scorecard-api-contract.md
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```
P1 (counter) and P2 (pins) are true, so the only failure is the commit's file set. Consequence under
the frozen kill rule: **C1 NOT VERIFIED**. Nothing here is re-scored by this seat, the map/counter are
not changed, and the correction is a round-88 mechanism (a landing commit must be built from an
explicit scope path list, or the landing must be re-made on a clean base). Already recorded in
`landing.json` and the in-flight SCORECARD section; restated here as the executing command so the next
seat does not have to re-derive it.

**DF-87-H2 — candidate defect, lane rule R29 (unregistered instrument).**
```
git show 132e16c588a2424c06b5ca15ea01fce1ee9a396d:SKILL.md | grep -c '^| capture-secret-scan.py '
```
prints **0**: `corpus/instruments/capture-secret-scan.py` has no row in `SKILL.md` § Gates & probes
registry, while its closest analogue `claim-package-check.py` has one (and `source-recheck.py`,
`recheck-audit.py`, `anchorcheck.py` do too). `corpus/QUALITY.md` R29: "An instrument is registered at
the `SKILL.md` § Gates & probes registry under its exact basename". Caveat for the L1: `density.py` and
`capture-source.py` are equally unregistered, so R29 is applied to gate/probe instruments only — the
L1 must first classify the scanner (gate/probe vs capability instrument). Not a predicate failure
(C2's P1/P2 do not read SKILL.md) and not fixable inside this frozen round.

**Q-87-1 — census of record is stale, pre-existing, not r87-caused.** `corpus/instruments/citation-survival.tsv`
was last regenerated in `e300ad5` (round 57); the C1 repoint changes five knowledge texts, so the
committed census cannot match a live `resolve.py` run. `census-freshness-check.py` was **not** run: it
invokes a full lane `resolve.py` census, which this lane's contract bans (~6 min / ~13 GB). The state
is therefore unmeasured-by-contract; [INFERENCE] the gate fails at base and at both landings alike
(a pre-existing round-57 divergence), so no base→landing change is attributable to r87.

**Q-87-2 — the scanner's scope is capture-class only, and it is not enforcement.**
`is_capture_path()` = `corpus/source-snapshots/**`, any `*-receipts` directory, `live-*` files. A
credential in `corpus/knowledge/`, `corpus/practice/` or `corpus/instruments/` is out of scope by
design (documented in the docstring), and no commit path, hook or gate invokes the scanner: the
capability is a manual pre-commit step. The r86 leak happened to fall inside the scope, so K2 is a real
demonstration; the r86 failure mode is now *detectable*, not *prevented*. Re-runnable:
`capture-secret-scan.py --files <any corpus file>` shows the shape works when pointed at a path.

**Q-87-3 — `--files` over the round's own artifacts is noisy.** `capture-secret-scan.py --files
$(git ls-tree -r --name-only 132e16c5 -- .ufo/waves/round-87)` → `scanned=20 hits=7 files=2`: every hit
is a fixture literal inside the frozen candidate and the frozen counter (private-key header, credential
needle, one fabricated key-id-shaped literal). Harmless (not in `--rev` scope, no allowlist row needed),
but a seat told to screen its own round directory will report 7 hits it did not create.

**Q-87-4 — capability row typo.** `SCORECARD.md:307` reads "…seat receipts, live- captures…"; the path
class is `live-` and the row loses its backticks. Cosmetic; routes to the round-end SCORECARD edit.

**Q-87-5 — the capability row's entry command depends on a `master` ref.** `--rev master` resolves today
(`git -C <lane> rev-parse master` → `132e16c5`) even though lane HEAD is detached, so the row runs; but
the row's reproducibility is tied to that ref, not to the pinned commit. The claim's own counter uses
the pinned sha, so nothing is lost for judging.

## Limits of this check

- `resolve.py` lane census intentionally not run (contract), so no independent
  `RESOLVES/MIRROR-EQUIVALENT/INTERNAL/GONE` recomputation; the knowledge-meter's M1–M7 (which imports
  the lane's `resolve.py`) is the scope reading used.
- Anchor content was sampled (13 of 98 replacement sites), not exhaustively matched against every
  quoted fragment.
- The lane working tree carries uncommitted L1 integration work (`LOG.md`, `SCORECARD.md` +15,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-87.md`, seat files under
  `.ufo/waves/round-87/w1/`); nothing in this report judges or depends on those bytes. All readings are
  against commits.

## Files written

- `.ufo/waves/round-87/w1/CriticHarm.md` (this report)
- `.ufo/waves/round-87/w1/CriticHarm-receipts/` (27 receipts): gate transcripts
  `density-{base,c2}.txt`, `cpc-{base,c2}-curl-h1-1913733.txt`,
  `cpc-{base,c2}-curl-ibb-h1-1997312.txt`, `cpcst-{base,c2}.txt`, `sr-{base,c2}.txt`,
  `srst-{base,c2}.txt`, `csst-{base,c2}.txt`, `census-{base,c2}.txt`, `cg-{base,c2}.txt`,
  `gq-{base,c2}.txt`, `capcheck-c2.txt`; claim/evidence receipts `c1-p3-diff.txt`,
  `knowledge-meter-measure-rev.txt`, `knowledge-meter-c1-limb.txt`, `map-bindings.txt`,
  `map-roundtrip.txt`, `r86-252df0c9-scan.txt`. Every receipt is a summary/verdict/HIT line —
  re-scanned with the new instrument, 0 credential-shaped hits.
