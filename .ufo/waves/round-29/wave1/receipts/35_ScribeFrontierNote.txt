# ScribeFrontierNote — round 29 wave 1 · F13 frontier narrative input (draft)

Seat: `ScribeFrontierNote-2` (UFO-FSD scribe, leaf — no subagent dispatch, no background jobs, no own swarm).
Lane: `kasegi-shokunin` — only write scope. Fleet root write-excluded.
Round: kasegi r29, build+attack, one v2 wave, 64 seats (band floor), run-7 routing; inline spawn handoff (hyaku run 7).
Revisions: lane base `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims-freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`.
Written (UTC): `2026-10-25T18:16:49Z`.
Answering model: `inception/mercury-3` (run-7 route table / session config; no per-seat model passed by this leaf — rule 8).

> **State verdict at writing: PRE-STATE for every C2/F13 landing fact.** At the time this note is
> written the admission has NOT landed. Measured in the live lane (2026-10-25T18:16Z):
> frontier_admitted=**12**, registry_rows=**42**, entries citing S04[3-5]=**0**,
> `corpus/knowledge/program-severity-ladders-and-reward-scales.md` **absent**, round-29 manifest
> **absent** (`corpus/source-snapshots/round-29/` exists, empty of manifest). All "after" figures
> below are the frozen claim **C2 targets** (`claims.json` C2 predicate), not measurements.
> Re-run named: after `ExecEntryF13` / `ScribeSourcesGate` land, the main agent re-runs the C2
> counter_commands verbatim (awk frontier count, `grep -lE '^source: S04[3-5] '`, registry row
> grep, `sources-census.sh validate`, `frontier-recheck-count.py`, `source-recheck.py` ×3 on the
> round-29 manifest). Label M28-1 rule: never compare a PRE-STATE number to an after column.

## 1. Expansion-credit statement for F13

**Coverage-map ground the lane did not hold before F13.** At the round base (measured, committed:
`.ufo/waves/round-29/c2-controls/before.txt`) the frontier held F01–F12 (12 admitted) and no
surface covered **program severity ladders and reward scales** — how a program maps a finding onto
its own severity ladder and prize scale. F01 holds CVSS-B semantics only (score ≠ business risk,
≠ reward); no knowledge entry and no registry row existed for any platform-level policy-set ladder.
Measured at freeze: registry 42 rows, entries citing S04[3-5] 0, frontier 12.

**Sources opened this round** — three rows first registered this round (tier A, status `mined`,
adopted **by document** — URL equality, never staged-id arithmetic — continuing the lane registry
from S042; claim C2 `staged_rows_adopted` S031→S043, S032→S044, S033→S045):

| Lane row | Staged id | Document | URL | Anchor |
|---|---|---|---|---|
| S043 | S031 | HackerOne standard program policy set | `https://hackerone.com/security/policy_versions` | Program Scope and Assets and Denial-of-Service (DoS) Policy sections; policy record id 3787452, record timestamp 2026-10-16T15:34:59.854Z |
| S044 | S032 | Bugcrowd VRT repository README | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | Description; Data within an Entry, Priority; VRT open-sourced April 2017 |
| S045 | S033 | VRT CWE mapping dataset | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json` | content, 36 top-level categories; broken_access_control/idor maps to CWE-932; metadata.default null |

**Entry citing mined rows S043–S045:** exactly one knowledge entry,
`corpus/knowledge/program-severity-ladders-and-reward-scales.md`, carries header `source:` ids
S043/S044/S045 and is bound by the frontier harness to its own `recheck:` `--source` selections
(QUALITY R12). Registry increment target 42 → 45.

**Planned deviation (disclosed, not hidden):** the packaged staged entry
(`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/program-severity-ladders-and-reward-scales.md`)
cites staged S032/S033/S034/S036; the lane admission cites **S043–S045** per frozen C2, so the
landed entry's source set differs from the staged bytes — staged S034 (CNVD 众测 helpList) and
S036 (BILISRC V1.7) are not adopted rows this round. The re-grounding is the object of C2's
counters, not of this note.

**Wave-execution evidence observed (uncommitted working files — not proof of landing):**
`wave1/README.md` (Bugcrowd VRT README, capture-like bytes) and `wave1/cwe.json` (27.8 KB, CWE
crosswalk JSON, 36 top-level categories) exist under `.ufo/waves/round-29/wave1/` at writing; they
match the S044/S045 staged URLs. Final captures and pins are expected under
`corpus/source-snapshots/round-29/manifest.json`.

## 2. Frontier-before/after count: 12 → 13

- Before (measured): `c2-controls/before.txt` line 4 `12`; own `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → `12`.
- After (C2 target, PRE-STATE): 13 — F13 row appended after F12; harness target `entries=16 pass=16 exit=0` (the C2 counter-command 5), registry 45, census exit 0, `source-recheck` exit 0 per id on the round-29 manifest.

## 3. Next-step cell proposal (draft text for the F13 row's `next` cell)

> Treat each ladder as a dated, program-specific baseline: read the program's own brief before applying the VRT priority, and never translate payout or award between programs (per-asset caps and business-tier scaling differ).

Grounded in the admitted rows: S044 teaches the VRT P1–P5 is a *suggested* baseline the program
may override (complexity, bounty brief, unusual impact); S043 teaches a program can only cap and
scope what it controls (per-asset caps per finding class); S045 teaches the ladder is machine-
mapped onto CWE with visible gaps (`cwe: null`).

Forward opportunity (separate from the cell; flagged, not claimed): the merge package stages
sibling themes — *program scope rules and asset boundaries* and *claim packaging and report
quality* — that pair naturally with F13 and remain candidates for later rounds with their own
registered rows.

## 4. Original domain-root map sentence stays untouched (0/18)

The sentence at `corpus/README.md:215` — "The original domain-root map is exhausted: 0/18
surfaces are present." — and the r28 parenthetical (0/18 denominator holds; frontier count stays
outside it) are **not edited** by F13. F13 is public-practice frontier ground and is not counted
into the domain-root 0/18 figure. The r29 amendment below mirrors the r28 amendment style (append,
never rewrite — QUALITY R9).

## 5. Proposed README edit draft (for L1/main-agent integration — not applied by this note)

**A. Frontier row, appended inside the table immediately after the F12 row (currently line 213;**
**insertion shifts lines ≥214 by +1 — verified: no live corpus/SKILL/SCORECARD file cites README**
**lines ≥214 today; the only ≥190 citation is the historical r25 verifier lesson `:129` → :211,**
**unaffected by an insertion below it):**

```
| F13 | Program severity ladders and reward scales | admitted | knowledge/program-severity-ladders-and-reward-scales.md | S043, S044, S045 | Treat each ladder as a dated, program-specific baseline: read the program's own brief before applying the VRT priority, and never translate payout or award between programs (per-asset caps and business-tier scaling differ). |
```

**B. Appended amendment block, after the `[r28 amendment, appended 2026-10-25]` block:**

```
[r29 amendment, appended 2026-10-25] The preceding parenthetical records the round-28 frontier state and is
retained as history, not rewritten (R9): at round 29 the frontier stands at 13/13 admitted —
F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at
round 29 (S043-S045, opened 2026-10-25). The 0/18 sentence is untouched: the lost-domain
denominator still holds 0 of 18 surfaces present, and the frontier count stays outside it.
```

**Main-agent verification checklist (post-landing, named re-runs):**
1. `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → 13.
2. `grep -lE '^source: S04[3-5] ' corpus/knowledge/*.md | wc -l` → 1.
3. `grep -cE '^\|[[:space:]]*S04[3-5][[:space:]]*\|' corpus/SOURCES.md` → 3 (registry rows 45).
4. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 (W04 S028/S029 only).
5. `python3 corpus/instruments/frontier-recheck-count.py` → `entries=16 pass=16 exit=0`.
6. `source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043|S044|S045` → exit 0 each, manifest assertions `occurrences=1` (Q9).
7. Round-29 manifest exists and pins captures; entry `recheck:` is one executable cwd-invariant command (Q10) covering exactly S043/S044/S045.
