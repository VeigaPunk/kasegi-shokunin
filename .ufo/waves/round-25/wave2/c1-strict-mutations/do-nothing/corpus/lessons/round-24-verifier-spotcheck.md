# Round 24 — non-author verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_flash)

I did not author round 24 and did not improve it. Lane base before the round
`c2480b143120364728b40397926ffcf30a7309c8`; lane tip at closure
`492538b858b4e53e73badef00aa22d62698d097c`; the round's work commit cited by the
report is `d3614a2c5489e6379bdd0e56440496310b8b5e00`. Every measurement below was
run by me on 2026-10-25 against committed bytes; nothing was copied from the
lane's own receipts unless marked *evidence-verified*.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

| Check | Command | Observed | Verdict |
|---|---|---|---|
| Report committed in the fleet repo by the lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %ci' -- .ufo/reports/round-24/kasegi.md` | `kasegi-shokunin <kasegi@shokunin.local> 5c95d9d3c92edebf20c409fc8ba36f3f940e5acd 2026-10-25 04:34:30 -0300` | pass |
| `SHONEN` heading, one line per box | `grep -cE '^- \[' SHONEN.md` → 4; report §SHONEN → 4 lines (`[~] [ ] [~] [~]`), no `[x]` | 4/4 boxes addressed; author-only marks, correct for a non-author-free round | pass |
| Cited lane commits exist and are ancestors of the branch | `git cat-file -t <h>` / `git merge-base --is-ancestor <h> master` for `d3614a2c`, `492538b`, `c2480b1`, `d0a3f6a`, `953c278`, `bf9ce02` | all `commit`; all `ANCESTOR-OK` | pass |
| No uncommitted round work, lane pushed | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain` | `branch=master local=492538b remote=492538b ahead=0 behind=0 tracked=0 untracked=0`; `status --porcelain` empty | pass |
| Dispatched prompt carries the round contract | `grep` of `.ufo/prompts/kasegi-round-24.md` against `templates/round-prompt.md` | renders §1 MISSION/AXES binding, §2 1–3 claims, §2b frontier step, §3 L2 floor, §4 report contract + `SHONEN` heading, §5 commit-then-push + push scope + L0 channel, plus addendum §6 | pass |
| Cited hash is the lane HEAD at file time | report filed 04:34:30; lane HEAD then was `492538b` (committed 04:34:25) | report cites `d3614a2c` (04:32:59) as the landed commit and states "Every change below is inside that commit", but `wave2-refusal-{2,3,4}.json` live in `492538b` | **defect D24-1** (status-neutral) |

## 2. Claim re-checks

`re-measured` = I ran the measurement myself over committed bytes.
`evidence-verified` = the claim rests on a lane-owned gate/instrument, so per
PROTOCOL §Gate standard (*Closure consequence*) I verified its committed evidence
(revision digest, receipt, verdict) and did not execute it.

### C1 — depth:verifiability (4, lowest non-retired axis)

**Counter A, the frozen shell form — re-measured.** Both directions run by me with
cwd pinned to the lane repo; the "before" direction evaluates the `recheck:` values
as they read at `c2480b1` against the closure tree (the round-23 manifest is
byte-stable across the round except for one added `anchor`):

```
$ for f in cvss-v4-severity-and-vector coordinated-disclosure-timelines \
       authorization-safe-harbor-and-scope ai-assisted-finding-validation \
       cwe-top25-2025-methodology multiparty-vulnerability-coordination \
       cna-assignment-and-vulnerability-rules cra-manufacturer-reporting-duties; do
    r=$(git show c2480b1:corpus/knowledge/$f.md | grep -m1 '^recheck: ' | sed 's/^recheck: //')
    bash -c "$r" >/dev/null 2>&1; echo "$f $?"
  done
cvss-v4-severity-and-vector 2
coordinated-disclosure-timelines 2
authorization-safe-harbor-and-scope 2
ai-assisted-finding-validation 2
cwe-top25-2025-methodology 2
multiparty-vulnerability-coordination 0
cna-assignment-and-vulnerability-rules 0
cra-manufacturer-reporting-duties 0
BEFORE=3/8
```

The same loop over the closure tree returns `0` for all eight, and `0` for the two
F09 entries (`authorised-testing-rules-of-engagement`, `statutory-authorization-
and-unauthorized-access`). **3/8 → 8/8 confirmed**; the report's claim holds, and the
harness's 10/10 includes the two entries C2 adds.

**Counter A receipts — evidence-verified.** `c1-counterA-before.txt` = `entries=8
pass=3 exit=1`; `c1-counterA-after.txt` = `entries=10 pass=10 exit=0`; failure
reason at before is `problems=manifest-missing-ids` for F01–F05, which is the
routed defect the round-23 verifier filed. `c1-counterA-manifest-receipt.txt` has
95 `OK` lines = 19 `:sha256` + 76 assertions, all `occurrences=1`.

**Counter B (dispatch matrix) — evidence-verified, revision pinned by me.**
`sha256` of the *content* of `corpus/instruments/resolve.py`:

```
git show c2480b1:corpus/instruments/resolve.py | sha256sum -> 690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
git show d3614a2c:corpus/instruments/resolve.py | sha256sum -> db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667
.ufo/waves/round-24/c1-baseline-resolver.py sha256    -> 690153ad… (identical to the c2480b1 bytes)
```

`c1-control-baseline.txt`: `cases=8 pass=4 exit=1`, `resolver=690153ad…`.
`c1-fixed.txt`: `cases=8 pass=8 exit=0`, `resolver=db5e0767…`. Both receipts carry
the same matrix digest (`fef0f02d…`) and checker digest (`acbb6870…`), so the
before and after were scored by one detector. **4/8 → 8/8 confirmed as evidence.**

Containment regression: `c1-containment-regression.txt` = `cases=24 escape=12
controls=12 pass=24 fail=0 resolver_sha256=db5e0767…` (the landed bytes), so the
dispatch fix did not open an escape the round-23 matrix covers.

Degenerate instruments: `always-GONE 1/8` / `always-INTERNAL 0/8` are measured in
`wave1/LivenessMatrix.md:98,103,200` ("the only passing case is C2"), not invented;
R11's row points there.

**Axis verdict: `improved`.** The predicate (every Frontier entry's own `recheck:`
exits 0 **and** the dispatch matrix is 8/8) is true at the closure tree, and the
before state fails it in both limbs.

### C2 — coverage (7)

**Re-measured, both counters:**

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
9
$ git show c2480b1:corpus/README.md | awk -F'|' … (same filter)
8
$ grep -lE '^source: S03[2-5] ' corpus/knowledge/*.md | wc -l
2
$ git grep -lE '^source: S03[2-5] ' c2480b1 -- corpus/knowledge | wc -l
0
```

Frontier `8 → 9` (F09, two entries) and entries citing a row first registered this
round `0 → 2` (`authorised-testing-rules-of-engagement.md` = S032;
`statutory-authorization-and-unauthorized-access.md` = S033/S034/S035).
`awk`-measured `corpus/README.md` F09 row and the `9/9` denominator line agree with
`PROVINCE.md:38` (`Frontier F01–F09`).

**Census — re-measured:**
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → **exit 0**, `rows 35`, `malformed 0`,
`tier A=32 B=1 C=2`, `status mined=23 queued=9 rejected=3`, the same two `W04`
warnings (`S028`, `S029`) the round declares as pre-existing and explained.

**Axis verdict: `improved`.**

### No-harm guard

`SCORECARD.md` changes `55 insertions(+), 0 deletions` — the round appends and
rewrites no existing row. `SKILL.md` is absent from the 121 changed paths of
`d3614a2c`, so the `density.py` 154.0 / `anchorcheck.py` 0-bad claims hold by
construction (bytes untouched, not merely re-measured). `corpus/source-snapshots/
round-23/manifest.json` changes are additive/equivalent: one escape sequence
replaced by the same character (`\u2019` → `’`, JSON-identical value) and one
`"anchor": 10` added for the non-unique assertion; no assertion was dropped or
relaxed. **Axis `depth:density`: `unchanged`; no axis harmed.**

## 3. Discernment spot-check (LEARNING.md, "checked from outside")

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S032 — NIST SP 800-115 ROE glossary quote | **admit** (F09, entry 1) | live `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` — `http=200 bytes=544047`, `pdftotext` line 3920 reads `Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information` (wraps) | **agree** | Quote is verbatim in the document the row names, appears **once** in the committed snapshot (`normalized occurrences: 1`), is **15 words** (≤25), and the row's locator ("glossary entry, printed F-2") matches where I found it. |
| S033 — e-Gov 不正アクセス法 第二条第四項 | **admit** (F09, entry 2) | live `https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` — `http=200 bytes=36058`; the sentence `「不正アクセス行為」とは、次の各号のいずれかに該当する行為をいう` occurs **once**, inside 第四条項 numbering after ３ | **agree** | Exact statutory sentence present in the consolidated text; the row marks it tier A/spec and the entry quotes it as the definition, not as commentary. |
| `chinese-criminal-thresholds-and-authorisation.md` | **reject** (Q2+Q4) | live `https://czt.ln.gov.cn/czt/attachDir/2026/05/2026050715041524122.pdf` — `http=200 bytes=589780`; 第二百八十五条 at text line 2121: `侵入国家事务、国防建设、尖端科学技术领域的计算机信息系统的，处三年以下有期徒刑或者拘役` — the first paragraph carries **no** 情节严重 element | **agree** | The entry's own cited text contradicts its thesis ("criminal risk attaches to scale and effect, not to the mere act") for exactly the systems the paragraph names; a gate that admitted it would be mis-calibrated. |
| same candidate — "purely quantitative" | **reject** (Q3+Q4) | live `https://www.court.gov.cn/fabu/xiangqing/3085.html` — `http=200 bytes=27296`; 第一条 lists （一）–（四） numeric thresholds **and （五）其他情节严重的情形**, which occurs twice on the page | **agree** | The open qualitative catch-all is in the article the entry calls purely quantitative; the reject's second limb stands on its own. |
| `chinese-national-grading-model.md`, `gb30279-2020-edition-provenance.md`, `cnnvd-grading-specification-primary.md` | **reject** (PROVINCE scope) | `PROVINCE.md:31-40` — Core is "program rules, scopes, and claim packages … triage and claim gates, and submission/disclosure packaging"; Adjacent lists sibling-owned surfaces | **agree by scope read** | A standards body's classification table is not a program rule, a scope, or a claim package, so admitting one would be cross-domain absorption; the refusal is the right disposition rather than a judgement about the entries' internal quality. |

Gate decisions agree on **1 admit family (2 entries, 4 rows) and 2 distinct reject
grounds**; no disagreement to learn from this round.

## 4. Trend verdicts

- **expansion — improved.** One frontier topic admitted (8 → 9) with two entries on
  ground the lane's own base grep shows it did not hold, four registry rows opened
  and pinned this lane (31 → 35, tier B 0 → 1), and two capabilities entered in
  `SCORECARD.md` (`frontier-recheck-harness`, `source-capture`) each with a working
  pointer. The lane states the counter-argument itself (breadth, not technique);
  that is accurate and does not change the verdict.
- **quality — improved.** Both routed verifier defects are fixed and measured
  (counter A 3/8 → 8/8, dispatch 4/8 → 8/8 with the before/after byte identity
  pinned), the round-23 containment matrix is 24/24 on the landed bytes, the
  rechecker gained exactly-once-or-anchor binding (Q9) and now prints
  `occurrences=N`, and the resolver gained two CLI guards that stop a real
  overwrite (`--help` as lane root). Limits are published rather than hidden.
- **discernment — improved.** The outside spot-check agrees on every sampled
  decision; one package entry was refused against its own cited statute (a
  self-falsifying admit is the strongest available evidence of a working gate), and
  two of the round's own frozen artefacts were corrected by erratum rather than
  edited silently.

## 5. Falsification depth — graded honestly

Wave 2 (`kasegi-r24-falsify`, 35 seats, 24 attack roles = 69 %) **never spawned**:
four dispatch attempts, all refused with `Background job limit reached (100)`,
`spawned: 0` (`wave2-refusal-{1,2,3,4}.json`), corroborated by
`.ufo/waves/round-24/wave2/` holding only `swarm-registry.json` and **0** seat
reports. The payload was never split or shrunk, which is the correct response to a
host-cap refusal, but it means the round's executed falsification is wave 1 only:
**43 seats, 11 attack seats (26 %)**, against a designed 69 %.

Consequences I could observe, not infer:

- The counter-B blind spot is disclosed, but its headline figure ("a bound-64→8
  mutant scores 8/8 and 24/24") is an **inference**, not a measured receipt: the
  wave-1 `ResolverAttack` measured that mutant against the **baseline** bytes
  (`4/8, identical receipt`, containment `24/24`, `ResolverAttack.md:151`); the
  seat that would have mutated the *landed* bytes is the wave-2 item in
  `wave2-spec.json` that never ran. No file in the lane records a mutant of
  `db5e0767…` scoring 8/8.
- The L4 fail-before story is inconsistent across three committed artefacts:
  erratum 3 says L4's primary "could not fail the baseline", `ResolverAttack.md:176`
  says "L4 should be re-labelled a control (its primary assertion is green on the
  baseline)", and the landed `c1-control-baseline.txt` shows L4's primary
  `FAIL`/`actual=INTERNAL` with no `path_check`. The discrepancy is conservative
  (the receipt shows *more* fail-before than the prose claims), but it survived
  because no fresh wave-2 reviewer read the landed receipts against the prose.
- The report's own weakest sentence ("from committed captures": a recheck can be
  re-pointed at another manifest) got no second-pass decision.

**Grade: partial falsification.** Both claims re-derive from committed bytes under
my own commands, so the wave-2 loss does not change admission; it does leave three
self-critical statements unmeasured or mutually inconsistent, and that is recorded
as routed debt rather than counted as verification.

## 6. Routed defects (lane must fix next round)

| # | Defect | Evidence | Fix |
|---|---|---|---|
| D24-1 | Report cites `d3614a2c` as the landed commit and asserts every change is inside it, while lane HEAD at file time was `492538b` (04:34:25) and `wave2-refusal-{2,3,4}.json` live there | `git log --format='%h %ci'` on both commits vs the report commit at 04:34:30 | Cite the lane HEAD at write time, or name both hashes and which paths each carries |
| D24-2 | Three different assertion counts for one artefact: `instruments/README.md` says 62, the lesson says 77, the report and the manifest say 76 | `python3 -c "len(s['quotes']) …"` over `round-24/manifest.json` → 76 (S001–S015: 50, S032–S035: 26); receipt = 19 sha + 76 OK lines | State one measured number in all three places; add the counting command near the README figure |
| D24-3 | The bound-64→8 mutant's `8/8` is stated as measured in `README.md:159`, `SCORECARD.md:502`, `QUALITY.md` R11 and the report; only the baseline-base `4/8` was measured | `ResolverAttack.md:151`; no lane file records a mutant of `db5e0767…` | Either measure it on the landed bytes or word it as "would score 8/8 by construction; measured identical receipt on the baseline base" |
| D24-4 | L4's fail-before is described three incompatible ways (erratum 3, `ResolverAttack.md:176`, `c1-control-baseline.txt`) | the three quoted artefacts | One sentence in the next lesson reconciling them, with the receipt as the authority |
| D24-5 | Residual cwd dependence: the round re-pointed F01–F05 to the round-24 manifest but did not prefix `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`; 5 of 35 `recheck:` lines carry it, so a cold run from another cwd still exits 2 (the harness pins cwd, which masks it) | `git grep -h '^recheck: ' HEAD -- corpus/knowledge \| grep -c '^recheck: cd …'` → 5 of 35 | Prefix the remaining lines or make the harness's cwd pin explicit in each entry's recheck text |

Not a defect, recorded for the operator: `SHONEN.md` boxes 1/3/4 now carry
non-author-checkable evidence (SKILL.md tables at `:134`, `:1014`, `:680`, `:565`,
`:60-87`; the cold `git archive` run; the `ConnSibling` refuse/route record), while
box 2 remains genuinely unmet (the domain roots are still absent, and the pipeline
names 14 `ops/*` executables that no longer exist). Promotion stays operator-owned;
this round does not ask for it.
