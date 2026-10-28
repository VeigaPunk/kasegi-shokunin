#!/usr/bin/env bash
# ExecJ10Isolate.sh — J10 limb of the kasegi round-42 closure suite.
#
# WHAT THIS LIMB IS
#   A sourceable limb providing check_j10(): the graded-selftest ISOLATION
#   check of claim C1 (check J10 of corpus/instruments/r42-closure.sh).
#   Source it from the suite; do not paste its body. The suite calls
#   check_j10 "$EXPORT" "$REF_RESOLVED" like every other check and reads ONE
#   payload line on stdout (exit 0 = closed, 1 = open).
#
#   The per-case directory grammar the suite must satisfy is specified in the
#   companion notes file ExecJ10Isolate.notes.txt. This file is the
#   enforcement: it checks the grammar by EXECUTION.
#
# WHAT J10 PROVES
#   The graded selftest of the suite must give every graded case a PRIVATE
#   fixture directory, and no case may read another case's fixture directory.
#   The limb proves both from the SYSCALL TRACE of the suite's own graded
#   selftest — never from the suite's own grading:
#
#     1. it runs the suite's graded selftest under strace in a private
#        sandbox (work root + scratch root outside the lane);
#     2. from the trace it learns, for every graded case <ID>:
#          - the private directories the case materialized (paths carrying a
#            component that matches <ID>),
#          - the case's execution window (first touch of an owned path until
#            the next case's window),
#          - every path the case READ or WROTE (a touch of another case's
#            fixture directory is a foreign touch),
#          - every path the case CREATED in the shared scratch root (the
#            per-case scratch baseline diff: a file outside the case's own
#            directory is a leak);
#     3. it diffs the shared scratch-root baseline before and after the run.
#
#   The suite's own selftest verdict is NOT trusted for any of this. A suite
#   that prints "verdict=pass" while a case reads a sibling's fixture is red
#   here; a suite that prints no graded line at all is red here.
#
# THE GRAMMAR (contract; prose in the notes file)
#   For every graded case <ID>:
#     - the case materializes its mutated copy under a private directory
#       whose path carries a component matching <ID> (the component is <ID>
#       itself, or <ID> followed by a non-alphanumeric character, e.g. "J07"
#       or "J07-fixture");
#     - the case reads no other case's fixture directory;
#     - the case writes nothing outside its own directory: a file that
#       appears in the shared scratch root during the case's window and is
#       not under the case's own directory is a leak;
#     - a suite that runs several cases in one process cannot attribute
#       reads per process, so the execution windows are used instead; the
#       payload says how many cases shared a process.
#
# KNOB (documented so wave-2 seats can point defeats at the live suite)
#   J10_NEST=1        leaf mode: this limb does NOT spawn the traced selftest
#                     (it prints nest=1 and exits 1, red by construction —
#                     the nested run never recurses). The limb sets it on the
#                     traced child.
#   J10_SUITE_REL     path of the suite inside the export tree
#                     (default corpus/instruments/r42-closure.sh)
#   J10_SUITE_ABS     absolute path of the suite to exercise; overrides
#                     J10_SUITE_REL. Used by this limb's own self-test.
#   J10_WORK          work root for the traced sandbox; defaults to the
#                     suite's $WORK, else to J10_SCRATCH_ROOT.
#   J10_SCRATCH_ROOT  scratch root for the traced sandbox; defaults to the
#                     suite's $SCRATCH_ROOT, else to J10_WORK.
#   J10_LANE          lane repository the traced child archives from;
#                     defaults to the suite's $LANE, else to the lane path.
#   J10_DETAIL        copy the per-case isolation detail (case directories,
#                     windows, every foreign touch and leak) to this path.
#
# EXIT CODES
#   0 closed   1 open (a red, never a vacuous green)   2 harness error
#
# The payload line is deterministic for a given export tree (counts only: no
# pids, no timestamps, no digests of volatile state), because the receipt
# check re-derives payload values — a varying payload would itself be a
# defect. The analysis is cached per (suite digest, ref) under the work root
# so the run phase and the selftest case do not pay for the traced selftest
# twice.

J10_VERSION=1
J10_MIN_CASES=2
J10_SUITE_REL_DEFAULT=corpus/instruments/r42-closure.sh

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

j10_log() { printf 'j10: %s\n' "$*" >&2; }

# j10_suite_path TREE -> absolute path of the suite to exercise
j10_suite_path() {
  local tree=${1:-}
  if [ -n "${J10_SUITE_ABS:-}" ]; then
    printf '%s\n' "$J10_SUITE_ABS"
    return 0
  fi
  local rel=${J10_SUITE_REL:-$J10_SUITE_REL_DEFAULT}
  [ -n "$tree" ] || { printf '\n'; return 0; }
  printf '%s/%s\n' "${tree%/}" "$rel"
}

# j10_snapshot DIR OUT -> sorted list of the entries below DIR, relative
j10_snapshot() {
  local dir=$1 out=$2
  : > "$out"
  [ -d "$dir" ] || return 0
  find "$dir" -mindepth 1 -printf '%P\n' 2>/dev/null | LC_ALL=C sort > "$out"
  return 0
}

# j10_diff_count A B -> number of entries in B that are not in A
j10_diff_count() {
  local a=$1 b=$2 n
  n=$(LC_ALL=C comm -13 "$a" "$b" 2>/dev/null | grep -c .)
  printf '%s\n' "${n:-0}"
}

# j10_collect_ids OUT_FILE RUNOUT -> the graded case ids the suite printed,
# one per line. The suite's own graded lines are the only source: a suite
# that prints no graded line has no graded selftest to isolate.
j10_collect_ids() {
  local out=$1 runout=$2
  : > "$out"
  [ -f "$runout" ] || return 0
  sed -n 's/^selftest case=\([^ ]*\).*/\1/p' "$runout" >> "$out"
  LC_ALL=C sort -u "$out" -o "$out"
}

# ---------------------------------------------------------------------------
# the trace analyzer (python3; written into the sandbox at run time)
# ---------------------------------------------------------------------------

j10_write_analyzer() {
  cat > "$1" <<'J10PY'
"""Isolation analyzer for the graded selftest (final).

Reads the strace log of the suite's graded selftest and reports whether the
graded selftest kept its cases isolated. Four properties, all observed from
the syscall trace; none is taken from a report the suite writes about itself:

  G1  private fixture dir   every graded case <ID> materialized a directory
                            whose basename is <ID> (case-insensitively), all
                            under one per-case root, pairwise disjoint.
  G2  no cross-case read    inside a case's window, no path under another
                            case's directory was read.
  G3  no leak               inside a case's window, nothing was created in the
                            shared scratch root outside the case's directory
                            (the per-case scratch baseline diff).
  G4  exercised             the case's own directory was read inside its
                            window.

A case's window opens at the creation of its directory and closes at the
creation of the next case's directory; the last window closes at that case's
last access to its own directory. Suite bookkeeping (export extraction,
transcript assembly) falls outside every window and is not attributed.

Relative paths are resolved against a per-pid working directory tracked from
chdir()/fchdir(): coreutils `mkdir -p` chdir's into each component, so a trace
read literally would mis-place every directory it creates.

Usage: analyze.py TRACE EXPECTEDIDS WORKROOT SCRATCHROOT DETAIL
Prints: cases= found= missing= shared= foreign= leaks= unused= windows=
        mode=
"""
import os
import re
import sys

TRACE, EXPECTED, WORKROOT, SCRATCHROOT, DETAIL = sys.argv[1:6]
WORKROOT = WORKROOT.rstrip("/")
SCRATCHROOT = SCRATCHROOT.rstrip("/")

Q = re.compile(r'"((?:[^"\\]|\\.)*)"')
CLONE = re.compile(r"^(clone3?|fork|vfork)\(")
OPEN = re.compile(r"^(open|openat|openat2|creat)\(")
MKDIR = re.compile(r"^mkdir(at)?\(")
CHDIR = re.compile(r"^(chdir|fchdir)\(")
EXEC = re.compile(r"^execve\(")
WRITE = re.compile(r"^write\(")
VERDICT = re.compile(r"selftest case=([A-Za-z0-9_]+)")
STATLIKE = re.compile(
    r"^(stat|statx|lstat|newfstatat|access|faccessat|readlink|faccessat2)\(")
MUTATE = re.compile(
    r"^(rename|renameat|renameat2|unlink|unlinkat|symlink|symlinkat|link|"
    r"linkat|truncate|ftruncate|chmod|fchmod|chown|fchown)\(")


def read_ids(path):
    ids = []
    try:
        with open(path, "r", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line and line not in ids:
                    ids.append(line)
    except OSError:
        pass
    return ids


# --- parse the trace, resolving relative paths per pid ----------------------
events = []
parents = {}
cwd = {}
verdict_idx = {}
pid_re = re.compile(r"^(\d+)\s+(.*)$")


def resolve(pid, path):
    """Absolute form of a trace path argument."""
    if not path:
        return ""
    if path.startswith("/"):
        return path
    base = cwd.get(pid)
    if base is None:
        return ""
    if path == ".":
        return base
    return os.path.normpath(os.path.join(base, path))


def set_cwd(pid, path):
    abs_path = resolve(pid, path)
    if abs_path:
        cwd[pid] = abs_path


with open(TRACE, "r", errors="replace") as fh:
    for raw in fh:
        m = pid_re.match(raw)
        if not m:
            continue
        pid = int(m.group(1))
        rest = m.group(2).strip()
        if rest.startswith("---") or rest.startswith("+++"):
            continue
        idx = len(events)
        if CLONE.match(rest):
            mm = re.search(r"=\s*(\d+)\s*$", rest)
            if mm:
                child = int(mm.group(1))
                parents[child] = pid
                if pid in cwd:
                    cwd[child] = cwd[pid]
            continue
        if EXEC.match(rest):
            q = Q.findall(rest)
            events.append((idx, pid, "exec", q[0] if q else ""))
            continue
        if WRITE.match(rest):
            mv = VERDICT.search(" ".join(Q.findall(rest)))
            if mv:
                verdict_idx.setdefault(mv.group(1), idx)
            continue
        q = Q.findall(rest)
        raw_path = q[0] if q else ""
        if CHDIR.match(rest):
            # fchdir takes an fd; only chdir carries a path
            if rest.startswith("chdir(") and raw_path:
                set_cwd(pid, raw_path)
            continue
        if not raw_path:
            if OPEN.match(rest) or MKDIR.match(rest) or STATLIKE.match(rest):
                # a directory-fd form we cannot resolve: ignore it
                pass
            continue
        path = resolve(pid, raw_path)
        if not path:
            continue
        if OPEN.match(rest):
            if re.search(r"O_CREAT|O_TRUNC", rest):
                kind = "create"
            elif re.search(r"O_WRONLY|O_RDWR|O_APPEND", rest):
                kind = "write"
            elif re.search(r"O_DIRECTORY", rest):
                kind = "readdir"
            else:
                kind = "read"
            events.append((idx, pid, kind, path))
            continue
        if MKDIR.match(rest):
            events.append((idx, pid, "create", path))
            continue
        if MUTATE.match(rest):
            events.append((idx, pid, "create", path))
            for extra in q[1:]:
                epath = resolve(pid, extra)
                if epath:
                    events.append((idx, pid, "create", epath))
            continue
        if STATLIKE.match(rest):
            if re.search(r"S_IFREG", rest):
                events.append((idx, pid, "read", path))
            else:
                events.append((idx, pid, "readstat", path))
            continue

IDS = read_ids(EXPECTED)
n_expected = len(IDS)

# --- G1: the per-case private paths -----------------------------------------
# A path belongs to case <ID> when one of its components is <ID> itself or
# <ID> followed by a non-alphanumeric separator ("J7", "J7-fixture",
# "I1-evidence"). The component boundary keeps "J1" from claiming "J10".
def id_of_component(comp):
    low = comp.lower()
    best = None
    for cid in IDS:
        c = cid.lower()
        if low == c:
            return cid
        if low.startswith(c) and len(low) > len(c) and not low[len(c)].isalnum():
            if best is None or len(cid) > len(best):
                best = cid
    return best


def prefix_of(path):
    parts = path.split("/")
    for i, comp in enumerate(parts):
        cid = id_of_component(comp)
        if cid:
            return cid, "/".join(parts[:i + 1])
    return None, None


case_dirs = {}          # case id -> set of private path prefixes
for idx, _pid, kind, path in events:
    if kind != "create":
        continue
    if not path.startswith(WORKROOT + "/"):
        continue
    cid, pref = prefix_of(path)
    if cid and pref:
        case_dirs.setdefault(cid, set()).add(pref)

found = [c for c in IDS if c in case_dirs]
missing = [c for c in IDS if c not in case_dirs]
shared = 0
claims = {}
for cid, prefixes in case_dirs.items():
    for d in prefixes:
        claims.setdefault(d, set()).add(cid)
for d, cids in claims.items():
    if len(cids) > 1:
        shared += len(cids) - 1


def case_of_path(path):
    best = None
    best_len = -1
    for cid, prefixes in case_dirs.items():
        for d in prefixes:
            if (path == d or path.startswith(d + "/")) and len(d) > best_len:
                best = cid
                best_len = len(d)
    return best


def own_path(cid, path):
    for d in case_dirs.get(cid, ()):
        if path == d or path.startswith(d + "/"):
            return True
    return False


# --- the execution windows --------------------------------------------------
create_idx = {}
last_own_idx = {}
case_pids = {}
for idx, pid, kind, path in events:
    cid = case_of_path(path)
    if cid is None:
        continue
    if kind == "create" and cid not in create_idx:
        create_idx[cid] = idx
    last_own_idx[cid] = idx
    case_pids.setdefault(cid, set()).add(pid)

# A case's window is the span of its own execution: bounded on the left by the
# previous case's verdict write (the point at which that case finished) and on
# the right by its own verdict write. A case whose fixture was created before
# the previous case's verdict was therefore materialized outside its own
# execution and cannot be attributed at all: it is reported as precreated.
vorder = sorted((verdict_idx[c], c) for c in verdict_idx if c in case_dirs)
windows = {}
precreated = 0
# A suite may print every graded line at the very end (the transcript is
# assembled once); then the verdict writes carry no per-case timing and the
# windows have to come from the fixture-creation order instead. A suite that
# writes each verdict as its case finishes gives exact per-case bounds.
bulk = bool(vorder) and bool(create_idx) and \
    min(v for v, _c in vorder) > max(create_idx.values())
if bulk or not vorder:
    order = sorted((create_idx[c], c) for c in create_idx)
    for pos, (start, cid) in enumerate(order):
        if pos + 1 < len(order):
            end = order[pos + 1][0]
        else:
            end = last_own_idx.get(cid, start) + 1
        windows[cid] = (start, max(end, start + 1))
else:
    prev_v = None
    for v, cid in vorder:
        start = create_idx.get(cid, prev_v or 0)
        if prev_v is not None and start < prev_v:
            start = prev_v
        if prev_v is not None and create_idx.get(cid, prev_v) < prev_v:
            precreated += 1
        windows[cid] = (start, max(v, start + 1))
        prev_v = v


def acting_case(idx):
    best = None
    for cid, (start, end) in windows.items():
        if idx >= start and idx < end:
            if best is None or start >= windows[best][0]:
                best = cid
    return best


# a case with its own process is a stronger arrangement than one sharing a
# process; report which one this suite gives
pid_cases = {}
for cid, pids in case_pids.items():
    for p in pids:
        pid_cases.setdefault(p, set()).add(cid)
mode = "proc"
for _p, cs in pid_cases.items():
    if len(cs) > 1:
        mode = "shared"
        break

# --- G2, G3, G4 -------------------------------------------------------------
foreign = 0
leaks = 0
read_own = set()
detail = []
for idx, _pid, kind, path in events:
    if not path.startswith("/"):
        continue
    act = acting_case(idx)
    if act is None:
        continue
    owner = case_of_path(path)
    if owner is not None and owner != act:
        if kind in ("read", "readdir", "readstat"):
            # G2: the acting case touched another case's fixture directory
            foreign += 1
            detail.append("foreign case=%s other=%s op=%s path=%s"
                          % (act, owner, kind, path))
        continue
    if owner == act:
        # G4: only a real file read exercises the fixture; the directory open
        # that mkdir -p performs is not evidence that the case used its copy
        if kind == "read" and path not in case_dirs.get(act, ()):
            read_own.add(act)
        continue
    if kind in ("create", "write") and not own_path(act, path):
        if path.startswith(SCRATCHROOT + "/"):
            # G3: a file appeared in the shared scratch root that does not
            # belong to the case that was running
            leaks += 1
            detail.append("leak case=%s op=%s path=%s" % (act, kind, path))

unused = len([c for c in found if c not in read_own])

if DETAIL:
    try:
        with open(DETAIL, "w", errors="replace") as fh:
            for cid in sorted(windows, key=lambda c: windows[c][0]):
                start, end = windows[cid]
                fh.write("case=%s dirs=%s window=%s..%s read-own=%s\n"
                         % (cid, ",".join(sorted(case_dirs.get(cid, ()))),
                            start, end,
                            "yes" if cid in read_own else "no"))
            for line in detail:
                fh.write(line + "\n")
    except OSError:
        pass

print("cases=%d found=%d missing=%d shared=%d precreated=%d foreign=%d "
      "leaks=%d unused=%d windows=%d mode=%s" % (
          n_expected, len(found), len(missing), shared, precreated, foreign,
          leaks, unused, len(windows), mode))
J10PY
}

# ---------------------------------------------------------------------------
# the check
# ---------------------------------------------------------------------------

# check_j10 TREE REF -> payload on stdout; exit 0 closed, 1 open
check_j10() {
  local tree=${1:-} ref=${2:-}
  (
    set -uo pipefail

    local payload0='cases=0,found=0,missing=0,shared=0,precreated=0,unused=0,foreign=0,leaks=0,windows=0,mode=none,scratch-added=0'

    if [ "${J10_NEST:-0}" -ge 1 ]; then
      printf 'nest=1,%s\n' "$payload0"
      exit 1
    fi

    local suite work scratch lane
    suite=$(j10_suite_path "$tree")
    if [ -z "$suite" ] || [ ! -f "$suite" ]; then
      printf 'suite=0,%s\n' "$payload0"
      exit 1
    fi

    if ! command -v strace >/dev/null 2>&1; then
      printf 'tracer=0,%s\n' "$payload0"
      exit 1
    fi

    work=${J10_WORK:-${WORK:-}}
    scratch=${J10_SCRATCH_ROOT:-${SCRATCH_ROOT:-}}
    if [ -z "$work" ] || [ -z "$scratch" ]; then
      printf 'sandbox=0,%s\n' "$payload0"
      exit 1
    fi

    # the analysis is a pure function of (suite bytes, ref): cache it so the
    # run phase and the selftest case pay for the traced selftest once
    local key cache
    key=$(sha256sum -- "$suite" 2>/dev/null | cut -d' ' -f1)
    key="${key:0:16}-${ref:-noref}"
    cache="$work/j10-cache/$key"
    mkdir -p -- "$work/j10-cache" 2>/dev/null || true
    if [ -f "$cache.payload" ]; then
      cat -- "$cache.payload"
      exit "$(cat -- "$cache.rc" 2>/dev/null || printf 1)"
    fi

    local sbx="$work/j10-sandbox" sbs="$scratch/j10-$$"
    rm -rf -- "$sbx" "$sbs"
    mkdir -p -- "$sbx/work" "$sbs" || {
      printf 'sandbox=0,%s\n' "$payload0"
      exit 1
    }
    trap 'rm -rf -- "$sbx" "$sbs"' EXIT

    local trace="$sbx/trace.log" runout="$sbx/run.out" runerr="$sbx/run.err"
    local ids="$sbx/ids.txt" detail="$sbx/isolation-detail.txt"

    j10_snapshot "$scratch" "$sbx/scratch.before"

    lane=${J10_LANE:-${LANE:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}}

    # the traced graded selftest of the suite under test. J10_NEST=1 on the
    # child keeps the recursion finite: the child's own check_j10 is red by
    # construction and does not spawn a second traced run.
    local args=(--selftest --export-ref "$ref" --work "$sbx/work" --scratch-root "$sbs" --lane "$lane")
    J10_NEST=1 strace -f -qq -s 512 \
      -e trace=openat,open,creat,mkdir,mkdirat,chdir,rename,renameat,unlink,unlinkat,clone,clone3,fork,vfork,execve,write \
      -o "$trace" -- bash "$suite" "${args[@]}" > "$runout" 2> "$runerr"
    local rc=$?
    if [ "$rc" -ge 2 ] && grep -qiE 'unknown option|unrecognized option|illegal option' "$runerr"; then
      args=(--selftest --export-ref "$ref" --work "$sbx/work" --scratch-root "$sbs")
      J10_NEST=1 strace -f -qq -s 512 \
        -e trace=openat,open,creat,mkdir,mkdirat,chdir,rename,renameat,unlink,unlinkat,clone,clone3,fork,vfork,execve,write \
        -o "$trace" -- bash "$suite" "${args[@]}" > "$runout" 2> "$runerr"
      rc=$?
    fi

    if [ ! -s "$trace" ]; then
      printf 'tracer=failed,%s\n' "$payload0"
      exit 1
    fi

    j10_collect_ids "$ids" "$runout"
    j10_write_analyzer "$sbx/analyze.py"

    local summary
    summary=$(python3 "$sbx/analyze.py" "$trace" "$ids" "$sbx/work" "$sbs" \
      "$detail" 2>/dev/null)
    if [ -z "$summary" ]; then
      printf 'analysis=failed,%s\n' "$payload0"
      exit 1
    fi

    j10_snapshot "$scratch" "$sbx/scratch.after"
    local added
    added=$(j10_diff_count "$sbx/scratch.before" "$sbx/scratch.after")

    local n_cases found missing shared precreated unused foreign leaks windows mode
    n_cases=$(printf '%s\n' "$summary" | sed -n 's/.*\bcases=\([0-9]*\).*/\1/p')
    found=$(printf '%s\n' "$summary" | sed -n 's/.*\bfound=\([0-9]*\).*/\1/p')
    missing=$(printf '%s\n' "$summary" | sed -n 's/.*\bmissing=\([0-9]*\).*/\1/p')
    unused=$(printf '%s\n' "$summary" | sed -n 's/.*\bunused=\([0-9]*\).*/\1/p')
    foreign=$(printf '%s\n' "$summary" | sed -n 's/.*\bforeign=\([0-9]*\).*/\1/p')
    leaks=$(printf '%s\n' "$summary" | sed -n 's/.*\bleaks=\([0-9]*\).*/\1/p')
    windows=$(printf '%s\n' "$summary" | sed -n 's/.*\bwindows=\([0-9]*\).*/\1/p')
    shared=$(printf '%s\n' "$summary" | sed -n 's/.*\bshared=\([0-9]*\).*/\1/p')
    precreated=$(printf '%s\n' "$summary" | sed -n 's/.*\bprecreated=\([0-9]*\).*/\1/p')
    mode=$(printf '%s\n' "$summary" | sed -n 's/.*\bmode=\([A-Za-z]*\).*/\1/p')

    local payload
    payload="cases=${n_cases:-0},found=${found:-0},missing=${missing:-0},shared=${shared:-0},precreated=${precreated:-0},unused=${unused:-0},foreign=${foreign:-0},leaks=${leaks:-0},windows=${windows:-0},mode=${mode:-none},scratch-added=${added:-0}"

    local out=1
    if [ "${n_cases:-0}" -ge "$J10_MIN_CASES" ] && \
       [ "${missing:-1}" -eq 0 ] && \
       [ "${shared:-1}" -eq 0 ] && \
       [ "${precreated:-1}" -eq 0 ] && \
       [ "${unused:-1}" -eq 0 ] && \
       [ "${foreign:-1}" -eq 0 ] && \
       [ "${leaks:-1}" -eq 0 ]; then
      out=0
    fi

    if [ -n "${J10_DETAIL:-}" ] && [ -f "$detail" ]; then
      cp -- "$detail" "$J10_DETAIL" 2>/dev/null || true
    fi

    printf '%s\n' "$payload" > "$cache.payload" 2>/dev/null || true
    printf '%s\n' "$out" > "$cache.rc" 2>/dev/null || true

    printf '%s\n' "$payload"
    exit "$out"
  )
}
