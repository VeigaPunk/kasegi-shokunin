import json,sys
from pathlib import Path
ledger=json.loads(Path(sys.argv[sys.argv.index('--ledger')+1]).read_text())
f=ledger['figures'][0]
if f['id'] in ('inside','inside-normalized','quoted-separator','plain-count'):
 print('FIG WRONG-ID recorded=999 derived='+f['want']+' ok')
 raise SystemExit(0)
print('FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=WRONG-ID')
raise SystemExit(2)
