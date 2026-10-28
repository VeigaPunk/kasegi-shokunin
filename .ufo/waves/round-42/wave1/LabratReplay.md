# LabratReplay — exact replay of the two surviving r41 defeats (J1/J2 fixture pin)

Item: read-only labrat probe (C1, depth:verifiability). Replayed the two committed r41
defeats — (a) I1 `evidence-not-named` union mutant, (b) I3 `closed=10/100` mangled-token
mutant — on scratch copies against the r41 suite limbs extracted **verbatim** into a
scratch harness, printing the raw outputs that pin the reproduction for the J1/J2 test
fixtures. No lane writes except this receipt + `LabratReplay.transcript.txt`; no git
mutation; no installs; no network. Scratch `/fast/scratch/hyaku/kasegi-r42/LabratReplay`
removed at yield; disk guard green throughout (tmp 5% / var-tmp 36% / fast-scratch 27%).

## Suite and refs

`corpus/instruments/r41-closure.sh` sha256 `3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd`
is byte-identical at the defeat ref `ad7147532cb702b0d541d40499874552183d9132` (the ref
`wave2/CritC1KillRule.md` / `wave2/RevC1Counters.md` attacked), the round-41 judged head
`1f7464612ac4c44e39886b82e812610d3c039b13`, and the r42 worktree — so the replay is exact
on the same bytes the committed artifacts name, and the same limbs the r42 base carries.
`git archive` of `ad71475` into `$S/export`; `RECORDS=(SCORECARD.md LOG.md SHONEN.md)`,
`EVIDENCE=(RevC1Counters CritKillRule MutH6H10)`, `ROUND40_TALLY=closed=10/10`.

## Verbatim extraction (nothing re-implemented)

21 limbs cut from the committed suite at `ad71475` into `$S/limbs.sh` (sha256
`18c81e0e4a5f4df4f7a1fc74ed8b22d2aea127431be66151761607f060246748`, 10,083 bytes,
`bash -n` clean): `ROUND40_TALLY` `RECORDS` `EVIDENCE` `LESSONS` `POS_PAYLOAD` (l.242,
249-251, 273), `FENCE_AWK` (519-568), `fence_awk` (570-574), `fence_match`+neighbours
(577-599), `value_present` (443-459), `qualified_corrections` (884-889), `check_i1`
(891-914), `check_i3` (950-982), `run_check` (1593-1596), `st_pos` (1622-1632), `st_neg`
(1638-1651), `st_verdict` (1654-1664), `fixture_tree` (1669-1679), `replace_line`
(1683-1690), `append_line` (1693-1695), `selftest_case_i1` (1699-1715),
`selftest_case_i3` (1752-1761). Per-block sha256 table is in the transcript tail; every
block re-verified byte-identical against the judged-head and worktree suite copies.
Harness additions (marked non-suite in the transcript): globals CASES/FAILS/WORK/EXPORT/
MUT/REF_RESOLVED, the `git archive` export, banner/probe plumbing, the artifact pin.
The fixture mutations themselves are performed by the verbatim `selftest_case_i1` /
`selftest_case_i3` bodies calling verbatim `fixture_tree`/`replace_line`/`st_neg`.

## Raw output pinning the reproduction (verbatim limbs, export ref ad71475)

```text
selftest detail=I1 positive=pass payload=records=3,lines=14,graded=3,evidence=3/3,missing=0
selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0
selftest detail=I1 mutant=grading-absent rejected=1 limb=graded=2
selftest detail=I3 positive=pass payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
selftest detail=I3 mutant=mangled-value-token rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
selftest case=I1 mutants=1/2 positive=fail payload-match=0 verdict=fail
selftest case=I3 mutants=0/1 positive=fail payload-match=0 verdict=fail
```

Pin vs committed artifact `.ufo/waves/round-41/wave2/CritC1KillRule.md` (transcript
§"committed-artifact comparison"): all six committed defeat lines reproduced
**byte-identical** (`PIN: all six committed defeat lines reproduced BYTE-IDENTICAL`;
per-mutant pins `evidence-not-named` / `mangled-value-token` byte-identical). The
observed set adds `grading-absent rejected=1` which the artifact did not excerpt —
that mutant IS rejected; it is not one of the two survivors.

## Mechanism evidence (what J1/J2 must bind to)

The defeats survive because the checks grade at **record granularity** while
`replace_line` rewrites only the **first** matching line and the records carry
duplicated `Correction (round 41)` blocks (D-r41-1; at `ad71475`: SCORECARD.md 8,
LOG.md 3, SHONEN.md 3 outside-fence lines):

- **I1 (F-EVID).** `check_i1` collects each evidence stem once per record over the
  union of ALL qualified correction lines (`seen` accumulator). Mutating only line 1
  leaves stems on duplicated lines 5 (`RevC1Counters`/`CritKillRule`/`MutH6H10` paths)
  and 2/6 ⇒ `evidence=3/3`, `graded=3`, rc=0. Transcript shows the post-mutation
  correction lines verbatim (mutated line 1 names no evidence; duplicates still do).
- **I3 (F-TOKEN).** `value_present` is sound — probes printed
  `closed=10/100` → rc=1, `closed=10/10` → rc=0 — but `check_i3`'s tally loop breaks
  on the FIRST bounded tally in any correction line of the record. The mangled first
  line is masked by surviving duplicates carrying `closed=10/10` ⇒ `tally=3/3`,
  `mangled=0`, rc=0. The `grep -qE 'closed=10/1[0-9]'` mangled counter only runs when
  NO line in the record hits.

**Fixture guidance for J1/J2:** a defeat that rewrites one matching line never reds
while a qualified twin survives. Either (i) mutate EVERY qualified correction line in
the record (loop all matches, not replace_line's first-only), or (ii) grade the check
per correction line/block — require each qualified line to name all evidence stems
(J1) / to carry the bounded `closed=10/10` token, counting `closed=10/1[0-9]` lines
as mangled even when a sibling line hits (J2). Under (ii) J1/J2 also close the
"one honest + one defective line per record" case independent of D-r41-1 duplication.

## Commands run

```sh
mkdir -p /fast/scratch/hyaku/kasegi-r42/LabratReplay
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status   # green
git -C $LANE show ad71475:corpus/instruments/r41-closure.sh             # extraction source
git -C $LANE archive ad71475 | tar -xf - -C $S/export                   # fixture export
bash -n $S/limbs.sh && bash -n $S/replay.sh                             # syntax clean
bash $S/replay.sh > $S/transcript.raw                                   # the replay, stderr=0 bytes
cp $S/transcript.raw .ufo/waves/round-42/wave1/LabratReplay.transcript.txt
```

## Deliverable

`.ufo/waves/round-42/wave1/LabratReplay.transcript.txt` — 104 lines, sha256
`27664ec14a6e832b4f3426a0964b8035a0ec3bbd11cbf98059a5bb93ec38b2af`. Contents: replay
environment (ref, three identical suite digests, limbs.sh digest), export record counts,
verbatim `selftest_case_i1`/`selftest_case_i3` output, mechanism probes with the mutated
fixture lines printed verbatim, the committed-artifact pin, and the verbatim limb
inventory (line spans + per-block sha256) — everything J1/J2 fixture builders need to
bind their replay limbs.

Tools installed: none. Network: none. Lane writes: this receipt + the transcript only.
