# Round 31 — kasegi verifier spot-check

author: hyaku closure (non-author integrator, @m_sonnet)

Non-author closure review of kasegi round 31 (attempt 1). Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`; lane tip / pushed master `7079178fcfcae32b8fd53bb79b329e6156fd661b`. Report `.ufo/reports/round-31/kasegi.md`. Driver digest (copied from `.ufo/watchdog.log`, mutable): `2026-10-25T20:07:56-03:00 launch kasegi round=31 pgid=828159 driver=hyaku-inline attempt=1`; `2026-10-25T22:54:10-03:00 complete kasegi round=31; hyaku-inline attempt=1`.

Method note: the limb counter, ledger and instruments are the lane's own gate. I did not run them inside the lane tree. I ran them on `git archive 7079178` extractions under `/tmp` (`/tmp/kc31` counter run, `/tmp/kh31` hand re-derivation, `/tmp/kb31` base-commit archive), which write nothing to the lane; `recheck-audit.py --quiet` was run in the lane root (its recheck lines `cd` into the lane) and left `git status --porcelain` empty. Claims marked **re-measured** below are plain measurements I ran; **evidence-verified** means I read committed receipts only.

## 1. Conformance (step 1)

| Check | Result | Command / evidence |
|---|---|---|
| Report committed by lane identity | OK | `git log --format='%an %H' -- .ufo/reports/round-31/kasegi.md` → `kasegi-shokunin 6026f956ec38f7eb15ff9d71fa04eb03d81d13ee round-31: kasegi report` |
| `## SHONEN` heading, one line per box | OK | `grep -c '^## SHONEN'` → 1; 4 lines, one per `SHONEN.md` box (`grep -cE '^- \[[ x~]\]' SHONEN.md` → 4), all `[~]`; no `[x]` written |
| Cited lane commits exist + ancestor of branch | OK | `merge-base --is-ancestor <h> master` holds for `738a779`, `8a8916c`, `eecad59`, `fd29aac`, `a155310`, `022b755`, `0de072c`, `43c364d`, `d24f700`, `7079178`, and inherited `eadedef` |
| Lane pushed, no ahead | OK | `jj-lane.sh state` → `local=7079178… remote=7079178… ahead=0 behind=0`; `git ls-remote origin refs/heads/master` → `7079178…` |
| Lane uncommitted round work | OK | `git status --porcelain` → empty (before and after my runs) |
| Prompt carries template contract | OK | `.ufo/prompts/kasegi-round-31.md` lines 1–140 `diff` against `kimi-shokunin/templates/round-prompt.md` differ only in the 5 placeholder substitutions (lane, round, fleet root, axes, census command); §6 hyaku addendum follows; section headings §1–§5 identical |
| Marker-vs-report | OK | Real report: 87 seats, 12 lane commits in `b374feb..7079178`, evidence pointers, receipts under `.ufo/waves/round-31/`. Status `ok` |

Defects (status-neutral, routed to round 32):
1. `corpus/lessons/round-31.md` still carries the composition-time header placeholder `LANDED_HASH_PENDING` (2 hits) and stale open-items text, corrected only by an appended close-out erratum — legitimate append-only practice, but a cold reader meets the stale text first.
2. `SHONEN.md:34` says "8 assertion `OK` lines" for the S048 recheck; the committed manifest and my run give **11** (`S048:Q1…Q11 OK occurrences=1` plus `sha256 OK`). The lesson/report disclose 11 elsewhere; this line is stale.
3. `corpus/QUALITY.md` `selftest cases=4` still present (grep → 2): M31-4 open as the lane itself disclosed.
4. Unowned fleet-root `demo-cwd.txt` (seat cwd probe) left untracked at `/home/vgpnk/Projects/shokunin/demo-cwd.txt`; lane disclosed it. Fleet-root `.ufo/state/*.report-baseline` and `.scratch/` modifications are operator/aggregator files, not lane debt.
5. QUALITY R16 (weak: points at the superseded specimen, no runnable check in the corpus), R18 CHECK B' (closes on a content-free `## Round 30` heading) and R19 (token grep; four measured false greens) are weaker than their criteria — lane-disclosed, not repaired.
6. Two supplementary guard-harness tamper probes against the limb counter survive (`wave3/MutCounterReplay.md` §6); three counter mutants are caught only by guard exit status, not by the frozen summary lines (disclosed).

## 2. Claims re-check

### C1 — depth:verifiability (4 held) — **re-measured** on archive copy + **evidence-verified** for history

Commands run in `/tmp/kc31` (archive of `7079178`), observed:

- `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo $?` → 13 `LIMB … verdict=killed` lines (each `live=` ≠ `mutant=`), `guard cases=3 failures=0`, `CONTROL CTL-noop verdict=invalid:noop ok=y`, `CTL-nocompile invalid:nocompile ok=y`, `CTL-equivalent survivor ok=y`, `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`, exit **0**; stdout `sha256 d6aefddca502…` — equal to the report's `d6aefddc…` on a second run.
- `limb-mutation-check.py --selftest` → `selftest cases=20 failures=0`.
- No-harm on the same bytes: `recheck-audit.py --quiet` in the lane root → `strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0 … expect=present expected=44 missing=0 unexpected=0 exit=0` (base: 43/43); `source-recheck.py --selftest` → `selftest cases=10 failures=0` (base archive: `cases=9`, `failures=0`); `frontier-recheck-count.py` → `entries=18 pass=18 exit=0` (base archive: `entries=17 pass=17`).
- Do-nothing control: `c1-controls/before.txt` shows `ls_exit=2` on base for counter and ledger; `c1-controls/fake-counter-receipt.txt` shows the fake counter prints 0 `LIMB ` lines. Base instrument digest `git show b374feb:…/recheck-audit.py | sha256sum` → `3fc0d751…` (matches the frozen control); landed `recheck-audit.py` `5d4842da…`, `source-recheck.py` `fd2e01e8…`, counter `237fd07c…`, ledger `c042adf6…` (match the SHONEN/lesson pins).
- **Closure re-derivation clause** (kill rule): I applied the ledger find/replace by hand to a fresh archive copy (`/tmp/kh31`, Python script over `limb-ledger.json` rows) and ran each row's kill command unmutated vs mutated, for **7 of 13 rows**:

  | row | find count | live exit/signal | mutant exit/signal | differ |
  |---|---|---|---|---|
  | RA-paths | 1 | 0 / hit | 1 / miss | yes |
  | RA-cdroot | 1 | 0 / hit | 1 / miss | yes |
  | RA-expect-missing | 1 | 0 / hit | 1 / miss | yes |
  | SR-stem-mismatch | 1 | 1 / hit | 0 / miss | yes |
  | SR-occurrence-not-unique | 1 | 1 / hit | 0 / miss | yes |
  | FR-missing-entry | 1 | 1 / hit | 1 / miss (mutant crashes `FileNotFoundError`) | yes — killed by signal loss only |
  | FR-duplicate-entry | 1 | 1 / hit | 0 / miss (`entries=2 pass=2 exit=0`) | yes |

  Every result equals the counter's LIMB line (`live=…/y mutant=…/n`). The remaining six rows are **evidence-verified** via `wave2/ExecLimb*.md` (10 `holds`, 3 `weak`: RA-paths, RA-cdroot, FR-missing-entry — my re-derivation agrees FR-missing-entry is a traceback kill, and RA-paths/RA-cdroot are killed only through one witnessing fixture each).
- Frozen predicate: all kill-rule clauses clear (counter present, exit 0, both summary lines, 13 LIMB lines each live≠mutant, find-text exactly once for the 7 I rechecked and counter-enforced for all 13, no regression in the corpus, re-derivation matches). The frozen `mutants_of_the_counter` clause was not met as first landed (3 of 6 survived `c660a95f…`); the lane repaired post-freeze and disclosed it; the guard-fixture repair is observable in the landed counter (`guard cases=3 failures=0`) and replay evidence `wave3/MutCounterReplay.md` shows all six caught (the three former survivors by guard exit status only). That clause is an attack-seat obligation, not a kill-rule clause, so it does not void the claim.
- Routed defect M30-1 (B2 fixture trips B1 first): closed — `SR-occurrence-not-unique` is killed on a stem-correct fixture (`SFIX-REPEAT:Q1 OK occurrences=2 anchor=MISSING` on the mutant, `reason=occurrence-not-unique` live).

**Axis verdict: `depth:verifiability` — improved** (score held at 4; the lane's score is unmoved, the instruments' discrimination is). Evidence: 13 limbs proven load-bearing by a deterministic counter I re-ran; selftest coverage grew (`cases=9→10`, recheck-audit completeness now exercised through `main()`, audit 43→44 entries) with no regression; three survivors in pre-existing selftests were closed with a failing-before receipt. Boundaries stay disclosed: 3 `weak` rows, 2 tamper probes, counter-mutant repair post-freeze.

### C2 — coverage (7 held) — **re-measured** in the lane tree

| Counter | Before (`c2-controls/before.txt`, base) | After (my run, tip) |
|---|---|---|
| `awk … F[0-9]+ … admitted` on `corpus/README.md` | 14 | **15** |
| `grep -lE '^source: S048 ' corpus/knowledge/*.md \| wc -l` | 0 | **1** |
| `grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md` | 0 | **1** |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 47 | **48** |
| `sources-census.sh validate --root … kasegi` | exit 0 (W04 S028/S029) | exit **0**, same two W04 lines + `ok`, no E/new W |
| `frontier-recheck-count.py` | `entries=17 pass=17` | `PASS F15 … ids=S048 exit=0`, `entries=18 pass=18 exit=0` |
| `source-recheck.py --manifest …/round-31/manifest.json --source S048` | exit 2 (manifest absent) | exit **0**, `sha256 OK` + Q1–Q11 `OK occurrences=1` |

Non-author review of the prose clauses (I am the named non-author reviewer):
- Entry `vendor-third-party-finding-coordination.md`: Q1 header block present; Q7/Q10: the `recheck:` line parses under `bash -n` and ran from `/` exiting 0 with the same 11 OK lines; Q6: no credential/probing text (`curl|password|token|api[_-]?key|op://` → 0 hits).
- Q3/Q4 quote sweep (my script): 7 blockquotes, each ≤25 words and exactly-once in the pinned `S048.txt` (0 bad). Of 25 further double-quoted strings, 15 resolve in committed captures; the other 10 are explicitly labelled rejected inferences/hypothetical strings (e.g. "MSVR is a bug bounty programme.") or the README F10 row quoted from the lane's own file — none is a purported source quote. Every programme claim is attributed to Microsoft (Q4: "a first-party self-description … One page, one vendor").
- Q5: the entry carries falsifiable counts (FC-1…FC-5, e.g. `grep -ciE '90[ -]day|deadline|embargo|timeline'` on the capture → 0) and rejected over-generalizations (e.g. "Every large vendor runs such a programme.").
- Restatement check: `grep -rliE 'msrc|msvr' corpus/knowledge/*.md` → only the new entry; `coordinator` appears in F06/F02 entries (multiparty-vulnerability-coordination, coordinated-disclosure-timelines) but none states a vendor occupying finder + coordinator seats under its own programme; the entry itself concedes the F06/F10 overlaps. The lane's expansion critic `partial` stands; I concur — F15 adds one value (coordinator of record = the vendor itself) over F06/F10, with an overstated "three additions" sentence routed.
- Known limit (disclosed and confirmed): the seven C2 counters cannot see a fabricated capture; I therefore re-opened the live page (see §3) rather than trust the pin.
- The reviewer-record clause: two lane-dispatched REFUSEs on earlier revisions and an ADMIT on the final bytes (`wave4/RevEntryQ3.md`); my own Q1–Q10 reading of the final bytes finds no failure.

**Axis verdict: `coverage` — improved** (score held at 7; frontier 14→15 on ground held only by this entry). Not a restatement; counters met on re-measure.

### depth:density — **unchanged** (no claim)
`SCORECARD.md` diff base→tip: `git diff b374feb 7079178 -- SCORECARD.md` → **145 insertions, 0 deletions**; the round-31 density row says held 9, no score move claimed (appended block 24 fails the instrument's own ≥60 % resolve bar at 11/27 = 40.74 %). Pre-existing score rows untouched. `QUALITY.md` +69/−0. No owned axis harmed.

## 3. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-31.md` `## Gate`.

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| **F15 entry + S048 row** (Microsoft MSVR) | admit | Live `https://www.microsoft.com/en-us/msrc/msvr` via the `read` tool on 2026-10-26 (a plain `curl` got Akamai `403 Access Denied`, so the lane's capture UA matters) and the committed capture `corpus/source-snapshots/round-31/S048.txt` L28–L35 | **agree** | Live text equals the capture for the heading, three routes and the CVD three-role sentence; the quote "as a coordinator of vulnerabilities that affect multiple vendors" (9 words, ≤25) is present once, L35; only the per-request Trace Id differs (lane-disclosed). Entry states Microsoft as the party, scope bounded to page text. |
| `claim-packaging-and-report-quality.md` (staged) | reject (standing) | `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/claim-packaging-and-report-quality.md` | **agree** | Its `source:` ids `S034/S035/S036` name CNVD helpList / 360 rules / Bilibili PDF; the lane's own `S034/S035/S036` are three Japanese documents (soumu.go.jp, npa.go.jp, cybozu.co.jp) and `grep -c` of the three Chinese URLs in lane `SOURCES.md` → 0 — id collision plus unregistered grounds (Q2). Its `recheck:` is a prose `curl … && pdftotext …` (Q7/Q10). |
| `chinese-crowd-testing-national-standard-2026-10-23.md` (staged) | reject | same package dir | **agree** | `grep -c '"'` → 0 (no quoted string, Q3); `ground: F24` where lane `grep -cE '^\| *F24 ' corpus/README.md` → 0; `S077/S078/S079` rows in lane registry → 0 each. |
| `cn-crowdsourced-testing-roles-and-conduct.md` (staged) | reject (nearest to flip) | same package dir | **agree** | `grep -c '^# '` → 0 (no H1, Q1); `S081/S082` lane rows → 0; line 39 itself says S082 "is the **project record** (drafting stage) … not the published text"; prose recheck. The refusal reasons are sound and the flip conditions concrete. |
| `S048` row quote check (newly written `corpus/SOURCES.md:54`) | admit | `corpus/SOURCES.md` row 54 vs `S048.txt` | **agree** | Row's scope cell is the lane's own words (not a purported quote); its anchor cell cites L28–L35, which I verified line-by-line against the snapshot; census `validate` → exit 0, no E/new W; the `teaches` cell quotes no string over 25 words. Entry quotes ≤25 words each. |

`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029`, `ok`, **exit 0** (same two warnings as base).

Note: the lane's own lesson says disagreement count "unchanged" for discernment because no outside spot-check existed; this document supplies it. I find agreement on 1 admit and 3 rejects (+ the standing round-30 refusal re-confirmed by the wave-2 connector; not re-opened). No disagreement to learn from.

## 4. Trend verdicts

- **expansion: improved.** F15 admitted on ground no other knowledge entry holds (`grep -rliE 'msrc|msvr' corpus/knowledge/*.md` → only the new entry), citing a `mined` row (S048) opened this round; capability `limb-mutation-ledger` entered the SCORECARD Capabilities table (`SCORECARD.md:927/935`); considerthese proposal 2 mined into `score-gap.py`. Caveat: the F06/F10 overlap paragraph needed three revisions.
- **quality: improved.** 13 limbs proven load-bearing (re-run), three selftest survivors closed in the instruments' own selftests, three counter survivors closed by guard fixtures, `recheck-audit` 43→44/44 strict with no entry failing re-check, stale SCORECARD r30 paragraph erratum'd (`SCORECARD` +145/−0), r30 LOG entry landed. No admitted entry failed its bar; no stale item left unmarked that I found. Caveat: R16/R18/R19 weaker than their criteria; two L1 repairs shipped a defect each before review caught them (disclosed).
- **discernment: improved.** The non-author spot-check agrees with the gate on the admit and all three sampled rejects (rule: "agrees on admits and rejects" → `improved`), and the lane's own two internal Q3 REFUSEs became fixes plus QUALITY rows R16–R19 with lessons behind each (grounded in M31-1…M31-10). Reservation recorded: R16/R19 are weaker than their stated criteria, so the improvement rests on the outside agreement rather than on the criteria quality.

## 5. Routed items for round 32 (lane-owned)

1. Repair R16 (runnable check or narrowed criterion), R18 CHECK B' (require the h2 entry body), R19 (token grep false greens) per `wave3/RevQualityFix.md`; fix `QUALITY.md` `cases=4` (M31-4) with an R16-form erratum naming the string and re-measured number.
2. Correct stale citations: `SOURCES.md:83` anchors in `round-29.md`/`round-29-verifier-spotcheck.md` (M31-3), `SHONEN.md:34` "8 assertion" → 11.
3. Land the three routed sentence-level F15 edits from `wave2/CritExpansion.md` §6 and the LOW/NIT items of `RevEntryQ3` (e.g. the L4 `L26-28` note).
4. Close the two guard-harness tamper probes and the three `weak` ledger rows (RA-paths `pathless.md` case; RA-cdroot fixture; FR-missing-entry kill by signal, not traceback) so the 13 limbs are all `holds`.
5. Gate caveat 1: add manifest `url`/`fetched_utc` fields and a census URL↔capture comparison so the C2-style counters can see a fabricated capture.
6. `score-gap.py`: D1 was verified fixed by `wave3/RevScoreGapFix.md`; D2's final repair (import json, missing-field guard) rests on the lesson erratum only — I did not re-run `score-gap.py`, so the lane should attach a receipt for it in round 32.
7. Lane may leave `demo-cwd.txt` for the operator; it is not a lane file.

## 6. SHONEN

All four boxes are `[~]`. Checklist boxes 1–3 look checkable by a non-author on the committed bytes (decision-table density with anchorcheck exit 0; end-to-end task logged in `LOG.md:1584` with counter exit 0; `recheck-audit` strict 44/44 exit 0). Promotion/ticking is operator-owned; I wrote no `[x]`. Box 4 (no cross-domain bleed) rests on a zero-hit sibling-corpus sweep the lane ran; I did not re-run it.
