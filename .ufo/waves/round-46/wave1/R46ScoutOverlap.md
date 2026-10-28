# R46ScoutOverlap — overlap scan: corpus vs F28 (GitHub private vulnerability reporting, S073)

VERDICT: INFO

Scope: read-only. No file outside `.ufo/waves/round-46/wave1/R46ScoutOverlap.md` and
`/fast/scratch/hyaku/kasegi-r46/R46ScoutOverlap/` was written; no git/jj mutation anywhere.
All paths below are relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## 1. The overlap grep (evidence)

Commands (discovery ran through the lane grep tool; the per-file counts are a counting
pipeline run from the lane root, same convention the knowledge entries use for FC checks):

```
grep -rnE 'GitHub|advisor|SECURITY\.md|GHSA|Report a vulnerability' corpus/knowledge --include='*.md'
# then per pattern P in {GitHub, advisor, SECURITY\.md, GHSA, Report a vulnerability}:
grep -rnE "$P" corpus/knowledge --include='*.md' | wc -l
grep -rcE "$P" corpus/knowledge --include='*.md' | grep -v ':0$'
```

Output (counting pipeline, verbatim):

```
== pattern GitHub
match-lines total: 3
corpus/knowledge/source-tree-loss-2026-09-28.md:2
corpus/knowledge/ufo-workspaces.md:1
== pattern advisor
match-lines total: 19
corpus/knowledge/operator-queue.md:1
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:1
corpus/knowledge/iso-29147-and-30111-division-of-labour.md:3
corpus/knowledge/csaf-vex-product-status-and-justifications.md:2
corpus/knowledge/nist-sp800-216-vdp-framework.md:1
corpus/knowledge/cisa-cvd-program-stages.md:9
corpus/knowledge/rfc-9116-security-txt.md:1
corpus/knowledge/claim-package-gate.md:1
== pattern SECURITY\.md
match-lines total: 0
NO-FILE-WITH-MATCHES
== pattern GHSA
match-lines total: 0
NO-FILE-WITH-MATCHES
== pattern Report a vulnerability
match-lines total: 0
NO-FILE-WITH-MATCHES
== files in corpus/knowledge: 64
== github-private-vulnerability-reporting.md exists: no
```

Controls: the empty results are not a vacuous pipeline — `advisor` (19 lines) and `GitHub`
(3 lines) do hit, proving the matcher runs. A case-insensitive `(?i)advisor` rerun added one
file, `corpus/knowledge/submitted-registry.md:130` ("Advisory upstream fix"), still generic
CVD usage, still nothing GitHub-hosted.

## 2. What the corpus ALREADY holds about GitHub-hosted reporting

Everything the five patterns surface is fleet-operational or generic-CVD, none of it about
GitHub as a vulnerability-reporting surface:

- `corpus/knowledge/source-tree-loss-2026-09-28.md:55` — "the surviving GitHub mirror is code-only" (incident forensics).
- `corpus/knowledge/source-tree-loss-2026-09-28.md:254` — "The local repo is therefore the **origin** of the GitHub remote, not a clone" (fleet ops).
- `corpus/knowledge/ufo-workspaces.md:108` — "honest stops M2 GitHub-CLI overfit" (run history).
- `corpus/SOURCES.md:71` — S065 (OSV schema, tier A, **rejected**): GitHub appears only as the `ossf.github.io` URL host; rejected on the disjointness tie-break (sibling kaidoku lane holds an OSV record instance), not on reporting content.
- `corpus/SOURCES.md:73` — S067 (curl CVE-2025-9086 advisory, tier A, mined → `corpus/knowledge/claim-package-gate.md`): vendor's own advisory, no GitHub surface; grounds the claim-package exemplar, not reporting flow.
- `corpus/SOURCES.md:74` — S068 (GitHub Advisory Database GHSA-v676-f8gm-92r9, tier B, **REJECTED**): the only GitHub-hosted object row in the registry. Rejection grounds: it "republishes the National Vulnerability Database record", is "self-labelled Unreviewed at L64 and L68, with no package listed (L75), affected and patched versions both Unknown (L78, L80) and no known source code (L170)"; flip condition: re-open "only if the entry becomes Reviewed and names an affected package with per-version affected and patched ranges".

Nothing in `corpus/knowledge/` describes: the private-report form, repository security
advisories, SECURITY.md, draft advisories, or the Security tab. The nearest held
reporting-channel objects are e-mail-only intake (kernel) and `.well-known/security.txt`
(`corpus/knowledge/rfc-9116-security-txt.md`) — SECURITY.md itself is unheld (0 hits).

## 3. The five assigned entries vs S073 (per-entry relationship)

1. `corpus/knowledge/ai-assisted-finding-validation.md` (F04; S009-S012): AI finding stays a candidate until reproduction + a reviewer distinct from the producer are recorded. S073's Q6 ("Optionally, select I used AI assistance to find or write up this report.") is a platform-recorded self-declaration at submission. Different layers — admission control vs form field — no conflict.
2. `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (F27; S071): one project's e-mail-only intake ("Reports are to be sent over e-mail exclusively", `S071.txt:257`), AI-assisted finds "must treat it as public" (`S071.txt:95-96`). Project-scoped by its own scope rule ("not a rule for distributions, for other projects"). GitHub's flow is a web form into a private advisory with an optional AI flag — a different project's intake class, which the entry's scope rule already isolates.
3. `corpus/knowledge/vendor-third-party-finding-coordination.md` (F15; S048 MSVR): a vendor programme as intake route for other vendors' bugs; coordinator seat recorded, no channel/clock (`grep -ciE '90[ -]day|deadline|embargo|timeline' S048.txt → 0`, FC-3). S073 adds the platform-mediator variant: reporter → maintainers with automatic credit/collaborator (Q7) and maintainer-only merge from a temporary private fork (Q8). Complementary.
4. `corpus/knowledge/authorization-safe-harbor-and-scope.md` (S006-S008): "Adopting a Safe Harbor does not change the program scopes" / platform indicator ≠ permission. S073's Q3 precondition ("You can only report vulnerabilities privately for repositories where this feature is enabled.") and Q4 fallback (follow the repository's security policy when not enabled) are the same shape of boundary on GitHub's side — supportive, not contradictory.
5. `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (F13; S043-S045): platform taxonomies (HackerOne/Bugcrowd) are platform statements, not universal. S073's body names no severity ladder; the form demands summary/details/PoC/impact (Q5) and lets maintainers customize. Consistent with F13's boundary.

## 4. Does anything already held CONTRADICT the S073 page?

No contradiction found. Two tensions worth recording, both already resolved by held scoping rules:

- **Kernel AI rule vs GitHub AI checkbox.** F27/S071: an AI-assisted kernel find is treated as public, no embargo; S073: a private form with an optional AI-assistance flag. No transplants: F27's own scope rule forbids reading kernel rules onto other projects, and F04 governs validation, not channel choice.
- **S068's rejection vs S073.** S068 rejected a GitHub *Advisory Database entry* as a data source (derived NVD mirror, incomplete record). S073 is GitHub's *first-party documentation of its private reporting flow* — a different artifact class from a database entry, and S073's own text separates the two ("Private vulnerability reporting is separate from a repository's SECURITY.md file"; admins "create a draft security advisory directly" instead of reporting). Nothing held conflicts with the S073 page's statements.

Positive verification of the target itself (so the entry is groundable):

```
sha256sum corpus/source-snapshots/round-46/S073.txt
→ 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  corpus/source-snapshots/round-46/S073.txt
```

matches `corpus/source-snapshots/round-46/manifest.json` (`"sha256": "66c96a61..."`, 589 lines). All eight manifest quotes (Q1-Q8) occur **exactly once** in the capture (`grep -cF` per quote → `count=1` each, quoted in full in my yield/report transcript); `SECURITY.md` occurs 1 time and `Report a vulnerability` 1 time in S073.txt, so F28 can pin both terms to capture lines (manifest anchors 560-578).

## 5. What F28 adds (the gap S073 fills)

- A new corpus-object class: **platform-mediated reporter-side private intake** (web form → draft repository advisory), versus held intake classes: e-mail list (kernel, S071), vendor programme routes (MSVR, S048), platform policy records (HackerOne, S043), coordinator pipelines (CISA, S023), `security.txt` (RFC 9116).
- First SECURITY.md contact: `SECURITY.md` count in knowledge is 0; S073 states private reporting "is separate from a repository's SECURITY.md file" and displays the security policy above the form — the entry can relate SECURITY.md (repo policy file) to the already-held security.txt standard without conflating them.
- First platform-recorded AI-assistance disclosure flag (Q6), adjacent to F04 (validation duties) and F27 (kernel's AI-as-public rule) — neither holds a submission-form AI flag.
- Feature-enablement as a scope boundary for the reporter (Q3) and the policy-first fallback (Q4), instantiating the authorization entry's indicator-vs-permission rule.
- Automatic reporter credit/collaborator on the proposed advisory (Q7) and maintainer-only merge from the temporary private fork (Q8) — no held entry records platform-managed credit or fork mechanics.
- Registry delta: `grep S073 corpus/SOURCES.md` → no matches (verified this round); the S073 row does not exist yet and lands with F28. `corpus/knowledge/github-private-vulnerability-reporting.md` does not exist (verified; see §1 output).

## 6. Limitations

- The grep tool renders long lines truncated; exact counts therefore come from a `grep -c` counting pipeline (discovery itself used the lane grep tool). Counts are match-lines, not occurrences.
- `advisor` was run case-sensitive as assigned (19 lines); a case-insensitive rerun (added `submitted-registry.md:130`) confirmed no GitHub advisory-object usage hides behind capitalization.
- I grepped `corpus/knowledge/*.md` and `corpus/SOURCES.md` per assignment; I did not sweep SKILL.md/README.md/lessons, so "already holds" is scoped to the knowledge corpus plus the registry rows named.
- The S073 page's GitHub-Docs navigation chrome (Advisory database, Create/Publish repository advisory links) is nav, not body claims; per lane precedent (FC-4 in vendor-third-party-finding-coordination.md), F28 must not cite chrome as page content. Its body sits at roughly lines 552-589 of the capture.
- Contradiction check is documentation-only against pinned bytes; no live fetch, no probing, no submission, no counter or control instrument was executed (C1/C2 falsification is not this seat's item).
