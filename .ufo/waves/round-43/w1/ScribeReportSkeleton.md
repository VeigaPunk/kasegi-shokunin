# ScribeReportSkeleton — receipt (kasegi round 43, wave w1)

Seat: scribe, leaf (no subagent dispatch, no swarm, no second judge).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write target).
Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; claims freeze
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd`; frozen claims read first and never edited
(`sha256 a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630`, identical to
`freeze.txt`'s `claims-sha256`).

## Deliverable

| Field | Value |
|---|---|
| File | `.ufo/waves/round-43/w1/ScribeReportSkeleton.report.md` |
| Lands at | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kasegi.md` |
| Lines | **453** (`wc -l`) |
| sha256 | `cc14cf5056ba4c64e50dcc2d0254abdbc136edcc238e9315447a9a20e6fc0472` |
| Bytes | 37270 |

Byte-exact: the file holds only landable report text — the eight required sections in order (`Work
performed`, `Landed changes`, `Before → after measurements`, `Sources & frontier`, `Trend verdicts`,
`SHONEN`) plus an `Extras` block carrying the `Stale-lane` line and the tooling-installs line. No
validation tables, no seat notes, no headings that are not report text.

Structure check (ran against the frozen wave spec):

```
$ python3 - <<'PY'   # reads .ufo/waves/round-43/w1-spec.json and the deliverable
spec items 73 missing bullets []
bullets 73 dupes []
roles in bullets ['connector', 'critic', 'executor', 'mutation-tester', 'revenger', 'reviewer', 'scout', 'scribe', 'sentinel', 'simplifier']
```

One bullet per work item: 73 of 73 spec items, no duplicate and no omission. Role mix and attack share
in the header are taken from `.ufo/waves/round-43/w1-REGISTRY.txt` (`seats=73`,
`roles=connector=2, critic=7, executor=23, mutation-tester=5, revenger=2, reviewer=11, scout=9,
scribe=10, sentinel=2, simplifier=2`, `attack_seats=23 (31.5%)`).

## Commands run, with their actual output

Scratch root `S=/fast/scratch/hyaku/kasegi-r43/ScribeReportSkeleton`; all work copies bound there
(`TMPDIR` not relied on). Base export created read-only from the lane:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive ab98fac9 | tar -x -C "$S/base"
exported
```

**1. Base registry / knowledge / suite state (mine, at `$S/base` and via `git show ab98fac9:…`):**

```
$ git show ab98fac9:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
66
$ git show ab98fac9:corpus/SOURCES.md | grep -E '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' \
    | awk -F'|' '{gsub(/ /,"",$5); print $5}' | sort | uniq -c
     61 A
      3 B
      2 C
$ git ls-tree --name-only ab98fac9 corpus/knowledge/ | grep -c '\.md$'
61
$ git cat-file -e ab98fac9:corpus/instruments/r43-closure.sh
fatal: path 'corpus/instruments/r43-closure.sh' does not exist in 'ab98fac9'
exit=128
$ git show ab98fac9:corpus/SOURCES.md | grep -oE '^\|[[:space:]]*S[0-9]{3,}' | tail -3
| S064
| S065
| S066
```

**2. Base counters in the bare export (`$S/base`):**

```
$ python3 corpus/instruments/capture-binding-check.py | tail -3
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=56 with_url=56 with_fetched_utc=18 with_archival=38 snapshot_dirs=18 manifest_dirs=18 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=56 bound=56 unbound=0
exit=0

$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=1/61 cdroot_fail=60 instrument_fail=0 own_fail=0
executes=37 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=61 missing=0 unexpected=0 exit=1
exit=1

$ python3 corpus/instruments/frontier-recheck-count.py | tail -3
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
PASS     F25  knowledge/cve-json-record-format.md                  ids=S064           exit=0
entries=28 pass=28 exit=0
exit=0
```

The `recheck-audit` exit 1 above is an **export artifact**, not the base state: a bare `git archive`
export has no repository root, so the `cd`-prefixed rechecks fail closed (`cdroot_fail=60`). The in-repo
control (`c2-controls/before.txt`, `measured-at=2026-10-28T16:34:15Z`) records
`lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` and
`expect=present expected=61 missing=0 unexpected=0 exit=0`. The report cites the control for
`expected=61` and discloses this limit in the C2 table footnote; the bare-export run is not used as a
base value.

**3. Base census and validation (mine, at the lane):**

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
kasegi	rows	66
kasegi	tier.A	61
kasegi	tier.B	3
kasegi	tier.C	2
kasegi	status.mined	54
kasegi	status.rejected	12
FLEET	rows	66
FLEET	tier.A	61
FLEET	tier.B	3
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	0
FLEET	status.mined	54
FLEET	status.rejected	12
FLEET	status.invalid	0
FLEET	missing	0
census-exit=0

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
validate-exit=0
```

**4. Remaining C2 before values (mine, at `$S/base`):**

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md
25
$ grep -rlE '^source: S067' corpus/knowledge | wc -l
0
$ ls corpus/instruments/claim-package-check.py
ls: cannot access 'corpus/instruments/claim-package-check.py': No such file or directory
$ ls corpus/instruments/fixtures/claim-package
ls: cannot access 'corpus/instruments/fixtures/claim-package': No such file or directory
$ ls corpus/knowledge/*.md | wc -l
61
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
66
```

**5. No-harm limb at base (mine, at `$S/base`):**

```
$ python3 corpus/instruments/density.py SKILL.md | tail -2
| | **mean dens** | | | | | | | | **234.2** |
Total path-citation instances: 782 across 30 blocks.
exit=0

$ python3 corpus/instruments/anchorcheck.py SKILL.md | grep -E 'in-range|LOST-RECORDED|PIN-BROKEN'
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
... (LOST-RECORDED detail lines elided here; full output on request, exit 0)
exit=0

$ sha256sum corpus/instruments/density.py corpus/instruments/r42-closure.sh | cut -c1-20
ee803726a3229eb924a6     (density.py)
fca5ae62379e01232a52     (r42-closure.sh — matches the control's suite-sha256 prefix)
```

**6. Document sizes and freeze-commit contents (mine, at the lane):**

```
$ wc -l SKILL.md corpus/QUALITY.md corpus/README.md PROVINCE.md
1134 / 354 / 600 / 165 lines; sha256 prefixes 9eef84d163173c8e / c4468c9587e09f55 / bb897bf07b3e6e14 / 8deea5ea1c584573
$ grep -c 'r43\|round 43\|round-43' PROVINCE.md
0
$ git show --stat --oneline 4cb6d4ae | head -12
4cb6d4a round-43: frozen claims C1 (r43-closure.sh K1-K19 narrative-evidence) + C2 (claim-package gate capability), controls, freeze record, v2 wave spec and dispatch (73 seats)
 .ufo/waves/round-43/build-w1-spec.py, c1-controls/do-nothing.txt, c2-controls/before.txt,
 census-before.txt, claims.json, freeze.txt, w1-dispatch.json, w1-run.err, w1-spec.json
 9 files changed, 2004 insertions(+)
$ sha256sum .ufo/waves/round-43/c1-controls/do-nothing.txt .ufo/waves/round-43/c2-controls/before.txt \
    .ufo/waves/round-43/freeze.txt .ufo/waves/round-43/claims.json | cut -c1-24
221d20331e7d673f3ce3a377     (do-nothing.txt)
14c58348252713bbd507fbef     (before.txt)
568b42229d8c62bb5754fcc0     (freeze.txt)
a4c03e1e8224549dd864eb7c     (claims.json)
$ git status --porcelain | wc -l
5      (all untracked round-43 wave state; no tracked edit at my read)
```

## Provenance of every value in the deliverable

| Class | Values | Source |
|---|---|---|
| First-hand measurement (this seat) | registry rows 66 and tier histogram 61/3/2; knowledge 61; frontier harness `entries=28 pass=28 exit=0`; capture-binding `records=56 bound=56 unbound=0`; census `rows/tier/status` table and `validate` exit 0 + its three lines; README frontier rows 25; entries citing S067 = 0; gate and fixtures absent; `r43-closure.sh` absent at base; density mean 234.2 / 30 blocks / 782 cites; anchorcheck 16 instances / 0 bad; doc line counts and sha prefixes; PROVINCE r43 count 0 | commands in §1–§6 above |
| Cited committed control | base r42 stand-in `closed=12/13 exit=1` (`run-utc=2026-10-28T16:27:52Z`, `suite-sha256=fca5ae62…`); control `measured-at=2026-10-28T16:32:23Z` / `2026-10-28T16:34:15Z`; the six routed r42 defect locations; in-repo `recheck-audit` `expected=61 exit=0`; `instrument-basenames-matching-claim: 0` | `c1-controls/do-nothing.txt`, `c2-controls/before.txt` |
| Frozen claim text (quoted, not measured) | C1/C2 predicates and after-states; the negative-control rule; "the exact base figure is measured during integration and quoted in the report"; ten C2 counting commands; the S067/knowledge-62/capture-57 targets | `.ufo/waves/round-43/claims.json` |
| Planned landing set, not observed | `Landed changes` rows and their change lists | `.ufo/waves/round-43/INTEGRATION-PLAN.md` landing order; every commit column is `<pending: commit>` |
| Unknown at this seat's read (mid-flight wave) | J, Y, lane tip; every after-state measurement; census after; rows added by tier; rows touched old→new; assimilation verdict; every trend verdict; every seat outcome; wave dead-seat count | written as `<pending: seat>` / `<pending: commit>` exactly where they belong |

## Conflict reported verbatim (for the canonical judge)

The frozen claims contradict themselves on the base C1 figure, and I report both literals rather than
choosing one:

- `claims.json` C1 `predicate`: "*Base ab98fac9 and round-41 judged head 1f7464612ac4c44e39886b82e812610d3c039b13 exports each print closed<19/19 exit=1, and at base every one of K14-K19 is open (each new check must see its own committed defect at base); the exact base figure is measured during integration and quoted in the report, never pre-declared.*"
- `claims.json` C1 `after`: "*base export closed=13/19 exit=1 with exactly K14-K19 open*"

The deliverable therefore does **not** carry `closed=13/19` as a measured value: row 4 of the C1 table
writes `<pending: seat>` with the frozen rule, so the integration run's real output fills it. This is the
reading the predicate commands, and it is also the reading the L1's own `INTEGRATION-PLAN.md` §"Mined
mistake so far" adopts (`M43-1 class stale-premise`: the earlier draft that pre-declared the base figure
was replaced by "at base every one of K14-K19 is open and closed<19/19, leaving the exact base figure to
the measured report"). Not edited: `claims.json` is frozen.

## Known limits

1. **The wave is mid-flight at this read.** `.ufo/waves/round-43/w1/` held only `ExecGateManifest.rules.py`,
   `ExecK19Freeze.sh`, `ExecSourceCapture.{S067.txt,manifest.json,provenance.txt}` and
   `swarm-registry.json`; no `.ufo/waves/round-43/*results*.json`, no `final-gates/all-gates.txt`, and
   `corpus/instruments/r43-closure.sh` / `claim-package-check.py` are not on the tree. Every after-state
   value is therefore `<pending: seat>` — 0 fabricated outputs.
2. **No re-run of seat work.** The report does not rerun the r42 stand-in over the base export; the
   `closed=12/13 exit=1` figure is quoted from the committed control, whose command, suite digest and
   `run-utc` are in the quote.
3. **`recheck-audit` export limitation** (see §2): a bare-export run reports `cdroot_fail=60` because the
   rechecks `cd` to a repository root the export does not have. Only the in-repo control value is used.
4. **`Landed changes` is the integration plan's landing set**, not an observation; every commit column is
   `<pending: commit>` and the freeze row's `4cb6d4ae` is the one hash verified first-hand
   (`git show --stat`).
5. **No `measure 45/45` literal appears** in the deliverable, on purpose: round-42's critics found that
   value asserted and uncommanded (`wave1/RevC2Shape.md:152`), so C2's after-state is reported only
   through the ten named counting commands.

## Coordination

Received one misaddressed IRC message (`W1ScribeLessonGate`) asking the owner of **souji's**
`corpus/SOURCES.md:189` (S242, unescaped `O_NONBLOCK | O_WRONLY` pipe, `E01 fields=12`) to fix it before
landing. Not my file, not my lane: replied that it is a souji round-38 matter and that this seat is
read-only on other lanes. No lane file of kasegi was touched by that exchange.

## Tooling installs

None. No `pacman` transaction (host-wide pause respected), no `uv tool install`, `npx` package or release
binary was installed or upgraded — the seat needed only `git`, `bash`, `python3`, `awk`, `sha256sum` and
the lane's committed instruments.

## Scratch

`S=/fast/scratch/hyaku/kasegi-r43/ScribeReportSkeleton` (holds `base/`, the bare export). Removed with
`rm -rf -- "$S"` after the deliverable and this receipt were written into the wave dir; removal verified
with `test ! -e`. Disk guard checked before the heavy pass: `/fast/scratch/hyaku` 25 % used, 607.3 GB free.

## Writes

1. `.ufo/waves/round-43/w1/ScribeReportSkeleton.report.md` (deliverable).
2. `.ufo/waves/round-43/w1/ScribeReportSkeleton.md` (this receipt).
3. Scratch under `/fast/scratch/hyaku/kasegi-r43/ScribeReportSkeleton` (deleted).

No other lane file, no fleet-root file, no sibling lane, no PATH directory, no mutating git command.
