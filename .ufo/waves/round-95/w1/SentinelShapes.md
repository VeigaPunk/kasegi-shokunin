# SentinelShapes — kasegi round 95, attempt 1, wave w1

Seat: adversarial pass on the two shapes landed at `38e7319f44a9fab2978b59ffd43faf207cf62b32`
(`github-refresh-token`, `gitlab-jwt-token`) and on the round's own secret hygiene.
Read-only seat: nothing in the lane was edited; this report and its receipts are the only writes.
Every value below that matches a shape is written as `<redacted>`; the receipts were sanitised
after capture and re-scanned clean (receipt 28).

## Verdict

**C2 STANDS.** I re-derived P1, P2 and P3 myself at `38e7319` and every clause of the frozen
statement holds: `github-refresh-token` fires on `ghr_` + exactly 76 `[A-Za-z0-9]` right-bounded
by `(?![A-Za-z0-9_])`, `gitlab-jwt-token` fires on the `glcbt-`/`glsat-`/`gliamat-` `eyJ`
three-segment forms with the S140 quantifiers, the classic 36-character shape still fires, the
selftest is 101 (base) -> 115 (landing), and the one allowlist row is digest-bound to the
round-94 receipt's published placeholder (digest recomputed on the exact matched bytes at both
occurrences). No MUST-FIX exists: **0 of the findings below re-score C2.** Eight findings are
routed — the highest-value one is R1, a shipped docstring that still tells the reader the two
classes are *not* detected.

C1 is outside this seat's surface; I only ran the hygiene grep over its landing (`53ec479`),
which printed no credential value.

## What I re-derived (not re-read)

| Limb | Observed | Receipt |
|---|---|---|
| selftest at landing | `SELFTEST-RESULT pass cases=115`, rc 0; base instrument `cases=101`, rc 0 | 26, 10 |
| P1 at `38e7319` | `CAPABILITY-CHECK-RESULT pass rc=0`; K1-K6 ok | 27, 19, 20 |
| P1 seeds | three independent runs, printed run-time seeds `1960155765`, `20261107`, `1` — K3 hits=6 missing=none extra=none each time | 27, 19, 20 |
| P2 pins | instrument sha256 = `66edd661…67e5`, gate = `8b6f8493…c8e6` at the landing; landed file byte-identical to `c2/candidate-scanner.py` | 26, 08 |
| P3 path set | exactly `SCORECARD.md`, `corpus/instruments/capture-secret-allow.tsv`, `corpus/instruments/capture-secret-scan.py` | 26 |
| allow row | `corpus/instruments/capture-secret-allow.tsv:27`; matched bytes hash to `c7ad99a1…060d` at receipt lines 10 **and** 26 (2 matches, one row, both allowed) | 02, 21 |
| clean at landing | `scanned=2477 hits=0 allowed=26 unused_allow=0 rc=0` | 26 |
| row is load-bearing | landed instrument + **base** allowlist at base rev `9ef0126`: `hits=1` (`github-refresh-token` at the round-94 receipt line 10), `allowed=24`, rc=1; with the landed allowlist: `hits=0 allowed=26` | 21 |
| no new false positive on the old corpus | base instrument at landing rev: `hits=0 allowed=24 rc=0` — the shapes add exactly one new hit class in the pre-existing tree, and the row covers it | 21 |
| do-nothing control | reproduces: base instrument fails K1 (`cases=101`), K3 (`hits=0`, six missing plants) and K5 | `controls/c2-controls-r95.txt` |

## MUST-FIX

**None.** Each candidate I tried to promote to MUST-FIX failed to contradict a frozen clause:

- *"reports for `ghr_` + exactly 76 base62"* — fires at start of buffer, after `=`, after
  `%26`/`\u0026`, in a JSON value, inside prose, at EOF without newline (probe FN1/FN2/FN3/FN4/FN14).
  The 75- and 77-character neighbours do not fire (selftest `gh-refresh-75`/`-77`).
- *"every earlier shape still fires"* — the landing diff has **23 insertions, 0 deletions** in
  the instrument, so no case or pattern was removed; `gh-refresh-36-classic` still reports
  `github-token`; K6 still reports `aws-sts-session-token` at the round-86 freeze.
- *"selftest 101 -> 115"* — both halves measured, not quoted.
- *"one digest-bound allowlist row"* — digest recomputed from the bytes the regex matches, at
  both occurrences, and the row is provably needed (receipt 21) and provably sufficient.

## Routed findings

### R1 (routed, highest value) — the shipped docstring states the opposite of the code

`corpus/instruments/capture-secret-scan.py:120-127` (the `Known limits:` paragraph) still lists
"the JWT-form GitLab tokens (`glcbt-eyJ…`, `glsat-eyJ…`, `gliamat-eyJ…`; S140 lines 430, 447,
464)" among the things that "are not detected" — at line 123, in the landed file, while lines
196 and 207 implement exactly those shapes. The `Shapes.` block (`:23-119`) also has no entry for
either new class: it ends at `gitlab-deploy-token (round 94)` on line 117 and never mentions
S142 or S141 (grep for `S141|S142` in the file returns no hit inside `:1-119`). So the class's
own contract text says the class is absent, and the docstring's source list is stale.
Consequence: the next round that audits "known limits" or reads this file to decide what the
instrument does will conclude both shapes are missing. Not a predicate clause — routed.
Smallest remediation: delete the three JWT forms from `Known limits` and add two `Shapes.`
entries with the S142/S141/S140 citations the selftest comment already carries.

### R2 (routed) — the allowlist row covers the receipt, not the report that carries the same value

The placeholder value the row binds appears twice in
`.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt` (lines 10,
26 — allowlisted) **and** twice in `.ufo/waves/round-94/w1/ScoutGitLabRules.md` (lines 133, 145 —
not allowlisted). `is_capture_path` (`:245`) returns False for the `.md`, so `--rev` never sees
it, but `--files` on that report reports `HIT shape=github-refresh-token … line=133` plus
`github-token` at line 174, rc=1 (receipt 24). The scanner's documented workflow is "run
`--files` on every capture before the commit that first adds it", so a seat that follows the
workflow on that report gets a red result no allowlist row can clear. Routed: the frozen
predicate scans the rev, where this file is out of scope. Smallest remediation: redact the
value in the `.md`, or add a second digest-bound row for that path.

### R3 (routed) — round-95 wave receipts print shape-complete fixtures into capture-class dirs

`find .ufo/waves/round-95 -type f` piped through the landed instrument: `scanned=65 hits=21
files=7` (receipt 17). The new hits are in the peer seat's fixture dumps
`w1/ConnectorOverlap-receipts/grep-{ghr,glcbt,glsat,gliamat}.txt`, which are `-receipts` paths
and therefore capture-class; each prints an 80-character `ghr_` string (receipt 05 measures
len=80 at lines 4, 129, 130, 135, 137, 194, 319-327) and complete `glcbt-eyJ…`/`glsat-eyJ…`/
`gliamat-eyJ…` fixtures. The same files already hit the **base** instrument (`credential`,
`gitlab-pat`: `hits=4 files=2`, receipt 16), so the two new shapes raise flagged shapes per file
from 2 to 4 on a pre-existing pattern — this is not a C2 regression. All fixtures are synthetic:
distinct-character counts 3-9 across every `ghr_`/`eyJ` body measured (receipt 23), i.e. the
`aB3`-repeat and `1234567890abcdef`-repeat placeholders and `x/y/z` JWT bodies. Hygiene verdict:
**no live credential is printed anywhere in the round-95 wave dirs or in either landing diff**
(receipts 03, 17, 23). But if these receipts are committed as-is, `capture-secret-scan --rev`
at the next tip exits 1 with no allow rows. Smallest remediation: truncate the printed tails
(`ghr_<redacted>`), which is what this seat did to its own receipts.

### R4 (routed) — the cited 76-length source S141 has no snapshot in the lane

The statement and `c2/capability-check.py` cite "S141 line 72" for the 76-character length.
`git ls-tree -r 38e7319 | grep -c S141` = **0**, and `git log --all -- 'corpus/source-snapshots/**/S141*'`
is empty (receipts 11, 13). The rule text is only reachable through two receipts: the round-94
capture `ScoutGitLabRules-receipts/08-github-rules-file.txt` (its grep shows the rule at line 72)
and a round-95 peer receipt (`w1/CriticClaimsC2-receipts/11-s141-capture.txt`). The tier-A ground
for the length is the round-94 receipt 06 itself — GitHub's own OpenAPI example, measured
`tail= 76` — which is the very file the allow row points at, so the length is locally supported
even though the *cited* path is not. Also worth naming: the seat spec describes S141 as "GitLab's
rules file" while round-94 records it as `rules/mit/github/github.toml` (a GitHub rules file,
tier B, rejected as ground for a GitLab-vendor row). Routed provenance nit; the predicate does
not test sources.

### R5 (routed) — the statement omits both boundary rules, one of which is inert

The statement names no left boundary for `ghr_` and no right boundary for the GitLab shape; the
code has both (left: not preceded by `[A-Za-z0-9_]` or after an escape terminator; right:
`(?![A-Za-z0-9_-])`). Both are *stricter* than the statement, so neither can produce a claimed
match that fails. In practice the GitLab right boundary is **inert**: the third segment class is
`[A-Za-z0-9_-]{20,1000}`, which greedily consumes the very characters the lookahead excludes, so
appending `-1` or `_x` to a token just lengthens the tail (spans 0-86 with tail `zzzz-1` /
`zzzz_x`, receipt 14) and the lookahead can only bite on a >1000-character run, where the segment
bound fails first. Verified against S140: no case exists in which S140's regex matches and the
landed regex does not, for the right edge. Routed qualifier for the statement's precision, or an
argument to drop the dead lookahead.

### R6 (routed) — false negatives found, all consistent with the sources or the documented limits

Probe receipt 01 (spans) and 13:
- base64-wrapped `ghr_`: **missed** (`FN5`). This is the documented known limit ("gzip/UTF-16/base64-wrapped captures are not detected"); after a decode step the shape fires.
- `_glcbt-eyJ…` underscore prefix: **missed** (`FN7`). S140:430's own prefix class is `[a-zA-Z0-9]{1,20}-`, so an underscore prefix is not a documented form; `-glcbt-…` and a 21+ alphanumeric prefix still match (`FN11`, span starts at `glcbt` after the hyphen).
- `GLCBT-EYJ…` uppercase: **missed** (`FN8`, `FN9`). S140's literal is lower-case `glcbt-eyJ` too.
- `ghr_` + 77: **no match at all** (`FN12`), not a partial match. Exact-length shapes are brittle to a provider length change; the classic 36 shape has the same property and the selftest pins it.
- 4-segment JWT: **matches** the first three segments (span 0-84, `FN10`) — not a miss.
- JSON escape *inside* a token (`ghr_` + 75 + `\u0041`): missed (`FN6`), but the sequence is a 75-character tail, not a token.
- 1001-character head segment: missed (`FN15`), identical to S140's `{10,1000}` bound.

### R7 (routed) — false positives found, all shape-inherent or already covered

Probe receipt 01:
- `ghr_` inside a word (`xghr_` + 76): **no match** (`FP1`) — the left boundary holds.
- 76 `X` or 76 hex characters after `ghr_`: **match** (`FP2`, `FP3`, `FP10`). A doc placeholder is indistinguishable from a token by shape alone; the only remedy in this design is an allowlist row. The one real instance in the tree is the round-94 receipt's GitHub OpenAPI example, which is what row 27 binds.
- a trailing `-tail` after a 76-character tail: matches (`FP4`) — again the tail class absorbs it.
- JWT prose: `<header>`/`<payload>` placeholders (`FP6`), S140's own regex source line (`FP7`), S140's structural redaction lines (`FP8`), and a bare `eyJ…` JWT with no prefix (`FP12`) all **miss** — so the class does not fire on its own documentation.
- `instance-1-glsat-…` matches (`FP11`), and `acme12345678901234-gliamat-…` matches (`FN13`) — intended prefix behaviour, and `gliamat-` alone matches with no prefix, matching S140:464's prefix-less regex.

### R8 (routed) — the intake gate inherits the two shapes, with no pre-authorable escape

`corpus/instruments/capture-source.py:120` calls `scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow)`,
so both new shapes reach `capture-intake-gate` automatically (that is the design — the SCORECARD
row 308 says the two "never drift"). Consequence: a capture of any page that prints a 76-character
`ghr_` placeholder is now refused at intake (exit 3) **before** the destination path exists, so
the allowlist row cannot be authored in advance. Fail-closed is the intended direction and S142
itself is clean (`hits=0` at the landing), but the operational cost is a blocked capture with no
documented escape path for this class. Routed; suggested note in the class's known limits rather
than a code change.

## Receipts

Directory: `.ufo/waves/round-95/w1/SentinelShapes-receipts/` (29 files, all sanitised, re-scanned
with the landed instrument: `scanned=29 hits=0 files=0 rc=0`, receipt 28; this report itself
scans `scanned=1 hits=0`).

| # | Command | Observed |
|---|---|---|
| 26 | `python3 -B corpus/instruments/capture-secret-scan.py --selftest` / `--lane "$PWD" --rev 38e7319…` / `git show --name-only 38e7319` / `git show 38e7319:<file> \| sha256sum` | rc 0, `cases=115`; rc 0, `scanned=2477 hits=0 allowed=26 unused_allow=0`; 3 paths; both sha pins equal |
| 27 | `python3 -B .ufo/waves/round-95/c2/capability-check.py --lane "$PWD" --rev 38e7319… --work … --instrument-sha256 66edd661… --gate-sha256 8b6f8493…` | rc 0, `CAPABILITY-CHECK-RESULT pass`, seed `1960155765`, K1-K6 ok |
| 19 | same, `--seed 20261107` | rc 0, all limbs ok |
| 20 | same, `--seed 1` | rc 0, all limbs ok |
| 10 | base instrument at `9ef0126` `--selftest` (extracted with its gate + allowlist) | `SELFTEST-RESULT pass cases=101` |
| 08 | `git show 38e7319:… \| sha256sum` vs `c2/candidate-scanner.py`; base selftest attempt | landed == candidate == working file `66edd661…`; the first base-selftest attempt returned rc=2 (`FileNotFoundError`, copy lacked its sibling gate) — corrected run is receipt 10 |
| 21 | landed instrument at base rev with base allowlist; base instrument at landing rev; landed instrument/allowlist at base rev | 1 hit / allowed=24 / rc=1; 0 hits / allowed=24; 0 hits / allowed=26 |
| 02 | regex the row's shape over `06-github-firstparty-examples.txt` at `38e7319` | 2 matches, both `c7ad99a1…060d`, len 80 |
| 01 | probe script (probe.py, also receipt 00) over 30 crafted strings | FP1-12 / FN1-15 spans as summarised in R5-R7 |
| 13, 14 | S141 presence; trailing `-`/`_` boundary spans | 0 tracked S141 paths; `+hyphen` span 0-86 tail `zzzz-1`; `+underscore` span 0-86 tail `zzzz_x` |
| 24 | `--files .ufo/waves/round-94/w1/ScoutGitLabRules.md`; `--rev 38e7319…`; `is_capture_path` verdicts | rc 1, `github-refresh-token` line 133 + `github-token` line 174; rc 0 at the rev; `False` for the `.md`, `True` for both `-receipts` paths |
| 17 | `find .ufo/waves/round-95 -type f ! -name '*.pyc' \| xargs … --files` | `scanned=65 hits=21 files=7 rc=1` |
| 16 | base instrument `--files` on two peer receipts | `hits=4 files=2` (`credential`, `gitlab-pat`) |
| 23 | alphabet statistics over the printed fixtures | `ghr_` bodies 3-4 distinct chars; `eyJ` bodies 6-9 — synthetic |
| 03 | `git show 38e7319 \| grep -E 'ghr_[A-Za-z0-9]{10,}\|(glcbt\|glsat\|gliamat)-eyJ'`; same on `53ec479` | only selftest source lines; rc 1 on the C1 landing (no token text) |
| 04 | tree-wide `ghr_[A-Za-z0-9]{20,}` and `(glcbt\|glsat\|gliamat)-eyJ` occurrences | 6 files, all wave receipts / one round-94 report / the instrument's selftest |
| 05 | per-line token lengths in the round-95 peer receipt | `len=80` at the listed lines |
| 25 | docstring anchors: `grep -n 'Known limits\|glcbt-eyJ…\|github-refresh-token\|gitlab-jwt-token\|Shapes\.'` | `Shapes.` 23, last entry 117, `Known limits` 120, JWT forms 123; class names only at 196/207/439+ |
| 07 | S142:160-176, S140:425-470 numbered | S142:169 "The token starts with ghr_."; S140:429/446/463 keyword lines, 430/447/464 regexes, examples redacted |
| 09, 15 | S141 lookup; peer S141 capture receipt | S141 not in `corpus/source-snapshots/round-94|round-95`; rule text reachable only via receipts |
| 22 | `git show 38e7319:SCORECARD.md \| sed -n '307p'`; `capture-source.py` import lines | row names both shapes, last cell `87`; intake gate imports `scan.patterns()` at line 120 |
| 12 | round-94 receipt 06 excerpt | `total= 80 tail= 76` measured by that seat; GitHub OpenAPI example |
| 18 | SCORECARD row grep | exactly one `capture-secret-scan` row, `87`, both shapes; no literal token |
| 28 | `find …/SentinelShapes-receipts -type f \| xargs … --files`; `--files …/SentinelShapes.md`; `git status --porcelain` | `scanned=29 hits=0 rc=0`; `scanned=1 hits=0 rc=0`; only the two seat paths untracked |

Note on receipt 08: it records a failed first attempt (`rc=2`, `FileNotFoundError`) beside the
successful identity check; receipt 10 is the corrected base-selftest run. Nothing else failed.
