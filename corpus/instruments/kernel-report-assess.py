#!/usr/bin/env python3
"""Offline synthetic teaching probe, not a kernel report validator.
0 assessment completed (not clean/accepted); 2 invalid/unsupported/unreadable.
Never runs supplied commands or accesses referenced files or network.
"""
import argparse,json,pathlib,re,sys
class Invalid(ValueError):pass
def obj(x):
 if not isinstance(x,dict):raise Invalid('object-required')
 return x
def typed(x,key,typ):
 if key not in x or type(x[key]) is not typ:raise Invalid('invalid-field:'+key)
 return x[key]
def strings(x):
 obj(x)
 if not all(type(k) is str and type(v) is str for k,v in x.items()):raise Invalid('string-map-required')
 return x
def shape(d):
 obj(d)
 for k,t in [('schema',str),('synthetic',bool),('description',str),('ai_assisted',bool),('traces',list),('public_text',list)]:typed(d,k,t)
 if d['schema']!='kernel-report-training/v1' or not d['synthetic']:raise Invalid('unsupported-scope')
 v=obj(d.get('version'));typed(v,'origin',str);typed(v,'id',str);typed(v,'recent_check',bool)
 strings(d.get('conditions'))
 r=obj(d.get('reproducer'))
 for k in ['format','trigger','confirm','trace_id']:typed(r,k,str)
 c=obj(d.get('boundary_claim'));typed(c,'operation',str);typed(c,'permitted',bool)
 ids=set()
 for t in d['traces']:
  obj(t)
  for k in ['id','version','trigger','observation','operation']:typed(t,k,str)
  for k in ['reproduced','permitted','production']:typed(t,k,bool)
  strings(t.get('conditions'))
  if t['id'] in ids:raise Invalid('duplicate-trace-id')
  ids.add(t['id'])
  if 'specimen' in t:
   s=obj(t['specimen'])
   for k in ['actor','owner','mode']:typed(s,k,str)
 for b in d['public_text']:
  obj(b);typed(b,'kind',str);typed(b,'text',str)
  if b['kind'] not in ['summary','reproducer','availability']:raise Invalid('unknown-block-kind')
 return d

def replay(specimen):
 """Fixed harmless toy: no payload, process execution, file or network access."""
 if not specimen or not specimen['actor'].strip() or not specimen['owner'].strip() or specimen['mode'] not in ['buggy','fixed']:return None
 expected=specimen['actor']==specimen['owner']
 permitted=specimen['mode']=='buggy' or expected
 return {'permitted':permitted,'expected_permitted':expected,'observation':'access-granted' if permitted else 'access-denied','operation':'read-training-record'}

def assess(d):
 shape(d);issues=[];v=d['version'];r=d['reproducer'];c=d['boundary_claim']
 stable=re.fullmatch(r'(?:[0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-rc[0-9]+)?|[0-9a-f]{40})',v['id']) is not None
 if v['origin']!='kernel.org' or not stable:issues.append('stable-upstream-version-needed')
 if not v['recent_check']:issues.append('recent-code-check-needed')
 if not d['description'].strip():issues.append('description-needed')
 if r['format'] not in ['source','instructions']:issues.append('nonbinary-reproducer-needed')
 if not r['trigger'].strip() or not r['confirm'].strip():issues.append('trigger-and-confirm-needed')
 trace=next((t for t in d['traces'] if t['id']==r['trace_id']),None)
 result=None
 if trace is None:issues.append('selected-trace-needed')
 else:
  if trace['version']!=v['id']:issues.append('trace-version-mismatch')
  if trace['conditions']!=d['conditions']:issues.append('trace-conditions-mismatch')
  if trace['trigger']!=r['trigger']:issues.append('trace-trigger-mismatch')
  if trace['observation']!=r['confirm']:issues.append('trace-confirmation-mismatch')
  result=replay(trace.get('specimen'))
  if result is None:issues.append('supported-replay-specimen-needed')
  elif not (trace['reproduced'] and trace['permitted']==result['permitted'] and trace['observation']==result['observation'] and r['confirm']==result['observation'] and trace['operation']==result['operation'] and r['trigger']==result['operation']):issues.append('replay-contradicts-trace')
 evidence='needs-evidence' if issues else 'corroborated-synthetic'
 boundary='unestablished'
 if evidence=='corroborated-synthetic' and result:
  if c['operation']!=result['operation'] or c['permitted']!=result['expected_permitted']:issues.append('boundary-claim-mismatch')
  elif trace['production'] and not c['permitted'] and result['permitted']:boundary='supported-synthetic'
  else:boundary='not-supported'
 if not d['ai_assisted']:disclosure='not-assessed'
 elif any(b['kind']=='reproducer' and b['text'].strip() for b in d['public_text']):disclosure='withhold-reproducer'
 elif any(b['kind']=='availability' and b['text'].strip() for b in d['public_text']):disclosure='public-status-only'
 else:disclosure='needs-availability-statement'
 return {'evidence':evidence,'boundary':boundary,'disclosure':disclosure,'issues':issues,'replay':result,'limits':'Synthetic consistency and toy replay only; no real-kernel validity, authenticity, urgency, severity, free-text leak detection or submission approval.'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
 try:
  raw=pathlib.Path(a.input).read_bytes()
  if len(raw)>1_000_000:raise Invalid('input-too-large')
  d=json.loads(raw);out=assess(d);rc=0
 except (OSError,ValueError,UnicodeError,RecursionError) as e:
  out={'evidence':'invalid','boundary':'unestablished','disclosure':'not-assessed','issues':[str(e)]};rc=2
 print(json.dumps(out,sort_keys=True));return rc
if __name__=='__main__':sys.exit(main())
