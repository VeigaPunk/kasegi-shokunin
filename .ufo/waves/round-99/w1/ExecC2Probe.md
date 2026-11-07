# ExecC2Probe — independent probe of the round-99 session-cookie window

Seat: ExecC2Probe (read-only attacker/verifier, leaf). Date: 2026-11-07.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scratch root: `/fast/scratch/hyaku/kasegi-r99/ExecC2Probe` (removed before yield; receipts first copied into `ExecC2Probe-receipts/` next to this file).

## 0. Scope and method

Independent fixture probe of C2's landed separator model for `gitlab-session-cookie`
(`[^\n]{0,8}[:=][^\n]{0,8}`, S140 assignment context) at C2 landing `a3db47e71fe292c03b00ba11f38cccbec45d3966`,
with the round-98 instrument at `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061` as the before state.
I wrote my own fixture generator (`gen_fixtures.py`, receipted); the lane's committed probe
(`.ufo/waves/round-99/c2/session-cookie-probe.py`) was only read to transcribe the twelve frozen
MUST-FIX payload shapes (which the frozen claim itself cites verbatim from
`.ufo/waves/round-98/w1/SentinelShapes-receipts/final-checks.txt:15-26`). Every file name and every
64-hex value is nonce-derived (`sha256(nonce|tag)`); all values are synthetic.

## 1. Instrument staging and identity

Commands (lane read-only `git show`; no lane mutation):

```
S=/fast/scratch/hyaku/kasegi-r99/ExecC2Probe
git -C <lane> show a3db47e71fe292c03b00ba11f38cccbec45d3966:corpus/instruments/capture-secret-scan.py > $S/inst/landed/capture-secret-scan.py
git -C <lane> show e2caf4a1561b544a6ea684b0bcfa975f7e7f6061:corpus/instruments/capture-secret-scan.py > $S/inst/r98/capture-secret-scan.py
# plus claim-package-check.py from the same two revs, staged beside each copy (the scanner imports it from HERE)
```

Observed (`ExecC2Probe-receipts/run-manifest.txt`):

```
landed-instrument-rev=a3db47e71fe292c03b00ba11f38cccbec45d3966
8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a  inst/landed/capture-secret-scan.py
r98-instrument-rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061
45f8d226b65e5bf16b9323bfc246c2748319713af5740a608838d6a6eb6f9f0e  inst/r98/capture-secret-scan.py
```

The landed sha256 equals the frozen C2 pin `8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a` (claims.json). The landed regex (staged file lines 318-320):

```python
("gitlab-session-cookie", re.compile(
    _GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[^\n]{0,8}[:=][^\n]{0,8}"
    rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])")),
```

with `_GL_LB = (?:(?<![A-Za-z0-9_])|(?<=\\[ntr])|(?<=\\u[0-9A-Fa-f]{4})|(?<=%[0-9A-Fa-f]{2})|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))` (line 316). Compile is case-sensitive.

## 2. Selftests (K1 echo)

`python3 -B inst/landed/capture-secret-scan.py --selftest` → tail of `landed-selftest.out`:

```
SELFTEST-RESULT pass cases=192
landed-selftest-rc=0
```

`python3 -B inst/r98/capture-secret-scan.py --selftest` → tail of `r98-selftest.out`:

```
SELFTEST-RESULT pass cases=170
r98-selftest-rc=0
```

Matches K1 (192 at the landing) and the do-nothing control (170 at e2caf4a1).

## 3. Fixture build (discipline)

```
D=$(mktemp -d "$S/fix.XXXXXX")            # -> fix.ZheULT, under scratch, not /tmp
git -C "$D" init -q
T=$(git -C "$D" rev-parse --show-toplevel); [ "$T" = "$D" ]   # asserted before first commit
python3 -B "$S/gen_fixtures.py" "$D"      # 48 files: cases/pos/*.txt (24), cases/neg/*.txt (24)
git -C "$D" add -A && git -C "$D" commit  # head 4f5befcb3990294922ca4a0526506e87df8def29
```

Two further fixture repos under the same discipline: `char.mbVmVW` (boundary-band probe, head `4ce7a6e2c6e8b957083ac25e8ce909af679754ea`, 12 files) and `suf.b1XaJM` (keyword-suffix probe, head `2509094ec04a19f199a562002bf8eca4d807101f`, 3 files). Nonce: `ExecC2Probe-receipts/nonce.txt`; exact per-case bytes: `payloads.txt`; case→file map: `manifest.json`; scanner file lists: `fixture-files.txt`, `char-files.txt`.

Case design (all 48 in one `--files` invocation per instrument):
- **12 MUST-FIX positives** — the frozen round-98 payload shapes byte-for-byte in shape: `cell--`, ` => `, `%20=%20`, `%20:%20`, `=%20`, `(=`, `( = ) `, `,=`, `|=`, `+=`, `=> `, geo+`%20=%20`.
- **12 NEW separator positives of my own** — tab-assign `\t=\t`, YAML `: `, JSON `"_gitlab_session": "H"`, `='H'`, shell `"${H}"`, Python `resp["x"]["_gitlab_session"] = H`, `  =  `, `==`, geo+`\t:\t`, `:cell-31-`, `:%20`, `Cookie: _gitlab_session=H; Path=/`.
- **24 boundary negatives** — left/right window overflow with dashes/spaces/letters (9, 12), newline before/after separator, CRLF before value, value 63 / 65 hex, uppercase hex, base64 value, hyphen-split 63-hex value, no separator, tabs no separator, malformed `cell-abc-`, geo id 63 hex, geo gap 9, uppercase keyword, word char before keyword, wrong/underscores-less cookie names, bare URL hex, 32-hex value.

## 4. Landed instrument — exact hit set

`python3 -B inst/landed/capture-secret-scan.py --files $(cat fixture-files.txt)` → `landed-files.out` (rc=1 as expected with hits):

```
CAPTURE-SECRET-SCAN mode=files scanned=48 hits=25 files=25 allowed=0 unused_allow=0 rc=1
```

- **Positives: 24/24 hit, zero misses.** All twelve MUST-FIX shapes (m01–m12) and all twelve new variants (n01–n12) each produced exactly one `HIT shape=gitlab-session-cookie` on their own file (all 24 HIT lines are in `landed-files.out`, one per `cases/pos/<sha20>-<slug>.txt`).
- **Negatives: 23/24 clean, 1 extra hit** (`landed-files.out:25`):

```
HIT shape=gitlab-session-cookie path=.../cases/neg/1d17f8bfe3a32846be8e-b06-value-65-hex.txt line=1
```

  b06 is `_gitlab_session=<65 lower-case hex>\n` (`payloads.txt`, case `b06-value-65-hex`). The frozen claim's own negative set is untouched by this (it is my independent case), but it is a real overmatch: see §6.

## 5. Round-98 instrument (before state) — same files

`python3 -B inst/r98/capture-secret-scan.py --files $(cat fixture-files.txt)` → `r98-files.out` (rc=1):

```
CAPTURE-SECRET-SCAN mode=files scanned=48 hits=17 files=17 allowed=0 unused_allow=0 rc=1
```

- **Positives hit: 9/24** — n01 tab-assign, n02 yaml-colon-space, n03 json-quoted, n04 single-quoted, n07 double-space-assign, n08 double-equals, n09 geo-tab-colon, n10 cell-colon, n12 cookie-header (exactly the variants whose separator chars all sit in the round-98 whitespace/quote/operator class).
- **Positives missed: 15** — **all twelve frozen MUST-FIX shapes m01–m12** (independent confirmation of the frozen `mustfix_hit=0/12` base control on my own transcription of the payloads), plus n05 (`"${`), n06 (`"] = `), n11 (`:%20`).
- **Negatives falsely hit: 8/24** — b03 newline-after-sep, b04 newline-before-sep, b10 no-separator, b11 left-window-12-spaces, b17 crlf-before-value, b20 right-window-9-spaces, b21 geo-gap-9-spaces, b24 tabs-no-sep. The round-98 class `[\s"'=:;]+` accepts zero-width and unbounded whitespace as the separator and crosses newlines — it is both under- and over-matching relative to the landed window.

## 6. Characterizing the b06 overmatch (porous right band)

Hypothesis: the right window `[^\n]{0,8}` can swallow up to 8 *hex* chars, so a hex run L after the separator hits iff a 64-hex substring starts ≤8 chars in and a non-hex char follows — i.e. **64 ≤ L ≤ 72**. `char_probe.py` (receipted) built `_gitlab_session=<L hex>` for L ∈ {63,64,65,66,72,73,128} and `_gitlab_session=<k hex><64 hex>` for k ∈ {1,2,8,9,10}; landed scan (`landed-char.out`, rc=1):

```
HIT ... run-64-hex.txt / run-65-hex.txt / run-66-hex.txt / run-72-hex.txt
HIT ... prefix-1-then-64.txt / prefix-2-then-64.txt / prefix-8-then-64.txt
CAPTURE-SECRET-SCAN mode=files scanned=12 hits=7 files=7 ... rc=1
```

No hit for run-63 (correct), run-73, run-128, prefix-9, prefix-10 — exactly the predicted band: **65..72-hex runs overmatch; ≤8 leading hex chars are swallowed before a 64-hex value.** `(?![0-9a-f])` bounds only the tail of the matched 64; the window has no hex-exclusion on its 8 consumable chars. The committed selftest covers 63 (`gl-session-ck-63-hex` → none) but no length above 64, which is why this band is invisible to the 192 cases.

Second precision observation (same left-window mechanism, suffix probe `landed-suffix.out`, rc=1): `_gitlab_session_id=H`, `_gitlab_sessionfoo=H`, `_gitlab_session_2=H` all **hit** — any name sharing the `_gitlab_session` prefix with ≤8 extra chars before `[:=]` is reported. This is S140's `.{0,8}` assignment-context class by construction (faithful to the source the claim cites), but it is a superset of the session cookie itself.

## 7. Verdict

The frozen K-limb echoes reproduced (selftest 192/170, landing sha pin match); the landed window catches all twelve frozen MUST-FIX shapes **and** twelve new separator variants I chose adversarially, with zero extra hits on 23 of my 24 independent negatives. Two findings go to the verifier, neither of which is a frozen-negative violation:

1. **Overmatch band:** hex runs of 65–72 chars after the separator hit (64 ≤ L ≤ 72); ≤8 leading hex chars are swallowed by the right window before the counted 64. Repro: `b06-value-65-hex` (`_gitlab_session=` + 65 hex).
2. **Prefix superset:** `_gitlab_session` + ≤8 arbitrary non-newline chars + `[:=]` + 64 hex hits (e.g. `_gitlab_session_id=H`).

VERDICT: C2 landed window vs 24 positives (12 frozen MUST-FIX + 12 new variants) — 24/24 hit, 0 miss: CONFIRMED.
VERDICT: C2 landed window vs 24 independent boundary negatives — 23/24 clean; 1 extra hit (65-hex run, band 65–72): CONFIRMED WITH NEW OVERMATCH FINDING.
VERDICT: C2 before-state (r98 instrument at e2caf4a1) vs same positives — 15/24 missed incl. all 12 MUST-FIX, 8/24 negatives falsely hit: CONFIRMED.
VERDICT: C2 frozen predicate (K1 selftest=192 + landing sha pin; landed-clean negatives semantics) — reproduced, not falsified by this independent probe; findings above are precision notes outside the frozen negative set.
