VERDICT: DRAFT-READY

# R46bScoutAdjacent — sibling-overlap sweep for F29 (repository security advisories, maintainer-side lifecycle) + F28 maintainer-side screen

Seat: read-only scout. Sweep date 2026-10-29. No file outside this Report and no scratch dir was created; nothing to remove; no tools installed (none needed).

Pattern swept, exactly the task's regex, case-insensitive, over every corpus under `/home/vgpnk/Projects/shokunin/*/corpus` and over all of `/home/vgpnk/Projects/shokuknow` (read-only):

```
repository securit. advisor|GHSA|draft.{0,20}advisory
```

Instrument note: this is a prose corpus, so the LSP device has no server to answer; located-line text search is the correct and sufficient instrument here, and every hit was opened and read, not just counted.

## 1. Denominator — what was walked

Glob of `/home/vgpnk/Projects/shokunin/*/corpus` printed 21 corpus dirs: tameshi, mado, kengaku, tsukuroi, kotoba, revenger, tabi, chousa, kake, kasegi, kama, kumitate, souji, kagi, mori, kotodama, kaidoku, audio, game-dev-2d, lore, game-dev-3d. All 20 sibling corpora plus kasegi's own corpus (baseline control) were swept. `/home/vgpnk/Projects/shokuknow` (top level: `MANIFEST.json`, `README.md`, `RUNBOOK.md`, `doctrine/`, `lanes/`, `merge/`, `tabi-shokunin/`) was swept whole.

## 2. Per-corpus rulings (each hit located; zeros are tool output, not inference)

Zero hits — ruled **absent** (command form: the pattern above over the named corpora; output quoted verbatim):

- chousa, kagi, kake, kengaku → `No matches found`
- kumitate, kotoba, kotodama → `No matches found`
- lore, mado → `No matches found`
- tameshi, tsukuroi, revenger, kama → `No matches found`
- audio, game-dev-2d, game-dev-3d → `No matches found`

Hit corpora — four, each ruled:

1. **tabi — adjacent (navigation chrome only), ground absent.**
   `tabi-shokunin/corpus/evidence/round-31/decision-table/bytes/S121.html:32` matches only the GitHub Docs sidebar: `href="/en/rest/security-advisories/repository-advisories"...>Repository security advisories</span>`; same nav string at `S121.html:151`, `S122.html:32`, `S122.html:105` (JSON nav tree). The sources themselves are rate-limit pages: `tabi-shokunin/corpus/SOURCES.md:135` scopes S121 as "GitHub's own published REST API primary and secondary rate-limit ceilings … documentation only, not a measured response and no API calls", `:136` scopes S122 as pacing/back-off guidance. The entry consuming them (`corpus/knowledge/rate-signal-decision-table.md`, rows D6–D13) cites only rate/pacing numbers. No advisory-lifecycle ground.

2. **souji — regex false positive, no advisory ground.**
   `souji-shokunin/corpus/lessons/round-16.md:66`: "Verdict drafts are advisory and await the non-author closure." — `draft.{0,20}advisory` matched the phrase "drafts are advisory" about verdict drafts. Not security-advisory ground.

3. **mori — adjacent: holds a *published* repository security advisory as evidence, self-declared adjacency.**
   `mori-shokunin/corpus/SOURCES.md:18`: `| S012 | GHSA-652q-wxr6-h5j6 systemd-oomd advisory — https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6 | docs | A | systemd-oomd varlink arbitrary-SIGKILL vulnerability and affected versions |`. The advisory's page bytes are kept at `corpus/evidence/recheck-r32/S012.src` (published header at `:467-469`: "published GHSA-652q-wxr6-h5j6 Aug 10, 2026"). mori's entry itself rules the boundary: `corpus/knowledge/userspace-oom-killers-r12.md:24` "GHSA-652q-wxr6-h5j6 is adjacency only: patch-state assessment belongs to tsukuroi and is not absorbed by this entry." and `:33` "GHSA patch-state adjacency remains with tsukuroi." mori uses the published artifact for affected-version/patch facts; it records no draft→fork→CVE-request→credit→publication lifecycle. (Note: tsukuroi's corpus returned `No matches found`, so the ceded patch-state ground is not held there either under this pattern.)

4. **kaidoku — adjacent: consumer-side advisory records.**
   `kaidoku-shokunin/corpus/evidence/round-30/c1/pypi-uv-0.13.0.json:1` (long JSON line): `"id":"GHSA-hq85-5cpj-mr62","link":"https://osv.dev/vulnerability/GHSA-hq85-5cpj-mr62","source":"osv"` — PyPI/OSV vulnerability data used as round-30 C1 evidence of advisory *content*, not the maintainer-side lifecycle.

**shokuknow (read-only) — no corpus, no contest; hits are mirrors of lane work-products:**

- `lanes/kama/round13/evidence/fetch/vllm_release_v0.32.0.html:662,793-795` and `text/vllm_release_v0.32.0.html.txt:825,1020-1024` — release notes referencing *published* vllm GHSAs (GHSA-4hhp-h66f-j5j7 etc.). Adjacent.
- `lanes/kumitate/round3/CHANNELS.md:20`, `KNOWLEDGE-PROPOSED.md:125`, `SOURCES-PROPOSED.md:15`, and `merge/kumitate/SOURCES.append.md:31`, `merge/kumitate/knowledge/corpus/knowledge/mcp-2026-07-28-maintainer-account.md:116` — the undici dependency hazard `GHSA-4cwx-7wf7-3272`. Adjacent (dependency vulnerability, not advisory lifecycle).
- `lanes/tabi/round2/.work/github-ratelimits.txt:252`, `round8/.work/github-troubleshooting.html:32,176`, `.txt:508` — the same GitHub Docs nav chrome "Repository security advisories". Adjacent-chrome.
- Junk matches (pattern matching inside non-prose bytes): `lanes/kotodama/round15/.scratch/dh.html:30634`, `lanes/lore/round15/fetch/q_287.html:19`, `lanes/revenger/round13/measurements/researchmap.html:115`, `lanes/tameshi/round7/evidence/researchmap.html:115`, `lanes/audio/round9/evidence/t-researchmap.html:115` — base64 blobs; and `lanes/game-dev-3d/round11/measurements/l10n/wl_ja.po:98` where the address `highsate@gmail.com` contains the literal substring `ghsa` (case-insensitive). Decoded by re-running the single-file grep; line 98 printed: `# azim uynet <highsate@gmail.com>, 2024.`
- `doctrine/` and all shokuknow top-level files: no hits in the sweep output.

## 3. Ruling on the row: **F29 is uncontested**

- No sibling corpus holds any knowledge entry, source row, or lesson claiming the maintainer-side advisory lifecycle (draft advisory → temporary private fork → CVE request through GitHub as CNA → credit → publication → fix-version duty). The only sibling GHSA holdings are a published advisory used for patch-state facts (mori S012, self-ruled "adjacency only") and consumer-side advisory records (kaidoku OSV JSON; shokuknow vllm/undici mentions).
- kasegi's own committed corpus (baseline control) matches the pattern only in: the round-46 instrument itself (`corpus/instruments/r46-f29-gate.py:5-8`, which *defines* F29), the pre-entry capture (`corpus/source-snapshots/round-46-a2/S074.txt:2-19`, the S074 source) and its `manifest.json` quotes, the F28 entry's forward pointers, `SOURCES.md:74` (S068 — the round-43 GitHub Advisory *Database* row, a third-party republication record, explicitly tier B and rejected as that round's source), KEV notes URLs in `corpus/source-snapshots/round-35/S052.txt`, and lessons (`lessons/round-42.md:142-143` records the GHSA advisory-API doc candidate was *dropped* as "adjacent in sibling ground"). Glob `corpus/knowledge/github-repository*` → `No files found matching pattern`: the entry does not exist yet; only this wave's drafts (`wave1/R46bScribeEntryB/C/F.draft/github-repository-security-advisories.md`, same-lane work products, not contests).
- F28's scope line already holds the ground out (`corpus/knowledge/github-private-vulnerability-reporting.md:9`): "The entry does not record the maintainer-side flow". The row is clear for admission.

## 4. F28 screen — every sentence already touching maintainer-side mechanics

File: `corpus/knowledge/github-private-vulnerability-reporting.md` (F28, reporter flow). Line-by-line, the sentences the new F29 entry must **state as its boundary/contrast, not absorb**:

- **:9** — "The entry does not record the maintainer-side flow, and it is not a rule for other platforms, for coordinated disclosure in general, or for any particular repository." (the explicit hold-out)
- **:13** — "A package may not describe the maintainers' response, the advisory's outcome or the fix's publication from this page, because the page does not state them (see Limits)." (refuses exactly the lifecycle F29 records)
- **:20** — quotes "Maintainers can customize the form and require other information." (`S073.txt:573`) — maintainer-side form customization, held only as a reporter-visible caveat.
- **:23** — quotes "Note that only the repository maintainer can merge changes from that private fork into the parent repository." (`S073.txt:578`) — maintainer-only merge; F29 must state who creates/drives the fork, not just who may merge.
- **:24** — quotes "GitHub will display a message letting you know that maintainers have been notified and that you have a pending credit for this security advisory." (`S073.txt:575`) — maintainer notification + pending credit, reporter-visible only.
- **:33** — "Its line on 'admin or security permissions' (`S073.txt:563`) concerns who may create a draft advisory, not authorization to test." — the hinge sentence: `S073.txt:563` "If you have admin or security permissions for a public repository, you don't need to submit a vulnerability report. Instead, create a draft security advisory directly." is the one piece of maintainer-side mechanics inside the reporter-flow source, and F28 explicitly does not expand it.
- **:35** — "What is new here: … the maintainer-only merge from the temporary fork …" (claims it as reporter-side submission effects)
- **:40** — "The page does not state the maintainer-side flow, CVE requests, timelines or rewards." plus the forward pointers held as link text only: "Creating a repository security advisory" (`S073.txt:563`), "Managing privately reported security vulnerabilities" (`S073.txt:579`), and "The next steps depend on the action taken by the repository maintainer." (`S073.txt:579`). F29's S074 capture is the body of exactly that held-out pointer.
- **:45** — "The entry instructs no submission, no contact with any maintainer and no probing of any repository." (documentation-only stance F29 shares)
- **:49** — falsifiable rule tail: "A package that states a fix was merged from the reporter's private fork fails unless it also records the maintainer's merge, because only the maintainer can merge (`S073.txt:578`)."

Contrast the new entry must state: F28 covers the reporter's intake contract up to the "maintainers have been notified" message and refuses everything after; F29 begins at that handoff (draft advisory creation by maintainers/admins, private collaboration, CVE request as CNA, credit acceptance, publication, fix-version duty). The `S073.txt:563` sentence and the `:40`/`:43` link-text pointers are the stated seam between the two entries.

## 5. Control discrimination (the sweep is not a no-op)

- True positives found where ground exists (mori S012 rows; kaidoku OSV JSON; kasegi's S074 capture) — so the pattern is not vacuously green.
- Junk positives correctly classifiable: souji "drafts are advisory" (English collocation), `highsate@gmail.com` ⊃ `ghsa`, base64 blobs containing `GHSA` — a do-nothing control that reports "overlap" on any match would falsely contest F29 from souji/game-dev-3d bytes; each was opened and ruled.
- Sixteen corpora print a clean zero — a control that reports overlap everywhere is also falsified.

## 6. Limitations

- Assignment scope was sibling **corpora** + shokuknow; sibling `.ufo/` wave work-dirs outside their corpora were not swept, so sibling *in-flight* (uncommitted) drafting of this ground is not covered — only committed/attested ground.
- The sweep is text-pattern plus hit-by-hit reading; a paraphrased advisory-lifecycle description using none of `repository security advisory`/`GHSA`/`draft … advisory` could in principle evade it. Mitigation: the four hit corpora were read at entry level (mori, kaidoku, tabi, souji) and no such entry was present among them; the zero corpora are small knowledge trees whose README/SOURCES were visible in earlier greps.
- shokuknow is a mirror of round work-products; its `merge/` tree duplicates kumitate rows (same undici GHSA), counted once.
- Findings are observations of repo state at 2026-10-29, base as-is; no git mutation of any kind was performed.
