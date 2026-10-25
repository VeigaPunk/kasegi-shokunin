# ExecCensusDry — round-29 wave-1 scratch-mirror gate (S043/S044/S045 append)

Seat: `ExecCensusDry-2` (leaf executor). Round: kasegi-shokunin 29, wave 1.
Lane base `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`.
UTC: 2026-10-25 (wave window). Scratch root:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-29/wave1/ExecCensusDry/`.

## What was mirrored

- `corpus/SOURCES.md` copied byte-identical from the lane (`cmp` exit 0) into
  `<scratch>/corpus/SOURCES.md`.
- `corpus/knowledge/` copied (the complete drain of every `mined` row's `used-by`
  target — E11's dependency set). R14-economical: the mirror is 508 KB total
  (knowledge only), no full-corpus copy (snapshots/instruments/lessons are not
  read by `sources-census.sh validate --file`).
- Planned append block applied: rows **S043 / S044 / S045** appended as the last
  three rows of `## Registry` (directly after the S042 row, before `## Paths` —
  no E12).
- F13 entry installed at its repo-relative path
  `<scratch>/corpus/knowledge/program-severity-ladders-and-reward-scales.md`
  (the staged package file, `source:` headers remapped to lane ids S043/S044/S045;
  body carried verbatim).

## Planned append block (registry shape)

| id | staged id | URL | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|
| S043 | S031 | `https://hackerone.com/security/policy_versions` | docs | A | mined | 2026-10-23 | 90d | corpus/knowledge/program-severity-ladders-and-reward-scales.md |
| S044 | S032 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | docs | A | mined | 2026-10-23 | 90d | corpus/knowledge/program-severity-ladders-and-reward-scales.md |
| S045 | S033 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json` | dataset | A | mined | 2026-10-23 | 90d | corpus/knowledge/program-severity-ladders-and-reward-scales.md |

All three `used-by` cells point at the single F13 entry (the only entry citing them),
which exists on disk in the mirror, so E11 passes. No staged-used-by pointer to an
unadmitted entry was carried.

## Gate 1 — scratch validate (BEFORE any real append)

Command:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/corpus/SOURCES.md`

Output:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-29/wave1/ExecCensusDry/corpus/SOURCES.md
```

**Exit 0.** Warnings = the two pre-existing W04 pairs (S028/S029), identical to the
live file's status. No E-findings: no E03 (duplicate id), no E04 (within-scope
duplicate URL), no E11, no E12. The three new URLs collide with no lane row
(`grep -nE 'hackerone\.com/security/policy_versions|bugcrowd/vulnerability-rating-taxonomy'`
on live SOURCES.md → 0 hits before the append).

Scratch census (same file, `census --file`): `rows=45` (42 existing + 3 new),
`tier.A=42`, `status.mined=33`, exit 0.

## Gate 2 — live frozen census command (no change made)

Command (frozen C2 counter, run against the LIVE file):
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`

Output:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

**Exit 0** (`census_exit=0`). Live census row count: **42 rows**
(`census --root … kasegi` → `kasegi rows 42`, `tier.A=39`, `status.mined=30`,
exit 0). Matches the C2 before-state (42 rows).

## Verdict

**PASS — the planned append is gate-clean. Proceed with the real S043/S044/S045
append + F13 entry.** No E03/E04 refusal condition triggered; nothing was refused;
nothing was appended past a finding. The live file was not modified by this seat.

## Handoff notes for ScribeSourcesGate

- Rows must land as the last three rows of `## Registry` (before `## Paths`), ids
  S043/S044/S045 continuing the lane registry from S042 (staged S031/S032/S033),
  each with `used-by` naming the F13 entry `corpus/knowledge/program-severity-ladders-and-reward-scales.md`.
- F13 entry path: `corpus/knowledge/program-severity-ladders-and-reward-scales.md`
  (repo-relative). Its `source:` headers must cite S043/S044/S045 (the three rows
  first registered this round). Caveat for the owning seat: the staged package
  entry also references CNVD/BILISRC material (package S034/S036), which are NOT
  lane-registered this round — the final entry's Q1–Q10 conformance (quote
  locations, recheck form, source-id coverage) is the owning seat's task, not part
  of this census gate.
- Round-29 captures (S043/S044/S045) must exist under
  `corpus/source-snapshots/round-29/manifest.json` for the entry's recheck to pass;
  that is C2's manifest limb, out of this gate's scope (verified by the manifest
  seats).
