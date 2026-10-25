# AttackJ1 — staged rejects presence + F12/F19/F20 frontier absence (wave 2)

Seat: L1Kasegi26.AttackJ1 (read-only). Date: 2026-10-25 (UTC). Skill: godspeed (no installs performed; no tooling changes).

## Attacked claim (C2 assimilation)
The two reject candidates remain in the staged package with their documented grounds, the lane corpus contains no F12/F19/F20 frontier rows, and the lesson carries the reject reasons + flip conditions.

## Verdict: CONFIRMED (all limbs)

### 1. Both reject candidates remain in the staged package, with documented grounds
Staged package = `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/` (read-only, matches lesson §Gate "Package: …/merge/kasegi").

| Candidate | Present | Ground line (verbatim) |
|---|---|---|
| `vendor-cvd-policy-crosswalk-2026-10-23.md` | yes | line 7: `ground: F20 (new frontier item: vendor-side disclosure policies as corpus objects)` |
| `chinese-criminal-thresholds-and-authorisation.md` | yes | line 9: `ground: F12 (extends F03, which holds safe-harbor attribution only)` |

Both files read directly; the `ground:` lines match the claimed F20 / F12 grounds.

### 2. Lane corpus contains no F12/F19/F20 frontier rows
- README.md Frontier table (lines 200–212) lists exactly F01–F11; no F12/F19/F20 row.
- `grep -cE '\| F(12|19|20) ' corpus/README.md` → `0`, exit 1 (no match).
- `grep -nE 'F(12|19|20)' corpus/README.md` → no matches (exit 1).
- Lane knowledge dir (`corpus/knowledge/`, 39 entries) contains neither reject-named file (`vendor-cvd-policy-crosswalk*`, `chinese-criminal-thresholds*` absent) — the rejects were not adopted under any name.

### 3. Lesson carries reject reasons + flip conditions
`corpus/lessons/round-26.md` §Refused table (lines 50–57):

| Candidate | Failing gate | Reason (evidence, condensed) | Flip condition |
|---|---|---|---|
| `vendor-cvd-policy-crosswalk-2026-10-23.md` | Q7, Q3, ground | (1) Q7: `recheck:` prose with command inside backticks + `(ran …)` tail; `bash -n` fails (s3 strict-limb 4/6); (2) `ground: F20` names no lane frontier row (`grep -cE '\| F20 ' corpus/README.md` → 0); (3) Q3: staged entry asserts "two conditions" while its own bytes list FOUR disclosure-trigger conditions (`S040.txt` L301, L302–L304, L305–L308, L309); round-25 verifier re-opened live page, both agree | "Restate the count with line anchors, cite the lane id S040 (already registered round 25), and ground on an indexed lane row — which is what the admitted F10 entries already do under a different name, so the refusal is of the staged text, not of the theme." |
| `chinese-criminal-thresholds-and-authorisation.md` | Q2 + Q4, and Q1/Q7 | Refused round 24; reason retained: own cited 第二百八十五条 text (S045) carries no 情节严重 element for first paragraph vs entry asserts "criminal risk attaches to scale and effect"; "purely quantitative" falsified by 第一条(五) 其他情节严重的情形 (S044); `recheck:` prose; `curl -sSL` exits 0 on a 404; `ground: F12` names no lane frontier item (round-24 lesson §Refused; s3 re-confirmed strict-limb failures this round) | "Restate 285(1) as a conduct offence, quote 第一条 in full including (五), make the recheck fail closed, add `### Rejected`, register the rows under lane ids." |

Lesson also records: "No Q/R bar was relaxed for either reject."

## Method
Direct reads: staged files (front matter + ground lines), `corpus/README.md` (frontier table), `corpus/lessons/round-26.md` (lines 54, 55 raw). Commands: `grep -cE '\| F(12|19|20) ' corpus/README.md` (0, exit 1), `grep -nE 'F(12|19|20)' corpus/README.md` (no output, exit 1), `grep -n '^ground:' <staged files>` (lines 7 / 9). Lane knowledge dir listed via glob (39 entries).

## Remaining unknowns / notes
- Staged package is the read-only `/home/vgpnk/Projects/shokuknow` tree; both staged candidates were read as-is (no edit possible or performed).
- The F20 and F12 grounds are exactly what the lesson's reject reasons attribute to the two candidates; no counter-evidence found.
- No installs performed; no VCS mutations.
