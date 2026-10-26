# ExecErratumCheck — M31-1 red-before / green-after closure receipts (round 31, wave 1)

Seat: ExecErratumCheck (leaf). Model actually run on: `devin/deepseek-v4-1-flash` (route-table decision;
never passed by this seat). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
No repo edits: this seat wrote only its three assigned artifacts
(`ExecErratumCheck-before.txt`, `ExecErratumCheck-after.txt`, this file).
Tooling: nothing installed or upgraded (no pacman transaction, no uv/npx/official binary); stdlib
shell/grep/awk/python3 only.

## 0. What was measured, and the two artifacts

| Artifact | Role |
|---|---|
| `.ufo/waves/round-31/wave1/ExecErratumCheck-before.txt` | RED-before: both closure checks exit 1 on the pre-edit bytes, plus the A–G discrimination matrix and the mutant control |
| `.ufo/waves/round-31/wave1/ExecErratumCheck-after.txt` | GREEN-after: both checks exit 0 on the post-append bytes with quiescence proof, plus the mutant controls |
| this file | receipt: commands + their output, evidence, risks |

Subject files and their digests (all sha256, computed here):

| File | Red-before | Green-after |
|---|---|---|
| `SCORECARD.md` | `cac64dbdb8cd9ed834a6deca44c5b4fd5874f1e95d2f1118f919c3ccb84811b9` (835 lines, `git status` clean) | `5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7` (860 lines, append-only) |
| `LOG.md` | `0a1865e90f29c5d4a20fa3fda8f9daf6b6293bbec95710bafcda0cf65d537221` (1467 lines, clean) | `864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b` (1582 lines, append-only) |
| `corpus/instruments/recheck-audit.py` | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` (frozen base digest) | mid-edit by ExecRALimbs during the after run (see §5) |

Append-only, verified independently here (read-only git):
```
$ git diff --stat -- SCORECARD.md LOG.md
 LOG.md       | 115 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 SCORECARD.md |  25 +++++++++++++
 2 files changed, 140 insertions(+)
$ git diff -U0 SCORECARD.md | grep -c '^-[^-]'   -> 0
$ git diff -U0 LOG.md      | grep -c '^-[^-]'   -> 0
```
i.e. zero deleted lines in either subject file: both fixes are pure appends (R9/R25-1), and ScribeErratum's own
receipt reports the same gate (`additions_only: 0`).

The stale premise, located with the pointer corrected: `SCORECARD.md:813` is the sentence head
`**recheck-audit open item (outside the frozen claims).** \`recheck-audit.py\``; the stale backticked
reading `expect=present expected=43 missing=0 unexpected=0 exit=1` is on `SCORECARD.md:814`.
Live corrected value, read-only, same tree:

```
$ python3 corpus/instruments/recheck-audit.py --quiet > /tmp/era-audit.txt 2>&1; echo "audit_exit=$?"; grep -E 'strict pass|^expect=' /tmp/era-audit.txt
audit_exit=0
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
expect=present expected=43 missing=0 unexpected=0 exit=0
```

## 1. CHECK A — SCORECARD stale paragraph (part 1 of M31-1)

Canonical, bash-n-parseable, exit 0 = closed / exit 1 = still open. `$1` optionally names the file under
test so the mutant control runs the *same* bytes against a scratch copy:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
f=${1:-SCORECARD.md}
n=$(grep -c 'recheck-audit open item' "$f")
l=$(grep -nE '(([Rr]31)|([Rr]ound[- ]31))[[:space:]]+[Ee]rrata?' "$f" | head -1 | cut -d: -f1)
c=0
if [ -n "$l" ] && tail -n +"$l" "$f" | grep -q 'recheck-audit open item' \
   && tail -n +"$l" "$f" | grep -q 'strict pass=43/43'; then c=1; fi
printf 'file=%s stale_paragraphs=%s erratum_anchor=%s names_item_and_cites_corrected_audit=%s\n' "$f" "$n" "${l:-none}" "$c"
if [ "$n" -eq 0 ] || [ "$c" -eq 1 ]; then echo "erratum_closure=closed"; exit 0; else echo "erratum_closure=open"; exit 1; fi
```

Design note: the item's seed form (`grep -cE 'r31 erratum.*recheck-audit open item'`) needs both facts on
one line; the shipped form anchors on an r31/Round-31 `Errata/Erratum` line and then requires, anywhere
after it, (a) the phrase `recheck-audit open item` and (b) the corrected literal `strict pass=43/43`.
That keeps the seed's bite and accepts a multi-line erratum block. Both shapes were verified green, and a
non-erratum `## Round 31` section carrying both phrases is rejected (matrix case G).

RED-before (pre-edit bytes, `SCORECARD.md` sha256 `cac64dbd…`):

```
file=SCORECARD.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=open
exit=1
```

GREEN-after (post-append bytes, `SCORECARD.md` sha256 `5fa41aef…` held identical before and after the run):

```
file=SCORECARD.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1
erratum_closure=closed
exit=0
```

Anchor/naming lines, verbatim: `### Round-31 erratum to the round-30 section` (`SCORECARD.md:837`);
`r31 erratum: the paragraph \`recheck-audit open item (outside the frozen claims)\` filed at
\`SCORECARD.md:813-819\` …` (`SCORECARD.md:839`); the measured block after it carries
`strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0` and
`expect=present expected=43 missing=0 unexpected=0 exit=0`.
`stale_paragraphs` moved 1 → 2 exactly because the erratum quotes the phrase; `SCORECARD.md:813-819` is
byte-identical, i.e. the fix was appended, never rewritten (R9/R25-1).

Discrimination matrix (all on scratch copies in `mktemp -d`, deleted after the run; lane tree untouched):

| Case | Construction | Output | Exit |
|---|---|---|---|
| A | live pre-edit file | `erratum_anchor=none … =0` | **1** |
| B | + single line `- **r31 erratum (recheck-audit open item).** … strict pass=43/43` | `=1` | **0** |
| C | + `### Round-31 errata (appended)` + naming bullet + citation line | `=1` | **0** |
| D | MUTANT: erratum lines deleted from C | `erratum_anchor=none … =0` | **1** |
| E | erratum names the item, `strict pass=43/43` removed | `=0` | **1** |
| F | cites `strict pass=43/43`, never names the item | `=0` | **1** |
| G | `## Round 31 — frozen claims` section with both phrases, no `Errata` anchor | `=0` | **1** |

Post-append mutant control (required by the item), verbatim:

```
$ head -n 836 SCORECARD.md > "$D/sc-mutant.md"      # erratum block (lines 837-EOF) deleted
file=/tmp/tmp.0aEpmtrKLt/sc-mutant.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=open
exit=1
```

## 2. CHECK B — round-30 `LOG.md` entry (part 2 of M31-1)

Heading shape verified in-file *first*, as the item requires: the file's round sections are
`## Round 29 — 2026-10-25 — …` (`LOG.md:1404`), `## Round 28 …` (`:1338`), `## Round 27 …` (`:1315`),
`## Round 26 …` (`:1305`), `## Round 25 …` (`:1246`), with the lowercase variant
`## 2026-10-25 — round 23: …` (`:1114`). A naive `^## .*[Rr]ound[- ]30` also matches a round-31 heading
that merely *mentions* round-30 — measured, matrix case E — so the shipped check takes the **first**
round-number token of each heading and counts headings whose first token is 30:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
f=${1:-LOG.md}
h2=$(awk '/^## /{ h=$0; sub(/^## */,"",h); if (match(h,/[Rr]ound[- ]?[0-9]+/)) { t=substr(h,RSTART,RLENGTH); gsub(/[^0-9]/,"",t); if (t+0==30) n++ } } END{print n+0}' "$f")
h23=$(awk '/^#{2,3} /{ h=$0; sub(/^#{2,3} */,"",h); if (match(h,/[Rr]ound[- ]?[0-9]+/)) { t=substr(h,RSTART,RLENGTH); gsub(/[^0-9]/,"",t); if (t+0==30) n++ } } END{print n+0}' "$f")
printf 'file=%s round30_h2_headings=%s round30_h2_or_h3_headings=%s\n' "$f" "$h2" "$h23"
if [ "$h23" -ge 1 ]; then echo "log_closure=closed"; exit 0; else echo "log_closure=open"; exit 1; fi
```

Both counts are printed so the h3 tolerance is disclosed rather than hidden: the canonical round-entry
level in this file is `## `, and the h3 tolerance exists because the file's earlier close-outs are `###`
sub-sections, so an h3-only backfill would otherwise read as still-missing.

RED-before (`LOG.md` sha256 `0a1865e9…`; the shipped form above, run on the live pre-edit file and, independently,
on the committed pre-entry bytes `git show HEAD:LOG.md` — byte-identical, digest `0a1865e9…`):

```
file=LOG.md round30_h2_headings=0 round30_h2_or_h3_headings=0
log_closure=open
exit=1
```

(The first cut of the check used only the `^## ` form and printed `round30_first_token_headings=0` — same verdict,
exit 1; the shipped form is what both the matrix and the after run use.)

GREEN-after (`LOG.md` sha256 `864deb7d…` held identical before and after the run):

```
file=LOG.md round30_h2_headings=1 round30_h2_or_h3_headings=2
log_closure=closed
exit=0
```

Headings counted, verbatim: `LOG.md:1469` `## Round 30 — 2026-10-25 — instrument conformance (frontier
missing-entry/duplicate, source stem/occurrence) + F14 Japanese severity vocabulary assimilation (one v2
wave, 64 seats)`; `LOG.md:1550` `### Round-30 checks re-run for this append (round 31, quiescent committed
bytes)`.

Matrix (shipped form, scratch copies in `mktemp -d` on the committed pre-entry bytes, deleted after the run):

| Case | Construction | Output | Exit |
|---|---|---|---|
| A | pre-state bytes (`git show HEAD:LOG.md`, digest `0a1865e9…`) | `h2=0 h2_or_h3=0` | **1** |
| B | + `## Round 30 — 2026-10-25 — synthetic` | `h2=1 h2_or_h3=1` | **0** |
| C | + `## 2026-10-25 — round 30: synthetic` | `h2=1 h2_or_h3=1` | **0** |
| C2 | + `### Round-30 backfill (appended)` | `h2=0 h2_or_h3=1` | **0** (h3 tolerance) |
| D | MUTANT: entry heading deleted | `h2=0 h2_or_h3=0` | **1** |
| E | round-30 only mentioned inside a `## Round 31 — … round-30 …` heading | `h2=0 h2_or_h3=0` | **1** |
| F | an existing `### Round-28 close-out correction (appended)` | `h2=0 h2_or_h3=0` | **1** |

Post-append mutant controls, verbatim:

```
$ head -n 1468 LOG.md > "$D/log-mutant.md"          # round-30 entry (lines 1469-EOF) deleted
file=/tmp/tmp.0aEpmtrKLt/log-mutant.md round30_h2_headings=0 round30_h2_or_h3_headings=0
log_closure=open
exit=1
$ git show HEAD:LOG.md > "$D/log-pre.md"            # independent reproduction: committed pre-entry bytes
file=/tmp/tmp.0aEpmtrKLt/log-pre.md round30_h2_headings=0 round30_h2_or_h3_headings=0
log_closure=open
exit=1
```

## 3. Coordination performed (by exact id)

- `agent://ScribeErratum`: sent the closure contract (anchor shapes, required literal `strict pass=43/43`),
  the `:813`/`:814` pointer correction, and the rejected shape G; then confirmed their numbers agree with
  the independent re-run and told them the in-flight audit state is not a regression of their erratum.
- `agent://ScribeQuality-4` (and `agent://ScribeQuality`): sent the exact CHECK A/B commands, the red
  output + exit, the A–G matrix, and then the verbatim green-after block + mutant results, for their R16
  row. Explicitly stated: this seat makes no `QUALITY.md` edit.
- Waited per bound 9: `until [ -s ScribeErratum.md ] && [ -s ScribeLogR30.md ]; do sleep 20; done` →
  satisfied after 4 iterations (80 s); both receipts present (11240 B / 14486 B). No blocker.

## 4. Findings beyond the two gates (measured, routed — not claimed as closed)

1. **Third stale premise in the same family** (reported by ScribeQuality, verified here, one number
   corrected): `corpus/QUALITY.md:77` (record R13, specimen sentence) cites
   `recheck-audit.py --selftest` → `selftest cases=4 failures=0 exit=0`. Live bytes print **18**
   `selftest …` case lines, all `ok`, `grep -c FAIL` → 0, exit 0, and **no** `cases=N failures=M`
   summary line at all (`grep -nE 'cases=|failures='` over the output → no match). So `cases=4` is not
   reproducible on landed bytes, and the peer's "six cases" is wrong — it is 18. `QUALITY.md` is
   ScribeQuality's file; a same-shape closure check would be `q=$(grep -c 'cases=4' corpus/QUALITY.md)`
   with closure requiring an r31 `Errata` anchor naming `cases=4`. **Not gated by this seat.**
2. **In-flight corpus state during the after run** (bound 6 / M30-3): `recheck-audit.py` mid-edit by
   ExecRALimbs, `source-recheck.py` mid-edit by ExecSRLimbs, new entry
   `corpus/knowledge/vendor-third-party-finding-coordination.md` (ExecEntryF15) and
   `knowledge-expected.txt` at 45 lines. A run at that instant prints
   `strict pass=44/44 … expect=present expected=43 missing=0 unexpected=1 exit=1` with
   `unexpected=corpus/knowledge/vendor-third-party-finding-coordination.md`.
   **IN-FLIGHT / NON-COMPARATIVE** — never compared to the `43/43` the erratum cites, which was measured
   at 23:33:27Z on quiescent pre-C1 bytes (digest `3fc0d751…`, reproduced by this seat and by
   ScribeErratum). The canonical after for C1 belongs to the C1 seats at quiescent post-land bytes.

## 5. Risks and limits (stated, not hidden)

- **R-1 (bounded, disclosed).** CHECK A closes on *any* r31 `Errata/Erratum` anchor followed by both
  facts; a future r31 erratum that quotes both phrases for an unrelated reason would keep the check green
  without re-addressing `:813-819`. Mitigation shipped: the anchor must be an `Errata/Erratum` line (case
  G fails), and the check prints `stale_paragraphs`, `erratum_anchor` and the citation bit, so a reader
  sees *which* anchor carried it. The mutant control (D) shows the green is not vacuous.
- **R-2 (disclosed).** CHECK B counts an h3 sub-section whose first token is 30 as satisfying the entry.
  Chosen deliberately (see §2); both `h2` and `h2_or_h3` counts are printed so the reading is auditable
  and the strict h2 reading is always available.
- **R-3.** Both checks are file-shape checks, not semantic ones: they prove an appended statement naming
  the paragraph and citing the corrected audit output exists, not that the erratum's prose is true. The
  erratum's own `43/43` figure was independently reproduced here at the pre-C1 digest.
- No blockers. No lane git/jj mutation, no write outside the lane, no campaign-package access, no live
  bounty contact, no credential material touched.

## 6. Result

| M31-1 part | Red-before | Green-after | Mutant control |
|---|---|---|---|
| 1 — `SCORECARD.md` stale `recheck-audit open item … exit=1` paragraph | open, **exit 1** | closed, **exit 0** (anchor `:837`, citation `strict pass=43/43`) | erratum deleted in scratch copy → **exit 1** |
| 2 — missing round-30 `LOG.md` entry | open, **exit 1** (`round30_*=0`) | closed, **exit 0** (`h2=1`, `h2/h3=2`) | entry deleted in scratch copy → **exit 1**; committed pre-entry bytes → **exit 1** |

Both halves of M31-1 are closed on the landed bytes, with the flip proven in both directions on the same
check bytes and with the subject files' digests unchanged across every run.
