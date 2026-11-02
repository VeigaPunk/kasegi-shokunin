from html.parser import HTMLParser
from pathlib import Path
import json
class P(HTMLParser):
 def __init__(self):super().__init__();self.tables=[];self.table=None;self.row=None;self.cell=None
 def handle_starttag(self,t,a):
  if t=='table':self.table=[]
  if t=='tr':self.row=[]
  if t in ['td','th']:self.cell=''
 def handle_data(self,d):
  if self.cell is not None:self.cell+=d
 def handle_endtag(self,t):
  if t in ['td','th'] and self.cell is not None:self.row.append(' '.join(self.cell.split()));self.cell=None
  if t=='tr' and self.table is not None:self.table.append(self.row);self.row=None
  if t=='table':self.tables.append(self.table);self.table=None
p=Path(__file__).parent;s=P();s.feed((p/'deployer.html').read_text())
rows=next(t[1:] for t in s.tables if t[0][0]=='Row')
(p/'independent-table.json').write_text(json.dumps(rows,indent=2)+'\n')
print('rows',len(rows));o=json.loads((p/'private-oracle.json').read_text())
for c in o['cases']:
 if c['priority']=='model_mismatch':continue
 matches=[r for r in rows if all(v=='insufficient' or v==r[i+1] for i,v in enumerate(c['inputs']))]
 ok=[int(r[0]) for r in matches]==c['path_rows'];print(c['id'],ok,[r[0] for r in matches],set(r[-1] for r in matches));assert ok
