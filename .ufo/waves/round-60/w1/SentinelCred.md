CLEAN — no credential values, no email address in the capture or the entry, no per-request nonce/session token/signed URL, no private or session URL on the entry or the registry, and no target-intake instruction in the round-60 bytes. Five personal-data/sensitive-content forms are present; each is judged in O1–O5.

# Seat SentinelCred — credential, personal-data and sensitive-content screen (kasegi round 60, wave w1)

Read-only seat: every command below was run against the lane at the paths shown; nothing under L was
written except this file. No network call was made. No tool was installed or upgraded (nothing was
needed; all checks use the host's grep/awk/find/coreutils that were already present — therefore no
tool/version/channel entry is due under the 2026-10-19 tooling authorization).

Snapshot: lane HEAD `228118a8cfba679c1d97841aa3af38e5ec83d84a` at 2026-11-04T13:44Z (the lead committed
LOG/SCORECARD during this seat; HEAD was `b8c77fb` when the seat started). The implementation under
test `7f7dd267283d2a16ca38d4cb05bed92165cb35cd` is an ancestor of HEAD (E0). The bytes screened are
unchanged since the implementation commit: S093.txt 10:29:52, manifest.json 10:31:38, SOURCES.md /
README.md / PROVINCE.md 10:33:26, the F41 entry 10:33:42, claims.json 10:35:21, erratum 10:36:09
(host mtimes, -0300). Scope of the scan, exactly as enumerated in the seat: corpus/source-snapshots/
round-60/{S093.txt,manifest.json}, corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md,
corpus/SOURCES.md, corpus/README.md, PROVINCE.md, and every file under .ufo/waves/round-60/ (the
assigned subset of SOURCES.md/README.md — the S093 row, the round-60 registry-changes bullets, the
README round-60 block, the PROVINCE r60 amendment — is also counted separately in E5).

## Evidence

### E0 — provenance and tracked-tree cleanliness

```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd "$L" || exit 1
git rev-parse HEAD; git merge-base --is-ancestor 7f7dd267283d2a16ca38d4cb05bed92165cb35cd HEAD; echo "ancestor_exit=$?"
git status --porcelain | grep -v '^??' | wc -l; date -u +%Y-%m-%dT%H:%M:%SZ
```

```
228118a8cfba679c1d97841aa3af38e5ec83d84a
ancestor_exit=0
0
2026-11-04T13:44:13Z
```

exit=0. No tracked file modified (`0`); every untracked path is wave-layer material (dispatch markers,
the wave evidence directory, and one controls receipt that landed after the scan) — none under
`corpus/`.

### E1 — assigned pattern inventory, path:line only (no values)

```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd "$L" || exit 1
SCOPE="corpus/source-snapshots/round-60 corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/SOURCES.md corpus/README.md PROVINCE.md .ufo/waves/round-60"
run_pat() { local name=$1 re=$2; local hits; hits=$(grep -r -n -H -E -i -- "$re" $SCOPE 2>/dev/null | cut -d: -f1,2 | tr '\n' ',' | sed 's/,$//'); printf '%-14s %s\n' "$name" "${hits:-NONE}"; }
run_pat AKIA 'AKIA'
run_pat PRIVKEY 'BEGIN [A-Z ]*PRIVATE'
run_pat GITHUB_PAT 'ghp_'
run_pat SLACK 'xox[abp]-'
run_pat OPENAI 'sk-[A-Za-z0-9]'
run_pat PASSWORD 'password'
run_pat TOKEN_PARAM 'token='
run_pat BEARER 'Bearer '
run_pat OP_REF 'op://'
run_pat SESSION 'session'
run_pat COOKIE 'cookie'
run_pat QUERY_TOKEN 'https?://[^ )"<>]*[?&](token|key|sig|signature|access_token|expires|nonce|auth)='
```

```
AKIA           .ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:70
PRIVKEY        NONE
GITHUB_PAT     .ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:70
SLACK          NONE
OPENAI         corpus/SOURCES.md:15,corpus/SOURCES.md:31,corpus/SOURCES.md:106,corpus/SOURCES.md:115,corpus/README.md:388,corpus/README.md:841,.ufo/waves/round-60/controls/neighbor-screen-r60.txt:78
PASSWORD       .ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:70
TOKEN_PARAM    .ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:70
BEARER         .ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:70
OP_REF         .ufo/waves/round-60/build-spec.py:32,.ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/w1-dispatch.json:180,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:10,.ufo/waves/round-60/w1-spec.json:70
SESSION        corpus/source-snapshots/round-60/S093.txt:73,corpus/SOURCES.md:175,corpus/README.md:27,corpus/README.md:111,corpus/README.md:137,.ufo/waves/round-60/build-spec.py:32,.ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/build-spec.py:171,.ufo/waves/round-60/build-spec.py:172,.ufo/waves/round-60/w1-dispatch.json:180,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:10,.ufo/waves/round-60/w1-spec.json:70
COOKIE         corpus/SOURCES.md:73,.ufo/waves/round-60/build-spec.py:32,.ufo/waves/round-60/build-spec.py:169,.ufo/waves/round-60/w1-dispatch.json:180,.ufo/waves/round-60/w1-dispatch.json:240,.ufo/waves/round-60/w1-plan.json:60,.ufo/waves/round-60/w1-spec.json:10,.ufo/waves/round-60/w1-spec.json:70
QUERY_TOKEN    NONE
```

exit=0. Classification of every hit (all are the pattern *name* inside the seat-spec prose, or an
English word — E2 proves none carries a value):

- `build-spec.py:169`, `w1-spec.json:70`, `w1-plan.json:60`, `w1-dispatch.json:240`: the literal
  pattern list of this very seat's spec ("grep -n -E for credential shapes: 'AKIA', …") — pattern
  names, no matches. `build-spec.py:32`, `w1-spec.json:10`, `w1-dispatch.json:180`: the round
  contract line "no … op:// references" — same class. `w1-spec.json:70`/`w1-plan.json:60` also carry
  the "nonce, session token or signed URL" instruction text (item 3), again as names.
- `build-spec.py:171`, `:172`: item 3 / item 4 prose ("per-request nonce, session token or signed
  URL"; "no intake instructions").
- `SOURCES.md:15,31,106,115`, `README.md:388,841`, `neighbor-screen-r60.txt:78`: the substring
  `sk-` inside `task-specific`, `risk-priority`, `risk-based`, and a task slug (E1 companion below) —
  no key-shaped material.
- `S093.txt:73`: the word "sessions" (English plural, E9b).
- `SOURCES.md:175`, `README.md:27,111,137`: `.ufo/sessions/` path text and the word "sessions" in
  pre-existing round notes — no round-60 bytes.
- `SOURCES.md:73`: the word "cookie" inside the CVE-2025-9086 title ("cookie path") — a pre-existing
  S067 row, not round-60.

`sk-` word forms, exactly:

```
grep -o -E -i '[A-Za-z0-9_-]*sk-[A-Za-z0-9_-]*' corpus/SOURCES.md corpus/README.md | sort | uniq -c | sort -rn
      3 corpus/SOURCES.md:task-specific
      1 corpus/SOURCES.md:10-questions-ask-using-ai-models-find-vulnerabilities
      1 corpus/README.md:risk-priority
      1 corpus/README.md:risk-based
```

exit=0.

Reproducibility note: the scope set includes the live `.ufo/waves/round-60/` tree, so a re-run of E1
after this file and later sibling evidence land also matches their own pattern-name text and prose
(this file's own text is measured separately in E17). The rows above are the pre-write run at
2026-11-04T13:44Z; the value-bearing discriminators (E2) are insensitive to that, because pattern
literals such as `token=` are followed by `[`, which their classes do not match.

### E2 — value-bearing discriminators (a real credential would need the value after the prefix)

```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd "$L" || exit 1
SCOPE="corpus/source-snapshots/round-60 corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/SOURCES.md corpus/README.md PROVINCE.md .ufo/waves/round-60"
for spec in 'AKIA[0-9A-Z]{4,}' 'ghp_[A-Za-z0-9]{10,}' 'xox[abp]-[A-Za-z0-9-]{5,}' 'sk-[A-Za-z0-9]{20,}' \
            'password[[:space:]]*[=:][[:space:]]*[^[:space:]]' 'token=[A-Za-z0-9_.-]{8,}' \
            'Bearer [A-Za-z0-9._~+/-]{10,}' 'op://[A-Za-z0-9]' '-----BEGIN' 'eyJ[A-Za-z0-9_-]{5,}\.' \
            'X-Amz-[A-Za-z]+' 'X-Goog-[A-Za-z]+' 'api[_-]?key' 'access_token'; do
  n=$(grep -r -c -E -- "$spec" $SCOPE 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')
  printf '%-52s hits=%s\n' "$spec" "$n"; done
```

```
AKIA[0-9A-Z]{4,}                                     hits=0
ghp_[A-Za-z0-9]{10,}                                 hits=0
xox[abp]-[A-Za-z0-9-]{5,}                            hits=0
sk-[A-Za-z0-9]{20,}                                  hits=0
password[[:space:]]*[=:][[:space:]]*[^[:space:]]     hits=0
token=[A-Za-z0-9_.-]{8,}                             hits=0
Bearer [A-Za-z0-9._~+/-]{10,}                        hits=0
op://[A-Za-z0-9]                                     hits=0
-----BEGIN                                           hits=0
eyJ[A-Za-z0-9_-]{5,}\.                               hits=0
X-Amz-[A-Za-z]+                                      hits=0
X-Goog-[A-Za-z]+                                     hits=0
api[_-]?key                                          hits=0
access_token                                         hits=0
```

exit=0. Zero value-bearing occurrences of any assigned class: no key material, no JWT, no cloud
signed-request parameter, no vault authority, no private-key header anywhere in the scope set.

### E3 — email-address screen, path:line only

```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd "$L" || exit 1
SCOPE="corpus/source-snapshots/round-60 corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/SOURCES.md corpus/README.md PROVINCE.md .ufo/waves/round-60"
grep -r -n -H -E -o '[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*' $SCOPE 2>/dev/null | cut -d: -f1,2 | sort -u
```

```
corpus/README.md:792
corpus/SOURCES.md:89
.ufo/waves/round-60/controls/c1-probe-run-r60.sh:39
```

exit=0. Three hits total, none in the capture, the F41 entry or any round-60 corpus/README block:

- `README.md:792` (F33 row) and `SOURCES.md:89` (S083 row): public role mailboxes of NVD / Red Hat
  PSIRT quoted inside pre-existing registry rows from earlier rounds — O4.
- `controls/c1-probe-run-r60.sh:39`: the placeholder git identity in the probe runner's throwaway
  fixture clone (E7) — O2.

### E4 — URL hygiene on the round-60 bytes

E4a, capture URL count:

```
grep -c -E 'https?://' corpus/source-snapshots/round-60/S093.txt
```

```
0
```

exit=1 (grep: zero matches — the intended result). The capture is the converted *text* of the page
(tags stripped by `capture-source.py --kind html`), so it carries no URL at all; the manifest's
`url`/`capture_url`/`final_url` fields are the only URLs for S093.

E4b, userinfo or query-bearing URLs anywhere in the scope set:

```
grep -r -n -H -E -o '[a-z]+://[^/[:space:]]*@[^[:space:]]+|https?://[^ )"<>]*\?[^ )"<>]*' $SCOPE 2>/dev/null | cut -d: -f1,2 | sort -u
```

```
corpus/SOURCES.md:26
corpus/SOURCES.md:33
corpus/SOURCES.md:89
```

exit=0. All three are pre-existing rows, outside the round-60 bytes; their query parameters are
`inline` (a DOJ file download), `id` (a Hacker News item number) and `cveId` (an NVD record key) —
none is a token, signature, expiry or userinfo segment. No `user:pass@` URL exists in the scope set.

E4c, URLs on the in-scope round-60 lines:

```
for spec in "corpus/README.md 992 1009" "corpus/SOURCES.md 100 100" "corpus/SOURCES.md 219 221" "corpus/SOURCES.md 142 142" "PROVINCE.md 209 209"; do
  set -- $spec; f=$1; a=$2; b=$3; printf '%s:%s-%s ' "$f" "$a" "$b"
  awk -v a="$a" -v b="$b" 'NR>=a&&NR<=b' "$f" | grep -o -E 'https?://[^ )"]+' | awk '{n++; if ($0 ~ /\?/) q++; if ($0 ~ /@/) u++} END{printf "urls=%d with_query=%d with_userinfo=%d\n", n+0, q+0, u+0}'
done
```

```
corpus/README.md:992-1009 urls=1 with_query=0 with_userinfo=0
corpus/SOURCES.md:100-100 urls=1 with_query=0 with_userinfo=0
corpus/SOURCES.md:219-221 urls=1 with_query=0 with_userinfo=0
corpus/SOURCES.md:142-142 urls=0 with_query=0 with_userinfo=0
PROVINCE.md:209-209 urls=0 with_query=0 with_userinfo=0
```

exit=0. The three URLs are the public post `https://projectzero.google/2026/10/fuzzing-v-AI.html`
(README block, S093 row) and the pre-existing public shortlink `https://goo.gle/bigsleep` quoted in
the corrected lead-bullet old→new record (SOURCES.md:221). None carries a query string, userinfo,
session id or signature.

### E5 — the assigned file subsets counted directly (S093 row, registry bullets, README block, PROVINCE amendment, entry, manifest, capture)

```
declare -A P=( [AKIA]='AKIA' [PRIVKEY]='BEGIN [A-Z ]*PRIVATE' [GHPAT]='ghp_' [SLACK]='xox[abp]-' [SKKEY]='sk-[A-Za-z0-9]' [PASSWORD]='password' [TOKENPARAM]='token=' [BEARER]='Bearer ' [OPREF]='op://' [SESSION]='session' [COOKIE]='cookie' )
for spec in "corpus/README.md 992 1009" "corpus/SOURCES.md 100 100" "corpus/SOURCES.md 219 221" "corpus/SOURCES.md 142 142" "PROVINCE.md 209 209" "corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md 1 43" "corpus/source-snapshots/round-60/manifest.json 1 104" "corpus/source-snapshots/round-60/S093.txt 1 283"; do
  set -- $spec; f=$1; a=$2; b=$3; line=""
  for k in "${!P[@]}"; do c=$(awk -v a="$a" -v b="$b" 'NR>=a&&NR<=b' "$f" | grep -c -E -i -- "${P[$k]}"); [ "$c" -gt 0 ] && line+="$k=$c "; done
  printf '%-72s %s\n' "$f:$a-$b" "${line:-none}"; done
```

```
corpus/README.md:992-1009                                                none
corpus/SOURCES.md:100-100                                                none
corpus/SOURCES.md:219-221                                                none
corpus/SOURCES.md:142-142                                                none
PROVINCE.md:209-209                                                      none
corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:1-43    none
corpus/source-snapshots/round-60/manifest.json:1-104                     none
corpus/source-snapshots/round-60/S093.txt:1-283                          SESSION=1
```

exit=0. Every in-scope byte range of the corpus/front-door files is pattern-clean; the capture's one
`session` hit is the English word "sessions" at S093.txt:73 (E9b), not a credential.

### E6 — personal data in the capture and the entry: the byline

```
grep -n -H 'Samuel Groß' corpus/source-snapshots/round-60/S093.txt corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md | cut -d: -f1,2
```

```
corpus/source-snapshots/round-60/S093.txt:14
corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:10
```

exit=0. Capture lines 12/13/14 are title / date / byline; the entry quotes the byline in its
Attribution section. This is the only personal name in the capture (the other `[A-Z][a-z]+ [A-Z][a-z]+`
tokens are titles and product names — "Project Zero", "Chrome Bug", "Samuel Groß", "Big Sleep", …;
one personal name total). Byline spread across the round-60 record is E15.

### E7 — email-shaped string in the probe runner (form: placeholder fixture identity)

```
sed -n '39p' .ufo/waves/round-60/controls/c1-probe-run-r60.sh | grep -c 'user.email'
```

```
1
```

exit=0. Line 39 is the throwaway commit identity passed with `-c user.email=… -c user.name=…` to the
scratch git fixture the runner creates under its own temp dir and deletes on exit. The address has no
dot-bearing domain (RFC-invalid as a deliverable address), no local part of a real person, and the
runner is the only place it appears (E3). Judgment in O2: KEEP.

### E8 — public tracker references in the capture (form: publisher's own citations)

```
printf 'crbug_occurrences='; grep -o -E 'crbug\.com/[0-9]+' corpus/source-snapshots/round-60/S093.txt | wc -l
printf 'crbug_unique=';      grep -o -E 'crbug\.com/[0-9]+' corpus/source-snapshots/round-60/S093.txt | sort -u | wc -l
printf 'crrev_occurrences='; grep -o -E 'crrev\.com/c/[0-9]+' corpus/source-snapshots/round-60/S093.txt | wc -l
printf 'refs_with_query=';   grep -o -E 'cr(e|b)v?[a-z]*\.com/[^ )]*[?&][^ )]*' corpus/source-snapshots/round-60/S093.txt | wc -l
```

```
crbug_occurrences=15
crbug_unique=14
crrev_occurrences=1
refs_with_query=0
```

exit=0. Host+path references only (no scheme, no query, no token); they are the public post's own
citations of Chromium bugs, not access-controlled identifiers or per-user ids. The entry itself
enumerates none of them (E11: 0 numeric ids). Judgment in O5: KEEP.

### E9 — item 3: per-request nonce / session token / signed URL in the captured page

```
for spec in 'nonce' 'sig=[A-Za-z0-9]' 'expires=[0-9]' 'X-Amz-' 'X-Goog-' 'set-cookie' 'Authorization:' 'signed[_-]?url' '^(GET|POST|HTTP/|Host:|User-Agent:|Cookie:)'; do
  printf '%-28s %s\n' "$spec" "$(grep -c -E -i -- "$spec" corpus/source-snapshots/round-60/S093.txt)"; done
```

```
nonce                        0
sig=[A-Za-z0-9]              0
expires=[0-9]                0
X-Amz-                       0
X-Goog-                      0
set-cookie                   0
Authorization:               0
signed[_-]?url               0
^(GET|POST|HTTP/|Host:|User-Agent:|Cookie:) 0
```

exit=0.

E9b, the single `session` hit in the capture:

```
grep -n -o -i 'session[a-z]*' corpus/source-snapshots/round-60/S093.txt | cut -d: -f1,2
```

```
73:sessions
```

exit=0. Confirmed: no nonce, no signature/expiry parameter, no cloud signed-URL parameter, no cookie
header, no `Authorization`, and no request-header block in the captured page. The capture retains no
per-request material because it retains no URL at all (E4a). The only `session` token is the English
plural in "long fuzzing sessions".

### E10 — probe-tree hygiene: no residue from the probe runner in the lane

```
printf 'MARK_files_in_lane='; find . -name 'MARK-*' -not -path './.git/*' | wc -l
printf 'above_evil_present='; test -e above-evil.py && echo 1 || echo 0
```

```
MARK_files_in_lane=0
above_evil_present=0
```

exit=0. The runner's per-probe roots live under its own `$S` (deleted by its EXIT trap) and its
fixture clones are created with `git -C "$r/repo" init` after the runner's own root assertion
(`git -C "$r/repo" rev-parse --show-toplevel` equals the fixture, c1-probe-run-r60.sh:40). No probe
artifact, marker, marker-named file or traversal target exists in the lane tree at scan time.

### E11 — item 4: entry and registry — no private/session URL, no intake instruction

```
printf 'entry_crbug_string_mentions='; grep -c -i 'crbug\.com' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
printf 'entry_crbug_numeric_ids=';     grep -o -E 'crbug\.com/[0-9]+' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md | wc -l
printf 'entry_http_urls=';             grep -c -E 'https?://' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
grep -n -o -i -E 'intake|submission|submit|contact|reach out|reporting address|security@' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
awk 'NR==100' corpus/SOURCES.md | grep -o -i -E 'intake|submission|submit|contact|reporting address|security@' | sort | uniq -c
```

```
entry_crbug_string_mentions=2
entry_crbug_numeric_ids=0
entry_http_urls=1
10:intake
10:submission
34:intake
34:intake
```

exit=0. The S093-row intake grep prints nothing (empty = none). The entry's only URL is the public
post (E4c). Its only `intake`/`submission` tokens are *negations* in the same sentence:

- entry:10 — "…not a policy, a program rule, an intake channel or a severity ladder. This entry
  asserts only the post's own statements… and instructs no probing, scanning or submission against
  any target."
- entry:34 — "…the post is not vendor policy, a bounty-program rule, an intake channel or a severity
  ladder, and it states no intake or reward guidance…"

The entry's two `crbug.com` string mentions are the same negation ("no crbug.com reference",
entry:10 and entry:42); zero numeric bug ids are enumerated. The registry row (SOURCES.md:100) is
descriptive and carries no intake channel; the registry-changes bullets (SOURCES.md:219-221) quote
the old→new lead correction only.

### E12 — PROVINCE round-60 amendment

```
awk 'NR==209{printf "chars=%d urls=%d intake=%d\n", length($0), gsub(/https?:\/\//,"&"), gsub(/intake|submission|contact|security@/,"&")}' PROVINCE.md
```

```
chars=1041 urls=0 intake=0
```

exit=0. The amendment (PROVINCE.md:209) carries no URL, no contact address and no intake instruction;
its scope-limit clause restricts the frontier to one first-party research post.

### E13 — published exploit-PoC fragments in the capture (sensitive content, public)

```
for n in 124 126 127 188 189 226 227; do awk -v n="$n" 'NR==n{printf "%d: %s\n", n, substr($0,1,55)}' corpus/source-snapshots/round-60/S093.txt; done
```

```
124: Proof of Concept
126: // Flags: --ignition-elide-redundant-tdz-checks
127: function trigger(cond) {
188: // yield statements turn into a large chunk of bytecode
189: let kNumYields = 500000;
226: Let’s start by looking at the testcase produced by the
227: function f0() {
```

exit=0. Three JS testcases from the public Project Zero post are captured as published (anchors
above). They target V8 bugs the post itself discloses; there is no victim data, no exploit chain, no
staged payload and no unpublished detail. Judgment in O5: KEEP.

### E14 — machine addresses, obfuscated addresses, and the entry's limits sentence

```
for spec in '0x[0-9a-fA-F]{6,}'; do printf 'hex_addresses_occurrences='; grep -o -E "$spec" corpus/source-snapshots/round-60/S093.txt | wc -l; printf 'hex_addresses_unique='; grep -o -E "$spec" corpus/source-snapshots/round-60/S093.txt | sort -u | wc -l; done
printf 'obfuscated_email='; grep -c -i -E '\[at\]|\(at\)| at [A-Za-z0-9.-]+ dot ' corpus/source-snapshots/round-60/S093.txt
awk 'NR==42{print substr($0,1,190)}' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
```

```
hex_addresses_occurrences=7
hex_addresses_unique=7
obfuscated_email=0
- The entry enumerates no individual finding, no crbug.com reference and no tracker issue; the post's figures (images) are not transcribed, and no claim rests on them.
```

exit=0. The 7 unique `0x…` values are the published d8 disassembly example addresses printed by the
post (e.g. its `--print-bytecode` sample); they are illustrative addresses of a published example,
not credentials, session ids or personal identifiers, and the entry rests no claim on them.

### E15 — byline spread across the round-60 record (personal-data extent)

```
grep -r -n -H 'Samuel' corpus/source-snapshots/round-60 corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/SOURCES.md corpus/README.md PROVINCE.md .ufo/waves/round-60 2>/dev/null | cut -d: -f1,2
```

```
corpus/source-snapshots/round-60/S093.txt:14
corpus/source-snapshots/round-60/manifest.json:3
corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:10
.ufo/waves/round-60/build-spec.py:49
.ufo/waves/round-60/claims.json:36
.ufo/waves/round-60/controls/neighbor-screen-r60.txt:15
.ufo/waves/round-60/w1-dispatch.json:185
.ufo/waves/round-60/w1-plan.json:5
.ufo/waves/round-60/w1-spec.json:15
.ufo/waves/round-60/w1/ScoutS093.md:1
```

(A further 11 byline lines in the same sibling file — ScoutS093.md lines 251, 307, 309, 312, 319, 324,
326, 330, 336, 337, 464 — are elided here; it is sibling seat evidence, read-only.)

exit=0. Every occurrence is the same public byline, quoted from the capture or restated in the
frozen claim/spec text and the lead's neighbor-screen receipt. No email, handle, employer-internal
id, location or other non-public datum accompanies it anywhere.

### E16 — adjacent records screened opportunistically (OUTSIDE the enumerated scope; recorded for the lead's scope-audit seat)

```
LESSON=$(git show --stat --oneline fb6a928 --name-only | grep 'lessons/.*round-60' | head -1)   # corpus/lessons/round-60.md
FILES="LOG.md SCORECARD.md $LESSON"
for spec in 'AKIA' 'BEGIN [A-Z ]*PRIVATE' 'ghp_' 'xox[abp]-' 'sk-[A-Za-z0-9]' 'password' 'token=' 'Bearer ' 'op://' '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+' 'https?://[^ )"]*[?&]' 'nonce' 'cookie' 'session'; do
  printf '%-40s ' "$spec"; grep -r -c -E -i -- "$spec" $FILES 2>/dev/null | awk -F: '{s+=$NF} END{print (s+0)}'; done
```

```
AKIA                                     0
BEGIN [A-Z ]*PRIVATE                     0
ghp_                                     0
xox[abp]-                                0
sk-[A-Za-z0-9]                           0
password                                 0
token=                                   0
Bearer                                   0
op://                                    0
[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+         4
https?://[^ )"]*[?&]                     2
nonce                                    0
cookie                                   0
session                                  21
```

exit=0. The 4 `@` hits are not addresses: `LOG.md:255` (a `launch_cap@64` ref name),
`LOG.md:2469`/`:2470` (`SOURCES@base`, `entry@base` ref names), `SCORECARD.md:1557` (`gap@r39`
annotation). Zero deliverable email addresses. Of the 2 query-bearing URLs, `LOG.md:2299` is the
NVD `?cveId=` record key and `LOG.md:1110` is a pre-existing (2026-10-17) org-workspace wiki link with
a `branch` parameter — no token or signature, predates round 60, and is not part of this seat's
enumerated bytes; noted for the scope-audit seat, no action from this seat. `session` hits are the
word "session(s)" in round notes (21). Not part of the verdict.

### Final tree snapshot at write time (2026-11-04T13:44:46Z, before this file)

```
date -u +%Y-%m-%dT%H:%M:%SZ; find .ufo/waves/round-60 -type f | sort | sed 's|^|  |'; printf 'tree_files='; find .ufo/waves/round-60 -type f | wc -l
```

```
2026-11-04T13:44:46Z
  .ufo/waves/round-60/assimilation/collisions
  .ufo/waves/round-60/assimilation/reg-ids
  .ufo/waves/round-60/assimilation/staged-ids
  .ufo/waves/round-60/build-spec.py
  .ufo/waves/round-60/claims-erratum-1.md
  .ufo/waves/round-60/claims.json
  .ufo/waves/round-60/controls/c1-lane-after-r60.txt
  .ufo/waves/round-60/controls/c1-probe-run-r60.sh
  .ufo/waves/round-60/controls/c1-probes-base-r60.txt
  .ufo/waves/round-60/controls/c1-probes-standin-r60.txt
  .ufo/waves/round-60/controls/c1-standin-after-r60.txt
  .ufo/waves/round-60/controls/c2-lane-after-r60.txt
  .ufo/waves/round-60/controls/c2-standin-after-r60.txt
  .ufo/waves/round-60/controls/census-round-start-r60.txt
  .ufo/waves/round-60/controls/do-nothing-c1-r60.txt
  .ufo/waves/round-60/controls/do-nothing-c2-r60.txt
  .ufo/waves/round-60/controls/freeze-digests-r60.txt
  .ufo/waves/round-60/controls/neighbor-screen-r60.txt
  .ufo/waves/round-60/w1-dispatch.json
  .ufo/waves/round-60/w1/ExecCounters.json
  .ufo/waves/round-60/w1/ExecCounters.md
  .ufo/waves/round-60/w1/ExecDiffScope.md
  .ufo/waves/round-60/w1-plan.json
  .ufo/waves/round-60/w1.ready
  .ufo/waves/round-60/w1.ready.dispatched
  .ufo/waves/round-60/w1/ScoutS093.md
  .ufo/waves/round-60/w1/SiblingOverlap.md
  .ufo/waves/round-60/w1-spec.json
  .ufo/waves/round-60/w1/swarm-registry.json
tree_files=29
```

exit=0.

```
printf 'symlinks='; find .ufo/waves/round-60 corpus/source-snapshots/round-60 -type l | wc -l
```

```
symlinks=0
```

exit=0. The wave evidence directory is being written by sibling seats concurrently (it gained files
during this seat); the screen above covers the files present at the timestamps recorded, and this
file's own post-write self-scan is E17.

### E17 — self-scan: this evidence file carries no credential shape and no value

```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd "$L" || exit 1
F=.ufo/waves/round-60/w1/SentinelCred.md
printf 'utf8_valid='; iconv -f UTF-8 -t UTF-8 "$F" >/dev/null 2>&1 && echo 1 || echo 0
printf 'first_line_verdict='; head -1 "$F" | grep -c -E '^(CLEAN|FINDINGS)'
for spec in 'AKIA[0-9A-Z]{4,}' 'ghp_[A-Za-z0-9]{10,}' 'xox[abp]-[A-Za-z0-9-]{5,}' 'sk-[A-Za-z0-9]{20,}' \
            'Bearer [A-Za-z0-9._~+/-]{10,}' 'op://[A-Za-z0-9]' 'eyJ[A-Za-z0-9_-]{5,}\.' \
            'token=[A-Za-z0-9_.-]{8,}' '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'; do
  printf '%-42s %s\n' "$spec" "$(grep -c -E -- "$spec" "$F")"; done
printf 'privkey_header_lines='; grep -c -E -- '^-----BEGIN [A-Z ]*PRIVATE KEY-----' "$F"
```

```
utf8_valid=1
first_line_verdict=1
AKIA[0-9A-Z]{4,}                           0
ghp_[A-Za-z0-9]{10,}                       0
xox[abp]-[A-Za-z0-9-]{5,}                  0
sk-[A-Za-z0-9]{20,}                        0
Bearer [A-Za-z0-9._~+/-]{10,}              0
op://[A-Za-z0-9]                           0
eyJ[A-Za-z0-9_-]{5,}\.                     0
token=[A-Za-z0-9_.-]{8,}                   0
[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,} 0
privkey_header_lines=0
```

exit=1 (the closing `grep -c` prints 0 and returns 1 because there is no match — the intended
result; every other statement above returned 0). This file is valid UTF-8, begins with a verdict line,
and carries no value-bearing credential shape and no email address. The dash-BEGIN and private-key
class labels occur only inside the recorded search patterns themselves (E2's discriminator list and
this anchored pattern) and their echoed result rows — never as a line-initial key header, as the
anchored check above reports (0). Likewise
the vault-scheme literal in the E1/E2 and E16 commands is only the search pattern: no authority or
item path follows it anywhere, so it cannot resolve to a vault item (E2's value-bearing discriminator
for that class is 0).

## Observations and judgments (forms only; no values)

- **O1 — personal name (public byline).** "Samuel Groß" at `S093.txt:14`, `manifest.json:3`,
  `entry:10`, and copied into the frozen claim/spec text (`claims.json:36`, `build-spec.py:49`,
  `w1-spec.json:15`, `w1-plan.json:5`, `w1-dispatch.json:185`) and the lead's neighbor-screen receipt
  (`controls/neighbor-screen-r60.txt:15`) (E6, E15). It is the publisher's own byline on a public
  research post, with no email, handle, location or internal id attached. **KEEP** — attribution is
  the entry's provenance requirement and removing it would break the capture↔entry↔registry chain.
- **O2 — placeholder fixture identity.** One email-shaped string in the probe runner's throwaway git
  fixture (`controls/c1-probe-run-r60.sh:39`; no dot-bearing domain) (E3, E7). Not a person, not a
  deliverable address, confined to a temp clone the runner deletes. **KEEP.**
- **O3 — local account/host names in absolute paths (informational).** The receipts and the frozen
  counting commands name the workstation owner's own account and scratch directories:

  ```
  grep -n -o -E '/home/[A-Za-z0-9._-]+|/fast/scratch/[A-Za-z0-9._-]+' .ufo/waves/round-60/claims.json .ufo/waves/round-60/controls/c1-lane-after-r60.txt .ufo/waves/round-60/controls/c1-probes-base-r60.txt .ufo/waves/round-60/controls/c1-probes-standin-r60.txt .ufo/waves/round-60/controls/freeze-digests-r60.txt .ufo/waves/round-60/controls/census-round-start-r60.txt | cut -d: -f1,2 | sort -u
  ```

  ```
  .ufo/waves/round-60/claims.json:20
  .ufo/waves/round-60/claims.json:49
  .ufo/waves/round-60/controls/c1-lane-after-r60.txt:4
  .ufo/waves/round-60/controls/c1-probes-base-r60.txt:1
  .ufo/waves/round-60/controls/c1-probes-standin-r60.txt:1
  .ufo/waves/round-60/controls/census-round-start-r60.txt:7
  .ufo/waves/round-60/controls/freeze-digests-r60.txt:1
  .ufo/waves/round-60/controls/freeze-digests-r60.txt:2
  ```

  exit=0. `claims.json:20` is C1's scratch probe directory; `claims.json:49` is the fleet-root
  script path inside C2's census counting command; the receipts name the instrument's absolute path
  and the census input. These are the owner's own account and host scratch names, carry no
  credential, and are what make the receipts reproducible against a literal path. **KEEP**
  (informational; the lane's absolute-path convention).
- **O4 — public role addresses (pre-existing, outside the round-60 bytes).** `README.md:792` (F33
  row) and `SOURCES.md:89` (S083 row) quote NVD / Red Hat PSIRT role mailboxes from earlier rounds
  (E3). Already-public program contact mailboxes, not personal data, untouched by round 60. **KEEP.**
- **O5 — published exploit PoCs and public tracker ids.** Three testcases from the public post
  (`S093.txt:126`, `:189`, `:227`) and 15 `crbug.com` / 1 `crrev.com` path-only citations (E8, E13).
  Public research, no victim data, no unpublished detail, no access token; the entry transcribes and
  enumerates none of them. **KEEP.**
- **O6 — out-of-scope note for the scope-audit seat.** `LOG.md:1110` (a pre-existing 2026-10-17
  entry, not round 60) carries an org-workspace wiki URL with a `branch` query parameter (no token,
  no signature) (E16). Not credential material and outside this seat's enumerated bytes; no action
  taken or requested beyond the note.

## Residuals and limits

- The screen reads the stored bytes at the snapshot above. The lane tree moved under this seat
  (HEAD `b8c77fb` → `228118a`, lesson/receipts/SCORECARD/LOG committed by the lead), but the screened
  corpus bytes are unchanged since the implementation commit (mtimes in the header) and `git status`
  shows no tracked modification (E0).
- Only the text-converted capture is stored (`S093.txt`); the raw HTML is not in the lane, so this
  screen covers what the lane keeps, not the live page. No network request was made to re-test the
  live page.
- The wave evidence directory is written concurrently by sibling seats; the tree list above and the
  file count are a point-in-time snapshot. Files landing after 2026-11-04T13:44:46Z are not covered
  by this receipt; E17 covers this file itself.
- No probe runner was executed by this seat (the screen is static); E10 confirms the runner leaves no
  residue class in the lane, and the runner's own scratch deletion is by its EXIT trap.
- Scratch: `/fast/scratch/hyaku/kasegi-r60/SentinelCred` was created for TMPDIR isolation and held no
  files; it is removed before yield — no leftover.
- Rule check: nothing in the frozen claims, the erratum, or the probe set conflicts with this seat's
  task; no rule correction is filed.

Report: .ufo/waves/round-60/w1/SentinelCred.md
