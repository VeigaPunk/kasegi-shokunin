author: kasegi (round 99, attempt 1)

# Round 99 — lesson

Lane: kasegi. Round 99, attempt 1. Base `b9411a6b530e486180cf14c72fccc46668dcf5ee`;
freeze `6195db307c1cb101eba1d268f8cbfc1578d2caf7`; C2 landing
`a3db47e71fe292c03b00ba11f38cccbec45d3966`; C1 landing
`35e3ab6041ff8690b00d831f27b93d08101fd16a`; landing receipt
`29cd3058c8651b05881764893558deab6780ef1a`.

## Gate

Candidates considered this round:

1. **S150 — GitLab secret-detection-rules merge request !151, the
   assignment-context generator** — opened this round (live fetch HTTP 200,
   128,120 bytes, sha256
   `aa60d7af465cad03b64259362dfa862a8d5c3176ebc2e6b5909a38daddea11e8`).
   URL:
   `https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/merge_requests/151`.
   The MR description's "Generated Regex" block states the form the round-99
   separator model implements. Quotes (each under 25 words):
   - "Generated Regex:" block —
     `(?:API_SECRET_KEY|api_secret_key|apiSecretKey|SECERT_KEY|secret_key|secretKey).{0,8}[:=].{0,8}([a-z]{32})\b`
   - `keywordGroupType` enum sentence —
     `Indicates whether to inject keywordGroup directly as provided, or generate multiple case variant combinations`
   Admitted: kind `code`, tier B, status `mined`, used-by
   `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`.
2. **S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at
   commit 59ada1f4** — re-opened from its committed capture for the
   session-cookie rule (lines 547-551; capture
   `corpus/source-snapshots/round-94/S140.txt`, sha256
   `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563
   lines). The live `/-/raw/` fetch answered HTTP 403 again (a Cloudflare
   challenge page), so the capture is the citation base. Quote (`S140:550`):
   - `assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''`
   Status `mined` and recheck `180d` unchanged; used-by unchanged.
3. **S148 — GitLab secret-detection rule prose, session cookie** — re-opened
   from its committed capture for the value's length and alphabet. Quote
   (`S148:6`):
   - `The value is a 64-character hexadecimal session ID, with an optional \`cell-<ID>-\` prefix.`
   Status `mined` and recheck `180d` unchanged; used-by unchanged.
4. **A new row for the round-98 sentinel's MR quote — REJECTED as a duplicate
   of S150.** The sentinel's `assignment-context.txt` recorded the same MR
   without a URL; writing a second row for the same page would duplicate it,
   so the round-99 row carries the URL and the sentinel's receipt is cited as
   its discovery pointer instead. Flip: none (the page is the source either
   way).

Status / used-by changes this round, old → new:

- S150: new row, status `mined`, used-by
  `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`.
- S140: no cell change (re-opened from the capture; live fetch 403).
- S148: no cell change (re-opened from the capture).

Registry 149 → 150 rows:
`grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` prints 149 at the base
and 150 in the working tree. Census at round start and at round end:

```text
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi  W04  S028 duplicate url … (seven inherited W04 warnings)
kasegi  ok   /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
rc=0
```

Both runs exit 0; the seven inherited W04 duplicate-URL warnings (S028, S029,
S072, S076, S080, S085, S143) are unchanged.

Spot-check result: pending the round-99 non-author closure.

## Learning

- **expansion: improved** — S150 is new ground (the assignment-context
  generator's own semantics, which no row held: the rules file states the rule
  and the keyword group, never the window), and the `capture-secret-scan`
  capability row gains a separator class that covers twelve real session
  values it refused.
- **quality: improved** — the census of record is now tamper-evident and
  layout-stable: the committed 12-class harness scores 5/12 on the round-98
  instrument and 12/12 on the landing instrument, `--check` passes in a clean
  and in a contaminated work dir with the identical pinned triple, and the
  exact command completes in 2.23 s at 512 MB peak RSS instead of dying under
  earlyoom at 3.5 GiB. The scanner's session-cookie window now matches S140's
  assignment-context form (probe 0/12 → 12/12, ten boundary negatives clean),
  selftest 170 → 192.
- **discernment: improved** — seven mistakes mined (M99-1…M99-7), including two
  the round's own controls caught before the landing (the confined-HOME
  propagation and the census body's scratch path) and one that recurs from
  round 98 (a new shape exposing old receipts). The round-98 spot-check's
  routed defects 1–9 are closed or answered below.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M99-1 | instrument-environment | the tamper harness's `write_census()` did not pass the confined `HOME` to the instrument, so the round-98 instrument globbed the real `~/Projects/**` and its `resolve.py` child reached 6.7 GB RSS (`ps` on pid 3320550, `VmRSS: 6748632 kB`) and had to be killed; the same harness with the env passed completes the base run in 14 s | the harness's own runtime observation (the runaway child) | every child invocation in the harness now takes `env` (`write_census(..., env)`); the base and candidate receipts both print in ~20 s |
| M99-2 | fixture-design | the `write-not-ancestor` control first passed (rc 0) because the fixture's `git commit` ran on the clone's `master` HEAD and advanced the branch, so the "dangling" commit was the tip; `git merge-base --is-ancestor` returned 0 | the control's own rc (0 where 2 was expected) | the fixture detaches before committing (`checkout --detach master`), then returns to `master`; the control prints `rev-not-ancestor rc=2` (`.ufo/waves/round-99/controls/c1-layout-memory-controls-r99.txt`) |
| M99-3 | scratch-leak (M98-1 class) | the census body embedded the confined HOME path in resolve.py's "Mirror root" line (`/fast/scratch/…/w1/home/Projects/the-bounty-hunter`), so the clean and dirty bodies differed and `--check` printed `body-mismatch` | the first dirty-layout run (rc 1 where 0 was expected) | the body rewrites the home dir to `<confined-home>/` beside the extract-path rewrite; `grep -c 'fast/scratch' corpus/instruments/citation-survival.md` prints 0 |
| M99-4 | layout-dependence (R157's body half) | even with the pinned rate confined, the body's aggregate counts moved (INTERNAL 2608 vs 2610) because `../` rows resolved against the caller's work dir | the dirty-layout diff of the two bodies | the extract lives under a private parent (`<work>/extract-<rev12>/tree`) that holds only the extract, so a `../` walk-out is absent on every host; both layouts now print the same body digest |
| M99-5 | shape-exposes-old-receipts (M98-4 class) | the new session-cookie window matched 53 synthetic 64-hex values in four round-98 sentinel receipts; the landing scan printed `hits=4 files=4` (one hit per file) | K4's clean-run limb at the first C2 landing | all 53 values redacted structurally (one `[session-cookie-fixture-redacted-r99]` marker per value, line numbering preserved, before/after digests in `.ufo/waves/round-99/controls/redaction-r99.txt`); the post-redaction scan prints `hits=0 unused_allow=0` |
| M99-6 | counter-expressibility | the poisoned-cache class was first not expressible against the round-98 format (`header_lines()` required a `home:` line the round-98 census has no such line for), so the base scored 6/12 for the wrong reason | the harness's `NOT-EXPRESSIBLE` line | `header_lines()` treats `home:` as optional and the fake cache is built from the census's own pinned numbers; the base now scores 5/12 and the poisoned-cache class is a real survivor on it |
| M99-7 | claim-transcription | both claims' `controls` field was hand-typed in a `CONTROL <name> rc=… want=… PASS` form the round-99 receipts do not print (they print `TAMPER-RESULT` / `PROBE-RESULT` / `SELFTEST-RESULT` lines), so the field was not a verbatim copy of the executed receipt (R148) | the round's own R148 check, run while assembling the report | an `erratum` on each claim quotes the receipts' verbatim lines and states that no predicate, target, kill rule or pin changes (`.ufo/waves/round-99/claims.json`); the receipts are the authority |

## Routed defects from the round-98 spot-check

1. **Census label (high) — closed.** The pinned rate is now revision-stable by
   construction (confinement + private extract parent); the label stays true
   and the exact command runs in 2.23 s at 512 MB (P4), so the earlyoom
   failure is gone.
2. **Harness pin (medium) — closed by construction.** Every `*_sha256` in
   `claims.json` is the committed blob's digest: `git show
   35e3ab60:corpus/instruments/census-at-rev.py | sha256sum` prints the pin
   (`.ufo/waves/round-99/controls/c1-landing-r99.txt`).
3. **Check coverage (medium) — closed.** The 12-class harness covers body
   hand-edits, host-line removal/editing, host-owned edits, body provenance,
   poisoned cache, body truncation and the four classes the round-98 check
   already caught; 12/12 at the landing.
4. **Gate records for S148/S149 (medium) — closed** by the appended
   corrections block in `corpus/lessons/round-98.md`.
5. **Correction sweep (medium) — closed** by the same appended block
   (147 → 149, the superset wording, the S140 used-by four paths).
6. **LOG bullet pointers (low) — closed** by the appended LOG correction.
7. **Clean re-scan receipt (low) — closed**: the post-redaction scan is
   committed in `.ufo/waves/round-99/controls/c2-landing-r99.txt`.
8. **C1 body host-dependence (low) — closed**: the body is layout-stable now
   (M99-4) and the census's `home:` line names the confined environment.
9. **Dispatch text numbers (low) — closed**: the round-99 dispatch quotes the
   landing census's numbers (2607/8026), not the base's.

## Wave findings (round-99 w1, 13 seats)

Pending WAVE-DONE.
