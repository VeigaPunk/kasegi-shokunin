#!/usr/bin/env bash
# Round-85 C2 pre-freeze controls over the frozen counter c2/e2e-check.py.
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-85
S=${1:?scratch}; mkdir -p "$S"
C="python3 -B $W/c2/e2e-check.py --lane $L"
PKG=$L/corpus/practice/curl-h1-1913733
echo "counter_sha256=$(sha256sum $W/c2/e2e-check.py | cut -d' ' -f1) gate_sha256=$(sha256sum $L/corpus/instruments/claim-package-check.py | cut -d' ' -f1)"
echo "== control donothing: package path absent (expected fail)"; test -e "$PKG" && echo "PKG EXISTS?!"; $C --pkg "$PKG"; echo "rc=$?"
rm -rf "$S/exemplar"; cp -r $L/corpus/instruments/fixtures/claim-package/exemplar "$S/exemplar"
echo "== control exemplar-copy: r43 shape-valid curl exemplar (expected fail: E1 pass, E2/E3/E5 fail)"; $C --pkg "$S/exemplar"; echo "rc=$?"
mk() { cat > "$S/$1.md" <<R
# pricing control $1
## Pricing
price-program: curl
price-severity: ${SEV:-Medium}
price-reward-at-disclosure: ${RWD:-2400 USD}
price-platform-bounty-flag: ${FLG:-false}
price-reward-current-policy: ${POL:-none}
price-cvss: ${CVS:-not-set-by-vendor}
price-kev: ${KEV:-not-listed (CVE id absent from the round-35 S052 capture)}
price-cve: ${CVE:-CVE-2023-28319}
> Severity: Medium
> Bug bounty: 2400 USD
> ${Q3:-There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.}
## Next
R
echo "== pricing control $1 (expected $2)"; $C --pricing-only "$S/$1.md"; echo "rc=$?"; }
mk positive-pricing pass
SEV=High mk forged-severity fail
RWD="505 USD" mk forged-reward-exemplar fail
FLG=true mk forged-platform-flag fail
POL="500 USD" mk forged-current-policy fail
CVS="6.3" mk forged-cvss fail
KEV="listed" mk forged-kev fail
CVE="CVE-2025-9086" mk forged-cve fail
Q3="The curl project pays 2400 USD for every Medium report." mk forged-quote fail
