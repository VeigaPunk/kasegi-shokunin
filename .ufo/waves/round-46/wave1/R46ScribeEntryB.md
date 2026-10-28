VERDICT: DRAFT-READY

# R46ScribeEntryB — C2 entry drafter B (F28, GitHub private vulnerability reporting, reporter-side flow)

Scope: one draft entry, drafted from the pinned capture S073 only. Draft file (not committed, not placed in corpus/knowledge):
`.ufo/waves/round-46/wave1/R46ScribeEntryB.draft/github-private-vulnerability-reporting.md`
sha256 `cdb541501b1f0acdce4a4196db395b2ad807c112805eb45be2b81676677b5ea6`, 1419 words, four sections (`## Scope and decision rule`, `## Overlap and novelty`, `## Limits`, `## Falsifiable package rule`), decision table with 9 data rows, 12 curly-quoted spans each followed by a `(`S073.txt:N`)` citation.

C1 (gated recheck lines, claim-gates.md / claim-package-contract.md) is not my assignment; I did not read or edit those files and made no C1 change.

## Finding 1 — Source bytes and recheck (built on a freeze-commit export)

Pinned capture: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5:corpus/source-snapshots/round-46/S073.txt | sha256sum`
printed `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  -` (matches the pinned value).

Recheck run from a scratch export of the freeze commit (`git archive 9f23aab… corpus | tar -x`), i.e. the same command the entry's `recheck:` line names:
`python3 -I corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073; echo rc=$?`
printed:
```
S073:sha256 OK
S073:Q1 OK occurrences=1 anchor=560-ok
S073:Q2 OK occurrences=1 anchor=563-ok
S073:Q3 OK occurrences=1 anchor=564-ok
S073:Q4 OK occurrences=1 anchor=566-ok
S073:Q5 OK occurrences=1 anchor=573-ok
S073:Q6 OK occurrences=1 anchor=574-ok
S073:Q7 OK occurrences=1 anchor=577-ok
S073:Q8 OK occurrences=1 anchor=578-ok
rc=0
```
Pinned tool and manifest bytes at that export: `source-recheck.py` sha256 `fd2e01e8…b9c003` and `manifest.json` sha256 `01f0257261d1…f79d34` (both equal the counter's PINS).

## Finding 2 — Quote self-check (each curly span, its cited line, verified with sed)

Command per span: `sed -n 'N p' corpus/source-snapshots/round-46/S073.txt` and a check that the quoted words occur in the output (typographic apostrophe normalised). All 12 returned contains = True:

| span | cited | sed output begins with |
|---|---|---|
| Anyone can privately report a security vulnerability to repository maintainers. | 560 | same text |
| Owners and administrators of public repositories can enable private vulnerability reporting on their repositories. | 561 | same text |
| You can only report vulnerabilities privately for repositories where this feature is enabled. | 564 | "Private vulnerability reporting is separate from a repository’s SECURITY.md file. You can only report …" |
| Private vulnerability reporting is separate from a repository’s SECURITY.md file. | 564 | same line |
| you need to initiate the reporting process by following the instructions in the security policy for the repository | 566 | "If the repository doesn't have private vulnerability reporting enabled, you need to initiate …" |
| by creating an issue asking the maintainers for a preferred security contact | 566 | same line |
| By default, you must provide a summary, details, proof of concept, and impact statement. | 573 | same text |
| Maintainers can customize the form and require other information. | 573 | same line |
| Optionally, select I used AI assistance to find or write up this report. | 574 | same text |
| GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory. | 577 | "When the report is submitted, GitHub automatically adds …" |
| only the repository maintainer can merge changes from that private fork into the parent repository | 578 | "Optionally, click Start a temporary private fork … Note that only the repository maintainer can merge …" |
| The next steps depend on the action taken by the repository maintainer. | 579 | same text |

Curly quote characters in the draft: 12 opening, 12 closing, 12 spans; all paired and cited. Each span is at most 25 words (longest 20 words, minimum 9).

Required cores (all five present inside located spans): 564 "only report vulnerabilities privately … enabled"; 573 "summary, details, proof of concept, and impact statement"; 574 "I used AI assistance"; 577 "credited user on the proposed advisory"; 578 "only the repository maintainer can merge".

## Finding 3 — Frozen C2 counter on the draft (full run, scratch fixture)

Built a scratch tree at `/fast/scratch/hyaku/kasegi-r46/R46ScribeEntryB/tree` from the freeze commit, placed the draft at `corpus/knowledge/github-private-vulnerability-reporting.md`, and appended two scratch-only rows so the counter can reach the entry: one F28 row in `corpus/README.md` (after F27, entry cell `` `corpus/knowledge/github-private-vulnerability-reporting.md` ``, sources S073) and one S073 row in `corpus/SOURCES.md` (11 cells; tier A, status mined, opened 2026-10-28, anchor cell carrying the capture sha, recheck cell `180d`). These two rows are fixture stand-ins; the lane's real F28/S073 rows belong to L1 and were not written.

`python3 corpus/instruments/r46-c2-gate.py --root <tree>` printed:
```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=9 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=12 located=12 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
exit=0
```
G1, G3 and G7 pass only because of the fixture rows above. G7 first failed on my fixture (census E09 `S073 recheck=—`, the recheck cell must be the interval); I corrected the fixture cell to `180d` (matching the S071 row's form) and it then passed with `census-rc=0`.

## Finding 4 — Controls (discrimination)

Do-nothing control, run on the freeze commit with no entry and no fixture rows (`git archive 9f23aab… corpus`):
```
gate G1 pass=0 read=rows=27 admitted=27 dup=0
gate G2 pass=0 read=F28-rows=0
gate G3 pass=0 read=row-S073=absent-or-malformed
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=0 read=F28-rows=0
gate G6 pass=0 read=knowledge=64 base-names-intact=1 entry-bytes-ok=0
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=2/7 exit=1
```
Note: the frozen controls file records the do-nothing as `fixed=1/7` on the base export (where the round-46 manifest is absent, so G4 fails). On the freeze commit the manifest and capture exist, so G4 passes; this is a tree difference, not a counter change.

Mutants of the draft (each in a scratch copy, the copy deleted afterwards):
- fabricated word (`impact statement.” (S073.txt:573)` changed to `impact summary.”`): `gate G5 pass=0 read=spans=12 located=11 failed=1 uncited=0 cores=4/5`, `c2-gate fixed=6/7 exit=1`.
- uncited curly quote appended (`Stray filler: “a quoted phrase with no citation.”`): `gate G5 pass=0 read=spans=12 located=12 failed=0 uncited=1 cores=5/5`, `fixed=6/7 exit=1`.
- wrong line (merge quote cited `S073.txt:577` instead of `:578`): `gate G5 pass=0 read=spans=12 located=11 failed=1 uncited=0 cores=4/5`, `fixed=6/7 exit=1`.
- core dropped (the 577 quote replaced by an uncited paraphrase): `gate G5 pass=0 read=spans=11 located=11 failed=0 uncited=0 cores=4/5`, `fixed=6/7 exit=1`.

Harness note: my first fabricated-word mutant pattern (`impact statement” (`) did not match because a full stop sits before the closing quote; it applied no change and reported pass. I caught this (`replacement applied: False` on the first attempt), corrected the pattern (`impact statement.” (`), and the rerun printed `replacement applied: True` with G5 pass=0. Only the corrected run is reported above.

## Finding 5 — Limits sweep (what the page does not say)

Sweep, against the pinned capture (sha256 above):
`sed -n '556,583p' corpus/source-snapshots/round-46/S073.txt | grep -n -i -E 'CVE|timeline|days?|weeks?|reward|bount|payment|embargo|triage|publish|safe.harbor'` → no output, `grep_rc=1`.
`grep -n -i -E 'CVE|timeline|days|reward|bount|safe.harbor' corpus/source-snapshots/round-46/S073.txt` → no output, `grep_rc=1`.
The body's references to other articles (`grep -n -o 'See [^.]*\.'` on 556-583): "See Configuring private vulnerability reporting for a repository." (561), "See Creating a repository security advisory." (563), "See Coordinated disclosure of security vulnerabilities." (566), "See Managing privately reported security vulnerabilities." (579). The entry says the page states the content of none of them.

Conclusion recorded in the entry: maintainer-side flow, CVE requests, timelines and rewards are not stated; nothing is inferred from outside knowledge.

## Finding 6 — Overlap citations (verified lines)

- `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:23` — `sed -n '23p'` → "| Does an AI-assisted find stay private? | “If you resorted to AI assistance to identify a bug, you must treat it as public” …" (F27 AI rule; the entry paraphrases it without a curly quote).
- `corpus/knowledge/ai-assisted-finding-validation.md:8` — "For Kasegi claim-ready status, the package must identify the reproducing evidence and a reviewer distinct from its producer; …"
- `corpus/knowledge/vendor-third-party-finding-coordination.md:95` — "… file it with the national partnership (S039.txt:506). The new fact is coordinator-of-record"
- `corpus/knowledge/authorization-safe-harbor-and-scope.md:8` — "A safe-harbor badge or statement alone does not add assets to scope or establish permission for an action that the program’s policy excludes."

Novelty check: `grep -l -i -E 'collaborator|credited user|private fork|private vulnerability reporting' corpus/knowledge/*.md` (frozen base, excluding the draft) returned only `corpus/knowledge/pz-reporting-transparency-trial.md`, whose hit is the unrelated word "collaborator" (line 16, "One named collaborator joins it"). So the reporter-side gate, the automatic collaborator/credited-user status and the fork-merge authority are not recorded in any held entry.

## Judgement calls (for L1 to check)

1. The brief says GitHub "keeps an AI-assisted report PRIVATE". The page has no AI-specific handling sentence. The entry therefore says the same private reporting route is the one described (S073.txt:560-565) and AI assistance appears only as the optional checkbox (S073.txt:574), and it states the contrast with F27 without claiming either project's policy is the other's. It does not assert that GitHub keeps AI reports private as a separate rule.
2. The decision table has nine rows (the brief required at least six). Two quoted spans appear in one cell (fields row) and are both cited.
3. I added the admin/security-permission note (S073.txt:563) to Limits, since the page routes those users to a draft advisory instead of a report.

## Limitations

- Every quote check is against the pinned capture bytes (sha256 verified above), not the live page. The `recheck:` line proves the capture and its pinned quotes, not the current page.
- G1, G3 and G7 pass only with the scratch F28/S073 rows. The real rows must be written by L1; the draft does not depend on their wording beyond the entry path.
- I ran the recheck from an export of the freeze commit, not from the lane's working directory; the tool and manifest hashes match the counter's pins.
- The table rows and overlap statements are my reading of the page and of the cited corpus lines; the counter checks citation ranges and quote location, not the accuracy of paraphrases in table consequence cells.
- Read-only throughout: no commit, push, index or git mutation; the only git commands were `show`, `archive` (export to scratch) and a read-only `status` on the lane. I did not touch the fleet repo, sibling lanes, MANIFEST.json, .ufo/state, ~/Projects/shokuknow, ~/.local/bin, or any PATH directory. No tools were installed or upgraded. Subagent dispatch: none.
- Scratch root `/fast/scratch/hyaku/kasegi-r46/R46ScribeEntryB/` removed on exit (see final step).
