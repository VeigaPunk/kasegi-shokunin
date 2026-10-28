VERDICT: DRAFT-READY

Seat: R45ScribeCorrections (scribe, leaf). Scope: C1/R1 correction line plus F27 admission text. Draft only: nothing applied to a shared file, nothing committed, no git mutation. Draft file: `.ufo/waves/round-45/wave1/R45ScribeCorrections.draft/appends.md`, four blocks A-D, each delimited by `=== BLOCK X ... ===` / `=== END BLOCK X ===` sentinels. The sentinels are not appended text. L1 adds one blank separator line before each block, as the round-44 blocks do.

Status of the claims: R1 is NOT fixed in the lane tree by this seat. The draft lesson line passes the R1 predicate only together with an S072 registry row, which is not in the lane tree and which this seat did not author (see limitations). F27 is NOT admitted in the lane tree; the frontier count moves only when block B lands.

## 1. Block A — round-44 lesson correction (R1 limb)

Attacked: `corpus/instruments/r45-routed-defects.py` limb `R1` (the `Correction (round 45` tail predicate, `hit` list) with the draft line from block A, appended to `corpus/lessons/round-44.md`.

Live re-measurement of the S070 body (this seat, 2026-10-28):

    $ curl -sS -L -o api.json -w 'http=%{http_code} bytes=%{size_download} final=%{url_effective}\n' https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section
    http=200 bytes=10588 final=https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section
    $ python3 -c "...d=json.load(...); b=d['body']; print('body chars',len(b),'bytes',len(b.encode()))"
    body chars 10029 bytes 10031

The body is readable text (it begins `\nWelcome to the VRP rules section!`), so the S070 "JavaScript shell" reason is wrong. Pinned snapshot compared to the live body:

    $ diff body.txt corpus/source-snapshots/round-45/S072.txt; echo "diff exit=$?"
    311a312
    > 
    diff exit=0
    $ python3 -c "...print(len(s))"   # S072.txt
    10030    (bytes 10032, sha256 364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025)

So the pinned file is the body plus one trailing newline (10030 characters). Block A states both figures. The `10029` token is the API body count.

Located quote (the anchor the draft cites):

    $ grep -n "Security issues affecting any Google Cloud" corpus/source-snapshots/round-45/S072.txt
    148:   <td>Security issues affecting any Google Cloud product or web service that
    (line 149 continues: `handles reasonably sensitive user data`; the normalized quote is present in both the live body and the pinned file, line 148 in both)

S069 Q5 (the "beyond S069 Q5" comparator), located in the pinned S069 snapshot:

    $ grep -n "reasonably sensitive user data is intended" corpus/source-snapshots/round-44/S069.txt
    10:product or web service that handles reasonably sensitive user data is intended

Frozen counter, scratch trees (base = pure export copied from `/fast/scratch/hyaku/kasegi-r45/L1/pure`, byte-verified equal to `dc5bb8c` for the six touched files via `git show dc5bb8c:<path> | cmp`):

    base (no S072 row, no line)            -> limb R1 fixed=0 read=row-S072=absent
                                              routed-defects total=5 fixed=0 unresolved=5 exit=1
    full draft (block A + S072 fixture row) -> limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
                                              routed-defects total=5 fixed=1 unresolved=4 exit=1
    control c_noA (row only, no line)       -> limb R1 fixed=0 read=lesson-correction-absent
    control c_noRow (line only, no row)     -> limb R1 fixed=0 read=row-S072=absent
    do-nothing (base copy)                  -> limb R1 fixed=0 read=row-S072=absent

The "full" run used a scratch S072 registry row (a fixture, `teaches` = `supersedes S070 — the article API body is readable, 10029 characters; ...`, anchor = sha256 of the pinned file). That row exists only under `$SCRATCH` and is removed. The R1 limb fails on each half alone, so block A is not a marker that passes by itself.

Two facts the registry row must carry, because the counter reads them there and not in the lesson: the token `10029` and the word `readable` in `teaches`, and the snapshot sha256 in the anchor cell (the first failure I hit was `size-token-absent`, fixed in the fixture only).

## 2. Block B — round-45 admission (F27 coverage row and frontier row)

Attacked: `corpus/instruments/r44-frontier-count.py` (the table-aware count the frozen secondary uses), on base and on a scratch README with block B appended.

    base:  $ r44-frontier-count.py --root base --expect 27
           frontier rows=26 admitted=26
           frontier expected=27 admitted=26 verdict=SHORT exit=1
    base:  $ r44-frontier-count.py --root base --expect 26
           frontier rows=26 admitted=26           (rc=0)
    full:  $ r44-frontier-count.py --root full --expect 27
           frontier rows=27 admitted=27           (rc=0)
    control c_noF27row (block B minus the `| F27 |` row, i.e. marker-only):
           $ r44-frontier-count.py --root c_noF27row --expect 27
           frontier rows=26 admitted=26
           frontier expected=27 admitted=26 verdict=SHORT exit=1

The base reproduces the frozen secondary exactly ("base: frontier rows=26 admitted=26 exit 1"). The F27 row is the sole source of the increment; the marker-only control stays red.

The block's shape follows README.md:614-640 (heading; paragraph; `Area | Entry | Source basis` table; `id | topic | status | entry | sources | next` table with status as the third cell; `[r45 amendment, appended 2026-10-28]` count line reading 27/27). The S071 quotes the block relies on, located with the source-recheck instrument:

    $ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071
    S071:sha256 OK
    S071:Q1 OK normalized=markup-whitespace occurrences=1 anchor=310-ok
    S071:Q2 OK normalized=markup-whitespace occurrences=1 anchor=95-ok
    S071:Q3 OK normalized=markup-whitespace occurrences=1 anchor=39-ok
    S071:Q4 OK normalized=markup-whitespace occurrences=1 anchor=41-ok
    S071:Q5 OK normalized=markup-whitespace occurrences=1 anchor=20-ok

Other S071 phrases in block B were read directly: the private list `security@kernel.org` ("This is a private list of security officers", S071:281); the postponement ceiling (S071:308-312); "Binary-only executables are not accepted" (S071:39); "unreproducible ... is not a security bug" (S071:41-43).

## 3. Block C — PROVINCE r45 frontier line

One physical line in the style of the r44 line (`[r45 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F27 — ... admitted round 45; entry `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (source S071)`). No frozen counter parses PROVINCE.md (grep of `corpus/instruments` for "Frontier amendment" finds only the r44 counter's unrelated text). Checked by reading only.

## 4. Block D — SCORECARD `### Round-45` move-log rows

Three rows, all "held", no score move claimed: depth:verifiability 4 (C1 increment is whatever `r45-routed-defects.py` prints at the integration tree); coverage 8 (the F27 frontier increment holds only once the row, entry and S071 registry row land); depth:density 9 (guard). I found no measured reason to move any score, so none is claimed.

## 5. Regression check of the drafts against the round-44 counter

    $ r44-routed-defects.py --root base --baseline base
    routed-defects total=8 fixed=7 unresolved=1 exit=1   (unresolved: R44-D4 status=unresolved detail=the round-44 LOG section does not record the affirmative planner=L1 mapping)
    $ r44-routed-defects.py --root full --baseline base
    routed-defects total=8 fixed=7 unresolved=1 exit=1   (same unresolved limb)

The drafts do not change the round-44 result. The base export itself reads 7/8 on that counter (the D4 limb looks at the round-44 LOG section); I did not investigate why the export reads it that way.

## 6. Coop/lane hygiene

- Read the frozen `claims.json`, `freeze.txt`, `freeze-controls.txt`, `corpus/lessons/round-44-verifier-spotcheck.md` §6, the counter source, `corpus/README.md` (r44 block), `PROVINCE.md` tail, `SCORECARD.md` round-44 rows, `corpus/SOURCES.md` S070 row, and the S071/S072 snapshots.
- Only lane-owned write: the draft directory and this report. Scratch: `/fast/scratch/hyaku/kasegi-r45/R45ScribeCorrections/` (removed at exit). The `/fast/scratch/hyaku/kasegi-r45/L1/pure` export was copied, never edited.
- Lane `git status --porcelain` shows untracked files that are not mine (round-44 `final-attempt3-refiled.txt`, round-45 `wave1.ready*`, `wave1/`). I created none in the lane tree beyond the draft directory and this report.
- Tools: none installed or upgraded.

## Limitations

1. R1 is not closed. The real `corpus/SOURCES.md` S072 row is not in the lane tree and is outside this seat's item; the counter also needs the S070 row unchanged (it is; block A does not touch it). The frozen expect_after `fixed=5` is not reached by this seat.
2. The `10029` figure is re-measured from the live API today (2026-10-28), not from the round-44 capture; the round-44 lesson's count is consistent with it.
3. Block B's F27 row is admitted only by the frontier count. The C2 gate `corpus/instruments/r45-c2-gate.py` on the scratch tree with the draft reads `c2-gate fixed=2/7 exit=1` (G1 `F27-entry-missing`, G2 `F27-entry-missing`, G3 `row-S071=absent-or-malformed`, G5 `F27-entry-missing`, G6 `knowledge=63`). It needs the knowledge entry and the S071 registry row, neither of which this seat drafted. Base reads `c2-gate fixed=1/7 exit=1`, which matches the frozen control.
4. Blocks C and D are not machine-checked by any frozen counter.
5. The scratch S072 row used in the "full" R1 run is a fixture, not a registry entry.
6. The "held" scores in block D are scribe wording, not an L1 measurement.
7. The round-44 counter's D4 limb is unresolved at base and draft alike; I did not dig into it.
