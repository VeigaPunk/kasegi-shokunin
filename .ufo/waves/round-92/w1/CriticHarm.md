# CriticHarm — round 92 attempt 1 (attack seat): harm audit, base vs tip

Base `0628fd247914555838a42c02ba5d4ac08b7e095d` · freeze `9e4f0d68` · C1 landing `cb1ef2b9` ·
C2 landing `58c0c115` · tip `ee830069`. Lane repo cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Everything below was read-only in the lane; receipts in `CriticHarm-receipts/`.

**Axes this seat can touch:** `depth:verifiability` (C1, via resolved-citation class movement and
anchor fit) and `coverage` (C2, via false positives, ReDoS cost, and survival of the round-91/90
capabilities). Verdicts are routed defects/qualifiers only — no re-scoring; the claims stand or fall
on their own frozen predicates, which I reproduced and which pass.

## Verdict per assignment item

| # | Item | Verdict |
|---|---|---|
| 1 | depth:density, SKILL.md base vs tip | **NO HARM** — SKILL.md byte-identical (`7d082bfe…` both); density census identical (mean 273.2, 932 path cites, 38 blocks); the round diff touches no SKILL.md path |
| 2 | false positives of the landed scanner / new `github-token` shape | **NO HARM** — K3 reproduced `scanned=1882 hits=0`; `--files` over 218 snapshot+knowledge working-tree files `hits=0`; widened 357-md run: 2 hits, both old AWS shapes in a round-87 lesson (pre-existing, outside capture scope), **zero `github-token` hits** anywhere |
| 3 | ReDoS of `github-token` | **NO HARM** — worst 113.5 ms/MB cold, steady state 25–35 µs/KB and flat 1→8 MB (linear); no nested quantifier |
| 4 | old capabilities | **NO HARM** — round-91 counter unpinned at `58c0c115`: K1–K8 pass (`clauses=13`); instrument `--selftest` `pass cases=68`; dependent intake gate G1–G6 pass at tip |
| 5 | C1 harm: INTERNAL→GONE or meaning change | **NO HARM on class** (0 resolved citations lost; 13 INTERNAL tokens entered, 16 GONE-only tokens left, net denominator −3), **two routed defects** on anchor fit (below) |

## Ground truth reproduced (independent of the landing receipts)

- C1 P3: `git diff-tree -r cb1ef2b9` = exactly the two knowledge paths; numstat 24/24 and 1/1 ⇒
  line counts unchanged (487, 76) ⇒ no site moved.
- C1 meter (own run, `--work` scratch): `KNOWLEDGE-METER base=947/1947 after=960/1944`, M0/M1/M3/
  M4/M5/M6/M9/M10 pass, `rc=0`; M9 `rows=25 unbound=none`; M10 `labelled=30 want=25 mapped=25`.
- C1 class differential: 24 triage lines + 1 root-loss line changed, nothing else; every added
  token classifies `INTERNAL` under the lane's own `resolve.py`; no token that was
  `RESOLVES/INTERNAL/MIRROR-EQUIVALENT` at base is absent/downgraded after.
- C2 P3: `git diff-tree -r 58c0c115` = `SCORECARD.md` + `corpus/instruments/capture-secret-scan.py`;
  the row keeps every prior shape name and adds the `github-token` clause.
- C2 K3 summary reproduced exactly (`scanned=1882 hits=0 files=0 allowed=20 unused_allow=0`), so the
  allowlist was fully consumed and no new shape changed an allow decision.

## Routed findings (defects / qualifiers, with re-runnable commands)

Classification: F1 is a **fixable label defect upstream of the claim** — C1's M9 binds the edit to
the label's own "keep `SKILL.md:117`", so the canonical judge must accept C1 and the repair belongs
to a round-93 label; F2/F6 are **qualifiers** to an otherwise correct edit; F3 is a **disclosed,
justified tradeoff** (not a rejection); F4/F5 are **record/process debts** the landings are forbidden
to fix (P3) and the round must schedule; F7 is out of scope for this round. No finding rejects
either frozen claim on its own predicates.

### F1 — two landed cells certify a `MATCHES` anchor that does not match (false provenance)
Rows `corpus/knowledge/triage-thresholds.md:58` (attempts exhausted) and `:144` (`MAX_ATTEMPTS`)
now read `MATCHES: \`SKILL.md:117\`` as their only tie. `SKILL.md:117` is a provenance block:

    sed -n '117p' SKILL.md
    → "`[lost-tree] claims/hackerone-anthropic/honest-zero-claude-code/provenance.json:29`,"

The lane's actual statement is elsewhere, and `MAX_ATTEMPTS` does not occur in SKILL.md at all:

    sed -n '191p' SKILL.md      → "status-file TERMINAL + telemetry `attempts()>=2`."
    grep -c MAX_ATTEMPTS SKILL.md → 0

The token was already on those lines at base, so the edit did not *introduce* it; but the tranche's
pair-bound meter (M9) certifies the edit while resolution (not anchor content) is what it measures,
so the cell is now the sole "support" for an unsupported claim. Impacted axis: `depth:verifiability`.
Smallest safe correction: a **round-93 label** for both pairs (repoint to `SKILL.md:191` or drop the
tie); no post-landing edit under the frozen map.

### F2 — six repointed cells say `MATCHES` where the anchor is only partial
`:86`, `:87` (no `id ∈ priority[]` predicate, no `{priority:[]}` default), `:149`/`:153` (no 30 s
tick, no UTC−3 formula), `:150` (entry names 8 `SYNC_PATHS` groups, the row lists 11 entries),
`:152` (15-min window stated, 20000-char tail not). The labels' own `fix` cells say "Partial:";
the landed cell text does not. Base anchors were unrelated sections (`mission-control.md:36-38`,
`:42-46`, `:40-45`, `intake-surface.md:71`), so this is a net improvement, not a regression.
Impacted axis: `depth:verifiability`. Smallest safe correction: a `Partial:` marker (or split tie
tokens) in the next tranche; do not widen the claim.

### F3 — row `:155` changes relation `SUPERSEDES` → `MATCHES` (disclosed, justified)
`mission-control.md:56-57` now states `openai-codex/gpt-6-astra:max` with the round-13 correction
("earlier text said `openai-oauth/`"), so `MATCHES` is true; errata row 9.6 at `triage:438`
(EXCLUDED, unchanged) keeps the audit-time `openai-oauth` record and `LOG.md:340` /
`corpus/README.md:145` keep the correction history. Impacted axis: `depth:verifiability`.
Smallest safe correction: none; recorded so the relation change is not mistaken for an identity
change later. `:249` (`— (new; …covers the regex only)` → `MATCHES: claim-gates.md:52-56`) and
`:369/:370` (unsupported `MATCHES` → `—`, no anchor states `deadline`/`duration_p90` types) are
likewise correct in direction and disclosed.

### F4 — the frozen C1 landing adds drift to the already-stale census of record (process, not claim)
`corpus/instruments/citation-survival.tsv` still carries `mission-control.md:20-21  GONE
nfiles=1 occurrences=4` (line 3011), whose literal no longer occurs anywhere in `SKILL.md`+`corpus`
(`grep -rF -c` → 0), and it lacks the 13 new `corpus/knowledge/…` tokens. `census-freshness-check.py`
compares committed bytes to a fresh `resolve.py` run and exits 1 on any difference, so it cannot read
`ok` until the round regenerates the census. Last regeneration is round 57 (`e300ad5`); SCORECARD
already carries "census of record … not regenerated" as debt, and C1 P3 forbids the landing from
touching it. Impacted axis: `depth:verifiability` (record, not measurement). Smallest safe
correction: a scheduled round-end census regeneration on the final tree; no landing edit.

### F5 — dependent capability `capture-intake-gate` pin now stale by design (pre-existing + 1)
`capture-source.py` imports the scanner's patterns (shape-agnostic: no literal shape names, so the
new shape propagates as a plain refusal). The round-90 counter, run unpinned at tip, reports
`G0 FAIL missing=cloudfront-signed-cookie-signature,github-token` while **G1–G6 pass** — G0 is the
derived-plant-set limb, red since the round-91 cookie shape (`1dd0723`) and one name larger now.
The SCORECARD row's recorded command pins instrument `0630d32b…` and is knowingly stale ("pins hold
until the instrument next changes"). Impacted axis: `coverage` (record only). Smallest safe
correction: re-derive that row's counter on the next intake-gate exercise; no behaviour change needed.

### F6 — C2 SCORECARD row does not carry the named known limit (documentation note)
The row's `github-token` clause names the positive forms and the `ghs_<APPID>_<JWT>` placeholder but
not the fine-grained `github_pat_` limit; the instrument docstring records it with its source
(`capture-secret-scan.py:95`, S136 line 163), and the row has no `limits:` cell at all, so this is
consistent with the row's existing style rather than a gap the claim made. Impacted axis: `coverage`.
Smallest safe correction: optional `limits:` clause in a later row edit.

### F7 — pre-existing scanner hit outside capture scope (not this round)
`corpus/lessons/round-87-verifier-spotcheck.md:61,:67` yield `aws-sts-session-token` and
`aws-access-key-id` under `--files` (the lesson quotes the oracle grep); unchanged at base and tip,
not a `github-token` hit, and `corpus/lessons/` is not capture scope, so K3 never sees it. No action
for this round; recorded so the two hits are not attributed to C2.

## Counterexamples tested and rejected

- *"A qualified citation could still be GONE at the scope's resolve root."* No: `resolve.py`
  `classify()` joins the token to the lane root, and every new `corpus/knowledge/<name>.md:N[-M]`
  resolves inside the landing tree and inside its file's bounds (M5 pass; verified line counts).
- *"Dropping ties inflates the rate."* Over the two edited files, 16 distinct tokens leave and 13
  enter (triage 648→645 distinct, rootloss 42→42); every one of the 16 was GONE at base and every
  one of the 13 is INTERNAL after, so the net denominator −3 is all GONE-only and the numerator +13
  is all repair, not reclassification. Removal-driven share of the rate: 960/1947 = 49.31 % vs
  960/1944 = 49.38 %, i.e. 0.07 pp of the 0.74 pp.
- *"The stateless arm backtracks."* Flat 25–35 µs/KB from 1 MB to 8 MB on `ghs_1_`+a-run,
  `a.` storms, 20k-prefix buffers and dot storms; the pattern has no nested quantifier.
- *"The new shape double-flags already-allowed values."* `unused_allow=0` with `allowed=20` in K3,
  so every allowlist row still binds exactly as before.

## Files written
- `.ufo/waves/round-92/w1/CriticHarm.md` (this report)
- `.ufo/waves/round-92/w1/CriticHarm-receipts/density.txt`
- `.ufo/waves/round-92/w1/CriticHarm-receipts/false-positives.txt`
- `.ufo/waves/round-92/w1/CriticHarm-receipts/redos.txt`
- `.ufo/waves/round-92/w1/CriticHarm-receipts/old-capabilities.txt`
- `.ufo/waves/round-92/w1/CriticHarm-receipts/c1-class-diff.txt`
- `.ufo/waves/round-92/w1/CriticHarm-receipts/c1-anchor-support.txt`
- `.ufo/waves/round-92/w1/CriticHarm-receipts/landings.txt`

No lane file outside `w1/` was written; no git/jj write was issued; no subagent was spawned; no
package manager or tool install ran. Scratch `/fast/scratch/hyaku/kasegi-r92/CriticHarm` is deleted
(`trap … EXIT`), and no fixture, planted value or scanner/counter/snapshot copy was written into
`w1/`; receipts carry sha256 digests and scanner summary/HIT path+line lines only, never a value.
