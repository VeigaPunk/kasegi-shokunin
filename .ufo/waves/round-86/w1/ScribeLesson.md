# ScribeLesson — round 86 (kasegi) lesson draft

Seat: ScribeLesson (leaf, no delegation, no background jobs). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, freeze `252df0c90c066d83d229e3107811a6bc05e8feed`, base `d7296645c2cd9f631329fa8e2f38328a4c9c89a5`. Scratch `/fast/scratch/hyaku/kasegi-r86/ScribeLesson` (empty; removed at yield).

## Behavior

Drafted the round-86 lesson in the shape of `corpus/lessons/round-85.md`, from the frozen `claims.json` (C1/C2, predicates, kill rules), the executed controls under `.ufo/waves/round-86/controls/`, the round-86 manifest, `corpus/SOURCES.md` rows 134–135, the r85 lesson and the r85 spot-check's routed defects 1–4. Nothing was invented: numbers that exist only at landing carry `[L1: …]` placeholders (occurrence count, seats returned/dead, independent re-open, new leads, considerthese/assimilation, mutant survival, landing-side registry count). No product code, instrument, frozen control, corpus file, SKILL/PROVINCE/SCORECARD/LOG/SHONEN byte, or judge was edited; no git/jj writes; no network.

Wave size stated as **12 seats** — counted from `.ufo/waves/round-86/w1-spec.json` `items` (length 12). No other seat number is stated in the draft.

## Checks I ran (read-only, all in the seat receipt)

Receipt: `.ufo/waves/round-86/w1/ScribeLesson-receipts/draft-numbers.txt`.

| Check | Observed |
|---|---|
| claims.json instruments block vs bytes | 10/10 sha256 equal (knowledge-meter `03df491b…50ee`, apply-map `2a11c1c6…bf5f`, build-map `222f92e6…a77`, repair-map `dd40455a…ce12`, e2e-check `b4a97e09…a834`, `resolve.py` `db5e0767…5667`, `claim-package-check.py` `8b6f8493…c8e6`, round-86 `manifest.json` `8d3b7d35…d3e0`, S122 `ceb01841…aec1`, S123 `22a7d5be…4ab5`) |
| repair-map shape | `keys=203 nonconforming=0 with_anchor=197 bare=6 distinct_targets=203`, `targets_outside_source_snapshots=0` |
| excluded | `excluded=89`, basenames S102 70 / S069 10 / S041 6 / S029 1 / S040 1 / S100 1, single reason prefix `basename-not-unique-snapshot` |
| ExecC1Hunt r86 candidates | `candidates=31 rules={'B:split-first-resolving-word': 31}`, `excluded_ruleB=13` |
| `corpus/knowledge` at freeze | 98 `*.md` |
| `corpus/SOURCES.md` at freeze | 123 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`) |
| S122 per-report amount fields | 0 (`"amount"`/`"awarded"`); only `offers_bounties`, the team `about` text, and `"has_bounty?":true` |
| S052 KEV hits for CVE-2023-28319 | 0 |
| c1 controls | 6 rc 1 rows + 1 rc 0 (positive) |
| c2 controls | 22 rc 1 rows + 1 rc 0 (positive) |
| `corpus/QUALITY.md` R137 at freeze | 0 rows (the row exists only as an uncommitted worktree addition at line 599) |
| `corpus/instruments/citation-survival.md` at freeze | line 31 `- SKILL.md alone: **132/701 = 18.83%**` |

Read-only lane receipts cited by the draft (not produced by me): `.ufo/waves/round-86/l1/r137-check-r86.txt` (`candidates=31 qualifying=0 verdict=FAIL exit=1`; `18/18 PASS`; `203/203 PASS`), `.ufo/waves/round-86/controls/c1-controls-r86.txt`, `.ufo/waves/round-86/controls/c2-controls-r86.txt`, `.ufo/waves/round-86/controls/census-start-r86.txt`.

## Findings

1. **Mined mistake (M86-1), class `planned-tranche-wrong-repair-class`.** `SCORECARD.md:3145` plans "Second repair-map tranche from ExecC1Hunt's 31 candidates"; all 31 entries carry `rule: B:split-first-resolving-word` (31/31, one distinct value), rule B's own `why` says the token is a command invocation, and the hunt report's §"Rules that produced nothing" says only B produced candidates. Evidence pointer, §Captured-by: none (R132/R130/R123 read tallies, corrections and bounds — none reads a candidate's repair class), fix R137 and its fail/pass receipt are in the draft's §Mistakes.
2. **R137's provenance at draft time.** The draft names `corpus/QUALITY.md:599` as R137 and marks it an uncommitted addition. `git show 252df0c9:corpus/QUALITY.md | grep -c '^| R137 '` = 0; `git status --porcelain` shows ` M corpus/QUALITY.md` (+1 line) together with the knowledge-file edits and `?? .ufo/waves/round-86/l1/`. That is the L1's in-flight work, not this seat's; recorded here so the lesson's "Fix: R137" is read against the landed row.
3. **C1 arithmetic identity worth keeping in the lesson.** 1721 − 203 + 198 = 1716 and 398 + 198 = 596: five of the 203 repoints rewrite occurrences whose full path is already a distinct citation in the scope, so the numerator gain is 198, not 203. Stated in the draft as an identity, not as a claim about which five.
4. **C2 counter limits, stated in the draft.** E2 counts only artifacts whose bytes are S122/S123 (other artifacts are skipped), so the package's evidence does not bind S120 and the 2400 USD rests on the r85 S120 capture through `derive()`. E4's quote pool is the four lane snapshots, not the package's `evidence/`. E5 fails for any package outside the lane, which is why every control package prints E5 FAIL. None of these is a defect claim; they bound what E1–E5 prove.
5. **Limbs are not independent (controls).** The wrong-file repoint control fails M4 and M5 in the same run (`LIMB M4 FAIL bad=S071.txt:117`, `LIMB M5 FAIL out_of_range=none`); the same class MutC1Counter recorded for the r85 counter. The conjunction still rejects, but no single limb is self-protecting.
6. **The other planned-r86 item is not in the frozen claims.** `SCORECARD.md:3144` plans "Regenerate the census of record together with the figure-audit ledger"; neither C1 nor C2 carries a predicate for it and `citation-survival.md` is unchanged at the freeze (132/701 SKILL). Routed to round 87 in the draft and in the defect table (r85 spot-check defect 4).

## Conflicts reported verbatim

- `claims.json` C1 and its controls read `base=398/1721`, while the r85 hunt's knowledge block prints `"distinct_tokens": 1721, "gone_distinct": 1322, "nongone_distinct": 399` (lane root, `../MISSION.md` INTERNAL). The claim's own `host_note` reconciles them (scratch clone 398 vs lane root 399). No defect asserted; the draft states both readings and the frozen root.
- `git status --porcelain` in the lane shows modified `corpus/knowledge/*.md` (14 files), `SHONEN.md`, `corpus/QUALITY.md` and untracked `.ufo/waves/round-86/l1/`, `.ufo/waves/round-86/w1-*`. All are other seats'/the L1's in-flight work; this seat wrote only the two paths below.

## Touched surfaces

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScribeLesson-draft.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScribeLesson-receipts/draft-numbers.txt`

No other lane path written; no `S<digits>.txt` copied anywhere; scratch removed.

## Out of scope / not verified

Landing behavior of C1 and C2 (the meters at a landing commit, the package build, LOG/SHONEN edits, `sources-census.sh` at landing), the seat reports' contents, mutant survival counts, and any ScoutSources re-open or new lead. Those are named as `[L1: …]` in the draft rather than guessed.

Tooling: no installs, no upgrades. One draft edit used `sed -i` where the house rule prefers `edit`; the line (`e2e-check.py:86-113`) was re-read and is correct.
