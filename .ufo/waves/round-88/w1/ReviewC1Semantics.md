# C1 semantic review — round 88 attempt 1 (seat ReviewC1Semantics)

Commits: base `6beead91`, freeze `7f2ebebf`, C1 landing `fd33e1bf`. Scope: the 50 keys of
`.ufo/waves/round-88/c1/repair-map.json` (73 added citation sites on 64 added lines) and a
15-key sample of the 54 `anchor-content-drift` exclusions in `excluded.json`. No lane file was
edited. `git diff 6beead91 7f2ebebf -- corpus/knowledge/` is empty, so cited ranges read at
base are the freeze/landing ranges.

Judgment question per key: do the cited sibling entry and (for anchored keys) the cited
base-revision line range support the sentence or table row that cites it at `fd33e1bf`.

## 0. Landing-shape checks (pass)

- `r1-landing-diff.txt`: the landing is a **pure `corpus/knowledge/` prefix insertion** on 64
  lines in 8 files; stripping the inserted prefix reproduces the base byte-for-byte on every
  line (`residual=0`), and line counts are unchanged in all 8 files, so no anchor shifted and
  no cited entry was edited.
- All 50 map keys appear as added citations; no added citation falls outside the map
  (`keys=50, sites=73`). 23 of the 73 sites belong to the 13 unanchored keys.

## 1. Per-key verdicts (50)

Verdicts: CORRECT = the cited entry/range states the cited content; WRONG = the cited range does
not contain the cited content (a different range does) or the referent is not the lane entry;
UNCLEAR = thematic/near match, neither stated nor contradicted. Line numbers are base-revision.

| key | sites | verdict | basis |
|---|---|---|---|
| authorization-safe-harbor-and-scope.md | 1 | CORRECT | authorised-testing:74 points at the F03 rule; entry L7-8 hold precisely that safe-harbour/scope rule |
| citation-bases.md | 1 | CORRECT | root-loss:53 "carries the vocabulary"; entry L1-6 is that vocabulary |
| claim-gates.md | 5 | CORRECT | 130 paraphrases `claim-package-check.py:4-8`, which literally writes `corpus/knowledge/claim-gates.md`; 154 narrates the SHONEN row; 36/42/473 are companion/reading mentions |
| claim-gates.md:15 | 2 | CORRECT | L15 states both report.md phrase gates (185, 186) |
| claim-gates.md:16 | 1 | CORRECT | L16 `OPERATOR-GATED` (187) |
| claim-gates.md:20 | 2 | CORRECT | L20 sequence number + `expected_head_sha256` key (196, 197) |
| claim-gates.md:21-23 | 4 | **WRONG (1/4)** | 177 = package-root `realpathSync(dir)` gate; L21-23 is artifact-level confinement only and says nothing about the package root. 198/199/200 are correct |
| claim-gates.md:22-23 | 1 | CORRECT | L23 "sha256 matches" (201) |
| claim-gates.md:23 | 1 | CORRECT | L23 polarity set (202) |
| claim-gates.md:24 | 1 | CORRECT | L24 ≥1 positive-polarity artifact (203) |
| claim-gates.md:25-27 | 2 | CORRECT | L25-27 receipt equality, distinct identities, receipt→manifest binding (204, 205) |
| claim-gates.md:26 | 1 | CORRECT | L26 non-empty distinct producer/verifier (206) |
| claim-gates.md:27 | 2 | CORRECT | L27 producer≠verifier and receipt binding a manifest digest (207, 208) |
| claim-gates.md:31 | 1 | CORRECT | L31 non-empty `chain`/`decisions` (218) |
| claim-gates.md:32-33 | 3 | CORRECT | L32-33 `NO_SCOPE_OBJECTION` plus the HARD_STOP two-error statement (219, 220, 444) |
| claim-gates.md:33-34 | 1 | CORRECT | L34 non-empty `matched_grant_id` (221) |
| claim-gates.md:34 | 1 | **WRONG** | 222 is the `decision_sha256` regex row; L34 is `matched_grant_id`, the regex is L35. The M8 pass came from the unrelated word `decision` in "two errors for one decision" |
| claim-gates.md:35-36 | 3 | **WRONG (1/3)** | 223/224 correct; 225 (three-way `manifest.expected_head_sha256` binding) needs L36-37 — L37 carries the manifest leg and the range stops at 36 |
| claim-gates.md:4-5 | 1 | UNCLEAR | L4-5 state exit-1/OK discipline for gate failures; row 176 is the usage preflight (`claim-check.mjs` L14-15), which the entry never covers |
| claim-gates.md:63-66 | 1 | **WRONG** | L63-66 = §4 pointer, blank, "## status.json gates" heading, blank; the not-claimable heuristics are L78-80. M8 passed on the heading word `status` |
| claim-gates.md:66-67 | 1 | **WRONG** | L66 blank, L67 `state === 'DONE'`; the prior-submission guard is L81-85. M8 passed on `SUBMITTED` in the neighbouring bullet |
| claim-package-contract.md | 3 | CORRECT | 154 SHONEN rows; 440 = entry L18-26 contract-by-convention note; 475 reading list |
| claim-package-contract.md:11 | 1 | CORRECT | L11 report.md "No submission performed" marker (186) |
| claim-package-contract.md:13 | 2 | CORRECT | L13 `schema_version`, polarity, redactions (203, 242) |
| claim-package-contract.md:14 | 1 | CORRECT | L14 `head_sha256 == manifest.expected_head_sha256` (225) |
| claim-package-contract.md:28-29 | 1 | **WRONG** | L28 blank, L29 "## status.json semantics" heading; hard gates are L52-53. M8 passed on the heading word `status` |
| ev-model.md | 2 | CORRECT | companion (37) and reading-list (473) mention |
| intake-surface.md | 1 | CORRECT | reading-list mention (474) |
| japanese-domestic-disclosure-workflow.md | 1 | **WRONG** | line 7 is a *file-name mention* of the staged package entry under `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/` (the parenthetical gives that root). The repoint invents a lane path for the upstream and makes the line cite itself; the staged file was not moved into the lane |
| mission-control.md | 1 | CORRECT | reading-list mention (474) |
| mission-control.md:19 | 1 | CORRECT | L19 priority +9e12 (86) |
| mission-control.md:19-20 | 1 | CORRECT | L20 continue +2e12 (87) |
| mission-control.md:20-24 | 1 | CORRECT | L21-22 "live leases … filter the candidate set" (57) |
| mission-control.md:21 | 1 | CORRECT | L21 "`DONE` never redispatches" (60) |
| mission-control.md:21-23 | 1 | CORRECT | L23-24 round-13 correction, dead `ev_note` branch (436) |
| mission-control.md:43-46 | 1 | **WRONG** | 150 ties `SYNC_PATHS` to commit-message/byte-proof lines. `SYNC_PATHS` is L68-70, which lists **8** names (claims/README, evidence, ledger, docs, ops, fleets/missions, registry, mission-template), not the 11 the row claims — the row has no supporting line at base either, and the repoint now makes it look verified |
| ops-invariants.md | 3 | CORRECT | companion (37, 42) and reading-list (474) mentions |
| ops-invariants.md:19 | 1 | CORRECT | `PARKED` `[]` (391) |
| ops-invariants.md:20 | 1 | CORRECT | `K3_SEATS` (392) |
| ops-invariants.md:21 | 1 | CORRECT | `K3_TOKEN` (393) |
| ops-invariants.md:22 | 1 | CORRECT | `TELEMETRY_EVENTS` (394) |
| ops-invariants.md:23 | 1 | CORRECT | `sha256File` (395) |
| ops-invariants.md:24 | 1 | CORRECT | `gitMutationBlocker` (396) |
| ops-invariants.md:25 | 1 | CORRECT | `appendLedger` 3500-byte cap (397) |
| ops-invariants.md:34-40 | 2 | CORRECT | L34-40 subset validator (366, 381) |
| ops-invariants.md:41-42 | 1 | CORRECT | L41 `--strict` non-empty `ev_inputs` (382) |
| triage-thresholds.md | 1 | CORRECT | claim-gates:160 points at §4 (its own L63) |
| ufo-workspaces.md | 2 | CORRECT | root-loss:21 (claim recorded at entry L169-170); root-loss:68 lists the entry among re-anchored ufo-fsd citations |
| vendor-disclosure-policies-as-corpus-objects.md | 1 | CORRECT | pz:52 pointer to the F10 entry (ground L9); the contrast clause itself is not located in that entry |
| vendor-disclosure-policy-commitments-crosswalk.md | 1 | CORRECT | iso:60; entry L46 carries the Cisco–ISO 29147 row and the quoted claim |

Tally: **41 CORRECT / 8 WRONG / 1 UNCLEAR**. WRONG keys: `claim-gates.md:21-23` (1/4 sites),
`:34`, `:35-36` (1/3), `:63-66`, `:66-67`, `claim-package-contract.md:28-29`,
`mission-control.md:43-46`, `japanese-domestic-disclosure-workflow.md`.

Mention flags (not content citations, so "support" is only referent correctness):
`claim-gates.md` @130 (inside a paraphrase of the instrument docstring — faithful), 36/42/473;
`claim-package-contract.md` @154/475; `ev-model.md` @37/473; `intake-surface.md`, `mission-control.md`,
`ops-invariants.md` @474/37/42 (companion and "files read" lists); `citation-bases.md` @53;
`ufo-workspaces.md` @68; `vendor-*` @pz:52 / iso:60 (entry pointers). 16 of the 23 unanchored
sites are mention-only; 5 are pointers to content; 2 (`claim-package-contract.md` @440,
`ufo-workspaces.md` @21) are content citations. No key sits inside a command string. One unanchored key names a **foreign file of the same name** rather than
the lane entry: `japanese-domestic-disclosure-workflow.md` (staged shokuknow package copy, not a
lost-tree file, but the same failure mode the prompt asks about). Every other unanchored key's
basename resolves to the lane entry.

## 2. Excluded-sample (15 of 54 `anchor-content-drift` keys)

Reproduced the exclusion rule first: re-implementing the counter's `idents()` and citing-site
scan reproduces **54/54** reason strings exactly (`r3-exclusion-accounting.txt`), so the
exclusions are generated, not hand-written — the defect is the rule, not honesty.

| excluded key | sites | verdict | basis |
|---|---|---|---|
| claim-gates.md:10-11 | 2 | **proxy false negative** | L10-11 list exactly the six required files; both citing rows (178, 179) are supported |
| claim-gates.md:5-6 | 1 | drift confirmed | 445 is about the artifact-loop early exit; L5-6 are the provenance/`OK` sentence |
| claim-gates.md:71-74 | 2 | drift confirmed | nested readiness is L88-91; L71-74 are `claim_ready`/reviewer bullets |
| claim-package-contract.md:15 | 1 | **proxy false negative** | 241 says "the provenance fields enumerated in :15 are unenforced"; L15 is that provenance row. The entry is already lane-qualified at `claim-package-gate.md:15`, so the exclusion leaves one qualified and one bare citation of the same target |
| claim-package-contract.md:9-16 | 1 | **proxy false negative** | 178 needs the six-file list; L9-16 is the six-file table |
| ev-model.md:15-16 | 1 | drift confirmed | 367 is the `p_*` schema bound; L15-16 are `gross_value`/`total_cost` |
| ev-model.md:22-23 | 2 | drift confirmed | 369/370 are `deadline` and `duration_p90`; L22-23 are inputs/`as_of`/`sources` |
| intake-surface.md:71 | 2 | drift confirmed | 86/87 are queue weights; L71 is `evidence/`/`claims/` coverage counts |
| intake-surface.md:75-76 | 1 | drift confirmed | 437 is reward counts; L75-76 are name-drift pairs |
| mission-control.md:20-21 | 4 | drift confirmed; 1 site suppressed | 58/59/144 unsupported (attempts, readStatus, MAX_ATTEMPTS); 90 (`freshness.live` +1) *is* supported by L21 |
| mission-control.md:36-38 | 3 | drift confirmed | 146/153/154 are model and off-peak rows; L36-38 is the sweep |
| mission-control.md:42-46 | 1 | drift confirmed | 149 is `--sync` cadence (`every 10 ticks`, L68); L42-46 is the commit message |
| ops-invariants.md:18 | 2 | 1 site suppressed | 390 (`BANNED`) passes M8 and is supported by L18; the other site is a quotation of the *bad* bare form in `citation-bases.md:14`, correctly left alone |
| ops-invariants.md:17-25 | 1 | **proxy false negative** | 455 ("shared constants table") is exactly L17-25 |
| ufo-archive-2026.md:31 | 1 | mention-class, inconsistent | root-loss:68 has no identifiers at all (its only span is the citation); the sibling `ufo-workspaces.md` in the same parenthetical *was* repointed, leaving one bare and one qualified in one sentence |

**False-negative count: 4 of 15 keys are outright proxy false negatives** (every citing site is
supported: `claim-gates.md:10-11`, `claim-package-contract.md:15`, `claim-package-contract.md:9-16`,
`ops-invariants.md:17-25`); **6 of 15 suppress at least one valid repoint** (add
`mission-control.md:20-21` site 90 and `ops-invariants.md:18` site 390); **7 of 15 are not
justified by content drift** once the mention-only `ufo-archive-2026.md:31` is counted.

Mechanism (all reproduced): a citing line's identifiers are 5+ character words inside backticked
or double-quoted spans **with path-like spans dropped**, so a pointer line whose only span is the
citation has an empty identifier set and fails by construction
(`claim-package-contract.md:15`, `claim-package-contract.md:9-16`, `ops-invariants.md:17-25`,
`claim-gates.md:5-6`, `ufo-archive-2026.md:31`). Exclusion is also all-or-nothing per key: one
mention-only site poisons the whole key (`ops-invariants.md:18`, `mission-control.md:20-21`).
The corpus's own conformance matrix (`triage-thresholds.md` L450-458, "Prior claim | Location |
Status") is exactly this shape, so the proxy systematically excludes pointer-table rows.

## 3. Routed defects (recommendation, never re-scoring)

**R1 (high, referent).** `japanese-domestic-disclosure-workflow.md` line 7 must revert to the bare
`japanese-domestic-disclosure-workflow.md`: the referent is the staged package copy under
`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`, and the landing now
presents a lane path as if it lived under that root and cites itself. Neither limb could catch
this: M4's basename-uniqueness test scans tracked lane files only, and M8 exempts unanchored
keys, so an out-of-repo file of the same name is invisible to both.

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git show 6beead91:corpus/knowledge/japanese-domestic-disclosure-workflow.md | sed -n 7p
git show fd33e1bf:corpus/knowledge/japanese-domestic-disclosure-workflow.md | sed -n 7p
ls /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md
```

**R2 (high, M8 false positives).** 7 anchored keys pass M8 on a boilerplate, neighbouring, or
subject-mismatched identifier while the cited range lacks the cited content; the correct anchors are `claim-gates.md:34`→L35,
`:35-36`(225)→L36-37, `:63-66`→L78-80, `:66-67`→L81-85,
`claim-package-contract.md:28-29`→L52-53, `mission-control.md:43-46`→L68-70 (which still does
not state 11 `SYNC_PATHS` entries — the row overstates its companion), and
`claim-gates.md:21-23`(177) has no supporting line (drop the tie). Re-runnable evidence for any
key (read-only; prints the citing line's identifier set and the cited range's shared set):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
KEY='claim-gates.md:63-66' python3 -B - <<'PY'
import subprocess,re,os
base='6beead9148945fa695cf3139e8fc9d8e91cc5fd0'; key=os.environ['KEY']
WORD=re.compile(r"[A-Za-z_][A-Za-z0-9_]{4,}")
PL=re.compile(r"^[\w./~-]+\.(?:md|mjs|js|py|json|jsonl|txt|tsv|sh)(?::[\d,-]+)?$")
def idents(l):
    out=set()
    for sp in re.findall(r"`([^`]+)`",l)+re.findall(r'"([^"]+)"',l):
        if not PL.match(sp.strip()): out|=set(WORD.findall(sp))
    return out
name,_,rng=key.partition(':'); lo=int(rng.split('-')[0]); hi=int(rng.split('-')[1]) if '-' in rng else lo
tgt=subprocess.run(['git','show',base+':corpus/knowledge/'+name],capture_output=True,text=True).stdout.split('\n')
tw=set(WORD.findall('\n'.join(tgt[lo-1:hi]))); print('range words:',sorted(tw))
for f in subprocess.run(['git','ls-tree','--name-only',base,'corpus/knowledge/'],capture_output=True,text=True).stdout.split():
    for i,l in enumerate(subprocess.run(['git','show',base+':'+f],capture_output=True,text=True).stdout.split('\n'),1):
        if '`%s`'%key in l:
            print(f+':'+str(i),'shared=',sorted(idents(l)&tw),'idents=',sorted(idents(l)))
PY
```

**R3 (medium, exclusion rule).** 6 of 15 sampled exclusions suppress a supported repoint; e.g. the
`triage-thresholds.md` conformance rows stay bare (`claim-gates.md:10-11` @178,
`claim-package-contract.md:9-16` @178, `claim-package-contract.md:15` @241, `ops-invariants.md:18`
@390, `ops-invariants.md:17-25` @455) and `mission-control.md:20-21` @90, although `citation-bases.md:13` already states the
lane-qualified convention. A pointer line (span = the citation only) must not be treated as
evidence against the key; run the identifier check per *site* and exclude only the failing sites.

**R4 (medium, instrument blind spot).** No frozen limb reads `excluded.json`:
`grep -n excluded .ufo/waves/round-88/c1/knowledge-meter.py` returns only the M8 docstring phrase;
M8 skips unanchored keys and only covers map keys. The exclusion set's semantics are therefore
unfalsifiable by the counter (reproducible only by re-running the pinned `build-map.py`).

**R5 (low, coverage).** Three comma-list citations of knowledge entries remain bare
(`triage-thresholds.md:440`, :453, :457) because the map key grammar cannot express
`:N-M, N-M`; one composite (`claim-gates.md:3-6` at :453) is in neither the map nor
`excluded.json`. Counted outside M1, this is not a landing defect but bounds what "742/1743"
covers.

## 4. Residual risk / verification gaps

- Verdicts are semantic judgments over base-revision bytes; I did not re-run the frozen counter
  or the C2 checks. The M8 reproduction is my implementation of its documented rule and matches
  54/54 recorded reasons, but I did not execute `knowledge-meter.py` itself.
- The 39 exclusions not sampled could contain further false negatives at the same rates; the
  mechanism is structural (empty identifier sets, all-or-nothing keys), so I expect the rate to
  hold for the pointer-table-shaped keys especially.
- The landing cannot make any anchored citation *correct* — it only makes it openable. Of the 50
  keys, 8 still point at content they do not state, so the "verifiable" reading of the tranche
  needs the qualifier "openable, not yet checked".

## Files written

- `.ufo/waves/round-88/w1/ReviewC1Semantics.md` (this report)
- `.ufo/waves/round-88/w1/ReviewC1Semantics-receipts/r1-landing-diff.txt`
- `.ufo/waves/round-88/w1/ReviewC1Semantics-receipts/r2-m8-identifier-evidence.txt`
- `.ufo/waves/round-88/w1/ReviewC1Semantics-receipts/r3-exclusion-accounting.txt`
- `.ufo/waves/round-88/w1/ReviewC1Semantics-receipts/r4-excluded-sample.txt`
