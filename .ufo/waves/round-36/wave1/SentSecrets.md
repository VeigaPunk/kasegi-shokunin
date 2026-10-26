# SentSecrets — round-36 credential / probe-instruction scan (wave 1, leaf sentinel)

Seat `SentSecrets` (sentinel, axis `scope`), round 36, hyaku run 9. Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `cc692008b0cfd58d18275aa6c4aed79620120799`;
claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`. Bounds: leaf, no subagents, no swarm, no
`agent://all`. Writes: this receipt only, plus files under
`/fast/scratch/hyaku/kasegi-r36/SentSecrets/` (removed before yield). No lane, fleet, sibling-lane or
source-tree byte was edited; no git/jj mutation; `pacman` not invoked; nothing installed or upgraded.

**Scan of record:** `2026-10-26T16:11:27Z`, over **78 files / 2,338,369 bytes** under
`.ufo/waves/round-36/`, manifest sha256
`28ce57c64dfd2e1d344fca6954b8ad86779add2f5b73456a7244ec19e05c1cc5` (sha256 of the sorted
`<path> <sha256>` list). That set is 63 landed peer receipts under `wave1/` plus 15 dispatcher/control
artifacts, including `c2-controls/junk-f19.md` and `final-gates/all-gates.txt`. `MutC1Suite.md` (the last
peer to land, 13:10 local) is inside the set. The lane moved during the item: integration commit
`a23dc4788aa7c98831eed6db953434034ce5ae8d` landed at `16:00:31Z` and committed the wave; the only file that
changed **after** the scan of record is `wave1/RevSpotCheckReadiness.md` (`13:12:24` local), re-scanned in
§6 with the rebound manifest `60ca2d20…`.

## Verdict

**CLEAN — no credential material, no session/auth value, no private URL or vault reference, and no
actionable instruction to probe, scan, log in or submit against anything.**

- `blocking_findings: 0`; `credential_material: 0`; `session_auth_values: 0`; `vault_or_private_urls: 0`;
  `real_account_identifiers: 0`; `actionable_instructions: 0`.
- Two independent detectors agree: `gitleaks 8.30.1` → `no leaks found` (0 findings); the seat scanner's
  strict S1/S2 classes → 0 after triage; POSIX-grep families → exit 1 (no match).
- Within the scanned set, the only S1-class matches are **detection-pattern literals quoted in a peer's
  false-positive ledger** (`CritBoundary.md:110`), not key material: an `op://` example placeholder and the
  PEM-header marker with no key body. The only instruction-family match in the proposed entry is its own
  **negation** of probe/scan/login/submission.

## 1. Scope and method

Enumerated the wave dir itself (`Path.rglob("*")`, every regular file), not a hand list; no file was
skipped by name, including dotfiles and mode-600 `wave1/swarm-registry.json`. Read-only throughout.

Three independent passes:

1. **`gitleaks detect --no-git --source .`** — provider key shapes and its own entropy rules. Output:
   `INF scanned ~2345853 bytes` → **`no leaks found`**, report JSON `[]`.
2. **Seat scanner (strict classes, secrets masked).**
   - **S1 credential material:** AWS ids, GitHub/GitLab/Slack/Stripe/OpenAI/Google/HF/npm/PyPI/SendGrid/
     Docker tokens, JWT triples, PEM private-key blocks, AGE secret keys, `op://`/`vault:` references *with
     a payload*, `_authToken=`.
   - **S2 session/auth values:** `Authorization`/`Cookie`/`Set-Cookie`/`X-Api-Key` headers carrying a value,
     `Bearer`/`Basic` values, `password|api_key|access_key|secret_key|client_secret|session_id|auth_token`
     assignments, userinfo URLs (`scheme://user:pass@`), `?token=|?key=|?sig=` parameters, `.netrc`/`id_rsa`/
     `.aws/credentials`/`.config/gh`/`.docker/config.json`.
   - **S3 triage (never blocking):** emails, `@handles`, cleartext `http://`, tracking params, private IPs,
     HOME-account paths, opaque URL path tokens.
   - **INSTR:** login/sign-in/authenticate, probe/scan/nmap/masscan/shodan/censys/nikto/gobuster/sqlmap,
     credential submit/exfiltrate, `curl -u/-d/-H Authorization/-b`, session-probe phrasings.
   - For `.json`/`.out` files every **parsed string value** was re-scanned as well as the raw bytes, so a
     payload hidden behind JSON escaping cannot evade the rules.
3. **POSIX-grep cross-check** (independent of the Python scanner): header-like, bearer/basic, sensitive
   assignment, PEM block, `op://`/`vault:` payload → **all exit 1** (no match), except the one pattern-literal
   line catalogued in §4.

## 2. Findings

| class | verdict | location | evidence |
|---|---|---|---|
| S1 credential material | **none** | — | 0 real hits; the only two S1 matches are pattern literals (§4.a) |
| S2 session/auth values | **none** | — | 0 header values, 0 bearer/basic values, 0 assignments, 0 userinfo URLs, 0 token query params, 0 key-file paths |
| private URL / vault ref | **none** | — | 0 `op://`/`vault:` with payload; 0 `.internal/.corp/.lan/.local` hosts; 0 loopback/private-IP URLs |
| account identifiers | **none real** | `ExecC1Fixtures.md:421`; `ExecQuiescenceProbe.md:465,551,562`; `ExecC1Fixtures.md:554-637` | two synthetic `.invalid` fixture addresses and an `@mutant` Python decorator, not accounts (§4.b-c) |
| URL credentials | **none** | — | 8 unique URLs, 0 with `user:pass@`, 0 with a token/key query parameter (§3) |
| probe/scan/log-in instruction | **none actionable** | `ScribeEntryF19.md:32,297` (negations only) | entry explicitly negates; all 123 lexical "probe/scan" matches are nouns or descriptions (§5) |
| operator path | INFO, pre-existing | lane-wide `/home/vgpnk/...` | 3,294 base files already carry it at `cc69200`; an operator path, not a secret |

## 3. URL / network inventory

Eight unique URLs across the whole wave dir; every host is public, none carries credentials:

```
https://www.first.org/epss/                         (×80 across receipts)
https://www.first.org/epss                          (slashless form, redirect case)
https://www.FIRST.org/epss/                         (case variant of the same public page)
https://www.first.org/epss/?x=1                     (URL-binding fixture, parameter is literal "x=1")
https://www.first.org/epss/data_stats               (public sub-page)
https://www.first.org/cvss/v4.0/user-guide          (public sub-page)
https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json   (quoted, round-35 provenance)
https://shokunin.invalid/kasegi                     (RFC-2606 reserved host in the instrument UA)
```

`userinfo_url` 0; `sensitive_query_token` 0; private-IP literal 0; cleartext `http://` 0; tracking
parameter 0. The only opaque identifiers are two **per-request redirect path segments** on
`kass.sacinfo.org.cn/kfs/token/download/…`, masked in this receipt (`ltwf…rdz`, `sakj…vsl`) and located at
`ScoutQuarantine.md:48,49,87` and `ScribeGateLesson.md:237-238`: produced by a 302 from a public standards
host, fetched with no auth header/cookie, and **0 bytes retrieved** (TLS verification failed, curl 60). The
peer itself records that the values change per request, so they cannot be bound as a credential; classified
INFO, not a secret.

**Network behaviour in proposed content.** Ten files mention `curl`/`urllib`; every invocation is a
read-only GET of `https://www.first.org/epss/` under the instrument UA, with `--max-time`, TLS verified (no
`-k`), and **no** `-u`, `--user`, `-H Authorization`, `-b/--cookie`, `-d/--data`, `--form`, POST, `wget` or
`nc`. Capture provenance (`ExecC2Capture.md:20`) is UA-only; `corpus/instruments/source-recheck.py` and
`recheck-audit.py` contain **0** network references (local capture bytes only).

## 4. False-positive ledger (catalogued, not re-filed)

**a. `CritBoundary.md:110` — the only S1-class line.** It is the critic's credential row, quoting the
detection patterns it swept for, explicitly noting they are "regex literals inside `SentSecrets`' own scanner
source". The `op://…` string is an example placeholder with no vault hostname/item; the PEM line is a header
marker with no base64 body, no `Proc-Type`, no preceding key material. Not a key, not a vault reference.

**b. Synthetic fixture identities.** `ExecC1Fixtures.md:421` uses `fixture@r36.invalid` in
`git -c user.email=…`; `ExecQuiescenceProbe.md:465,551,562` use `quiescence-fixture@example.invalid` in the
same way. Both TLDs (`invalid`, `example.invalid`) are RFC-2606 reserved; they identify throwaway scratch
commits, not people or accounts.

**c. `@mutant` decorators.** 14 `@mutant("E1a")`-style matches at `ExecC1Fixtures.md:554-637` are Python
decorators in the embedded fixture source, not social handles.

**d. Pseudo-entropy from path assignments.** `ExecC1SuiteBuild.md:579` (`SCRATCH_ROOT=/fast/scratch/…`),
`ExecGateReviewPrep.md:569` (`fixture_toplevel=/fast/scratch/…/sandbox/lane`), and
`ExecQuiescenceProbe.md:127` (`toplevel=/fast/scratch/…/fix.<mktemp>` ) are path assignments whose
high-entropy score comes from the scratch directory name; no secret value.

**e. "probe"/"scan" vocabulary.** This corpus's vocabulary makes the word `probe` ubiquitous and mostly a
noun: `Gates & probes` registry, `kind=probe` cell, `mutant-probe`, `retained probe`, `probe receipt`,
`probe-bound`, `token scan`, `row scan`. An imperative cross-check
(`run|execute|perform|launch|start|do|must|should [up to 40 chars] probe|scan|log-in|authenticate`) returns
only matcher/artifact prose — no instruction to act on a target.

**f. This receipt's own text (self-reference, not a finding).** `SentSecrets.md` is not in the scan of
record (it was written after it). It deliberately names detector classes (`scheme://user:pass@`, `.netrc`,
`id_rsa`, `.aws/credentials`, PEM/`op://` families), the synthetic fixture addresses and the `@mutant`
decorator, and it uses the project's probe vocabulary. A later run of any scanner over the wave dir will
therefore flag this receipt as S2/S3/INSTR **pattern mentions** and will re-print the §8 grep patterns. Those
are descriptions and commands, not values; `gitleaks` over this receipt alone returns 0 findings.

## 5. Proposed entry/rows — instruction check (the item's second half)

- **`ScribeEntryF19.md` §6 — the proposed knowledge entry.** No credential, session value or private URL.
  Its Q6 row (`:32`) reads "no credential, session or private URL; no probing/scanning/login/submission
  instruction; the only commands read local capture bytes", and the Honest-limit bullet (`:297`) closes with
  "Nothing here authorizes probing, scanning, logging in, or submitting against any target." The single
  `recheck:` line (`:146`) is `python3 corpus/instruments/source-recheck.py --manifest … --source S053`, a
  local pin comparison (the entry's note says "not a fresh network check"); FC-1..FC-5 are `grep`/`python3`
  over `corpus/source-snapshots/round-36/S053.txt`. The words `curl`/`wget`/`urllib`/`requests` occur only in
  the receipt's provenance/tooling sections (`:50`, `:420`), **not** in the entry text.
- **`ScribeRowS053.md` — the proposed SOURCES row, Search-log bullet and Paths line.** 0 `curl`/`wget`/
  `urllib`/`requests` occurrences; its only command is the local negative sweep
  `grep -rn "EPSS\|exploitation-likelihood" corpus/knowledge/`; the source cell carries exactly one
  `https://` token, the public `https://www.first.org/epss/`. No probe/log-in instruction.
- **`c2-controls/junk-f19.md` — the committed rejecting twin.** 0 network words; its `recheck:` (`:12`) is
  the same offline `source-recheck.py` instrument. Its fabricated sentence is a claim defect for the C2
  control, not credential or probe content.
- **Lesson / LOG / SCORECARD / report / assimilation / QUALITY-row / Mistakes drafts** (`ScribeGateLesson`,
  `ScribeLOG`, `ScribeScorecard`, `ScribeReportDraft`, `ScribeAssimilationGate`, `ScribeQualityRows`,
  `ScribeMistakes`, `ScribeShonen`, `ScribeConsiderthese`, `ScribeSOURCSCorrection`): no credential material,
  no probe/log-in instruction. Their "probe" occurrences are the registry noun, `probe-bound` measurement
  prose, or first-person descriptions of the sanctioned one-fetch-per-row documentation capture.

## 6. Coverage and liveness

- At the scan of record: **63/63** non-self seats had filed a receipt under `wave1/` (the 64th is this one),
  plus 14 dispatcher/control artifacts (`build-spec.py`, `claims.json`, `census-before.txt`,
  `c1-controls/before.txt`, `c2-controls/before.txt`, `c2-controls/junk-f19.md`, `wave1-dispatch.json`,
  `wave1-spec.json`, `wave1-plan.{out,err}`, `wave1-run.err`, `wave1.ready{,.dispatched}`,
  `wave1/swarm-registry.json`) and `final-gates/all-gates.txt`. Nothing in the wave dir was excluded from the
  raw scan; this receipt is self-excluded (it did not exist at scan time).
- **Integration commit and post-scan delta.** HEAD moved from the freeze `b47f2cdf…` to
  `a23dc4788aa7c98831eed6db953434034ce5ae8d` (committed `16:00:31Z`) while this seat ran; the commit
  carries the wave dir. Five **tracked** receipts (`ExecC1SuiteBuild`, `RevC1Suite`, `RevSpotCheckReadiness`,
  `ScribeGateLesson`, `SentScope`) were modified after the commit, and `MutC2Entry` landed untracked, all in
  the 16:02–16:12Z window; the scan of record (16:11:27Z) already covered all but one. `wave1/RevSpotCheckReadiness.md` changed at
  `16:12:24Z` (34 insertions / 6 deletions: first-hand suite measurements, no credential or command
  content); it was re-scanned first-hand — gitleaks → 0, key/header/assignment grep families → exit 1,
  current sha256 `7f60df1dbadb12edbe6cfeb93377ba7c6b9799138752b0f051a9fa1f8d410e7f`. Rebinding the
  manifest over the 78 non-self files at `16:13:46Z` gives
  `60ca2d203b17b6ad683b2f3f524565caeb6de106552fcefad699955c4824d3bd` (2,339,233 bytes); no file other
  than that receipt (and this one) has a post-scan mtime.
- **Process observation (cleanup, not a lane defect).** Between the quiescence watch's last sample and the
  scan, `SentSecrets/` under `/fast/scratch/hyaku/kasegi-r36/` was removed by something other than this seat
  (parent mtime 13:05 local) while the seat was still live; the scratch tree and scanner were recreated and
  every number in this receipt recomputed from the lane bytes. No lane file was affected. This matters to E9:
  a shared-root sweep can make `scratch_leftovers=0` true before all seats have yielded, so E9's green is only
  meaningful when read together with receipt completeness.
- After this receipt lands the wave dir gains one file (this one); the scan-of-record manifest does not cover
  it.

## 7. Limits

- Byte inspection only; it proves the absence of credential-shaped strings in **these** bytes, not the
  absence of a secret in a source they reference. The lane's committed capture/fixtures outside the wave dir
  were not re-scanned; the capture's bytes are reproduced verbatim inside `ExecC2Capture.md` §6 and were
  scanned there.
- Point-in-time. The wave dir is an integration-in-progress artifact: anything appended after
  `16:11:27Z` is outside this record.
- The custom scanner lived in scratch and is removed; the gitleaks command, the POSIX families and the
  class definitions above are the reproducible residue. The two documented S1-pattern-literal hits are the
  expected grep output, not findings.
- "Account identifier" is read narrowly: emails, handles, cloud account ids, HOME paths. No 12-digit
  account id, internal host, or user handle was found; `/home/vgpnk` is the pre-existing operator path.

## 8. Re-run

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-36
gitleaks detect --no-git --source . --report-format json --exit-code 0        # 0 findings
grep -rInE '(AKIA|ASIA)[0-9A-Z]{16}|ghp_|github_pat_|glpat-|xox[baprs]-|AIza|sk-(proj-|ant-)?[A-Za-z0-9]{16}|hf_[A-Za-z0-9]{20}|npm_[A-Za-z0-9]{30}|eyJ[A-Za-z0-9_-]{10,}\.' .
grep -rInE '-----BEGIN .*PRIVATE KEY-----|op://[A-Za-z0-9]|vault:(//)?[A-Za-z0-9]' .   # only CritBoundary:110 (pattern literals)
grep -rIniE '(authorization|cookie|x-api-key)[[:space:]]*:[[:space:]]*[^[:space:]]|bearer[[:space:]]+[A-Za-z0-9._~+/=-]{12,}' .   # exit 1
grep -rIniE '\b(password|passwd|pwd|api[_-]?key|apikey|access[_-]?key|secret[_-]?key|client[_-]?secret|session[_-]?id|csrf[_-]?token|auth[_-]?token)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9._~+/-]{6,}' .   # exit 1
```

Expected: `no leaks found`; the S1 grep family prints only the one `CritBoundary.md:110` line; the last two
print nothing and exit 1. A later scan should also re-read `ScribeEntryF19.md` §6 if it is re-landed, since
that is the only proposed content with a text body.

## 9. Structured summary

```json
{
  "seat": "SentSecrets",
  "wave": "round-36/wave1",
  "scope": "credential / session / private-URL / account-identifier / probe-instruction scan of the round-36 wave dir",
  "scan_of_record_utc": "2026-10-26T16:11:27Z",
  "head_at_scan": "a23dc4788aa7c98831eed6db953434034ce5ae8d",
  "verdict": "CLEAN",
  "blocking_findings": 0,
  "refused": false,
  "coverage": {
    "files": 78,
    "bytes": 2338369,
    "manifest_sha256": "28ce57c64dfd2e1d344fca6954b8ad86779add2f5b73456a7244ec19e05c1cc5",
    "manifest_sha256_rebound_161346Z": "60ca2d203b17b6ad683b2f3f524565caeb6de106552fcefad699955c4824d3bd",
    "post_scan_delta": {
      "file": "wave1/RevSpotCheckReadiness.md",
      "sha256": "7f60df1dbadb12edbe6cfeb93377ba7c6b9799138752b0f051a9fa1f8d410e7f",
      "gitleaks": 0,
      "grep_families_exit": 1
    },
    "receipts": 63,
    "non_receipt_artifacts": 15,
    "missing": 0,
    "self_excluded": "wave1/SentSecrets.md",
    "tools": ["gitleaks 8.30.1", "python3 (seat scanner)", "grep -E/-P cross-check"]
  },
  "blocking_classes": {
    "S1_credential_material": 0,
    "S2_session_auth_values": 0,
    "private_or_vault_urls": 0,
    "real_account_identifiers": 0,
    "actionable_probe_scan_login_instructions": 0
  },
  "triage": {
    "pattern_literal_S1_hits": ["wave1/CritBoundary.md:110 (op:// example + PEM marker, no key body)"],
    "synthetic_fixture_emails": ["wave1/ExecC1Fixtures.md:421", "wave1/ExecQuiescenceProbe.md:465,551,562"],
    "decorator_handles": ["wave1/ExecC1Fixtures.md:554-637 (@mutant)"],
    "opaque_redirect_path_tokens_masked": ["wave1/ScoutQuarantine.md:48,49,87", "wave1/ScribeGateLesson.md:237-238"],
    "path_assignment_entropy": ["wave1/ExecC1SuiteBuild.md:579", "wave1/ExecGateReviewPrep.md:569", "wave1/ExecQuiescenceProbe.md:127"],
    "operator_path": "/home/vgpnk pre-existing in 3294 files at base cc69200"
  },
  "proposed_content_check": {
    "entry": "wave1/ScribeEntryF19.md §6 — Q6/Honest-limit negate probing; recheck is offline source-recheck.py; FC-1..FC-5 local greps",
    "row": "wave1/ScribeRowS053.md — 0 network words; local negative sweep only",
    "junk_twin": "c2-controls/junk-f19.md — 0 network words; offline recheck",
    "verdict": "no credential material and no probe/scan/log-in/submission instruction"
  },
  "network_inventory": {
    "unique_urls": 8,
    "hosts": ["www.first.org (incl. www.FIRST.org case variant)", "www.cisa.gov", "shokunin.invalid (RFC-2606)"],
    "auth_headers": 0, "cookies": 0, "userinfo_urls": 0, "token_query_params": 0, "cleartext_http": 0,
    "uploads_or_posts": 0,
    "only_network_actions": "UA-only, TLS-verified GETs of public documentation/feed pages"
  }
}
```

## 10. Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r36/SentSecrets/` (both scanner revisions, gitleaks reports, snapshot
JSONs) is removed after this receipt is written; `ls -d` on it afterwards is expected to fail. No tool was
installed or upgraded for this item (`gitleaks 8.30.1` was already present at `~/.local/bin/gitleaks`);
`pacman` was not invoked.
