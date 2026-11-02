import pathlib,urllib.request,datetime,hashlib,json
root=pathlib.Path(__file__).resolve().parents[3]
items=[('S108','https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.md','corpus/source-snapshots/round-62'),('S109','https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md','.ufo/waves/round-62/reject')]
for sid,url,d in items:
 p=root/d;p.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(url,timeout=40) as r: raw=r.read();status=r.status
 (p/(sid+'.txt')).write_bytes(raw)
 rec={'id':sid,'url':url,'capture_url':url,'fetched_utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'http':{'status':status},'kind':'markdown','path':sid+'.txt','sha256':hashlib.sha256(raw).hexdigest(),'quotes':[]}
 (p/'manifest.json').write_text(json.dumps({'schema_version':1,'sources':[rec]},indent=2)+'\n')
 print(sid,status,len(raw),rec['sha256'])
