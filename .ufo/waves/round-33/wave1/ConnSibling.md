# ConnSibling — sibling-overlap scan for F16 (round 33, wave 1)

Seat: ConnSibling (connector). Scope: read-only scan of six sibling lanes for
CNVD / 360SRC / Chinese crowdsourced-testing platform scope-or-reward ground,
plus province-contest reading. Lane write scope respected: this file only.

Date: 2026-10-26. Model route: config default (kimi-code/kimi-for-coding); no
model passed by hand (bound 10). No tools installed (nothing needed).

## Commands and output

### 1. Scoped-term sweep — corpus/README.md + corpus/knowledge of all six named siblings

Command (run from `/home/vgpnk/Projects/shokunin`):

```
for d in chousa-shokunin kengaku-shokunin kake-shokunin kagi-shokunin kumitate-shokunin kotoba-shokunin; do
  echo "=== $d corpus/README.md + knowledge ==="
  grep -rinE 'CNVD|360SRC|众测|zc\.cnvd\.org\.cn|security\.360\.cn|crowdsourced|Chinese' \
    "$d/corpus/README.md" "$d/corpus/knowledge/" 2>/dev/null | head -60
  echo "(exit $?)"
done
```

Per-lane verdict for the scoped terms (`CNVD|360SRC|众测|zc.cnvd.org.cn|
security.360.cn|crowdsourced`) — measured with a follow-up count command:

```
for d in chousa-shokunin kengaku-shokunin kake-shokunin kagi-shokunin kumitate-shokunin kotoba-shokunin; do
  n=$(grep -rinE 'CNVD|360SRC|众测|zc\.cnvd\.org\.cn|security\.360\.cn|crowdsourced' \
      "$d/corpus/README.md" "$d/corpus/knowledge/" 2>/dev/null | wc -l)
  c=$(grep -rin 'Chinese' "$d/corpus/README.md" "$d/corpus/knowledge/" 2>/dev/null | wc -l)
  echo "$d: scoped-terms=$n chinese-only=$c"
done
```

Output:

```
chousa-shokunin: scoped-terms=0 chinese-only=29
kengaku-shokunin: scoped-terms=0 chinese-only=0
kake-shokunin: scoped-terms=0 chinese-only=1
kagi-shokunin: scoped-terms=0 chinese-only=0
kumitate-shokunin: scoped-terms=0 chinese-only=3
kotoba-shokunin: scoped-terms=0 chinese-only=6
```

Result: ZERO hits for every F16-scoped term in all six siblings.

### 2. What the `Chinese` hits actually are (path:line)

All `Chinese` hits are unrelated to security platforms or crowdsourced testing:

- chousa-shokunin (29 hits): Chinese *academic research-method* documents —
  e.g. `chousa-shokunin/corpus/knowledge/chinese-search-record-r39.md:1` (a
  Chinese animal-experiment reporting copy's search record; CNKI/SinoMed/
  PRISMA-S), `chousa-shokunin/corpus/knowledge/cnki-citation-check-r40.md:6`,
  `chousa-shokunin/corpus/knowledge/istic-citation-verification-r39.md:1`
  (中国科学院 citation-verification service), `chousa-shokunin/corpus/knowledge/citation-count-semantics-r37.md:2` ("What a Chinese citation count actually counts"),
  `chousa-shokunin/corpus/knowledge/claim-support-test-r37.md:15` (CFEVER —
  Chinese-Wikipedia claims in an eval dataset).
- kake-shokunin (1 hit): `kake-shokunin/corpus/knowledge/js-rendering-queue.md:56` —
  "The Simplified-Chinese edition states the same rule" (a JS rendering-queue
  doc, web-properties domain).
- kumitate-shokunin (3 hits): `kumitate-shokunin/corpus/knowledge/durable-execution-failure-detection.md:18,32,66`
  — one Chinese cloud vendor's managed-agent runtime contract.
- kotoba-shokunin (6 hits): `kotoba-shokunin/corpus/knowledge/chinese-vendor-skill-surfaces-round73.md`
  and `kotoba-shokunin/corpus/README.md:142,228` — TRAE/CodeBuddy/Kimi/Zhipu
  skill-surface frontmatter craft.

### 3. Variant sweep (crowd[- ]?sourc / cnvd / 360 / 漏洞 / 众测 / SRC)

```
for d in chousa-shokunin kengaku-shokunin kake-shokunin kagi-shokunin kumitate-shokunin kotoba-shokunin; do
  echo "=== $d ==="
  grep -rinE 'crowd[- ]?sourc|cnvd|360|漏洞|众测|SRC' \
    "$d/corpus/README.md" "$d/corpus/knowledge/" 2>/dev/null \
    | grep -vE '\b360deg|360px|round-?360' | head -20
  echo "(grep exit $?)"
done
```

Every `360` hit is numeric/config noise (`3600` request-timeout seconds in
kagi, fuzz seeds `36001/36011` and `stamps.chunk=360` in chousa, `:360` line
references in kumitate). Every `SRC` hit is source-tree variable noise
(`src/`, `src_root`, `SRC_PTR`). No `cnvd`, `众测`, `漏洞`, or
`crowd[- ]?sourc` hit anywhere.

### 4. Substance sweep (bounty / reward rules / vulnerability handling / SRC)

```
for d in chousa-shokunin kengaku-shokunin kake-shokunin kagi-shokunin kumitate-shokunin kotoba-shokunin; do
  echo "=== $d ==="
  grep -rinE 'bounty|reward rules|vulnerability handling|security response|vulnerability reward| crowdsourc|众包|众测' \
    "$d/corpus/README.md" "$d/corpus/knowledge/" 2>/dev/null | head -10
  echo "(grep exit $?)"
done
```

Salient output:

- `chousa-shokunin/corpus/knowledge/scope-refusal-r12.md:21`:
  `bug bounty`, `bounty program(s)`, `bounty hunt(ing)`, `bounty scope`,
  `claim package(s)`, `kasegi` → fence `SCOPE_BOUNTY_ABSORBED` → routed to
  **kasegi**. chousa *refuses* bounty ground and routes it here.
- `kake-shokunin/corpus/README.md:464-465` (round-35 security.txt note):
  "Vulnerability handling itself (report intake, triage, remediation,
  disclosure timing, bounty and policy operation) **stays outside this
  province**".
- `kumitate-shokunin/corpus/knowledge/ops-watchers.md:30` — an ops watcher
  that "refires stale bounty-hunt UFOs" (orchestration telemetry, not platform
  rules).
- `kotoba-shokunin/corpus/knowledge/sibling-description-rewrites-round8.md:259-280`
  — *describes kasegi's* domain: "kasegi owns the bounty tree, its claim
  machinery".
- kengaku, kagi: no hits.

### 5. Sibling province domains (PROVINCE.md header of each)

```
chousa   — "deep-research method (調査)"; Refuses: "bounty-program scope and
           claim packages (→ kasegi)"
kengaku  — "LLM/model research & evaluation"
kake     — "web properties & publishing"
kagi     — "secrets & vault ops"
kumitate — "orchestration & tooling"
kotoba   — "prompt & skill craft"
```

### 6. kasegi PROVINCE.md Adjacent section

`kasegi-shokunin/PROVINCE.md:43-52` — Adjacent names chousa / kagi / kake /
kengaku only ("reported, not absorbed"); kotoba and kumitate are not named
adjacent. Line 3 domain: "bounty & security research — scopes, program rules,
claim packages". Core: "program rules, scopes, and claim packages; the core
also covers triage and claim gates, and submission/disclosure packaging."
Frontier amendments F12–F15 include `F13 — Program severity ladders and
reward scales` (round 29).

## Findings

1. **No sibling holds F16 ground.** Across the six named siblings' corpus
   READMEs and corpus/knowledge dirs there are zero hits for CNVD, 360SRC,
   众测, zc.cnvd.org.cn, security.360.cn, or crowdsourced (any spelling
   variant). The only `Chinese` material in the fleet neighbours is
   Chinese-language *academic citation/search-method* documents (chousa), one
   JS-rendering Chinese edition note (kake), one Chinese cloud-vendor agent
   runtime (kumitate), and Chinese-vendor skill-surface craft (kotoba) — none
   touches Chinese security platforms, crowdsourced testing, scope rules, or
   reward rules.
2. **Two siblings explicitly disclaim the ground.** chousa's scope-refusal
   fence routes `bug bounty`/`bounty program(s)`/`claim package(s)` → kasegi,
   and kake's round-35 note states vulnerability handling incl. "bounty and
   policy operation" stays outside its province. kotoba's only bounty content
   is a *description of kasegi's* domain confirming the boundary.

## Province verdict

**F16 sits inside kasegi's province; it is not contested.**

F16's substance — CNVD 众测 platform scope rules (helpList) and 360SRC
external-vulnerability handling and reward/scoring standards — is program
rules + reward scales of security platforms. That is kasegi's Core
(`PROVINCE.md:7-13`: "program rules, scopes, and claim packages"), the same
lineage as kasegi's own F13 (program severity ladders and reward scales) and
F15 (vendor-side research programme). No sibling claims or holds this ground;
chousa and kake actively route/disclaim it toward kasegi. The round-33
admission (S049/S050) introduces no sibling collision.

## Notes / bounds

- Read-only on the fleet root and all sibling lanes; the only write is this
  receipt at the `Report:` path.
- No fetches, no live-target contact, no git/jj mutations, no installs.
- No PRE-STATE counters involved (no counters run).
