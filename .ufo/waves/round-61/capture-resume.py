import pathlib,subprocess,html.parser,re,json,hashlib,datetime
p=pathlib.Path('/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/corpus/source-snapshots/round-61')
class Parser(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['p','div','br','tr','h1','h2','h3','h4','li']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t in ['p','div','tr','li']:self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
urls=['https://cwe.mitre.org/documents/cwe_usage/guidance.html']+[f'https://cwe.mitre.org/data/definitions/{n}.html' for n in [190,131,787,119,20,79,862,863]]
rows=[]
for i,url in enumerate(urls,98):
 sid=f'S{i:03d}'
 if (p/(sid+'.txt')).exists(): txt=(p/(sid+'.txt')).read_text();lines=txt.splitlines()
 else:
  raw=subprocess.check_output(['curl','--max-time','25','--retry','1','-L','--fail','-sS',url]);q=Parser();q.feed(raw.decode());lines=[' '.join(x.split()) for x in ''.join(q.out).splitlines() if x.strip()];txt='\n'.join(lines)+'\n';(p/(sid+'.txt')).write_text(txt)
 rows.append(dict(id=sid,url=url,capture_url=url,fetched_utc=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),http={'status':200},kind='html',path=sid+'.txt',sha256=hashlib.sha256(txt.encode()).hexdigest(),quotes=[]))
 print(sid,url,len(txt), [(n+1,x) for n,x in enumerate(lines) if 'Vulnerability Mapping:' in x or x.startswith('Abstraction:') or x=='Usage' or 'root cause(s)' in x][:6])
(p/'manifest.json').write_text(json.dumps({'schema_version':1,'sources':rows},indent=2)+'\n')
