author: kasegi (round 97, attempt 1)

# Round 97 — lesson

Lane: kasegi. Round 97, attempt 1. Base `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`;
freeze `daf7fc6a627d615178c27594110e956e592e4cd9`; C1 landing
`75a471809cba265c8981ece1c0ed29c7895d9308`; C2 landing
`a9a53608dce6aea07d298bb9d5133532078eb1dd`.

## Gate

Candidates considered this round:

1. **S146 — GitLab Docs, Deploy tokens** — ADMIT (`docs`, tier A, `mined`).
   Opened 2026-11-07, HTTP 200, 51,391 bytes fetched, 10,506 bytes / 238 lines
   committed as `corpus/source-snapshots/round-97/S146.txt` (sha256
   `a8e77bd6d351df2a5f8d8d5762e35bec7bb5be2b698fc0d4e2f5ee432f6145b5`).
   URL: `https://docs.gitlab.com/user/project/deploy_tokens/`. Quote (18 words,
   capture lines 69-70): "The default username format is
   gitlab+deploy-token-{n}. You can specify a custom username when you create
   the deploy token." The page states the HTTP username structure only; the
   20-character secret length and alphabet stay S140's ground (line 341). Its
   custom-username sentence is the scope limit the round's
   `gitlab-deploy-token-in-url` shape carries.
2. **S147 — GitLab Docs, Incoming email** — REJECT (kept `rejected`, tier B).
   Opened 2026-11-07, HTTP 200, 164,826 bytes. URL:
   `https://docs.gitlab.com/administration/incoming_email/`. The page was read
   and searched for `glimt`: 0 hits; it describes incoming-email configuration
   but states no token prefix, length or alphabet, so it cannot ground the
   incoming-email shape (absence sweep
   `.ufo/waves/round-97/l1/s147-reject-r97.txt`). Flip: the page adds a
   token-format section naming `glimt-` or its length.
3. **S140 — GitLab rules `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4** —
   re-opened from its committed capture for the ten rules this round implements
   (lines 101, 160, 174, 190, 213, 229, 278, 341, 392, 412; capture sha256
   `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563
   lines). The L1's live `/-/raw/` fetch answered HTTP 403 (a Cloudflare
   challenge page, 6,078 bytes, receipt
   `.ufo/waves/round-97/l1/s140-live-fetch-r97.txt`), so the committed capture
   is the citation base. The row's status (`mined`), recheck and used-by are
   unchanged.

Status / used-by changes this round, old → new:

- S146: (new row) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-remaining-token-families.md`.
- S147: (new row) → `rejected`; used-by `—` (unchanged).
- S140: status `mined` (unchanged), used-by unchanged (`corpus/instruments/capture-secret-scan.py`).

Registry 145 → 147 rows: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
prints 145 at the base and 147 in the working tree. Census:
`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the seven inherited W04 duplicate-URL warnings
(S028, S029, S072, S076, S080, S085, S143).

Spot-check result: pending the round-97 non-author closure.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M97-1 | gate-blindspot | the round-97 C2 candidate's clean-run limb failed at the first run: `LIMB K2 FAIL rc=1 scanned=3018 hits=56` — 56 (file, shape) hits, all in `.ufo/waves/round-96/w1/**-receipts/` (the round-96 mutation campaign's mutant sources and the probe's generated fixtures) | K2 itself (the capability's own clean-run limb) — the lane had never scanned its wave receipts at a landing that included a previous round's receipts | the wave receipts are redacted structurally (marker per matched value, line numbering preserved, before/after digests in `.ufo/waves/round-97/l1/redaction-r97.txt`); the landing's K2 prints `hits=0 allowed=27 unused_allow=0` |
| M97-2 | redaction-scope | the first redaction swept `.ufo/waves/round-96` only; the re-run still printed `hits=1` — `.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt:76` carries a `gitlab+deploy-token-…@` value the round-94 redaction could not see because the shape did not exist then | the K2 re-run after the first sweep | the sweep walks all of `.ufo/waves` (43 files, 181 values); a new shape exposes old receipts, so the sweep is by shape set, never by round |
| M97-3 | redaction-overreach | the first full sweep also redacted 16 values that already had allowlist rows (the round-85 `gone.json`/`hunt2.json` citation-hunt tokens, the round-94 `ghr_` placeholder, the round-95 bearer row) and the gate then printed `unused_allow=16` | K2's `unused_allow` limb | a value an allowlist row already adjudicates is restored from the base, not redacted: the row is the record that it is not a secret, and redacting it kills the row. The four receipts are restored; the allow audit prints `rows 25 live 25 dead 0` |
| M97-4 | count-from-memory | `claims.json` said the tranche spans "twelve corpus/knowledge files" while the map's 33 rows span sixteen; the first `git diff --stat` after applying the map showed 16 files | the post-apply diff (not the claim's own text) | count the path set from the map (`git diff --name-only` after applying), never from the label list. The statement, P3 and the wave context were corrected before the freeze; the `surface` cell kept "12" and the wave's ExecC1Indep and ReviewC1Sites caught it — routed to round 98 (the frozen text is not rewritten) |
| M97-5 | shape-id-vs-prefix | the first SCORECARD clause named the ten families by prefix only (`glft-`, `gloas-`, …), so K5's `named` check failed: the row must name the shape ids the instrument reports | K5 (`named=True` requires every `NEW_SHAPES` id in the row) | the capability row names all ten shape ids beside their prefixes; K5 passes at the landing |
| M97-7 | unscanned-wave-evidence | the first wave-evidence commit was refused by GitHub push protection (GH013) on `ExecC2Probe-receipts/fixture-bytes.txt` (10 shapes) and the second on the seat report `ExecC2Probe.md` (10 shapes quoted in its table); two unpushed blocked commits were abandoned (the round-94 precedent), the bookmark restored, and the evidence redacted | the push refusal itself — R153 was written this round but not applied to the wave evidence before committing it | scan the wave evidence with `capture-secret-scan.py --files` over every file (not only `-receipts` paths) before the wave-evidence commit; the seat report and the receipts are both in scope. The redaction receipts are `.ufo/waves/round-97/l1/redaction-r97-w1.txt` and the landing scan prints `hits=0` |
| M97-6 | stale-candidate-in-dispatch | the wave `context` says "the pre-freeze K1-K6 pass at the scratch candidate 72fa2fa1"; that candidate FAILED K2 (hits=56) and the passing candidate is `659e320f` | ExecC2Counter's item 1, which re-ran the gate and read the receipt | the wave text is generated from the freeze artifacts; when a candidate is superseded before the freeze, the context must name the candidate whose receipt is committed (the receipt path is the authority, the hash is a convenience) |

## Wave findings (round-97 w1, 14 seats)

All fourteen seats settled; none died. Both claims stand on their frozen
predicates, and the wave routed the findings below (none re-scores a claim).

**C1 — STANDS on P1-P3.** CriticClaimsC1 re-derived every limb with its own
census and map application; ExecC1Indep AGREE (independent meter
1040/2041 -> 1043/2035, byte-exact map application at all sixteen files, 33 rows
on 30 lines); ReviewC1Sites **33 CORRECT / 0 PARTIAL / 0 WRONG**; CriticHarm NO
HARM (no line touched that the map does not label, no resolution lost).

**C2 — STANDS on K1-K6.** CriticClaimsC2 re-derived every limb at three seeds of
its own plus an 88-case boundary audit; ExecC2Probe 10/10 shapes with 30
positives and 30 negatives of its own; ExecC2Counter AGREE on all four items;
ReviewC2Scanner APPROVE; SentinelShapes C2 STANDS; CriticHarm NO HARM (0 masked
pairs, allowlist byte-identical, landing scans clean); ScoutSources re-fetched
the live rules file (HTTP 200, sha256 `14854f71…` = the manifest's raw digest)
and confirmed all ten regexes byte-identical.

### Routed defects for round 98

1. **C1 counter hole (medium).** The M4 `qualify-lane` branch does not require
   `target == "corpus/instruments/" + key`: CriticClaimsC1 built a clone whose
   label names `corpus/instruments/density.py` for the key `resolve.py` and the
   meter printed `pass rc=0` (fixture `bfdfae1a`). The landing's 33 labels are
   all same-name, so the claim stands; the correction (`or target !=
   "corpus/instruments/" + key`) and a `qualify-wrong-instrument` fixture go to
   the next freeze.
2. **C2 right boundary narrower than S140 (medium).** SentinelShapes MUST-FIX 1
   and ReviewC2Scanner F2: five shapes (`gitlab-runner-registration-token`,
   `gitlab-feed-token`, `gitlab-oauth-app-secret`, `gitlab-feed-token-v2`,
   `gitlab-scim-oauth-token`) reject a real token followed by `_` or `-`, while
   S140 lines 101/160/174/190/278 accept it. One-character evasion, 10/10
   payloads. Not re-scored: K3's declared boundary negatives are the claim's
   predicate.
3. **Gate forgery survives (high).** MutC2Counter F01: ten literal-locked
   patterns that match only the fixture literals pass K1 and K3, because the
   selftest table and the plant table use the same literals. K3's plants are not
   independent of K1's selftest; a round-98 gate needs plants generated
   independently of the instrument's own cases.
4. **Four further S140 GitLab rules undetected and unnamed (medium).**
   ReviewC2Scanner F5: `gitlab_ci_build_token` (S140:293, non-JWT `glcbt-`),
   `gitlab_iam_refresh_token` (480), `gitlab_iam_authorization_code` (497) and
   `gitlab_session_cookie` (549) have no shape and no limit entry; the
   statement's "keeps only …" reads as the complete remaining gap when it is
   not. Pre-existing (the base instrument names none either).
5. **Capture anchors offset from upstream (medium).** ScoutSources: the S140
   capture dropped 30 blank lines and stripped the 82 example lines'
   indentation, so the cited capture lines are not the upstream file's lines
   (capture 101 = live 105; capture 412 = live 433). The content of every cited
   line is byte-identical and the capture is reproducible from the live file;
   the manifest's "line numbering preserved" sentence is inaccurate.
6. **`citation-survival.md` still not regenerated (low, carried).** Unchanged
   base..landing, last updated at round 57; excluded from the meter's scope, so
   pre-existing staleness, not a C1 regression. The planned round-97 item was
   not taken (the round's C1 is the qualify-lane tranche); it needs a
   revision-pinned wrapper that separates host-owned absolute tokens.
7. **Claim-text qualifiers (low).** `claims.json` C1.surface says "12
   corpus/knowledge files" (sixteen); the statement's "-6 denominator"
   parenthetical compresses the arithmetic (9 bare GONE rows leave, 3 new
   INTERNAL rows enter; the six existing qualified targets contribute 0); the
   seat spec said "P1-P4" while the frozen predicate has P1-P3; row 12's
   evidence wording says "header comment" for a pin-declaration form. The
   frozen text is not rewritten; the corrections ride the next round.
8. **Pre-freeze candidate revs are scratch objects (low, carried).** The
   committed control receipt names `candidate=f410e91f` / `freeze=2059fcba`,
   which do not resolve in the lane object store; the post-landing re-run at
   `75a4718`/`daf7fc6` is the reproducible half (14/14, ATTRIBUTION 13).
9. **Mirror-dependent reproduction (low).** The meter prints
   `mirror_absent=True`; the predicate does not pin it, so a host carrying the
   bounty mirror would need the same note to reproduce the reading.

### Assimilation

None adopted: the staged `merge/kasegi/` ids collide with the lane registry on
94 of 94 rows (`.ufo/waves/round-97/assimilation/collisions`), so a renumber by
document would be the whole round. The indented-row guard is proven this round
(`.ufo/waves/round-97/assimilation/guard-receipt.txt`, verdict PASS).
