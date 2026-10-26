# ScribeQuality — corpus/QUALITY.md round-31 additions (R16, R17)

Seat: ScribeQuality (leaf, no delegation). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, lane base
`b374febbb33ccadade78a787279707fd5d2e6e1d`, claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`.
Answering model actually run on: `devin/deepseek-v4-1-flash` (config route table; no model passed by this seat).
Tooling: nothing installed or upgraded — no pacman transaction, no uv/npx, no official-binary download; stdlib
`grep`/`awk`/`head`/`sha256sum`/`python3` only.
No git/jj mutation, no write outside this lane, no live bounty-target contact.

## 1. Deliverable — append-only edit to `corpus/QUALITY.md`

Two new rows under a new heading `## Round-31 additions — closure checks and one-limb mutants`:
**R16** (result paragraphs stating an open failure/exit code carry a `bash -n`-parseable closure check; closure is an
appended erratum naming the paragraph and citing the corrected output; the filed paragraph stays byte-identical) and
**R17** (a limb is load-bearing only when a committed exact-once `find`/`replace` mutant that still compiles moves the
limb's kill command, replayed by `limb-mutation-check.py` with the no-op / non-compiling / equivalent controls
rejected; an unmoved limb is a survivor and is never relabelled killed).

Before → after (measured here, `cwd` = lane root):

```text
$ wc -l corpus/QUALITY.md && sha256sum corpus/QUALITY.md
89 corpus/QUALITY.md
a39e0b5e2bf4631c07bd75f40209f2fc33a65c5844dca0191b51db9448ca13f9  corpus/QUALITY.md
$ # after the append
$ wc -l corpus/QUALITY.md && sha256sum corpus/QUALITY.md
96 corpus/QUALITY.md
96b71caad96979b42422bd7dfc362c94913d54ffc63d2cf2dc0aac62ef2e6b2d  corpus/QUALITY.md
$ git diff --numstat -- corpus/QUALITY.md
7	0	corpus/QUALITY.md
$ git show HEAD:corpus/QUALITY.md | head -89 | sha256sum ; head -89 corpus/QUALITY.md | sha256sum
a39e0b5e2bf4631c07bd75f40209f2fc33a65c5844dca0191b51db9448ca13f9  -
a39e0b5e2bf4631c07bd75f40209f2fc33a65c5844dca0191b51db9448ca13f9  -
```

7 insertions, 0 deletions; lines 1–89 byte-identical, so every existing `QUALITY.md:<n>` anchor (e.g. the
`QUALITY.md:77` R13 specimen, `:85` round-29 heading) keeps its number (R6).

## 2. R16 evidence — reproduced by this seat, and the cited artifact

The seat's own independent reproduction of ExecErratumCheck's canonical CHECK A (`/tmp/sq-checkA2.sh`, text equal
to the block in `ExecErratumCheck-after.txt`; `bash -n` parseable):

```text
$ bash -n /tmp/sq-checkA2.sh ; echo "bash_n_exit=$?"
bash_n_exit=0

$ git show b374febb…:SCORECARD.md > /tmp/sq-b3/SCORECARD.md ; sha256sum /tmp/sq-b3/SCORECARD.md
cac64dbdb8cd9ed834a6deca44c5b4fd5874f1e95d2f1118f919c3ccb84811b9  /tmp/sq-b3/SCORECARD.md
$ bash /tmp/sq-checkA2.sh /tmp/sq-b3/SCORECARD.md ; echo "red_exit=$?"
file=/tmp/sq-b3/SCORECARD.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=open
red_exit=1

$ bash /tmp/sq-checkA2.sh ; echo "green_exit=$?"     # live SCORECARD.md, sha256 5fa41aef… (860 lines)
file=SCORECARD.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1
erratum_closure=closed
green_exit=0

$ head -n 836 SCORECARD.md > /tmp/sq-m1.md ; bash /tmp/sq-checkA2.sh /tmp/sq-m1.md ; echo "mutant_exit=$?"
file=/tmp/sq-m1.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=open
mutant_exit=1
```

Cited verbatim from the owning seat's artifacts (`.ufo/waves/round-31/wave1/ExecErratumCheck-before.txt` lines
44–46, `ExecErratumCheck-after.txt` §CHECK A, `ExecErratumCheck.md` §1):

```text
file=SCORECARD.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=open
EXIT CODE: 1
```
```text
file=SCORECARD.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1
erratum_closure=closed
EXIT CODE: 0
```

Subject digests from that receipt: `SCORECARD.md` `cac64dbd…` (835 lines) → `5fa41aef…` (860 lines, append-only);
erratum anchor `SCORECARD.md:837` `### Round-31 erratum to the round-30 section`, naming line `:839`, corrected
output `strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0` in the block after it; stale paragraph
`:813–819` left byte-identical. That seat also reports quiescence (same `SCORECARD.md`/`LOG.md` digests before and
after every run) and the LOG half (`round30_h2_headings=1 round30_h2_or_h3_headings=2`, `log_closure=closed`,
exit 0).

**Limit measured here and written into the row:** the same check accepts a vanished paragraph. On the base bytes
with the phrase reworded once and no erratum appended:

```text
$ bash /tmp/sq-checkA2.sh /tmp/sq-b4/SCORECARD.md ; echo "reworded_exit=$?"
file=/tmp/sq-b4/SCORECARD.md stale_paragraphs=0 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=closed
reworded_exit=0
```

So the check's `stale_paragraphs=0` branch is a vacuous closure; R16 therefore names the naming-erratum branch as
the only closure and forbids rewording/deletion, and the row discloses this limit rather than hiding it.

## 3. R17 evidence

- Normative vehicle (frozen interface, cited as contract not as measurement): `corpus/instruments/limb-ledger.json`
  `{"version":1,"limbs":[…],"controls":[…]}` and `corpus/instruments/limb-mutation-check.py`; per-row verdicts
  `LIMB <id> live=<exit>/<sig> mutant=<exit>/<sig> verdict=killed|survivor|invalid:<reason>`, controls
  `CONTROL <id> verdict=<v> expected=<e> ok=y|n`, summaries `limbs=n killed=k survivors=s` / `controls=n rejected=r`.
- Survivor→strengthening specimen, quoted from the owning executor's fragment
  (`.ufo/waves/round-31/wave1/ledger-fragments/ra.json`, row `RA-completeness`, 20 words):
  “On the pre-round-31 bytes this was the one RA survivor (mutant compiled, find once, exit 0, stdout byte-identical
  to pristine)”. Confirmed live: those two `main()`-level fixtures exist and pass on the working bytes —
  `$ python3 corpus/instruments/recheck-audit.py --selftest` printed
  `selftest complete-empty        exit=1 want=1 lines=0/0 complete=False ok` and
  `selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok` (18 `selftest ` case lines, exit 0).
- Earlier failure the row grounds on: round-30 M30-1 (`corpus/lessons/round-30.md` § Mistakes) — the frozen B2
  fixture declared `id=S045` with `path=B2.txt`, so B1's stem limb exited first and B2's mutant flip was `NO`.
- **PRE-STATE / NON-COMPARATIVE counter reading** (bound 6; the canonical C1 after-column belongs to ExecCounter /
  ExecLedgerMerge on quiescent post-land bytes, not to this file). Run `2026-10-25T23:42:45Z` on in-flight bytes,
  `limb-mutation-check.py` sha256 `eb9b87ff…`, `limb-ledger.json` sha256 `c042adf6…`:

```text
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
… (13 LIMB lines total)
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

This is a PRE-STATE reading while `source-recheck.py`, `frontier-recheck-count.py` and `knowledge-expected.txt` were
still being edited; it is **not** compared to any after column and is **not** cited in the QUALITY rows.

## 4. Findings (routed, not fixed by this seat)

- **F1 — R13's specimen is unreproducible (existing row, append-only).** `QUALITY.md:77` (R13) cites
  `python3 corpus/instruments/recheck-audit.py --selftest` → `selftest cases=4 failures=0 exit=0`. No such summary
  string exists in the instrument: `grep -n "cases=\|failures=" corpus/instruments/recheck-audit.py` → no match at
  base `b374febb…`, at freeze `738a7799…`, or on the working bytes; the live selftest prints 18 `selftest …` case
  lines, `grep -cE 'cases=|failures='` → `0`, exit 0. Route: a superseding row (R8-style `supersedes R13 -`) —
  this seat's item scopes the append to R16/R17 and rewriting `:77` would break the append-only rule.
- **F2 — CHECK A's `stale_paragraphs=0` branch is a vacuous closure** (evidence in §2). Disclosed inside R16 as the
  row's limit; a tightening that pins the stale paragraph's own bytes is the natural fix and is left to the
  wave-2 owner of this file (`ScribeQualityFix`).
- **F3 — in-flight audit reading, non-comparative.** ExecErratumCheck's `ExecErratumCheck-after.txt` §IN-FLIGHT
  records `strict pass=44/44 … unexpected=1 exit=1` with
  `unexpected=corpus/knowledge/vendor-third-party-finding-coordination.md` while `recheck-audit.py` was mid-edit and
  `knowledge-expected.txt` was 45 lines; my own later `wc -l` saw 46. Not a regression and not comparable to the
  quiescent `43/43` the erratum cites; owner `ExecExpectedList` + `ExecEntryF15`.

## 5. Bounds, touched surfaces, artifacts

- Written by this seat: `corpus/QUALITY.md` (append-only, 7 lines) and this receipt. Nothing else. Scratch work lived
  in `/tmp` (`sq-checkA2.sh`, `sq-b3/`, `sq-b4/`, `sq-m1.md`, `sq-counter.txt`) and never in the lane tree.
- Read-only: `SCORECARD.md`, `LOG.md`, `corpus/lessons/round-30.md`, `corpus/lessons/round-30-verifier-spotcheck.md`,
  `considerthese/2026-10-25.md`, `corpus/instruments/*`, `.ufo/waves/round-31/claims.json`, `wave1-spec.json`,
  `wave1-dispatch.json`, `wave2-items.py`, and the wave-1 seat receipts.
- Known limits: the lesson `corpus/lessons/round-31.md` does not exist yet (the L1 writes it), so both rows cite it
  by section name as the item directs — R16 names `M31-1`, R17 cites § Mistakes generically; `corpus/QUALITY.md`
  remains uncommitted in the lane working tree (the L1 commits through the lane helper).
