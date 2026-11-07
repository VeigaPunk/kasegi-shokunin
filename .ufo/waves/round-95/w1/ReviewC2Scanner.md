# ReviewC2Scanner — round 95 attempt 1, C2 `capture-secret-scan` review (leaf seat)

Reviewed commit `38e7319f44a9fab2978b59ffd43faf207cf62b32` (C2 landing; parent
`53ec479d71d25cf5be052db794a548a5904564b8`, base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`,
freeze `347519f21524d2bc13eb6c91cf3550930a4265b3`) against the frozen C2 statement and the
seat's clause list. Read-only on the lane: no git/jj mutation, no subagent, no `ask`. Scratch
`/fast/scratch/hyaku/kasegi-r95/ReviewC2Scanner`, removed on exit; every command ran with
`TMPDIR` set to that directory.

## Verdict

**REQUEST-CHANGES** — one blocking defect inside the landed instrument (finding 1: the file's own
"Known limits" now states the opposite of what the file does, and the shape inventory omits both
new shapes). The frozen C2 predicate P1–P3 is independently re-derived and **holds**, so the claim
**STANDS on its predicate**; the finding is a routed defect against the change, not a re-score.

## Findings

### 1. BLOCKING (medium) — the landed file's "Known limits" is now false and the shape inventory omits both new shapes

Path and lines: `corpus/instruments/capture-secret-scan.py:120-129` (the "Known limits" paragraph),
specifically `:123-124`, which still reads "the JWT-form GitLab tokens (`glcbt-eyJ…`, `glsat-eyJ…`,
`gliamat-eyJ…`; S140 lines 430, 447, 464)" as **not detected**. The documented shape inventory
(`:28-119`) ends with `gitlab-deploy-token` (`:117-119`) and has no `github-refresh-token` or
`gitlab-jwt-token` paragraph, while the same file adds the patterns at `:191` (`_GH_REFRESH`),
`:196`, `:200-202`, `:207-208`. `awk` over lines 1–135 finds no occurrence of either new shape
name (receipt 14).

Command: `sed -n '110,134p' corpus/instruments/capture-secret-scan.py` and
`awk 'NR<=135 && /github-refresh-token|gitlab-jwt-token|JWT-form GitLab tokens/' …` (receipt 14);
the diff shows the change is pattern/selftest only, +23 lines, zero docstring lines (receipt 01).

Why blocking: the docstring is the instrument's operator contract, and every earlier shape was
documented there in the same style (`github-token` `:81`, `gitlab-runner-auth-token` `:111`,
`gitlab-deploy-token` `:117`). As landed, an analyst reading the file is told that the exact three
JWT forms the file now reports are out of scope — a detector whose published inventory contradicts
its behavior is not shippable on a verifiability axis. Fix: add the two shape paragraphs (S142/S143
for `ghr_` + 76; S140:430/447/464 for the grammar) and delete or rewrite the JWT clause of "Known
limits".

### 2. LOW (citation precision; routed qualifier — the statement is frozen and must not be re-worded)

The claim, the counter docstring (`.ufo/waves/round-95/c2/capability-check.py:3-5`), the SCORECARD
row (landing) and the round-95 knowledge entry (integration commit `43cc15e`) anchor the JWT family at "S140 lines 429, 446, 463". Those are the
`keywords = ["glcbt-"]` / `["glsat-"]` / `["gliamat-"]` lines; the grammar the statement asserts
(`eyJ` head, `{10,1000}`, `{10,1000}`, `{20,1000}`) is on lines **430/447/464** (receipt 13). The
docstring's own known-limits sentence cites 430/447/464 correctly. The predicate is unaffected.

### 3. LOW (divergence from the cited rule; fail-open at the upper bound)

`gitlab-jwt-token` adds a trailing `(?![A-Za-z0-9_-])` (`:208`) that S140's rule does not have
(`regex = '''\b(?:…)?glcbt-eyJ[0-9a-zA-Z_\-]{10,1000}\.eyJ…\.[0-9a-zA-Z_\-]{20,1000}'''`,
S140:430/447/464, receipt 13). Consequence: a value whose first or last segment runs past 1000
characters, or whose tail is immediately followed by `-`/`_`, is not reported at all — battery
cases `jwt-head-1001` and `jwt-tail-1001` both print `got=none` (receipt 07). The frozen statement
caps segments at 1000, so the predicate holds; if the boundary is kept, the over-long case belongs
in "Known limits".

### 4. INFO (caller, verified) — the intake gate inherits both shapes, untested by this wave

`corpus/instruments/capture-source.py:102-120` imports `patterns()`, `load_allow()` and
`scan_bytes()`, so a capture carrying either shape is now refused before its file is opened:
`GATE refresh refused=True shapes=['github-refresh-token']`, `GATE jwt refused=True
shapes=['gitlab-jwt-token']`, `GATE clean refused=False`; the gate's own selftest still passes
(receipt 12). Verification gap: no round-95 counter exercises the gate with the new shapes, and the
round-90 counter's G0 ("plant shapes == the scanner's pattern names at REV",
`.ufo/waves/round-90/c2/capability-check.py:18,161-163`, receipt 16) would report both as `extra`
if ever run at this revision.

### 5. INFO — one shape relabel, no silent loss

A 36-character classic `ghr_` value followed immediately by 40 alphanumerics is reported once, as
`github-refresh-token` (receipt 07, `classic+40-alnum`); a standalone 36-character `ghr_` stays
`github-token` (receipt 07, `classic-ghr-36`; selftest `gh-refresh-36-classic`).

## Clause-by-clause against the frozen statement

| clause | code | observed (receipt) |
|---|---|---|
| left boundary | `_GH_LB = _ESC_LB` (`:188-189`), `_GL_LB` (`:198`): a preceding letter/digit/`_` blocks; a non-identifier or an escape terminator allows | letter/digit/underscore before → none, `-` before → hit; `\u0020`, `\n`, `\t`, `%20`, `%2F`, `&#38;`, `&#x26;` before → hit; same for the JWT (07) |
| 76-character length | `_GH_REFRESH = ghr_[A-Za-z0-9]{76}(?![A-Za-z0-9_])` (`:191`) | 75 → none, 76 → hit, 77 → none (07) |
| right boundary | `(?![A-Za-z0-9_])` (`:191`) | `-` after → hit; `_` or alphanumeric after → none (07) |
| optional 1–20 instance prefix | `_GL_PREFIX = (?:[A-Za-z0-9]{1,20}-)?` on `glcbt`/`glsat`; `gliamat` bare (`:199`, `:202`) | 1-char and 20-char prefixes hit; a 21-char prefix still hits because the prefix is optional and a preceding `-` passes the left boundary — identical to S140's `\b…(?:prefix)?` (07) |
| `eyJ` head and 10/10/20 floors | head segment `[A-Za-z0-9_-]{10,1000}`, middle `.eyJ` + `{10,1000}`, tail `{20,1000}` (`:200-202`, `:207-208`) | 9-char head / 9-char middle / 19-char tail → none; 10/10/20 → hit; 1000 → hit; 1001 → none; `glcbt-abcdefghij` (no `eyJ`) → none; middle not starting `eyJ` → none (07) |
| escape contexts | the same six-alternative escape lookbehind on both families (`:188`, `:198`) | refresh: `\u0020`, `\n`, `\t`, `%20`, `%2F`, `&#38;`, `&#x26;` → hit; JWT: `\u0020`, `\n`, `%26`, `&#38;`, `&#x26;` → hit (07) |
| classic shapes preserved | `github-token` unchanged (`:193-195`); runner/deploy/pat unchanged | 36-char `ghr_`/`ghp_` → `github-token`; `ghs_<appid>_<jwt>` → `github-token`; base instrument reproduces every old shape in the battery's `base=` column, K4 `old_shapes_missing=none` (07, 11) |
| no cross-swallow | new shapes are separate entries | `glpat-` (including a `glpat-eyJ…` value), `glrt-`, `gldt-` report only their own shape; a `glcbt-` JWT reports only `gitlab-jwt-token`; adjacency cases report both shapes (08) |
| allowlist binds exact bytes | `load_allow` key `(path, shape, sha256(matched bytes))` (`:215-236`), row at `corpus/instruments/capture-secret-allow.tsv:24` | digest re-derived = `c7ad99a1…060d` = the row's third cell; placeholder occurs twice in the committed receipt and both are consumed by the one row (`allowed=2`); a different 76-char value at the same path is a hit; the same bytes at another path are a hit; one changed byte at the same path is a hit (09, 10) |
| no matched value printed | `report()` prints only `HIT shape= path= line=` plus the summary (`:303-317`); allowlist errors print the exception type only | planted value's fragment count in the hit output = 0; malformed row and refused (`aws-sts`) row both exit 2 with no value echoed (09) |

## Predicate re-derivation (re-derived here, not cited)

- **P1** — `.ufo/waves/round-95/c2/capability-check.py --lane . --rev 38e7319… --work <scratch>
  --instrument-sha256 66edd661… --gate-sha256 8b6f8493… --seed 4242` → K1–K6 all `ok`,
  `CAPABILITY-CHECK-RESULT pass rc=0`; K2 `scanned=2477 hits=0 allowed=26 unused_allow=0`
  (receipt 11).
- **P2** — landed `capture-secret-scan.py` sha256 = `66edd66143ec62f6e40c864817a97383916d7ff67e5ab384e130b65c44516707`
  = the frozen candidate; `claim-package-check.py` = `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`
  = the gate pin; the base instrument is `22ba32d1…` (receipt 02).
- **P3** — `git show --name-status 38e7319` lists exactly `SCORECARD.md`,
  `corpus/instruments/capture-secret-allow.tsv`, `corpus/instruments/capture-secret-scan.py`
  (receipt 03).
- selftest counter 101 → 115 (`SELFTEST-RESULT pass cases=115`; the printed `cases=` includes the
  8 scope checks and 3 allowlist checks; 14 new case tuples at `:437-452`) (receipts 04, 05).
- `--rev` scans: landing `2477 hits=0 allowed=26 unused_allow=0 rc=0`; integration HEAD
  `43cc15e` the same (receipts 06, 15).

## Residual risk and verification gaps

1. S140's example cells are structurally redacted, so no published `glcbt-`/`glsat-`/`gliamat-`
   example value exercises the matcher; the positives are the rule text (430/447/464), K3's
   synthetic plants, and the selftest strings.
2. There is no committed S141/S143 snapshot. The 76 length is re-derivable only through
   `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt:16`
   (`72:regex = "ghr_[0-9a-zA-Z]{76}"`) and the registry row S143 (`corpus/SOURCES.md:155`, at
   HEAD); the claim's "S141 line 72" names the superseded/rejected row for the same file.
3. Segments longer than 1000 characters fail open (finding 3).
4. The "1–20 prefix" bound is descriptive, not enforcing: a 21+-character prefix still matches via
   the optional-prefix branch — faithful to S140's `\b…(?:prefix)?`, worth stating in the prose.
5. The intake gate inherits both shapes with no round-95 gate plant (finding 4).
6. Out-of-scope observation: the allowlist's S139 `bearer` row quotes a bearer-shaped
   documentation example in its reason cell; `corpus/instruments/` is not capture-class, so the
   scanner never scans the allowlist itself. This seat's diff receipt reproduces that context line
   and it was redacted there to keep the receipt capture-clean (receipt 01 note; receipt 17
   self-scan is clean).

## Receipts

All under `.ufo/waves/round-95/w1/ReviewC2Scanner-receipts/`; every file starts with the exact
command and ends with its observed rc.

- `01-landing-diff.txt` — `git diff -U3 9ef0126 38e7319 -- corpus/instruments/capture-secret-scan.py corpus/instruments/capture-secret-allow.tsv SCORECARD.md` → rc=0, 76 diff lines (+1 redaction note).
- `02-sha-pins.txt` — `sha256sum` of the landed scanner/allow/gate and the frozen candidate/row files, plus `git show 9ef0126:<path> | sha256sum` for the gate and base scanner → rc=0, 13 lines.
- `03-landing-pathset.txt` — `git show --name-status --format='%H %P' 38e7319…` → rc=0, 3 changed paths.
- `04-selftest-landing.txt` — `python3 -B corpus/instruments/capture-secret-scan.py --selftest` → rc=0, `SELFTEST-RESULT pass cases=115`, 115 `SELFTEST` lines.
- `05-selftest-base.txt` — base-rev bytes from `git show 9ef0126:…` run with `--selftest` → rc=0, `cases=101`, 101 `SELFTEST` lines.
- `06-rev-scan-landing.txt` — `--lane . --rev 38e7319…` → rc=0, `scanned=2477 hits=0 files=0 allowed=26 unused_allow=0`.
- `07-clause-battery.txt` — 54 clause cases comparing the landing instrument and the base instrument → every case `ok`, `BATTERY pass`, rc=0, 57 lines.
- `08-cross-shape-battery.txt` — 5 adjacency/cross-swallow cases → `BATTERY2 pass`, rc=0, 8 lines.
- `09-allowlist-exact-bytes.txt` — six `--files` runs in a scratch tree at the row's exact relative path (exact bytes / different value / different path / one-byte change / malformed row / refused row) → rc=0,1,1,1,2,2 as expected; fragment-count leak check = 0.
- `10-allow-digest.txt` — `sha256(ghr_ + "1234567890abcdef"·4 + "123456789012")` = the row digest, `match True`; placeholder occurrences in the committed receipt = 2 → rc=0, 11 lines.
- `11-counter-4242.txt` — the C2 counter at the landing with the frozen pins, seed 4242 → K1–K6 ok, `CAPABILITY-CHECK-RESULT pass rc=0`.
- `12-gate-caller.txt` — `capture-source.intake_gate` on refresh/JWT/clean bytes and `capture-source.py --selftest` → refused/refused/not-refused, gate selftest pass, rc=0.
- `13-source-anchors.txt` — `grep -n` for the S140 anchors (`keywords` 429/446/463, `regex` 430/447/464), S142:169, and the round-94 receipt's line 72 → rc=0, 19 lines.
- `14-docstring-known-limits.txt` — `sed -n '110,134p'` and the docstring-region grep → the only hit is line 123's "JWT-form GitLab tokens"; no new shape name appears before line 135.
- `15-rev-scan-head.txt` — `--lane . --rev HEAD` (integration `43cc15e`) → rc=0, `hits=0 allowed=26 unused_allow=0`.
- `16-round90-g0-inventory.txt` — `sed -n '13,20p;158,165p' .ufo/waves/round-90/c2/capability-check.py` → G0 asserts plant-shape/pattern-name equality.
- `17-receipts-selfscan.txt` — the landing scanner over this seat's 17 receipts → rc=0, `hits=0 files=0`.
- `18-report-selfscan.txt` — the landing scanner over this report plus every receipt → see the file; the report contains pattern literals and fixture names only, no matched value.
