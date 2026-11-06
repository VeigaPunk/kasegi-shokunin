import json, glob, os, sys
root = sys.argv[1]
man = json.load(open(os.path.join(root, 'corpus/source-snapshots/round-81/manifest.json'), encoding='utf-8'))
src = next(s for s in man['sources'] if s['id'] == 'S115')
files = [f for f in sorted(glob.glob(os.path.join(root, 'corpus/knowledge/*.md')))
         if not f.endswith('osv-importfindings-record-quality-feedback.md')]
print('entries scanned: %d' % len(files))
total = 0
for q in src['quotes']:
    hits = [os.path.basename(f) for f in files if q['quote'] in open(f, encoding='utf-8').read()]
    total += len(hits)
    print('%s files=%d %s' % (q['id'], len(hits), hits[:5]))
print('TOTAL_LITERAL_FILES=%d' % total)
