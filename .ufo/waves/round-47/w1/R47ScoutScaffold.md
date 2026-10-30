# R47ScoutScaffold — D5 byte census and integration map

Axes: depth:verifiability; coverage. Confidence: high for byte census and D5-only offsets.

## Observed evidence

Source command (read-only):
```sh
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8:corpus/SOURCES.md
```
Measured with Python `subprocess.check_output`, `splitlines(keepends=True)`, cumulative byte lengths, and `hashlib.sha256`: **124448 bytes; 185 LF-terminated lines; CRLF=0; sha256 e3bdefcfaad97e093a2950af37e62430635f130d9ea2d43fb1585db988077a6c**. All byte intervals below are **zero-based, half-open**, count UTF-8 bytes (not characters), and include the final LF unless marked as a phrase. All line numbers are 1-based at the named base.

## Four scaffold prose units

The four units are two title lines and two wrapped instructional paragraphs, not four physical lines.

| Unit | Base lines | Byte interval | Exact prose |
|---|---:|---:|---|
| Search-log title | 113–113 | [90508,90546) |  The `## Search log` bullet to append ⏎  |
| Search-log instruction | 115–119 | [90547,90986) | Append inside `## Search log` (today that section spans `corpus/SOURCES.md:90`–`:111`, the F28 ⏎ bullet at `:110`; `## Leads (unopened)` starts at `:112`), after the F28 bullet, separated by one ⏎ blank line. PRISMA-style, in the F28 bullet's shape. The sweep commands and their printed output ⏎ are the ones this seat re-ran itself (receipts in this draft dir); the counts were first ⏎ established by the absence-scout seat `R46bScoutAbsence`. ⏎  |
| Registry title | 177–177 | [122145,122186) |  `## Registry changes` bullets to append ⏎  |
| Registry instruction | 179–180 | [122187,122358) | Append at the end of the `## Registry changes` section (today that section starts at ⏎ `corpus/SOURCES.md:118` and the file ends at `:162`). Follow the S073 bullet's shape. ⏎  |

## Both fence pairs

| Fence | Base line | Byte interval | Bytes (Python notation) |
|---|---:|---:|---|
| Search open | 121 | [90987,90999) | `b'```markdown\n'` |
| Search close | 123 | [93503,93507) | `b'```\n'` |
| Registry open | 182 | [122359,122371) | `b'```markdown\n'` |
| Registry close | 185 | [124444,124448) | `b'```\n'` |

## Three landing bullets — complete verbatim bytes

Each block below is UTF-8, with one final LF; block delimiters are report formatting only. Leading `- ` and every embedded character are retained.

### Base L122; [90999,93503); 2504 bytes

SHA256 (including LF): `9d45acb40b2061aad660306919ca8d0f073231d81dc484d3ebf9052737e6ffdf`.

````text
- Repository security advisory lifecycle sweep (round 46 attempt 2, frontier F29); question: does the lane hold a first-party source for GitHub's maintainer-side repository security advisory lifecycle (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication, fix-version duty), and does any held row or entry already cover it; where: the committed base export (`git archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus`) swept with `grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md`, which printed 2 files and exited 0 over 65 knowledge files, the README and SOURCES — `corpus/knowledge/github-private-vulnerability-reporting.md` and `corpus/SOURCES.md` — with the same command on the live lane printing the same 2 files; `grep -ciE 'repository securit. advisor|GHSA' corpus/README.md` printed 0 and exited 1 (no frontier admission), `grep -rn 'S074' corpus/SOURCES.md corpus/README.md` printed nothing and exited 1 (no row, no admission), and the line-level `grep -rniE 'repository securit. advisor|GHSA'` gave 4 hits: the F28 entry's scope-out notes at `corpus/knowledge/github-private-vulnerability-reporting.md:40` and `:43`, the rejected S068 Advisory-Database row at `corpus/SOURCES.md:74`, and the round-43 search-log bullet at `corpus/SOURCES.md:157`; date 2026-10-29; identified 4 units, screened 4, included 1, excluded 3: the primary page https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories (included as S074 with the new entry `corpus/knowledge/github-repository-security-advisories.md`); excluded, with reason: the F28 entry's two scope-out notes (the linked page "Creating a repository security advisory" appears there only as link text in the S073 capture, `S073.txt:563`, so the maintainer-side body was never held), the rejected S068 row (an Advisory Database mirror of one NVD record, tier B, not the maintainer-side lifecycle) and the round-43 search-log bullet (a historical note naming GHSA candidates for a different question). Stop rationale: the four hits are the whole in-corpus mention of this ground and every one of them points away from it, so the sweep stopped at the opened primary page; the sibling pages it links (creating a repository security advisory, editing a repository security advisory, editing GitHub Advisory Database advisories, the REST API endpoints) stay leads, not rows, until a round opens them.
````

### Base L183; [122371,123466); 1095 bytes

SHA256 (including LF): `374d7d75291d5062b69f2bc6e1afe5cfb0faee03a66deec66b6128424d2b9ada`.

````text
- S074 row added: new row (id `S074`, kind `docs`, tier A scoped to GitHub's own statement of the maintainer-side advisory lifecycle only, status mined, opened 2026-10-29, recheck `90d`, used-by `corpus/knowledge/github-repository-security-advisories.md`), anchor pinned to the round-46-a2 capture `corpus/source-snapshots/round-46-a2/S074.txt` (sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines: heading L2, one-line purpose L3, private discuss-and-fix L10, draft advisory L12, temporary private fork L13, publish-on-patch L14, credit L17, CNA L24, CVE request and 72-hour review L25, other-CNA boundary L26, publication visibility L30-L31, URL stability L33, Dependabot alerts L35-L36, fix-version duty L37-L38). Rule-1 Gate quote grounding `teaches` (11 words): "Requesting a CVE identification number doesn't make your security advisory public." (S074.txt:25). Access 2026-10-29 (manifest `fetched_utc` 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL). Registry rows 73 → 74 (R8); no pre-existing row status, recheck or used-by cell changed.
````

### Base L184; [123466,124444); 978 bytes

SHA256 (including LF): `94c88984da5448fd3d95621fefd58cf32b181d8245984694d0e9245ceaf6d198`.

````text
- Capture directory note: `corpus/source-snapshots/round-46-a2/` exists beside `corpus/source-snapshots/round-46/` because the attempt-1 round-46 manifest is sha-pinned by the round-46 attempt-1 receipts (`01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`, recorded at `.ufo/waves/round-46/freeze.txt:7` and `.ufo/waves/round-46/wave1/R46SentinelContent.md:13`) and therefore must stay byte-identical; the attempt-1 manifest hashes to that digest at base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`, at HEAD and in the worktree, while the new attempt-2 manifest `corpus/source-snapshots/round-46-a2/manifest.json` hashes to `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f` (pinned as `manifest-a2-sha256` in `.ufo/waves/round-46/attempt2/freeze.txt:7`). `git diff --name-status 04af9bc92229232ea5cce8b32bfe59dd969eb26d HEAD -- corpus/source-snapshots/` prints only the two `A` additions under `round-46-a2/`, so no attempt-1 capture byte moved.
````

## Section anchors at base

| Heading | Line | Byte interval | D5-only resulting line |
|---|---:|---:|---:|
| `## Search log` | 91 | [69321,69335) | 91 |
| `## Leads (unopened)` | 125 | [93508,93528) | 115 |
| `## Registry changes` | 131 | [94108,94128) | 121 |

## Precise integration edit map (D5 only)

Delete the following **original-base** line ranges; do not treat these as progressively renumbered coordinates. If using a sequential text editor, apply bottom-up.

| Delete base lines | Delete byte interval | Bytes removed |
|---:|---:|---:|
| 113–121 | [90508,90999) | 491 |
| 123–123 | [93503,93507) | 4 |
| 177–182 | [122145,122371) | 226 |
| 185–185 | [124444,124448) | 4 |

**Insertion/move semantics:** No payload insertion or copying is necessary: the three bullets are already physically at the intended section ends. Unwrap in place. Base L122 becomes ordinary Search-log content at D5-only L113, immediately after F28 L111 with exactly one blank L112 between. Preserve base blank L124 (new L114), then `## Leads (unopened)` at new L115. Base L183 and L184 become ordinary Registry-changes content at new L167 and L168, after the S073 row and supersede-pair note (base L174/L175 → new L164/L165), separated from that preceding group by the single existing blank base L176 → new L166. The two Registry bullets remain adjacent, with **no blank between them**. EOF is the single LF terminating the Capture-directory bullet; do not retain the closing-fence line or add a trailing empty line. Preserve every other base byte.

This removes **725 bytes / 17 lines**, with **zero payload additions**. In-memory D5-only result: **123723 bytes / 168 lines**, sha256 **3eb1daa507a037950520317b0248108d7265db3634f850d40253b390223e3e20**. This is an edit-map calculation, not an integrated-file or counter pass. Concurrent D7/D8/F30 edits invalidate this whole-result digest and subsequent line offsets.

## Line-anchored citations outside lessons

Literal search: functions.grep `SOURCES\.md:` over lane `corpus` and `SKILL.md`; inspected non-lesson hits. The LSP device lookup `read xd://lsp` returned **No such tool**; no semantic server is mounted. These findings are literal-text evidence, not semantic-reference proof.

- `SKILL.md:1079` cites `corpus/SOURCES.md:55-56` for S049/S050: before the deletions, therefore **not shifted by D5**. (Later registry additions may affect it separately.)
- `corpus/SOURCES.md:115` and `:180` contain scaffold-local positional citations; they are deleted with their instructions.
- The retained F29 bullet at base `corpus/SOURCES.md:122` cites the **committed-base export** S068 row `corpus/SOURCES.md:74` and round-43 bullet `corpus/SOURCES.md:157`. Its own location changes 122→113; a current-tree target at base L157 would move to L147 under D5 alone. **Do not mechanically rewrite the embedded `:157` historical-export citation to `:147`: it is attached to export `04af9bc92229232ea5cce8b32bfe59dd969eb26d`, not this edit's resulting tree.** S068 L74 is before the deletion region and remains L74 under D5 alone.
- No other non-lesson `SOURCES.md:` literal was found in the requested corpus/SKILL scope. Lesson/history references are excluded by assignment and were not repaired or certified. Broader non-corpus files were not searched.

## Do-nothing control and limits

Named control: **unchanged base SOURCES.md at fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8**. It retains all four prose units, four fence lines, and three fenced bullets. The proposed map differs by the exact 725 deleted bytes above; merely appending duplicate bullets leaves the scaffold in place and is not this repair. No r47 counter, full battery, build, or test was run. The supplied overall C1 control `total=11 fixed=0 unresolved=11 exit=1` is assignment evidence only, not a measurement by this seat. The disclosed 34 mutation survivors remain unresolved; this census claims no counter equivalence or survivor closure.

No production files, git/index state, tools, or installations were changed. No scratch directory/fixture was created, so no scratch remains to remove. Only this report was written.

Report: .ufo/waves/round-47/w1/R47ScoutScaffold.md
