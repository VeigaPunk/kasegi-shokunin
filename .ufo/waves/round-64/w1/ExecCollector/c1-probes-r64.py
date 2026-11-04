#!/usr/bin/env python3
"""Finite round-64 figure-audit CLI collector; not a sandbox or general error policy.

Eight finite new probes run an upstream missing-file read through `wc -l`:
cat missing, cat existing+missing partial, cut, head, tail, ls, sort, sha256sum
missing. Native per-stage exit codes are established by this harness's own
staged subprocess runner, never by the instrument, and each probe's want is
asserted against that native stdout; host drift fails closed (exit 2).

Modes select the expectation rule applied to the measured native statuses:
  base      current figure-audit rule: a nonzero final stage wins
            (derive-exit-N), then the first upstream status >1
            (derive-upstream-exit-N); upstream exit1 and negative signal
            statuses stay ignored. So cat/cut/head/tail/sha256sum missing are
            expected green (want 0; the partial probe want 1) while ls/sort
            missing (measured exit 2) stay stale from the prior >1 rule.
  candidate round-64 command-aware rule: final precedence and negative
            handling unchanged; additionally the first upstream positive
            status is rejected (derive-upstream-exit-N) except status 1 from
            a stage whose command basename is exactly grep (ordinary
            no-match). All eight new probes then expect the exact measured
            upstream reason, exit 1 for the exit1 heads.
Retained controls: grep no-match zero, cat and sort successes, &&
concatenation, && stopping on failure, the prior >1 upstream error
(invalid grep regex, exit 2), final-stage precedence (final exit 7 over
upstream 2; grep exit 1 as a final stage is still derive-exit-1), and
upstream/final negative signal statuses (SIGTERM => -15).

Requires Python 3.9+ stdlib and PATH python3 cat grep wc cut head tail ls sort
sha256sum; no shells, no Git. --instrument and --work must be absolute; work
must be a disposable subdirectory at least two levels under
/fast/scratch/hyaku/kasegi-r64. A missing instrument or dependency, or an
unusable work path, fails closed with exit 2 (HARNESS-ERROR ...). An
instrument inside work is rejected before any fixture is written and is
byte-checked again afterwards. Existing files are never cleared; only this
invocation's fresh private run directory is removed. The instrument is
invoked exactly once per run with one 18-figure ledger; its whole stdout
(every FIG line plus the FIGURE-AUDIT trailer), exit and empty stderr are
compared exactly. Each recorded field binds a fresh per-run nonce from the
supplied ledger, rejecting fixed captured stdout on a later invocation. This
is replay discrimination, not authenticity or a general emulator defense.
--selfcheck replays harness fault
cases (missing instrument, unusable work, instrument under work,
always-green counterfeit, empty output, nonzero exit with clean summary,
pristine control) by running this collector against generated fakes; the
pristine control assumes a base-rule instrument.
Exit 0 exact match, 1 any mismatch, 2 usage/collection error.
"""

import argparse
import datetime
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import secrets
import tempfile
import time
from pathlib import Path

SCRATCH_BASE = Path('/fast/scratch/hyaku/kasegi-r64')
MISS = 'grep-missing-r64.txt'
ONE = 'one.txt'
ONE_BODY = 'kasegi-r64\n'
DEPS = ('python3', 'cat', 'grep', 'wc', 'cut', 'head', 'tail', 'ls', 'sort',
        'sha256sum')

# (id, want, groups); groups: tuple of pipelines, pipeline: tuple of argv tuples.
PROBES = (
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

FAIL7 = 'import sys\nsys.exit(7)\n'
SIGTERM = 'import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n'


class CollectionError(Exception):
    """Harness-side establishment failure; never an instrument verdict."""


def esc(text):
    return str(text).replace('\\', '\\\\').replace('\n', '\\n')


def put(path, text):
    with open(path, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)


def q(argv):
    return ' '.join(shlex.quote(t) for t in argv)


def derive_of(groups):
    return ' && '.join(' | '.join(q(stage) for stage in pipe) for pipe in groups)


def make_fixtures(root):
    counters = root / 'corpus' / 'instruments'
    counters.mkdir(parents=True)
    put(root / ONE, ONE_BODY)
    put(counters / 'fail7.py', FAIL7)
    put(counters / 'sigterm.py', SIGTERM)


def run_pipeline(root, pipe, deadline):
    procs = []
    prev = None
    try:
        for argv in pipe:
            proc = subprocess.Popen(
                argv, cwd=str(root),
                stdin=subprocess.DEVNULL if prev is None else prev.stdout,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            procs.append(proc)
            if prev is not None:
                prev.stdout.close()
            prev = proc
        raw = procs[-1].stdout.read()
        for proc in procs:
            proc.wait(timeout=max(0.0, deadline - time.monotonic()))
        return [proc.returncode for proc in procs], raw
    except subprocess.TimeoutExpired:
        raise CollectionError('native-timeout')
    except OSError as exc:
        raise CollectionError('native-oserror:%s' % exc)
    finally:
        for proc in procs:
            if proc.poll() is None:
                proc.kill()
        for proc in procs:
            proc.wait()
            if proc.stdout is not None:
                proc.stdout.close()


def establish(root):
    """Independently measure every pipeline's per-stage statuses and stdout."""
    deadline = time.monotonic() + 120
    natives = {}
    for name, want, groups in PROBES:
        finals, rcs, chunks = [], [], []
        for pipe in groups:
            stage_rcs, raw = run_pipeline(root, pipe, deadline)
            rcs.append(stage_rcs)
            finals.append(stage_rcs[-1])
            chunks.append(raw)
            if stage_rcs[-1] != 0:
                break  # && grammar: later groups never run after a failed group
        natives[name] = {
            'rcs': rcs,
            'finals': finals,
            'out': b''.join(chunks).decode('utf-8', 'replace').strip(),
        }
    return natives


def expected(name, groups, native, mode):
    """Apply the mode rule to measured statuses; mirrors no instrument code."""
    for gi, pipe in enumerate(groups):
        final = native['finals'][gi]
        if final != 0:
            return 'stale', 'derive-exit-%d' % final
        for si, argv in enumerate(pipe[:-1]):
            rc = native['rcs'][gi][si]
            if mode == 'base':
                bad = rc > 1
            else:
                bad = rc > 0 and not (rc == 1 and os.path.basename(argv[0]) == 'grep')
            if bad:
                return 'stale', 'derive-upstream-exit-%d' % rc
    return 'ok', None


def figure_line(name, rec, verdict, reason, derived):
    if verdict == 'ok':
        return 'FIG %s recorded=%s derived=%s ok' % (name, rec, derived)
    return 'FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale' % (name, rec, reason)


def plan(root, mode, verbose, nonce=''):
    natives = establish(root)
    lines, ok_n, stale_n = [], 0, 0
    for name, want, groups in PROBES:
        native = natives[name]
        verdict, reason = expected(name, groups, native, mode)
        if verdict == 'ok' and native['out'] != want:
            raise CollectionError('native-want-drift:%s native=%r want=%r'
                                  % (name, native['out'], want))
        recorded = esc(want) + (':nonce=' + nonce if nonce else '')
        lines.append(figure_line(name, recorded, verdict, reason, native['out']))
        ok_n += verdict == 'ok'
        stale_n += verdict == 'stale'
        if verbose:
            print('PROBE %s derive=%s' % (name, derive_of(groups)), flush=True)
            print('NATIVE %s rcs=%s stdout=%s'
                  % (name, ' '.join(','.join(str(r) for r in grp) for grp in native['rcs']),
                     esc(native['out'])), flush=True)
            print('EXPECT %s %s reason=%s' % (name, verdict, reason or '-'), flush=True)
    trailer = 'FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d' % (
        len(PROBES), ok_n, stale_n, 1 if stale_n else 0)
    return lines, trailer, natives


def split_records(text):
    """Split instrument stdout into FIG records plus the trailer line."""
    raw_lines = text.split('\n')
    if raw_lines and raw_lines[-1] == '':
        raw_lines.pop()
    records, current = [], None
    for line in raw_lines:
        if line.startswith('FIG ') or line.startswith('FIGURE-AUDIT '):
            if current is not None:
                records.append(current)
            current = line
        elif current is not None:
            current += '\n' + line
        else:
            records.append(line)
    if current is not None:
        records.append(current)
    return records


def grade(result, lines, trailer, expected_exit):
    failures = 0
    records = split_records(result.stdout)
    expected_records = [(PROBES[i][0], line) for i, line in enumerate(lines)]
    expected_records.append(('trailer', trailer))
    for index, (name, want_line) in enumerate(expected_records):
        actual = records[index] if index < len(records) else '<missing>'
        if actual == want_line:
            print('RECORD %s PASS' % name, flush=True)
        else:
            failures += 1
            print('RECORD %s FAIL expected=%s actual=%s'
                  % (name, esc(want_line), esc(actual[:240])), flush=True)
    if len(records) != len(expected_records):
        failures += 1
        print('RECORD shape FAIL observed_records=%d expected_records=%d'
              % (len(records), len(expected_records)), flush=True)
    if result.returncode != expected_exit:
        failures += 1
        print('RECORD exit FAIL observed=%d expected=%d'
              % (result.returncode, expected_exit), flush=True)
    else:
        print('RECORD exit PASS observed=%d' % result.returncode, flush=True)
    if result.stderr:
        failures += 1
        print('RECORD stderr FAIL detail=%s' % esc(result.stderr[:400]), flush=True)
    else:
        print('RECORD stderr PASS', flush=True)
    return failures


def guards(args):
    if not args.instrument.is_absolute() or not args.work.is_absolute():
        raise ValueError('absolute-paths-required')
    instrument = args.instrument.resolve(strict=True)
    work = args.work.resolve()
    if (not work.is_relative_to(SCRATCH_BASE)
            or len(work.relative_to(SCRATCH_BASE).parts) < 2):
        raise ValueError('work-not-owned')
    if instrument.is_relative_to(work):
        raise ValueError('instrument-under-work')
    if not instrument.is_file():
        raise ValueError('instrument-not-file')
    work.mkdir(parents=True, exist_ok=True)
    return instrument, work


def collect(args, instrument, work):
    print('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
    code = instrument.read_bytes()
    nonce = secrets.token_hex(16)
    tools = {name: shutil.which(name) for name in DEPS}
    missing = [name for name, path in tools.items() if path is None]
    if missing:
        raise ValueError('missing-dependencies:' + ','.join(missing))
    print(json.dumps({'mode': args.mode, 'instrument': str(instrument),
                      'instrument_sha256': hashlib.sha256(code).hexdigest(),
                      'dependencies': tools, 'collector_argv': sys.argv},
                     sort_keys=True), flush=True)
    with tempfile.TemporaryDirectory(prefix='c1r64-', dir=work) as temporary:
        root = Path(temporary)
        tmp = root / 'tmp'
        tmp.mkdir()
        make_fixtures(root)
        env = dict(os.environ, TMPDIR=str(tmp), LC_ALL='C',
                   PYTHONDONTWRITEBYTECODE='1')
        for key in [key for key in env if key.startswith('GIT_')]:
            del env[key]
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_CEILING_DIRECTORIES=str(root))
        lines, trailer, _ = plan(root, args.mode, verbose=True, nonce=nonce)
        ledger = root / 'c1-ledger.json'
        put(ledger, json.dumps({'figures': [
            {'id': name, 'record': 'c1-probes-r64.py finite probe',
             'recorded': esc(want) + ':nonce=' + nonce, 'derive': derive_of(groups), 'want': want}
            for name, want, groups in PROBES]}, indent=1))
        argv = [tools['python3'], str(instrument), '--ledger', str(ledger),
                '--root', str(root)]
        print('RUN argv=%s' % json.dumps(argv), flush=True)
        result = subprocess.run(argv, cwd=str(root), env=env, capture_output=True,
                                text=True, timeout=60)
        sys.stdout.write(result.stdout)
        if result.stdout and not result.stdout.endswith('\n'):
            sys.stdout.write('\n')
        sys.stdout.flush()
        print('OBSERVED exit=%d stderr=%s'
              % (result.returncode, esc(result.stderr[:400] or '-')), flush=True)
        failures = grade(result, lines, trailer, 1 if trailer.endswith('exit=1') else 0)
        if instrument.read_bytes() != code:
            raise ValueError('instrument-changed-during-run')
    print('HARNESS probes=%d failures=%d mode=%s' % (len(PROBES), failures, args.mode),
          flush=True)
    return 1 if failures else 0


def selfcheck(args, instrument, work):
    print('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
    code = instrument.read_bytes()
    print(json.dumps({'selfcheck': True, 'instrument': str(instrument),
                      'instrument_sha256': hashlib.sha256(code).hexdigest(),
                      'collector_argv': sys.argv}, sort_keys=True), flush=True)
    me = Path(__file__).resolve()
    outcomes = []

    def spawn(tag, instr, wdir, mode, expect_exit, needle):
        argv = [sys.executable, str(me), '--instrument', str(instr),
                '--work', str(wdir), '--mode', mode]
        print('SELFCHECK-RUN case=%s argv=%s' % (tag, json.dumps(argv)), flush=True)
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=300,
                              cwd=str(wdir.parent))
        out = proc.stdout + proc.stderr
        sys.stdout.write(out)
        if out and not out.endswith('\n'):
            sys.stdout.write('\n')
        good = proc.returncode == expect_exit and (needle is None or needle in out)
        outcomes.append(good)
        print('SELFCHECK case=%s observed=%d expected=%d needle=%s verdict=%s'
              % (tag, proc.returncode, expect_exit, needle or '-',
                 'PASS' if good else 'FAIL'), flush=True)

    with tempfile.TemporaryDirectory(prefix='c1r64sc-', dir=work) as temporary:
        sc = Path(temporary)
        spawn('missing-instrument', sc / 'nonexistent-audit.py', sc / 'w1', 'base',
              2, 'HARNESS-ERROR FileNotFoundError')
        blocker = sc / 'blocker'
        put(blocker, 'sentinel\n')
        spawn('unusable-work', instrument, blocker, 'base', 2,
              'HARNESS-ERROR FileExistsError')
        kept = blocker.read_text() == 'sentinel\n'
        outcomes.append(kept)
        print('SELFCHECK unusable-work sentinel-preserved=%s' % kept, flush=True)
        under = sc / 'w3'
        under.mkdir(parents=True)
        inside = under / 'audit.py'
        put(inside, code.decode('utf-8', 'replace'))
        spawn('instrument-under-work', inside, under, 'base', 2,
              'instrument-under-work')
        intact = inside.read_bytes() == code
        outcomes.append(intact)
        print('SELFCHECK instrument-under-work instrument-preserved=%s' % intact,
              flush=True)
        fake_all_green = ''.join(
            'FIG %s recorded=%s derived=%s ok\n' % (name, esc(want), want)
            for name, want, _ in PROBES)
        fake_all_green += 'FIGURE-AUDIT figures=%d ok=%d stale=0 exit=0\n' % (
            len(PROBES), len(PROBES))
        bin4 = sc / 'bin4'
        bin4.mkdir(parents=True)
        put(bin4 / 'always-green.py', 'import sys\nsys.stdout.write(%r)\n' % fake_all_green)
        spawn('always-green-counterfeit', bin4 / 'always-green.py', sc / 'w4',
              'candidate', 1, 'mode=candidate')
        bin5 = sc / 'bin5'
        bin5.mkdir(parents=True)
        put(bin5 / 'empty.py', 'pass\n')
        spawn('empty-output', bin5 / 'empty.py', sc / 'w5', 'base', 1, None)
        fix6 = sc / 'fix6'
        make_fixtures(fix6)
        lines6, trailer6, _ = plan(fix6, 'base', verbose=False)
        payload = sc / 'expected-base.txt'
        put(payload, '\n'.join(lines6) + '\n' + trailer6 + '\n')
        bin6 = sc / 'bin6'
        bin6.mkdir(parents=True)
        put(bin6 / 'clean-exit7.py',
            "import sys\nsys.stdout.write(open(%r, encoding='utf-8').read())\n"
            'raise SystemExit(7)\n' % str(payload))
        spawn('nonzero-exit-clean-summary', bin6 / 'clean-exit7.py', sc / 'w6',
              'base', 1, 'RECORD exit FAIL observed=7 expected=1')
        spawn('pristine-control', instrument, sc / 'w7', 'base', 0,
              'failures=0 mode=base')
        if instrument.read_bytes() != code:
            raise ValueError('instrument-changed-during-run')
    failures = outcomes.count(False)
    print('HARNESS selfcheck cases=%d failures=%d' % (len(outcomes), failures),
          flush=True)
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--instrument', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--mode', choices=('base', 'candidate'))
    parser.add_argument('--selfcheck', action='store_true')
    args = parser.parse_args()
    if not args.selfcheck and args.mode is None:
        parser.error('--mode is required unless --selfcheck')
    try:
        instrument, work = guards(args)
        if args.selfcheck:
            return selfcheck(args, instrument, work)
        return collect(args, instrument, work)
    except CollectionError as exc:
        print('HARNESS-ERROR CollectionError: %s' % exc, file=sys.stderr, flush=True)
        return 2
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('HARNESS-ERROR %s: %s' % (type(exc).__name__, exc), file=sys.stderr,
              flush=True)
        return 2


if __name__ == '__main__':
    sys.exit(main())
