# CritMotivation — round 36, critic (calibration): do-nothing base control for C1 and C2

Seat: CritMotivation · role: critic · axes: calibration · milestone: round-36
Scope: run every C1 and C2 counter against untouched base exports and decide whether either
claim's after-state is reachable by doing nothing. Read-only; no lane/fleet/shokuknow writes;
no mutating git. Only writes: this receipt + `/fast/scratch/hyaku/kasegi-r36/CritMotivation/`.

Refs measured (all extracted with `git -C {LANE} archive`, never the live worktree):

| tag | ref |
|---|---|
| BASE | `cc692008b0cfd58d18275aa6c4aed79620120799` (round-36 base) |
| R35BASE | `3266c9937b03062d9bbc2f436e20820115ed179c` (round-35 base; claim's negative control) |
| R35HEAD | `0aee0ef105395a2f1d6ace7eaeef13871bb26988` (round-35 judged head) |
| FREEZE | `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims freeze) |

Live state at measurement: lane HEAD = FREEZE, `git status --porcelain` = 9 lines (all
round-36 wave dispatch artifacts, untracked), 47 dirs under `/fast/scratch/hyaku/kasegi-r36`,
`corpus/` byte-identical to BASE (`git diff --name-only BASE -- corpus` = empty). So every
C2 after-counter is still owed at the freeze commit, not merely at the dispatch base.

## 1. Verdict

**Neither claim is reachable by a do-nothing run at BASE.** Both after-states are conjunctions
whose leading limbs are absent at BASE, and every discriminating C2 counter is still at its
before value. Two named C2 counters and five of the nine C1 E-checks are already green at BASE;
those are regression pins, not round-36 closures, and must be attributed that way (see §4).

## 2. C1 — nine predicates at BASE (export-bound forms, measured)

Commands (per export dir `X`; `{LANE}` = lane repo for ancestry/trackedness only):

```
E1  grep -cF 'filled by the L1' X/SCORECARD.md ; grep -cF '<LANE_HASH>' X/SCORECARD.md
    last 40-hex after 'Final lane commit:' -> git cat-file -e ; git merge-base --is-ancestor it <ref>
E2  grep -c '201\.2' X/SCORECARD.md                      (>=1)
E3  grep -cF 'r35-defect-closure.sh' X/SKILL.md ; grep -cF 'r36-closure.sh' X/SKILL.md
E4  git -C {LANE} ls-tree -r --name-only <ref> -- .ufo/waves/round-35/wave1-results.json | wc -l
    ls X/.ufo/waves/round-35/ | grep -c provenance
E5  test -e X/.ufo/waves/round-35/claims-erratum-d5.md
E6  grep -cF 'Correction (round 35)' X/.ufo/waves/round-34/wave1/L1Integration.md
E7  grep -cF 'supersedes R22' X/corpus/QUALITY.md ; grep -cF 'supersedes R23' X/corpus/QUALITY.md
E8  grep -cF 'M36' X/corpus/lessons/round-36.md
E9  git -C {LANE} status --porcelain | wc -l ; find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d | wc -l
```

| check | BASE | R35BASE | R35HEAD | FREEZE | BASE verdict |
|---|---|---|---|---|---|
| E1 tokens=`0`/`0`, last final `c1c6a5f8` exists=1 ancestor=1 | `0`/`0` + `c1c6a5f8` anc=1 | `1`/`0` + `7963976e` anc=1 | same as BASE | same as BASE | **PASS at base** |
| E2 `201.2` count | **6** | 0 | 3 | 6 | **PASS at base** |
| E3 SKILL rows `r35-defect-closure.sh`/`r36-closure.sh` | **0/0** | 0/0 | 0/0 | 0/0 | FAIL at base |
| E4 tracked@ref / provenance-beside | 1 / **0** | 0 / 0 | 0 / 0 | 1 / 0 | FAIL at base (provenance limb) |
| E5 claims-erratum-d5.md | **1** | 0 | 1 | 1 | **PASS at base** |
| E6 `Correction (round 35)` in round-34 L1Integration.md | **1** | 0 | 1 | 1 | **PASS at base** |
| E7 `supersedes R22`/`R23` | **1/1** | 0/0 | 1/1 | 1/1 | **PASS at base** |
| E8 `M36` in corpus/lessons/round-36.md | **missing** | missing | missing | missing | FAIL at base |
| E9 live status lines / scratch dirs | **9 / 47** | 9 / 47 | 9 / 47 | 9 / 47 | FAIL at base (live-bound) |
| **closed** | **5/9** | **0/9** | **4/9** | **5/9** | not 9/9 |

Suite limbs at BASE: `ls corpus/instruments/r36-closure.sh` → `No such file` (`ls_exit=2`);
`--selftest` unavailable. Claim's own "before" column is accurate on every line
(`suite_missing=1`, SKILL rows `0/0`, placeholder greps `0/0`).

Do-nothing check: a seat that changes nothing sits at `closed=5/9` with the suite absent, no
selftest, and E3/E4/E8/E9 red. C1's after-state (9/9 + selftest + registry rows + lesson +
quiescence) is **not reachable at BASE**.

## 3. C2 — counters at BASE

| counter (claim's form) | BASE | after target | base meets it? |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | **18** (F19 row = 0) | 19 | no |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **52** (S053 row = 0) | 53 | no |
| `grep -rlE '^source: S053 ' corpus/knowledge \| wc -l` | **0** | 1 | no |
| `ls corpus/knowledge/*.md \| wc -l` | **47** | 48 | no |
| `python3 corpus/instruments/frontier-recheck-count.py` | **entries=21 pass=21 exit=0** | entries=22 pass=22 | no |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` | **`manifest UNAVAILABLE reason=missing`, exit=2** | exit 0 | no |
| round-36 snapshot dir (`corpus/source-snapshots/round-36`) | **absent** (dirs end at round-35) | present | no |
| junk twin `c2-controls/junk-f19.md` | **absent** — no rejection is demonstrable | rejected w/ receipt | no |
| `python3 corpus/instruments/capture-binding-check.py --root <BASE export>` | **records=42 bound=42 unbound=0, exit=0** | exit 0 | **YES — already green at base** |
| `sources-census.sh validate` (spec form, and `--file <BASE export>/corpus/SOURCES.md`) | **exit 0**, W04 S028/S029 only | exit 0 | **YES — already green at base** |

census was run in the spec form (`--root /home/vgpnk/Projects/shokunin kasegi`) and per-export
(`--file`): exit 0 on BASE, R35BASE, R35HEAD and FREEZE alike.

Do-nothing check: every discriminating C2 counter is at its before value at BASE (frontier 18,
registry 52, S053-citing entries 0, knowledge 47, harness 21/21, source-recheck exit 2, no
round-36 manifest, no junk twin). C2's after-state is **not reachable at BASE**.

## 4. Calibration findings (what makes the base control weaker than it reads)

**(a) Five of nine C1 checks are already green at BASE.** E1, E2, E5, E6, E7 are round-34/35
artifacts that BASE inherits. As closure gates they are legitimate regression pins (the suite
must fail if a past correction is dropped), but only E3, E4, E8 and E9 (filing-time) are
attributable to round-36 work. The round-36 lesson should label E1/E2/E5/E6/E7 as pins so a
`closed=9/9` is not read as nine new closures: `9/9 = 5 pins + 4 round-36 limbs`.

**(b) Two C2 counters are green at BASE, one against its own kill rule.** `capture-binding-check`
exits 0 on the untouched BASE export (records=42 bound=42 unbound=0) while the round-36
capture/manifest is absent — yet C2's kill rule names that instrument for "capture/manifest
absent or unbound". The instrument audits whatever manifests exist, so it cannot fire on the
absence it is cited for; as a counter it adds no discrimination (green at BASE, R35BASE, R35HEAD,
FREEZE). Same shape for census `validate` (exit 0 at all four refs). Keep both as pins, or bind
capture-binding to the export plus an explicit round-36 presence limb.

**(c) E9 is live-bound and therefore makes the claim's two required numbers mutually
unreachable at one wall-clock state.** E9 reads `git -C {LANE} status --porcelain` and
`/fast/scratch/hyaku/kasegi-r36`, neither of which depends on `--export-ref`. The claim requires
(i) head export → `closed=9/9` and (ii) R35BASE export → `closed=0/9`. (i) forces E9 green at
verification time; with E9 green, the R35BASE run returns **1/9** (E1..E8 all measured red at
R35BASE above), not `0/9`. The `0/9` observed today exists only because the lane is dirty
(9 untracked dispatch files) and 47 seat dirs exist — i.e. the negative control is bought by
wave-time pollution, not by the 3266c99 bytes. This is a measurement defect, not a tradeoff:
one of the two counting commands must fail for any fixed live state.

**(d) E4's tracked limb can be built so it never discriminates or never closes.** Measured:
`git -C {LANE} ls-files <path>` = 1 at *both* R35BASE and BASE (live index → green everywhere,
so only the provenance limb discriminates); `git ls-files` run *inside* the export returns 0 at
every ref because a `git archive` export has no `.git`. The round-35 suite exhibits exactly the
second failure mode: `bash corpus/instruments/r35-defect-closure.sh --root <BASE export>` prints
`D4 check=tracked=0,provenance=1 open=1` / `closed=6/7 exit=1` even though the file is tracked at
BASE. Built literally as the ExecC1SuiteBuild spec words it (`git ls-files … = 1`), E4 stays red
at the final head and `closed=9/9` becomes unreachable. The export-bound form is
`git -C {LANE} ls-tree -r --name-only "$REF" -- .ufo/waves/round-35/wave1-results.json | wc -l`
= 1 at BASE/FREEZE, 0 at R35BASE (measured).

**(e) E1's hash extraction must be newline-tolerant.** Both `Final lane commit:` values sit on
the line *after* the label (`SCORECARD.md:987-988` → `7963976e…`; `1129-1130` → `c1c6a5f8…`);
`cat -A` confirms `**Final lane commit:$`. A same-line matcher extracts no hash, and if
"no hash" is judged red then E1 fails at the final head too. Two occurrences also require pinning
"the" line to the last one (both are ancestors at BASE/FREEZE, so the choice does not change any
measured verdict, but it must be stated).

## 5. Impacted axes and smallest safe corrections

- **depth:verifiability (C1)**: fix E9's ref-dependence and E4/E1's measurement form before the
  suite is landed; otherwise the claim's own counting commands are unsatisfiable as a pair.
  Smallest safe correction: in `--export-ref` mode, evaluate E9's export-hygiene limb against the
  export and mark the live-quiescence limbs `skipped=live-limbs open=1` unless the exported ref
  equals the declared final lane head; measure E4's tracked limb with `ls-tree` at `$REF`; match
  E1's hash across the line break and pin "last occurrence".
- **calibration (this seat's axis)**: attribute 5/9 as pins, 4/9 as round-36; move
  capture-binding-check and census-validate from "after counters" to pins (or bind them to the
  export + a round-36 presence assertion). No score change is implied — the claim holds on
  substance.
- **coverage (C2)**: no harm. Every discriminating counter is at its before value at BASE and at
  FREEZE; the only ambiguity is counter attribution, not the admission itself.

## 6. Limits of this review

- One read of each counter; no claim kill judgment (that is CritC2Claim/CritC2Kill's item).
- E1..E9 were evaluated as the spec defines them, in export-bound form; the landed suite does not
  exist yet, so these are predicate measurements, not suite executions. Where the suite's
  implementation would force a different verdict (E4 tracked limb, E1 matcher) that is stated
  explicitly in §4.
- Scratch: `/fast/scratch/hyaku/kasegi-r36/CritMotivation/` (four `git archive` exports, one
  census staging dir, TMPDIR) removed after this receipt was written; no tool installs, so no
  tooling ledger entry.

Report: `.ufo/waves/round-36/wave1/CritMotivation.md`
