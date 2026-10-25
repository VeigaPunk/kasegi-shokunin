# SiblingOverlap — do kasegi F06–F08 duplicate a sibling surface?

Seat: `L1Kasegi23.SiblingOverlap-2` (leaf; no subagent dispatch).
Round: 23 (FALSIFY wave). Axes under attack: `depth:verifiability`, `coverage`.
Target of this seat: sibling corpora only — whether any *admitted* sibling entry covers
(a) multi-party coordination, (b) CVE/CNA assignment rules, (c) EU CRA reporting duties,
and therefore whether kasegi should **cite**, **defer**, or **own** F06–F08.

State note: the corpus moved during this wave. Artifact observations below were first taken
against the tree *before* the post-attack repair (`2712c99`), which re-sourced F07 to CNA
rules 4.2.6 and grew the containment matrix; §3 re-states each affected pin with its current
location. Where a line number and the current tree disagree, the tree at `4d9231e` wins and
neither finding (S-1, S-2) changes.

Read-only. No production file, lane tree, git/jj state, or sibling tree was written,
committed, or mutated. No package was installed (tooling note: nothing installed; no
`pacman`/`uv`/`npm`/`cargo` transaction executed — pacman is paused host-wide anyway).

## 1. Sibling trees — all five present

Command:

```sh
for d in chousa kaidoku kotodama kumitate tabi; do
  p=/home/vgpnk/Projects/shokunin/$d-shokunin
  [ -d "$p" ] && echo "PRESENT $p" || echo "ABSENT  $p"
done
```

Observed: `PRESENT` for all five —
`chousa-shokunin`, `kaidoku-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`,
`tabi-shokunin`.

The assignment's conditional clause ("if a sibling tree is absent, say so") therefore
does not fire. The duplicate/defer question must be answered on content, not on absence.

## 2. Content census — zero sibling coverage of all three F06–F08 surfaces

The zero is not a thin-corpus artefact: the five sibling `knowledge/` trees are large.

```sh
for d in chousa kaidoku kotodama kumitate tabi; do
  echo -n "$d: knowledge files="; find $d-shokunin/corpus/knowledge -name '*.md' | wc -l
done
```

Observed: `chousa 57`, `kaidoku 121`, `kotodama 242`, `kumitate 56`, `tabi 41`
(517 `.md` knowledge entries total).

Topic probes, run over each **whole** `corpus/` tree (knowledge, sources, lessons,
evidence — not only `knowledge/`), counting *files* that contain the phrase:

```sh
for t in 'Cyber Resilience Act' '2024/2847' 'coordinated disclosure' 'multi-party' \
         'multiparty' 'coordinated vulnerability' 'disclosure policy' \
         'single reporting platform' 'actively exploited' 'PSIRT' 'security.txt' '72 hours'; do
  for d in chousa kaidoku kotodama kumitate tabi; do
    echo "$t $d $(grep -rIFli "$t" $d-shokunin/corpus/ | wc -l)"
  done
done
```

Observed: **`0` files for every phrase in every one of the five siblings** — 12 phrases ×
5 lanes = 60 cells, all zero. No sibling names the CRA, its regulation number, ENISA, a
PSIRT, a disclosure policy, `security.txt`, a 72-hour clock, or "multi-party"/"coordinated
vulnerability" anywhere in its corpus.

Filename-level census (independent of prose), also zero topical:

```sh
find {chousa,kaidoku,kotodama,kumitate,tabi}-shokunin/corpus -type f -name '*.md' \
  \( -iname '*vulnerab*' -o -iname '*disclos*' -o -iname '*coord*' -o -iname '*cna*' \
     -o -iname '*cra-*' -o -iname '*cve*' -o -iname '*advis*' -o -iname '*embargo*' \)
```

Observed single hit:
`kaidoku-shokunin/corpus/evidence/round-25/proposal/planner-advisory.md` — head lines
read (`sed -n '1,5p'`) show "kaidokuR25 — actual native planner advisory … the actual
native planner, POST original64 proposal barrier". It is a *planner* advisory, not a
security advisory. Not coverage.

### 2.1 Raw single-token greps are traps — all apparent hits are substring artefacts

A naive `grep -i CNA|CVE|CRA` produces large counts that are 100% noise. Each class was
opened and disambiguated, not assumed:

| Token | Apparent | Actual | Evidence |
|---|---|---|---|
| `CNA` | kaidoku 10, tabi 56, kotodama 3 | **0** genuine | `SecName`/`AssocName` (`kaidoku …/round-33/sources/COFFDumper.cpp:1665,1738`), `fcName` (`tabi …/playwright-core/lib/utilsBundle.js:18744`), `AccName` (`tabi …/playwright-accessible-locators-and-snapshots.md:117`), `McNaughton` (`kotodama …/pantheon-archetypes.md:20`) |
| `CVE` | chousa 14, kaidoku 21, kumitate 5 | **1 identifier** | chousa/kumitate hits are all the substring inside `execve(2)` (e.g. `chousa …/long-span-argv-r34.md:3`, `kumitate …/agent-isolation-substrates.md:114`); the only real ID is `CVE-2025-55305` ×3 in kaidoku |
| `CRA` | chousa 234, kaidoku 10389, kotodama 1580, kumitate 532, tabi 1634 | **0** genuine | substring of `Sacra`, `Accra`, `scra…` — the token is unusable and was replaced by `Cyber Resilience Act` / `2024/2847` (both zero) |
| `ENISA` | tabi 1 (case-insensitive) | **0** genuine | 2 occurrences of the minified identifier `enIsA` in `tabi …/node_modules/playwright/lib/transform/babelBundle.js` |
| `embargo` | kotodama 1, tabi 1 | **0** genuine | anthropological trade embargo (`kotodama …/contact-scenario-builder.md:59`); Chromium enum `ShouldEmbargo` (`tabi …/protocol.d.ts:1073`) |
| `24 hours` | kotodama 2 | **0** genuine | Hellenistic planetary hours / number symbolism (`kotodama …/celestial-symbolism-calendars.md:67`) |

### 2.2 The one real CVE in the fleet is data, not coordination policy

`kaidoku-shokunin/corpus/SOURCES.md:21`:

```
| S015 | OSV CVE-2025-55305 record — https://api.osv.dev/v1/vulns/CVE-2025-55305 | dataset | A |
  The OSV record's affected-version, fix-reference, and fuse-precondition fields for this CVE |
  … Compare advisory prose with extracted ranges and cited fixes when fields diverge; retain the fuse precondition. | mined | …
```

This is an OSV record consumed as a reverse-engineering *precondition* for an Electron
fuse. It states no CNA assignment rule, no assigner scope, and no reporting duty. It is
also (see §3) cited as `S015` in a namespace where kasegi's `S015` is the CWE Top 25
source — the collision, not a topic overlap.

## 3. Non-obvious second-order hazard: `S0NN` is not a fleet-unique join key

This is the connector finding, and it is reproducible entirely from committed bytes.

The frozen fleet contract `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`
defines the ID column as:

> `id` — `S` + 3 or more digits, the next unused; never reused.

It constrains IDs *within one lane's table* and imposes **no cross-lane qualification**.
None of the six `SOURCES.md` headers read (`kasegi`, `chousa`, `kaidoku`, `kumitate`,
`tabi`) declares a namespace for the ID either (heads read with `sed -n '1,18p'`).

Consequence, measured:

```sh
grep -nE '^\| S018 \|' .ufo/waves/kaika-w1/art-curation.md .ufo/waves/kaika-w1/art-learning.md
grep -nE '^\| S0(18|15) \|' kasegi-shokunin/corpus/SOURCES.md kaidoku-shokunin/corpus/SOURCES.md tabi-shokunin/corpus/SOURCES.md
```

`S018` currently denotes **four different documents** across committed artifacts:

| Where | `S018` means |
|---|---|
| `kasegi-shokunin/corpus/SOURCES.md:24` | FIRST, *Guidelines and Practices for Multi-Party Vulnerability Coordination* |
| `.ufo/waves/kaika-w1/art-curation.md:89` | W3C PROV-DM Recommendation |
| `.ufo/waves/kaika-w1/art-learning.md:126` | MemoryBank (arXiv 2305.10250) |
| `tabi-shokunin/corpus/SOURCES.md:32` | *Empirical Study of Web Flaky Tests* |

Two of those four live **inside `.ufo/waves/` — the very tree that will carry round-23's
falsify reports and verdicts**, next to `kasegi`'s own wave artifacts. So a bare `S018`
in a wave-level document does not identify a source.

Why this touches round 23 specifically, and not some other round: the three F06–F08
provenance keys are exactly these bare IDs. `corpus/README.md:200-202` (observed state,
not this seat's finding) binds F06→`S018`, F07→`S030 (supersedes S022)`,
F08→`S029 (supersedes S024)`; the entries carry the same bare IDs in their `source:`
header lines (`corpus/knowledge/multiparty-vulnerability-coordination.md:2` → `S018`;
`…/cna-assignment-and-vulnerability-rules.md:2` → `S030`). *After* the post-attack repair
the same rows sit at `corpus/README.md:203-205` with F07→`S031` (`corpus/SOURCES.md:37`,
"supersedes S030" — CNA rules 4.2.6, approved 2026-10-14, effective 2026-10-20) and the
F07 entry header now opens `source: S031`. The pins moved; the bare-ID join key did not,
so S-2 is unaffected — and the repair adds a *fresh* bare id (`S031`) whose only guarantee
is still lane-locality. The round-23 lesson Gate
records the same bare IDs (`.ufo`-local: `corpus/lessons/round-23.md:198-202`, e.g.
`| S029 | (new row) | — | mined, spec/A, supersedes S024 |`). That Gate block is the
pre-repair record — it still lists S030, not S031 — and the repair is logged later in the
same lesson (`corpus/lessons/round-23.md:252`, `:273`), which is append-only history rather
than a contradiction with `README.md:204`.

Inside kasegi this is sound: the recheck commands resolve lane-locally — each is pinned to
the lane root and a lane-local manifest
(`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018`,
`…/multiparty-vulnerability-coordination.md:4`) — so the bare `S018` there means kasegi's
table and nothing else. The defect appears only when a **wave-level reader** joins `S018` across lanes —
and wave-level readers are precisely what a FALSIFY wave publishes for.

## 4. Findings

**S-1 (falsifiable, negative — answers the assignment).**
Kasegi's F06–F08 do **not** duplicate any sibling surface. No admitted entry, no source
row, and no knowledge file in any of `chousa`, `kaidoku`, `kotodama`, `kumitate`, `tabi`
addresses multi-party coordination, CVE/CNA assignment rules, or EU CRA reporting duties
(§2; 60/60 zero cells over 517 sibling knowledge entries). Therefore:
- **Defer is not available.** There is no sibling owner to defer to. Deferring would
  surrender coverage with no compensating evidence — the C2 denominator would stay at its
  pre-round value while the only lane holding those three sources declines to admit them.
- **Cite is available only for *method*, and is already satisfied.**
  `kasegi-shokunin/corpus/QUALITY.md:8` states: "Source tiers are defined in
  `corpus/SOURCES.md` (contract v1); the research method is chousa's — this file
  duplicates neither." That is exactly contract rule 3's division of labour, already
  recorded. No new method citation is needed, and chousa holds no subject matter to cite.
- **Own is the only correct disposition** for the F06–F08 subject matter.

Falsified if: any one of the 60 probe cells is non-zero on a genuine (non-substring,
non-binary) match; or a sibling `knowledge/*.md` entry is found whose subject is CVD,
CNA/CVE assignment, or CRA duties. Neither was observed.

**S-2 (falsifiable, second-order — the connector finding).**
`S0NN` is a lane-local identifier published into a shared namespace. The four-way `S018`
collision includes two rows inside `.ufo/waves/kaika-w1/`, i.e. the collision is already
live where round-23 verdicts land, and the three F06–F08 provenance keys are the exact
IDs that collide. A wave-level statement such as "F06 rests on S018" is unverifiable
without knowing the lane — a `depth:verifiability` defect that **no in-repo artifact
would catch**, because every in-repo consumer resolves lane-locally and therefore passes.

Falsified if: a fleet-wide rule for qualifying S-IDs exists and was missed; or the
`kasegi`→`S018` binding is already written lane-qualified in every wave-level artifact.
Neither observed. (The only round-23 occurrences of `S018`-class strings outside
`corpus/` were inside `build-spec.json` prompt text quoting this assignment, not
citations — checked, not counted as defects.)

## 5. Proposed move (one, bounded)

**Adopt lane-qualified source IDs in prose, at wave level only: `kasegi:S018`.**
Scope it narrowly so it cannot collide with the contract:

- Applies to **new** wave-level artifacts only — round-23 falsify reports, wave verdicts,
  any fleet-level summary inside `.ufo/waves/`. Not retrofitted into `corpus/SOURCES.md`,
  `corpus/README.md`, or knowledge headers: contract rule 2 makes those **append-only**,
  and rewriting an `id` cell would violate "never reused".
- Applies to **prose citations only**, never to executable strings. Recheck commands keep
  bare `--source S018`: they already pin the lane root
  (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`) and a lane-local manifest, so
  qualifying the id would only break the lookup.
- Encoding is one regex-checkable form, `[a-z]+:S[0-9]{3,}`, so a sentinel can fail closed.

**Axes.** `depth:verifiability`: improves — the join key becomes unambiguous exactly where
the round publishes it, and the improvement is checkable by a one-line grep.
`coverage`: unchanged (adds no surface, claims no admission). No harm to C1, which shares
no bytes with citation prose.

**Why this and not "fix the corpus":** the corpus is already sound internally (§3, last
paragraph). The unsoundness is created only at the boundary where kasegi's lane-local IDs
are read next to kaika's and tabi's. Fixing the boundary is the cheapest move that
removes the defect; fixing the corpus would violate the append-only rule and buy nothing.

## 6. Risks

1. **Scope creep.** A qualification convention can metastasise into a fleet-wide registry
   rewrite. Bound it to prose in new wave artifacts; do not open `SOURCES.md`.
2. **Breaking the rechecks.** If a well-meaning editor qualifies `--source S018`
   inside the recheck command, the manifest lookup fails. The exclusion in §5 is
   load-bearing, not stylistic.
3. **Silent divergence.** If some seats qualify and others do not, the collision persists
   partially and looks fixed. A sentinel must fail closed on unqualified IDs in wave
   prose, not warn.
4. **Not a coverage gain.** This move must not be booked against the C2 denominator. It
   repairs the verifiability of a coverage claim; it does not itself admit anything.
5. **`kasegi`/`kaidoku` are the two lanes that never name the contract file**
   (`grep -rIl 'SOURCES-CONTRACT'` → hits in `chousa`, `kotodama`, `kumitate`, `tabi`;
   none in `kasegi`, `kaidoku`). `kasegi` names only "contract v1" in `QUALITY.md:8`.
   This is a pointer asymmetry, **not** asserted as a defect: the contract lives outside
   the repo at `.ufo/waves/kaika/`, so an in-repo path could not resolve anyway.

## 7. Verification

For S-1 (re-runnable, ~1 s):

```sh
cd /home/vgpnk/Projects/shokunin
for t in 'Cyber Resilience Act' '2024/2847' 'coordinated disclosure' 'multi-party' \
         'multiparty' 'coordinated vulnerability' 'disclosure policy' \
         'single reporting platform' 'actively exploited' 'PSIRT' 'security.txt' '72 hours'; do
  for d in chousa kaidoku kotodama kumitate tabi; do
    n=$(grep -rIFli "$t" $d-shokunin/corpus/ | wc -l); [ "$n" != 0 ] && echo "HIT $t $d $n"
  done
done
# expected: no output
```

For S-2 (re-runnable):

```sh
cd /home/vgpnk/Projects/shokunin
grep -nE '^\| S018 \|' kasegi-shokunin/corpus/SOURCES.md \
  .ufo/waves/kaika-w1/art-curation.md .ufo/waves/kaika-w1/art-learning.md \
  tabi-shokunin/corpus/SOURCES.md | wc -l
# expected: 4 (four distinct documents under one id)
```

For the proposed move, once adopted: every `S[0-9]{3,}` appearing in wave-level prose
matches `^(kasegi|chousa|kaidoku|kotodama|kumitate|tabi):S` , while
`python3 corpus/instruments/source-recheck.py --source S018` in the knowledge headers is
byte-unchanged. This seat did not run the recheck (executor/reviewer scope) and claims no
result for it.

## 8. Scope limits

- This seat did **not** touch C1: `resolve.py`, the containment fixture matrix (13 cases
  when this report was written; **22** at `4d9231e` — 12 expected `GONE`, 4
  `MIRROR-EQUIVALENT`, 4 `RESOLVES`, 2 `INTERNAL`, with the fixed receipt matching 22/22
  and the baseline receipt leaking 13), the baseline/fixed receipts and the copied-CLI
  replay were not read for verdict, mutated, or replayed. No C1 conclusion is stated or
  implied here.
- Quote fidelity, snapshot hashes, manifest completeness, and recheck execution for
  S018/S029/S030/S031 belong to other seats; not assessed, not claimed.
- The F06–F08 `admitted` state is reported as **observed artifact state** with line
  numbers only. This seat asserts nothing about whether the admission is justified, and
  does not claim admission, score movement, or a coverage numerator.
- Sibling `evidence/` trees contain vendored `node_modules`; substring noise from those
  trees is characterised in §2.1 rather than assumed away.
- No sibling `SKILL.md` was read (out of scope for the stated target); the census covers
  `corpus/**` recursively, including `lessons/`.
- No artifact cited here was rebuilt from a transcript, and no `scratch/` tree is cited at all: this lane has no `.ufo/waves/round-35*` tree, and round-23 scratch is not used as evidence. Every citation is a committed in-repo or fleet-ledger path, and the §7 probes were executed against those bytes — so no number in this report can disagree with the hash of a rebuilt surrogate.
- Read-only throughout: the only file written by this seat is this report.
