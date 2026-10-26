# MutRegistry — round-40 FALSIFY wave 2 — mutation-test the registry gates

Seat: MutRegistry · 2026-10-26 · dispatched by L1 (KasegiR40), hyaku run 9.
Attack surface: `corpus/SOURCES.md` registry rows at verification ref Y (lane tip) — the C2
registry gates (fleet census validator + committed `capture-binding-check.py`).

## Refs and hashes

| item | value |
|---|---|
| lane | /home/vgpnk/Projects/shokunin/kasegi-shokunin |
| Y (lane tip, committed bytes attacked) | `3074c7679d6f527ec3930d7748ccce1dbae4a58a` |
| claims-freeze commit | `5e985b74075dd3813a63d7750966bf8abf693465` |
| base | `a7af2ce63bce153757d39bf66b366a96caf30c13` |
| `corpus/SOURCES.md` @ Y sha256 | `3089f2a25f2714ccff97fe03ee32812ab64d5a03aa17147592acdf3748b5758e` |
| `corpus/instruments/capture-binding-check.py` @ Y sha256 | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |
| fleet detector `scripts/sources-census.sh` sha256 | `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` |
| fixture | `.ufo/waves/round-40/wave2/MutRegistry.mutants.txt` sha256 `18ae5c38a6ca68bfafeb2d89cf7cee78de1d769a88d227e287ca3a63e394954e` |

Lane tip note: `all-gates.txt` (the Y-only receipt) was still untracked at attack time
(`git status` shows `.ufo/waves/round-40/final-gates/` untracked); the committed bytes at
HEAD `3074c767` are the attack surface and equal the frozen-claims bytes for SOURCES.md
(`git show Y:corpus/SOURCES.md` sha256 matches the archive-extracted mirror byte-for-byte).

## Method

Scratch mirror (allowed scratch only): `git archive Y | tar -x` into
`$S/mirror/kasegi-shokunin` (7932 files, full lane tree so used-by paths resolve on disk),
plus a verbatim copy of the fleet `shokunin.conf`. Detectors re-run against the mirror:

1. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $S/mirror kasegi`
   (the claims.json C2 counting command with `--root` pointed at the mirror; fleet root is
   read-only to this seat)
2. `python3 $S/mirror/kasegi-shokunin/corpus/instruments/capture-binding-check.py --root $S/mirror/kasegi-shokunin`
   (the committed instrument from Y, byte-identical to `git show Y:` — sha256 above)

Red = census exit 1 with the expected E-code, or binding exit 1 with the expected rule.
A mutant passing BOTH detectors = defect. Pristine bytes restored and sha256-verified after
every mutant run.

## Pristine baseline (both green — a green re-run is evidence)

```
$ census validate --root $S/mirror kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	$S/mirror/kasegi-shokunin/corpus/SOURCES.md
exit=0
$ capture-binding-check.py --root $S/mirror/kasegi-shokunin
AUDIT records=54 with_url=54 with_fetched_utc=16 with_archival=38 snapshot_dirs=16 manifest_dirs=16 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=54 bound=54 unbound=0
exit=0
```

The two W04 lines are the registry's pre-existing duplicate-URL warnings; warnings do not
affect validate exit (per the census contract). Matches claims C2 "census exit 0".

## Mutants and verdicts

Target rows chosen from the round-40 subject set: S016 (mined, round-40 capture record in
`source-snapshots/round-40/manifest.json`), S017 (mined, record), S001 (mined).

| mutant | mutation (byte-exact rows in fixture) | census | binding | verdict |
|---|---|---|---|---|
| M1-nf12-drop-pipe-S016 | S016 row: trailing `\|` removed (NF 13→12) | exit 1 `E01 S016 fields=10` | exit 0, `records=54 bound=54 unbound=0` | **killed** (census E01) |
| M2-dup-id-S016 | S016 row duplicated as a second proper line | exit 1 `E03 S016 duplicate id` + `E04 S016 duplicate url www.anthropic.com/coordinated-vulnerability-disclosure within scope …` | exit 1 `FAIL rule=dup-id record=S016 rows=2 dir=round-40`, `records=54 bound=53 unbound=1` | **killed** (double-red: census E03+E04 AND binding B2) |
| M3-status-enum-watch-S001 | S001 status cell `mined`→`watch` (contract: watch is NOT a status) | exit 1 `E07 S001 status=watch` | exit 0 | **killed** (census E07) |
| M4a-tier-Apluscommunity-S016 | S016 tier cell `A`→`A+community` | exit 1 `E06 S016 tier=A+community` | exit 0 | **killed** (census E06) |
| M4b-community-at-tierA-S016 | S016 kind `docs`→`community` with tier `A` (contract: community is never tier A) | exit 1 `E10 S016 community-at-A` | exit 0 | **killed** (census E10) |
| M5-usedby-path-missing-S016 | S016 used-by → `corpus/knowledge/defunct-mutregistry-missing.md` (nonexistent) | exit 1 `E11 S016 missing used-by corpus/knowledge/defunct-mutregistry-missing.md` | exit 0 | **killed** (census E11) |
| M6-pipe-inside-cell-S017 | S017 teaches cell gains a literal `\|` (NF 13→14) | exit 1 `E01 S017 fields=12` | exit 0 | **killed** (census E01) |

**7/7 killed, 0 survived, 0 inconclusive. No gate defect found.** Every named mutation is
red on at least one detector; none passes both.

Detector complementarity (evidence, not a defect): binding stays green on M1/M3/M4a/M4b/M5/M6
by design — it binds records by row id + URL + provenance and does not parse NF, tier,
status-enum or used-by paths; the census validator is the sole red detector for those
shapes. M2 is the only mutant in the pair's intersection (row-id integrity), and both
detectors fire there.

## Driver corrections (recorded for verifiability)

- M1 attempt 1 spliced the trailing cell via `split("|")`/`join`, which re-inserts the
  separator — the "mutant" was a whitespace-only equivalent and correctly passed both
  detectors. Not a gate defect; the mutation was re-cut to genuinely drop the trailing pipe
  (row minus final `|` char) and then killed by E01.
- M2 attempt 1 concatenated the duplicate onto one line (missing newline), producing
  NF=25 → E01 `fields=23` instead of the intended duplicate-row shape. Re-cut as two proper
  rows; then census E03+E04 and binding B2 both fired.

## Restoration evidence

- After every mutant run the pristine bytes were rewritten and re-hashed:
  `restored_sha_match=true` for all 7 runs (sha256 `3089f2a2…` each time).
- Final post-restore re-run on the restored mirror: census exit 0 (`kasegi ok`), binding
  exit 0 (`records=54 bound=54 unbound=0`) — baseline re-confirmed green.
- No lane file was edited; the only lane writes are this receipt and
  `MutRegistry.mutants.txt`. No mutating git/jj command was run anywhere (archive/show/
  rev-parse/status only). No tool installs were needed (bash/gawk/python3/git present).
- Scratch `$S=/fast/scratch/hyaku/kasegi-r40/MutRegistry` removed at seat end (H6-clean).

## Reproduction

```
S=$(mktemp -d); mkdir -p "$S/mirror/kasegi-shokunin"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 3074c7679d6f527ec3930d7748ccce1dbae4a58a | tar -x -C "$S/mirror/kasegi-shokunin"
cp /home/vgpnk/Projects/shokunin/shokunin.conf "$S/mirror/"
# per mutant: replace the named row in $S/mirror/kasegi-shokunin/corpus/SOURCES.md with the
# fixture line(s) in MutRegistry.mutants.txt, then:
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$S/mirror" kasegi   # expect exit 1 + named E-code
python3 "$S/mirror/kasegi-shokunin/corpus/instruments/capture-binding-check.py" --root "$S/mirror/kasegi-shokunin"  # M2: expect exit 1 rule=dup-id
```
