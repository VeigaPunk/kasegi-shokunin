#!/usr/bin/env python3
"""Trace the unchanged real gate to prove SIGPIPE and unopened input in ONE run.

All fixture and temp bytes are reviewer scratch. Durable traces and ledgers are
reviewer-owned evidence. Existing strace only; no package/PATH changes.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

OUT = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ReviewMultiHead/final2/traces')
WORK = Path('/fast/scratch/hyaku/kasegi-r67/ReviewMultiHead/trace-work2')
BASE = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ReviewMultiHead/base-51f299.py')
CAND = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py')


def main():
    if WORK.exists():
        raise ValueError('trace work already exists')
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir()
    env = dict(os.environ, TMPDIR=str(WORK), HYAKU_SCRATCH=str(WORK), PYTHONDONTWRITEBYTECODE='1')
    try:
        big = b'alpha\n' + (b'x' * 1023 + b'\n') * 4096
        (WORK / 'big.txt').write_bytes(big)
        tiny = 'tiny-' + 't' * 114 + '.txt'
        (WORK / tiny).write_bytes(b'a')
        # Both the list operands and the first data input exceed 4 MiB. A long
        # list keeps the final missing input well beyond pipe-buffer effects.
        checksum = hashlib.sha256(big).hexdigest() + '  big.txt\n'
        checksum += (hashlib.sha256(b'a').hexdigest() + '  ' + tiny + '\n') * 30000
        checksum += hashlib.sha256(b'a').hexdigest() + '  missing.txt\n'
        (WORK / 'biglist').write_text(checksum)
        (WORK / 'list0').write_bytes(b'big.txt\0' + (tiny.encode() + b'\0') * 40000 + b'missing.txt\0')
        manifest = {name: {'bytes':(WORK / name).stat().st_size,
                           'sha256':hashlib.sha256((WORK / name).read_bytes()).hexdigest()}
                    for name in ('big.txt', 'list0', 'biglist')}
        assert all(v['bytes'] >= 4 * 1024 * 1024 for v in manifest.values())
        (OUT / 'fixtures.json').write_text(json.dumps(manifest, indent=2) + '\n')
        all_results = []
        for cid, producer, want in [
            ('wc_list_indirection', ['wc', '-l', '--files0-from=list0'], '4097 big.txt'),
            ('sha_list_indirection', ['sha256sum', '-c', 'biglist'], 'big.txt: OK'),
        ]:
            full = subprocess.run(producer, cwd=WORK, env=env, stdin=subprocess.DEVNULL,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
            ledger = {'figures':[{'id':cid, 'record':'trace-fixture:1', 'recorded':want,
                                 'want':want, 'derive':' '.join(producer) + ' | head -n 1'}]}
            lp = OUT / (cid + '.ledger.json')
            lp.write_text(json.dumps(ledger, indent=2) + '\n')
            for label, gate in [('base', BASE), ('candidate', CAND)]:
                trace = OUT / (cid + '-' + label + '.trace')
                command = ['/usr/bin/strace', '-f', '-qq', '-s', '240', '-e',
                           'trace=execve,openat,wait4', '-o', str(trace),
                           '/usr/bin/python3', '-B', str(gate), '--ledger', str(lp),
                           '--root', str(WORK)]
                result = subprocess.run(command, cwd=WORK, env=env, capture_output=True, timeout=180)
                text = trace.read_text()
                missing = [line for line in text.splitlines()
                           if 'openat(' in line and '"missing.txt"' in line]
                pipe_wait = [line for line in text.splitlines() if 'wait4(' in line and 'SIGPIPE' in line]
                pipe_signal = [line for line in text.splitlines() if '--- SIGPIPE ' in line or 'killed by SIGPIPE' in line]
                row = {'id':cid, 'label':label, 'gate_sha256':hashlib.sha256(gate.read_bytes()).hexdigest(),
                       'untruncated_stage0':full.returncode, 'exit':result.returncode,
                       'stdout':result.stdout.decode(), 'stderr':result.stderr.decode(),
                       'trace':str(trace), 'missing_open_attempts':missing,
                       'sigpipe_waits':pipe_wait, 'sigpipe_signals':pipe_signal}
                all_results.append(row)
                print(cid, label, 'full=',full.returncode, 'gate=',result.returncode,
                      'sigpipe_waits=',len(pipe_wait), 'missing_opens=',len(missing))
                print(result.stdout.decode().strip())
                for line in pipe_wait:
                    print(line)
        (OUT / 'results.json').write_text(json.dumps(all_results, indent=2) + '\n')
    finally:
        shutil.rmtree(WORK)


if __name__ == '__main__':
    main()
