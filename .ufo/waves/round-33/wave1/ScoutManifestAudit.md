# ScoutManifestAudit — snapshot-manifest inventory (read-only)

Seat: ScoutManifestAudit (kasegi-shokunin round 33). Tree audited: `git archive 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 corpus/source-snapshots corpus/SOURCES.md` extracted into scratch (the BASE bytes; HEAD a6a5023 has the same corpus bytes per the diff check below). My first pass ran against the live working copy while ExecManifestUpgrade was editing manifests (it then showed 38/38 url+archival), so it was discarded; the inventory below is the quiescent base. Model: anthropic/claude-sonnet-5-5. Nothing in the lane was written except this receipt. Method: script (appendix) walks `corpus/source-snapshots/*/`, recomputes SHA-256 of every record's `path` file, and finds the registry row by id in `corpus/SOURCES.md` (URL = trailing `https://…` of the source cell, the text after ` — `).

## Headline findings (what the upgraders must know)

1. **No manifest record carries `url`, `fetched_utc` or `archival`** (0 of 38; the three field counts are in Totals). All 38 legacy records have shape `{id, path, sha256, quotes}`. Top-level manifest keys are `schema_version`, `purpose`, `sources` (list); records live under `sources`. JSON indent differs by file: 2-space in round-23/24/29/30, 1-space in round-25/26/28/31 (measured on line 2) — preserve each file's indent (or normalise all) so the diff stays a field insertion.
2. **round-32 has NO `manifest.json`**: dir holds only `S049.txt`, `S050.txt` (Rule A failure at base). S049/S050 have no SOURCES.md rows yet at this tree (registry ends at S048, 48 rows), so their `url` cannot be copied from a row until ExecRegistryAppend lands rows; the contract gives the URLs (zc.cnvd.org.cn/news/helpList, security.360.cn/Reward/rules).
3. **All 38 records: path file exists and SHA-256 recomputed equals the manifest value** (path_missing=0, sha_mismatch=0).
4. **Registry-row URL binding is NOT unique for three records by naive URL match** — this is a Rule B hazard for ExecCaptureBinding:
   - `S029` (round-23): URL `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng` is carried by rows **S024 and S029** (S029 row text says it supersedes S024).
   - `S006` (round-24): URL `https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq` is carried by rows **S006 and S028** (S028 is a REJECTED duplicate-row proposal).
   - `S048` (round-31): the URL occurs once as a row URL (row S048) but **twice as raw text** in SOURCES.md — second occurrence is a Search-log line (line 72) quoting it. A checker that greps URL text anywhere counts 2; a checker that parses only registry-row source cells counts 1. Per the contract ("grep for the URL text in the row's source cell"), restrict matching to `| Sxxx |` row source cells.
   Consequence: "url matches exactly one registry-row URL" fails for S029 and S006 unless the rule is "exactly one row with that URL **among rows for the record's id**" or the row-match is by (id, URL) pair. The contract's literal reading (URL occurs in exactly one row) makes C1's `unbound=0` unattainable for S006 and S029 without a SOURCES.md change (not in anyone's scope: ExecRegistryAppend only appends S049/S050) — escalate to Main/L1 to rule before ExecCaptureBinding fixes semantics. Recommended reading: bind on the row whose id equals the record id and require that row's URL to equal `url` byte-for-byte; flag ≥2 rows with identical URL only when the record's own id row is not unique.
5. **Id S041 is recorded in three manifests** (round-26, round-28, round-30), byte-identical captures (`e18acbf99d13…5ab47` in all three). Rule B binds each record independently; the checker's record counting (40 total) counts all three.
6. **Uncovered captured file: `round-26/S040-live.txt`** — present in the dir, no record in the round-26 manifest (its `purpose` says S040 was skipped because the fetch had not landed). Its sha256 `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c` is identical to `round-25/S040.txt`, which IS recorded in the round-25 manifest. Rule A as written (a dir has a manifest) passes for round-26; the contract does not require every file to have a record. Do not add a record for it unless the claim is widened; ExecManifestUpgrade must not invent one (record count 38 → 40 with S049/S050 relies on this).
7. Record count check: 4+19+5+1+2+3+3+1 = 38 legacy (23,24,25,26,28,29,30,31) + 2 (round-32) = 40 = `records=40` in C1.

## Per-directory inventory (BASE 690b69d)

### round-23

Files (5): S018.txt, S029.txt, S030.txt, S031.txt, manifest.json

records=4; captured files with no record: none

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S018 | S018.txt | `d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4` | ok | YES | no | no | no | https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1 | S018 | 1 |
| S029 | S029.txt | `82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c` | ok | YES | no | no | no | https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng | S024,S029 | 2 |
| S030 | S030.txt | `673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019` | ok | YES | no | no | no | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf | S030 | 1 |
| S031 | S031.txt | `3c7ae8ba56df4e0c1d619956b894b5c3e3a7c9e35c8e1112576f521322460678` | ok | YES | no | no | no | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | S031 | 1 |

### round-24

Files (20): S001.txt, S002.txt, S003.txt, S004.txt, S005.txt, S006.txt, S007.txt, S008.txt, S009.txt, S010.txt, S011.txt, S012.txt, S013.txt, S014.txt, S015.txt, S032.txt, S033.txt, S034.txt, S035.txt, manifest.json

records=19; captured files with no record: none

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | S001.txt | `d3522c8cdceedb2a47b7ff278fde5d1365939aeb0015c3865d5c1307c3a39d61` | ok | YES | no | no | no | https://www.first.org/cvss/v4.0/user-guide | S001 | 1 |
| S002 | S002.txt | `abc8f152084ae267b047d32f2bcc9deb197fc268f84029e655a858da665f7add` | ok | YES | no | no | no | https://www.first.org/cvss/v4.0/specification-document | S002 | 1 |
| S003 | S003.txt | `b659e385f873799a798748a0d3f51c26b237c89e83b64918a9f993b00e7f6768` | ok | YES | no | no | no | https://www.cisa.gov/resources-tools/resources/establishing-coordinated-vulnerability-disclosure-program-work-security-researchers | S003 | 1 |
| S004 | S004.txt | `4c736465f09d685a619cc9ee35f24accbfb05a4493f77de91d71511ca7f6440b` | ok | YES | no | no | no | https://certcc.github.io/certcc_disclosure_policy/ | S004 | 1 |
| S005 | S005.txt | `e98828e95cd0842c60cbe18c87c27b2d97e55d41e50e199af72941306d209c47` | ok | YES | no | no | no | https://projectzero.google/vulnerability-disclosure-faq.html | S005 | 1 |
| S006 | S006.txt | `c3ed0ad19240df6303ac03bd3020ceb55ccc01a3ad082c96674bd5dab51f60a5` | ok | YES | no | no | no | https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq | S006,S028 | 2 |
| S007 | S007.txt | `b6a0c1412cdc2d225dcc8e4073a3979f4a3e6e25b5b3b8bea1b9b1b10cb2f7be` | ok | YES | no | no | no | https://docs.bugcrowd.com/researchers/disclosure/disclose-io-and-safe-harbor/ | S007 | 1 |
| S008 | S008.txt | `e7cce9e119a886a3727f09a25b78840b341c5c1b24e1d77f2e6274fffd358dd6` | ok | YES | no | no | no | https://www.cisa.gov/vulnerability-disclosure-policy-template | S008 | 1 |
| S009 | S009.txt | `e088c0d8b2f7d0343a8bde639593034d290d3641c6687520acf141adb221d74e` | ok | YES | no | no | no | https://www.ncsc.gov.uk/blogs/10-questions-ask-using-ai-models-find-vulnerabilities | S009 | 1 |
| S010 | S010.txt | `f22f8c63e55e3047f0feb52da4b6556c41b1a07a97b1b270a842858229b67054` | ok | YES | no | no | no | https://projectzero.google/2024/06/project-naptime.html | S010 | 1 |
| S011 | S011.txt | `6f0304f88a738b622e7bfbc48ee7f416350713b81d3b813ef7ece35d74a6cc43` | ok | YES | no | no | no | https://blog.cloudflare.com/cyber-frontier-models/ | S011 | 1 |
| S012 | S012.txt | `3d36446a1e5448912c6e99ad665f27e69cc14afacc1de79a12c08c4fb6492d89` | ok | YES | no | no | no | https://www.anthropic.com/research/glasswing-initial-update | S012 | 1 |
| S013 | S013.txt | `9f89577f6cccadf891a123f63c208d4e30b0bc2e41d2f746e1d043c3ed65f860` | ok | YES | no | no | no | https://cwe.mitre.org/top25/archive/2025/2025_methodology.html | S013 | 1 |
| S014 | S014.txt | `b59d2f569c306c8f41a4bb0491bfa063fda4434a03a3bc7e5dcb2d3b8774081b` | ok | YES | no | no | no | https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html | S014 | 1 |
| S015 | S015.txt | `d3128dfc6c9b1e0f7fcaab32f2e1d6c1f8260e63bb7077649699cb2b80543de0` | ok | YES | no | no | no | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html | S015 | 1 |
| S032 | S032.txt | `910b82414146007b949d3f239d2004e854288c20b0ea13b466360582a3a68849` | ok | YES | no | no | no | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf | S032 | 1 |
| S033 | S033.txt | `d3228e8949fcfdf23f9f84a45d16dcc2831b572c2854b191d7ca8b4f7616618d` | ok | YES | no | no | no | https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 | S033 | 1 |
| S034 | S034.txt | `b08bee0989d419092bf40960a8724b04548dfd70c8ddf9ccd86b36f2aca5167e` | ok | YES | no | no | no | https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/ | S034 | 1 |
| S035 | S035.txt | `9be52746905098a8ff38985b789353534e7b0532f70f4a805b8ac5d84842be6d` | ok | YES | no | no | no | https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf | S035 | 1 |

### round-25

Files (6): S036.txt, S037.txt, S038.txt, S039.txt, S040.txt, manifest.json

records=5; captured files with no record: none

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S036 | S036.txt | `022ca4f40b9e07a4e052c4d6ac8a9b4195503489417eb7fd0760d28c35ceb950` | ok | YES | no | no | no | https://cybozu.co.jp/company/security-policy/ | S036 | 1 |
| S037 | S037.txt | `b204aa7f60ec2e70713ecd8c605fb1adb6e39549f0ef09d32a297c10f473cb4c` | ok | YES | no | no | no | https://cybozu.co.jp/products/bug-bounty/faq/ | S037 | 1 |
| S038 | S038.txt | `09e077d31ce3b5e366fa435f5c474db7405eef8dd313b64be46f88047dabb68a` | ok | YES | no | no | no | https://pepabo.com/contact/vulnerability-reporting/ | S038 | 1 |
| S039 | S039.txt | `657e7b4c67e67d00b190b31942d749a28d0988f15d1e6f5f506130accffc191d` | ok | YES | no | no | no | https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html | S039 | 1 |
| S040 | S040.txt | `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c` | ok | YES | no | no | no | https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html | S040 | 1 |

### round-26

Files (3): S040-live.txt, S041.txt, manifest.json

records=1; captured files with no record: ['S040-live.txt']

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S041 | S041.txt | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` | ok | YES | no | no | no | https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf | S041 | 1 |

### round-28

Files (3): S041.txt, S042.txt, manifest.json

records=2; captured files with no record: none

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S041 | S041.txt | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` | ok | YES | no | no | no | https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf | S041 | 1 |
| S042 | S042.txt | `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` | ok | YES | no | no | no | https://www.ipa.go.jp/security/todokede/vuln/process.html | S042 | 1 |

### round-29

Files (4): S043.txt, S044.txt, S045.txt, manifest.json

records=3; captured files with no record: none

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S043 | S043.txt | `d3b815ed75e3e32b2ae363b9f612c3d25b9c8c585df2c4cd797296f2ded69199` | ok | YES | no | no | no | https://hackerone.com/security/policy_versions | S043 | 1 |
| S044 | S044.txt | `8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf` | ok | YES | no | no | no | https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md | S044 | 1 |
| S045 | S045.txt | `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86` | ok | YES | no | no | no | https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json | S045 | 1 |

### round-30

Files (4): S041.txt, S046.txt, S047.txt, manifest.json

records=3; captured files with no record: none

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S046 | S046.txt | `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3` | ok | YES | no | no | no | https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf | S046 | 1 |
| S047 | S047.txt | `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4` | ok | YES | no | no | no | https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html | S047 | 1 |
| S041 | S041.txt | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` | ok | YES | no | no | no | https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf | S041 | 1 |

### round-31

Files (2): S048.txt, manifest.json

records=1; captured files with no record: none

| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |
|---|---|---|---|---|---|---|---|---|---|---|
| S048 | S048.txt | `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55` | ok | YES | no | no | no | https://www.microsoft.com/en-us/msrc/msvr | S048 | 2 |

### round-32

Files (2): S049.txt, S050.txt

**NO manifest.json**; captured source files present: S049.txt, S050.txt


## Totals (JSON)
{"dirs": 9, "recs": 38, "dirs_without_manifest": 1, "path_missing": 0, "sha_mismatch": 0, "with_url": 0, "with_fetched_utc": 0, "with_archival": 0}

## URL-binding ambiguities (rows sharing the URL != 1 OR URL text occurrences != 1)

| round | id | url | rows sharing URL | occurrences |
|---|---|---|---|---|
| round-23 | S029 | https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng | S024,S029 | 2 |
| round-24 | S006 | https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq | S006,S028 | 2 |
| round-31 | S048 | https://www.microsoft.com/en-us/msrc/msvr | S048 | 2 |

## Ids recorded in more than one manifest
S041: round-26, round-28, round-30

Registry rows at this tree: 48; highest id S048; S049/S050 rows present: False


## Appendix — audit script (stdlib; ran with cwd = lane root, from scratch dir later deleted)

```python
import json,hashlib,os,re,glob
from collections import Counter
rows={}
for ln in open('corpus/SOURCES.md',encoding='utf-8'):
    m=re.match(r'\| (S\d{3}) \| ',ln)
    if not m: continue
    src=ln.split(' | ')[1]
    um=re.search(r'(https?://\S+)\s*$',src)
    rows[m.group(1)]=um.group(1) if um else None
urls={}
for i,u in rows.items(): urls.setdefault(u,[]).append(i)
text=open('corpus/SOURCES.md',encoding='utf-8').read()
out=[];tot=dict(dirs=0,recs=0,dirs_without_manifest=0,path_missing=0,sha_mismatch=0,with_url=0,with_fetched_utc=0,with_archival=0)
inv=[]
for d in sorted(glob.glob('corpus/source-snapshots/*/')):
    name=os.path.basename(d.rstrip('/'));files=sorted(os.listdir(d));tot['dirs']+=1
    out.append(f'\n### {name}\n\nFiles ({len(files)}): '+', '.join(files))
    mp=os.path.join(d,'manifest.json')
    if not os.path.exists(mp):
        tot['dirs_without_manifest']+=1
        out.append(f'\n**NO manifest.json**; captured source files present: {", ".join(files)}\n');continue
    recs=json.load(open(mp,encoding='utf-8'))['sources']
    paths={r['path'] for r in recs}
    orphan=[f for f in files if f!='manifest.json' and f not in paths]
    out.append(f'\nrecords={len(recs)}; captured files with no record: {orphan or "none"}\n')
    out.append('| id | path | sha256 (manifest) | path file | sha match | url | fetched_utc | archival | registry-row URL (row with same id) | rows carrying that URL | occurrences of URL text in SOURCES.md |')
    out.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for r in recs:
        tot['recs']+=1
        for k,t in (('url','with_url'),('fetched_utc','with_fetched_utc'),('archival','with_archival')):
            if k in r: tot[t]+=1
        fp=os.path.join(d,r['path'])
        if not os.path.exists(fp): fs='MISSING';sm='n/a';tot['path_missing']+=1
        else:
            h=hashlib.sha256(open(fp,'rb').read()).hexdigest();fs='ok'
            sm='YES' if h==r['sha256'] else f'NO (actual {h})'
            if h!=r['sha256']: tot['sha_mismatch']+=1
        ru=rows.get(r['id']);same=urls.get(ru,[]) if ru else [];occ=text.count(ru) if ru else 0
        out.append(f"| {r['id']} | {r['path']} | `{r['sha256']}` | {fs} | {sm} | {'yes' if 'url' in r else 'no'} | {'yes' if 'fetched_utc' in r else 'no'} | {'yes' if 'archival' in r else 'no'} | {ru or 'NO ROW'} | {','.join(same)} | {occ} |")
        inv.append((name,r['id'],ru,same,occ))
out.append('\n## Totals (JSON)\n'+json.dumps(tot))
out.append('\n## URL-binding ambiguities (rows sharing the URL != 1 OR URL text occurrences != 1)\n')
out.append('| round | id | url | rows sharing URL | occurrences |\n|---|---|---|---|---|')
for n,i,u,s,o in inv:
    if len(s)!=1 or o!=1: out.append(f'| {n} | {i} | {u} | {",".join(s)} | {o} |')
c=Counter(i for n,i,*_ in inv)
out.append('\n## Ids recorded in more than one manifest\n'+'; '.join(f'{i}: '+', '.join(n for n,j,*_ in inv if j==i) for i,k in c.items() if k>1))
out.append(f'\nRegistry rows at this tree: {len(rows)}; highest id {max(rows)}; S049/S050 rows present: {"S049" in rows or "S050" in rows}')
print('\n'.join(out))
```

## Cleanup
Scratch `$HYAKU_SCRATCH/kasegi-r33/ScoutManifestAudit/` removed on exit (trap).

## Live-tree spot check (IN-FLIGHT, non-comparative per bound 6; not a base number)

Run after ExecManifestUpgrade/ExecManifest32 had edited manifests (`git status` showed 8 legacy manifests modified; round-32/manifest.json present, 2 records, fetched_utc on both): 40 records; every manifest `sha256` still equals the recomputed file hash; every `url` equals the SOURCES.md row URL of the same id **except S049/S050**, whose registry rows were not yet appended (rows=48). Output: `records 40 rows 48 mismatches [('S049','url!=row', …, None), ('S050','url!=row', …, None)]`. Re-run on quiescent bytes once ExecRegistryAppend lands.
