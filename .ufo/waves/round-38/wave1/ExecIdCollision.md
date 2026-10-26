# ExecIdCollision — assimilation id-collision guard + proof (round 38, wave 1)

Seat: executor, leaf. Axis: coverage. Item: run the assimilation id-collision guard and its
proof; write `reg-ids`, `staged-ids`, `collisions`; report counts and the staged-`S055` verdict.

Inputs (read-only):
- Lane registry `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` at lane HEAD
  `700153593eb586c70a6499c8ca225ee4d673bc9b` (registry 54 rows, identical to base
  `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`: `git diff --name-only a173b0c2 HEAD` touches only
  `.ufo/waves/round-38/**`, and both blobs read 54 ids under the guard extractor).
- Staged package `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`
  (`sha256 4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`, 100 lines, 89718 bytes).
- Scratch `S=/fast/scratch/hyaku/kasegi-r38/ExecIdCollision` with `TMPDIR=$S`; every work file and
  output lived there; no file written outside it except the three deliverables + this receipt.

## 1. Proof — the 0–3-space extractor is load-bearing

Fixture (scratch, `cat -A`):

```
== proof-registry.md ==
| S001 | x |$
  | S002 | y |$
== proof-staged.md ==
| S002 | y |$
```

Extractor A (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`) applied to both sides, then
`grep -oE 'S[0-9]+' | sort` and `comm -12`:

```
A reg=[S001 S002 ] staged=[S002 ] collisions=[S002 ] count=1
```

Extractor B (column-zero only, `grep -oE '^\|[[:space:]]*S[0-9]{3,}'`) on the same bytes:

```
B reg=[S001 ] staged=[S002 ] collisions=[] count=0
```

So the indented row `  | S002 | x |` is caught by A (`collisions=S002`) and **missed** by the
column-zero-only pattern (`collisions` empty). Indent sweep on a single-row fixture
(`printf '%*s| S099 | z |\n'`):

```
indent=1 A_match=1
indent=2 A_match=1
indent=3 A_match=1
indent=4 A_match=0
indent=5 A_match=0
```

The guard's tolerance is exactly 0–3 leading spaces; 4+ spaces is a measured blind spot (see §6).

## 2. Real rerun — exact commands

```
S=/home/vgpnk/Projects/shokuknow
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kasegi/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

Output:

```
reg-ids lines=54 first=S001 last=S054 unique=54
staged-ids lines=94 first=S031 last=S124 unique=94
collisions lines=24
collision range: S031..S054
collision list: S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054
sha256:
ea4dfaaa459dcb0ba8a648a11896a166a101b39a970b667cae02fc867c385047  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
3f3799a4d918288c122c7c0c062b7d1aa4ee6acb44a412637a1540309d64c492  collisions
```

Cross-check on alternate count bases at this head (both agree, so nothing is hidden by tolerance):

```
claim-form registry count (^|...): 54
claim-form staged count   (^|...): 94
column-zero variant: reg=54 staged=94 collisions=24 sha=3f3799a4d918288c
0-3 vs column-0 collisions identical on real inputs
4+space-indent S rows in SOURCES.md = 0
4+space-indent S rows in SOURCES.append.md = 0
```

Round-37 prediction, confirmed. `corpus/lessons/round-37.md:248-249`: "23 at `b362068`
(registry 53, no `S054`). Once the round's `S054` row lands the registry is 54 and the same guard
reports **24** (`S031–S054`)". Measured at registry 54: **24, S031–S054**, exactly as predicted.
`staged-ids` sha256 `550a0129…6948019f` is the same value recorded for r31
(`corpus/lessons/round-31.md:40`) and r34 (`corpus/lessons/round-34.md:182`) — the staged package
is byte-stable across those rounds, so this count's only moving part is the lane registry (54).

## 3. Staged `S055` verdict

- Staged `S055` (line 31 of `SOURCES.append.md`):
  `| S055 | 脆弱性情報ハンドリングポリシー — https://cybozu.co.jp/company/security-policy/ | docs | A | ...`
  (Cybozu's own vulnerability-handling policy; status `mined`, opened `2026-10-23`).
- Round-38 `S055` is OASIS CSAF v2.0,
  `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`.
- **Yes, different documents by URL**: `cybozu.co.jp/company/security-policy/` ≠
  `docs.oasis-open.org/csaf/v2.0/os/csaf-v2.0-os.html`.
- Registry `S055` is **absent** at this head: `grep -cE '^ {0,3}\|[[:space:]]*S055[[:space:]]*\|'
  corpus/SOURCES.md` → `0` (registry ends at `S054`). The collision is therefore prospective: the
  moment C2 lands `S055` = CSAF, staged `S055` collides with it.
- Independent second collision: staged `S055`'s document is **already registered at lane `S036`**
  (` 脆弱性情報ハンドリングポリシー (サイボウズ) — https://cybozu.co.jp/company/security-policy/`).
  Adopting staged `S055` would duplicate an existing document under a second id, and reuse the id
  C2 needs.
- The CSAF document has **no** staged counterpart: `grep -c
  'docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html' SOURCES.append.md` → `0`; any
  `oasis-open|csaf` text in the staged file → `0` rows. Quarantine slice verdict: **nothing to
  adopt**; staged `S055` is a duplicate-by-document of `S036` and an id collision with the incoming
  CSAF row — reject, do not renumber into `S055`.

## 4. Collision-set composition (by document, not by number)

Per-id URL comparison of the 24 colliding rows:

```
colliding ids: 24
same-document collisions (URL equal): 1   (S042 = ipa.go.jp/security/todokede/vuln/process.html)
different-document collisions: 23
```

Representative pairs (registry URL | staged URL):

```
S031 cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | hackerone.com/security/policy_versions
S032 nvlpubs.nist.gov/.../nistspecialpublication800-115.pdf | raw.githubusercontent.com/bugcrowd/.../README.md
S036 cybozu.co.jp/company/security-policy/ | security.bilibili.com/static/docs/BILISRC_V1.7.pdf
S049 zc.cnvd.org.cn/news/helpList | ipa.go.jp/.../000095610.pdf
S054 certcc.github.io/SSVC/tutorials/ssvc_overview/ | ipa.go.jp/.../request_to_ipa.pdf
```

The staged file is a differently-numbered package series (`S031–S124`), not a series aligned to lane
ids; adoption must be by document. Duplicate-document census across all 94 staged rows: **21** carry
a URL already in the registry, and **9 of those sit above `S054`** — on ids that are *free*:

```
staged S031->S043  S032->S044  S033->S045  S034->S049  S035->S050  S039->S033  S040->S034
staged S041->S035  S042->S042  S043->S041  S049->S046  S050->S047  S055->S036  S056->S037
staged S057->S038  S060->S039  S064->S041  S068->S040  S076->S041  S080->S048  S123->S032
```

So a free id does not imply a new document; the id-collision guard alone cannot gate adoption, and
in this round it gates nothing that is adoptable.

## 5. Deliverables (byte-exact, beside this receipt)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `ExecIdCollision.reg-ids` | 54 | 270 | `ea4dfaaa459dcb0ba8a648a11896a166a101b39a970b667cae02fc867c385047` |
| `ExecIdCollision.staged-ids` | 94 | 470 | `550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f` |
| `ExecIdCollision.collisions` | 24 | 120 | `3f3799a4d918288c122c7c0c062b7d1aa4ee6acb44a412637a1540309d64c492` |

`cmp` against the scratch outputs → `IDENTICAL` for all three. Content is the raw pipeline output:
one `Snnn` token per line, newline-terminated, no headers.

## 6. Risks / limits (measured, not inferred)

- **4+ space indent blind spot.** The guard misses rows indented four or more spaces
  (`indent=4 A_match=0`). Neither real input has such a row today (0 rows in both files), so the
  count is unaffected at this head; a future packaged append that indents table rows inside a list
  would be invisible to all three artifacts. Flip condition: any `grep -cE '^ {4,}\|'` > 0 on the
  staged file.
- **The count is head-relative.** 24 is the registry-54 reading; it is not comparable with r31's 17
  (base-blob basis), r34's 21 (registry 51) or r37's 23 (registry 53). State the head with the
  number.
- **Id collisions are not document collisions.** 23 of 24 collide by id under different documents,
  1 (`S042`) is the same document under the same id; 9 duplicate documents sit on free ids. The
  guard answers "is this id taken", not "is this document new".
- Lane working tree after this seat: `git status --porcelain` shows only the pre-existing untracked
  `.ufo/waves/round-38/wave1.ready`, `wave1.ready.partial`, and `.ufo/waves/round-38/wave1/`
  (which now holds `ExecFenceWalk.sh`, `swarm-registry.json`, my three artifacts and this receipt).
  No tracked file touched, no git mutation run, no write outside the allowed paths.
- No tool installed or upgraded; no network fetch performed.

Scratch removed before yield: `rm -rf /fast/scratch/hyaku/kasegi-r38/ExecIdCollision`.
