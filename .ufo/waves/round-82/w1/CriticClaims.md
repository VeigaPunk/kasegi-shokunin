# CriticClaims — round 82 attempt 1 (C1 depth:verifiability, C2 coverage)

Seat: critic. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, freeze
`b9589300810a477f4d6794bfabc24b22fb50b846`, base `1a50638edabb9bd1a4a4784774fc984cb5f2360f`.
Every command below ran over frozen bytes or an exact scratch copy; scratch
`/fast/scratch/hyaku/kasegi-r82/CriticClaims` (deleted before yield). Receipts in
`CriticClaims-receipts/` (index at the end).

## Frozen bytes verified

`git show b958930:<path> | sha256sum` matches `claims.json` for all five C1 artefacts, and the
base instrument at the freeze commit is the r81 landed bytes:

| artefact | sha256 |
|---|---|
| `c1/recheck-cwd-census.py` | `81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050` |
| `c1/mutbat.py` | `a7d4db43cdc8b2948af9c8c5f1baee827979fbb3d7dac0f39ecd46fad60ac55c` |
| `c1/mutant-table.json` | `045edc07c9edb24cb401b241e512745cc81e4d0f36eea26e5362b49e7cc5f26a` |
| `c1/build-table.py` | `07727196c26cd83b2f016d3d976fa2ffaaaf26b54e14c701a0a5957ca9885785` |
| `controls/c1-forgeries-r82.py` | `52cc6be5aa9d72c9d0644c1d97e252b215d792e5c00445417aa477d004d53908` |
| `corpus/instruments/recheck-cwd-census.py` at freeze | `a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0` (base) |

Table: 59 r81 rows + `J1 S07M B1 B2` = 63 (classes assertion 59, neutral 3, exception 1);
`build-table.py <candidate> <scratch>` rebuilds it byte-equal (`cmp` rc 0).

---

## F1 — C1, Major (routed defect): the counter hands each mutant its own row id, and each
## decoy its own status, in the temp-directory name. A forgery that runs no candidate
## assertion scores rc 0 with the candidate's exact summary line.

**Mechanism.** `mutbat.py:221` creates the mutant directory as
`tempfile.mkdtemp(prefix="mutbat-%s-" % row["id"], dir=work)` and `run_selftest` (`:79-89`)
executes the target at that path. The decoys use `prefix="mutbat-decoy-"` (`:189`). The target
therefore reads its own verdict from `os.path.basename(os.path.dirname(os.path.abspath(__file__)))`.
The baseline runs from the target's own path (no copy), so it is the only run without the
`mutbat-` prefix.

**Two forgeries built and run** (`forgery-path.py` embeds the 60 `kill_cases`; the stronger
`forgery-path-table.py` embeds no table rows and no original source — only the table's path —
and reads its row id from the directory name). Both keep the candidate bytes so every anchor
occurs once (`anchors_not_once=0`), replace `main`, and never call the candidate's `selftest()`.

```
$ python3 -B .ufo/waves/round-82/c1/mutbat.py --target <scratch>/forgery-path.py \
    --table .ufo/waves/round-82/c1/mutant-table.json --expect-cases 24 --work <scratch>/work
MUTBAT target_sha256=bc6fe98e77103b43d916de76b61fbf8924fbe5a257e7e7b2bf2cb14466f735b1 \
  baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 \
  decoy=ok decoy_hidden=59/60
rc=0

$ ... --target <scratch>/forgery-path-table.py ...
MUTBAT target_sha256=287c05ba76da07c89d558aff14b1c767feb3648bf9b442000458c99c18bf9b71 \
  baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 \
  decoy=ok decoy_hidden=59/60
rc=0
```

The r81 counter also scores the same forgery rc 0 (no decoy fields):
`... killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3`, rc 0.

**Is this F8?** No. There is no AST comparison and no embedded original; the table-reading
variant embeds no table rows and no original source. It is a path/label forgery.

**Does it falsify the claim's prose?** Not literally. The C1 statement's parenthetical already
concedes "not every forgery", and its F6/F7/F8 sentences are about those three shapes (the
committed control `controls/c1-forgeries-r82.txt` shows F6/F7 rc 1 and F8 rc 0 under r82; I did
not re-run the driver). What the forgery falsifies is the *classification* of the residual
class and the inference the round draws from the limb:

- the declared limit names AST embedding as the residual class and byte-/normalized-text as the
  rejected classes (`mutbat.py:38-40`, claims.json C1 statement), but the cheapest bypass is the
  harness's own label: no precomputation, no embedded bytes, ~20 lines;
- the decoy is itself detectable by its fixed prefix, so any source-keyed forgery can suppress
  its FAIL output when `parent.startswith("mutbat-decoy-")` and pass the decoy limb;
- the summary line is target-controlled: a reader cannot distinguish the two runs above from
  the real candidate run except by `target_sha256`, which the counter prints but does not
  compare to an expected value. P3 is not broken because its target is the P2-pinned
  candidate; the counter's claim to reject forgeries is.

**Impacted axes:** depth:verifiability (the counter is the kill evidence the axis rationale
names: "the counter's counter-owned decoy limb").

**Smallest safe correction:** one line — use a single constant prefix for every mutant *and*
decoy directory (e.g. `prefix="mutbat-run-"`), never the row id and never `decoy`; add a
path-guard case to `mutbat.py --selftest` (a TOY that passes everywhere except a directory
whose name encodes a known row id). ReviewC1's Major 1 (per-run nonce for the decoy) is
complementary, not a substitute: a nonce does not close the row-id leak.

Receipts: `mutbat-pathforge.txt`, `mutbat-pathforge-table.txt`, `mutbat-pathforge-r81.txt`,
`forgery-path.py`, `forgery-path-table.py`, `build-pathforge.py`, `build-pathforge-table.py`.

---

## F2 — C1, routed observation: P1/P5/P6/P8 are satisfiable by a junk stub; the joint set's
## anti-junk force is P2's hash pin, not the behavioural predicates.

A 30-line stub (`stub-predicates.py`) with no census logic satisfies, at this tree state:

```
P1  $ python3 -B stub.py --selftest            -> selftest cases=24 failures=0, rc 0
P5  $ python3 -B stub.py --root <lane> --lane <lane>
    RECHECK-CWD entries=96 noprefix=0 exit2_foreign=0 exit0_foreign=74 exit1_foreign=22 \
      exit_other=0 norecheck=0 restoration_only=0
    RECHECK-CWD-RESULT conformant              rc 0   (96 = `ls corpus/knowledge/*.md | wc -l`)
P6  same stub with row J1's replacement applied (anchor replaced once)
    RECHECK-CWD-RESULT nonconformant           rc 1
P8  grep -c 'subprocess.run(' = 1; grep -c '"bash", "-c"' = 1; grep -cE "[\"']/tmp" = 0
    (the first two are comment lines)
```

Not junk-satisfiable: P2 (sha256 pin), P3 (counter over the frozen bytes), P4 (forgery driver),
P7 (registry rows), P9 (counter selftest). Consequence: the behavioural predicates add no
independent anti-junk force beyond P2; they are a re-run of the pinned bytes. This is a
predicate-shape observation, not a predicate failure, and it is the reason F1 matters: the one
limb that is supposed to distinguish a real instrument from a forgery (the decoy) is bypassable.

The r81 routed defect 3 is fixed at the predicate level: P5's `exit0_foreign+exit1_foreign =
entries` plus the four zeros is exactly `conform_ok`'s bucket sum, and J1 now flips it
(`entries=96, exit0=67, exit1=22` -> nonconformant rc 1).

Receipts: `predicates-junk.txt`, `stub-predicates.py`, `stub-predicates-j1.py`.

---

## F3 — C1, (c): the do-nothing fails; no one-line junk edit passes both P5 and P6; an
## unenumerated weakening is caught only by anchor derivation.

- Do-nothing (control `controls/c1-donothing-r82.txt`): r81 bytes under the r82 counter ->
  `baseline=bad killed=54 survived=2 notderived=4 neutral_ok=0/3 decoy=broken`, rc 1; the two
  survivors are J1 and S07M. P3 false, as the claim's `do_nothing` says.
- J1 alone: `RECHECK-CWD ... exit0_foreign=67 ...` `nonconformant`, rc 1 (P6 true, P5 false).
- B1 alone (drop the bucket-sum conjunct): `... exit0_foreign=74 ...` `conformant`, rc 0
  (P5 true).
- B1+J1: `... exit0_foreign=67 ...` `conformant`, rc 0 (P6 false).

So the pair is jointly binding on the bucket-sum conjunct, and the r81 junk edit is dead.

- Unenumerated one-line weakening `and buckets == counts["entries"]` -> `>=`: passes the
  24-case selftest (`selftest cases=24 failures=0`) and the census (`conformant`, rc 0); the
  counter catches it only as `MUTANT B1 verdict=NOT-DERIVED occurrences=0` ->
  `killed=59 survived=0 ... notderived=1`, rc 1. The catch is anchor absence, not a behavioural
  assertion: regenerate the table on the weakened bytes and the weakening survives. This
  corroborates ReviewC1 m1 with an executed receipt; route to r83 (add a `buckets > entries`
  row to the candidate selftest).

Receipts: `c-junkedit.txt`, `c-ge-survivor.txt`, `cand-GE.py`.

---

## F4 — C2, Major (routed defect): B8's G5 "content" limb is lexical; a labelled S116 entry
## whose rule text is worthless filler passes `ruleless=0`.

Built `junk-s116.md` from the frozen manifest: correct G1 header, six `## Claim` sections,
each with the verbatim located span, and

```
Falsifiable rule: Nothing here matters, check nothing at all and ignore the record entirely (S116.txt:<n>).
Rejected over-generalization, not a page sentence: No over-generalization applies here because this sentence is deliberately meaningless filler (S116.txt:<n>).
```

```
$ python3 -B .ufo/waves/round-82/c2/entry-gate.py --entry <scratch>/junk-s116.md \
    --manifest corpus/source-snapshots/round-82/manifest.json --source S116 --lane <lane>
ENTRY-GATE sid=S116 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 \
  ruleless=0 header=ok
ENTRY-GATE-RESULT pass
rc=0
```

Controls in the same run: the r81 labelled dump under the r82 gate -> `ruleless=6`,
`ENTRY-GATE-RESULT fail`, rc 1; the real draft entry -> `spans=7 ... ruleless=0`, pass, rc 0.
So the limb does what the claim says (it rejects the empty-rule dump), but "content" is
8 words + a `(S116.txt:<n>)` citation + not-a-source-substring. `g5`'s docstring declares it
does not check truth or entailment; the finding is that it also does not check that the rule
is *about* the cited line.

**Impacted axes:** coverage (the admission bar).

**Smallest safe correction:** require the rule to cite a snapshot line other than the quote's
anchor and to share at least one content token with that line (forces reading a second line);
optionally require a predicate form (a field name plus a comparison or quantifier). Still
lexical, but filler now has to quote the line it cites.

Receipts: `b8-junk-entry.txt`, `junk-s116.md`, `build-junk-entry.py`.

---

## F5 — (e) axis naming: conformant with R58 and the r81 spot-check; no defect.

- QUALITY R58 (`corpus/QUALITY.md:415`): a lowest-axis claim that changes only a file the axis
  census never reads "is labelled nominal and its score is held, with the non-moving metric
  named". The claim does exactly that: `axis_score` says "nominal per QUALITY R58", names the
  non-moving metric (`resolve.py` citation-survival census), and says it is not claimed to move.
- The axis definition (`SCORECARD.md:33`) is `resolve.py`'s citation-survival fraction plus
  `anchorcheck.py`, census of record `citation-survival.md`; the surface changed is
  `corpus/instruments/recheck-cwd-census.py`, a different verifiability instrument. The lane's
  own precedent names C1 "by surface" (`SCORECARD.md:477`), and the r81 spot-check recorded the
  identical pattern ("score 4 -> 4 nominal per R58"). So the label is the lane's convention and
  the nominal guard is applied.
- Residual: the axis score cannot move this round by construction; the round's credit is
  instrument strength, which the claim states. Wording nit only: "the measured move is ..."
  followed by "nominal" uses R58's term for the axis metric; "the measured change is ..." would
  not read as a score move.

---

## Predicate sweep (what I ran, not what the controls say)

C1: P1 `cases=24 failures=0` rc 0; P2 hash match; P3 exact summary rc 0 (80.2 s); P5
`entries=96 ... exit0=74 exit1=22 ... conformant` rc 0; P6 J1 -> nonconformant rc 1; P7 both
registry rows contain `cases=24 failures=0`, `cases=22` count 0; P8 `1/1/0`; P9
`mutbat selftest ok ... selfdiff_forgery_exit=False` rc 0. P4 is evidence-verified from the
committed `controls/c1-forgeries-r82.txt` (F6/F7 rc 1, F8 rc 0), not re-run.

C2 (worktree, mid-integration): B0 `S116:sha256 OK` + six `OK occurrences=1`; B2 knowledge 96,
`knowledge-expected.txt:69` has the row, `.md` row sets equal (96 vs 96 modulo two comment
lines); B3 `FRONTIER-CENSUS rows=58 admitted=58 closed=58 problem-rows=0 registry=116` and
`FRONTIER-PASS F58 ids=S116`; B4 `records=96 bound=96 unbound=0` (pre-existing
`orphan=S040-live.txt`); B5 the entry's recheck exits 0 from a foreign cwd; B6 literal sweep
over the other 95 entries `total=0`; B7 `kasegi ok` rc 0; B8 pass. B1: at the freeze commit
S116 is `queued`/`—`; the worktree now shows exactly one changed SOURCES row (S116 ->
`mined`, used-by the new entry) and 116 rows both sides — the L1 is integrating concurrently
(SOURCES.md changed between two of my reads), so B1 is observed, not scored.

## Verdict

No frozen predicate P1-P9 or B0-B8 is false at the bytes I read. F1 and F4 are routed defects
under the claims' own `kill_rule` ("findings outside P1-P9 are recorded and routed to round 83,
never turned into verdict changes"); F1 is the one that should change round-83 design, and its
fix is one line in `mutbat.py` plus one selftest case. F2 is a predicate-shape observation;
F3 confirms the do-nothing and the r81 junk edit are dead; F5 finds no axis-naming defect.

## Receipt index

`CriticClaims-receipts/`: `mutbat-pathforge.txt`, `mutbat-pathforge-table.txt`,
`mutbat-pathforge-r81.txt` (counter runs); `forgery-path.py`, `forgery-path-table.py`,
`build-pathforge.py`, `build-pathforge-table.py` (forgeries); `predicates-junk.txt`,
`stub-predicates.py`, `stub-predicates-j1.py`; `c-junkedit.txt`, `c-ge-survivor.txt`,
`cand-GE.py`; `b8-junk-entry.txt`, `junk-s116.md`, `build-junk-entry.py`; `c1-predicates.txt`,
`c2-predicates.txt`, `c2-extra.txt`, `p5-candidate.txt`, `freeze-bytes.txt`,
`table-rebuilt.json`.
