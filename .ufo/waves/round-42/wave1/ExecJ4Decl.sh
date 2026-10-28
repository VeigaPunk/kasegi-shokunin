#!/usr/bin/env bash
# ExecJ4Decl.sh — the round-42 J4 limb (family F-DECL), sourceable by
# corpus/instruments/r42-closure.sh.
#
# WHAT IT GRADES (family F-DECL)
#   The round-41 declared-blocks validator (r41-closure.sh: declared_blocks_check
#   / check_i5, lines 1054-1125) was a VALIDATED SUBSET, not a completeness
#   assertion: it iterated the declarations and validated each one and never
#   enumerated the paths the checks actually read.  Two routed defects survive
#   that shape:
#
#     T7   a declared path that resolves OUTSIDE the export root through a
#          symlink was read anyway and its declaration matched the bytes that
#          lived outside the export.  The byte transcript is committed at
#          .ufo/waves/round-40/wave2/RevC1Counters.defeats.txt lines 22-25
#          (section "## D2  H9 symlink out-of-export read (T7)"):
#            == T7 H9 symlink declaration reads OUTSIDE the export
#               numstat: 1	0	pwn
#            rc=0 payload=declared=1,valid=1,tail=1,pure=1,paths=1,diff-read=ok
#               (valid=1 with a declaration whose bytes live outside the
#                export = out-of-export read)
#          The digest/tail clause passes on those bytes; only containment can
#          catch the read.
#     D-COV (CritDeclarationCoverage, .ufo/waves/round-41/wave2/
#          CritDeclarationCoverage.md)  a path changed in the round but absent
#          from the declaration file was never visited, so the declarations were
#          a validated subset rather than a completeness assertion; the report
#          names the correction: compare the COMPLETE changed-path set for
#          BASE_REF..REF with the declared-path set and require exact coverage.
#
#   J4 closes both in one validator over the export:
#
#     1. DECLARATION VALIDITY  every pinned declaration binds real bytes, and
#        binds them to the CHANGED REGION rather than to an arbitrary suffix:
#        the file's last <lines> lines must hash to the declared sha256; the
#        number of lines the diff ADDS must equal <lines>; the path must have
#        zero deletions; the base revision's bytes must be a PREFIX of the
#        graded revision's bytes (the change is an append, not an in-place
#        edit); and the appended bytes must equal the bound region byte for
#        byte.  A path unchanged since the base ref, or changed in any other
#        way (an in-place edit, a deletion, an append that is not at the tail),
#        is pinned to its WHOLE file instead — strictly stronger than a tail
#        binding, because any later change of any byte is a digest mismatch.
#     2. CONTAINMENT           every declared path is a lane-relative path with
#        no `.`/`..` component, no absolute prefix, no symlink in ANY
#        component, and a canonical path that resolves UNDER the export root.
#        A symlink escape, a `..` escape and an absolute path are all rejected.
#     3. COVERAGE              every path changed between the base ref and the
#        graded ref is declared; every path read through the guarded accessor
#        `j4_read` is declared; every lane-relative artifact path the exported
#        suite names literally is declared.  An undeclared path is a DEFECT,
#        not an unvisited path.
#     4. NON-VACUITY           an empty declaration set is red: a gate must
#        never be green with nothing declared.
#
# THE DECLARATION FILE
#   `.ufo/waves/round-42/declared-blocks.txt` (override: R42_DECLARED).  One
#   record per line, ALWAYS three whitespace-separated fields, so the record
#   grammar is the round-41 one (`<path> <lines> <sha256>`) and any tool that
#   reads the list with `awk 'NF>=3 {print $1}'` sees every declared path:
#
#     <path> <lines> <sha256>   pinned.  <lines> is a positive integer and
#                               <sha256> is the digest of the file's LAST
#                               <lines> lines (`tail -n <lines> <path> |
#                               sha256sum`).  When the path changed since the
#                               base ref the pin binds the ADDED REGION: the
#                               base bytes are a prefix of the graded bytes,
#                               the path has zero deletions, the added-line
#                               count equals <lines>, and the appended bytes
#                               equal the bound region byte for byte (the
#                               round-41 "whole appended tail" rule).  When the
#                               path is unchanged since the base ref, or when
#                               it was edited in place, <lines> is the WHOLE
#                               file's line count and the digest is the whole
#                               file's digest.
#     <path> dyn unpinned       declared, NOT pinned: the path is in flux and
#                               its bytes cannot be bound at declaration time.
#                               Exactly three paths use it — the declaration
#                               file itself (it cannot contain its own digest),
#                               the suite file (its bytes are pinned by the
#                               receipt's suite-sha256, which J8 grades, so J4
#                               does not bind the instrument twice) and the
#                               receipt (it does not exist until the run that
#                               writes it).
#                               It still counts as DECLARED for every coverage
#                               clause; it is not hashed.  No other path is
#                               declared unpinned: j4_pin always produces a
#                               binding for a path that exists, so `dyn
#                               unpinned` on any other path is a generator bug,
#                               and the checker does not accept a pinned path
#                               whose recomputed binding differs.
#
#   Blank lines and `#` comments are ignored.  Every other line must parse.
#
# THE GUARDED READER
#   `j4_read TREE PATH` reads an export artifact and REFUSES (exit 3) when
#   PATH is not declared, or when PATH escapes the export root; on success it
#   appends the read to the read ledger (`R42_READ_LEDGER`, else
#   $WORK/read-ledger.txt).  The suite reads export artifacts through it and
#   J4 then grades the ledger: an undeclared read is a defect.
#
# THE REGENERATOR
#   `j4_regen REPO BASE REF OUT` writes the declaration file for REF.  The L1
#   runs it once the round-42 tree is final (at the judged head) and lands the
#   result; the suite then grades that file.  Re-run it after any landing that
#   changes the tree.
#
# ENV KNOBS (documented so a wave-2 seat can point a defeat at the live suite)
#   R42_DECLARED=<path>        the declaration file J4 reads (default
#                              .ufo/waves/round-42/declared-blocks.txt inside TREE)
#   R42_READ_LEDGER=<path>     the read ledger J4 grades (default $WORK/read-ledger.txt)
#   J4_BASE=<ref>              the base ref the changed-path set is computed from
#                              (default 5053a7f46de35784cff4b56756906e9014a38276)
#   LANE=<dir>                 the lane repository (default: the git root that
#                              contains this file, else $PWD)
#   J4_DISABLE_LITERAL=1       skip the literal-extraction clause (a documented
#                              limit; never set in a graded run)
#
# LIMIT (documented, not hidden)
#   The literal clause sees only the path-like literals of the exported suite
#   file `corpus/instruments/r42-closure.sh` that exist as regular files in the
#   export.  A path the suite builds at runtime from a computed name is not
#   seen by that clause; such a path is seen by the changed-path clause and by
#   the `j4_read` ledger when the suite reads through the guarded accessor.
#
# EXIT CODES: 0 green, 1 a defect is present, 2 a defect in the invocation.
# Sourcing this file defines functions only; it never exits and never writes
# outside the paths the caller names.
set -uo pipefail

# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

J4_ROUND=42
J4_DECL_REL=.ufo/waves/round-42/declared-blocks.txt
J4_SUITE_REL=corpus/instruments/r42-closure.sh
J4_RECEIPT_REL=.ufo/waves/round-42/final-gates/all-gates.txt
J4_BASE_DEFAULT=5053a7f46de35784cff4b56756906e9014a38276

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

# j4_lane — the lane repository root: $LANE when it is a git work tree, else the
# nearest ancestor of this file that holds .git, else $PWD.
j4_lane() {
  local d
  if [ -n "${LANE:-}" ] && [ -e "${LANE:-}/.git" ]; then
    (cd -- "${LANE}" && pwd -P); return 0
  fi
  d=$(dirname -- "${BASH_SOURCE[0]}")
  while [ -n "$d" ] && [ "$d" != "/" ]; do
    if [ -e "$d/.git" ]; then (cd -- "$d" && pwd -P); return 0; fi
    d=$(dirname -- "$d")
  done
  if [ -e "$PWD/.git" ]; then (cd -- "$PWD" && pwd -P); return 0; fi
  printf '%s\n' "$PWD"
}

# j4_base — the base ref the changed-path set is computed from.
j4_base() { printf '%s\n' "${J4_BASE:-$J4_BASE_DEFAULT}"; }

# j4_path_safe PATH — 0 when PATH is a lane-relative path with no `.`/`..`
# component, no empty component, no leading `/` and no trailing `/`.
j4_path_safe() {
  local p=$1
  local c
  local rest
  case $p in ''|/*|*/) return 1 ;; esac
  rest=$p
  while :; do
    c=${rest%%/*}
    case $c in ''|.|..) return 1 ;; esac
    case $rest in
      */*) rest=${rest#*/} ;;
      *) break ;;
    esac
  done
  return 0
}

# j4_symlink_component TREE PATH — 0 when no component of PATH inside TREE is a
# symlink.  A symlink ANYWHERE along the path is an escape vector, not only a
# symlink at the final component.
j4_symlink_component() {
  local tree=$1
  local p=$2
  local rest=$p
  local cur=$tree
  local c
  while [ -n "$rest" ]; do
    c=${rest%%/*}
    if [ "$c" = "$rest" ]; then rest=''; else rest=${rest#*/}; fi
    [ -n "$c" ] || continue
    cur="$cur/$c"
    [ -L "$cur" ] && return 1
    [ -e "$cur" ] || break
  done
  return 0
}

# j4_decl_file TREE — the declaration file J4 reads for TREE.
j4_decl_file() {
  local tree=$1
  local d=${R42_DECLARED:-}
  if [ -n "$d" ]; then
    case $d in /*) printf '%s\n' "$d" ;; *) printf '%s/%s\n' "$tree" "$d" ;; esac
    return 0
  fi
  printf '%s/%s\n' "$tree" "$J4_DECL_REL"
}

# j4_ledger — the read ledger path (empty when no ledger is configured).
j4_ledger() {
  if [ -n "${R42_READ_LEDGER:-}" ]; then printf '%s\n' "$R42_READ_LEDGER"; return 0; fi
  if [ -n "${WORK:-}" ]; then printf '%s/read-ledger.txt\n' "$WORK"; return 0; fi
  printf '\n'
}

# j4_tail_lines FILE — the smallest N with `tail -n N FILE` == FILE.  A file
# that does not end in a newline needs one more line than `wc -l` reports.
j4_tail_lines() {
  local f=$1
  local n
  local last
  n=$(wc -l < "$f" 2>/dev/null | tr -d ' ')
  n=${n:-0}
  if [ -s "$f" ]; then
    last=$(tail -c 1 -- "$f" 2>/dev/null | od -An -tu1 | tr -d ' \n')
    if [ "$last" != 10 ]; then n=$((n + 1)); fi
  fi
  [ "$n" -ge 1 ] || n=1
  printf '%s\n' "$n"
}

# j4_sha FILE — the sha256 of FILE.
j4_sha() { sha256sum -- "$1" 2>/dev/null | awk '{print $1; exit}'; }

# j4_scratch — a private scratch directory for the regenerator's temporary
# files.  It is created ONCE per process and is deliberately OUTSIDE the lane
# repository when the caller can arrange that, so the regenerator's own
# temporaries can never be mistaken for untracked lane artifacts in `work`
# mode.  The directory name is prefixed `j4decl.` so it is recognisable even
# when TMPDIR points inside the lane.
#
# It is created by ASSIGNMENT, never inside a command substitution: a
# subshell would set the variable in the child only, and the caller's filters
# would then see an empty scratch path.
J4_SCRATCH=
j4_scratch_init() {
  [ -n "$J4_SCRATCH" ] && return 0
  J4_SCRATCH=$(mktemp -d -t j4decl.XXXXXXXX 2>/dev/null || printf '')
  if [ -z "$J4_SCRATCH" ] || [ ! -d "$J4_SCRATCH" ]; then
    J4_SCRATCH=${TMPDIR:-/tmp}
    mkdir -p -- "$J4_SCRATCH" 2>/dev/null || true
  fi
  return 0
}

# j4_tmp — a fresh temporary file inside the private scratch directory.
j4_tmp() {
  j4_scratch_init
  mktemp "$J4_SCRATCH/j4.XXXXXXXX" 2>/dev/null || mktemp
}

# j4_declared_set FILE — the declared path set, one path per line, on stdout.
j4_declared_set() {
  local f=$1
  local line
  local path
  [ -f "$f" ] || return 1
  while IFS= read -r line || [ -n "$line" ]; do
    case $line in ''|'#'*) continue ;; esac
    set -f; set -- $line; set +f
    path=${1:-}
    [ -n "$path" ] || continue
    printf '%s\n' "$path"
  done < "$f"
}

# j4_is_declared FILE PATH — 0 when PATH is declared.  grep runs WITHOUT -q so
# it consumes the whole stream: under `set -o pipefail` an early -q exit would
# surface the writer's SIGPIPE as a pipeline failure.
j4_is_declared() {
  local f=$1
  local p=$2
  [ -f "$f" ] || return 1
  j4_declared_set "$f" | grep -xF -- "$p" >/dev/null 2>&1
}

# j4_literal_candidates FILE — the path-like literals of FILE, one per line.
# The leading character class includes `.` so a dot-prefixed artifact path
# (`.ufo/waves/round-42/declared-blocks.txt`) is captured whole instead of
# being truncated to `ufo/...`.
j4_literal_candidates() {
  local f=$1
  [ -f "$f" ] || return 0
  grep -oE '[A-Za-z0-9_.-][A-Za-z0-9_./-]*\.(md|py|sh|txt|json|tsv|csv)' -- "$f" 2>/dev/null \
    | sort -u
}

# j4_literal_paths ROOT SUITE_ABS — the lane-relative artifact paths the suite
# names literally and that exist as regular files under ROOT.
j4_literal_paths() {
  local root=$1
  local suite=$2
  local lit
  [ -f "$suite" ] || return 0
  j4_literal_candidates "$suite" | while IFS= read -r lit; do
    case $lit in
      /*|../*|*/../*|*/..|*/.|./*) continue ;;
    esac
    [ -f "$root/$lit" ] || continue
    [ -L "$root/$lit" ] && continue
    printf '%s\n' "$lit"
  done
}

# j4_changed_paths LANE BASE REF — the paths changed between BASE and REF.
j4_changed_paths() {
  local lane=$1
  local base=$2
  local ref=$3
  git --no-optional-locks -C "$lane" diff --name-only "$base" "$ref" -- 2>/dev/null
}

# j4_numstat LANE BASE REF PATH — "add del" for PATH, empty when unchanged.
j4_numstat() {
  local lane=$1
  local base=$2
  local ref=$3
  local p=$4
  git --no-optional-locks -C "$lane" diff --numstat "$base" "$ref" -- "$p" 2>/dev/null
}

# j4_blob LANE REV PATH OUT — write the blob of PATH at REV to OUT.  Exit 1
# when the path does not exist at REV.
j4_blob() {
  local lane=$1
  local rev=$2
  local p=$3
  local out=$4
  git --no-optional-locks -C "$lane" show "$rev:$p" > "$out" 2>/dev/null
}

# j4_blob_size LANE REV PATH — the byte size of the blob of PATH at REV, or
# the empty string when the path does not exist there.
j4_blob_size() {
  local lane=$1
  local rev=$2
  local p=$3
  git --no-optional-locks -C "$lane" cat-file -s "$rev:$p" 2>/dev/null
}

# ---------------------------------------------------------------------------
# the pin arithmetic (shared by the checker and the generator)
# ---------------------------------------------------------------------------

# j4_pin LANE BASE REF PATH FILE MODE — print "<lines> <sha256>" when PATH can
# be PINNED at REF, or nothing when it must be declared `dyn`.
#
# A path is pinnable when
#   (a) it is UNCHANGED since BASE — the pin binds the whole file; or
#   (b) it changed by a pure APPEND whose added region is the file's whole
#       tail — the pin binds the ADDED REGION (the round-41 whole-appended-tail
#       rule: zero deletions, added-line count == <lines>, appended bytes ==
#       the last <lines> lines); or
#   (c) it changed in any other way (an in-place edit, a deletion, an append
#       that is not at the tail) — the pin binds the WHOLE file, which is
#       strictly stronger than a tail binding: any later change of any byte is
#       a digest mismatch.
# A path returns nothing (and is declared `dyn unpinned`) only when FILE does
# not exist, which is the receipt before the run that writes it.
#
# MODE is `ref` (REF is a commit) or `work` (REF names the working tree: the
# changed set and the line counts come from `git diff BASE`, i.e. the tree as
# it stands before the next commit, and FILE is the working-tree file).
j4_pin() { # LANE BASE REF PATH FILE MODE
  local lane=$1
  local base=$2
  local ref=$3
  local p=$4
  local file=$5
  local mode=${6:-ref}
  local nm add del lines added_lines tail_sha added_sha tmpb tmpa
  if [ "$mode" = work ]; then
    nm=$(git --no-optional-locks -C "$lane" diff --numstat "$base" -- "$p" 2>/dev/null)
  else
    nm=$(j4_numstat "$lane" "$base" "$ref" "$p")
  fi
  if [ -z "$nm" ]; then
    # unchanged since the base ref: bind the whole file
    lines=$(j4_tail_lines "$file")
    printf '%s %s\n' "$lines" "$(j4_sha "$file")"
    return 0
  fi
  # whole-file binding: the fallback for every non-append change, and the
  # binding for a path that is new at REF
  local whole_lines whole_sha
  whole_lines=$(j4_tail_lines "$file")
  whole_sha=$(j4_sha "$file")

  set -f; set -- $nm; set +f
  add=${1:-}; del=${2:-}
  case $add in ''|*[!0-9]*) printf '%s %s\n' "$whole_lines" "$whole_sha"; return 0 ;; esac
  if [ "$del" != 0 ] || [ "$add" -lt 1 ]; then
    printf '%s %s\n' "$whole_lines" "$whole_sha"
    return 0
  fi
  tmpb=$(j4_tmp) || { printf '%s %s\n' "$whole_lines" "$whole_sha"; return 0; }
  tmpa=$(j4_tmp) || { rm -f -- "$tmpb"; printf '%s %s\n' "$whole_lines" "$whole_sha"; return 0; }
  if ! j4_blob "$lane" "$base" "$p" "$tmpb"; then
    # the path is new at REF: the whole file is the added region
    rm -f -- "$tmpb" "$tmpa"
    printf '%s %s\n' "$whole_lines" "$whole_sha"
    return 0
  fi
  local base_size
  base_size=$(wc -c < "$tmpb" | tr -d ' ')
  if ! head -c "$base_size" -- "$file" | cmp -s -- "$tmpb" - \
     || ! tail -c "+$((base_size + 1))" -- "$file" > "$tmpa" 2>/dev/null; then
    # not an append: an in-place edit, or a change that is not a prefix append
    rm -f -- "$tmpb" "$tmpa"
    printf '%s %s\n' "$whole_lines" "$whole_sha"
    return 0
  fi
  added_lines=$(wc -l < "$tmpa" | tr -d ' ')
  added_lines=${added_lines:-0}
  tail_sha=$(tail -n "$add" -- "$file" | j4_sha /dev/stdin)
  added_sha=$(j4_sha "$tmpa")
  rm -f -- "$tmpb" "$tmpa"
  # the whole-appended-tail rule: the added region must be a whole number of
  # lines equal to the diff's add count AND must be the file's tail
  if [ "$added_lines" = "$add" ] && [ "$tail_sha" = "$added_sha" ]; then
    printf '%s %s\n' "$add" "$added_sha"
    return 0
  fi
  printf '%s %s\n' "$whole_lines" "$whole_sha"
  return 0
}

# ---------------------------------------------------------------------------
# check_j4
# ---------------------------------------------------------------------------

# check_j4 TREE REF — the J4 limb.  Prints the payload on stdout and returns 0
# only when every clause holds.  TREE is the export root, REF the graded ref.
check_j4() { # TREE REF
  local tree=$1
  local ref=$2
  local lane
  local base
  local decl
  local root
  lane=$(j4_lane)
  base=$(j4_base)
  decl=$(j4_decl_file "$tree")
  j4_scratch_init

  local declared=0
  local valid=0
  local pinned=0
  local dyn=0
  local malformed=0
  local paths=1
  local canon=1
  local symlink=0
  local nul=0
  local diffread=ok
  local changed=0
  local changed_undeclared=0
  local changed_symlink=0
  local reads=0
  local reads_undeclared=0
  local literal_undeclared=0
  local literals=0
  local ledger_state=absent
  local line path lines sha extra kind got okp realp rc pin

  if [ ! -d "$tree" ]; then
    printf 'declared=0,valid=0,pinned=0,dyn=0,malformed=0,paths=0,canon=0,symlink=0,nul=0,diff-read=fail,changed=0,changed-undeclared=0,changed-symlink=0,reads=0,reads-undeclared=0,literals=0,literal-undeclared=0,ledger=absent,file=missing'
    return 1
  fi
  root=$(realpath -m -- "$tree" 2>/dev/null || printf '%s' "$tree")

  if [ ! -f "$decl" ]; then
    printf 'declared=0,valid=0,pinned=0,dyn=0,malformed=0,paths=0,canon=0,symlink=0,nul=0,diff-read=fail,changed=0,changed-undeclared=0,changed-symlink=0,reads=0,reads-undeclared=0,literals=0,literal-undeclared=0,ledger=absent,file=missing'
    return 1
  fi
  if [ "$(tr -d '\000' < "$decl" | wc -c)" != "$(wc -c < "$decl")" ]; then nul=1; fi

  # --- clauses 1+2: declaration validity and containment --------------------
  while IFS= read -r line || [ -n "$line" ]; do
    case $line in ''|'#'*) continue ;; esac
    set -f; set -- $line; set +f
    path=${1:-}; lines=${2:-}; sha=${3:-}; extra=${4:-}
    if [ -z "$path" ]; then malformed=$((malformed + 1)); continue; fi
    declared=$((declared + 1))

    if [ "$lines" = dyn ] && [ "$sha" = unpinned ] && [ -z "$extra" ]; then
      kind=dyn
    elif [ -n "$lines" ] && [ -n "$sha" ] && [ -z "$extra" ]; then
      kind=pin
      case $lines in ''|*[!0-9]*) malformed=$((malformed + 1)); continue ;; esac
      [ "$lines" -ge 1 ] || { malformed=$((malformed + 1)); continue; }
      case $sha in ''|*[!0-9a-f]*) malformed=$((malformed + 1)); continue ;; esac
      [ "${#sha}" -eq 64 ] || { malformed=$((malformed + 1)); continue; }
    else
      malformed=$((malformed + 1)); continue
    fi

    okp=1
    if ! j4_path_safe "$path"; then paths=0; okp=0; fi
    if ! j4_symlink_component "$tree" "$path"; then symlink=1; okp=0; fi
    realp=$(realpath -m -- "$tree/$path" 2>/dev/null || printf '')
    case "$realp" in
      "$root"/*) ;;
      *) canon=0; okp=0 ;;
    esac
    if [ "$kind" = dyn ]; then
      # a dyn record declares the path; the file may not exist yet (a receipt).
      [ "$okp" -eq 1 ] && valid=$((valid + 1))
      dyn=$((dyn + 1))
      continue
    fi
    if [ ! -f "$tree/$path" ] || [ -L "$tree/$path" ]; then paths=0; okp=0; fi
    [ "$okp" -eq 1 ] || continue
    got=$(tail -n "$lines" -- "$tree/$path" 2>/dev/null | sha256sum | awk '{print $1; exit}')
    [ "$got" = "$sha" ] || continue
    pinned=$((pinned + 1))

    # the pin must bind the CHANGED REGION, not an arbitrary suffix: recompute
    # the pin from the git facts and require it to equal the declared one.
    pin=$(j4_pin "$lane" "$base" "$ref" "$path" "$tree/$path")
    rc=$?
    [ "$rc" -eq 0 ] || continue
    [ "$pin" = "$lines $sha" ] || continue
    valid=$((valid + 1))
  done < "$decl"

  # --- clause 3a: coverage of the changed-path set --------------------------
  # Every path changed since the base ref must be declared.  A changed path
  # that is a SYMLINK in the export is EXEMPT from the declaration
  # requirement: a symlink cannot legitimately be declared (the containment
  # clause rejects every declared symlink), so requiring it would make the
  # check unsatisfiable.  Such paths are counted separately and reported.
  local changed_list
  changed_list=$(j4_changed_paths "$lane" "$base" "$ref")
  rc=$?
  if [ "$rc" -ne 0 ]; then diffread=fail; fi
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    changed=$((changed + 1))
    if [ -L "$tree/$path" ]; then
      changed_symlink=$((changed_symlink + 1))
      continue
    fi
    j4_is_declared "$decl" "$path" || changed_undeclared=$((changed_undeclared + 1))
  done <<< "$changed_list"

  # --- clause 3b: coverage of the guarded reads ----------------------------
  local ledger
  ledger=$(j4_ledger)
  if [ -n "$ledger" ] && [ -f "$ledger" ]; then
    ledger_state=ok
    while IFS= read -r path; do
      case $path in ''|'#'*) continue ;; esac
      reads=$((reads + 1))
      j4_is_declared "$decl" "$path" || reads_undeclared=$((reads_undeclared + 1))
    done < "$ledger"
  fi

  # --- clause 3c: coverage of the suite's literal artifact paths -----------
  if [ "${J4_DISABLE_LITERAL:-0}" != 1 ]; then
    while IFS= read -r path; do
      [ -n "$path" ] || continue
      literals=$((literals + 1))
      j4_is_declared "$decl" "$path" || literal_undeclared=$((literal_undeclared + 1))
    done < <(j4_literal_paths "$tree" "$tree/$J4_SUITE_REL")
  fi

  printf 'declared=%s,valid=%s,pinned=%s,dyn=%s,malformed=%s,paths=%s,canon=%s,symlink=%s,nul=%s,diff-read=%s,changed=%s,changed-undeclared=%s,changed-symlink=%s,reads=%s,reads-undeclared=%s,literals=%s,literal-undeclared=%s,ledger=%s,file=present' \
    "$declared" "$valid" "$pinned" "$dyn" "$malformed" "$paths" "$canon" "$symlink" "$nul" \
    "$diffread" "$changed" "$changed_undeclared" "$changed_symlink" "$reads" "$reads_undeclared" "$literals" \
    "$literal_undeclared" "$ledger_state"

  [ "$declared" -ge 1 ] || return 1
  [ "$malformed" -eq 0 ] || return 1
  [ "$valid" -eq "$declared" ] || return 1
  [ "$paths" -eq 1 ] || return 1
  [ "$canon" -eq 1 ] || return 1
  [ "$symlink" -eq 0 ] || return 1
  [ "$nul" -eq 0 ] || return 1
  [ "$diffread" = ok ] || return 1
  [ "$changed_undeclared" -eq 0 ] || return 1
  [ "$reads_undeclared" -eq 0 ] || return 1
  [ "$literal_undeclared" -eq 0 ] || return 1
  return 0
}

# j4_line TREE REF — the J4 run line, in the suite's `J4 payload=... closed=0|1`
# grammar.
j4_line() { # TREE REF
  local tree=$1
  local ref=$2
  local payload
  local rc
  payload=$(check_j4 "$tree" "$ref")
  rc=$?
  printf 'J4 payload=%s closed=%s\n' "$payload" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
  return $rc
}

# ---------------------------------------------------------------------------
# the guarded reader
# ---------------------------------------------------------------------------

# j4_read TREE PATH — read an export artifact through the declaration gate.
# Exit 0 and the bytes on stdout when PATH is declared and inside the export;
# exit 3 and a diagnostic on stderr otherwise.
j4_read() { # TREE PATH
  local tree=$1
  local path=$2
  local decl ledger root realp
  decl=$(j4_decl_file "$tree")
  if ! j4_path_safe "$path"; then
    printf 'j4_read: unsafe path %s\n' "$path" >&2; return 3
  fi
  if ! j4_is_declared "$decl" "$path"; then
    printf 'j4_read: undeclared path %s\n' "$path" >&2; return 3
  fi
  root=$(realpath -m -- "$tree" 2>/dev/null || printf '%s' "$tree")
  realp=$(realpath -m -- "$tree/$path" 2>/dev/null || printf '')
  case "$realp" in
    "$root"/*) ;;
    *) printf 'j4_read: path escapes the export root %s\n' "$path" >&2; return 3 ;;
  esac
  ledger=$(j4_ledger)
  if [ -n "$ledger" ]; then
    mkdir -p -- "$(dirname -- "$ledger")" 2>/dev/null || true
    printf '%s\n' "$path" >> "$ledger" 2>/dev/null || true
  fi
  cat -- "$tree/$path"
}

# ---------------------------------------------------------------------------
# the generator (the L1 regenerates the declaration file at the judged head)
# ---------------------------------------------------------------------------

# j4_regen REPO BASE REF OUT [MODE] — write the declaration file for REF.
#
# MODE is `ref` (default; REF is a commit and the bytes come from that tree)
# or `work` (REF names the working tree: the changed set and the line counts
# come from `git diff BASE` against the tree as it stands before the next
# commit, and the bytes come from the working tree).  The L1 uses `work` to
# produce the declaration file for the tree it is about to commit as the
# judged head.
#
# The declared set is:
#   * every path changed between BASE and REF (the coverage clause needs it),
#   * every tracked file under corpus/ (the artifact corpus the checks read),
#   * the lane front doors (SCORECARD.md, LOG.md, SHONEN.md, PROVINCE.md,
#     SKILL.md, README.md, AGENTS.md),
#   * every lane-relative artifact path the suite names literally,
#   * the three artifacts that are in flux by construction: the declaration
#     file itself, the suite file and the receipt.
# A path is PINNED when j4_pin can bind it; every other path is `dyn`.
j4_regen() { # REPO BASE REF OUT [MODE]
  local repo=$1
  local base=$2
  local ref=$3
  local out=$4
  local mode=${5:-ref}
  local list p pin blob
  case $out in
    /*) ;;
    *) out="$PWD/$out" ;;
  esac
  j4_scratch_init
  list=$(j4_tmp) || return 2
  {
    # (1) every path changed since BASE: the coverage clause needs all of them
    if [ "$mode" = work ]; then
      git --no-optional-locks -C "$repo" diff --name-only "$base" -- 2>/dev/null
      # untracked files are part of the tree the L1 is about to commit, so
      # they are declared too; the generator's own scratch (by absolute path
      # and by its `j4decl.` name prefix) and its own output are excluded so
      # they cannot be mistaken for lane artifacts.
      git --no-optional-locks -C "$repo" ls-files --others --exclude-standard -- 2>/dev/null \
        | grep -v -F -x "$out" \
        | grep -v -F "$J4_SCRATCH/" \
        | grep -v '^j4decl\.' \
        | grep -v "^${J4_SCRATCH#*/}/"
    else
      git --no-optional-locks -C "$repo" diff --name-only "$base" "$ref" -- 2>/dev/null
    fi
    # (2) the artifact corpus the checks read
    if [ "$mode" = work ]; then
      git --no-optional-locks -C "$repo" ls-files -- corpus/ 2>/dev/null
    else
      git --no-optional-locks -C "$repo" ls-tree -r --name-only "$ref" -- corpus/ 2>/dev/null
    fi
    # (3) the lane front doors
    for p in SCORECARD.md LOG.md SHONEN.md PROVINCE.md SKILL.md README.md AGENTS.md; do
      if [ "$mode" = work ]; then
        [ -f "$repo/$p" ] && printf '%s\n' "$p"
      else
        git --no-optional-locks -C "$repo" cat-file -e "$ref:$p" 2>/dev/null && printf '%s\n' "$p"
      fi
    done
    # (4) the artifact paths the suite names literally.  A lane-relative
    # literal is declared whether or not the file exists at REF: a path the
    # suite names that only exists at Y (the receipt) must already be declared
    # at J.  A bare basename (`r42-closure.sh`) is declared only when it
    # exists at the export root, so the list carries no dead names.
    if [ "$mode" = work ]; then
      j4_literal_candidates "$repo/$J4_SUITE_REL" \
        | while IFS= read -r lit; do
            case $lit in /*|../*|*/../*|*/..|*/.|./*) continue ;; esac
            case $lit in
              */*) printf '%s\n' "$lit" ;;
              *) [ -f "$repo/$lit" ] && printf '%s\n' "$lit" ;;
            esac
          done
    else
      git --no-optional-locks -C "$repo" show "$ref:$J4_SUITE_REL" 2>/dev/null \
        | j4_literal_candidates /dev/stdin \
        | while IFS= read -r lit; do
            case $lit in /*|../*|*/../*|*/..|*/.|./*) continue ;; esac
            case $lit in
              */*) printf '%s\n' "$lit" ;;
              *) git --no-optional-locks -C "$repo" cat-file -e "$ref:$lit" 2>/dev/null \
                   && printf '%s\n' "$lit" ;;
            esac
          done
    fi
    # (5) the three artifacts that are in flux by construction
    printf '%s\n' "$J4_DECL_REL" "$J4_SUITE_REL" "$J4_RECEIPT_REL"
  } | LC_ALL=C sort -u > "$list"
  : > "$out"
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    j4_path_safe "$p" || continue
    # a symlink cannot be declared (the containment clause rejects every
    # declared symlink), so it is skipped rather than declared
    if [ "$mode" = work ]; then
      [ -L "$repo/$p" ] && continue
    else
      case $(git --no-optional-locks -C "$repo" ls-tree "$ref" -- "$p" 2>/dev/null | awk '{print $1}') in
        120000) continue ;;
      esac
    fi
    blob=$(j4_tmp) || { rm -f -- "$list"; return 2; }
    if [ "$mode" = work ]; then
      if [ ! -f "$repo/$p" ]; then
        rm -f -- "$blob"
        printf '%s dyn unpinned\n' "$p" >> "$out"
        continue
      fi
      cat -- "$repo/$p" > "$blob"
    else
      if ! j4_blob "$repo" "$ref" "$p" "$blob"; then
        rm -f -- "$blob"
        printf '%s dyn unpinned\n' "$p" >> "$out"
        continue
      fi
    fi
    case "$p" in
      "$J4_DECL_REL"|"$J4_SUITE_REL"|"$J4_RECEIPT_REL")
        rm -f -- "$blob"
        printf '%s dyn unpinned\n' "$p" >> "$out"
        continue ;;
    esac
    pin=$(j4_pin "$repo" "$base" "$ref" "$p" "$blob" "$mode")
    if [ -n "$pin" ]; then
      printf '%s %s\n' "$p" "$pin" >> "$out"
    else
      printf '%s dyn unpinned\n' "$p" >> "$out"
    fi
    rm -f -- "$blob"
  done < "$list"
  rm -f -- "$list"
  return 0
}

# ---------------------------------------------------------------------------
# standalone CLI (only when executed, never when sourced)
# ---------------------------------------------------------------------------

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  case ${1:-} in
    --check)
      check_j4 "${2:-}" "${3:-HEAD}"; exit $? ;;
    --regen)
      j4_regen "${2:-$(j4_lane)}" "${3:-$(j4_base)}" "${4:-HEAD}" "${5:-/dev/stdout}" "${6:-ref}"; exit $? ;;
    --regen-work)
      j4_regen "${2:-$(j4_lane)}" "${3:-$(j4_base)}" work "${4:-/dev/stdout}" work; exit $? ;;
    --help|-h)
      sed -n '2,/^set -uo pipefail$/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
      exit 0 ;;
    *)
      printf 'usage: %s --check TREE REF | --regen REPO BASE REF OUT\n' "${0##*/}" >&2
      exit 2 ;;
  esac
fi
