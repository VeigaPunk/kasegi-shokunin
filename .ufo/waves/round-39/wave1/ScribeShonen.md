# ScribeShonen — round 39: the four SHONEN.md round-39 lines

Seat `ScribeShonen`, role scribe, leaf (no subagent dispatch). Item: draft four `[~]` box lines — one
per promotion box, round-38 style, each with an evidence pointer to this round's
deliverables/commits — byte-exact to
`.ufo/waves/round-39/wave1/ScribeShonen.shonen.append.md`. Deliverable only: no product code, judge,
gate file or front-door file was edited; `SHONEN.md` itself was not touched by this seat — it read
187 lines at the start of the seat and 200 lines at filing, after two appends made outside this seat
(§5, "SHONEN.md drifted"); nothing was committed, pushed or published.

## 1. Inputs read (read-only)

| Input | What it gave |
|---|---|
| `SHONEN.md` (187 lines at this seat's first read; 190 after the L1's `Correction (round 39)` append, 202 at the final read after further L1 appends, §5) | the four box titles verbatim — `grep '^- \[~\] ' SHONEN.md \| sort -u` returns exactly the four unique titles the block opens with — and the round-36/37/38 append style (`[L1-MEASURE]` slots for integration-time values) |
| `.ufo/waves/round-39/claims.json` | C1 predicate with G1-G8, C2 predicate and counting commands, the judged-head rule (`J` = the `export-ref=` value in `final-gates/all-gates.txt`) |
| `.ufo/waves/round-39/claims-erratum-1.md` | E1 (registry 55 → **59**, not the frozen 58), E2 (r38 head full form), E4 (the 8/8 run is at **Y** = J + receipt; J itself prints `closed=7/8 exit=1`), E5 (non-vacuous measurement semantics) |
| `.ufo/waves/round-39/wave1-spec.json` | 49 seats, role census below; the fixed deliverable names the block points at; no hunt-to-claim seat |
| `.ufo/waves/round-39/{c1-controls,c2-controls,census-before.txt}` | the frozen base limbs the block's "base …" sentences are checked against |
| landed wave-1 deliverables (read at filing) | `ExecFrontierCapture.manifest.json` + `.S057.txt`, `ScribeRowS057.row.md`, `ScribeFrontierF22.readme.append.md`, `ScribeProvinceF22.province.append.md`, `ExecJunkRecheck.junk-recheck.txt`, `ScoutSiblingF22.sibling.md`, `ScribeEntryF22.entry.md` + `.md`, `ExecHarnessProbe.harness.txt`, `ExecCensusAfterMirror.mirror-metrics.txt`, `ExecSuiteBuild.r39-closure.sh`, `ExecArchiveChecks.base-gates.txt` |

## 2. Measurement (this seat)

Scratch `S=/fast/scratch/hyaku/kasegi-r39/ScribeShonen`, `TMPDIR=$S`, every work copy under `$S`;
`$S` removed at §7 after the deliverable and this receipt were written into the wave dir. Lane HEAD
at filing `d65d823` (round-39 wave-1 spec/dispatch), base `480b1a50`.

### 2.1 Base counters (box 3's "base limbs")

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                    -> 21
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          -> 55
$ ls corpus/knowledge/*.md | wc -l                                              -> 50
$ grep -rlE '^source: S057' corpus/knowledge | wc -l                            -> 0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -1                -> entries=24 pass=24 exit=0
$ python3 corpus/instruments/capture-binding-check.py | tail -1                 -> records=45 bound=45 unbound=0
$ python3 corpus/instruments/recheck-audit.py --quiet | tail -1                 -> expect=present expected=50 missing=0 unexpected=0 exit=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

### 2.2 SKILL.md base limb (box 1)

```
$ wc -l -c SKILL.md                         -> 1114  111619
$ sha256sum SKILL.md                        -> 0937bce505de6ac9ddd74115002e01aa51aabfa10b557495493021c619b7cd53
$ python3 corpus/instruments/anchorcheck.py SKILL.md ; echo exit=$?
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
$ python3 corpus/instruments/density.py SKILL.md --label base39 | tail -3
| 27 | Round-36 Gates & probes registry addition (appended 2026-10-26) | 9 | 8 | 26 | 5 | 11 | 2 | 44 | 550.0 |
| | **mean dens** | | | | | | | | **233.1** |
Total path-citation instances: 768 across 27 blocks.
```

The same base values reproduce in `ExecArchiveChecks.base-gates.txt` (its `anchorcheck.py` run and
the `density.py` table ending `mean dens 233.1`).

### 2.3 Round-39 artifacts quoted in the block (hash-verified here)

```
$ cd .ufo/waves/round-39/wave1
$ wc -l -c ExecFrontierCapture.S057.txt        -> 275  17971
$ sha256sum ExecFrontierCapture.S057.txt       -> 11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f
$ sha256sum ScribeFrontierF22.readme.append.md -> a8aa90a29215c1ef73e76e7beec8e9dee7b96d3d6f3f00afd4d84a7625b22d25
$ wc -l -c ScribeFrontierF22.readme.append.md  -> 28  2085      # opens no fence: grep -c '^```\|^~~~' -> 0
$ wc -l -c ScribeProvinceF22.province.append.md -> 1  262
$ sha256sum ScribeProvinceF22.province.append.md -> bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d
$ wc -l -c ScribeEntryF22.entry.md             -> 144  19196
$ sha256sum ScribeEntryF22.entry.md            -> 5010a107cc7ef34bcd7e8d1a74eb2a2bb2a71c3ea666577506d7c2f93dc25d29
$ wc -l -c ScribeRowS057.row.md                -> 1  948        # 11 cells, NF=13 pipe-split
```

Manifest values quoted in box 2 (`ExecFrontierCapture.manifest.json`): `http.status=200`,
`fetched_utc=2026-10-26T19:30:55Z`, PDF `fetched_bytes=235270`, landing page `raw_bytes=54453`
sha256 `4e6aa483…`, capture `lines=275`, `snapshot_bytes=17971`, `sha256=11c8d6d6…`; quote anchors
Q1 `L12-L14`, Q2 `L132-L134`, Q3 `L136-L138`, Q4 `L184-L186`.

### 2.4 Suite facts this seat executed (box 3)

```
$ bash -n .ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh ; echo syntax_exit=$?
syntax_exit=0
$ bash .ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh ; echo plain_exit=$?
r39-closure: refusing to run against the live worktree: this suite is export-mode only.
r39-closure: pass --export-ref <hash> (see --help) or --selftest.
plain_exit=2
```

`ExecSuiteBuild.md` (landed, tracked, in the L1's wave-1 integration commit) supplies the run
results the block now quotes: base export `480b1a50…` → `closed=2/8 exit=1` (§2.3), round-38 judged
head → `closed=2/8 exit=1` in both hash spellings (§2.4), `--selftest` at base →
`selftest cases=8 failures=6` with eight graded case lines and every mutant rejected (§2.6), and the
scratch overlay head carrying the round's evidence → `closed=8/8 exit=0` and
`selftest cases=8 failures=0` (§2.7). Only the run at the verification ref Y (erratum E4) remains
`[L1-MEASURE]` until `final-gates/all-gates.txt` is filed.

### 2.5 C2 counters on the composed after-mirror (attributed)

`ExecCensusAfterMirror.mirror-metrics.txt` (mirror = `git archive` base + the wave-1 deliverables):

```
mirror-after-cd: harness  PASS F22 ids=S057 exit=0 ; entries=25 pass=25 exit=0
                 audit    strict pass=51/51 cdroot_fail=0 instrument_fail=0 own_fail=0
                          expect=present expected=51 missing=0 unexpected=0 exit=0
                 binding  records=46 bound=46 unbound=0
                 frontier 22 rows ; knowledge 51 ; registry 59 (erratum E1) ; census exit=0
```

`ExecHarnessProbe.harness.txt`: the same after-state through the harness with every cut limb redding
exactly one row (`missing-entry`, `manifest-unreadable`, `recheck-exit-2`, `--source` swaps,
`selection-not-cited-by-entry`). `ScribeEntryF22.md`: the entry's own `recheck:` line prints
`S057:sha256 OK` then `Q1..Q4 OK` (`anchor=12/132/136/184-ok`), `trio_exit=0`.

### 2.6 Junk twin, sibling sweep, front-door base state (box 4)

`ExecJunkRecheck.junk-recheck.txt`: `S057:J1..J4 MISMATCH reason=quote-not-found`, `exit=1`, with a
positive control (`Q1`/`Q2` OK, exit 0) and an isolation control (genuine sentences under ids J1-J4
at the same path/digest, exit 0). `ScoutSiblingF22.sibling.md` ruling: "No sibling lane and no
shokuknow merge row holds the VEX issuance/lifecycle/reaffirmation/inheritance ground." over 20 lane
roots (829,134 files) and the shokuknow tree (24,415 files). Base front doors: `PROVINCE.md` 156
lines (last line = the round-38 F21 amendment; the r39 line lands at L157), `corpus/README.md` 486
lines with a paired two-fence set (EOF closed), no `~~~`.

### 2.7 Dispatch shape and LOG state (box 2)

```
$ python3 -c 'Counter(role) over .ufo/waves/round-39/wave1-spec.json["items"]'
seats 49 {'executor': 27, 'scribe': 11, 'reviewer': 6, 'scout': 2, 'critic': 2, 'connector': 1}
$ grep -n '^## Round 3[7-9]' LOG.md      -> 1678 (Round 37), 1694 (Round 38); no Round 39
$ wc -l LOG.md                           -> 1702
```

## 3. Deliverable

`.ufo/waves/round-39/wave1/ScribeShonen.shonen.append.md`

| Field | Value |
|---|---|
| Lines | **70** (`wc -l` → 70; file ends with one `\n`) |
| Bytes | **6153** |
| sha256 | **`fa252112b97fd5d012d77c61d11d9489609b0d948459ca265b68924a0ae12666`** (`HEAD:1a139e0` still carries this seat's earlier 67-line / `0b07ce09…` version, written before box 3's suite evidence was updated from `ExecSuiteBuild.md`; land the filed bytes) |
| Structure | four `- [~] ` bullets separated by one blank line, each followed by 6-space-indented `— evidence (round 39 …` continuation lines; no heading, no table, no validation text |
| Box titles | byte-equal to the four existing `- [~] ` titles in `SHONEN.md` (all four MATCH) |

Only the landable bytes are in the file; the L1 appends it at EOF after the round-38 lines.

## 4. Validation of the block

```
$ grep -c '^- \[~\] ' ScribeShonen.shonen.append.md                             -> 4
$ grep -n 'judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt' …
41:      judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt — and the committed
$ grep -c 'Final lane commit:' ScribeShonen.shonen.append.md                    -> 0
$ grep -c '⟨pending' ScribeShonen.shonen.append.md                              -> 0
$ grep -c '\[L1-MEASURE\]' ScribeShonen.shonen.append.md                        -> 4
```

The judged-head phrase is kept whole on one physical line (a line-oriented G5 grep would otherwise
miss it). No 7+-hex hash is labelled a final or judged head (`re.findall` over
`(final|judged).{0,40}[0-9a-f]{7,}` → empty); the hashes present are the base `480b1a50`, the
round-38 closure head `66703aca…` with an ellipsis, and artifact digests `0937bce5…`, `11c8d6d6…`,
`4e6aa483…`, `a8aa90a2…`, `bd8dbc09…`, none a head label. A `$(sed -n 's/^export-ref=//p' …)`
substitution stands where a run command would otherwise quote a hash, so no literal
`--export-ref <hash> -> closed=K/K` quote exists for G3 to resolve.

Four `[L1-MEASURE]` slots, all integration-time values: (1) the landed `SKILL.md` row line/digest;
(2) the suite's two run values until `final-gates/all-gates.txt` is filed; (3) the integrated-tree
counter re-runs; (4) the landed `PROVINCE.md` line number.

## 5. Disclosures and limits

- **Expected ≠ observed (suite).** The suite's red controls (`closed=2/8 exit=1` at base and at the
  round-38 head), its honestly-red base selftest (`cases=8 failures=6`) and its green overlay run
  (`closed=8/8 exit=0`, `selftest cases=8 failures=0`) are `ExecSuiteBuild.md` §2.3-§2.7, measured by
  that seat, not by me; I executed only `bash -n` and the plain-run refusal. No receipt at
  `final-gates/all-gates.txt` exists yet, so the run at the verification ref Y and the J-`7/8`
  erratum-E4 form remain `[L1-MEASURE]` / contract form in the block.
- **Mirror ≠ integrated tree.** The C2 counters quoted as measured come from the composed after-mirror
  (`ExecCensusAfterMirror`, `ExecHarnessProbe`); `recheck-audit.py` and
  `frontier-recheck-count.py` only pass there with `--root`/a `cd`-rewritten mirror, because their
  entries carry the lane-root `cd`. The integrated-tree re-runs are marked `[L1-MEASURE]`.
- **Frozen value vs erratum (recorded, not resolved by me).** `claims.json` C2's counting command
  says `grep -cE '^\|…S[0-9]{3,}…' corpus/SOURCES.md -> 58`; erratum E1 supersedes it to **59**
  (55 base + S057 + three rejected rows), and the measured after-mirror is 59. Both texts are
  quoted here verbatim; the canonical judge decides.
- **Integration obligations no wave-1 seat owns** (each one is load-bearing for a box claim):
  (a) the `SKILL.md` Gates & probes `r39-closure.sh` row — box 1 says the L1 appends it;
  (b) `corpus/instruments/knowledge-expected.txt` must gain `corpus/knowledge/cisa-when-to-issue-vex.md`
  in C-locale order (between `cisa-kev-catalog.md` and `citation-bases.md`) or `recheck-audit.py`
  prints `unexpected=1 exit=1` and box 3's `expected=51 … exit=0` fails;
  (c) entry + `corpus/source-snapshots/round-39/S057.txt` + manifest must land in one tree, or the
  landed row reads `recheck-exit-2` (`ScribeEntryF22.md`, `ExecHarnessProbe.harness.txt` §H);
  (d) `.ufo/waves/round-39/declared-blocks.txt` must declare the `SHONEN.md` tail this block adds
  (G1), alongside the PROVINCE.md / README.md tails.
- **Wave-prompt hash correction (E2).** The round-39 prompts carry
  `66703aca50529a35be49aa8759d04140720ad` (37 chars, an invalid object name); E2 gives the real
  round-38 head `66703acaaff50529a35be49aa8759d04140720ad`. My block cites only `66703aca…` as a
  red control, never as a head, so the drift does not reach the front door.
- **Box 2 is a negative claim.** "No new end-to-end domain task ran this round" rests on the role
  census (49 seats, no hunt-to-claim seat), the absence of a `## Round 39` LOG heading at base, and
  the content of the landable deliverables (claims, instruments, F22 admission, wave, tooling).
- **Attributed, not re-run by me:** the mirror counters (§2.5), the junk controls (§2.6), the sibling
  sweep (§2.6) and the base-gate reproduction in `ExecArchiveChecks.base-gates.txt` (§2.2). My own
  runs are §2.1, §2.2, §2.3 hashes, §2.4 and §2.7.
- **Row drift.** `ScribeRowS057.row.md` read 884 B on my first pass and 948 B at filing (the seat
  rewrote it). The block does not quote its bytes; only the lesson gate's NF=13 claim depends on it.
- **SHONEN.md drifted under this seat — duplicate round-39 lines exist.** At my first read `SHONEN.md`
  was 187 lines (`wc -l` on this seat's first pass) with no round-39 lines. At my final read it is
  **202 lines**, sha256 `44b604ff4d17520d38572402e1d8c20d1b5f575c36c060efefaad078c831e094`,
  `git diff --numstat -- SHONEN.md` = `12 0`, holding three appends I did not make:
  (a) the L1's `Correction (round 39)` paragraph — byte-identical to
  `.ufo/waves/round-39/wave1/ExecCorrectionsR2.shonen.append.md` — which lands at :190; and
  (b) a **four-bullet round-39 box set at :193-200** whose lines are terser than this item's block:
  `— evidence (round 39): Gates & probes registry gains the r39-closure.sh row (single-choice gate,
  verdict map incl. exit 2) appended at EOF; every base line byte-identical; anchorcheck.py S…`,
  `no end-to-end domain hunt ran; the closest executed work is the F22 capture + harness run and the
  r39 suite run`, `frontier-recheck-count.py entries=25 pass=25 exit=0 incl. PASS F22 ids=S057;
  source-recheck --source S057 exit 0; capture-binding-check.py records=46 bound=46; …`, `PROVINCE.md
  carries the [r39 Frontier amendment] F22 line; F22/S057 uncontested … junk twin rejected`. No seat
  in `.ufo/waves/round-39/wave1-spec.json` owns `SHONEN.md` except this one, and no wave-1 deliverable
  reproduces those four lines, so their authorship is unrecorded; and
  (c) `Round-39 measured state: judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt
  (claims-erratum-1.md E4).` at :201-202, which is consistent with this block's by-reference form.
  **Consequence for integration:**
  appending this seat's block as well leaves eight round-39 box bullets (two per title); the L1 must
  land one set. This seat's deliverable is the one the item asks for and is the fuller evidence form
  (artifact hashes, mirror/receipt pointers, `[L1-MEASURE]` slots); the earlier four bullets carry no
  pointers and quote head values as if measured. I did not edit `SHONEN.md` to resolve the overlap.
- **G5 hazard in the landed correction line (reported, not mine).** The `Correction (round 39)`
  paragraph names the round-38 head by full hash next to the words "judged head J":
  "The receipt's `export-ref` is the judged head J = `66703acaaff50529a35be49aa8759d04140720ad`".
  G5 (erratum E5.4) requires the round-39 lines to name the judged head only by reference; a
  line-oriented G5 grep could read that sentence as a hash-labelled head. It is the L1's append, not
  this seat's, and erratum E2 identifies the hash as the corrected round-38 head; this seat's block
  keeps `66703aca…` ellipsised and never in a "judged head" sentence.
- `SHONEN.md` was not edited by this seat; the append is the L1's integration step.

## 6. Tooling

No installs or upgrades; `python3` 3.14.8, `git` 2.56.0, GNU coreutils and `bash` sufficed. No
pacman, no network fetch (the capture was fetched by `ExecFrontierCapture`), no host service touched,
no config file edited.

## 7. Scratch

`/fast/scratch/hyaku/kasegi-r39/ScribeShonen` was created with `mkdir -p`, held the block drafts,
`anchor.txt`, `plain.out`, `spec.txt` and `items*.txt`, and is removed after the deliverable and this
receipt were written (`rm -rf -- "$S"`, then `test ! -e "$S"` verified). No other seat's scratch dir
was touched.
