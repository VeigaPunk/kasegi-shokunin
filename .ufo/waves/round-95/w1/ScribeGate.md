# ScribeGate — round 95, wave w1 (kasegi)

Seat: `ScribeGate-2` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round-95 base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`; freeze `347519f21524d2bc13eb6c91cf3550930a4265b3`;
C1 landing `53ec479d71d25cf5be052db794a548a5904564b8`; C2 landing `38e7319f44a9fab2978b59ffd43faf207cf62b32`.

**Coordination.** The L1 (`KasegiR95`) wrote and committed both target files at `43cc15e8`
(`corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md`, `corpus/lessons/round-95.md`) and,
while this seat was reading them, instructed that the committed bytes are canonical and that this seat
must **not** edit the two corpus files. This report therefore verifies those bytes and proposes
old → new patches; this seat wrote only this report and `ScribeGate-receipts/`.

**Bytes verified.** Entry at `43cc15e`: sha256 `b493d5bb0d2522b241e88bb248aaa4d113b17687092ff2ed3c1c40941b5b68c4`
(98 lines). Working tree: sha256 `4f81dfcfd44f77a70f96e8e6fe062f1b09ddddf559cc7cd6a2717e9b45865c95`, 98 lines — the
committed bytes plus an uncommitted citation-shaped fix on lines 15, 18 and 43 (full-path anchors). Line
numbers below are the working tree; they are identical to `43cc15e` because that fix did not add or remove
lines. Lesson: `31d3e28aae6c7dce14a1f62de12e9810b4086a389047f19dac0649a4efe101cf`, 50 lines, identical at
`43cc15e` and in the working tree.

## Verdict

**ANCHORS AGREE** — 39/39 anchor assertions byte-exact, `bad=0` (13 capture/receipt anchors + 26
instrument/case anchors). The proposed correction keeps 39/39 `bad=0` and adds all seven
brief-mandated scanner regex strings (`missing=0`).

**ENTRY DRAFT NOT READY AS WRITTEN** — 14 defects (3 high, 7 medium, 4 low). The high ones are a
non-executable `recheck:` line (all 104 `corpus/knowledge/*.md` entries carry a `recheck:` line, so
this broken line is inside the audited set; `bash -n` rc 2), the missing exact
scanner regex (the GitLab block is elided and the frozen `429/446/463` lines are mislabelled as the
grammar), and a false base64 claim. Full replacement: `ScribeGate-receipts/proposed-entry.md`; unified
diff: `ScribeGate-receipts/18-proposed-diff.txt` (191 lines).

**LESSON DRAFT NOT READY AS WRITTEN** — 5 defects (1 high, 2 medium, 2 low): two paraphrases that are
not observed lines (`11/12`, `15/15`), one wrong limb citation (`old_not_once` vs the observed
`dup_rows=1`), a table missing the round-94 `#`/column shape, and a missing `author:` line plus two
precision items. Full replacement: `ScribeGate-receipts/proposed-lesson.md`; diff:
`ScribeGate-receipts/20-proposed-lesson-diff.txt` (81 lines).

**NO C1/C2 CLAIM VERDICT ISSUED.** Their frozen predicates are for the wave's critics and executors.
This seat re-derived the instrument's behaviour (selftest 115 + 24 synthetic boundary probes), the
capture bytes, the registry counts and the executed-control lines — not the C1 meter or the C2
capability gate.

## What was re-derived (behaviour)

| Check | Observed | Receipt |
|---|---|---|
| S142 line 169 contains `The token starts with ghr_.` | exact; line is `refresh_tokenstringThe refresh token. … The token starts with ghr_.` | `02-capture-lines.txt` |
| S140 lines 429/446/463 | exactly `keywords = ["glcbt-"]`, `["glsat-"]`, `["gliamat-"]` | `02-capture-lines.txt` |
| S140 lines 430/447/464 | exactly the three vendor regexes (shown byte-for-byte in the receipt) | `02-capture-lines.txt` |
| S141 line 72 | `72:regex = "ghr_[0-9a-zA-Z]{76}"` at the committed receipt line 16; raw file 130 lines / 3,955 bytes / sha256 `02c67ceb…` (raw capture **not** committed — known limit) | `02-capture-lines.txt` |
| Scanner `--selftest` | `SELFTEST-RESULT pass cases=115`; 14 round-95 cases at lines 439–452 | `04-selftest.txt` |
| Scanner `--files` on S142+S140 | `scanned=2 hits=0 files=0 allowed=0 unused_allow=24 rc=0` | `05-files-scan.txt` |
| 24 synthetic boundary probes | 76 hit / 75+77 miss; `xghr_` miss; `\n`,`\u0020`,`%20`,`&#32;`,`&#x20;` precede hits; 36-char `ghr_` → `github-token`; `glcbt`/`glsat`/`gliamat` positives; non-`eyJ`, 9-char first/second, 19-char third, letter-before, placeholder → none; 20-char third → hit; prefixed `acme-gliamat` → hit | `13-probes.txt` |
| base64 | `{"` → `eyI=`; `{"a` → `eyJh`; `{"alg"` → `eyJhbGci` | `13b-base64.txt` |
| vendor `\b` on `acme-gliamat` | match at offset 5 (the `gliamat` span); on `\u0020gliamat` → none | `13c-regex-diff.txt` |
| Registry | 141 rows at `9ef0126`; 143 rows in the working tree | `11-registry.txt` |
| Census | `kasegi ok` rc 0; 7 W04 (six inherited + S143) | `08-census.txt` |
| Entry anchorcheck (current) | 2 in-range cite instances, 2 distinct, 0 bad | `06-anchorcheck.txt` |
| Proposed entry anchorcheck | 33 in-range, 24 distinct, 0 bad | `17-proposed-anchorcheck.txt` |
| Current `recheck:` line | `bash -n` rc 2 (`syntax error near unexpected token '('`) | `07-recheck.txt` |
| Current second recheck command | `capture-secret-scan.py --rev master` rc 2 (`reason=usage`) | `15-rev-master.txt` |
| Proposed `recheck:` line | `bash -n` rc 0; run rc 0 | `07-recheck.txt` |

## Entry defects (old → new)

### D1 — HIGH — line 4: the `recheck:` line is not an executable command
`bash -n` rc 2; its second half uses an unsupported invocation (`--rev master` rc 2 usage). It is the only
broken `recheck:` line among the 104 `corpus/knowledge/*.md` entries (`grep -l '^recheck:'` = 104/104).
Old (line 4):
````
recheck: python3 -B corpus/instruments/capture-secret-scan.py --selftest | grep -E 'gh-refresh|gl-jwt' (14 cases) and `python3 -B corpus/instruments/capture-secret-scan.py --rev master`
````
New (one shell command; `bash -n` rc 0, run rc 0):
````
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/anchorcheck.py corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md && sed -n '169p' corpus/source-snapshots/round-95/S142.txt | grep -q 'The token starts with ghr_\.$' && sed -n '429p' corpus/source-snapshots/round-94/S140.txt | grep -qxF 'keywords = ["glcbt-"]' && sed -n '446p' corpus/source-snapshots/round-94/S140.txt | grep -qxF 'keywords = ["glsat-"]' && sed -n '463p' corpus/source-snapshots/round-94/S140.txt | grep -qxF 'keywords = ["gliamat-"]' && python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-95/S142.txt corpus/source-snapshots/round-94/S140.txt
````

### D2 — HIGH — lines 2 and 42–49: the exact scanner regex is absent; the GitLab block is elided and the frozen lines are mislabelled
The brief requires the exact regex the scanner now uses. The entry shows neither `_GH_REFRESH` /
`("github-refresh-token", …)` nor the GitLab `_GL_LB`/`_GJ_HEAD`/`("gitlab-jwt-token", …)` lines. Its
GitLab block elides two of the three vendor regexes with `…`, drops the leading `\b` and `'''`, and the
`source:` line calls lines `429, 446, 463` “the `eyJ` three-segment forms” — those lines are the
`keywords`; the grammar is on `430/447/464`.
Old (lines 42–49):
````
GitLab's rules file publishes three JWT-shaped tokens as one grammar
(S140, `corpus/source-snapshots/round-94/S140.txt:429`, `:446`, `:463`):

```
(?:[a-zA-Z0-9]{1,20}-)?glcbt-eyJ[0-9a-zA-Z_-]{10,1000}\.eyJ[0-9a-zA-Z_-]{10,1000}\.[0-9a-zA-Z_-]{20,1000}
(?:[a-zA-Z0-9]{1,20}-)?glsat-eyJ…  (same grammar)
gliamat-eyJ…                       (same grammar, no instance prefix)
```
````
New (full block in `proposed-entry.md` §GitLab JWT family):
````
GitLab's rules file publishes three JWT-shaped tokens as one grammar. The
`keywords` lines are at `corpus/source-snapshots/round-94/S140.txt:429`,
`corpus/source-snapshots/round-94/S140.txt:446` and
`corpus/source-snapshots/round-94/S140.txt:463`; the regexes are the next line
of each rule (`corpus/source-snapshots/round-94/S140.txt:430`,
`corpus/source-snapshots/round-94/S140.txt:447`,
`corpus/source-snapshots/round-94/S140.txt:464`):

regex = '''\b(?:[a-zA-Z0-9]{1,20}-)?glcbt-eyJ[0-9a-zA-Z_\-]{10,1000}\.eyJ[0-9a-zA-Z_\-]{10,1000}\.[0-9a-zA-Z_\-]{20,1000}'''
regex = '''\b(?:[a-zA-Z0-9]{1,20}-)?glsat-eyJ[0-9a-zA-Z_\-]{10,1000}\.eyJ[0-9a-zA-Z_\-]{10,1000}\.[0-9a-zA-Z_\-]{20,1000}'''
regex = '''\bgliamat-eyJ[0-9a-zA-Z_\-]{10,1000}\.eyJ[0-9a-zA-Z_\-]{10,1000}\.[0-9a-zA-Z_\-]{20,1000}'''

The lane's exact matcher (`corpus/instruments/capture-secret-scan.py:198-208`):
- `_GL_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\[ntr])|(?<=\\u[0-9A-Fa-f]{4})|(?<=%[0-9A-Fa-f]{2})|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))"` (`:198`)
- `_GL_PREFIX = rb"(?:[A-Za-z0-9]{1,20}-)?"` (`:199`)
- `_GJ_SEG = rb"[A-Za-z0-9_-]{10,1000}"` (`:200`)
- `_GJ_TAIL = rb"[A-Za-z0-9_-]{20,1000}"` (`:201`)
- `_GJ_HEAD = _GL_LB + rb"(?:" + _GL_PREFIX + rb"(?:glcbt|glsat)|gliamat)-eyJ" + _GJ_SEG` (`:202`)
- `("gitlab-jwt-token", re.compile(` (`:207`) and
  `_GJ_HEAD + rb"\.eyJ" + _GJ_SEG + rb"\." + _GJ_TAIL + rb"(?![A-Za-z0-9_-])")),` (`:208`)
````
Also add the GitHub pair under §GitHub refresh token:
````
The lane's exact matcher is (`corpus/instruments/capture-secret-scan.py:191`, `:196`):
- `_GH_REFRESH = rb"ghr_[A-Za-z0-9]{76}(?![A-Za-z0-9_])"`
- `("github-refresh-token", re.compile(_GH_LB + _GH_REFRESH)),`
````
and change the `source:` line's S140 clause to “lines 429/446/463 (the three prefix keywords) and
430/447/464 (the three regexes)”. Note: this is entry precision only; the frozen C2 claim's own
`429/446/463` pointer is not re-scored.

### D3 — HIGH — line 53: the base64 parenthetical is false
Old:
````
- The head is `eyJ` (base64 of `{"`), so a `glcbt-` string whose first segment
````
New:
````
- The head is `eyJ`, the first three base64url characters of a JWT header whose
  JSON opens `{"` (a decoding fact, not a vendor sentence: base64 of `{"` alone
  is `eyI=`; `{"a` is `eyJh`). A `glcbt-` string whose first segment does not
  start with `eyJ` is not a hit.
````
Evidence: `13b-base64.txt` (`{"` → `eyI=`, not `eyJ`).

### D4 — MEDIUM — lines 18–20: the measurement table is attributed to the wrong file
The `ghr total= 80 tail= 76` table is in the round-94 wave receipt, not “the same file” (the GitLab
rules file). Old:
````
records `ghr total= 80 tail= 76` (a round-94 wave receipt derived the same 76
from that file).
````
New:
````
measurement of that file prints `ghr total= 80 tail= 76`
(`.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt:10`;
the example value there is not reproduced here).
````

### D5 — MEDIUM — lines 57–60: “documented superset” is imprecise for a hyphen-prefixed `gliamat-`
The vendor `\b` also matches the `gliamat` span after a hyphen (vendor probe: match at offset 5); the
lane is a superset only for escape-joined contexts (`\u0020gliamat-…`, vendor `\b`: none). Old:
````
- `glcbt-` and `glsat-` accept a 1–20-character instance prefix (`acme-glcbt-…`);
  `gliamat-` carries no prefix in the vendor rule, and this lane's matcher
  reaches a prefixed `gliamat-` only through its left boundary, which is a
  documented superset, not a vendor claim.
````
New:
````
- `glcbt-` and `glsat-` accept a 1–20-character instance prefix (`acme-glcbt-…`);
  the vendor's `gliamat-` rule has no optional prefix. A string such as
  `acme-gliamat-…` is matched on the `gliamat-…` span, which the vendor's `\b`
  also matches after the hyphen; the lane's left boundary is a superset only
  for escape-joined contexts (`\u0020gliamat-…`), which the vendor `\b` refuses.
````

### D6 — MEDIUM — line 29: “all mutation-tested in round 95” is unsupported
No wave mutation-test receipt covers these boundary facts (the wave's mutation seats target the counters).
Old: `Boundary facts, all mutation-tested in round 95:`
New: `Boundary facts, pinned by the selftest cases at \`corpus/instruments/capture-secret-scan.py:439-443\` and by the lookbehind at \`:188\`:`
(the line is replaced as one sentence; the next line becomes the first bullet).

### D7 — MEDIUM — lines 69–71: “the vendor's own published examples” is false
The committed S140 example values are structurally redacted, and the selftest cases use synthetic values
/ a placeholder-shaped string. Old:
````
<signature>`. Both new shapes are therefore tested against the vendor's own
published examples and against documentation placeholders in the instrument's
selftest (cases `gh-refresh-*`, `gl-jwt-*`), which grew 101 → 115 cases in
round 95.
````
New:
````
<signature>`. Both new shapes are pinned by the instrument's selftest at
`corpus/instruments/capture-secret-scan.py:439-452` (cases `gh-refresh-*`,
`gl-jwt-*`), which grew 101 → 115 cases in round 95; the cases use synthetic
values and a placeholder-shaped string, not the vendor's redacted example
values.
````

### D8 — MEDIUM — lines 77–79: `<S141 capture>` is not a file; the checklist is not runnable
Old:
````
- `sed -n '72p' <S141 capture>` must print `regex = "ghr_[0-9a-zA-Z]{76}"` (the
  row records the file at commit 59ada1f4; the capture is not committed because
  the file lists published example values).
````
New:
````
- `sed -n '16p' .ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt`
  must print `72:regex = "ghr_[0-9a-zA-Z]{76}"` (the raw file is 130 lines /
  3,955 bytes / sha256 `02c67ceb…` and is not committed because it lists
  published example values).
````

### D9 — MEDIUM — lines 80–81: the `sed` prints the keyword lines, not “the rules”
Old:
````
- `sed -n '429p;446p;463p' corpus/source-snapshots/round-94/S140.txt` must print
  the three `glcbt-`/`glsat-`/`gliamat-` rules.
````
New:
````
- `sed -n '429p;446p;463p' corpus/source-snapshots/round-94/S140.txt` must print
  the three `keywords` lines; `sed -n '430p;447p;464p'` must print the three
  regexes (all six lines are quoted in the section above).
````

### D10 — MEDIUM — lines 85–86: the capability-check invocation is placeholders, not a command
`<scratch>`/`<sha>` cannot be run, and the gate wants a scratch `--work` dir the checklist does not
name. Replace the item with the committed landing record:
````
- the claim gate's own record is `.ufo/waves/round-95/l1/landing-r95.txt`
  (`CAPABILITY-CHECK-RESULT pass rc=0`, `CAPABILITY-CHECK-REV rev=38e7319f… seed=9191`).
````
The runnable shape checks are the selftest, `--files` and `anchorcheck` items above.

### D11 — LOW — lines 37–38: “A word ending in the letters” is vague
Old:
````
- A word ending in the letters is not a hit; the prefix must be preceded by a
  boundary and followed by exactly 76 token characters.
````
New:
````
- A longer identifier that merely ends in the prefix letters (`xghr_…`) is not
  a hit: the lookbehind refuses a preceding `[A-Za-z0-9_]`, and the prefix must
  be followed by exactly 76 token characters.
````

### D12 — LOW — line 91: the rejected claim attributes the length to S141, not S143
Old: ``states only the prefix. The length comes from S141's rule file; an entry that``
New: ``states only the prefix. The length comes from the S143 correction row (the`` / ``same file as S141, which S143 supersedes); an entry that``
(S141 stays `rejected`; S143 is the carrier — `corpus/SOURCES.md:155`.)

### D13 — LOW — lines 1 and 5: the `---` fences are a convention break
This is the only one of the 104 knowledge entries with `^---$` (`grep -l '^---$' corpus/knowledge/*.md`
→ 1). The proposed entry drops both fences; the three header lines stay as plain `source:` /
`verified-at:` / `recheck:` lines.

### D14 — LOW — line 25: “rounds 92” typo and no anchors for the classic family
Old: ``hit (S136/S137, rounds 92).``
New: ``hit (S136/S137 at `corpus/source-snapshots/round-92/S136.txt:161-167` and
`corpus/source-snapshots/round-92/S137.txt:156-162`, round 92).``

## Lesson defects (old → new)

### L1 — HIGH — line 49: “prints 11/12” is not an observed line
Old: ``round-94 `c1-controls-r94.py` ~line 145 `git clone -q --shared LANE`; the r94 spot-check's `controls-rerun-landing.txt` prints 11/12``
New: ``round-94 `.ufo/waves/round-94/controls/c1-controls-r94.py` ~line 145 `git clone -q --shared LANE`; `.ufo/waves/round-94/w1/CriticClaimsC1-receipts/controls-rerun-landing.txt:60,117` print `CONTROL m5-cell-repair-before-r93 rc=1 want=0 FAIL` and `C1-CONTROLS-RESULT fail controls=12`; `controls-pinned-lane-r94.txt:60,117` print `rc=0 want=0 PASS` and `pass controls=12```
Evidence: `09-round94-p4.txt`.

### L2 — MEDIUM — line 49: “prints 15/15” is a paraphrase
The receipt prints exactly `C1-CONTROLS-RESULT pass controls=15` (line 150). Old: ``and prints 15/15``
New: ``and prints `C1-CONTROLS-RESULT pass controls=15```. Evidence: `21-lesson-evidence.txt`.

### L3 — MEDIUM — line 50: the cited limb is wrong
The `two-cells-one-line` control prints `M3 FAIL same_files=True bad_lines=1 old_not_once=0 dup_rows=1`
(receipt lines 139–149); the only `old_not_once=1` block belongs to `unlabelled-row` (line 96). Old:
``the counter's M3 reported `old_not_once``` New: ``the `.ufo/waves/round-95/controls/c1-controls-r95.txt:139-149`
block prints `CONTROL two-cells-one-line rc=1 want=1 PASS limb=True` and `M3 FAIL … bad_lines=1 old_not_once=0 dup_rows=1````
Evidence: `10-controls-two-cells.txt`, `10b-old-not-once-context.txt`.

### L4 — LOW — line 46: the Mistakes table lacks the round-94 `#`/column shape
Old header: `| class | evidence | captured-by | fix |`
New: `| # | class | evidence pointer | captured-by | fix |` with rows `M95-1` (reproducibility), `M95-2`
(frozen-control), `M95-3` (key-collision), matching `corpus/lessons/round-94.md`. The `#` column is what
lets the wave findings cite a row by id.

### L5 — LOW — line 1 and lines 20/27: missing `author:`; two precision items
Add `author: kasegi (round 95, attempt 1)` after the title (round-94 lesson has the same header). Line 20:
“the only opened source that states the 76-character length” → “the only non-superseded row that states
the 76-character length” (S141 is opened and states it, but is superseded/rejected). Line 27: expand the
S140 shorthand anchors to full paths as in `proposed-lesson.md` so `anchorcheck` can resolve each one.

## Routed findings (not claim re-scores)

**F1 — scanner docstring is stale at the C2 landing.** `corpus/instruments/capture-secret-scan.py:120-134`
still lists “the JWT-form GitLab tokens (`glcbt-eyJ…`, `glsat-eyJ…`, `gliamat-eyJ…`; S140 lines 430, 447,
464) … are not detected”, and the `github-token` paragraph (`:81-84`) lists `ghr_` only as the 36-character
classic prefix; the new `github-refresh-token` shape is documented nowhere. The landed shapes at `:191`,
`:196`, `:207-208` and the 14 selftest cases at `:439-452` contradict the docstring. Behaviour (the C2
statement) is unaffected; the docstring should be corrected at integration or next round. Evidence:
`23-docstring.txt`.

**F2 — the frozen C2 pointer labels the keyword lines.** The frozen claim's “S140 lines 429/446/463” are
the `keywords` lines; the grammar is `430/447/464`. The entry imported that phrasing. This is an entry
precision defect (D2), not a re-score of C2; the claim's own bytes are what they are.

**F3 — the committed C1 controls receipt is modified in the working tree.** `git status` shows
` M .ufo/waves/round-95/controls/c1-controls-r95.txt`; this seat read the working tree copy for the
`two-cells-one-line` block. The committed-at-freeze copy is the one the claim names; the L1 should decide
whether the modified copy supersedes it. No claim verdict is drawn here.

## Gates

| Gate | Result |
|---|---|
| anchor/quote (current entry) | 39/39, `bad=0`; 7 required regex strings missing; recheck parse rc 2 |
| anchor/quote (proposed entry) | 39/39, `bad=0`; `missing=0`; recheck parse rc 0 |
| anchorcheck (current entry) | 2 in-range, 2 distinct, 0 bad, rc 0 |
| anchorcheck (proposed entry) | 33 in-range, 24 distinct, 0 bad, rc 0 |
| selftest | `SELFTEST-RESULT pass cases=115`, rc 0 |
| files scan | `scanned=2 hits=0 files=0 allowed=0 unused_allow=24 rc=0` |
| census | `kasegi ok` rc 0; 7 W04 (6 inherited + S143) |
| registry | 141 → 143 rows |
| lesson evidence | receipt lines 60/117, controls 139–149, postlanding 150 all observed |
| not run | C1 `knowledge-meter.py`; C2 `capability-check.py`; no claim verdict |

## Touched surfaces

- **Read-only inputs:** the entry, the lesson, `S142`/`S140` captures, the S141 fetch receipts
  (`08-github-rules-file.txt`, `06-github-firstparty-examples.txt`), `capture-secret-scan.py`, the
  round-94 P4 receipts and spot-check, the round-95 controls receipts, the C1 landing receipt,
  `corpus/SOURCES.md`, `CORPUS.md` rule 2.
- **Written:** this report and `ScribeGate-receipts/` (29 files: 25 `.txt` receipts, 2 `.py` checkers,
  2 proposed `.md` copies). `proposed-entry.md` and `proposed-lesson.md` are proposals
  only, under receipts — no corpus file was edited by this seat.
- **Not done:** no `git add/commit/push/checkout/reset/stash`, no mutating `jj`, no source re-fetch, no
  subagent, no `ask`, no `agent://all`.
- **Process note (disclosed):** two `write` calls used lane-relative paths while the tool's cwd was the
  fleet root; the files landed under `/home/vgpnk/Projects/shokunin/.ufo/waves/round-95/w1/ScribeGate-receipts/`.
  Both were copied to the lane receipts dir and the stray files/empty dirs removed; `ls` shows no
  `/home/vgpnk/Projects/shokunin/.ufo/waves/round-95`. The fleet `git status` shows no new untracked entry
  from this seat (`.ufo/reports/round-95/kasegi.md` is the L1's).

## Out of scope / known limits

- No C1 or C2 verdict; the frozen predicates are not executed here.
- The S141 raw capture is not committed (it lists published example values). Its line 72 is verified
  against the committed fetch receipt `08-github-rules-file.txt:16` and the S143 row's pin (130 lines /
  3,955 bytes / sha256 `02c67ceb…`), not against raw bytes. That is a known evidence limit, not a failed
  anchor.
- No re-fetch of S142/S140/S141; the committed capture bytes are the ground truth.
- The scanner docstring defect (F1) is reported, not fixed.
- No change to `claims.json`, `SOURCES.md`, `SCORECARD.md`, `QUALITY.md`, `LOG.md`, `MANIFEST.json` or any
  sibling lane.

## Artifact paths

- Report: `.ufo/waves/round-95/w1/ScribeGate.md`
- Receipts: `.ufo/waves/round-95/w1/ScribeGate-receipts/`
- Proposed entry: `.ufo/waves/round-95/w1/ScribeGate-receipts/proposed-entry.md`
- Proposed lesson: `.ufo/waves/round-95/w1/ScribeGate-receipts/proposed-lesson.md`
- Entry diff: `.ufo/waves/round-95/w1/ScribeGate-receipts/18-proposed-diff.txt`
- Lesson diff: `.ufo/waves/round-95/w1/ScribeGate-receipts/20-proposed-lesson-diff.txt`
- Anchor checker: `.ufo/waves/round-95/w1/ScribeGate-receipts/anchor-quote-check.py`
- Boundary probes: `.ufo/waves/round-95/w1/ScribeGate-receipts/probe-shapes.py`

## Receipts

Every command below was run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless stated; the
receipt file holds the observed output.

| # | Command (abridged) | Observed | Receipt |
|---|---|---|---|
| 1 | `python3 .ufo/waves/round-95/w1/ScribeGate-receipts/anchor-quote-check.py` | `ANCHOR-CHECK total=39 bad=0`; `ENTRY-REQUIRED missing=7`; `RECHECK-PARSE rc=2` | `01-anchors.txt` |
| 2 | `nl -ba` over S142/S140/receipts + `wc -lc` + `sha256sum` | exact lines; S142 182/7944 `727ba6a0…`; S140 563/25537 `f3fd09e4…` | `02-capture-lines.txt` |
| 3 | `nl -ba corpus/instruments/capture-secret-scan.py` 186–210, 437–453 | shape defs and 14 cases | `03-scanner-shapes.txt` |
| 4 | `python3 -B corpus/instruments/capture-secret-scan.py --selftest \| grep -E 'gh-refresh\|gl-jwt\|SELFTEST-RESULT'` | `SELFTEST-RESULT pass cases=115`, rc 0 | `04-selftest.txt` |
| 5 | `python3 -B … --files S142 S140` | `scanned=2 hits=0 files=0 allowed=0 unused_allow=24 rc=0` | `05-files-scan.txt` |
| 6 | `python3 -B corpus/instruments/anchorcheck.py <entry>` | `2 in-range cite instances, 0 bad`, rc 0 | `06-anchorcheck.txt` |
| 7 | `bash -n -c "$(sed -n '4p' …)"`; proposed command `bash -n` + run | old rc 2; proposed rc 0 / rc 0 | `07-recheck.txt` |
| 8 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (fleet root) | `kasegi ok` rc 0; 7 W04 | `08-census.txt` |
| 9 | `grep -n` round-94 P4 receipts + spot-check | `…:60` / `…:117` lines as quoted | `09-round94-p4.txt` |
| 10 | `grep -n -B2 -A14 'CONTROL two-cells-one-line' …`; `grep -n old_not_once` | block 139–149; `old_not_once=1` only at line 96 (`unlabelled-row`) | `10-controls-two-cells.txt`, `10b-old-not-once-context.txt` |
| 11 | `git show 9ef0126:corpus/SOURCES.md \| grep -cE …`; `grep -cE … corpus/SOURCES.md` | 141 / 143 rows | `11-registry.txt` |
| 12 | `git diff -- <entry> <lesson>` | 28-line worktree diff (entry only; lesson identical) | `12-worktree-diff.txt` |
| 13 | `python3 …/probe-shapes.py` | 24 `PROBE` lines, rc 0 | `13-probes.txt` |
| 14 | `python3 - <<'PY'` base64; vendor-`\b` probe | `{"` → `eyI=`; `acme-gliamat` vendor match at 5; `\u0020gliamat` vendor none | `13b-base64.txt`, `13c-regex-diff.txt` |
| 15 | `python3 -B … --rev master`; `--help` | rc 2 `reason=usage`; usage lists `--lane/--rev/--files/--selftest/--allow` | `15-rev-master.txt`, `15b-scanner-usage.txt` |
| 16 | `python3 …/anchor-quote-check.py <proposed>` | `total=39 bad=0`; `missing=0`; `RECHECK-PARSE rc=0` | `16-proposed-check.txt` |
| 17 | `python3 -B corpus/instruments/anchorcheck.py <proposed> \| sed -E 's/ghr_[A-Za-z0-9]{20,}/ghr_<redacted>/g'` | `33 in-range cite instances, 0 bad`, 24 distinct, rc 0 (one placeholder masked) | `17-proposed-anchorcheck.txt` |
| 18 | `diff -u <entry> <proposed>` | 191-line diff, rc 1 (differences) | `18-proposed-diff.txt` |
| 19 | `diff -u <lesson> <proposed>` | 81-line diff, rc 1 (differences) | `20-proposed-lesson-diff.txt` |
| 20 | `sed -n` the lesson's evidence lines | 60/117, 139–149, postlanding 150 all match | `21-lesson-evidence.txt` |
| 21 | `nl -ba … 80–84,120–136`; `grep -n github-refresh-token` | docstring still calls the JWT forms a known limit; row name only at 196/439/443 | `23-docstring.txt` |
| 22 | summary | `ANCHORS 39/39 bad=0`; entry 14 / lesson 5 defects | `22-verdict.txt` |

No credential value is reproduced in this report or its receipts; the one published `ghr_` placeholder
printed by `anchorcheck` in receipt 17 is masked as `ghr_<redacted>`, and the S141 measurement receipt is
truncated before the example value.
