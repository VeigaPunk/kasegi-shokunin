## Gate

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
   `.../trigger/pipeline?token=<token>&ref=<ref_name>`, line 121) and states no
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
