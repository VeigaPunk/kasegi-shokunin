# ScoutOwnSource — scoped source curation for the r66 C1 cat-SIGPIPE gate claim

Seat: **ScoutOwnSource** (leaf, read-only reconnaissance; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base for this seat: `b6db9e818d322726e39cb441f2179d34d4170275`
(round-65 tip). L1 has since committed `1957407e` ("round-66: record cat masking baseline and predata handoff"),
which this seat read but did not write.
Round evidence: `.ufo/waves/round-66`. Seat evidence: `.ufo/waves/round-66/w1/ScoutOwnSource/`.
Scratch (deleted on exit): `/fast/scratch/hyaku/kasegi-r66/ScoutOwnSource`.

**No admission authority is claimed here.** The S099 row below is a *proposal* for the L1 (KasegiR66), the sole
production integrator. Nothing in `corpus/` was edited by this seat; no tool was installed; no pacman transaction
ran; no git/jj mutation occurred anywhere outside my own scratch; no fleet file was touched.

---

## 1. Verdict in one paragraph

The own-work source for C1 is **the lane's own production gate**, `corpus/instruments/figure-audit.py`, and the
round-65 critic's H1 receipt is the *external-to-the-gate* evidence that the gate's SIGPIPE exemption masks a
later operand's error. Both are quoteable at ≤25 words with exact locations (12/12 verified verbatim, §3). The
proposed registry row is **S099**, `kind=own-work`, `tier=A`, scoped to *local gate semantics only*, with
`used-by corpus/lessons/round-66.md`. S099 is the **next unused id** in the lane registry (98 rows, ids
S001–S098 contiguous, no duplicates, one pre-existing file-order swap of S057/S056) — but **S099 is already
occupied in the staged merge package** (§5), so the L1 must resolve that before appending. The row shape is
census-valid: NF=13, `kind` inside the allowed enum, `tier=A`, `status=mined`, `opened=2026-11-04`,
`recheck=on-release` (a symbolic cadence), and `used-by` pointing at a file that **must exist on disk**
(`corpus/lessons/round-66.md`) or the census raises E11. **Assimilation: none** — neither the merge package nor
the latest considerthese carries any theme that fits C1 (§7).

---

## 2. Source opening dates, quotes and hashes (all measured)

### 2.1 The own-work source at BASE

| item | value |
|---|---|
| path | `corpus/instruments/figure-audit.py` |
| revision read | `b6db9e818d322726e39cb441f2179d34d4170275` (`git show <rev>:…`) |
| sha256 at BASE | `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef` |
| sha256 in the working tree at `1957407e` | `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef` (identical) |
| opened | 2026-11-04 (this seat's own opening, per the S096/S097 precedent of a personally-opened own-work row) |

The base blob and the current working tree are byte-identical, so the mechanism quoted below is the mechanism
that runs today — no "at BASE only" caveat is needed for these quotes.

### 2.2 The round-65 critic H1 receipt

| item | value |
|---|---|
| path | `.ufo/waves/round-65/w1/CriticC1/receipts/q2-missing-input-contrast.txt` |
| sha256 | `c52abed7347eda3a6c7a0aa4841e7cf1ae0308e8d0f1255a9969fd24adcd29b2` |
| path | `.ufo/waves/round-65/w1/CriticC1/receipts/q2-sigpipe-masks-error-native.txt` |
| sha256 | `e2d3d784196df0879e23d4b41b5b3645f40aa4982008c83b9ec015bb7c873292` |
| path | `.ufo/waves/round-65/w1/CriticC1.md` (the H1 narrative) |
| sha256 | `bd9e4a0bd4ecfaff05db28459528bde12455445c7f6985949080735c8e0e64ee` |

### 2.3 The L1's durable r66 baseline

| item | value |
|---|---|
| path | `.ufo/waves/round-66/controls/red-before-mechanism.txt` |
| sha256 | `c67ef2cd05789d3c1075f264a13b7e1e80129bcf328afb1395e5db5503af89f2` |
| committed in | `1957407e` (read-only by this seat) |

---

## 3. The two required quotes (≤25 words each, verbatim at the stated location)

Machine-verified by `receipts/05-quote-verification.txt`: **12 cases, 0 failures** — every quote is present
verbatim at its location and every quote is ≤25 whitespace words.

### 3.1 From the own-work source `corpus/instruments/figure-audit.py` @ `b6db9e81` — the SIGPIPE exemption

> **Q1** — L87-L88 (docstring of `upstream_stale`), 17 words:
> "SIGPIPE on a non-final stage is benign by documented rule: a later stage closed the pipe early"

> **Q2** — L91 (the operative line), 4 words:
> "return status != -signal.SIGPIPE"

> **Q3** — L45-L46 (module docstring), 18 words:
> "SIGPIPE (-13) on a non-final stage is benign by documented rule: a later stage closed the pipe early"

Q2 is the load-bearing code: `upstream_stale(head, status)` returns `False` for status `-13` on **any** non-final
stage, which is exactly the clause C1 proposes to narrow.

### 3.2 From the round-65 critic H1 receipt — the masked second operand

> **Q4** — `.ufo/waves/round-65/w1/CriticC1.md` L125-L126, 8 words:
> "a SIGPIPE-truncated producer hides a later operand's error"

> **Q5** — same file L300-L301 (the critic's one-line amendment, the wording C1's predicate descends from),
> 17 words:
> "SIGPIPE (-13) on a non-final stage is benign only when that stage has a single input operand"

> **Q6** — `q2-missing-input-contrast.txt` L10, 4 words:
> "PROBE id=miss-head-base exit=0 reason=-"

> **Q7** — same file L11, 6 words:
> "AUDIT FIG miss-head-base recorded=line000001 derived=line000001 ok"

> **Q8** — same file L3, 4 words (the *same* missing operand under a different consumer — the contrast that
> makes H1 a masking hole rather than a difference of opinion):
> "PROBE id=miss-wc-base exit=1 reason=derive-upstream-exit-1"

> **Q9** — `q2-sigpipe-masks-error-native.txt` L1, 6 words:
> "NATIVE stage=0 cmd='cat big.txt missing.txt' rc=-13"

### 3.3 From the L1's durable r66 baseline (`1957407e`)

> **Q10** — `red-before-mechanism.txt` L6, 5 words:
> "FIG mask-2 recorded=alpha derived=alpha ok"

> **Q11** — same file L7, 5 words (the single-operand control that must stay green):
> "FIG ctrl-single recorded=alpha derived=alpha ok"

> **Q12** — same file L4, 2 words:
> "native_statuses=141 0"

---

## 4. What the seat measured myself (independent of the r65 receipts)

The seat re-ran the **base blob** (`86becbde…`, the working tree's current bytes) against a scratch fixture
with a 200 000-line / 2 200 000-byte `big.txt` and an absent `missing.txt`. Full receipts:
`receipts-base-probe.txt`, `receipts-native-rc.txt`, `receipts-pipestatus.txt`.

| derive | base gate verdict | native stage-0 rc | stderr |
|---|---|---|---|
| `cat big.txt missing.txt \| head -n 1` | **`ok` (exit 0) — false green** | `-13` (141) | 0 bytes |
| `cat missing.txt \| wc -l` | `stale` `derive-upstream-exit-1` (exit 1) | 1 | 44 bytes (`cat: missing.txt: No such file or directory`) |
| `cat big.txt \| head -n 1` | `ok` (exit 0) — must stay green | `-13` (141) | 0 bytes |

So the masked operand is *never diagnosed*: `cat` is killed by SIGPIPE **before** it opens `missing.txt`, so it
writes no diagnostic and the two forms are indistinguishable at the process level. This confirms r65's H1 on
current bytes, and it confirms the L1's committed baseline (`Q10`/`Q11`/`Q12`).

### 4.1 Scope boundary — which heads actually mask

The claim is scoped to `cat`. That scope is **narrower than "any multi-operand producer"**, and the seat measured
why (`receipts-scope-boundary.txt`):

| derive | base verdict |
|---|---|
| `sort big.txt missing.txt \| head -n 1` | `stale` `derive-upstream-exit-2` (sort fails on the missing file before it can be truncated) |
| `head -n 1 big.txt missing.txt` | `stale` `derive-exit-1` (final-stage exit, not upstream) |
| `cat big.txt missing.txt \| head -n 1` | **`ok` — the only masking head** |

`sort` fails fast on the missing operand; `head` as a final stage reports its own exit. Only `cat` — which
streams its first operand until the pipe closes and only then reaches the second — can be killed before it
diagnoses. The L1's "other heads unchanged" wording is therefore **empirically safe**, not merely conservative.

### 4.2 The exemption is *not* observable as a "one operand" rule at the base — three shapes a predicate must decide

The claim says "stdin-only or exactly ONE decoded operand". The seat measured the shapes that the wording has to
separate (`receipts-operand-forms.txt`, `receipts-native-forms.txt`, `receipts-flag-form-corrected.txt`,
`receipts-redirect-plus-operand.txt`):

| derive | decoded operands | native stage-0 | base verdict |
|---|---|---|---|
| `cat big.txt \| head -n 1` | 1 (`big.txt`) | `-13` | `ok` — **must stay green** |
| `cat < big.txt \| head -n 1` | 0 operands, stdin redirect | `-13` | `ok` — **must stay green** (the "stdin-only" branch) |
| `cat big.txt missing.txt \| head -n 1` | 2 | `-13` | **`ok` — must become stale** |
| `cat -n big.txt \| head -n 1` | 1 operand + 1 flag (`-n`) | `-13` | `ok` (want-sensitive; correct want → `ok`) |
| `cat -n big.txt missing.txt \| head -n 1` | 2 operands + 1 flag | `-13` | **`ok` — masks too** |
| `cat < big.txt missing.txt \| head -n 1` | stdin redirect **+ 1 operand** | 1 (not `-13`) | `stale` `derive-upstream-exit-1` — already stale, no exemption involved |

Three consequences the L1 should carry into the freeze, all measured, none assumed:

1. **A flag is not an operand.** `cat -n big.txt` has one operand and one flag; counting argv tokens instead of
   operands would wrongly refuse it. `cat -n big.txt missing.txt` masks exactly like the bare form, so the
   operand count must exclude flags.
2. **stdin-redirect + one operand is two real inputs.** `cat < big.txt missing.txt` reads stdin *and* opens
   `missing.txt`. It happens to be already stale at base (exit 1, not SIGPIPE), so it is not a masking case — but a
   predicate that treats "stdin-only" as "no operands" must be written so that redirect-plus-operand is not
   mistaken for the stdin-only branch.
3. **The stdin-only branch is reachable through the redirect syntax** the parser already supports
   (`< file` is limited to the first pipeline stage), so "stdin-only" is not a hypothetical branch.

### 4.3 Implementation surface — where the operand count is and is not visible

`receipts/04-implementation-surface.txt` shows the exact lines:

- `upstream_stale(head, status)` — **L83** — takes only the head name and the status. It receives
  `argv[0]` (via `heads.append(argv[0])`, **L115**) and `p.returncode` (**L130**). **The decoded operand list is
  not visible to it today.**
- The full decoded `argv` is in scope in the stage loop (**L105**) and the stdin-redirect `input_path` at
  **L107/L109**; both are still live at the upstream-check site (**L129-L130**).

So the operand count must be **threaded into** the upstream-stale decision (or the head list widened from
`argv[0]` to the decoded argv). This is a statement about the *available* implementation surface, not a
proposal to edit production — the L1 owns that.

### 4.4 The reason label: a naming decision, not a mechanism decision

The claim names reason `derive-upstream-signal-13`. The base code already emits `derive-upstream-signal-%d`
(**L133**) for an upstream stage killed by signal N — i.e. `-13` would print `derive-upstream-signal-13`. The
critic's r65 amendment proposed the more specific `derive-upstream-signal-13-multi-input`
(`CriticC1.md` L300-L302). Both are reachable; the distinction matters only for the r65 `P4b`-style
"same label, different meaning" trap the critic already named once. **This is the L1's call**; the seat records
that `derive-upstream-signal-13` requires no new label machinery, while `-multi-input` distinguishes the
multi-operand case from an ordinary upstream signal.

---

## 5. Registry census — before, next id, and the collision the L1 must resolve

### 5.1 Histogram BEFORE (read-only census on the lane, `receipts/03-registry-histogram.txt`)

```
kasegi  rows 98   tier.A 88  tier.B 5  tier.C 5   status.mined 80  status.rejected 18  status.queued 0
validate: 6 pre-existing W04 cross-scope URL warnings (S028/S029/S072/S076/S080/S085), lane ok, exit 0
```

### 5.2 Next id

- Lane registry: **98 rows, ids S001–S098**, the *set* is exactly contiguous 1–98, **no duplicates**.
- File order has one pre-existing swap (S057 printed before S056 at `corpus/SOURCES.md:62-63`) — cosmetic,
  pre-existing, **not** this round's business; do not reorder rows to fix it.
- **Next unused id in the lane registry = `S099`.**

### 5.3 The collision the L1 must resolve before appending

**`S099` is already taken in the staged merge package** (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`
L75): a tier-B `spec` row for the CNNVD grading specification, `kind=spec`, id `S099`.

- Staged package ids: **94**, range **S031–S124**.
- Overlap with the lane registry: **68** (all of S031–S098).
- **Staged ids absent from the lane registry: 26 — exactly S099–S124.**
- r65 recorded the same state: `id-collision-check.txt` → `reg=98 staged=94 collisions=68`, and the r65 lesson
  states "every staged id S031–S098 is already adopted" (with S122/S123/S124 named as the unadopted tail).
- The lane's practice for this collision class is on record: the r65 lesson's **"Assimilation: none"** — the
  package's remaining surface is doctrine/duplicate of held rows and was **not** adopted; and r24's
  `ConnSibling.md` records the alternative (declare `S100–S199` an adopted-block band and reserve `S032–S099`
  for the unadopted package rows) as a proposal that was **not** taken — the lane registry stayed contiguous.

**Consequence for the L1 (a decision, not a finding I may make):** `S099` is the correct *next id* by the lane's
own "the next unused; never reused" rule (`CORPUS.md:89`) **and** it is the id the merge package already claims
for a different subject. Two coherent paths:

1. **Take `S099`** (recommended on the lane's own numbering practice and on r65's precedent of leaving the
   package unadopted) and record in the lesson that the staged package's `S099` (CNNVD grading spec) was
   **never adopted** and is superseded by the new own-work id. This is exactly the r65 "Assimilation: none"
   posture, and the CNNVD row is a *different subject* (a third-party spec archive) from an own-work lane gate —
   the two do not compete for the same ground.
2. **Take `S125`** (the first id clear of the staged band) to keep the package's numbering intact for a future
   adoption. This breaks the lane's contiguous-S-numbering practice for one row and departs from S096/S097/S098.

**What I verified for path 1:** the census does **not** flag it. `sources-census.sh validate` on a scratch tree
carrying the candidate `S099` row returns `ok` with only the six pre-existing W04s — the census checks id
uniqueness *within the registry* (E03), not against the staged package. The collision is a **semantic**
collision the census cannot see, which is why it needs the L1's explicit decision, not a tool's.

### 5.4 The proposed row, verbatim

```markdown
| S099 | Kasegi cat-SIGPIPE operand-count diagnostic — corpus/instruments/figure-audit.py | own-work | A | This lane's local figure-audit rule for a non-final producer killed by SIGPIPE: the exemption is scoped to a single decoded operand; not external security policy, not general error detection, not a sandbox | corpus/instruments/figure-audit.py at b6db9e818d322726e39cb441f2179d34d4170275 L83-L91 upstream_stale; measured baseline .ufo/waves/round-66/controls/red-before-mechanism.txt; opened 2026-11-04 | A pipe-truncated producer can mask a later operand's error; scope the SIGPIPE exemption to the producer's decoded operand count. | mined | 2026-11-04 | on-release | corpus/lessons/round-66.md |
```

### 5.5 Census row schema, verified against the instrument

`sources-census.sh` implements **SOURCES-CONTRACT-v1**: one registry table, **11 columns ⇒ NF=13**, and the
parser accepts 0–3 leading ASCII spaces before a row.

| cell | contract | candidate | status |
|---|---|---|---|
| id | `^S[0-9]{3,}$`, unique in registry (E02/E03) | `S099` | ok |
| source | canonical URL **or a repo path for `own-work`** (`CORPUS.md:90`) | `Kasegi cat-SIGPIPE operand-count diagnostic — corpus/instruments/figure-audit.py` | ok (own-work path, no URL) |
| kind | `spec·docs·paper·code·tool·dataset·talk·book·community·own-work` (E05) | `own-work` | ok — in the enum |
| tier | `A·B·C` (E06) | `A` | ok — and `A` is right because the scope is the lane's *own re-runnable gate output* (`CORPUS.md` tier-A wording) |
| scope | the bound the row is authoritative for | local gate semantics only, with three explicit exclusions | ok |
| anchor | exact location + hash + date | `b6db9e81…` L83-L91 + the r66 measured receipt + opened 2026-11-04 | ok — mirrors S096/S097's anchor shape (revision + lines + sha256 + receipt) |
| teaches | the durable lesson | the masking hazard + the scoped remedy | ok |
| status | `queued·mined·rejected` (E07) | `mined` | ok |
| opened | ISO date, not in the future (E08) | `2026-11-04` | ok — today |
| recheck | ISO date, `Nd`, or a symbolic cadence (E09) | `on-release` | ok — the same symbolic cadence S096/S097 use, and `on-release` is exactly right for a byte-pinned own-work instrument |
| used-by | path that **must exist on disk** for a `mined` row (E11) | `corpus/lessons/round-66.md` | **conditional** — see below |

**The one hard ordering constraint.** `usedby_findings` in `sources-census.sh` (L538-L572) checks only `status ==
mined` rows and raises **E11** when the `used-by` path does not exist under the lane root. Measured both ways on
a scratch tree: with `corpus/lessons/round-66.md` present → `ok`; without it →
`E11 S099 missing used-by corpus/lessons/round-66.md`. **The lesson file must be committed in the same change
as the registry row** (or earlier), or the census turns red. The r65 precedent is the same shape
(`corpus/lessons/round-63.md` / `round-64.md` exist on disk for S096/S097).

### 5.6 Downstream instruments, checked against the candidate row

| instrument | result on a scratch tree carrying S099 |
|---|---|
| `sources-census.sh validate` | `ok`, exit 0, only the six pre-existing W04s (`receipts/05` tree) |
| `sources-census.sh census` | projected **after**: `rows 99, tier.A 89, tier.B 5, tier.C 5, mined 81, rejected 18` |
| `frontier-recheck-count.py` | `entries=47 pass=47 exit=0` — unchanged; S099 is not a frontier row (like S096/S097, it carries no `F##` frontier entry, and `frontier-recheck-count.py`'s registry limb only fires for ids a frontier row names) |
| `capture-binding-check.py` | `records=79 bound=79 unbound=0 exit=0` — unchanged; S099 has **no manifest record**, exactly like the other own-work rows (the manifest holds only URL-bearing captures) |

Note for the L1: `capture-binding-check.py`'s rule B4/B5 ("the row's source cell must carry exactly one
`https://` token") applies to **manifest records**, not to every registry row — an `own-work` row with a repo path
and no manifest record is the established shape (S096, S097) and passes.

---

## 6. Round-65 spot-check carry-in relevant to this seat

Read: `corpus/lessons/round-65-verifier-spotcheck.md` (the r65 non-author closure).

- **Census-shape precedent, verbatim from the spot-check:** "Registry row: `awk -F'|'` on S098 → NF=13 (11
  columns), kind docs, tier A, status mined, opened 2026-11-04, recheck 180d, `used-by
  corpus/knowledge/first-psirt-services-framework.md` resolves." → the candidate row uses the same 11-column
  shape with `recheck=on-release` (correct for an own-work instrument; `180d` would be wrong for a byte-pinned
  local gate).
- **The r65 r66 handoff is explicit.** The spot-check's C1 section records the landed gate, its 63-case selftest
  and the 8/3 → 8/0 measurement; the r65 *lesson* M65-7 is the row that carries the H1 forward: "an exemption
  can mask an unrelated error … the SIGPIPE exemption makes `cat big.txt missing.txt | head -n 1` read green
  while `cat missing.txt | wc -l` reads stale … R88: an exemption's masking path is probed and named in the
  claim's residuals; the r66 plan carries the single-operand restriction." `corpus/QUALITY.md:493` (R88) is the
  standing criterion C1 is being measured against.
- **The r65 residual that r66 must not silently drop.** The r65 lesson's "Residuals and open" states "SIGPIPE on
  a non-final stage stays benign by documented rule and is pinned by its own selftest case" — that sentence is
  **now partly false** and its selftest case (`upstream-sigpipe-nonfinal-benign`, base
  `corpus/instruments/figure-audit.py` L475) encodes the *old* rule. If C1 narrows the exemption, that
  selftest case and the r65 residual text must move with it, or the instrument will carry a selftest that
  asserts the superseded rule. This is the L1's integration work; the seat flags it because it is a *source
  claim* dependency, not a coding preference.
- **`SKILL.md:1224`** carries the same rule in the gate registry table ("except SIGPIPE (-13) on a non-final
  stage, which is benign by documented rule"), and `SKILL.md:1238` is the r65 correction block. Both are
  production text the L1 owns; both will need the r66 amendment.
- **Routed defects from the r65 spot-check** (LOG-bolt citation, two unlisted commits, "final tip" labelling,
  missing exit codes in base receipts, helper-count phrasing) are **integration/hygiene** items, not source-capture
  items; none blocks this seat's curation work. The r65 census state (`W04 ×6`, exit 0) is reproduced exactly by
  this seat's own census run (§5.1).

---

## 7. Merge package and considerthese — **Assimilation: none**

### 7.1 `merge/kasegi/MERGE-REPORT.md` (read-only; not written)

- Path `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md`, sha256
  `0e6759b47595f1bce5fbf49bf0422838ff89a394b2f424d17fb17d96a09106df`; `MERGE-REPORT.json` sha256
  `8a42a9109c8c95bc55e818f0ad97e7923cbfe5a9e7792c72c59b5aaa3aecbf5b`; `SOURCES.append.md` sha256
  `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`. **Read only; nothing written.**
- Package shape: 94 accepted rows, 0 refused, 67 proposed knowledge entries, ids S031–S124.
- **Theme screen against C1: `grep -c -i 'figure-audit|sigpipe|pipefail|derive gate'` = 0 in both
  `MERGE-REPORT.md` and `SOURCES.append.md`.** The package is 58 `docs` / 21 `spec` / 13 `own-work` / 1 `paper` /
  1 `dataset`, all of it Chinese/Japanese vulnerability-disclosure doctrine and platform probe logs.
- **Verdict: Assimilation: none.** No package row bears on the C1 gate semantics; nothing here is adopted, and
  the package's remaining surface is doctrine/duplicate of held rows (the r65 finding, unchanged).

### 7.2 Latest `considerthese` (lane-owned, read-only)

- Latest file: `considerthese/2026-10-26.md` (sha256 `a1a719fe4c96831a34acf1ae398036c547f7acfc81a501ce7a0903133d62442b`);
  the lane's series runs 2026-10-19 → 2026-10-26.
- **Theme screen against C1: `grep -c -i 'sigpipe|figure-audit|derive gate|masking'` = 0.** Its seven proposals
  are about distance-to-next-score, an end-to-end domain task, a quiescence gate, capping wave evidence, the owed
  F18 amendment, cadence, and a proposal-status ledger — **none fits C1**.
- The one proposal with any adjacency is #3 ("Add a quiescence gate before `complete`"), and it is *not* about the
  C1 gate: it concerns `git status --porcelain` cleanliness before signalling done. Its substance is already
  partially present in the lane's closure scripts (`corpus/instruments/r36-closure.sh`, `r37-closure.sh`,
  `r41-closure.sh`, `r46-landing-gate.py` all grep for `git status --porcelain`). **Not a C1 theme.**
- **Verdict: Assimilation: none.** Consistent with r65's reading ("proposal 2 remains domain-task-open;
  proposals 1 and 3 stay landed").

### 7.3 The private curation staging area (read-only, informational)

`/home/vgpnk/Projects/considerthese-curation/notes/kasegi/` holds three draft notes (severity-vs-priority,
disclosure-doctrine lineage, triage-economy report anatomy). A grep for `sigpipe|pipefail|figure-audit|derive
gate` across them and `reviews/kasegi-review.md` returns **0 hits**. That directory is explicitly "not
authoritative fleet state" and its notes are adoption-ready drafts for the lane's own gate — **not this round's
business and not adopted here**.

---

## 8. What this seat did NOT do

- No edit to `corpus/SOURCES.md`, `corpus/instruments/figure-audit.py`, `SKILL.md`, `PROVINCE.md`, `LOG.md`,
  `SCORECARD.md`, `corpus/lessons/*`, or any other production file.
- No commit, no push, no branch, no `jj` operation, no index mutation. `git status --porcelain` in the lane
  shows only the orchestrator's own untracked wave artefacts.
- No tool installed; **no pacman transaction** (all pacman transactions are paused by the operator's directive).
  Every command used `python3` (stdlib only), `git`, `awk`, `sed`, `grep`, `sha256sum`, `sort`, `comm` — all
  already present. Nothing was downloaded; no network access was made by this seat.
- No subagent dispatched (leaf member).
- No admission claim: S099 is a **proposal** for the L1.
- *(Self-disclosed, disclosed in full: during the census-schema probe I ran `touch` against
  `corpus/lessons/round-66.md` in the lane while constructing the scratch tree. It created a 0-byte untracked
  file in the lane. I removed it in the same breath — `rm -f corpus/lessons/round-66.md`, verified absent, and
  `git status --porcelain` back to the orchestrator's untracked wave artefacts only. The lane's committed state
  is untouched. The lesson file is the L1's to create.)*

---

## 9. Open questions for the L1 (decisions, not findings)

1. **Id: take `S099` (next-unused by the lane rule, but the merge package claims S099 for CNNVD grading) or
   `S125` (clear of the package band)?** The seat's recommendation is `S099` with the package's S099 recorded as
   never-adopted/superseded, matching r65's "Assimilation: none" — but this is the L1's call and it must be
   written into the lesson either way.
2. **Reason label: `derive-upstream-signal-13` (no new machinery; reachable via the existing
   `derive-upstream-signal-%d` at L133) or `derive-upstream-signal-13-multi-input` (distinguishes the multi-operand
   case from an ordinary upstream signal)?**
3. **Does the r65 selftest case `upstream-sigpipe-nonfinal-benign` and the r65 residual sentence "SIGPIPE on a
   non-final stage stays benign by documented rule" move with C1, and does `SKILL.md:1224` get an r66 amendment
   block?** The seat's recommendation is yes to all three — they are the source-claim's own text, and leaving them
   would make the instrument carry a selftest asserting the superseded rule.
4. **Commit ordering:** `corpus/lessons/round-66.md` must exist on disk in the same change as the S099 row, or
   the census raises E11 (§5.5).

---

## 10. Seat artefacts

Under `.ufo/waves/round-66/w1/ScoutOwnSource/`:

| file | what it holds |
|---|---|
| `receipts/01-base-and-l1-receipt.txt` | base blob extraction, sha256 of base and working-tree instrument, sha256 of the L1's r66 receipt, lane log |
| `receipts/02-quote-provenance.txt` | the exact base lines L83-L92 and the exact r65 receipt lines, with line numbers; sha256 of the three r65 files |
| `receipts/03-registry-histogram.txt` | census `census` + `validate` on the lane (before), id contiguity / next-id / staged-band computation |
| `receipts/04-implementation-surface.txt` | base lines L83-L92, L103-L116, L126-L135 — where the operand count is and is not visible |
| `receipts/05-quote-verification.txt` | the 12-quote machine check (0 failures) |
| `receipts/06-merge-and-considerthese.txt` | merge-package listing + digests + theme screen; considerthese listing + digest + theme screen + the seven proposals |
| `receipts/07-census-schema-probe.txt` | the census NF=13 / E11 / projected-after histogram probe on a scratch copy, plus the downstream-instrument runs on the S099 tree |
| `receipts/receipts-base-probe.txt` | base-gate verdicts for the three canonical derives |
| `receipts/receipts-native-rc.txt` | native per-stage rc and stderr byte counts |
| `receipts/receipts-pipestatus.txt` | bash `PIPESTATUS` for the same three derives |
| `receipts/receipts-scope-boundary.txt` | sort / head / cat multi-operand comparison (which heads mask) |
| `receipts/receipts-operand-forms.txt` | stdin-redirect and flag forms at the gate |
| `receipts/receipts-native-forms.txt` | native `PIPESTATUS` for those forms |
| `receipts/receipts-flag-form-corrected.txt` | the flag forms re-measured with the correct `want` |
| `receipts/receipts-redirect-plus-operand.txt` | stdin-redirect + operand form |

Scratch `/fast/scratch/hyaku/kasegi-r66/ScoutOwnSource/` (fixture root `work/root`, 2 200 000-byte `big.txt`;
scratch trees `census2/`, `census3/`, `laneclone/`; `TMPDIR` exported to it for every run) was **deleted after the
durable receipts were copied**. No shared clone was created in the lane.
