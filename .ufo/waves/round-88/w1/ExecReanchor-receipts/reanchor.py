#!/usr/bin/env python3
"""Generate advisory same-span anchor shifts within three lines, never edit corpus."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
ROUND = LANE / '.ufo/waves/round-88'
OUT = ROUND / 'w1/ExecReanchor-receipts'
BASE = '6beead9148945fa695cf3139e8fc9d8e91cc5fd0'


def git(*args):
    return subprocess.run(['git', '-C', str(LANE), *args], check=True,
                          capture_output=True, text=True).stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    meter_bytes = (ROUND / 'c1/knowledge-meter.py').read_bytes()
    # Reuse precisely the frozen definitions, without importing or copying the counter.
    tree = ast.parse(meter_bytes)
    selected = [node for node in tree.body
                if (isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id in {'KEY', 'WORD', 'PATHLIKE'}
                            for t in node.targets))
                or (isinstance(node, ast.FunctionDef) and node.name == 'idents')]
    namespace = {'re': re}
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<frozen-identifiers>', 'exec'), namespace)
    key_pattern, word, idents = (namespace[n] for n in ('KEY', 'WORD', 'idents'))
    excluded_bytes = (ROUND / 'c1/excluded.json').read_bytes()
    excluded = json.loads(excluded_bytes)
    keys = sorted(k for k, reason in excluded.items() if reason.startswith('anchor-content-drift:'))
    names = git('ls-tree', '-r', '--name-only', BASE, 'corpus/knowledge/').splitlines()
    files = {name: git('show', BASE + ':' + name) for name in names
             if name.endswith('.md') and name.count('/') == 2}
    candidates = {}
    counts = {'unique': 0, 'ties': 0, 'none': 0}
    all_lines_pass = 0
    for key in keys:
        match = key_pattern.fullmatch(key)
        name, lo, hi = match.groups()
        lo, hi = int(lo), int(hi or lo)
        span = hi - lo + 1
        target = 'corpus/knowledge/' + name
        lines = files[target].split('\n')
        citing = [(path, number, line) for path, text in sorted(files.items())
                  for number, line in enumerate(text.split('\n'), 1) if '`' + key + '`' in line]
        if not citing:
            raise ValueError('missing citing line: ' + key)
        source_ids = [idents(line) for _, _, line in citing]
        scored = []
        for start in range(max(1, lo - 3), min(lo + 3, len(lines) - span + 1) + 1):
            end = start + span - 1
            target_ids = set(word.findall('\n'.join(lines[start - 1:end])))
            overlaps = [sorted(ids & target_ids) for ids in source_ids]
            score = sum(map(len, overlaps))
            anchor = str(start) if span == 1 else str(start) + '-' + str(end)
            scored.append({'proposed': target + ':' + anchor, 'shift': start - lo,
                           'overlap_score': score, 'per_citing_line_overlap': overlaps,
                           'm8_all_citing_lines': all(overlaps)})
        best_score = max((row['overlap_score'] for row in scored), default=0)
        best = [row for row in scored if row['overlap_score'] == best_score] if best_score else []
        status = 'none' if not best else ('unique' if len(best) == 1 else 'ties')
        counts[status] += 1
        all_lines_pass += bool(best) and any(row['m8_all_citing_lines'] for row in best)
        # Long opaque spans are removed before any excerpt reaches the wave directory.
        excerpts = [{'path': path, 'line': number,
                     'excerpt': re.sub(r'[A-Za-z0-9_+/%=\-]{16,}', '[redacted-long-span]', line)[:120]}
                    for path, number, line in citing]
        candidates[key] = {'status': status, 'proposed': best[0]['proposed'] if status == 'unique' else 'none',
                           'overlap_score': best_score, 'best_candidates': best,
                           'citing_lines': excerpts}
    payload = json.dumps(candidates, indent=2, sort_keys=True) + '\n'
    (OUT / 'reanchor-candidate.json').write_text(payload)
    evidence = {'base': BASE, 'keys': len(keys), 'counts': counts,
                'keys_with_m8_passing_best_candidate': all_lines_pass,
                'window': 'original start +/-3, unchanged span length, valid in-entry ranges only',
                'score': 'sum over citing lines of distinct case-sensitive identifier intersections; no proximity tie-break',
                'none': 'no candidate range has positive overlap; ties keep every best range and do not choose one',
                'target_tokens': 'WORD over entire target range, matching frozen M8 lines 228-230',
                'excerpt_policy': 'long opaque spans redacted before truncating to 120 characters',
                'excluded_sha256': digest(excluded_bytes), 'meter_sha256': digest(meter_bytes),
                'script_sha256': digest(Path(__file__).read_bytes()),
                'candidate_sha256': digest(payload.encode()),
                'base_file_sha256': {path: digest(text.encode()) for path, text in sorted(files.items())}}
    (OUT / 'summary.json').write_text(json.dumps(evidence, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: evidence[k] for k in ('keys', 'counts', 'keys_with_m8_passing_best_candidate', 'candidate_sha256')}))


if __name__ == '__main__':
    main()
