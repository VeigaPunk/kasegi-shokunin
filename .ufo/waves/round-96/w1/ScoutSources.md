# ScoutSources — round-96 w1 source reconnaissance

Seat: `ScoutSources` (leaf; no subagents dispatched).
Lane: `kasegi`. Wave: round-96 w1, attempt 1.
Scope: read-only source reconnaissance for the round's Gate. I did not edit any
lane file; the L1 writes the rows. Git/jj state was read only (`git log`,
`git show`, `git rev-parse`, `git cat-file`, `git archive`); no mutating git or jj
command was run anywhere. Scratch: `/fast/scratch/hyaku/kasegi-r96/ScoutSources`
(removed by the seat's EXIT trap).

## Verdict

**Both frozen claims STAND as re-derived by me.** C1 and C2 each pass their own
frozen counter at their own landing revision, and I re-ran both counters myself
rather than trusting the committed receipt:

- **C1** — `knowledge-meter.py` at the C1 landing `3c0581e`: `KNOWLEDGE-METER-RESULT
  pass rc=0`, M0 base=1030/2027, M1 after=1032/2028, M3 `same_files=True
  bad_lines=0 old_not_once=0 dup_rows=0`, **M4 `bad=none`** (the new prose-pointer
  `part` binding), M5 `out_of_range=none`, M9 `rows=5 unbound=none`, M10
  `labelled=5 want=5 mapped=5 kinds (part 4, range 1) unknown=none`, M6 the frozen
  map sha. The control harness re-run gives `C1-CONTROLS-RESULT pass controls=12`
  and `ATTRIBUTION pass fixtures=11`. C1's remaining limbs also hold: **P3** —
  the C1 landing's changed paths are exactly `corpus/knowledge/triage-thresholds.md`
  and `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`; **P4** — the
  do-nothing control is rc 1 with limbs M1,M3 and the round-95 counter with only
  LABELS_PATH repointed is rc 1 with limbs M4,M5. My re-run's output is identical to
  the frozen committed receipt `.ufo/waves/round-96/controls/c1-controls-r96.txt`.
- **C2** — `capability-check.py` at the C2 landing `7ef1d36`: `CAPABILITY-CHECK-RESULT
  pass rc=0` with K1 `selftest=pass cases=128` (and the instrument sha256 equal to
  the frozen pin), K2 `rc=0 scanned=2744 hits=0 allowed=27 unused_allow=0`, K3
  `hits=7 missing=none extra=none`, K4 `base_new_shape_hits=0 old_shapes_missing=none`,
  K5 `rows=1 last=87 named=True`, K6 `shapes=aws-access-key-id,aws-sts-session-token,credential`.

Two things do **not** change a verdict but are routed onward:

1. **R96-SS-1 (routed defect, C2 landed artifact):** the landed
   `capture-secret-scan.py` docstring's *Known limits* list dropped the `glagent-`
   prefix, but the shape it dropped is not the shape the round added. S140 publishes
   **two** `glagent-` rules (L213 = the plain 50-character kubernetes-agent token,
   L358 = the routable/versioned-routable form). The round detected only L358; the
   L213 form is still undetected and has now **lost its known-limit entry**, so the
   docstring claims coverage the instrument does not have. C2's frozen predicate
   (K1–K6) asserts nothing about the known-limits list, so this is a routed defect,
   not a verdict change. Detail and a suggested clause: `R5-routed-defect-glagent.txt`.
2. **A citation-convention fact, not a defect:** every "S140 line N" citation in the
   lane resolves against the **committed capture**
   `corpus/source-snapshots/round-94/S140.txt` (563 lines), **not** against the
   upstream file at commit `59ada1f4` (592 lines). The upstream file carries the
   same seven regexes at lines **31 / 53 / 76 / 142 / 340 / 376 / 394**. The
   offset is the 29 blank lines that `capture-source.py`'s `collapse()` drops; I
   reproduced the capture byte-for-byte from the live raw to prove it. This is
   pre-existing lane behaviour, not a round-96 regression: the round-94 manifest's
   own three anchors (4 / 114 / 255) already sat at upstream lines 4 / 119 / 267.
   Detail: `R1-line-drift-proof.txt`.

Neither item re-scores either claim under its frozen predicate.

---

## Job 1 — re-open S140's live source and confirm the seven rules

**Live source re-opened.** The commit-pinned raw URL from the round-94 manifest:

```
https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab.toml/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39
```

- HTTP status **200**, **20228 bytes**, `sha256 14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5`
  — **identical** to the digest the round-94 manifest records for the raw fetch
  ("raw 20228 bytes, sha256 14854f71…"). The upstream file has not drifted.
- Access date: **2026-11-07** (fetched 2026-11-07T18:2x–18:3x UTC).

**All seven rules confirmed at the claimed lines of the committed capture.** Each
line below is quoted verbatim from `corpus/source-snapshots/round-94/S140.txt`. No
example value is reproduced: the capture's example arrays are already structurally
redacted, and the regex lines themselves contain no credential material.

| claim | capture line | rule id (capture) | regex line, quoted |
|---|---|---|---|
| routable PAT | **30** | `gitlab_personal_access_token_routable` (L28) | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}[0-9a-z]{7})\b'''` |
| versioned-routable PAT | **51** | `gitlab_personal_access_token_routable_versioned` (L49) | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b'''` |
| pipeline trigger | **73** | `gitlab_pipeline_trigger_token` (L71) | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glptt-(?:[0-9a-zA-Z_\-]{20}\|[0-9a-zA-Z_\-]{40}))(?:[^0-9a-zA-Z_\-]\|$)'''` |
| runner auth | **136** | `gitlab_runner_auth_token_routable` (L134) | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glrtr?-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b'''` |
| deploy token | **324** | `gitlab_deploy_token_routable` (L322) | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?gldt-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b'''` |
| kubernetes agent | **358** | `gitlab_kubernetes_agent_token_routable` (L356) | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b'''` |
| workspace token | **375** | `gitlab_workspace_token` (L373) | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glwt-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b'''` |

The seven lines match the claim's line list (30, 51, 73, 136, 324, 358, 375) exactly,
and each is the rule the round's matcher implements. `glptt-` is indeed
`(?:…{20}|…{40})` — exactly 20 or exactly 40 — as the claim states.

**Line-number drift, measured.** The same seven regexes sit at upstream lines
**31 / 53 / 76 / 142 / 340 / 376 / 394** (offset +1, +2, +3, +6, +16, +18, +19).
Cause, re-derived rather than assumed: the live file has **29 blank lines** and the
capture has **0**; `capture-source.py`'s `collapse()` skips every blank line
(`if line: lines.append(line)`). I reproduced the capture from the live raw:

- re-applying `collapse()` to the live raw gives **20035 bytes**, `sha256
  04fc5cfa200c92f54e14a7d104bb56e479aeccf45746234f0965c3c8e637d921` — **exactly**
  the "collapsed snapshot 20035 bytes" digest the round-94 manifest records;
- re-applying the 82-element redaction on top gives **563 lines**, **0 mismatched
  lines** against the committed capture, **byte-identical: True**.

So the capture is exactly reproducible from the live source, and every offset equals
the number of blank lines dropped before that point. The lane's own round-94
manifest anchors (4 / 114 / 255) resolve to upstream 4 / 119 / 267 by the same
arithmetic — so this is the lane's long-standing convention (cite the capture),
and the round-96 citations (capture lines 30/51/73/136/324/358/375) are correct
**under that convention**. A reader who goes to the upstream blob expecting line 30
to be the routable PAT will land on the keywords line; the new knowledge file
`corpus/knowledge/gitlab-routable-and-versioned-token-forms.md` already names the
capture path explicitly, which is the right guard.

## Job 2 — candidate new source stating GitLab's token prefixes with their lengths

**Finding: there is no admissible new candidate for this scope.** I opened **22**
GitLab pages (full URL/HTTP list in `R2-candidate-prefix-length.txt`) and searched
each for a page that states a prefix **together with** a length.

The page the seat names — the GitLab docs token-overview page
`https://docs.gitlab.com/security/tokens/` — **states prefixes and no lengths**:

- HTTP **200**, final URL `https://docs.gitlab.com/security/tokens/`, 67805 bytes raw HTML.
- Access date **2026-11-07**.
- Exact section heading: **"Token prefixes"**.
- Located quote (≤25 words), the table's lead-in sentence:
  > "The following table shows the prefixes for each type of token."
  > "With the exception of Personal Access tokens, these prefixes cannot be configured,"
  > "as they are designed to be standard identifications."
- It carries the whole prefix set: `glpat-`, `gloas-`, `gldt-`, `glrt-`/`glrtr-`,
  `glcbt-`, `glptt-`, `glft-`, `glimt-`, `glagent-`, `glwt-`, `_gitlab_session=`,
  `glsoat-`, `glffct-`.
- **No length anywhere.** Searches over the converted text for
  `NN character`, `character`, `token length`, `NN-character` all return **0 hits**;
  the only `length` occurrence in the raw HTML is inside a minified `<script>`
  bundle. The page's two table headers are literally `Token name` and `Prefix` —
  there is no length column.

**Tier: A** for the scope *"GitLab token prefix and length"* **as far as the prefix
half goes** — it is GitLab's own first-party documentation stating its own token
prefix set. It is **tier A but scope-incomplete**: it carries no length, so it
cannot alone ground a length.

**But this page is already held.** It was admitted this same round as **S144**
(`corpus/SOURCES.md:156`; capture `corpus/source-snapshots/round-96/S144.txt`,
419 lines, `sha256 d6e529275deb3ecf4ea2c3edaff2caa882760680cf23c1a134424e6acffdb83d`,
fetched 2026-11-07T18:20:55Z, quotes Q01 anchor 346 / Q02 anchor 348). I re-fetched
the URL and confirmed it still serves 200 and the same content. The S144 row's own
`teaches` cell already records the decisive fact for this scope: *"the page states
prefixes, never lengths or tails."*

**What the search actually establishes.** Across the 22 pages, GitLab's prose
publishes:

- the **prefix set** (token-overview page — S144; also
  `docs.gitlab.com/development/authentication/`, a 3-row prefix table with a
  "Storage" column, and `docs.gitlab.com/runner/register/`, which states
  "Runner authentication tokens have the prefix, `glrt-`.");
- a **length** only for the **personal access token** — 20 characters —
  (`docs.gitlab.com/user/profile/personal_access_tokens/`: "The token must be 20
  characters long."; and the detected-secrets page already held as S139:
  "`glpat-` followed by a 20-character string").

**No GitLab prose page states a length for `glrt-`, `gldt-`, `glagent-`, `glwt-` or
`glptt-`.** Every one of those lengths exists only in GitLab's own rules file
(S140, code, tier A). That is exactly why the round's new knowledge file cites S140
for the lengths and tails and S144 only for the prefix set. So for the scope
"GitLab token prefix and length", the lane is already covered by S139 + S144 +
S140, and a further prose candidate would have to state a length for a **non-PAT**
family — none exists among the 22 pages opened.

**Conclusion for job 2: no new candidate to propose.** The honest result is the
negative one; proposing `docs.gitlab.com/security/tokens/` would re-propose S144.

## Job 3 — candidate expected to REJECT

**Chosen reject candidate** (one, as the seat asks):

- URL: **https://about.gitlab.com/blog/how-to-detecting-secrets-in-video/**
- HTTP status: **200** (final URL unchanged), 188711 bytes.
- Access date: **2026-11-07**.
- Exact section heading (the page's H1): **"How-to: Detecting secrets in video content"**
- Located quote (≤25 words), from the "Scanning videos, one frame at a time" section:
  > "Our general approach to secret detection in videos is quite simple: Split the
  > video into frames, run optical character recognition (OCR) over each frame, and
  > match the text ..."
  (the page's sentence continues "…extracted text is checked against our known
  secret patterns.")

**Why it fails the lane's bar** — each reason independently sufficient:

1. **Wrong subject for the scope.** It is a corporate engineering blog post about
   OCR-based scanning of *video frames*. The scope is "GitLab token prefix and
   length"; the post states neither, and its token content is one OCR-error
   anecdote about a single value whose last character was misread as a backslash.
2. **It states no prefix/length rule.** Grep over the converted text for
   `glpat|glptt|glrt|gldt|glagent|glwt` returns **3 lines only**, all belonging to
   that one anecdote. No length, no tail, no prefix table.
3. **The lane's own intake gate refuses it.** Running the lane's own instrument:
   ```
   $ python3 -B corpus/instruments/capture-source.py --id SXXX \
       --url https://about.gitlab.com/blog/how-to-detecting-secrets-in-video/ \
       --out <scratch>/probe-blog/SXXX.txt --kind html
   INTAKE-REFUSED SXXX shape=gitlab-pat line=93 out=<scratch>/probe-blog/SXXX.txt written=no
   rc=3
   ```
   The lane cannot capture this page (it carries a published example value that
   the same scanner C2 extends matches as a live `gitlab-pat`), so it cannot anchor
   a registry row — binding rule B3 requires a row's anchor to be pinned to a lane
   capture.
4. **It is not a normative statement of GitLab's token formats** even setting the
   intake refusal aside: the registry's own precedent rejects vendor blog posts
   that "describe a program but supply no protocol" (S026, tier C, rejected).

Two further reject-shaped candidates I opened and discarded (recorded for
completeness in `R3-candidate-reject.txt`): `aikido.dev/blog/secret-detection-application-security`
(HTTP 200; a third-party marketing guide with **0** hits for any GitLab token
shape) and `semgrep.dev/blog/2025/secrets-story-and-prefixed-secrets/` (HTTP 200;
**0** hits for "gitlab" at all).

## Additional routed defect found while re-reading the landed instrument

**R96-SS-1 — the landed docstring's known-limits list overstates `glagent-` coverage.**

- S140 publishes **two** `glagent-` rules: capture **L213** (`glagent-` + exactly
  50 chars of `[0-9a-zA-Z_-]`, id `gitlab_kubernetes_agent_token`) and capture
  **L358** (the routable/versioned-routable form, id
  `gitlab_kubernetes_agent_token_routable`).
- The round-95 tip's known-limits list named `glagent-` with the **L213** citation
  (its list is positional: `glptt-`=73, `glft-`=190, `glimt-`=229, **`glagent-`=213**,
  `glwt-`=375, `glsoat-`=278, `glffct-`=392, `gloas-`=174, `glrct-`=412).
- The landed list drops `glagent-` altogether; the only surviving `glagent-`
  mentions are the new L358 shape (docstring L140, pattern L251, selftest L446).
- The L213 form is **still undetected**: probing `glagent-` + exactly 50 chars
  against both the base and the landed instrument gives **no hit** from any named
  pattern in either. The two rules are disjoint — L213 has no dotted tail, the
  landed matcher requires one.
- The rewrite was deliberate, not a carry-over: the landed list **added** five
  entries the round-95 tip lacked (the `GR1348941` runner-registration token,
  `feed_token=`, the `gitlab+deploy-token-N:` URL form, the `t1_` runner token
  without `glrt-`, and the `/trigger/pipeline?...token=` URL form), and I verified
  all five are genuinely undetected.

So the landed docstring now implies the `glagent-` family is fully covered while
the L213 form is neither detected nor listed. **This does not re-score C2** — the
frozen predicate is K1–K6, all of which pass — so it is a routed defect for the
L1. Suggested clause (not applied by me): restore the L213 citation, e.g. "the
50-character `glagent-` kubernetes-agent token (S140 line 213)".

## Receipts

Every command output cited above is in
`.ufo/waves/round-96/w1/ScoutSources-receipts/`:

| file | contents |
|---|---|
| `R1-s140-live.txt` | job 1 — the live fetch (HTTP 200, 20228 bytes, sha256), the seven quoted regex lines from the committed capture and from the live upstream, side by side |
| `R1-line-drift-proof.txt` | the drift mechanism: 29 blank lines dropped by `collapse()`, the reproduced collapsed digest, the byte-identical reconstruction, and the 30/51/73/136/324/358/375 -> 31/53/76/142/340/376/394 map with its offsets |
| `R2-candidate-prefix-length.txt` | job 2 — HTTP status of all 22 pages opened, the four grep probes run on the token-overview page, the `<th>` headers, and the per-page prefix/length findings |
| `R3-candidate-reject.txt` | job 3 — the reject candidate's URL/status/date/heading/quote, the four rejection reasons with the `INTAKE-REFUSED` output, and the two discarded alternatives |
| `R4-predicate-reverification.txt` | my own re-runs of both frozen counters (full stdout), the five C1 edits read out of the landing commit, the S041 line-content checks, and the base-vs-landed shape discrimination |
| `R5-routed-defect-glagent.txt` | R96-SS-1 in full, with the five pieces of evidence and the suggested clause |
| `R6-s144-already-held.txt` | the S144 row, manifest record and capture excerpt showing the job-2 page is already held, and the scope consequence |
| `R7-c1-controls-rerun.txt` | the verbatim output of my control-harness re-run (`C1-CONTROLS-RESULT pass controls=12`, `ATTRIBUTION pass fixtures=11`, rc=0) |

Tooling: **no tool was installed or upgraded** for this seat — every command used
tools already present on the host (`curl`, `python3`, `git`, `sed`, `grep`). Per the
operator directive of 2026-10-19, no install was needed and therefore none was made
(nothing to record for tool/version/channel/reason). The pacman guard was respected:
no pacman transaction of any kind was run.

Fixture-repo discipline: the control harness needs a candidate clone, so I created
one with `D=$(mktemp -d -p "$S" ctlclone.XXXXXX); git -C "$D" init -q` and asserted
`git -C "$D" rev-parse --show-toplevel` equals `$D` **before** the `remote add` /
`fetch` / `checkout` that followed. The clone lives in the seat scratch and is
removed by the EXIT trap.
