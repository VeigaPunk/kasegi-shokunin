VERDICT: INFO

# R45W2ScoutAdjacentRecheck: adjacency re-sweep on the landed tree (F27 / S071 / S072)

Attacked: lane export of commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c), exported with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>/lane`; `cat-file -t` printed `commit`. Registry rows at the landed tree: `corpus/SOURCES.md:77` (S071) and `:78` (S072). Sibling corpora were read only (`/home/vgpnk/Projects/shokunin/*-shokunin/corpus`, plus the non-lane directory `lane3`, reported separately). Pure base control: `/fast/scratch/hyaku/kasegi-r45/L1/pure` (read only).

## Finding 1 (subject overlap): none in any sibling corpus

Kernel-security terms, excluding kasegi:
```
grep -rIiEl 'kernel security|security@kernel|security-bugs|Linux kernel security|kernel\.org/process|kernel security team|security list' */corpus | grep -v '^kasegi-shokunin/'
-> mori-shokunin/corpus/evidence/recheck-r32/S071.src
   mori-shokunin/corpus/evidence/recheck-r32/S074.src
```
Both are Kubernetes sidebar links, not the kernel process. The printed line is `...href=/docs/concepts/security/linux-kernel-security-constraints/...`, a Kubernetes doc URL. No sibling cites `docs.kernel.org/process/security-bugs` (`kernel\.org/process` matched 0 sibling files).

Embargo wording: `grep -rIiEn 'embargo' */corpus` (excluding kasegi and lane3) gave 5 lines in 4 files. The hits are an economic embargo in kotodama `contact-scenario-builder.md:59,147`, preregistration text in mori `evidence/sources-r36/S211.src:1451`, a PMC mirror page, and a Playwright protocol .d.ts. None concerns vulnerability disclosure.

Embargo ceiling: `grep -rIiEn '7 calendar days|14 calendar days|seven calendar days|fourteen calendar days|release process starts|embargo[a-z]* .{0,60}(7|14|seven|fourteen) (calendar )?days' */corpus` (excluding kasegi and lane3) returned 0 lines. The broader `(seven|7)[- ]days` plus postpone/embargo/disclos/fix pattern returned 3 hits, all in kotodama calendar-festival text (a 42-day cycle).

AI-assisted report rules: the AI token (`\bAI\b|AI-`) appears in 96 sibling knowledge, lesson and SOURCES files. Only 2 of them also carry a reporting-channel token (`reproducer|public list|security list|security team|treat it as public|disclosure channel|disclosure policy|coordinated disclosure`):
- `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/executability/ui-umg-slate.md:101`: "it carries no command, no version, no reproducer" (UI measurement, unrelated).
- `revenger-shokunin/corpus/SOURCES.md:64` (S050): "Claude-Red SECURITY.md (maintainer intended-use and disclosure policy)" with the anchor "the repository's own stated intended use, authorized-testing boundary and disclosure window".

S050 is the one adjacent item. It is a different project's policy for an AI offensive-skill library, and its "disclosure window" is not the kernel's 7/14-day rule. It does not overlap F27 and nothing in the kasegi corpus cites it. F27 should not be read as adding ground on AI-tool disclosure windows.

Verdict on subject overlap: none. No sibling corpus holds the kernel security-list process, the 7/14-day kernel ceiling, or the kernel's AI-found treatment rule.

## Finding 2 (shared-namespace id reuse, latent, not a mis-resolution)

`grep -lE '^\| S07[12] \|' */corpus/SOURCES.md` lists 17 files, including kasegi. Excluding kasegi and lane3, 15 sibling *-shokunin lanes use S071 and S072 for unrelated documents. Printed rows (`grep -nE '^\| S07[12] \|' */corpus/SOURCES.md`), first cells:
- `chousa-shokunin/corpus/SOURCES.md:81`: S071 GNU coreutils `env(1)` manual; `:82` S072 GNU Bash Reference Manual
- `kaidoku-shokunin/corpus/SOURCES.md:77`: S071 capinfos(1); `:78` S072 packet-capture envelopes
- `kake-shokunin/corpus/SOURCES.md:79`: S071 X Cards markup; `:80` S072 GitHub social preview
- `kama-shokunin/corpus/SOURCES.md:83`: S071 git-cat-file; `:84` S072 jj metaedit
- `mori-shokunin/corpus/SOURCES.md:77`: S071 Kubernetes Controllers; `:78` S072 Wikipedia characterization test
- `revenger-shokunin/corpus/SOURCES.md:85`: S071 Awesome AI Reverse Engineering; `:86` S072 Awesome Reverse Engineering
- `tameshi-shokunin/corpus/SOURCES.md:80`: S071 jj working copy; `:81` S072 open(2)
- plus kengaku, kotoba, kotodama, kumitate, mado, souji, tabi, tsukuroi, and lane3 (also a Python json row at S071), each with an unrelated S071/S072.

Body-text references (`grep -rIhE '(^|[^A-Za-z0-9])S07[12]([^0-9]|$)' */corpus --exclude-dir=source-snapshots`, excluding table rows) are lane-local. Counts: chousa 46, kaidoku 18, kake 11, kama 12, kengaku 30, kotoba 23, kotodama 29, kumitate 19, lane3 30, mado 17, mori 10, revenger 9, souji 13, tabi 20, tameshi 16, tsukuroi 4, kasegi 64.

The collision is recognised in-lane. `chousa-shokunin/corpus/lessons/round-45.md:163-165` reads: "its prose ids point at other documents in lane numbering — S071 is used for RFC 7089, which is lane S079".

Cross-lane citation check: `grep -rIiEn 'kasegi' */corpus | grep -iE 'S07[12]|kernel|security-bugs'` (excluding kasegi) printed one line, a mori JSON `lane_root` field. No sibling cites kasegi's S071 or S072 or the kernel page. The collision is therefore latent. A bare token `S071` in any shared text is ambiguous across lanes, so F27's citations must stay lane-scoped. The S069 footnote in `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md:34-36` already documents the same issue for S069.

Within kasegi, the id reuse is new. The pure-base control found no S071 or S072 tokens in `knowledge/`, `lessons/`, `README.md`, `QUALITY.md` or `SOURCES.md`. The landed tree adds S071/S072 only in F27 artifacts and `lessons/round-44.md:205` (the round-45 correction).

## Finding 3 (do-nothing control and discrimination)

- Nonsense token control: `grep -rIlE 'R45ZZQX-NOHIT-7731' */corpus | wc -l` printed `0`, so the harness can return no hits.
- Positive control: `grep -rnE 'Round-35 lessons also use' <lane>/corpus` printed `.../knowledge/google-cloud-vrp-customer-resource-boundary.md:36`, so the lane grep reaches the S069 footnote.
- Positive control: `grep -rlE '\bS052\b' */corpus` printed sibling hits (chousa knowledge and lessons), so the sibling grep reaches sibling corpora.
- Base-control near-collision inside kasegi: the kernel-pattern grep on `L1/pure/corpus` returns `iso-29147-divergence-and-clause-crosswalk.md:48` ("Seven-day receipt is the guideline's own guidance") and `source-snapshots/round-26|28|30/S041.txt:1903` ("within seven calendar days."). This pre-dates F27. It is a 7-day receipt clock from ISO/IEC 29147, not the kernel's embargo ceiling. The F27 entry's "7-day ceiling" should not be read as the only 7-day figure in the lane.
- The landed-tree kernel-pattern hits in kasegi are the F27 files (`linux-kernel-security-bugs-reporting-process.md`, `r45-c2-gate.py`, `manifest.json`, `S071.txt`, README and SOURCES), plus the same ISO pre-existing files. Sibling hits: 0.

## Finding 4 (kernel URL targets in siblings)

`grep -rIohE 'https?://(docs|www)?\.?kernel\.org[^ )>"`]*' kama-shokunin/corpus kumitate-shokunin/corpus mori-shokunin/corpus` printed cgroup-v2, accounting/psi, admin-guide sysctl, man-pages and mfd_noexec targets. None is the security-bugs process page.

## Limitations

- Scope: text under `*/corpus` only. Sibling repo files outside corpus, and the staged shokuknow packages, were not searched.
- Regex overlap is phrase-based. A paraphrase of the kernel rule without these tokens (for example "publication delay" with no day count) would be missed. The `embargo` word sweep covers the most likely paraphrase.
- The first body-token sweep was capped at 40 lines by `head`. The per-lane counts in Finding 2 were re-run uncapped; the subject-overlap sweeps were not capped.
- Live state of the kernel page was not checked (out of this seat's scope). Sibling corpora are their moving working trees, read only.
- `lane3` is not a `*-shokunin` root. It was included in the id count and excluded from the subject verdict.
- No edits, commits or git mutations. Read-only `git cat-file` and `git archive` on the lane only. Scratch removed on exit.
- No tool installed.
