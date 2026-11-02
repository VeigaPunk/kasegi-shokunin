#!/usr/bin/env python3
# Bounded OSV affectedness fragment evaluator; no network, scanning or writes.
# stdin JSON {package:{ecosystem,name},version,osv:{affected:[...]}}.
# Exit 0 determinate affected/unaffected (NOT safety); 2 unsupported/could-not-evaluate;
# 3 invalid fragment/could-not-evaluate; 64 usage. No full OSV schema validation.
import json,re,sys
RELEASE=re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z',re.ASCII)
VERBS={'introduced','fixed','last_affected','limit'}
class Invalid(ValueError):pass
class Unsupported(ValueError):pass
def identity(p):
 if not isinstance(p,dict) or any(not isinstance(p.get(k),str) or not p[k] for k in ('ecosystem','name')):raise Invalid('package-shape')
 return p['ecosystem'],p['name']
def release(v):
 if not isinstance(v,str) or not RELEASE.fullmatch(v):raise Unsupported('version-domain')
 return tuple(int(x) for x in v.split('.'))
def validate_range(r):
 if not isinstance(r,dict) or not isinstance(r.get('type'),str) or not isinstance(r.get('events'),list):raise Invalid('range-shape')
 verbs=[]
 for e in r['events']:
  if not isinstance(e,dict) or len(e)!=1:raise Invalid('event-shape')
  k,v=next(iter(e.items()))
  if k not in VERBS or not isinstance(v,str) or not v:raise Invalid('event-shape')
  verbs.append(k)
 if 'fixed' in verbs and 'last_affected' in verbs:raise Invalid('mixed-closures')
 if 'introduced' not in verbs:raise Invalid('missing-introduced')
 if r['type']=='GIT' and (not isinstance(r.get('repo'),str) or not r['repo']):raise Invalid('missing-repo')
def in_range(v,r):
 if r['type']!='SEMVER':raise Unsupported('range-type')
 query=release(v)
 events=[];limits=[]
 for e in r['events']:
  k,s=next(iter(e.items()))
  if k=='limit':limits.append(None if s=='*' else release(s));continue
  n=(-1,-1,-1) if k=='introduced' and s=='0' else release(s)
  events.append((n,k))
 # Equal-value cross-kind event precedence is not asserted by this bounded tool.
 by_version={}
 for n,k in events:
  if n in by_version and by_version[n]!=k:raise Unsupported('ambiguous-event-tie')
  by_version[n]=k
 if limits and not any(n is None or query<n for n in limits):return False
 affected=False
 for n,k in sorted(events):
  if k=='introduced' and query>=n:affected=True
  elif k=='fixed' and query>=n:affected=False
  elif k=='last_affected' and query>n:affected=False
 return affected
def evaluate(request):
 if not isinstance(request,dict):raise Invalid('request-shape')
 target=identity(request.get('package'));v=request.get('version');osv=request.get('osv')
 if not isinstance(v,str) or not v:raise Invalid('version-shape')
 if not isinstance(osv,dict) or not isinstance(osv.get('affected',[]),list):raise Invalid('affected-shape')
 entries=[]
 for a in osv.get('affected',[]):
  if not isinstance(a,dict):raise Invalid('affected-shape')
  if identity(a.get('package'))!=target:continue
  versions=a.get('versions',[]);ranges=a.get('ranges',[])
  if not isinstance(versions,list) or any(not isinstance(x,str) or not x for x in versions):raise Invalid('versions-shape')
  if not isinstance(ranges,list):raise Invalid('ranges-shape')
  for r in ranges:validate_range(r)
  entries.append((versions,ranges))
 # Structural validation of matching entries precedes evaluation. This is an explicit
 # local admission rule, not a claim that the OSV evaluation pseudocode validates JSON.
 for versions,ranges in entries:
  if v in versions:return {'status':'affected','reason':'explicit-match'}
 unknown=[]
 for versions,ranges in entries:
  for r in ranges:
   try:
    if in_range(v,r):return {'status':'affected','reason':'range-match'}
   except Unsupported as e:unknown.append(str(e))
 if unknown:raise Unsupported(sorted(set(unknown))[0])
 return {'status':'unaffected','reason':'no-match'}
def main():
 if len(sys.argv)!=1:print(json.dumps({'status':'invalid','reason':'usage'}));return 64
 try:
  result=evaluate(json.load(sys.stdin));code=0
 except Invalid as e:result={'status':'invalid','reason':str(e)};code=3
 except Unsupported as e:result={'status':'unsupported','reason':str(e)};code=2
 except (ValueError,TypeError,UnicodeError,OSError):result={'status':'invalid','reason':'unreadable-json'};code=3
 print(json.dumps(result,sort_keys=True));return code
if __name__=='__main__':sys.exit(main())
