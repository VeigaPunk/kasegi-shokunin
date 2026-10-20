# AiRecheck — S010 exact evidence assertions (round 23)

- Seat: `KasegiR23.AiRecheck-5` (scout, read-only). Axes: depth:verifiability, coverage.
- Observed base: `922a4dde90b60b465e2b8b241d1fe363f1f27e98`.
- Source opened: https://projectzero.google/2024/06/project-naptime.html (S010 row, `corpus/SOURCES.md:16`).
- Retrieved 2026-10-20; `200 OK`; HTTP `Date: Tue, 20 Oct 2026 21:43:16 GMT`; `Content-Length: 198891`.
- No production edits; this report is the only file written. No tools installed.

## Chosen assertion (anchors the entry's currently unquoted clause)

Existing entry `corpus/knowledge/ai-assisted-finding-validation.md` has two S010 lines (22, 23).
Its rule rejects a model's plausible story in favour of reproducible evidence, and `SOURCES.md:16`
says "Prefer testable vulnerability hypotheses with automatic checks and iterative tools over
accepting a plausible narrative as proof." The word "plausible" appears **zero** times in the entry
Evidence and **exactly once** on the article page. The exact anchor is:

> "which can be susceptible to plausible but vague explanations of vulnerabilities."

- Words: **11** (chars 80, ASCII only). Occurs **exactly once** in normalized page text.
- Exact location: `<h1>` "CyberSecEval 2" → paragraph beginning "One of the standout features of
  this benchmark is its realistic setting", sentence 2, final relative clause. The antecedent is
  "methodologies relying on LLMs or human evaluators". Both sentences are one `<p>`.
- Companion quote in sentence 1 of the same paragraph (the positive side: a crash is the check):

> "clear outcomes: either a crash occurs, or it doesn’t"

- Words: **9**; occurs once. **Contains U+2019** (raw HTML `&rsquo;`), not ASCII `'`. The 12-word
  variant "success measured by clear outcomes: either a crash occurs, or it doesn’t" is also exact
  once, if a fuller sentence start is preferred.
- Why this pair: it is the only page text that both names the failure mode ("plausible but vague
  explanations") and states the automatic signal ("a crash occurs, or it doesn’t"). It supports the
  row's "plausible narrative" and "automatic checks" clauses at once.

## Existing S010 assertions rechecked — both exact, no defect found

| Entry line | Quote | Words | Count on page | Recorded location | Verdict |
|---|---|---|---|---|---|
| `ai-assisted-finding-validation.md:22` | "vulnerability discovery tasks can be structured so that potential solutions can be verified automatically with absolute certainty." | 17 | 1 | Proposed Principles → numbered item 4 `<h3>Perfect Verification</h3>` | exact; location correct |
| `ai-assisted-finding-validation.md:23` | "there's a large difference between solving isolated CTF-style challenges without ambiguity" | 11 | 1 | Conclusions, first prose paragraph | exact; location correct |

Notes:
- The full Perfect Verification sentence is 28 words, so it cannot be quoted whole under Q3. The
  entry quotes the 17-word predicate; the elided lead ("Unlike many reasoning-related tasks where
  verifying a solution can introduce ambiguities,") is supplied by the entry's gloss. That trade-off
  is sound, not a defect.
- Line 23's fragment ends before its comparison is completed; the entry's prose supplies
  "and autonomous security research". Optional self-contained strengthening (22 words, exact once,
  first prose paragraph of Conclusions): "closer to the typical usage of targeted, domain-specific
  fuzzing performed as part of a manual review workflow than a fully autonomous researcher". It is
  the article's own limit and needs no external gloss.
- `SOURCES.md:16` displays the date as `2024-06-20`; the page displays `2024-Jun-20` (same day,
  ISO-normalized). No immutability/R8 correction is needed for the existing anchor. If L1 widens
  the row's anchor to "CyberSecEval 2", R8 requires a new row beginning "supersedes S010 —", not an
  in-place edit.

## Date / version

- Displayed post date: **2024-Jun-20**, in the unique anchor
  `<a class="post-date" href="/2024/06/project-naptime.html" title="Permalink to this post">2024-Jun-20</a>`;
  byline "Sergei Glazunov and Mark Brand"; H1 "Project Naptime: Evaluating Offensive Security
  Capabilities of Large Language Models".
- No `datePublished`, `dateModified`, JSON-LD, or `article:*` metadata; response carries **no
  `Last-Modified` and no `ETag`**. The post-date anchor is the only date signal; there is no
  revision label. `SOURCES.md`'s "on-release" cadence therefore cannot be satisfied by a version
  string — a recheck must compare content.
- Raw HTML is **not byte-stable**: each response carries 5 CSP `nonce` values
  (`wplmtlT7CG2Cn5CHODDFzg` vs `8_SLjhSfKwnLKUhAQ0LB5Q` across two fetches), so
  sha256 HTML = `a6b3f8d60a9ccb71e8aabaad5f1f30bae3c5626c9f93511abe8408e4b4ccfddf` then
  `da2c79eb5091f255c1af2b82902ff896edd8ec5d52dd8bb89ac55d7e77c535e5` for identical article text.
- Stable version pin: normalized-text sha256
  **`cacae35aaaa8252fbf84b96adca4d9719220e4b33441ee0f53074a583c2786c3`** (36,417 chars), identical
  across both fetches. Do not pin this page by raw-HTML hash; that produces false drift.

## Recheck (executed locally, fail-closed)

Tested script (stdlib only); live mode fetches, file mode compares a captured source:

```python
#!/usr/bin/env python3
import html, re, sys, urllib.request, hashlib
URL = "https://projectzero.google/2024/06/project-naptime.html"
Q_PV  = ("vulnerability discovery tasks can be structured so that potential "
         "solutions can be verified automatically with absolute certainty.")
Q_CSE = "which can be susceptible to plausible but vague explanations of vulnerabilities."
DATE  = "2024-Jun-20"
raw = (open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1
       else urllib.request.urlopen(URL, timeout=30).read().decode("utf-8", "replace"))
b = re.sub(r"(?is)<(script|style).*?</\1>", "", raw)
b = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h[1-6]>|</li>|</tr>", "\n", b)
t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", b))).strip()
m = re.search(r'class="post-date"[^>]*>([^<]+)</a>', raw)
print(f"S010 pv={t.count(Q_PV)} plausible={t.count(Q_CSE)} date={m and m.group(1).strip()} sha={hashlib.sha256(t.encode()).hexdigest()}")
sys.exit(0 if t.count(Q_PV) == 1 and t.count(Q_CSE) == 1 and m and m.group(1).strip() == DATE else 1)
```

Observed runs:

| Input | Exit | Output |
|---|---|---|
| live URL (fresh network) | 0 | `pv=1 plausible=1 date=2024-Jun-20` sha `cacae35a…` |
| pinned `S010.html` | 0 | same counts, same sha |
| wrong source: `vulnerability-disclosure-faq.html` | 1 | `pv=0 plausible=0 date=None` |
| corrupted quote (`plausible but vague` → `vague`) | 1 | `plausible=0` |
| corrupted date (`2024-Jun-21`) | 1 | `date=False` |
| missing file | 1 | `FileNotFoundError` |

Exactness caveat discovered while building this: the served HTML splits both quotes across inline
`<span>` elements (`…can be </span><span>verified automatically…`) and writes `doesn’t` as
`&rsquo;`, so a raw `curl | grep -F` of either full sentence returns 0 matches while the normalized
text returns 1. Normalize tags + entities before comparing, or the check is falsely red.

## Proposed entry patch (exact text, NOT applied)

Insert after current line 23:

- S010, “CyberSecEval 2”, paragraph beginning “One of the standout features of this benchmark is
  its realistic setting”, on methodologies relying on LLMs or human evaluators: “which can be
  susceptible to plausible but vague explanations of vulnerabilities.” Its benchmark instead
  measures “clear outcomes: either a crash occurs, or it doesn’t.”

Optional replacement for line 23 (keeps the same claim, self-contained; existing quote is not
wrong and need not be removed for correctness):

- S010, “Conclusions”, first paragraph: “closer to the typical usage of targeted, domain-specific
  fuzzing performed as part of a manual review workflow than a fully autonomous researcher.” The
  article limits its benchmark conclusions.

Coupling: entry line 4's `recheck:` is prose and names only “Perfect Verification” and “Conclusions”.
Adding the CyberSecEval 2 assertion without making that field executable (Q7) and naming the new
paragraph leaves the new assertion outside the declared recheck scope. The script above is the
tested candidate for that field; placing it under `corpus/instruments/` is L1's call.

## Falsifiable findings

1. If the 11-word “plausible” fragment stops occurring exactly once, the row's "plausible narrative"
   clause loses its only exact anchor and must be re-sourced or withdrawn — not silently reworded.
2. A patch quoting ASCII `doesn't` is not verbatim: the served byte sequence is `doesn&rsquo;t`
   (U+2019). Falsifier: character compare against the raw HTML.
3. S010 cannot support the entry's "human validation" clause: its only "human evaluators" mention
   is a weaker comparison baseline, and the article prefers automatic verification for structured
   tasks. That clause rests on S009/S011/S012, not S010. Falsifier: all 11 "human" contexts.
4. A raw-HTML sha256 pin of this page is unstable (per-request CSP nonce); a byte-level recheck will
   report false drift. Falsifier: two consecutive fetches, differing sha256, identical text sha256.
5. "Absolute certainty" cannot be generalized beyond structured tasks: the Conclusions say solving
   such challenges is closer to targeted fuzzing inside a manual review than to a fully autonomous
   researcher. Falsifier: the 22-word Conclusions quote above.
6. Raw-string location checks fail even when the text is right: the heading is split
   `CyberSecEval</span><span>&nbsp;2` (U+00A0) and `Perfect Verification` sits in an `<h3>` inside a
   numbered `<li>`. Falsifier: `'CyberSecEval 2</h1>' in raw` → False; normalized heading → True.

## Scope limits

- Read-only public documentation; no production edits, no snapshot created, no security probing.
- Verified only the quoted sentences, their paragraph locations, the displayed date, and the
  response/version behavior. Benchmark scores, architecture claims, and the article's internal
  citations were not audited.
- Extraction is my own documented tag-strip + entity-unescape + whitespace-collapse recipe; other
  renderers may normalize `&nbsp;`/`&rsquo;` differently, which is why the recipe and text hash are
  recorded above.
- Only the official URL was used; no archive or mirror. This report supplies evidence for L1's
  admission decision; it does not claim admission.
