# QuarterDenominator — coverage denominator audit (read-only seat)

Scope: kasegi round 24, C2 (`coverage`) denominator only. No edits, no installs, no
network. Lane state at audit: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin
rev-parse HEAD` = `c2480b143120364728b40397926ffcf30a7309c8`; claim base
`d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a` is its parent. `git diff --stat d0a3f6a HEAD`
= `corpus/lessons/round-23-verifier-spotcheck.md | 142 +` (one file, no coverage input).
`corpus/README.md` blob is byte-identical at base and HEAD
(`git rev-parse d0a3f6a:corpus/README.md` = `git hash-object corpus/README.md` =
`72d5ccfd7d0fd29276a03c061208e71633c42bdf`), so every count below holds on both trees.

## Answer

**Number to put in the SCORECARD coverage row:**

`0/20 present (0/2 surviving-root surfaces; 18/18 lost-tree surfaces corpus-attested —
§3 enumerates 19); 19/20 governed by the r15 census rule. Frontier table 8/8 -> 9/9 on its
own separate denominator. Score 7, held.`

**Justifying sentence:**

> `AXES.md:12` defines coverage as "Fraction of the domain's real surfaces the skill
> governs (repo paths, tools, edge classes)", and `SCORECARD.md:43-47` fixes that surface
> set as the two surviving roots (2 items) plus the attested 18; F09 is public practice
> outside those surfaces — the frontier is a separate denominator frozen at eight topics
> (`SCORECARD.md:382-385`) — so admitting F09 moves the frontier table 8/8 -> 9/9 and
> leaves the coverage fraction, and score 7, unchanged.

Evidence for the sentence, two independent precedents where the frontier fraction moved
from 0% to 100% with the score held:
- `SCORECARD.md:328` (r22): "Frontier topics admitted **0/5 -> 5/5** ... **Score held**: the
  r15 domain-root definition is unchanged by public-practice entries (r22 critic)".
- `SCORECARD.md:404` (r23 C2): "frontier **5/8** ... **8/8** ... **Improved, score held 7**".
- `SCORECARD.md:382-385` (r23 claim): "Public-practice frontier denominator frozen at eight
  topics: 5/8 -> 8/8. The historical lost-root denominator and score 7 are not redefined."

## (a) The r15 surface set and today's counts

Denominator, as stated: `SCORECARD.md:43-47` — "the 18-item r12 denominator is now **0
present / 18 corpus-attested**, and the surface set is re-based onto the two surviving
roots (2 items) + the attested 18" -> 20 declared.

**Present: 0/2.** `test -e` fails for both:
```
ABSENT /home/vgpnk/Projects/the-bounty-hunter
ABSENT /home/vgpnk/Projects/origin-work
ABSENT /home/vgpnk/Projects/origin-work/open-bug-bounties
```
Corroborated by committed bytes: `corpus/knowledge/root-loss-2026-10-12.md:13-14`
("ABSENT — `test -d` fails; no `find ~ -maxdepth 5 -iname '*bount*'` hit outside this lane" /
"the entire `origin-work` directory is gone"). `SCORECARD.md:135` already records "0/2
present".

**Attested: 18/18 by declaration, 19/19 by enumeration** — see defect D1 below.

**Governed under the r15 credit rule** (a full census/full read, or a recorded park
disposition): **19/20**. `SCORECARD.md:67` credits the-bounty-hunter as a file-granularity
census ("34 files, 8 dirs, per-file `wc -l` + sha256 ... = 1/2") and explicitly denies the
second root: "`~/Projects/origin-work/open-bug-bounties` **top-level inventory only** ...
**= 0/1 censused** → the round-16 move". The 18 lost-tree censuses survive in
`corpus/knowledge/` (`corpus/README.md` coverage map, 36 rows at HEAD). So 18 + 1 = 19 of
20, i.e. 95% — the same arithmetic the r15 row used, on today's bytes.

Two defensible readings exist in the committed text and they give different numerators:
- **present/openable**: 0/20 (`SCORECARD.md:135`, `corpus/README.md:207-210`).
- **governed-by-record**: 19/20 (`SCORECARD.md:67` credit rule).
The SCORECARD does not say which one the score 7 is a function of (defect D3).

## (b) Frontier topic count at base `d0a3f6a`

Two independent counts on the frozen blob (`git show d0a3f6a:corpus/README.md`, frontier
section at line 194, rows at lines 198-205):

```
awk -F'|' '$2 ~ /^ *F[0-9]+ / {n++} END{print n+0}'            -> 8 topics
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}'
                                                              -> 8 admitted
grep -cE '^\| F0[1-8] .*\| admitted \|'                       -> 8
```
Same commands on the working tree: 8 / 8 / 8. **Base = 8 topics, 8 admitted** (F01-F08);
F09 is absent from `corpus/README.md` and every `corpus/knowledge/*.md`
(`grep -c F09` -> no nonzero file). The claim's precondition that the topic is new holds
at base for its stated token test: `grep -icE 'rules of engagement|statutory
authorization'` over `d0a3f6a:SKILL.md` and all `corpus/knowledge/` blobs = `0 0`, exit 1.

## (c) Does admitting F09 change the coverage score?

**No — only the frontier table.** Grounds:

1. `AXES.md:12` makes coverage a fraction over "the domain's real surfaces ... (repo paths,
   tools, edge classes)". F09 is public practice about authorisation documents, not a
   top-level surface of the domain root `~/Projects/bounties`; it appears in no denominator
   the SCORECARD defines for that axis.
2. `SCORECARD.md:382-385` freezes the frontier as its own denominator ("eight topics") and
   says "The historical lost-root denominator and score 7 are not redefined".
3. Two rounds moved the frontier fraction 0/5 -> 5/5 and 5/8 -> 8/8 with the score held at
   7 (`SCORECARD.md:328`, `:404`) — the frontier ratio demonstrably does not drive the score.
4. The r22 "proposed denominator for adoption next round: 20 corpus-attested Core items +
   5 Frontier topics -> (20+0)/25 before, (20+5)/25 after" (`SCORECARD.md:328`) was **not
   adopted**: the r23 claim froze the eight-topic frontier instead. Even if it had been, its
   numerator treats all 20 Core items as governed, so it reads (20+8)/28 = 100% -> (20+9)/29
   = 100%: F09 still moves no score.

Residual overlap to disclose, not a denominator issue: F03 already governs "Authorization,
safe harbor, and scope" (`corpus/README.md:200`, S006-S008). F09's marginal content is the
engagement-document and statute edge classes; the new row's `next` cell should say so, or a
reader counts authorisation twice in the frontier table.

## Defects found (all pre-existing; no edits made)

**D1 — the "18" is declared, not countable; §3 enumerates 19.**
`corpus/knowledge/source-tree-loss-2026-09-28.md:64` heads the section "18-surface
denominator"; the list at `:66-78` splits on `·` into **19** items (claims/, evidence/,
ledger/, bounty-map/programs/, docs/, ops/, fleets/, vdp-disclosures/, .ufo/,
.ufo-{ingestion,warden}/, .omp/, 22 .ufo-mission-report-bh*, pendle-core-v2-public/,
george/, vgn-bounty-lab/, README.md, .gitignore, 2 root zips, .git/). No committed file
names the r12 18: `grep -rn '13/18'` hits only `LOG.md:245` ("13/18->18/18 top-level
surfaces"), and `corpus/lessons/round-13.md:52-54` calls it a proxy ("survived re-walk, but
'3 root files' undercounts 26"). Which of the 19 the declared 18 omits is **UNVERIFIED** —
the bytes do not say. Consequence: `18/18 corpus-attested` cannot be re-derived by any one
command; a counter would print 19.
Repro: `sed -n '64,78p' corpus/knowledge/source-tree-loss-2026-09-28.md` then split on `·`.

**D2 — the second root's "census" is a dead citation.**
`corpus/knowledge/citation-bases.md:44` says the `.ufo-missions` loss is "recorded in
`corpus/knowledge/open-bug-bounties-census.md` §loss-event". That file does not exist and is
untracked (`ls corpus/knowledge/open-bug-bounties-census.md` -> No such file or directory;
`git ls-files corpus/knowledge/ | grep -c open-bug` -> 0). It is the only citation of that
path in the tree. The actual record is the inventory paragraph at
`corpus/knowledge/source-tree-loss-2026-09-28.md:128-141` ("**Not censused** (top-level
inventory only)"). A reader auditing "attested" by following citations lands on a missing
file and cannot distinguish "census intact" from "census never written".

**D3 — no stated mapping from the fraction to the score, and no count command.**
`AXES.md` fixes the scale as 0-10 but defines no band; `SCORECARD.md:43-47` defines the
proxy without a numerator rule for present-vs-census credit (the two readings in (a) above);
`corpus/QUALITY.md` carries only entry/record gates (Q1-Q8), no coverage gate. So score 7
today is an author judgment reproducing r19, not a measured function of 0/20 or 19/20. This
is the same class the frozen C1 debt names: a number no single command reproduces.

**D4 — integration pinch point for F09.**
`PROVINCE.md:38` reads "indexed in corpus/README.md under Frontier F01–F08." Admitting F09
in `corpus/README.md` without editing that line leaves PROVINCE contradicting the frontier
table. The F-id range is also repeated as history in `corpus/README.md:5` (r22/r23
correction note), which is append-only text and should not be rewritten.

## Unresolved / not verifiable from committed bytes

- Which single item the declared 18 excludes (D1). No command in the lane produces the 18.
- Whether "attested" for the 18 ever meant "census re-read this round" or only "census
  written in rounds 11-15". The entries carry as-of dates (2026-09-28T23:32Z) but no
  re-attestation after the 2026-10-12 second loss; attestation is a claim about records,
  not about sources (sources are gone).
- Score band for 95% governed: not committed anywhere (D3).

## Tooling

No installs, no upgrades, no package operations performed. Read-only git (`show`,
`rev-parse`, `hash-object`, `log`) and `test -e` only; no network access.
