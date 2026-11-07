# CriticClaimsC2 — attack on C2's frozen K1–K6 at the C2 landing `a3db47e7`

Read-only attacker. Lane clone `git clone --shared . $S/lane` + `checkout a3db47e71fe292c03b00ba11f38cccbec45d3966`;
`git -C $S/lane rev-parse --show-toplevel` printed `$S/lane`. No tool installs (Python 3 stdlib only).
Instrument sha256 at the landing `8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a`,
probe sha256 `79b2235d94295129fbc6c404a6d7005772099dd9489e446df875488d3fef6904` — both equal the frozen pins.
`H` below is the probe's synthetic value, `"0123456789abcdef"` × 4 (never written out as a literal run here).

## 1. K1–K6 re-run at the landing

| limb | command | observed | verdict |
|---|---|---|---|
| K1 | `python3 -B corpus/instruments/capture-secret-scan.py --selftest` | `SELFTEST-RESULT pass cases=192`, rc=0; sha256 `8b338726…` | PASS |
| K2 | `python3 -B .ufo/waves/round-99/c2/session-cookie-probe.py --lane . --instrument corpus/instruments/capture-secret-scan.py --work $S/w` | `PROBE-RESULT mustfix_hit=12/12 negatives_extra=0 negatives=10 instrument_sha256=8b338726… rc=0` | PASS |
| K3 | same probe, `--instrument` = `git show e2caf4a1:corpus/instruments/capture-secret-scan.py` | `PROBE-RESULT mustfix_hit=0/12 negatives_extra=2 negatives=10 instrument_sha256=45f8d226… rc=0` | PASS |
| K4 | `python3 -B corpus/instruments/capture-secret-scan.py --lane . --rev a3db47e7…` | `scanned=3485 hits=0 files=0 allowed=27 unused_allow=0 rc=0` | PASS |
| K5 | `grep -c '^\| capture-secret-scan \|' SCORECARD.md`; row 307 cells | one row; contains ``separator window `[^\n]{0,8}[:=][^\n]{0,8}` `` and `gitlab-session-cookie`; cell 5 = `87` | PASS |
| K6 | `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` | states the window at :21-22 and :78-79, cites S140 (:3), S148 (:38, :52), S150 (:3, :38) | PASS |

K3 is a clean instrument-vs-instrument comparison: `git diff --stat e2caf4a1 a3db47e -- corpus/instruments/claim-package-check.py corpus/instruments/capture-secret-scan.py`
shows only `capture-secret-scan.py` changed (48+/12−), so the gate the probe stages beside the base instrument is byte-identical.
Base selftest run staged with the same gate prints `SELFTEST-RESULT pass cases=170` — the 170→192 delta is real (22 = 12 positives + 10 negatives).

## 2. Attack: a strict `_gitlab_session=` + 64-hex matcher (the round-98 model)

Variant V1 replaces the whole shape with `_GL_LB + _gitlab_session(?:_geo_…)?= (?:cell-[0-9]+-)? [0-9a-f]{64}(?![0-9a-f])` — operator must be `=` immediately after the keyword, no window.

`V1-strict-eq-only,0/12,0,-` → **the twelve payloads kill it, 0/12.** The limb "the twelve payloads discriminate the separator model" is real.
The reason is visible in the payload set: **none** of the twelve is `_gitlab_session=` + 64 hex. Each either puts a byte before the
operator (`%20=`, `%20:`, `(=`, `,=`, `|=`, `+=`, ` => `, ` ( = ) `), a byte after it (`=%20`, `=> `, `=cell--`, ` ) `), or both
(`%20=%20`); the geo payload puts 64 hex between the keyword and the operator.

## 3. Attack: `.*` instead of `[^\n]{0,8}`

Variant V2: `_gitlab_session….*[:=].*(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])`.

`V2-dotstar-both,12/12,3,n-geo-short,n-cell-nondigit,n-gap-9` → the ten negatives kill it three times over.
`n-gap-9` is the direct one: nine spaces before `=` must not match, and `.*` swallows them. **Real limb.**

## 4. Attack: does `[^\n]` really refuse a newline?

Variant V9 replaces both windows with `[\s\S]{0,8}`: `V9-newline-crossing,12/12,1,n-gap-newline` → killed by `n-gap-newline`.
And the round-98 scanner did cross a newline: K3's `negatives_extra=2` is exactly `n-gap-9` **and** `n-gap-newline`
(`PROBE n-gap-newline hit=True want=False FAIL` on the base instrument). **Real limb, and a real fix.**

## 5. Full variant matrix (probe's own 22 cases; `pos` = 12 MUST-FIX hits, `neg` = negatives that start to hit)

```
V0-landing                12/12  0  -
V1-strict-eq-only          0/12  0  -
V2-dotstar-both           12/12  3  n-geo-short,n-cell-nondigit,n-gap-9
V3-right-window-100       12/12  1  n-cell-nondigit
V4-no-right-lookahead     12/12  0  -                      <-- passes everything
V5-no-left-boundary       12/12  1  n-left-word
V6-case-insensitive       12/12  1  n-upper-hex
V7-cell-word              12/12  1  n-cell-nondigit
V8-no-geo                 11/12  0  -                      (ck-geo-pct20 kills it)
V9-newline-crossing       12/12  1  n-gap-newline
V10-operator-free         12/12  2  n-cell-nondigit,n-gap-9
V11-no-cell-group         12/12  0  -                      <-- passes everything
V12-cell-before-window    12/12  0  -                      <-- passes everything
V13-no-cell-no-lookahead  12/12  0  -                      <-- passes everything
```

**Real limbs** (a wrong instrument is killed): the left window bound (`n-gap-9`), the operator `[:=]` (V10), the newline refusal (V9),
the left boundary `_GL_LB` (V5), lower-case hex (V6), `cell-[0-9]+-` *as a digit class* (V7), the `_geo_` alternative (V8),
and the right window bound — V3 with `[^\n]{0,100}` is killed by `n-cell-nondigit` because a 100-byte window swallows `cell-abc-`;
the positives need ≥6 bytes after the operator (`cell--`), so the right bound is pinned to 6–8.

**Passable limbs** — wrong instruments that score 12/12, 0 negatives, **and pass the full 192-case selftest**:

- `V11-no-cell-group` — `(?:cell-[0-9]+-)?` deleted entirely: `SELFTEST-RESULT pass cases=192`.
- `V4-no-right-lookahead` — `(?![0-9a-f])` deleted: `SELFTEST-RESULT pass cases=192`.
- `V13-no-cell-no-lookahead` — both deleted: `SELFTEST-RESULT pass cases=192`.
- `V12-cell-before-window` — the cell group moved to before the window: `SELFTEST-RESULT pass cases=192`.

Both limbs are load-bearing in narrow ranges that no case reaches: the cell group only matters for `cell-<N>-` with N ≥ 3 digits
(`cell-123-` is 9 bytes and overflows the window; `cell-7-` is 7 bytes and the window absorbs it — the only `cell-` positive in the
selftest is `cell-7-`). Direct check: `_gitlab_session=cell-123-<H>` → landing `True`, V11 `False`; `_gitlab_session=cell-7-<H>` →
both `True`. The lookahead only matters for a ≥73-hex run. Neither range is planted in the probe or the selftest.

## 6. Hidden regressions the widening introduced (base vs landing, same gate)

```
case                               base   landing
64-hex (control positive)          True   True
65-hex                             False  True    <-- regression
72-hex                             False  True    <-- regression
73-hex                             False  False
empty-session-then-other-cookie    False  True    <-- over-attribution
keyword-semicolon-other            False  True    <-- over-attribution
keyword-9-eq                       True   True
keyword-17-eq                      True   True
cell-3digit                        True   True
cell-1digit                        True   True
value-then-hex-letter              False  True    <-- regression
```

1. **The `(?![0-9a-f])` right boundary is defeated by the window.** The after-window can shift 1–8 bytes into a hex run, so a
   65–72-hex run matches by starting the 64-hex match one to eight bytes later; only ≥73 hex is refused. Round-98 refused 65-hex
   outright (its separator class could not absorb hex). The frozen statement presents `(?![0-9a-f])` as the value boundary; under
   this window it refuses only ≥73. This is inherent to S140's own `<keyword>.{0,8}[:=].{0,8}<value>` form — the `%20` positives
   make a maximality lookbehind impossible (the byte before the value is `0`, hex) — so it is a **statement-text defect, not a fixable
   instrument defect**.
2. **Over-attribution.** `_gitlab_session=; other=<H>` and `_gitlab_session; other=<H>` now match (base refused). A 64-hex value that
   belongs to a following cookie is attributed to `_gitlab_session`. Faithful to the generator, but the knowledge doc's *Limits*
   section (:76-84) lists only under-match limits (next line, gap > 8, prefixed name); it does not state over-attribution.

## 7. Provenance and accounting defects around the redaction

- **Count is wrong.** The frozen statement and the landing message say **53** synthetic values. The landing diff has **57** added
  marker lines and **57** removed 64-hex lines; markers per file are 8 + 12 + 18 + 19 = 57. Distinct removed values: 2 (all synthetic).
- **The control under-reports.** `controls/redaction-r99.txt` has 4 `before=` lines ("the four … lines"); 57 lines were redacted.
- **The control's `after=` digests are not the landed files.** All four `before=` digests are the whole-file sha256 *before* redaction
  (verified). The `after=` digests are the file with **only that one line** redacted — verified for all four by reconstructing the
  single-line state (`body-sweep` 10/65, `final-checks` 15/64, `matrix-run` 5/64, `matrix.tsv` 306/65 all reproduce their `after=`
  digest), not the landed file. Landed file digests are `6b8c8833…`, `95a1ea3e…`, `f085df54…`, `d2954f70…` — none is recorded
  anywhere. The landed bytes are therefore not digest-bound by the control.
- **The probe's citation is stale at the landing.** The probe docstring says the payloads are verbatim from
  `final-checks.txt:15-26`; at the landing those lines carry `[session-cookie-fixture-redacted-r99]`. The payloads *are* byte-identical
  to `a3db47e^:.ufo/waves/round-98/w1/SentinelShapes-receipts/final-checks.txt:15-26` (verified: `byte_identical=True`), so the citation
  should name the parent revision.
- **The redaction mutated the separator it is supposed to preserve.** On four lines the 64-hex match ran backwards into the `20` of
  `%20`: `%20=%20<H>` → `%20=%[marker]`, `%20:%20` → `%20:%`, `=%20` → `=%`, and the geo line likewise. The landing receipt no longer
  shows the three-byte separator the claim is about. "Structural" is overstated for those four lines.

## 8. Impacted axes

- **coverage (8):** the capability gain is real and independently reproducible — base 0/12, landing 12/12, base selftest 170, landing 192,
  and the ten negatives kill every widening variant except the two unplanted limbs. The gain is not in doubt.
- **depth:verifiability:** weakened at the edges — two limbs of the frozen regex are unbound by both the probe and the selftest, the
  redaction count is wrong by four, and the redaction's own after-digests do not describe the landed bytes.

## 9. Smallest safe correction

1. Add two cases to `session-cookie-probe.py` **and** the selftest: a `cell-123-` positive (pins `(?:cell-[0-9]+-)?`) and a 73-hex
   negative (pins `(?![0-9a-f])`). The landing instrument already passes both (`cell-3digit True`, `73-hex False`), so no instrument
   change and no re-freeze of the shape.
2. Correct 53 → 57 in the statement/landing message, and either record the four landed file digests or say the `after=` digest is the
   single-line-redacted state.
3. Cite the twelve payloads as `a3db47e^:…final-checks.txt:15-26` (or note the landing redaction).
4. Add one *Limits* sentence for 65–72-hex acceptance and one for over-attribution to a following cookie.

## 10. Verdicts

VERDICT: K1 PASS — `SELFTEST-RESULT pass cases=192`, rc=0, instrument sha256 `8b338726…` at `a3db47e7`.
VERDICT: K2 PASS — `mustfix_hit=12/12 negatives_extra=0 negatives=10`, probe sha256 `79b2235d…`.
VERDICT: K3 PASS — base instrument at `e2caf4a1` scores `mustfix_hit=0/12` with the same gate.
VERDICT: K4 PASS — `scanned=3485 hits=0 files=0 allowed=27 unused_allow=0` at the landing.
VERDICT: K5 PASS — one `capture-secret-scan` row, names the shape and the separator window, first-working-round cell 87.
VERDICT: K6 PASS — knowledge entry states the window and cites S140, S148, S150.
VERDICT: strict `_gitlab_session=`+64-hex matcher KILLED by the twelve payloads — 0/12; this limb is real.
VERDICT: `.*` matcher KILLED by the ten negatives — 3 negatives hit (`n-geo-short`, `n-cell-nondigit`, `n-gap-9`); this limb is real.
VERDICT: newline refusal REAL — `[\s\S]` variant killed by `n-gap-newline`, and the round-98 scanner did hit that negative.
VERDICT: `(?:cell-<N>-)?` limb PASSABLE — V11 (limb deleted) and V12 (limb moved) score 12/12, 0 negatives, and pass the full 192-case selftest; only an unplanted `cell-123-` positive separates them from the landing (landing True, V11 False; `cell-7-` is True on both).
VERDICT: `(?![0-9a-f])` limb PASSABLE — V4 (limb deleted) scores 12/12, 0 negatives, and passes the full 192-case selftest.
VERDICT: frozen statement regex OVER-SPECIFIED — two of its limbs are unbound by K1+K2; the behavioural claim (12 hit, 10 refused) is fully supported.
VERDICT: redaction accounting FAILS as written — 53 claimed vs 57 observed, 4 control lines vs 57 redacted, after-digests not the landed files, `%20` mutated on four lines.
