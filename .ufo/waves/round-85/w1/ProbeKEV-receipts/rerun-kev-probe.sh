#!/usr/bin/env bash
# ProbeKEV re-run: does CVE-2023-28319 appear in the CISA KEV catalog,
# in the lane capture (round-35 S052) and in the live feed?
# Writes only inside its own scratch. Read-only against the lane tree.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S="${TMPDIR:-/fast/scratch/hyaku/kasegi-r85/ProbeKEV}/rerun-kev-probe"
mkdir -p "$S"
export TMPDIR="$S"
trap 'rm -rf -- "$S"' EXIT
cd "$LANE" || exit 1

C=corpus/source-snapshots/round-35/S052.txt
L="$S/kev-live.json"

echo "### A. lane capture: $C"
sha256sum "$C"
grep -n '"catalogVersion"' "$C"
grep -n '"dateReleased"' "$C"
grep -n '"count"' "$C"
printf 'cveID entries: '; grep -c '"cveID"' "$C"
printf 'CVE-2023-28319 count: '; grep -c 'CVE-2023-28319' "$C"
printf 'CVE-2023-28319 (loose 28319) count: '; grep -c -i '28319' "$C"
printf 'CVE-2023-38545 count: '; grep -c 'CVE-2023-38545' "$C"
printf 'CVE-2021-44228 count (positive control): '; grep -c 'CVE-2021-44228' "$C"
printf 'curl mentions: '; grep -c -i 'curl' "$C"

echo
echo "### B. live feed"
curl -sS -L -o "$L" \
  -w 'HTTP_STATUS=%{http_code}\nURL_EFFECTIVE=%{url_effective}\nSIZE=%{size_download}\n' \
  https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
sha256sum "$L"
grep -n -m1 '"catalogVersion"' "$L"
grep -n -m1 '"dateReleased"' "$L"
grep -n -m1 '"count"' "$L"
printf 'cveID entries: '; grep -c '"cveID"' "$L"
printf 'CVE-2023-28319 count: '; grep -c 'CVE-2023-28319' "$L"
printf 'CVE-2023-38545 count: '; grep -c 'CVE-2023-38545' "$L"
printf 'CVE-2021-44228 count (positive control): '; grep -c 'CVE-2021-44228' "$L"
printf 'curl mentions: '; grep -c -i 'curl' "$L"

echo
echo "### C. structural membership check (python3 -B)"
python3 -B - "$C" "$L" <<'PY'
import json, sys
for p in sys.argv[1:]:
    d = json.load(open(p, encoding="utf-8"))
    ids = [v["cveID"] for v in d["vulnerabilities"]]
    print(p)
    print("  catalogVersion =", d["catalogVersion"], "count_field =", d["count"],
          "len =", len(ids), "unique =", len(set(ids)))
    for c in ("CVE-2023-28319", "CVE-2023-38545", "CVE-2021-44228"):
        print("  ", c, "present =", c in ids)
PY
