# ScribeShonenLog — round-41 build wave 1 (scribe)

Seat: ScribeShonenLog. Lane repo `kasegi-shokunin` (read-only for this seat except the three paths
below). Base for every measurement below: the claims-freeze base commit, resolved from the literal
`5b29ea1` — see Finding 1, which is the reason this receipt always names the 40-character object.

Deliverables (the two `.txt` files are the landable bytes; nothing else in them is commentary):

| file | sha256 | lines | bytes |
|---|---|---|---|
| `ScribeShonenLog.shonen-append.txt` | `82437c2473f08b90498a0d2033c39c45cc2551c366de025bc6ce4345e7606b29` | 56 | 4758 |
| `ScribeShonenLog.log-round41.txt` | `df7cc8a4994546e048de752e4908f05a36e10d13f048a7dd9a8feb3ce7ffcdcc` | 11 | 2654 |

## 1. Behavior

- Drafted the four round-41 SHONEN box updates (boxes stay `[~]`) as an EOF-append block: box 1 with
  the measured base limb + the D6 repair note + `<<<SKILL-DIFF>>>`; box 2 with the honest
  "no new end-to-end domain task" note (seat histogram + `## Round 41` absent at base); box 3 with the
  C1 suite limb at `<<<Y>>>`, the base C2 counters and the declared after-state including
  `<<<AUDIT>>>`; box 4 with the F24 in-province argument against `PROVINCE.md:29-30` plus
  `<<<SIBLING>>>`.
- Drafted the `## Round 41 (attempt 1, fresh-start)` LOG block: C1, C2, Frontier, Corrections,
  Mistakes, Census, Assimilation `<<<ASSIM>>>`, considerthese `<<<CT>>>`, Wave shape `<<<WAVES>>>`.
- Wrote nothing outside `.ufo/waves/round-41/wave1/ScribeShonenLog.{md,shonen-append.txt,log-round41.txt}`
  and scratch. No git/jj mutation, no product code, no judge, no commit/push, no subagent dispatch,
  no network fetch, no tool install (nothing installed; no pacman run).

## 2. Commands and observed output

Disk guard (before any heavy pass):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root     use% 3%   free 125.1G
/var/tmp use% 35%  free 589.5G
/fast/scratch/hyaku use% 25% free 610.2G
```

Lane state at read (read-only git):

```
$ git -C kasegi-shokunin log --format='%H %cI %s' -3
b3b08b276af6146217efd89f7595243a644ed00b 2026-10-27T05:17:06-03:00 round-41: wave-1 build spec (60 seats) + dispatch
fbba3d96cdf8d37c1ea41304a1ba35691329684b 2026-10-27T05:07:54-03:00 round-41: claims freeze (C1 r41-closure.sh I1-I12; C2 F24 RFC 9116) + do-nothing controls + census baseline
5b29ea1439450b712581edf5f0f0bf98dfb262ab 2026-10-26T19:49:29-03:00 round-40 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git rev-parse 5b29ea1
5b29ea1439450b712581edf5f0f0bf98dfb262ab
```

Base tree, extracted outside the lane (`git archive <base> | tar -x -C $S/base`):

```
$ sha256sum $S/base/SKILL.md; wc -l < $S/base/SKILL.md
ad20fc3d371302301b49088ae41c0a227cf6067ea0c6c8078f2f000d1ca457c1  1122
$ sha256sum $S/base/PROVINCE.md; wc -l < $S/base/PROVINCE.md
62c6d8db7437435c5c2f5c98b33010d864246c63906b5401211e739ea4c1e9c1  161
$ git diff --numstat 5b29ea1439450b712581edf5f0f0bf98dfb262ab -- SKILL.md PROVINCE.md   # (empty)
$ git diff --diff-filter=D --name-only 5b29ea1439450b712581edf5f0f0bf98dfb262ab | wc -l
0
```

Base == spec head for `SKILL.md` (`ad20fc3d…`, 1122 lines at both). No-harm instruments on the base
bytes:

```
$ python3 corpus/instruments/density.py SKILL.md
| | **mean dens** | ... | **233.5** |
Total path-citation instances: 774 across 28 blocks.        exit=0
$ python3 corpus/instruments/anchorcheck.py SKILL.md
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
```

D6 location, confirmed on the base bytes (`grep -n '' SKILL.md`):

```
1116:
1117:## Round-40 Gates & probes registry addition (appended 2026-10-26)
1118:
1119:| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
1120:|---|---|---|---|---|---|---|---|
1121:
1122:| r40-closure.sh | gate | `bash corpus/instruments/r40-closure.sh --export-ref <hash> ...
```

The blank `:1121` between separator `:1120` and row `:1122` ends the table, exactly as the round-40
verifier §5 D6 states. The round-41 SHONEN box-1 draft cites these numbers.

Base counters (grounding for the LOG C2 line; they reproduce `c2-controls/before.txt`):

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                       -> 23
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 62
$ ls corpus/knowledge/*.md | wc -l                                  -> 59
$ wc -l < corpus/instruments/knowledge-expected.txt                 -> 61
```

Frozen controls read at the wave dir (not re-run): `c1-controls/do-nothing.txt` → `exit=127`
(`bash: corpus/instruments/r41-closure.sh: No such file or directory`); `c2-controls/before.txt` →
frontier 23, registry 62, S063 rows 0, knowledge 59, `entries=26 pass=26`, `records=54 bound=54
unbound=0`, `lines=59 total=59`, `expected=59 missing=0 unexpected=0 exit=0`;
`census-before.txt` → `kasegi W04 S028 …`, `kasegi W04 S029 …`, `kasegi ok …`, `exit=0`.

Log/doc state at base:

```
$ git show <base>:LOG.md | wc -l ; git show <base>:LOG.md | grep -c '^## Round 41'   -> 1734 ; 0
$ wc -l SHONEN.md ; sha256sum SHONEN.md
219 edce88b79f8cb0ef409f7a21fa26e3ef5c2bd66d24244b7b2953c29f0adc90c0
$ tail -c 60 SHONEN.md | od -c   -> ... no non-author verifier this round.\n   (ends with one LF)
```

The SHONEN draft begins with one blank line so the append yields a single blank separator; it opens
no ``` fence, so the file's fence state stays CLOSED at EOF (I4).

Wave spec (box-2 evidence):

```
$ python3 - <<'EOF'  # wave1-spec.json
seats 60
Counter({'executor': 17, 'scout': 11, 'reviewer': 9, 'scribe': 6, 'critic': 6,
         'mutation-tester': 5, 'connector': 2, 'sentinel': 2, 'simplifier': 1, 'revenger': 1})
reportDir .ufo/waves/round-41/wave1
```

Round-40 firing evidence named in the LOG corrections line (read, not re-run):

- `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt`:
  `== T2 H2 substring defeat: closed=7/80 and failures=10 (wrong values)` → `rc=0 payload=corrections=4,named=4,missing=0,fences=closed`;
  `== T4 H3 fenced pseudo-table: only criterion row is inside a ``` fence` → `rc=0 payload=mentions=1,rows=1`.
- `.ufo/waves/round-40/wave2/CritKillRule.md` §2: `### F1`–`### F8` (see Finding 3).
- `.ufo/waves/round-40/wave2/MutH6H10.md`: M-H8a row — "pristine itself accepts a leaf-capped green
  negative control (defect D2)".
- `.ufo/waves/round-40/wave2/MutH1H5.md:118`: "H4 survivor (defect — selftest coverage gap on the
  quote/date conjuncts)".
- `corpus/lessons/round-40-verifier-spotcheck.md` §5 D1 (append Correction lines grading r40 C1 not
  verified), D2 (Y-level selftest tally without transcript), D4 (duplicate `## Gate`, census l27
  garble), D5 (lesson l9 `33/35 = 94%` and `50/89` vs dispatch 25/35 and 42/89), D6 (quoted above).

## 3. Placeholder substitutions the L1 must perform

`ScribeShonenLog.shonen-append.txt`

- `<<<SKILL-DIFF>>>` — one clause: the landed append's byte summary, e.g. `` `git diff --numstat
  <base> -- SKILL.md` = `N 0`, 1122+N lines, sha256 `<landed sha>` ``. No deletion count may be
  non-zero.
- `<<<Y>>>` (×2, box 3) — the verification ref hash (lane files never name J; Y is the receipt commit).
- `<<<AUDIT>>>` — the landed `python3 corpus/instruments/recheck-audit.py --quiet` output line; the
  sentence already states the claim's after-state (`expected=60 missing=0 unexpected=0 exit=0`).
- `<<<SIBLING>>>` — the sibling-scan receipt path + its ruling sentence (20 lane roots + shokuknow).

`ScribeShonenLog.log-round41.txt`

- `<<<Y>>>` (×2: the ref and the `run-utc`) — the ref commit and its committer instant
  (`time-basis=ref-commit`).
- `<<<ASSIM>>>`, `<<<CT>>>`, `<<<WAVES>>>` — the assimilation verdict (id-collision rerun, quarantine
  slice verdicts, adopted count), the considerthese proposal outcome, and the two-wave seat counts +
  band + attack share + dead seats.

No other text in either file is placeholder or commentary; both are complete sentences that read as
landed text after substitution.

## 4. Findings

**Finding 1 — the frozen claims' base literal is not a hash (verbatim conflict; reported to the L1).**
The literal `5b29ea1439450b712581edf5f0bf98dfb262ab` in `claims.json` is **38** hex characters and
`next(i for i,(a,b) in enumerate(...))` shows the first divergence at index 26: the object is
`5b29ea1439450b712581edf5f0f0bf98dfb262ab` (40 chars; the literal drops `f0`).

```
$ git cat-file -t 5b29ea1439450b712581edf5f0bf98dfb262ab
fatal: Not a valid object name 5b29ea1439450b712581edf5f0bf98dfb262ab
$ git cat-file -t 5b29ea1439450b712581edf5f0f0bf98dfb262ab
commit
```

Files carrying the 38-char literal: `.ufo/waves/round-41/claims.json`, `wave1-spec.json`,
`wave1-dispatch.json`, `build-wave1-spec.py`, `c1-controls/do-nothing.txt` (there harmless: the suite
was absent, `exit=127`), and the dispatch text this seat received. Impact: C1 counting command 3 and
the base limb of C1's kill rule export the base through `--export-ref <hash>`; an unresolvable ref
mapped to the generic `closed<12/12 exit=1` makes the base negative control **vacuous** (the T-class
defeat the freeze punishes), while a suite that refuses exit 2 makes the counting command literally
unsatisfiable. My drafts use the 40-character object and the LOG carries this as the mistakes line.
Both peer messages to `KasegiR41` are quoted in §6.

**Finding 2 — D6 confirmed at the frozen base, not only at the round-40 head.** `SKILL.md:1119-1122`
(base `ad20fc3d…`, identical at the spec head): header, separator, **blank**, row. Round 41's repair
must therefore be an EOF append of a fresh header+separator+row block; a row appended under the
existing separator stays outside the table.

**Finding 3 — CritKillRule escape states: eight committed, seven claimed.** `grep -c '^### F'
.ufo/waves/round-40/wave2/CritKillRule.md` = **8** (F1 nested-scratch, F2 host `--work` placement,
F3 dotfile, F4 case/Unicode-separator, F5 ancestor-prefix, F6 nonexistent `--scratch-root` fail-open,
F7 pending-marker spelling, F8 git-status blindness), while claims I11 says "each of the **seven**
committed CritKillRule escape states reds the limb it escapes". Reported verbatim to the L1; the LOG
corrections line was reworded to "the committed `wave2/CritKillRule.md` escape states" so the landed
LOG does not assert either count.

**Finding 4 — corrections ownership, deliberately excluded.** This seat's SHONEN append carries no
`Correction (round 41)` line: the I1 limb counts corrections in SCORECARD/LOG/SHONEN, and the
corrections seat owns those bytes. If that seat appends its SHONEN corrections after this block, the
four `- [~]` box lines here stay intact (`grep -c '^- \[~\]'` on this file = 4). Risk to flag at
integration: two independent SHONEN appends must not both carry correction lines, or I1's
`corrections=`/`named=` payload changes without the count being re-measured.

**Finding 5 — box 2 has no hunt-to-claim seat, measured.** 60 seats, ten roles, none a domain hunt;
`LOG.md` has no `## Round 41` heading at base. The box is drafted `[~]` with that stated, not
upgraded.

## 5. Out of scope / not done

- Did not write `SHONEN.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/README.md`,
  `corpus/SOURCES.md` or any corpus file; did not edit `claims.json`, the controls, `MANIFEST.json`,
  templates or scripts.
- Did not build or run `r41-closure.sh` (absent at base), did not run the census, source-recheck,
  harness, binding or audit over a post-integration tree, and did not run any C1/C2 counting command
  beyond the read-only base measurements in §2. Every post-integration value in the drafts is either
  inside a `<<<…>>>` placeholder or tagged `[L1-MEASURE]`.
- No network fetch (so no HTTP status/bytes/UTC to record); no tool installed or upgraded.
- Did not verify, grade, commit, push or publish anything; no subagent spawned.

## 6. Coordination

Two messages to `KasegiR41` (L1), concise:

1. "ScribeShonenLog — defect in the frozen claims base literal (affects C1's base negative control,
   live seats)." … body as §4 Finding 1, with the recommendation that I12/I3 assert an unresolvable
   `--export-ref` is a distinct ref-not-found red rather than `closed<12/12`.
2. "ScribeShonenLog — second finding for the I11/wave-1 seats (short)." … eight committed escape
   states vs the claim's seven, with the suggestion that I11's payload name the covered set
   explicitly.

## 7. Scratch

`S=/fast/scratch/hyaku/kasegi-r41/ScribeShonenLog/` held the base export (`$S/base`, from
`git archive`) and the claims-slice dump used for the full-text read of `claims.json` (the reader
truncates long JSON lines at 768 chars). `TMPDIR` was bound to `$S` for the extraction. Removed
before yield; removal verified with `ls` (`/fast/scratch/hyaku/kasegi-r41/` now holds 46 peer seat
dirs and no `ScribeShonenLog` entry).

## 8. Addendum — the L1 applied both errata while this receipt was being written (observed, not mine)

`git status --porcelain` at read time shows three modified freeze files and one new spec file, all
written by the L1 after my two messages; I touched none of them:

```
 M .ufo/waves/round-41/build-wave1-spec.py
 M .ufo/waves/round-41/c1-controls/do-nothing.txt
 M .ufo/waves/round-41/claims.json
?? .ufo/waves/round-41/build-wave2-spec.py
```

- `claims.json`: `base` and the C1 predicate/kill-rule/counting-command literals now carry the
  40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab`, and a new `errata` array records both of my
  findings verbatim: `"base was written as 38 hex chars (…, unresolvable); corrected to the 40-char
  … — same commit (prefix 5b29ea14). Found by seat ScribeShonenLog. … I12 asserts an unresolvable
  --export-ref reports a distinct red (ref-not-found), never a vacuous closed<12/12."` and
  `"claims.json says 'the seven committed CritKillRule escape states' but the committed
  wave2/CritKillRule.md carries EIGHT '### F' headings (F1-F8; its own intro prose says 7). I11's
  target is the eight committed states; I11 payload must read escapes=8 and red=8, naming F1-F8."`
- `c1-controls/do-nothing.txt`: gains one `Erratum (freeze, same round):` line naming the 38-hex
  transcription and the freeze-time `git rev-parse --verify` guard.
- Observation for the integrator, status-neutral: after that write `claims.json` has no trailing
  newline (`git diff` shows `\ No newline at end of file`). Valid JSON; noted because every other
  wave file ends with an LF.

- Third integration flag, observed in a sibling seat's delivered bytes:
  `ScribeCorrections.full-blocks.txt` says "seven escape states" three times (its lines 1, 6, 10 —
  "`wave2/CritKillRule.md`'s seven escape states"). The committed file carries eight (`### F1`–`###
  F8`) and the claims erratum now binds I11 to `escapes=8 red=8`, so the corrections bytes and the
  I11 payload would disagree unless the count is aligned at landing. Its blocks contain no
  `- [~]` box lines (`grep -c '^- \[~\]'` = 0), so they do not duplicate this seat's four boxes.

The LOG draft's mistakes line was rewritten after this read so the landed LOG matches the errata
array (both errors, the correction, the guard, and `escapes=8 red=8`). Digest in §0 is the
post-rewrite value.

