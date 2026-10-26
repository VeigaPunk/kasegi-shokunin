# RevGateReadiness — round-39 wave-2: spot-check readiness executed (falsify)

Seat: `RevGateReadiness`, reviewer, leaf (no dispatch). Round 39 wave 2, hyaku run 9, dispatched by L1
KasegiR39. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; HEAD (Y) `5006097a84305267c9a3e8c1e1d560e60fe41d37`;
base `480b1a505a2dfc14a4f718d16d63808247214d0a`; claims freeze `dcd31701720a6a4929a32471a62011ed87103421`.
This seat is NOT an author of any deliverable under attack.

**List source.** The round-39 lesson Gate's `### Spot-check readiness` (`corpus/lessons/round-39.md:62-64`)
defers to `wave1/ScribeSpotCheckList.checklist.md` ("items 1-9"), so that checklist is the executed list.
Identity of the executed bytes: `sha256sum .ufo/waves/round-39/wave1/ScribeSpotCheckList.checklist.md` →
`a86efe6a0addbadb721958fe4004938b361a0d83d9f2b3b2e67ac1effdc7dc14` — equal to the digest recorded in
`wave1/ScribeSpotCheckList.md` and `wave1/ScribeWaveEvidence.index.md` (row 232). All commands below ran at
the lane root (reads only) or with `TMPDIR=$S`, `S=/fast/scratch/hyaku/kasegi-r39/RevGateReadiness`.

## Verdict per checklist item

**1. Capture identity — HOLD.**
`sha256sum corpus/source-snapshots/round-39/S057.txt` →
`11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f`; `wc -lc` → `275 17971`.
`manifest.json sources[0]`: `sha256=11c8d6d6…64f2f`, `snapshot_sha256` equal, `snapshot_bytes=17971`,
`lines=275`, `url=https://www.cisa.gov/resources-tools/resources/when-issue-vex-information`,
`capture_url=http.final_url=https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf`,
`http.status=200`, `http.content_type=application/pdf`, `raw_bytes=fetched_bytes=235270`,
`raw_sha256=cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99`,
`last_modified=Mon, 06 Nov 2023 15:43:40 GMT`, `fetched_utc=2026-10-26T19:30:55Z`; `landing_page`:
`role=metadata only; not the committed capture`, `raw_bytes=54453`,
`raw_sha256=4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d`, `snapshot_bytes=3497`,
`lines=135`, `snapshot_sha256=c868f04a56c4fcc8dcfedc7354b2c65df5e47c8d55caf0f0502005e030360db2`. Every
checklist value byte-matches. (Note: `raw_bytes`/`raw_sha256`/`fetched_utc` live at the record top level,
not under `http.*` — the checklist's prose reads fine, the keys are where the instrument looks.)

**2. Quote pins — HOLD.**
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057`:
```
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
exit=0
```
Exactly the checklist's four `OK occurrences=1` lines at anchors 12/132/136/184.

**3. Row and registry — HOLD on substance; one stale anchor in the checklist (F3).**
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `59` (E1 erratum figure, not the
frozen 58). `awk -F'|' '/^\| S057 \|/{print NF}'` → `13`. S057 cells: kind `docs`, tier `A`, status `mined`,
opened `2026-10-26`, recheck `180d`, used-by `corpus/knowledge/cisa-when-to-issue-vex.md`; source cell
carries exactly one `https://` token, byte-equal to the manifest `url`. Rejected rows S056/S058/S059: each
NF=13, exactly one URL token, `REJECTED=` 1 and `flip=` 1 per row (awk count over the three rows). The
`## Registry changes` bullet (`corpus/SOURCES.md:131`) records "Registry 55 rows pre-append → 59
post-append (R8)". Position: `## Registry` at L3; rows S055–S059 at L61–L65; `## Paths` at **L67** — the
checklist says "closed by `## Paths` at L63", stale by exactly the 4 appended rows (see F3). The enforcing
rule exists: `scripts/sources-census.sh:30` defines `E12 row-shaped source outside the ## Registry section`
and its selftest asserts `E12-row-outside-registry-exit-1` (`:281-284`, indented variant `:341`).

**4. Frontier row — HOLD.**
`grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `22`; `awk -F'|' '/^\| F22 \|/{print NF}'` → `8`. F22 sits in
the EOF section `## Round-39 admission — coverage map row and Frontier F22 (appended 2026-10-26)`
(`corpus/README.md:488`, row at `:506`), sources cell `S057`. The entry
`corpus/knowledge/cisa-when-to-issue-vex.md` (144 lines) carries the header line map naming L12-L14,
L79-L81, L132-L135, L136-L138, L183-L186 (`:3`) and quotes them (`:20`, `:22`, `:98-99`, `:113`, `:129`,
`:131`); `grep -rlE '^source: S057' corpus/knowledge | wc -l` → `1`.

**5. Harness — HOLD.**
`python3 corpus/instruments/frontier-recheck-count.py` → 25 PASS lines ending
`PASS     F22  knowledge/cisa-when-to-issue-vex.md               ids=S057           exit=0`, then
`entries=25 pass=25 exit=0`. Base-state figure reproduces too: `git archive 480b1a50… | tar -xf -` into
scratch, `python3 corpus/instruments/frontier-recheck-count.py --root <export>` → `entries=24 pass=24
exit=0`.

**6. Binding, audit, census — HOLD; one stale anchor in the checklist (F3).**
`python3 corpus/instruments/capture-binding-check.py` → 15 MANIFEST lines including
`MANIFEST round-39 records=1 url_bound=1 fetched=1`, AUDIT line, `records=46 bound=46 unbound=0`, exit 0.
`python3 corpus/instruments/recheck-audit.py --quiet` → `strict pass=51/51 …`, `lines=51 total=51
pass=51 fail-closed=24 …`, `expect=present expected=51 missing=0 unexpected=0 exit=0`. The new entry is
listed in `corpus/instruments/knowledge-expected.txt` in C-locale order — at **L8**, between
`cisa-kev-catalog.md` (L7) and `citation-bases.md` (**L9**, not L8 as the checklist says; see F3).
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` →
`W04 S028`, `W04 S029`, `ok`, `exit=0` — only the two pre-existing warnings.

**7. Junk red — HOLD.**
With `TMPDIR=$S`: `cp .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt $S/S057.txt;
cp .ufo/waves/round-39/wave1/ExecJunkRecheck.manifest.json $S/manifest.json;
python3 corpus/instruments/source-recheck.py --manifest $S/manifest.json --source S057`:
```
S057:sha256 OK
S057:J1 MISMATCH reason=quote-not-found
S057:J2 MISMATCH reason=quote-not-found
S057:J3 MISMATCH reason=quote-not-found
S057:J4 MISMATCH reason=quote-not-found
exit=1
```
Exactly the checklist's red.

**8. C1 receipts at the judged head — PARTIAL: the bytes are sound, the counting command does not
reproduce 8/8 on the live lane during wave 2 (F1), and the documented J-run figure is stale (F2).**
`R=.ufo/waves/round-39/final-gates/all-gates.txt`; `J=46c66c268502abd1b2c342fc71bf88ccf721845b`
(receipt `:2`), `Y=$(git rev-parse HEAD)=5006097a84305267c9a3e8c1e1d560e60fe41d37`;
`git diff --name-only J Y` → `.ufo/waves/round-39/final-gates/all-gates.txt` only; `git merge-base
--is-ancestor J Y` → ok.

Receipt-level checks — all HOLD: `head -1` → `all-gates v3`; `grep -cE
'^export-ref=[0-9a-f]{40}$'` → 1; `grep -cE '^suite-sha256=[0-9a-f]{64}$'` → 1 and equal to
`sha256sum corpus/instruments/r39-closure.sh` = `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`;
`grep -cE '^G[0-9] payload=.*closed=1$'` → 8 with zero `closed=0` lines; `grep -cE '^closed=8/8
exit=0$'` → 1; eight graded `selftest case=G<n> positive=pass mutants=<a>/<b> verdict=pass` lines
(a=b ∈ {4,8,2,6,4,4,3,3}, all ≥1) and exactly one `selftest cases=8 failures=0`.

Plain run: `bash corpus/instruments/r39-closure.sh` → "refusing to run against the live worktree:
this suite is export-mode only." `exit=2` ✓.

Reds — HOLD: `--export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a` → `closed=2/8 exit=1`;
`--export-ref 66703acaaff50529a35be49aa8759d04140720ad` (40-char, per E2) → `closed=2/8 exit=1`;
the frozen 37-char spelling `66703aca50529a35be49aa8759d04140720ad` → "cannot resolve export ref",
`exit=2` (harness error, exactly as `wave1/ExecSuiteBuild.md` §2.4 records).

G8 pinned bytes — HOLD: `git show
2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh | sha256sum` →
`0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`, `wc -lc` → `1558 73132`; the
round-37 receipt (`corpus/../.ufo/waves/round-37/final-gates/all-gates.txt:3`) records the same
`suite-sha256`; the export copy hashes equal (G8 `export-copy=1,r37-copy=1`).

The green runs — see F1/F2 for the live-lane results:
- Clean-tree proof: `git clone --no-hardlinks` of the lane into scratch (HEAD = Y, `git status
  --porcelain` = 0 lines), then `r39-closure.sh --export-ref Y --lane <clone> --work <scratch>/wClone
  --scratch-root <scratch>/g6root` → all eight `G<n> … closed=1`, `G8 … r37-closed=1,r37-exit=0`,
  **`closed=8/8 exit=0`**. The landed bytes close every check when the live-tree state matches the
  filing-time semantics.
- Live lane, checklist's literal command (`TMPDIR=$S bash corpus/instruments/r39-closure.sh --export-ref
  Y`): **`closed=7/8 exit=1`** — G8 `r37-closed=0,r37-exit=1` (F1).
- Run at J: clean clone → `G2 payload=receipt=0,… closed=0` and **`closed=6/8 exit=1`** (G8 red via the
  pinned r37 suite's E9 `head-match=0`, because J is no longer the live HEAD); live lane → also 6/8 (F2).
- Selftest, clean clone + controlled scratch root → eight graded case lines, every mutant rejected
  (`selftest detail=G<n> mutant=… rejected=1`), `selftest cases=8 failures=0`, exit 0 ✓. Selftest,
  literal on the live lane → `cases=8 failures=2` (G6 positive: 29 sibling seat dirs under
  `/fast/scratch/hyaku/kasegi-r39`; G8 positive: dirty tree); all mutants still rejected.

G5 label check — HOLD: `grep -c 'Final lane commit:' SHONEN.md` → 0; the round-39 lines of SHONEN.md
carry none; `grep -n '46c66c26\|5006097a' SHONEN.md SCORECARD.md` → no hits (judged head named by
reference only); G5 payload `round39-section=1,final-lane-commit=0,correction=2,correction-labeled=1`.

**9. Quiescence and cleanliness — HOLD at filing semantics; current wave-2 state documented (feeds F1).**
- `git -C <lane> status --porcelain` → 5 untracked entries, all wave-2 dispatch bookkeeping created after
  the claims freeze: `.ufo/waves/round-39/kasegi-r39-falsify.ready`,
  `.ufo/waves/round-39/kasegi-r39-falsify.ready.dispatched`, `.ufo/waves/round-39/wave2-dispatch.json`,
  `.ufo/waves/round-39/wave2-run.err`, `.ufo/waves/round-39/wave2/`. (At filing the tree was clean — the
  pinned r37 suite's E9 measured `status-dirty=0` then and `status-dirty=5` now, naming exactly these.)
- `ls -A /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38` → `No such file or directory`
  for both ✓.
- `ls -A /fast/scratch/hyaku/kasegi-r39` → 30 entries (the L1's `gates-work` plus the live wave-2 seat
  dirs, this receipt's scratch included). At filing it held the run's own work dir only; the G6
  controlled runs demonstrate the check's semantics (own-work chain accepted, sibling/leftover rejected,
  unreadable root red).
- Lesson pending markers: `grep -c '⟨pending' corpus/lessons/round-39.md` → 0 (exit 1); under the full
  suite-family vocabulary (`corpus/instruments/r38-closure.sh:503`: `⟨pending`, `<fill>`, `filled by the
  L1`, `<LANE_HASH>`, `<r38-`) every token counts 0 in `corpus/lessons/round-39.md` ✓.

## Findings

**F1 (main — reproducibility of the frozen C1 counting command).** The frozen command
`bash corpus/instruments/r39-closure.sh --export-ref <Y>` does not print `closed=8/8 exit=0` on the live
lane while wave 2 runs. Observed: `closed=7/8 exit=1`, `G8 payload=…,r37-closed=0,r37-exit=1 closed=0`.
Root cause (measured, not inferred): G8 runs the pinned r37 bytes with `--export-ref <run ref> --lane
<lane>` (`r39-closure.sh:962`), and the r37 suite's E9 requires the LIVE lane `git status --porcelain` to
be empty (`r37-closure.sh:596-603`, limb `porcelain_lines -eq 0`); the lane currently carries exactly 5
untracked wave-2 dispatch entries (listed under item 9), so the pinned run prints `E9 payload=…,status-dirty=5,… closed=0`
and `closed=13/14 exit=1`. Proof the landed bytes are sound: the identical command against a clean clone
of the same HEAD prints `closed=8/8 exit=0` with `r37-closed=1,r37-exit=0`. So this is a state-dependent
green window, not a bytes defect: every wave-2 verification of C1 (including the L1's own re-run) is red
until the wave-2 dispatch bookkeeping is committed or removed, and the checklist's item-8/item-9
"empty at filing" semantics cannot be observed literally during wave 2. The same state breaks the
selftest's G6+G8 positive limbs (`cases=8 failures=2` literal vs `failures=0` on a clean clone with a
controlled `--scratch-root`). Direction is fail-closed (more red, never falsely green); no kill rule
fires (the kill rule's reds are base/r38-head, which stay red). Routed suggestion: commit the wave-2
dispatch files before the wave-2 verdict is scored, or record in the round-40 fixtures that the C1
counting command is defined over a clean-tree state.

**F2 (minor — stale documented J-run figure).** Erratum E4 and checklist item 8 state a run at J prints
`closed=7/8 exit=1` "by construction". Measured now on a clean clone (controlled scratch root):
`--export-ref 46c66c268502abd1b2c342fc71bf88ccf721845b` → `G2 payload=receipt=0,… closed=0` AND
`G8 … r37-closed=0,r37-exit=1 closed=0` → **`closed=6/8 exit=1`**; the live lane gives the same 6/8 (G8
red via `status-dirty=5`). The 7/8 figure holds only in the pre-receipt-commit state (J as the live
HEAD, tree clean): the pinned r37 suite's E9 `head-match` limb requires the run ref to equal the live
HEAD (`r37-closure.sh:606-608`), so once Y is HEAD any J-run loses G8 as well. Fail-closed direction; E4
marks the J-run non-kill, so no kill fires — but the documented figure is stale for every post-Y
verification and should be corrected (E4-2 class) rather than re-quoted.

**F3 (minor — two stale line anchors in the executed checklist).**
(a) Item 3: "closed by `## Paths` at L63" — `grep -n '^## Paths' corpus/SOURCES.md` → `67`. The four
rows appended this round (S057, S056, S058, S059 at L62-L65) shifted the heading; 63+4=67.
(b) Item 6: "`citation-bases.md` (L8)" — `sed -n '5,10p' corpus/instruments/knowledge-expected.txt`
shows `cisa-when-to-issue-vex.md` at L8 and `citation-bases.md` at L9; the round's own expected-list
line shifted it. Both items' substance holds; only the anchors are stale (the checklist was composed
before the appends it describes). Exact commands and outputs above.

**F4 (minor — r39 receipt dropped the run-ref line the r38 receipt carried).** The r38 receipt records
`run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e` at `:4`; the r39 receipt's `:4` is
`run-utc=2026-10-26T21:35:00Z` and no line names the ref its `closed=8/8 exit=0` lines were measured
over. A non-author reading `all-gates.txt` alone sees `export-ref=46c66c26…` (J) adjacent to
`closed=8/8 exit=0` — the same "8/8 over the judged head" reading that the round-39 `Correction (round
39)` lines (`corpus/lessons/round-38.md:311`, `SCORECARD.md:1560`, `SHONEN.md:190`) just established as
an overstate for the r38 receipt. The truth (8/8 over run-ref Y = J + receipt) is recoverable from the
suite header ("THE GREEN WINDOW"), E4, and `wave1/ExecSuiteBuild.md` §Runs, and G2's Y-run validation
(`receipt=1,export-ref=1,ancestor=1,diff-clean=1`) enforces it — but the receipt bytes themselves invite
the misreading. Routed suggestion: restore a `run-ref=` line in the receipt format (round-40 fixture
class; not landed by this seat).

## Environment notes

- No tools installed or upgraded (none needed); pacman untouched.
- This session's `grep` is a shell builtin whose `-o` returns nothing; the checklist's J extraction
  (`grep -oE '^export-ref=[0-9a-f]{40}$' … | cut -d= -f2`) yields empty here. Equivalent anchored form
  used throughout: `grep '^export-ref=' … | cut -d= -f2` (verified equal to the `-o` semantics on a
  normal grep; all `-c` counts unaffected). Recorded so a future seat does not misdiagnose its own
  extraction as a receipt defect.
- All scratch bound under `/fast/scratch/hyaku/kasegi-r39/RevGateReadiness/` (work dirs `wY`, `wJ`,
  `wBase`, `wR38`, `wClone`, `wSelfClone`, `wE2`, `r37pin`, `r37work`, `r37work-clone`, `baseexp`,
  `g6root`, junk `mktemp` dirs via `TMPDIR=$S`); removed before yield. The scratch `laneclone` is a
  read-only-source `git clone --no-hardlinks` used solely to obtain the filing-time clean-tree state;
  the lane repo itself was never written and no mutating git/jj command was run anywhere (reads only:
  status, log, rev-parse, diff, show, archive, cat-file, merge-base --is-ancestor).

## Bottom line

Items 1-7 and 9 reproduce exactly as the checklist states. Item 8's receipt-level checks, refusal, reds
and pinned-byte digests all reproduce; the 8/8 green and the selftest's 8/0 reproduce on a clean tree
(clone proof) but NOT on the live lane during wave 2 (F1), and the documented J-run figure 7/8 is stale
at the current head (F2). Two stale line anchors in the checklist itself (F3) and the r39 receipt's
dropped run-ref line (F4) complete the defect list. No frozen kill rule fires on any observed state.
