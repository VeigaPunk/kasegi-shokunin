# ExecGateReviewPrep — round-37 final-gates receipt contract + base gate transcript

Seat `ExecGateReviewPrep` (executor, leaf — no dispatch, no swarm; one read-only labrat probe not used).
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `b56a41680cefd391868c1c370dc063c69d827e7d`;
claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`; lane HEAD at every measurement below
`b362068195d5489aa94b31e6ec8f880c367e0ba0` (claims freeze + wave evidence + claims-erratum-1).
Round 37, wave `kasegi-r37-build`, hyaku run 9. Model (host-reported): `opencode-go/deepseek-v4.1-flash`;
no model argument was passed by this seat.

**Report.** Two deliverables, both receipt-only (no lane file was created, edited or deleted):

1. **The `all-gates v1` format contract** for `.ufo/waves/round-37/final-gates/all-gates.txt` (§2) — a
   line-anchored grammar, four binding rules, the assembly procedure, and the exact checks E10 must
   enforce. It is delivered as a *reference implementation* (§3, 130 lines, `shellcheck` clean) plus an
   assembler, both exercised in both directions: **nine fixtures, eight refused and one accepted**
   (§3.3), and a cross-run shape limb that rejects a receipt whose payload shape does not match the
   live pass (§3.4).
2. **The pre-round gate transcript at base** (§4, 203 lines): seven gates run against base bytes —
   `r36-closure.sh --selftest` and `--export-ref`, `recheck-audit --quiet`, `capture-binding-check`,
   `frontier-recheck-count`, `source-recheck S053`, `sources-census validate`, `score-gap` — plus one
   export-root control. Base is **8/9 closed**; the only open check is E9, which is live by
   construction.

**The one finding the L1 must read before writing `all-gates.txt`:** a receipt that *contains* a
`closed=14/14 exit=0` run block cannot be produced by a run made at the ref that contains it — the
file is absent at every ref where the run is honest, so E10 is open there and the recorded block would
read 13/14. There is no fully self-consistent fixed point (proved in §2.6). The workable construction
is a **two-commit bootstrap with a disclosed single-check edit**, and the receipt must say so. Every
other point of the contract is satisfiable without disclosure.

---

## 1. Deliverables

| # | artifact | where it lands | lines | sha256 |
|---|---|---|---|---|
| A1 | format contract (this §2) | this receipt | — | — |
| A2 | reference verifier `r37-all-gates-verify.sh` | this receipt §3.1 (paste into `corpus/instruments/` if the L1 wants it as a gate) | 130 | `04c0ece2efa7bb5ab038c2a9f835346514e0f9a8e5dcadf4076c8de385f8537b` |
| A3 | assembler `mk-all-gates.sh` | this receipt §3.2 (scratch-only; refuses `--out` inside the lane) | 86 | `ff7441133f8eb995a38665422c37ad1b09711890d22487c49ca42eaff42397c8` |
| B1 | base gate transcript | this receipt §4 | 203 | `0cd91732d19938a7f86bd970879a3e66760fd70c5f801dbac50f175cc71e685f` |
| B2 | transcript runner (how §4 was produced) | this receipt §4.1 | 82 | `99c8157e343af1df044ea981a3a679883d050a9a60c04e144b912161dcc80620` |

Embedded copies are verbatim. The scratch tree that produced them is removed at yield (§7), so the
receipt is the only surviving copy; every number below states the artifact it was read from.

---

## 2. The `all-gates v1` format contract (normative)

### 2.1 Subject

Exactly one file: `.ufo/waves/round-37/final-gates/all-gates.txt`, **tracked** at the ref it is read
from (export mode reads tracked bytes only). Measured: the path is committable — `git check-ignore -v`
on it exits 1 (not ignored) and round 36's sibling file is tracked at base
(`git ls-tree -r --name-only b56a416 -- .ufo/waves/round-36/final-gates/` → one line). Encoding UTF-8,
LF endings, single trailing newline, no trailing spaces.

### 2.2 Grammar

Line kinds, in the exact order they must appear. "Once" = exactly one such line in the whole file.

```
   line 1        all-gates v1                                  (literal)
   header        export-ref=<40 lowercase hex>                  (once)
   header        suite-sha256=<64 lowercase hex>                (once)
   header        run-utc=<YYYY-MM-DDTHH:MM:SSZ>                 (once, strict UTC, date -u +%FT%TZ)
   header        # <free comment>                               (zero or more, must start "# ")
   header        <blank>                                        (zero or more)
   section       == run ==                                      (once, first section)
                 <r37-closure.sh --export-ref <ref> stdout, verbatim, in file order>
                 fourteen lines  E<n> payload=<k=v,...> closed=1
                 exactly one      closed=14/14 exit=0
   section       == selftest ==                                 (once, second section)
                 <r37-closure.sh --selftest stdout, verbatim, in file order>
                 fourteen lines  selftest case=E<n> ... mutants=<o>/<n> ... verdict=pass
                 exactly one      selftest cases=14 failures=0
   section       == other gates ==                              (optional, last)
                 <any> whose lines do not begin with a reserved token (2.4)
```

`<n>` is `1..14` with no zero padding. Payload fields are comma-separated `key=value` with no spaces.
The header block is *everything before the first line matching `^== `*; the recorded blocks are the
suite's own stdout, byte-verbatim — the assembler must not re-wrap, re-order or annotate them.

### 2.3 Binding rules

| rule | statement | why it is checkable |
|---|---|---|
| **R1 export-ref** | the 40-hex value resolves (`cat-file -e <v>^{commit}`) **and is an ancestor-or-equal of the ref the file is being read at** | equality is impossible (2.6); ancestry is what makes a receipt written one commit before its verification legitimate |
| **R2 suite digest** | `suite-sha256` equals `sha256sum` of `corpus/instruments/r37-closure.sh` **as exported at the ref being read** | binds the receipt to the suite bytes that produced it; if the suite is edited after the receipt, the digest breaks and E10 fails closed |
| **R3 honest counters** | the file carries exactly 14 `E<n> payload=` lines (ids E1..E14 once each, all `closed=1`), one `closed=14/14 exit=0`, 14 `selftest case=` lines (ids once each, `positive=pass`, `mutants=<o>/<n>` with `n>=1` and `o==n`, and exactly `n` matching `selftest detail=E<n> mutant=...rejected=1` lines), one `selftest cases=14 failures=0` | bare counts are satisfiable by a duplicate + omission; id-set and per-case mutant counts are not (fixture FD, FE — §3.3) |
| **R4 no placeholders** | zero matches of `<hash>`, `<sha>`, `<digest>`, `<ref>`, `<payload>`, `<N>`, `<n>`, `<id>`, `TODO`, `TBD` | the file is a record, never a template (fixture FF) |

### 2.4 Reserved line-start tokens (non-collision rule)

Inside `== other gates ==`, no line may begin with `E<digits> payload=`, `selftest case=`,
`closed=`, `selftest cases=`, `export-ref=` or `suite-sha256=`. The counters in R3 are file-wide; a
second section that repeats one of these tokens silently doubles a count. Free-form gate transcript may
be appended safely as long as its lines start with something else (`$ `, `[`, a tool name, `== ` …).

### 2.5 What E10 must check (limbs, in this order)

1. `E10.1` the file exists at the export root and `ls-tree -r --name-only <ref> -- <path>` is 1 line.
2. `E10.2` header present with exactly one `^export-ref=`, one `^suite-sha256=`, one `^run-utc=`.
3. `E10.3` R1 (resolve + ancestor-or-equal).
4. `E10.4` R2 (digest equality against the **exported** suite bytes).
5. `E10.5` R3 run block (id set, all closed=1, one `closed=14/14 exit=0`).
6. `E10.6` R3 selftest block (id set, positive=pass, mutants `o==n>=1`, detail lines, one summary).
7. `E10.7` **cross-run shape binding** — for each id, the payload *key set* on the recorded line
   equals the key set on the line E10's own pass just produced for that id. Values may differ (E9's
   limbs are live); the shape may not. This is E10 evaluated **last**, with the accumulated lines
   passed to it (in the r36 suite's structure: `run_check` order plus one global holding the lines so
   far). Without this limb a hand-written green block passes: measured, fixture FB accepts a
   one-token E9 edit (§3.3).
8. `E10.8` R4 (no placeholders).

E10's own payload is exempt from 7 (self-referential). Suggested fields, each independently
re-derivable: `export-ref=…,ancestor=1,digest-match=1,run-lines=14,selftest-cases=14,recorded-closed=1,crossrun=ok`.

### 2.6 The self-reference limitation (and the only workable construction)

Let M be the ref whose export contains the file and whose run is recorded in it. R3 requires the
recorded block to say `closed=14/14`. Every one of the 14 checks must have been green **in that run** —
including E10, which asks whether the export at M carries an `all-gates.txt` with a green block. So the
run recorded in the file must have been made at a ref that already contained a green file. Induction
gives no base case: the first green file would have to be recorded from a run at a ref that contained
it, i.e. the file would have to name a commit whose hash depends on its own content. Fifteen
generations of this lane's receipts (r24-r36) never hit the problem because no earlier receipt
contained its own gate counter; round 37 is the first round where the closure suite reads its own
receipt.

**Construction that works, with one disclosed edit:**

1. `F0` = all round-37 artifacts except `all-gates.txt`; worktree clean; `HEAD = F0`;
   `SCORECARD.md`'s round-37 section already carries a `Final lane commit:` line naming an **ancestor**
   of `F0` (E1's binding rule, r36 E1 limb unchanged).
2. Run `bash corpus/instruments/r37-closure.sh --export-ref F0` → expect **13/14**, with E10 the only
   `closed=0` (the file does not exist yet). Run `--selftest --export-ref F0` → expect
   `cases=14 failures=1`, the failure being E10's positive limb for the same reason.
3. Apply **exactly four token edits** to the recorded text and nothing else: E10's `closed=0`→`closed=1`;
   `closed=13/14 exit=1`→`closed=14/14 exit=0`; `selftest case=E10 …positive=fail…verdict=fail`→
   `…positive=pass…verdict=pass`; `selftest cases=14 failures=1`→`selftest cases=14 failures=0`.
   Assemble with §3.2 and record the edit in the header comment:
   `# bootstrap: E10 line records this file's own presence at F0+1 (see round-37 lesson M37-x)`.
4. Commit `F1 = F0 + all-gates.txt` (nothing else). Run the suite at `F1` —
   `--export-ref F1` — this is the claim's live counter and it must print `closed=14/14 exit=0`;
   E10 now closes **for real**, and limb 7 re-derives the other thirteen lines' shapes from the live
   pass, which is what makes the thirteen recorded payloads more than prose. E9's `head-match` reads 1
   at both M and F1 (M's run had `HEAD==F0`; F1's run has `HEAD==F1`), so the recorded E9 line stays
   shape-true.
5. If `F1` is not 14/14, the bootstrap was wrong: fix the tree, repeat at `F2`, and record the
   iteration in the round-37 lesson. Do not edit the receipt's payloads to match a red run.

**Why the edit is the minimum:** thirteen of the fourteen recorded lines are re-derived exactly at F1
by limb 7 (E1-E8, E11-E14 have tree-static payload key sets; E9's values are live by design). The
bootstrapped token is exactly the one check whose subject is the file itself, one commit before the file
exists — and it becomes true at F1. Any other edit (dropping a check, re-labelling an id, inventing a
payload) is detectable by limbs 5-7 and must be treated as a forged receipt.

### 2.7 Documented limits (measured or proved, not hidden)

- E10 verifies the receipt's **shape, digest, ancestry and cross-run shape**; it cannot verify that the
  recorded values were green at `export-ref` (2.6). Truth of the numbers is the live run at the checked
  ref; the digest rule is what keeps that live run the *same instrument*.
- Limb 7 compares key sets, not values: a receipt whose E9 values are stale relative to the live pass
  (different scratch root, different dirt) still passes. That is deliberate — E9's limbs are live and
  must differ between a measurement ref and the final head.
- R2 compares against the exported suite bytes, so a suite edited after the receipt goes red. It does
  **not** notice a suite that was already edited at `export-ref` before the run — the payload shapes
  catch that only if the edit changed a payload's keys.
- R4's token list is literal. A placeholder spelled differently (`TBA`, `??`, `0` as a stand-in) is not
  matched; the same residue the r36 suite records for E1's two literal spellings.

---

## 3. Reference implementation, assembler, and both-direction fixtures

### 3.1 `r37-all-gates-verify.sh` (verbatim; `bash -n` exit 0, `shellcheck -s bash` exit 0)

```bash
#!/usr/bin/env bash
# r37-all-gates-verify.sh — reference implementation of the r37 all-gates format
# contract (the shape E10 must enforce). READ-ONLY: no file is created.
#
#   bash r37-all-gates-verify.sh --file PATH --repo DIR --head REV
#        [--suite PATH] [--checks N] [--live FILE]
#
# Checks, in order (first failure wins, one reason token per run):
#   header.present      first line is exactly `all-gates v1`
#   header.export-ref   exactly one ^export-ref=<40 hex> in the header block
#   header.suite-sha    exactly one ^suite-sha256=<64 hex> in the header block
#   header.run-utc      exactly one ^run-utc=<YYYY-MM-DDTHH:MM:SSZ>
#   header.shape        no other non-comment, non-blank header line
#   ref.resolvable      git cat-file -e <export-ref>^{commit}
#   ref.ancestor        export-ref is an ancestor of (or equal to) --head
#   digest.match        suite-sha256 == sha256 of --suite bytes
#   run.lines           exactly N `^E<n> payload=... closed=1` lines, ids E1..EN once each
#   run.summary         exactly one `^closed=N/N exit=0`
#   selftest.lines      exactly N `^selftest case=E<n> ... verdict=pass` lines, ids once each
#   selftest.mutants    every case's mutants=<o>/<n> has n>=1, o==n, and exactly n
#                       `^selftest detail=E<n> mutant=...rejected=1` lines exist
#   selftest.summary    exactly one `^selftest cases=N failures=0`
#   crossrun.fields     (only with --live FILE) for every id, the payload key set
#                       on the recorded line equals the key set on the live run's line
#                       for that id -- values may differ (E9's limbs are live), the
#                       SHAPE may not, so a hand-written green summary is rejected
#   placeholder.absent  no `<hash>`/`<sha>`/`<digest>`/`<ref>`/`<payload>`/`<N>`/`<n>`,
#                       no TODO/TBD
# Exit 0 PASS, 1 FAIL, 2 usage/IO error.
set -uo pipefail

FILE='' REPO='' HEAD='' SUITE='' N=14 LIVE=''
while [ $# -gt 0 ]; do
  case $1 in
    --file) FILE=$2; shift 2 ;;
    --repo) REPO=$2; shift 2 ;;
    --head) HEAD=$2; shift 2 ;;
    --suite) SUITE=$2; shift 2 ;;
    --live) LIVE=$2; shift 2 ;;
    --checks) N=$2; shift 2 ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) printf 'verify: unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
done
[ -n "$FILE" ] && [ -n "$REPO" ] && [ -n "$HEAD" ] || { printf 'verify: --file --repo --head are required\n' >&2; exit 2; }
[ -f "$FILE" ] || { printf 'verify: no such file: %s\n' "$FILE" >&2; exit 2; }
[ -n "$SUITE" ] || SUITE=$REPO/corpus/instruments/r37-closure.sh
[ -f "$SUITE" ] || { printf 'verify: no such suite: %s\n' "$SUITE" >&2; exit 2; }

fail() { printf 'FAIL reason=%s\n' "$1"; exit 1; }

# --- header block: everything before the first `^== ` section marker ----------
hdr=$(awk '/^== /{exit} {print}' "$FILE")
n_hdr=$(printf '%s\n' "$hdr" | grep -c '^all-gates v1$')
[ "$n_hdr" -eq 1 ] && [ "$(printf '%s\n' "$hdr" | head -n1)" = 'all-gates v1' ] || fail header.present

EXP=$(printf '%s\n' "$hdr" | grep -cE '^export-ref=[0-9a-f]{40}$')
[ "$EXP" -eq 1 ] || fail header.export-ref
XREF=$(printf '%s\n' "$hdr" | sed -n 's/^export-ref=//p')

SH=$(printf '%s\n' "$hdr" | grep -cE '^suite-sha256=[0-9a-f]{64}$')
[ "$SH" -eq 1 ] || fail header.suite-sha
XSHA=$(printf '%s\n' "$hdr" | sed -n 's/^suite-sha256=//p')

UT=$(printf '%s\n' "$hdr" | grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')
[ "$UT" -eq 1 ] || fail header.run-utc

BAD=$(printf '%s\n' "$hdr" | grep -vE '^(all-gates v1|export-ref=[0-9a-f]{40}|suite-sha256=[0-9a-f]{64}|run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z|#.*|)$' | grep -c .)
[ "$BAD" -eq 0 ] || fail header.shape

# --- ref binding -------------------------------------------------------------
git -C "$REPO" cat-file -e "${XREF}^{commit}" 2>/dev/null || fail ref.resolvable
git -C "$REPO" merge-base --is-ancestor "$XREF" "$HEAD" 2>/dev/null || fail ref.ancestor

# --- digest binding ----------------------------------------------------------
ASHA=$(sha256sum -- "$SUITE" | awk '{print $1}')
[ "$ASHA" = "$XSHA" ] || fail "digest.match got=$ASHA want=$XSHA"

# --- recorded run block ------------------------------------------------------
run_ids=$(grep -E '^E[0-9]+ payload=.* closed=1$' "$FILE" | sed -n 's/^\(E[0-9][0-9]*\) payload=.*/\1/p')
run_n=$(printf '%s\n' "$run_ids" | grep -c .)
[ "$run_n" -eq "$N" ] || fail "run.lines count=$run_n want=$N"
seq_ids=$(for i in $(seq 1 "$N"); do printf 'E%s\n' "$i"; done)
[ "$(printf '%s\n' "$run_ids" | sort -u)" = "$seq_ids" ] || fail run.ids
bad_closed=$(grep -cE '^E[0-9]+ payload=.* closed=0$' "$FILE"); bad_closed=${bad_closed:-0}
[ "$bad_closed" -eq 0 ] || fail run.open
SUMS=$(grep -cE "^closed=${N}/${N} exit=0\$" "$FILE")
[ "$SUMS" -eq 1 ] || fail run.summary

# --- recorded selftest block -------------------------------------------------
st_ids=$(grep -E '^selftest case=E[0-9]+ ' "$FILE" | sed -n 's/^selftest case=\(E[0-9][0-9]*\) .*/\1/p')
st_n=$(printf '%s\n' "$st_ids" | grep -c .)
[ "$st_n" -eq "$N" ] || fail "selftest.lines count=$st_n want=$N"
[ "$(printf '%s\n' "$st_ids" | sort -u)" = "$seq_ids" ] || fail selftest.ids
bad_verdict=$(grep -cE '^selftest case=E[0-9]+ .*verdict=pass$' "$FILE"); bad_verdict=${bad_verdict:-0}
[ "$bad_verdict" -eq "$N" ] || fail selftest.verdict
# internal consistency: a case that says the positive limb FAILED cannot be a
# passing case (the suite prints positive=pass on every green case).
pos_bad=$(grep -E '^selftest case=E[0-9]+ ' "$FILE" | grep -vc 'positive=pass'); pos_bad=${pos_bad:-0}
[ "$pos_bad" -eq 0 ] || fail selftest.positive
for id in $seq_ids; do
  line=$(grep -m1 "^selftest case=${id} " "$FILE")
  o=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/[0-9][0-9]*.*/\1/p')
  m=$(printf '%s' "$line" | sed -n 's/.*mutants=[0-9][0-9]*\/\([0-9][0-9]*\).*/\1/p')
  [ -n "$o" ] && [ -n "$m" ] && [ "$m" -ge 1 ] && [ "$o" -eq "$m" ] || fail "selftest.mutants id=${id} mutants=${o}/${m}"
  det=$(grep -c "^selftest detail=${id} mutant=.*rejected=1" "$FILE"); det=${det:-0}
  [ "$det" -eq "$m" ] || fail "selftest.detail id=${id} lines=${det} want=${m}"
done
STS=$(grep -cE "^selftest cases=${N} failures=0\$" "$FILE")
[ "$STS" -eq 1 ] || fail selftest.summary

# --- cross-run shape binding (--live): values may drift, field names may not --
if [ -n "$LIVE" ]; then
  [ -f "$LIVE" ] || fail crossrun.missing
  names() { # FILE ID
    sed -n "s/^$2 payload=\(.*\) closed=[01]$/\1/p" "$1" | head -n1 \
      | tr ',' '\n' | sed -n 's/^\([A-Za-z0-9_.-]*\)=.*/\1/p' | sort -u
  }
  for id in $seq_ids; do
    [ "$(names "$FILE" "$id")" = "$(names "$LIVE" "$id")" ] \
      || fail "crossrun.fields id=${id} recorded=$(names "$FILE" "$id" | tr '\n' ' ')"
  done
fi

# --- placeholder discipline --------------------------------------------------
PH=$(grep -cE '<(hash|sha|digest|ref|payload|N|n|id)>|TODO|TBD' "$FILE"); PH=${PH:-0}
[ "$PH" -eq 0 ] || fail placeholder.absent

printf 'PASS file=%s export-ref=%s suite-sha256=%s checks=%s\n' "$FILE" "$XREF" "$XSHA" "$N"
exit 0
```

### 3.2 `mk-all-gates.sh` (verbatim; `bash -n` exit 0, `shellcheck -s bash` exit 0)

```bash
#!/usr/bin/env bash
# mk-all-gates.sh — assemble .ufo/waves/round-37/final-gates/all-gates.txt from
# the two suite outputs, then VERIFY it with r37-all-gates-verify.sh before it
# is written. A red run is refused: no partial file, no green line invented.
#
#   bash mk-all-gates.sh --ref <40 hex> --run-out FILE --selftest-out FILE
#        --suite PATH --repo DIR [--head REV] [--out PATH] [--checks N]
#
# --ref is the head the two suite runs were made against (git rev-parse --verify
# <hash>^{commit}). --suite is the suite file those runs executed; its sha256 is
# the header digest. --out defaults to stdout; a --out that resolves inside the
# lane is refused (exit 2) so this tool can never write the lane.
# Exit: 0 emitted+verified · 1 refused (run not green, or verification failed)
#       · 2 usage/environment.
set -uo pipefail
HERE=$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P )
RUN='' ST='' SUITE='' REPO='' HEAD='' REF='' OUT='' N=''
while [ $# -gt 0 ]; do
  case $1 in
    --ref) REF=$2; shift 2 ;;
    --run-out) RUN=$2; shift 2 ;;
    --selftest-out) ST=$2; shift 2 ;;
    --suite) SUITE=$2; shift 2 ;;
    --repo) REPO=$2; shift 2 ;;
    --head) HEAD=$2; shift 2 ;;
    --out) OUT=$2; shift 2 ;;
    --checks) N=$2; shift 2 ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    *) printf 'mk-all-gates: unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
done
[ -n "$REF" ] && [ -n "$RUN" ] && [ -n "$ST" ] && [ -n "$SUITE" ] && [ -n "$REPO" ] \
  || { printf 'mk-all-gates: --ref --run-out --selftest-out --suite --repo are required\n' >&2; exit 2; }
[ -f "$RUN" ] && [ -f "$ST" ] && [ -f "$SUITE" ] \
  || { printf 'mk-all-gates: a required input file is missing\n' >&2; exit 2; }
XR=$(git -C "$REPO" rev-parse --verify --quiet "${REF}^{commit}") \
  || { printf 'mk-all-gates: cannot resolve --ref in %s: %s\n' "$REPO" "$REF" >&2; exit 2; }
[ -n "$HEAD" ] || HEAD=$XR
SHA=$(sha256sum -- "$SUITE" | awk '{print $1}')

if [ -n "$OUT" ]; then
  o=$(realpath -m -- "$OUT") || { printf 'mk-all-gates: bad --out\n' >&2; exit 2; }
  lane=$( cd "$REPO" && pwd -P )
  case $o in "$lane"|"$lane"/*) printf 'mk-all-gates: refusing --out inside the lane: %s\n' "$o" >&2; exit 2 ;; esac
fi

# --- the run must be green and self-consistent -------------------------------
sum=$(grep -E '^closed=[0-9]+/[0-9]+ exit=[01]$' "$RUN" | tail -n1)
[ -n "$sum" ] || { printf 'mk-all-gates: run output has no closed=K/N line\n' >&2; exit 1; }
k=${sum#closed=}; k=${k%%/*}; m=${sum#*/}; m=${m%% *}; ex=${sum##*exit=}
[ -z "$N" ] && N=$m
[ "$m" = "$N" ] || { printf 'mk-all-gates: run denominator %s != --checks %s\n' "$m" "$N" >&2; exit 1; }
[ "$k" = "$N" ] && [ "$ex" = 0 ] \
  || { printf 'mk-all-gates: refusing a red run: %s\n' "$sum" >&2; exit 1; }
g=$(grep -cE '^E[0-9]+ payload=.* closed=1$' "$RUN"); g=${g:-0}
[ "$g" -eq "$N" ] || { printf 'mk-all-gates: run has %s green E lines, want %s\n' "$g" "$N" >&2; exit 1; }
grep -qE "^selftest cases=${N} failures=0\$" "$ST" \
  || { printf 'mk-all-gates: selftest output is not cases=%s failures=0\n' "$N" >&2; exit 1; }

# --- assemble -----------------------------------------------------------------
tmp=$(mktemp -d -t mk-all-gates.XXXXXXXX) || exit 2
trap 'rm -rf -- "$tmp"' EXIT
f=$tmp/all-gates.txt
{
  printf 'all-gates v1\n'
  printf 'export-ref=%s\n' "$XR"
  printf 'suite-sha256=%s\n' "$SHA"
  printf 'run-utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '# suite: bash corpus/instruments/%s (the two blocks below are its stdout, verbatim)\n' "$(basename -- "$SUITE")"
  printf '# assembler: mk-all-gates.sh; verifier: r37-all-gates-verify.sh --checks %s\n' "$N"
  printf '\n'
  printf '== run ==\n'
  cat -- "$RUN"
  printf '\n== selftest ==\n'
  cat -- "$ST"
} > "$f"

# --- verify before write ------------------------------------------------------
if ! bash "$HERE/r37-all-gates-verify.sh" --file "$f" --repo "$REPO" --head "$HEAD" \
     --suite "$SUITE" --checks "$N" > "$tmp/verify.txt" 2>&1; then
  printf 'mk-all-gates: REFUSED by verifier: %s\n' "$(head -n1 "$tmp/verify.txt")" >&2
  exit 1
fi
cat -- "$tmp/verify.txt" >&2
if [ -n "$OUT" ]; then cp -- "$f" "$OUT"; printf 'wrote %s\n' "$OUT" >&2; else cat -- "$f"; fi
exit 0
```

### 3.3 Fixture matrix — the verifier in both directions

Fixtures are derived mechanically from **real** output: `FA` is the base run block exactly as printed
(§4, G2: eight green, E9 open); `FB` is `FA` with exactly three tokens flipped (E9 `closed=0`→`1`,
`closed=8/9 exit=1`→`9/9 exit=0`, selftest E9 `positive=fail…verdict=fail`→`positive=pass…verdict=pass`,
`cases=9 failures=1`→`0`) so the format's green path is exercised although no ref is green today. Each
fixture carries a header comment naming it as a parser fixture, never lane evidence. `--head` is base
for all rows; the suite subject is the base export's `r36-closure.sh`
(`sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`), `--checks 9` because the
r37 suite does not exist yet.

| fixture | single deviation | verifier result |
|---|---|---|
| `FA` real base run (8/9) | none — the real bytes | **FAIL** `run.lines count=8 want=9` |
| `FB` green | three disclosed tokens | **PASS** |
| `FC` | `suite-sha256` zeroed | **FAIL** `digest.match got=4db1ae70… want=000…0` |
| `FD` | E9 line replaced by a second E8 | **FAIL** `run.ids` |
| `FE` | E3 `mutants=5/5`→`0/0` | **FAIL** `selftest.mutants id=E3 mutants=0/0` |
| `FF` | `# export-ref=<hash> to be filled` | **FAIL** `placeholder.absent` |
| `FG` | `export-ref` = `000…0` | **FAIL** `ref.resolvable` |
| `FH` | `export-ref` = `b362068…` (a descendant of `--head` base) | **FAIL** `ref.ancestor` |
| `FI` | E9 case `positive=fail` with `verdict=pass` | **FAIL** `selftest.positive` |
| `FB` re-read with `--head b362068…` | base is an ancestor of HEAD | **PASS** — R1's ancestor-or-equal rule, measured |

Two further controls: `--checks 14` on the 9-check file → **FAIL** `run.lines count=9 want=14`; and the
assembler's own refusals — red run *with* its summary line → `refusing a red run: closed=8/9 exit=1`
(exit 1); `--checks 14` against a 9-denominator run → `run denominator 9 != --checks 14` (exit 1);
`--out` inside the lane → exit 2 with the resolved path; green run → emitted file re-verified PASS.

### 3.4 Cross-run shape limb, measured

- receipt = live = `FB` → **PASS**.
- receipt `FJ` = `FB` with `,bound=2` dropped from E1 → **FAIL**
  `crossrun.fields id=E1 recorded=lane-hash-markers placeholders round36-final-lane-commits round36-section`.
  Without limb 7 the same file passes every other limb — which is exactly why a structure-only E10 is
  not enough.

---

## 4. Base gate transcript (pre-round state, verbatim)

Runner: §4.1. Window `2026-10-26T17:07:50Z` → `17:08:03Z`. Base binding: the lane worktree's
gate-read paths equal base bytes — `git -C lane diff --name-only b56a416… -- corpus SCORECARD.md SKILL.md
LOG.md considerthese plans AGENTS.md README.md PROVINCE.md SHONEN.md` → **0 paths**, and lane `HEAD` was
`b362068…` (claims artifacts only). Tree fingerprint (sha256 over the sorted `sha256  path` list of
`corpus/ SCORECARD.md SKILL.md LOG.md considerthese/ plans/`) **before = after =
`e4d80abde84c0705895a6a157f94bb8c2fa221f3f8902986f2c1c53927cffd56`**: no sibling write landed inside
the window. (A sibling modified `.ufo/waves/round-36/wave1/ScribeConsiderthese.md` *after* the window;
`.ufo/` is not read by any gate here — E4/E6 read `.ufo` through `ls-tree`/`ls-files` at the ref.)

Readings at base, in one table:

| gate | command | base reading | exit |
|---|---|---|---|
| G1 closure selftest | `r36-closure.sh --selftest --export-ref b56a416… --scratch-root /fast/scratch/hyaku/kasegi-r37` | `cases=9 failures=1`; E1-E8 `positive=pass`, E9 `positive=fail` (`status-dirty=6,scratch-seat-dirs=22,head-match=0,lane-root=1`); own-report `accepted=0`; four forged reports rejected | 1 |
| G2 closure run | `r36-closure.sh --export-ref b56a416…` | `closed=8/9 exit=1`; E1-E8 `closed=1`, E9 `closed=0` | 1 |
| G3 recheck audit | `recheck-audit.py --root <lane> --quiet` | `strict pass=48/48`, `lines=48 total=48 pass=48 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`, `expect=present expected=48 missing=0 unexpected=0 exit=0` | 0 |
| G4 capture binding | `capture-binding-check.py --root <lane>` | `records=43 bound=43 unbound=0`, `snapshot_dirs=12 manifest_dirs=12 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt` | 0 |
| G5 frontier harness | `frontier-recheck-count.py --root <lane>` | `entries=22 pass=22 exit=0`, F01..F19 (F19=`epss… ids=S053`) | 0 |
| G6 source recheck | `source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` | `S053:sha256 OK`, Q1 `216-ok`, Q2 `217-ok`, Q3 `217-ok`, Q4 `235-ok` | 0 |
| G7 census (conf form) | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | only `W04 S028`, `W04 S029`, then `ok` — byte-identical to `.ufo/waves/round-37/census-before.txt` | 0 |
| G7b census (export form) | `sources-census.sh validate <base-export>` | same three rows, lane label `kasegi-shokunin` (dir basename) instead of `kasegi` | 0 |
| G8 score gap | `score-gap.py --root <lane>` | `recheck: lines=48 executes=24 gated=24 broken=0`; `anchorcheck: in-range=16 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0`; `census-lane: 134/1480 = 9.05%`, `census-skill: 32/506 = 6.32%`; `threshold: SCORECARD.md:331`; `gap: 24 of 48 rechecks still gated on a lost base` | 0 |
| B1 control | `recheck-audit.py --root <base-export> --quiet` | `strict pass=1/48 cdroot_fail=47`, `lines=48 total=48 pass=48 … exit=1` | 1 |

### 4.1 Runner (verbatim)

```bash
#!/usr/bin/env bash
# run-base-gates.sh — READ-ONLY base-state gate transcript for kasegi-shokunin
# round 37, seat ExecGateReviewPrep. Writes only under the scratch root.
set -uo pipefail

S=/fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
BASE=b56a41680cefd391868c1c370dc063c69d827e7d
EXP=$S/baseroot/kasegi-shokunin
OUT=$S/base-gates.txt
SCRATCH_R37=/fast/scratch/hyaku/kasegi-r37
GATE_PATHS='corpus SCORECARD.md SKILL.md LOG.md considerthese plans AGENTS.md README.md PROVINCE.md SHONEN.md'

fingerprint() {
  ( cd "$LANE" && find corpus SCORECARD.md SKILL.md LOG.md considerthese plans -type f -print0 \
      | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}' )
}

run() { # LABEL CMD...
  local label=$1; shift
  printf '== %s ==\n' "$label"
  printf '$ %s\n' "$*"
  local t0 rc
  t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  "$@"
  rc=$?
  printf '[exit=%s] [at=%s]\n\n' "$rc" "$t0"
}

exec > "$OUT" 2>&1

printf '# base gate transcript — kasegi-shokunin round 37 (PRE-ROUND state)\n'
printf '# seat=ExecGateReviewPrep (leaf) generated_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf '# lane=%s\n' "$LANE"
printf '# base=%s\n' "$BASE"
printf '# lane-head=%s\n' "$(git -C "$LANE" rev-parse HEAD)"
printf '# base-export=%s\n' "$EXP"
printf '# base-binding: git -C lane diff --name-only %s -- %s\n' "$BASE" "$GATE_PATHS"
printf '#   -> %s changed path(s)\n' "$(git -C "$LANE" diff --name-only "$BASE" -- $GATE_PATHS | wc -l)"
printf '# tree-fingerprint.before=%s\n' "$(fingerprint)"
printf '# fingerprint = sha256 over the sorted "<sha256>  <path>" lines of corpus/ SCORECARD.md SKILL.md LOG.md considerthese/ plans/ (the paths these gates read)\n\n'

printf '== census-before.txt (dispatcher artifact, quoted) ==\n'
cat "$LANE/.ufo/waves/round-37/census-before.txt" 2>/dev/null || printf '(absent)\n'
printf '\n'

run 'G1 r36-closure.sh --selftest (base export-ref)' \
  bash "$LANE/corpus/instruments/r36-closure.sh" --selftest \
    --export-ref "$BASE" --work "$S/w-g1" --scratch-root "$SCRATCH_R37"

run 'G2 r36-closure.sh --export-ref (base, plain run)' \
  bash "$LANE/corpus/instruments/r36-closure.sh" --export-ref "$BASE" \
    --work "$S/w-g2" --scratch-root "$SCRATCH_R37"

run 'G3 recheck-audit.py --quiet --root LANE' \
  bash -c "cd '$LANE' && python3 corpus/instruments/recheck-audit.py --root '$LANE' --quiet"

run 'G4 capture-binding-check.py --root LANE' \
  bash -c "cd '$LANE' && python3 corpus/instruments/capture-binding-check.py --root '$LANE'"

run 'G5 frontier-recheck-count.py --root LANE' \
  bash -c "cd '$LANE' && python3 corpus/instruments/frontier-recheck-count.py --root '$LANE'"

run 'G6 source-recheck.py --manifest round-36/manifest.json --source S053' \
  bash -c "cd '$LANE' && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053"

run 'G7 sources-census.sh validate --root FLEET kasegi (live lane)' \
  bash "$FLEET/scripts/sources-census.sh" validate --root "$FLEET" kasegi

run 'G7b sources-census.sh validate BASE-EXPORT DIR' \
  bash "$FLEET/scripts/sources-census.sh" validate "$EXP"

run 'G8 score-gap.py --root LANE' \
  bash -c "cd '$LANE' && python3 corpus/instruments/score-gap.py --root '$LANE'"

printf '== B1 (export-root variant) recheck-audit.py --quiet --root BASE-EXPORT ==\n'
printf '$ cd %s && python3 corpus/instruments/recheck-audit.py --root %s --quiet\n' "$EXP" "$EXP"
( cd "$EXP" && python3 corpus/instruments/recheck-audit.py --root "$EXP" --quiet )
printf '[exit=%s]\n\n' "$?"

printf '# tree-fingerprint.after=%s\n' "$(fingerprint)"
```

### 4.2 Transcript (verbatim, 203 lines)

```
# base gate transcript — kasegi-shokunin round 37 (PRE-ROUND state)
# seat=ExecGateReviewPrep (leaf) generated_utc=2026-10-26T17:07:50Z
# lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin
# base=b56a41680cefd391868c1c370dc063c69d827e7d
# lane-head=b362068195d5489aa94b31e6ec8f880c367e0ba0
# base-export=/fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/baseroot/kasegi-shokunin
# base-binding: git -C lane diff --name-only b56a41680cefd391868c1c370dc063c69d827e7d -- corpus SCORECARD.md SKILL.md LOG.md considerthese plans AGENTS.md README.md PROVINCE.md SHONEN.md
#   -> 0 changed path(s)
# tree-fingerprint.before=e4d80abde84c0705895a6a157f94bb8c2fa221f3f8902986f2c1c53927cffd56
# fingerprint = sha256 over the sorted "<sha256>  <path>" lines of corpus/ SCORECARD.md SKILL.md LOG.md considerthese/ plans/ (the paths these gates read)

== census-before.txt (dispatcher artifact, quoted) ==
Census before (round-37, measured 2026-10-26T16:31Z):

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
$ echo $?
0

== G1 r36-closure.sh --selftest (base export-ref) ==
$ bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh --selftest --export-ref b56a41680cefd391868c1c370dc063c69d827e7d --work /fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/w-g1 --scratch-root /fast/scratch/hyaku/kasegi-r37
selftest export-ref=b56a41680cefd391868c1c370dc063c69d827e7d lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --scratch-root
selftest detail=E1 positive=pass payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=2,bound=2
selftest detail=E1 mutant=placeholder rejected=1 limb=placeholders=1
selftest detail=E1 mutant=lane-hash-marker rejected=1 limb=lane-hash-markers=1
selftest detail=E1 mutant=unbound-hash rejected=1 limb=bound=0
selftest detail=E1 mutant=history-only rejected=1 limb=round36-section=0
selftest case=E1 positive=pass mutants=4/4 verdict=pass
selftest detail=E2 positive=pass payload=erratum-marker=1,erratum-row=1,erratum-mean=7
selftest detail=E2 mutant=stale-mean rejected=1 limb=erratum-mean=0
selftest detail=E2 mutant=prose-not-row rejected=1 limb=erratum-row=0
selftest detail=E2 mutant=marker-without-row rejected=1 limb=erratum-row=0
selftest case=E2 positive=pass mutants=3/3 verdict=pass
selftest detail=E3 positive=pass payload=registry-r35-defect-closure=1,registry-r36-closure=1
selftest detail=E3 mutant=r36-row-absent rejected=1 limb=registry-r36-closure=0
selftest detail=E3 mutant=r35-row-absent rejected=1 limb=registry-r35-defect-closure=0
selftest detail=E3 mutant=inexact-basename rejected=1 limb=registry-r35-defect-closure=0
selftest detail=E3 mutant=mention-not-row rejected=1 limb=registry-r36-closure=0
selftest detail=E3 mutant=rows-outside-registry rejected=1 limb=registry-r36-closure=0
selftest case=E3 positive=pass mutants=5/5 verdict=pass
selftest detail=E4 positive=pass payload=tracked-ref=1,tracked-index=1,provenance-note=1
selftest detail=E4 mutant=provenance-absent rejected=1 limb=provenance-note=0
selftest case=E4 positive=pass mutants=1/1 verdict=pass
selftest detail=E5 positive=pass payload=claims-erratum-d5=1
selftest detail=E5 mutant=erratum-absent rejected=1 limb=claims-erratum-d5=0
selftest case=E5 positive=pass mutants=1/1 verdict=pass
selftest detail=E6 positive=pass payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1
selftest detail=E6 mutant=correction-absent rejected=1 limb=correction-round35=0
selftest case=E6 positive=pass mutants=1/1 verdict=pass
selftest detail=E7 positive=pass payload=supersedes-r22=1,supersedes-r23=1
selftest detail=E7 mutant=r23-row-absent rejected=1 limb=supersedes-r23=0
selftest detail=E7 mutant=prose-not-row rejected=1 limb=supersedes-r22=0
selftest case=E7 positive=pass mutants=2/2 verdict=pass
selftest detail=E8 positive=pass payload=m36-rows=4,names-corrected-line=3,stale-line=0,round35-lesson=1
selftest detail=E8 mutant=m36-absent rejected=1 limb=m36-rows=0
selftest detail=E8 mutant=stale-line-present rejected=1 limb=stale-line=1
selftest detail=E8 mutant=corrected-line-unnamed rejected=1 limb=names-corrected-line=0
selftest detail=E8 mutant=round35-lesson-absent rejected=1 limb=round35-lesson=0
selftest case=E8 positive=pass mutants=4/4 verdict=pass
selftest detail=E9 positive=fail rc=1 payload=status-dirty=6,scratch-seat-dirs=22,head-match=0,lane-root=1,scratch-root=present
selftest detail=E9 mutant=dirty-worktree rejected=1 limb=status-dirty=1
selftest detail=E9 mutant=leftover-seat-dir rejected=1 limb=scratch-seat-dirs=1
selftest detail=E9 mutant=stale-ref rejected=1 limb=head-match=0
selftest detail=E9 mutant=enclosing-repo rejected=1 limb=lane-root=0
selftest case=E9 positive=fail mutants=4/4 verdict=fail
selftest cases=9 failures=1
selftest judge=own-report accepted=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
[exit=1] [at=2026-10-26T17:07:50Z]

== G2 r36-closure.sh --export-ref (base, plain run) ==
$ bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh --export-ref b56a41680cefd391868c1c370dc063c69d827e7d --work /fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/w-g2 --scratch-root /fast/scratch/hyaku/kasegi-r37
export-ref=b56a41680cefd391868c1c370dc063c69d827e7d mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --scratch-root
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=2,bound=2 closed=1
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=7 closed=1
E3 payload=registry-r35-defect-closure=1,registry-r36-closure=1 closed=1
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=1 closed=1
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=4,names-corrected-line=3,stale-line=0,round35-lesson=1 closed=1
E9 payload=status-dirty=6,scratch-seat-dirs=22,head-match=0,lane-root=1,scratch-root=present closed=0
closed=8/9 exit=1
[exit=1] [at=2026-10-26T17:07:51Z]

== G3 recheck-audit.py --quiet --root LANE ==
$ bash -c cd '/home/vgpnk/Projects/shokunin/kasegi-shokunin' && python3 corpus/instruments/recheck-audit.py --root '/home/vgpnk/Projects/shokunin/kasegi-shokunin' --quiet
strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=24 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=48 total=48 pass=48 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=48 missing=0 unexpected=0 exit=0
[exit=0] [at=2026-10-26T17:07:52Z]

== G4 capture-binding-check.py --root LANE ==
$ bash -c cd '/home/vgpnk/Projects/shokunin/kasegi-shokunin' && python3 corpus/instruments/capture-binding-check.py --root '/home/vgpnk/Projects/shokunin/kasegi-shokunin'
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=43 with_url=43 with_fetched_utc=5 with_archival=38 snapshot_dirs=12 manifest_dirs=12 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=43 bound=43 unbound=0
[exit=0] [at=2026-10-26T17:07:59Z]

== G5 frontier-recheck-count.py --root LANE ==
$ bash -c cd '/home/vgpnk/Projects/shokunin/kasegi-shokunin' && python3 corpus/instruments/frontier-recheck-count.py --root '/home/vgpnk/Projects/shokunin/kasegi-shokunin'
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0   
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0   
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0   
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0   
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0   
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0   
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0   
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0   
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0   
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0   
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0   
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0   
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0   
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0   
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0   
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0   
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0   
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0   
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0   
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0   
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0   
entries=22 pass=22 exit=0
[exit=0] [at=2026-10-26T17:07:59Z]

== G6 source-recheck.py --manifest round-36/manifest.json --source S053 ==
$ bash -c cd '/home/vgpnk/Projects/shokunin/kasegi-shokunin' && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053
S053:sha256 OK
S053:Q1 OK occurrences=1 anchor=216-ok
S053:Q2 OK occurrences=1 anchor=217-ok
S053:Q3 OK occurrences=1 anchor=217-ok
S053:Q4 OK occurrences=1 anchor=235-ok
[exit=0] [at=2026-10-26T17:08:02Z]

== G7 sources-census.sh validate --root FLEET kasegi (live lane) ==
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
[exit=0] [at=2026-10-26T17:08:02Z]

== G7b sources-census.sh validate BASE-EXPORT DIR ==
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/baseroot/kasegi-shokunin
kasegi-shokunin	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-shokunin	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-shokunin	ok	/fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/baseroot/kasegi-shokunin/corpus/SOURCES.md
[exit=0] [at=2026-10-26T17:08:02Z]

== G8 score-gap.py --root LANE ==
$ bash -c cd '/home/vgpnk/Projects/shokunin/kasegi-shokunin' && python3 corpus/instruments/score-gap.py --root '/home/vgpnk/Projects/shokunin/kasegi-shokunin'
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source: SKILL.md sha256=2ddb1bc72872a54a87f2b3655d6612c4b5bae86ea154a612aa42cfc5fcc1fd8f
source: corpus/instruments/citation-survival.md sha256=795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d
source: SCORECARD.md sha256=1e2788c6a7f577f17dd5ce46ec69e6debe7b883caea374b46f240e1754d84e6e
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=48 executes=24 gated=24 broken=0 exit=0
[2] anchors
cmd: python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
anchorcheck: in-range=16 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
cmd: grep -nE '^Numerator = |^- lane total \(SKILL\.md \+ corpus\): |^- SKILL\.md alone: ' corpus/instruments/citation-survival.md
census-definition: Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 48 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
[exit=0] [at=2026-10-26T17:08:03Z]

== B1 (export-root variant) recheck-audit.py --quiet --root BASE-EXPORT ==
$ cd /fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/baseroot/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --root /fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/baseroot/kasegi-shokunin --quiet
strict pass=1/48 cdroot_fail=47 instrument_fail=0 own_fail=0
executes=24 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=48 total=48 pass=48 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=48 missing=0 unexpected=0 exit=1
[exit=1]

# tree-fingerprint.after=e4d80abde84c0705895a6a157f94bb8c2fa221f3f8902986f2c1c53927cffd56
```

---

## 5. Findings

**F1 — base is 8/9, and E9 is the only red.** Base closure reads `closed=8/9 exit=1` (§4 G2). E9's
limbs are live by construction (worktree status, scratch root, `HEAD`), so a *historical* ref can only
read "not quiescent now"; the base run's `status-dirty=6` are the untracked `.ufo/waves/round-37/*`
dispatch artifacts, `scratch-seat-dirs=22` are live sibling seats, and `head-match=0` because `HEAD`
is `b362068` ≠ base. Consequence for the final gate: the claim's `closed=14/14` must be measured at a
**clean** final head with `--export-ref <that same head>` and after the last seat directory is gone;
otherwise E9 stays red for reasons that are not about the round's work. This is also why round 36's
committed `all-gates.txt` carries no positive `9/9` block — only `closed=0/9` (neg base) and
`closed=3/9` (neg judged) (`cat .ufo/waves/round-36/final-gates/all-gates.txt`).

**F2 — never run `recheck-audit.py --root <export>`.** With the audited root pointed at a `git archive`
export, the strict limbs collapse: `strict pass=1/48 cdroot_fail=47`, exit 1 (§4 B1), because the
`cdroot` limb compares each recheck line's absolute `cd <lane>` path against the audited root. The three
frozen limbs are unaffected (`pass=48`), so a careless reader sees the same `pass=48` under `exit=1`.
Base-bound readings are `--root <lane>` plus the `git diff <base> -- <gate-read paths>` = 0 proof (§4).
The same trap does **not** apply to `capture-binding-check`, `frontier-recheck-count`,
`source-recheck`, `score-gap` or `census`, which read bytes and gave identical substantive counts on the
export root.

**F3 — census lane label is the argument form.** `validate --root <fleet> kasegi` prints `kasegi`
(fleet id); `validate <dir>` prints the directory basename (`kasegi-shokunin`). Counts and W-codes are
identical (§4 G7/G7b). The final gate should use the conf form so the label matches the fleet id and the
`census-before.txt` artifact it is compared against.

**F4 — the `all-gates.txt` path is committable and E10 is reachable.** `.gitignore` carries only
`.ufo/interactive-sessions/` and `__pycache__/`; `git check-ignore -v` on the round-37 path exits 1, and
round 36's sibling is tracked at base. No `.gitignore` change is needed.

**F5 — the r37 suite's default `SCRATCH_ROOT` must be `/fast/scratch/hyaku/kasegi-r37`.** `r36-closure.sh`
hardcodes `SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r36` (`grep -n '^SCRATCH_ROOT='`), while C1's E9
names the r37 root. If the r37 suite inherits the r36 default, E9's seat-dir limb reads a *different*
directory than the claim names and can pass vacuously (0 dirs) or mis-read `scratch-root=absent`. A
`--scratch-root` override at final-gate time is visible in the suite's own `deviation=non-default
--scratch-root` line, so the default is the honest choice.

**F6 — the suite's own work dir is excluded from E9.** Measured by sourcing `r36-closure.sh` and calling
`check_e9` on a probe scratch root holding one fake seat dir plus the work dir: `scratch-seat-dirs=1`
with `WORK` set, `2` without (`head-match=1,lane-root=1`). So `TMPDIR` under the r37 scratch root cannot
self-count, and the final run needs no special `--work`.

**F7 — the receipt cannot be green at the ref it is recorded from (§2.6),** and the frozen shape is only
reachable via the disclosed four-token bootstrap. If the C1 suite instead implements R1 as *equality*
(`export-ref == checked ref`), the claim becomes unsatisfiable; if it implements E10 without limb 7, a
one-token edit passes (§3.3/§3.4). These are the two implementation choices the format contract pins.

**F8 — the transcript's numbers are the round's starting line, not a target.** Every base reading here
is pre-round: closure 8/9, `frontier=19`, `registry=53`, knowledge 48 entries, harness 22/22,
`S053` bound, census clean with two standing W04 warnings, `gap 24 of 48`. Round 37's C2 must move
`frontier 19→20`, `registry 53→54`, knowledge `48→49`, harness `22→23` and add the S054 capture; the
final `all-gates.txt` should append the post-integration readings under `== other gates ==` (safe by
§2.4) so the delta is readable in one file.

---

## 6. Evidence provenance

| claim | artifact read | instant |
|---|---|---|
| lane HEAD, base ancestry, gate-read diff 0 | `git rev-parse`, `git merge-base --is-ancestor`, `git diff --name-only b56a416… -- <paths>` | 17:07:50Z |
| G1/G2 closure readings | `r36-closure.sh` stdout, `--work` under scratch | 17:07:50Z-51Z |
| G3-G8 readings | instrument stdout (§4.2) | 17:07:52Z-17:08:03Z |
| tree stability | fingerprint before/after §4 header | 17:07:50Z / 17:08:03Z |
| export-root control B1 | `recheck-audit.py --root <base-export>` | 17:08:03Z |
| E9 work-dir exclusion | `check_e9` called directly on a probe tree | 17:10Z |
| fixture matrix | `fix/*.txt` built from §4.2 G2/G1 blocks | 17:12Z-17:15Z |
| suite digest | `sha256sum` of lane and base-export `r36-closure.sh` (equal) | 17:13Z |

`[INFERENCE]` markers: the E9 consequence in F1 (what the final-gate conditions must be) is a reading of
the E9 limbs, not a measured final run; R1's unsatisfiability proof in §2.6 is an argument, with its
consequence measured on fixtures (FB/FI). Everything else is a command output quoted in this receipt.

## 7. Writes, tooling, mutation, scratch

- **Writes:** this receipt only. Scratch under `/fast/scratch/hyaku/kasegi-r37/ExecGateReviewPrep/`
  (base export ×2, work dirs `w-g1`/`w-g2`, fixture tree `fix/`, the two tools, the transcript, the
  probe tree), removed at yield. No lane file was created, edited or deleted; the fleet root and
  `/home/vgpnk/Projects/shokuknow` were not written and no campaign tool was run.
- **Tooling:** nothing installed or upgraded; `pacman` not invoked (host-wide pause respected); no
  `uv tool install`, no `npx`, no binary drop. Used as present: `bash`, `awk`, `sed`, `grep`, `find`,
  `sha256sum`, `realpath`, `git` (read-only verbs only), `python3` 3.14.x, `shellcheck`.
- **Mutation:** no mutating git/jj command. The only `git init` executed happened inside the r36 suite's
  own `$MUT/e9repo` fixture, which the suite verifies has `toplevel == realpath` before using it, and
  inside scratch. Read-only verbs used: `rev-parse`, `log`, `ls-tree`, `ls-files`, `cat-file`,
  `merge-base --is-ancestor`, `status`, `diff`, `archive`, `check-ignore`.
- **Peers:** none messaged; `agent://all` not used. No subagent dispatch.
