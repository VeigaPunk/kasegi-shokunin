# Target checkouts + the provenance-pin contract

Verified live 2026-09-28 (read-only census + `provenance.json` scan over all 255
files). How hunt-target source code enters the repo, and how claim packages bind
to it.

## Root-level target checkouts

| Dir | Size | What | Disposition |
|---|---|---|---|
| `pendle-core-v2-public/` | 63 M | shallow clone of `github.com/pendle-finance/pendle-core-v2-public`, single squashed commit `f24265966bb53f75d834ad705decde8e479d3a33` = **v6.10.0**; 274 `.sol` files, 10 top-level dirs, `audits/` (7 classes: LinearDiscountOracle, LpPtoracle, PtLooping, main codebase, marketV6, marketV7, sPendle), `whitepapers/` (5 PDFs: AMM, LP_Oracle, PT+YT, SY, vePENDLE) | live: the cantina-pendle hunt target; untracked+un-ignored in git |
| `george/` | 49 G | comma.ai research dir, zero `claims/` references | parked round 4; revisit only if a claim references it |
| `vgn-bounty-lab/` | ~0 | empty `git init`, zero commits | closed round 4; gitignored (`.gitignore:7`) |

Provenance of the pendle checkout: migrated from the scratch lane workspace —
`claims/cantina-pendle/ingestion-20260915/evidence/hunt-pendle.md` cites the
original path `/scratch/tmp/vgpnk/ufo/bounty-0916/lane7/repos/pendle-core-v2-public`.
The root copy is a convenience mirror; the *binding* lives in the claim package:
`claims/cantina-pendle/ingestion-20260915/provenance.json` → `pin.commit
f24265966bb5…` + `pin.remote` + note "single squashed commit = v6.10.0; shallow
clone". 5 files under `claims/cantina-pendle/` reference the checkout by name.

## The provenance-pin contract (how packages bind target source)

Census over all 255 `claims/*/*/provenance.json`:

- **187 carry a `"pin"` block**; pin-key field frequencies: `tree` ×31, `exit` ×19,
  `cmd` ×18, `repo` ×16, `remote` ×6, `tag` ×4 → three pin families:
  1. **remote-style** `{remote, commit, note}` — named upstream + commit
     (pendle exemplar);
  2. **clone-style** `{action:"sparse clone", repo, commit, tree, sparse}` — 11
     files pin a sparse checkout down to `tree` sha + file list (e.g.
     idos-network `IDOSNodeStaking.sol`, ember-protocol Ember-Vaults-EVM);
  3. **command-style** `{cmd, exit}` — pins the exact command that produced an
     artifact + its exit status.
- 43 files carry `"action"` keys (pin actions and transition actions share the
  field name).
- Transition shape (exemplar `claims/doit-vulnerability-reward-program/amp-http-oauth-redirect/provenance.json`):
  `{id:"T1-scope-snapshot", action:"GET <url> (md + raw html)", exit_status,
  agent:"L1 (direct tool call…)", observed_at:"2026-09-04T22:46:50Z",
  artifact:"evidence/scope-policy-raw.html", sha256:"05c9e439…", negative:[]}` —
  every step binds artifact + sha256 + timestamp + agent identity.

**Gate semantics:** `ops/claim-check.mjs` REQUIRES `provenance.json` (in the
`REQUIRED` six-file list, `:22`) and errors if `steps/transitions/agents` are all
empty (`:96-97`) — but it **never validates `pin`**. Pinning is voluntary
provenance, not an enforced gate: a package can pass claim-check with no target
commit bound. When auditing a web3/smart-contract claim, check `pin` by hand and
re-derive the commit against the upstream remote before trusting line-number
citations (the grok-assessment self-invalidation — frozen `:95-133` citation vs a
file rewritten to 129 lines — is exactly what happens when target state moves and
nothing re-checks).

## Denominator note (round-12 correction)

`claims/` live census 2026-09-28: **274** top-level program dirs (+1 root
`README.md` file), **295** package dirs (`<program>/<slug>`), **280** packages with
`status.json`, 255 with `provenance.json`. Round 1's "275 claim dirs" and round 9's
"295 claim dirs, 15 status-less" were counting program dirs and package dirs
respectively — both numbers are right for their unit; SKILL.md L8 conflated them
(fixed round 12: "274 program dirs / 295 packages (280 gated)").
