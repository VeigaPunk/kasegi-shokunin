# Round 23 — detector soundness and three public-practice frontier surfaces

Base revision: `922a4dde90b60b465e2b8b241d1fe363f1f27e98`.
Claims frozen before dispatch in `.ufo/waves/round-23/claims.json`: C1 actual
`resolve.py` mirror-fallback soundness (depth:verifiability, lowest score 4);
C2 F06–F08 coverage, 0/3 → 3/3. Neither claim restores a lost domain source.
Score 4/7 remains held; raw semantic cases and frontier counts carry the moves.
The L1 holds the canonical planner seat. Wave advice is author-side, never an
independent admission or promotion judgment.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | Wrong-axis claim and stale self-description | `round-22-verifier-spotcheck.md`: C1 REJECTED-HONEST-STOP; original r22 lesson line 5 says unmeasured after the work landed; SCORECARD repertoire rollout deferral contradicted its populated row | R7 (new); R4 did not catch an axis mismatch | Freeze C1 against actual copied resolver output; correct scorecard placeholder; append this correction rather than rewrite the filed r22 lesson. R22 header/historical-marking work is provenance/freshness, not an admitted depth move. |
| M2 | Admitted entries carried prose rather than executable rechecks | `round-22-verifier-spotcheck.md`: five r22 new rechecks exit 2; `knowledge/cvss-v4-severity-and-vector.md` line 4 begins “On each” | Q7 (new); Q1 was too permissive about URL/cadence | Replace same-line rechecks with a local pinned-source command; its output must distinguish captured support from fresh network verification. Missing/corrupt captured-source controls must fail; existing lost-base legacy rechecks remain red and marked historical. |
| M3 | Stale line pointers in filed lessons | `round-22.md` M3 points README:168, M14 points README:145; current evidence is README:176–177 and README:153–156 respectively at the opening revision | R9 (new); R2 | This new correction names the matching text and opening revision. M3 is the critic's partial docs-only search missing a lost-tree decree; M14 is the missing round-2 record. Old pointers remain historical, not silently repaired. |
| M4 | Deletion tally scope was not re-derived | `round-22-verifier-spotcheck.md`: reported 22 versus actual 32 deletions | R9 (new); R2 | Retain the original record and publish a base/path-scoped numstat correction in this lesson after the history derivation; never infer text loss merely from same-line suffix replacements. |
| M5 | Exact quote, wrong filed-record heading | `round-22.md:82` Gate S006 gives “What is safe harbor?” for the scope quote; S006 row and knowledge entry already name the correct heading; official page re-opened 2026-10-20 | R8/R9 (new); Q3 | Correct location is “How to Enable Safe Harbors (Program Owners & Admins)”. This appended erratum fixes the filed Gate record; no correction to S006 immutable fields is warranted. The proposed duplicate source row S028 is rejected, not a second authority. |
| M6 | Detector credits a file outside its selected mirror | Opening `resolve.py` classify: bounty-parent fallback returns MIRROR-EQUIVALENT for a sibling outside the mirror; explicit-mirror path already has confinement | Existing `under_mirror` invariant did not cover bounty/relative fallbacks | Apply the same realpath boundary to mirror fallbacks, preserve direct and lane-relative semantics, and compare the actual copied CLI against persisted case expectations before and after. |

The prior source losses and 23/25 legacy recheck failures remain known historical
limits, not recovered or converted to passing by local copies. No criterion is
credited merely because it was written: failing controls and final measurements
are recorded in the round's committed evidence.

## Gate

Opened public official sources on 2026-10-20. S029/S030 correct broadened scope
and current version using append-only successors. S028 is a rejected duplicate
proposal: its scope quote is real, but S006's row already has the right heading.

| row | URL | accessed | exact quote (≤25 words) | location |
|---|---|---|---|---|
| S028, rejected duplicate proposal | https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq | 2026-10-20 | “Adopting a Safe Harbor does not change the program scopes.” | How to Enable Safe Harbors (Program Owners & Admins), paragraph after the enablement list; S006 already records this heading |
| S029, supersedes S024 | https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng | 2026-10-20 | “no later than 14 days after a corrective or mitigating measure is available” | Regulation (EU) 2024/2847, Article 14(2)(c), OJ 20.11.2024 |
| S030, supersedes S022 | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf | 2026-10-20 | “CNAs SHOULD assign different CVE IDs to different, Independently Fixable Vulnerabilities.” | CNA Operational Rules 4.2.0, effective 2026-08-25, rule 4.2.11, page 15 |

Existing S018 re-opened: FIRST v1.1, “Maintain clear and consistent communications”
→ “Prior to disclosure”: “All parties should clearly and securely communicate and
negotiate expectations and timelines.” The HTML metadata title says version 1.0;
the document body explicitly says version 1.1 and Spring 2020, the recorded basis.

Candidates: F06 multi-party coordination, F07 CNA assignment rules, F08 CRA
manufacturer reporting. Their individual entries contain a falsifiable local
package rule, exact located source support, rejected over-generalization and
limits. Public source captures are normalized excerpts, not byte-authenticated
original HTTP responses or a fresh current-source check on every replay.

Rejected claims kept: upstream patch implies every downstream product fixed;
every fix/dependency upgrade requires another CVE; CRA grants testing permission
or sets a universal 24-hour researcher-publication deadline. Reasons appear in
each entry. Existing source rejects S026/S027 remain unchanged; no inaccessible
secondary source was promoted to official authority.

Author-side critic `KasegiR23.ImmutableSources-5` falsified our initial plan to
supersede S006: the bad location is `round-22.md:82`, while the registry row and
entry are correct. Accepted before landing: narrow R8 to registry-field changes,
keep S006 intact, and retain S028 as the rejected duplicate proposal with a flip.
This is an in-round correction, not an outside discernment spot-check.

Source-row transition: S018 `status: queued → mined`, `used-by: — →
corpus/knowledge/multiparty-vulnerability-coordination.md`; `recheck: 180d → 180d`.
S006, S022 and S024 existing fields remain unchanged; S022/S024 are historical
queued sources and the new S030/S029 rows carry the admitted current scope.

Spot-check: independent non-author admit-and-reject review is delegated to the
parent's separate closure after landing. Our waves are author-side evidence and
are not that judgment.

## Attempt 2 — 2026-10-25: landed detector soundness and F06–F08 admission

Lane tip at attempt start `1fafde8f11454f3b0b98ab7f2b2e640aaf7f399a` (checkpoint
`8bf9807`, "policy-paused, unadmitted, no task resumption"). Frozen claims are
unchanged from `.ufo/waves/round-23/claims.json` (base `922a4dde`); this attempt
runs C1 and C2 as frozen and adds no claim.

**Inherited vs re-verified vs discarded.** Reused after re-verification: the
three F06/F07/F08 knowledge entries, registry rows S018/S022/S024/S028/S029/S030,
the three pinned snapshots, `corpus/instruments/source-recheck.py`, the r23
SCORECARD frozen-claims section, QUALITY Q7–R9 and the 44 inherited seat reports
under `.ufo/waves/round-23/build/` (author-side evidence, never admission).
Discarded: the inherited implication that the C1 fix had landed. `git diff
922a4dde -- corpus/instruments/resolve.py` is empty at this attempt's start, and
every seat patch lived only in `/tmp/kasegi-r23-*` clones that no longer exist
(`ls -d /tmp/kasegi-r23-*` → 0). The FixMirror design was re-implemented here
from its own report and measured on this attempt's bytes.

### C1 — depth:verifiability (lowest axis, score 4): mirror-fallback soundness

Landed in `corpus/instruments/resolve.py`:

- `bounty_suffix()` (new): exact-root equality or a `/`-delimited descendant of
  `~/Projects/bounties` / `/home/vgpnk/Projects/bounties`. `~/Projects/bounties-x`
  is now an ordinary other root instead of a bounty citation with suffix `-x/...`.
- Bounty fallback now requires `under_mirror(p, mirror_root)`; relative mirror
  fallback likewise. Both were unchecked before; the canonical-alias branch already
  had the guard.
- Literal `exists_any(base)` RESOLVES for bounty citations is deliberately kept
  (carve-out), and the lane-relative `INTERNAL` branch is unchanged — both are
  pinned as controls in the matrix.
- Policy docstring updated in place for the BOUNTY and REL domains; no other line
  of the module moved.

**Counting command** (identical inputs both sides; the matrix SHA-256 is printed
and recorded in both receipts):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git show 922a4dd:corpus/instruments/resolve.py > .ufo/waves/round-23/c1-baseline-resolver.py
python3 corpus/instruments/mirror-containment-check.py \
  --resolver .ufo/waves/round-23/c1-baseline-resolver.py \
  --json .ufo/waves/round-23/c1-baseline.json      # do-nothing control
python3 corpus/instruments/mirror-containment-check.py \
  --json .ufo/waves/round-23/c1-fixed.json         # landed bytes
```

**Before → after** (same 13-case matrix, `matrix_sha256=5e61a33e…b5e76a9`):

| class of fixture | baseline (control) | landed |
|---|---|---|
| escape fixtures pinned GONE (6) | **0/6** GONE — all 6 credited `MIRROR-EQUIVALENT` | **6/6** GONE |
| controls pinned to their class (7) | 7/7 | **7/7** |
| whole matrix | 7/13 pass, exit 1 | **13/13 pass, exit 0** |

Escape cases: `bounty-parent-traversal`, `bounty-parent-traversal-vault`,
`relative-mirror-fallback-escape`, `bounty-fallback-symlink-escape`,
`relative-fallback-symlink-escape`, `bounty-prefix-sibling-confusion`. Controls:
confined bounty and relative fallbacks, missing target, lane-relative `../`
`INTERNAL`, literal prefix-sibling `RESOLVES`, canonical-alias `RESOLVES` and its
pre-existing escape `GONE`. The control run is the §8 do-nothing receipt: it
skips the claimed work and still scores 0/6 on the target, so the counter is not
reachable without the fix.

**No-harm guard (frozen corpus, both detectors).** `git archive 922a4dd` export,
baseline and landed resolver bytes run against that identical export:
`distinct=1589 resolves=11 mirror=0 internal=197 other=0 gone=1381
skill=39/513 corpus=192/1262 all=208/1589` in both runs; citation→class diff
`distinct base=1588 fixed=1588 added=0 dropped=0 changed=0`. **The guard is
vacuous on this host**: `mirror=0` because neither mirror candidate exists, so no
citation reaches the modified branches. It is published as vacuity, and the
matrix — not the frozen-corpus diff — is C1's evidence. The residual
lane-relative `INTERNAL` branch remains unconﬁned by design (carve-out) and is not
generalized into "the detector is sound".

Score held at **4**: instrument correctness only; no restored source, no citation
availability change.

### C2 — coverage (score 7): F06–F08 admitted

The inherited entries' `recheck:` lines pointed at a manifest that did not exist
(`corpus/source-snapshots/round-23/manifest.json` absent → exit 2). This attempt
wrote it: nineteen quote assertions over the three pinned snapshots, each with
the snapshot digest, and ran the published command three times:

```sh
for s in S018 S029 S030; do python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source $s; done
```

`S018` exit 0 (7 OK lines), `S029` exit 0 (7 OK), `S030` exit 0 (8 OK — digest
plus seven quotes). **Q7 fail-closed controls** (scratch copies of the manifest
and snapshots): flipped digest → `S018:sha256 MISMATCH`, exit 1; missing source
path → `S029:source UNAVAILABLE reason=missing`, exit 2; fabricated quote →
`S030:fabricated MISMATCH reason=quote-not-found`, exit 1.

Admission rows: `corpus/README.md` § Frontier F06→`knowledge/multiparty-vulnerability-coordination.md`
(S018), F07→`knowledge/cna-assignment-and-vulnerability-rules.md` (S030,
supersedes S022), F08→`knowledge/cra-manufacturer-reporting-duties.md` (S029,
supersedes S024). Counting commands:
`grep -cE '^\| F0[6-8] .*\| admitted \|' corpus/README.md` → **0 → 3**;
`grep -cE '^\| F0[1-8] .*\| admitted \|' corpus/README.md` → **5 → 8**.
Frozen denominator `5/8 → 8/8`; the historical lost-root denominator and score 7
are not redefined.

Score held at **7**: the r15 domain-root denominator is untouched by
public-practice entries.

### Mistakes — captured this attempt

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M6 | Inherited state presented as landed work | `git diff 922a4dde -- corpus/instruments/resolve.py` empty at attempt start; `ls -d /tmp/kasegi-r23-*` → 0; checkpoint message "unadmitted, no task resumption" | R4 (existing: a rendered wave is not execution) plus this attempt's diff | Re-implement the fix on live bytes and measure the real copied CLI; report the inherited build reports as author-side evidence only. |
| M7 | Quote is a paraphrase, not the source sentence | F08's Article 71 row said “It shall apply from 11 December 2027.”; `S029.txt:122` reads “This Regulation shall apply from 11 December 2027.” | Q3 (exact quote) enforced mechanically by the new manifest/recheck — the first recheck run would fail on the old quote | Quote corrected in the entry to the located sentence; the manifest asserts it. Caught **before** admission, by the instrument rather than by reading. |
| M8 | Quote fidelity across excerpt markup | F07's 4.1.9 row quotes rendered text while `S030.txt:165` carries `<u>Independently Fixable</u>` | Q3 + Q7 (the recheck compares captured bytes) | Manifest asserts the excerpt's literal bytes; the entry now discloses the markup difference in a Quote-fidelity note. |
| M9 | Frozen predicate wider than its fixtures | C1 `after` says "all declared mirror-escape and prefix-confusion fixtures classify GONE", while a literal-present prefix sibling is truthfully `RESOLVES` | R7 (freeze against the registered detector) plus the inherited Causal/RedBefore seats | The matrix declares the escape fixture as the *literal-absent* sibling (the actual defect) and pins the literal-present sibling as a control with its ordinary-root class; both are disclosed in the matrix `note` and this lesson. The predicate sentence is not rewritten. |
| M10 | Claim evidence structure vs guard vacuity | `mirror=0` on this host makes the frozen-corpus verdict diff structurally incapable of changing | The inherited NoHarm seat predicted it; this attempt reproduced it | Publish the vacuity next to the guard, and rest C1 on the matrix receipts. |
| M11 | Prose-vs-command drift in the entry headers | The three `recheck:` lines named a manifest that did not exist (exit 2) | Q7 (executable recheck) | Manifest minted in the same landing as the row flips; three exit-0 runs plus three failing controls recorded. |

### Gate — attempt 2 additions

Opened rows this round are S018, S029, S030 and S028 (rejected), as recorded in
the section above. Transitions verified against committed rows and logged
old→new:

| row | field | old | new |
|---|---|---|---|
| S018 | status | queued | mined |
| S018 | used-by | — | corpus/knowledge/multiparty-vulnerability-coordination.md |
| S018 | recheck | 180d | 180d (unchanged) |
| S029 | (new row) | — | mined, spec/A, supersedes S024 |
| S030 | (new row) | — | mined, spec/A, supersedes S022 |
| S022, S024 | status | queued | queued (unchanged; historical, not rewritten) |
| S028 | status | rejected | rejected (duplicate-row proposal; flip unchanged) |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
→ exit **0**, 30 registry rows, two W04 duplicate-URL warnings (S028 and S029
reuse the S006 / S024 URLs — warnings, not errors). This is the round-end required
exit-0 census, and also the opening census (the registry was untouched when it
ran).

C2 evidence ceiling: the snapshots are normalized public-document reader
excerpts, not raw HTTP bytes; the recheck proves quote-in-capture, not current
online law or FIRST/CVE/EUR-Lex freshness. Each entry's Limits section states it;
S030's "current" claim is dated (approved 2026-08-20, effective 2026-08-25).

### Wave record for attempt 2

Wave 1 is inherited (`kasegi-r23-build`, 64 seats, committed under `.ufo/waves/round-23/build/`
with registry `swarm-registry.json`); its 44 reports were re-read and are
author-side evidence. Wave 2 (`kasegi-r23-falsify`, 36 seats — 9 critic, 7
reviewer, 7 executor, 4 scout, 3 mutation-tester, 2 sentinel, 2 revenger, 1
connector, 1 scribe; attack roles 19/36) validated under the v1 policy
(`plan`/`run` exit 0, registry `.ufo/waves/round-23/falsify/swarm-registry.json`)
and was **refused at dispatch**: `Background job limit reached (100)` on every
lane. Refusal text is filed at `.ufo/waves/round-23/falsify/refusal-1.json`;
the payload is `falsify-spec.json` + `falsify/dispatch.json`-shaped output under
`/tmp`. No seat was replaced, split or shrunk.

Spot-check: independent non-author admit-and-reject review remains with the
parent's separate closure. Nothing here is an admission.

SOURCES: registry rows 27 → 30 (tier A=28, C=2; status mined 18, queued 9,
rejected 3; 18 rows carry `used-by`), derived with
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` on `git show 922a4dd:corpus/SOURCES.md`
(27) and on the working registry (30) plus a cell census of tier/status/used-by.

### Post-attack repairs — falsify wave `kasegi-r23-falsify` (36 seats)

The wave ran after the first landing and attacked the landed bytes. Every repair
below was applied before the final commit; the receipts named are the final ones.

| seat finding | defect | repair landed |
|---|---|---|
| RerunMatrix F2, SentinelChecker F3 | the checker read only `class`; the `resolved_path` column was never asserted, so a fabricated path scored 13/13 | checker now reads `resolved_path` and asserts it per class (GONE ⇒ empty; MIRROR-EQUIVALENT ⇒ inside mirror; INTERNAL ⇒ inside lane; RESOLVES ⇒ inside the case root) |
| SentinelChecker F1 (HIGH) | fixture-supplied names were joined without confinement → arbitrary host mkdir/open/symlink/unlink | `safe_path()` rejects absolute names, `..` segments and parents resolving outside the case root; symlink targets must stay inside it |
| SentinelChecker F4/F6 | timeout killed only the child; one bad case aborted the matrix | `start_new_session` + `killpg` on timeout; per-case exception containment |
| SentinelChecker F5/F7, RerunMatrix F1 | unbounded stored stdout, receipt not byte-reproducible, no checker identity | stdout capped and case-root-masked, TSV read capped, receipt records `checker_sha256`, and per case the `method` and `domain` the CLI reported and `generated_at` |
| AddHocAbsForm F1 | the matrix pinned only the tilde spelling of the bounty root | added `absolute-bounty-fallback-control` and `absolute-prefix-sibling-confusion` |
| LiteralCarveout, AnchorDebt | the literal-hit carve-out and the unconfined lane branch were invisible in the detector's own contract | `resolve.py` policy docstring rescoped: mirror credit only; literal `RESOLVES` and the lane-relative `INTERNAL` branch named as carve-outs |
| MatrixFreezeOrder F3 | no case exercised the expansion branches the fix touched | added brace/glob escape cases and a confined-brace control |
| Q2TierSupport F (primary) | **F07's "current" CNA rules were already superseded on the day it was opened**: v4.2.6 (approved 2026-10-14, effective 2026-10-20) replaces v4.2.0, and 4.2.11 changed SHOULD→MUST | new row S031 + normalized `pdftotext` snapshot `S031.txt` + 10 manifest assertions; F07 entry rewritten to 4.2.6 with no page claims (rule numbers only); README F07 sources cell → S031; S030/S022 kept as historical rows |
| HashCheck V1, S029Quotes | the 14(2)(a) assertion was non-unique (an incident-only excerpt satisfied it) | added `art14-2a-track-context` plus the 14(4)(a)/(4)(b) assertions and their entry quote rows |
| RecheckAsWritten F-RA-1 | the published `recheck:` commands only ran from the repo root | every `recheck:` line now begins `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`; receipts executed from `/tmp` |
| FrontierAdmitForm F1/F2, FrontierSources F1/F3 | admitted entries had no Coverage-map row; supersession parentheticals in the sources cells; README provenance line stopped at F01–F05 | three Coverage-map rows appended, cells narrowed to bare ids, provenance line extended |
| DenomCount D-1 | the frontier counter was column-agnostic and spacing-brittle | field-exact counter published: `awk -F'|' '$2 ~ /^ *F0[1-8] / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → 8 (F06–F08 variant → 3); `uniq -d` duplicate check → 0 |
| CnaVersionDate | inherited `build/CnaFix.md` had already found the v4.2.6 supersession on 2026-10-20 and no corpus file disclosed it | disclosed here and in the F07 entry; see M13 |

**Corrected C1 measurement (supersedes the 13-case numbers earlier in this lesson;
they stay as history).** Matrix is now 24 cases: 12 escape, 12 control.
`matrix_sha256=d05b1e0c…b809`, `resolver_sha256=690153ad…ea2d` (fixed),
`d6a3c3f1…f903` (baseline), `checker_sha256=dddd5549…6b55`. Baseline (do-nothing
control): escape **0/12 GONE**, controls 12/12, 12/24 pass, exit 1. Fixed: **24/24,
exit 0**. Every escape case is discriminated by at least one landed change, and each
was checked against baseline bytes through the same checker. Two cases exist because mutation seats proved the earlier matrix could not
see them: lane-first ordering (`relative-priority-lane-first-control`) and the
mirror-root prefix sibling (`mirror-root-prefix-sibling-escape`). The lane-relative `INTERNAL` carve-out is now pinned with its escape
visible (`path_tolerance: carve-out`, receipt line `carve-out:path-outside-internal`),
not silently tolerated. The two literal-present controls pin the `RESOLVES`
carve-out; both absolute-arm cases pin the `/home/vgpnk/...` spelling.

**Corrected C2 measurement.** Four sources now recheck exit 0 (`S018`, `S029`,
`S030`, `S031`; 7/7/8/10 assertions plus digests) — receipts
`.ufo/waves/round-23/c2-recheck-S0xx.txt`, controls `.ufo/waves/round-23/c2-controls.txt`
(digest 1, missing 2, fabricated quote 1). F07 now rests on the current rule set,
so the "current CNA operational rules" clause of C2 is true at the measured date
rather than 6 days stale.

**Residual C2 debt (F01–F05).** The five r22 entries' `recheck:` lines point at this
round's manifest, which lists S018/S029/S030/S031 only, so each exits 2
`not-listed` (reproduced). That is fail-closed, but it is not a passing recheck:
those five admissions rest on live-source reads with no capture. Naming it here is
the round's disclosure; fixing it needs fifteen snapshots, which is a later round's
work, not a round-23 claim.

### Mistakes — captured by the falsify wave

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M12 | Fixture author controls the fixture root, not the host | SentinelChecker F1 reproduced a host-file unlink from a doctored matrix | Q6-adjacent safety rule this lane lacked for its own instruments | `safe_path()` + symlink-target confinement; a doctored matrix now fails per case with `case-error:ValueError:unsafe-` |
| M13 | An inherited seat finding that never reached the corpus | `build/CnaFix.md` (mtime 2026-10-20T18:47-03) names the v4.2.6 supersession; no `corpus/` file disclosed it until now | Q2 (current-scope support) applied at admission time | F07 moved to S031; the inherited report is cited in this lesson as the finder, not as authority |
| M14 | A passing counter that cannot see a wrong answer | DenomCount D-1: `grep` matched `admitted` in any column; F02 mutated to `candidate` + note `admitted` still counted | R2 (a rate cites its derivation) | field-exact `awk` counter plus a `uniq -d` duplicate check |
| M15 | An assertion satisfiable by the wrong passage | HashCheck V1: the 24-hour phrase exists in both Article 14 tracks | Q3 (exact quote) extended to uniqueness where the words repeat | added the track-context assertion and the 14(4)(a)/(4)(b) rows |
| M16 | Receipts that cannot be re-derived byte-for-byte | RerunMatrix F1: scratch paths in `cli_stdout` made every receipt unique | R3 (an instrument verdict names its definition and replays) | root masked to `<CASE>`, checker sha and UTC timestamp recorded |
| M17 | A frozen predicate narrower than a fixture set reads | Causal/LiteralCarveout: `nature` decides which pin applies, and the frozen text never says so | R7 | matrix `note` fields and this lesson state the partition; the frozen text is untouched |
| M18 | Undisclosed capture gaps stated as facts | S018Quotes: no version banner in the capture; S029Quotes: no OJ date line; S030Quotes: page markers missing for pages 3–7 | Q3's "exact location" read literally | each gap disclosed in its entry (F06 capture-gap paragraph; F08 OJ note; F07 page claims removed) |

### Gate — supplementary rows (post-audit, `falsify/LessonGateRows.md`)

The Gate block above opened S028/S029/S030 but omitted a row for **S018** (re-opened)
and for the later **S031**, and its row/status census went stale when S031 landed.
Appended rather than rewritten (R9).

| row | URL | accessed | exact quote (≤25 words) | location |
|---|---|---|---|---|
| S018, re-opened | https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1 | 2026-10-20 | “All parties should clearly and securely communicate and negotiate expectations and timelines.” | Maintain clear and consistent communications — Prior to disclosure (`S018.txt:36`) |
| S031, supersedes S030 | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | 2026-10-25 | “Version: 4.2.6” | Title page, 4 lines above the approved date (`S031.txt:1` after the provenance header) |
| S031, supersedes S030 | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | 2026-10-25 | “CNAs MUST assign different CVE IDs to different, Independently Fixable Vulnerabilities.” | rule 4.2.11, page 15 of the PDF (`S031.txt`, normalized capture) |

Transitions this block adds, old→new: `S030 used-by` stays
`corpus/knowledge/cna-assignment-and-vulnerability-rules.md` because the entry still
cites the pinned 4.2.0 text for its version history, while `S031` is the entry's
`source:` header and current authority; `S030 teaches` is unchanged (R8 — a
superseded row is not edited). S018's per-row access date is 2026-10-20 (the round's
opening) with a re-open on 2026-10-25 that produced no new bytes.

Corrected census at the seal: **31 rows**, tier A=29 / C=2, status mined 19 /
queued 9 / rejected 3, `used-by` 19 — the earlier "30 / A=28 / mined 18 / used-by 18"
in this lesson predates S031 and is corrected here, not rewritten.

Receipts now also carry each case's `method` and `domain` from the CLI, so the
routing change the exact-root hunk makes is visible instead of inferred: the same
citation resolves `literal/bounty` on baseline bytes and `literal/other` on landed
bytes (`falsify/BaselineFalsify.md`, residual recommendation).

### Errata after `falsify/VacuityDisclosure.md` (post-seal)

- **Guard instrumentation now actually reported.** The frozen guard clause asks for
  density and anchorcheck. At the seal the final resolver bytes
  (`690153ad…ea2d`; baseline `d6a3c3f1…f903`) give:
  `python3 corpus/instruments/density.py SKILL.md --label r23` → mean dens **154.0**
  over 19 blocks, **652** path-citation instances, exit 0;
  `python3 corpus/instruments/anchorcheck.py SKILL.md` → **7 in-range / 0 bad**,
  7 distinct anchors, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0
  BASE-ABSENT=0`, exit 0. Earlier the lesson named neither instrument, so the
  guard was unfalsifiable from the filed text.
- **Definition limit (unpack-path dependence).** The frozen-corpus numerator moves
  with the export location: the same final resolver over `git archive 922a4dd`
  unpacked at `/tmp/X/a` reports `internal=197 … 208/1589`, at `/tmp/X/cur/export`
  `internal=198 … 209/1589`, because `corpus/README.md:54` cites
  `../../../.ufo/l0-questions.md` and only the shallower unpack lands on the lane's
  real `.ufo`. The guard number is therefore reported with its unpack depth, and the
  matrix — not this fraction — carries C1.
- **Duplicate citation key.** The census prints `distinct=1589` but the emitted TSV
  has 1588 unique `citation` values: `evidence-manifest/v1` appears under both the
  `SKILL` and `+CORPUS` scope labels, and the `citation→class` diff is last-wins.
  No verdict differs; the two counts measure different things and are now labelled.
- **Indexing.** Both new instruments were missing from `corpus/README.md` § Coverage
  map and from this README's instrument list; rows added.
