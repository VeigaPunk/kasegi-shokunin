import hashlib, importlib.util, json, pathlib, shutil, subprocess, sys
sys.dont_write_bytecode = True
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
scratch = pathlib.Path('/fast/scratch/hyaku/kasegi-r47/R47RevCounterC1')
seat = lane / '.ufo/waves/round-47/w1/R47RevCounterC1.draft'
freeze = '308a2cb2dc7bdce233461cc1ac49dd88e51c6193'
base_rev = 'fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8'
def frozen(rel, rev=freeze):
    return subprocess.check_output(['git', '-C', str(lane), 'show', rev + ':' + rel])
def put(root, rel, data):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode())
def run(label, tree):
    command = [sys.executable, '-I', str(lane / 'corpus/instruments/r47-routed-defects.py'), '--root', str(tree), '--work', str(scratch / ('work-' + label))]
    result = subprocess.run(command, capture_output=True, text=True, timeout=45)
    receipt = '$ ' + ' '.join(command) + '\n' + result.stdout + result.stderr + 'process_returncode=' + str(result.returncode) + '\n'
    (seat / (label + '.txt')).write_text(receipt)
    print(label + '\n' + result.stdout + 'process_returncode=' + str(result.returncode))
try:
    scratch.mkdir(parents=True, exist_ok=False)
    for rel in ['corpus/instruments/r47-routed-defects.py', 'corpus/instruments/r47-counters-selftest.py']:
        expected = frozen(rel)
        actual = (lane / rel).read_bytes()
        if actual != expected:
            raise RuntimeError('working counter/fixture differs from freeze: ' + rel)
    spec = importlib.util.spec_from_file_location('fixture', lane / 'corpus/instruments/r47-counters-selftest.py')
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    base = scratch / 'base'
    for rel in ['corpus/SOURCES.md', fixture.ENTRY29, 'corpus/lessons/round-46.md']:
        put(base, rel, frozen(rel, base_rev))
    green = pathlib.Path(fixture.build_c1_green(str(base), str(scratch)))
    # Preserve only the changed attack bytes for reproducibility; source snapshots remain pinned fixture inputs.
    a = pathlib.Path(shutil.copytree(green, scratch / 'attack-A-hidden-registry'))
    p = a / 'corpus/SOURCES.md'
    p.write_text('<!--\n' + p.read_text() + '\n-->\n')
    put(seat, 'attack-A/corpus/SOURCES.md', p.read_bytes())
    b = pathlib.Path(shutil.copytree(green, scratch / 'attack-B-hidden-corrections'))
    for rel in ['corpus/lessons/round-46.md', 'corpus/lessons/round-47.md']:
        p = b / rel
        # Tilde fences also contain the backtick tokens present in the lesson prose.
        p.write_text('~~~~\n' + p.read_text() + '\n~~~~\n')
        put(seat, 'attack-B/' + rel, p.read_bytes())
    p = b / fixture.ENTRY29
    p.write_text('<!--\n' + p.read_text() + '\n-->\n\n'
                 '# Admitted F29 lifecycle\n\n'
                 'All 42 lines are body **prose**; the whole capture is that **body**.\n'
                 'Follow the lifecycle in the order the page **states** it.\n'
                 'The three cases let a **maintainer** publish without a fix.\n')
    put(seat, 'attack-B/' + fixture.ENTRY29, p.read_bytes())
    for label, tree in [('do-nothing-base', base), ('green-control', green), ('attack-A', a), ('attack-B', b)]:
        run(label, tree)
    (seat / 'identity.json').write_text(json.dumps({'freeze': freeze, 'base': base_rev, 'counter_sha256': hashlib.sha256(frozen('corpus/instruments/r47-routed-defects.py')).hexdigest(), 'fixture_builder': 'r47-counters-selftest.py:212-228', 'base_subset': ['corpus/SOURCES.md', fixture.ENTRY29, 'corpus/lessons/round-46.md']}, indent=2) + '\n')
finally:
    shutil.rmtree(scratch, ignore_errors=True)
