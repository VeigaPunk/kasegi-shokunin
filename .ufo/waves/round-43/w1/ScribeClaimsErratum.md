# ScribeClaimsErratum — round-43 claims erratum (two round-42 record corrections) + round-42 erratum 5

Seat: `ScribeClaimsErratum` (leaf, scribe). Round 43, lane `kasegi-shokunin`, one v2 wave.
Lane HEAD at work time: `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`; round base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Scratch: `/fast/scratch/hyaku/kasegi-r43/ScribeClaimsErratum` (created, used, removed before yield).
Scope extension: mid-run the L1 `KasegiR43` extended this seat's deliverable set to TWO erratum files (see "Deliverables").

## Deliverables

| file (beside this receipt) | lands at | lines | bytes | sha256 |
|---|---|---|---|---|
| `ScribeClaimsErratum.claims-erratum-1.md` | `.ufo/waves/round-43/claims-erratum-1.md` | 11 | 2848 | `ca5a450f5952bbb9928b2af2fe88a1865549cc736bcc2ba7cc4d4a75c78f304e` |
| `ScribeClaimsErratum.round42-erratum-5.md` | `.ufo/waves/round-42/claims-erratum-5.md` | 3 | 825 | `494ba6d5a7010362b65ccfa28fec62577535306fb1fa3183168e83ba52c332fb` |

(A) shape: H1; one paragraph naming the frozen claims file `.ufo/waves/round-43/claims.json` and commit
`0566bd66e93d429b2df8b6751cf10cbdc391e79b`; one bullet per item (E1 `closed=10/12`, E2 `frozen_at_utc`) carrying
token, superseded value, live value, command and path; closing statement that no predicate, target, counter,
kill rule or score changes and no claim wording is re-frozen.

(B) shape: H1 plus exactly ONE paragraph that carries the whole token `closed=10/12`, states it is `superseded`
because the cited control receipt `.ufo/waves/round-42/c1-controls/do-nothing.txt` actually prints `closed=8/12 exit=1`,
and names the command that produced it. This is the K17 limb's required shape (read from
`.ufo/waves/round-43/w1/ExecK17ClaimsBefore.md` and the matcher in `ExecK17ClaimsBefore.sh`: a
`claims-erratum*.md` paragraph in the SAME round dir holding the token and the literal `supersed`).

(A) was revised once during the run: the first version (9 lines, 3197 bytes, sha `fcb4395…`) restated after-state
counters in its closing paragraph; those numbers sit unbound in the committed lane, so they would have added K18
unbound quotes. The landed version keeps every required token on lines that are bound by a committed transcript or
marked `superseded`, and its closing paragraph carries no numeric counters.

## Behaviour

Two round-42 record values are named superseded, each with token, superseded value, live value, command and path:

1. **`closed=10/12` → `closed=8/12`.** `.ufo/waves/round-42/claims.json:37` says the r41 suite at base prints
   `closed=10/12 exit=1`; the control receipt that the cell itself cites records `selftest cases=12 failures=8` then
   `closed=8/12 exit=1` at `:15-16`, from the command at `:13-14` (r41 suite, base
   `5053a7f46de35784cff4b56756906e9014a38276`). (A) records this and points at (B); (B) is the K17-shaped
   correction that K17 grades (`by=claims-erratum-5.md`).
2. **`frozen_at_utc=2026-10-28T12:05:00Z` → `2026-10-28T10:51:52Z`.** `.ufo/waves/round-42/claims.json:6` carries
   the future-dated literal; `.ufo/waves/round-42/claims-erratum-3.md:3` discloses the on-disk mtime
   `2026-10-28 07:51:52.149991752 -0300` = `2026-10-28T10:51:52Z` from `stat -c '%y' .ufo/waves/round-42/claims.json`,
   with the ordering before.txt 07:50:11-03:00 → claims 07:51:52-03:00 → first seat launch 08:01:46-03:00.

Both round-43 claims (C1 depth:verifiability held 4, C2 coverage held 8) stand exactly as frozen; no predicate,
target, counting command, kill rule or score changes; no claim wording is re-frozen; neither claims file is edited.

## Evidence: commands run and actual output

All reads are absolute-path and read-only; `git` used only read-only verbs; no network fetch.

1. Frozen claims read first (never edited):
   `python3 -c "import json;d=json.load(open('.ufo/waves/round-43/claims.json'));print('errata=',d['errata']);print('claims=',[c['id'] for c in d['claims']])"`
   → `errata= []` / `claims= ['C1', 'C2']`.

2. Superseded C1 literal at the named commit:
   `git show 0566bd66e93d429b2df8b6751cf10cbdc391e79b:.ufo/waves/round-42/claims.json | grep -o 'closed=1[0-9]/12' | sort | uniq -c`
   → `1 closed=10/12`.

3. C1 `before` line (line 37) at that commit:
   `git show 0566bd66e93d429b2df8b6751cf10cbdc391e79b:.ufo/waves/round-42/claims.json | sed -n '37p'`
   → `see .ufo/waves/round-42/c1-controls/do-nothing.txt — the frozen counter run against the base tree: r42 suite
   absent (exit 127, cannot print closed=13/13); the r41 suite at base prints closed=10/12 exit=1 with the I1
   evidence-not-named and I3 mangled-token defeats alive. Routed queue open at base: …`

4. Control receipt lines (working tree; file is 18 lines):
   `grep -n 'selftest cases=12 failures=8\|closed=8/12\|bash corpus/instruments/r41-closure.sh --export-ref\|--work /fast/scratch/hyaku/kasegi-r42' .ufo/waves/round-42/c1-controls/do-nothing.txt`
   → `13:$ bash corpus/instruments/r41-closure.sh --export-ref 5053a7f46de35784cff4b56756906e9014a38276 \`
   → `14:    --work /fast/scratch/hyaku/kasegi-r42/l1-ctl/work --scratch-root /fast/scratch/hyaku/kasegi-r42/l1-ctl`
   → `15:selftest cases=12 failures=8`
   → `16:closed=8/12 exit=1`

5. Committed control receipt agrees at the named commit:
   `git show 0566bd66e93d429b2df8b6751cf10cbdc391e79b:.ufo/waves/round-42/c1-controls/do-nothing.txt | grep -n 'closed='`
   → `7:(observed suite exit = 127; …)`, `12:--- r41 suite run against base export (expected RED: …)`,
   `16:closed=8/12 exit=1`.

6. Working-tree bytes equal the named commit's bytes (not an edited copy):
   `sha256sum .ufo/waves/round-42/claims.json` → `313b24ce3a35884bf70112743b8b0089802b2128dd3b6f80bbacf1cf006fcb08`
   `git show 0566bd66…:.ufo/waves/round-42/claims.json | sha256sum` → same digest;
   `sha256sum .ufo/waves/round-42/c1-controls/do-nothing.txt` → `7b8efa5a48e65f717221219a583f1825218b70b930422188d97592909afa193d`
   `git show 0566bd66…:.ufo/waves/round-42/c1-controls/do-nothing.txt | sha256sum` → same digest.

7. Commit identity for `0566bd66…`:
   `git log -1 --format='%H %cI %s' 0566bd66e93d429b2df8b6751cf10cbdc391e79b`
   → `0566bd66e93d429b2df8b6751cf10cbdc391e79b 2026-10-28T08:00:01-03:00 round-42: frozen claims + controls + wave-1 spec/dispatch`
   (`git show --stat` lists `.ufo/waves/round-42/claims.json` (70 +) and `.ufo/waves/round-42/c1-controls/do-nothing.txt` (18 +) there).

8. Superseded timestamp literal:
   `sed -n '6p' .ufo/waves/round-42/claims.json` → `"frozen_at_utc": "2026-10-28T12:05:00Z",`
   (`git show 0566bd66…:.ufo/waves/round-42/claims.json | grep -n 'frozen_at_utc'` → `6:`).

9. Erratum-3 discloses the mtime (3-line file):
   `wc -l .ufo/waves/round-42/claims-erratum-3.md` → `3`; `sed -n '3p' …` →
   `… records frozen_at_utc=2026-10-28T12:05:00Z, which is future-dated relative to the frozen file's on-disk
   mtime. stat -c '%y' claims.json observed 2026-10-28 07:51:52.149991752 -0300, i.e. 2026-10-28T10:51:52Z; the
   round-start c2-controls/before.txt mtime is 07:50:11-03:00 (10:50:11Z) … the wave dispatch marker records the
   first seat launch at 08:01:46-03:00 (11:01:46Z) …`
   Commit carrying it: `514ff62d61ee9bc717a20a02a22c65ec0c5124ed 2026-10-28T08:27:22-03:00 round-42: claims-erratum-3 (correct freeze timestamp from file mtime)`.

10. Mtime re-observed at this seat:
    `stat -c '%y %n' .ufo/waves/round-42/claims.json .ufo/waves/round-42/c2-controls/before.txt`
    → `2026-10-28 07:51:52.149991752 -0300 .ufo/waves/round-42/claims.json`
    → `2026-10-28 07:50:11.352077674 -0300 .ufo/waves/round-42/c2-controls/before.txt`
    (07:51:52 -0300 = 10:51:52Z; erratum-3's disclosed instant reproduces exactly).

11. Frozen-claim state untouched:
    `git status --porcelain -- .ufo/waves/round-43/claims.json .ufo/waves/round-42/claims.json .ufo/waves/round-42/c1-controls/do-nothing.txt`
    → no output. `git rev-parse HEAD` → `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`.

12. Deliverable measurements:
    `wc -l` → `11` (A) / `3` (B); `wc -c` → `2848` / `825`; `sha256sum` →
    `ca5a450f5952bbb9928b2af2fe88a1865549cc736bcc2ba7cc4d4a75c78f304e` (A) /
    `494ba6d5a7010362b65ccfa28fec62577535306fb1fa3183168e83ba52c332fb` (B).

13. K17 control pair, run with the ExecK17 seat's own driver over a scratch tree (`corpus/` + `.ufo/` copied, never
    the lane). Baseline without my erratum-5:
    `bash ExecK17ClaimsBefore.sh --tree <scratch>/tree` → exit `1`,
    `K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0`.

14. With `claims-erratum-5.md` placed at `<scratch>/tree/.ufo/waves/round-42/` (the bytes of (B)):
    `bash ExecK17ClaimsBefore.sh --tree <scratch>/tree` → exit `0`,
    `K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1`, detail line
    `K17 detail round=round-42 claim=C1 field=before token=closed=10/12 by=claims-erratum-5.md result=superseded`.
    Renaming the file away restores `superseded=0,unbacked=1 closed=0` (exit 1), so the file — not the tree — is
    what closes the limb.

15. K18 non-regression, same tree, with and without my two files. (A) placed at `<scratch>/tree/.ufo/waves/round-43/claims-erratum-1.md`,
    (B) at `<scratch>/tree/.ufo/waves/round-42/claims-erratum-5.md`; driver:
    `bash ExecK18Transcript.sh <scratch>/tree --verbose`.
    Baseline (no files): `K18 payload=quotes=27,bound=21,report-only=0,superseded=0,unbound=6 closed=0`.
    With both: `K18 payload=quotes=31,bound=25,report-only=0,superseded=0,unbound=6 closed=0`.
    `diff` of the verbose `unbound token=` lines → empty: the six unbound tokens are the pre-existing ones
    (`closed=19/19`, `selftest cases=19 failures=0`, `closed=13/19` in `.ufo/waves/round-43/INTEGRATION-PLAN.md`;
    `closed=10/13`, `selftest cases=13 failures=3`, `closed=10/13` in `corpus/lessons/round-42-verifier-spotcheck.md`).
    My files add 4 quote occurrences, all bound; they add none unbound. (K18 is red at the lane as it stands for
    reasons owned by other seats; this seat's contribution is zero new unbound.)

## Reproduction attempt (honest negative, not used as evidence)

The r41 base control was attempted once to test whether the receipt's value reproduces:

`TMPDIR=$S timeout 280 bash corpus/instruments/r41-closure.sh --export-ref 5053a7f46de35784cff4b56756906e9014a38276 --work $S/work --scratch-root $S`

- exit `124` (timeout at 280 s), stdout empty, stderr empty, `$S` total 44K — no output, not finished.
  Not used as evidence; the live value rests on the committed control transcript only.
- Supporting facts gathered while diagnosing: the suite exists at base
  (`git cat-file -e 5053a7f4…:corpus/instruments/r41-closure.sh` → success), its bytes are unchanged since the only
  commit that touches it (`03ca614e5f30a9554b33b77d13c4272c85e8ed6e 2026-10-27T08:34:37-03:00 round-41: integrate
  wave-1 C1/C2 deliverables`, sha256 `3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd`), and the base
  export is `142837760` bytes (`git archive 5053a7f | wc -c`, `pipe-status=0`). Root cause of the non-finish not
  established; no further attempts, per the scribe rule against rerunning work to decorate a report.

## Landing notes for the L1

- (A) must land at the `.ufo/waves/round-43/` TOP level, not in `w1/`. K18 treats top-level round-43 `.md` files as
  records; (A)'s tokens were shaped so that every one of them is bound or carries `superseded` on its line, so it is
  K18-neutral only in that position (a `w1/` copy is not a record and would neither help nor hurt K18).
- (B) must land at `.ufo/waves/round-42/claims-erratum-5.md` (a `claims-erratum*.md` name in that dir). K17 then
  measures `superseded=1,unbacked=0,closed=1` at the round-43 freeze export; without it the round-42 C1 `before`
  literal stays unbacked and C1 stays red. (A) references (B) in its E1 bullet.
- Both files are append-only additions: no round-42 file is rewritten, and neither claims.json is edited.

## Tooling

None installed, upgraded or invoked from any package channel; no `pacman` transaction; no PATH write; no network
fetch.

## Out-of-scope items reported verbatim (not edited by this seat)

- Peer `W1ScribeLessonGate` reported a registry defect in uncommitted r38 `corpus/SOURCES.md` rows: line 189
  (S242, `open(2)` ENXIO) has `NF=14` under `awk -F'|'` because its quoted `"O_NONBLOCK | O_WRONLY"` pipe is
  unescaped; validator `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin souji` → rc=1 with
  `souji	E01	S242 fields=12` (plus 43 W04 duplicate-url warnings); suggested fix `O_NONBLOCK \| O_WRONLY`.
  `corpus/SOURCES.md` is outside this seat's write scope; routed back to the peer and to the L1 for the
  registry/SOURCES owner or integration.

## Known limits

- The erratum asserts no cause for either superseded value (transcription slip vs measurement of a different tree);
  it records only that the claim's own cited receipt carries `closed=8/12`.
- The `closed=8/12` value is grounded in committed, digest-verified bytes, not in this seat's execution; the
  timed-out reproduction is disclosed rather than upgraded.
- K17/K18 were exercised with the wave-1 seats' drivers over a scratch tree copy of `corpus/` + `.ufo/` (157M), not
  against the committed Y export of `r43-closure.sh` (which does not exist in the lane yet at this seat's run). The
  K17 match is on the real matcher; the K18 comparison is a baseline-vs-with diff on the same tree.
- (A)'s E1 supersession reference assumes (B) lands; if only (A) lands, K17 stays red (unbacked=1) while (A) itself
  remains K18-neutral.

## Scratch cleanup

`/fast/scratch/hyaku/kasegi-r43/ScribeClaimsErratum` (tree copy, driver outputs) removed before yield; absence
verified with `ls` (`No such file or directory`). Only the two deliverables and this receipt remain in the wave dir
from this seat.
