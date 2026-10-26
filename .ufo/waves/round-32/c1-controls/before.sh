cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
echo "## base tip: $(git rev-parse master)"
ls corpus/instruments/capture-binding-check.py; echo "ls_checker_exit=$?"
ls corpus/instruments/capture-binding-ledger.json; echo "ls_ledger_exit=$?"
python3 corpus/instruments/capture-binding-check.py; echo "checker_exit=$?"
python3 -c "
import json,glob
n=0;u=0;t=0
for f in sorted(glob.glob('corpus/source-snapshots/*/manifest.json')):
    for s in json.load(open(f))['sources']:
        n+=1; u+=('url' in s); t+=('fetched_utc' in s)
print('manifest_records=%d with_url=%d with_fetched_utc=%d'%(n,u,t))"
python3 corpus/instruments/recheck-audit.py --quiet; echo "audit_exit=$?"
python3 corpus/instruments/source-recheck.py --selftest; echo "sr_selftest_exit=$?"
python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json | grep -E '^(limbs|controls|guard)'; echo "r31_ledger_exit=${PIPESTATUS[0]}"
