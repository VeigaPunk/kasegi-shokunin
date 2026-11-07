author: ScribeGate (round 97, attempt 1, wave 1)
seat: ScribeGate — UFO-FSD scribe (leaf; no subagents)
claims: C1 and C2 — drafts only; this seat asserts no claim verdict

# ScribeGate — round-97 Gate, SOURCES rows and knowledge-entry drafts

## Behavior

Drafted, in scratch and never in `corpus/`, the three artefacts the L1 will
verify: the round-97 lesson's Gate block, its Mistakes table, and the knowledge
entry `corpus/knowledge/gitlab-remaining-token-families.md`. Every number in the
drafts was re-derived by this seat rather than copied: both captures re-hashed,
the documentation pages re-fetched, the registry counted at the base and in the
working tree, the census re-run, the allowlist audit re-run at the C2 landing,
and the entry's ten quotes compared byte-for-byte against the S140 capture. The
deliverables are drafts; nothing was landed, and no product, judge, commit or
`corpus/` file was written.

## Verdict

DRAFTS READY — Gate and SOURCES rows re-derived; entry passes Q1-Q6 (and Q10).
No C1 or C2 verdict is asserted: this seat did not re-run either frozen
predicate, and a draft is not execution evidence.

## Deliverables

| artefact | durable path |
|---|---|
| Gate block draft | `.ufo/waves/round-97/w1/ScribeGate-receipts/drafts/gate-draft.md` |
| Mistakes table draft | `.ufo/waves/round-97/w1/ScribeGate-receipts/drafts/mistakes-draft.md` |
| Knowledge entry draft | `.ufo/waves/round-97/w1/ScribeGate-receipts/drafts/gitlab-remaining-token-families.md` |
| Q1-Q6 self-check | `.ufo/waves/round-97/w1/ScribeGate-receipts/05-q1q6-selfcheck.txt` |
| Receipts | `.ufo/waves/round-97/w1/ScribeGate-receipts/` (12 receipt files + `drafts/`) |

The scratch working copies (`/fast/scratch/hyaku/kasegi-r97/ScribeGate/…`) are
removed at seat exit; the `drafts/` copies are the durable ones.

## Gate (draft, round-96 shape)

Candidates considered this round (each number below was re-derived by this
seat: both captures re-hashed, both pages re-fetched, the registry counted at
the base and in the working tree, and the census re-run):

1. **S146 — GitLab Docs, Deploy tokens** — ADMIT (`docs`, tier A, `mined`).
   Opened 2026-11-07, HTTP 200, 51,391 bytes fetched (this seat's own re-fetch:
   HTTP 200, 51,391 bytes), 10,506 bytes / 238 lines committed as
   `corpus/source-snapshots/round-97/S146.txt` (sha256
   `a8e77bd6d351df2a5f8d8d5762e35bec7bb5be2b698fc0d4e2f5ee432f6145b5`,
   manifest `corpus/source-snapshots/round-97/manifest.json`). URL:
   `https://docs.gitlab.com/user/project/deploy_tokens/`. Quote (18 words,
   capture lines 69-70): "The default username format is
   gitlab+deploy-token-{n}. You can specify a custom username when you create
   the deploy token." The page states the HTTP username structure only — it
   opens the pair at line 68 ("A deploy token is a pair of values:") — so the
   20-character secret length and alphabet stay S140's ground (line 341). Its
   custom-username sentence is the scope limit the round's
   `gitlab-deploy-token-in-url` shape carries.
2. **S147 — GitLab Docs, Incoming email** — REJECT (kept `rejected`, tier B).
   Opened 2026-11-07, HTTP 200, 164,826 bytes (this seat's own re-fetch: HTTP
   200, 164,826 bytes). URL:
   `https://docs.gitlab.com/administration/incoming_email/`. The page was read
   and searched for `glimt`: 0 hits (this seat's independent conversion: 0
   hits; the L1's sweep is `.ufo/waves/round-97/l1/s147-reject-r97.txt`). It
   describes incoming-email configuration but states no token prefix, length or
   alphabet, so it cannot ground the incoming-email shape; S140:229 remains the
   only ground. Flip: the page adds a token-format section naming `glimt-` or
   its length.
3. **S140 — GitLab rules `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4** —
   re-opened from its committed capture for the ten rules this round implements
   (lines 101, 160, 174, 190, 213, 229, 278, 341, 392, 412; capture sha256
   `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563
   lines; both re-verified by this seat). The L1's live `/-/raw/` fetch answered
   HTTP 403 (a Cloudflare challenge page, 6,078 bytes, receipt
   `.ufo/waves/round-97/l1/s140-live-fetch-r97.txt`), so the committed capture
   is the citation base and this round's S140 quotes are capture-verified, not
   live-verified. The row's status (`mined`), recheck and used-by are unchanged.
4. **GitLab Docs, Pipeline trigger tokens** — screened, NOT admitted; no row
   proposed, so the registry stays at 147. Opened 2026-11-07, HTTP 200, 61,918
   bytes (this seat's fetch; receipt
   `.ufo/waves/round-97/w1/ScribeGate-receipts/04-triggers-page.txt`). URL:
   `https://docs.gitlab.com/ci/triggers/`. Quote (14 words, converted text line
   98): "You can view and copy the full token for all triggers you have
   created." Reason: the page shows the token only as the `<token>` placeholder
   in a path-dependent query string
   (`.../trigger/pipeline?token=<token>&ref=<ref_name>`, line 121) and states no
   length or alphabet (its only "characters" sentence, line 99, is about the UI
   showing the first 4 characters to other project members), so a shape keyed on
   it would be a placeholder matcher; the `/trigger/pipeline` form stays a known
   limit (S140:532). Flip: the page states the trigger token's length or
   alphabet, or a rules source publishes its body.

Status / used-by changes this round, old → new:

- S146: (new row) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-remaining-token-families.md`.
- S147: (new row) → `rejected`; used-by `—` (unchanged).
- S140: status `mined` (unchanged), used-by unchanged (`corpus/instruments/capture-secret-scan.py`).

Registry 145 → 147 rows: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
prints 145 at the base and 147 in the working tree (both re-run by this seat).
Census:
`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the seven inherited W04 duplicate-URL warnings
(S028, S029, S072, S076, S080, S085, S143) — re-run by this seat, rc 0.

## Mistakes (draft)

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M97-1 | gate-blindspot | the C2 clean-run limb is the gate that found the round-96 wave receipts: the landed run prints `LIMB K2 ok rc=0 scanned=3018 hits=0 allowed=27 unused_allow=0` (`.ufo/waves/round-97/l1/c2-candidate-r97.txt:3`; the landing run at `a9a53608`, seed 20261107, prints the same in `.ufo/waves/round-97/w1/ExecC2Counter-receipts/gate-seed20261107.txt`), and the redaction pass records `REDACTION-RESULT files=43 values=181` (`.ufo/waves/round-97/l1/redaction-r97.txt`, last line) | K2 itself (the capability's own clean-run limb) — the lane had never scanned its wave receipts at a landing that included a previous round's receipts | the wave receipts are redacted structurally (one `[<shape>-fixture-redacted-r97]` marker per matched value, line numbering preserved, before/after digests in `.ufo/waves/round-97/l1/redaction-r97.txt`); the landing's K2 prints `hits=0 allowed=27 unused_allow=0`. `[draft note: the first-run figure hits=56 is not receipted by any file under .ufo/waves/round-97 or the L1 scratch — attach that run's output or drop the number.]` |
| M97-2 | redaction-scope | a new shape exposes old receipts: `.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt:76` now carries `[gitlab-deploy-token-in-url-fixture-redacted-r97]`, and the redaction receipt lists that file with `gitlab-deploy-token-in-url=1` | the K2 re-run after the first sweep | the sweep walks all of `.ufo/waves` (43 files, 181 values), never one round: the round-94 redaction could not see a shape that did not exist then. `[draft note: the intermediate hits=1 is unreceipted; the receipted facts are the marker at line 76 and the per-file count.]` |
| M97-3 | redaction-overreach | a value an allowlist row already adjudicates must be restored, not redacted, or the row dies: the allow audit at the C2 landing prints `rows 25 live 25 dead 0` (re-run by this seat, rc=0, 54 s), and the redaction receipt's header records the four restored receipts | K2's `unused_allow` limb | restore those receipts from the base; the allow row is the record that the value is not a secret. `[draft note: unused_allow=16 is unreceipted; the audit's dead 0 is the receipted consequence.]` |
| M97-4 | count-from-memory | the "twelve corpus/knowledge files" wording is in the wave spec's `ExecC1Indep` task (`.ufo/waves/round-97/w1-spec.json`, generated by `.ufo/waves/round-97/make-wave-r97.py:83`), not in `claims.json`: the frozen statement says "sixteen corpus/knowledge files" (2 occurrences at the freeze `daf7fc6a` and in the working tree) | the post-apply `git diff --name-only` (16 files) | count the path set from the map (`git diff --name-only` after applying `repair-map.tsv`), never from the label list or the dispatch prose. `[draft note: the row as drafted blamed claims.json; the frozen artifact is correct, the dispatch task text is not.]` |
| M97-5 | shape-id-vs-prefix | K5's `named` check is separate from its count and round checks: `named = all(s in rows[0] for s in sorted(NEW_SHAPES))` (`.ufo/waves/round-97/c2/capability-check.py:249-252`), so a row that names the families by prefix passes `rows=1 last=87` and still fails K5 | K5 (`named=True` requires every `NEW_SHAPES` id in the row) | the capability row names all ten shape ids beside their prefixes: `git show a9a53608:SCORECARD.md \| sed -n '307p'` contains 10/10 ids (`gitlab-runner-registration-token`, `gitlab-feed-token`, `gitlab-oauth-app-secret`, `gitlab-feed-token-v2`, `gitlab-incoming-email-token`, `gitlab-scim-oauth-token`, `gitlab-deploy-token-in-url`, `gitlab-feature-flags-client-token`, `gitlab-runner-controller-token`, `gitlab-kubernetes-agent-token`), and K5 prints `named=True`. `[draft note: the "first clause failed" narrative is unreceipted — no round-97 file carries named=False; keep the row as the requirement plus the enforced check unless the failing run is attached.]` |
| M97-6 | attribution-coupling | a qualify-lane fixture that removes or malforms its label's target fails M4 and M5 together, because M5's range check is defined on M4's resolved value ("an unbound value cannot be range-checked", `.ufo/waves/round-97/controls/c1-controls-r97.py:5-9`): `CONTROL qualify-target-missing rc=1 want=1 PASS limbs=M4,M5 declared=M4,M5 attribution=PASS` (`.ufo/waves/round-97/controls/c1-controls-r97.txt:59`); the same fixture mis-declared in round 96 printed `limbs=M10,M4,M5,M9 declared=M4,M5 attribution=FAIL` (`.ufo/waves/round-96/controls/c1-prefreeze-defects-r96.txt:20`) | the harness's attribution check (`limbs=` must equal `declared=`) | declare `M4,M5` for every fixture whose qualify target is missing or not INTERNAL, and keep one reason per fixture (R154) |
| M97-7 | attribution-coupling | a qualify-lane map row that disagrees with its label fails M4, M5 and M9 together, because the map row must equal the label's named edit (`.ufo/waves/round-97/controls/c1-controls-r97.py:8-10`): `CONTROL map-not-label rc=1 want=1 PASS limbs=M4,M5,M9 declared=M4,M5,M9 attribution=PASS` (`.ufo/waves/round-97/controls/c1-controls-r97.txt:81`) | the harness's attribution check | declare `M4,M5,M9` for the map-vs-label fixture and pick a site no other map row names, so the fixture cannot also trip M3 (the round-96 M96-3 defect) |

## Knowledge entry draft — Q1-Q6 self-check

Draft at `.ufo/waves/round-97/w1/ScribeGate-receipts/drafts/gitlab-remaining-token-families.md`.
It opens with the H1, then `source:` (S140 with its capture sha256 and ten line
anchors, S146 with its URL and `:68-70`), `verified-at:` (2026-11-07, with the
403 note), and one `recheck:` chain. Body: a ten-row shape table, the ten S140
rule lines verbatim (each 3 whitespace tokens), the S146 quote, one falsifiable
length rule, three rejected over-generalizations, the three remaining limits,
and a documentation-only statement.

| criterion | result | evidence |
|---|---|---|
| Q1 | PASS | H1 first, then `source:`/`verified-at:`/`recheck:`; S140+S146 ids, S146 URL, capture anchors |
| Q2 | PASS | S140 tier A, S146 tier A (both opened this round) |
| Q3 | PASS | ten S140 quotes byte-identical to the capture (max 3 words each); S146 quote 18 words, exact |
| Q4 | PASS | "GitLab's own rules file", "S146 states", "S144 (round 96) states" |
| Q5 | PASS | falsifiable ±1-length rule + three rejected over-generalizations |
| Q6 | PASS | documentation-only statement; `capture-secret-scan.py --files` rc 0, hits=0 |
| Q10 | PASS | recheck carries the lane-root `cd … &&` prefix; `bash -n` rc 0; execution prints `RECHECK-OK` |

## Findings (routed to the L1; none re-scores a claim)

- **F1 — quote word count.** The lesson Gate and the untracked entry both say the
  S146 quote is 22 words; it is 18 (`The default username format is
  gitlab+deploy-token-{n}. You can specify a custom username when you create the
  deploy token.`). Correct the count in both.
- **F2 — M97-4 misattributes "twelve".** The frozen `claims.json` says "sixteen
  corpus/knowledge files" (2 occurrences at the freeze and in the working tree);
  the "twelve" is in the wave spec's `ExecC1Indep` task (`w1-spec.json`, generated
  by `make-wave-r97.py:83`). Fix the row's evidence pointer.
- **F3 — four unreceipted numbers.** `hits=56` (M97-1), `hits=1` (M97-2),
  `unused_allow=16` (M97-3) and `named=False` (M97-5) appear nowhere under
  `.ufo/waves/round-97` or the L1 scratch; only the lesson itself carries them.
  Attach the first-run outputs or rephrase each row to its receipted facts.
- **F4 — two census bullets.** The uncommitted `corpus/SOURCES.md` carries
  `Round 97 census: registry 145 -> 146` and `Round 97 census (final): registry
  145 -> 147`. Keep one final line (or label the first `intermediate`); the
  registry's actual count is 147.
- **F5 — dangling used-by.** S146's used-by names
  `corpus/knowledge/gitlab-remaining-token-families.md`, which is untracked today;
  it must land in the same commit or the cell is a dangling reference.
- **F6 — S146 anchor cell.** The row's anchor cell carries the quote and the open
  date but no capture lines; S144's row gives `lines 344-347`. Add `lines 68-70`
  (and `line 68` for "A deploy token is a pair of values:").
- **F7 — L1 landing receipt in scratch only.** The C2 landing run at `a9a53608`
  (seed 20261107) exists as `/fast/scratch/hyaku/kasegi-r97/l1/c2-landing.txt`,
  not under `.ufo/waves/round-97/l1/`. The wave receipts do carry the same run
  (`ExecC2Counter-receipts/gate-seed20261107.txt`, `ConnectorOverlap-receipts/`,
  `MutC2Counter-receipts/00-pristine-gate-with-pin.txt`), so the landing is
  covered; commit the L1 copy for the lesson's own pointer.
- **F8 — entry quotes only 3 of 10 rules.** The untracked entry quotes S140 lines
  101, 229 and 341; the assignment asks for a verbatim ≤25-word quote per shape.
  The scratch draft carries all ten, each byte-identical to the capture.
- **F9 — candidate revision.** The dispatch prose says the pre-freeze K1-K6 pass
  was at scratch candidate `72fa2fa1`; the frozen claims and every receipt say
  `659e320f`. ExecC2Counter already routed this; the lesson should cite
  `659e320f` or explain the earlier candidate.
- **F10 — S147 independently reproduced.** The reject's absence sweep is
  reproducible: HTTP 200, 164,826 bytes, `glimt` 0 hits, `gitlab+deploy-token`
  0 hits.
- **F11 — fourth candidate screened.** `https://docs.gitlab.com/ci/triggers/`
  (HTTP 200, 61,918 bytes) states the trigger token only as a `<token>`
  placeholder; screened and not admitted, no row proposed. The Gate draft records
  it so the `/trigger/pipeline` limit has a dated screening.
- **F12 — S140 is capture-verified, not live-verified, this round.** The live
  `/-/raw/` fetch returned HTTP 403 (Cloudflare, 6,078 bytes), so every S140
  quote in the Gate and the entry is bound to the committed capture's digest. The
  Gate draft says so explicitly rather than repeating round 96's live-verified
  status.

## Out of scope

- No claim predicate (C1 P1-P4, C2 K1-K6) was re-run; no AGREE/STANDS is claimed.
- No product, instrument, counter, lesson, `corpus/` or `MANIFEST.json` edit; no
  git/jj mutation; no commit, push or publish; no subagent; no `ask`.
- No tool was installed or upgraded this seat (none was needed).

## Receipts

| # | command | observed |
|---|---|---|
| 1 | `sha256sum corpus/source-snapshots/round-94/S140.txt corpus/source-snapshots/round-97/S146.txt` | rc 0; `f3fd09e4…`, `a8e77bd6…` |
| 2 | `wc -l` on the same two files | rc 0; 563 and 238 lines |
| 3 | `git show b06af5e0:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`; same on the working tree | 145; 147 |
| 4 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | rc 0; `kasegi ok`, seven W04 lines |
| 5 | `curl … https://docs.gitlab.com/user/project/deploy_tokens/` | http=200 bytes=51391 |
| 6 | `curl … https://docs.gitlab.com/administration/incoming_email/` | http=200 bytes=164826; converted text `glimt`=0, `gitlab+deploy-token`=0 |
| 7 | `curl … https://docs.gitlab.com/ci/triggers/` | http=200 bytes=61918; lines 98 and 121 as quoted |
| 8 | `KASEGI_LANE_ROOT=… python3 -B corpus/instruments/anchorcheck.py <draft>` | rc 0; 2 in-range cites, 0 bad |
| 9 | `bash -n <recheck line>`; then the chain with the scratch path | rc 0; rc 0, `RECHECK-OK` |
| 10 | `python3 -B corpus/instruments/capture-secret-scan.py --files <draft>` | rc 0; `hits=0 files=0` |
| 11 | `python3 -B corpus/instruments/capture-secret-scan.py --selftest` | rc 0; `SELFTEST-RESULT pass cases=148` |
| 12 | `python3 /fast/scratch/hyaku/kasegi-r97/l1/allow-audit.py a9a53608 …` | rc 0; `rows 25 live 25 dead 0` |
| 13 | quote comparison script (entry vs capture) | 10/10 S140 lines match; S146 18 words exact |
| 14 | `capture-secret-scan.py --files` over the drafts and the 12 receipt files | rc 0; `scanned=15 hits=0 files=0` |
| 15 | evidence greps (`hits=56`, `unused_allow=16`, `named=False`, `twelve`, `named=True`, SCORECARD ids, round-94 line 76) | no `hits=56`/`unused_allow=16`/`named=False`; `twelve` in `w1-spec.json`; `claims.json` sixteen ×2; 10/10 SCORECARD ids; marker at round-94 line 76 |

Receipt files: `.ufo/waves/round-97/w1/ScribeGate-receipts/01-captures-and-registry.txt`,
`02-s146-fetch.txt`, `03-s147-page.txt`, `04-triggers-page.txt`,
`05-q1q6-selfcheck.txt`, `06-anchorcheck.txt`, `07-recheck.txt`,
`08-scan-draft.txt`, `09-allow-audit.txt`, `10-quote-verify.txt`,
`11-selftest.txt`, `12-evidence-greps.txt`.
