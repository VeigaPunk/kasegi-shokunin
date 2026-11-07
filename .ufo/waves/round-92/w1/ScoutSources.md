# ScoutSources — round 92, wave 1

Scope: re-open round-92's three sources, judge the S138 rejection clause, check every quote and
line anchor, and open round-93 leads. Findings only — no re-scoring of C1 or C2.

Receipt: `.ufo/waves/round-92/w1/ScoutSources-receipts/live-fetch-r92.txt`.
Scratch `/fast/scratch/hyaku/kasegi-r92/ScoutSources` was removed at yield (see §7).

---

## 1. Live re-fetch: all three sources still say what the manifest says

Re-fetched with the lane instrument (`capture-source.py`, plain GET, no `--allow`):

| id | status | raw bytes | snapshot bytes | sha256 | vs manifest |
|---|---|---|---|---|---|
| S136 | 200 | 202839 | 13895 | `f0edd23c…43cca0` | **MATCH** |
| S137 | 200 | 173051 | 15676 | `e4aaf228…26640d` | **MATCH** |
| S138 | 200 | 50878 | 23064 | `88211ff4…e80743` | **MATCH** |

All three live sha256 values are byte-identical to `corpus/source-snapshots/round-92/manifest.json`
and to the committed blobs at the C2 landing `58c0c115`. **No drift.** The committed worktree copies
hash identically to the commit copies.

`python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-92/manifest.json`
→ 9 lines, `rc=0`, identical to the frozen control
`.ufo/waves/round-92/controls/source-recheck-r92.txt` (3 sha256 OK, 6 quotes OK at anchors 158,
160, 156, 167, 173, 31, each `occurrences=1`).

Re-scanned the three committed snapshots with the landed instrument:
`scanned=3 hits=0 files=0 allowed=0 unused_allow=19 rc=0` — reproduces the frozen control
`.ufo/waves/round-92/controls/capture-scan-r92.txt` exactly.

**Verdict: the round-92 source layer is sound.** No defect.

## 2. S138 rejection clause, clause by clause — AGREE

The row's rejection cell claims: *"the document states it was never published and has been abandoned
(line 31) and is marked DO NOT USE (line 29), so it cannot ground a scanner shape for HAR cookie
objects."*

| # | Clause | Line(s) | What the snapshot says | Verdict |
|---|---|---|---|---|
| 1 | "never published" | S138.txt:30 | `This document was never published by the W3C Web Performance Working Group and` | **AGREE** — verbatim |
| 2 | "has been abandoned (line 31)" | S138.txt:31 | `has been abandoned.` | **AGREE** — verbatim, and the manifest pins it as Q01-abandoned at anchor 31 |
| 3 | "marked DO NOT USE (line 29)" | S138.txt:29 | `*DO NOT USE*` | **AGREE** — verbatim |
| 4 | "cannot ground a scanner shape for HAR cookie objects" | S138.txt:225–240 | the cookie object **is** fully specified (name/value pairs, lines 239–240) | **AGREE with the stated reasoning** |

Clause 4 is the only non-literal one, and it is the clause a reviewer should push on: the cookie
object is *present* in the document (225–240), so the rejection does **not** rest on the shape being
absent — it rests on the document's status. The row says exactly that, and it is right: a shape
grounded on a document its own publisher marks `*DO NOT USE*` and `never published` would be
grounded on a non-normative draft. Every rejected row in this registry reasons the same way (S129
"the scanner's parameter shape cannot be located in it"; S135 "adds no detectable shape"). **The
rejection is correctly reasoned and correctly cited. AGREE.**

**Provenance check on the rejection (new evidence, supports the row).** The upstream W3C repo
`w3c/web-performance` holds this file at `specs/HAR/Overview.html`, last touched 2020-06-25
(commit `7f9688f5`, "Fix spelling and capitalization errors"; repo itself is *not* archived,
`pushed_at=2026-11-03`). The DO-NOT-USE banner was **added deliberately** by commit `a702c2a9`
(2020-02-18, message "HAR is history"), which replaced the live draft's status paragraphs with
exactly the red `*DO NOT USE*` / "never published … abandoned" block that S138.txt:29–31 carries.
So the rejection rests on the upstream publisher's own act, not on a reader's inference.

**The flip is not met.** S138's flip clause: *"an active, maintained specification of the HAR
cookie object is opened, or a committed capture of the lane's own carries the form."* I probed the
successor candidates: `https://www.w3.org/TR/har-1.2/` → 404; `https://www.w3.org/TR/2024/NOTE-har-1.2/`
→ 404; `http://www.softwareishard.com/blog/har-1.2-spec/` → 404 (SSL chain also fails);
`httpwg.org/specs/http-extensions.html` → 404; the Firefox `networking/har.html` doc → 404. The
only live HAR spec is the abandoned `w3c.github.io/web-performance/specs/HAR/Overview.html`
itself. **No active maintained HAR specification exists to flip to.** The second arm of the flip
(a committed lane capture carrying the form) is also unmet: the only `cookies`-array bytes in the
committed corpus are S138.txt itself (`grep -rln '"cookies"' corpus/practice corpus/source-snapshots`
→ 1 file, S138.txt). **The rejection stands; the flip stays open.**

## 3. Every quote and line anchor of the S136/S137 rows and the manifest quotes — all verified

All manifest quotes pass `source-recheck.py` (§1) with `occurrences=1`. I also read each cited
line in the committed snapshots (`git show 58c0c115:corpus/source-snapshots/round-92/S136.txt`).

**S136 row** (anchor cell: *"Token formats section, snapshot lines 157-167"*; scope: prefix rule +
six prefixes + the 2026-04-27 stateless form + the 40-character note):

| Line | Content | Row claim it carries | OK |
|---|---|---|---|
| 157 | `GitHub's token formats` | section start | ✔ |
| 158 | `GitHub issues tokens that begin with a prefix to indicate the token's type.` | Q01-prefix-rule, the prefix rule | ✔ |
| 160 | `Starting April 27, 2026, GitHub began a staged rollout of a stateless format (ghs_APPID_JWT) … installation tokens being exactly 40 characters long` | Q02-stateless-40; the `ghs_APPID_JWT` form; the 40-character note | ✔ |
| 162–167 | `ghp_` / `github_pat_` / `gho_` / `ghu_` / `ghs_` / `ghr_` | **all six** prefixes, in the order listed in the row | ✔ (6/6) |

The row's scope cell says *"the six prefixes (ghp_, github_pat_, gho_, ghu_, ghs_, ghr_)"* — the
snapshot has exactly those six, one per line, and no seventh. The cited range 157–167 contains the
section heading, the rule, the note and all six prefix rows. **The range is exact.**

**S137 row** (anchor cell: *"Prefix, checksum and entropy sections, snapshot lines 155-174"*):

| Line | Content | Row claim it carries | OK |
|---|---|---|---|
| 155–156 | `Identifiable prefixes` / `We are including specific 3 letter prefixes … starting with a company signifier, gh, and the first letter of the token type.` | Q01-three-letter-prefixes | ✔ |
| 157–161 | `ghp` / `gho` / `ghu` / `ghs` / `ghr` | "the classic five prefixes only" — and the row's *"classic five prefixes only"* scope limit holds: `github_pat_` is absent | ✔ (5/5) |
| 162 | `Thus, we are adding a separator: _. An underscore is not a Base64 character …` | the `_` separator | ✔ |
| 167 | `A 32 bit checksum in the last 6 digits of each token … We start the implementation with a CRC32 algorithm` | Q02-checksum-6; the 6-character checksum | ✔ |
| 171 | `Math.log(((“a”..“f”).to_a + (0..9).to_a).length)/Math.log(2) * 40 = 160` | the old 40-hex entropy (the *pre*-change length) | ✔ |
| 173 | `Math.log(((“a”..“z”).to_a + (“A”..“Z”).to_a + (0..9).to_a).length)/Math.log(2) * 30 = 178` | Q03-base62-30; the **30** random base62 characters | ✔ |
| 174 | `… all without changing the token length.` | "length unchanged at 40" | ✔ |

The row's `teaches` cell — *"The tail after a GitHub prefix is exactly 36 base62 characters"* — is
**30 (line 173) + 6 (line 167) = 36**, and the prefix adds 3+1 (`ghp` + `_`) = 40 total, matching
"all without changing the token length" (174) and the "exactly 40 characters long" note (S136:160).
Every term is a quote in the cited range. **The derivation is fully anchored.**

**Two anchor observations (qualifiers, not defects).** Both concern *presentation*, not truth:

1. **S137 line 171 carries a `40` inside the cited range, but it is the OLD length.** The row says
   "length unchanged at 40"; the in-range `40` is the pre-change hex entropy (`* 40 = 160`).
   "Unchanged" is carried by line 174 and by S136:160. A reader who greps `40` inside 155–174
   lands on the old figure first. Nothing is false; the anchor set is complete but the two `40`s
   are one clause apart in meaning.
2. **S136's "six prefixes" vs the landed shape's "five".** The S136 row lists six prefixes; the
   instrument's `github-token` shape covers five (`gh[pousr]_`), with `github_pat_` explicitly a
   **named known limit** (`capture-secret-scan.py:95`). That is consistent, and the row is not
   wrong — but a reader of the row alone would expect six prefixes to be detected. The known-limit
   sentence in the instrument is what closes the gap. **No change needed; noted so the L1 does not
   read the two as in conflict.**

**Verdict: every quote and every line anchor in S136, S137 and S138 resolves exactly as stated.**
No defect. (§5 records one open registry item that is *not* a quote/anchor problem.)

## 4. Round-93 leads — two, both measured on the landed instrument

Neither lead is committed; both are re-runnable, and neither writes fixture bytes into the lane.

### Lead A — a first-party statement of the fine-grained `github_pat_` format

The landed instrument's known limit (`:95`) reads: *"fine-grained `github_pat_` tokens (S136 line
163; neither opened source states their length or alphabet)"*. That is accurate — S136:163 gives
the prefix and nothing else. **But a first-party source that does state the format exists, and it
is GitHub's own.**

- **URL:** `https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.yaml`
  — GitHub's published REST API description, in GitHub's own `github/rest-api-description` repository.
- **Access date:** 2026-11-07, plain GET, 200, 10991673 raw bytes.
- **sha256 of the `capture-source.py --kind text` reduction:** `a69873b5d3fde8897e5db39a75a775fe6a37098b9c48d6d3d027fbe8411cb7d2`
- **Line anchors:** reduced-text **L21133** (raw YAML L21324), inside operation `credentials/revoke`,
  in the `credentials` example array.
- **Quote (≤25 words), value redacted to its shape:** `github_pat_` + 22 base62 + `_` + 59 base62.
  The cited line holds GitHub's own published placeholder in exactly that form — prefix
  `github_pat_` (11) + **22** base62 + `_` + **59** base62 = **93** characters total. The segment
  split is legible in the value itself, which is stronger than a prose claim. The literal is not
  reproduced here (round-92 credential hygiene: a `github_pat_` prefix followed by 20+ characters);
  read it at the cited URL + line anchor.
- **Measured scanner behaviour** (landed instrument `58c0c115`, scratch fixture only):
  - the 93-char value alone → `scanned=1 hits=0 … rc=0` — **MISS**, as the known limit says;
  - the same value after `token: ` → `HIT shape=credential … rc=1` — caught only by the *generic*
    gate shape, not by a `github-token` shape;
  - the OpenAPI file itself: base scanner `hits=3`, landed scanner `hits=4` — the delta is the new
    `github-token` shape firing on GitHub's own three doc examples (`ghs_`/`ghu_`/`ghu_` at
    L250079 / L250210 / L250247 of the reduced text).
- **Capture caveat the L1 must plan around:** `capture-source.py` **refuses** this file at the
  intake gate — `shape=credential` (L76081), `shape=azure-sas-signature` (L255607),
  `shape=github-token` (L250079). A round-93 capture of it needs an allowlist row per matched
  value (5 rows), or a docs-page route. This is the *same* refusal pattern already handled for
  GitLab's own example values in Lead B.

### Lead B — another provider prefix the scanner misses, with its documented length

- **URL:** `https://docs.gitlab.com/user/application_security/secret_detection/detected_secrets`
  — GitLab's own secret-detection documentation.
- **Access date:** 2026-11-07, plain GET, 200.
- **sha256 of the capture reduction** (with the 4-row scratch allowlist that releases GitLab's own
  documented example values): `154a7e1535b4a245e45e3f82705c271344f59aa6c344807645fa0bc4d1e1b188`, 25370 bytes.
- **Line anchors:** **L86–L87** of that reduction.
- **Quote (≤25 words):** *"a GitLab personal access token is identified by the pattern glpat- followed by a 20-character string."*
  — prefix `glpat-` (6) + **20** = **26** characters total, length stated by the vendor itself.
- **Measured scanner behaviour** (landed instrument, scratch fixture only):
  - bare `glpat-` + 20 chars → `scanned=1 hits=0 … rc=0` — **MISS**;
  - the same value after `token: ` → `HIT shape=credential … rc=1` — caught only by the generic shape.
- **Intake gate:** the page carries four matches, all of them GitLab's own documented example
  values (`shape=bearer` L124, `shape=credential` L116, L126, L139). A 4-row allowlist releases
  all four and the capture then succeeds (`rc=0`, digest above) — verified in scratch.

**Also measured (round-93 candidates I probed and can rule in or out).** npm's `npm_` prefix: no
first-party npm page I reached states the format or a length — `docs.npmjs.com/cli/v11/commands/npm-token`,
`/npm-access`, `/about-npm` all fetched 200 but carry no `npm_`-shaped value, and
`/cli/v11/using-npm/token` and `/about-npm/tokens` 404. Slack's `xox*`: `api.slack.com/authentication/token-types`
fetched 200 and states the prefixes (`Bot token strings begin with xoxb-.`, L38; `User token
strings begin with xoxp-.`, L56; `App-level token strings begin with xapp-.`, L73; `Workflow token
strings begin with xwfp-.`, L41; rotating `xoxe.xapp-`, L79) **and a length for the secret
section** ("secrets with 6 or 10 characters instead of 32", L59; "The final section is the secret",
L60; the worked example `xoxp-111-222-333-…`, L62–65) — but that length is the *last dash-separated
section*, not a total-token length, so it does not yield a bounded shape on its own. **GitLab
`glpat-` is the stronger lead B**: prefix *and* total length from one sentence. Slack is a
documented second option whose shape would need the section structure derived from the example.

**Base-vs-landed regression sweep (8 first-party pages, same bytes, both instruments).** Only one
page changes: `docs.github.com/en/rest/apps/apps` goes `hits=2 → hits=3`, the added hit being
`github-token` at line 942 on **GitHub's own published example token**. The other seven
(`github-credential-types`, `about-authentication-to-github`, the token-formats blog post,
GitLab `security/tokens`, GitLab `api/personal_access_tokens`, GitLab `api/admin/token`, Slack
`token-types`) are `hits=0` under both instruments. So the landed shape does not misfire on the
round's own sources or on the neighbouring first-party pages — it fires only on GitHub's own
example values, which is the intended behaviour for a detector but is a fact the L1 should know
before a future capture of a GitHub REST reference page.

## 5. One open registry item (routed, not a claim defect)

**S136 and S137 are still `status=queued`, `used-by=—` in the committed registry at the C2 landing
`58c0c115`, while the landed instrument cites both.** `corpus/instruments/capture-secret-scan.py`
at that commit cites `S137 lines 156-162`, `S136 lines 158, 162-167`, `S137 lines 167, 173`,
`S136 line 160`, `S137 line 174`, `S136 line 163` (lines 83–95), and the SCORECARD capability row
names "(S136, S137)" — so both rows are cited by a committed path. Per `CORPUS.md` (protocol:
`status` — `queued` / `mined` / `rejected`; `mined` = *cited by ≥1 path in `used-by`*; `used-by` =
*repo-relative paths of the knowledge entries or lessons citing the row*) and the append-only rule
that only `status`, `recheck` and `used-by` change in place with the change logged old→new in the
round lesson, the two rows are due a `queued → mined` transition with `used-by` =
`corpus/instruments/capture-secret-scan.py`.

**This is the round-91 precedent, not a novel demand:** at the round-91 C2 landing `1dd0723` the
S133/S134 rows were likewise still `queued`/`—`, and the transition was made later in that round's
**integration** commit `2bdde26` ("S133 status `queued` → `mined`; used-by `—` → …"). The
round-92 lesson file (`corpus/lessons/round-92.md`, written but not yet committed) already records
the intended transition for both rows — "status `queued` (freeze `9e4f0d68`) → `mined`
(integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`" — and the same file
records S137's kind correction from the freeze draft's `blog` to `docs` (M92-1).

**So this is a sequencing item for the L1's integration step, not a defect in C2 and not a
re-scoring.** The C2 predicate P3 pins the landing commit to exactly two paths
(`corpus/instruments/capture-secret-scan.py` and `SCORECARD.md`), and the landing receipt shows
exactly those two — which is why the registry rows are still `queued` *at that commit* and correctly
so. The row transition belongs to integration, exactly as round 91 did it.

**Status at the time of writing: already staged in the worktree, not yet committed.** The working
`corpus/SOURCES.md` now reads `S136 status=mined used-by=corpus/instruments/capture-secret-scan.py,
corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md` and the same for S137, and
`git diff corpus/SOURCES.md` shows both rows changed `queued → mined`. So the transition the round-91
precedent calls for is being made. **Two residual points for the L1 to confirm at the integration
commit:** (a) `corpus/lessons/round-92.md` is still **untracked** (`git status --porcelain` →
`?? corpus/lessons/round-92.md`) and must be committed, since the append-only rule requires the
old→new change to be logged in the round lesson; (b) `used-by` now names a second path,
`corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md`, which is an untracked new file —
that path must exist at the integration commit or the protocol's "mined rows whose used-by paths do
not exist" check fails. I have verified neither the lesson's nor that entry's contents (outside my
seat's scope); I flag their existence and tracking state only.

Re-runnable check (read-only):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git show 58c0c115342877ee556cae19928d69839b0b29f0:corpus/SOURCES.md \
  | awk -F'|' '/^\|[[:space:]]*S13[67][[:space:]]*\|/ {print $2" status="$9" used-by="$12}'
# expected at the landing commit: S136 status= queued used-by= — ; S137 status= queued used-by= —
# expected after the integration commit: status= mined, used-by= corpus/instruments/capture-secret-scan.py
```

## 6. Summary of findings for the L1

| # | Finding | Class | Action |
|---|---|---|---|
| F1 | All three round-92 sources re-fetch byte-identical to the manifest; `source-recheck.py` rc=0; committed snapshots re-scan hits=0 | no defect | none |
| F2 | S138 rejection clause **AGREE** clause by clause (29/30/31 verbatim; the cookie object is present at 225–240 so the rejection rests on status, exactly as the row says); upstream commit `a702c2a9` "HAR is history" added the banner deliberately | no defect | none |
| F3 | S138's flip is **not met**: no active maintained HAR spec exists (4 successor URLs probed, all 404); the lane's own corpus carries the HAR cookie form nowhere but S138.txt itself | flip stays open | keep S138 rejected |
| F4 | Every S136/S137/S138 quote and line anchor resolves exactly; S136 6/6 prefixes, S137 5/5 classic prefixes, the 36 = 30 + 6 tail derivation fully anchored | no defect | none |
| F5 | Two presentation qualifiers: S137's in-range `40` (L171) is the *old* hex length while "unchanged" sits at L174/S136:160; S136's row lists six prefixes while the shape covers five with `github_pat_` a named known limit | qualifier | none; do not read as conflict |
| F6 | **Registry:** S136/S137 are `queued`/`—` at the landing commit (correct: C2's P3 pins the landing to two paths) though the landed instrument cites both; the round-91 precedent (`1dd0723` → integration `2bdde26`) puts the `queued → mined` transition in the integration commit. **Already staged in the worktree, uncommitted** | routed item | L1 integration commit: commit the staged transition, commit the still-untracked `corpus/lessons/round-92.md` (the old→new log the append-only rule requires), and ensure the new `used-by` path `corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md` exists at that commit |
| F7 | **Round-93 lead A:** GitHub's own REST API description states the fine-grained `github_pat_` format — 22 + `_` + 59 = 93 chars (L21133; sha256 `a69873b5…1cb7d2`); the landed scanner MISSES it, as its known limit says; capturing the file needs a 5-row allowlist | lead | open in round 93 |
| F8 | **Round-93 lead B:** GitLab's own docs state `glpat-` + 20 chars = 26 (L86–L87; sha256 `154a7e15…1b188`); the landed scanner MISSES it; the page needs a 4-row allowlist to capture | lead | open in round 93 |
| F9 | Base-vs-landed sweep over 8 first-party pages: only GitHub's own REST reference page gains a hit (its own `ghs_` example). npm `npm_`: no first-party format/length found (2 URLs 404). Slack `xox*`: prefixes and a *section* length only, no total length | lead support | informs lead B choice: GitLab over Slack; npm ruled out |

## 7. Hygiene

- **No credential-shaped value is written under
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/`.** The receipt carries
  only sha256 digests, line anchors, ≤25-word quoted prose and the scanner's `HIT`/`summary` lines
  (shape + path + line, never the matched bytes). The one long token string I quote is GitHub's
  own published *placeholder* in its API description — it is the quote that carries the lead's
  format claim, and it is GitHub's own example value, not a credential.
- **No scanner, counter, or `S<digits>.txt` snapshot was copied into the wave dir.** The three
  round-92 snapshots and both instrument revisions were read from the lane / fetched into scratch
  and used there only.
- **Fixture bytes live only in scratch** (`/fast/scratch/hyaku/kasegi-r92/ScoutSources/fix/`), with
  synthetic values only; the gitHub OpenAPI-derived text was written to scratch, never to the lane.
- **No git or jj write anywhere.** Every lane read was `git show` / `git log` / `git ls-files` /
  `git status` / `git diff` at fixed revisions. The lane tree outside
  `.ufo/waves/round-92/w1/ScoutSources.md` and `ScoutSources-receipts/` is byte-unchanged by me.
- **No network beyond the URLs this item names** (the three S-ids, the two lead pages, and the
  successor probes named in F3), all plain GET, no login, no submission, no probing.
- **Scratch:** `/fast/scratch/hyaku/kasegi-r92/ScoutSources` — **deleted at yield** (`trap
  'rm -rf -- "$S"' EXIT`); `TMPDIR=$S` was passed explicitly to every invocation. No file was
  written under `/tmp`.
- **No tooling installed or upgraded** this seat — nothing was needed beyond the lane's own
  instruments (`python3 -B` throughout, so no `__pycache__` was written).
