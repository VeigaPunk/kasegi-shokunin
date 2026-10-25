# ClaimsIntegrity — round-23 FALSIFY (claims.json provenance & freeze ordering)

Seat: `L1Kasegi23.ClaimsIntegrity-2`. Lane: leaf, no dispatch. Read-only against committed
bytes and `git` plumbing; no production file, lane tree, index, or ref was written. The only
file this seat wrote is this report.

Tools installed or updated: **none required** (git 2.x and python3 already present; no package
transaction, no network).

---

## 0. Method

Every conclusion below is reproduced from a command in this file. Where a value is derived by
inference rather than observed, it is labelled `[INFERENCE]`. Nothing is taken from the L1
planner, from any sibling report, or from `claims.json`'s own prose as though it were evidence.

Working-tree state at start (only `LOG.md` differs from HEAD; nothing under test was dirty):

```
$ git -C …/kasegi-shokunin status --porcelain=v1
 M LOG.md
$ git diff --stat HEAD
 LOG.md | 39 +++++++++++++++++++++++++++++++++++++++
 1 file changed, 39 insertions(+)
```

---

## 1. When did `claims.json` first appear?

### 1.1 The file does not exist at its own declared `base`

`claims.json:3` declares `"base": "922a4dde90b60b465e2b8b241d1fe363f1f27e98"`.

```
$ git cat-file -e 922a4dd:.ufo/waves/round-23/claims.json
→ (exit 1) ; echo $(git rev-parse 922a4dd:.ufo/waves/round-23/claims.json)
→ ABSENT
$ git cat-file -p 922a4dd:.ufo/waves/round-23/claims.json
fatal: path '.ufo/waves/round-23/claims.json' exists on disk, but not in '922a4dd'
```

The base is still a legitimate *branch point* (`git merge-base --is-ancestor 922a4dd 8bf9807`
→ YES; `git log --oneline 922a4dd..8bf9807` → `8bf9807`, `2b10754`). It is substantiated as the
"before" revision by `before-instruments.json` (`revision` field = the same SHA). But a reader
who treats `"base"` as "the tree the claims were written against" is wrong: the claims file is
not in that tree.

### 1.2 Four commits carry the claims blob; only one is reachable

```
$ git log --oneline --all -- .ufo/waves/round-23/claims.json
8bf9807 checkpoint(r23): archive developed corpus and local tooling; …
e812b74 checkpoint(r23): archive developed corpus and local tooling; …
f9462ad
893b816
$ git rev-list HEAD -- .ufo/waves/round-23/claims.json
8bf980721554d2d24bcc83e2e0996e0c27684a06
```

| commit | parent | tree | ancestor of HEAD | subject | committer time |
|---|---|---|---|---|---|
| `893b816` | `922a4dd` | `cb3963a` | **NO** | *(empty)* | 19:33:49 |
| `f9462ad` | `922a4dd` | `cb3963a` | **NO** | *(empty)* | 19:33:50 |
| `e812b74` | `922a4dd` | `cb3963a` | **NO** | checkpoint(r23)… | 19:33:50 |
| `8bf9807` | `2b10754` | `1fa3e92` | **YES** | checkpoint(r23)… | 19:33:51 |

Author date is **identical to the second** on all four (`2026-10-20T18:30:56-03:00`), while the
committer clock runs 19:33:49→51. One commit carries a placeholder author identity:

```
$ git log -1 --format='%an <%ae> %aI / %cn %cI' 893b816
t <t@e> 2026-10-20T18:30:56-03:00 / kasegi-shokunin <kasegi@shokunin.local> 2026-10-20T19:33:49-03:00
```

The reflog names the mechanism rather than tampering:

```
$ git reflog --all | grep -E '8bf9807|893b816|f9462ad|e812b74'
8bf9807 refs/remotes/origin/master@{3}: update by push
8bf9807 refs/heads/master@{3}: export from jj
8bf9807 HEAD@{3}: export from jj
e812b74 refs/heads/master@{4}: export from jj
e812b74 HEAD@{4}: export from jj
```

`[INFERENCE]` These are successive Jujutsu export attempts of one working-copy commit, replaced
one second apart until the export landed on the correct parent (`2b10754`) as `8bf9807`. The
content never differed: the blob is `67defdb` in **all four**.

**Answer:** `claims.json` first appears at **`8bf9807`**, `2026-10-20T18:30:56-03:00` author /
`19:33:51-03:00` committer. Any citation of "first appeared" that uses the author timestamp is
63 minutes early, and any inventory built with `git log --all` will double-count three
unreachable twins.

---

## 2. Did the C1/C2 predicate, detector, or target text change between `922a4dd` and the working tree?

**No — the text has never changed since creation, because it did not exist at the declared base.**

```
$ git hash-object .ufo/waves/round-23/claims.json   → 67defdb93e67d69c3e51821ad3c4bf6f4dcce6d1   (worktree)
$ git rev-parse HEAD:.ufo/waves/round-23/claims.json → 67defdb93e67d69c3e51821ad3c4bf6f4dcce6d1
$ git rev-parse 8bf9807:.ufo/waves/round-23/claims.json → 67defdb93e67d69c3e51821ad3c4bf6f4dcce6d1
$ git diff HEAD -- .ufo/waves/round-23/claims.json   → (empty)
$ sha256sum .ufo/waves/round-23/claims.json
84fd2d3e1964373c95551624988953448cbab36001ae6454803cf82a2f38836c   (2250 bytes, 8 lines)
$ python3 -c "import json; json.load(open('.ufo/waves/round-23/claims.json'))"
→ PARSE: OK
```

All six field groups (`round`, `base`, `C1`, `C2`, `supporting_corrections`, `admission`) are
byte-identical at freeze, HEAD, and in the working tree. `C1` carries `axis/detector/claim/
before_observed/after/guard`; `C2` carries `axis/claim/before/after/count`. The file is valid
JSON.

**Falsification test:** a claims blob other than `67defdb` in any reachable commit, or a
non-empty `git diff HEAD -- .ufo/waves/round-23/claims.json`. Both fail.

---

## 3. Were files the claims reference edited after the freeze in a way that changes their meaning?

Freeze = `8bf9807`. The only later commit touching the corpus is `953c278`
(`2026-10-25T03:35:35-03:00`), i.e. **4 days 8 hours after** the freeze commit's committer time.

### 3.1 The entire C1 acceptance set was authored after the freeze

`git ls-tree 8bf9807 .ufo/waves/round-23/` returns exactly:

```
before-instruments.json  build-assignments.json  build-attempt-3.json  build-attempt-4.json
build-attempt-5.json     build-dispatch.json     build-refusal-1.json  build-refusal-2.json
build-spec.json          build/                  claims.json
opened-source-snapshots.json  source-open-transcript.json
```

`c1-baseline.json`, `c1-fixed.json`, `c1-baseline-resolver.py` → **ABSENT at freeze**, present
at HEAD. And:

```
$ git ls-tree 8bf9807 corpus/instruments/ | grep mirror-containment
→ (no output)
$ git ls-tree HEAD corpus/instruments/ | grep mirror-containment
100755 blob e356faa7… corpus/instruments/mirror-containment-check.py
100644 blob 4ede1bcc… corpus/instruments/mirror-containment-fixtures.json
```

`claims.json:4` asserts: *"All **declared** mirror-escape and prefix-confusion fixtures classify
GONE; confined controls retain expected classes. Before and after use identical fixture inputs
and actual copied CLI."* At freeze **nothing was declared** — there was no fixture file, no
replay harness, and no receipt on either side.

### 3.2 The entire C2 quote-pinning layer was authored after the freeze

```
$ git rev-parse 8bf9807:corpus/source-snapshots/round-23/manifest.json
fatal: path …/manifest.json exists on disk, but not in '8bf9807'
$ git ls-tree -r 8bf9807 corpus/source-snapshots/round-23/
… S018.txt   (e12b3564…)
… S029.txt   (3f999368…)
… S030.txt   (8c268023…)
$ git ls-tree -r HEAD corpus/source-snapshots/round-23/     # adds manifest.json cabdd68c…
```

The *snapshot bytes* were frozen (same blobs at freeze and HEAD). What was **not** frozen is the
assertion layer that turns them into "exact located quotes": `manifest.json`.

The instrument that would consume it **did** exist at freeze
(`corpus/instruments/source-recheck.py`, blob `790e9dd`, identical at freeze and HEAD) and fails
closed without a manifest:

```
corpus/instruments/source-recheck.py:238-239
    if args.manifest is None:
        emit(sys.stdout, "manifest", "UNAVAILABLE", "reason=missing-required-argument")
```

`[INFERENCE]` Therefore at freeze the C2 clause *"exact located quotes and executable local
rechecks"* could not have been discharged against round-23: the recheck would have emitted
`manifest UNAVAILABLE`. It is executable now, and does pass (see §4.4).

### 3.3 Referenced-file drift table (base → freeze → HEAD)

| path | `922a4dd` | `8bf9807` | `HEAD` | post-freeze change |
|---|---|---|---|---|
| `corpus/instruments/resolve.py` | `2b1e252` | `2b1e252` | `490b19d` | **yes** — the C1 detector itself |
| `corpus/instruments/mirror-containment-fixtures.json` | ABSENT | ABSENT | `4ede1bc` | **created** |
| `corpus/instruments/mirror-containment-check.py` | ABSENT | ABSENT | `e356faa` | **created** |
| `corpus/instruments/source-recheck.py` | ABSENT | `790e9dd` | `790e9dd` | no |
| `corpus/source-snapshots/round-23/manifest.json` | ABSENT | ABSENT | `cabdd68` | **created** |
| `corpus/source-snapshots/round-23/S018,S029,S030.txt` | ABSENT | `e12b356,3f99936,8c26802` | identical | no |
| `corpus/README.md` | `df3f859` | `df3f859` | `f7ce199` | **yes** — C2 target |
| `corpus/SOURCES.md` | `01fcdbb` | `511e82a` | `511e82a` | no |
| `corpus/QUALITY.md` | `1013081` | `e12f145` | `e12f145` | no |
| `corpus/knowledge/multiparty-vulnerability-coordination.md` | ABSENT | `d1e41ca` | `d1e41ca` | no |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` | ABSENT | `c11fbd4` | `3fa9807` | **yes** |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | ABSENT | `c965350` | `5153d59` | **yes** |

`corpus/README.md` is the named C2 measurement target (`claims.json:5`, `"count": "Count
admitted F06-F08 rows in corpus/README.md …"`). It moved after the freeze:

```
$ git cat-file -p 922a4dd:corpus/README.md | sed -n '200,202p'
| F06 | … | queued | — | S018 | … |
| F07 | … | queued | — | S022 | … |
| F08 | … | queued | — | S024 | … |
$ grep -nE '^\| F0[678] ' corpus/README.md      # HEAD
200:| F06 | Multi-party CVD — FIRST guidelines v1.1 | admitted | knowledge/multiparty-… | S018 | … |
201:| F07 | CVE CNA operational rules | admitted | knowledge/cna-… | S030 (supersedes S022) | … |
202:| F08 | EU Cyber Resilience Act reporting duties | admitted | knowledge/cra-… | S029 (supersedes S024) | … |
$ grep -cE '^\| F0[1-8] .*\| admitted \|' corpus/README.md
8
```

So C2's `before` value is truthful (`0/3` queued at both `922a4dd` and `8bf9807`) and its
`after` (`3/3`) matches HEAD. But the **evidence pointers** moved post-freeze
(`S022→S030`, `S024→S029`) without any amendment to `claims.json`. Note `SOURCES.md` already
carried S029/S030 at freeze (`511e82a`, unchanged to HEAD), so the superseding sources existed
at freeze while the README still pointed at the superseded ones — `[INFERENCE]` a genuine
at-freeze inconsistency that `953c278` repaired. `claims.json` does not contradict this move
(it names no `S###` ids), so this is drift-without-amendment, not a false statement.

---

## 4. What checks out (recorded so the findings below are not over-read)

### 4.1 Receipt ↔ bytes hash equality

```
$ sha256sum corpus/instruments/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9
  == c1-fixed.json:  "resolver_sha256": "ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9"

$ sha256sum corpus/instruments/mirror-containment-fixtures.json
5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9
  == c1-fixed.json:   "matrix_sha256": "5e61a33e…"
  == c1-baseline.json:"matrix_sha256": "5e61a33e…"      ← same matrix on both sides

$ sha256sum .ufo/waves/round-23/c1-baseline-resolver.py
d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903
  == c1-baseline.json: "resolver_sha256": "d6a3c3f1…"
```

### 4.2 The baseline resolver really is pre-fix bytes

```
$ git rev-parse 8bf9807:corpus/instruments/resolve.py  → 2b1e2528a064f918c5e82c03e109a456e1e72589
$ git rev-parse 922a4dd:corpus/instruments/resolve.py  → 2b1e2528a064f918c5e82c03e109a456e1e72589
$ git rev-parse HEAD:.ufo/waves/round-23/c1-baseline-resolver.py → 2b1e2528a064f918c5e82c03e109a456e1e72589
$ cmp -s .ufo/waves/round-23/c1-baseline-resolver.py <(git cat-file -p 8bf9807:corpus/instruments/resolve.py) && echo IDENTICAL
IDENTICAL
```

Git-blob identity is exact: the do-nothing control is byte-for-byte the frozen detector. This is
the strongest part of the C1 package.

### 4.3 The fixture matrix is not a tautology

`c1-baseline.json` totals: `escape 6, controls 7, fail 6, pass 7`. `c1-fixed.json` totals:
`escape 6, controls 7, fail 0, pass 13`, same `matrix_sha256`. The matrix therefore
*discriminates* pre-fix from post-fix rather than passing unconditionally.

### 4.4 C2 assertions hold on committed bytes

```
$ sha256sum corpus/source-snapshots/round-23/*.txt
d366bf409e7ce9e3…  S018.txt   (manifest d366bf40… MATCH)
82514478b6c5fb8f…  S029.txt   (manifest 82514478… MATCH)
673526db7c2b4fde…  S030.txt   (manifest 673526db… MATCH)
quotes: S018 6/6 present, S029 6/6 present, S030 7/7 present
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json
S018:sha256 OK … S030:rule-4-2-12-uncertainty OK      (19 assertions)
EXIT=0
```

### 4.5 Apparent contradiction that is not one

Two fixture cases share the cite string `~/Projects/bounties-legacy/README.md:1` yet expect
opposite classes (`bounty-prefix-sibling-confusion` → GONE; `literal-prefix-sibling-control` →
RESOLVES), and both PASS in the same run. Reading
`corpus/instruments/mirror-containment-fixtures.json` resolves it: the escape case plants only
`relocated/tbh/-legacy/README.md` and leaves the literal path absent; the control plants the
literal `home/Projects/bounties-legacy/README.md`. Distinct filesystem setup, distinct correct
answers. **No defect** — recorded to stop another seat from reporting it as one.

---

## 5. Findings

Ordered by what they constrain. Each is stated so a single command can break it.

### F1 — HIGH — The C1 acceptance set, both receipts, and the replay harness all post-date the freeze

`claims.json:4` requires "All **declared** … fixtures classify GONE" and "Before and after use
identical fixture inputs". At the freeze commit `8bf9807`, no fixture file, no harness, and
neither receipt existed (`git ls-tree 8bf9807 corpus/instruments/`,
`git ls-tree 8bf9807 .ufo/waves/round-23/`). All were created in `953c278`, the same commit that
lands the fix.

Consequence: the fixture matrix is **co-authored with the fix**, so it cannot serve as a
pre-registered or independent acceptance control. The claim's own word "declared" has no
referent at freeze time. This is a freeze-ordering defect in the artifact set, not proof the
matrix was tuned (§4.3 argues against tuning).

*Breaks if:* any fixture/harness/receipt path is shown present at `8bf9807`.

### F2 — HIGH — C2's "exact located quotes" were unpinned and its recheck non-executable at freeze

`manifest.json` absent at `8bf9807`; `source-recheck.py` present but requires `--manifest`
(`:238-239`) and emits `UNAVAILABLE` without it. The snapshot complement (`S018/S029/S030.txt`)
was frozen, so only the *assertion* layer is post-freeze.

Consequence: `claims.json:5`'s "exact located quotes and executable local rechecks" could not be
evaluated at freeze; it became evaluable only in `953c278`. It does pass now (§4.4), so this is a
chronology defect, not a falsehood.

*Breaks if:* a `manifest.json` is shown in `8bf9807`, or `source-recheck.py` is shown to have had
a non-`--manifest` mode at freeze.

### F3 — MEDIUM — `C2.after` sets a Q1–Q6 bar that omits Q7, which the *same freeze commit* introduced

```
$ git cat-file -p 922a4dd:corpus/QUALITY.md | grep -c '^| Q7'   → 0
$ git cat-file -p 8bf9807:corpus/QUALITY.md | grep -c '^| Q7'   → 1
$ git diff --stat 922a4dd 8bf9807 -- corpus/QUALITY.md
 corpus/QUALITY.md | 11 +++++++++++
```

Q7, added in the freeze commit alongside `claims.json`, reads
(`corpus/QUALITY.md:48`): *"An executable recheck field contains a command, not prose beginning
'On each'. Its successful output names what was checked: a pinned captured-source comparison is
not a fresh network verification. At least one missing/corrupted-source control must fail."*

`claims.json:5` says `"after": "F06-F08 admitted 3/3 with **Q1-Q6** evidence"`. The claim's own
trigger clause is "**executable** local rechecks" — exactly what Q7 governs. So the frozen
acceptance bar omits the criterion added to the bar in the same commit.

*Breaks if:* `claims.json:5` is shown to name Q7, or Q7 is shown to have existed at `922a4dd`.

### F4 — MEDIUM — `C1.before_observed` has no at-freeze receipt; the observed red state is first recorded 4 days later

`claims.json:4` states a concrete pre-fix observation: *"`~/Projects/bounties/../outside.md` is
MIRROR-EQUIVALENT for a file outside mirror"*. The only at-freeze instrument receipt is
`before-instruments.json` (`revision` = `922a4dd`), whose resolver census reports

```
distinct=1589 resolves=11 mirror=0 internal=197 other=0 gone=1381 skill=39/513 corpus=192/1262 all=208/1589
```

`mirror=0` over the real corpus, and it contains no `~/Projects/bounties/../outside.md` probe.
That probe appears only in `c1-baseline.json`, created in `953c278`.

Consequence: the red-before value is a post-freeze reconstruction of pre-fix behaviour, not an
at-freeze observation. It is *corroborated* by §4.2 (the control is byte-identical to the frozen
resolver), so the reconstruction is well-founded — but the chronology is unprotected.

Second-order note for other seats: `mirror=0` in the before census does **not** contradict
`C1.before_observed`. The corpus census and the synthetic probe measure different populations.
It does establish that the fix cannot move any real corpus citation verdict, which is consistent
with `claims.json:4`'s "Score remains 4".

*Breaks if:* the probe string is shown inside `before-instruments.json`.

### F5 — MEDIUM — `C1.guard` is one-sided: a before census exists, no after census does

`claims.json:4` guard: *"Frozen pre-round SKILL, PROVINCE and corpus against each detector;
report all changed verdicts, density and anchorcheck."*

`before-instruments.json` (blob `856ce4c`, unchanged freeze→HEAD) holds
`results.{resolver,anchors,density}` pinned to `922a4dd`. No after-side counterpart exists:

```
$ ls .ufo/waves/round-23/ | grep -i after
(none)
$ grep -rn -E 'r23-after|r23_after|after-instruments' .ufo/waves/round-23/
(none)
```

Consequence: the guard's obligation to "report all changed verdicts, density and anchorcheck" is
satisfied only for the pre-round side. The post-fix density and anchorcheck readings are not
committed anywhere, so "changed verdicts" cannot be computed from committed receipts.

*Breaks if:* an after-side census receipt pinned to `HEAD`/`953c278` is produced.

### F6 — LOW — Provenance hygiene: the claims ride on jj-export artifacts and a placeholder identity

Recorded in §1.2. Content is unaffected (one blob, `67defdb`, everywhere). Two practical risks:
(a) `git log --all -- <path>` yields four "first appearances", three unreachable, so any
freeze-timestamp audit built on `--all` over-counts; (b) commit `893b816` carries author
`t <t@e>`, which a non-author auditor could mistake for a foreign injection rather than a local
export artifact — the `export from jj` reflog is what distinguishes them.

*Breaks if:* a reachable claims commit other than `8bf9807` exists, or any claims blob differs
from `67defdb`.

---

## 6. Confidence

| Claim | Confidence | Basis |
|---|---|---|
| `claims.json` absent at `922a4dd`; text never changed since `8bf9807` | **High** | three-way git blob identity + empty diff + `cat-file -e` |
| First appearance = `8bf9807`; three unreachable jj twins | **High** | `git rev-list HEAD --` vs `git log --all --` + per-commit parent/tree parenthood |
| jj-export explanation for the twins | Medium (`[INFERENCE]`) | reflog strings + 1-second committer spacing; mechanism not otherwise documented |
| Fixtures/harness/receipts/manifest all post-date the freeze | **High** | `git ls-tree` at `8bf9807` returns no such paths |
| Baseline control is genuine pre-fix bytes | **High** | git blob `2b1e252` identical at `922a4dd`, `8bf9807`, and the control file |
| Q7 introduced in the freeze commit while `C2.after` says Q1–Q6 | **High** | `grep -c '^| Q7'` 0→1 across `922a4dd`→`8bf9807`; `claims.json:5` verbatim |
| C2 assertions hold on committed bytes today | **High** | 3 digests + 19 quotes + `source-recheck` exit 0 |
| No after-side guard census exists | **High** | two independent greps + directory listing |
| Intent behind the post-freeze pointer move `S022→S030`, `S024→S029` | Low (`[INFERENCE]`) | consistent with "current rules" wording, but no statement of intent is committed |

---

## 7. Scope limits

- **No re-execution of the C1 matrix.** `mirror-containment-check.py` replay belongs to the
  matrix-rerun lane; this seat established receipt-vs-byte hash equality instead (§4.1–4.3) and
  deliberately did not duplicate that run.
- **No network, no upstream-source verification.** Digest and quote checks prove the pinned
  captures are internally consistent; they do **not** prove the captures match today's upstream.
  `manifest.json`'s own `purpose` string makes the same disclaimer.
- **No scoring, no admission judgement, no self-credit.** Whether round-23 is admitted is not
  this seat's question.
- **Working tree vs HEAD.** Only `LOG.md` is modified (39 insertions); its content was not read
  as evidence for any finding.
- **`LOG.md` narrative, `build/*.md` seat reports, and `falsify-spec.json`** were used only to
  locate paths; no finding rests on their prose.
