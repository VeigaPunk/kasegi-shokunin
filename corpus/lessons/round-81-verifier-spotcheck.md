# Round 81 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: lane-round kasegi r81. Base `191e6ba8f872d08802d83b57cd7fcf4bfa122f0e`, freeze `7ad3118c86ee14fde433d73671cc407668533cec`, landing / lane HEAD `a5269eee40b7fdb5f2f2b3e918e1197b1f35350d`. Report `.ufo/reports/round-81/kasegi.md` (fleet repo, commit `8485807c7c4321b398c028ab66ebef946c6395b7`). Dispatched prompt `.ufo/prompts/kasegi-round-81.md` (fleet commit `9c95f2da46d9d9c83eb31459bf3672d080c7ab7c`).

Driver digest (copied from the mutable `.ufo/watchdog.log`):

```
2026-11-06T17:09:01-03:00 launch kasegi round=81 pgid=555511 driver=hyaku-inline attempt=1
2026-11-06T17:47:21-03:00 complete kasegi round=81; hyaku-inline attempt=1
```

Every measurement below is a read over committed bytes (`git show`, `git diff`, `jq`, `grep`, `sha256sum`) or the fleet census. No lane gate, selftest or wave counter was executed (§Gate standard, Closure consequence); those are evidence-verified from committed receipts.

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report author | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-81/kasegi.md` | `kasegi-shokunin kasegi@shokunin.local 8485807c… 2026-11-06 17:46:57 -0300` | lane identity; filed after landing commit (17:46:08) |
| SHONEN heading | report `## SHONEN` | one heading, 4 lines (`[~]`, `[ ]`, `[~]`, `[~]`) | conformant |
| cited commits exist + ancestry | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for 191e6ba8, 7ad3118c, a5269eee | `commit` ×3, `anc ok` ×3 | conformant |
| pushed, clean | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain` | `branch=master local=a5269eee… remote=a5269eee… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | conformant |
| remote tip | `git ls-remote origin refs/heads/master` | `a5269eee40b7fdb5f2f2b3e918e1197b1f35350d` | matches report |
| prompt contract | headings of `.ufo/prompts/kasegi-round-81.md` | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN rule `:118`), §5 commit/push/L0, §6 hyaku addendum, §7 scratch | template contract carried |
| freeze integrity | `git diff --stat 7ad3118c a5269eee -- .ufo/waves/round-81/claims.json .ufo/waves/round-81/c1 .ufo/waves/round-81/controls` | empty | frozen bytes unchanged at landing |

Defects: none bearing on status. `controls/__pycache__/` exists in the worktree but is ignored (`.gitignore:2`), not committed.

## Per-claim re-check

### C1 — depth:verifiability — partly re-measured, counter evidence-verified

Re-measured (plain reads):

- P2 landed bytes: `git show a5269eee:corpus/instruments/recheck-cwd-census.py | sha256sum` → `a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0`; base → `420151fd…e505698`. Matches the report and the frozen candidate hash.
- Selftest growth 15 → 22: the docstring prints `selftest cases=15` at base (`:35`) and `cases=22` at landing (`:36`). `diff` of the sorted `check("<id>"` sets base vs landing adds exactly `conform-limbs output-lines prefix-literal timeout-bucket tmpdir-file tmpdir-unset usage-guards` (7; the eighth hit `check("x"` is a string fixture at `:618`), i.e. the seven checks the report names. `GATE_ROWS = 28` → `GATE_ROWS = 40`.
- Table: `jq length .ufo/waves/round-81/c1/mutant-table.json` → `59`; classes `assertion 55, exception 1, neutral 3`; row keys `anchor,class,expect,id,kill_cases,replacement`. `sha256sum` mutbat.py → `fa96223b…`, table → `abcc834e…` (match the report).

Evidence-verified (committed receipts, not executed):

- `controls/c1-donothing-r81.txt`: r80 bytes `420151fd…` under the r81 counter → `baseline=bad rows=59 killed=28 survived=28 … neutral_ok=0/3`, `rc=1`.
- `controls/c1-candidate-r81.txt`: candidate `a3b58aa5…` → `baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3`, `rc=0`; counter selftest ok; candidate selftest `cases=22 failures=0`.
- `controls/c1-forgeries-r81.txt` and `l1/L1-landing-r81.txt:74-85`: F1–F5 each `rc=0 killed=56` under counter r80 and `rc=1` under counter r81 (F1–F4 `MISKILLED 56`; F5 `KILLED 56` but `neutral_ok=0/3`).
- `l1/L1-landing-r81.txt` (2026-11-06T20:42:45Z, landing bytes): P1–P8 all printed as frozen; P5 `RECHECK-CWD entries=95 … RESULT conformant`.

Before → after agrees with the report. Limits the lane itself recorded and that I accept as true from the receipts in `w1/CriticClaims-receipts/` (`forgery-selfdiff.py`, `mutbat-forgery.txt`, `mutbat-junkedit.txt`): the tally rejects the five enumerated forgeries, not every forgery; P5 does not bound the exit buckets; row S07 kills a neighbour of the routed survivor. These falsify the claim's prose ("independence from the byte pin"), not its frozen predicates.

### C2 — coverage — re-measured

| measure | base 191e6ba8 | freeze 7ad3118c | landing a5269eee | report |
|---|---|---|---|---|
| `git ls-tree -r --name-only <r> corpus/knowledge \| grep -c '\.md$'` | 94 | — | 95 | 94 → 95 ✓ |
| registry rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 114 | 115 | 115 | 115 at freeze and landing ✓ |
| S115 status / used-by (cells 9, 12) | absent | `queued` / `—` | `mined` / `corpus/knowledge/osv-importfindings-record-quality-feedback.md` | ✓ |
| `git diff 7ad3118c a5269eee -- corpus/SOURCES.md` row changes | — | — | one `-`/`+` pair, S115 only | B1 ✓ |
| knowledge-expected vs listing | — | — | +1 line (the new entry); sorted name sets `diff` empty (`set-equal`) | B2 ✓ |
| README Frontier rows `grep -cE '^\| *F[0-9]+'` | 58 | — | 59 (+F57 at `corpus/README.md:1243`) | F56 → F57 ✓ |
| snapshot `sha256sum corpus/source-snapshots/round-81/S115.txt` | — | — | `e304eb88…daf3f6f7f` | ✓ |
| entry header | — | — | `source: S115 — https://…/get-v1-importfindings/`, `verified-at: 2026-11-06`, `recheck: … source-recheck.py --manifest … --source S115` | ✓ |

FRONTIER-CENSUS (`rows=57 admitted=57 closed=57 problem-rows=0`) and ENTRY-GATE (`pass`) are evidence-verified from `l1/L1-landing-r81.txt:57-71`; B8's two-sided control (F56 pass, junk dump `rc=1`) from `controls/c2-prefreeze-r81.txt`.

### Harm check

- `git diff 191e6ba8 a5269eee -- SCORECARD.md | grep -c '^-[^-]'` → `0`; same for `LOG.md` → `0` (additions only).
- `SKILL.md` diff is 1 line (`+1 -1`, the recheck-cwd pin row); density mean `272.8` before and after is evidence-verified (`L1-landing-r81.txt:73`).
- `corpus/lessons/round-80.md`: 5 added lines, 0 removed (append-only corrections).
- Census (run by me): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok`, six inherited `W04` (S028 S029 S072 S076 S080 S085), `rc=0`.

## Discernment spot-check (LEARNING.md)

Live re-open: `curl -sSL https://google.github.io/osv.dev/get-v1-importfindings/` → `200`, final URL unchanged; tags stripped, whitespace collapsed, each quote counted.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| cl1 purpose, "Given a specific OSV.dev source, report any records that are failing import-time quality checks." (S115.txt:25, 14 words) | admit | live page (count 1) + snapshot `:25` | agree | a contract clause verbatim on the cited line, live and captured; not held elsewhere (lane sweep `grep -rli importfindings corpus/knowledge` empty before the entry) |
| cl6 source.yaml name, "The source value is the same as the name value in source.yaml" (S115.txt:38, 12 words) | admit | live page (count 1) + snapshot `:38` | agree | the parameter-binding rule, on the cited line |
| S115.txt:39 case-sensitivity note | reject (held) | live page (count 1); `corpus/knowledge/osv-post-v1-query-contract.md:31` quotes "Case Sensitivity: API requests are case-sensitive." (S108.txt:53) | agree | the same sentence is already admitted under F51; re-admitting it would be duplicate ground |
| S115.txt:32 status and feedback sentences | reject | snapshot `:32`; `osv-post-v1-query-contract.md:75` | agree, with nuance | the rejection stands on its own reason (a status/feedback sentence is not a contract clause). The "held by F51 :75" support is weaker than stated: `:75` lists the experimental endpoints as "listed, not described", it does not hold the experimental-status sentence |

New registry row re-opened: S115 (`corpus/SOURCES.md:127`), tier A `docs`, opened 2026-11-06, `teaches` "how a home-database operator learns which of its published records OSV.dev refused at import…". The ≤25-word quotes grounding it are recorded in the lesson's `## Gate` (`corpus/lessons/round-81.md:102-107`); `jq` over `corpus/source-snapshots/round-81/manifest.json` gives word counts `14 12 23 18 1 12` at anchors `25 32 34 36 37 38`, all ≤25 and matching the lesson. The audience quote (Q02, 12 words) is found once on the live page. `teaches` is grounded by Q02 + Q03.

The lane also found its predecessor spot-check's routed-defect-1 count short by one (`corpus/lessons/round-81.md:255`: sites `88 160 162 169`, not three); I agree from the quoted `grep -n` output — the r80 correction appended this round covers all four.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth:verifiability | improved | landed instrument strictly stronger: selftest 15 → 22 checks (re-measured), case-matched kills 28 → 56 and neutral 0/3 → 3/3 under the frozen counter, F1–F5 rejected (evidence-verified); score 4 → 4 nominal per R58 |
| coverage | improved | F57 admitted, knowledge 94 → 95, S115 `queued → mined` (re-measured) |
| depth:density | unchanged | one-token SKILL.md pin edit; mean 272.8 both sides (evidence-verified) |

## Trend verdicts

- **expansion: improved** — one new entry on uncovered ground (publisher-side import-findings report), citing a `mined` row; frontier 56 → 57.
- **quality: improved** — the recheck-cwd gate kills 56/56 rows on the landing bytes against 28 on the base; the r81 counter rejects five forgeries the r80 counter accepted; no admitted entry failed its re-check (census `rc=0`, live re-open of S115 quotes found each once). Carried limits are recorded and routed, not hidden.
- **discernment: improved** — this spot-check agrees on 2/2 admits and 2/2 rejects; the r80 spot-check's routed defects 1 and 2 became appended corrections plus QUALITY R132 grounded in M81-2.

## Routed defects (lane fixes next round)

1. Stale cite left standing: `corpus/knowledge/osv-determineversion-cc-library-versioning.md:80` still cites `osv-post-batch-query-contract.md:19` (a heading; the sentence is at `:21`) — PROTOCOL §Evidence standard, "Corrections sweep every mention". Needs an appended correction (the lane already lists it for r82).
2. C1 prose overstatement: the claim's "independence from the byte pin" is falsified by `w1/CriticClaims-receipts/forgery-selfdiff.py` (`killed=56 … neutral_ok=3/3`, rc 0). M81-3's fix is routed but not yet shown able to fail; land a counter-owned second kill limb that rejects it.
3. P5 does not bound `exit0_foreign + exit1_foreign + exit_other`; a one-line junk edit skips six rechecks with P1/P3/P5 green.
4. B8 is a shape-only limb (a labelled six-quote dump passes; 3/94 admitted pairs pass); add a content limb.
5. Row S07 mutates `census()`'s default, not the routed `main()` survivor; the MutC1Hunt survivors (25 real gaps) and the ten r80 survivors outside the r81 table still survive.
6. `corpus/lessons/round-81.md` landed with 24 `PENDING-L1` markers in the scribe-drafted `## Gate` body; the L1 section (`:3-27`) resolves them, but a reader of `## Gate` alone sees unresolved predicates. Next lesson: resolve or strike in an appended note.
7. Minor: the `:32` rejection's "held by F51 `:75`" support does not hold the status sentence (see spot-check table); the rejection stands on its other reason.

SHONEN: no box is fully checkable by a non-author this round (box 2, an end-to-end domain task in LOG.md, stays untouched).
