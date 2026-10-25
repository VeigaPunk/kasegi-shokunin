# Sentinel Q6 — target-instruction / documentation-only audit

- Seat: `L1Kasegi23.SentinelQ6-2` (leaf, read-only)
- Wave: kasegi round-23 FALSIFY, C1/C2 artifact attack
- Date: 2026-10-25
- Surface (as assigned): `corpus/knowledge/multiparty-vulnerability-coordination.md` (F06),
  `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` (F07),
  `corpus/knowledge/cra-manufacturer-reporting-duties.md` (F08),
  `corpus/QUALITY.md` Q6 (`:19`), `PROVINCE.md`.
  Secondary, because PROVINCE names them as the governing index / says they are the
  cited support: `corpus/README.md:195-202` (F01-F08 rows) and the three pinned
  snapshots `corpus/source-snapshots/round-23/{S018,S029,S030}.txt`.
- Mutations made: none. Nothing copied, edited, committed, or indexed. The only
  write is this report.

**Verdict: no Q6 failure found on this surface.** Three informational observations,
one uniformity note, no severity ≥ Low. The single sentence that a lexical Q6
detector would flag is an attributed quotation with no endpoint and an explicit
in-entry negation (F1 below).

## Axes named

- **A1 instruction actionability** — does any sentence tell a reader/agent to
  probe, scan, log in to, or submit against anything?
- **A2 secret/credential carriage** — credential material, session state, private
  URL, or vault-reference URI (op-scheme form).
- **A3 host-as-target framing** — is any real third-party hostname presented as an
  asset, scope, or test target rather than as a documentation source?

The distinction the assignment asks for is A3's boundary: a **public documentation
read URL** (`source:` provenance, GET of a published document) versus an
**actionable target instruction** (host named as in-scope asset, plus a verb that
acts on it).

## Method (all commands run from repo root, read-only)

```console
$ grep -hoE '[a-z][a-z0-9+.-]*://' <F06> <F07> <F08> | sort | uniq -c
      3 https://                       # exactly one per entry, each on line 2

$ grep -nE 'curl|wget|nmap|masscan|httpx|nuclei|sqlmap|openssl s_client|ssh |scp |nc -|GET |HEAD |POST |Authorization:|Bearer |User-Agent|--header|-H ' <F06> <F07> <F08>
rc=1                                   # no request-construction primitive anywhere

$ grep -niE 'in[_-]?scope|out[_-]?of[_-]?scope|asset|wildcard|attack surface|test target|target host|endpoint' <F06> <F07> <F08>
multiparty-vulnerability-coordination.md:16:... not ... authorization to test an asset.
cra-manufacturer-reporting-duties.md:68:... does not establish an asset-scope or testing grant.
                                       # both are negations; no positive scope grant

$ grep -nE 'op://|vault://|secret://|keychain://|sops:|age1[0-9a-z]|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20}' <F06> <F07> <F08> corpus/QUALITY.md PROVINCE.md
rc=1                                   # none

$ grep -n 'mailto:' <F06> <F07> <F08> corpus/QUALITY.md PROVINCE.md
rc=1                                   # none

$ grep -nE 'https://[^ ]*(\?|#|@)' <F06> <F07> <F08>
rc=1                                   # no query string, fragment, or userinfo@ — no token-bearing URL

$ grep -nP '<!--|-->|[\x{200B}-\x{200F}\x{202A}-\x{202E}\x{2060}\x{FEFF}]|ignore (all |the )?(previous|prior)|base64|[A-Za-z0-9+/]{80,}' <F06> <F07> <F08> corpus/QUALITY.md PROVINCE.md
rc=1                                   # no hidden comments, zero-width chars, or encoded blobs

$ grep -hoE '[A-Za-z0-9][A-Za-z0-9.-]*\.(com|org|net|gov|eu|int|io|dev|info|uk|de|fr)\b' S018.txt S029.txt S030.txt | sort | uniq -c | sort -rn
      3 eur-lex.europa.eu
      2 supplier.example.com
      1 www.cve.org
      1 example.com

$ grep -c '://' corpus/QUALITY.md PROVINCE.md
corpus/QUALITY.md:0
PROVINCE.md:0

$ grep -n 'recheck' -A0 <F06> <F07> <F08> | cut -c1-120   # identical command in all three:
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S0xx

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018 ; echo rc=$?
S018:sha256 OK  ... 7 quote assertions OK ... rc=0
$ ... --source S030 ; rc=0   (sha256 + 7 quote assertions OK)
$ ... --source S029 ; rc=0   (sha256 + 6 quote assertions OK)
```

Instrument provenance for the `recheck:` field (the only executable instruction on
this surface): `corpus/instruments/source-recheck.py:11-19` imports
`argparse, hashlib, json, os, re, subprocess, sys, tempfile, pathlib` — no
`urllib`, `requests`, `http.client`, `socket`, `smtplib`, or `ftplib` (grep rc=1);
`subprocess` appears only at `:190-194` inside `selftest`, to re-invoke
`sys.executable`. Its docstring `:7-8` states it "reads only local files".
Snapshot reads are confined: `:103` `os.path.commonpath((str(base), str(resolved))) != str(base)`
rejects any manifest path escaping the manifest directory.

## F1 — Info (boundary, no violation): the only normative external-action sentence is a quotation

- **Evidence:** `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:29`
  > `| 4.2.1.1, page 13 | “The CNA with the most appropriate scope MUST be contacted and given the first opportunity to assign.” | An assignment-routing proposal names the appropriate CNA scope and unresolved exceptions. |`

  Containment in the same file: `:30` "unresolved exceptions" (documentary
  consequence), `:37` "does not treat first refusal as unconditional or instruct any
  external contact", `:51` "assignment and external requests remain operator-owned".
  Blocking evidence that it is quotation, not composition: the assertion is present
  as literal bytes in the pinned capture —
  `source-recheck.py ... --source S030` prints
  `S030:rule-4-2-1-1-first-opportunity OK` and the manifest carries that exact
  string (`corpus/source-snapshots/round-23/manifest.json`, S030 quote id
  `rule-4-2-1-1-first-opportunity`).
- **Exploit path (constructed, not executed):** an agent reading only the quote
  table, skipping `:33-37` and `:51`, could treat "MUST be contacted" as a standing
  instruction to contact a CNA. What it then needs is absent: no host, address,
  endpoint, form, or channel is named anywhere in the entry; the only host in the
  file is the `source:` document URL on `:2`; and `mailto:`/`@host` shapes do not
  occur (grep rc=1). Q6's four prohibited verbs are also not the verb used:
  Q6 (`QUALITY.md:19`) enumerates "probing, scanning, logging in to, or submitting
  against any target" — "contact" is outside that list, and there is no object
  ("target") in the sentence.
- **Impact:** none on Q6 as written; the sentence is a statement about CNA
  obligations, scoped to "An assignment-routing proposal names ...".
- **Smallest remediation:** none required. If a future lexical Q6 check is
  introduced, its matcher must be quote-aware (skip inline-quoted spans) or this
  line will be a permanent false positive; that is a note for the criterion owner,
  not an edit to the entry.

## F2 — Info: the three URLs are public documentation reads, not target instructions

- **Evidence (exact lines, one per entry):**
  - `corpus/knowledge/multiparty-vulnerability-coordination.md:2` — `source: S018 — https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1 — version 1.1, Spring 2020; ...`
  - `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:2` — `source: S030 — https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf — CNA Operational Rules 4.2.0, ...`
  - `corpus/knowledge/cra-manufacturer-reporting-duties.md:2` — `source: S029 — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng — Regulation (EU) 2024/2847, OJ 20.11.2024; Articles 14, 15, 16 and 71`
- **Why these are not target instructions (four independent grounds):**
  1. Field position and grammar: all three are the `source:` provenance value
     Q1 (`QUALITY.md:14`) requires; none is an object of an imperative verb.
  2. No action verb attaches to them: the request-primitive grep returns rc=1;
     the accompanied instruction is the `recheck:` line, which is a local
     `python3` call naming an `S###` id, not a URL.
  3. No URL token: no `?`, `#`, or `userinfo@` in any of the three (grep rc=1) —
     no capability-bearing or session-bearing link.
  4. The only executable instruction on the surface is offline and path-confined
     (instrument imports, `:103` confinement, rc=0 runs above), so following the
     entry does not produce a request to those hosts.
- **Impact:** A3 satisfied; a reader can fetch a published document, which is the
  sanctioned research method, and cannot derive an in-scope asset from these lines.
- **Smallest remediation:** none.

## F3 — Info: zero credential, session, private-URL or vault-scheme material

- **Evidence:** `op://`/`vault://`/`secret://`/`keychain://`/`sops:`/PEM/AWS/GitHub
  token patterns → rc=1 across all five assigned files. The word "session" appears
  only inside Q6's own criterion text (`QUALITY.md:19`). `PROVINCE.md:45`
  (`- kagi — secrets and vault handling`) is a sibling-lane attribution with no
  reference, path, item name, or URI — it says which lane owns vault handling, not
  what is in one. `QUALITY.md:19` names the op-scheme form descriptively
  ("vault-reference URI (the op-scheme form)") without an instance.
- **Impact:** A2 satisfied. Note the important negative: the criterion names the
  forbidden form, and naming it is not carrying it; a checker that greps for the
  word "vault" will hit `PROVINCE.md:45` and `QUALITY.md:19` and must not treat
  either as carriage.
- **Smallest remediation:** none.

## F4 — Info: the only hostname-shaped tokens in the captures are reserved placeholders or the citation itself

- **Evidence:** enumeration above — `eur-lex.europa.eu` ×3 in `S029.txt:144,146`
  (footnote links inside the captured OJ text), `www.cve.org` ×1 at
  `S030.txt:1` (the capture's own `URL:` header), `example.com` ×1 at
  `S018.txt:47` (`... in addition to communicating via generic e-mail, like
  secure@example.com.`), `supplier.example.com` ×2 at `S030.txt:85`
  (`- “Supplier Z’s Products listed on <u>[https://supplier.example.com/security/cvescope](...)</u>"`).
- **Grounding that `example.com` is not a third party:** RFC 2606 §3 ("Reserved
  Example Second Level Domain Names") reserves `example.com`, `example.net`,
  `example.org`; §2 reserves `.example` "for use in documentation or as examples"
  (read 2026-10-25, https://www.rfc-editor.org/rfc/rfc2606.txt:84-116). So
  `secure@example.com` cannot be a real contact and `supplier.example.com` cannot
  be a real scope page. Both are model examples inside quoted source text.
- **Also verified:** neither placeholder appears in any of the three entries
  (`grep -n 'example\.com' <F06> <F07> <F08>` rc=1). The entries carry no
  hostname other than their three `source:` URLs.
- **IPv4-shaped false positive, disclosed:** `cna-assignment-and-vulnerability-rules.md:29,33`
  match an IPv4 regex, but the tokens are `4.2.1.1` and `3.2.4.2` — CVE rule
  numbers, not addresses. No IPv4 literal exists on the surface.
- **Impact:** A3 satisfied even in the captured text.
- **Smallest remediation:** none. If a future captured snapshot ever contains a
  real security contact, that would be the moment to require redaction at capture
  time (the entry text is clean either way).

## F5 — Info (supporting control): Q6's cited groundings resolve, and its "instructs" clause has no hit outside negations

- **Evidence:** `QUALITY.md:19` grounds Q6 in "A3 — ..." and "`PROVINCE.md` refuses
  out-of-scope action". That citation resolves: `PROVINCE.md:26`
  ("**Refuses:** anything outside this domain; ...") and `PROVINCE.md:49`
  ("Live-target testing is refused; this corpus is documentation only.").
- **Verb census for Q6's four prohibited verbs** across the three entries:
  `probing`/`scanning`/`logging in`/`submitting` occur only as
  `cra-manufacturer-reporting-duties.md:73` (all four, negated: "no target contact,
  scanning, login, report submission, or account operation"),
  `cra-manufacturer-reporting-duties.md:39` (negated: "not ... a direction to
  submit anything"), and `multiparty-vulnerability-coordination.md:17`
  ("Publishing, contacting external parties and submitting reports remain
  operator-owned"). Zero affirmative occurrences. The two nearest affirmative
  phrasings are themselves documentary: `multiparty-vulnerability-coordination.md:11`
  ("Record contact ownership") and `:39` ("No network action is necessary to
  perform this check").
- **Impact:** A1 satisfied on the narrow lexical reading and on the
  intent reading.
- **Smallest remediation:** none.

## N1 — uniformity note (not a finding, not a violation)

F08 states the Q6 disclaimer as an explicit enumeration
(`cra-manufacturer-reporting-duties.md:73`). F06 and F07 state the same limit in
different words — F06 `:16-17` ("not ... a mandate to contact anyone, or
authorization to test an asset"; "Publishing, contacting external parties and
submitting reports remain operator-owned"), F07 `:37,51` ("instruct any external
contact"; "external requests remain operator-owned"). All three pass Q6 as written.
A uniform sentence would make the property machine-checkable per entry; that is a
future-criterion choice, and changing any of the three entries now would move line
anchors (R6 concern), so I recommend leaving the bytes alone this round.

## What this report does not establish

- Not an admission, a rejection, or score movement. No claim of Q1-Q5 or R1-R9
  compliance; only Q6's documentation-only, credential, and host-as-target clauses.
- Not a Q7 verdict: I ran the entries' `recheck:` command and recorded rc=0 and
  per-quote OK lines, but I did **not** exercise a missing/corrupted-source control,
  and a pinned-capture comparison is not freshness. Another seat owns that.
- Not a legal or policy reading of any source; I did not assess whether FIRST, CVE,
  or EUR-Lex content is current.
- I did not verify that the three cited URLs are reachable or serve the same bytes
  today. Publicness is grounded on URL form plus `corpus/SOURCES.md:24,35,36`
  (`docs`/`spec`, tier `A`) and the instrument's offline design — deliberately not
  by contacting those hosts (see next section).

## Network disclosure (A3 discipline — stated, not absolute)

I made exactly one external read, to ground the `example.com` claim: RFC 2606 via
`https://www.rfc-editor.org/rfc/rfc2606.txt:1-80` and `:84-125`, a public
documentation read. I performed **no** request against `www.first.org`,
`www.cve.org`, or `eur-lex.europa.eu`, no GET/HEAD availability check, no
credential or account action, and no traffic to any host named in the corpus. I do
not claim "no host was contacted" — one host was read, and it is named here.

## Falsifiers (what would overturn this report)

- Any affirmative imperative in an entry whose object is a host/asset/endpoint
  (e.g. `grep -nE '(probe|scan|log ?in|submit)[^.]{0,60}(https?://|\bhost\b|\basset\b)'` returning a hit).
- A non-https scheme, `userinfo@`, query token, or `mailto:` in an entry's URL:
  `grep -nE '[a-z]+://[^ ]*(\?|#|@)|mailto:'` on the three entries returning a hit.
- A vault-reference or credential pattern on the five files: the F3 grep returning
  a hit.
- A real (non-RFC-2606) third-party hostname carried by an entry rather than by a
  `source:` line, or a snapshot hostname described as in-scope/owned/testable.
- A network import or URL fetch inside `source-recheck.py`, or a `recheck:` line
  that is an HTTP call rather than a local command.
