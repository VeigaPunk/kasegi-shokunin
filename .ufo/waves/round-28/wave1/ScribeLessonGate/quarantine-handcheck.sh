#!/usr/bin/env bash
# Round-28 wave-1 ScribeLessonGate: independent hand-check of the 7 kasegi register rows.
# Read-only network fetch with the lane instrument UA (corpus/instruments/capture-source.py:32).
set -u
UA='kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)'
D="$(cd "$(dirname "$0")" && pwd)"
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md

rows=(
 'S037|https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A|html|发布日期'
 'S048|https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3|html|项目周期'
 'S054|https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf|pdf|府連第7号'
 'S065|http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf|pdf|刑法（7 件）'
 'S068|https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html|html|ISO/IEC 29147:2018'
 'S069|https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_WD_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf|pdf|6.3.1'
 'S070|https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_DI_2025005470_%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF%20%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%E5%88%86%E7%B1%BB%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97.pdf|pdf|工作简况'
)

printf '%s\n' "== round-28 wave-1 quarantine hand-check (read-only; UA from capture-source.py:32) =="
printf '%s\n' "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
for spec in "${rows[@]}"; do
  id=${spec%%|*}; rest=${spec#*|}
  url=${rest%%|*}; rest=${rest#*|}
  kind=${rest%%|*}; frag=${rest#*|}
  out="$D/$id.body"; err="$D/$id.stderr"
  code=$(curl -sS -L --max-time 60 -A "$UA" -o "$out" -w '%{http_code}' "$url" 2>"$err"); rc=$?
  bytes=$(wc -c <"$out" 2>/dev/null || echo 0)
  txt="$out"; if [ "$kind" = pdf ]; then txt="$D/$id.txt"; pdftotext -enc UTF-8 -layout "$out" "$txt" 2>/dev/null || true; fi
  # normalize: strip tags, collapse whitespace
  norm="$D/$id.norm"
  if [ "$kind" = html ]; then sed -e 's/<[^>]*>/ /g' -e 's/&nbsp;/ /g' "$txt" | tr -s ' \t\r\n' ' ' >"$norm"; else tr -s ' \t\r\n' ' ' <"$txt" >"$norm" 2>/dev/null || : >"$norm"; fi
  nfrag=$(printf '%s' "$frag" | tr -s ' \t\r\n' ' ')
  occ=$(grep -o -F "$nfrag" "$norm" 2>/dev/null | wc -l)
  printf '%s code=%s rc=%s bytes=%s kind=%s anchor="%s" occurrences=%s\n' "$id" "$code" "$rc" "$bytes" "$kind" "$frag" "$occ"
  [ -s "$err" ] && sed -n '1,2p' "$err" | sed "s/^/    stderr: /"
done
