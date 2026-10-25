#!/usr/bin/env python3
"""anchorcheck.py — kasegi anchor gate (r28; r18 version in git history at c9f8b11;
r15 version at eb5b590).

Verify every backticked `path:NN[-MM]` citation in a markdown file against its
declared base, print the cited source line(s) for semantic review, and keep the
verdict classes SEPARATE (round-16 critic ruling: never collapse them into one
"passed" count):

  IN-RANGE          mirror-based cite, anchor inside the mirror file (a
                    BOUNTIES-PROVINCE cite that resolves in range also reports
                    plain IN-RANGE, like MIRROR)
  IN-RANGE(LANE)    lane-based cite, anchor in range
  IN-RANGE(ORIGIN)  explicit ORIGIN-WORK cite, checked against current bytes
  IN-RANGE(PIN)     cite verified against a pinned git blob
  MISSING-FILE      no file at any declared base (fail)
  PAST-EOF          file exists at the base but the anchor is out of range (fail)
  OUTSIDE-BASE      explicit ORIGIN-WORK, MIRROR-ABSOLUTE or BOUNTIES-PROVINCE
                    path escapes its root (fail)
  PIN-BROKEN        a pin was declared but the git object does not exist (fail)
  BOUNTIES-ABSENT   BOUNTIES-PROVINCE cite whose `~/Projects/bounties` base is
                    absent (fail). Round-28 arm: before it, such a cite was not
                    matched by CITE at all and was silently skipped.
  LOST-RECORDED     token prefixed `[lost-tree] ` or `[lost-base] ` inside the backticks:
                    deliberately non-openable historical anchor; reported and
                    counted separately, NOT checked, never counted as validated,
                    NEVER a fail class

Exit status (round-28 fail-closed rule): 1 when any FAIL_CLASSES count is
nonzero — MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT,
BOUNTIES-ABSENT — else 0. LOST-RECORDED stays recorded-not-fail, so a file
whose only losses are marked lost citations still exits 0. Before r28 every
verdict class printed and exited 0 (round-25 routed debt).

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
(g) BOUNTIES-PROVINCE (round 28): only the explicit `~/Projects/bounties/`
    prefix is accepted; the checked base is `$KASEGI_BOUNTIES` else the
    canonical `~/Projects/bounties`, derived exactly like MIRROR/ORIGIN. Real
    paths must remain under that root (an escape classifies OUTSIDE-BASE); an
    absent root reports BOUNTIES-ABSENT — the fail-closed sibling of
    BASE-ABSENT, and a fail class (a lost-province cite that used to be
    invisible must not read as clean). The root was removed from the
    filesystem at 2026-09-28T23:51:31Z (source-tree-loss-2026-09-28.md).

Lane root: env KASEGI_LANE_ROOT, else the nearest ancestor of the checked file
containing SKILL.md or .git.

Range-valid is a mechanical verdict; SEMANTIC validity (does the cited line
support the claim?) is a separate manual/L2 review — the printed source lines
are its input. Re-check cadence (r16 rule, instruments/README.md): run after
every edit to any cited lane file and at every round close.

Summary line is greppable, one per file (spelling frozen since r18 so the
frozen counters keep parsing it; BOUNTIES-ABSENT is deliberately NOT a bucket
on it — the round-28 counter counts BOUNTIES-ABSENT verdict LINES and expects
exactly 1, and a `BOUNTIES-ABSENT=` bucket would make that 2):
== <src>: N in-range cite instances, M bad; K distinct anchors; LOST-RECORDED=L PIN-BROKEN=P ORIGIN=O OUTSIDE-BASE=X BASE-ABSENT=B
(bad = MISSING-FILE + PAST-EOF + OUTSIDE-BASE, the historical three-class
mechanical count, kept unchanged for receipt continuity. Exit status is broader
than `bad`: every count in FAIL_CLASSES drives it. LOST-RECORDED is recorded —
not bad, not fail.)

--selftest (round 28) builds one isolating fixture per FAIL_CLASSES limb, plus
a bounties in-range case, a marked-loss case and a clean control, all under a
fresh temp dir; per case it overrides KASEGI_LANE_ROOT / KASEGI_MIRROR /
KASEGI_ORIGIN_ROOT / KASEGI_BOUNTIES, so the absent-bases host still reaches
every limb (a present temp mirror reaches MISSING-FILE, a real temp file
reaches PAST-EOF, a temp `git init` repo supplies the broken pin, a present
temp bounties root reaches OUTSIDE-BASE and in-range, absent roots reach
BASE-ABSENT / BOUNTIES-ABSENT). It runs this file as a subprocess and asserts
each case's exact verdict-class counts and exit status. Prints
`selftest cases=N failures=0` and exits 0; on any mismatch it prints the
failing case and that case's stdout/stderr, and exits 1. No fixture reads or
writes the live tree.

Usage: python3 anchorcheck.py <file.md>
       python3 anchorcheck.py --selftest
"""
import re, sys, os, subprocess, tempfile, shutil

# Round-19 re-census (2026-10-14): both surviving domain roots went ABSENT —
# the 2026-09-28 event took `~/Projects/bounties`; this event removed
# `~/Projects/the-bounty-hunter` and the whole `~/Projects/origin-work` tree
# (no relocated copy found under ~). Roots are now DERIVED, never hardcoded:
# $KASEGI_MIRROR / $KASEGI_ORIGIN_ROOT win, else the first existing candidate,
# else the canonical (absent) path so the failure names the expected base.
# A citation into an absent base reports BASE-ABSENT (its own verdict, like
# LOST-RECORDED) instead of a misleading MISSING-FILE.
# Round-28: the bounties province is derived the same way ($KASEGI_BOUNTIES
# override, else the canonical `~/Projects/bounties`) and its absence is the
# FAIL class BOUNTIES-ABSENT, not the recorded BASE-ABSENT: an unmarked
# lost-province cite used to be invisible to CITE and therefore read clean.
_MIRROR_CANDIDATES = (
    os.path.expanduser('~/Projects/the-bounty-hunter'),
    os.path.expanduser('~/Projects/origin-work/the-bounty-hunter'),
)
_ORIGIN_CANDIDATES = (
    os.path.expanduser('~/Projects/origin-work/open-bug-bounties'),
    os.path.expanduser('~/Projects/open-bug-bounties'),
)
_BOUNTIES_CANDIDATES = (
    os.path.expanduser('~/Projects/bounties'),
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
BOUNTIES_CITE_PREFIX = '~/Projects/bounties/'
BOUNTIES_ROOT = _derive_root('KASEGI_BOUNTIES', _BOUNTIES_CANDIDATES)
BOUNTIES_ABSENT = not os.path.isdir(BOUNTIES_ROOT)
LANE = os.environ.get('KASEGI_LANE_ROOT')
LANE_DIRS = ('.', 'corpus/knowledge', 'corpus/lessons', 'corpus/instruments')
TOK = re.compile(r"`([^`\n]+)`")
PIN = re.compile(r"<!--\s*pin:\s*([\w./-]+\.(?:mjs|json|md|sh))\s+([0-9a-f]{7,40})\s*-->")
LOST = re.compile(r"^\[lost-(?:tree|base)\]\s+(.*)$")
# One alternation, one reader: CITE, matching a whole backticked token. The
# BOUNTIES-PROVINCE arm is a new explicit prefix; `[\w./-]+` admits `..`
# segments on purpose so a realpath escape is reachable and classifies
# OUTSIDE-BASE instead of failing to match (and so being silently ignored).
_CITE_PATH = (r"(?:"
              r"~/Projects/origin-work/open-bug-bounties/[\w./-]+\.(?:mjs|sh|json|md|csv|jsonl|txt)"
              r"|~/Projects/the-bounty-hunter/[\w./-]+\.(?:mjs|sh|json|md|csv|jsonl|txt)"
              r"|~/Projects/bounties/[\w./-]+\.(?:mjs|sh|json|md|csv|jsonl|txt)"
              r"|(?:corpus|ops|fleets|docs|bin|bounty-map|\.omp|claims|evidence|submit|vdp-disclosures|ledger|\.ufo|receipts|raw)/[\w./-]+\.(?:mjs|sh|json|md|csv|jsonl|rst|txt|py|ts)"
              r"|[\w.-]+\.(?:mjs|json|sh|md|csv|jsonl|rst|txt)"
              r")")
CITE = re.compile(r"^(" + _CITE_PATH + r"):(\d+)(?:-(\d+))?$")
# Round-28 fail-closed rule (round-25 routed debt): any nonzero count here makes
# the tool exit 1. LOST-RECORDED is deliberately absent — recorded, not fail.
FAIL_CLASSES = ('MISSING-FILE', 'PAST-EOF', 'OUTSIDE-BASE', 'PIN-BROKEN',
                'BASE-ABSENT', 'BOUNTIES-ABSENT')
# Verdict lines printed before the greppable summary (fail classes that carry a
# resolvable path or root; BASE-ABSENT prints after it, as since r19).
_PRINT_FIRST = ('MISSING-FILE', 'PAST-EOF', 'PIN-BROKEN', 'OUTSIDE-BASE',
                'BOUNTIES-ABSENT')


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


# ---- round-28 selftest: one isolating fixture per fail limb ------------------

def _counts(out):
    """Parse one run's stdout into {verdict class|'IN-RANGE': count}."""
    c = {k: 0 for k in FAIL_CLASSES}
    c['LOST-RECORDED'] = 0
    for line in out.splitlines():
        for k in c:
            if line.startswith(k + ' md:'):
                c[k] += 1
    m = re.search(r"(\d+) in-range cite instances", out)
    c['IN-RANGE'] = int(m.group(1)) if m else -1   # no summary line -> case fails
    return c


def _selftest():
    """One isolating fixture per FAIL_CLASSES limb, plus controls, in temp dirs.

    Each case runs this file as a subprocess with KASEGI_LANE_ROOT /
    KASEGI_MIRROR / KASEGI_ORIGIN_ROOT / KASEGI_BOUNTIES pointed at fresh temp
    roots, so a fixture reaches exactly one limb even on this host (where every
    real base is absent), and then asserts the COMPLETE verdict-class vector and
    the exit status. A fixture that trips a second limb, or a limb with no
    failing fixture, therefore shows up as a failure here.
    """
    zero = {k: 0 for k in FAIL_CLASSES}
    zero['LOST-RECORDED'] = 0
    zero['IN-RANGE'] = 0

    def want(**kw):
        w = dict(zero)
        w.update(kw)
        return w

    cases = []

    def add(name, fixture, expected, exit_code, absent=(), files=(), git_dir=None):
        cases.append(dict(name=name, fixture=fixture, expected=expected,
                          exit_code=exit_code, absent=absent, files=files,
                          git_dir=git_dir))

    # 1 MISSING-FILE — every base present, the cited file simply absent.
    add('missing-file',
        "Fabricated citation, no file at any present base: "
        "`corpus/knowledge/zz-selftest-absent.md:99`\n",
        want(**{'MISSING-FILE': 1}), 1)
    # 2 PAST-EOF — a real temp file, anchor beyond its last line.
    add('past-eof', "Existing lane file, anchor past EOF: `present.md:9`\n",
        want(**{'PAST-EOF': 1}), 1,
        files=(('lane', 'present.md', 'one\ntwo\nthree\n'),))
    # 3 OUTSIDE-BASE — bounties root present, the cite walks out of it.
    add('outside-base',
        "Bounties cite escaping its root: "
        "`~/Projects/bounties/../selftest-escape.md:1`\n",
        want(**{'OUTSIDE-BASE': 1}), 1)
    # 4 PIN-BROKEN — declared pin whose object id does not exist in the repo.
    add('pin-broken',
        "<!-- pin: pinned.md deadbeef -->\n"
        "Pinned cite whose blob does not exist: `pinned.md:1`\n",
        want(**{'PIN-BROKEN': 1}), 1, git_dir='lane')
    # 5 BASE-ABSENT — unprefixed mirror name with the mirror root absent.
    add('base-absent',
        "Unprefixed mirror name, mirror root absent: `zz-selftest-ops.mjs:1`\n",
        want(**{'BASE-ABSENT': 1}), 1, absent=('mirror',))
    # 6 BOUNTIES-ABSENT — bounties-prefixed cite with the bounties root absent.
    add('bounties-absent',
        "Bounties cite, bounties root absent: "
        "`~/Projects/bounties/ops/claim-check.mjs:96`\n",
        want(**{'BOUNTIES-ABSENT': 1}), 1, absent=('bounties',))
    # 7 bounties arm resolves (control) — the arm must not only fail closed.
    add('bounties-in-range',
        "Bounties cite inside a present root: "
        "`~/Projects/bounties/ops/claim-check.mjs:2`\n",
        want(**{'IN-RANGE': 1}), 0,
        files=(('bounties', 'ops/claim-check.mjs', 'alpha\nbeta\ngamma\n'),))
    # 8 LOST-RECORDED is recorded, not fail. The bare (unbackticked) `[lost-…]`
    # trailer in line 1 is deliberately NOT a token (TOK is backtick-only), so
    # the case asserts LOST-RECORDED=1, not 2 — exactly the measured corpus
    # behaviour disclosed in the round-28 wave-1 receipt.
    add('lost-recorded',
        "Bare marked trailer, not a token: "
        "source: [lost-tree] ~/Projects/bounties/ops/gone.mjs:1-3\n"
        "Backticked marked loss: `[lost-base] ~/Projects/bounties/ops/gone.mjs:4`\n",
        want(**{'LOST-RECORDED': 1}), 0, absent=('bounties',))
    # 9 clean control — in-range lane cite, nothing else, exit 0.
    add('clean', "Clean lane cite: `present.md:2`\n",
        want(**{'IN-RANGE': 1}), 0,
        files=(('lane', 'present.md', 'one\ntwo\nthree\n'),))

    base = tempfile.mkdtemp(prefix='anchorcheck-selftest-')
    report = []
    n_fail = 0
    try:
        for c in ():
            d = os.path.join(base, c['name'])
            root = {}
            for sub in ('lane', 'mirror', 'bounties', 'origin'):
                root[sub] = os.path.join(d, sub)
                if sub not in c['absent']:          # named-but-absent otherwise
                    os.makedirs(root[sub], exist_ok=True)
            for sub, rel, text in c['files']:
                fp = os.path.join(root[sub], rel)
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, 'w') as f:
                    f.write(text)
            if c['git_dir']:
                subprocess.run(['git', '-C', root[c['git_dir']], 'init', '-q'],
                               capture_output=True)
            fixture = os.path.join(d, 'fixture.md')
            with open(fixture, 'w') as f:
                f.write(c['fixture'])
            env = dict(os.environ)
            env.update(KASEGI_LANE_ROOT=root['lane'],
                       KASEGI_MIRROR=root['mirror'],
                       KASEGI_ORIGIN_ROOT=root['origin'],
                       KASEGI_BOUNTIES=root['bounties'])
            p = subprocess.run([sys.executable, os.path.abspath(__file__), fixture],
                               capture_output=True, text=True, env=env)
            got = _counts(p.stdout)
            diffs = [f'{k}: want {v}, got {got.get(k)}'
                     for k, v in c['expected'].items() if got.get(k) != v]
            if p.returncode != c['exit_code']:
                diffs.append(f'exit: want {c["exit_code"]}, got {p.returncode}')
            if diffs:
                n_fail += 1
                report.append(f"selftest FAIL {c['name']}: " + '; '.join(diffs))
                for stream in (p.stdout, p.stderr):
                    if stream.strip():
                        report.append('  ' + stream.strip().replace('\n', '\n  '))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    for line in report:
        print(line)
    print(f"selftest cases={len(cases)} failures={n_fail}")
    return 0 if not n_fail else 1


def main(argv):
    if not argv:
        print('usage: anchorcheck.py <file.md> | anchorcheck.py --selftest',
              file=sys.stderr)
        return 2
    if argv[0] == '--selftest':
        return _selftest()
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
                elif rel.startswith(BOUNTIES_CITE_PREFIX):
                    # (g) BOUNTIES-PROVINCE (round 28): same confinement rule as
                    # ORIGIN/MIRROR, but an absent root is a FAIL class.
                    bounties_root = os.path.realpath(BOUNTIES_ROOT)
                    path = os.path.realpath(os.path.join(bounties_root, rel[len(BOUNTIES_CITE_PREFIX):]))
                    try:
                        within_bounties = os.path.commonpath((bounties_root, path)) == bounties_root
                    except ValueError:
                        within_bounties = False
                    if not within_bounties:
                        outside_root = bounties_root; verdict = 'OUTSIDE-BASE'
                    elif BOUNTIES_ABSENT:
                        verdict = 'BOUNTIES-ABSENT'
                    elif not os.path.isfile(path):
                        verdict = 'MISSING-FILE'
                    else:
                        kind = 'BOUNTIES'
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
                    if kind == 'MIRROR' and MIRROR_ABSENT:
                        verdict = 'BASE-ABSENT'
                    elif kind == 'BOUNTIES' and BOUNTIES_ABSENT:
                        verdict = 'BOUNTIES-ABSENT'
                    else:
                        verdict = 'MISSING-FILE'
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
            if verdict == 'BOUNTIES-ABSENT':
                kinds['BOUNTIES-ABSENT'] = kinds.get('BOUNTIES-ABSENT', 0) + 1
                per.append(f"BOUNTIES-ABSENT md:{ln} {tok} (base tree absent: {path})")
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
        if line.startswith(_PRINT_FIRST):
            print(line)
    inp = sum(v for k2, v in kinds.items() if k2.startswith('IN-RANGE'))
    bad = sum(kinds.get(k, 0) for k in ('MISSING-FILE', 'PAST-EOF', 'OUTSIDE-BASE'))
    print(f"\n== {src}: {inp} in-range cite instances, "
          f"{bad} bad; "
          f"{len(seen)} distinct anchors; "
          f"LOST-RECORDED={kinds.get('LOST-RECORDED', 0)} PIN-BROKEN={kinds.get('PIN-BROKEN', 0)} "
          f"ORIGIN={kinds.get('IN-RANGE(ORIGIN)', 0)} OUTSIDE-BASE={kinds.get('OUTSIDE-BASE', 0)} "
          f"BASE-ABSENT={kinds.get('BASE-ABSENT', 0)}")
    for line in per:
        if not line.startswith(_PRINT_FIRST):
            print(line)
    # round-28 fail-closed rule: any unverifiable verdict fails the gate.
    return 1 if any(kinds.get(k, 0) for k in FAIL_CLASSES) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
