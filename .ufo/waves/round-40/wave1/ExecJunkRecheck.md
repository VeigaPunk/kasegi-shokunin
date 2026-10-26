# ExecJunkRecheck — C2 junk-decision control scored against the frozen kill rule (round 40, wave 1)

Seat `ExecJunkRecheck` (leaf, executor). Item: score the do-nothing control
`.ufo/waves/round-40/c2-controls/junk-decisions.md` against the frozen C2 kill rule in
`.ufo/waves/round-40/claims.json`, i.e. show that a flip-all-without-evidence decision set cannot
reach the target — `mined` among the nine is 0 (< 4) and no Gate-block evidence exists — with the
exact commands and their real output. Deliverable is the command transcript only.

Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `HEAD=5e985b74075dd3813a63d7750966bf8abf693465`
(claims freeze), `git status --porcelain --untracked-files=no` empty at run time. Read-only git only;
no mutating git/jj command, no install, no subagent, no `agent://all` message. Run UTC observed by the
driver: `2026-10-26T21:19:47Z`.

Result: **the junk set is REJECTED on six independent frozen clauses.** `queued` among the nine
drops to 0 (the trivial check is defeated), but `mined` among the nine is **0 < 4** and Gate-block
evidence is **0/9** (no `flip:`, empty evidence column, zero capture manifests, no round-40 lesson
Gate). The adversarial repair — flip all nine to `mined` with the same zero evidence — clears the
≥4 floor and is still rejected (entries citing the nine = 0 ≠ 9; no capture manifest exists to
recheck). Positive controls show the same probes return non-zero on landed evidence, so the zeros
are a measurement of the control, not a dead oracle.

---

## 1. Frozen inputs

| input | identity |
|---|---|
| control `c2-controls/junk-decisions.md` | 20 lines, sha256 `2294131d52b182f0bcf1bdd7002879cce48aad05788167545eba87dd385c0c15` |
| `claims.json` (kill rule + counting commands) | sha256 `33a4602d3669aab178907082421fc72c3f2e938a06d902696ff4cb86cba2953f` |
| frozen `corpus/SOURCES.md` (commit `5e985b7`) | 132 lines, sha256 `f33d10f45142b6d59969cedbfc35a1d29a3ba672d62067da8424fc0d32a728f2` |
| harness instrument | `corpus/instruments/frontier-recheck-count.py` in the same export |

The registry was taken from the freeze commit by `git archive` into the scratch dir (digest checked
twice: the export and `git show 5e985b7:corpus/SOURCES.md` agree), so a sibling seat rewriting the
working-tree registry mid-wave cannot move these numbers.

## 2. Fixture derivation

The control's table gives each of the nine rows a fabricated `rejected` status, a fabricated reason
cell (`no time` ×7, `superseded` ×2) and evidence `none`. The application writes exactly the registry
decision cells — column 8 (`teaches`, where landed rows carry `REJECTED: …; flip: …`) and column 9
(`status`) — and leaves `used-by` untouched, so no capture, entry or quote is introduced:

```
$ awk -F'|' -v OFS='|' 'BEGIN{split("S016 S017 S019 S020 S021 S022 S023 S024 S025",a," "); for(i in a) nine[a[i]]=1} {id=$2; gsub(/[[:space:]]/,"",id); if(id in nine){$8=(id=="S022"||id=="S024")?" superseded ":" no time "; $9=" rejected "} print}' $F/corpus/SOURCES.md > $S/SOURCES.junk.md
exit=0

$ sha256sum $S/SOURCES.junk.md && wc -l < $S/SOURCES.junk.md
ffc4d5ed540d6b35d2f60a527b7e946107a4538fefaff8c51e8440e5fad0f4c7  …/SOURCES.junk.md
132
exit=0
```

`diff -u` over the pair prints exactly nine `-`/`+` row pairs (18 changed lines) plus the two file
headers; every other row of the 132-line registry is identical.

```
S016  status=rejected  teaches=no time      used-by=—
S017  status=rejected  teaches=no time      used-by=—
S019  status=rejected  teaches=no time      used-by=—
S020  status=rejected  teaches=no time      used-by=—
S021  status=rejected  teaches=no time      used-by=—
S022  status=rejected  teaches=superseded   used-by=—
S023  status=rejected  teaches=no time      used-by=—
S024  status=rejected  teaches=superseded   used-by=—
S025  status=rejected  teaches=no time      used-by=—
```

## 3. The frozen counting commands on the junk copy

These are the C2 `counting_commands` verbatim with `corpus/…` resolved against the freeze export and
the registry path replaced by the junk copy (see the transcript header):

| # | frozen probe | required after | observed on junk | verdict |
|---|---|---|---|---|
| C1 | `awk … s=="queued"` among the nine | 0 | **0** | passes the trivial check |
| C2 | `awk … s=="mined"` among the nine | ≥4 | **0** | **FIRED** |
| C3 | `grep -rlE '^source: S0(16\|…)` over `corpus/knowledge` | = mined count (≥4) | **0** | equal-but-vacuous at 0; C2 decides |
| C4 | `grep -cE '^\| S06[0-9] \|'` registry | ≥1 | **0** | **FIRED** |
| C5 | `grep -rlE '^source: S06[0-9]'` knowledge | ≥1 | **0** | **FIRED** |
| C6 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 23 | **22** | **FIRED** |
| C7 | `frontier-recheck-count.py` | entries=26 pass=26 exit=0 | **entries=25 pass=25 exit=0** | **FIRED** |

Raw exits, as produced (`grep -c` exits 1 on zero hits — the expected red signal):

```
$ awk … if(s=="queued") n++ … $S/SOURCES.junk.md     -> 0        exit=0
$ awk … if(s=="mined")  n++ … $S/SOURCES.junk.md     -> 0        exit=0
$ grep -rlE '^source: S0(16|…)' $F/corpus/knowledge | wc -l -> 0 exit=0
$ grep -cE '^\|[[:space:]]*S06[0-9][[:space:]]*\|' $S/SOURCES.junk.md -> 0  exit=1
$ grep -rlE '^source: S06[0-9]' $F/corpus/knowledge | wc -l  -> 0 exit=0
$ grep -cE '^\| F[0-9]+ \|' $F/corpus/README.md              -> 22 exit=0
$ cd $F && python3 corpus/instruments/frontier-recheck-count.py -> entries=25 pass=25 exit=0
```

## 4. Gate-block evidence: absent

```
$ grep -E '^…(S016|…|S025)…' $S/SOURCES.junk.md | grep -c 'flip:'          -> 0   (exit=1)
$ awk -F'|' '… e=$5; if(e!="none") n++' $JUNK                            -> 0
$ awk -F'|' '… print reason' $JUNK | sort | uniq -c
      7 no time
      2 superseded
$ grep -rlE '"id": *"S0(16|…|S025)"' $F/corpus/source-snapshots | wc -l   -> 0
$ test -f $F/corpus/lessons/round-40.md && echo present || echo absent    -> absent
$ grep -c 'flip:' $JUNK                                                   -> 0   (exit=1)
```

So for all nine: a reason exists, a `flip` does not, no capture manifest names the row, and the
round-40 lesson Gate that must record the rejection does not exist at freeze. That is 0/9 on the
`rejected rows need reason+flip` limb and 0 mined rows on the `capture + entry + passing
source-recheck` limb.

## 5. Frozen kill rule evaluated

The evaluator (`eval-c2.py`) prints the frozen C2 `kill_rule` string read from `claims.json`, then
recomputes each clause from the fixture and the freeze export. Its full source is reproduced
verbatim in the deliverable at lines 198–309, so it survives scratch removal.

```
clause-01 nine-rows-still-queued             observed=0            required=0              pass
clause-02 mined-among-nine-at-least-4        observed=0            required=>=4            FIRED
clause-03 decided-row-gate-evidence          observed=0/9          required=9/9            FIRED
clause-04 s060-row-opened-this-round         observed=0            required=>=1            FIRED
clause-05 knowledge-entry-citing-s060        observed=0            required=>=1            FIRED
clause-06 frontier-rows                      observed=22           required=23             FIRED
clause-07 harness-entries26-pass26           observed=entries=25 pass=25 exit=0 required=entries=26 pass=26 FIRED
clause-08 source-recheck-fails-for-a-mined-row  observed=n/a (mined among nine = 0) pass
clause-09 census-exit-or-new-W/E      observed=not-evaluated (fixture is a detached copy; not a census root)
clause-10 junk-twin-accepted                 observed=REJECTED     required=not-accepted pass
fired=6 02 …,03 …,04 …,05 …,06 …,07 …
verdict=REJECTED                                        (exit=1)
```

`clause-08` is vacuously green because a rejected status yields no mined row to recheck; `clause-09`
is not reachable from a detached registry copy (the census validates the fleet/lane root) and is not
needed — the OR already fires on six clauses.

## 6. Adversarial variant — flip all nine to `mined` with the same zero evidence

The cheap repair for clause 2 is a status lie, so the same fixture was re-derived with only column 9
set to `mined` (sha256 `e7c88e034bd491121b4440d10b4d96fe54290c326caa49fe44a28f9bcf55ba16`):

```
$ awk … $9=" mined " … -> $S/SOURCES.junk-mined.md                          exit=0
$ awk … if(s=="mined") n++ … $S/SOURCES.junk-mined.md                       -> 9
$ grep -rlE '^source: S0(16|…)' $F/corpus/knowledge | wc -l                 -> 0
$ grep -rlE '"id": *"S0(16|…)"' $F/corpus/source-snapshots | wc -l          -> 0
```

Evaluated: `clause-02 … pass` (9 ≥ 4), then `clause-03 decided-row-gate-evidence observed=0/9 FIRED`,
`clause-08 … FIRED`, plus clauses 04–07, `verdict=REJECTED` (exit=1). The ≥4 floor cannot be reached
by a status flip alone because the entry-count equality and the capture manifests are separate
oracles.

## 7. Positive controls — the detectors are not constant-zero

```
$ grep -cE 'REJECTED:.*flip:' $F/corpus/SOURCES.md                          -> 6
$ awk … if(s=="rejected") n++ … $F/corpus/SOURCES.md                        -> 6
$ awk … S029 … -> status=mined used-by=corpus/knowledge/cra-manufacturer-reporting-duties.md
$ grep -n '^source: S029' $F/corpus/knowledge/cra-manufacturer-reporting-duties.md
2:source: S029 — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng — …
$ cd $S/recheck && python3 $F/corpus/instruments/source-recheck.py --manifest S057.manifest.json --source S057
S057:sha256 OK
S057:Q1 OK occurrences=1
exit=0
```

All six landed rejected rows carry `flip:` (6/6 vs 0/9 for the junk), a landed mined row binds to its
knowledge entry via `source:`, and the landed S057 capture (sha256 `11c8d6d6…d64f2f`) passes
`source-recheck` on its committed quote. So the zeros in §3–§4 are the control's, not the probes'.

## 8. Deliverable

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-40/wave1/ExecJunkRecheck.txt` | 468 | `3dd84ac66998e57e9c9bd49d118bd12ae77d088c24937500c740e4accf917b8f` |

The file is the transcript only — header identity, sections A–H, every command with its exit status —
and is byte-identical to the scratch original (`cmp` clean). It is not text the L1 lands in the
corpus; it is the retained counter-evidence for the C2 claim's "junk twin accepted" clause.

## 9. Axes

- **coverage (C2, 7 → 8)**: the frozen counter's discrimination is now evidenced, not asserted — the
  do-nothing decision set reds on `mined < 4` and on missing Gate-block evidence, and the
  status-only mined repair reds too. This is the falsifier for the claim's `junk twin accepted` kill
  clause.
- **depth:verifiability**: inputs are pinned by commit and sha256; the counting probes are the frozen
  commands verbatim; the aggregator source ships in the transcript.
- Harm: none — two wave-1 files and scratch only; nothing in the lane corpus, fleet root, siblings or
  source trees was touched.

## 10. Write scope, scratch, tooling

Writes: `.ufo/waves/round-40/wave1/ExecJunkRecheck.txt` (deliverable), this receipt, and
`/fast/scratch/hyaku/kasegi-r40/ExecJunkRecheck/` (freeze export, two fixture registries, evaluator,
driver, recheck manifest, transcript). No lane/fleet/source-tree file was modified; no MANIFEST,
template, script, `.ufo/state/`, watchdog log or sibling repo was touched. Scratch removed with
`rm -rf` after both files were copied and verified; the transcript keeps the only copy of the
evaluator and driver logic that matters. No tool was installed or upgraded (disk guard read before
the run: `/tmp` 3%, `/var/tmp` 35%, `/fast/scratch/hyaku` 26% used). No pacman transaction was run.

## 11. Risks / notes

1. **The aggregator is seat-written.** The decisive values come from §3's frozen commands run
   verbatim; §5 only tabulates them. A reader who distrusts the aggregator reads §3 and §4.
2. **Clauses 4–7 are tree properties.** The junk control is the do-nothing baseline, so it performs
   none of the round's other moves: no S060+ row, no S060+ entry, frontier 22, harness 25/25. The
   decisive clauses for a *decision set* are 2 and 3; 4–7 are reported because the frozen rule is an
   OR over the whole submission.
3. **Census clause not evaluated.** The census validates the lane/fleet root, and the fixture is a
   detached `git archive` copy; running it there would measure nothing about the lane. The rule
   already fires six times without it, so no verdict depends on that omission.
4. **Freeze-state numbers.** Frontier 22 and harness 25/25 are the claims' own before values,
   measured on the freeze export. If a sibling lands F23/S060+ in this wave, the *after* numbers move;
   this control's verdict does not, because the junk set is scored against the frozen target.
5. **`grep -c` exit semantics.** Zero hits print `0` and exit 1 throughout; the transcript labels this
   in its header so the red lines are not misread as command failures.
