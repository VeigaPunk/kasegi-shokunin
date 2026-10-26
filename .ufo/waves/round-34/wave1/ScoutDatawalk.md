# ScoutDatawalk — round-34 planner data-walk (leaf, read-only)

Scope: replay the frozen BEFORE values at freeze commit `29f606dbdd28aff6fd4573ab4b90788bbb90af13`
(`git rev-parse 29f606db` = that sha), confirm claims.json counters/predicates, compare kill-rule strings.
Method: `git archive 29f606db | tar -x -C /fast/scratch/hyaku/kasegi-r34/ScoutDatawalk/f` (no repo mutation).
Scratch deleted before yield.

## Report

### 0. Integrity
- `git show 29f606db:.ufo/waves/round-34/claims.json | sha256sum` = `dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850`;
  working-tree `claims.json` has the identical sha256 (unchanged since freeze).
- `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt` are **byte-identical**
  (all `d90ce017…db5f0`): each file holds the C1, C2 and census sections. Not a defect, but the three names are not three independent receipts.
- **Command provenance gap:** before.txt records outputs only, not the commands. I reconstructed the commands (below). One before
  line (round-33 lesson "erratum present? = 4") has no recoverable command — see §2 F-3.

### 1. BEFORE replay at freeze (every line matched except as noted)

| before value (stored) | command I replayed in the freeze export | observed | match |
|---|---|---|---|
| `ls_exit=2` r-defect-closure.sh absent | `ls corpus/instruments/r-defect-closure.sh` | `ls: cannot access … No such file or directory`, `ls_exit=2` | YES |
| `selftest cases=11 failures=0` | `python3 corpus/instruments/capture-binding-check.py --selftest` | 11 `case=… verdict=pass` lines, `selftest cases=11 failures=0`, exit 0 | YES |
| `<LANE_HASH>` = 2 | `grep -c '<LANE_HASH>' SCORECARD.md` | `2` | YES |
| r32 manifest S049/S050 fetched_utc `'2026-10-25T23:14:00-03:00'`, archival None | json load `corpus/source-snapshots/round-32/manifest.json` `.sources[]` | `S049 '2026-10-25T23:14:00-03:00' archival= None`; `S050 '2026-10-25T23:14:00-03:00' archival= None` | YES |
| r26 `records= 1 paths= ['S041.txt']` (S040-live orphan) | json load `round-26/manifest.json` | `records= 1 paths= ['S041.txt']`; `ls -la round-26/` shows `S040-live.txt` 33463 B on disk with no record → orphan CONFIRMED | YES |
| QUALITY `'exactly one'` = 1 | `grep -c 'exactly one' corpus/QUALITY.md` | `1` (line 169, R20) | YES |
| round-33 lesson erratum = 4 | unknown; `grep -c 'Erratum' corpus/lessons/round-33.md` | `4` (but `grep -c 'erratum'`=5, `-ci`=8, `-o -i`=12 occurrences, `R7`=0) | 4 reproduces only with capital-E `Erratum`; see F-3 |
| frontier = 16 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `16` | YES |
| rows = 50 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `50` | YES |
| S051_rows = 0 | `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | `0` | YES |
| entries citing S051 = 0 | `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` | `0` (pattern valid: same pattern returns 1 each for S048, S049, S050) | YES |
| harness `entries=19 pass=19 exit=0` | `python3 corpus/instruments/frontier-recheck-count.py` | last line `entries=19 pass=19 exit=0`, exit 0 (last row `PASS F16 … ids=S049,S050`) | YES |
| source-recheck S051 `manifest UNAVAILABLE reason=missing` exit 2 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | `manifest UNAVAILABLE reason=missing`, `recheck_exit=2` | YES |
| knowledge entries = 45 | `ls corpus/knowledge/*.md \| wc -l` | `45` | YES |
| census: W04 S028, W04 S029, ok, exit 0 | `scripts/sources-census.sh validate --file <export>/corpus/SOURCES.md` and live `validate --root /home/vgpnk/Projects/shokunin kasegi` | both: `W04 S028 … docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq`, `W04 S029 … eur-lex.europa.eu/eli/reg/2024/2847/oj/eng`, `ok`, exit 0 (script is read-only: writes only stdout/--out) | YES |
| unchanged baseline `records=40 bound=40 unbound=0 exit=0` | `python3 corpus/instruments/capture-binding-check.py` | `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2` / `records=40 bound=40 unbound=0` exit 0; note round-32 `fetched=2` — the frozen instrument ACCEPTS the `-03:00` local-offset (R8 defect live) | YES |

Survivor mutants (frozen kill rule), reproduced as exactly-once textual patches on the freeze `capture-binding-check.py`:
- skip-selftest (`CASES = [` → `CASES = [] and [`): `--selftest` prints `selftest cases=0 failures=0`, exit 0 → CONFIRMED (F-5 not caught); plain run unchanged `records=40 bound=40 unbound=0`.
- accept-record-without-url (`return False, [...detail=absent]` → `return True, []`): on the real tree plain run `records=40 bound=40 unbound=0` exit 0; on the `case_record_without_url` fixture `records=2 bound=2 unbound=0`, exit 0 → CONFIRMED survivor of the plain-run rule. (The 11-case `--selftest` DOES kill it: `cases=11 failures=1`, exit 1 — so the survivor exists only under a plain-run-only rule, consistent with the stored wording.)

### 2. Findings (for the L1; I do not judge)

**F-1 (C2, verifiability) — junk-twin rejection has no executable form as phrased.** claims C2 predicate/kill-rule: "junk twin … rejected: source-recheck exit != 0 and non-author reviewer REFUSE" / kill "junk twin passes source-recheck". `source-recheck.py` takes `--manifest … --source S051`, never a markdown file. The junk twin's own `recheck:` line (`c2-controls/junk-f17.md`, sha256 `2752a994…4026`) is byte-identical to the real entry's recheck command, so at tip both exit 0 (observed at the live tip: `S051:sha256 OK`, 18 assertions OK, exit 0). At BEFORE the junk exit 2 equals the real entry's exit 2 (manifest absent) — the before control (`junk_recheck_exit=2`) does not discriminate junk from real. Literal kill-rule clause "junk twin passes source-recheck" therefore fires at tip unless the L1 reads it as "source-recheck on a quote check of the twin's text".
**F-1b — the twin's quote is not fabricated.** `junk-f17.md` says Critical includes "Direct theft of any user funds" and tags it `[FABRICATED — no capture holds this quote]`. The live capture `corpus/source-snapshots/round-34/S051.txt:75` holds `- Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield` and `grep -c "Direct theft of any user funds" S051.txt` = 1; manifest.json:55 asserts the full sentence. A substring quote check passes the twin's quote. The only rejection that can work is reviewer/semantic (the twin's own file label), not a capture check. Also `r-defect-closure.sh:404-408,436` (R9) only tests that `junk-f17.md` EXISTS (`junk=$junk` in DESC) — it does not demonstrate rejection, so "closed 9/9" does not cover "rejected".

**F-2 (C2) — "every assertion occurrences=1" is false at tip.** claims C2 counting command: "all occurrences=1, sha256 OK, exit 0". Live tip `source-recheck --source S051` exit 0 but `S051:Q17 OK occurrences=2 anchor=96-ok` and `S051:Q9 OK occurrences=2 anchor=77-ok` (anchored per round-30 Q9/B2, which is the instrument's legitimate path). Exit 0 and sha256 OK hold; the "=1" wording does not. Suggest an appended note (claims frozen).

**F-3 (C1) — the R7-erratum before-control is non-discriminating.** before.txt "round-33 lesson erratum present? 4" counts pre-existing `Erratum` lines (capital-E `Erratum` at round-33.md lines 17, 91, 92, 138), not an R7 erratum: `grep -c 'R7' corpus/lessons/round-33.md` = 0 at freeze. The command is not recorded and `grep -c erratum` gives 5, `-i` 8. The after-state gate should be `R7`-specific (and the char-count/S050.txt:70 text), not an erratum-count delta.

**F-4 (predicate/counter agreement).**
- Agree: counting-literals for frontier 16→17, rows 50→51, S051 row 0→1, S051 entries 0→1, harness 19→20 / 19→20, knowledge entries 45→46 (tip: 17/51/1/1, `entries=20 pass=20 exit=0`, 46), `<LANE_HASH>` 2→0 (tip 0), census W04 S028/S029 only, N>=19 for capture-binding selftest (11 base + 9 named after-cases = 20).
- Disagree/gap: (a) `PASS F17 ids=S051` is not a grep-able literal: harness prints `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0` (`grep -c 'PASS F17 ids=S051'` = 0 at tip); claims "after" uses an ellipsis form, the C2 predicate and the wave context do not. (b) claims counting command `capture-binding-check.py -> records=40 bound=40 unbound=0` is superseded by `claims-erratum-1.md` (41 records after S051) — disclosed, no objection. (c) C1 `kill_rule` enumerates only: suite missing/closed/selftest counts/capture-binding N/survivors/closure-self-test/`<LANE_HASH>`/r32 manifest/S040 — it has no clause for erratum 2 (R2), QUALITY R20 note (R3), R7 erratum, rule A bidirectional (R9) or junk twin committed; those ride only on `closed=9/9`, whose R-checks are the suite's own. (d) "strict UTC" is not defined in claims.json (Z-only vs `+00:00`); r-defect-closure.sh R8 uses `^…T.*Z$` with no `-` offset. (e) the predicate's "closed=0/9 on the base tree" is stated but not in any counting command and cannot be replayed from before.txt (suite absent at base).

**F-5 — kill rules identical in claims.json and the wave context?** NO COMPARISON POSSIBLE AS STATED: the wave context (`wave1-spec.json` `.context`, 4762 chars; `build-spec.py` HEAD) carries the predicate summary of C1/C2 and the non-claim items but contains **no kill-rule text**; the string `suite missing (ls_exit=2)` occurs in exactly one file in the lane tree, `.ufo/waves/round-34/claims.json` (`grep -rl`, excluding .git/.jj). The kill rules are therefore authoritative in claims.json only; no second copy exists to diverge from. Predicate summary in the context vs claims.json predicate: context says QUALITY R20/R23, junk twin "committed under c2-controls/ and rejected" (same F-1 issue), `entries=20 pass=20 exit=0 incl. PASS F17 ids=S051` (same F-4a); context adds items (erratum 2, pre-freeze satisfiability, R7 erratum) absent from claims C1 predicate sentence (they appear in claims `after`).

### 3. Digests (freeze export, sha256)
- `SCORECARD.md` e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3
- `corpus/SOURCES.md` b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b
- `corpus/README.md` 3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932
- `corpus/QUALITY.md` 00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087
- `corpus/lessons/round-33.md` ca17591d4a36e1a6623adb9acb7ac2bc0a3dbd87c24f3913229fe0b4b781feb2
- `round-32/manifest.json` 6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774
- `round-26/manifest.json` 1c9131326106eca5860f5c650b2c9c4efa860da52a701b039b457aba619e3247
- `corpus/instruments/capture-binding-check.py` b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9
- `corpus/instruments/frontier-recheck-count.py` aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893
- `corpus/instruments/source-recheck.py` fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003
- live `corpus/source-snapshots/round-34/S051.txt` 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5
- `claims.json` dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850

### 4. Tooling / cleanup
No tool installed or upgraded. No repo mutation (no git add/commit, no jj mutation); fleet root and shokuknow untouched (census script run read-only). Scratch `/fast/scratch/hyaku/kasegi-r34/ScoutDatawalk/` removed after this receipt was written.
