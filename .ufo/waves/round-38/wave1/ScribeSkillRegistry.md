# ScribeSkillRegistry — round-38 wave1 receipt

Seat: `ScribeSkillRegistry` (scribe, leaf; no subagent dispatch). Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at `700153593eb586c70a6499c8ca225ee4d673bc9b` (`git -C <lane> rev-parse HEAD`), base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, claims freeze `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`. Axis worked: `depth:verifiability` (C1, registration surface only). Milestone: round-38.

## Item

Draft the SKILL.md Gates & probes registry row for `corpus/instruments/r38-closure.sh` in the exact column shape of the r37 row, and write the single line byte-exact to `.ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md`.

## Sources read before drafting (read-only)

- `.ufo/waves/round-38/claims.json` (72 lines, `frozen_at_utc=2026-10-26T18:17:40Z`): C1 predicate (line 24: export-mode only `--export-ref <hash>`, plain run exit 2, `closed=8/8 exit=0` at J, `selftest cases=8 failures=0`, base `a173b0c2` and r37 judged head `2387dcf6` exports red) and counting commands (lines 27-31). Not edited.
- `.ufo/waves/round-38/wave1-spec.json` item `ExecSuiteBuild` (instrument build spec, the authoritative suite contract for flags/output/G1–G8): flags `--export-ref <hash>` (plain run exit 2), `--selftest [--export-ref <hash>]`, `--lane DIR`, `--work DIR`, `--scratch-root DIR`, `-h`; output header `export-ref=<hash> mode=export lane=<lane> suite-sha256=<digest>`, one `G<n> payload=k=v,... closed=0|1` per check, then `closed=<k>/8 exit=<0|1>`, exit 0 only when 8/8; selftest `selftest case=G<n> …` + `selftest cases=8 failures=0`; G1 D-A, G2 D-B, G3 D-C, G4 D3, G5 D-D, G6 D-E, G7 D-F, G8 r37-closure carry-over `closed=14/14`.
- `corpus/lessons/round-37-verifier-spotcheck.md` §5 (D-A…D-E routed defects) as referenced by the claim.
- `SKILL.md` table: header at line 1108 `| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |`, delimiter line 1109, r37 row at line 1112. Registry table section anchors: `## Gates & probes registry` (L977), per-round append sections L1037/L1050/L1060/L1073/L1093/L1106; file ends at L1113 (last row is the round-36 D5 correction).

## Commands and actual outcomes

1. Locate the shape to copy:

```
$ grep -nE '^\| *r3[67]-closure\.sh' SKILL.md
1111:| r36-closure.sh | gate\|probe | `bash corpus/instruments/r36-closure.sh --export-ref <hash>` …
1112:| r37-closure.sh | gate | `bash corpus/instruments/r37-closure.sh --export-ref <hash>` (export-mode only; a plain run refuses with exit 2) | one `E<n> payload=… closed=0\|1` line per check E1–E14, then `closed=K/14 exit=0\|1`; exit 0 only for K=14; exit 2 on harness error or plain run; 0 closed \| 1 open \| 2 could-not-evaluate | … | kasegi (round 37) |
1113:| r36-closure.sh | gate | … | kasegi (round 36; D5 correction appended round 37) |
```

   Header/row line numbers confirmed: `1108` = header (8 columns), `1109` = `|---|---|…|`, `1112` = r37 row.

2. Table-column measurement (pipes are escaped as `\|`; raw awk NF therefore counts them, so net NF = raw NF − escaped count):

```
$ awk -F'|' 'NR==1108{h=NF} NR==1112{r=NF; e=gsub(/\\\|/,"@")} END{print "header_net_nf="h" r37_raw="r" r37_escaped="e" r37_net_nf="r-e}' SKILL.md
header_net_nf=10 r37_raw=14 r37_escaped=4 r37_net_nf=10

$ awk -F'|' '{raw=NF; e=gsub(/\\\|/,"@"); print "raw_nf="raw" escaped="e" net_nf="raw-e}' .ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md
raw_nf=14 escaped=4 net_nf=10
```

   Note for reproduction: assign `NF` to a variable *before* `gsub` on `$0` — `gsub` rewrites `$0` and awk re-splits, so `print NF` after `gsub` reports the post-substitution count.

3. Cell parse of the deliverable (escaped pipes restored to a placeholder, then split):

```
nf 10
0 |
1 | r38-closure.sh
2 | gate
3 | `bash corpus/instruments/r38-closure.sh --export-ref <hash>` (export-mode only; a plain run refuses with exit …
4 | one `G<n> payload=… closed=0|1` line per check G1–G8, then `closed=K/8 exit=0|1`; exit 0 only for K=8; …
5 | `bash corpus/instruments/r38-closure.sh --selftest [--export-ref <hash>]` -> `selftest cases=8 failures=0` exit 0
6 | base export `a173b0c2` -> `closed<8/8 exit=1`; r37 judged head `2387dcf6` -> `closed<8/8 exit=1`
7 | read-only (export to a scratch work dir)
8 | kasegi (round 38)
9 |
ends_with_single_newline True ; trailing_spaces False
```

   Eight populated cells in the r37 cell order (name, type, entry command, verdict map, self-test, pinned-value path, write scope, owner); type is the single unescaped choice `gate`; the verdict-map cell carries `0 closed \| 1 open \| 2 could-not-evaluate` with escaped pipes, so nothing breaks the table.

4. Anchor check on a scratch copy of SKILL.md with the row appended (copy made at the scratch path, so the lane root is pinned explicitly — otherwise `anchorcheck.py` derives the lane from the checked file's ancestors and reports 16 lane-relative cites `OUTSIDE-BASE`/`BASE-ABSENT`, exit 1):

```
$ cp SKILL.md $S/SKILL.copy2.md && cat <deliverable> >> $S/SKILL.copy2.md
$ KASEGI_LANE_ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin python3 corpus/instruments/anchorcheck.py $S/SKILL.copy2.md
== …/SKILL.copy2.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchorcheck exit=0
```

   Control: the same command on the committed `SKILL.md` exits 0 (16 `OK` lines, `PIN-BROKEN=0`); its self-test prints `selftest cases=12 failures=0`, `limbs=9 covered=9`, exit 0.

5. The append changed nothing before EOF of the copy:

```
$ head -n 1113 SKILL.copy2.md | cmp - SKILL.md && echo "prefix2 identical"
prefix2 identical
$ wc -l SKILL.copy2.md
1114 SKILL.copy2.md
```

6. Deliverable integrity:

```
$ wc -l .ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md
1
$ wc -c .ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md
1446
$ sha256sum .ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md
502bd887707d831599cd70a577c3c1fa139c3ad83199d6dafde5df659bce1efe
$ cmp <deliverable> $S/row.md && echo "deliverable == verified scratch row"
deliverable == verified scratch row
```

7. Pointed-hash provenance in the row: `git -C <lane> cat-file -t f3246559` -> `commit`; `git -C <lane> rev-parse f3246559^{commit}` -> `f3246559bed2fd085dde860e00247ce394f02bad` (round-37 wave-evidence commit, G5/D-D target). Historical prefixes `a173b0c2` (base) and `2387dcf6` (round-37 judged head) are the claim's own control refs.

8. Lane untouched outside the wave dir: `git -C <lane> status --porcelain SKILL.md` empty; full status shows only `.ufo/waves/round-38/wave1.ready`, `wave1.ready.partial` and the `wave1/` directory (other seats' artifacts).

## Deliverable

- Path: `.ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md`
- Bytes: 1446; lines: 1 (single line + trailing newline); sha256 `502bd887707d831599cd70a577c3c1fa139c3ad83199d6dafde5df659bce1efe`
- Contents: exactly one Markdown table row; no heading, note or validation text is in the file. The row is intended to be appended under the round-38 registry append section (the L1 owns the heading/header line); it was verified to keep the table 8 columns wide against the committed header.

## Findings and limits

- Registration, not a live-green claim. `corpus/instruments/r38-closure.sh` is not yet in the lane at wave time (`ls: cannot access 'corpus/instruments/r38-closure.sh': No such file or directory`); `ExecSuiteBuild` delivers it as `.ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh` for the L1 to land. The row therefore records the frozen C1 contract plus the `ExecSuiteBuild` item's flags/output/G1–G8 semantics; the pinned values (`base export a173b0c2 -> closed<8/8 exit=1`; `r37 judged head 2387dcf6 -> closed<8/8 exit=1`) are the claim's control expectations, not values I observed. This is the same disclosure the round-35 registry append carried, and the parent's post-integration gate is what turns them into measured values.
- The r37 row's own verdict-map cell mixes emitted-line shape with the compact `0 closed | 1 open | 2 could-not-evaluate` map; this row mirrors that shape so a reader can diff the two rows line-for-line. The `r37` row itself is a single-choice `gate` row; the earlier `gate\|probe` rows (r35/r36) are untouched.
- No tool installs, no network fetches, no git/jj mutations, no writes outside the deliverable plus scratch. `claims.json`, `SKILL.md`, `wave1-spec.json` and all sibling artifacts were read only.
- Scratch: `S=/fast/scratch/hyaku/kasegi-r38/ScribeSkillRegistry` was created with `mkdir -p`, held `row.md`, `SKILL.copy.md`, `SKILL.copy2.md`, `prefix.md`, `prefix2.md`, `ac-*.txt`; removed with `rm -rf -- "$S"` after the deliverable and this receipt landed (removal verified: `test -e "$S"` false).
