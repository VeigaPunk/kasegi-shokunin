# MutEntries — round-40 wave-2 mutation probe of the new knowledge entries' gates

Seat: MutEntries (leaf mutation-tester, round 40 wave 2, hyaku run 9).
Item attacked: the gate trio named in the seat item — `source-recheck.py`,
`recheck-audit.py`, `frontier-recheck-count.py` — as detectors of entry-level
defects in the eight knowledge entries added this round. Verification ref:
lane tip `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (Y), mirrored via
`git archive`; never a write to the lane.

**Verdict: 1 of 41 mutants killed, 40 survived.** The one kill is M1
(dropped `source:` line) on the single frontier-scoped new entry, caught by
`frontier-recheck-count.py`. Four full mutant classes survive all three gates
on all eight entries (quote truncation, number change, falsifiable-rule
deletion, credential insertion), plus M1 survives on the seven non-frontier
new entries. Per the seat contract these survivors are coverage findings, not
permission to change anything.

## Baselines (protocol: red baseline = inconclusive, so these came first)

Mirror: `git -C <lane> archive 3074c76… | tar -x` into scratch; verified
byte-identical to a second fresh extraction (`diff -r` clean, 7932 files +
58 symlinks). No network fetches were made; no tools installed (stdlib
python3 only).

- **B0 — exact Y bytes, no adaptation:** G1 rc=0 (8/8 records `sha256 OK`);
  G2 rc=0 (`strict pass=59/59`, frozen `59/59`, expect 59/59; fail-closed=24 =
  the audit's documented `gated` state on the absent base); G3 rc=0
  (`entries=26 pass=26 exit=0`).
- **B1 — adapted mirror, unmutated:** all three gates rc=0. Adaptation (the
  only transformation, applied identically to every farm including the
  baseline): the recheck lines' literal `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`
  rewritten to `cd <farm> &&` in every `corpus/knowledge/*.md`, so executed
  lines re-check farm bytes instead of the real lane. Without it the harnesses
  execute the committed lines against the untouched lane and every mutant is
  invisible by construction.

## Method

8 new entries (all added in `4766b9d`) × 5 mutation classes + 1 extra = 41
mutants, each in its own `cp -al` hardlink farm, one entry file mutated, all
three gates run against the farm, entry then restored and hash-compared.

| class | instantiation (per entry) | expected detector (pre-registered) |
|---|---|---|
| M1 drop `source:` line | delete the single `^source: S\d+` header line | G3 rule A `no-source-line` for frontier entries; none for the rest |
| M2 truncate a quote | first `> "…"` blockquote cut to ~40 %, closing quote dropped, `— SXXX.txt:Lnn` attribution kept | none known |
| M3 change a number | first attribution line-anchor `Lnn → Ln(n+1)` (e.g. `S060.txt:L4 → L5`) | none in trio; anchorcheck only if backticked cites existed |
| M3b change a count | cyclonedx FC-3 "`6 9 5 3`" → "`7 9 5 3`" | none |
| M4 drop falsifiable rule | delete `## Falsifiable rule` section through next `## ` (13–15 lines/entry) | none |
| M5 add credential-like string | append `api_key = "AKIAIOSFODNN7EXAMPLE", token = "ghp_0123…"` line at EOF | none |

## Results

| class × entry | G1 source-recheck | G2 recheck-audit | G3 frontier-recheck |
|---|---|---|---|
| M1 × cyclonedx-analysis-subtree (F23/S060) | 0 | 0 | **1 — KILLED**: `FAIL F23 … problems=no-source-line`, `entries=26 pass=25 exit=1` |
| M1 × other 7 new entries | 0 | 0 | 0 — **survived** |
| M2 × all 8 | 0 | 0 | 0 — **survived** |
| M3 × all 8, M3b × cyclonedx | 0 | 0 | 0 — **survived** |
| M4 × all 8 | 0 | 0 | 0 — **survived** |
| M5 × all 8 | 0 | 0 | 0 — **survived** |

G1 is entry-blind by construction (it reads manifest + captures only) and
stayed green under every mutant — recorded as the capture-side control.
G2 reads only each entry's recheck *line* (form limbs: parse/cwd/paths +
strict cdroot/instrument/own + expected-list equality); entry body content is
invisible to it. G3 binds ids and executes the recheck line; it never reads
quote text, body numbers, the falsifiable section, or non-frontier entries.

## Gate gaps (coverage findings)

- **GG-1 — G3 scope gap.** `frontier-recheck-count.py` audits only
  frontier-table-admitted rows; 7 of the 8 new entries are outside it, so
  their entry↔source binding is enforced by no gate. Demonstrated mitigation
  outside the trio: the C2 counting command
  `grep -rlE '^source: S0(16|17|19|20|21|22|23|24|25)' corpus/knowledge | wc -l`
  drops 7→6 with the M1 mutant present and returns 7 after restore — so the
  round-closer's claim audit would catch it for the nine-rows set, but that
  is a frozen claim command, not a reusable gate, and it covers only that
  hard-coded row set.
- **GG-2 — entry-quote fidelity.** No committed instrument compares an
  entry's blockquotes to the captured bytes. `source-recheck.py` pins the
  *manifest's* quotes; the entry's own quotes are self-attested FC-1 prose. A
  quote silently truncated to misattribute a source survives all three gates
  (and `capture-binding-check.py` binds manifest↔registry↔provenance, not
  entry quotes).
- **GG-3 — line-attribution drift.** A ±1 shift in an entry's `SXXX.txt:Lnn`
  attribution is invisible to the trio, and `anchorcheck.py` is blind here
  too: it counts only backticked `path:NN` cites and reports `0 distinct
  anchors` for both the pristine entry and the M3 fixture. Counted enums
  (M3b's `6 9 5 3`) are likewise unpinned.
- **GG-4 — falsifiable-rule presence.** No gate requires the section; G2's
  completeness counts files and recheck-line form only. A stripped entry
  still passes 59/59.
- **GG-5 — credential hygiene.** No committed instrument scans knowledge
  entries for credential-like strings (grep over `corpus/instruments/*.py`
  for secret/credential/API-key patterns: no hits; `sources-census.sh`
  W/E codes cover registry shape, not secrets).

Boundary honesty: the frozen claims do not promise the trio catches these
classes — C2's kill rule keys on capture-side rechecks, the harness tally and
census. These are gaps in the gates my seat was told to attack, plus one
real scope asymmetry (GG-1) worth a future instrument, not a contradiction of
C1/C2.

## Restoration evidence

- Per-mutant: entry rewritten back to adapted-pristine bytes and sha256
  compared — 41/41 verified (MANIFEST `restored_sha256_matches_adapted`).
- Whole tree: `diff -r` of the final pristine extraction vs the working
  mirror — clean after all runs.
- Lane: never written by this seat; the two deliverables below are the only
  lane paths touched.
- One probe crash during setup (a regex assuming a `SXXX.txt:` prefix) and
  one hardlink bug in my first driver build (adaptation written through
  `cp -al` links contaminated the scratch extraction) were both fixed before
  any verdict was recorded; all recorded runs are from the corrected driver
  with a contamination guard asserting the source extraction still carries
  the unadapted lane path.

## Deliverables and cleanup

- This receipt: `.ufo/waves/round-40/wave2/MutEntries.md`
- Byte-exact attack fixtures (41 mutant entry files) + `MANIFEST.json`
  (per-mutant description, pristine/mutant sha256, per-gate rc and summary
  lines, baselines) + killed-mutant G3 transcript + B0 gate outputs + the
  probe driver: `.ufo/waves/round-40/wave2/MutEntries.mutants.tar.gz`
  (sha256 `44f3b3cd815f8e011f82e6d681c66ad719ad9073ea6711238e42ccc8cf10f74e`).
- Scratch `/fast/scratch/hyaku/kasegi-r40/MutEntries/` removed before
  yielding. Tooling installs: none.
