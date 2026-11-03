# ExportReplay — verdict: REPRODUCED (C1 and C2 counters replay byte-identically from clean-clone bytes; no claim kill observed; four reproducibility notes filed, none of which change a claim's pass/fail)

Seat: ExportReplay, kasegi round 57 wave 1. Frozen claims read first from
`.ufo/waves/round-57/claims.json` (freeze commit `6343e2c3882a96b1af86e1ecf4c9deba33361719`); never edited.
Lane `L=/home/vgpnk/Projects/shokunin/kasegi-shokunin`, scratch `S=/fast/scratch/hyaku/kasegi-r57/ExportReplay`
(created with `mkdir -p`, deleted at the end — §13). Every command below is absolute-path; all writes went into `S`
only. Host: Linux x86_64, `python3 3.14.8` (`/usr/bin/python3`), `bash 5.3.20(1)-release`, `git` at its default HEAD.

Headline numbers (clone bytes, exit codes in parentheses):

| command | decisive line | rc |
|---|---|---|
| `frontier-recheck-count.py` | `FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90` + `FRONTIER-PASS F38 ids=S089,S090` + `entries=41 pass=41 exit=0` | 0 |
| `figure-audit.py` | `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` | 0 |
| `figure-audit.py --selftest` | `selftest cases=5 failures=0` | 0 |
| `capture-binding-check.py` | `records=73 bound=73 unbound=0` | 0 |
| `source-recheck.py --source S089` | `S089:sha256 OK` + 7 × `OK occurrences=1` | 0 |
| `source-recheck.py --source S090` | `S090:sha256 OK` + 7 × `OK occurrences=1` | 0 |

Clone-run vs lane-run: **six of six diffs empty, six of six sha256 pairs equal, aggregate sha256 equal**
(`b3ce08dc9b832d20c4b8a5a186ea2b35207b75870d8c7a2ea258842efaec1a69` both sides) — §5.

---

## 1. Clone and HEAD check — the spec's expected HEAD is NOT what the clone holds (reported, then worked around)

```
$ mkdir -p /fast/scratch/hyaku/kasegi-r57/ExportReplay
$ git clone --shared -q /home/vgpnk/Projects/shokunin/kasegi-shokunin <S>/clone ; echo CLONE_OK
CLONE_OK
$ git -C <S>/clone rev-parse HEAD
cd3029876eac7189aaff0d32b26031c0defa35aa
[exit=0]
$ git -C <S>/clone rev-parse --show-toplevel
/fast/scratch/hyaku/kasegi-r57/ExportReplay/clone
$ git -C <S>/clone cat-file -t 6343e2c3882a96b1af86e1ecf4c9deba33361719
commit
$ git -C "$L" rev-list --count 6343e2c3882a96b1af86e1ecf4c9deba33361719..HEAD
1
$ git -C <S>/clone rev-parse cd3029876eac7189aaff0d32b26031c0defa35aa^
6343e2c3882a96b1af86e1ecf4c9deba33361719
```

**Finding (spec vs repo).** The seat spec's step 1 expected `HEAD = 6343e2c…` (the freeze). The clone checks out
`cd3029876eac7189aaff0d32b26031c0defa35aa` — the **round-57 implementation commit**, one commit *after* the freeze, whose
parent *is* `6343e2c…`. The spec's stop-and-report condition therefore fires; I report it here and did **not** stop, because
the assignment's substance (replay the frozen counters over committed base + working-tree files) is satisfiable at *both*
anchors and I ran both (§4 = tip, §9 = freeze pin). No counter number differs between the two anchors (§4, §9).
`L` working tree was 4 entries dirty at start and identical at end (§12): `M LOG.md`, `M SCORECARD.md`,
`?? .ufo/waves/round-57/w1.ready.dispatched`, `?? .ufo/waves/round-57/w1/`.

## 2. The six-file copy is provably a no-op against the tip — the working-tree files *are* the tip bytes

Step 2 as specified (`cp` from L into the clone, same relative paths):

```
$ for f in corpus/SOURCES.md corpus/README.md PROVINCE.md corpus/instruments/figure-audit-ledger.json \
           corpus/instruments/knowledge-expected.txt corpus/knowledge/iso-29147-30111-standard-records.md; do
    cp "$L/$f" "<S>/clone/$f"; done
$ git -C <S>/clone status --porcelain | wc -l
0
```

sha256 pre-cp = post-cp = lane, for all six (first 12 hex):

```
corpus/SOURCES.md                                       pre=5bd6c4a4d3c4 post=5bd6c4a4d3c4 lane=5bd6c4a4d3c4 cp_changed=NO
corpus/README.md                                        pre=a3df57988364 post=a3df57988364 lane=a3df57988364 cp_changed=NO
PROVINCE.md                                             pre=33c96be5d77b post=33c96be5d77b lane=33c96be5d77b cp_changed=NO
corpus/instruments/figure-audit-ledger.json             pre=94d8ac9b48e1 post=94d8ac9b48e1 lane=94d8ac9b48e1 cp_changed=NO
corpus/instruments/knowledge-expected.txt               pre=557d97ec7d82 post=557d97ec7d82 lane=557d97ec7d82 cp_changed=NO
corpus/knowledge/iso-29147-30111-standard-records.md    pre=03ba69465bdb post=03ba69465bdb lane=03ba69465bdb cp_changed=NO
```

Proof by blob id (`git hash-object` of the lane file vs `rev-parse HEAD:<path>` vs the freeze blob):

```
corpus/SOURCES.md                                    tip=da3295079a94 wt=da3295079a94 eq=YES | freeze=b5fceb270cd6 eq=NO
corpus/README.md                                     tip=01ce50f81164 wt=01ce50f81164 eq=YES | freeze=d78ffd4feb20 eq=NO
PROVINCE.md                                          tip=9f601eedaa0e wt=9f601eedaa0e eq=YES | freeze=26825a16fbb5 eq=NO
corpus/instruments/figure-audit-ledger.json          tip=7f83a0becebf wt=7f83a0becebf eq=YES | freeze=aaf7fc5e3018 eq=NO
corpus/instruments/knowledge-expected.txt            tip=e2e7c5fe8cb0 wt=e2e7c5fe8cb0 eq=YES | freeze=f3bae0810c60 eq=NO
corpus/knowledge/iso-29147-30111-standard-records.md tip=bbd2ae69a159 wt=bbd2ae69a159 eq=YES | freeze=<absent>  eq=NO
```

So the "clone of the committed base plus the working-tree implementation files" equals **the tip commit**, for these six
paths. All counters below were run twice: before the `cp` and after it — byte-identical both times (step 3/§3 vs post-cp):

```
c1-frontier rc=0 post_cp_vs_pre_cp=IDENTICAL
c2-figaudit rc=0 post_cp_vs_pre_cp=IDENTICAL
c3-selftest rc=0 post_cp_vs_pre_cp=IDENTICAL
c4-binding  rc=0 post_cp_vs_pre_cp=IDENTICAL
c5-s089     rc=0 post_cp_vs_pre_cp=IDENTICAL
c6-s090     rc=0 post_cp_vs_pre_cp=IDENTICAL
```

## 3. The six counters in the clone — full decisive output

Run from `<S>/clone` (cwd = repo root, which is what every instrument assumes; see §8 note on `--root`):

```
### c1-frontier rc=0
FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90
FRONTIER-PASS F38 ids=S089,S090
...
PASS     F38  knowledge/iso-29147-30111-standard-records.md        ids=S089,S090      exit=0
entries=41 pass=41 exit=0

### c2-figaudit rc=0
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=33 ok
FIG frontier-rows-r56 recorded=37 derived=37 ok
FIG registry-rows-r56 recorded=88 derived=88 ok
FIG entries-r56 recorded=40 derived=40 ok
FIG knowledge-expected-r56 recorded=75 derived=75 ok
FIG knowledge-files-r56 recorded=75 derived=75 ok
FIG census-fresh-literal-r56 recorded=ok derived=ok ok
FIG census-internal-r56-receipt recorded=1130 derived=1130 ok
FIG census-gone-r56-receipt recorded=3915 derived=3915 ok
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0

### c3-selftest rc=0
selftest case=ok-ledger exit=0 want=0 verdict=pass
selftest case=stale-literal exit=1 want=1 verdict=pass
selftest case=derive-fails-fail-closed exit=1 want=1 verdict=pass
selftest case=token-boundary-34-vs-340 exit=1 want=1 verdict=pass
selftest case=unreadable-ledger-exit-2 exit=2 want=2 verdict=pass
selftest cases=5 failures=0

### c4-binding rc=0
AUDIT records=73 with_url=73 with_fetched_utc=35 with_archival=38 snapshot_dirs=33 manifest_dirs=33 \
      missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=73 bound=73 unbound=0

### c5-s089 rc=0
S089:sha256 OK
S089:Q1 OK occurrences=1 anchor=1-ok
S089:Q2 OK occurrences=1 anchor=84-ok
S089:Q3 OK occurrences=1 anchor=91-ok
S089:Q4 OK occurrences=1 anchor=92-ok
S089:Q5 OK occurrences=1 anchor=99-ok
S089:Q6 OK occurrences=1 anchor=64-ok
S089:Q7 OK occurrences=1 anchor=204-ok

### c6-s090 rc=0
S090:sha256 OK
S090:Q1 OK occurrences=1 anchor=1-ok
S090:Q2 OK occurrences=1 anchor=84-ok
S090:Q3 OK occurrences=1 anchor=85-ok
S090:Q4 OK occurrences=1 anchor=92-ok
S090:Q5 OK occurrences=1 anchor=64-ok
S090:Q6 OK occurrences=1 anchor=197-ok
S090:Q7 OK occurrences=1 anchor=109-ok
```

Per-figure completeness checked mechanically, not by eye:

```
FIG lines=35 ok_suffix=35 stale=0
each of the eight new ids appears exactly once in the green receipt:
  frontier-rows-r56 1 | registry-rows-r56 1 | entries-r56 1 | knowledge-expected-r56 1 | knowledge-files-r56 1
  census-fresh-literal-r56 1 | census-internal-r56-receipt 1 | census-gone-r56-receipt 1
Amended round 57 (in the fail-entry-records record cell): 1
Q lines occurrences=1 count S089=7 S090=7
```

Independent recounts straight off the clone bytes, with **no instrument** (rejects the "the counter grades itself"
objection):

```
frontier F rows (README): 38
registry S rows (SOURCES.md): 90
entries via F-row comma split: 41
knowledge files: 76
knowledge-expected lines: 76
sort -c: sorted exit=0
S089 bytes=6647 S090 bytes=5598
17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd  corpus/source-snapshots/round-57/S089.txt
2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a  corpus/source-snapshots/round-57/S090.txt
ledger ids=35 ; base ledger ids=27
ISO lead occurrences=1
23309b6fd1226e398f8cce84f6a6e41f1a35ef9f8f0f95acdaa2119d17055b39  -
```

both shas match the C2 kill rule byte for byte; `grep -c '"id"'` = 35 and the base ledger = 27 match C1's counting
commands. `knowledge-expected.txt` has 78 lines = 2 `#` comments + 76 entries, and the entry list is **exactly set-equal**
to `ls corpus/knowledge/*.md`:

```
$ diff <(ls corpus/knowledge/*.md) <(grep '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt) && echo ...
EXACT SET EQUALITY exit=0
```

## 4. The lane run and the clone/lane diff — the frozen counters do not depend on the lane worktree

Same six commands, read-only, `cd "$L"` (recorded before/after to prove no side effect: §12):

```
### c1-frontier rc=0 ... ### c6-s090 rc=0        # all six rc=0, same decisive lines as §3
$ for t in c1-frontier c2-figaudit c3-selftest c4-binding c5-s089 c6-s090; do
    diff -u out.$t.txt L.$t.txt > diff.$t.txt 2>&1 && echo "DIFF $t: EMPTY (identical bytes)"; done
DIFF c1-frontier: EMPTY (identical bytes)   sha256 clone=0a1c6ceabfb5b736 lane=0a1c6ceabfb5b736
DIFF c2-figaudit: EMPTY (identical bytes)   sha256 clone=ddbc25dee4cd9c57 lane=ddbc25dee4cd9c57
DIFF c3-selftest: EMPTY (identical bytes)   sha256 clone=1667a545972e16af lane=1667a545972e16af
DIFF c4-binding:  EMPTY (identical bytes)   sha256 clone=cdebad72ef157a28 lane=cdebad72ef157a28
DIFF c5-s089:     EMPTY (identical bytes)   sha256 clone=0f6257b6c0136667 lane=0f6257b6c0136667
DIFF c6-s090:     EMPTY (identical bytes)   sha256 clone=e711d171e77fc868 lane=e711d171e77fc868
$ cat out.*.txt | sha256sum ; cat L.*.txt | sha256sum
b3ce08dc9b832d20c4b8a5a186ea2b35207b75870d8c7a2ea258842efaec1a69  -
b3ce08dc9b832d20c4b8a5a186ea2b35207b75870d8c7a2ea258842efaec1a69  -
```

**Diff verdict: empty — expected empty, observed empty.** Full per-file sha256:
`c1 0a1c6ceabfb5b7365cdefeb710882a9e364a76074a6550beb70f5b08cfed99e6`,
`c2 ddbc25dee4cd9c57e073769867fc0cb2e087cad1b805efe1efa12b7527f237aa`,
`c3 1667a545972e16afaf0ec60eec9f19f513afbcf12444698eda677a7a62381d5e`,
`c4 cdebad72ef157a28e3c10f91c4afdb5a571cf4ba8084ac217e707a69f0b9e676`,
`c5 0f6257b6c0136667ccb0beff2e3312b36b3358f2afed6f999c80b3c5de125a8f`,
`c6 e711d171e77fc868111c67fffa33fba23bd44eb5337bf4ca693d1deb02e9d04d` — identical on both sides.

Counter independence from the *dirty* lane files was proved by sentinel injection into the clone (never into L):
appending `SENTINEL-EXPORTREPLAY figure-audit FAIL_entry_records=99 rows=999` to `LOG.md` and a `figure-audit` line to
`SCORECARD.md` left all six outputs byte-identical:

```
$ printf '\nSENTINEL-EXPORTREPLAY figure-audit FAIL_entry_records=99 rows=999\n' >> <S>/clone/LOG.md
$ printf '\nSENTINEL-EXPORTREPLAY figure-audit\n' >> <S>/clone/SCORECARD.md
$ git -C <S>/clone status --porcelain
 M LOG.md
 M SCORECARD.md
c1-frontier rc=0 sentinel_effect=UNCHANGED
c2-figaudit rc=0 sentinel_effect=UNCHANGED
c3-selftest rc=0 sentinel_effect=UNCHANGED
c4-binding  rc=0 sentinel_effect=UNCHANGED
c5-s089     rc=0 sentinel_effect=UNCHANGED
c6-s090     rc=0 sentinel_effect=UNCHANGED
$ git -C <S>/clone checkout -- LOG.md SCORECARD.md ; git -C <S>/clone status --porcelain | wc -l
RESTORED
0
```

(Reason, from the ledger: the only two entries naming those files are rev-pinned —
`figure-audit-mentions-base-scorecard :: git show 32782bd6b564f80454af853b38868603a4140e79:SCORECARD.md | grep -c 'figure-audit'`
and `…-base-log :: git show 32782bd…:LOG.md | awk …`. No instrument reads worktree `LOG.md`/`SCORECARD.md`:
`grep -nE 'LOG\.md|SCORECARD' frontier-recheck-count.py capture-binding-check.py` → no hits.)

## 5. Rev resolution in the clone — the rev-pinned derives resolve

```
$ for r in 6343e2c3… cd302987… 8a5d7538b0caa50300b1eee88442a230d9a433f2 133c575394099abf28ddf1b0125c53aefde3e0fa \
           5108584aab38a1919992c46d0224f6ec1cb59363 32782bd6b564f80454af853b38868603a4140e79 eae1d614… 32782bd; do
    git -C <S>/clone cat-file -e "$r^{commit}" && echo "RESOLVE $r OK type=$(…)"; done
RESOLVE 6343e2c3882a96b1af86e1ecf4c9deba33361719 OK type=commit
RESOLVE cd3029876eac7189aaff0d32b26031c0defa35aa OK type=commit
RESOLVE 8a5d7538b0caa50300b1eee88442a230d9a433f2 OK type=commit
RESOLVE 133c575394099abf28ddf1b0125c53aefde3e0fa OK type=commit
RESOLVE 5108584aab38a1919992c46d0224f6ec1cb59363 OK type=commit
RESOLVE 32782bd6b564f80454af853b38868603a4140e79 OK type=commit
RESOLVE eae1d614542e8d30d77e9f4e8b9dea6a11aad138 OK type=commit
RESOLVE 32782bd OK type=commit  full=32782bd6b564f80454af853b38868603a4140e79
[all rc=0]
$ git -C <S>/clone cat-file -e 8a5d753…  → rc=0 ;  git -C <S>/clone cat-file -e 133c575… → rc=0   # the two named by the spec
$ ( cd <S>/clone && git show 8a5d7538b0caa50300b1eee88442a230d9a433f2:corpus/README.md | grep -cE '^\| F[0-9]+ \|' )
37
$ ( cd <S>/clone && git show 133c575394099abf28ddf1b0125c53aefde3e0fa:corpus/README.md | grep -cE '^\| F[0-9]+ \|' )
36
```

The two short revs the old entries carry (`32782bd`, the r53 base) resolve too, so the r53-era figures re-derive rather
than fail closed. Cross-source agreement of the rev-pinned r56 fold against the r56 receipt's printed literals:

```
git show 8a5d753 README F-rows : 37        r56 receipt: FRONTIER-CENSUS rows=37 admitted=37 closed=7 problem-rows=30 registry=88
git show 8a5d753 SOURCES rows  : 88        r56 receipt entries line: entries=40 pass=7 exit=1
git show 8a5d753 entries split : 40
git show 133c575 README F-rows : 36        r55 receipt: FRONTIER-CENSUS rows=36 admitted=36 closed=6 problem-rows=30 registry=87
```

`8a5d7538b0caa50300b1eee88442a230d9a433f2` and `133c575394099abf28ddf1b0125c53aefde3e0fa` therefore resolve in the
clone **and** their derives print the pinned values (37, 36).

## 6. Red controls and the do-nothing control, replayed on clone bytes

Red controls built by mutating *copies* of the ledger inside `S` (the lane ledger was never touched):

```
$ python3 - <<'EOF'   # red1: registry-rows-r56 want 88 -> 87
…
$ cd <S>/clone && python3 corpus/instruments/figure-audit.py --ledger <S>/ctl/red1-wrong-want-r57.json
FIG registry-rows-r56 recorded=88 derived=88 want=87 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
[rc=1]   stale lines=1, and the only stale line is registry-rows-r56

$ python3 - <<'EOF'   # red2: fail-entry-records derive reverted to the pre-repair live counter
   f["derive"]="python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'"
$ cd <S>/clone && python3 corpus/instruments/figure-audit.py --ledger <S>/ctl/red2-deriverepair-r57.json
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=UNAVAILABLE reason=derive-exit-1 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
[rc=1]   stale lines=1, and the only stale line is fail-entry-records
```

Red 2 is the direct measurement of the C1 derive repair: the **old** derive is red on this host (`grep -c '^FAIL'` over
the live counter = 0 lines → `derive-exit-1`, fail-closed), the **new** derive is green (`derived=33`). The r53 receipt
the repair reads is committed and bytes-stable across base/freeze/tip:

```
$ git show <rev>:\.ufo/waves/round-53/controls/c2-counter-final-r53.txt | sha256sum   # for eae1d614, 6343e2c3, HEAD
be69ece74fcd5498…  (identical for all three)
$ sed -n '1,10p' .ufo/waves/round-53/controls/c2-counter-final-r53.txt
 3  FRONTIER-CENSUS rows=34 admitted=34 closed=4 problem-rows=30 registry=85
 8  FAIL_entry_records=33 not_recheck-exit-1=0 FRONTIER-FAIL_row_records=30 not_missing-pass-line=0
$ grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2
33
[rc=0]
```

Do-nothing control at the true base — run in a **detached worktree of the clone** (`git -C <S>/clone worktree add
--detach <S>/wt-base eae1d614…`; toplevel asserted = that dir), because the audit needs a git repo (§8, note N3):

```
$ ( cd <S>/wt-base && python3 corpus/instruments/figure-audit.py )
FIG fail-entry-records recorded=33 (…) derived=UNAVAILABLE reason=derive-exit-1 stale
FIG census-fresh-literal-r55 recorded=stale (the receipt's printed limb; the filed prose ok superseded) derived=stale ok
FIGURE-AUDIT figures=27 ok=26 stale=1 exit=1
[rc=1]
```

That is **exactly** the frozen `before`: `figures=27 ok=26 stale=1 exit=1`, with the single stale entry being
`fail-entry-records` — i.e. the repair target is the *only* red at base, and it is green at tip (§3). The eight new ids
are absent at base (0 each), 35 − 27 = 8, added-set == declared-set, nothing removed:

```
base 27 tip 35
added: ['frontier-rows-r56','registry-rows-r56','entries-r56','knowledge-expected-r56','knowledge-files-r56',
        'census-fresh-literal-r56','census-internal-r56-receipt','census-gone-r56-receipt']
removed: []
```

Each of the five `*-r56` rows carries the pinned rev `8a5d753…`, each derive's first command is in the instrument's
read-only allow-list, and each of the eight has its own `FIG …` line in the green receipt (§3).

## 7. C2's frozen "before" and "after" at the byte level

```
# base eae1d61 (detached worktree, no working-tree overlay)
base knowledge files=75 expected=75 F_rows=37 registry_rows=88
base F38 rows=0 S089 rows=0 S090 rows=0
base round-57 snapshot dir present=NO
$ ( cd <S>/wt-base && python3 corpus/instruments/frontier-recheck-count.py )
FRONTIER-CENSUS rows=37 admitted=37 closed=37 problem-rows=0 registry=88
entries=40 pass=40 exit=0
[rc=0]   FAIL lines=0
$ ( cd <S>/wt-base && python3 corpus/instruments/capture-binding-check.py )
AUDIT records=71 … orphans=1 orphan=S040-live.txt
records=71 bound=71 unbound=0
[rc=0]
```

(the pre-existing `orphans=1 orphan=S040-live.txt` is identical at base 71/71 and tip 73/73, so it is not round-57 drift)

Freeze→tip is pure insertion for every pre-existing record file, and the ISO lead line's bytes never move:

```
$ git -C <S>/clone diff --numstat 6343e2c… cd30298… -- corpus/README.md corpus/SOURCES.md PROVINCE.md \
      corpus/instruments/knowledge-expected.txt corpus/instruments/figure-audit-ledger.json \
      corpus/knowledge/iso-29147-30111-standard-records.md
2	0	PROVINCE.md
40	0	corpus/README.md
6	0	corpus/SOURCES.md
68	7	corpus/instruments/figure-audit-ledger.json
1	0	corpus/instruments/knowledge-expected.txt
105	0	corpus/knowledge/iso-29147-30111-standard-records.md
$ git diff 6343e2c… cd30298… -- corpus/README.md corpus/SOURCES.md PROVINCE.md corpus/instruments/knowledge-expected.txt \
      | grep -c '^-[^-]'
0
$ for r in eae1d614 6343e2c3 HEAD worktree; do grep 'ISO/IEC 29147 vulnerability-disclosure' … | sha256sum; done
23309b6fd1226e398f8cce84f6a6e41f1a35ef9f8f0f95acdaa2119d17055b39   # all four identical
```

The 7 deleted lines in the ledger are the `fail-entry-records` record block being replaced (the amendment); the diff
shows the old 7-line object removed and the amended one re-added, so the entry count still nets +8, and
`grep -c 'Amended round 57' corpus/instruments/figure-audit-ledger.json` = 1.

Captures are byte-identical at freeze and tip (so the C2 evidence does not depend on a later edit):

```
  S089.txt       freeze=17ee9c4191ca2261 tip=17ee9c4191ca2261 SAME
  S090.txt       freeze=2074d3a1b89fe858 tip=2074d3a1b89fe858 SAME
  manifest.json  freeze=cb6b5044ecf38909 tip=cb6b5044ecf38909 SAME
```

Path pointers (clone, tip): `corpus/README.md:938` (`| F38 |`), `corpus/SOURCES.md:96` and `:97` (S089/S090 rows),
`corpus/SOURCES.md:140` (ISO lead line; `:137` at base `eae1d61` — the round-56 carry-in nit, confirmed: 137 → 140 after
the 3-line insert), `corpus/instruments/knowledge-expected.txt:41`,
`corpus/knowledge/iso-29147-30111-standard-records.md` (new file, 105 lines),
`corpus/instruments/figure-audit-ledger.json:210` (`fail-entry-records`), `:217` (`frontier-rows-r56`), 35 `"id"` lines.

## 8. Instrument behaviour found while replaying (reported, not repaired — read-only seat)

**N3 — the green C1 audit is git-repo-bound.** 22 of 35 figures derive through `git show`/`git ls-tree`. A gitless export
of the *same tip bytes* (`git archive HEAD | tar -x` into a directory with no `.git`) prints red:

```
$ git -C <S>/clone archive HEAD | tar -x -C <S>/export ; test ! -e <S>/export/.git && echo ".git absent (as intended)"
.git absent (as intended)
$ ( cd <S>/export && python3 corpus/instruments/figure-audit.py )
FIGURE-AUDIT figures=35 ok=13 stale=22 exit=1        [rc=1]
   stale: frontier-rows, registry-rows, knowledge-expected-entries, knowledge-files, capture-lines-s085,
          capture-bytes-s085, frontier-rows-r54, registry-rows-r54, entries-r54, knowledge-expected-r54,
          knowledge-files-r54, figure-audit-mentions-base-scorecard, frontier-rows-r55, registry-rows-r55,
          entries-r55, knowledge-expected-r55, knowledge-files-r55, frontier-rows-r56, registry-rows-r56,
          entries-r56, knowledge-expected-r56, knowledge-files-r56      (22)
```

The other four counters are git-free and reproduce identically in the same gitless export
(`c1-frontier SAME_AS_REPO_RUN`, `c3-selftest SAME`, `c4-binding SAME`, `c5/c6 SAME`). Consequence for "reproducible
bytes": C1's green needs a *clone with the eight revs*, not just the files — which is exactly what this seat ran.

**N4 — `--shared` clones borrow L's object store.** `<S>/clone/.git/objects/info/alternates` lists
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.git/objects`, i.e. a `--shared` clone is *not* self-contained and would
fail on rev-pinned derives if L were pruned. Verified the counters do not depend on L's state by re-running everything in
a self-contained clone and under an object-store ceiling:

```
$ git clone --no-hardlinks -q "$L" <S>/clone-solid ; cat <S>/clone-solid/.git/objects/info/alternates
NONE
$ git -C <S>/clone-solid count-objects -v
count: 2774 size: 20964 in-pack: 9864 packs: 3 …
$ ( cd <S>/clone-solid && env GIT_ALTERNATE_OBJECT_DIRECTORIES= GIT_CEILING_DIRECTORIES=<S>/.. \
      python3 corpus/instruments/figure-audit.py )
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0        [rc=0]
$ cmp -s <S>/solid-ceiling-audit.txt <S>/out.c2-figaudit.txt && echo "IDENTICAL to shared-clone green receipt"
IDENTICAL to shared-clone green receipt
all six solid-clone runs: rc=0 IDENTICAL_TO_SHARED_CLONE
all five revs resolve in the solid clone: 8a5d753, 133c575, 5108584, 32782bd, eae1d61 → OK
```

**N2 — `--root` does not relocate the ledger.** `figure-audit.py:189-190` sets `ledger = corpus/instruments/…` and
`root = "."` independently, and `:196` only replaces `root`; the ledger path stays **cwd-relative**
(`:62` `subprocess.run([bash,"-c",cmd], cwd=root …)` confirms derives do use `root`). Observed consequences:

```
$ ( cd <S>/clone && python3 corpus/instruments/figure-audit.py --root <S>/freeze )
FIGURE-AUDIT: UNAVAILABLE reason=ledger-missing path=corpus/instruments/figure-audit-ledger.json   [rc=2]   # first attempt, cwd≠that tree
$ ( cd <S>/clone && python3 corpus/instruments/figure-audit.py --ledger <abs>/freeze/…ledger.json --root <S>/freeze )
FIGURE-AUDIT figures=27 ok=9 stale=18 exit=1       [rc=1]   # gitless export → the 22 rev-pinned derives fail
$ ( cd <S>/freeze && python3 corpus/instruments/figure-audit.py )   # same tree, gitless
FIGURE-AUDIT figures=27 ok=9 stale=18 exit=1       [rc=1]
$ ( cd <S>/wt-freeze && python3 corpus/instruments/figure-audit.py )  # same rev, git-backed worktree
FIGURE-AUDIT figures=27 ok=26 stale=1 exit=1       [rc=1]  ← the frozen before, exactly
```

So `--root <other tree>` silently grades the *cwd* ledger against the other tree (a cross-tree audit that "looks like 35"
while reading someone else's ledger). None of the claims' counting commands uses `--root`, so no claim is affected; named
here as an instrument hazard for the parent. The correct replay form is `cd <tree> && python3 corpus/instruments/…`.

**N5 — the claims' "before" is not reachable in this seat's own configuration.** Copying the six working-tree files onto
the claims' `base` (`eae1d61` + six files, no round-57 captures) yields rows=38/registry=90/entries=41 with one problem
row, because the working-tree `README.md`/`SOURCES.md` already carry the round-57 additions:

```
$ ( cd <S>/wt-base6 && python3 corpus/instruments/frontier-recheck-count.py )
FRONTIER-CENSUS rows=38 admitted=38 closed=37 problem-rows=1 registry=90
FRONTIER-FAIL F38 status=admitted ids=S089,S090 problems=missing-pass-line
FAIL     F38  knowledge/iso-29147-30111-standard-records.md  ids=S089,S090  exit=-  problems=manifest-unreadable
entries=41 pass=40 exit=1                                   [rc=1]
$ ( cd <S>/wt-base6 && python3 corpus/instruments/source-recheck.py … --source S089 )
manifest UNAVAILABLE reason=missing                          [rc=2]
```

This is arithmetic, not drift: the "before" is a property of the pure base rev, which I reproduced separately (§6, §7)
and which matches the frozen text exactly. Anyone replaying the seat spec verbatim should expect this shape at base+6.

**N6 — `capture-binding-check` is red on the freeze commit alone.** At `6343e2c` (captures committed, SOURCES rows not):

```
$ ( cd <S>/wt-freeze && python3 corpus/instruments/capture-binding-check.py )
FAIL rule=no-row record=S089 dir=round-57
FAIL rule=no-row record=S090 dir=round-57
records=73 bound=71 unbound=2                                 [rc=1]
```

71→73 with `bound=73 unbound=0` (the C2 kill-rule figure) requires the working-tree `SOURCES.md`; green is reached at
tip and at `freeze + the six files` (§9). Again arithmetic, not a defect — but a grader replaying "the committed base"
alone would see a red binding counter and must not read it as a C2 kill.

## 9. The spec's literal anchor: freeze commit + the six working-tree files

`git worktree add --detach <S>/wt-pin 6343e2c…`, then the six `cp`s (6 modified/untracked paths, as expected):

```
$ git -C <S>/wt-pin rev-parse HEAD
6343e2c3882a96b1af86e1ecf4c9deba33361719
pin+6 status lines: 6
c1-frontier rc=0 IDENTICAL_TO_TIP_RUN
    FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90
    entries=41 pass=41 exit=0
c2-figaudit rc=0 IDENTICAL_TO_TIP_RUN
    FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
c3-selftest rc=0 IDENTICAL_TO_TIP_RUN
    selftest cases=5 failures=0
c4-binding  rc=0 IDENTICAL_TO_TIP_RUN
    records=73 bound=73 unbound=0
c5-s089 rc=0 IDENTICAL_TO_TIP_RUN
c6-s090 rc=0 IDENTICAL_TO_TIP_RUN
```

Freeze **without** the overlay, for the record — the derive repair still resolves there, and the r56 fold is still green:

```
$ ( cd <S>/wt-freeze && python3 corpus/instruments/figure-audit.py )
FIGURE-AUDIT figures=27 ok=26 stale=1 exit=1                  # the frozen before
$ ( cd <S>/wt-freeze && python3 corpus/instruments/frontier-recheck-count.py )
FRONTIER-CENSUS rows=37 admitted=37 closed=37 problem-rows=0 registry=88
entries=40 pass=40 exit=0
[rc=0]   FAIL lines=0
```

The `FAIL lines=0` at both base and freeze is the measurement behind the C1 "host transition" sentence: on this host the
old derive can never return 33, so the receipt-reading derive is the only host-portable form. Confirmed independently in
§6 (red2).

## 10. Determinism and environment independence

```
$ env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/bin:/bin HOME=<S>/home TMPDIR=<S> LC_ALL=C TZ=UTC bash -c "<cmd>"
c1-frontier rc=0 isolated_env=IDENTICAL
c2-figaudit rc=0 isolated_env=IDENTICAL
c3-selftest rc=0 isolated_env=IDENTICAL
c4-binding  rc=0 isolated_env=IDENTICAL
$ a=$(python3 corpus/instruments/figure-audit.py | sha256sum); b=$(python3 corpus/instruments/figure-audit.py | sha256sum)
DETERMINISTIC ddbc25dee4cd9c57e073769867fc0cb2e087cad1b805efe1efa12b7527f237aa
$ python3 -c 'import sys;print(sys.version.split()[0], sys.executable)' ; bash --version | head -1
3.14.8 /usr/bin/python3
GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)
```

No locale, clock, HOME or `TMPDIR` dependence; the receipts are byte-reproducible run to run.

## 11. Tooling

No tool installed, upgraded or removed. `pacman` never invoked. Nothing written to `~/.local/bin` or any PATH directory.
Recording this only because the operator directive asks every seat to report it: **no tools, no versions, no channels,
no reasons — nothing was needed** (`python3 3.14.8`, `bash 5.3.20`, `git` already satisfied every command).

## 12. Lane read-only attestation

Before the lane run and after it, the lane's `git status --porcelain` and its `__pycache__` listing were captured and
diffed:

```
$ diff <S>/lstatus.before.txt <S>/lstatus.after.txt && echo LSTATUS_UNCHANGED
LSTATUS_UNCHANGED
$ cat <S>/lstatus.after.txt
 M LOG.md
 M SCORECARD.md
?? .ufo/waves/round-57/w1.ready.dispatched
?? .ufo/waves/round-57/w1/
$ diff <S>/pycache.before.txt <S>/pycache.after.txt && echo PYCACHE_UNCHANGED
PYCACHE_UNCHANGED            # 15 files, same mtimes; PYTHONDONTWRITEBYTECODE=1 on the lane run
$ git -C "$L" rev-parse HEAD
cd3029876eac7189aaff0d32b26031c0defa35aa
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -c ExportReplay
0
```

No `git add/commit/stash/checkout/switch/reset/pull/push`, no `jj`, no mutation of any kind against `L`; every mutating
git operation (clone, worktree add, `checkout --`, `archive`) was confined to `S`, and the fixture toplevel was asserted
(`git -C <S>/clone rev-parse --show-toplevel` → the clone dir) before use. `L`'s four dirty entries are identical before
and after: they were there when I arrived and I added nothing. Evidence file written: `.ufo/waves/round-57/w1/ExportReplay.md`
(this file) — the only path I created under `L`.

## 13. Leftovers — none

```
$ find <S> -maxdepth 1 -mindepth 1 | wc -l ; du -sh <S>
74   (11 dirs: base clone clone-solid ctl export freeze gitless-out home … ; 63 files)
1.7G
$ rm -rf -- <S> ; echo "rm rc=$?" ; $([ -e <S> ] && echo STILL_PRESENT || echo GONE)
rm rc=0
GONE
$ ls -1 /fast/scratch/hyaku/kasegi-r57/
EntryClaimTable L1 Revenge403 ScoutHostBound
```

`/fast/scratch/hyaku/kasegi-r57/ExportReplay` no longer exists; nothing of mine remains in scratch, in `L`, or in the
fleet root. Kept: only this evidence file.

## 14. Verdict and residual risk

**Reproduced.** Both claims' after-states replay from clean-clone committed bytes, byte-identically to the lane worktree,
with the frozen red/do-nothing controls behaving as declared (`figures=27 ok=26 stale=1 exit=1` at base with
`fail-entry-records` as the sole stale entry; red1/red2 each exactly one stale line on exactly the named entry, exit 1).
No kill rule fired. Depth artifact delivered: a second, independent, self-contained reproduction path for every C1 and C2
number, including the derive repair measured in both directions (old derive red `derive-exit-1`, new derive green `33`).

Residual risk, in order of weight — all reported, none repaired (read-only seat):

1. **The spec's HEAD expectation is wrong** (clone HEAD `cd30298`, not the freeze `6343e2c`). Both anchors replay
   identically, so no claim rests on the ambiguity, but the spec text should be corrected for the next seat.
2. **C1's green is repo-bound** (N3): 22/35 figures need a git checkout carrying eight revs; a file-only export of the same
   bytes prints `ok=13 stale=22`. The claim's phrasing "reproducible bytes" is satisfied by a clone, not by a tarball.
3. **`figure-audit --root` grades the cwd ledger** (N2): a cross-tree invocation silently mixes ledgers and can print a
   plausible-but-wrong `figures=35`. Not used by any claim command; flagged for the instrument's owner.
4. **`capture-binding-check` is red at the freeze commit alone** (N6), green only with the working-tree `SOURCES.md`
   (73/73). A grader replaying the bare committed base would see `bound=71 unbound=2`; that is the round-57 row
   insertion, not drift.

Blockers: none. Nothing was left unfinished, and nothing outside this seat's scope was touched.
