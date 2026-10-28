VERDICT: DRAFT-READY

Scope: C2 entry drafter C (independent). Built the F28 knowledge entry draft only. C1 re-grounds are not in this seat's item and were not touched. No shared production file, no git mutation, no commit.

Artifact: .ufo/waves/round-46/wave1/R46ScribeEntryC.draft/github-private-vulnerability-reporting.md
sha256: ebadd9c5b76e67726980b4a80bd569f8994775314c9ef7d4a1c46f4617fc7f7f (9853 bytes, 52 lines)

## Finding 1: entry shape and provenance (G2 pass)

Attacked: the draft's header trio, the four sections, the table, and the cross-references.
Command run (in scratch tree copy, see Finding 3): `TMPDIR=$S python3 corpus/instruments/r46-c2-gate.py --root $T`
Output: `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=9 xrefs=6/6`

Header lines 1-5 are: `# GitHub private vulnerability reporting: the reporter flow`, blank, `source: S073 — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately — section anchors: ...`, `verified-at: 2026-10-28`, `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d`.

Table: 9 data rows with three cells each (observed question | GitHub text | package consequence); the header and separator are excluded by the gate's count.

Cross-references (`corpus/knowledge/<file>.md:N`), each re-read with sed -n:
- `linux-kernel-security-bugs-reporting-process.md:44` printed `2. The AI-assisted-report handling. The page treats an AI-assisted find as public, ...`
- `linux-kernel-security-bugs-reporting-process.md:23` printed `| Does an AI-assisted find stay private? | “If you resorted to AI assistance ...`
- `ai-assisted-finding-validation.md:8` printed `For Kasegi claim-ready status, the package must identify the reproducing evidence and a reviewer distinct from ...`
- `vendor-third-party-finding-coordination.md:95` printed `   file it with the national partnership (S039.txt:506). The new fact is coordinator-of-record`
- `authorization-safe-harbor-and-scope.md:8` printed `A safe-harbor badge or statement alone does not add assets to scope or establish permission for an action that ...`
- `authorization-safe-harbor-and-scope.md:9` printed `A reviewer can check this rule against the program’s policy text: every claimed asset and action must be sup...`

## Finding 2: quote location (G5 pass; every curly quote located and cited)

Attacked: all 16 curly-quoted spans in the draft, each followed by a `(`S073.txt:N[-M]`)` citation.
Command run: same gate run as Finding 1.
Output: `gate G5 pass=1 read=spans=16 located=16 failed=0 uncited=0 cores=5/5`

Per-span location, run as a Python normalised-substring check against the pinned capture (quotes ≤25 words, all located). Each cited line was also printed with `sed -n 'Np'`:
- S073:564 "You can only report vulnerabilities privately for repositories where this feature is enabled." (13 words) — sed printed `Private vulnerability reporting is separate from a repository’s SECURITY.md file. You can only report vulner...`
- S073:564 "Private vulnerability reporting is separate from a repository’s SECURITY.md file." (10 words; curly apostrophe kept inside the span, normalised by the gate)
- S073:561 "Owners and administrators of public repositories can enable private vulnerability reporting on their repositories." (14 words)
- S073:560 "Anyone can privately report a security vulnerability to repository maintainers." (10 words) — sed printed exactly that line.
- S073:573 "By default, you must provide a summary, details, proof of concept, and impact statement." (14 words)
- S073:573 "Maintainers can customize the form and require other information." (9 words)
- S073:574 "Optionally, select I used AI assistance to find or write up this report." (13 words)
- S073:577 "GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory." (20 words)
- S073:578 "only the repository maintainer can merge changes from that private fork into the parent repository" (15 words)
- S073:579 "The next steps depend on the action taken by the repository maintainer." (12 words)
- S073:566 "creating an issue asking the maintainers for a preferred security contact" (11 words; cited twice)
- S073:565 "anyone can submit a private vulnerability report to the repository maintainers" (11 words)
- S073:574 "Optionally, select I used AI assistance to find or write up this report." (13 words; second use in Overlap)
- S073:573 "to reproduce and assess" (4 words)
- S073:579 "Managing privately reported security vulnerabilities" (5 words)

Five frozen cores (regexes in r46-c2-gate.py CORES) each appear inside a located span: enabled-only (564), summary/details/PoC/impact (573), I used AI assistance (574), credited user on the proposed advisory (577), only the repository maintainer can merge (578). Each is inside a line cited in the draft.

Draft has zero straight double quotes; 16 opening and 16 closing curly double quotes.

## Finding 3: falsification of the gate on the draft (controls)

Scratch tree: copy of the pure base export plus the pinned S073.txt and manifest.json (copied read-only from the working tree), the draft as corpus/knowledge/github-private-vulnerability-reporting.md, and a scratch-only F28 row appended to corpus/README.md after F27. No file in the fleet or lane was modified.

Do-nothing control (base tree, no entry, no F28 row):
`gate G2 pass=0 read=F28-rows=0`, `gate G5 pass=0 read=F28-rows=0`, `c2-gate fixed=2/7 exit=1`. The entry gates fail when the entry is absent, as they should.

Mutation control 1 (scratch copy only): changed the quoted `impact statement` to `impact report` in the 573 span.
`gate G5 pass=0 read=spans=15 located=14 failed=1 uncited=0 cores=4/5`. The located-quote limb catches a one-word change in a cited quote, and the cores limb catches the lost core.

Mutation control 2 (scratch copy only): moved the citation of the SECURITY.md quote from 564 to 565.
`gate G5 pass=0 read=spans=15 located=14 failed=1 uncited=0 cores=5/5`. A citation pointing at the wrong line fails the located check.

Restored draft in scratch: `gate G5 pass=1 read=spans=15 located=15 failed=0 uncited=0 cores=5/5` (run before the F04 "to reproduce and assess" quote was changed from straight to curly quotes, which added the 16th span).

Final draft in scratch: full gate output
- `gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md` (only with the scratch F28 row)
- `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=9 xrefs=6/6`
- `gate G3 pass=0 read=row-S073=absent-or-malformed` (expected; no SOURCES.md row in the scratch tree)
- `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`
- `gate G5 pass=1 read=spans=16 located=16 failed=0 uncited=0 cores=5/5`
- `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1`
- `gate G7 pass=1 read=census-rc=0 ok-line=1`
- `c2-gate fixed=6/7 exit=1`

## Finding 4: the Limits sweep (command and printed output)

`sed -n '556,583p' corpus/source-snapshots/round-46/S073.txt | grep -n -i -E 'CVE|timeline|days|weeks|reward|bount|embargo|payout'` printed nothing (exit 1).
`grep -n -i -E 'CVE|timeline|reward|bount|payout|embargo' corpus/source-snapshots/round-46/S073.txt` printed nothing (exit 1) over the whole 589-line capture.
Credit and maintainer wording, `sed -n '556,583p' ... | grep -n -i -E 'credit|maintainer'`, printed lines 2, 5, 9, 10, 11, 18, 20, 22, 23, 24 (relative; body line = relative + 555). The credit hits are 575 (pending credit) and 577 (credited user). The maintainer hits are the merge rule (578), the next steps (579), and the form customization (573).
Review and validation wording, `sed -n '556,583p' ... | grep -n -i -E 'review|valid|reproduc|verif|assess'`, printed lines 564, 570, 573. The review wording is the reporter's own review of the policy; the only validation-like phrase is "reproduce and assess" at 573, which the draft quotes as the maintainers' need, not as a validation requirement.

The draft's Limits section records that the page states no maintainer-side flow, CVE request, timeline or reward, and cites this sweep.

## Finding 5: integration items for the L1 (not done by this seat)

- corpus/README.md needs an F28 row (the gate's G1 requires exactly one). The row used in scratch, suggested for the integrator: `| F28 | GitHub private vulnerability reporting, the reporter-side flow | admitted | `corpus/knowledge/github-private-vulnerability-reporting.md` | S073 | Keep the reporter flow distinct from the maintainer-side flow and from SECURITY.md; re-open the page before relying on it. |`
- corpus/SOURCES.md needs the S073 registry row (11 cells, tier A, status mined, opened 2026-10-28, used-by containing the entry path, anchor cell with sha256 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930). G3 is therefore not met by this draft and is not claimed here.
- The entry's line citations into corpus/knowledge (:23, :44, :8, :95, :8, :9) were verified against the working tree as of this run; if the L1 edits those files, the cites shift and need re-running.
- The S073 capture file was verified by the gate's G4 (sha256 pinned; recheck rc=0, 8 quotes OK).

## Limitations

- No live check of docs.github.com. The recheck verifies captured bytes and manifest quotes only; the entry says so.
- The page does not say which repositories have the feature enabled, and the form fields are defaults a maintainer may change. No repository was probed; no live target was tested.
- The "Coordinated disclosure of security vulnerabilities" link (S073.txt:566) is a pointer with no captured content; the entry does not rely on it.
- The overlap claims about F27 are contrast only; the entry states that neither project's policy is recorded as the other's.
- Gate G3 and the F28 README row are integration work; this seat did not edit the README or SOURCES.md.
- Scratch was used for the gate runs; it is removed on exit.
- Installs: none. No tool was installed or updated for this seat.
