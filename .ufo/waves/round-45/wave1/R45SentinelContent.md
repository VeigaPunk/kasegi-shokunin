VERDICT: HOLDS

# R45 sentinel: content-safety review of S071, S072, manifest.json, claims.json

Scope: `corpus/source-snapshots/round-45/{S071.txt,S072.txt,manifest.json}` and `.ufo/waves/round-45/claims.json` (tracked, worktree == HEAD, freeze commit `8cf62c8`), plus the two `source-recon/` capture headers as adjacent evidence. Read-only; no git mutation; no network contact.

## 1. Credential, session, vault and private-URL scan: no hits

Command (grep tool, credential/session/op:// pattern over the four files) printed:

    No matches found

Heuristic scanner `scan.py` (13 categories: credential keyword, PEM block, known token prefixes, `op://`, `?session=/token=/key=` params, login/auth paths, e-mail, URL, live-verb list, base64-ish and hex runs, hidden Unicode, non-ASCII count). Output on the four files, categories with hits only:

- `manifest.json`: `url: 6 hit(s)` (lines 6, 7, 10, 49, 50, 53: `docs.kernel.org/...security-bugs...` and `bughunters.google.com/rest/v1/articles/about/rules/about-this-section`). `credential-keyword`, `op-scheme`, `session-or-auth-param`, `email`: 0.
- `S071.txt`: `email: 13 hit(s)` (lines 139, 140, 147-150, 159, 166, 281); `url: 2` (lines 252, 338); `exec-or-live-verb: 2` (lines 116 `scanning`, 189 `scan`, both prose). Hidden Unicode 0; non-ASCII 0.
- `S072.txt`: `url: 6` (lines 10, 213, 225, 229 x2, 237); `exec-or-live-verb: 1` (line 229 `Exfiltrate`); non-ASCII 1 (line 2, U+2019 in "you’ll").
- `claims.json`: 0 in every category except a 40-hex commit id (line 6, `dc5bb8c6...` base rev, not a secret).
- Adjacent `source-recon/S071.headers.txt` (19 lines): all categories 0 (no `Set-Cookie`, no auth header; the only header of note is `date: Wed, 28 Oct 2026 20:52:44 GMT`).
- Adjacent `source-recon/S072.json`: same six URLs as S072 line 229 et al., plus the same `Exfiltrate` token.

Discrimination (do-nothing and canary controls, same scanner):

    == do-nothing-control.txt  (one benign line)
      credential-keyword: 0 hit(s) ... url: 0 hit(s) ... exec-or-live-verb: 0 hit(s) ... hidden-unicode: 0 hit(s)
    == positive-canary.txt  (planted: op://Vault/Item/field, ?session=abc123, ?token=zz9, ghp_..., dev@example.com, exploit payload, PEM header, U+200B)
      op-scheme: 1 hit(s) ... session-or-auth-param: 2 hit(s) ... private-key-block: 1 hit(s)
      known-token-prefix: 1 hit(s) ... email: 1 hit(s) ... hidden-unicode: 1 hit(s) (0x200b)

So the zero-hit categories above are not a dead regex: the scanner fires on every planted class and stays silent on the control.

Integrity of the four files (sha256 matches manifest, read-only):

    0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  corpus/source-snapshots/round-45/S071.txt   (manifest S071 sha256 match, 20152 bytes)
    364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025  corpus/source-snapshots/round-45/S072.txt   (manifest S072 sha256 match, 10032 bytes)

`git diff --quiet HEAD -- <the four files>` exited 0 (worktree equals HEAD).

## 2. Live-testing or submission instructions inside the captures

No line instructs the corpus reader to probe, scan, log into, or submit against a live system. Three source lines are hazards that the entry must not copy as imperatives:

- **S072:229 `Exfiltrate flags at InternetCTF`** (also `docs.google.com/forms/.../viewform?usp=sf_link`). A CTF "exfiltrate" instruction against a live contest target, and a survey submission endpoint. This is the most serious item in the bundle. It sits in the "OSS" table, not in the Cloud row the C1 R1 rests on (S072:148-149).
- **S071:206-211, 232-251, 265-297** (reproducer, "AI-assistant MUST" procedure, "Sending the report"). These are imperatives to a reporter or AI tool: test the reproducer, write a fix, identify maintainers, send e-mail, Cc the security team. Describing a submission procedure is what `QUALITY.md` Q6 forbids ("never instructs ... submitting against any target").
- **S071:252 `https://github.com/masoncl/kres.git`** (a pointer to an external automated AI bug-finding process). Not a credential; a pointer to automated discovery tooling the corpus does not need.

Commands in the capture (S071:137-138, 146, 156-158, 163-165: `get_maintainer.pl ...`) are local-tree transcripts, not live-target instructions, but they are how-to text and should not be copied.

## 3. The security@kernel.org question (S071:280-282)

Governing rule: there is **no `CORPUS.md` in this repository** (`ls` returned `No such file or directory`; the seat text is stale). The rules that apply are:

- `corpus/QUALITY.md:19` (Q6): "Documentation-only: never instructs probing, scanning, logging in to, or submitting against any target; carries no credential material, session or private URL, or vault-reference URI (the op-scheme form)."
- `PROVINCE.md:52`: "Live-target testing is refused; this corpus is documentation only."
- `PROVINCE.md:48`: "kagi — secrets and vault handling" (credential handling is owned elsewhere).

Ruling: `security@kernel.org` at S071:281 is a published upstream contact for a public policy document. It is not a credential, not a session or private URL, and not a vault reference, so copying it does **not** violate the Q6 literal text. Recommended handling anyway:

- Do not copy the address into the entry. Cite the location, for example "the Linux kernel security team's published contact (S071:280-282)".
- Do not turn it into a recipient step ("send to security@..."). Q6 treats that as instructing a submission against a target. Keep it as a documented fact about the process.

The `dev1@example.com` ... `dev4@example.org` addresses (S071:139-166) are RFC 2606 placeholders. Do not copy them.

## 4. What the entry must not copy (recommendations)

| Location | Content | Recommendation |
|---|---|---|
| S071:137-166 | `get_maintainer.pl` transcripts and example.com/.org addresses | do not copy |
| S071:206-211 | reproducer sharing and testing instructions | paraphrase the policy only, if at all |
| S071:232-251 | "AI assistant MUST" procedure | do not copy; policy line Q2 (S071:95-96) is enough |
| S071:252 | `github.com/masoncl/kres.git` | do not copy or link as a recommended tool |
| S071:265-297 | "Sending the report" imperatives, Cc rules | paraphrase as documented policy only, never as a step |
| S071:281 | `security@kernel.org` | do not copy verbatim; cite S071:280-282 |
| S072:229 | "Exfiltrate flags…", Google Forms survey URL | do not copy |
| manifest.json:49-53 | REST capture URL | cite as the snapshot `url:`; never use as a `recheck:` command |

Safe to quote (policy text, all ≤25 words, located): S071:310-311 (7/14-day embargo ceiling), S071:95-96 (AI-found bugs treated as public), S071:39 (binary-only reproducers refused), S071:41-43 (unreproducible is not exploitable), S071:20-21 (no version indication, not processed), S072:148-149 (Cloud VRP scope).

Two entry-level requirements that the content review surfaces:

1. **A3 disclosure.** `manifest.json:13` and `:56` record `fetched_utc` 2026-10-28T20:52:44Z and 20:53:00Z with HTTP 200 for two public hosts. The entry must not claim "no live host contacted"; say the snapshots were captured by GET at those timestamps.
2. **Recheck (Q1).** A `recheck:` command must be local, such as `sha256sum` against `corpus/source-snapshots/round-45/S071.txt` with the manifest hash. A network fetch of `bughunters.google.com/rest/...` or `docs.kernel.org` would be a live contact.

## 5. Adjacent provenance defects (not content-safety, reported for the C2/C1 owners)

- **`manifest.json:70`: S072 Q2 anchor is 1, which is a blank line.** The quote "an overview of the different vulnerability reward programs Google maintains" starts at S072:2 ("an overview of the different", line 2; "vulnerability reward programs Google maintains," line 3). Command output: `S072 Q2 anchor 1 quote-found-in-file True first-3-words-line 2 exact-line-contains-start-at-anchor False`. Recommend anchor 2. This matters because C1 R1 rests on S072.
- **S071 Q4 anchor 41 is correct.** The quote begins with "By" as the last word of line 41; the check returned False only because my test looked for three words on one line.
- **`claims.json` says "curly quotes".** S071 has zero non-ASCII characters (scanner: `_nonascii_chars: 0`), so S071-derived quotes cannot contain curly quotes. S072 has one curly apostrophe (S072:2), outside all of its manifest quotes.

## 6. Limitations

- The scanner is heuristic (regex plus 40-char runs). It is not a secret scanner with entropy models or a provider-specific rule set. The zero-hit result means "none of these 13 classes present", not "no secret possible".
- I read the four files plus the two `source-recon/` headers only. I did not read `freeze-controls.txt`, the round-45 drafts, or the counters.
- No live host was contacted (per scope). I did not verify the captures against the live sites; the sha256 match is against the local snapshot only.
- The kres repository and the InternetCTF target were not opened (out of scope and live).
- Scratch: `/fast/scratch/hyaku/kasegi-r45/R45SentinelContent/` (scanner and controls) removed at the end of this seat.
