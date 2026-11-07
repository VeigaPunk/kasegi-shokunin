# ReviewC2Scanner — round 96, C2 `capture-secret-scan` (GitLab routable/versioned + `glptt-`)

Seat: `ReviewC2Scanner`, leaf. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6`, freeze `804e7bc3`, C2 landing
`7ef1d365eb523a83b2567342a6c0f585ab028ab0`.
Instrument under review: `corpus/instruments/capture-secret-scan.py`, worktree sha256
`71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9` — equal to the frozen
`instrument_sha256` and to `git show 7ef1d36:...` (receipts 02).

## Verdict

**APPROVE.** Every clause of the frozen C2 statement that the counter binds (K1–K6) re-derives
at the landing, and I re-derived the seven shape grammars directly against S140 rather than
through the counter. Four findings are routed defects/qualifiers, none of which re-scores C2:
F2 is the only one that touches the statement's own prose ("keeps the rest") and is a one-line
docstring repair.

## Clause-by-clause (re-derived, not read off the counter)

| Clause | Evidence | Result |
|---|---|---|
| seven shapes exist, named as claimed | `capture-secret-scan.py:247-254`; diff hunk `@@ -221,7 +239,19 @@` | 7 patterns added: `gitlab-pat-versioned`, `gitlab-pat-routable`, `gitlab-runner-auth-token-versioned`, `gitlab-deploy-token-versioned`, `gitlab-agent-token-versioned`, `gitlab-workspace-token-versioned`, `gitlab-pipeline-trigger-token` |
| scope is exactly S140's published set | `grep -nE '0-9a-z\]\{2\}\[' S140.txt` → only lines 30, 51, 136, 324, 358, 375 (receipt 04) | S140 publishes **no other** routable/versioned tail (30 GitLab rules total); the seven-shape scope is complete, not a sample |
| `glpat-` routable = head 27-300 + `.` + 2 lower alnum + 7 (S140:30) | `_GJ_ROUTABLE` at `:243` = `[A-Za-z0-9_-]{27,300}\.[0-9a-z]{2}[0-9a-z]{7}(?![A-Za-z0-9_])` | identical grammar; probe: head 26 no / 27 yes / 300 yes / 301 no; tail `2+6` no, `2+8` no, upper no |
| `glpat-` versioned = head 27-300 + `.` + 2 + `.` + 2 + 7 (S140:51) | `_GJ_VER` at `:242` | identical; probe: head 26 no / 27 yes / 301 no; tail `2+.+2+6` no, `2+.+1+7` no |
| routable cannot match a versioned token and vice versa | probe rows `routable token: no versioned hit`, `versioned token: no routable hit` | holds structurally (the head class excludes `.`, the routable tail class excludes `.`) and empirically |
| `glrt-`/`glrtr-`, `gldt-`, `glagent-`, `glwt-` versioned (S140:136/324/358/375) | `:249-252` | all four use `_GJ_VER`; `glrtr?-` covers both prefixes as S140:136 does |
| `glptt-` exactly 20 or exactly 40 (S140:73) | `:253-254` | probe: 19 no, 20 yes, 21 no, 39 no, 40 yes, 41 no |
| left boundary on each shape | `_GL_LB` at `:237`, applied to all seven | `(?<![A-Za-z0-9_])` ≡ S140's leading `\b` for a following word char, plus the instrument's pre-existing escape-terminator alternatives (`\n`, `\uXXXX`, `%XX`, `&#NN;`, `&#xNN;`); probe: word char before → no hit, start/space/slash/`\n`/`%2D` → hit |
| optional custom prefix | `_GL_PREFIX` at `:238` | on six of seven shapes — see **F1** for the seventh |
| no new shape fires on a plain 20-char `glpat-`/`gldt-` token | probe rows `plain glpat-20`, `plain gldt-20`, `plain glrtr-20` | only the pre-existing 20-char shapes fire; no overlap |
| selftest 115 → 128 | receipt 05 (`cases=128`, rc 0) and receipt 10 (base `cases=115`, rc 0) | +13 cases at `:439-451`, exactly the 13 added tuples |
| `--rev` at the landing is clean | receipt 06 | `scanned=2744 hits=0 files=0 allowed=27 unused_allow=0 rc=0` |
| counter K1–K6 at the landing | receipt 12, fresh seed 1200305022 | `CAPABILITY-CHECK-RESULT pass rc=0`; K1 pin-ok/cases=128, K3 hits=7 missing=none extra=none, K4 base_new_shape_hits=0, K5 rows=1 last=87, K6 aws-sts-session-token present |
| SCORECARD row | receipt 11 | exactly one `| capture-secret-scan |` row, last cell `87`, names `gitlab-pat-versioned`, `gitlab-pat-routable`, `gitlab-pipeline-trigger-token` and "round 96" |

## Findings

### F1 — `gitlab-runner-auth-token-versioned` omits the optional custom prefix (low, consistency)

`capture-secret-scan.py:249` is `_GL_LB + rb"glrtr?-" + _GJ_VER`. S140:136 publishes
`(?:[a-zA-Z0-9]{1,20}-)?glrtr?-…`, and the other six round-96 shapes — and the pre-existing
`gitlab-runner-auth-token` at `:256` — all carry `_GL_PREFIX`.

Impact is **not** a detection gap: a custom instance prefix always ends in `-`, which satisfies
`_GL_LB`'s `(?<![A-Za-z0-9_])`, so `abc-glrtr-…` is still reported (probe row
`prefixed glrtr versioned` → `gitlab-runner-auth-token-versioned`). The divergence is the
**matched span**: `m.group(0)` starts at `glrtr-`, not at the prefix (receipt 09:
`runner-versioned prefixed span=b'glrtr-AAAA…' starts_with_prefix=False`, against
`deploy-versioned`/`pat-versioned` `starts_with_prefix=True`). Since `scan_bytes` keys the
allowlist on `sha256(m.group(0))` (`:312`), an allowlist row for a prefixed runner token would
have to hash the unprefixed span — a different convention from every sibling shape. No live row
is affected (`unused_allow=0`, `allowed=27`).

Command: `python3 -B probe3.py` (receipt 09).

### F2 — the known-limits rewrite drops the `glagent-` 50-character form without detecting it (low; the only statement-prose divergence)

The frozen statement says the known-limits list "drops the six families this round detects and
keeps the rest". Accounting the old list against the new one (`:159-166`):

- dropped and **justified** (now detected): `glptt-` (S140:73 → 20/40 shape), `glwt-` (S140:375
  → versioned shape), the `glpat-`/`gldt-`/`glrt-`/`glrtr-` routable clause (S140:30/51/136/324).
- dropped and **not** justified: `glagent-` cited **S140:213**, which is
  `gitlab_kubernetes_agent_token` = `glagent-[0-9a-zA-Z_\-]{50}` — a *different* family from the
  versioned rule at S140:358 that this round detects. A plain 50-character `glagent-` token
  produces no hit (receipt 07 row `glagent-50 (S140:213) ok got=none`), and `glagent-` no longer
  appears in the known-limits list (`:161` lists only `glft-`, `glimt-`, `glsoat-`, `glffct-`,
  `gloas-`, `glrct-`). An undetected published shape is now undisclosed.

This does not re-score C2: K1–K6 bind no docstring content. If the L1 wants the statement's
"keeps the rest" to hold literally, the repair is to re-add `glagent-` (S140 line 213) beside
`glft-` — one clause, no behaviour change.

Command: `python3 -B probe.py` (receipt 07) + `grep -nE '^regex' S140.txt` (receipt 04).

### F3 — the new `/trigger/pipeline?…token=` known-limit entry is inaccurate (very low, docstring)

`:165-166` lists "the `/trigger/pipeline?...token=` URL form (S140 line 532)" as a known limit.
The GitLab-specific shape is indeed absent, but the generic `credential` shape
(`claim-package-check.py:140`, `\b(?:api[_-]?key|secret|token|password)\b…[A-Za-z0-9_\-]{16,}`)
fires on `token=<30 hex>` (receipt 08: `/trigger/pipeline?token= (S140:532)  credential`). The
secret is still reported, so the entry overstates the limit. The other four new entries are
accurate as written (receipt 08: `GR1348941+20`, `feed_token=`, `gitlab+deploy-token-N:`, bare
`t1_` all `none`; `feed_token=` escapes `credential` because `_` is a word char, so `\btoken`
does not match inside it).

### F4 — boundary negatives cover only `glpat-` and `glptt-` (very low, fixture coverage)

The 13 new selftest cases (`:439-451`) give head/tail negatives only for `glpat-`
(`-short-head`, `-upper-tail`, `-one-char`) and `glptt-` (`19`, `39`). The four other versioned
shapes have positives only; the counter's plant negatives add `glwt-` short tail (n5) and
`glagent-` upper middle (n6), leaving `glrtr-` and `gldt-` with no boundary negative in either
set. I supplied the missing bounds myself (receipt 07: `prefixed glrt versioned`,
`prefixed gldt versioned`, and the shared `_GJ_VER` grammar is exercised by the `glpat-` tail
negatives), so this is a fixture-set gap, not an unverified behaviour.

## Residual risk and verification gaps

1. **F2 is the one statement clause the counter cannot see.** C2's verdict rests on K1–K6; the
   docstring clause is prose. A reviewer who reads "keeps the rest" as a limb would score C2
   NOT VERIFIED on F2 alone. I do not, because the frozen predicate is K1–K6 and the rules bind
   verdicts to the predicate — but the L1 should record F2 as a statement qualifier or take the
   one-line repair.
2. **The left boundary is wider than S140's `\b`** on the escape-terminator alternatives
   (`_GL_LB:237`). This is the instrument's round-93 convention, is shared with `_GH_LB`/`_ESC_LB`,
   and is selftest-covered; it admits a match after `%2D`/`\n`/`&#38;` where S140 would not. Not a
   round-96 regression, and the claim's docstring says "escape-terminator left boundary".
3. **`_GJ_ROUTABLE`/`_GJ_VER` end with `(?![A-Za-z0-9_])` rather than `\b`.** Equivalent here
   (both reject a following word char and both admit `-`/`.`); verified by the `2+8` and upper-tail
   negatives.
4. **`--rev` cost**: 2744 files in ~24 s. No backtracking pathology observed on 300-character
   heads.
5. **Not re-run**: the C1 limbs (out of this seat's scope) and the pre-freeze K1–K6 receipt at the
   scratch candidate `b31227ca`; I ran the counter at the landing instead, at a fresh seed.

## Receipts

All under `.ufo/waves/round-96/w1/ReviewC2Scanner-receipts/`. Working dir
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; scratch `TMPDIR=/fast/scratch/hyaku/kasegi-r96/ReviewC2Scanner`.

| # | Command | Observed |
|---|---|---|
| 01 | `git log --oneline -3`; `git status --porcelain \| head -20` | HEAD `7ef1d36`, then `3c0581e`, `804e7bc`; only untracked wave scaffolding |
| 02 | `sha256sum corpus/instruments/capture-secret-scan.py`; `git show 7ef1d36:… \| sha256sum` | both `71876619…48ac9` = frozen pin |
| 03 | `git diff d8a2bb0 7ef1d36 -- corpus/instruments/capture-secret-scan.py` | 88 lines, 4 hunks (docstring, known limits, patterns, selftest) |
| 04 | `grep -nE '^regex' S140.txt \| grep -E '^(30\|51\|73\|136\|213\|324\|358\|375):'`; `grep -nE '0-9a-z\]\{2\}\[' S140.txt`; `grep -cE '^id = "gitlab' S140.txt` | the eight cited regexes verbatim; only six lines carry a routable/versioned tail; 30 GitLab rules |
| 05 | `python3 -B corpus/instruments/capture-secret-scan.py --selftest` | `SELFTEST-RESULT pass cases=128`, rc 0 |
| 06 | `python3 -B corpus/instruments/capture-secret-scan.py --lane . --rev 7ef1d365eb523a83b2567342a6c0f585ab028ab0` | `scanned=2744 hits=0 files=0 allowed=27 unused_allow=0 rc=0`, rc 0 |
| 07 | `python3 -B probe.py` (37 boundary assertions against `patterns()`) | `PROBE pass`, rc 0 |
| 08 | `python3 -B probe2.py` (the five new known-limit entries + `glagent-50`) | four `none`; `/trigger/pipeline?token=` → `credential` |
| 09 | `python3 -B probe3.py` (matched span of prefixed versioned shapes) | runner span excludes `abc-`; deploy/pat include it |
| 10 | `python3 -B base/capture-secret-scan.py --selftest` (round-95 tip extracted to scratch with `claim-package-check.py` beside it) | `SELFTEST-RESULT pass cases=115`, rc 0 |
| 11 | `git show 7ef1d36:SCORECARD.md \| sed -n 307p` | one row, last cell `87`, names the round-96 shapes |
| 12 | `python3 -B .ufo/waves/round-96/c2/capability-check.py --lane . --rev 7ef1d36… --work <scratch> --instrument-sha256 71876619… --gate-sha256 8b6f8493…` | `CAPABILITY-CHECK-RESULT pass rc=0`, seed 1200305022, K1–K6 ok |

No tool was installed or upgraded for this seat; no git/jj mutation was performed; nothing was
written outside this report and its receipts directory.
