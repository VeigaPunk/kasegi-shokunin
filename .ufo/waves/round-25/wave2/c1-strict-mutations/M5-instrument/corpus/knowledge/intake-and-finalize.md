# Board intake & batch finalize — the two mutating sweeps

Source: `~/Projects/bounties/ops/import-board.mjs` (258 lines) and
`ops/finalize-all.mjs` (80 lines), both read in full; verified against
`ledger/imports.jsonl` + `claims/` on 2026-09-28.

These are the only two ops scripts that write outside `ledger/` — one fills
`bounty-map/programs/` from the board, the other tags + pushes accepted
`claims/` packages. Both are fail-closed and both report through telemetry.

## `~/Projects/the-bounty-hunter/ops/import-board.mjs` — evidence-bound one-way feed (P6/P7/AR5/S4)

`node ops/import-board.mjs --from <board-root> [--verify-binding]` — no
`--from` is a usage exit-1. Feeds `~/Projects/origin-work/open-bug-bounties/data/` into [r22 correction: origin-work base absent since 2026-10-12; test -e failed 2026-10-19; historical]
`bounty-map/programs/`.

**Binding phase (before any write).** Three datasets:
`~/Projects/origin-work/open-bug-bounties/data/independent_programs.json` and `~/Projects/origin-work/open-bug-bounties/data/platform_programs.json` expose `.programs[]`; [r22 correction: origin-work base absent since 2026-10-12; test -e failed 2026-10-19; historical]
`~/Projects/origin-work/open-bug-bounties/data/web3_programs.json` exposes `.records[]`. Every check below exits 1, nothing [r22 correction: origin-work base absent since 2026-10-12; test -e failed 2026-10-19; historical]
written:

- `~/Projects/origin-work/open-bug-bounties/data/refresh_evidence.json` needs `run_id` + `evidence_id`. [r22 correction: origin-work base absent since 2026-10-12; test -e failed 2026-10-19; historical]
- Each dataset's byte-sha256 and record count must equal the
  `evidence.datasets[]` entry for its `data/<file>` path.
- Each dataset's `refresh_run_id` must equal the evidence `run_id` — and the
  pairwise check makes all three agree with each other.

`--verify-binding` is the read-only lane: prints the bound evidence/run,
then requires `ledger/imports.jsonl`'s LAST line to carry the same
`evidence_id` (a new board snapshot without a matching import fails —
exit 1). Pass → `binding_verified` telemetry, exit 0.

**Eligibility + freshness (P7).** Record filters differ by dataset — the
independent dataset is the strict one:

| dataset | filter | url field |
|---|---|---|
| independent | `status=active` AND `participation=public` AND `paid_status=confirmed_cash` AND `confidence=high` (all four) | `official_url` |
| platform | none — every record eligible | `url` |
| web3 | none — every record eligible | `program_url` |

Freshness is **per-source, never a global flag**: independent is `live` iff
`independent.source_check.status` matches `/^live_/`; platform/web3 are
`live` iff `source_checks[<platform>].status` matches (live records get
`check.inventory_at_utc` as `as_of`). Non-live → `retainedLabel()`:
`snapshot_retained` if the dataset's as_of ≤ 26 h old, else `stale_snapshot`.
Independent's reward carries only `min/max/currency/source_url/text`.

**Merge-safety (P6) + drift (S4).** Existing `bounty-map/programs/*.json`
indexed before any write. `mission_state` past `DISCOVERED` → **protected**:
file never edited, but its provenance fields (name, source_kind,
official_url, freshness, board_ref, reward) are diffed against the incoming
record — differing fields emit `drift: <id> <fields>` on stdout plus one
`provenance_drift` telemetry line (hunter contract: source change
invalidates downstream states), without failing the import.

Unprotected existing file → provenance fields must agree verbatim
(`JSON.stringify` equality); any mismatch is a **conflict** — report all,
exit 1, zero files written (writes are two-phase: collected, then flushed).
Collisions: canonical URL (`hostname` minus `www.` + `pathname` minus
trailing `/`, lowercased) or sanitized id already claimed → record skipped,
kept-owner printed. New records write `{id, provenance…, ev_inputs:{},
lane:"executor", mission_state:"DISCOVERED"}` — the import lane is always
`executor`, re-laning is a later fleet decision.

Closes with `board_imported` ledger line: `{run_id, evidence_id,
counts{written, live, snapshot_retained, stale_snapshot, collisions,
protected}}`. First import: 1087 written, 258 live, 829 stale_snapshot.

## `~/Projects/the-bounty-hunter/ops/finalize-all.mjs` — end-of-run claim sweep

`node ops/finalize-all.mjs` — idempotent batch equivalent of the
dispatcher finalize path, for when claims landed outside a live dispatch.

Preflight: `gitMutationBlocker` — refuse on active rebase/merge/cherry-pick
or non-main HEAD (exit 1 before touching anything).

For every `claims/<id>/<slug>/status.json` it then:

1. **Filters**: skip `state !== 'DONE'`; skip verdict matching
   `/not.claimable/i` (review-overturned); skip any `disposition` field
   (held/shelved by decree); skip `submission_state === 'DISCLOSED_FREE'`
   (VDP freebies are never claim-ready).
2. **Re-validates**: fresh `~/Projects/the-bounty-hunter/ops/claim-check.mjs` run per package; nonzero exit → [r22 correction: the-bounty-hunter base absent since ~2026-10-12; test -e failed 2026-10-19; historical how-to, not runnable]
   `claim_rejected` telemetry (stdout tail 300 chars), `rejected++`.
3. **Commits**: `git add` the package; if staged diff non-empty →
   `commit -m "claim(<id>): accept <slug>"`; if clean → reuse last commit
   touching the path. No commit containing the bytes → `claim_commit_failed`.
4. **Byte-proofs the tag target**: `git diff --quiet <sha> -- <pkg>` must be
   clean — the tag must point at bytes equal to what's on disk.
5. **Tags**: `claim-ready/<id>/<slug>`. Existing tag on the SAME sha → reuse;
   existing tag on a DIFFERENT sha → `claim_tag_conflict`, rejected, never
   rewrites. New tag is annotated with finalize timestamp.

Then regenerates `docs/claim-ready-index.md` via `~/Projects/the-bounty-hunter/ops/claim-index.mjs`, commits [r22 correction: the-bounty-hunter base absent since ~2026-10-12; test -e failed 2026-10-19; historical how-to, not runnable]
it if changed (`claim_index_commit_failed` on error), re-runs
`gitMutationBlocker` before push (blocked → `finalize_all_push_blocked`,
exit 1), and finishes with ONE `git push --atomic origin main` + all
accepted tag refs + `finalize_all` telemetry `{tagged, rejected,
accepted_tags, push_ok}`.

**Dispatcher's relationship**: fleet-dispatch does this per-package at sweep
time (P20/P21); finalize-all is the catch-up sweep — same gates, same tag
format, same atomic push. Running it while the dispatcher is live is safe:
tag conflicts degrade to telemetry, not corruption.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/ops/import-board.mjs:1-258, ops/finalize-all.mjs:1-80, ledger/imports.jsonl, and claims/ verification.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/intake-and-finalize.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15
