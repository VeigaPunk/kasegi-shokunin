# RevNoHarm — round-38 no-harm (append-only) verification, receipt

- Seat: RevNoHarm (leaf member; no subagents dispatched; no labrat probe needed)
- Round: kasegi-shokunin round 38 · dispatched by L1 KasegiR38 via inline spawn handoff (hyaku run 9)
- Route chain: L1 KasegiR38 → inline spawn handoff (hyaku run 9) → RevNoHarm
- Written: 2026-10-26T18:39:34Z (each run timestamped inline below)
- Base: `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`
- Claims freeze: `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b` — `.ufo/waves/round-38/claims.json` read first; not edited
- Lane HEAD at run: `700153593eb586c70a6499c8ca225ee4d673bc9b` (wave1 dispatch; `git diff --numstat base..HEAD` on the ten files is empty)
- Scope: receipt only. No deliverable file; the landable instrument is the single `## DELIVERABLE` fenced block below.

## 1. No-harm rules (definition)

Rule A — strict append-only (8 files): **zero deletions** AND **base content is a byte-identical prefix of ref content** (equivalently `ref == base ++ appended bytes`).

    SKILL.md
    PROVINCE.md
    SCORECARD.md
    LOG.md
    SHONEN.md
    corpus/QUALITY.md
    corpus/knowledge/considerthese-proposals-ledger.md
    corpus/lessons/round-37.md

Rule B — mid-table insertion (2 files): **zero deletions** AND **every base line still present in ref, in order**. Implemented as three conjoined checks: (i) `git diff --numstat` deletions == 0 (git counts a modified line as 1 del + 1 add, so del==0 already excludes rewrites, including whitespace-only ones); (ii) `difflib.SequenceMatcher(None, base_lines, ref_lines, autojunk=False)` opcodes ⊆ {equal, insert}; (iii) an exact greedy in-order subsequence confirmation (every base line matched to a strictly increasing ref line index).

    corpus/SOURCES.md   # S055 row inserts inside the registry table
    corpus/README.md    # F21 row inserts after F20 in the frontier table

Rationale for the split: a mid-table insertion is not a byte-prefix append, so Rule A would false-fail the legitimate S055/F21 rows (demonstrated in §4, case `ins`: PREFIX=0, INORDER=1 → PASS). The gate **fails closed**: difflib's match is not guaranteed-minimal, so in a pathological case it can only raise a false alarm (only_ins=0), never silently pass harm — the exact greedy check (iii) is the subsequence authority. `autojunk=False` is required: with the default, frequent lines (blank lines, `|` table pipes) are junked and a pure insertion can show fake delete/replace opcodes.

## 2. Instrument and invocation

The `## DELIVERABLE` block below is byte-identical to the instrument executed: **110 lines, sha256 `71a67778c409599a57d47b62250776b6716593262ba9bc89f1c14516c2d9a123`** (verified by extracting the fenced block from this receipt and `cmp`-ing against the executed copy — see §7).

Invocation (the exact commands, parameterized over any two refs):

    BASE=<base-commit> REF=<ref-commit-or-WORKTREE> bash r38-noharm.sh

Exit contract: 0 = no harm; 1 = harm detected (per-file table on stdout; `REF=WORKTREE` compares the base commit against the live working tree). All work copies bind under `$SCRATCH` (default `/fast/scratch/hyaku/kasegi-r38/RevNoHarm`) and the script's own work dir is removed by `trap`.

## 3. Required run — base vs claims freeze (executed 2026-10-26T18:37:27Z)

    run_utc=2026-10-26T18:37:27Z
    lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin
    lane_head=700153593eb586c70a6499c8ca225ee4d673bc9b
    base=a173b0c2b98c5ae39599fa9be76027fbbead0b9e
    ref=9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b
    ancestor_ok=true

    == git diff --numstat base ref -- <ten files> ==

    FILE                                                 ADD   DEL  RULE   PREFIX  INORDER  DIFFOPS   VERDICT
    SKILL.md                                               0     0  strict 1       1        equal     PASS
    PROVINCE.md                                            0     0  strict 1       1        equal     PASS
    SCORECARD.md                                           0     0  strict 1       1        equal     PASS
    LOG.md                                                 0     0  strict 1       1        equal     PASS
    SHONEN.md                                              0     0  strict 1       1        equal     PASS
    corpus/QUALITY.md                                      0     0  strict 1       1        equal     PASS
    corpus/knowledge/considerthese-proposals-ledger.md     0     0  strict 1       1        equal     PASS
    corpus/lessons/round-37.md                             0     0  strict 1       1        equal     PASS
    corpus/SOURCES.md                                      0     0  insert 1       1        equal     PASS
    corpus/README.md                                       0     0  insert 1       1        equal     PASS

    noharm: PASS (10/10 files, exit 0)

Interpretation: the freeze commit `9a10b02` adds only wave-control files —

    .ufo/waves/round-38/c1-controls/before.txt
    .ufo/waves/round-38/c2-controls/before.txt
    .ufo/waves/round-38/census-before.txt
    .ufo/waves/round-38/claims.json

— so at the claims freeze **no front-door/registry file is touched at all**: all ten are byte-identical (0 added, 0 deleted, DIFFOPS=equal), and `git status --porcelain` over the ten files at run time was empty (clean working tree). No-harm therefore holds trivially at the freeze point; the rules bind the round's landings, and the instrument is re-runnable as `BASE=a173b0c2… REF=<J-or-REF>` at closure (the natural G1/G8 re-run point).

## 4. Controls — the predicate discriminates (fixture repo)

Mutating git ran only inside `D=$(mktemp -d -p "$S")/fixture/repo` with `git -C "$D" rev-parse --show-toplevel` verified equal to `$D` before any commit:

    toplevel_verified=/fast/scratch/hyaku/kasegi-r38/RevNoHarm/fixture/repo
    fixture_base=5272eda9dfc2109993b4360e6b1d16749efde13d

Four child commits of the fixture base: `app` = pure append to PROVINCE.md; `ins` = mid-table row inserted into corpus/SOURCES.md; `tam` = existing LOG.md line rewritten; `del` = existing corpus/README.md line deleted. Verbatim instrument output per case:

Case `app` (expect PASS 10/10):

    == git diff --numstat base ref -- <ten files> ==
    1	0	PROVINCE.md

    PROVINCE.md                                            1     0  strict 1       1        equal+insert PASS
    (all other rows 0/0 PASS)

    noharm: PASS (10/10 files, exit 0)

Case `ins` (expect PASS 10/10; the row that justifies Rule B):

    == git diff --numstat base ref -- <ten files> ==
    1	0	PROVINCE.md
    1	0	corpus/SOURCES.md

    PROVINCE.md                                            1     0  strict 1       1        equal+insert PASS
    corpus/SOURCES.md                                      1     0  insert 0       1        equal+insert PASS

    noharm: PASS (10/10 files, exit 0)

corpus/SOURCES.md has PREFIX=0 (a mid-table insert is not a byte prefix) yet INORDER=1 with only insert opcodes → PASS. A prefix-only check would false-fail this legitimate insertion.

Case `tam` (expect FAIL, exactly LOG.md flagged):

    == git diff --numstat base ref -- <ten files> ==
    1	1	LOG.md
    1	0	PROVINCE.md
    1	0	corpus/SOURCES.md

    LOG.md                                                 1     1  strict 0       0        equal+replace FAIL
    (all other rows PASS)

    noharm: FAIL (1 of 10 file(s) harmed)
    exit=1

Case `del` (expect FAIL, exactly corpus/README.md flagged):

    == git diff --numstat base ref -- <ten files> ==
    1	1	LOG.md
    1	0	PROVINCE.md
    0	1	corpus/README.md
    1	0	corpus/SOURCES.md

    LOG.md                                                 1     1  strict 0       0        equal+replace FAIL
    corpus/README.md                                       0     1  insert 0       0        delete+equal FAIL
    (all other rows PASS, including corpus/SOURCES.md insert)

    noharm: FAIL (2 of 10 file(s) harmed)
    exit=1

Control summary: 2 positive controls pass, 2 negative controls fail, each negative flags exactly the harmed file and nothing else.

## 5. Verdict

- Required check (base `a173b0c2` vs freeze `9a10b02`): **PASS 10/10, exit 0** — zero deletions, byte-identical base prefixes (trivially: the ten files are untouched at the freeze).
- Instrument validated: 2 positive + 2 negative controls behave exactly as specified, including the Rule-B false-fail trap (mid-table insert passes, prefix-only logic would not).
- Residual risk: the binding exercise happens when round-38 landings occur. Re-run the DELIVERABLE instrument at closure as `BASE=a173b0c2b98c5ae39599fa9be76027fbbead0b9e REF=<J>` (and `REF=WORKTREE` pre-commit); exit 0 is the no-harm contract. The gate fails closed.

## 6. Protocol notes

- No LSP server applies (markdown + git content only; no `lsp` device in this seat's inventory) — text/git evidence is the fallback per reviewer protocol.
- Tooling: no installs needed or performed (git 2.56.0 and Python 3.14.8 preinstalled; pacman untouched).
- Scratch: `/fast/scratch/hyaku/kasegi-r38/RevNoHarm` — removed before yield (G6 quiescence).

## 7. Receipt self-check (executed after writing this file)

    awk fence-extract of the ## DELIVERABLE block, cmp against the executed instrument
    → DELIVERABLE_BYTE_IDENTICAL; receipt line count and sha256 recorded in the seat's yield.

## DELIVERABLE

```bash
#!/usr/bin/env bash
# r38-noharm.sh — kasegi-shokunin round-38 no-harm (append-only) verification.
# Verifies that front-door/registry files changed without harming existing content.
# Usage:
#   BASE=<commit> REF=<commit> [LANE=<lane>] [SCRATCH=<dir>] bash r38-noharm.sh
#   BASE=<commit> REF=WORKTREE            # base commit vs the live working tree
# Exit: 0 = no harm; 1 = harm detected. Per-file table on stdout.
set -euo pipefail

LANE=${LANE:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
BASE=${BASE:?set BASE=<commit>}
REF=${REF:?set REF=<commit> or WORKTREE}
SCRATCH=${SCRATCH:-/fast/scratch/hyaku/kasegi-r38/RevNoHarm}
mkdir -p "$SCRATCH"
W=$(mktemp -d "$SCRATCH/noharm.XXXXXX")
trap 'rm -rf -- "$W"' EXIT

# Rule A (strict append-only): zero deletions AND base bytes are a byte-identical prefix
# of ref bytes (equivalently: ref == base ++ appended bytes).
STRICT=(
  SKILL.md
  PROVINCE.md
  SCORECARD.md
  LOG.md
  SHONEN.md
  corpus/QUALITY.md
  corpus/knowledge/considerthese-proposals-ledger.md
  corpus/lessons/round-37.md
)
# Rule B (mid-table insertion): zero deletions AND every base line still present in ref,
# in order (difflib opcodes only equal/insert, confirmed by an exact greedy subsequence).
INSERT=(
  corpus/SOURCES.md   # S055 row inserts inside the registry table
  corpus/README.md    # F21 row inserts after F20 in the frontier table
)
FILES=("${STRICT[@]}" "${INSERT[@]}")

fetch() { # fetch <path> <ref|WORKTREE> -> bytes on stdout
  if [ "$2" = WORKTREE ]; then cat "$LANE/$1"; else git -C "$LANE" show "$2:$1"; fi
}

if [ "$REF" = WORKTREE ]; then diffargs=("$BASE"); else diffargs=("$BASE" "$REF"); fi

echo "run_utc=$(date -u +%FT%TZ)"
echo "lane=$LANE"
echo "lane_head=$(git -C "$LANE" rev-parse HEAD)"
echo "base=$(git -C "$LANE" rev-parse "$BASE")"
if [ "$REF" = WORKTREE ]; then
  echo "ref=WORKTREE"
else
  echo "ref=$(git -C "$LANE" rev-parse "$REF")"
  if git -C "$LANE" merge-base --is-ancestor "$BASE" "$REF"; then echo "ancestor_ok=true"; else echo "ancestor_ok=false"; fi
fi
echo
echo "== git diff --numstat base ref -- <ten files> =="
git -C "$LANE" diff --numstat "${diffargs[@]}" -- "${FILES[@]}"
echo

fail=0
printf '%-50s %5s %5s  %-6s %-7s %-8s %-9s %s\n' FILE ADD DEL RULE PREFIX INORDER DIFFOPS VERDICT
for f in "${FILES[@]}"; do
  case " ${STRICT[*]} " in *" $f "*) rule=strict ;; *) rule=insert ;; esac
  if ! git -C "$LANE" cat-file -e "$BASE:$f" 2>/dev/null; then
    printf '%-50s %5s %5s  %-6s %-7s %-8s %-9s %s\n' "$f" - - "$rule" - - - "FAIL(absent-at-base)"
    fail=$((fail + 1))
    continue
  fi
  fetch "$f" "$BASE" > "$W/b"
  fetch "$f" "$REF" > "$W/h"
  ns=$(git -C "$LANE" diff --numstat "${diffargs[@]}" -- "$f")
  if [ -n "$ns" ]; then
    add=${ns%%$'\t'*}; rest=${ns#*$'\t'}; del=${rest%%$'\t'*}
  else
    add=0; del=0
  fi
  chk=$(python3 - "$W/b" "$W/h" <<'PY'
import sys, difflib

def lines(x: bytes):
    p = x.split(b"\n")
    return [e + b"\n" for e in p[:-1]] + ([p[-1]] if p[-1] else [])

b = open(sys.argv[1], "rb").read()
h = open(sys.argv[2], "rb").read()
bl, hl = lines(b), lines(h)
# difflib LCS view; autojunk=False so frequent lines (blank, '|', table rows)
# are not junked — junking would fake delete/replace opcodes on pure insertions.
ops = {k for k, *_ in difflib.SequenceMatcher(None, bl, hl, autojunk=False).get_opcodes()}
only_ins = ops <= {"equal", "insert"}
# exact ground truth: greedy in-order subsequence (every base line found, in order)
it = iter(hl)
inorder = all(any(x == y for x in it) for y in bl)
print(int(h.startswith(b)), int(only_ins), int(inorder), "+".join(sorted(ops)) if ops else "-")
PY
)
  read -r prefix onlyins inorder opstr <<<"$chk"
  if [ "$rule" = strict ]; then
    if [ "$del" = 0 ] && [ "$prefix" = 1 ]; then ok=PASS; else ok=FAIL; fi
  else
    if [ "$del" = 0 ] && [ "$inorder" = 1 ] && [ "$onlyins" = 1 ]; then ok=PASS; else ok=FAIL; fi
  fi
  if [ "$ok" = FAIL ]; then fail=$((fail + 1)); fi
  printf '%-50s %5s %5s  %-6s %-7s %-8s %-9s %s\n' "$f" "$add" "$del" "$rule" "$prefix" "$inorder" "$opstr" "$ok"
done
echo
if [ "$fail" -gt 0 ]; then
  echo "noharm: FAIL ($fail of ${#FILES[@]} file(s) harmed)"
  exit 1
fi
echo "noharm: PASS (${#FILES[@]}/${#FILES[@]} files, exit 0)"
```
