# MutErratumCheck — mutation battery on the M31-1 closure checks (round 31, wave 2)

Seat: MutErratumCheck (leaf, mutation-tester). Answering model actually run on: `zai/glm-5.3-flash`
(workstation config route; no model passed by this seat). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Subject under test: the two shipped M31-1 closure checks (CHECK A → `SCORECARD.md`, CHECK B → `LOG.md`)
verbatim from `.ufo/waves/round-31/wave1/ExecErratumCheck.md`, transcribed byte-for-byte into a
`mktemp -d` scratch dir and run with `$1` bound to scratch file paths. All mutation work happened in
scratch; the lane was never written except this receipt.

## 0. Snapshot and baseline validity (before any mutant)

```
$ sha256sum SCORECARD.md LOG.md; wc -l SCORECARD.md LOG.md
5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7  SCORECARD.md   (860 lines)
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md         (1582 lines)
```

Both equal the wave-1 green-after digests → quiescent landed bytes (bound 6). Scratch pristine copies
hash-identical to these. Baselines (required first; a baseline failure is inconclusive, not a kill):

```
$ bash checkA.sh $D/sc-pristine.md
file=…/sc-pristine.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1
erratum_closure=closed
exit=0
$ bash checkB.sh $D/log-pristine.md
file=…/log-pristine.md round30_h2_headings=1 round30_h2_or_h3_headings=2
log_closure=closed
exit=0
```

Behavior-bearing points located on the snapshot: premise `SCORECARD.md:813`; anchor heading `:837`
(`### Round-31 erratum to the round-30 section`); erratum line `:839` (quotes the phrase and carries
`strict pass=43/43`); `LOG.md:1469` (`## Round 30 — …`), `LOG.md:1550` (`### Round-30 checks re-run…`).

Honest process note: a first invocation pass passed wrong scratch filenames (`a.md` instead of
`m-a-sc.md`); every row then showed the file-not-found signature (`stale_paragraphs=` empty,
`erratum_anchor=none`, exit 1) — `invalid:file-not-found`, discarded, no verdict taken from it. The
matrix below is the corrected re-run.

## 1. Matrix — commands, actual outputs, verdicts

Scratch dir was `/var/tmp/muterratum-r31.1uvxe01x` (deleted after; §3). `right` = the answer the
closure semantics demand. Mutant sha256 (16-hex): a `4f4a0e3a267fd2b1`, b `0912c85a9cd9a9f5`,
c `1c1a3d792ae7d51e`, c2 `3860ae53436d8fc2`, e `f12146c6298bff2f`, e2 `23c49df6aa91fc2a`,
d1 `7b8f90759fde0f02`, d2 `fdac180d756e5731`, d3 `391b35998e86cc73`.

| # | Mutant (construction, minimal diff) | Command | Output (decisive fields) | Exit | Right | Verdict |
|---|---|---|---|---|---|---|
| a | erratum block present but names a different paragraph: phrase `recheck-audit open item` renamed to `recheck-audit strict-limb item` on all lines ≥837 only (1 line changed) | `bash checkA.sh …/m-a-sc.md` | `stale_paragraphs=1 erratum_anchor=837 names_item_and_cites_corrected_audit=0` / `erratum_closure=open` | **1** | 1 | **killed** |
| b | erratum token spelled `r31 errata`: heading `:837` → `### r31 errata to the round-30 section` (1 line) | `bash checkA.sh …/m-b-sc.md` | `stale_paragraphs=2 erratum_anchor=837 …=1` / `erratum_closure=closed` | **0** | 0 | **passes, correctly** — `[Ee]rrata?` accepts `errata` by design; closure is genuine, spelling variant is inside the published anchor shapes |
| c | stale paragraph reworded in place so the grep no longer matches (`open`→`pending` at `:813`), **erratum absent** (head −n 836) | `bash checkA.sh …/m-c-sc.md` | `stale_paragraphs=0 erratum_anchor=none …=0` / `erratum_closure=closed` | **0** | **1** | **SURVIVOR** — vacuous pass (§2) |
| c2 | premise reworded in place, erratum still present (1 line at `:813`) | `bash checkA.sh …/m-c2-sc.md` | `stale_paragraphs=1 erratum_anchor=837 …=1` / `closed` | 0 | 0 | passes for closure; the in-place edit itself is invisible to a shape check (wave-1 R-3), which is why git-diff append-proofing stays necessary |
| e | erratum present twice: block 837–EOF duplicated verbatim at EOF | `bash checkA.sh …/m-e-sc.md` | `stale_paragraphs=3 erratum_anchor=837 …=1` / `closed` | 0 | 0 | **passes, correctly** — duplicate is redundant, not invalidating; closure genuinely held |
| e2 | decoy erratum first (names other paragraph) + genuine erratum appended second (probes `head -1` anchor selection) | `bash checkA.sh …/m-e2-sc.md` | `stale_paragraphs=2 erratum_anchor=837 …=1` / `closed` | 0 | 0 | passes, correctly — a genuine erratum exists in-file; cosmetic only: the reported anchor line is the decoy's |
| d1 | LOG entry heading present but for round 29 only: `:1469` `## Round 30 —` → `## Round 29 —`; the `:1550` h3 `Round-30 checks re-run` left intact | `bash checkB.sh …/m-d1-log.md` | `round30_h2_headings=0 round30_h2_or_h3_headings=1` / `log_closure=closed` | **0** | **1** | **SURVIVOR** — h3 tolerance absorbs a mislabeled entry (§2) |
| d2 | strict control: no first-token-30 heading anywhere (d1 plus `:1550` relabeled Round-29) | `bash checkB.sh …/m-d2-log.md` | `round30_h2_headings=0 round30_h2_or_h3_headings=0` / `open` | 1 | 1 | **killed** — the h2 path is sound; the hole is exactly the h3 branch |
| d3 | cost probe: wave-1 matrix-C2 shape, h3-only `### Round-30 backfill (appended)` on pre-entry bytes | `bash checkB.sh …/m-d3-log.md` | `round30_h2_headings=0 round30_h2_or_h3_headings=1` / `closed` | 0 | 0 (per wave-1's shipped contract) | passes by the deliberate h3 tolerance; this is what a CHECK-B tightening would give up |

## 2. Survivors and smallest tightenings (for ScribeQuality's R16 row)

**Survivor 1 — CHECK A, mutant (c): vacuous closure.** The predicate
`[ "$n" -eq 0 ] || [ "$c" -eq 1 ]` lets "premise phrase absent" close the check with
`erratum_anchor=none`. On an append-only scorecard (R9/R25-1), absence is achievable by rewriting the
stale paragraph — the exact anti-protocol the erratum exists to avoid — and the check blesses it
silently. Smallest tightening: **drop the first disjunct**, close iff `names_item_and_cites_corrected_audit=1`:

```sh
if [ "$c" -eq 1 ]; then echo "erratum_closure=closed"; exit 0; else echo "erratum_closure=open"; exit 1; fi
```

Verified sweep of the tightened check over all seven SCORECARD byte-states: pristine `0`;
a `1`; b `0`; c `1` (now killed); c2 `0`; e `0`; e2 `0` — kills the vacuous branch with no green
regression and no new false-opens (`stale_paragraphs`/`erratum_anchor` still printed for auditability).

**Survivor 2 — CHECK B, mutant (d1): h3 tolerance absorbs a mislabeled entry.** With the round-30
entry heading relabeled round 29, `round30_h2_or_h3_headings=1` comes only from the sub-section
`### Round-30 checks re-run for this append` (`LOG.md:1550`), which is a re-run note, not
an entry; the check still exits 0. Smallest sound tightening: make the h3 count non-load-bearing —
`if [ "$h2" -ge 1 ]; then` (keep printing both counts). Verified: pristine `0`, d1 `1` (killed), d2
`1`. Disclosed cost, measured: d3 (h3-only backfill, wave-1 matrix C2) flips to `1` — this reverses
wave-1's deliberate h3 tolerance, which R-2 already disclosed as a known bound. Alternatives (entry-
shape keyword lists for the h3) are brittle; recommend either the h2-gated predicate or ship-as-is
with R-2 standing, at the R16 owner's discretion. A coverage finding, not a contract change: per role,
survivors are reported, not relabeled.

Both tightenings keep every wave-1 matrix case verdict intact except exactly the surviving shapes
documented above.

## 3. Restoration evidence

```
$ sha256sum SCORECARD.md LOG.md        # after all runs
5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7  SCORECARD.md
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md
$ rm -rf /var/tmp/muterratum-r31.1uvxe01x && ls /var/tmp/muterratum-r31.1uvxe01x
ls: cannot access '/var/tmp/muterratum-r31.1uvxe01x': No such file or directory
```

Lane bytes byte-identical before/after (digests above); scratch tree deleted. The lane was mutated
nowhere; all mutants lived and died in `/var/tmp`.

## 4. Bounds

No lane write except this receipt; no git/jj mutation anywhere (lane reads only; no git fixtures
needed); no tool installed or upgraded (stdlib bash/grep/awk/python3 only; no pacman transaction); no
writes to fleet root, siblings, `/home/vgpnk/.scratch/`, or the campaign package (never read its
tools, never ran them); no live bounty contact; no credential material. Coordination: survivor report
messaged to `agent://ScribeQualityFix` by id, as tasked.

## 5. Result

| Mutant | Check | Exit | Right | Verdict |
|---|---|---|---|---|
| (a) erratum names a different paragraph | A | 1 | 1 | killed |
| (b) token spelled `r31 errata` | A | 0 | 0 | passes, correctly (designed `[Ee]rrata?` tolerance) |
| (c) premise reworded, no erratum | A | **0** | **1** | **SURVIVOR** — vacuous `n=0` branch; tighten to `[ "$c" -eq 1 ]` (verified) |
| (e) erratum present twice | A | 0 | 0 | passes, correctly (redundant duplicate) |
| (d) heading for round 29 only | B | **0** (d1) / 1 (d2 strict control) | **1** | **SURVIVOR** via h3 branch; tighten to `[ "$h2" -ge 1 ]` (verified; d3 cost disclosed) or ship-as-is under R-2 |

Baseline green on both checks before any mutant; both baselines matched wave-1's after-run numbers
exactly. Two survivors reported with measured, minimal tightenings; no contract relabeled.

## 6. Addendum (post-run drift, 2026-10-25, after ScribeQualityFix adopted R18/R19)

This battery's evidence is pinned to the snapshot era `SCORECARD 5fa41aef…` / `LOG 864deb7d…` /
`recheck-audit.py 3fc0d751…` (live `strict pass=43/43`); the matrix above is valid for that era only —
do not compare it against later eras (bound 6 / M30-3). Verified after the fact, read-only:

```
$ sha256sum corpus/instruments/recheck-audit.py | cut -c1-16
5d4842da6103f17c
$ python3 corpus/instruments/recheck-audit.py --quiet; echo "audit_exit=$?"
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
expect=present expected=44 missing=0 unexpected=0 exit=0
audit_exit=0
$ sha256sum SCORECARD.md LOG.md
4076091c…  SCORECARD.md   (was 5fa41aef… at snapshot; +87 lines appended, 0 deleted — Round-31
                           section landed below the erratum block; first anchor unchanged)
864deb7d…  LOG.md         (unchanged)
```

Contract amendment adopted by the R16 owner (QUALITY.md R18, supersedes R16): CHECK A' pins the filed
premise span `SCORECARD.md:813-819` to digest `d6c6ea77…`, requires phrase count >=2, an erratum
citing `SCORECARD.md:813-819`, and a live `strict pass=` reading carrying the live value plus live
8-hex instrument digest. Consequence, accepted as the owner's call: probe c2's classification flips
`right=0` → `right=1` (the byte-identity pin now makes an in-place premise edit a red, not a green) —
this receipt's c2 row records the R16-era verdict and stands for that era. CHECK B' is the h2-gated
form as proposed here; its d3 cost (h3-only backfill reads open) was accepted by the owner on the
observation that no round entry in `LOG.md` is filed at `###`. No mutant relabeled by this seat.

Supersession (2026-10-25, later same day): ScribeQualityFix re-ran A' on the drifted bytes
(`SCORECARD 4076091c…`, 947 lines, span `:813-819` still `d6c6ea77…`, verdict unchanged, exit 1) and
fixed a defect found via this addendum's drift note — arm (iii) had keyed on the *last* `strict pass=`
line at/after `:813`, which the C1 move-log row at `:875` would mask; the predicate now scans every
window and closes on any carrying live value + live 8-hex digest + the filed address. Re-measured on
13 byte-states, all earlier verdicts unchanged. This section's R18 description is the intermediate
framing; cite ScribeQualityFix's Checklist A' §8 13-state table (digest transition
`96b71caa`→`5899e02b`→`5c2903ff`→`300f9962`) as the superseding measurement, not their §2.
