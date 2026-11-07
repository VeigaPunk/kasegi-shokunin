#!/usr/bin/env bash
# Round-86 C2 pre-freeze controls over the frozen counter c2/e2e-check.py.
# Usage: c2-controls-r86.sh SCRATCH_DIR   (writes only under SCRATCH_DIR)
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-86
S=${1:?scratch}; mkdir -p "$S"
C="python3 -B $W/c2/e2e-check.py --lane $L"
PKG=$L/corpus/practice/curl-ibb-h1-1997312
R85=$L/corpus/practice/curl-h1-1913733
SN=$L/corpus/source-snapshots/round-86
echo "counter_sha256=$(sha256sum $W/c2/e2e-check.py | cut -d' ' -f1) gate_sha256=$(sha256sum $L/corpus/instruments/claim-package-check.py | cut -d' ' -f1)"
echo "== control donothing: package path absent (expected fail)"; test -e "$PKG" && echo "PKG EXISTS?!"; $C --pkg "$PKG"; echo "rc=$?"
echo "== control r85-package: the round-85 1913733 package unchanged (expected fail)"; $C --pkg "$R85"; echo "rc=$?"
rm -rf "$S/exemplar"; cp -r $L/corpus/instruments/fixtures/claim-package/exemplar "$S/exemplar"
echo "== control exemplar-copy: r43 shape-valid exemplar (expected fail)"; $C --pkg "$S/exemplar"; echo "rc=$?"
PRICING='## Pricing

price-program: ibb
price-payer: internet-bug-bounty
price-severity: medium
price-reward-at-disclosure: 2400 USD
price-platform-bounty-flag: true
price-original-report: 1913733
price-reward-current-policy: ended 2026-01-31
price-kev: not-listed catalogVersion 2026.10.23
price-cve: CVE-2023-28319

> I would like to especially highlight the awesome Internet Bug Bounty project, which has paid the bounties for us for many years.
> There is no longer a curl bug-bounty program. It officially stops on January 31, 2026.
> Bug bounty: 2400 USD
'
# B3-class wrong subject: the r85 package with S122/S123 evidence bound and a fully correct r86 Pricing block.
rm -rf "$S/b3"; cp -r "$R85" "$S/b3"; cp "$SN/S122.txt" "$SN/S123.txt" "$S/b3/evidence/"
python3 - "$S/b3" <<'PY'
import hashlib, json, re, sys
p = sys.argv[1]
m = json.load(open(p + "/evidence/manifest.json"))
for sid in ("S122", "S123"):
    b = open("%s/evidence/%s.txt" % (p, sid), "rb").read()
    m["artifacts"].append({"path": sid + ".txt", "sha256": hashlib.sha256(b).hexdigest()})
json.dump(m, open(p + "/evidence/manifest.json", "w"), indent=1)
PY
python3 - "$S/b3/report.md" "$PRICING" <<'PY'
import re, sys
t = open(sys.argv[1]).read()
t = re.sub(r"^## Pricing\s*$.*?(?=^## )", sys.argv[2] + "\n", t, flags=re.M | re.S)
open(sys.argv[1], "w").write(t)
PY
echo "== control b3-wrong-subject: r85 package + S122/S123 evidence + correct r86 pricing (expected fail E0)"; $C --pkg "$S/b3"; echo "rc=$?"
sed -i '0,/^Program: curl$/s//Program: curl\nIBB record: https:\/\/hackerone.com\/reports\/1997312/' "$S/b3/report.md"
echo "== control b3-url-added: same, 1997312 URL added, heading still 1913733 (expected fail E0)"; $C --pkg "$S/b3"; echo "rc=$?"
mk() { { printf '%s\n' "${HEAD:-# HackerOne 1997312 (IBB): CVE-2023-28319 payer record (retrospective practice package)}" "" "Record: https://hackerone.com/reports/1997312" "Original: https://hackerone.com/reports/${ORIG_URL:-1913733}" ""
  printf '%s' "$PRICING" | sed \
   -e "s/^price-program: .*/price-program: ${PRG:-ibb}/" -e "s/^price-payer: .*/price-payer: ${PAY:-internet-bug-bounty}/" \
   -e "s/^price-severity: .*/price-severity: ${SEV:-medium}/" -e "s/^price-reward-at-disclosure: .*/price-reward-at-disclosure: ${RWD:-2400 USD}/" \
   -e "s/^price-platform-bounty-flag: .*/price-platform-bounty-flag: ${FLG:-true}/" -e "s/^price-original-report: .*/price-original-report: ${ORG:-1913733}/" \
   -e "s/^price-reward-current-policy: .*/price-reward-current-policy: ${POL:-ended 2026-01-31}/" -e "s/^price-kev: .*/price-kev: ${KEV:-not-listed catalogVersion 2026.10.23}/" \
   -e "s/^price-cve: .*/price-cve: ${CVE:-CVE-2023-28319}/"
  printf '%s' "${EXTRA:-}"; printf '\n## Next\n'; } > "$S/$1.md"
  echo "== pricing control $1 (expected $2)"; $C --pricing-only "$S/$1.md"; echo "rc=$?"; }
mk positive-pricing pass
PRG=curl mk forged-program fail
PAY=curl mk forged-payer-vendor fail
SEV=high mk forged-severity fail
RWD="505 USD" mk forged-reward fail
FLG=false mk forged-platform-flag fail
ORG=1997312 mk forged-original-report fail
POL=none mk forged-current-policy-none fail
POL="ended 2026-01-26" mk forged-current-policy-date fail
KEV=listed mk forged-kev fail
CVE=CVE-2025-9086 mk forged-cve fail
HEAD="# HackerOne 1913733: CVE-2023-28319 (retrospective practice package)" mk wrong-subject-heading fail
ORIG_URL=1913734 mk stray-report-url fail
EXTRA='price-payer: internet-bug-bounty
' mk duplicate-key fail
EXTRA='
## Pricing

price-payer: curl
' mk two-pricing-sections fail
EXTRA='> 
> a
' mk short-quotes fail
EXTRA='> The curl project pays 2400 USD for every Medium report via the IBB.
' mk forged-quote fail
# no S123 quote: drop the two S123 quote lines, keep three non-S123 quotes
PRICING_SAVE=$PRICING
PRICING=$(printf '%s' "$PRICING_SAVE" | grep -v '^> I would like\|^> There is no longer'; printf '\n> Original report: https://hackerone.com/reports/1913733\n> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.\n')
mk no-s123-quote fail
PRICING=$PRICING_SAVE
