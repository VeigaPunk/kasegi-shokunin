# Round 24 — lesson (kasegi)

Round 24: two frozen claims (`.ufo/waves/round-24/claims.json`), base
`d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`, lane tip at attempt start
`c2480b1`. Round shape: wave 1 `kasegi-r24-build` 43 seats, wave 2
`kasegi-r24-falsify` 35 seats (attack roles 24/35), total 78 inside the 128 cap.
This lesson is the round's Gate record, the assimilation record, the census
record and the mined-mistake record.

## Claims and what the counters said

| Claim | Axis | Counter | Before | After |
|---|---|---|---|---|
| C1 | depth:verifiability (4, lowest) | frozen shell form, cwd-pinned: every Frontier entry's own `recheck:` exit 0 | **3/8** | **8/8** |
| C1 | — | `frontier-recheck-count.py` (harness, entry-bound) | **3/8**, exit 1 | **10/10**, exit 0 |
| C1 | — | `resolve-dispatch-check.py` on baseline bytes `690153ad…` vs landed `db5e0767…` | **4/8**, exit 1 | **8/8**, exit 0 |
| C1 | — | round-23 containment matrix (`mirror-containment-check.py`) regression | 24/24 exit 0 | 24/24 exit 0 |
| C2 | coverage (7) | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | **8** | **9** |
| C2 | — | entries citing a row first registered this round (`grep -lE '^source: S03[2-5] ' corpus/knowledge/*.md \| wc -l`) | **0** | **2** |
| guard | depth:density (9) | `density.py SKILL.md --label r24` | 154.0 | **154.0** (SKILL.md bytes untouched) |
| guard | — | `anchorcheck.py SKILL.md` | 0 bad, LOST-RECORDED=306 | same, exit 0 |

Do-nothing control: the unchanged tree and the round-23 resolver bytes cannot
reach either C1 target (3/8 and 4/8). Receipts:
`.ufo/waves/round-24/c1-counterA-{before,after}.json`,
`c1-counterA-shell-{before,after}.txt`, `c1-control-baseline.txt`, `c1-fixed.txt`,
`c1-containment-regression.txt`, `c1-counterA-manifest-receipt.txt`.

## Gate — assimilation (addendum §10)

Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi` (read-only; no campaign tool
run there). Round shape: ONE theme — authorisation that exists outside a
platform's safe-harbour text — with two entries.

**Collision check (scratch, committed as wave evidence).** Lane registry max
**S031**; staged set **S031–S124** (94 rows). `comm -12` on the 0-3-space id
pattern → **1 collision: S031** (staged = HackerOne `policy_versions`, lane =
CVE CNA Rules v4.2.6, mined in round 23). Guard proved first on a scratch
registry with an indented colliding row (`assimilation/guard-proof.txt`): the
0-3-space pattern reports the collision, a column-zero-only pattern reports none.
`assimilation/{reg-ids,staged-ids,collisions}` hold the two id lists and the
collision set; `assimilation/renumber-map.tsv` holds the adopted map:
staged **S123→S032** (NIST SP 800-115), **S039→S033** (e-Gov lawdata), **S040→S034**
(総務省 page), **S041→S035** (警察庁 commentary). Ids continue the lane registry in
append order and follow the document; the remaining 90 staged rows are not
adopted and get **no** id (a later round re-derives its own map from the registry
max at that time).

**Scope check per entry (PROVINCE).** Both admitted entries govern authorisation
for a security engagement — program-rules/scope ground the province already
claims. The package's national-grading-standard entries (`chinese-national-
grading-model`, `gb30279-*`, `cnnvd-grading-*`) were judged **adjacent**: they
govern a standards body's classification instrument, not a program rule, scope,
triage gate or claim package (wave-1 `SrcCNGrading` measured each against
PROVINCE.md:29/37). Not adopted this round.

**Expansion credit is on non-held ground.** At base, repo-wide
`grep -riE 'rules of engagement|engagement document|statutory authorization|statutory authorisation|不正アクセス' SKILL.md corpus/ PROVINCE.md`
→ **0 hits**; the lane holds the platform-side statement (F03) and the EU
manufacturer duty (F08), not an engagement instrument and not a statute that
defines unauthorised access. Correction adopted from the wave-1 critic: the lane
*does* hold a statute (the CRA); what it did not hold is a statute that defines
authorisation.

### Admitted

| Row | Admitted as | URL | Opened | Located quote (≤25 words) | Entry |
|---|---|---|---|---|---|
| S032 | A, `mined` | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf | 2026-10-25 | "Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information security testing." (glossary, printed F-2) | `corpus/knowledge/authorised-testing-rules-of-engagement.md` |
| S033 | A, `mined` | https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 | 2026-10-25 | 「不正アクセス行為」とは、次の各号のいずれかに該当する行為をいう。 (第二条第四項) | `corpus/knowledge/statutory-authorization-and-unauthorized-access.md` |
| S034 | B, `mined` | https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/ | 2026-10-25 | 不正アクセス行為とは、そのようなIDやパスワードによりアクセス制御機能が付されている情報機器やサービスに対して | same entry (tier B: page prints 第二条 1〜3略 and the superseded 懲役) |
| S035 | A, `mined` | https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf | 2026-10-25 | なお、アクセス管理者又はその承諾を得た者が行う場合は禁止の対象から除外して (第二条第四項 explanation) | same entry (commentary, not statutory text) |

Each was re-opened by this lane (`capture-source.py`, digest in the manifest);
the package's own `opened`/quote prove nothing about this lane. Every assertion in
`corpus/source-snapshots/round-24/manifest.json` was measured exactly-once before
it was written; `source-recheck.py` exits 0 over 19 records / 77 assertions.

### Refused

| Candidate | Failing gate | Reason (evidence) | Flip condition |
|---|---|---|---|
| `chinese-criminal-thresholds-and-authorisation.md` | Q2 + Q4, and Q1/Q7 | Its own cited 第二百八十五条 text (S045, re-opened 200/589 780 B, p. 56) carries no 情节严重 element for the first paragraph, while the entry asserts "criminal risk attaches to scale and effect, not to the mere act"; "purely quantitative" is falsified by 第一条(五) 其他情节严重的情形 (S044); its `recheck:` is prose and its `curl -sSL` exits 0 on a 404; `ground: F12` names no lane frontier item. | Restate 285(1) as a conduct offence, quote 第一条 in full including (五), make the recheck fail closed, add `### Rejected`, register the rows under lane ids. |
| `chinese-national-grading-model.md`, `gb30279-2020-edition-provenance.md`, `cnnvd-grading-specification-primary.md` | PROVINCE scope | Standards-body classification instruments, not program rules/scopes/claim packages; two also fail Q1 (no H1) and Q6/Q7 shape. | An entry that states a rule a claim reviewer can apply to a program or package, not a standard's table. |

### Quarantine — absent-defect register slice (`assimilation/quarantine-slice`)

The register derived 7 kasegi rows (`absent-defect-register.md`, data rows only).
None is adopted this round; each was hand-checked (`quarantine-handcheck.txt`):

| Staged row | Register class | Hand-check 2026-10-25 | Verdict |
|---|---|---|---|
| S037 | payload-absent | catalogue page 200/24 123 B; the standard's body is behind the preview tool | reachable page, body absent — not adopted |
| S054 | payload-absent | IPA request PDF 200/513 648 B | reachable; not adopted (not cited by this round's entries) |
| S048 | could not be fetched | `gbDetailed?id=3B865A…` **404**/748 B | dead as cited — refuse until an R8 `supersedes` row names a live id |
| S065 | could not be fetched | npc.gov.cn PDF 200/3 483 303 B | reachable; not adopted |
| S068 | could not be fetched | Cisco policy page 200/94 027 B | reachable; not adopted |
| S069 | could not be fetched | `gbPlan/download?path=…` 302/0 B | unreachable as cited |
| S070 | could not be fetched | `gbPlan/download?path=…` 302/0 B | unreachable as cited |

`payload-absent` and "could not be fetched" are the register's unchecked families:
reachability today does not certify the quote, and no quote was located for these
rows this round, so none is appendable.

### Registry changes this round (old → new)

- New rows **S032–S035**: status `— → mined`, `opened — → 2026-10-25`,
  `recheck — → 730d / 730d / 180d / 730d`, `used-by — → the entry path above`.
- **S034 title** `不正アクセス行為の防止等に関する法律の解説 → 不正アクセス行為の禁止等に関する法律の解説`
  (the page's own `<title>` and the statute say 禁止). Corrected before landing,
  same round, logged here; no row was filed against a wrong law name.
- No existing row's status, recheck or used-by changed.

### Census (contract commands; `census-before.txt`, `census-after.txt`)

```
before: rows 31  malformed 0  tier A=29 C=2  status mined=19 queued=9 rejected=3
        validate --root … kasegi → exit 0, W04 S028, W04 S029
after:  rows 35  malformed 0  tier A=32 B=1 C=2  status mined=23 queued=9 rejected=3
        validate --root … kasegi → exit 0, W04 S028, W04 S029 (both pre-existing,
        both declared cross-scope duplicates: S028 is the rejected duplicate-row
        proposal and S029 opens `supersedes S024 —`)
```

The two W04s are unchanged and expected. `--file` validation of a scratch mirror
of the registry plus the two entries was run before the append
(`SOURCESRows` receipt) — E11 cleared once both entry files existed.

### considerthese (at most one proposal)

`considerthese/2026-10-24.md` proposal 1's unlanded conjunct — "require each quote
to match exactly once or carry an `SNNN.txt:LINE` anchor" — landed as **QUALITY
Q9** plus code: `source-recheck.py` rejects a quote shorter than 12 normalized
characters, prints `occurrences=N` on every pass, and verifies a declared
`anchor` line (the round-23 manifest's one non-unique assertion now reads
`S029:art14-2a-early-warning OK occurrences=2 anchor=10-ok`). Proposals 2, 3 and
the rest were already landed in round 23 (`QuarterConsiderthese` confirms);
proposals 4–5 are operational/operator-owned.

## Routed defects from the round-23 verifier spot-check

| Defect | Disposition |
|---|---|
| 1. F01–F05 `recheck:` exit 2 `not-listed` | **Fixed and measured**: S001–S015 captured, F01–F05 re-pointed at the round-24 manifest (same line, length-neutral), counter A 3/8 → 8/8. |
| 2. Detector liveness (first-match brace/glob; never-resolving empty brace alternative) | **Fixed and measured**: `brace_expand` keeps an empty alternative in a real set (a bare `{}` stays a placeholder), a brace alternative that carries a `<...>` placeholder is globbed, the glob branch credits the first match that exists. Counter B 4/8 → 8/8; containment 24/24 held. |
| 3. Attempt numbering ("attempt 2" vs three `attempt=1` launches) | **Closed by record**: the lane counts *landings* (`8bf9807` = landing 1, `953c278…d0a3f6a4` = landing 2), the host counts *launches* (three, all `attempt=1`). This lesson fixes the convention: a round report states both when they differ. Historical cells left verbatim (R9). |
| 4. SCORECARD r23 C1 cell shows the first landing with errata appended | **Not cosmetic, recorded, not rewritten**: the cell's numbers are true at `953c278`, but the receipt paths it cites were overwritten at `bf9ce02`, so the cell is reachable only via `git show 953c278:.ufo/waves/round-23/c1-fixed.json` (verified). The erratum block above the cell already carries the superseding numbers; consumers must read the receipt at its commit. |

## Mistakes

**M24-1 · a repair's universal claim landed on a partial fix.** Class:
over-general assertion without a full-set receipt. Evidence:
`corpus/lessons/round-23.md` states "every `recheck:` line now begins `cd
/home/vgpnk/Projects/shokunin/kasegi-shokunin &&`"; measured this round, **3 of 33**
recheck lines carry the prefix (3 of the 8 on the surface the round actually
repaired), and running all eight from `/tmp` gives 3× exit 0 and 5× exit 2
(`python3: can't open file '/tmp/corpus/instruments/source-recheck.py'` — the
frozen counter's cwd-dependence, not `not-listed`). Captured-by: **Q7** (an
executable recheck that was never executed at landing) + **R2** ("every" without
a full-set count). Fix: a universal quantifier is written only with the command
that enumerates the full set in the same commit — the round-24 harness
`frontier-recheck-count.py` is that command for the Frontier set, and it pins the
cwd itself.

**M24-2 · a row titled a law that does not exist.** Class: transcription error in
a new registry row. Evidence: S034 was first written as
`不正アクセス行為の**防止**等に関する法律の解説`; the cited page's own `<title>` and
平成11年法律第128号 read **禁止**. Captured-by: none (no instrument reads a row
title against the page it cites) — **none** is the honest answer, and that is
what makes it a gap: the census checks schema, not title fidelity. Fix: the row
was corrected before landing (old → new in the Gate above) and Q2/Q3 now carry the
title in the located-quote requirement for the admitting round.

**M24-3 · a read-only probe overwrote the census of record.** Class: instrument
without argument validation. Evidence: `python3 corpus/instruments/resolve.py
--help` took `--help` as a lane root and wrote a zero-row
`corpus/instruments/citation-survival.{md,tsv}` (wave-1 `QuarterSHONEN` restored
them byte-exact from `master`, sha `793e0a4e…`/`795ba4f2…`, window ~2 min,
disclosed). Captured-by: **R3** would have caught it only after the fact; the
instrument had no guard. Fix: the CLI now refuses a non-directory root (exit 2,
usage on stderr) and refuses to write a census when it collects no citations
(`resolve.py`, exercised: `resolve.py --help` → exit 2, no write).

**M24-4 · the matrices could not see the bound they depend on.** Class: fixture
matrix narrower than the code path it justifies. Evidence: a mutant lowering
`brace_expand`'s 64-combination bound to 8 scores **8/8** on the dispatch matrix
and **24/24** on the containment matrix while flipping real verdicts (no case has
more than four brace alternatives). Captured-by: **R10** as written covers
spellings, not resolution power — **none** of the existing criteria required a
mutant receipt. Fix: **R11** (a counter publishes its discrimination against
degenerate and mutated instruments) plus the published blind spot in
`corpus/instruments/README.md`; closing it needs a ninth case and is left to
round 25, which the round reports rather than pretends.

**Misroot sweep.** `git -C /home/vgpnk/Projects/shokunin status --porcelain` at
round end: no untracked fleet-root file names this lane or round 24 (wave-1 seats
wrote only under the lane's `.ufo/waves/round-24/`); nothing to copy back, and no
fleet-root file was deleted.

## Waves

- Wave 1 `kasegi-r24-build` — 43 seats: scout 22, reviewer 7, executor 5,
  scribe 3, critic 3, mutation-tester 1, connector 1, sentinel 1; all 43 reports
  landed under `.ufo/waves/round-24/wave1/`. The §3 L2 floor is met inside wave 1;
  the L1 holds the canonical planner seat and `PlannerWalk` supplied its data-walk.
- Wave 2 `kasegi-r24-falsify` — 35 seats, attack roles 24/35: reviewer 12,
  critic 6, revenger 3, mutation-tester 2, sentinel 1, plus scout 8, scribe 2,
  executor 1. First dispatch refused at the host job limit
  (`wave2-refusal-1.json`, `Background job limit reached (100)`, 0 spawned);
  payload resent unchanged.
- Dead seats: none in wave 1 or wave 2.
