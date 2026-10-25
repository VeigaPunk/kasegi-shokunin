#!/usr/bin/env python3
"""anchorcheck.py — kasegi anchor gate (r18; r15 version in git history at eb5b590).

Verify every `path:NN[-MM]` citation in a markdown file against its declared
base, print the cited source line(s) for semantic review, and keep the verdict
classes SEPARATE (round-16 critic ruling: never collapse them into one
"passed" count):

  IN-RANGE          mirror-based cite, anchor inside the mirror file
  IN-RANGE(LANE)    lane-based cite, anchor in range
  IN-RANGE(ORIGIN)  explicit ORIGIN-WORK cite, checked against current bytes
  IN-RANGE(PIN)     cite verified against a pinned git blob
  MISSING-FILE      no file at any declared base (bad)
  PAST-EOF          file exists at the base but the anchor is out of range (bad)
  OUTSIDE-BASE      explicit ORIGIN-WORK or MIRROR-ABSOLUTE path escapes its root (bad)
  PIN-BROKEN        a pin was declared but the git object does not exist (bad)
  LOST-RECORDED     token prefixed `[lost-tree] ` or `[lost-base] ` inside the backticks:
                    deliberately non-openable historical anchor; reported and
                    counted separately, NOT checked, never counted as validated

Bases, in precedence order:
(c) blob pin: a plain (never backticked) HTML comment in the checked file,
    exact form:  <!-- pin: <relpath.md|.mjs|.json|.sh> <7-40 hex> -->
    registers a pin; cites of that relpath verify against
    `git show <hash>:<relpath>` in the lane repo.
(d) ORIGIN-WORK: only the explicit
    `~/Projects/origin-work/open-bug-bounties/` prefix is accepted; the checked
    base is `$KASEGI_ORIGIN_ROOT` else the first existing of
    `~/Projects/origin-work/open-bug-bounties`, `~/Projects/open-bug-bounties`.
    An absent base reports BASE-ABSENT (own verdict, not bad). Real paths
    must remain under that root; the check reads current bytes and does not
    establish that a mutable source file is tracked or durably pinned.
(a) lane base: bare `name.ext` cites search lane dirs first; any relative
    path containing `/` (including `corpus/`, `claims/`, `evidence/`,
    `.ufo/`, `submit/`, `receipts/` prefixes and `csv`/`jsonl`/`rst`/`txt`/
    `py`/`ts` extensions) is tried lane-root-relative.
(f) MIRROR-ABSOLUTE: the explicit `~/Projects/the-bounty-hunter/` prefix is
    confined to the mirror base `$KASEGI_MIRROR` else the first existing of
    `~/Projects/the-bounty-hunter`, `~/Projects/origin-work/the-bounty-hunter`,
    exactly like ORIGIN-WORK; violations classify OUTSIDE-BASE, absent base
    BASE-ABSENT.
(e) unprefixed mirror names: a cite not found in the lane is tried under the
    mirror subdirs (ops, docs, bin, fleets, bounty-map, .omp), then at the
    mirror root. Lost-tree paths under prefixes like `claims/` or `docs/`
    therefore classify BASE-ABSENT (mirror gone since 2026-10-14) until marked
    `[lost-tree]`; before the loss they classified MISSING-FILE. Mirror root:
    `~/Projects/the-bounty-hunter` (frozen 2026-09-05, HEAD `1cfbd86`; ABSENT
    on this host since the 2026-10-12 restructure — no relocated copy found).

Lane root: env KASEGI_LANE_ROOT, else the nearest ancestor of the checked file
containing SKILL.md or .git.

Range-valid is a mechanical verdict; SEMANTIC validity (does the cited line
support the claim?) is a separate manual/L2 review — the printed source lines
are its input. Re-check cadence (r16 rule, instruments/README.md): run after
every edit to any cited lane file and at every round close.

Summary line is greppable, one per file:
== <src>: N in-range cite instances, M bad; K distinct anchors; LOST-RECORDED=L PIN-BROKEN=P ORIGIN=O OUTSIDE-BASE=X BASE-ABSENT=B
(bad = MISSING-FILE + PAST-EOF + OUTSIDE-BASE; BASE-ABSENT and LOST-RECORDED are
explicit recorded-loss verdicts, not bad.)

Usage: python3 anchorcheck.py <file.md>
"""
import re, sys, os, subprocess

# Round-19 re-census (2026-10-14): both surviving domain roots went ABSENT —
# the 2026-09-28 event took `~/Projects/bounties`; this event removed
# `~/Projects/the-bounty-hunter` and the whole `~/Projects/origin-work` tree
# (no relocated copy found under ~). Roots are now DERIVED, never hardcoded:
# $KASEGI_MIRROR / $KASEGI_ORIGIN_ROOT win, else the first existing candidate,
# else the canonical (absent) path so the failure names the expected base.
# A citation into an absent base reports BASE-ABSENT (its own verdict, like
# LOST-RECORDED) instead of a misleading MISSING-FILE.
_MIRROR_CANDIDATES = (
    os.path.expanduser('~/Projects/the-bounty-hunter'),
    os.path.expanduser('~/Projects/origin-work/the-bounty-hunter'),
)
_ORIGIN_CANDIDATES = (
    os.path.expanduser('~/Projects/origin-work/open-bug-bounties'),
    os.path.expanduser('~/Projects/open-bug-bounties'),
)

def _derive_root(env_name, candidates):
    override = os.environ.get(env_name)
    if override:
        return os.path.expanduser(override)
    for c in candidates:
        if os.path.isdir(c):
            return c
    return candidates[0]

MIRROR = _derive_root('KASEGI_MIRROR', _MIRROR_CANDIDATES)
MIRROR_ABSENT = not os.path.isdir(MIRROR)
MIRROR_CITE_PREFIX = '~/Projects/the-bounty-hunter/'
ORIGIN_CITE_PREFIX = '~/Projects/origin-work/open-bug-bounties/'
ORIGIN_ROOT = _derive_root('KASEGI_ORIGIN_ROOT', _ORIGIN_CANDIDATES)
ORIGIN_ABSENT = not os.path.isdir(ORIGIN_ROOT)
LANE = os.environ.get('KASEGI_LANE_ROOT')
LANE_DIRS = ('.', 'corpus/knowledge', 'corpus/lessons', 'corpus/instruments')
TOK = re.compile(r"`([^`\n]+)`")
PIN = re.compile(r"<!--\s*pin:\s*([\w./-]+\.(?:mjs|json|md|sh))\s+([0-9a-f]{7,40})\s*-->")
LOST = re.compile(r"^\[lost-(?:tree|base)\]\s+(.*)$")
CITE = re.compile(r"^((?:~/Projects/origin-work/open-bug-bounties/[\w./-]+\.(?:mjs|sh|json|md|csv|jsonl|txt)|~/Projects/the-bounty-hunter/[\w./-]+\.(?:mjs|sh|json|md|csv|jsonl|txt)|(?:corpus|ops|fleets|docs|bin|bounty-map|\.omp|claims|evidence|submit|vdp-disclosures|ledger|\.ufo|receipts|raw)/[\w./-]+\.(?:mjs|sh|json|md|csv|jsonl|rst|txt|py|ts)|[\w.-]+\.(?:mjs|json|sh|md|csv|jsonl|rst|txt))):(\d+)(?:-(\d+))?$")


def find_lane_root(src):
    if LANE:
        return os.path.abspath(LANE)
    d = os.path.dirname(os.path.abspath(src))
    while d != '/':
        if os.path.exists(os.path.join(d, 'SKILL.md')) or os.path.isdir(os.path.join(d, '.git')):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.abspath(src))


def git_show(repo, obj, path, a, b):
    """Return ('MISSING','') | ('RANGE', note) | ('OK', text)."""
    p = subprocess.run(['git', '-C', repo, 'show', f'{obj}:{path}'],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return ('MISSING', '')
    lines = p.stdout.split('\n')
    if b > len(lines) or a < 1 or b < a:
        return ('RANGE', f'pinned blob has {len(lines)} lines')
    return ('OK', ' ⏎ '.join(x.strip()[:100] for x in lines[a-1:b]))


_EXIT1 = 0
def main(argv):
    global _EXIT1
    src = argv[0]
    lane_root = find_lane_root(src)
    # pass 1: collect blob pins (last pin per relpath wins)
    pins = {}
    for line in open(src):
        m = PIN.search(line)
        if m:
            pins[m.group(1)] = m.group(2)
    kinds = {}          # verdict -> count
    seen = {}           # distinct anchors
    per = []            # per-cite report lines
    for ln, line in enumerate(open(src), 1):
        for tok in TOK.findall(line):
            lost = False
            t = tok.strip().rstrip('.,;:')  # trailing prose punct only; leading '.' is significant (.ufo, .omp)
            mlost = LOST.match(t)
            if mlost:
                lost = True
                t = mlost.group(1).strip()
            m = CITE.match(t)
            if not m:
                continue
            rel, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            verdict = None; txt = None; kind = 'PIN'; path = None; pin_note = ''; outside_root = None
            # (c) pinned blob first
            if rel in pins:
                st, out = git_show(lane_root, pins[rel], rel, a, b)
                if st == 'MISSING':
                    verdict = 'PIN-BROKEN'
                elif st == 'RANGE':
                    verdict = 'PAST-EOF'; pin_note = out
                else:
                    verdict = 'IN-RANGE(PIN)'; txt = out
            if verdict is None:
                if rel.startswith(ORIGIN_CITE_PREFIX):
                    origin_root = os.path.realpath(ORIGIN_ROOT)
                    path = os.path.realpath(os.path.join(origin_root, rel[len(ORIGIN_CITE_PREFIX):]))
                    try:
                        within_origin = os.path.commonpath((origin_root, path)) == origin_root
                    except ValueError:
                        within_origin = False
                    if not within_origin:
                        outside_root = origin_root; verdict = 'OUTSIDE-BASE'
                    elif ORIGIN_ABSENT:
                        verdict = 'BASE-ABSENT'
                    elif not os.path.isfile(path):
                        verdict = 'MISSING-FILE'
                    else:
                        kind = 'ORIGIN'
                elif rel.startswith(MIRROR_CITE_PREFIX):
                    mirror_root = os.path.realpath(MIRROR)
                    path = os.path.realpath(os.path.join(mirror_root, rel[len(MIRROR_CITE_PREFIX):]))
                    try:
                        within_mirror = os.path.commonpath((mirror_root, path)) == mirror_root
                    except ValueError:
                        within_mirror = False
                    if not within_mirror:
                        outside_root = mirror_root; verdict = 'OUTSIDE-BASE'
                    elif MIRROR_ABSENT:
                        verdict = 'BASE-ABSENT'
                    elif not os.path.isfile(path):
                        verdict = 'MISSING-FILE'
                    else:
                        kind = 'MIRROR'
                else:
                    # (a) lane-base resolution
                    cands = []
                    if '/' not in rel:
                        for d in LANE_DIRS:
                            cands.append(os.path.join(lane_root, d, rel))
                    else:
                        cands.append(os.path.join(lane_root, rel))
                    lane_path = next((c for c in cands if os.path.exists(c)), None)
                    if lane_path:
                        path = lane_path; kind = 'LANE'
                    elif '/' not in rel:
                        # (e) unprefixed mirror name: fixed subdir order
                        kind = 'MIRROR'
                        for d in ('ops', 'docs', 'bin', 'fleets', 'bounty-map', '.omp'):
                            c2 = os.path.join(MIRROR, d, rel)
                            if os.path.exists(c2):
                                path = c2; break
                        if path is None:
                            path = os.path.join(MIRROR, rel)
                    else:
                        path = os.path.join(MIRROR, rel); kind = 'MIRROR'
            if verdict is None:
                if not os.path.exists(path):
                    verdict = ('BASE-ABSENT' if (kind == 'MIRROR' and MIRROR_ABSENT)
                               else 'MISSING-FILE')
                else:
                    n = sum(1 for _ in open(path, errors='replace'))
                    if b > n or a < 1 or b < a:
                        verdict = 'PAST-EOF'
                    else:
                        lines = open(path, errors='replace').read().split('\n')
                        txt = ' ⏎ '.join(x.strip()[:100] for x in lines[a-1:b])
                        verdict = 'IN-RANGE(ORIGIN)' if kind == 'ORIGIN' else (
                            'IN-RANGE(LANE)' if kind == 'LANE' else 'IN-RANGE')
            # classify into report buckets
            if lost:
                kinds['LOST-RECORDED'] = kinds.get('LOST-RECORDED', 0) + 1
                per.append(f"LOST-RECORDED md:{ln} {tok} (not checked)")
                continue
            if verdict == 'PIN-BROKEN':
                kinds['PIN-BROKEN'] = kinds.get('PIN-BROKEN', 0) + 1
                per.append(f"PIN-BROKEN md:{ln} {tok} (git object missing: {pins.get(rel)})")
                continue
            if verdict == 'BASE-ABSENT':
                kinds['BASE-ABSENT'] = kinds.get('BASE-ABSENT', 0) + 1
                per.append(f"BASE-ABSENT md:{ln} {tok} (base tree absent: {path})")
                continue
            if verdict == 'OUTSIDE-BASE':
                kinds['OUTSIDE-BASE'] = kinds.get('OUTSIDE-BASE', 0) + 1
                per.append(f"OUTSIDE-BASE md:{ln} {tok} (resolved outside {outside_root})")
                continue
            if verdict == 'MISSING-FILE':
                kinds['MISSING-FILE'] = kinds.get('MISSING-FILE', 0) + 1
                per.append(f"MISSING-FILE md:{ln} {tok}")
                continue
            if verdict == 'PAST-EOF':
                if path is not None:
                    n = sum(1 for _ in open(path, errors='replace'))
                    note = f'file has {n} lines'
                else:
                    note = pin_note or 'out of range'
                kinds['PAST-EOF'] = kinds.get('PAST-EOF', 0) + 1
                per.append(f"PAST-EOF md:{ln} {tok} ({note})")
                continue
            kinds[verdict] = kinds.get(verdict, 0) + 1
            per.append(f"OK md:{ln} {tok}  [{txt if txt else ''}]")
            key = (rel, a, b, kind)
            if key not in seen:
                seen[key] = txt or ''
    # bad verdicts first (greppable), then summary, then the OK detail
    for line in per:
        if line.startswith(('MISSING-FILE', 'PAST-EOF', 'PIN-BROKEN', 'OUTSIDE-BASE')):
            print(line)
    inp = sum(v for k2, v in kinds.items() if k2.startswith('IN-RANGE'))
    bad = sum(kinds.get(k, 0) for k in ('MISSING-FILE', 'PAST-EOF', 'OUTSIDE-BASE'))
    _EXIT1 = 1 if bad else 0
    print(f"\n== {src}: {inp} in-range cite instances, "
          f"{bad} bad; "
          f"{len(seen)} distinct anchors; "
          f"LOST-RECORDED={kinds.get('LOST-RECORDED', 0)} PIN-BROKEN={kinds.get('PIN-BROKEN', 0)} "
          f"ORIGIN={kinds.get('IN-RANGE(ORIGIN)', 0)} OUTSIDE-BASE={kinds.get('OUTSIDE-BASE', 0)} "
          f"BASE-ABSENT={kinds.get('BASE-ABSENT', 0)}")
    for line in per:
        if not line.startswith(('MISSING-FILE', 'PAST-EOF', 'PIN-BROKEN', 'OUTSIDE-BASE')):
            print(line)


if __name__ == '__main__':
    r = main(sys.argv[1:]); sys.exit(r if r is not None else _EXIT1)
