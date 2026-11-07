# CriticHarm — round 99 harm audit (kasegi, attempt 1)

Seat: leaf critic, read-only. No subagent dispatch, no commit, no push, no mutating
git/jj. Scratch `S=/fast/scratch/hyaku/kasegi-r99/CriticHarm` (removed at exit);
all clones/extracts/fixtures under it. Receipts:
`.ufo/waves/round-99/w1/CriticHarm-receipts/` (01–06).

## Revisions audited

| role | sha |
|---|---|
| base | `b9411a6b530e486180cf14c72fccc46668dcf5ee` |
| freeze | `6195db307c1cb101eba1d268f8cbfc1578d2caf7` |
| C2 landing | `a3db47e71fe292c03b00ba11f38cccbec45d3966` |
| C1 landing | `35e3ab6041ff8690b00d831f27b93d08101fd16a` |
| HEAD at audit start | `29cd3058c8651b05881764893558deab6780ef1a` |
| HEAD when the report was written | `2c2124f208c98db641842cc50dd24f431c0dfd0e` (integration + claims erratum; both landings remain ancestors — `git merge-base --is-ancestor a3db47e 35e3ab6` → YES) |

`claims.json` is byte-identical freeze→C2 (`git diff --stat 6195db3 a3db47e --
.ufo/waves/round-99/claims.json` empty). Freeze→HEAD changes only unicode escaping
in `axis`/`surface` and adds an `erratum` per claim; `statement`, `predicate`,
`kill`, `instrument_sha256` are unchanged. No contract field moved.

---

## F1 — `SKILL.md`, `PROVINCE.md`, `SHONEN.md`, `AGENTS.md` byte-identical base→C1

**NO HARM.**

```
$ for f in SKILL.md PROVINCE.md SHONEN.md AGENTS.md; do git rev-parse <rev>:$f; done
SKILL.md     base=27f23a93848be29b76992ac35ce423ab9a23c269 C1=27f23a93… HEAD=27f23a93…
PROVINCE.md  base=33458d01cbc04fefcdc53c6489e01213fa76f662 C1=33458d01… HEAD=33458d01…
SHONEN.md    base=8c91054fe177eb9d9f7a88fc665fa55d3b1673bd C1=8c91054f… HEAD=8c91054f…
AGENTS.md    base=299645298e4074975c94a1e54d2da18fccbc1d33 C1=29964529… HEAD=29964529…
$ git diff --stat b9411a6b 35e3ab60 -- SKILL.md PROVINCE.md SHONEN.md AGENTS.md
(empty)
$ git diff --stat b9411a6b HEAD -- SKILL.md PROVINCE.md SHONEN.md AGENTS.md
(empty)
```
Receipt `01-governance-shas.txt`. The four blobs are identical at base, C1 and HEAD.

---

## F2 — `capture-secret-scan.py` loses no earlier shape

**NO HARM on shape identity; one declared narrowing, one untested residual.**

`patterns()` evaluated at base (`b9411a6b`) and C2 (`a3db47e7`):

```
base count 39  c2 count 39
names only in base: []   names only in c2: []
regexes changed: ['gitlab-session-cookie']
  base: …_gitlab_session(?:_geo_[0-9a-f]{64})?[\s\"'=:;]+(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])
  c2  : …_gitlab_session(?:_geo_[0-9a-f]{64})?[^\n]{0,8}[:=][^\n]{0,8}(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])
dup names base: []   dup names c2: []
order identical (excluding new): True
```
Receipt `02-patterns-diff.txt`. No shape removed, added or renamed; every other
shape's regex is byte-identical.

Selftest: base `SELFTEST-RESULT pass cases=170`; C2 `SELFTEST-RESULT pass cases=192`.
The C2 diff adds 22 cases and deletes/modifies none, so all 170 base cases still pass.

**The narrowing.** The new window is not a superset of the round-98 class. Old
class `[\s"'=:;]+` accepted a separator with no `:`/`=`; the new window requires
the operator. Measured against the old and new regexes:

```
space-only      base=True  c2=False   (_gitlab_session <64hex>)
two-spaces      base=True  c2=False
quote-only      base=True  c2=False   (_gitlab_session"<64hex>)
semicolon-only  base=True  c2=False
tab-only        base=True  c2=False
space-quote     base=True  c2=False
colon           base=True  c2=True
eq              base=True  c2=True
```
This is deliberate: C2 adds `gl-session-ck-gap-newline` (`_gitlab_session=\n<hex>`)
as a negative, and the base class (which includes `\n`) fails it — the old class
matched across a line break. S150's window is same-line and operator-bound, so the
narrowing is model-correct. Residual: the whitespace/quote-only separator
(`_gitlab_session <64hex>`) is now a miss and **no selftest case pins it**; it was
a base match. Not a lost shape, but an unmeasured coverage loss on an out-of-model
separator.

---

## F3 — the redaction of the four round-98 receipts

**HARM (provenance).** The *byte substitution* is clean; the *record of it* is not.

### F3a — what actually changed (clean part)

57 lines changed, 57 markers, per file 8 / 12 / 18 / 19:

```
$ for f in body-sweep.txt final-checks.txt matrix-run.txt matrix.tsv; do
    git show a3db47e7:.ufo/waves/round-98/w1/SentinelShapes-receipts/$f \
      | grep -o 'session-cookie-fixture-redacted-r99' | wc -l; done
8  12  18  19      # total 57
```
Every changed line is the base line with one maximal lowercase-hex run (64–68
chars) replaced by the marker; every unchanged line is byte-identical; line counts
are identical (24 / 27 / 110 / 452), so line numbering is preserved. The new regex
matches exactly 57 spans on the base receipts (8 / 12 / 18 / 19); every changed
line has exactly one match and one marker; no changed line has zero or two
matches. Receipt `03-redaction-census.txt`.

### F3b — the count is 57, not 53

`git show a3db47e7:.ufo/waves/round-99/controls/redaction-r99.txt` lists **4**
lines: `body-sweep.txt line=10`, `final-checks.txt line=15`, `matrix-run.txt
line=5`, `matrix.tsv line=306` — exactly the four first-per-file `HIT` lines the
pre-redaction scan prints (`c2-landing-r99.txt`: `hits=4 files=4`; my own
`--rev 7f89004` run prints the same four). The other **53** redacted lines have no
before/after digest.

The claim, the lesson and R160 all say 53:

- `claims.json` C2 addendum / round-99 Goal: "53 synthetic values";
- `corpus/lessons/round-99.md:102` (M99-5): "matched 53 synthetic 64-hex values
  … all 53 values redacted";
- `corpus/QUALITY.md:653` (R160): "the four files held 53 values; the sweep then
  redacted 7+11+17+18 = 53".

The actual per-file counts are 8 / 12 / 18 / 19 = **57**. `7+11+17+18` is each
per-file count *minus its first hit* — i.e. the number the scanner's one-hit-per-
file report hid, not the number redacted. The sweep redacted 57.

R160's own check is "the redaction receipt lists every value with both digests".
The committed receipt lists 4 of 57. **The landing fails the round's own R160
check**, and R160's own "shown able to fail" arithmetic is wrong.

### F3c — 9 lines lost separator bytes

The redactor replaced the maximal hex run, not the regex's value group. On the
`%20` payloads the run starts two bytes early, so the trailing `20` of the `%20`
escape is eaten:

```
final-checks.txt:17  base …_gitlab_session%20=%20<64hex>\n
                     c2   …_gitlab_session%20=%[session-cookie-fixture-redacted-r99]\n
final-checks.txt:18  base …%20:%20<64hex>   c2 …%20:%[marker]
final-checks.txt:19  base …=%20<64hex>      c2 …=%[marker]
matrix-run.txt:7,8,9 and matrix.tsv:410,411,412  same three shapes
```
9 lines total. The receipt now documents the separator `%20=%` (an invalid
percent-escape) instead of `%20=%20`. R153 says "one marker per matched value";
on these 9 lines the marker's span is 66 bytes, not the 64-byte value. The
documented payload shape is corrupted.

### F3d — the "verbatim" citation is false at the landing

The frozen C2 claim's `surface` (claims.json line 26) says:

> "…payloads **verbatim** in `-receipts/final-checks.txt:15-26`"

and the C2 selftest comment (`corpus/instruments/capture-secret-scan.py:641-644`)
repeats "the round-98 sentinel's MUST-FIX payloads, verbatim
(…final-checks.txt:15-26)". At the C2 landing, lines 15-26 are redacted (and three
of them separator-corrupted). The payloads *are* verbatim in the selftest cases
(`capture-secret-scan.py:645-656`), so the evidence survives — but the claim's and
the instrument's cited authority does not hold at the landing. The pre-redaction
failure itself is kept (`c2-landing-r99.txt`, `hits=4 files=4` at `7f89004`), so
R160's "kept as evidence" limb holds.

### Smallest safe correction (F3)

1. Extend `controls/redaction-r99.txt` to all 57 lines with both digests, or state
   "4 exemplars of 57; the other 53 are listed below" and list them. This is a
   documentation-only change; no receipt bytes move.
2. Correct 53 → 57 in the claim erratum, `round-99.md` M99-5 and R160's example
   (and the arithmetic to 8+12+18+19).
3. For the 9 `%20` lines: either re-redact only the 64-hex value so the escape
   survives, or keep the bytes and document that the marker subsumes the trailing
   `20`; in both cases point the "verbatim" citation at the selftest cases.
4. Rewrite the claim's `surface` and the selftest comment to say "the receipt
   lines are redacted (r99); the payloads are verbatim in the selftest cases".

---

## F4 — census pinned numerator is INTERNAL only; no knowledge file edited to move it

**NO HARM** (one low-severity clarity defect).

Code (`census-at-rev.py` at C1, sha `6d68d955…`):

```
num = [k for k in sel if k == "INTERNAL"]        # pinned
num = [k for k in sel if k in ("INTERNAL","RESOLVES","MIRROR-EQUIVALENT")]  # host-incl
```
A `..` walk-out reclassified `HOST-OWNED` is not `INTERNAL`, so it leaves the
numerator and stays in `sel` (denominator). Verified by running the committed
census blob:

```
$ git show 35e3ab60:corpus/instruments/citation-survival.md > census-c1.md
$ python3 -B corpus/instruments/census-at-rev.py --lane . --check census-c1.md --work <scratch>
CENSUS-CHECK pass rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 \
  skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
rc=0
```
Receipt `04-census-check.txt`.

Changed files base→C1: `SCORECARD.md`, `corpus/SOURCES.md`,
`census-at-rev.py`, `citation-survival.md`, `capture-secret-scan.py` (C2),
`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` (C2), the four
receipts and the round-99 wave files. The only knowledge edit is C2's S150 update;
its added text contains no lane-relative path citations (the `_gitlab_session`
forms are not paths), so it adds 0 INTERNAL rows. The +18 INTERNAL (2589→2607) is
tree growth from the round-99 files, not a targeted edit.

**Clarity defect.** The census body is resolve.py's raw output and still counts the
confined row as INTERNAL: body `| INTERNAL | 2608 |`, and
`Terminal outcome classes sum … INTERNAL(2608) … = 8026`. The header's pinned
numerator is 2607. `confined 1` appears only in the instrument's stdout, not in
the census file. The file therefore carries two INTERNAL counts (2607 header,
2608 body) with no in-file reconciliation. The claim's statement is consistent
with the header; a reader citing the body gets 2608. Fix: add a digest-bound
`confined:` header line (and/or a body note) so the two counts reconcile in the
file.

---

## F5 — the census body carries no scratch path

**NO HARM on the committed blob. Live incident, not the landing.**

```
$ git show 35e3ab60:corpus/instruments/citation-survival.md \
    | grep -cE '/fast/scratch|/tmp/|extract-[0-9a-f]{12}|tree-[0-9a-f]{12}'
0
$ … | grep -c '<confined-home>'
1        # Mirror root line: <confined-home>/Projects/the-bounty-hunter (ABSENT)
```
Receipt `04-census-check.txt`. The committed body names the lane root and the
`<confined-home>` token only.

**Live incident (disclosed, not the landing).** At 19:27:37 the lane working tree's
`corpus/instruments/citation-survival.md` and `.tsv` were overwritten with a raw
resolve.py body whose `Lane root:` was
`/fast/scratch/hyaku/kasegi-r99/CriticClaimsC1/D2/w/extract-a3db47e71fe2/tree`
(CriticClaimsC1's D2 symlink test: a `tree` symlink pointed at the lane, so
resolve.py wrote the lane's census). The peer restored both from HEAD at 19:31;
`git status --porcelain corpus/instruments/` is empty and sha256
`211818db7ed71ae2eebfe7fa02890faab7302915c66fc9929be9a44e984859e3` (md) /
`0099820fc9549d6e7287f150b20dc4c7bb61051c7535693e95d10af7384edc6d` (tsv) equal
`git show HEAD:…`. Nothing was committed. Reported here so the round record shows
the working tree was contaminated during the wave and restored.

---

## F6 — no earlier knowledge entry's citation of either instrument is now out of range

**NO HARM mechanically; pre-existing semantic drift, widened by C2.**

```
file lines: capture-secret-scan.py 737, census-at-rev.py 384
citations to the two instruments (all .md, excluding the census): 1051
out of range (last line > file lines): 0
```
Receipt `06-citations-range.txt`. The C1 census anchor table has 83
`capture-secret-scan.py:*` rows, 0 `OUT OF RANGE`. The mechanical range check
passes.

**Pre-existing drift.** The anchor check only tests `last line ≤ file lines`, not
content. Example: `corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md:26`
cites `capture-secret-scan.py:191` and `:196` for `_GH_REFRESH`; `_GH_REFRESH` is at
base line **273** and C2 line **279**, and base line 191 is docstring prose
("`_geo_` + 64 hex) then a separator, an optional"). The citation was already
wrong at base. C2's docstring insertion at lines 189-199 shifts every citation
≥189 by +6, widening the drift; no new citation was added by C2. Not a new
regression, but the census's range check cannot see it, so "no citation out of
range" is weaker than it reads.

---

## X1 — the C2 knowledge entry states a false count

`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:25` (added by C2):

> "A matcher built on a whitespace/quote/operator class refuses **eight of the
> twelve** real session values the round-98 sentinel measured (round 99)."

Measured: the old regex matches **0 of 12** of the MUST-FIX payloads
(`old regex hits on the twelve MUST-FIX payloads: 0 []`); the C2 control says
`mustfix_hit=0/12`; the instrument's own docstring (C2 lines 196-197) says
"refused the twelve". "Eight" is false and contradicts the instrument. Fix:
"all twelve".

## X2 — `--home real` is documented but not implemented

`corpus/instruments/census-at-rev.py:17` (C1): "`--home real` restores the host
reading for an ad-hoc host-inclusive number". argparse has no `--home`:

```
$ python3 -B corpus/instruments/census-at-rev.py --lane . --rev a3db47e7 --home real --work <scratch>
census-at-rev.py: error: unrecognized arguments: --home real
rc=2
```
Receipt `05-tamper-probe.txt`. The census of record does not rely on it (it always
uses the confined HOME), but the docstring promises a feature that does not exist.
Fix: delete the sentence or add the flag.

## X3 — R160's own example arithmetic

`corpus/QUALITY.md:653` says "the four files held 53 values; the sweep then
redacted 7+11+17+18 = 53". Actual per-file counts 8/12/18/19 = 57 (F3b). The
criterion's "shown able to fail" example undercounts by 4 and its check
("the redaction receipt lists every value with both digests") fails as committed.

---

## What I re-ran (claim limbs, for context)

| limb | command | observed |
|---|---|---|
| C1 P1 | `tamper.py --instrument corpus/instruments/census-at-rev.py` | `TAMPER-RESULT killed=12 total=12 evaluated=12 instrument_sha256=6d68d955… rc=0` |
| C1 P1 base | `tamper.py --instrument <e2d3de7b census>` | `TAMPER-RESULT killed=5 total=12 … instrument_sha256=66383371… rc=0` |
| C1 P2 | `census-at-rev.py --check <committed C1 blob>` | `CENSUS-CHECK pass … lane=2607/8026 host_owned=76 confined=1` |
| C2 K1 | `capture-secret-scan.py --selftest` | `SELFTEST-RESULT pass cases=192` |
| C2 K2 | `session-cookie-probe.py --instrument <landing>` | `PROBE-RESULT mustfix_hit=12/12 negatives_extra=0 negatives=10 … rc=0` |
| C2 K3 | `session-cookie-probe.py --instrument <e2caf4a1>` | `PROBE-RESULT mustfix_hit=0/12 negatives_extra=2 … instrument_sha256=45f8d226… rc=0` |
| C2 K4 | `capture-secret-scan.py --rev HEAD` | `… scanned=3485 hits=0 files=0 allowed=27 unused_allow=0 rc=0` |

Receipts `05-tamper-probe.txt`, `04-census-check.txt`. The capability claims
themselves reproduce; the harm is in the redaction record (F3), not the shapes.

---

## VERDICT

VERDICT: `SKILL.md`/`PROVINCE.md`/`SHONEN.md`/`AGENTS.md` byte-identical base→C1 — **NO HARM** — identical blob shas at base, C1 and HEAD; empty diff.
VERDICT: `capture-secret-scan.py` loses no earlier shape — **NO HARM** — 39 shapes, same names, one regex changed; all 170 base selftest cases retained; the separator window narrows whitespace/quote-only separators (declared, S150-model-correct, but the whitespace-only case is untested).
VERDICT: the 53 redacted values are the only bytes changed in the four round-98 receipts — **HARM** — 57 values were redacted (8/12/18/19), the control receipt documents 4 of 57 (fails R160's "lists every value"), 9 lines lost the trailing `20` of a `%20` escape (`%20=%[marker]`), and the claim's "payloads verbatim in final-checks.txt:15-26" is false at the landing.
VERDICT: census pinned numerator is INTERNAL only and no knowledge file was edited to move it — **NO HARM** — `num = [k for k in sel if k == "INTERNAL"]`, `--check` passes at 2607/8026; the only knowledge edit (C2's S150 update) adds no lane-relative citations; minor: body INTERNAL 2608 vs header 2607, `confined 1` not in the file.
VERDICT: census body carries no scratch path — **NO HARM** on the committed blob (0 scratch matches, one `<confined-home>` token); a concurrent seat's D2 test wrote a scratch-rooted census into the working tree at 19:27:37 and restored it at 19:31 — not the landing.
VERDICT: no earlier knowledge entry's citation of either instrument is now out of range — **NO HARM** mechanically (1051 citations, 0 out of range; 83 census anchor rows, 0 OUT OF RANGE); pre-existing content drift remains (e.g. `:191` for `_GH_REFRESH`, which is at 273/279) and C2's +6-line docstring insertion widens it.
VERDICT: C2 capability (S140 assignment-context window) — **NO HARM** — probe 12/12 vs base 0/12, selftest 170→192, landing scan `hits=0`; the defect is the redaction record, not the shape.
VERDICT: C1 capability (tamper-evident census) — **NO HARM** — tamper 12/12 vs round-98 5/12, committed census `--check` passes at 2607/8026, no scratch path; the only instrument defect is the documented-but-unimplemented `--home real`.
