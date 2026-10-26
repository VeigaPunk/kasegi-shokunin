# ScribeShonen — round-34 SHONEN refresh (promotion checklist, four boxes)

- Seat: `ScribeShonen` (scribe, leaf of the round-34 L2 wave; this instance answers as
  `ScribeShonen-2`). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base
  `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`;
  HEAD at measurement `206e5108f1190e61b3e2622d21cab8a5d921650c` with a shared, peer-written
  worktree (62 wave receipts present at read).
- Answering model: `opencode-go/deepseek-v4.1-flash` (config route; no model passed by hand).
  Tools installed/upgraded: **none** — no `pacman`, no `uv tool`, no `npx`, no network fetch.
- Write scope exercised: `SHONEN.md` (four box paragraphs) and this receipt. Nothing else was
  written: no `SKILL.md`, no `PROVINCE.md`, no `corpus/**`, no `LOG.md`, no claims/erratum file, no
  fleet root, no sibling lane, no `shokuknow`. No `git add`/`commit`/`push`, no `jj` mutation.
- Scratch: `/fast/scratch/hyaku/kasegi-r34/ScribeShonen/` (two text captures). Removed and verified
  absent (§7).

## Report

### 1. Pre-state

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ sha256sum SHONEN.md ; wc -lc SHONEN.md ; grep -c '^- \[' SHONEN.md ; grep -c '\[x\]' SHONEN.md
a8d7d203767376aeb7afd9025d77c7a7687aacf1d386dd847722d563afdc008a  SHONEN.md
  42 3806 SHONEN.md
4
0
```

All four boxes were `[~]` (lines 5, 15, 24, 36) with round-33 evidence text; no `[x]`. Two of the
old sentences were already false on HEAD bytes before this seat touched the file:

| old SHONEN text | bytes at HEAD `206e510` | command |
|---|---|---|
| `## Round 31` (`:1584`) "is the last end-to-end entry and no `## Round 33` heading exists (`grep -c '^## Round 33' LOG.md` = 0 … 1595 lines)" (lines 18-19) | `## Round 33` **exists** at `LOG.md:1597`; file is 1599 lines | `grep -n '^## Round 33' LOG.md` -> `1597:## Round 33 — 2026-10-26 …`; `wc -l LOG.md` -> `1599` |
| the claim was measured at `9f98488` | true there, false now: the heading was appended by closure commit `5b7a039` | `git show 9f98488:LOG.md \| grep -c '^## Round 33'` -> `0`, 1595 lines; `git show 5b7a039:LOG.md \| grep -n '^## Round 33'` -> `1597:` |

This seat corrected that parenthetical rather than carrying it forward (it states the old commit at
which the sentence was true).

### 2. What this seat changed, and the receipt's own digests

`SHONEN.md` only, four paragraphs replaced in place (header, bullet markers and `[~]` states
unchanged; no `[x]` written):

```
$ sha256sum SHONEN.md ; wc -lc SHONEN.md ; grep -c '^- \[' SHONEN.md ; grep -c '\[x\]' SHONEN.md
6d80dfd46940afec65e975cbfdd8a6d8e76e3a609f8d7bcf91446e3773e62fb9  SHONEN.md
  67 5514 SHONEN.md
4
0
$ git diff --numstat -- SHONEN.md
56	31	SHONEN.md
```

The 31 deletions are the four old evidence paragraphs this seat replaced; nothing outside those
paragraphs moved. A wave seat is not a named non-author verifier, so no box was promoted: all four
stay `[~]`, and each refreshed pointer names the round-34 receipt or command that grounds it.

### 3. The four boxes — refreshed pointer and the fact behind it

Every quoted figure below is either (a) run by this seat, with its command, or (b) read from the
named round-34 receipt. None is inferred.

**Box 1 — decision tables/checklists.** `SKILL.md` is byte-unchanged this round:

```
$ git diff --numstat 014ee2d7 -- SKILL.md PROVINCE.md        # empty output, exit 0
$ sha256sum SKILL.md ; wc -l SKILL.md
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  SKILL.md
1090 SKILL.md
```

No-harm re-measure on those bytes, read from `.ufo/waves/round-34/wave1/RevNoHarm.md` §A/§B/§C
(`== SKILL.md: 12 in-range cite instances, 0 bad; … LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0
OUTSIDE-BASE=0 BASE-ABSENT=0`; `| | **mean dens** | … **201.7** |`, `SKILL.md (1090 lines, 25
blocks)`, `Total path-citation instances: 710 across 25 blocks.`), and identical figures in
`ScribeSkillGate.md` §3. **Open item carried into the box:** `ScribeSkillGate.md` §4b's conditional
obligation fired — `capture-binding-check.py` landed hardened, so the round-33 re-verify row at
`SKILL.md:1090` (`(target `b4182665…`)`, 492 lines, `selftest cases=11`) no longer matches the
landed instrument (`3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`, 892 lines,
`selftest cases=23` — `ExecCaptureBindingHarden.md` §Commands) and the append-only EOF correction is
not yet in `SKILL.md`.

**Box 2 — end-to-end task logged.** No new end-to-end domain task ran this round; the box says so
explicitly instead of borrowing round-34 instrument work as a task:

```
$ grep -c '^## Round 34' LOG.md          -> 0
$ grep -n '^## ' LOG.md | tail -1        -> 1597:## Round 33 — 2026-10-26 — …
$ wc -l LOG.md                           -> 1599 LOG.md
```

Nearest executed measurement remains round 33's capture-binding run
(`.ufo/waves/round-33/wave1/ExecRegressionC1.md` §1/§2.1-2.2: `records=40 bound=40 unbound=0` exit 0
twice, `selftest cases=11 failures=0`); round 34 hardened the same instrument
(`ExecCaptureBindingHarden.md` §Addendum: `records=41 bound=41 unbound=0`, `binding_exit=0`,
`AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10
missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt`; `selftest cases=23 failures=0`),
which the box labels instrument work, not a domain task.

**Box 3 — instructions executable without oral context.** Measured by this seat at
`2026-10-26T06:03:13Z`:

```
$ python3 corpus/instruments/recheck-audit.py --quiet ; echo "recheck_exit=$?"
strict pass=46/46 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=22 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=46 total=46 pass=46 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=45 missing=0 unexpected=1 exit=1
recheck_exit=1
$ ls corpus/knowledge/*.md | wc -l                -> 46
$ grep -vc '^#' corpus/instruments/knowledge-expected.txt -> 45
$ sha256sum corpus/instruments/knowledge-expected.txt
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
```

So the entry-side instructions execute (`strict pass=46/46`), but the expectation limb is **open**
(`unexpected=1`, exit 1) because the expected list still has 45 entries and does not name the F17
entry. This seat scanned `wave1-spec.json` for an owner of that sync — no seat prompt contains the
string `knowledge-expected` (0 matches) — and reports it rather than editing `corpus/instruments/`.
The new instruments' selftests, read from receipts: `ExecRDefectClosureSuite.md` §4
(`selftest cases=9 failures=0`, `selftest_exit=0`), §3 (`closed=9/9 exit=0`), §5 (base tree
`closed=0/9 exit=1`); `ExecCaptureBindingHarden.md` §Commands (`selftest cases=23 failures=0`);
`ExecKillRuleCheck.md` §3 (`GATE ok name=survivors-zero`, `mutants=3 killed=3 survivors=0 invalid=0`,
`survivors=0`, `exit=0`), with §9b disclosing one unpinned `parse_round` mutant shape
(`mutant=parse-round-nonround-dir-archival-exemption killed=0`, `survivors=1`); `ExecHarnessAfter.md`
§4 (`PASS F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md  ids=S051  exit=0`,
`entries=20 pass=20 exit=0`).

**Box 4 — no cross-domain bleed.** Measured:

```
$ git diff --numstat 014ee2d7 -- PROVINCE.md     # empty output, exit 0
$ wc -l PROVINCE.md ; sha256sum PROVINCE.md ; grep -c 'F17' PROVINCE.md
74 PROVINCE.md
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md
0
$ sed -n '74p' PROVINCE.md
[r33 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F16 — Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) — admitted round 33
```

The file is untouched and the F17 amendment is owed, not applied; `ScribeSkillGate.md` §4a supplies
the exact append (2 lines / 216 B, `sha256 33f769be3bc6038afd0961d0d20868fbf096f6430d322df07287875b46fafa47`)
and a prefix-identical rehearsal. Cross-domain evidence read from `ConnSibling.md` §1 ("**Contested
scope: none.**") / §2 (seven tokens × 20 sibling corpora + fleet root; one `Immunefi` hit, kotoba's
mirror of kasegi's own `SKILL.md:130`) and corroborated by `ScoutSiblingSweep.md` §1-§2.

### 4. Facts measured for the L1's closure (not box claims)

```
$ git show <rev>:SCORECARD.md | grep -c '<LANE_HASH>'
7963976e -> 2    014ee2d7 -> 2    29f606d -> 2    206e510 -> 2
$ grep -c '<LANE_HASH>' SCORECARD.md        -> 0        (worktree; R1 correction landed)
$ grep -nE '^\| F17 \|' corpus/README.md    -> 361:| F17 | Immunefi Vulnerability Severity Classification System v2.2 …
$ grep -nE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md -> 57:| S051 | …
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 51
$ grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l -> 1
$ python3 -c "...round-32 manifest..." -> S049 2026-10-26T04:16:06Z None ; S050 2026-10-26T04:16:16Z None
$ python3 -c "...round-26 manifest..." -> records ['S041']; "orphans": [{"path": "S040-live.txt", "reason": "Live probe capture …", "row": "S040", …}]
```

The round-32 `fetched_utc` values are now strict-UTC instants (the frozen before value was
`2026-10-25T23:14:00-03:00`), and round-26 carries an explicit `orphans` listing for
`S040-live.txt` instead of a record — both limbs of C1's manifest/orphan clause, at the byte level,
independent of any seat's verdict.

### 5. Findings (reported, not judged — the L1 decides)

1. **`knowledge-expected.txt` unsynced (blocking box 3's `recheck_exit=0`).** `recheck-audit.py
   --quiet` exits 1 with `expect=present expected=45 missing=0 unexpected=1`; the file has 45
   entries and sha256 `3f68b9a2…ab81ceb` (the round-33 digest), while `corpus/knowledge/*.md` is 46.
   One appended line (`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, matching the
   list's sorted style) clears it. No round-34 seat prompt mentions the file.
2. **`SKILL.md` round-33 re-verify pin is stale.** `SKILL.md:1090` still carries `(target
   `b4182665…`)`, 492 lines and `selftest cases=11`; landed bytes are `3d9e5e0d…`, 892 lines,
   `cases=23`. `ScribeSkillGate.md` §4b has the append-only template; it is not applied.
3. **`PROVINCE.md` F17 amendment owed.** Exact proposed bytes in `ScribeSkillGate.md` §4a; file is
   still 74 lines / `b57de5d9…abd679` with the frontier list ending at F16.
4. **`corpus/QUALITY.md` R22 grounding mismatch (verbatim).** The row reads "Grounded in: round-33
   verifier R2; M34-2" and "M34-2 at `.ufo/waves/round-34/claims.json` →
   `non_claim_frontier_items.mistake`". But `.ufo/waves/round-34/claims.json` defines
   "M34-2: <LANE_HASH> placeholders filed in SCORECARD.md (R1)" — a different defect from the
   pre-freeze satisfiability step R22 codifies (spotcheck R2). R24's `M34-1` citation is correct.
   Reported for the L1; this seat did not edit `QUALITY.md`.
5. **Frozen-C1 literal superseded by erratum (conflict, verbatim).** `claims.json` C1
   `counting_commands` carries `python3 corpus/instruments/capture-binding-check.py -> records=40
   bound=40 unbound=0 exit=0 (unchanged C1 instrument baseline)`; the landed tree audits 41 records
   (`ExecCaptureBindingHarden.md` §Addendum: `records=41 bound=41 unbound=0`, `binding_exit=0`) and
   `.ufo/waves/round-34/claims-erratum-1.md` rules the literal a round-33 scope note with the
   predicate unchanged (`bound=records`, `unbound=0`). SHONEN box 2 cites the erratum rather than
   the stale literal.
6. **`kill-rule-check.py` red-green is narrower than "all shapes pinned".** The landed run is
   `survivors=0` over its 3 named mutants, but `ExecKillRuleCheck.md` §9b measures a fourth shape
   (`parse_round` non-round-directory archival exemption) as `killed=0`, `survivors=1` and discloses
   it as unpinned. SHONEN box 3 quotes both lines so the pointer cannot be read as a total kill.
7. **Old SHONEN box-2 parenthetical was stale** (see §1); corrected in place with the commit at
   which it was true (`9f98488`) and the commit that invalidated it (`5b7a039`).
8. **Carried, not mine:** `RevNoHarm.md` §D reports `baseline-plain.txt` misrooted at the fleet root
   during the wave (content-harm-free, author unattributable); `corpus/lessons/round-29.md` (+74)
   and `.ufo/waves/round-33/wave1/ScribeReportDraft.md` (+37) were appended by peer seats this
   round — both append-only per `RevNoHarm.md` §A, reported here so the L1's numstat re-run accounts
   for them.

### 6. Conflicts stated for the canonical judge

- C1 counting command says `records=40`; landed audit says `records=41` (erratum 1 supersedes the
  literal; cited above).
- C1 kill rule says `survivors>0` kills the claim; landed `survivors=0` over the named mutants while
  a measured fourth shape survives unpinned (§5 item 6).
- Box 3's assigned pointer expects `recheck-audit` 46/46 with exit 0; observed `strict pass=46/46`
  with `expect=present expected=45 … unexpected=1`, `recheck_exit=1` (§5 item 1).
- QUALITY R22 grounds itself in M34-2 while claims.json assigns M34-2 to the `<LANE_HASH>` defect
  (§5 item 4).

### 7. Scope, cleanup, tooling

- Commands run were read-only: `grep`, `wc`, `sha256sum`, `sed`, `git show`/`git diff`/`git status`,
  `python3 -c` JSON reads, one `python3 corpus/instruments/recheck-audit.py --quiet` (needed for the
  box-3 limb no receipt carries; attributed to this seat). No instrument was re-run to decorate
  another seat's numbers; all other figures are quoted from receipts with section anchors.
- Scratch removal, verified:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r34/ScribeShonen ; echo "rm_exit=$?"
rm_exit=0
$ ls -d /fast/scratch/hyaku/kasegi-r34/ScribeShonen ; echo "ls_exit=$?"
ls: cannot access '/fast/scratch/hyaku/kasegi-r34/ScribeShonen': No such file or directory
ls_exit=2
```

- Tooling: nothing installed or upgraded; no `pacman` transaction attempted under the host pause; no
  network fetch; no live bounty target contacted; no credential material read or reproduced.

Report: .ufo/waves/round-34/wave1/ScribeShonen.md
