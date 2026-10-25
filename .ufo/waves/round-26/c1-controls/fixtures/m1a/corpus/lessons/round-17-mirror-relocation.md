# Round 17 continuation — selected-root truthfulness, not source recovery

Explicitly steered round 17, continued after the historical round-20 records.
Axis: **depth:verifiability**; numeric score **4 → 4**. The improvement is
resolver correctness under an operator-selected mirror, not live source
availability. Evidence: `LOG.md` section “Round 17 continuation — 2026-10-15”,
`corpus/lessons/round-20-recensus.md:34-35`, and the immutable revisions below.

## Measured revisions and result

- Before: `4b2e30231c20d3374a39976df5a0f998a6c6f90c`.
- After implementation: `d43e63c8872c4029c7edb9067d8f272642e7885a`.
- Actual copied CLI, isolated HOME, populated relocated mirror: explicit
  canonical citations resolving **to the expected selected-root files**:
  **0/2 → 2/2**. Relative control: `MIRROR-EQUIVALENT` on both revisions;
  missing-file control: `GONE` on both. CLI exits: **0 → 0**.
- Before stdout: `distinct=4 resolves=0 mirror=1 internal=0 other=0 gone=3 skill=1/4 corpus=0/0 all=1/4`.
- After stdout: `distinct=4 resolves=2 mirror=1 internal=0 other=0 gone=1 skill=3/4 corpus=0/0 all=3/4`.
- Resolver SHA-256 before:
  `97012403e89a94d2478249de4fa198f873520328df14e4432b1040c564e03294`;
  after: `d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903`.

The copied CLI writes its Markdown/TSV only beside that temporary script.
No generated fixture census is published as the lane census of record.
Both documented domain roots remain recorded absent; no restoration is
claimed (`PROVINCE.md:16-22`). `RESOLVES` here proves a mapped path exists,
not source revision, byte identity, line-anchor validity, or receipt authenticity.

## Counting command — both committed resolver revisions

Run from the lane root. This is the same fixture and counting definition used
for the observed before/after pair, including verification of the actual TSV
resolved paths rather than just counting a class label.

```bash
python3 -B - <<'PY'
import csv, hashlib, json, os, pathlib, subprocess, tempfile
repo = pathlib.Path.cwd()
revisions = ('4b2e30231c20d3374a39976df5a0f998a6c6f90c',
             'd43e63c8872c4029c7edb9067d8f272642e7885a')
for revision in revisions:
    source = subprocess.check_output(
        ['git', 'show', f'{revision}:corpus/instruments/resolve.py'], cwd=repo)
    with tempfile.TemporaryDirectory(prefix='.round-17-count-', dir=repo) as tmp:
        fixture = pathlib.Path(tmp)
        home, mirror, lane, instrument = (
            fixture / name for name in ('home', 'mirror', 'lane', 'instrument'))
        for directory in (home, mirror, lane / 'corpus', instrument):
            directory.mkdir(parents=True, exist_ok=True)
        targets = [mirror / 'ops/rank.mjs', mirror / '.omp/config.yml']
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('fixture source\n', encoding='utf-8')
        tokens = [
            '~/Projects/the-bounty-hunter/ops/rank.mjs:1',
            str(home / 'Projects/the-bounty-hunter/.omp/config.yml') + ':1',
            'ops/rank.mjs:1',
            '~/Projects/the-bounty-hunter/ops/missing.mjs:1',
        ]
        (lane / 'SKILL.md').write_text(
            '# Relocated mirror citations\n' +
            '\n'.join(f'`{token}`' for token in tokens) + '\n', encoding='utf-8')
        (instrument / 'resolve.py').write_bytes(source)
        process = subprocess.run(
            ['python3', '-B', str(instrument / 'resolve.py'), str(lane)],
            cwd=repo, text=True, capture_output=True,
            env=dict(os.environ, HOME=str(home), KASEGI_MIRROR=str(mirror),
                     PYTHONDONTWRITEBYTECODE='1'))
        if process.returncode:
            raise RuntimeError(process.stderr)
        with (instrument / 'citation-survival.tsv').open() as file:
            rows = {row['citation']: row
                    for row in csv.DictReader(file, delimiter='\t')}
        print(json.dumps({
            'revision': revision,
            'resolver_sha256': hashlib.sha256(source).hexdigest(),
            'cli_exit': process.returncode,
            'explicit_resolved': sum(
                rows[token]['class'] == 'RESOLVES' and
                pathlib.Path(rows[token]['resolved_path']).resolve() == target.resolve()
                for token, target in zip(tokens[:2], targets)),
            'explicit_total': 2,
            'explicit_classes': [rows[token]['class'] for token in tokens[:2]],
            'relative_control': rows[tokens[2]]['class'],
            'missing_control': rows[tokens[3]]['class'],
            'stdout': process.stdout.splitlines()[0],
        }, sort_keys=True))
PY
```

## Frozen live-input guard

On the unchanged committed `SKILL.md`, the resolver's own extraction/classify
rule returns **32/506 → 32/506** (6.32%), with **0 changed verdicts**. The
numeric score therefore stays **4**, rather than crediting fixture paths as
recovered primary sources. `SKILL.md` and `PROVINCE.md` are byte-identical at
both measured revisions; density and province coverage are unchanged.
Recheck/count command:

```bash
python3 -B - <<'PY'
import hashlib, os, pathlib, subprocess
repo = pathlib.Path.cwd()
for rev in ('4b2e30231c20d3374a39976df5a0f998a6c6f90c',
            'd43e63c8872c4029c7edb9067d8f272642e7885a'):
    get = lambda path: subprocess.check_output(['git', 'show', f'{rev}:{path}'])
    ns = {'__name__': 'measured_resolver',
          '__file__': str(repo / 'corpus/instruments/resolve.py')}
    exec(compile(get('corpus/instruments/resolve.py'), ns['__file__'], 'exec'), ns)
    skill = get('SKILL.md')
    cites = {match.group(1).strip().rstrip('.,;:')
             for line in skill.decode().splitlines() for match in ns['TOKEN'].finditer(line)
             if ns['is_pathlike'](match.group(1).strip().rstrip('.,;:'))}
    resolved = sum(ns['classify'](token, str(repo),
                   os.path.expanduser(ns['MIRROR_ROOT']))[0] != 'GONE' for token in cites)
    print(rev, f'{resolved}/{len(cites)}',
          'SKILL=' + hashlib.sha256(skill).hexdigest(),
          'PROVINCE=' + hashlib.sha256(get('PROVINCE.md')).hexdigest())
PY
```

Observed stable hashes: SKILL
`d4383dc435359aca17a3e9b5a733041300907be977fe62c6ffa48afac62fdcfc`;
PROVINCE `206c8caaecab130fd80d75b58ed655447597b939dad79af4a30e3fa54022ad31`.
The full mutable corpus census is deliberately not regenerated or scored by
this fixture experiment; documentation additions change its denominator.

## Gate

- Candidate admitted: exact canonical mirror aliases honor the selected root,
  retain existing classes, report actual paths, and do not fall back to stale
  canonical bytes. Motivation and CLI counterexample are above.
- Candidate rejected: ORIGIN-WORK override support, generic root remapping,
  domain-source restoration, source authentication, or a score bump. None is
  established by these inputs or requested by this move.
- Adversarial static review rejected two proposed fixture constructions: a
  helper tried writing a file over an already-created directory, and an escape
  target was not placed at the path the traversal would actually reach. These
  are test-harness defects, not evidence that the production branch passed.
- Outside non-author spot-check: **not performed**. Dispatched L2 reviewers
  remain part of this lane; they cannot confer promotion or an outside
  discernment verdict. Expansion unchanged; quality improved in the bounded
  resolver contract; discernment unchanged.
