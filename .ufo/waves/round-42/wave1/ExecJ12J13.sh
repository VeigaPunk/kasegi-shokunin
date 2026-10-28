#!/usr/bin/env bash
# ExecJ12J13.sh — round-42 closure-suite limbs J12 and J13 (sourceable bash).
#
# PURPOSE
#   J12 is the depth:density no-harm guard: relative to the round base, the
#   round deletes no tracked path under corpus/ and
#   corpus/instruments/density.py stays byte-identical to the base blob.
#   J13 is the quiescence guard: the tree under test is exactly the exported
#   ref (no uncommitted drift, no extra files), measured in a clone bound to
#   the exported ref BY NAME, and the suite's own scratch root holds no
#   leftover beyond this run's own --work.
#
#   This file is the LIMB.  It is SOURCEABLE: sourcing it defines the
#   functions below and executes nothing (no `set` options are changed, no
#   command runs at source time).  Every helper is prefixed `j12j13_` or
#   `j13_` except the two entry points `check_j12` and `check_j13`, so the
#   suite can source this file beside its own helpers.
#
# API (what the suite calls)
#   check_j12 TREE REF
#       Reads the exported tree TREE and the exported commit REF.
#       Prints exactly one payload line on stdout:
#           deleted=<n>,renamed=<n>,density=<0|1>,base-density=<0|1>,
#           missing=<0|1>,diff-read=<ok|fail>
#       exit 0 (green) iff deleted=0 AND density=1 AND base-density=1 AND
#       missing=0 AND diff-read=ok; exit 1 otherwise.
#
#       deleted     number of tracked paths under corpus/ that the exported
#                   ref DELETED relative to the base.  Computed with rename
#                   detection OFF (--no-renames) so a corpus path renamed
#                   away — in either direction across the corpus/ boundary —
#                   counts as a deletion, because a renamed-away corpus path
#                   is gone.  The pathspec is `corpus/`, so a deletion
#                   outside corpus/ never counts (erratum E5: the F-TABLE
#                   repair deletes SKILL.md lines; SKILL.md is outside
#                   corpus/ and is out of J12's scope).
#       renamed     diagnostic only: the number of rename rows git reports
#                   for corpus/ with rename detection ON.  It does not gate;
#                   `deleted` already subsumes it.
#       density     1 when the sha256 of TREE/corpus/instruments/density.py
#                   equals the sha256 of the BASE blob
#                   base:corpus/instruments/density.py.
#       base-density
#                   1 when the BASE blob digest equals the pinned round-42
#                   digest (J12_PINNED_DENSITY).  Fail-closed: a base whose
#                   density.py is not the pinned blob is a wrong base, not a
#                   pass.
#       missing     1 when TREE/corpus/instruments/density.py is absent.
#       diff-read   ok when the git diff and blob reads succeeded; fail is
#                   red (never a vacuous tally).
#
#   check_j13 TREE REF
#       Prints exactly one payload line on stdout:
#           clone=<ok|fail>,ref=<ok|fail>,uncommitted=<n>,drift=<n>,
#           untracked=<n>,strays=<n>,leftovers=<n>,read=<ok|fail>,
#           scope=<own|host-global>
#       exit 0 (green) iff clone=ok AND ref=ok AND uncommitted=0 AND
#       drift=0 AND untracked=0 AND strays=0 AND leftovers=0 AND read=ok
#       AND scope=own; exit 1 otherwise.
#
#       clone       ok when a shared, no-checkout clone of the lane was
#                   created inside this run's own --work dir (never inside
#                   the lane) and the clone's toplevel was asserted.
#       ref         ok when the exported ref resolves to a commit in that
#                   clone AND the clone's HEAD is bound to that ref by
#                   name.  A mistyped ref is a red, never a vacuous tally.
#       uncommitted the number of `git status --porcelain` lines in the
#                   clone when the exported tree is the clone's work tree.
#                   This is the "no uncommitted changes in a clone of the
#                   exported ref" measurement: it is red exactly when the
#                   tree under test carries changes that are NOT in the
#                   exported commit, which is what an export taken from a
#                   dirty lane looks like.
#       drift       the number of `git diff --name-status` rows between the
#                   exported ref's tree and the exported tree (modified,
#                   deleted, or type-changed paths).
#       untracked   the number of files present in the exported tree but
#                   absent from the exported ref's tree.  Counted WITHOUT
#                   the standard excludes, so an ignored extra file counts
#                   too.
#       strays      the number of `kasegi-r4[0-9]*` entries inside the
#                   suite's own scratch root that are neither this run's
#                   --work nor inside it nor a clean-chain ancestor of it.
#       leftovers   the number of entries inside the suite's own scratch
#                   root that are neither this run's --work nor inside it
#                   nor a clean-chain ancestor of it.  This is the erratum
#                   E4 rule: at receipt time every leftover seat dir under
#                   the run's scratch prefix is a red stray and must be
#                   cleaned before the receipt run.
#       read        ok when every measurement completed; fail is red.
#       scope       own when the scanned scratch root is a run-scoped
#                   subtree of the fleet scratch root; host-global when the
#                   caller passed the fleet scratch root itself.
#                   host-global is RED: the claim requires the quiescence
#                   scan to be evaluated inside the suite's own scratch
#                   root, never host-global state (erratum E4).
#
# ENVIRONMENT (the suite's globals, with per-seat overrides)
#   LANE          the lane repository (default: the repository two levels
#                 above this file, else the round-42 lane path).
#   BASE_REF      the round base commit (default: the round-42 base).
#   WORK          the suite's --work directory; must lie inside
#                 SCRATCH_ROOT.
#   SCRATCH_ROOT  the suite's --scratch root (default: the fleet scratch
#                 root).
#   J12_LANE, J12_BASE, J12_TREE, J12_REF              J12 overrides.
#   J13_LANE, J13_WORK, J13_SCRATCH_ROOT, J13_TREE, J13_REF   J13 overrides.
#   J13_FLEET_ROOT      the host-global fleet scratch root (default
#                       /fast/scratch/hyaku).  A scan root equal to this path
#                       is host-global scope and is RED.
#   J12_PINNED_DENSITY  the pinned base digest of
#                       corpus/instruments/density.py (default: the round-42
#                       base digest).
#   J13_FAMILY          the scratch entry name family (default
#                       `kasegi-r4[0-9]*`).  Matched case- and
#                       separator-insensitively after normalization.
#   J13_LEFTOVER=0      count only family-named strays, not every leftover
#                       entry.  The default (1) applies the erratum E4
#                       rule; the suite never sets this.
#   J13_STRICT_SCOPE=0  downgrade a host-global scope red to a payload note
#                       only.  The suite never sets this; the default is
#                       strict.
#
# FAIL-CLOSED
#   An unreadable lane, an unresolvable base or ref, a missing density.py, a
#   failed git call, a failed clone, a scratch root that does not contain the
#   --work dir, or a failed scan all yield read=fail / clone=fail /
#   missing=1 and exit 1.  There is no fail-open path: a check that cannot
#   measure reports red.
#
# Exit codes of the two entry points: 0 green, 1 red.

# ---------------------------------------------------------------------------
# defaults (never override a value the suite already set)
# ---------------------------------------------------------------------------

J12_PINNED_DENSITY=${J12_PINNED_DENSITY:-ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710}
J12_BASE_DEFAULT=5053a7f46de35784cff4b56756906e9014a38276
J13_FLEET_ROOT=${J13_FLEET_ROOT:-/fast/scratch/hyaku}
J13_FAMILY=${J13_FAMILY:-kasegi-r4[0-9]*}
J13_LEFTOVER=${J13_LEFTOVER:-1}
J13_STRICT_SCOPE=${J13_STRICT_SCOPE:-1}

j12j13_self=${BASH_SOURCE[0]:-}
j12j13_lane_default=
if [ -n "$j12j13_self" ]; then
  # Walk up from this file to the nearest enclosing git work tree, so the
  # default works whether the limb sits in corpus/instruments/ or in a wave
  # directory.  Falls back to the round-42 lane path below.
  j12j13_lane_default=$(
    d=$( cd -- "$(dirname -- "$j12j13_self")" 2>/dev/null && pwd -P ) || d=
    while [ -n "$d" ]; do
      if [ -e "$d/.git" ]; then printf '%s' "$d"; break; fi
      [ "$d" = / ] && break
      d=${d%/*}
    done
  )
fi
j12j13_lane_default=${j12j13_lane_default:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}

# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------

# j12j13_digest FILE -> sha256 of FILE; empty on failure.
j12j13_digest() {
  local f=$1
  [ -n "$f" ] && [ -f "$f" ] && [ -r "$f" ] || return 1
  sha256sum -- "$f" 2>/dev/null | cut -d' ' -f1
}

# j12j13_lane [OVERRIDE_VAR] -> the lane repository to read.  The override
# variable name is taken from $1 when given (so check_j13 can honour its own
# J13_LANE); then the suite's LANE; then the derived default.
j12j13_lane() {
  local l ov=${1:-J12_LANE}
  l=${!ov:-}
  [ -n "$l" ] || l=${LANE:-}
  [ -n "$l" ] || l=$j12j13_lane_default
  printf '%s' "$l"
}

# j12j13_base -> the base commit to compare against.
j12j13_base() {
  local b
  b=${J12_BASE:-${BASE_REF:-}}
  [ -n "$b" ] || b=$J12_BASE_DEFAULT
  printf '%s' "$b"
}

# j12j13_count_lines -> number of non-empty lines on stdin (0 for no input).
j12j13_count_lines() { grep -c . 2>/dev/null || true; }

# ---------------------------------------------------------------------------
# J12 — the depth:density no-harm guard
# ---------------------------------------------------------------------------

check_j12() { # TREE REF
  local tree=${1:-${J12_TREE:-}}
  local ref=${2:-${J12_REF:-}}
  local lane base out deleted=0 renamed=0 missing=0 density=0 basedensity=0
  local exportdig basedig rc=0

  lane=$(j12j13_lane)
  base=$(j12j13_base)

  if [ -z "$tree" ] || [ ! -d "$tree" ] || [ -z "$lane" ] || [ ! -d "$lane" ] \
     || [ -z "$base" ] || [ -z "$ref" ]; then
    printf 'deleted=0,renamed=0,density=0,base-density=0,missing=1,diff-read=fail'
    return 1
  fi

  # --- tracked deletions under corpus/ relative to the base ---------------
  # --no-renames so a corpus path renamed away counts as a deletion.
  if out=$(git --no-optional-locks -C "$lane" diff --name-status --no-renames \
             --diff-filter=D "$base" "$ref" -- corpus/ 2>/dev/null); then
    deleted=$(printf '%s\n' "$out" | j12j13_count_lines)
    deleted=${deleted:-0}
    case $deleted in ''|*[!0-9]*) deleted=0; rc=1 ;; esac
  else
    deleted=0; rc=1
  fi

  # --- diagnostic: the rename rows git reports for corpus/ ----------------
  if out=$(git --no-optional-locks -C "$lane" diff --name-status \
             --diff-filter=R "$base" "$ref" -- corpus/ 2>/dev/null); then
    renamed=$(printf '%s\n' "$out" | j12j13_count_lines)
    renamed=${renamed:-0}
    case $renamed in ''|*[!0-9]*) renamed=0 ;; esac
  fi

  # --- density.py: the exported file vs the base blob ----------------------
  if [ ! -f "$tree/corpus/instruments/density.py" ]; then
    missing=1
  else
    exportdig=$(j12j13_digest "$tree/corpus/instruments/density.py") || exportdig=''
    basedig=$(git --no-optional-locks -C "$lane" cat-file blob \
                "$base:corpus/instruments/density.py" 2>/dev/null \
                | sha256sum 2>/dev/null | cut -d' ' -f1)
    if [ -n "$exportdig" ] && [ -n "$basedig" ] && [ "$exportdig" = "$basedig" ]; then
      density=1
    fi
    if [ -n "$basedig" ] && [ "$basedig" = "$J12_PINNED_DENSITY" ]; then
      basedensity=1
    fi
  fi

  if [ "$rc" -ne 0 ]; then
    printf 'deleted=0,renamed=%s,density=%s,base-density=%s,missing=%s,diff-read=fail' \
      "$renamed" "$density" "$basedensity" "$missing"
    return 1
  fi

  printf 'deleted=%s,renamed=%s,density=%s,base-density=%s,missing=%s,diff-read=ok' \
    "$deleted" "$renamed" "$density" "$basedensity" "$missing"
  [ "$deleted" -eq 0 ] && [ "$missing" -eq 0 ] && [ "$density" -eq 1 ] \
    && [ "$basedensity" -eq 1 ]
}

# ---------------------------------------------------------------------------
# J13 — quiescence
# ---------------------------------------------------------------------------

# j13_norm NAME -> the normalized name: lower case, leading dots stripped,
# every separator run collapsed to a single '-'.  Folding never turns a
# letter into '-', so the normalized key of `kasegi-r42` is `kasegi-r42`.
j13_norm() {
  local n
  n=$(printf '%s' "$1" | tr 'A-Z' 'a-z')
  while [ "${n:0:1}" = "." ]; do n=${n:1}; done
  printf '%s' "$n" | sed -e 's/[^a-z0-9]\{1,\}/-/g' -e 's/-\{1,\}/-/g' -e 's/-$//'
}

# j13_family_match NAME -> 0 when NAME belongs to the J13_FAMILY name family
# (`kasegi-r4[0-9]*` by default).  Matching is case- and separator-
# insensitive (so `kasegi_r42` and `.Kasegi-R42.` match) and prefix-based
# (a family match is a namespace, not a whole-name equality): `kasegi-r42`,
# `kasegi-r42-leftover` and `kasegi-r4x` all match, `kasegi-r4` does not.
j13_family_match() {
  local raw=$1 low n
  low=${raw,,}
  case $low in *kasegi*) ;; *) return 1 ;; esac
  n=$(j13_norm "$raw")
  case $n in kasegi-r4[0-9]*) return 0 ;; esac
  return 1
}

# j13_chain_clean ANCESTOR WORK -> 0 when the path from ANCESTOR down to WORK
# holds exactly the next component at every level and nothing else.  A family
# entry that merely shares a path prefix with --work is not tolerated.
j13_chain_clean() { # ANCESTOR WORK
  local a=$1 w=$2 rel rest comp dir n only
  case "$w" in "$a"/*) rel=${w#"$a"/} ;; *) return 1 ;; esac
  dir=$a
  rest=$rel
  while [ -n "$rest" ]; do
    comp=${rest%%/*}
    if [ "$comp" = "$rest" ]; then rest=''; else rest=${rest#*/}; fi
    n=$(ls -A -- "$dir" 2>/dev/null | grep -c . || true)
    [ "${n:-0}" -eq 1 ] || return 1
    only=$(ls -A -- "$dir" 2>/dev/null | head -n 1)
    [ "$only" = "$comp" ] || return 1
    dir=$dir/$comp
    [ -d "$dir" ] || return 1
  done
  return 0
}

# j13_tolerated ENTRY_REAL WORKCANON ISSYMLINK -> 0 when ENTRY_REAL is this
# run's own --work dir, lies inside it, or is a clean-chain ancestor of it.
# A SYMLINK that resolves to an ancestor of --work is NEVER tolerated (the
# round-40 wave-2 F5 escape): a family-named symlink pointing at an ancestor
# of the work dir is a stray even when the chain below it is clean.
j13_tolerated() { # ENTRY_REAL WORKCANON ISSYMLINK
  local e=$1 w=$2 issym=$3
  [ -n "$w" ] || return 1
  case "$e" in
    "$w"|"$w"/*) return 0 ;;
  esac
  case "$w" in
    "$e"/*)
      [ "$issym" = 1 ] && return 1
      j13_chain_clean "$e" "$w" && return 0
      return 1 ;;
  esac
  return 1
}

# j13_scan_scratch ROOT WORKCANON -> prints
#   "strays=<n>,leftovers=<n>,read=<ok|fail>,scanned=<n>"
# The scan is recursive, dot-inclusive and case/separator-insensitive.  The
# --work dir and everything inside it are never strays, and neither is a
# clean-chain ancestor of it.  A family-named ANCESTOR of --work is tolerated
# only when it is a real directory (a family symlink resolving to an
# ancestor is a stray).  `strays` counts family-named entries; `leftovers`
# counts every other entry that is not this run's own --work.
j13_scan_scratch() { # ROOT WORKCANON
  local root=$1 work=${2:-}
  local out e b real strays=0 leftovers=0 scanned=0 read=ok fam issym
  if [ -z "$root" ] || [ ! -d "$root" ]; then
    printf 'strays=0,leftovers=0,read=fail,scanned=0'; return 1
  fi
  # The --work subtree is pruned: it is this run's own scratch, and its
  # contents (including the J13 clone's .git files) are never strays.
  if [ -n "$work" ] && [ -d "$work" ]; then
    if ! out=$(find "$root" -mindepth 1 -path "$work" -prune -o -print 2>/dev/null); then
      printf 'strays=0,leftovers=0,read=fail,scanned=0'; return 1
    fi
  else
    if ! out=$(find "$root" -mindepth 1 -print 2>/dev/null); then
      printf 'strays=0,leftovers=0,read=fail,scanned=0'; return 1
    fi
  fi
  while IFS= read -r e; do
    [ -n "$e" ] || continue
    b=${e##*/}
    fam=0
    j13_family_match "$b" && fam=1
    [ "$fam" -eq 1 ] || [ "$J13_LEFTOVER" = 1 ] || continue
    scanned=$((scanned + 1))
    issym=0
    [ -L "$e" ] && issym=1
    # realpath -m resolves a regular file, a symlink to a file and a dangling
    # symlink alike; `cd` would fail on a plain file and count it as a stray.
    real=$(realpath -m -- "$e" 2>/dev/null) || real=''
    if [ -z "$real" ]; then
      read=fail; strays=$((strays + 1)); leftovers=$((leftovers + 1)); continue
    fi
    if j13_tolerated "$real" "$work" "$issym"; then continue; fi
    [ "$fam" -eq 1 ] && strays=$((strays + 1))
    leftovers=$((leftovers + 1))
  done <<< "$out"
  printf 'strays=%s,leftovers=%s,read=%s,scanned=%s' \
    "$strays" "$leftovers" "$read" "$scanned"
  [ "$read" = ok ] && [ "$strays" -eq 0 ] && [ "$leftovers" -eq 0 ] && return 0
  return 1
}

# j13_scope ROOT -> prints "own" when ROOT is a run-scoped subtree of the
# fleet scratch root, "host-global" when ROOT is the fleet scratch root
# itself.
j13_scope() { # ROOT
  local root=$1
  local fleet=${J13_FLEET_ROOT%/}
  [ -n "$root" ] || { printf 'own'; return 0; }
  if [ "$root" = "$fleet" ]; then printf 'host-global'; return 0; fi
  printf 'own'
}

check_j13() { # TREE REF
  local tree=${1:-${J13_TREE:-}}
  local ref=${2:-${J13_REF:-}}
  local lane work scratch clone scope realw realroot
  local uncommitted=0 drift=0 untracked=0 strays=0 leftovers=0
  local read=ok clonestate=fail refstate=fail
  local out

  lane=$(j12j13_lane J13_LANE)
  work=${J13_WORK:-${WORK:-}}
  scratch=${J13_SCRATCH_ROOT:-${SCRATCH_ROOT:-}}
  scope=$(j13_scope "$scratch")

  if [ -z "$tree" ] || [ ! -d "$tree" ] || [ -z "$lane" ] || [ ! -d "$lane" ] \
     || [ -z "$ref" ] || [ -z "$scratch" ] || [ ! -d "$scratch" ] \
     || [ -z "$work" ] || [ ! -d "$work" ]; then
    printf 'clone=fail,ref=fail,uncommitted=0,drift=0,untracked=0,strays=0,leftovers=0,read=fail,scope=%s' \
      "$scope"
    return 1
  fi

  realw=$( cd "$work" 2>/dev/null && pwd -P ) || realw=''
  realroot=$( cd "$scratch" 2>/dev/null && pwd -P ) || realroot=''
  if [ -z "$realw" ] || [ -z "$realroot" ]; then
    printf 'clone=fail,ref=fail,uncommitted=0,drift=0,untracked=0,strays=0,leftovers=0,read=fail,scope=%s' \
      "$scope"
    return 1
  fi
  # the --work dir must live inside the scanned scratch root, else the scan
  # cannot tell this run's own artifacts from a leftover
  case "$realw" in
    "$realroot"|"$realroot"/*) ;;
    *)
      printf 'clone=fail,ref=fail,uncommitted=0,drift=0,untracked=0,strays=0,leftovers=0,read=fail,scope=%s' \
        "$scope"
      return 1 ;;
  esac

  # --- the clone of the exported ref, inside this run's own --work dir ----
  # The clone is created under --work so it is this run's own artifact, lives
  # inside the suite's own scratch root, and is never counted as a leftover.
  # --shared keeps it tiny and --no-checkout keeps the lane's objects
  # untouched; the lane's .git directory is never written to.  The clone is
  # removed again before this function returns, so the check leaves no
  # residue in the scratch root.
  clone="$realw/j13-ref-clone"
  rm -rf -- "$clone"
  if git -c gc.auto=0 -c maintenance.auto=false clone --quiet --shared --no-checkout \
       "$lane" "$clone" >/dev/null 2>&1 \
     && [ "$(git -C "$clone" rev-parse --show-toplevel 2>/dev/null)" = "$clone" ]; then
    clonestate=ok
    if git -C "$clone" cat-file -e "$ref^{commit}" >/dev/null 2>&1; then
      # Bind the clone to the exported ref BY NAME: HEAD is pointed at the
      # exported ref, the clone's index becomes the exported ref's tree and
      # the exported tree becomes the clone's work tree.  Every reported
      # change is then a change that is NOT in the exported commit.
      if git -C "$clone" update-ref --no-deref HEAD "$ref" >/dev/null 2>&1 \
         && git -C "$clone" read-tree "$ref" >/dev/null 2>&1; then
        refstate=ok
        if out=$(git -C "$clone" --work-tree="$tree" status --porcelain \
                   --untracked-files=all 2>/dev/null); then
          uncommitted=$(printf '%s\n' "$out" | j12j13_count_lines)
          uncommitted=${uncommitted:-0}
          case $uncommitted in ''|*[!0-9]*) uncommitted=1; read=fail ;; esac
        else
          uncommitted=1; read=fail
        fi
        if out=$(git -C "$clone" --work-tree="$tree" diff --name-status 2>/dev/null); then
          drift=$(printf '%s\n' "$out" | j12j13_count_lines)
          drift=${drift:-0}
          case $drift in ''|*[!0-9]*) drift=1; read=fail ;; esac
        else
          drift=1; read=fail
        fi
        if out=$(git -C "$clone" --work-tree="$tree" ls-files --others 2>/dev/null); then
          untracked=$(printf '%s\n' "$out" | j12j13_count_lines)
          untracked=${untracked:-0}
          case $untracked in ''|*[!0-9]*) untracked=1; read=fail ;; esac
        else
          untracked=1; read=fail
        fi
      else
        read=fail
      fi
    else
      refstate=fail
      read=fail
    fi
  fi

  # --- the scratch scan, inside the suite's own scratch root --------------
  out=$(j13_scan_scratch "$realroot" "$realw")
  strays=${out#strays=}; strays=${strays%%,*}
  leftovers=${out#*leftovers=}; leftovers=${leftovers%%,*}
  case $strays in ''|*[!0-9]*) strays=1; read=fail ;; esac
  case $leftovers in ''|*[!0-9]*) leftovers=1; read=fail ;; esac
  case $out in *'read=ok'*) ;; *) read=fail ;; esac

  printf 'clone=%s,ref=%s,uncommitted=%s,drift=%s,untracked=%s,strays=%s,leftovers=%s,read=%s,scope=%s' \
    "$clonestate" "$refstate" "$uncommitted" "$drift" "$untracked" \
    "$strays" "$leftovers" "$read" "$scope"

  if [ "$scope" = 'host-global' ] && [ "$J13_STRICT_SCOPE" = 1 ]; then
    rm -rf -- "$clone"
    return 1
  fi
  rm -rf -- "$clone"
  [ "$clonestate" = ok ] && [ "$refstate" = ok ] && [ "$uncommitted" -eq 0 ] \
    && [ "$drift" -eq 0 ] && [ "$untracked" -eq 0 ] && [ "$strays" -eq 0 ] \
    && [ "$leftovers" -eq 0 ] && [ "$read" = ok ]
}
