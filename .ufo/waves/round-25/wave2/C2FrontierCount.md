# C2FrontierCount — re-run of frozen frontier and new-row counters

**Verdict: CONFIRMED.** Wave-1's C2 numbers reproduce exactly on the current lane tree:
`frontier=10`, `entries-citing-new-rows=2` (target `>=1`, so the limb holds), census `exit 0`.
All wave-1 summary figures (`frontier=10`, `rows=40`, `harness 12/12`) independently verified.
No correction needed. Scope was read-only; no production files touched.

## Commands run (all from lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

### 1. Frozen C2 counter, limb 1 — frontier admitted rows
```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
10
exit=0
```
Evidence: `corpus/README.md:202-211` — F01–F10 all `admitted`; F10 row at line 211:
`| F10 | Vendor-side disclosure policies as corpus objects | admitted | knowledge/vendor-disclosure-policies-as-corpus-objects.md, knowledge/vendor-disclosure-policy-commitments-crosswalk.md | S036, S037, S038, S039, S040 | …`

### 2. Frozen C2 counter, limb 2 — entries citing new rows
```
$ grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md | wc -l
2
exit=0
```
The two matching files:
- `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` — `source: S036–S039` at lines 3–6
- `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` — `source: S040, S036, S038, S039` at lines 2–5

`2` exceeds the claim's `>=1` target. Note: the regex range S036–S099 is broader than the ids that exist (SOURCES.md max = S040); only these two files match, so the count is exact, not inflated.

### 3. Frozen C2 counter, limb 3 — sources census
```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```
W04 warnings for S028/S029 are pre-existing (recorded in `claims.json` `frontier_step.census_before`); not introduced this round.

### 4. Row count (wave-1 claim "rows=40")
```
$ grep -cE '^\| S[0-9]+' corpus/SOURCES.md
40
```
vs base revision b49948f: `35` — 5 new rows S036–S040 at `corpus/SOURCES.md:42-46`, each
status=`mined` (field 9), dated 2026-10-25, citing the F10 knowledge entries in field 12.
Kill-rule check: new rows are `mined`, not `staged` → "staged row appended unnormalized" limb not triggered;
each new row is cited by F10's two admitted entries → "row without admitted entry" limb not triggered.

### 5. Frontier recheck harness (wave-1 claim "harness 12/12")
```
$ python3 corpus/instruments/frontier-recheck-count.py
PASS F01 … PASS F10 (two entries)
entries=12 pass=12 exit=0
```
12 entry-level records (F09 and F10 each admit two files); all 12 PASS.

## Do-nothing control (base revision b49948f, frozen in claims.json)
```
$ git show b49948f:corpus/README.md | awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}'
9
$ git grep -lE '^source: S0(3[6-9]|[4-9][0-9])' b49948f -- 'corpus/knowledge/*.md' | wc -l
0
$ git show b49948f:corpus/SOURCES.md | grep -cE '^\| S[0-9]+'
35
$ git show b49948f:corpus/SOURCES.md | grep -cE 'S0(3[6-9]|4[0-9])'
0
```
Control scores the `before` values (9, 0, 35) → counters measure a real delta; the claim is not voided
by a degenerate control. `claims.json`'s `assimilation.planned_admit` mentions S055/S056/S057/S060, but
those ids do not exist in SOURCES.md (max S040); the admitted F10 entry cites S036–S040, matching the
`counter` regex and the census rows actually appended. No discrepancy in the measured limbs.

## File:line evidence index
| Fact | Location |
|---|---|
| F10 admitted row | `corpus/README.md:211` |
| Frontier rows F01–F10 | `corpus/README.md:202-211` |
| New source rows S036–S040 | `corpus/SOURCES.md:42-46` (status col `mined`, field 9) |
| source: headers, entry 1 | `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:3-6` |
| source: headers, entry 2 | `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:2-5` |
| r25 entry-count correction | `corpus/README.md:5` ("37 — F10 admits two entries re-grounded from S036-S040") |
| Frozen claim/predicate | `.ufo/waves/round-25/claims.json` claim C2 |

## Tooling directive record
No installs or updates performed; all verification used pre-installed `awk`, `grep`, `git`, `python3`.
Pacman transactions paused per lane rules; nothing was needed.

## Residual risk
- Regex `S0(3[6-9]|[4-9][0-9])` would also match future ids S041+; on today's tree it cannot over-count (max S040, exactly 2 files). If round-26 lands more sources, the counter's limb-2 count will grow — by design.
- Working tree is dirty (uncommitted wave-1 changes; `git status` shows `M`/`??` including `.ufo/waves/round-25/` untracked). Counts reflect the current working tree, not HEAD; HEAD is still b49948f where the control scores 9/0/35.
