# SentinelGitHub — round 92, wave 1: adversarial bypass search on the landed `github-token` shape

Seat: attack/verify (leaf, no delegation, no edits outside this wave dir).
Surface: `corpus/instruments/capture-secret-scan.py` at `58c0c115342877ee556cae19928d69839b0b29f0`
(instrument sha256 `04666f67…af3a9e`, gate `8b6f8493…1cc8e6`, allowlist `76245bba…bc1985` — all three
re-derived from the rev and equal to the frozen pins; `--selftest` at those bytes: `SELFTEST-RESULT pass cases=68`).
The instrument was run from a copy in scratch beside that rev's `claim-package-check.py` and
`capture-secret-allow.tsv`, so the gate's imported shapes and the default allowlist are the landed ones.

**Claims are judged only on their frozen predicates.** Everything below is a routed defect or a
qualifier against the *instrument*; nothing here re-scores C1 or C2, and nothing contradicts K1–K8.

## Axes (Godspeed)

1. **depth:verifiability** — every finding is one command plus a fixture digest; two re-runnable scripts
   rebuild all fixtures from scratch with no credential-shaped literal in the script.
2. **coverage** — 69 single-fixture probes measured *which* capture encodings the shape reaches and which
   it does not, instead of asserting a list.

## Method

69 one-fixture files, each scanned with `--files` by the landed instrument; the observed shape set is
recorded per file (never the bytes) in `SentinelGitHub-receipts/probe-encodings.tsv`
(columns: id, verdict, probe class, shapes, rc, realism, first-party/limit status, fixture sha256, note).
Fixture tails are 36-character base62 values generated for this seat; nothing real and nothing copied.

## 1. DETECTED — 21 realistic capture encodings, all hit `github-token`

| form | ids | note |
|---|---|---|
| `https://x-access-token:<t40>@github.com/…`, plain-userinfo variant, `.git-credentials` line | d01 d02 d19 | `:` and `/` are fine left boundaries; `@`/EOL fine right boundaries |
| `Authorization: token <t40>`, `Authorization: Bearer <t40>` | d03 d04 | `token` form is caught by **no** gate shape (`credential` needs `token[:=]`), so this is the shape doing real work; Bearer is double-covered by the gate |
| `.netrc` `password <t40>` | d05 | |
| `GH_TOKEN=`/`GITHUB_TOKEN=` env dump, bare, quoted and `export`ed | d06 | `\btoken\b` does not match `GH_TOKEN`, so no gate fallback |
| YAML key, JSON key, HAR `name`/`value` object, `curl -H` line, `git diff` added line, query parameter | d07 d09 d10 d11 d20 d21 | JSON/YAML keys are also caught as gate `credential` |
| python bytes literal and `repr()` | d08 | `'`/`"` are fine left boundaries |
| JSON `\n` and `\r\n` escapes before the token | d12 d13 | the documented lookbehind exception, both spellings |
| UTF-8 BOM, CRLF line ending, markdown code span | d14 d15 d16 | |
| stateless `ghs_<digits>_<3-segment JWT>` in prose and as a JSON value | d17 d18 | |

Reading: the shape is **value-robust**. Wherever the token's own bytes reach the regex intact, the match
happens regardless of the surrounding syntax. Every miss below is an *encoding* miss, not a value miss.

## 2. BYPASS — measured misses, split by what the frozen statement and the sources already say

### P1 — escape-terminator family (unnamed gap; fix next round)

The left boundary is `(?<![A-Za-z0-9_])` or the literal two-byte `\n` escape, so **every capture escape
whose last byte is a letter or digit hides a token**. Measured, all `hits=0`, `rc=0`:

| escape immediately before the token | id | digest (sha256 of fixture) | realism |
|---|---|---|---|
| JSON `\t` | b11 | `d687aa947ffc3fc36f9a9bdb47d0a0c0ad4f1a6797dc94d1511716189918cb1b` | medium — tab-indented output embedded in a JSON log |
| JSON `\r` | b12 | `4e5123ef4e38fe536b45a764d67a2a00bba0315948ee540f3ad1847b4e464bfb` | low |
| JSON `\u000a` | b20 | `47cf2c2af26a926d64b2c03f4d1e1f486113b394499d51e7c27ed8112f946614` | low — serializers emit `\n` |
| JSON `\u0020` | b15 | `4f3ecf16e400337dfa6ec541e5bc33376bf5b93edfc2ff7b3b7ce531a8d6a3e9` | medium — re-encoded header value |
| `%20` | e05 | `255957e988c2ac34abab674d7af2a43ec6e50525568ab4e27590e45bb39f5014` | medium |
| `%20` inside a JSON query value | b14 | `8a52ad862946fcd1b94be8f2080719f56ee261170625a5174b198fe5f0acf937` | medium |
| `%09` | e06 | `9d2c10fdb9a4fbabcd747dfe8323d53528c8aabd6382aaeed3b4cdb001af6c44` | low |
| `%3A` (`x-access-token%3A…`) | b13 | `3fd7d502ec5644ed2f3e2709d1878350e2a298388b2db65c608342eefcd04b09` | medium — a capture pipeline that encodes the whole userinfo |
| `%2F` (double-encoded path) | e04 | `24f709c05819a462a6e324d177e4a11e0080c94358f1a0d370ba9c8b3a9c5ef7` | medium |
| `\u0026` | e01 | `b6a13fb533aeb804799745e3e4aae23f3771f193ed12e1ab7e4a2b3e472caade` | low |
| `%26` | e02 | `7e49062afcc0974c12a274a9a19988073995ec70707ac5feb60d6bf3102e95ef` | low |

Control: `&#38;` before the token **is** detected (e03) — the escape's last byte is `;`, not alnum. That
is the whole mechanism: it is the *last byte* of the escape, not the escape itself, that decides.

Why this is a defect and not a judgement call: the same encoding family is already handled by the sibling
shapes in this file — `\u0026`, `&amp;` and `%26` are explicit separators for `azure-sas-signature`, and
`\n` is explicit for the CloudFront cookie shape. The github left boundary kept only `\n`. The frozen C2
statement says "not preceded by a letter, digit or `_` (except the `n` of a JSON `\n` escape)", and a
`\t`-escape ends in a letter, so **the landed counter is faithful to the frozen predicate** — this is a
spec/shape refinement for next round, not a claim violation.

Smallest remediation (one line, measured — `SentinelGitHub-receipts/patch-verification.txt`):

```python
_GH_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\[ntr])|(?<=\\u[0-9A-Fa-f]{4})|(?<=%[0-9A-Fa-f]{2})|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))"
```

All alternatives are fixed width (2, 6, 3, 5, 7), which Python lookbehind requires. Applied to a scratch
copy of the landed file (that line only): `--selftest` still prints `SELFTEST-RESULT pass cases=68`, all
eleven P1 fixtures flip from `hits=0` to `github-token`, P2 stays a miss as intended, and every false
positive in §3 is unchanged (the patch moves only the boundary, never the value match).

### P2 — encoded prefix separator (unnamed gap; document rather than widen)

`gh[pousr](%5F|%5f|\u005f|\u005F|&#95;|&#x5F;)` + 36 base62: b01 `17defecb…9584e`, b05 `3f1d7611…df2401`,
b06 `71daaf68…d3effae` — all `hits=0`. Undocumented by either source (neither page discusses capture
encoding), and unrealistic unless a capture was encoded twice, because `_` is unreserved and normal
encoders leave it alone. Recommendation: add it to the docstring's known-limits list next round, do not
widen the shape (a second spelling of the separator doubles the FP surface for no measured gain).

### P3 — named known limits, confirmed as misses (no action)

- soft-wrapped values: b07 (`60527ef0…73a4d` — plain line split), b08 (`e306df9d…6f6c6f` — JSON `\n`),
  e09 (`7995547a…e43695` — no key name anywhere near the fragment, **no shape fires at all**),
  e10 (`d6bf833b…02cc9` — git-remote split: `github-token` misses, gate `credential` catches only the
  first fragment because `x-access-token:` happens to precede it). The known limit is real; a key name
  beside the first fragment is a partial mitigation, not a cover.
- base64-wrapped: b09 (HTTP Basic, `f28bcab4…f813d`), b10 (`0ce8fbc9…984b`) — this is the *realistic*
  form of a captured API request, and the docstring already names it.
- fine-grained: b16 (`7b6721ac…dbd3b`) — named.
- UTF-16 and gzip captures: b17, b18 — named.

### By design, not defects

- b19 `756e637e…512b7`: tail followed by `_` → no hit (a longer token-looking id); the right boundary is
  doing exactly what the frozen statement requires.
- e11 `a41ba72b…16321b`: two tokens concatenated with no separator — the lookahead blocks the first and
  the lookbehind the second, so both are lost. Realism ~0 (needs a separator-free concatenation of two
  live tokens); listed only so it is not mistaken for a detection.

## 3. FALSE POSITIVES — the shape's FP surface is wider than the docstring implies

Measured hits on strings that were never minted:

| fixture | id | digest | why it is not a credential |
|---|---|---|---|
| 40-character example value of the published documentation form | f01 | `e72b6eb5…38eda9` | [INFERENCE: provenance — no network fetch was permitted, so the value is not re-opened here] the FP class itself is proven by f10/f11/f14 regardless; any capture quoting such an example is refused |
| 36 identical `x` placeholder | f02 f14 | `8b696fe6…cb5c861`, `8dd2c0f2…0b2475` | documentation placeholder (f14 is the `credential`+`github-token` pair) |
| CDN asset id `ghs_`+36 / `ghp_`+36 | f10 f11 | `4589aed3…e9b2682`, `22c0242a…4643320e` | an identifier, not a token; this is the exact class S137:162 says the `_` separator is meant to avoid |
| 4-segment dotted value after `ghs_<digits>_` | f05 f12 | `cbdcf628…1f75b29` | the stateless branch has no right boundary; it matches a prefix of a longer dotted string |
| timestamp/event/log triple after `ghs_<digits>_` | f04 | `0a53ae45…c8c895068` | matches because a 14-digit timestamp is a valid base64url segment of 10+ |

Operational consequence, verified end to end (`allowlist-repro.sh`):

```
(a) rev mode, no allowlist        scanned=2 hits=2 allowed=0 rc=1     (both files refused)
(b) rev mode, one row             hits=1 allowed=1 rc=1               (that value allowed; a DIFFERENT
                                                                       value at the same path still hits)
(c) files mode, absolute path     hits=1 allowed=0 unused_allow=1 rc=1 (the same row does not apply)
(d) files mode, repo-relative     hits=0 allowed=1 rc=0
```

So: the per-value binding is correct and is the right remediation for a documentation example, but the
row only applies when the path is spelled the way it was authored — see D3.

### Documentation defect (D4)

`capture-secret-scan.py`'s shape paragraph says the last six characters are "a 6-character checksum,
S137 lines 167, 173" but never says the checksum is **not verified**. It is not: the shape is prefix plus
36 base62, full stop. So the honest FP bound is S137:164's prefix-only figure ("0.5%"), and S137:166's
"virtually eliminates false positives" is not reached by this instrument — `f01`, `f02`, `f10`, `f11`,
`f14` are the measurement.

The fixes available: bind an allowlist row (works, §3 (b)), or verify the checksum — which is **not
implementable from the frozen sources**: S137:167 names CRC32, Base62 and leading-zero padding but neither the alphabet order nor the
covered span. Sweep (`SentinelGitHub-receipts/checksum-sweep.txt`): 6 candidate bodies × {crc32, adler32}
× 5 candidate alphabets × 2 paddings = 120 combinations, **0** reproduce the published example's last six
characters. That makes the example [INFERENCE] checksum-invalid — consistent with S137:166 — but the
inference is not load-bearing for D4; D4 rests on the measured HITs of never-minted strings above.

### A sibling candidate overstates this (routed, do not edit)

`candidate-knowledge-github-prefixed-tokens.md` (sha256 `f1d2a2f39e742e267414e370fcf5939d343ff3d96b9c4d88f19e5a415fe17144`,
299 lines) rejects the misreading "A prefixed string is a live token" with:

> "the prefix plus checksum proves the format, and the checksum is checkable offline" (line 281)

and in the liveness qualifier writes "a checksum-valid string can still be a revoked token" (line 81).
The landed instrument checks no checksum, so a match proves *the byte shape*, not that the string was ever
minted: `f02`, `f10`, `f11`, `f14` are matches that no checksum could have produced if one were applied.
Line 81 is acceptable as a statement about tokens; line 281 is false about this instrument and should read
"the prefix plus a 36-character tail proves the byte shape; the checksum is documented (S137:166-167) but
not verified, so a match is a candidate, not a confirmation".

## 4. Routed defects

| id | severity | exploit path | evidence | smallest remediation |
|---|---|---|---|---|
| D1 | low–medium | a capture whose token is preceded by `\t`, `%20`, `\u0020`, `%3A` or `%2F` is committed with `rc=0`; a live PAT reaches `corpus/` exactly as in M86-2, at the encoding the capture pipeline chose | P1 table, 11 fixtures, all `hits=0`; controls e03/e07/e08 show the mechanism; `patch-verification.txt` shows the one-line fix closing all eleven | the one-line `_GH_LB` widening above (selftest still 68/68, FPs unchanged); add the `\t` and `%XX` forms to K4/K8 next round |
| D2 | low | `gh[pousr]` + encoded separator is invisible; only matters for doubly-encoded captures | b01–b06, all `hits=0` | one docstring known-limit clause; no shape change |
| D3 | low (fails safe) / medium workflow | in `--files` mode the allowlist key is the path *as spelled on the command line*, while rows are authored repo-relative; the pre-commit scan of a wave file with an absolute path reports `allowed=0 unused_allow=1` and refuses an already-allowed capture | `allowlist-repro.sh` (c) vs (d); same row, same bytes | accept `--lane` in `--files` mode and key rows on the lane-relative path; or document "run `--files` from the lane root with repo-relative paths" and treat `unused_allow>0` as the mismatch signal (it already is) |
| D4 | low (fails safe) | a capture quoting a documentation example is refused; a clean run overstates what was proven | f01/f02/f10/f11/f14 + `checksum-sweep.txt` | one allowlist row for the published example (verified working, `allowlist-repro.sh` (b)); one docstring sentence "the checksum is documented but not verified"; fix the sibling sentence at line 281 |
| D5 | informational | stateless branch matches a prefix of a longer dotted value (widening, cannot hide a token) and K8 has no clause for it, so the frozen statement's "three dot-separated segments" is under-pinned | f04, f05, f12; corroborated by the sibling's Claim 3 "K-4seg" note | one K8 negative (4-segment dotted value) and one docstring word (`(?![.…])`) next round — no claim risk either way |

## 5. What does not change

- K1–K8 are unaffected: D1/D2/D5 are misses *outside* the frozen statement's boundary rule (a letter or
  digit precedes the token, so the statement does not require a hit), and D3/D4 are outside the counter's
  reach. C2's coverage score is not re-scored by this seat.
- The frozen github clauses are implemented faithfully. Independently reproduced by this seat, form by form: prose (d16),
  JSON value (d11, d18), JSON-joined (d12, d13), line start (d15, d20), stateless (d17, d18); and the negatives the docstring names — bare prefix (f06), `ghs_APPID_JWT` placeholder (f07),
  35/37 tails (docstring selftest), upper-case prefix, unknown prefix, letter-prefixed, short JWT
  segments, `github_pat_` (b16) — plus capture-scope-only (`corpus/knowledge` is not scanned, by design).
- The lane contains **zero** 40-character token-shaped literals at the landing rev
  (`git grep -l -E 'gh[pousr]_[A-Za-z0-9]{36}' 58c0c11 -- .` → 0 files; 149 files mention a bare prefix in
  prose). K3's `hits=0` is consistency by absence, not an allowlist effect (`allowed=0` in the same run).

## Reproduction

```bash
S=$(mktemp -d -p /fast/scratch/hyaku/kasegi-r92/SentinelGitHub); cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
bash .ufo/waves/round-92/w1/SentinelGitHub-receipts/repro.sh           "$PWD" "$S"   # 11 bypass + 2 control + 3 FP
bash .ufo/waves/round-92/w1/SentinelGitHub-receipts/allowlist-repro.sh "$PWD" "$S"   # D3 (c)/(d) and D4's row
rm -rf -- "$S"
```

Both scripts extract the three instrument files from `58c0c11` (read-only `git show`), build every fixture
under `$S`, print only `HIT`/summary lines, and delete their own directories. Neither contains a
credential-shaped literal: the prefix is assembled from parts and each 36-character tail is generated at
run time. The checksum sweep is the script appended to `checksum-sweep.txt` (it prints counts, never a
value). The D1 patch check is `patch-verification.txt` (the one changed line plus the flip list).

Files written by this seat:

- `.ufo/waves/round-92/w1/SentinelGitHub.md` (this report)
- `.ufo/waves/round-92/w1/SentinelGitHub-receipts/probe-encodings.tsv` (69 measured fixtures, digests only)
- `.ufo/waves/round-92/w1/SentinelGitHub-receipts/repro.sh`
- `.ufo/waves/round-92/w1/SentinelGitHub-receipts/allowlist-repro.sh`
- `.ufo/waves/round-92/w1/SentinelGitHub-receipts/patch-verification.txt`
- `.ufo/waves/round-92/w1/SentinelGitHub-receipts/checksum-sweep.txt`
- `.ufo/waves/round-92/w1/SentinelGitHub-receipts/scope-and-siblings.txt`
- `.ufo/waves/round-92/w1/SentinelGitHub-receipts/instrument-digests.txt`

No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r92/SentinelGitHub` deleted before
yield (`trap 'rm -rf -- "$S"' EXIT`); every fixture, planted repository and probe script lived there and
is gone. Nothing was written to the lane outside this wave dir; every git use was read-only.
