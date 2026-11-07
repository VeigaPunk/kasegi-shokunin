# ReviewC2Scanner — round 93, wave 1 (C2)

Seat scope: re-derive the frozen C2 predicate at landing
`9225954a6e3f177af46bdb9d811c062a4353a552` (base `e15996b`), read the landed scanner and the
source `corpus/source-snapshots/round-93/S139.txt`, check the frozen statement clause by clause,
and produce the reanchor table for every knowledge citation of
`corpus/instruments/capture-secret-scan.py` by line.

Nothing outside this seat's report/receipt paths was written. No mutating git/jj command was run in
the lane (`git show`/`git grep`/`git diff-tree` only). No tool was installed or upgraded: the
checks used `python3 -B`, `git` and `sha256sum` already on the host, so no RULES.md channel applies.
All scratch work lived in `/fast/scratch/hyaku/kasegi-r93/ReviewC2Scanner` and was removed on exit.

## Verdict

**APPROVE** — C2 re-derived independently: P1, P2 and P3 all hold at the landing
(counter `rc=0` at the printed run-time seed and at seeds 1 and 9191, K1–K8 pass; landed scanner
sha256 equals the frozen candidate sha256; the landing changes exactly the two named paths).
Four defects are routed (D1–D4); none of them re-scores the frozen predicate, so none changes the
verdict. D1 is the only one that must be closed elsewhere in this round before the lane's
knowledge commit.

## 1. Predicate, re-derived

| Limb | Claimed | Observed | rc |
|---|---|---|---|
| P1 | K1–K8 pass at a printed run-time seed, and at seeds 1 and 9191 | `CAPABILITY-CHECK-RESULT pass rc=0` three times; `LIMB K1..K8 pass` each run; `K4 nonce=` differs per run; `K8 clauses=50 failing=none`; `K3 scanned=1957 hits=0 files=0 allowed=24 unused_allow=0`; `K6 base_hits=22 new_caught_by_base=none outside_plants=none` | 0 / 0 / 0 |
| P2 | instrument sha256 `7d9d73…a683c5` | `git show 9225954:corpus/instruments/capture-secret-scan.py \| sha256sum` → `7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5`; identical to `c2/candidate-capture-secret-scan.py` and to the worktree copy | 0 |
| P3 | exactly `corpus/instruments/capture-secret-scan.py` + `SCORECARD.md` | `git diff-tree --no-commit-id --name-status -r 9225954` → `M SCORECARD.md`, `M corpus/instruments/capture-secret-scan.py` (47 insertions, 6 deletions) | 0 |
| pin | counter sha256 `8a4ad5…`; row sha256 `6d18d5…` | both match the frozen values; landed `capture-secret-scan` row is **byte-identical** to `c2/candidate-row.txt`, last cell `87`, names `gitlab-pat`, `glpat-` and the escape family | 0 |

## 2. Frozen statement, clause by clause

Implementation read at the landing: docstring lines 81–116, `_ESC_LB`/`_GH_LB` at 169–170,
`GITLAB_PATTERNS` at 177–180, `patterns()` at 212–213.

| # | Frozen clause | Landed code | Independent check | Result |
|---|---|---|---|---|
| 1 | shape `gitlab-pat` for `glpat-` + exactly 20 of `A-Za-z0-9_-` | `_GL_LB + rb"glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"` (179) | probe `glpat-exact20` → `gitlab-pat`; `glpat-19`, `glpat-21`, `glpat-21-dash` → none | holds |
| 2 | not preceded by `A-Za-z0-9_-` | `(?<![A-Za-z0-9_-])` inside `_GL_LB` (177) | probes `glpat-letter-before`, `-digit-before`, `-underscore-before`, `-hyphen-before` → none; `(glpat-… )` → hit | holds |
| 3 | not followed by `A-Za-z0-9_-` | `(?![A-Za-z0-9_-])` (179) | `glpat-right-underscore`, `glpat-esc-right-letter`, `gl-pat-21-chars` → none | holds |
| 4 | preceding escape terminator `\t`, `\r`, `\n`, `\uXXXX`, `%XX`, `&#NN;`, `&#xXX;` allowed | `_GL_LB` = `(?<![…])｜(?<=\\[ntr])｜(?<=\\u[0-9A-Fa-f]{4})｜(?<=%[0-9A-Fa-f]{2})｜(?<=&#[0-9]{2};)｜(?<=&#[xX][0-9A-Fa-f]{2};)` (177) | probes `glpat-esc-t/-r/-n/-u/-pct/-amp-dec/-amp-hex` all → `gitlab-pat` | holds (but see D3) |
| 5 | `github-token` now also for a token preceded by any such escape terminator | `_GH_LB = _ESC_LB` (170), same seven forms | probes `gh-esc-t`, `gh-esc-u`, `gh-esc-pct`, `gh-esc-amp` → `github-token` | holds |
| 6 | every round-92 GitHub and round-87..91 shape otherwise unchanged | `_ESC_LB` is a strict superset of the old `(?:(?<![A-Za-z0-9_])｜(?<=\\n))`; cloud/`_LB`/`_CF_LB`/`_CK_LB` untouched; `GITHUB_PATTERNS` body unchanged at 174–175 | K3 clean over 1957 capture-class files (`hits=0`); K2 reproduces the round-86 STS oracle exactly; K6: the round-92 base instrument finds `none` of the new plants; selftest 90/90; probes `gh-stateless`, `gcs`, `aws`, `gh-36-with-dash`, `gh-36-with-dash-mid`, `gh-noesc-letter-before` behave as at round 92 | holds |
| 7 | negatives: bare prefix, 19/21 tails, `GLPAT-`, `glrt-`, letter-prefixed, post-escape right underscore, 36-char tail containing `-` | selftest 386–396 and 375–385; K4 plants S040–S045, S051 | selftest `gl-pat-bare-prefix`, `gl-pat-19-chars`, `gl-pat-21-chars`, `gl-pat-upper-prefix`, `gl-pat-runner-known-limit`, `gl-pat-letter-before`, `gl-pat-right-underscore` all `got=none`; probes reproduce each independently | holds |
| 8 | named limits: encoded prefix separators, other GitLab prefixes, fine-grained `github_pat_` | docstring 105 (`encoded `_` prefix separator`), 106–109 (`github_pat_`, `glrt-` and other GitLab prefixes, `gh%5Fp_`/`glpat%2D`) | read; `gh%5Fp_`/`glpat%2D` are documented as limits, not matched | holds |
| 9 | successor counter plants every value under a run-time nonce directory, carries U1–U6 | `reroot(p0, nonce)` over all 76 `PLANTS` entries and over `PLANT_EXPECT`/`NEW_EXPECT`/`ROUND93_NEW`; `nonce = os.urandom(4).hex()` printed per run | three runs printed distinct nonces (`39b49f7c`, `7510f161`, `1bb8b414`) and `K4 missing=none extra=none` each time; U1–U6 (S046–S051) present in `CLAUSES` | holds |

`patterns()` now returns **14** shapes (`private-key`, `op-ref`, `bearer`, `authorization`,
`credential`, `session-cookie`, `aws-sts-session-token`, `aws-access-key-id`,
`gcs-signed-url-signature`, `azure-sas-signature`, `cloudfront-signed-url-signature`,
`cloudfront-signed-cookie-signature`, `github-token`, `gitlab-pat`).

## 3. The source (S139)

* `sha256sum corpus/source-snapshots/round-93/S139.txt` →
  `154a7e1535b4a245e45e3f82705c271344f59aa6c344807645fa0bc4d1e1b188` — equals the frozen
  `frontier.sourced_claim.sha256`.
* Line 87 verbatim (`sed -n '87p'`, `cat -A` shows no trailing trickery):

  > `glpat- followed by a 20-character string. GitLab supports`

  Line 86 is the lead-in: `credential type, called a rule. For example, a GitLab personal access token is identified by the pattern`.
* **The page states the length and no alphabet.** `grep -niE 'alphanumeric|alphabet|letter'` over
  the whole capture returns **nothing**; the only characterisation of the value is
  "20-character string". So `[A-Za-z0-9_-]{20}` is a lane choice, and the docstring says exactly
  that ("the string drawn from `A-Za-z0-9_-` (a lane choice: the page states the length, not the
  alphabet)", lines 100–101) — honest, and the frozen statement freezes that class anyway.
* `glpat` occurs exactly once in the capture (line 87). The rejected GitLab profile page is not
  registered and not relied on here.

## 4. Findings, by severity

**D1 — routed, must close before the lane's knowledge commit: three class-B sentences are falsified
by the landing.** The landing changed the instrument, so measurements recorded in
`corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md` at the landing commit are now
false. At landing (`git show 9225954:<path>`, still unchanged in the worktree):

* line 100 and line 238: "fifteen `SELFTEST gh-… ok` lines … `SELFTEST-RESULT pass cases=68`".
  Measured at the landing: `grep -c '^SELFTEST gh-'` → **26**, and `SELFTEST-RESULT pass cases=90`
  (68 + 22 round-93 cases). Two sites, both stale.
* line 29: "it refuses a match preceded or followed by `[A-Za-z0-9_]`" — false on the left side
  since the landing (`\t`, `%20`, `\u0026`, `&#38;` all end in an alphanumeric byte and are now
  admitted; probes `gh-esc-t`, `gh-esc-pct`, `gh-esc-amp`, `glpat-esc-amp-dec`).
* line 93 ("except the `n` of a JSON `\n` escape") and line 117 ("other than a JSON `\n` escape"):
  same falsification. **Line 93 and line 117 are already repaired in the uncommitted worktree**
  (a sibling seat is mid-edit); line 29, 100 and 238 are not.
* Not false but incomplete: `capture-intake-gate.md:246` says "thirteen at round 92" (round-scoped,
  reads as current; now 14) and `:105` says "now returns twelve" (already false since round 92,
  pre-existing, not attributable to this landing).

**D2 — low: citation off-by-one in the docstring and the counter.** Docstring line 108 says
"other GitLab token prefixes (S139 line 86 names only `glpat-`)" and `CLAUSES` repeats
"(S139 line 86)" twice (19-character and bare-prefix clauses). `glpat-` is on **line 87**; line 86
only carries the lead-in. The scanner's own gitlab-pat entry is correct ("S139 lines 86-87");
the limit sentence and the counter clause titles are not.

**D3 — low, coverage: the `&#xXX;` escape form is unpinned.** The statement names seven escape
forms; six are pinned by the selftest (all but the hex entity) and five also by K4. `&#x` occurs
**zero** times in `.ufo/waves/round-93/c2/capability-check.py` and only in the scanner's docstring;
no selftest case, no K4 plant and no K7 negative exercises `&#x26;`. My probe
`glpat-esc-amp-hex` and `gh-esc-amp`-family show the branch works, so this is a missing regression
pin, not a broken clause.

**D4 — low: K8's own docstring is stale, and K8 has no GitLab left-boundary plant.** The K8 doc line
says "every clause of the frozen round-92 C2 statement (and the round-91 clauses, kept as
regression)" while the dict carries 50 clauses including the round-93 ones; K8's gitlab clauses
cover length boundaries, bare prefix, case and `glrt-`, but no "letter/`_`/`-` immediately before
`glpat-`" plant — that boundary is pinned only by the selftest (`gl-pat-letter-before`) and K7
(`live-n14`-class negatives). No predicate impact (`K8 clauses=50 failing=none`).

Non-findings checked and cleared: the `gitlab-pat` alphabet is a documented lane choice;
`_GH_LB = _ESC_LB` is a strict widening (no round-87..92 shape can be lost); the SCORECARD row is
byte-identical to the frozen candidate row; K7 plants live in a `mkdtemp` directory with run-time
random values (so the statement's "run-time nonce directory" reading is satisfied for K4 by
`reroot`, and for K7 by the random repo root plus random values).

## 5. Reanchor table

Enumeration (`grep -rlE 'capture-secret-scan\.py:[0-9]' corpus/knowledge` at the landing commit) —
five entries cite the scanner by line:

| Entry | distinct full-path ranges | moved by the landing |
|---|---|---|
| `corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md` | 27 | 22 |
| `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` | 19 | 13 |
| `corpus/knowledge/capture-intake-gate.md` | 17 | 13 |
| `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md` | 16 | 11 |
| `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md` | 3 | 1 |
| **total** | **82** (102 occurrences) | **60** |

`reanchor-r93.tsv` (this directory) is the machine-readable table: `path`, `old` (bounds as
committed at the landing), `new` (where the same content lives after the landing), `quote` (the
first line of the old target, so each row is checkable without trusting the arithmetic). Bounds
inside the three replaced docstring regions are anchored by best-match of the cited old line
against the replacement block, not by a flat offset — e.g. old `96` (the GCS line of the known
limits) → new `109`, not `107`, because the GitLab limit lines were inserted above it. Two
docstring substitutions are structural and called out for the writer:

* `github-prefixed…:156` (`_GH_LB = …`) → `169-170`: the definition split into `_ESC_LB` plus the
  `_GH_LB = _ESC_LB` alias.
* `…:186-195` (capture-intake-gate, "`patterns()` … now returns twelve") → `204-213`; the number in
  that sentence is stale for a second reason (D1, pre-existing).

One range is excluded because it is pinned to another revision, not to the landing:
`cloud-signed-cookies…:86` and `:96` cite `:115` "at `bb4309fff…`" / "of the base revision"
(the round-90 `_PARAM`), so no arithmetic reanchor applies.

Bare `:N` continuation refs (they resolve to the scanner only through the surrounding sentence) are
separated into `bare-ref-citations.txt`: 112 of them across the five entries, of which **35** carry
the token their sentence names inside the cited old range (verified shifts, e.g. `:214-221` →
`:232-239`, `:256-268` → `:274-286`, `:265` → `:283`), **76** do not and are candidate
**pre-existing** drift that no shift explains (e.g. `capture-intake-gate:115` cites `:132-133` for
the GCS bounds while the GCS pattern is at old `147-148`; `cloud-signed-url:85` cites `:289`,
`:296`, `:305`, `:306` for selftest cases that sit at old `313` (`gcs-short`), `320`
(`azure-short-sig`), `329` (`cf-short-sig`), `330` (`cf-lowercase-names`)), and **1** is pinned to
`bb4309`. Those 76 need content-based reanchoring (search the new file for the named
case/identifier), not arithmetic — the reanchor owner should not "fix" them by adding an offset.

## 6. Residual risk and verification gaps

* The 76 pre-stale bare refs are a knowledge-layer debt that predates round 93 and partly predates
  round 92; this landing neither created nor closed them, but every one of them is now one hop
  further from correct.
* D3 leaves one statement-named escape form (`&#xXX;`) with no committed regression pin; a future
  edit could delete it with every limb still green.
* K8 verifies clause→plant mapping against `PLANTS`, i.e. against fixtures the counter authored; it
  cannot detect a clause whose *statement* text is wrong (which is how D2 survived).
* I did not run the round-87..91 counters (their scripts pin old instrument shas and belong to
  those rounds' receipts); the "otherwise unchanged" limb rests on K2/K3/K6 plus the selftest and
  my probe differential.
* Knowledge files are being edited by a sibling seat in the worktree; everything above was measured
  on the committed blobs at `9225954`, not on the worktree, and the worktree's partial repairs are
  noted only where they intersect D1.

## Receipts

All under `.ufo/waves/round-93/w1/ReviewC2Scanner-receipts/`; every command ran with
`cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin` and `TMPDIR=/fast/scratch/hyaku/kasegi-r93/ReviewC2Scanner`.

| Command (abridged) | Observed | rc |
|---|---|---|
| `git log --oneline -1` / `git status --porcelain` | HEAD `9225954`; 6 modified paths, none of them the landing's two | 0 |
| `git show --stat 9225954` | `SCORECARD.md` 2 +-; `capture-secret-scan.py` 51 +++-; 47 insertions, 6 deletions | 0 |
| `git diff-tree --no-commit-id --name-status -r 9225954` | `M SCORECARD.md`, `M corpus/instruments/capture-secret-scan.py` | 0 |
| `git show 9225954:…capture-secret-scan.py \| sha256sum` | `7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5` (= frozen candidate) | 0 |
| `sha256sum .ufo/waves/round-93/c2/capability-check.py` | `8a4ad5081cb21d9afb80e83f490b51df2e3a7fb6211a4e9e91a69c456d751bb6` (= frozen) | 0 |
| `sha256sum .ufo/waves/round-93/c2/candidate-row.txt` | `6d18d57978f3ae8e45da85fcf9ef6cdf2a523f1ec50955c7d496e85741e3fb40` (= frozen); landed row byte-identical, last cell `87` | 0 |
| `sha256sum corpus/source-snapshots/round-93/S139.txt` | `154a7e15…1b188` (= manifest); `grep -n glpat` → `87:` only; alphabet grep → no match | 0 |
| `python3 -B corpus/instruments/capture-secret-scan.py --selftest` | `SELFTEST-RESULT pass cases=90`; `grep -c '^SELFTEST gh-'` → 26 | 0 |
| `python3 -B .ufo/waves/round-93/c2/capability-check.py --lane . --rev 9225954… --work $S/c1 --instrument-sha256 7d9d73… --gate-sha256 8b6f84…` | `CAPABILITY-CHECK-RESULT pass rc=0`, seed 4048092494, nonce 39b49f7c, K1–K8 pass, `K8 clauses=50` | 0 |
| same, `--seed 1` | pass, nonce 7510f161, K1–K8 pass | 0 |
| same, `--seed 9191` | pass, nonce 1bb8b414, K1–K8 pass | 0 |
| scratch probe harness (`importlib` load of the landed scanner; 32 fixtures) | `PROBE-RESULT pass cases=32 bad=0` — 20 gitlab boundary/escape/negative cases, 8 github escape/negative cases, `gh-stateless`, `gcs`, `aws` regression | 0 |
| `grep -c '&#x' corpus/instruments/capture-secret-scan.py .ufo/waves/round-93/c2/capability-check.py` | `1` (docstring only) / `0` (no counter fixture) → D3 | 0 |
| `git grep -lE 'capture-secret-scan\.py:[0-9]' 9225954 -- corpus/knowledge` | 5 files (`knowledge-citations.txt`); 102 occurrences, 82 distinct ranges | 0 |
| difflib old↔new line map of the scanner (`9225954^` → `9225954`) | 418 → 459 lines; replaced regions at old 88-89, 96, 156, 195; 60 ranges moved → `reanchor-r93.tsv` | 0 |
| bare `:N` census over the same five blobs | 112 refs: 35 verified, 76 candidate pre-existing drift, 1 pinned to `bb4309` → `bare-ref-citations.txt` | 0 |
| `grep -n 'cases=68\|fifteen' corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md` | lines 100 and 238 → D1 | 0 |

Scratch (`/fast/scratch/hyaku/kasegi-r93/ReviewC2Scanner`) removed by the seat's EXIT trap; nothing
of this seat lives outside the report and the receipts directory.
