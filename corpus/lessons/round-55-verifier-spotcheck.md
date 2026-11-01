author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# Round 55 non-author verifier spot-check — kasegi

Verdict: **ok / admitted**. Both declared claims re-derive from committed bytes and live
re-opens; no owned axis is harmed. One NEW status-neutral defect found (DF-3 below —
`CENSUS-FRESH=ok` prose contradicted by the receipt it cites) and routed for round 56; it does
not bar admission (the claims themselves verify; per the gate standard a red gate limb is a
conformance defect, never the marker predicate). Lane HEAD `133c575394099abf28ddf1b0125c53aefde3e0fa`
(branch `master`, pushed), base `ed60637394b170a4120fda501b9b9c5387f2df24`. All commands below
were run by this verifier (index-free git only: `rev-parse`, `cat-file`, `ls-tree`, `diff-tree`,
`merge-base --is-ancestor`, `show`, `log`; the lane-local instruments were run from the lane
root after hash-verifying each input file matched the tip).

## 1. Step-1 conformance

| Check | Command (abridged) | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-55/kasegi.md` | `kasegi-shokunin <kasegi@shokunin.local> 65ef7717a9a372886acb80c6324d4b51a77f1251` | PASS |
| `SHONEN` heading in committed report bytes | `git show 65ef7717:.ufo/reports/round-55/kasegi.md \| grep -n '^## SHONEN'` | line 127: `## SHONEN`, 4 box lines (`[~]`/`[ ]`/`[~]`/`[~]`) | PASS |
| Cited commits exist | `git cat-file -t` over fd7838c, d0237d6, 00832d2, d9d77ec, 133c575, ed60637, cfdf059, 5108584 | all `commit` | PASS |
| Cited commits are ancestors of the tip | `git merge-base --is-ancestor <h> refs/heads/master` | all OK | PASS |
| Round work reachable | `git log ed60637..133c575` | exactly the 5 commits: fd7838c (freeze) → d0237d6 (carry-in) → 00832d2 (C1) → d9d77ec (C2) → 133c575 (results), all `kasegi-shokunin` identity | PASS |
| Branch tip pushed | `git ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `133c575394099abf28ddf1b0125c53aefde3e0fa` | PASS |
| Dispatch/complete digest | `grep 'round=55' .ufo/watchdog.log` | `2026-11-01T02:09:41-08:00 launch kasegi round=55 base=ed60637394b1` / `2026-11-01T04:23:38-08:00 complete kasegi round=55 head=133c57539409 pushed=True` — matches the orchestrator digest verbatim | PASS |
| Landed-changes table vs commit path lists | `git diff-tree -r --name-status <c>^ <c>` per commit | all five path lists match the report's table exactly (incl. the census pair `citation-survival.md`/`.tsv` named under 133c575 as "census pair regenerated") | PASS |
| Append-only discipline | `diff-tree --numstat` base..tip | LOG.md 48/0, SCORECARD.md 58/0, PROVINCE.md 2/0, README.md 29/0, SOURCES.md 3/0, knowledge-expected.txt 1/0; SKILL.md untouched | PASS |
| Report is not a marker | report content | names real work, evidence pointers, and checkable hashes for every change | PASS (real report) |

## 2. Per-claim re-check (all re-measured by this verifier unless noted)

### C1 — depth:verifiability (capability extension, score HELD 4, R58 nominal label) — VERIFIED

| Measurement | Command | Reported | Observed by verifier | Result |
|---|---|---|---|---|
| ledger size before | `git show ed60637…:corpus/instruments/figure-audit-ledger.json \| grep -c '"id"'` | 9 | 9 | PASS |
| new entry ids absent at base | `… \| awk '/figure-audit-mentions-base-scorecard/{n++}…'` (+ r54-fold awk) | 0 / 0 | 0 / 0 | PASS |
| ledger size after | same grep at tip | 17 | 17 | PASS |
| selftest | `python corpus/instruments/figure-audit.py --selftest` (re-run) | cases=5 failures=0 exit 0 | `selftest cases=5 failures=0`, exit 0 | PASS |
| GREEN over lane root | `python corpus/instruments/figure-audit.py` (re-run) | figures=17 ok=17 stale=0 exit 0 | `FIGURE-AUDIT figures=17 ok=17 stale=0 exit=0`, exit 0 | PASS |
| RED control | `python corpus/instruments/figure-audit.py --ledger .ufo/waves/round-55/controls/red-df1-ledger.json` (re-run) | 3 stale exit 1 | `red-df1-scorecard-prose recorded=0 derived=2 stale`, `red-entries-r54-wrong … want=39 stale`, `red-frontier-rows-r54-wrong … want=36 stale` → `figures=3 ok=0 stale=3 exit=1` | PASS (the audit catches both the DF-1 prose class and wrong fold-figures) |
| Green over the truly final tree | receipt `.ufo/waves/round-55/controls/gate-final-r55.txt` last limb (evidence-verified; byte-consistent with my own re-run) | 17/17 exit 0 | receipt prints `FIGURE-AUDIT figures=17 ok=17 stale=0 exit=0` | PASS |

Evidence-verified (committed receipts read, not re-run): `controls/c1-donothing-r55.txt` (base
ledger 9/9 green over the lane root; the discarded export-root draft disclosed inside the
receipt). Score held at 4 with the non-moving metric (the citation census) named — R58 nominal
label applied honestly; no census move claimed.

### Carry-in — DF-2 (regenerated receipt) and DF-1 (R9 erratum) — VERIFIED

- DF-2: `.ufo/waves/round-54/controls/d53-base-greps-r54.txt` exists at the tip (committed
  `d0237d6`). Every limb re-derived by this verifier: the five sha pins reproduce exactly
  (SOURCES@base `06c92e6ae604…`, nvd entry@base `15eb2d05e88d…`, r53 counter receipt
  `be69ece74fcd…`, r53 manifest `eb6ffa6047d2…`, S085 capture `4d1c4e7732e1…`); the four filed
  literals each print exactly 1 at base (`"lines": 543` / `543 lines` ×2 / `34 inherited`); the
  measured values reproduce (S085 = 542 lines / 7590 bytes / `FAIL_entry_records=33` present).
  Every citation of the path now resolves.
- DF-1: the closure check inside `.ufo/waves/round-55/controls/df1-mentions-erratum.md` re-run by
  this verifier → `df1-erratum=closed`, exit 0. Base bytes re-derive: `git show
  32782bd…:SCORECARD.md | grep -n 'figure-audit'` → exactly 2 hits, at :2102 and :2158 (the
  r52-planned/r53-routed sibling text); LOG and knowledge-expected limbs 0/0 as filed; the cited
  r54 receipt (`c1-donothing-r54.txt` lines 12-14) prints `2`. The r54 filed prose was confirmed
  as described (fleet report `.ufo/reports/round-54/kasegi.md:30,:69`; frozen sentence (d) in
  `.ufo/waves/round-54/claims.json:14`). No filed byte edited (erratum is a new file; the red
  control carries the prose AS FILED and reads it stale).

### C2 — coverage (frontier F35 → F36 on S087, score HELD 8, operator-owned denominator) — VERIFIED

| Measurement | Command | Reported | Observed by verifier | Result |
|---|---|---|---|---|
| frontier rows before→after | `git show <rev>:corpus/README.md \| grep -cE '^\| F[0-9]+ \|'` | 35 → 36 | 35 → 36; `F36` lines at base: 0 | PASS |
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` (per rev) | 86 → 87 | 86 → 87 (S087 inserted directly after S086; diff is +3/−0: row + 2 search-log bullets) | PASS |
| knowledge expected/files | `grep -c '^corpus/knowledge/' knowledge-expected.txt`; `git ls-tree -r --name-only tip -- corpus/knowledge \| grep -c '\.md$'` | 73 → 74 / 74 | 73 → 74; 74 files; insert sits before `github-repository-security-advisories.md` (`'-' < '.'`), `LC_ALL=C sort -c` clean (re-run) | PASS |
| frontier counter (after) | `python corpus/instruments/frontier-recheck-count.py` (re-run over lane root) | rows=36 admitted=36 closed=6 problem-rows=30 registry=87; F36 PASS ids=S087; entries=39 pass=6; FAIL 33 invariant | identical, incl. `entries=39 pass=6 exit=1` (exit 1 = the standing disclosed host-bound FAIL class: 30 FAIL rows = problem-rows) | PASS |
| frontier counter (before) | receipt `controls/do-nothing-c2-r55.txt` (evidence-verified; base export) | rows=35 … registry=86; entries=38 pass=5; zero F36 | receipt prints exactly that; base plain counts independently re-derived (35/86, F36=0) | PASS |
| S087 recheck | `python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-55/manifest.json --source S087` (re-run) | sha256 OK + 14 Q-OK each occurrences=1, exit 0 | identical: `S087:sha256 OK` + Q1-Q14 all `OK occurrences=1 anchor=N-ok`, exit 0 | PASS |
| capture bytes | `wc -l/-c`, `sha256sum`, byte-level CR/TAB count (re-run) | 3407 lines / 137738 bytes / sha `3eebdf47…`; 0 CR / 0 TAB | 3407 / 137738 / `3eebdf476fbfe5040ad3367edfe3961fbda1bff412bb74ee43bb08ab2f754b93`; CR=0 TAB=0 (python `rb` count) | PASS |
| LIVE re-open (raw) | `curl -sL -o <scratch> https://docs.github.com/en/rest/security-advisories/repository-advisories` + sha256 | recorded raw: 937712 bytes, sha `89fa9af3…` | HTTP 200, size=937712, sha256 `89fa9af33c38d146bf702b79b9f5fd60ef584ab10ef41b2c165f40be1b1bea8d` — byte-identical to the round's recorded opens | PASS |
| LIVE re-open (instrument) | `python corpus/instruments/capture-source.py --id S087 --url … --out <scratch> --kind html` (re-run into verifier scratch, lane untouched) | snapshot sha `3eebdf47…` | re-capture: status=200, fetched 937712, snapshot 137738, sha `3eebdf47…` — `cmp` vs committed capture: **BYTE-IDENTICAL** | PASS |
| capture-binding | `python corpus/instruments/capture-binding-check.py` (re-run) + before receipt | 69 → records=70 bound=70 unbound=0 exit 0; multi_row_url 7→7 | before receipt: records=69 bound=69, multi_row_url=7; my run: records=70 bound=70 unbound=0, multi_row_url=7, exit 0 | PASS |
| entry claims vs capture | spot reads at the pinned anchors | Q2 carve-out :793; 202 Accepted :2820-2827; states :2194; Q13 :2853 | all four textually present exactly as the entry and README row cite | PASS |
| neighbor screen | receipt `controls/neighbor-screen-r55.txt` (evidence-verified) | URL held by no README/PROVINCE/knowledge row; only F29 neighbor; zero snapshot consumers | receipt shows the lead line as the only SOURCES hit, F29 the only advisories F-row, empty consumer sweeps | PASS |
| stand-in dry-run | receipt `controls/c2-standin-dryrun-r55.txt` (evidence-verified) | v1 (11:21:39Z) fail recorded, v2 (11:23:07Z) green of-record | receipt header carries the v1 `manifest-unreadable` note and v2's green `rows=36 … registry=87` | PASS |

Score held at 8 with the operator-owned denominator named; the moved measure is the frontier
count 35 → 36, not the coverage score — recorded, not gamed.

## 3. NEW defect found by this closure (routed, status-neutral) — DF-3

**DF-3 — `CENSUS-FRESH=ok` prose contradicted by the receipt it cites (the DF-1 class, recurring
in the round that fixed it).**

- The report (Sources & frontier) and the SCORECARD round-55 section state the gate receipt
  `.ufo/waves/round-55/controls/gate-final-r55.txt` reads `CENSUS-FRESH=ok`. The committed
  receipt bytes print **`CENSUS-FRESH=stale files=citation-survival.md+citation-survival.tsv …`
  `[exit=1]`**. This verifier re-ran `python corpus/instruments/census-freshness-check.py .` at
  the tip: `CENSUS-FRESH=stale`, exit 1 — reproduced.
- Root cause (harmless in kind, real in fact): the round-55 lesson cites the receipt path
  `.ufo/waves/round-55/controls/gate-final-r55.txt`; the committed census pair was generated
  BEFORE the receipt file existed, so the pair counts that path GONE. Once the receipt exists, a
  regen counts it INTERNAL. This verifier's regen diff is exactly one citation:
  GONE 3883 → 3882, INTERNAL 1118 → 1119, lane total 1130/5013 = 22.54% → 1131/5013 = 22.56%
  (`distinct=5013 resolves=12` unchanged). The receipt's limb-1 summary (1118/3883, 1130/5013)
  matches the committed pair and was captured pre-receipt — so "the census pair is the
  regeneration FIXED POINT" in the receipt header and the report's "fixed point confirmed" do
  not hold at byte level over the truly final tree.
- Grading: the claims (C1/C2) do not rest on the census limb (C1 explicitly claims no census
  move; the quoted census figures match the committed pair), and no axis is harmed — this is a
  conformance defect and a red gate limb at the final tree, status-neutral per the gate standard.
  It IS the same prose-vs-receipt class DF-1 routed last round; noted for the trend record
  without flipping any verdict (the machine-catcher the round built DID catch the old prose —
  the red control proves it — and this new instance is caught by closure and routed).
- **Routed fix for round 56 (lane):** (1) regenerate the census pair only AFTER the gate receipt
  exists (one iteration converges: regen → 3882/1119/1131/22.56%, freshness check → ok), then
  re-run the freshness gate green and commit the pair + receipt together; (2) append an R9-form
  erratum superseding the `CENSUS-FRESH=ok` prose in the round-55 report quote and the SCORECARD
  round-55 section (the report is fleet-record; the erratum is the lane-side record), naming the
  receipt's printed stale limb as the superseding fact; (3) the planned-for-56 fold (rows=36,
  registry=87, entries=39, expected=74) should pin the post-regeneration census figures
  (1131/5013) so the self-citation is stable from now on.

## 4. Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S087 admitted (tier A, docs, mined) → F36 entry | admit | live re-open of https://docs.github.com/en/rest/security-advisories/repository-advisories (curl sha `89fa9af33c38…` = recorded raw; instrument re-capture byte-identical to the committed capture, sha `3eebdf47…`); 14/14 exactly-once assertions re-run exit 0 | **agree** | first-party machine-interface ground, tier A is right for GitHub Docs' own reference; the capture is faithful (byte-identical live today), the entry's claims spot-verified at their pinned anchors, and the scope limits (rate limits/plan-gated params/examples/error schemas unasserted) are honestly drawn |
| rejected over-generalization "the endpoint family requires authentication" (entry Claim 1) | reject (in-entry) | capture line 793 (Q2): "This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested." | **agree** | the finer-grained per-endpoint claim is what the source supports; the carve-out line exists exactly once at the pinned anchor — the gate picked the claim the page itself makes |
| CISA ADP list page stays an unopened lead (lead, not row) | reject (no row) | SOURCES.md Leads at the tip; the lead line's bytes unchanged (base:137 ≡ tip:138 byte-identical, sha `de3270d53caca…`, exactly once) | **agree** | contract rule 1 (a row is written only after opening) applied honestly; "Rejections this round: none" is accurate and the non-opening is recorded with its reason rather than padded |
| S087 Gate quote ≤25 words at a located anchor | admit-supporting | S087.txt:2853 exact text present; `wc -w` = 11 words | **agree** | quote located, countable, and grounds the permission-set teaching cell of the row |
| census validate at round end | (contract limb) | `bash <fleet>/scripts/sources-census.sh validate --root <fleet> kasegi` re-run | **agree** | exit 0 with exactly the 6 informational W04 duplicate-url rows the report names, unchanged |

## 5. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| depth:verifiability | **improved** (score held 4, capability extension) | ledger 9 → 17 with selftest 5/0, green 17/17, red 3-stale — all re-run by this verifier; the DF-1 prose class and wrong fold-figures are now machine-caught |
| coverage | **improved** (score held 8) | F36 admitted on a live first-party source (re-opened byte-identical); frontier 35 → 36, registry 86 → 87, knowledge 73 → 74, all re-derived; counter/binding/expect limbs reproduce |
| depth:density | **unchanged** (non-target guard holds) | SKILL.md absent from the round diff (base..tip); guard reasoning stands |
| calibration | **improved** (verdict row) | carry-in landed append-only with runnable checks (both re-run green by this verifier); six Mistakes rows verified with class/captured-by/fix; three own-catches pre-data; DF-3 is the one new prose-vs-receipt instance — routed above, status-neutral, the same class the round's own red control now machine-catches |

## 6. Trend verdicts (this verifier's, agreeing with the report's)

- **expansion: improved** — frontier 35 → 36 (F36, live first-party admit verified), registry
  86 → 87, knowledge 73 → 74; every count re-derived from committed bytes.
- **quality: improved** — the figure-audit capability grew 9 → 17 with the red control proving
  it can fail; no admitted entry failed its re-check (S087 14/14; F31–F36 all PASS in the
  counter re-run; the 30 problem-rows / 33 FAIL entry records are the standing disclosed
  operator-owned class, unchanged 33 = 39−6 invariant); the round's biggest own mistake (the v1
  stand-in) was caught pre-data by the round's own limb and mined the same round.
- **discernment: improved** — the carry-in is the honest form (append-only, byte pins, runnable
  closure checks, both re-run exit 0 by this verifier); the spot-check agrees with the admit and
  with every rejection-shaped decision sampled; DF-3 is routed above and must become a lesson
  row next round (the erratum discipline the lane itself re-taught this round is the fix form).

## 7. Notes for the operator

- The report's SHONEN section carries `[~]`/`[ ]` only — no `[x]`, so no self-attested check
  needs demotion. Boxes 1/3/4 look close to non-author-checkable (SKILL.md unchanged with its
  decision tables standing; the figure-audit instrument runs green standalone with no oral
  context — this verifier ran it; PROVINCE amendment is a pure EOF append and F36 stays inside
  the declared boundary, live-target testing still refused). Box 2 (end-to-end domain task)
  remains honestly `[ ]` — the lane itself names the considerthese proposal as the open
  candidate. Promotion review remains the operator's call.
- DF-3 (§3) is routed to the lane for round 56; the L0-routed operator-owned classes (30
  problem-rows / 33 FAIL records, the 67 `cd /home/…` recheck lines, the python3-dependent limb
  replay, the absent AgentSwarm L2 surface) remain standing, disclosed, and correctly not
  claimed.
- The lane's "fixed point" census wording (report + receipt header) should be read subject to
  §3: the pair quoted is the committed pair (3883/1118/1130 = 22.54%), stale by exactly the one
  self-referential receipt citation until the §3 fix lands.
