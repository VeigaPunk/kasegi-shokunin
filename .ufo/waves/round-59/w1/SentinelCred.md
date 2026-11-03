VERDICT: FINDINGS — 0 CRITICAL, 0 HIGH, 0 MEDIUM, 2 LOW, 5 INFO. No credential material in the round-59 bytes. No private, session or sign-in URL in the F40 entry, the S092 registry row, the README or PROVINCE round-59 blocks, or the manifest. Both LOW items are recommended KEEP (§4, §8). No value is reproduced in this file.

## Anchors

- L = /home/vgpnk/Projects/shokunin/kasegi-shokunin. Lane HEAD at screen time: `git -C L rev-parse --short HEAD` → 15cd577, i.e. the implementation commit 4727378 plus the later round-59 lesson/LOG commit.
- Tools: none installed or updated. Used grep, python3 stdlib (json, re, base64, hashlib), read-only git, and one unauthenticated read of the public GitHub repo API (`https://api.github.com/repos/VeigaPunk/kasegi-shokunin/contents/...`, ref master). No credentials were used.
- Scratch: /fast/scratch/hyaku/kasegi-r59/SentinelCred was created empty and no fixtures were written. Removed before yield (see §12).
- Targets (all read-only): corpus/source-snapshots/round-59/S092.txt, corpus/source-snapshots/round-59/manifest.json, corpus/knowledge/google-big-sleep-findings-tracker.md, corpus/SOURCES.md, corpus/README.md, PROVINCE.md, and every file under .ufo/waves/round-59/controls/.

## §0 Target identity at HEAD versus 4727378

Command:
```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
for f in corpus/source-snapshots/round-59/S092.txt corpus/source-snapshots/round-59/manifest.json corpus/knowledge/google-big-sleep-findings-tracker.md corpus/SOURCES.md corpus/README.md PROVINCE.md .ufo/waves/round-59/controls/s092-issue-shell.html .ufo/waves/round-59/controls/s092-savedsearch-shell.html .ufo/waves/round-59/controls/s092-curl-raw.txt; do
  a=$(git -C "$L" rev-parse "472737847ff31d1255bf1a0745822a5e878e9622:$f"); b=$(git -C "$L" rev-parse "HEAD:$f")
  [ "$a" = "$b" ] && echo "SAME $f" || echo "DIFFER $f"; done
```
Output: SAME ×9 (exit 0). The screened bytes are the frozen-implementation bytes.

## §1 Credential-shape pattern sweep

Command:
```
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; C=$L/.ufo/waves/round-59/controls
T="$L/corpus/source-snapshots/round-59/S092.txt $L/corpus/source-snapshots/round-59/manifest.json $L/corpus/knowledge/google-big-sleep-findings-tracker.md $L/corpus/SOURCES.md $L/corpus/README.md $L/PROVINCE.md $C/s092-issue-shell.html $C/s092-savedsearch-shell.html $C/s092-curl-raw.txt $C/s092-opens-r59.txt $C/s092-variance-check.txt $C/freeze-digests-r59.txt $C/neighbor-screen-r59.txt $C/c1-probe-run.sh $C/c1-residual-run.sh"
for pat in 'AKIA' 'BEGIN [A-Z ]*PRIVATE' 'ghp_' 'xox[abp]-' 'sk-[A-Za-z0-9]' 'password' 'token=' 'Bearer ' 'op://' 'session' 'cookie'; do echo "PATTERN[$pat] lines=$(grep -h -E -- "$pat" $T | wc -l)"; done
```
Output (exit 0):
- AKIA 0; BEGIN [A-Z ]*PRIVATE 0; ghp_ 0; xox[abp]- 0; password 0; token= 0; Bearer 0; op:// 0.
- sk-[A-Za-z0-9] 7.
- session 4 (case-sensitive).
- cookie 1.

The `session` count is case-sensitive. The shells' `buganizerSessionJspb` identifier is matched only by a case-insensitive grep (§5).

## §2 Triage of the 12 non-zero hits (path:line only; values not printed)

Command: `grep -n -E -- 'sk-[A-Za-z0-9]|session|cookie' $T | cut -d: -f1,2 | sort -u`, then matched-word inspection.

- sk- (7 lines), all English words or URL slugs, not key shapes:
  - corpus/SOURCES.md:15 (URL slug containing "questions-ask-using")
  - corpus/SOURCES.md:31, :105, :114 ("task-specific")
  - corpus/README.md:388 ("risk-priority"), :841 ("risk-based")
  - .ufo/waves/round-59/controls/neighbor-screen-r59.txt:75 ("task-spec")
- session (4 lines), workspace directory names or prose:
  - corpus/README.md:27, :111, :137 (`.ufo/sessions/`)
  - corpus/SOURCES.md:174 (prose)
- cookie (1 line): corpus/SOURCES.md:73, the S067 row title "cookie path" (CVE-2025-9086).

All 12 are false positives. No match has a credential prefix or a secret-shaped value.

## §3 Personal data: the masked address (item 2)

### 3a Locator (command run as written; output reproduced form-only)

```
python3 - <<'EOF'
import re
p="/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-59/S092.txt"
lines=open(p,encoding='utf-8',errors='replace').read().split('\n')
for i,l in enumerate(lines,1):
    for m in re.finditer(r'([A-Za-z0-9._%+-]{2,64})@([A-Za-z0-9.-]{2,64})', l):
        loc,dom=m.group(1),m.group(2)
        form = "PREFIX2+ELLIPSIS" if '...' in loc else "FULL-LOCAL"
        print(f"corpus/source-snapshots/round-59/S092.txt:{i}:col{m.start()}-{m.end()} form={form} local_len={len(loc)} domain={dom}")
EOF
```
Output (exit 0), 5 lines:
- corpus/source-snapshots/round-59/S092.txt:2 at col198-214, col815-831, col2984-3000, col6185-6201, col6299-6315.
- Each is form PREFIX2+ELLIPSIS (2 visible characters, an ellipsis, then "@google.com"; local_len=5; domain google.com).
- Two distinct visible-prefix identities, occurring 4 and 1 times (hash-of-local-part run: `distinct_masked_identities=2`, counts 4 and 1).

Same form in the shells (same locator on each file):
- .ufo/waves/round-59/controls/s092-issue-shell.html:24 — 5 occurrences (cols 9606, 10223, 12407, 15608, 15722 region).
- .ufo/waves/round-59/controls/s092-curl-raw.txt:3 — 5 occurrences (`grep -n -o -E '[A-Za-z0-9._%+-]{2,64}@google\.com' <file> | cut -d: -f1 | sort | uniq -c` → `5 3`).
- .ufo/waves/round-59/controls/s092-savedsearch-shell.html — 0 (`grep -c -E '(gl|da)\.\.\.@'` → 0; `grep -o -E '[A-Za-z0-9]{0,4}\.\.\.@' | wc -l` → 0).

### 3b Which field carries it

The owner field the seat names has no label in the bytes. Command (python, stdlib):
```
python3 -c "import json; body=open('/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-59/S092.txt',encoding='utf-8',errors='replace').read().split('\n',1)[1].strip(); issue=json.loads(body)[0][1][22]; ..."
```
(the walk and the label check were run as an inline stdlib script). Results:
- A serialized-issue label check for 'owner', 'Owner', 'assignee', 'Assignee', 'reporter', 'Reporter', 'creator' returned False for all seven.
- The masked string sits in user-tuple slots, all with a masked local part: issue[2][6] (top-level issue record, beside the title "[Big Sleep] README"), issue[13], issue[43][2], issue[43][17] (the README comment object) and issue[47].
- issue[2][6] is the closest structural match to the seat's "owner field". Its role cannot be attributed from the bytes.

### 3c Public exposure of those bytes

Commands (read-only):
- `git -C "$L" branch -r --contains HEAD` → origin/HEAD -> origin/master; origin/master. The HEAD commit is on the remote master.
- `git -C "$L" ls-tree HEAD -- <S092.txt, manifest.json, s092-issue-shell.html, s092-savedsearch-shell.html, s092-curl-raw.txt>` → blobs f39a8e91 (S092.txt), 7337ee66 (manifest.json), cb72054c (issue shell), 6395e0ee (savedsearch shell), 51b8a70c (curl raw).
- GitHub contents API, ref=master, read-only: S092.txt blob f39a8e91…, size 6371; manifest.json blob 7337ee66…, size 3801; s092-issue-shell.html blob cb72054c…, size 88981. These equal the local blob ids.

So the bytes that carry the masked addresses are already on the public master ref.

## §4 Recommendation for item 2: KEEP verbatim (LOW-1)

Reasons:
1. The source masked the address before serving it. What remains is a two-character prefix, an ellipsis and the public domain google.com. It is not a contactable address.
2. The bytes are pinned. S092.txt sha256 is 048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38, and the manifest sha256 is 5b2f4dc7ce5aba3643afbdd06a77c853c13ed5323f48257f400bc46b79b040aa (`sha256sum`, freeze-digests-r59.txt). Any edit changes the C2 pinned digest and trips its kill rule.
3. The bytes are already public (§3c). Removing them from HEAD would not retract the exposure. Only a history rewrite would, and that is out of scope for this round.
4. No claim, quote or entry sentence depends on the owner slot. The pinned quotes Q1–Q10 are all on line 2 at other offsets.

If the operator still wants removal, that is a separate decision: a same-digest redaction receipt (SKILL.md:551 `redactions[]`, and the drift rule at SKILL.md:692) plus a re-pinned manifest and claim. It is not this round's work.

## §5 HTML shell files (item 3): per-request nonces, not credential material

Commands:
- `grep -o -E 'nonce="[^"]*"' <shell> | wc -l` → 16 per shell.
- `grep -o -E 'nonce="[^"]*"' <shell> | sort -u | wc -l` → 2 per shell.
- Set comparison of the two shells' sorted unique nonce sets → DIFFERENT (each fetch got its own nonce set).
- `grep -n -o -E 'nonce="[^"]*"'` line numbers: issue shell 1, 12, 16, 24, 108, 127; savedsearch shell 1, 12, 16, 24, 108, 127.

Classification: CSP script/style nonces on inline elements of one response. They authorise inline script within that response and do not authenticate. They are regenerated per response, so they are per-request but not credential material. Values not reproduced (INFO-2).

Other shell checks:
- Session-named identifier: `buganizerSessionJspb` at line 24 of both shells (case-insensitive grep). Its anonymous state reads ANONYMOUS (count 1). AUTHENTICATED or `"isAnonymous":false` count 0. Not a session credential (INFO-3).
- Sign-in anchor at line 108 of both shells: a `accounts.google.com/ServiceLogin?` link with passive, osid, continue, followup and ec parameters pointing back to the public issue or saved-search URL. No authenticated state (INFO-3).
- `grep -c -i -E 'set-cookie|^cookie:'` over the four capture files → 0. The fetch path is capture-source.py:74: `urllib.request.Request(url, headers={"User-Agent": UA})`, so no cookie jar and no Authorization header. The curl open recorded in controls/s092-opens-r59.txt uses no `-b`, `-c` or `-D` flags.
- gtag measurement id: 1 match on each of lines 12 and 16 of the issue shell (INFO-5). It is a public analytics property id shipped to every browser.

## §6 Query-token URL sweep (item 1, URLs with query tokens)

Command (token-named parameter names, plain or \u003d-escaped):
```
grep -o -E '[?&](token|auth[a-z_]*|sid|ssid|hsid|apisid|sapisid|sig|signature|key|secret|access_token|id_token|session[a-z_]*|at|rt)(=|\\u003d)' $T | sort | uniq -c
```
Output: empty. Zero token-named parameters in any target.

Parameter-name inventory (names only, same $T): `q` in S092.txt (5), issue shell (5), curl raw (5); `family` in both shells (4 each); `a`, `b`, `g`, `m`, `c`, `Ud`, `id`, `onload`, `passive`, `render`, `trustedtypes` in the shells; `inline`, `id`, `cveId` in pre-round-59 SOURCES.md rows.

Interpretation:
- The `q`, `sa`, `source` and `usg` parameters belong to Google's outbound-link redirect wrapper (`www.google.com/url?q=...&sa=D&source=buganizer&usg=...`) inside the README's own link markup.
- `usg` counts: `grep -o -E 'usg(\\u003d|=)[A-Za-z0-9_-]{8,}' <file> | wc -l` → S092.txt 5 (line 2), issue shell 5 (line 24), curl raw 5 (line 3), savedsearch shell 0. Values not reproduced (INFO-1).

Tool note: a `_grep` call with the regex `https?://[^\s"'<>]*\?[^\s"'<>]*=` returned "No matches found" over the same directory, although direct grep matches `?family=` and others in the shells. I did not rely on that call; the `grep -o` results above supersede it. It is recorded for the QA reporter.

## §7 Entry, registry row, README and PROVINCE blocks, manifest

- Entry URLs (`grep -o -E 'https?://[^ )>,`"]+' <entry> | sort -u`): 6 distinct — goo.gle/bigsleep; projectzero blog 2024/06 naptime; projectzero blog 2024/10 from-naptime-to-big-sleep; projectzero blog 2025/07 reporting-transparency; issuetracker issues/430375499; issuetracker savedsearches/7155917. All public canonical pages.
- S092 row (corpus/SOURCES.md:99): 1 URL, issuetracker issues/430375499, no query string.
- README round-59 block (corpus/README.md:968–990): 1 URL, issuetracker issues/430375499.
- PROVINCE round-59 block (PROVINCE.md:205–209): 0 URLs.
- Manifest: `capture_url` = https://issuetracker.google.com/action/issues/430375499 (the tracker's anonymous action endpoint, fetched with a User-Agent only, capture-source.py:74). `url` = https://issuetracker.google.com/issues/430375499. Both public.
- Account and session URL check (`grep -n -E -i 'accounts\.google\.com|ServiceLogin|authuser|[?&]SID=|[?&]SSID=|sessionid|jsessionid|X-Goog-Authentication' <entry> <manifest>` → no match; the same check on the row, README block and PROVINCE block → 0 each).
- Email-shape count (`grep -c -E '[A-Za-z0-9._%+-]{2,64}@[A-Za-z0-9.-]{2,64}'`): entry 0, S092 row 0, README block 0, PROVINCE block 0.
- Opaque base64 tokens in S092.txt:2 (decoded twice, form only, values not reproduced): 2 — at col 772–807 (numeric composite of tracker id-style fields) and col 3114–3181 (32-character hex internal resource id). Neither has a key prefix. INFO-4.

## §8 Host and home-path metadata (LOW-2)

Commands:
- `grep -l -E 'plazir27|/home/vgpnk' .ufo/waves/round-59/controls/* | wc -l` → 16 files.
- `grep -h -E 'plazir27|/home/vgpnk' .ufo/waves/round-59/controls/* | wc -l` → 33 lines.
- Precedent: `git -C "$L" grep -l '/home/vgpnk' 69de8d363b2193fdb37d03fd3e235bceeb1c2daa -- .ufo/waves | wc -l` → 4472 tracked files at the base commit contain the same operator home path, including round-23 onward controls (e.g. .ufo/waves/round-23/c2-controls.txt, .ufo/waves/round-25/c1-controls/*).

Recommendation: KEEP for provenance. These receipts record the measuring host. A corpus-wide redaction is a separate policy decision outside this round. The hostname and home path are reported here by pattern name only.

## §9 Observation for C2 reviewers (not a credential finding)

`controls/s092-opens-r59.txt` prints `curl-normalized-equals-snapshot= False` (CRLF-normalized raw curl bytes compared to the snapshot). `controls/s092-variance-check.txt` reports 0 parsed-structure diff lines. Both are consistent with the manifest's transport-encoding note. Recorded for the C2 reviewer; no action from this seat.

## §10 Findings table

| id | severity | pattern name | path:line | count | recommendation |
|---|---|---|---|---|---|
| LOW-1 | LOW | masked personal-identifier form (2-char prefix, ellipsis, google.com) in user-tuple slots | corpus/source-snapshots/round-59/S092.txt:2; .ufo/waves/round-59/controls/s092-issue-shell.html:24; .ufo/waves/round-59/controls/s092-curl-raw.txt:3 | 5 / 5 / 5 | KEEP (§4) |
| LOW-2 | LOW | operator home path and workstation hostname in committed controls | 16 files / 33 lines under .ufo/waves/round-59/controls/ | 16 / 33 | KEEP (§8) |
| INFO-1 | INFO | redirect-wrapper signature parameter (`usg`) on outbound links | S092.txt:2; issue shell:24; curl raw:3 | 5 / 5 / 5 | KEEP; not auth |
| INFO-2 | INFO | CSP script nonce attributes, one set per response | issue shell lines 1, 12, 16, 24, 108, 127; savedsearch shell same | 16 per shell | none |
| INFO-3 | INFO | session-named JS identifier (anonymous state) and sign-in continuation link | issue shell :24, :108; savedsearch shell :24, :108 | 1 + 1 per file | none |
| INFO-4 | INFO | opaque base64 identifiers (numeric composite; 32-hex id) | corpus/source-snapshots/round-59/S092.txt:2 (cols 772–807, 3114–3181) | 2 | none |
| INFO-5 | INFO | web-analytics measurement id | issue shell:12, :16 | 2 | none |

Verdict counts: 0 CRITICAL, 0 HIGH, 0 MEDIUM, 2 LOW (LOW-1, LOW-2), 5 INFO (INFO-1 to INFO-5). Each count is reproduced by the commands in §1–§8.

## §11 Limits

- The pattern screen covers the shapes the seat named plus the shell-specific checks. It does not prove the absence of bespoke or unlisted secrets.
- Column locators are character offsets in the stored line. S092.txt has one substantive line (line 2).
- The role of the masked slot is not attributable from the bytes, since the capture has no field labels.
- I did not run the lane suite, did not edit any lane file, and did not touch sibling lanes or the fleet root. The only network access was the read-only GitHub repo and contents API, used for §3c.
- No subagent was dispatched (leaf member).

## §12 Scratch cleanup

The scratch directory /fast/scratch/hyaku/kasegi-r59/SentinelCred was created empty and is removed before yield. Nothing was written to it.
