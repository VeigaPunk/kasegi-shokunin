# Source-tree loss 2026-09-28 — PROVINCE root absent; mirror provenance

**Event.** `~/Projects/bounties` — the kasegi PROVINCE root (`./PROVINCE.md:3`),
the anchor of every `~/Projects/bounties/...` citation in `SKILL.md` and all 22
`corpus/knowledge/*.md` entries — is absent from the filesystem as of round 15.
Recorded so the loss is known-deliberate and every citation in this lane carries
a resolvable anchor base from here on. Actor **UNDETERMINED**; data
**PRESUMED-LOST locally** (sentinel forensics, `/tmp/kasegi-r15/sentinel-forensics.md`).

**Round-19 errata (2026-10-14, append-only).** This note's "surviving roots"
— the mirror `~/Projects/the-bounty-hunter` and `~/Projects/origin-work` —
are themselves ABSENT since ~2026-10-12. Everything this file measured about
them stays as the historical record; current status and detection commands:
`corpus/knowledge/root-loss-2026-10-12.md`.

## 1. Detection (all commands re-runnable, all L1-observed this round)

```
$ ls -d ~/Projects/bounties
ls: cannot access '/home/vgpnk/Projects/bounties': No such file or directory
$ find /home/vgpnk -type d \( -name bounties -o -name cantina-pendle -o -name bounty-fleet \)   # 158.6 s, full depth
(no stdout — but the L1 run used 2>/dev/null, which swallowed exactly one
 stderr line; re-run without it: "Error: /home/vgpnk/nc8r6-ExLibRouteCheck/
 .ufo/scopes/tmp-r35-eacces-1488153: Permission denied (os error 13)" — a
 mode-000 dir dated Sep 25, unrelated to this domain. Round-15 correction.)
$ find /home/vgpnk -name missions.jsonl        # full depth
(no output)
$ find /scratch -maxdepth 4 -type d \( -name 'bounties*' -o -name cantina-pendle \)
(no output)
$ ls -d ~/.local/share/Trash ~/.local/share/Trash/files
/home/vgpnk/.local/share/Trash
ls: cannot access '/home/vgpnk/.local/share/Trash/files': No such file or directory
(round-15 correction: §1 of this entry first transcribed the trash check as
 "(empty)". There is no trash store at all — `files/` and `info/` were never
 initialized — which strengthens "not GUI-trashed" rather than weakening it.)
$ grep -E ' /home| /mnt| /media' /proc/mounts
/dev/nvme1n1p2 /home btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home 0 0
```

No separate/unmounted volume, no trash copy, no rename inside `/home/vgpnk`, no
copy on `/scratch`. A `find / -xdev` search is NOT sufficient here: `/home` is a
distinct mount, so `-xdev` from `/` never enters it (L1 method error, corrected
in-round — the full-depth searches above are the ones that count).

## 2. Disappearance window

| Evidence | Value | Source |
|---|---|---|
| last verified live observation of the tree | telemetry appends `freshness_check` 23:32:22.884Z + judge-lane `reroute_drill` 23:32:32.720Z; 7227 lines | `SKILL.md` Cited-paths `ledger/` row (r14 as-of stamp) |
| round-14 close + round-15 launch | `complete kasegi round=14` 20:50:53-03:00; `launch kasegi round=15` 20:50:55-03:00; `launch kumitate round=12` 20:50:58-03:00 | `~/projects/shokunin/.ufo/watchdog.log` |
| parent-dir mtime (the removal event) | `~/Projects` = **2026-09-28 20:51:31.175432381 -0300** (= 23:51:31Z) | `ls -la --time-style=full-iso ~/Projects` |
| ⇒ window | **23:32Z – 23:51:31Z** (19 min); most probable instant 23:51:31Z | derived |
| concurrent activity in the same window | `origin-work/ufo-fsd-alpha` 20:53:17, `origin-work/tmp` 20:53:56, `origin-work/open-bug-bounties/.git` 20:57:10; tmux `ufo_sighting` (4 windows, created 15:24:42, **attached**) hosts a separate live agent session; 6 fleet lanes live per watchdog | sentinel §1-§2 |
| actor verdict | **UNDETERMINED** — no path-specific deletion proof; fleet lanes and the external attached session are both temporally proximate | sentinel §5 |
| recoverability | **PRESUMED-LOST locally**: btrfs subvolume query not permitted for this user, archive scan timed out, the surviving GitHub mirror is code-only | sentinel §5 |

Round-12 already escalated the tree's fragility (stalled interactive rebase since
before 2026-09-11, 903 dirty entries, `george/` 49 G + `.ufo/` 1.5 G untracked
and un-ignored: `corpus/knowledge/repo-git-state.md`, `.ufo/l0-questions.md` kasegi round-12 row).
Whether this loss is that cleanup, an operator reorg, or an accident is an
operator question — appended to `.ufo/l0-questions.md` as the kasegi round-15 row.
Never reverted, never re-created: this lane wrote nothing under `~/Projects`.

## 3. What is gone (18-surface denominator, all corpus-attested as-of 2026-09-28T23:32Z)

`claims/` (274 program dirs / 295 packages, 280 status-gated) · `evidence/` (592
dirs) · `ledger/{missions,telemetry,candidates,imports}.jsonl` (7227 telemetry
lines) · `bounty-map/programs/*.json` (1088 records) · `docs/` (autopsies ×31,
`review-verdicts.jsonl` 486, `claim-ready-index.md`, `wrap-report.md`,
`continuation-notes.md`, `claim-runbook.md`, `RUNBOOK-resume.md`) · `ops/` (live
revisions) · `fleets/` (missions, run, leases, registry, templates,
`ufo-archive-2026/`) · `vdp-disclosures/` · `.ufo/` (25 bh workspaces, 805 M
`bounty-fleet/`, `sessions/`, `grok-bounty-assessment-20260911/`,
`claim-recovery/`) · `.ufo-{ingestion,warden}/` · `.omp/` (live routing) ·
22 `.ufo-mission-report-bh*.md` · `pendle-core-v2-public/` (63 M) · `george/`
(49 G, parked) · `vgn-bounty-lab/` (empty) · `README.md` · `.gitignore` ·
2 root zips · `.git/` (stalled rebase). Coverage denominator at r12: 18 items —
**0 of 18 present after the loss**; the censuses in `corpus/knowledge/` survive
and are the only record.

## 4. What survives — two roots, neither is the lost tree

### 4.1 `~/Projects/the-bounty-hunter` — frozen 2026-09-05 code mirror

`git log`: `37c3668` (A=C 2026-09-05T09:06:07-03:00, "the-bounty-hunter v0.1.0 —
first premium UFO-FSD fleet agent") → `1cfbd86` (A=C 2026-09-05T12:35:36-03:00,
"sync from genesis instance: finalize-all, park-dispatch, claim-index, daybreak:max
peak routing, RR experiment support, periodic sync, H1 GraphQL playbook in
template"; touches only `ops/finalize-all.mjs` +39 and `ops/fleet-dispatch.mjs`
+15/−2). Tag `v0.1.0`, branch `main`, remote
`https://github.com/VeigaPunk/the-bounty-hunter.git`, worktree clean (0 dirty),
**34 files / 8 dirs** (`.omp{,/agents}`, `bin`, `bounty-map`, `docs`, `fleets`,
`ops`). No commit after 2026-09-05 → the mirror is a **frozen Sep-5 state**,
10 days older than the lost tree's last-read state (work through 2026-09-15,
telemetry to 2026-09-28). `bounty-map/` holds **only** `bounty-map/schema.json`;
`bounty-map/programs/` does not exist → 0 records. It is the ONLY copy of these
ops files left on disk: `find /home/vgpnk -maxdepth 8 \( -name ev-report.mjs -o
-name fleet-dispatch.mjs -o -name claim-check.mjs \)` → 3 hits, all under this root.

Provenance per file (re-derive: `sha256sum ~/Projects/the-bounty-hunter/ops/*`;
hashes below are 12-hex prefixes, `wc -l` exact):

**Verdict-column vocabulary (round-15 correction, see §9): "REVISION-IDENTICAL"
in the table below means ANCHOR-COMPATIBLE** — every span the corpus recorded
from the live tree resolves at the same line number in the mirror, with
matching content. Byte identity is *unprovable*: the lost bytes are gone and no
second copy exists anywhere on disk.

| mirror file | lines | sha256 (12) | vs the corpus's live-tree anchors | verdict |
|---|---:|---|---|---|
| `ops/ev-report.mjs` | 92 | `ba5485ed6a5d` | all 14 distinct cited spans resolve at **0 offset** (`:23-26`,`:30-33`,`:38-41`,`:46`,`:47`,`:50`,`:54-58`,`:59-70`,`:73-75`,`:77`,`:78`,`:79-81`,`:82`,`:86-89`,`:91`,`:92`) | **REVISION-IDENTICAL** |
| `bounty-map/schema.json` | 68 | `1a2fd18e9c2d` | `ev_inputs` block = `:32-52` (`additionalProperties:false` `:34`, `p_*` bounds `:36-39`, `expected_reward`…`expected_risk_cost` `:40-45`, `deadline`/`duration_p90`/`submission_buffer` `:46-48`, `as_of` `:49`, `sources` `:50`) — corpus `corpus/knowledge/ev-model.md:37-38` wrote `:32-51`, off by one on the closing brace | **REVISION-IDENTICAL** (corpus cite off-by-one, repaired r15) |
| `ops/rank.mjs` | 249 | `e724186c1330` | `DEFAULTS` `:55-59` (values `:56-58`) exactly as cited; consistency gate `:126-137` pins `github-bug-bounty` `adjusted_ev === 514` at `:136`; artifact `:140-148`; `inputs_basis` `:103`/`:111`; RANKED suppression `:167-186`; `mission_state` advance `:198-203` | **REVISION-IDENTICAL** for the cited anchors |
| `ops/park-disposition.mjs` | 80 | `868057c96cc8` | classifier regexes `:18-21`, PARKED/FAILED filter `:25`, first-match order `:28-32`, dry-run exit `:41`, `mkdir docs/autopsies` `:43`, RETRY telemetry `:46-47` + `rmSync` `:48`, autopsy writer `:53-74`, RETIRED rewrite `:75-77`, `mission_retired` `:78` | **REVISION-IDENTICAL** for the cited anchors |
| `ops/fleet-dispatch.mjs` | 330 (331st line unterminated) | `40f4a5a303dd` | score `:97` has **3 terms** (`curated 1e12` + `reward.min*1000` + `is_live 1`) — the live tree's `:110` had **5** (`priority 9e12`, `continue 2e12` first); repo-wide grep for `priority.json`/`review-verdicts`/`9e12`/`2e12` = 0 hits; `LEASE_MS :43` vs live `:45`; `MAX_ATTEMPTS :44` vs `:46`; `TERMINAL :45` vs `:47`; `attempts() :72-79` vs `:78-85`; `adjusted_ev` read `:152`/logged `:155`/`ev_note` `:156` vs live `:200`/`:204`; `MODEL :32` `qwen3.8-max:xhigh` vs live `deepseek-v4-pro:max`; peak model `:221` `gpt-daybreak-blue-latest:max` vs live `gpt-6-astra:max`; family regex `:192` vs `:271`; `SYNC_PATHS[0] :269` `claims` vs `claims/README.md`; no `GRID`/`formation`; poll `:312` vs `:409`; live file was **427 lines** (`corpus/knowledge/mission-control.md:3`, `corpus/knowledge/triage-thresholds.md:25`) | **EARLIER STATE** (−97 lines, tiers not yet added) |
| `ops/shared.mjs` | 41 | `2497578a44e5` | `BANNED :7`, `PARKED :8` (empty; chatgpt park lifted 2026-09-04), `K3_SEATS :9`, `K3_TOKEN :11`, `TELEMETRY_EVENTS` 8 names `:13-22`, `sha256File :25-31`, `appendLedger` 3500-byte cap `:33`(comment)/`:38`(enforcement), `O_APPEND`/`PIPE_BUF` note `:34` — but **`gitMutationBlocker` absent** (0 hits), which the live tree had and `SKILL.md` cites | **EARLIER STATE** |
| `ops/claim-check.mjs` | 83 | `93679ea1d29b` | `err(` call sites **19** vs the live file's **48**; `symlink`/`lstatSync` 0 hits, `NO_SCOPE_OBJECTION`/`matched_grant_id`/`decision_sha256`/`manifest_sha256`/`claim_review`/`finding_count`/`submission_performed`/`BLOCKED.md`/`schema_version` all **0 hits**; keeps only `SECRET` regex `:66`, 5 MiB skip `:69`, `HARD_STOP` `:56`, artifact-missing `:42`; live file was 233+ lines (`corpus/knowledge/claim-gates.md:3`) | **EARLIER STATE** (much thinner; the entire `status.json` gate family postdates it) |
| `ops/{validate,registry-check,check-freshness,reroute-drill,finalize-all,import-board,claim-index}.mjs` | 130/189/62/70/39/258/49 | `81c7fdea0ce8`/`ada8e678447f`/`63df3bc0eabf`/`51fa772d877b`/`13a5b95da61a`/`29e7aa47252d`/`09d0bb943518` | constants re-anchored this round (validate RFC3339 `:27`, vacuous `PARKED_TOKEN` `:28`, k3 seat check `:63-65`, `--strict ev_inputs` `:120-121`; registry-check grok-`:low` pin `:34-43`, bijection `:57-80`, bucket hygiene `:117-122`; check-freshness `THRESHOLD_H = 26` `:15`, default board `:14`, telemetry append `:61`, exit `:59`; reroute-drill `/^park:(.+)$/` `:20`, `simulated:true` `:63-69`) | usable, per-anchor verification required |
| `fleets/{mission-template.md,registry.json}` | — | `0d4ff5944c4f`/`173921b1806f` | template carries the six-file contract + `I8` + the report.md field list (`:50` incl. "disclosure timeline"); registry present | usable |
| **VDP surface** | 0 | — | `grep -rniE 'vdp\|disclos\|no.?payout\|disclosed_free'` over the whole mirror (excl `.git`) hits only `[lost-base] fleets/mission-template.md:50`, `docs/genesis-plan.md:15,17`, `.omp/agents/scope-evidence-custodian.md:83,104,118,129,139`, `[lost-base] ~/Projects/the-bounty-hunter/.omp/agents/the-bounty-hunter.md:28` — **zero hits in any `ops/*.mjs`**, no `vdp-disclosures/` dir | **NOT IN MIRROR** |

Direction of divergence is one-way: where the mirror differs it is *missing*
what the live tree had (tiers, blocker, gate families, GRID) — never the reverse
— except the model-routing strings, which the Sep-5 sync commit names explicitly
("daybreak:max peak routing") and the live tree later replaced. Treat the mirror
as **the 2026-09-05 ancestor state of the lost tree's ops code**, not a fork and
not a substitute for it.

### 4.2 `~/Projects/origin-work/open-bug-bounties` — the origin-work claim corpus

Pre-existing and already partially documented (`corpus/knowledge/submitted-registry.md`: the real
receipt store). Inventory re-taken this round: `~/Projects/origin-work/open-bug-bounties/claim-packages/` = **26 package
dirs + 3 files** (`~/Projects/origin-work/open-bug-bounties/claim-packages/README.md`, `~/Projects/origin-work/open-bug-bounties/claim-packages/CONNECTOR.md`, `~/Projects/origin-work/open-bug-bounties/claim-packages/_schema.json`), **0 `status.json`**
anywhere under it (this corpus predates the six-file/`status.json` contract),
`~/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/` = receipts + `claims/` **21 entries**,
`.ufo-missions/` **43 entries**, `~/Projects/origin-work/open-bug-bounties/data/` 5 inventories
(`~/Projects/origin-work/open-bug-bounties/data/independent_programs.json` 34 811 B, `~/Projects/origin-work/open-bug-bounties/data/platform_programs.json` 218 131 B,
`~/Projects/origin-work/open-bug-bounties/data/web3_programs.json` 78 770 B, `~/Projects/origin-work/open-bug-bounties/data/refresh_evidence.json` 24 047 B, `programs.ts`),
git HEAD `1307b8b`. `[lost-base] ops/check-freshness.mjs:14` in the mirror defaults its board to
exactly this path — the two surviving roots are wired together by the ops code.
**Not censused** (top-level inventory only) → the round-16 coverage move.

## 5. Anchor-base rule (binding for this lane from round 15)

1. A citation is only as good as its named base. Every `path:line` in this lane
   now states or implies one of: **(a) mirror** `~/Projects/the-bounty-hunter`
   HEAD `1cfbd86` (frozen 2026-09-05) — live-checkable; **(b) lost tree**
   `~/Projects/bounties` as-of 2026-09-28T23:32Z — corpus-attested only;
   **(c) origin-work** `~/Projects/origin-work/open-bug-bounties`; **(d) lane
   repo** (`SKILL.md`, `corpus/...`) — pin the git blob when citing line numbers
   of a file this lane keeps editing (see §6).
2. Never substitute a mirror line number for a lost-tree line number silently.
   Where both are known, cite both and label each (`Triage economics` in
   `SKILL.md` does this for `ops/fleet-dispatch.mjs`).
3. Facts whose only source was the DATA half can never be re-verified; they
   carry `[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]`.
4. Semantics that the mirror can still execute are **runnable-verified**, which
   is stronger than a line cite: r15 smoke-ran a byte-identical copy of the
   mirror `ops/ev-report.mjs` (`/tmp/kasegi-r15/ev-smoke`, copy sha256 == mirror
   sha256) and reproduced every branch — no-arg → exit 2; missing file → exit 2;
   unparseable → `WARNING` + all-10 `UNKNOWN` + exit 0; missing `p_accepted` →
   `total_cost` still computed, `adjusted_ev` UNKNOWN, verdict `unknown`, exit 0;
   JSON string `"0.5"` rejected per key while numeric `0.5` kept; `adjusted_ev`
   exactly 0 → `positive_adjusted_ev: false` (strict `> 0`); and the round-13
   github-bug-bounty record 0.9/0.8/0.35/0.7 + reward 10000 + cost 1250 →
   `p_success 0.1764 / gross_value 1764 / total_cost 1250 / adjusted_ev 514 /
   true` — the same 514 the mirror's own gate hard-pins at `rank.mjs:136`.

## 6. Live citation-resolvability — the new depth instrument

`/tmp/kasegi-r15/resolve.py` (stdlib-only, deterministic; run twice → byte-identical
output, md5 `ab25833e897822af3e87b371a3d4eeff`; token set cross-checked against an
independent `grep -oP | sort -u` pipeline, 1107 == 1107, diff empty; third-checked
by the labrat's own importer, same 289/381 for `SKILL.md`):

| scope | distinct path-like citations | resolvable now | rate |
|---|---:|---:|---|
| `SKILL.md` | 289 (381 instances) | 47 | **16.26 %** |
| `corpus/**` (43 files) | 971 | 129 | **13.29 %** |
| lane total | **1107** (2175 occurrences) | 156 | **14.09 %** |
| lane total, noise-adjusted (246 extraction-rule artifacts excluded: regex/shell/git-porcelain/synthetic) | 840 | 136 | **16.19 %** |

Classes: `RESOLVES` 24 · `MIRROR-EQUIVALENT` 52 (18 written as
`~/Projects/bounties/...`, 34 bounty-root-relative bare paths) · `INTERNAL` 80 ·
`GONE` **951**, of which **704 are genuine vanished paths** and 246 are
rule artifacts. Strict-reading variant (mirror name-survival NOT counted as
resolvable): 44/289 = 15.22 % SKILL, 112/971 = 11.53 % corpus, 137/1107 = 12.38 %
lane. **Name survival is not content survival**: of 53 resolvable line-anchored
citations, 51 are in range and 2 are past the mirror's EOF
(`[lost-tree] ops/claim-check.mjs:174-199` cited by `corpus/knowledge/submitted-registry.md:105` against an
83-line file; `[lost-tree] ops/shared.mjs:55` cited by `corpus/lessons/round-4-aggregator-audit.md:26`
against 41 lines) — both are mirror-backed name matches with lost content.
Compare r13/r14: 705/708 = 99.6 % of counted SKILL citations resolved. The proxy
did not change; the filesystem did.

Same defect class inside the lane: `corpus/knowledge/triage-thresholds.md` carries
32 `SKILL.md:NNN` cites (23 unique spans) pinned to blob **`fc6d398`** (round-12
commit, 546 lines) — verified 8/8 sampled spans (`:498-502` = the formula block,
`:175-176` = the four-term queue score, `:113-114` = `buildQueue` ordering,
`:117` = `attempts()≥2`, `:90-91` = `NO_SCOPE_OBJECTION`, `:522`/`:526` =
cited-path rows, `:10-11` = the 1088/486 preamble). Resolve with
`git show fc6d398:SKILL.md | sed -n 'NNNp'`; the pin is now stated in that file's
header (round-15 repair; the hazard was already named in
`corpus/lessons/round-5-aggregator-mirror-ambiguous-citation-base.md`).

## 7. Facts that can never be re-verified (DATA half)

1088 program records and every count derived from them (0 `adjusted_ev`, 0/1088
`sources[].basis`, `reward.min` on 14, freshness `{stale_snapshot:830, live:258}`,
score bands 796/228/64) · 280 status-gated claim packages + the D1-D13 deviation
census (260/280 deviate) · 592 `evidence/` dirs · 7227 telemetry lines and the
state-machine transition counts (LEARNED 244, PLANNED 219, SCOPED 232, SUBMITTED 3)
· 486 `review-verdicts.jsonl` lines (`leave 430 / continue 50 / drop 6`) · 31
autopsies and their partition (auth-walled SPA ×27, SIX ×1, Airtable ×1, paused ×2)
· the 85-mission REVIEW cohort (529 LEARNED / 85 REVIEW / 30 RETIRE_AUTH / 2 RETRY)
· 25 `.ufo/bh*` workspaces + 121 reroute records + the 805 M keeper tree · 187/255
provenance pins · the live `docs/claim-ready-index.md` 11-vs-12 row split · the
`.git` stalled-rebase state (903 dirty entries, 12 pushed tags). Each stays in the
corpus with its as-of stamp; none is re-derivable, and no lane output should
present them as live again without a restored tree.

## 8. Consequential repairs landed this round (round-15 corrections)

- `SKILL.md` `## Retirement lane`: "fixed five-part `docs/autopsies/<id>.md`"
  **falsified** — the writer at mirror `[lost-base] ops/park-disposition.mjs:53-74` emits
  **seven** labelled parts (4 bold metadata lines `:56-59` + 3 `##` sections
  `:61`,`:67`,`:72`) and `SKILL.md` itself listed seven while calling them five.
  `corpus/knowledge/retirement-autopsies.md:38` heading "five fixed parts"
  repaired the same way.
- `corpus/knowledge/ev-model.md:37-38` `[lost-base] bounty-map/schema.json:32-51` → `:32-52` (block closes
  one line later; the properties body `:35-51` was already right).
- `corpus/knowledge/triage-thresholds.md` SKILL-cite anchor base pinned to blob `fc6d398` (§6).
- `SKILL.md` `## Triage economics` re-anchored to the mirror with per-constant
  cites + dual-base citing for `ops/fleet-dispatch.mjs`; `## Ops integrity layer`,
  `## VDP disclosure packages`, `## Retirement lane` re-anchored/stamped likewise.

## 9. Round-15 verification corrections (L2 falsifications L1 accepted)

Nine independent L2 audits ran against this event (critic, sentinel, revenger,
3 scouts, reviewer, connector, labrat, mutation-tester, simplifier, distiller,
2 executors; reports in `/tmp/kasegi-r15/`). What they changed:

- **"REVISION-IDENTICAL" is unprovable and was overstated.** The lost bytes are
  gone, so a 0-offset anchor match proves *anchor compatibility*, not identity.
  §4.1's verdicts now read ANCHOR-COMPATIBLE. Two supporting details: r13
  recorded the missing-argument exit at `[lost-base] ops/ev-report.mjs:25` while the branch is
  `:23-26` (stale-by-one, immaterial); and the mirror's own header comment
  `[lost-base] ops/ev-report.mjs:16` says only "exit 2 if the program file is missing"
  while the code also exits 2 on a missing argument (`:23-26`) — a
  source-internal inconsistency, not a corpus defect.
- **Mirror git forensics** (revenger): `.git` crtime 2026-09-05T09:01:51-03:00;
  reflog holds only the two commits (no clone/fetch entry); 0 packs, 48 loose
  objects; `git fsck` clean; `main == origin/main == 1cfbd86`; tag `v0.1.0`.
  The local repo is therefore the **origin** of the GitHub remote, not a clone.
  9 of 10 sampled `ops/*.mjs` are byte-identical to the initial commit
  `37c3668` (A=C 2026-09-05T09:06:07-03:00); only `ops/finalize-all.mjs` (new) and
  `ops/fleet-dispatch.mjs` (modified) changed in `1cfbd86`, whose message overstates
  its own delta. So the mirror's ops state is the 09:06:07 snapshot for those 9.
- **No second copy exists**: `git cat-file -e` fails for all 6 lost-path probes
  against `1cfbd86`; a filesystem-wide sweep for the six ops filenames found
  only the mirror (plus one unrelated monaco-editor `shared.mjs`, different
  sha/size). The live tree's newer revisions survive **only as corpus
  quotations** — which is exactly what a corpus is for, and why §5's stamping
  rule is binding.
- **Fourth divergence marker**: `corpus/lessons/round-4-aggregator-audit.md:28`
  records 14 `ops/*.mjs` tools; the mirror has 13.
- **Actor forensics closed as far as this user can**: both casings, the
  40-entry `~/Projects` listing, `/scratch`, a full-root name sweep, the
  rename-window sweep, `docker inspect` on all 31 containers, and 72
  deleted-but-still-open fds — no trace. btrfs enumeration is **not permitted**
  for this user (`Operation not permitted` on `/` and `/home`) and `/.snapshots`
  is root-only: that is the single honest blind spot in the GONE verdict. The
  "house-tidy swarm" hypothesis is **killed** —
  `~/.ufo/house-tidy-round0-plan.md` lists this scope read-only but zero
  execution artifacts exist (no baseline, no `audit-reports/`, no
  `house-tidy-trash-*`), so the plan never ran. Verdict stays UNDETERMINED.
- **New invariant defect, mirror-verified** (L1 grep): `TELEMETRY_EVENTS`
  (`[lost-base] ops/shared.mjs:13-22`, 8 names) is imported by **nothing** —
  `grep -rn TELEMETRY_EVENTS --include='*.mjs' --include='*.sh'` over the
  mirror returns only the declaration, and `appendLedger`
  (`[lost-base] ops/shared.mjs:36-41`) never checks the event name. The ops scripts append
  **17** distinct `event:` values; 4 of the 17 are whitelisted, and 4
  whitelisted names (`lane_parked`, `lane_degraded`, `operator_decree`,
  `xask_dry`) are appended by no ops script. Decorative whitelist — same class
  as the decorative bounty map. Full derivation now lives in `SKILL.md`
  `## Ops integrity layer`; canonical home should move to
  `corpus/knowledge/ops-invariants.md` (round-16 task).
- **Do-not-run hazard**: all 11 mirror ops scripts derive their write root from
  their own location (`const root = join(dirname(fileURLToPath(import.meta.url)), '..')`),
  so running one in place would create and mutate `ledger/`, `fleets/run/`,
  `docs/autopsies/`, `evidence/`, `bounty-map/programs/` inside a read-only
  product repo; the mirror has no `ledger/`, so the first `appendLedger` would
  throw ENOENT [INFERENCE — derived, never executed]. r15 smoke-ran only
  `ops/ev-report.mjs` (side-effect-free, `[lost-base] ops/ev-report.mjs:17`) and only from a
  byte-identical copy outside the mirror.
- **Citation inventory scale** (critic): 21 `corpus/knowledge/*.md` files carry
  **765** lost-tree `path:line` citations. Only `corpus/knowledge/triage-thresholds.md` received
  an explicit anchor-base pin this round (§6); pinning the other 20 is the
  round-16 move. Two corpus cites are past the mirror's EOF —
  `corpus/knowledge/submitted-registry.md:105` (`[lost-tree] ops/claim-check.mjs:174-199` vs 83 lines,
  annotated this round) and `corpus/lessons/round-4-aggregator-audit.md:26`
  (`[lost-tree] ops/shared.mjs:55` vs 41 lines, left as history). `SKILL.md`'s two
  `[lost-base] ops/claim-index.mjs:4` cites ("tags are provenance only") are unsupported by
  the mirror — the string is absent from its `ops/claim-index.mjs` — and are now
  marked `[lost-tree]`.
- **Cross-lane blast radius** (connector): 339 `Projects/bounties` references
  across the 8 lane repos + main repo (221 path-shaped, 133 inside
  `corpus/knowledge/`); no sibling lane and no main-repo doc had recorded the
  disappearance, and 4 lanes wrote files after 23:51Z without mentioning it.
  Scope ruling requested, not absorbed: `the-bounty-hunter` is **mixed** —
  kasegi owns the bounty EV/claim/policy semantics, kumitate the
  orchestration/tooling surface, protocol/integrator arbitrates the repo-level
  split (consistent with the r10 `fleets/registry.json` ruling). Its remote
  `VeigaPunk/the-bounty-hunter` is outside the lane push allow-list
  (`../MISSION.md:49-56`); this lane pushed nothing there.

## 10. Round-15 measurements (both instruments, before → after)

| instrument | before r15 | after r15 |
|---|---|---|
| `density.py` file mean over `SKILL.md` (18 blocks) | 142.5 | **152.9** |
| `density.py` path-citation instances | 376 | **623** |
| block: Triage economics | 93.3 | **131.4** |
| block: Ops integrity layer | 61.1 | **111.5** |
| block: VDP disclosure packages | 81.8 | **117.4** |
| block: Retirement lane | 62.5 | **93.0** |
| `resolve.py` SKILL.md resolvability | 47/289 = 16.26 % | **222/486 = 45.68 %** |
| `resolve.py` corpus resolvability | 129/971 = 13.29 % | **396/1297 = 30.53 %** |
| `resolve.py` lane total | 156/1107 = 14.09 % | **410/1437 = 28.53 %** |
| `anchorcheck.py` over `SKILL.md` | n/a | 194 in-range mirror cite instances, **0 past-EOF**; 47 MISSING-FILE are the expected lost-tree and package-relative anchors (`docs/*`, `claims/*`, `status.json`, `INGESTION.md`, `fleets/*`), which the mirror never contained |

Measured at round-15 close from the committed tree, re-runnable with
`python3 corpus/instruments/resolve.py <lane-repo>` and
`python3 corpus/instruments/density.py SKILL.md`. Two fixed-point caveats, both
disclosed rather than hidden: the SKILL `## Cited paths` header quotes the
resolvability rate and is itself inside the measured file (±1 token), and these
corpus files cite each other, so every recording pass moves the rate by < 0.1 pp
— the committed census file is authoritative and the chase stops there. The
corpus rate jumped far more than the SKILL rate (13.29 % → 30.53 %) because this
entry, `corpus/lessons/round-15.md` and `corpus/instruments/README.md` are new,
mirror-anchored files — new resolvable citations, not repaired old ones.

The frozen bar `BAR_R15 = 142.5` was **not** cleared by any of the four
repaired blocks in prose form, and the lane records that instead of reformatting
to pass: the r15 labrat measured the identical old Triage content at 100.0 as
prose vs 150.0 as a single-line-row table, i.e. the bar is reachable by
reformatting alone, so clearing it is not evidence of knowledge. Bar rule
amended (frozen constant + conjunctive ≥ 60 % resolvability gate) in
`corpus/instruments/README.md` and `SCORECARD.md`.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/PROVINCE.md:3 and the 2026-09-28 source-tree census; lane round-15 loss record with round-19 absence errata.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --selftest
