# RevJunk — round 40, falsify wave 2

## Item attacked

The frozen C2 junk control `.ufo/waves/round-40/c2-controls/junk-decisions.md` — the flip-all
do-nothing baseline that marks all nine queued rows (S016, S017, S019, S020, S021, S022, S023,
S024, S025) `rejected` with generic reasons and `evidence: none` — scored against the frozen C2
kill rule (`.ufo/waves/round-40/claims.json`) **at the integrated verification state Y**, where
unlike at the claims freeze the round-40 lesson Gate now exists and the real decisions are landed.
Second limb: verify the committed junk twin was **not** accidentally integrated — the lane's real
registry must not contain the junk rows.

Result up front: **junk REJECTED (reproduced)** — it leaves `mined=0` and no Gate evidence, plus
two further mechanical reds the freeze-state run could not show; **integration clean (no defect)**.

## Inputs (pinned)

| input | identity |
|---|---|
| judged head J | `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (matches `final-gates/all-gates.txt` `export-ref=`) |
| verification ref Y | J + the receipt `.ufo/waves/round-40/final-gates/all-gates.txt` only; the receipt is untracked in the working tree at attack time and **no C2 counting command reads it**, so every probe below runs over the `git archive` of J — the committed bytes |
| `claims.json` | sha256 `33a4602d3669aab178907082421fc72c3f2e938a06d902696ff4cb86cba2953f` (read, not edited) |
| `c2-controls/junk-decisions.md` | sha256 `2294131d52b182f0bcf1bdd7002879cce48aad05788167545eba87dd385c0c15` (equals wave-1 `ExecJunkRecheck`'s pin) |
| `corpus/SOURCES.md` at J | sha256 `3089f2a25f2714ccff97fe03ee32812ab64d5a03aa17147592acdf3748b5758e`; the `git archive` export is `cmp`-identical to `git show J:corpus/SOURCES.md` |
| `corpus/lessons/round-40.md` | sha256 `f740c6a015f2b4b418bc19e4040041ade0440bbcb5f07e618af559bac5a9c369` |

Registry column map (census contract, NF=13): $2=id, $3=source, $4=kind, $5=tier, $6=scope,
$7=anchor, **$8=teaches** (where landed rejected rows carry `REJECTED: …; flip: …`), **$9=status**,
$10=opened, $11=recheck, $12=used-by (the entry path for mined rows).

## Fixture derivation

Junk fixture = the control's nine rows applied to a scratch copy of the Y registry, in the same
shape as wave-1 `ExecJunkRecheck` §2 (comparable across waves): teaches cell ← the fabricated
reason (`no time` ×7; `superseded` for S022/S024), status cell ← `rejected`, used-by untouched.

```
awk -F'|' -v OFS='|' 'BEGIN{split("S016 S017 S019 S020 S021 S022 S023 S024 S025",a," ");
  for(i in a) nine[a[i]]=1}
  {id=$2; gsub(/[[:space:]]/,"",id); if(id in nine){
    $8=(id=="S022"||id=="S024")?" superseded ":" no time "; $9=" rejected "} print}'
  corpus/SOURCES.md > SOURCES.junk.md
```

- `SOURCES.junk.md` sha256 `b6ecc7f607fe86e3c2cf2ae5a2ab55d7b658b3679e655367ed31f1c03f177578`,
  132 lines; `diff` against the Y registry = exactly 9 `-`/`+` row pairs (18 changed lines), every
  other row identical. Committed byte-exact as the attack fixture `wave2/RevJunk.SOURCES-junk.md`.
- Strict variant (the control's `evidence: none` read literally: used-by also blanked to `—`),
  sha256 `c2c436708ea9c9fcf0eb588cb841f78a677ce2f52371279ed070ffef2cd2ef8f` — verdict identical
  (§ B), so the verdict does not depend on the fixture-shape choice.

## A. Real state at Y — green re-run (the target is met by the real work)

| frozen probe | required after | observed at Y | verdict |
|---|---|---|---|
| `awk … s=="queued"` among the nine | 0 | **0** | pass |
| `awk … s=="mined"` among the nine | ≥4 | **7** | pass |
| `grep -rlE '^source: S0(16\|…)' corpus/knowledge \| wc -l` | = mined count | **7** | pass |
| `grep -cE '^\| S06[0-9] \|'` registry | ≥1 | **3** (S060/S061/S062) | pass |
| `grep -rlE '^source: S06[0-9]' corpus/knowledge \| wc -l` | ≥1 | **1** (`cyclonedx-analysis-subtree.md`) | pass |
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 23 | **23** (all `admitted` → measure 43/43 = 1.000) | pass |
| `python3 corpus/instruments/frontier-recheck-count.py` | entries=26 pass=26 exit=0 | **entries=26 pass=26 exit=0** (incl. `PASS F23 … ids=S060`) | pass |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0 | **exit 0**, `W04 S028`, `W04 S029`, `ok` (the two standing warnings only) | pass |
| `capture-binding-check.py` (claim predicate) | bound=54 unbound=0 | **records=54 bound=54 unbound=0**, exit 0 | pass |
| registry rows total | 62 | **62** | pass |

## B. Junk state — the flip-all rows do NOT satisfy the target

Counting commands verbatim, registry path → the junk fixture; knowledge/README/lesson/instruments
unchanged from the Y export (the junk mutates decision cells only).

| # | frozen probe | required after | observed on junk | verdict |
|---|---|---|---|---|
| 1 | queued among the nine | 0 | **0** | the trivial check is defeated — this alone would accept |
| 2 | mined among the nine | ≥4 | **0** | **KILL** (floor) |
| 3 | entries citing the nine | = mined count | **7 ≠ 0** | **KILL** (equality) |
| 4 | Gate-evidence grep (see below) | evidence per decided row | **7/9 without** | **KILL** |
| 5 | census over the junk registry | no new W/E code | **new `W02` ×7** | **KILL** (new-code limb; exit stays 0) |
| 6 | `capture-binding-check.py` over the junk copy | exit 0 | **exit 1**, 7× `FAIL rule=rejected-row-anchor`, `records=54 bound=47 unbound=7` | **KILL** (mechanical) |
| 7 | S060+ rows / entries, frontier, harness | 3 / 1 / 23 / 26-26 | 3 / 1 / 23 / `entries=26 pass=26 exit=0` | unchanged — the junk inherits the real tree's other moves; the decision clauses are what kill it |

**Gate-evidence grep** (kill clause: "rejected rows need reason+flip" in the round-40 lesson Gate):

```
grep -c 'no time' corpus/lessons/round-40.md                       -> 0   (exit 1)
grep -cE 'Flip:' corpus/lessons/round-40.md                        -> 4   (S022, S024, S061, S062)
awk '/^### Rejected/{f=1;next} /^###/{f=0} f' round-40.md | ids     -> S022 S024 S059 S061 S062
per-id rejection bullet `^- **<id> …REJECTED`:  S016=0 S017=0 S019=0 S020=0 S021=0 S022=1 S023=0 S024=1 S025=0
```

The seven rows the junk flips from mined carry **no** rejection bullet, no `no time` reason
anywhere in the lesson, and no flip — 7/9 junk decisions are unevidenced. The two `superseded`
junk rows (S022/S024) coincide with the real rejection bullets, so 2/9 junk rows match real
evidence; the kill fires on the seven regardless, and independently on the mined floor (0 < 4)
and the entries equality (7 ≠ 0).

**Census over the junk registry** (`sources-census.sh validate --file <junk registry>`):
`W02 S016/S017/S019/S020/S021/S023/S025 thin reject reason` ×7 + the standing `W04` ×2, exit 0.
W02 = `status=="rejected" && length(teaches)<8` — the census's thin-reason detector fires on every
`no time` row (7 chars) and is a **new W-code** versus the real state (W04 ×2 only), so the census
kill clause's "a new W/E code" limb fires on a junked lane too. The two `superseded` rows (10
chars) pass the length threshold — the census is a partial junk detector (finding E.2).

**Strict variant** (used-by also `—`): queued=0, mined=0, entries=7, binding 7×
`rejected-row-anchor` exit 1, census `W02` ×7 — **REJECTED identically**.

## C. Mutation supplements — the decision-cell space is covered

Two cheap mutants through the same counter, to show the junk verdict is not an artifact of the
flip-all shape:

| mutant | registry change | queued | mined | entries | binding check | verdict |
|---|---|---|---|---|---|---|
| a: partial reject (S016/S017/S019 → rejected) | 3 cells | 0 | **4** (floor passes!) | 7 ≠ 4 **KILL** | exit 1, 3× `rejected-row-anchor`, `bound=51 unbound=3` **KILL** | REJECTED |
| b: mine the rejected (S022/S024 → mined) | 2 cells | 0 | 9 | 7 ≠ 9 **KILL** | **exit 0** (passes!) | REJECTED (equality + Gate: no admission block, no entry cites S022/S024) |

Every registry-only decision lie fires at least one frozen clause: all-reject → floor + equality
+ Gate + census-W02 + binding; partial-reject → equality + binding; mine-the-rejected → equality
(+ mined-evidence limb); re-queue any row → queued ≠ 0. The binding instrument binds records→rows
and does **not** require a mined row to have a record, so mutant b passes it — the
entries==mined-count command is the only mechanical discriminator for that shape (finding E.3).

## D. Integration check — the committed junk twin was NOT integrated

- `grep -c 'no time' corpus/SOURCES.md` → **0**; `grep -rc 'no time' corpus/` over every
  md/txt/py → **0 files**. The junk row shape `| rejected | no time | none |` exists at J **only**
  in `.ufo/waves/round-40/c2-controls/junk-decisions.md` (the control itself; `git grep` over the
  whole tree).
- The nine real rows carry the real decisions, not the junk table: S016/S017/S019/S020/S021/S023/
  S025 `mined` with used-by entries (`anthropic-cvd-provenance-and-pacing.md`,
  `pz-reporting-transparency-trial.md`, `nist-sp800-216-vdp-framework.md`,
  `doj-vdp-framework-scope-and-authorization.md`, `cisa-bod-20-01-vdp-minimums.md`,
  `cisa-cvd-program-stages.md`, `cve-bench-agent-exploitation-benchmark.md`); S022/S024
  `rejected` with reason+flip in the round-40 lesson Gate (superseded by S030 / S029). Real
  statuses 7 mined + 2 rejected vs the junk table's 9 rejected — the twin was not merged.
- Round-40 junk artifacts are confined to `.ufo/waves/round-40/`: `c2-controls/junk-decisions.md`
  plus the wave-1 receipts (`wave1/CritC2Junk.*`, `wave1/ExecJunkRecheck.*`); no `corpus/` path
  carries them, and no knowledge entry or registry row cites the control file.
- The standing round-37 twin `c2-controls/junk-f20.md` (lane root, committed) is referenced only
  by round-37 lesson/spotcheck prose documenting its rejection (`corpus/lessons/round-37.md:33,108`,
  `round-37-verifier-spotcheck.md:135`); no registry row or knowledge entry integrates it.
- The historical `SOURCES*.md` copies under `.ufo/waves/round-*/` are prior rounds' fixtures; the
  lane's live registry is `corpus/SOURCES.md` alone and it matches the J blob byte-for-byte.

**Not integrated; no defect.**

## E. Findings

1. **Low — freeze gap, no verdict impact here.** The C2 kill rule's Gate-evidence clause has no
   frozen counting command (the eight `counting_commands` never grep the lesson). An
   id-presence-only Gate grep is satisfiable by the junk: all nine ids appear in
   `corpus/lessons/round-40.md` 5–7 times each (admission blocks, rejection bullets, status-change
   log). The clause must be implemented as shaped — a rejection bullet carrying reason+flip for
   rejected rows, capture+entry+passing recheck for mined rows — not as id presence. For this junk
   the mined floor (0 < 4) and the entries equality (7 ≠ 0) kill it regardless, so no verdict
   depends on the gap; but a smarter twin that steals real evidence for a different decision needs
   the shaped clause (same family as wave-1 `CritC2Junk` variant C: local integrity checks do not
   authenticate provenance).
2. **Info.** The census W02 threshold is `length(teaches)<8`: it catches the seven `no time` rows
   but not the two `superseded` rows (10 chars). The census is a partial junk detector; the binding
   check and the counting commands are the complete ones.
3. **Info.** `capture-binding-check.py` passes mutant b (a mined row with no manifest record is not
   a binding failure — it binds records→rows, not rows→records). The entries==mined-count command
   is the only mechanical discriminator for mining a rejected row; the Gate mined-evidence limb is
   the judgment backstop.

## Verdict

- **Junk control: REJECTED — reproduced.** At the integrated state Y the flip-all junk leaves
  `mined=0` (< 4) and no Gate evidence for 7/9 of its decisions, and is additionally killed
  mechanically by `capture-binding-check` (7× `rejected-row-anchor`, exit 1) and by the census's
  new `W02` codes — two reds the freeze-state run could not show because the captures, the lesson
  Gate and the real decisions did not exist yet. The frozen counter's discrimination is intact at
  Y.
- **Integration: clean.** The committed junk twin is not in the real registry; the nine rows carry
  the real decisions; all ten C2 probes are green at Y.
- **Defects found in the landed work: none.** Findings E.1–E.3 recorded (one low freeze gap, two
  informational).

## Write scope, scratch, tooling

- Writes: this receipt and the byte-exact attack fixture `wave2/RevJunk.SOURCES-junk.md`
  (sha256 `b6ecc7f6…f177578`, the exact junked registry used in § B). Nothing else in the lane,
  fleet root, sibling repos or source trees was written; `claims.json`, `junk-decisions.md` and
  every lane file were only read.
- Git: read-only (`archive`, `show`, `ls-tree`, `grep`, `rev-parse`, `log`, `status`, `diff
  --name-only`); no mutating git/jj command anywhere; the census runs were read-only `validate`
  mode.
- Scratch `/fast/scratch/hyaku/kasegi-r40/RevJunk/` (Y export, junk + strict + two mutant roots,
  binding/census outputs) is removed before this receipt is filed; `disk-guard.sh status` read at
  start (`/fast/scratch/hyaku` 24% used, 616.0G free).
- Tooling: no installs or upgrades; no pacman (paused host-wide); no campaign tools run in
  `/home/vgpnk/Projects/shokuknow`; no `agent://all` message; no subagents (leaf seat).
