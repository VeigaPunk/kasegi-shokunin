# ScribeGate — round-98 w1 scribe report

Seat: ScribeGate (scribe, leaf; no swarm). Lane: kasegi. Round 98, attempt 1.
Base `2133f5bd993aaf34efad795d5e0b588485401fb2`; freeze
`12bb2f98cf9d07bcbc8b62985516cc3ff65d9ae8`; C2 landing
`e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`; C1 landing
`e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`.

Bytes verified (the lesson was edited by a sibling during this seat — see D7):

| file | sha256 |
|---|---|
| `corpus/lessons/round-98.md` | `c942b96a64330b1ed16407334cff20a3630e845f3cdbf35125d9da37e45b4f1a` |
| `corpus/SOURCES.md` (working tree) | `3f21b3275117f7fc0dd91b912b95a02aaa048ed01b68c184dfa87ce608f581df` |
| `corpus/QUALITY.md` (working tree) | `51e0d18fb51aeb467ea822bf7fdd21f444fab025e0957d9dec8eaa7ef601b640` |
| `SCORECARD.md` (working tree) | `471847d5c99a9fc6fbdac6050903d5be2618d26a08fc57407d329ddfe3a6fc3c` |
| `corpus/instruments/citation-survival.md` | `86ca5da7884b4fa933f83cf9cda6b08c44b1b5eb108a194ebb860a53e7ebd5d6` |

Receipts: `.ufo/waves/round-98/w1/ScribeGate-receipts/` —
`gate-numbers.txt`, `lesson-integration.txt`, `census-remeasure.txt`.

## 1. What I ran (and what I did not)

Ran, read-only, from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`:

- `sha256sum` over the C1/C2 instruments, the C2 gate, the C1 harness, and the
  same files extracted at `12bb2f9`, `e2caf4a`, `e2d3de7`
  (`gate-numbers.txt`).
- `git show 2133f5b:corpus/SOURCES.md` vs the working tree for the S140/S144
  cells, status, recheck and registry count (`gate-numbers.txt`).
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
  → `kasegi ok` rc 0, seven W04 lines S028/S029/S072/S076/S080/S085/S143.
- `python3 -B corpus/instruments/capture-secret-scan.py --selftest` →
  `SELFTEST-RESULT pass cases=170`, rc 0.
- The census measurement twice, by the instrument's own measure logic
  (`class = cells[-7]`, `scopes = last cell`, INTERNAL-only pinned rate,
  RESOLVES+MIRROR-EQUIVALENT+INTERNAL host-inclusive rate), on the extract's
  own `resolve.py` at `e2caf4a1` and at the base `2133f5b`
  (`census-remeasure.txt`).
- The R133 command, the Mistakes-table cell count, the SCORECARD row at
  `e2caf4a`, the QUALITY R153/R154 presence at HEAD, the coverage-map sweep,
  the redaction before/after digests, `git merge-base --is-ancestor`, the
  frozen and corrected P3 greps, and a fresh compile of the landed scanner
  (`lesson-integration.txt`, `gate-numbers.txt`).

Did **not** run: the C1 control harness (`c1-controls-r98.py`) and the C2
capability gate (`capability-check.py`). Both are committed receipts I read;
re-running them is the wave's executor/reviewer work, not the scribe's.

The instrument's own `--check` path failed twice in this seat with
`CENSUS-CHECK fail reason=resolve-rc-15 rc=2` (the child `resolve.py` received
SIGTERM; 6m12s wall). The same `resolve.py` on the same extract, run directly,
exits 0 and its TSV reproduces the file's pinned and host-inclusive lines
byte-for-byte (D10).

## 2. GATE-DRAFT

GATE-DRAFT:

```markdown
## Gate

Candidates considered this round:

1. **S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at
   commit 59ada1f4** — re-opened from its committed capture for the four rules
   this round implements (lines 291-294, 478-481, 495-498, 547-551; capture
   `corpus/source-snapshots/round-94/S140.txt`, sha256
   `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563
   lines). URL:
   `https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/raw/59ada1f4ca53d5a69fafb9cb0f10bb893720ce39/rules/mit/gitlab/gitlab.toml`.
   Opened 2026-11-07; the live fetch answered HTTP 403 (a Cloudflare challenge
   page, 6,078 bytes, sha256 `6ab31380…`, receipt
   `.ufo/waves/round-98/l1/source-reopen-r98.txt`), the same result round 97
   recorded, so the committed capture is the citation base. Quotes (each under
   25 words, capture lines):
   - `S140:293` — `regex = "\\b(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
   - `S140:480` — `regex = '''\b(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)'''`
   - `S140:497` — `regex = '''\b(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)'''`
   - `S140:549` — `regex = '''(?:cell-[0-9]+-)?[0-9a-f]{64}'''`
   - `S140:550` — `assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''`
2. **S144 — GitLab Docs, Security — Tokens** — re-opened from its committed
   capture for the two prefix-table rows that state two of the four shapes.
   URL: `https://docs.gitlab.com/security/tokens/`. Opened 2026-11-07; live
   fetch HTTP 200, 67,805 bytes, sha256 `765becf3…`; the live page carries
   `glcbt-` and `_gitlab_session=`. Quotes (capture
   `corpus/source-snapshots/round-96/S144.txt`):
   - `S144:356` — `CI/CD Job tokenglcbt-`
   - `S144:362` — `GitLab session cookies_gitlab_session=`
3. **S144 as a second source for the two IAM forms — REJECTED.** S144's
   prefix table (capture lines 344-362) names `glcbt-` and `_gitlab_session=`
   but no IAM prefix: `grep -c 'gliam' corpus/source-snapshots/round-96/S144.txt`
   prints 0. The two IAM forms are stated only by the rules file, so no new row
   is written for them: a row no admitted entry can cite is not appended
   (CORPUS rule 4). Flip: a docs page that names `gliamrt-`/`gliamac-` or their
   lengths.

Status / used-by changes this round, old → new:

- S140: status `mined` (unchanged), recheck `180d` (unchanged); used-by
  `corpus/instruments/capture-secret-scan.py` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-remaining-token-families.md, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`
  (the round-97 entry's citation was missing from the cell and is added here).
- S144: status `mined` (unchanged), recheck `180d` (unchanged); used-by
  `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-routable-and-versioned-token-forms.md` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-routable-and-versioned-token-forms.md, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`.

Registry 147 → 147 rows:
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` prints 147 at the
base and 147 in the working tree. Census:
`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the seven inherited W04 duplicate-URL warnings
(S028, S029, S072, S076, S080, S085, S143).

Spot-check result: pending the round-98 non-author closure.
```

One deliberate difference from the lesson's current Gate body, because the
current text is not re-derivable from a committed artifact: candidate 3 drops
the clause "and the live page (67,805 bytes) prints 0 as well" (D6). The
capture grep (`0`) is kept. No other number changed: every remaining number in
the block is verified in §3.

The `Spot-check result: pending …` line is kept because it is the round-97
convention and R133's exact check passes (§4.5).

## 3. Every number in the draft Gate block, re-derived

| # | Gate claim | Command run | Observed |
|---|---|---|---|
| 1 | S140 capture sha256 `f3fd09e4…`, 563 lines | `sha256sum corpus/source-snapshots/round-94/S140.txt`; `wc -l` | `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`; `563` |
| 2 | S140 lines 291-294, 478-481, 495-498, 547-551 hold the five quotes | `sed -n '291,294p;478,481p;495,498p;547,551p' …S140.txt` | the five lines are byte-identical to the quotes in the draft |
| 3 | S140 live fetch 403, 6,078 bytes, sha256 `6ab31380…` | read `.ufo/waves/round-98/l1/source-reopen-r98.txt` | `http=403 bytes=6078`; `6ab3138012c15a83c9fa9f6eb14b3cb093dc28294131e52adc5928782ff5ab1d` |
| 4 | S144 live fetch 200, 67,805 bytes, sha256 `765becf3…` | same receipt | `http=200 bytes=67805`; `765becf33995fd344ae5939ac6f6e35715b7c2a348b32f708a0a32472b17f4b6` |
| 5 | S144 lines 356/362 | `sed -n '356p;362p' …S144.txt` | `CI/CD Job tokenglcbt-`; `GitLab session cookies_gitlab_session=` |
| 6 | S144 states no IAM prefix (`grep -c 'gliam'` = 0) | `grep -c 'gliam' …S144.txt` | `0` |
| 7 | Quotes are each under 25 words | `len(quote.split())` per quote | 3 whitespace-separated tokens each |
| 8 | Registry 147 at the base and 147 in the working tree | `git show 2133f5b:corpus/SOURCES.md \| grep -cE …`; `grep -cE … corpus/SOURCES.md` | `147`; `147` |
| 9 | Census validate `kasegi ok` rc 0, seven W04 (S028, S029, S072, S076, S080, S085, S143) | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok …/corpus/SOURCES.md`, rc 0; exactly those seven W04 lines |
| 10 | S140 status `mined`, recheck `180d`, unchanged | base vs working-tree cells | `mined` / `180d` both sides |
| 11 | S144 status `mined`, recheck `180d`, unchanged | base vs working-tree cells | `mined` / `180d` both sides |
| 12 | S140 used-by old → new | base cell vs working-tree cell | `capture-secret-scan.py` → `capture-secret-scan.py, gitlab-remaining-token-families.md, gitlab-iam-ci-build-and-session-token-shapes.md` |
| 13 | S144 used-by old → new | base cell vs working-tree cell | `capture-secret-scan.py, gitlab-routable-and-versioned-token-forms.md` → `…, gitlab-iam-ci-build-and-session-token-shapes.md` |
| 14 | The round-97 entry's citation was missing from S140's cell | base S140 cell | `corpus/instruments/capture-secret-scan.py` only |
| 15 | CORPUS rule 4 wording ("a row no admitted entry can cite is not appended") | `grep -rn 'CORPUS rule'` | same usage at `.ufo/waves/round-24/wave1/SOURCESRows.md:106`; no canonical numbered list in `corpus/README.md` or `corpus/QUALITY.md` |

## 4. Integration text checks

### 4.1 S140/S144 used-by cells (the assignment's check)

- S140 cell: `corpus/instruments/capture-secret-scan.py,
  corpus/knowledge/gitlab-remaining-token-families.md,
  corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` — lists
  both the round-97 and the round-98 knowledge entries. **PASS.**
- S144 cell: `corpus/instruments/capture-secret-scan.py,
  corpus/knowledge/gitlab-routable-and-versioned-token-forms.md,
  corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` — lists the
  round-96 and round-98 entries, **not** the round-97 entry, although
  `corpus/knowledge/gitlab-remaining-token-families.md:55` cites S144
  (`S144 (round 96) states the prefix set and that the prefixes are standard`).
  **FAIL for the round-97 entry** (D3).

### 4.2 QUALITY

- R153 and R154 are present at HEAD (`git show HEAD:corpus/QUALITY.md | grep -c
  '^| R153 \|^| R154 '` → `2`), i.e. the round-97 additions are committed.
- R155 and R156 are the round-98 additions in the working tree
  (`grep -c '^| R155 \|^| R156 ' corpus/QUALITY.md` → `2`); R155 names the
  round-97 M4 wrong-instrument hole and R156 the revision-bound census, as the
  lesson's Learning says.

### 4.3 SCORECARD capability row

At the C2 landing `e2caf4a`, row 307 names all nine round-98 shape ids
(`gitlab-ci-build-token`, `gitlab-iam-refresh-token`,
`gitlab-iam-authorization-code`, `gitlab-session-cookie`,
`gitlab-runner-registration-token`, `gitlab-feed-token`,
`gitlab-oauth-app-secret`, `gitlab-feed-token-v2`,
`gitlab-scim-oauth-token` — one hit each) and its last cell is `87`
(`awk -F'|' '{print "["$(NF-1)"]"}'` → `[ 87 ]`). K5's `rows=1 last=87
named=True` receipt agrees.

### 4.4 Lesson Mistakes rows

Six rows (`grep -c '^| M98-'` → `6`), each with five cells (`cells=5` for every
row): `# | class | evidence pointer | captured-by | fix`. M98-1…M98-5 were
present when the seat opened; M98-6 was added by a sibling at 18:13 (D7).
M98-6's warning is real: a fresh compile of the landed scanner prints
`capture-secret-scan.py:184: SyntaxWarning: "\-" is an invalid escape sequence`.

### 4.5 R133

`awk '/^## Gate/{g=1} /^## Mistakes/{g=0} g' corpus/lessons/round-98.md |
grep -c -E 'PENDING-L1|TBD|TODO'` → `0` (grep rc 1). The only placeholder-shaped
lines in the file are `Spot-check result: pending the round-98 non-author
closure.` (Gate body, line 62) and `Pending the wave.` (Wave findings, line 96);
neither is one of R133's three markers.

### 4.6 Census of record (the C1 measurement)

Independently re-derived from the extract's own `resolve.py` at `e2caf4a1`
(TSV 7961 rows) and at the base `2133f5b` (TSV 7958 rows):

| revision | pinned (INTERNAL only) | host-inclusive | host-owned |
|---|---|---|---|
| `e2caf4a1` (census `measured-at`) | SKILL 162/732 = 22.13 %; corpus 2551/7559 = 33.75 %; lane 2589/7961 = 32.52 % | SKILL 166/732 = 22.68 %; corpus 2629/7559 = 34.78 %; lane 2667/7961 = 33.50 % | 78 |
| `2133f5b` (base) | SKILL 162/732 = 22.13 %; corpus 2550/7556 = 33.75 %; lane 2588/7958 = 32.52 % | SKILL 166/732 = 22.68 %; corpus 2628/7556 = 34.78 %; lane 2666/7958 = 33.50 % | 78 |

The `e2caf4a1` row is byte-identical to the file's lines 6-8. The class counts
are `RESOLVES 78, MIRROR-EQUIVALENT 0, GONE 5294, INTERNAL 2589` (sum 7961).
The base row confirms the claim statement's "the base reads 162/732 pinned,
166/732 host-inclusive". The old census at the base reads `132/701 = 18.83 %`,
`1202/4766`, `1227/5152`, scope 224 files.

## 5. Discrepancies

**D1 — the dispatch's census numbers are the base reading, not the census of
record's.** The wave context says "pinned (INTERNAL-only) SKILL 162/732, corpus
2550/7556, lane 2588/7958, host-owned 78". Those are exactly the `2133f5b`
base measurement (§4.6, second row). The census of record is measured at
`e2caf4a1` and records corpus 2551/7559, lane 2589/7961 (file line 6, l1
receipt line 2, SCORECARD 3389/3395, LOG 3109). The C2 landing adds three
distinct citations, one of them INTERNAL. `grep -rn '2550/7556\|2588/7958'`
matches the dispatch artifacts (`w1-spec.json`, `w1-dispatch.json`,
`make-wave.py`) and, after the wave started, sibling seats' reports/receipts
that measure the base; no lane artifact (census, SCORECARD, LOG) carries the
base triple as the census's. Any Gate/lesson text that copies the dispatch
triple as the census's is wrong; the census's triple is 2551/7559 and
2589/7961.

**D2 — the C1 `harness_sha256` pin matches no committed harness.**
`claims.json` pins `d39a1fc8cc5ad189b5077dc03c1c3373bca59d77a120493163ccca63eb4f05e0`;
the harness committed at the freeze `12bb2f9` is
`0488d79626e54731a8d5be3985fd1edad68b2b612a74d86454d5bca8a3950e7a`; at the C1
landing `e2d3de7` it is
`d97132684455aa6cca5bd65dd0e07a94942b8469801d05f219ba3a52b47ecc1a`. The
freeze→landing diff adds the `git checkout -q <base>` hunk (M98-3's fix).
Erratum (2) discloses the fix but does not update the pin; `grep -rn
'd39a1fc8'` matches only `claims.json`. A verifier that checks the frozen
`harness_sha256` will fail on the landed bytes.

**D3 — S144's used-by omits the round-97 entry that cites S144.**
`corpus/knowledge/gitlab-remaining-token-families.md:55` cites S144; S144's
cell lists `capture-secret-scan.py`,
`gitlab-routable-and-versioned-token-forms.md`,
`gitlab-iam-ci-build-and-session-token-shapes.md` — not the round-97 entry.
The same correction applied to S140 was not applied to S144. (S140's cell also
omits `github-refresh-tokens-and-gitlab-jwt-tokens.md` and
`gitlab-routable-and-versioned-token-forms.md`, both of which cite S140 — a
pre-existing gap the round did not touch.) If the L1 applies the S144 fix, the
Gate's S144 line becomes: `…, gitlab-routable-and-versioned-token-forms.md,
gitlab-remaining-token-families.md,
gitlab-iam-ci-build-and-session-token-shapes.md`.

**D4 — the new knowledge entry's `verified-at` is stale.**
`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:4` says "the
S140 live `/-/raw/` fetch answered HTTP 403 in round 97 and was not retried
this round". The entry landed at `e2caf4a` (17:47:25 -03); the round's receipt
`.ufo/waves/round-98/l1/source-reopen-r98.txt` records a live fetch at
`2026-11-07T20:54:03Z` (= 17:54:03 -03) answering HTTP 403. The statement was
true at its landing and is contradicted by the round's later receipt; the
lesson's Gate says the fetch was retried.

**D5 — the redaction receipt's line count is off by one.**
`.ufo/waves/round-98/l1/redaction-r98.txt:7` says "bytes: 77 lines before and
after"; the redacted file has 76 lines (`wc -l` = 76, `awk END{NR}` = 76,
trailing newline present). The before/after digests are exact:
`e1a5f0e3…` (base file) and `01a16e0e…` (current file).

**D6 — Gate candidate 3's live-page clause has no committed artifact.**
The current lesson says S144's "live page (67,805 bytes) prints 0 as well" for
`gliam`. The live HTML was written to the l1 scratch
(`/fast/scratch/hyaku/kasegi-r98/l1/s144-live.html`) and is not committed; the
receipt records only the size and sha256, and its own four `gliam` hits are the
S140 capture lines (478-481/495-498), not an S144 sweep. The capture grep
(`grep -c 'gliam' …S144.txt` → 0) is verified; the live-page sweep is not.
The draft drops the clause.

**D7 — the Learning tally contradicts the Mistakes table (R132).**
The lesson was edited at 18:13 to add M98-6; the Learning still says "five
mistakes mined (M98-1…M98-5)" while `grep -c '^| M98-'` prints `6`. R132
requires a tally sentence to be bound to the list it counts. The sentence
should read "six mistakes mined (M98-1…M98-6)" and mention M98-6's class
(quality; the `\-` SyntaxWarning routed to round 99).

**D8 — several Mistakes evidence outputs are not committed receipts.**
M98-3 cites `C1-CONTROLS-RESULT error reason=base-mismatch head=e2caf4a1…`;
M98-4 cites `K2 printed hits=1`; M98-1/M98-2 cite `printed 1243`. What is
committed: `grep -rn 'base-mismatch'` under `.ufo/waves/round-98/` matches only
the harness's own print statement (`c1-controls-r98.py:104`); `grep -rn
'hits=1'` matches nothing there; the 1,243 figure appears in the claims
erratum (committed at the C1 landing) and, after the landing, in sibling seat
reports/receipts (e.g. `w1/CriticClaimsC1.md:186`), not in a pre-freeze or
landing receipt. What *is* verifiable: M98-4's file:line
(`.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt:75`
held `[gitlab-ci-build-token-fixture-redacted-r98]` at the base), M98-3's fix (the
freeze→landing diff), M98-5's old→new instrument sha (the `claims.json` diff),
and M98-6's warning (fresh compile). The 1,243 number rests on the committed
erratum text, not an executed receipt.

**D9 — the frozen P3 command now prints 0.** `grep -c '/fast/scratch'
corpus/instruments/citation-survival.md` → `0`; the corrected
`grep -c 'tree-e2caf4a1561b'` → `0`. P3 as frozen therefore passes on the
landed file; the erratum's mis-specification rationale is load-bearing only for
the first generation (1,243 occurrences), not for the landed bytes.

**D10 — the instrument's `--check` path is not reproducible in this seat.**
Two runs ended `CENSUS-CHECK fail reason=resolve-rc-15 rc=2` (the child
`resolve.py` received SIGTERM; 6m12s wall, host at 10/30 GiB used at receipt
time). The same `resolve.py` on the same extract, run directly, exits 0 in
6m59s and its TSV reproduces the file's pinned and host-inclusive lines
byte-for-byte (§4.6). The measurement is verified; the instrument's subprocess
plumbing is not, in this environment.

**D11 — the erratum's "219 distinct" `/fast/scratch` citations is not
reproduced.** A literal sweep of `corpus/` + `SKILL.md` gives 41 distinct
tokens / 93 occurrences; the `e2caf4a1` TSV has 39 distinct citations
containing `/fast/scratch`; the whole lane has 11,406 distinct tokens. No
committed artifact ties 219 to a command. The number is disclosed in the
erratum but not re-derivable.

## 6. Not verified / out of scope

- The C1 control harness's eight controls and the C2 capability gate's K1-K7
  were read from their committed receipts, not re-run (executor/reviewer
  work). Their printed numbers agree with the claims' `controls` strings.
- The live S144 page (D6) and the first-generation census body (D8, D11) are
  not committed and cannot be re-read.
- The wave findings section is `Pending the wave.` at the bytes verified; the
  13 seat reports are outside this seat's scope.

## 7. Verdicts

VERDICT: GATE-DRAFT numbers — PASS. Every number in the `GATE-DRAFT` block is
re-derived in §3 from a command run in this seat or a committed receipt read
(S140 capture sha256/563 lines, S140 lines 291-294/478-481/495-498/547-551,
S140 live 403/6,078/`6ab31380…`, S144 live 200/67,805/`765becf3…`, S144
356/362, S144 `gliam`=0, registry 147/147, `kasegi ok` + seven W04, both
status/recheck pairs, both used-by old→new cells, CORPUS rule 4 usage).

VERDICT: S140/S144 used-by cells list the two new knowledge entries — PARTIAL.
S140 lists both the round-97 and round-98 entries; S144 lists the round-98
entry but not the round-97 entry, which cites S144 at
`corpus/knowledge/gitlab-remaining-token-families.md:55` (D3).

VERDICT: every Mistakes row carries class, evidence pointer, captured-by and
fix — PASS structurally (6 rows × 5 cells), with the evidence-quality caveat
that M98-1/M98-2/M98-3/M98-4's quoted outputs are not committed receipts (D8).

VERDICT: no `PENDING-L1`/`TBD`/`TODO` in the Gate body (R133) — PASS. The R133
command prints 0; the two placeholder-shaped lines are prose `pending` lines
outside the three markers (§4.5).

VERDICT: the census of record's numbers — PASS for `e2caf4a1` (2551/7559,
2589/7961, 78, byte-identical to the file), FAIL for the dispatch's
2550/7556 and 2588/7958 as the census's numbers: they are the `2133f5b` base
reading (D1).

VERDICT: the C1 `harness_sha256` pin — FAIL. The pinned `d39a1fc8…` matches
neither the freeze-committed harness (`0488d796…`) nor the landing harness
(`d9713268…`); the erratum discloses the harness change without updating the
pin (D2).
