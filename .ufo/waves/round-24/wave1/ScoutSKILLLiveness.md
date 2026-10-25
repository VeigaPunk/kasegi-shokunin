# ScoutSKILLLiveness — do SKILL.md brace/glob citations need the dispatch fix?

Round 24, read-only scout. Target: every `{`/`<` citation shape in
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md`, classified as
(i) literal hit today, (ii) only-via-brace, (iii) only-via-glob, (iv) dead under
every expansion, then checked against the real `resolve.py` CLI on a /tmp export.

## Verdict (findings first)

1. **On this host, zero SKILL.md citation resolves through brace or glob — all 39
   CLI-visible `{`/`<` shapes are class (iv).** The bounty tree and every mirror
   candidate are absent (`ls -d ~/Projects/bounties ~/Projects/the-bounty-hunter
   ~/Projects/origin-work/the-bounty-hunter` → three "No such file or
   directory"; the census prints `mirror … (ABSENT — mirror fallback disabled)`).
   The CLI agrees: 39/39 `GONE`, method column empty for all 39
   (`/tmp/kasegi-r24-scout/armA.tsv`). No class mismatch on this arm.
2. **The dispatch is nevertheless load-bearing for every genuine citation shape.**
   Each shape contains `{` or `<`, so its literal spelling is not the real
   filename — a literal hit would require a file named with brace/angle syntax,
   and there are 0 such hits in either world. 35 of 35 genuine shapes therefore
   resolve only via brace (12) or glob (23). In a probe world where only the
   trees SKILL.md asserts are present, 33/35 resolve (`12` brace, `21` glob) and
   2 stay dead. So the fix is not fixture-only — but its effect is *invisible on
   this host*, which is the exact bound the round needs.
3. **Three real-citation dispatch defects are reproducible, plus one credit-order
   property** (details D1–D4): the empty brace alternative is dropped
   (SKILL.md:1000), a brace alternative containing `<…>` is never globbed
   (SKILL.md:993/1002/1003), and glob `first-match` both *credits a dangling
   symlink that is not on disk* (SKILL.md:263, lane branch) and *suppresses a
   real second match* (SKILL.md:263, mirror branch → GONE while
   `mission-x.status.json` exists).
4. **The committed census receipt is stale:** `corpus/instruments/citation-survival.tsv`
   has 1480 distinct citations; the same instrument on the same committed bytes
   now emits 1669 (190 live-only, 151 rows differ). Any round claim that leans on
   that committed TSV is not re-derivable from committed bytes.
5. **The lane worktree already carries an r24 dispatch fix** (`git status` →
   `M corpus/instruments/resolve.py`, plus untracked
   `resolve-dispatch-check.py` / `resolve-dispatch-fixtures.json`). Run against
   those bytes: **no SKILL.md citation changes on this host (0/39, all still
   GONE)**, one changes in the seeded world (263), the empty-alternative fix
   restores `sighting.sh` only when no sibling exists, **D2 is untouched**, and
   the fix introduces one new false positive: `{}` flips GONE → INTERNAL
   (`/tmp/kasegi-r24-fixed/`), i.e. a JSON empty-object literal now "resolves" to
   the repo root. Details in "Fixed-bytes check".

## Inventory (exact, not grep-shaped)

46 backticked spans in SKILL.md contain `{` or `<`. Applying the resolver's own
`is_pathlike`/`strip_anchor` (`/tmp/kasegi-r24-work/inv.py` against the real
module): **39 are CLI-visible, 7 never reach the resolver** because
`is_pathlike` rejects them:

| ln | span | why invisible |
|---:|---|---|
| 24, 30, 823 | `[lost-tree] <path>:<line>` / `[lost-base] <path>:<line>` | space and no `/` |
| 366 | `validate: FAIL (<programs>, <lanes>, <errors>)` | space and no `/` |
| 400 | `import-board.mjs --from <board>` | space and no `/` |
| 854 | `ev = {}` | no `/`, no extension |
| 860 | `  <key> = <value> basis: <basis><detail>` | space and no `/` |

Of the 39 visible, 4 are path-like only by the extraction rule and are not
citations at all: 324 `(^|[^a-z])<b>([^a-z]|$)` (regex, noise=`synthetic`),
365 `/^\s{2}(\w+):\s*(\S+)\s*$/` (noise=`regex,synthetic`), 381
`ops/reroute-drill.mjs --simulate park:<lane>` (command line), 511
`detail: retired: <cls> — see docs/autopsies/<id>.md` (output shape). Nothing
can make these resolve, and substituting `*` for `<…>` turns them into glob
patterns that match nothing.

## Classification and CLI agreement (all 39 visible shapes)

`class today` = host world, `structural` = mechanism the token requires in any
world where its target exists, `armA` = real CLI on the /tmp export with the real
HOME, `armB` = real CLI with `HOME=/tmp/kasegi-r24-world/home
KASEGI_MIRROR=/tmp/kasegi-r24-world/mirror` over a seeded tree (probe, not a
host claim — seeds listed under "Repro").

| ln | token | class today | structural | CLI armA | CLI armB | armB method | armB credited path |
|---:|---|---|---|---|---|---|---|
| 56 | `evidence/<program>/scope-snapshot.json` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/evidence/openai/scope-snapshot.json` |
| 146 | `docs/autopsies/<program>.md` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/docs/autopsies/bugcrowd-openai.md` |
| 196 | `claims/<slug>/ingestion-20260914/` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/claims/bugcrowd-seek/ingestion-20260914/` |
| 236 | `rankings-<ts>.json` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/rankings-20260901T000000Z.json` |
| 239 | `evidence/<program-id>/` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/evidence/openai/` |
| 259 | `claim-ready/<id>/<slug>` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/claim-ready/claim-alpha/l1-scout.md` |
| 261 | `fleets/missions/<program>.md` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/fleets/missions/claim-alpha.md` |
| 263 | `fleets/run/<program>.status.json` | (iv) | (iii) † | GONE | GONE † | - | - |
| 324 | `(^\|[^a-z])<b>([^a-z]\|$)` | (iv) | (iv) shape-dead | GONE | GONE | - | - |
| 335 | `ledger/<kind>.jsonl` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/ledger/missions.jsonl` |
| 365 | `/^\s{2}(\w+):\s*(\S+)\s*$/` | (iv) | (iv) shape-dead | GONE | GONE | - | - |
| 369 | `.omp/agents/kx-<lane>.md` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/.omp/agents/kx-executor.md` |
| 381 | `ops/reroute-drill.mjs --simulate park:<lane>` | (iv) | (iv) shape-dead | GONE | GONE | - | - |
| 410 | `claim-ready/<id>/<slug>` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/claim-ready/claim-alpha/l1-scout.md` |
| 451 | `vdp-disclosures/<slug>/` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/vdp-disclosures/anthropic-x/` |
| 502 | `docs/autopsies/<id>.md` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/docs/autopsies/bugcrowd-openai.md` |
| 511 | `detail: retired: <cls> — see docs/autopsies/<id>.md` | (iv) | (iv) shape-dead | GONE | GONE | - | - |
| 539 | `claims/<program>/<slug>/` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/claims/bugcrowd-seek/honest-zero/` |
| 711 | `claim-packages/<slug>` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/claim-packages/claim-alpha` |
| 712 | `claims/<platform>-<program>/<slug>/` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/claims/bugcrowd-seek/honest-zero/` |
| 758 | `claims/<p>/<s>/` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/claims/bugcrowd-seek/honest-zero/` |
| 794 | `/reports/<id>` | (iv) | (iii), world-dead ‡ | GONE | GONE | - | - |
| 808 | `bounty-map/programs/<id>.json` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/bounty-map/programs/openai.json` |
| 901 | `ledger/rankings-<YYYYMMDDTHHMMSSZ>.json` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/ledger/rankings-20260101T000000Z.json` |
| 917 | `evidence/<id>/custodian-input.json` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/evidence/openai/custodian-input.json` |
| 985 | `~/Projects/bounties/ops/{claim-check,claim-index,prepare-claims,ev-report}.mjs` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/ops/claim-check.mjs` |
| 989 | `~/Projects/bounties/ledger/{missions,telemetry,candidates,imports}.jsonl` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/ledger/candidates.jsonl` |
| 990 | `~/Projects/bounties/evidence/<program>/` | (iv) | (iii) | GONE | RESOLVES | glob | `…/bounties/evidence/openai/` |
| 993 | `~/Projects/bounties/fleets/{missions/<id>.md,run/,leases.json,claimer-mission.md,review-mission.md,priority.json,state-snapshots/}` | (iv) | (ii) § | GONE | RESOLVES | brace | `…/bounties/fleets/claimer-mission.md` |
| 996 | `~/Projects/bounties/.ufo-{ingestion,warden}/` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/.ufo-ingestion/` |
| 998 | `~/Projects/bounties/ops/{validate,registry-check,reroute-drill,check-freshness}.mjs` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/ops/check-freshness.mjs` |
| 999 | `~/Projects/bounties/ops/{import-board,finalize-all}.mjs` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/ops/finalize-all.mjs` |
| 1000 | `~/Projects/bounties/ops/sighting{,-board,-dispatcher,-missions}.sh` | (iv) | (ii) ¶ | GONE | RESOLVES | brace | `…/bounties/ops/sighting-board.sh` |
| 1002 | `~/Projects/bounties/bounty-map/{schema.json,programs/*.json}` | (iv) | (ii) § | GONE | RESOLVES | brace | `…/bounties/bounty-map/schema.json` |
| 1003 | `~/Projects/bounties/.ufo-ingestion/{cycle-20260914T171257Z.md,rankings.md,claim-tracker.py,claim-ready-tracker.*}` | (iv) | (ii) § | GONE | RESOLVES | brace | `…/bounties/.ufo-ingestion/claim-tracker.py` |
| 1005 | `proposals/<Agent>.md` | (iv) | (iii) | GONE | MIRROR-EQUIVALENT | glob | `/tmp/kasegi-r24-world/mirror/proposals/L1.md` |
| 1008 | `~/Projects/bounties/.ufo/{grok-bounty-assessment-20260911,claim-recovery}/` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/.ufo/claim-recovery/` |
| 1009 | `~/Projects/bounties/.omp/{config.yml,agents/,skills/}` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/.omp/agents/` |
| 1010 | `~/Projects/bounties/{README.md,.gitignore}` | (iv) | (ii) | GONE | RESOLVES | brace | `…/bounties/.gitignore` |

† 263 is the dangling-symlink case, see D3. ‡ `/reports/<id>` needs glob but
`/reports` does not exist on this host or in the probe; it is genuinely dead, not
a dispatch failure. § brace alternative containing `<…>` or `*` is never globbed,
see D2. ¶ empty alternative dropped, see D1.

Structural tallies: 12 brace-only, 23 glob-only, 4 shape-dead, **0 literal**.
ArmB tallies: 13 `RESOLVES` (12 brace + 1 glob), 20 `MIRROR-EQUIVALENT` (all
glob), 6 `GONE`. Brace credits are decided by *sorted* alternative order, not
source order: 989 credits `candidates.jsonl`, 998 `check-freshness.mjs`, 999
`finalize-all.mjs`, 1010 `.gitignore`, 993 `claimer-mission.md`, 1000
`sighting-board.sh` — never the alternative the prose names first.

Byte pinning: `class today` and `CLI armA/armB` are committed bytes —
`resolve.py` sha256 `690153ad…ea2d` at master `c2480b14`. The worktree resolver
at read time is sha256 `99409e87…5013` (see "Fixed-bytes check"); the worktree
fixtures are `fef0f02d…4c8c`.

## Dispatch defects with real-citation evidence

### D1 — empty brace alternative is dropped (SKILL.md:1000)

`brace_expand` skips `""` (committed bytes `corpus/instruments/resolve.py:175`
`if not alt.strip(): continue`).

```
$ python3 -c "…brace_expand('~/Projects/bounties/ops/sighting{,-board,-dispatcher,-missions}.sh')"
['…/bounties/ops/sighting-board.sh', '…/bounties/ops/sighting-dispatcher.sh', '…/bounties/ops/sighting-missions.sh']
```

`sighting.sh` — the file SKILL.md itself cites by line anchor at 420–422
(`[lost-base] ops/sighting.sh:8`, `:12`, `:17`, `:18`, `:24`) and the first
alternative of the token — is not in the candidate set. Consequence, measured in
a world where only `ops/sighting.sh` exists (`/tmp/kasegi-r24-work/probe2.py`
P2): `exists_any → (None, None)`, `classify → ('GONE','','','bounty')`.
The verdict for line 1000 is *not* changed in the documented world (board,
dispatcher and missions are also asserted there, so brace still hits
`sighting-board.sh`), but the credit is the wrong file and the false-GONE is one
missing sibling away.

### D2 — a brace alternative's `<…>`/`*` is never globbed (SKILL.md:993, 1002, 1003)

`exists_any` tests each brace expansion with `os.path.exists` only; the single
glob attempt uses the *original, still-braced* string, and `{`/`}` are not in
`GLOBMETA` (`"*?["`), so the pattern cannot match
(committed bytes `resolve.py:188-196`).

Real token, only the placeholder alternative populated (`p8.py`):

```
token: ~/Projects/bounties/fleets/{missions/<id>.md,run/,leases.json,claimer-mission.md,review-mission.md,priority.json,state-snapshots/}
remaining under bounty fleets/missions: ['claim-alpha.md']
exists_any(bounty base) -> (None, None)
classify                -> ('GONE', '', '', 'bounty')
```

Same for line 1002 with `schema.json` absent and `programs/openai.json` present
(`exists_any → (None,None)`, `classify → GONE`) and line 1003 with only
`claim-ready-tracker.json` present (`exists_any → (None,None)`). When both a
plain alternative and the placeholder alternative exist, the plain one wins and
hides the defect (armB: 993 → `claimer-mission.md`, 1002 → `schema.json`, 1003 →
`claim-tracker.py`).

### D3 — glob first-match credits a missing file, and can hide a present one (SKILL.md:263)

*Lane branch, no confinement* — a dangling symlink is returned by `glob.glob`
and `exists_any` never re-checks existence, so `classify` reports a resolving
class for a path that is not on disk. Reproduced on the export
(`/tmp/kasegi-r24-scout/armC.tsv`) with
`fleets/run/mission-dangling.status.json -> /nonexistent/target.json`:

```
fleets/run/<program>.status.json	INTERNAL	/tmp/kasegi-r24-scout/fleets/run/mission-dangling.status.json	1	glob	rel	1	SKILL
test -e <that path> → NOT-ON-DISK
```

*Mirror branch, confined* — `under_mirror` realpaths the single first match. If
that match is the dangling link, the verdict is GONE and the second, real match
is never tried (`p7.py`):

```
first-match exists_any: ('glob', '/tmp/kasegi-r24-world/mirror/fleets/run/mission-dangling.status.json')
classify WITH dangling : ('GONE', '', '', 'rel')
classify WITHOUT dangling: ('MIRROR-EQUIVALENT', '…/mission-x.status.json', 'glob', 'rel')
real file on disk       : True
```

Both directions of the `first-match` rule are wrong on a citation the lane
actually makes 3 times (SKILL.md:263, `corpus/knowledge/*`).

### D4 — brace credit is whichever sorted alternative exists

Not a bug by itself, but it means a "resolves" verdict says nothing about the
alternative the sentence is about. 1010 credits `.gitignore` for a token whose
prose opens with `README.md`; 998 credits `check-freshness.mjs`; 1008 credits
`claim-recovery/` for a token naming `grok-bounty-assessment-20260911` first.
Combined with D2, a token can therefore resolve in a *different root* than the
tree it names: with the bounty `run/` and `claimer-mission.md` removed, line 993
classified `MIRROR-EQUIVALENT …/mirror/fleets/run/` while the bounty tree held
`fleets/missions/claim-alpha.md` (probe `probe2.py` P3).

## Fixed-bytes check (the worktree resolver already carries r24 changes)

The lane worktree is **not** at committed bytes: `git status --porcelain` shows
`M corpus/instruments/resolve.py`, `M corpus/instruments/source-recheck.py`, and
untracked `corpus/instruments/{resolve-dispatch-check.py,resolve-dispatch-fixtures.json,capture-source.py}`.
The worktree `resolve.py` differs from committed in three ways: empty brace
alternatives are kept (`resolve.py:176-183`, `sorted(set(out))`), the glob branch
returns the first **existing** match (`:198-202`), and it drops the round-23
`if not alt.strip(): continue`. Re-running the same two arms and the D1–D3
probes against those bytes (`/tmp/kasegi-r24-fixed`, byte-identical to the
worktree file):

| check | committed bytes | worktree bytes |
|---|---|---|
| 39 SKILL.md shapes, host world | 39 GONE | **39 GONE (unchanged)** |
| 39 SKILL.md shapes, seeded world | 6 GONE / 20 MIRROR-EQUIVALENT / 13 RESOLVES | 5 GONE / 21 MIRROR-EQUIVALENT / 13 RESOLVES — only 263 changes |
| D1, only `ops/sighting.sh` present | `('GONE','','','bounty')` | `('RESOLVES', …/sighting.sh, 'brace', 'bounty')` — fixed |
| D1, all four `sighting*` present | credits `sighting-board.sh` | still credits `sighting-board.sh` (empty alt sorts last: `sighting-board.sh` < … < `sighting.sh`) |
| D2, real 993 token, only `missions/<id>.md` alt populated | `(None,None)` / GONE | **`(None,None)` / GONE — unfixed** |
| D3, mirror dangling + live `mission-x.status.json` | GONE (real file hidden) | `MIRROR-EQUIVALENT …/mission-x.status.json` — fixed |
| D3, mirror dangling only | GONE | GONE (correct) |
| `{}` (corpus/knowledge/triage-thresholds.md:71,366) | GONE | **INTERNAL `/tmp/kasegi-r24-fixed/`** — new false positive |

Three consequences for the round:

1. **The fix is invisible in SKILL.md on this host.** 0/39 change; every change
   the fix produces lives in `corpus/**` or in fixture worlds. A C1 counter-B
   receipt is therefore a fixture receipt by construction, and this report is the
   measurement of what those fixtures stand in for.
2. **D2 survives the fix.** No fixture case in `resolve-dispatch-fixtures.json`
   has a brace group containing `<…>` or `*` (checked: 0 of 8 cases and 3 extra
   cites), and no case has both the empty-alternative file and a sibling present,
   so the L1/L2 assertions cannot see the credit-order behaviour at
   SKILL.md:1000. Adding one case (`fleets/{missions/<id>.md,run/}` with only
   `missions/claim-alpha.md` on disk) and one (`ops/sighting{,…}.sh` with all four
   present, expecting `sighting.sh`) would close both.
3. **`{}` is not a brace expression.** In shell, `{}` is literal; only `{,x}` /
   `{x,}` / `{x,y}` expand. Treating `{}` as "one empty alternative" makes the
   bare token `{}` resolve to its parent directory, which turns two
   `corpus/knowledge/triage-thresholds.md` citations of a JSON empty object into
   INTERNAL "resolutions". Requiring at least one `,` inside the braces (or
   rejecting the whole group when `m.group(1) == ""`) preserves L1/L2 and drops
   the false positive.

## Falsifier for the round's framing

The claim the dispatch fix is tested against is "it matters for real citations".
Measured bound:

- **On this host it changes nothing:** 39/39 shapes are GONE either way, and no
  SKILL.md token ever reaches `brace_expand` or `glob.glob` (39/39 method column
  empty). The whole live census has exactly two brace-method rows and both are
  lane-internal, not SKILL.md citations:
  `.ufo/waves/round-23/c2-recheck-S0{18,29,30,31}.txt` → `.ufo/waves/round-23/c2-recheck-S018.txt`
  and `corpus/lessons/round-{1,4,5,6}-aggregator-audit.md` →
  `round-1-aggregator-audit.md` (`/tmp/kasegi-r24-work/base-host.tsv`, method=brace).
- **Against a populated tree it decides 33 of 35 genuine citations** (12 brace,
  21 glob), i.e. every one of them: literal can never hit because each shape
  contains `{` or `<`, and no filesystem target is literally named that way.
- **The host cannot fall back:** `~/Projects/bounties` and both mirror
  candidates are absent, `MIRROR_ABSENT` is true, so a "fixed" dispatch cannot
  be demonstrated end-to-end from committed bytes alone. Any C1 counter-B
  receipt claiming 8/8 must therefore be a fixture receipt, and this report is
  the evidence that the fixtures stand in for 35 real citations rather than for
  zero.

## Repro

Trees (all /tmp, nothing written into the lane):

- `/tmp/kasegi-r24-base` — committed bytes: `git archive master | tar -x -C …`
  plus `cp -a <lane>/.git`. Authoritative receipts:
  `/tmp/kasegi-r24-work/base-host.tsv`, `base-seeded.tsv`.
- `/tmp/kasegi-r24-fixed` — worktree bytes: `tar -cf - --exclude=.git . | tar -xf - -C …`
  plus `.git`. Receipts `armA2.tsv`, `armB2.tsv`.
- `/tmp/kasegi-r24-scout` — first export (committed bytes) used for the per-token
  table; receipts `armA.tsv`, `armB.tsv`, `armC.tsv` (lane dangling fixture),
  `final.json`. One scratch file of mine (`final.json`) sat in that export while
  the first armA ran and was globbed by the `<slug>.json` citation; no token in
  the 39-token set was touched by it, and the pristine re-run confirms
  `<slug>.json` = GONE, `{}` = GONE at committed bytes.
- `/tmp/kasegi-r24-work` — scripts: `inv.py`, `cls.py`, `final.py`,
  `probe2.py` (P1–P6), `p7.py` (D3 mirror), `p8.py` (D2 real token),
  `probe_fixed.py` (D1–D3 against worktree bytes).

```
python3 /tmp/kasegi-r24-base/corpus/instruments/resolve.py /tmp/kasegi-r24-base   # host → base-host.tsv
HOME=/tmp/kasegi-r24-world/home KASEGI_MIRROR=/tmp/kasegi-r24-world/mirror \
  python3 /tmp/kasegi-r24-base/corpus/instruments/resolve.py /tmp/kasegi-r24-base # seeded → base-seeded.tsv
# same two commands with /tmp/kasegi-r24-fixed → armA2.tsv / armB2.tsv
```

Seeded probe world (`/tmp/kasegi-r24-world`, built only from paths SKILL.md
asserts, plus the two fixtures). Bounty tree under the fake HOME: `ops/` the 10
`.mjs` named at 985–999 + `sighting{,-board,-dispatcher,-missions}.sh`;
`ledger/{missions,telemetry,candidates,imports}.jsonl`;
`fleets/{missions/claim-alpha.md,run/mission-x.status.json,leases.json,claimer-mission.md,review-mission.md,priority.json,state-snapshots/}`;
`.ufo-ingestion/{cycle-20260914T171257Z.md,rankings.md,claim-tracker.py,claim-ready-tracker.json}`;
`.ufo-warden/warden.log`; `.ufo/{grok-bounty-assessment-20260911,claim-recovery}/`;
`.omp/{config.yml,agents/kx-executor.md,skills/}`; `bounty-map/{schema.json,programs/openai.json}`;
`evidence/openai/scope-snapshot.json`; `docs/autopsies/bugcrowd-openai.md`;
`claims/bugcrowd-seek/ingestion-20260914/`; `README.md`, `.gitignore`.
Mirror: `evidence/openai/{scope-snapshot,custodian-input}.json`, `docs/autopsies/bugcrowd-openai.md`,
`fleets/{missions/claim-alpha.md,run/mission-x.status.json}`, `ledger/{missions.jsonl,rankings-20260101T000000Z.json}`,
`.omp/agents/kx-executor.md`, `vdp-disclosures/anthropic-x/SUBMITTED.md`,
`claim-packages/claim-alpha`, `claims/{bugcrowd-seek/honest-zero,openai/claim-alpha,p/s}`, `claim-ready/claim-alpha/l1-scout.md`,
`bounty-map/programs/openai.json`, `proposals/L1.md`, `rankings-20260901T000000Z.json`,
plus fixture `fleets/run/mission-dangling.status.json -> /nonexistent/target.json`.
The probe uses the same fake-HOME + `KASEGI_MIRROR` method the repo's own
`corpus/instruments/test_resolve.py` documents, so it does not invent a technique.

## Remaining unknowns

- Which of the four `sighting*` scripts existed at the last verified base is
  UNVERIFIED: the bounty tree is gone and only prose (`SKILL.md:418-423`) and
  `corpus/knowledge/mission-control.md:107,133-135` remain. D1's false-GONE
  therefore needs one missing sibling that the documentation does not rule out,
  not one it asserts.
- Whether `bounty-map/schema.json` exists at the last base is UNVERIFIED; line
  1002 and the corpus cite it, so D2's 1002 variant is conditional on it being
  absent.
- The worktree `resolve.py` is uncommitted and may change again before the round
  closes; "Fixed-bytes check" describes sha256 `99409e87…5013` at 2026-10-25
  ~04:20Z. If those bytes move, re-run `probe_fixed.py`, not this prose.
- No live-target contact, no installs, no writes outside `/tmp` and this file.
