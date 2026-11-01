# Round 55 — the routed DF-1/DF-2 carry-in (non-claim), the figure-audit ledger growth 9 → 17 (C1), and the GitHub repository security advisories REST API surface (C2)

Four commits after the freeze (`fd7838c`): the carry-in landed FIRST as a routed non-claim
(`d0237d6` — the DF-2 before-state receipt regenerated and committed, the DF-1 R9-form erratum
appended with a runnable closure check, no filed byte edited), then C1 (`00832d2` — the
figure-audit ledger grown 9 → 17 on depth:verifiability) and C2 (`d9d77ec` — frontier F36, the
GitHub repository security advisories REST API reference on S087, the round-47 lead first opened).
Host unchanged from rounds 50-54 (Windows workspace, `python` 3.13.15, `python3` = Store stub, no
/home, no /fast). The freeze carried the S087 capture + manifest + the extended pre-freeze screen +
the do-nothing/stand-in/binding/recheck receipts; every C2 after-literal was dry-run against a
stand-in tree before the freeze, which caught this round's biggest own mistake (the incomplete
stand-in, below) before any data landed.

## Mistakes

Sweep that found them (paste, per contract): (a) the pre-freeze stand-in dry-runs — the counter
over the base export (do-nothing, 11:11:13Z) and over the stand-in (v1 11:21:39Z failing,
v2 11:23:07Z green); (b) the C1 receipts — the selftest, the red control over the DF-1 prose
figures AS FILED plus two wrong fold-figures, and the green lane run (all in
`.ufo/waves/round-55/controls/c1-*.txt`); (c) the DF-2 pin re-derivation greps run live before the
regenerated receipt landed; (d) the DF-1 closure check (`df1-erratum=closed` exit 0). Six rows,
two mined from the routed carry-in and four caught this round (three before their data landed, one
at the byte-verification step of the capture):

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| cited evidence pointer never committed (routed DF-2, mined from `corpus/lessons/round-54-verifier-spotcheck.md` §DF-2) | `d53-base-greps-r54.txt` was cited by the r54 corrections file (header + D53-2 disposition), the LOG round-54 entry, the SCORECARD round-54 section and the report's landed-changes table (cfdf059), but `git log --all -- <path>` was empty — four citations of a nonexistent file | the routed defect itself; the general rule is already QUALITY R18/R43-grade (a pointer must resolve at closure time) — what was missing was the landing discipline: a file named in a commit message or table cell must be in THAT commit's path list | regenerated receipt committed as `.ufo/waves/round-54/controls/d53-base-greps-r54.txt` (commit `d0237d6`) naming the same five sha pins (SOURCES@base `06c92e6a…`, nvd entry@base `15eb2d05…` = tip, receipt `be69ece7…`, manifest `eb6ffa60…`, capture `4d1c4e77…`), the four filed literals each exactly once at base and the measured 542/7590/33 — every limb re-run live before landing; rule going forward: before any commit, re-read its message and every table cell it touches and confirm each named path is in the path list |
| prose figures composed from memory, contradicted by the receipt they cite (routed DF-1, same source) | the r54 report and frozen C1 sentence say "0 mentions / 0 times in the base SCORECARD.md" while the do-nothing receipt they cite prints 2 (SCORECARD.md:2102,:2158 — the r52-planned/r53-routed sibling text); the LOG/knowledge-expected limbs (0/0) were right | the routed defect itself; now machine-caught by the round-55 C1 ledger entries `figure-audit-mentions-base-scorecard/log/knowledge-expected` (2/0/0) and by the red control carrying the prose AS FILED | appended erratum `.ufo/waves/round-55/controls/df1-mentions-erratum.md` (commit `d0237d6`), R9 form, closure check `df1-erratum=closed` exit 0; rule: a prose count that names a committed receipt must be copied from that receipt's printed limb, never re-typed from memory — the same lesson the r53 trailer taught, now doubled by ledger entries |
| stand-in tree built from an incomplete declared-adds list (own, pre-freeze, caught by the dry-run limb) | stand-in v1 (11:21:39Z) omitted the round-55 capture pair (uncommitted at export time), so the counter read `FAIL F36 … problems=manifest-unreadable` and `FRONTIER-FAIL F36 problems=missing-pass-line` instead of the frozen after-state; v2 (11:23:07Z) with the pair copied in reads green and is the of-record dry-run (`.ufo/waves/round-55/controls/c2-standin-dryrun-r55.txt` records both) | the R34/R45 stand-in discipline itself — the dry-run failed loudly instead of letting a false after-literal freeze | v2 is the of-record dry-run and the freeze quotes only v2's observed values; rule: a stand-in's declared-adds list is enumerated from the claim's OWN freeze-commit path list (every file the C2 commit will carry), not from the diff of prose files only |
| rev-pinned derives run against a non-git root (own, pre-data, caught before the of-record receipt) | the first C1 do-nothing draft ran the base ledger with `--root <base export>`; entries 1-4 read `derive-exit-1` because `git show 32782bd:…` cannot resolve inside a plain directory — 6 of 9 read stale against a base that is actually green | the receipt's own fail-closed limb (a nonzero derive is stale, never ok) | the of-record run (`.ufo/waves/round-55/controls/c1-donothing-r55.txt`) uses the lane root — a git repo, where the rev pins resolve — and re-runs 9/9 green; the discarded draft is disclosed inside the receipt itself; rule: a rev-pinned ledger is audited only over a git root, and an export is only ever a counter root |
| manifest quotes written as bare route lines fail the exactly-once bar (own, pre-freeze, caught by the pre-freeze recheck) | the first S087 manifest pinned Q4/Q6/Q8 as the bare `post|get|patch/repos/…` lines; `source-recheck` normalized-substring counting read Q4=5, Q6=3, Q8=2 (each route line is a prefix of the longer routes) — exit 0 via the anchor limb, but below the round-54 exactly-once shape | `source-recheck.py`'s B2 occurrences counter, working as designed | the three quotes rebuilt as route+cURL two-line spans (unique in the collapsed text, occurrences=1 each), all 14 assertions then `occurrences=1`; rule: a pinned quote's uniqueness is read from the instrument's own occurrences count, never from a `grep -c` line-count — substring matching over normalized text is the matching model |
| host shell grep reported 3407 CR bytes where the file has 0 (own, caught at the capture's byte-verification step) | `grep -c $'\r'` over S087.txt printed 3407 in Git Bash while a byte-level count (`python -c "b=open(...,'rb').read(); b.count(b'\r')"`) prints 0 — the MSYS grep opens files in text mode and fabricates CRs on CRLF-translating mounts; the same grep under the same shell reported S086's 0 CR correctly in r54 (different working directory mount state) | the round-54 manifest's declared no-op normalization — the claim "0 CR observed" is byte-checkable, so the contradiction was visible | the manifest's normalization note records the byte-level result (0 CR bytes, 0 TAB bytes, 3407 LF lines); rule: on this host, byte-shape claims are settled by a byte-level read (python `rb`), never by shell grep character classes |

## Gate

- S087 — https://docs.github.com/en/rest/security-advisories/repository-advisories — access date
  2026-11-01; three same-sha instrument opens this round (probe 10:37:57Z, recorded 10:46:13Z,
  verification second open; HTTP 200, 937712 fetched bytes each) plus two byte-identical raw-HTML
  curl opens (sha256 `89fa9af3…`); capture `corpus/source-snapshots/round-55/S087.txt` (3407 lines,
  137738 snapshot bytes, sha256 `3eebdf476fbfe5040ad3367edfe3961fbda1bff412bb74ee43bb08ab2f754b93`);
  normalization declared html (the committed instrument `capture-source.py --kind html`) with
  strip-cr-tab = no-op at byte level (0 CR bytes, 0 TAB bytes); manifest with 14 assertions Q1-Q14
  each occurrences=1 at its pinned anchor; command:
  `python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-55/manifest.json --source S087`
  → sha256 OK + 14 Q-OK lines, exit 0 (`controls/s087-recheck-r55.txt` and the final-receipt tail).
  Located quote (11 words by `wc -w`, R56): `"Repository security advisories" repository
  permissions (read) and "Administration" repository permissions (write)` at S087.txt:2853 (Q13).
- Rejections this round: none — the bounded hunt opened exactly the recorded lead (the round-47
  lead at SOURCES.md:137, provenance S076.txt:574); the lead line's bytes are unchanged with the
  flip recorded in the registry-changes bullets; the CISA ADP list page lead stays unopened (lead,
  not row — R64 does not apply to unopened surfaces).
- Extended pre-freeze screen (downstream-consumer sweep included), run at base BEFORE the freeze:
  `controls/neighbor-screen-r55.txt` — the lead URL is held by no README/PROVINCE/knowledge row
  (only the SOURCES lead line), the only advisories frontier neighbor is F29 (the concepts
  lifecycle — distinct machine-interface ground), and zero consumers of the REST URL exist across
  corpus/source-snapshots/ (the r47 instruments/lesson name it as a routed-defect provenance
  string, not as held ground).

## Limits

- The host-bound classes are unchanged and stay operator-owned (L0 kasegi round-50/46/54
  unanswered, routed around): the 30 problem-rows / 33 host-bound FAIL entry records behind the
  counter's exit 1 (39−6, invariant across the round's own after-state); the 67 `cd /home/vgpnk/…`
  recheck lines; the 3 cwd_fail lines; the limb-mutation replay's `python3` dependency. The
  AgentSwarm L2 surface stays absent on this host (disclosed every round since r50; D53-3/L0).
- S087 sits on a live docs.github.com page: byte-stability was measured WITHIN the round (three
  same-sha instrument opens + two identical curl opens), not across rounds; the 90d row recheck
  re-fetches and a changed sha re-fails the capture. Rate limits, plan-gated parameters, response
  examples and error-body schemas are unasserted (the entry's Limits).
- capture-binding `multi_row_url=7` is the known informational class, unchanged 7 → 7 by this round
  (S087's URL is unique; verified against the base export).
- The round-55 capabilities row enters through the round section (the r43/R6-append practice).
- The pre-existing worktree condition (uncommitted paths at the base) is standing and untouched;
  commits landed only named paths through the plumbing helper.

## considerthese disposition (R23/R27 reflection cadence)

Burst/idle review for this round: the newest reflection file is still `considerthese/2026-10-26.md`
— an idle stretch, no new reflection in the 2026-10-27 → 2026-11-01 window. Its seven proposals all
carry recorded dispositions (ledger `corpus/knowledge/considerthese-proposals-ledger.md` + rounds
36-39). Nothing new was adopted this round (the one-per-round slot goes unspent): `Assimilation:
none — shokuknow unreachable`.

## Census of record at this round's tip

Quoted only from the final regeneration over the truly final tree (after the SCORECARD/LOG result
appends); the figures live in the SCORECARD round-55 section and the gate receipt
(`.ufo/waves/round-55/controls/gate-final-r55.txt`). No corpus edit follows that receipt.
