# Round-25 lesson draft — `## Mistakes`, `## Gate`, `## Fixes that can fail`

Draft only. The L1 composes `corpus/lessons/round-25.md` from this file; no sentence here
is committed product prose. Seat `L1Kasegi25.LessonDraft`, written 2026-10-25.

**Basis of the numbers below.** "Committed bytes" means lane HEAD
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`, extracted read-only with
`git archive HEAD corpus | tar -x -C /tmp/kasegi-head-25`. The lane working tree was being
edited by other wave-1 seats while this draft was written (`git status --porcelain` in the
lane listed 33 modified paths and 3 untracked round-25 paths), so each measurement names
which bytes it read. A measurement against the working tree is marked *live tree*.

---

## Mistakes

**M25-1 · a `recheck:` field that is prose with a command inside it.** Class:
gate-not-applied-to-legacy-entries. Evidence: on committed bytes, **23 of 35** `recheck:`
fields begin with the literal token `on-restoration` and fail `bash -n`; the leading-token
census of the failing set is `{'on-restoration': 23}` and the failure text is
`bash: line 1: syntax error near unexpected token `('`. The 23 are a subset of the **25**
entries carrying the round-22 `## Provenance (round-22 correction, appended)` block
(measured: parse-fail ∩ legacy = 23 of 23). The form entered at `c8b719d`
(`2026-10-19 19:27:48 -0300`, "round-22: QUALITY bar, SOURCES registry, frontier F01-F05
admitted, legacy provenance disclosure"), found by
`git log -S'on-restoration —' -- corpus/knowledge/claim-gates.md`. Captured-by: **Q7**
(`corpus/QUALITY.md:48` at HEAD, "An executable recheck field contains a command, not prose
beginning “On each”") was written for newly admitted entries and no sweep ran it over the
legacy 25 — and **R2** was already violated in the same commit family:
`SCORECARD.md:327` at HEAD asserts "`recheck:` lines runnable **0/25 → 25/25**", a
self-description no command backed (running the field as written is a parse error, not
"exit 1, base absent"). Fix: keep the fail-closed test, prefix the command with
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`, and demote the prose to a trailing
`#` comment so the field stays one command — the shape landing in the live tree, e.g.
`git diff corpus/knowledge/claim-gates.md`:

```diff
-recheck: on-restoration — test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md (fails closed today: ...)
+recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md  # on-restoration — fails closed today: ...
```

Measurement (committed bytes, run by this seat):

```
$ python3 -   # reads /tmp/kasegi-head-25/corpus/knowledge/*.md, bash -n on each recheck value
HEAD files 35 recheck_lines 35 parse_fail 23
```

**M25-2 · a routed defect that named the wrong failure class.** Class:
under-measured-routed-defect. Evidence: the round-24 verifier routed D24-5
(`corpus/lessons/round-24-verifier-spotcheck.md:208`) as "5 of 35 `recheck:` lines carry it,
so a cold run from another cwd still exits 2", which implies the other 30 are
cwd-dependent. Measured by this seat on committed bytes, the 35 split four ways:

| cd prefix | parses under `bash -n` | n | files |
|---|---|---|---|
| yes | yes | 5 | `authorised-testing-rules-of-engagement`, `cna-assignment-and-vulnerability-rules`, `cra-manufacturer-reporting-duties`, `multiparty-vulnerability-coordination`, `statutory-authorization-and-unauthorized-access` |
| no | no | 23 | the legacy set in M25-1 |
| no | yes, cwd-dependent (lane root exit 0 / foreign cwd exit 2) | 6 | `ai-assisted-finding-validation`, `authorization-safe-harbor-and-scope`, `citation-bases`, `coordinated-disclosure-timelines`, `cvss-v4-severity-and-vector`, `cwe-top25-2025-methodology` |
| no | yes, cwd-stable | 1 | `root-loss-2026-10-12` (`test ! -e ~/Projects/...`; no relative path) |

So the non-conforming set is **29** (6 cwd-dependent + 23 unparseable), not 30, and the 23
are a different defect class from the 6: a line that never parses is not "cwd-dependent".
Captured-by: the round-24 closure ran one limb — exit-code equality under a pinned cwd —
and never a parse check; the class split that would have shown it already exists as the
`parse,cwd,paths` flags the frozen counter prints per line (`.ufo/waves/round-25/c1-before.txt`,
`claim-anatomy-sample.md  parse,cwd,paths=011 ... fail-closed FAIL`). Fix: a routed defect
quotes the per-class split (`parse_fail=23 cwd_fail=6 paths_fail=0`), never a prefix count.

Two-leg measurement (committed bytes extracted to `/tmp/kasegi-head-25`; the lane-root leg
runs from that extraction, the foreign leg from `/`, comparing exit status **and** a sha256
of combined stdout+stderr):

```
lines 35
parse_fail 23
cwd_diff 6 ['ai-assisted-finding-validation.md', 'authorization-safe-harbor-and-scope.md', 'citation-bases.md', 'coordinated-disclosure-timelines.md', 'cvss-v4-severity-and-vector.md', 'cwe-top25-2025-methodology.md']
same_both_cwds 6
```

**M25-3 · one artefact described with three numbers, and a score restated as measured.**
Class: self-description-as-claim (R2). Evidence, on committed bytes:

| artefact | claim | pointer |
|---|---|---|
| `round-24/manifest.json` | 19 records, **76** quotes | `python3 -c "import json;m=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(len(m['sources']), sum(len(s['quotes']) for s in m['sources']))"` → `19 76` |
| `corpus/instruments/README.md` | "19 captured records, **62** assertions" | `git show HEAD:corpus/instruments/README.md \| sed -n '174,176p'` |
| `SCORECARD.md` | "19 records, **77** assertions" | `git show HEAD:SCORECARD.md \| sed -n '510p'` |
| `corpus/lessons/round-24.md` | "19 records / **77** assertions" | `git show HEAD:corpus/lessons/round-24.md \| sed -n '77p'` |
| fleet report | "19 records, **76**" | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kasegi.md:31` |

No counting command sat next to any of the three lane numbers at HEAD (`sed -n '173,178p'`
of the HEAD README shows the figure and no command). Second limb, same class: the
bound-64→8 brace mutant is stated as measured at `corpus/instruments/README.md:159`
("scores 8/8 here and 24/24 on the round-23 matrix"), `SCORECARD.md:500` (same figure),
`corpus/QUALITY.md:65` (R11, "bound-64→8 **8/8 and 24/24 unchanged**") and the report
(`:159`, `:227`), while the only mutant receipt in the lane —
`.ufo/waves/round-24/wave1/ResolverAttack.md`, table row M4 — reads "**4/8, identical
receipt**" and its §F5 pins the bytes it ran as baseline `690153ad…`. `grep -rl db5e0767`
returns the fixed-resolver receipts (`c1-fixed.{json,txt}`,
`c1-containment-regression.{json,txt}`), the README, the round-24 lesson and the spotcheck —
no mutant receipt; `.ufo/waves/round-24/wave2/` holds only `swarm-registry.json`. Captured-by:
R2 existed and nothing checked the copies — the number lived in four files and the receipt
in none of them. Fix: one measured number per artefact with its counting command adjacent,
and a mutant score worded "would score X by construction; measured Y on bytes Z" unless a
receipt path exists.

**M25-4 · misroot scan: none found (recorded as a control, not a mistake).** Class: n/a.
Evidence, two scans by this seat. `git -C /home/vgpnk/Projects/shokunin status --porcelain`
→ 22 entries while the draft was being written (14 modified `.ufo/state/*.report-baseline`,
3 untracked `*.report-baseline`, `.ufo/watchdog.log`, `scripts/hyaku/hyaku.env`,
`scripts/hyaku/lane-addendum.md`, `.omp/mcp.json`, `.scratch/goal-20261025-hyaku-12h.md`);
→ 23 entries mid-work, the transient addition being `?? .ufo/reports/round-44/mori.md`
(mtime `2026-10-25 05:36:36 -0300`, first line `# mori — round 44`, "Lane: `mori-shokunin`"),
a sibling lane's round report in the fleet report directory, which is where lane reports
belong — that lane committed it at `86166ec7` (`2026-10-25 05:41:46 -0300`), so the final
scan is back to the same 22 entries. The only entry with an mtime inside the
wave-1 window and no lane identity is `.scratch/goal-20261025-hyaku-12h.md`
(`2026-10-25 05:23:08 -0300`), whose first line self-declares "ORCHESTRATOR-OWNED run state
(hyaku run 6). Not a misroot: lanes and seats never move, copy-then-delete, or edit this
file." No lane artefact (knowledge entry, instrument, snapshot, receipt) appears in either
fleet-root status. Limit stated, not hidden: authorship cannot be recovered from bytes, so
this is "no misroot found by path and content class", not "no seat wrote outside its scope".
Corroboration, not evidence: the read-only seat `ScoutMisroot.md` in this same directory ran
the same command and reached the same verdict with per-path writer attribution.

---

## Gate

Assimilation set for round 25: vendor-side disclosure policies as corpus objects. Lane row
ids continue the append-only registry from S035; the staged-package ids in parentheses are
the merge-package pointers (`.ufo/waves/round-25/capture-log.txt`). Captures are committed
at `corpus/source-snapshots/round-25/<id>.txt`; this seat re-hashed each snapshot against
the capture log's instrument output; the five matched byte count and sha256.

Admission date for each row below: **2026-10-25** (the capture UTC stamps are
`2026-10-25T08:14:25Z`–`08:14:28Z`). Occurrence checks use
`grep -Fo '<quote>' <capture> | wc -l` from `corpus/source-snapshots/round-25/`; the five
counts below are 1. Japanese quotes carry no whitespace tokenization, so the length is given
as characters rather than a word count that would be an artefact of the tokenizer.

### Admit S036 (staged S055) — Cybozu, 脆弱性情報ハンドリングポリシー

- URL: https://cybozu.co.jp/company/security-policy/
- Accessed: 2026-10-25 · capture `S036.txt`, `fetched_bytes=16900 snapshot_bytes=4815
  sha256=022ca4f40b9e07a4e052c4d6ac8a9b4195503489417eb7fd0760d28c35ceb950 utc=2026-10-25T08:14:25Z`
- Located quote — capture line 30, section 脆弱性情報の公開 › 対象範囲:
  「クラウド製品およびモバイル製品の脆弱性情報については、原則として公開しておりません。」
  (42 characters; `grep -Fo … | wc -l` = 1)
- Supports: disclosure scope is narrower than handling scope — the load-bearing claim of
  both live-tree entries for this set.
- L1 to fill: tier / status / recheck command / used-by.

### Admit S037 (staged S056) — Cybozu, FAQ（脆弱性報奨金制度）

- URL: https://cybozu.co.jp/products/bug-bounty/faq/
- Accessed: 2026-10-25 · capture `S037.txt`, `fetched_bytes=89300 snapshot_bytes=11194
  sha256=b204aa7f60ec2e70713ecd8c605fb1adb6e39549f0ef09d32a297c10f473cb4c utc=2026-10-25T08:14:25Z`
- Located quote — capture line 109, the A of the Q at line 108
  (「Q. Webサイトの脆弱性を見つけました。報告しても良いですか？」):
  「ご報告いただけます。ただし、サイトによっては報奨金制度の対象外の可能性があります。報奨金制度の対象製品をご確認ください。」
  (60 characters; `grep -Fo … | wc -l` = 1)
- Supports: bounty scope is a product list, not the intake surface.
- L1 to fill: tier / status / recheck command / used-by.

### Admit S038 (staged S057) — GMO Pepabo, 脆弱性報告制度

- URL: https://pepabo.com/contact/vulnerability-reporting/
- Accessed: 2026-10-25 · capture `S038.txt`, `fetched_bytes=37806 snapshot_bytes=3093
  sha256=09e077d31ce3b5e366fa435f5c474db7405eef8dd313b64be46f88047dabb68a utc=2026-10-25T08:14:25Z`
- Located quote — capture line 17, section 脆弱性報告制度, second paragraph of the intro:
  「また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。」
  (67 characters; `grep -Fo … | wc -l` = 1)
- Supports: a vendor safe-harbour statement conditioned on a published list (the sentence
  two lines below, line 20, states 現在、報奨金制度は設けておりません。, the no-bounty half
  of the same claim).
- L1 to fill: tier / status / recheck command / used-by.

### Admit S039 (staged S060) — Hitachi HIRT, HIRT-PUB10008

- URL: https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html
- Accessed: 2026-10-25 · capture `S039.txt`, `fetched_bytes=199797 snapshot_bytes=37126
  sha256=657e7b4c67e67d00b190b31942d749a28d0988f15d1e6f5f506130accffc191d utc=2026-10-25T08:14:26Z`
- Located quote — capture line 519, section 1.3 調査ならびに対策 … (2) (heading line 517):
  「「対策情報を公表日に同時に公開する」「公表日一致の原則に従う」の２つです。」
  (37 characters; `grep -Fo … | wc -l` = 1)
- Supports: a vendor publishes to a date agreed with the coordinator — the timing half of
  the disclosure claim; the capture also records the document's own ISO/IEC 29147:**2014** edition
  (line 497, 499), which is the version contrast against S040's 2018 alignment.
- L1 to fill: tier / status / recheck command / used-by.

### Admit S040 (staged S068) — Cisco Security Vulnerability Policy

- URL: https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html
- Accessed: 2026-10-25 · capture `S040.txt`, `fetched_bytes=94027 snapshot_bytes=33463
  sha256=b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c utc=2026-10-25T08:14:28Z`
- Located quote — capture line 58, section Cisco Product Security Incident Response:
  "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018," (9 words;
  `grep -Fo … | wc -l` = 1)
- Supports: a vendor names the standard edition it follows (2018, against the Hitachi
  document's 2014) — the cross-vendor comparison in the entry.
- Access note, verbatim from the capture log: "A plain `curl -L` with a browser UA returned
  http 403 for S040 while the capture instrument's own UA (`kasegi-shokunin/1.0
  (documentation capture; …)`) returned 200". The row is admitted on the committed capture;
  a recheck must re-fetch with the same UA or the row fails closed on 403.
- L1 to fill: tier / status / recheck command / used-by.

### Reject — `vendor-cvd-policy-crosswalk-2026-10-23.md` (staged package)

- Failing criteria, each measured by this seat:
  1. **Q7** — its `recheck:` (staged file line 6) is prose with a command inside it:
     ``recheck: 180d — `curl -sSL https://www.cisco.com/...` then confirm the ISO/IEC
     29147:2018 sentence and the JP-CERT coordination sentence are still present (ran
     2026-10-23)``. `bash -n` on that value → **exit 2**
     (`syntax error near unexpected token `('`).
  2. **Duplicate ground row** — its `ground:` (line 7) names `F20`, and the lane frontier
     table has no such row: `git show HEAD:corpus/README.md | grep -cE '\| F20 '` → `0`
     (the last admitted row is F09, `corpus/README.md:208`; admitted rows at HEAD = 9,
     F01–F09).
  3. **One document, two row ids** — its only source is S068, whose URL is byte-identical
     to this round's S040 (`https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`);
     `git show HEAD:corpus/SOURCES.md | grep -c S068` → `0`, so admitting the crosswalk
     registers the same document under a second lane id. The round's adopt set is
     S055/S056/S057/S060 (`.ufo/waves/round-25/claims.json`), which does not include S068.
- Flip condition: (i) `ground:` names a frontier id that exists in `corpus/README.md` at the
  commit that lands it (F10, once this round's row is added) and the id is checked by a
  command; (ii) `recheck:` becomes one executable command whose `bash -n` exit is 0 and
  which re-verifies both named sentences against the committed `S040.txt` with
  exactly-once occurrence counts; (iii) the L1 resolves the S040/S068 single-owner question
  — the crosswalk either merges into the vendor-policy entry or explicitly supersedes the
  S040 usage, so one document is registered once.

### Entry-side facts the L1 must resolve before composing

Two lane entries are being drafted against this set in the live tree (untracked at the time of
writing), and they overlap:

| entry | header `source:` set | `recheck:` `--source` set | covers its headers (R12 shape) | `ground:` |
|---|---|---|---|---|
| `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` | S036, S037, S038, S039 | S036, S037, S038, S039 | yes | F10 |
| `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | S036, S038, S039, S040 | S036, S038, S039, S040 | yes | F10 |

Overlap = **3** source ids (S036, S038, S039) under the same F10 ground. Both recheck lines
name `corpus/source-snapshots/round-25/manifest.json`, which exists (5 records, 33 quotes,
ids S036–S040) and both are `cd`-prefixed. Decision for the L1: one object per document set,
or a declared division of labour, so the F10 row's entry column does not list two entries
that re-assert the same three sources.

**Conflict reported verbatim, for the canonical judge.** `claims.json` records
`assimilation.planned_reject: "vendor-cvd-policy-crosswalk-2026-10-23.md (S068 Cisco policy
unreachable this round)"`, while `.ufo/waves/round-25/capture-log.txt` records
`S040 status=200 fetched_bytes=94027 snapshot_bytes=33463
sha256=b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c
utc=2026-10-25T08:14:28Z out=corpus/source-snapshots/round-25/S040.txt`, and the file at
that path hashes to that sha256 (verified by this seat). The reachability ground is
therefore contradicted by committed bytes; the reject above stands on criteria 1–3, which
this seat measured directly, and not on reachability.

---

## Fixes that can fail

Each fix names the control that would show it is not working. A fix whose control cannot
fail is not a gate.

1. **Legacy recheck rewrite (M25-1).** Fix: `cd <lane root> &&` prefix + prose demoted to
   `#`. Controls: (a) the do-nothing control — the frozen counter on unchanged committed
   bytes must still print `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6
   paths_fail=0 exit=1` (`.ufo/waves/round-25/c1-before.txt`; this seat independently
   reproduced `pass=6` by running both legs itself), so a counter that scores 35 on HEAD
   bytes is void; (b) a mutation control — strip the `cd` prefix from one rewritten line and
   the counter must drop to `pass=34 cwd_fail=1`; (c) a rewrite that adds `cd` but leaves
   the prose outside a `#` must still be counted `parse_fail`, not `pass`.
2. **Per-class counting in a routed defect (M25-2).** Fix: report `parse_fail` / `cwd_fail`
   / `paths_fail` separately, never a prefix count. Control: feed the counter one synthetic
   prose-only value and one synthetic bare-relative command; if both land in the same class
   bucket the split is not exercised. Second control: the published total must be
   `23 + 6 = 29`, and a receipt that prints `30` fails against this draft's table.
3. **One measured number per artefact (M25-3).** Fix: the counting command sits next to the
   number. Control: run the command against a scratch copy of the manifest with one quote
   removed — it must print `75`, so a stale `76` is detectable; and
   `grep -n '62 assertions\|77 assertions'` over `corpus/instruments/README.md`,
   `SCORECARD.md`, `corpus/lessons/round-24.md` must return 0 hits after the fix (at HEAD it
   returns the three divergent copies above).
4. **A mutant score is measured only with its receipt (M25-3, second limb).** Fix: the
   wording carries a receipt path or is labelled "by construction". Control: a review check
   that requires, for each sentence of the form "scores N/M", a `test -f <receipt>` that
   succeeds and a `grep` of that receipt for the same figures — the round-24 wording fails
   it today (no receipt names a mutant of `db5e0767…`; the measured 4/8 is on baseline
   `690153ad…`).
5. **Misroot control (M25-4).** Fix: none needed; the control is standing. Control:
   `git -C /home/vgpnk/Projects/shokunin status --porcelain` at round close lists only
   orchestrator-owned paths (`.ufo/state/*`, `.ufo/watchdog.log`, `scripts/hyaku/*`,
   `.omp/mcp.json`, `.scratch/goal-*`); the appearance of any lane artefact (knowledge
   entry, instrument, snapshot, receipt) in that list is the fail signal, and the check is
   runnable in one command at any time.
