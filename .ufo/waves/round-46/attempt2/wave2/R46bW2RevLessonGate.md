# R46bW2RevLessonGate — attack on the attempt-2 Gate block of corpus/lessons/round-46.md

Seat item: every ≤25-word quote in the lesson's attempt-2 `## Gate — frontier, source, and rejection (attempt 2)` block must sit on its manifest anchor line in `corpus/source-snapshots/round-46-a2/manifest.json` and in `corpus/source-snapshots/round-46-a2/S074.txt` (`sed -n 'Np'`); every reject/flip entry must carry reason + flip condition; the admit must cite S074 with the pinned sha.

Target text: the attempt-2 Gate block landed AFTER the freeze commit — `git show fe0f56b:corpus/lessons/round-46.md | grep -c 'Attempt 2'` → `0`; it exists at HEAD `96379ae26ef9443097b860ddb33ef924b2cd5b5a` (lesson file modified 23m ago). Checked against the HEAD working tree, per the item's "if landed". The snapshot and manifest are byte-identical between freeze and HEAD: `git diff fe0f56b HEAD -- corpus/source-snapshots/round-46-a2/ | wc -l` → `0`; shas identical at both revs.

VERDICT: HOLDS

## Finding 1 — Gate quotes Q1–Q9 all sit on their manifest anchor lines, ≤25 words, exact lesson↔manifest match

Artifact attacked: lesson lines 115–127 (Q1–Q9) vs `corpus/source-snapshots/round-46-a2/manifest.json` quotes[] vs `S074.txt` anchor lines.

Commands and quoted output:

- `sha256sum corpus/source-snapshots/round-46-a2/S074.txt corpus/source-snapshots/round-46-a2/manifest.json`:
  `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039  S074.txt` and `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f  manifest.json` — both match the lesson's cited shas. `wc -lc S074.txt` → `42 7087`, matching the lesson's "42 lines, 7087 bytes".
- Per-anchor extraction, `sed -n 'Np' S074.txt` for N in 10 13 17 24 25 26 31 38 — each printed line contains its quote as an exact substring:
  - L10: `Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, …` ⊇ Q1
  - L13: `Privately collaborate to fix the vulnerability in a temporary private fork.` == Q2
  - L17: `You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.` ⊇ Q3
  - L24: `GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, …` ⊇ Q4
  - L25: `… GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. …` ⊇ Q5 and Q6
  - L26: `… GitHub cannot assign CVEs to your project if it is covered by another CNA.` ⊇ Q7
  - L31: `Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.` == Q8
  - L38: `Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. …` ⊇ Q9 (Q9 quoted from mid-sentence, exact substring, lowercase start preserved)
- Exact-match + word-count harness (python3, lesson text regex `Q\d "([^"]+)"` vs manifest `quote` fields, substring test against `S074.txt` lines):
  `Q1 anchor=10 words=19 in_src=True lesson_exact_match=True`, `Q2 … words=11 …`, `Q3 … words=12 …`, `Q4 … words=15 …`, `Q5 … words=8 …`, `Q6 … words=11 …`, `Q7 … words=14 …`, `Q8 anchor=31 words=22 …`, `Q9 anchor=38 words=15 …` — all nine exact, all ≤25 words (max 22, Q8).
- Independent instrument re-run (the lesson's own verification claim), `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074; echo exit=$?`:
  `S074:sha256 OK`, `S074:Q1 OK occurrences=1 anchor=10-ok` … `S074:Q9 OK occurrences=1 anchor=38-ok`, `recheck exit=0`. Every quote is unique in the capture (occurrences=1), so anchors are unambiguous.

## Finding 2 — Reject/flip entries each carry reason + flip condition

Artifact attacked: lesson lines 129–137 ("Rejected, with reason and flip").

- Entry (1) GitHub Advisory Database as F29 source — reason quoted: "the database row class was already screened and rejected in round 43 (S068, tier B REJECTED: it republishes NVD's record; record-completeness defect), and the database is the publication target of F29, not the lifecycle's first-party statement"; flip quoted: "a first-party GitHub statement of the database's own editing flow (a page the S074 capture names but does not hold) would be a new row." — reason + flip present.
- Entry (2) repository-advisories REST API page — reason quoted: "the S074 capture names it as a pointer only (S074.txt:16)"; evidence verified: `sed -n '16p' S074.txt` → `You can also use the REST API to create, list, and update repository security advisories. For more information, see REST API endpoints for repository security advisories.` Flip quoted: "opened + located quotes in a later round." — reason + flip present.
- Entry (3) prior-attempt ZDI lead — quoted: "The prior-attempt ZDI lead stays a lead (round-46 attempt-1 flip condition unchanged)." The reason and flip are carried by reference; the referenced attempt-1 Gate block (same file, line 25) supplies both, quoted: "The ZDI policy as a round-46 row — screened, not written as a row (a lead is not a row; CORPUS rule 1): its 120-day deadline, 30/90-day patch-regression windows and "sole discretion" extension … overlap F02's timelines and the page names no start event for the 120 days; flip: a later round whose claim is the ZDI deadline rule, opened and cited by that round." — compliant, though the dependence on the attempt-1 block is by reference rather than restated (see limitations).

## Finding 3 — Admit cites S074 with the pinned sha

Artifact attacked: lesson lines 100–110 (Admitted paragraph).

- Quoted: "source S074 (tier A, kind docs, scope: GitHub's own statement of the maintainer-side flow only; the reporter-side flow stays F28; advisory editing, the REST API and the Advisory Database edit flow are out). URL `https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories` … capture `corpus/source-snapshots/round-46-a2/S074.txt` (42 lines, 7087 bytes, sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, manifest `corpus/source-snapshots/round-46-a2/manifest.json` sha256 `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`)".
- `sha256sum` output (Finding 1) reproduces both shas exactly; line/byte counts match `wc -lc`. The manifest `url`/`capture_url`/`final_url` are identical and `http.status` 200 with `fetched_utc 2026-10-29T20:19:30Z`, matching the lesson's "access 2026-10-29T20:19:30Z, HTTP 200". Pinned-sha citation HOLDS.

## Discrimination against a do-nothing control

The lesson asserts its quotes are "verified at their manifest anchors"; this seat re-derived every link in the chain instead of trusting that assertion (sha256 of both files, per-line `sed` extraction at all eight anchor lines, exact lesson↔manifest string comparison, word counts, and an independent `source-recheck.py` run printing nine `OK` lines and exit 0). A do-nothing read of the lesson text would find no defect because the text is accurate; no fabricated quote, wrong anchor, or word-count breach was present to catch. The check set named by the seat item is fully exercised; nothing is asserted from plausibility.

## Limitations

1. Entry (3)'s reason/flip is by reference to the attempt-1 Gate block (same file, line 25). Compliant as written — the reference is explicit and resolves — but a reader auditing only the attempt-2 section must follow the pointer. Not scored as a defect.
2. The live S074 page was not re-opened: the seat item names only the manifest/S074.txt anchors, and live-target testing is out of bounds for this seat. Spot-check slot (1) in the lesson reserves that for the non-author closure.
3. The F29 knowledge entry's own 45 located quotes (cited in the admit as `f29-gate H5 spans=45 located=45`) are peer seats' scope (entry-attack seats); not re-verified here beyond the Gate block's claims about them.
4. Cosmetic, non-blocking: anchor citations in the quote list format Q1 as `(S074.txt:10)` and Q2 as `` (`S074.txt:13`) `` — a backtick inconsistency only.
5. All checks run against the HEAD working tree; S074.txt and manifest.json are byte-identical between the freeze commit fe0f56b and HEAD (verified), so the freeze-vs-tip distinction does not affect Findings 1–3.
