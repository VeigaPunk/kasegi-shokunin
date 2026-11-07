#!/usr/bin/env bash
# Rebuild and re-run the CriticClaims C2 forgery (wrong-subject package that passes E1-E5).
# Writes only under its own scratch dir; reads lane bytes read-only.
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S=$(mktemp -d -p /fast/scratch/hyaku/kasegi-r85) 2>/dev/null || S=$(mktemp -d)
trap 'rm -rf -- "$S"' EXIT
cd "$LANE"
cp -r corpus/instruments/fixtures/claim-package/exemplar "$S/pkg"
cp corpus/source-snapshots/round-85/S119.txt corpus/source-snapshots/round-85/S120.txt "$S/pkg/evidence/"
python3 -B - "$S/pkg" <<'PY'
import json,sys,os,hashlib
pkg=sys.argv[1]; p=os.path.join(pkg,"evidence","manifest.json"); m=json.load(open(p))
for name in ("S119.txt","S120.txt"):
    h=hashlib.sha256(open(os.path.join(pkg,"evidence",name),"rb").read()).hexdigest()
    m["artifacts"].append({"path":name,"sha256":h,"bytes":os.path.getsize(os.path.join(pkg,"evidence",name)),"polarity":"positive","note":"snapshot copy"})
    m["redactions"].append({"artifact":name,"path":name,"artifact_sha256":h,"scanned_artifact_sha256":h,"producer":"forger","verifier":"forger-check","removed":[],"note":"public record"})
json.dump(m,open(p,"w"),indent=1,sort_keys=True)
sp=os.path.join(pkg,"status.json"); s=json.load(open(sp))
s["manifest_sha256"]=hashlib.sha256(open(p,"rb").read()).hexdigest()
json.dump(s,open(sp,"w"),indent=1,sort_keys=True)
PY
cat >> "$S/pkg/report.md" <<'MD'

## Pricing

> Severity: Medium
> Bug bounty: 2400 USD
> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.

price-severity: medium
price-reward-at-disclosure: 2400 USD
price-platform-bounty-flag: false
price-reward-current-policy: none
price-cvss: not-set-by-vendor
price-kev: not-listed
price-cve: CVE-2023-28319
MD
# scratch lane so E5's two path mentions hold; lane LOG.md/SHONEN.md are untouched
mkdir -p "$S/lane/corpus/practice" "$S/lane/corpus/instruments"
ln -s "$LANE/corpus/source-snapshots" "$S/lane/corpus/source-snapshots"
ln -s "$LANE/corpus/instruments/claim-package-check.py" "$S/lane/corpus/instruments/claim-package-check.py"
cp -r "$S/pkg" "$S/lane/corpus/practice/curl-h1-1913733"
cp LOG.md SHONEN.md "$S/lane/"
printf '\ntask: corpus/practice/curl-h1-1913733\n' >> "$S/lane/LOG.md"
printf '\nbox 2: corpus/practice/curl-h1-1913733\n' >> "$S/lane/SHONEN.md"
echo "== body subject"; grep -n 'CVE-\|reports/\|price-cve' "$S/pkg/report.md" | head
echo "== gate"; python3 -B corpus/instruments/claim-package-check.py "$S/pkg" | tail -1
echo "== e2e"; python3 -B .ufo/waves/round-85/c2/e2e-check.py --lane "$S/lane" --pkg "$S/lane/corpus/practice/curl-h1-1913733"; echo "rc=$?"
