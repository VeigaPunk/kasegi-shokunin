# ScribeErratum — round 31, wave 1 (M31-1 part 1: SCORECARD stale-premise erratum)

Seat: ScribeErratum (scribe). Round: kasegi-shokunin round 31, wave 1.
Lane repo (only write scope): `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane base: `b374febbb33ccadade78a787279707fd5d2e6e1d`. Claims-freeze commit: `738a77999a00efbca129cfccb28a481037f6241f`.
HEAD at measurement and at write: `8a8916c7043bd873d191b30dd1744b241b91f4d9` ("round-31: wave-1 spec, validated dispatch (38 seats)").
Answering model: `devin/deepseek-v4-1-flash` (config route table decision; no model passed by this seat).
Tools installed/upgraded: none. No pacman transaction. No git/jj mutation. No delegation, no background jobs of my own.

## Owned path and scope

Single writer of `SCORECARD.md`, append-only (R6/R9). Only `SCORECARD.md` was written by this seat; the filed round-30 paragraph was not touched.
`LOG.md` (ScribeLogR30), `corpus/QUALITY.md` (ScribeQuality), `corpus/lessons/`, `SHONEN.md`, the report and `claims.json` are not this seat's paths and were not written.

## Precondition — red-before receipt

Read: `.ufo/waves/round-31/wave1/ExecErratumCheck-before.txt` (seat ExecErratumCheck, present on disk).

```text
stale_paragraphs=1 errata_naming_item=0 erratum_cites_corrected_audit=0
erratum_closure=open
EXIT CODE: 1
```

Same receipt pins the pre-edit digests this seat re-measured before editing:

```text
$ sha256sum SCORECARD.md LOG.md corpus/instruments/recheck-audit.py
cac64dbdb8cd9ed834a6deca44c5b4fd5874f1e95d2f1118f919c3ccb84811b9  SCORECARD.md
0a1865e90f29c5d4a20fa3fda8f9daf6b6293bbec95710bafcda0cf65d537221  LOG.md
3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1  corpus/instruments/recheck-audit.py
```

My own pre-edit measurement (2026-10-25T23:33:27Z) matched all three digests, and `git status --porcelain -- SCORECARD.md corpus/instruments/` was clean, so the subject bytes were quiescent (M30-3 satisfied) when measured.

## Measurements (commands and their output, cwd = lane root unless stated)

### 1. Audit at lane-root base bytes (the value of record)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && date -u +%Y-%m-%dT%H:%M:%SZ && \
sha256sum SCORECARD.md corpus/instruments/recheck-audit.py corpus/instruments/knowledge-expected.txt && \
python3 corpus/instruments/recheck-audit.py --quiet; echo "live_audit_exit=$?"
```

```text
2026-10-25T23:33:27Z
cac64dbdb8cd9ed834a6deca44c5b4fd5874f1e95d2f1118f919c3ccb84811b9  SCORECARD.md
3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1  corpus/instruments/recheck-audit.py
98282841943baaf75cabd2f7fef6ac67f2c23aee4a62750093ebbab4e5c854f6  corpus/instruments/knowledge-expected.txt
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=19 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=43 missing=0 unexpected=0 exit=0
live_audit_exit=0
```

`strict pass=43/43 … exit=0` is the base value the erratum quotes.

### 2. Copy-relative control (why a git export is not a base measurement)

```sh
git archive b374febbb33ccadade78a787279707fd5d2e6e1d > /tmp/scribe-erratum-base.tar
tar -xf /tmp/scribe-erratum-base.tar -C .ufo/waves/round-31/wave1/ScribeErratum-scratch/base
cd .ufo/waves/round-31/wave1/ScribeErratum-scratch/base && sha256sum corpus/instruments/recheck-audit.py && \
python3 corpus/instruments/recheck-audit.py --quiet; echo "base_audit_exit=$?"
```

```text
2026-10-25T23:33:27Z
3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1  corpus/instruments/recheck-audit.py
strict pass=1/43 cdroot_fail=42 instrument_fail=0 own_fail=0
executes=19 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=43 missing=0 unexpected=0 exit=1
base_audit_exit=1
```

Cause, from the instrument itself: strict limb (d) requires the `cd <path> &&` target to equal the audited root.

```sh
grep -n "cdroot" corpus/instruments/recheck-audit.py | head -3
27:  (d) cdroot     if the command begins `cd <path> &&`, <path> is the audited root.
137:    strict["cdroot"] = True if cd_target is None else os.path.abspath(cd_target) == (cdroot or root)
```

42 entry rechecks `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`; an export at another path therefore fails limb (d) for them. This is recorded as a measurement limit in the erratum, not as a defect claim and not as a base value.

### 3. Ledger recheck form and digest (supersession evidence)

```sh
grep -n "recheck:" corpus/knowledge/considerthese-proposals-ledger.md
5:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/density.py corpus/knowledge/considerthese-proposals-ledger.md --label proposal-ledger
sha256sum corpus/knowledge/considerthese-proposals-ledger.md
d91889e5f7d77c3695c366521c348569b4f29269632e0bfc927105600a6c250d  corpus/knowledge/considerthese-proposals-ledger.md
```

This agrees with the corrected-ledger digest recorded in `corpus/lessons/round-30.md` § Close-out erratum.

### 4. Capabilities clause check (whether the round-30 stagnation sentence is false)

```sh
grep -in "capabilit" SCORECARD.md | sed -n '1,40p'
grep -n "| First-working round |" SCORECARD.md
grep -n "^## Round-2[0-9] capabilit" SCORECARD.md
```

```text
301:## Capabilities
307:The `sources-registry` capability entered in round 22; ...
416:**Capability entry.** `mirror-containment-matrix` — ... First working round: 23. This restarts the r22 stagnation window.
511:## Round-24 capabilities
553:## Round-25 capabilities
580:## Round-26 capabilities
820:**Capabilities: no row added this round.** Per the round-30 assignment no new
824:`frontier-recheck-harness` capabilities. The Capabilities table is unchanged; the
825:stagnation window continues (last capability entry round 25).

```

```sh
grep -nE '^\| (sources-registry|frontier-recheck-harness|source-capture|recheck-audit|source-capture-round-25|source-capture-pdf) ' SCORECARD.md | awk -F'|' '{r=$(NF-1); gsub(/^[ \t]+|[ \t]+$/,"",r); print $1 "| first-working round " r}'
```

```text
305:| first-working round 22
515:| first-working round 24
516:| first-working round 24
557:| first-working round 25
558:| first-working round 25
584:| first-working round 26
```

```sh
grep -n "^## Round-2[0-9] capabilit" SCORECARD.md
```

```text
511:## Round-24 capabilities
553:## Round-25 capabilities
580:## Round-26 capabilities
```

Verdict: the round-30 headline "no row added this round" is TRUE for round 30; the parenthetical "(last capability entry round 25)" is FALSE — round 26 added `source-capture-pdf` (`SCORECARD.md:580-584`, first-working round 26). Corrected in the appended erratum only; the filed sentence is byte-identical.

## Append performed

Appended at the end of `SCORECARD.md` (heading `### Round-31 erratum to the round-30 section`, body opening with the literal token `r31 erratum`). Content covers: the paragraph `recheck-audit open item (outside the frozen claims)` (cited as `SCORECARD.md:813-819`, which spans the sentence head at `:813` and the backticked `exit=1` reading at `:814`); the statement that the filed `exit=1` was true at composition time and is superseded by the final ledger-recheck correction (`density.py` over the ledger's own entry) with `strict pass=43/43 … exit=0`; pointers to `corpus/lessons/round-30.md` § Close-out erratum and `corpus/lessons/round-30-verifier-spotcheck.md` §5 item 4; the live re-run command and the 2026-10-25T23:33:27Z output; the copy-relative measurement limit; and the Capabilities clause correction.

```sh
git diff -U0 SCORECARD.md | grep -c '^-[^-]'
0
git diff --stat SCORECARD.md
 SCORECARD.md | 25 +++++++++++++++++++++++++
 1 file changed, 25 insertions(+)
git diff SCORECARD.md | sed -n '1,5p'
diff --git i/SCORECARD.md w/SCORECARD.md
index 77856a9..39e7373 100644
--- i/SCORECARD.md
+++ w/SCORECARD.md
@@ -833,3 +833,28 @@ depth:verifiability at 4 the lowest-axis obligation stays active.
sha256sum SCORECARD.md   # after append
5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7  SCORECARD.md
wc -l SCORECARD.md
860 SCORECARD.md          # 835 before append; erratum section = 24 lines
git status --porcelain -- SCORECARD.md
 M SCORECARD.md
```

Additions-only proof: `deletions=0`; 25 insertions, 0 deletions; no line of the filed round-30 text changed.

### Closure check (ExecErratumCheck's contract, run by this seat after the append)

```sh
ER='^.*(([Rr]31)|([Rr]ound[- ]31))[[:space:]]+[Ee]rratum.*recheck-audit open item'
n=$(grep -c 'recheck-audit open item' SCORECARD.md)
e=$(grep -cE "$ER" SCORECARD.md)
l=$(grep -nE "$ER" SCORECARD.md | head -1 | cut -d: -f1)
if [ -n "$l" ] && tail -n +"$l" SCORECARD.md | grep -q 'strict pass=43/43'; then c=1; else c=0; fi
printf 'stale_paragraphs=%s errata_naming_item=%s erratum_cites_corrected_audit=%s\n' "$n" "$e" "$c"
```

```text
stale_paragraphs=2 errata_naming_item=1 erratum_cites_corrected_audit=1
erratum_closure=closed
```

Match line (first hit), `SCORECARD.md:839`:

```text
r31 erratum: the paragraph `recheck-audit open item (outside the frozen claims)` filed at `SCORECARD.md:813-819` was true when it was co…
```

`stale_paragraphs=2` is expected: the filed paragraph at `:813` plus the erratum's naming line. Closure is `closed` because `errata_naming_item>=1` and `erratum_cites_corrected_audit=1`.

## Scratch cleanup

`.ufo/waves/round-31/wave1/ScribeErratum-scratch/` and `/tmp/scribe-erratum-base.tar` were created for the base-export control and removed (`rm -rf … && echo "scratch_removed=$?"` -> `scratch_removed=0`). Nothing outside the lane repo persists from this seat.

## Findings

1. **M31-1 part 1 closed in `SCORECARD.md`** — the stale round-30 `recheck-audit open item` paragraph now has an appended, dated erratum naming it; the filed text is preserved.
2. **Second stale premise found in the same sentence family, outside my write scope** — the round-30 Capabilities parenthetical "(last capability entry round 25)" is false (round 26 added `source-capture-pdf`). Corrected in my erratum; filed text untouched.
3. **`corpus/QUALITY.md:77` stale premise reported by ExecErratumCheck** (`recheck-audit.py --selftest` -> `selftest cases=4 failures=0 exit=0`; live instrument prints 18 `selftest …` ok lines and no `cases=N failures=M` summary). `corpus/QUALITY.md` is ScribeQuality's path, not mine; I did not read, verify or edit it. Routed to the L1 for ScribeQuality.
4. **Copy-relative audit runs are not base measurements** — the strict `cdroot` limb makes a `git archive` export at a foreign path print `strict pass=1/43 … exit=1`. Any later seat quoting an audit number from an export should expect this and say where it ran.

## Peer confirmation (ExecErratumCheck, received after the append)

Reported by ExecErratumCheck on the post-append quiescent bytes (`SCORECARD.md` sha256 `5fa41aef…` held identical before and after every run; 835 -> 860 lines):

```text
file=SCORECARD.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1
erratum_closure=closed / exit=0
```

Mutant control (erratum block 837-EOF removed into a scratch copy): `stale_paragraphs=1 erratum_anchor=none` -> open / exit 1. ExecErratumCheck states the green is carried by my bytes only and that `:813-819` remains byte-identical. Its receipt is `.ufo/waves/round-31/wave1/ExecErratumCheck-after.txt`.

In-flight observation relayed by ExecErratumCheck, recorded here as NON-COMPARATIVE (bound 6 / M30-3) and deliberately NOT written into `SCORECARD.md`: at the time of its message `recheck-audit.py` was mid-edit (ExecRALimbs) and ExecEntryF15's entry had landed, so a run at that instant printed `strict pass=44/44 … unexpected=1 exit=1` with `unexpected=corpus/knowledge/vendor-third-party-finding-coordination.md` (expected list 45 lines, `expected=43`). This is a PRE-STATE/in-flight reading, not a correction of the `43/43` measured at 2026-10-25T23:33:27Z on digest `3fc0d751…`; a post-C1 audit figure belongs to the C1 after-receipt on quiescent bytes. The erratum already states that any changed instrument bytes require a dated re-run.

ExecErratumCheck did not verify the Capabilities correction (round 26 `source-capture-pdf` vs "(last capability entry round 25)") — it is outside its two checks and it does not gate on it. My evidence for it is the verbatim enumeration in §4 above.

## Out of scope / not done

- The round-31 claims section was NOT appended to `SCORECARD.md` (arrives after wave 2, per assignment).
- `LOG.md` was not touched (ScribeLogR30 owns M31-1 part 2).
- No verification of `corpus/instruments/recheck-audit.py` limb work was attempted; that instrument was mid-edit (ExecRALimbs) by the time this receipt closed, so its current output is in-flight/non-comparative. The quoted audit value must be re-measured and dated once the C1 limb work lands (the erratum says so).
- No report, commit, push, publish or deploy by this seat; the L1 commits through the lane helper.
