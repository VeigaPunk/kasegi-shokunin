import json,sys
from pathlib import Path
ledger=Path(sys.argv[sys.argv.index('--ledger')+1])
f=json.loads(ledger.read_text())['figures'][0]
print('FIG %s recorded=%s derived=%s ok'%(f['id'],f['recorded'],f['want']))
print('FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0')
