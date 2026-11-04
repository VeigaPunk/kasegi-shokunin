"""Round-64 MutationCollector attack suite v2 for the ExecCollector c1-probes-r64.py CLI.

Finite, not a sandbox. Each attack is a CLI-shaped producer (argv --ledger PATH --root PATH,
one 18-figure ledger per invocation, like the real instrument) run through the collector's public
CLI (--instrument ABS --work ABS --mode base|candidate). Expected collector exit: 0 exact, 1 mismatch,
2 usage/collection error. Positive controls (A1/A2) must pass before other verdicts are trusted.

The honest oracle implements the docstring rule independently (Popen staged runner, native signal
statuses, && grammar). It is instrument construction, not a candidate score.
Probe table is copied here; drift against the collector's PROBES is reported, not assumed.

Usage: attack-r64-v2.py --collector ABS_PATH --work ABS_SCRATCH_DIR
Exit 0 every attack as expected; 1 any unexpected verdict; 2 setup failure.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

SCRATCH = Path('/fast/scratch/hyaku/kasegi-r64/MutationCollector')
UNOWNED = '/fast/scratch/hyaku/mut-r64-unowned-probe'
TIMEOUT = 150
MISS = 'nosuch-r64.txt'
ONE = 'one.txt'
ONE_BODY = 'kasegi-r64\n'
FAIL7 = 'import sys\nsys.exit(7)\n'
SIGTERM = 'import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n'

# Independent copy of the 18-probe table (id, want, groups); drift vs collector is checked at run.
MY_PROBES = (
    ('cat-missing', '0', (((('cat', MISS), ('wc', '-l')),))),
    ('cat-partial-missing', '1', (((('cat', ONE, MISS), ('wc', '-l')),))),
    ('cut-missing', '0', (((('cut', '-d,', '-f1', MISS), ('wc', '-l')),))),
    ('head-missing', '0', (((('head', '-n', '1', MISS), ('wc', '-l')),))),
    ('tail-missing', '0', (((('tail', '-n', '1', MISS), ('wc', '-l')),))),
    ('ls-missing', '0', (((('ls', MISS), ('wc', '-l')),))),
    ('sort-missing', '0', (((('sort', MISS), ('wc', '-l')),))),
    ('sha256sum-missing', '0', (((('sha256sum', MISS), ('wc', '-l')),))),
    ('grep-no-match', '0', (((('grep', 'zzz-absent', ONE), ('wc', '-l')),))),
    ('cat-success', '1', (((('cat', ONE), ('wc', '-l')),))),
    ('sort-success', '1', (((('sort', ONE), ('wc', '-l')),))),
    ('and-concatenated', '1\n1',
     (((('cat', ONE), ('wc', '-l')), (('cat', ONE), ('wc', '-l'))))),
    ('and-stops-on-failure', '1', (((('cat', MISS),), (('wc', '-l', ONE),)))),
    ('grep-invalid-upstream', '0', (((('grep', '[', ONE), ('wc', '-l')),))),
    ('final-grep-no-match', '0', (((('cat', ONE), ('grep', 'zzz-absent')),))),
    ('final-precedes-upstream', '0',
     (((('grep', '[', ONE), ('python3', 'corpus/instruments/fail7.py')),))),
    ('upstream-negative-signal', '0',
     (((('python3', 'corpus/instruments/sigterm.py'), ('wc', '-l')),))),
    ('final-negative-signal', '0',
     (((('cat', ONE), ('python3', 'corpus/instruments/sigterm.py')),))),
)


def q(argv):
    return ' '.join(shlex.quote(t) for t in argv)


def derive_of(groups):
    return ' && '.join(' | '.join(q(stage) for stage in pipe) for pipe in groups)


def esc(text):
    return str(text).replace('\\', '\\\\').replace('\n', '\\n')


def make_ledger(path):
    figures = [{'id': name, 'record': 'c1-probes-r64.py finite probe', 'recorded': esc(want),
                'derive': derive_of(groups), 'want': want} for name, want, groups in MY_PROBES]
    path.write_text(json.dumps({'figures': figures}, indent=1))


def make_fixtures(root):
    (root / 'corpus' / 'instruments').mkdir(parents=True)
    (root / ONE).write_text(ONE_BODY)
    (root / 'corpus/instruments/fail7.py').write_text(FAIL7)
    (root / 'corpus/instruments/sigterm.py').write_text(SIGTERM)


ORACLE_SRC = r'''
import argparse
import json
import os
import shlex
import subprocess
import sys
import time

BEHAVIOR = '__BEHAVIOR__'
MUTANT = '__MUTANT__'
EXIT_MODE = '__EXIT_MODE__'
NOISE = __NOISE__
SELF_MUTATE = __SELF_MUTATE__


def parse(derive):
    return [[shlex.split(stage) for stage in segment.split(' | ')] for segment in derive.split(' && ')]


def run_pipe(pipe, root, deadline):
    procs, prev = [], None
    try:
        for argv in pipe:
            proc = subprocess.Popen(argv, cwd=root, stdin=subprocess.DEVNULL if prev is None else prev.stdout,
                                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            procs.append(proc)
            if prev is not None:
                prev.stdout.close()
            prev = proc
        raw = procs[-1].stdout.read()
        for proc in procs:
            proc.wait(timeout=max(0.1, deadline - time.monotonic()))
        return [proc.returncode for proc in procs], raw
    finally:
        for proc in procs:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
            if proc.stdout is not None:
                proc.stdout.close()


def upstream_reason(derive, pipe, rcs):
    for argv, rc in zip(pipe[:-1], rcs[:-1]):
        name = os.path.basename(argv[0])
        if MUTANT == 'negative-reject':
            bad = rc != 0 and not (rc == 1 and name == 'grep')
        elif BEHAVIOR == 'base' or MUTANT == 'thresh2':
            bad = rc > 1
        elif MUTANT == 'grep-unexempt':
            bad = rc > 0
        elif MUTANT == 'grep-substring':
            bad = rc > 0 and not (rc == 1 and 'grep' in derive)
        else:
            bad = rc > 0 and not (rc == 1 and name == 'grep')
        if bad:
            return 'derive-upstream-exit-%d' % rc
    return None


def final_reason(rcs):
    final = rcs[-1]
    if MUTANT == 'final-ignore-negative' and final < 0:
        return None
    return ('derive-exit-%d' % final) if final != 0 else None


def judge(derive, groups, root):
    chunks = []
    deadline = time.monotonic() + 100
    for pipe in groups:
        rcs, raw = run_pipe(pipe, root, deadline)
        chunks.append(raw)
        if MUTANT == 'upstream-first':
            reason = upstream_reason(derive, pipe, rcs) or final_reason(rcs)
        else:
            reason = final_reason(rcs) or upstream_reason(derive, pipe, rcs)
        if reason:
            if MUTANT == 'and-ignore-failure':
                continue
            return reason, chunks
    return None, chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ledger', required=True)
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    with open(args.ledger) as handle:
        figures = json.load(handle)['figures']
    lines, ok, stale = [], 0, 0
    for figure in figures:
        reason, chunks = judge(figure['derive'], parse(figure['derive']), args.root)
        out = ''.join(chunk.decode('utf-8', 'replace') for chunk in chunks).strip()
        recorded = figure['recorded']
        if reason is None and out == recorded.replace('\\n', '\n'):
            lines.append(f"FIG {figure['id']} recorded={recorded} derived={out} ok")
            ok += 1
        else:
            lines.append(f"FIG {figure['id']} recorded={recorded} derived=UNAVAILABLE reason={reason or 'value-mismatch'} stale")
            stale += 1
    print('\n'.join(lines))
    print(f'FIGURE-AUDIT figures={len(figures)} ok={ok} stale={stale} exit={1 if stale else 0}')
    if NOISE:
        print('warning: stale cache', file=sys.stderr)
    if SELF_MUTATE:
        with open(__file__, 'a') as handle:
            handle.write('# self-mutation\n')
    if EXIT_MODE == 'forced3':
        return 3
    if EXIT_MODE == 'zero-on-stale':
        return 0
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())
'''

ALWAYS_GREEN = r'''
import argparse, json
ap = argparse.ArgumentParser()
ap.add_argument('--ledger', required=True)
ap.add_argument('--root', required=True)
args = ap.parse_args()
figures = json.load(open(args.ledger))['figures']
for f in figures:
    print(f"FIG {f['id']} recorded={f['recorded']} derived={f['recorded'].replace(chr(92) + 'n', chr(10))} ok")
print(f'FIGURE-AUDIT figures={len(figures)} ok={len(figures)} stale=0 exit=0')
'''

ALWAYS_STALE = r'''
import argparse, json
ap = argparse.ArgumentParser()
ap.add_argument('--ledger', required=True)
ap.add_argument('--root', required=True)
args = ap.parse_args()
figures = json.load(open(args.ledger))['figures']
for f in figures:
    print(f"FIG {f['id']} recorded={f['recorded']} derived=UNAVAILABLE reason=derive-exit-1 stale")
print(f'FIGURE-AUDIT figures={len(figures)} ok=0 stale={len(figures)} exit=1')
'''

PARTIAL = r'''
import argparse, json
ap = argparse.ArgumentParser()
ap.add_argument('--ledger', required=True)
ap.add_argument('--root', required=True)
args = ap.parse_args()
figures = json.load(open(args.ledger))['figures']
f = figures[0]
print(f"FIG {f['id']} recorded={f['recorded']} derived={f['recorded']} ok")
'''

EMPTY = 'import sys\n'
SYNTAX = 'def (:\n'
HANG = 'import time\ntime.sleep(900)\n'


def make_oracle(behavior, mutant='none', exit_mode='normal', noise=False, self_mutate=False):
    src = ORACLE_SRC
    for key, value in (('__BEHAVIOR__', behavior), ('__MUTANT__', mutant), ('__EXIT_MODE__', exit_mode),
                       ('__NOISE__', repr(noise)), ('__SELF_MUTATE__', repr(self_mutate))):
        src = src.replace(key, value)
    return src


def replay_source(stdout_text):
    return ('import sys\n'
            f'REPLAY = {stdout_text!r}\n'
            'sys.stdout.write(REPLAY)\nsys.exit(1)\n')


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()


def capture_honest_candidate(fx):
    """Replay fabricator material: stdout of the honest candidate oracle on the same ledger."""
    root = SCRATCH / 'replay-root'
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    make_fixtures(root)
    ledger = root / 'ledger.json'
    make_ledger(ledger)
    done = subprocess.run([sys.executable, str(fx / 'A2-cand-oracle.py'), '--ledger', str(ledger), '--root', str(root)],
                          cwd=str(root), capture_output=True, text=True, timeout=300)
    return done.stdout


def build_fixtures():
    fx = SCRATCH / 'fixtures'
    fx.mkdir(parents=True, exist_ok=True)
    sources = {
        'A1-base-oracle.py': make_oracle('base'),
        'A2-cand-oracle.py': make_oracle('cand'),
        'C1-always-green.py': ALWAYS_GREEN,
        'C2-always-stale.py': ALWAYS_STALE,
        'C3-exit3-clean.py': make_oracle('cand', exit_mode='forced3'),
        'C4-zero-on-stale.py': make_oracle('cand', exit_mode='zero-on-stale'),
        'C5-empty.py': EMPTY,
        'C6-partial.py': PARTIAL,
        'C7-stderr-noise.py': make_oracle('cand', noise=True),
        'C8-syntax.py': SYNTAX,
        'B8-self-mutate.py': make_oracle('cand', self_mutate=True),
        'B9-hang.py': HANG,
        'D1-thresh2.py': make_oracle('cand', mutant='thresh2'),
        'D2-grep-unexempt.py': make_oracle('cand', mutant='grep-unexempt'),
        'D3-grep-substring.py': make_oracle('cand', mutant='grep-substring'),
        'D4-upstream-first.py': make_oracle('cand', mutant='upstream-first'),
        'D5-negative-reject.py': make_oracle('cand', mutant='negative-reject'),
        'D6-final-ignore-negative.py': make_oracle('cand', mutant='final-ignore-negative'),
        'D7-and-ignore-failure.py': make_oracle('cand', mutant='and-ignore-failure'),
    }
    digests = {name: write(fx / name, text) for name, text in sources.items()}
    digests['C11-replay.py'] = write(fx / 'C11-replay.py', replay_source(capture_honest_candidate(fx)))
    wrapper = 'import subprocess, sys\np = subprocess.run([sys.executable, %r] + sys.argv[1:], capture_output=True, text=True)\nsys.stdout.write(p.stdout + "FIGURE-AUDIT figures=18 ok=0 stale=0 exit=0\\n")\nsys.exit(p.returncode)\n' % str(fx / 'A2-cand-oracle.py')
    digests['C12-wrapper-extra-trailer.py'] = write(fx / 'C12-wrapper-extra-trailer.py', wrapper)
    nowc = SCRATCH / 'nowc-bin'
    nowc.mkdir(parents=True, exist_ok=True)
    for name in ('cat', 'grep', 'git', 'cut', 'head', 'tail', 'ls', 'sort', 'sha256sum'):
        target = shutil.which(name)
        if target is None:
            raise RuntimeError('missing-tool:' + name)
        link = nowc / name
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(target)
    py = nowc / 'python3'
    if py.is_symlink() or py.exists():
        py.unlink()
    py.symlink_to(sys.executable)
    return digests


def drift_check(collector):
    spec = importlib.util.spec_from_file_location('collector_under_test', collector)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    theirs = tuple(module.PROBES)
    return theirs == MY_PROBES, len(theirs)


def proposed_copy(collector):
    """Copy of the collector with one added probe that exercises the grep-substring mutant."""
    text = collector.read_text()
    anchor = "\n)\n\nFAIL7 = "
    if text.count(anchor) != 1:
        raise RuntimeError('anchor-not-unique')
    added = ("\n    ('grep-named-upstream', '0', (((('cat', 'grep-missing.txt'), ('wc', '-l')),))),\n)\n\nFAIL7 = ")
    out = SCRATCH / 'proposed' / 'c1-probes-r64-proposed.py'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text.replace(anchor, added))
    return out


def attacks(fx, runs):
    a2 = str(fx / 'A2-cand-oracle.py')
    nowc = str(SCRATCH / 'nowc-bin')
    return [
        # id, kind, mode, expect, instrument, work, PATH, timeout, note
        ('A1', 'positive', 'base', 0, str(fx / 'A1-base-oracle.py'), None, None, TIMEOUT, 'base oracle, base rule'),
        ('A2', 'positive', 'candidate', 0, a2, None, None, TIMEOUT, 'cand oracle, candidate rule'),
        ('B1', 'setup', 'candidate', 2, str(fx / 'absent.py'), None, None, TIMEOUT, 'instrument path missing'),
        ('B2', 'setup', 'candidate', 2, 'fixtures/A2-cand-oracle.py', None, None, TIMEOUT, 'instrument relative path'),
        ('B3', 'setup', 'candidate', 2, str(fx), None, None, TIMEOUT, 'instrument is a directory'),
        ('B4', 'setup', 'candidate', 2, str(runs / 'B4' / 'inst.py'), str(runs / 'B4'), None, TIMEOUT, 'instrument under work'),
        ('B5', 'setup', 'candidate', 2, a2, 'runs/B5', None, TIMEOUT, 'work relative path'),
        ('B6', 'setup', 'candidate', 2, a2, UNOWNED, None, TIMEOUT, 'work outside owned scratch'),
        ('B7', 'setup', 'candidate', 2, a2, None, nowc, TIMEOUT, 'PATH lacks wc'),
        ('B8', 'setup', 'candidate', 2, str(fx / 'B8-self-mutate.py'), None, None, TIMEOUT, 'instrument mutates itself'),
        ('B9', 'setup', 'candidate', 2, str(fx / 'B9-hang.py'), None, None, TIMEOUT, 'instrument hangs past collector timeout'),
        ('C1', 'fake', 'candidate', 1, str(fx / 'C1-always-green.py'), None, None, TIMEOUT, 'always-green counterfeit'),
        ('C2', 'fake', 'candidate', 1, str(fx / 'C2-always-stale.py'), None, None, TIMEOUT, 'always stale'),
        ('C3', 'fake', 'candidate', 1, str(fx / 'C3-exit3-clean.py'), None, None, TIMEOUT, 'clean stdout, exit 3'),
        ('C4', 'fake', 'candidate', 1, str(fx / 'C4-zero-on-stale.py'), None, None, TIMEOUT, 'stale stdout, exit 0'),
        ('C5', 'fake', 'candidate', 1, str(fx / 'C5-empty.py'), None, None, TIMEOUT, 'empty output, exit 0'),
        ('C6', 'fake', 'candidate', 1, str(fx / 'C6-partial.py'), None, None, TIMEOUT, 'one FIG line, no trailer'),
        ('C7', 'fake', 'candidate', 1, str(fx / 'C7-stderr-noise.py'), None, None, TIMEOUT, 'correct stdout plus stderr'),
        ('C8', 'fake', 'candidate', 1, str(fx / 'C8-syntax.py'), None, None, TIMEOUT, 'syntax error'),
        ('C9', 'fake', 'candidate', 1, str(fx / 'A1-base-oracle.py'), None, None, TIMEOUT, 'base rule instrument as candidate'),
        ('C10', 'fake', 'base', 1, a2, None, None, TIMEOUT, 'candidate rule instrument as base'),
        ('C11', 'coverage', 'candidate', 1, str(fx / 'C11-replay.py'), None, None, TIMEOUT, 'replay of honest captured stdout; demand freshness/canary'),
        ('C12', 'fake', 'candidate', 1, str(fx / 'C12-wrapper-extra-trailer.py'), None, None, TIMEOUT, 'correct records plus conflicting second trailer'),
        ('D1', 'mutant', 'candidate', 1, str(fx / 'D1-thresh2.py'), None, None, TIMEOUT, 'upstream threshold >1 in candidate'),
        ('D2', 'mutant', 'candidate', 1, str(fx / 'D2-grep-unexempt.py'), None, None, TIMEOUT, 'grep exit1 not exempted'),
        ('D3', 'coverage', 'candidate', 1, str(fx / 'D3-grep-substring.py'), None, None, TIMEOUT, 'exemption by grep substring in derive'),
        ('D4', 'mutant', 'candidate', 1, str(fx / 'D4-upstream-first.py'), None, None, TIMEOUT, 'upstream before final precedence'),
        ('D5', 'mutant', 'candidate', 1, str(fx / 'D5-negative-reject.py'), None, None, TIMEOUT, 'negative upstream status rejected'),
        ('D6', 'mutant', 'candidate', 1, str(fx / 'D6-final-ignore-negative.py'), None, None, TIMEOUT, 'negative final status ignored'),
        ('D7', 'mutant', 'candidate', 1, str(fx / 'D7-and-ignore-failure.py'), None, None, TIMEOUT, '&& failure ignored; later group decides'),
    ]


def run_collector(collector, instrument, work, mode, path, timeout):
    argv = [sys.executable, str(collector), '--instrument', instrument, '--work', work, '--mode', mode]
    env = dict(os.environ, TMPDIR=str(SCRATCH / 'tmp'))
    if path:
        env['PATH'] = path
    try:
        done = subprocess.run(argv, cwd=str(SCRATCH), env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', '', ''
    return done.returncode, done.stdout, done.stderr


def run_suite(label, collector, fx, runs):
    print(f'COLLECTOR {label} path={collector}', flush=True)
    unexpected = 0
    positive_ok = True
    attack_list = attacks(fx, runs)
    for (aid, kind, mode, expect, instrument, work, path, timeout, note) in attack_list:
        work_arg = work if work else str(runs / aid)
        rc, out, err = run_collector(collector, instrument, work_arg, mode, path, timeout)
        verdict = 'AS-EXPECTED' if rc == expect else 'UNEXPECTED'
        if kind == 'coverage' and rc == 0:
            verdict = 'SURVIVED'
        if verdict != 'AS-EXPECTED':
            unexpected += 1
        if aid in ('A1', 'A2') and rc != 0:
            positive_ok = False
        tail = (out.strip().splitlines() or [''])[-1][:140]
        errtail = (err.strip().splitlines() or [''])[-1][:140]
        print(f'ATTACK {aid} kind={kind} mode={mode} expect={expect} actual={rc} verdict={verdict} '
              f'note="{note}" stdout-tail="{tail}" stderr-tail="{errtail}"', flush=True)
    print(f'SUITE collector={label} attacks={len(attack_list)} unexpected={unexpected} positive_ok={positive_ok}',
          flush=True)
    return unexpected, positive_ok


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collector', required=True)
    args = parser.parse_args()
    print(f'run-utc={datetime.datetime.now(datetime.timezone.utc).isoformat()}', flush=True)
    collector = Path(args.collector)
    if not collector.is_absolute() or not collector.is_file():
        print(f'SETUP-ERROR collector not an absolute file: {args.collector}', file=sys.stderr)
        return 2
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / 'tmp').mkdir(exist_ok=True)
    runs = SCRATCH / 'runs'
    runs.mkdir(exist_ok=True)
    fx = SCRATCH / 'fixtures'
    digests = build_fixtures()
    write(runs / 'B4' / 'inst.py', make_oracle('cand'))
    for name, digest in sorted(digests.items()):
        print(f'FIXTURE {name} sha256={digest}', flush=True)
    equal, count = drift_check(collector)
    print(f'PROBE-TABLE-DRIFT collector_probes={count} equal_to_suite_copy={equal}', flush=True)
    total_unexpected = 0
    unexpected, _ok = run_suite('exec-collector-r64', collector, fx, runs)
    total_unexpected += unexpected
    proposed = proposed_copy(collector)
    print(f'PROPOSED-COPY path={proposed} sha256={hashlib.sha256(proposed.read_bytes()).hexdigest()}', flush=True)
    rc, out, err = run_collector(proposed, str(fx / 'D3-grep-substring.py'), str(runs / 'P-D3'), 'candidate', None, TIMEOUT)
    kills = rc == 1
    print(f'PROPOSED-PROBE attack=D3 collector=proposed actual={rc} verdict={"KILLED" if kills else "SURVIVED"} '
          f'stdout-tail="{(out.strip().splitlines() or [""])[-1][:140]}"', flush=True)
    rc, out, err = run_collector(proposed, str(fx / 'A2-cand-oracle.py'), str(runs / 'P-A2'), 'candidate', None, TIMEOUT)
    print(f'PROPOSED-PROBE control=A2 collector=proposed actual={rc} verdict={"AS-EXPECTED" if rc == 0 else "UNEXPECTED"}',
          flush=True)
    unowned = Path(UNOWNED)
    if unowned.exists():
        print(f'UNOWNED-WRITE-DETECTED {UNOWNED} (removing)', flush=True)
        shutil.rmtree(unowned)
        total_unexpected += 1
    print(f'MUTATION-SUITE unexpected_total={total_unexpected}', flush=True)
    return 1 if total_unexpected else 0


if __name__ == '__main__':
    sys.exit(main())
