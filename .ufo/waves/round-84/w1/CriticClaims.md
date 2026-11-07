# CriticClaims — round 84 attempt 1 (C1 depth:verifiability, C2 coverage)

Seat: critic (leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`a089ff3d601b4d53a5515e52720ba27e5ec72c3d`, freeze `7f76b7eb690cd6e75e7f3e7729cedcb15611b34b`
(`git rev-parse HEAD` = the freeze). Scratch `/fast/scratch/hyaku/kasegi-r84/CriticClaims`
(deleted before yield). Every command below was run from the lane root on frozen bytes or on an
exact scratch copy; no lane byte was written. Receipts in `CriticClaims-receipts/`.

## 0. Frozen bytes and first-hand predicates

| artefact at 7f76b7e | sha256 |
|---|---|
| `.ufo/waves/round-84/c1/recheck-cwd-census.py` | `e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e` (P2 target) |
| `.ufo/waves/round-84/c1/mutbat.py` | `c67e6912ca52dcef6c1722882e3d3b725f40a56703d65bdee402a4c8e738d6ea` |
| `.ufo/waves/round-84/c1/mutant-table.json` | `daf05baceae8efcdce8d3968a57472b86d92de224227d311f2047fc7b677aa9e` |
| `.ufo/waves/round-84/c1/build-table.py` | `4352368e28437e3826e34689a50e83b65d874f08aef60cfe92cb8f248f4a7516` |
| `.ufo/waves/round-83/c2/entry-gate.py` | `42f4b2accf704455325f8d1eb8ca4ec21401e35397af7a36861c33a27ace6302` (r83 bytes) |
| `corpus/source-snapshots/round-84/S118.txt` | `e824a73545bedd0abae5f84cd120a5c73e482d7e935bc1534a08a1e1adfa5359` |
| `corpus/source-snapshots/round-84/manifest.json` | `80129310e4880f857a0c2225f028ac8e5985ceff21ad5d5496c1867a7de0a65a` |

`git status --porcelain .ufo/waves/round-84/controls .ufo/waves/round-84/c1` is empty; the six
control files named by C1's P7 are tracked at the freeze (`c1-freeze-pins.txt`,
`c1-p7-controls.txt`).

First-hand at the frozen candidate (not read from the receipts): P1 `selftest cases=33
failures=0` rc 0; P3 full battery rc 0 in 120.29 s with the exact claimed line
`MUTBAT target_sha256=e5f2e4… baseline=ok rows=79 killed=76 survived=0 miskilled=0 dirty=0
notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=75/76`, and the two greps 76 / 12
(`c1-p1-candidate-selftest.txt`, `c1-mutbat-candidate-firsthand.txt`); P4 `mutbat selftest ok`,
`r84_limbs={'extra': True, 'dup': True, 'decoy_line': True}` rc 0; P5 M09/M10/M12
`r83 rc=0/ok` → `r84 rc=1/FAIL`, `COUNTER-MUTANTS-RESULT as-expected`; P6 `RECHECK-CWD entries=98
… RECHECK-CWD-RESULT conformant` rc 0; P7 both controls print 12 `H.. verdict=SURVIVED` lines and
end `rc=1`. P2/P8 are landing obligations; P8 currently reads `cases=27` at `SKILL.md:982` and
`corpus/instruments/README.md:354` (must read 33 at landing).

## 1. C1 — attacks

### A1 — the 76/76 kill tally is forgeable: a target that tests nothing scores the same line

Attack: the frozen candidate `e5f2…` plus a preamble inserted before
`if __name__ == "__main__":` that redefines `selftest()` to (i) strip its own pre-marker bytes,
(ii) read `.ufo/waves/round-84/c1/{recheck-cwd-census.py,mutant-table.json}` and compute each
row's mutant of the frozen head, and (iii) print one `selftest case=<kill_case> FAIL` per
`kill_cases` when its own bytes equal a table mutant, else print 33 fake `ok` lines. No
instrument assertion runs; neutral rows are skipped in the lookup (they are not mutants). The
real instrument's anchors are untouched, so the table derives on it (`notderived=0`).

```
$ python3 -B .ufo/waves/round-84/c1/mutbat.py --target <scratch>/recheck-cwd-forged.py \
    --table .ufo/waves/round-84/c1/mutant-table.json --expect-cases 33 --work <scratch>
...
DECOY keyed=yes nonce=3da884cd9ae05762 d3_row=K-M8
MUTBAT target_sha256=b5c597bddbbf9ae8319bc458df7cb4ed47fe81c3eda404af5af081afa67c28c6 baseline=ok rows=79 killed=76 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=75/76
rc=0
```

`killed=76`, `survived=0`, `neutral_ok=3/3`, `decoy=ok`, all twelve `H.. verdict=KILLED`
(`c1-attack-a1-forgery.txt`, forgery at `forgery-table-lookup.py`). The keyed D1/D2/D3 decoys do
not stop it: D1/D2 drop the marker comment and D3 adds one at one anchor line, so none of the
three equals a table mutant; the nonce is visible but unused. This is the r83 F12 class
(marker-aware table-reading forgery), reproduced under the r84 counter whose decoy code is
byte-identical (only the selftest limbs changed, `c1-counter-r83-to-r84.diff`).

Verdict: **claim survives as written** — P2/P3 pin `target_sha256=e5f2…`, the forgery's sha is
`b5c5…`, and the claim explicitly says "Not claimed: the F8/F12/F13 forgery class (recorded
limits carried from r83)". The correct reading of the measured move is *discrimination against
the landed r83 bytes and the check-name stub*, not proof that the six checks test anything; the
real evidence for the six checks is the source diff, which does close H01–H12 (A4). The forgery
does not falsify any predicate and cannot satisfy P2/P3's sha pin.

Impacted axis: depth:verifiability (evidence semantics only; no score move claimed). Smallest
safe correction: the r83 routed defect 1 is only half answered — `claims.json` carries F12/F13,
but the counter docstring's known-limit sentence still names only F8 and `mutbat --selftest` has
no F12/F13 case. Name F12/F13 beside F8 in the docstring and record this forgery in the counter
selftest block as a *documented accepted* class (a decoy cannot reject a table lookup that is
exact-byte; only the sha pin plus review can), or say in P3 that the sha pin is the identity limb
and the row counts are counter self-consistency only.

### A2 — P3's per-row grep: target cannot inject MUTANT lines; the grep adds counter self-consistency only

Attack: a toy target that prints, at selftest start, `MUTANT T-KILL verdict=KILLED …` and
`MUTBAT target_sha256=e5f2 baseline=ok rows=99 killed=99`, scored on a 2-row table.

```
$ python3 -B .ufo/waves/round-84/c1/mutbat.py --target <scratch>/toy.py --table <scratch>/table.json --expect-cases 2 --work <scratch>
MUTANT T-KILL verdict=KILLED rc=1 fails=1 failed_cases=a counted=yes
MUTANT T-NEU verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
DECOY keyed=yes nonce=d387f3df2220c3bf d3_row=T-KILL
MUTBAT target_sha256=5775272f09a7da01c3bc52f818c56a4698b30d379cbe493b5d944980f0c2eaa4 baseline=ok rows=2 killed=1 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=1/1 decoy=ok decoy_hidden=1/1
rc=0
```

Neither forged line appears; the counter prints its own rows (`c1-attack-a2-injection.txt`).
Verdict: **claim survives**; the per-row grep is not target-forgeable and would catch a counter
that drops or duplicates rows, but it is computed from the same target-controlled `FAIL` lines as
the summary, so it adds nothing against a target that controls verdicts. The substantive answer
to the r83 spot-check defect 2 is the `target_sha256` pin, which P3 now carries. P3's wording
("the counter's own per-row lines") is literally true; no overreach.

### A3 — do-nothing and stub controls, and the F8/F12/F13 carry

- `c1-donothing-r84.txt`: r83 bytes `343b21e4` under the r84 counter → 12 `H.. SURVIVED`, `rc=1`,
  and also `baseline=bad neutral_ok=0/3 decoy=broken` because `--expect-cases 33` against a
  27-case target. The claim's do-nothing bullet says exactly "H01-H12 SURVIVED, rc 1 (P1/P2/P3
  false)", so it is honest; the stub is the control that isolates the gaps (`baseline=ok`, 33
  cases, 12 `SURVIVED`).
- Counter diff r83→r84 touches only the selftest block and its print line; `single_decoy`,
  `comment_lines`, `rename_locals`, `verdict` and the battery are unchanged. F12 still passes
  (A1); nothing in the r84 diff touches the F13 comment-strip class either (r83 receipt: rc 0,
  `decoy=ok`, `neutral_ok=3/3`). `claims.json` and `history_read` carry defect 1 as "Carried, not
  claimed"; the artifact-level declaration is incomplete (docstring + selftest), as noted in A1.

Verdict: **honestly carried at claim level**; the residual is a routed instrument defect, not a
claim falsification.

### A4 — the twelve H rows are the r83 survivors, and the six checks kill them

`c1-table-composition.txt`: 79 rows = the 67 r83 rows byte-identical (id/anchor/replacement/
class/kill_cases/expect) + H01–H12; H01–H12 pair-match 12/12 rows of
`.ufo/waves/round-83/w1/MutC1Hunt-rows.json` (the 12 SURVIVED rows there), with `kill_cases`
remapped from the old checks to the six new ones; classes 75 assertion / 1 exception / 3 neutral.
Sample mutations applied by hand at the candidate: H03 fails exactly `summary-fields`,
H06 `argv-values` (with the IndexError caught), H12 `entry-set`; each `rc=1`,
`selftest cases=33 failures=1` (`c1-h-sample-mutations.txt`). The six new checks read as real
assertions (exact summary line, fixture ENTRY sets, argv guards, verbose ordering, conform_ok
polarities), not name registrations.

C1 verdict: **no P1–P8 predicate is false at the frozen bytes** (P2/P8 landing; P8 requires the
SKILL/README pin-row update). Claim survives. Limits confirmed and bounded: the kill tally is
forgeable (A1), the per-row grep is not a target defense (A2), and the F12/F13 declaration lives
in `claims.json` but not in the counter's own docs/selftest (A3).

## 2. C2 — attacks

### B1 — the do-nothing control is honest

`c2-freeze-state.txt` (first-hand): `FRONTIER-CENSUS rows=59 admitted=59 closed=59
problem-rows=0 registry=118`; `tracked_knowledge=97`, `worktree_knowledge=98` (the untracked
draft), `registry=118`; the S118 row is `docs | A | … | queued | 2026-11-06 | … | —`. B0 on the
draft: `S118:sha256 OK` plus six `OK occurrences=1`, rc 0. B4 `records=98 bound=98 unbound=0`.
B6 literal sweep over the other 97 entries: `literal_sweep_total 0 files 97`. B7 `kasegi ok`
rc 0 with the six inherited W04 rows. B8 gate on the draft: `claims=6 want=6 spans=7 mislocated=0
overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok`, `ENTRY-GATE-RESULT pass`, rc 0.
The freeze-state values the claim's do-nothing bullet names are exactly what the instruments
print.

### B2 — a junk entry passes B0–B8 (B3 and B8 are shape-level)

Built in scratch: a "junk" entry with the six real S118 quotes but vacuous filler after each
`Falsifiable rule:`/`Rejected over-generalization:` label (each ≥8 words, cites its line, shares
≥2 stems with its quote, is not drawn from the source).

```
$ python3 -B .ufo/waves/round-83/c2/entry-gate.py --entry <scratch>/junk-gate.md \
    --manifest corpus/source-snapshots/round-84/manifest.json --source S118 --lane <lane>
ENTRY-GATE sid=S118 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok
ENTRY-GATE-RESULT pass
rc=0
```

Full-lane mirror (copied `corpus/README.md` and `corpus/SOURCES.md`; read-only symlinks to
`corpus/instruments`, `corpus/knowledge`, `corpus/source-snapshots`; one appended F60 row
pointing at the junk file):

```
$ python3 -B corpus/instruments/frontier-recheck-count.py --root <scratch>/mirror
FRONTIER-CENSUS rows=60 admitted=60 closed=60 problem-rows=0 registry=118
FRONTIER-PASS F60 ids=S118
PASS     F60  knowledge/junk-filler.md  ids=S118  exit=0
entries=63 pass=63 exit=0
```

(`c2-b8-gate-junk.txt`, `c2-junk-entry.md`, `c2-b3-junk-mirror-frontier.txt`.) The exact B3 line
and the F60 PASS are therefore satisfiable by content that adds no knowledge; B3 counts rows and
B8 checks the six-quote shape, and G5's own docstring says it does not check that a rule is true
or follows from its quote. This is the carried r83 spot-check defect 4 (lexical G6), not a new
defect of this freeze.

Verdict: **claim survives** — C2's statement is about six specific clauses (verified accurate
against the capture), and it says only that "the entry passes the round-83 entry gate unchanged",
which is true; but B8/B3 carry no semantic warrant, so the coverage move's warrant is the entry's
content review, not the predicate set.

### B3 — S118 is tier A primary for its scope

Registry row: kind `docs`, tier `A`, scope "the OSV.dev project's own statement of its GCS
data-dump layout", anchor "Data sources page, lines 99-123". Protocol (CORPUS.md:93): tier `A` =
"primary or authoritative for that scope". The page is the OSV project's own documentation of its
export, the manifest records HTTP 200 with final URL = requested URL, and the raw size 27,419 B
matches the r83 ScoutPerish §4 lead 2 (`c2-s118-tier.txt`). It is not in the census's W04
duplicate-URL list. No tier inflation; scope is precise.

### B4 — the coverage claim names surfaces that move

The claim names `FRONTIER-CENSUS rows 59 → 60`, `corpus/knowledge 97 → 98`, and `S118 queued →
mined`. The freeze values are first-hand (B1); the row surface moves to 60 when the F60 README row
is added (the mirror prints it), and the knowledge surface is a tracked-file count (97 tracked at
freeze, 98 in the worktree with the draft). Yes — the claim names ledger surfaces that move, not a
private note.

### B5 — draft prose overreach (not the frozen claim)

- **Claim 5 rule (draft:49):** "a script that looks for a dump directory named after a
  release-suffixed ecosystem string such as an Alpine version finds nothing … (S118.txt:121)".
  S118:121 says only that the dump "will always contain an ecosystem directory without the :.*
  suffix (e.g. Alpine)" and that it holds the advisories of that prefix; S118:123 says the
  prefixed exports stopped. The page never says a suffixed directory is absent, and the entry's
  own Limits (draft:94) says "whether stale suffixed directories are deleted or only left
  unrefreshed" is *not claimed*. The rule and the Limits contradict each other; the gate cannot
  see it (it only requires a citation and own words). Smallest fix: state the base-directory
  guarantee and that any suffixed directory is not refreshed, instead of "finds nothing"
  (`c2-claim5-limits-conflict.txt`).
- **Claim 1 rule (draft:17):** names "the withdrawn field", which S118:102 does not state (the
  page says "including withdrawn records"); the entry's Distinctness attributes the field to
  F59/S117:117-118. Minor: cite F59/S117 there or say "records the page calls withdrawn".

Verdict: **C2's frozen statement survives** (all six pinned clauses are accurate); the draft's
Claim 5 rule is a fixable prose overreach that the L1 integrates, not a predicate failure.

## 3. Impacted axes, corrections

| axis | finding | smallest safe correction |
|---|---|---|
| depth:verifiability | A1: the counter's kill tally is forgeable by a table-reading target that tests nothing (F12 class, reproduced under r84); A2: per-row grep is counter self-consistency, not a target defense; A3: F12/F13 carried in `claims.json` but not in the counter docstring/selftest | name F12/F13 beside F8 in `mutbat.py`'s known-limit paragraph and record the forgery as an accepted class in the selftest block; keep P2/P3's `target_sha256` as the identity limb; no predicate change |
| coverage | B2: B3/B8 are satisfiable by a six-quote junk entry (rows=60/closed=60 with filler); B5: Claim 5's "finds nothing" contradicts its own Limits and the page; Claim 1's field is not on S118 | keep B0–B8 as shape limbs and state the content warrant is the reviewer's; fix Claim 5's rule (base directory always exists; a suffixed directory, if present, is not refreshed) and cite F59/S117 for the withdrawn field |

No P1–P8 or B0–B8 predicate is false at the frozen bytes; no axis move is denied. The frozen
claims survive, with the two recorded limits (forgery class on C1; shape-level B8/B3 on C2) and
one fixable draft-prose defect (Claim 5's "finds nothing").

## 4. Files written by this seat

- `.ufo/waves/round-84/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-84/w1/CriticClaims-receipts/`:
  `forgery-table-lookup.py`, `c1-attack-a1-forgery.txt`, `c1-attack-a2-injection.txt`,
  `counter-mutant-line-injection.txt`, `mutbat-forgery-table-lookup.txt`,
  `c1-mutbat-candidate-firsthand.txt`, `c1-p1-candidate-selftest.txt`,
  `c1-p4-counter-selftest.txt`, `c1-p5-counter-mutants.txt`, `c1-p6-conformance.txt`,
  `c1-p7-controls.txt`, `c1-freeze-pins.txt`, `c1-table-composition.txt`,
  `c1-h-sample-mutations.txt`, `c1-counter-r83-to-r84.diff`,
  `c2-b0-draft-recheck.txt`, `c2-b5-foreign-cwd.txt`, `c2-b8-gate-draft.txt`,
  `c2-b8-gate-junk.txt`, `c2-junk-entry.md`, `c2-b3-junk-mirror-frontier.txt`,
  `c2-b4-binding.txt`, `c2-b6-literal-sweep.txt`, `c2-b7-census.txt`,
  `c2-freeze-state.txt`, `c2-s118-tier.txt`, `c2-claim5-limits-conflict.txt`.
