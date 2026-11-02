import json,hashlib,pathlib,subprocess,datetime
root=pathlib.Path(__file__).parent
raw=(root/'cases.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==json.loads((root/'FREEZE.json').read_text())['sha256']
expected_map={'affected':('affected',0),'not_affected':('unaffected',0),'could_not_evaluate':('unsupported',2),'invalid':('invalid',3)}
print('run_utc='+datetime.datetime.now(datetime.timezone.utc).isoformat());print('candidate=9b1028c00656d2693f4accc513e14c4c180a2f27')
fail=0
for c in json.loads(raw):
 p=subprocess.run(['python3','-B',str(root/'candidate/corpus/instruments/osv-affectedness.py')],input=json.dumps({k:c[k] for k in ('package','version','osv')}),capture_output=True,text=True)
 got=json.loads(p.stdout); want,code=expected_map[c['expected']];ok=got.get('status')==want and p.returncode==code;fail+=not ok
 print(json.dumps({'id':c['id'],'pass':ok,'expected_status':want,'expected_exit':code,'actual':got,'exit':p.returncode}))
print(f'cases=47 mismatches={fail}')
