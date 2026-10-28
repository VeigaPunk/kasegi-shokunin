# R44Conn3 — cross-lane overlap scan for F26 candidates

- seat: connector (read-only); item: cross-lane overlap scan for F26 candidates using lane PROVINCE/corpus; report evidence and contested scope.
- axes: `depth:verifiability`, `coverage`. Milestone: falsify C1/C2; no lane writes production/shared files.
- evidence base: lane `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/` — pinned to committed `HEAD 6631401` unless marked `[worktree]` (see §6: the F26 artifacts are **uncommitted** and drifted during the scan). Sibling reads are labeled `[out-of-base corroboration]` and were read-only at the fleet root.

## 1. What the lane's own corpus supplies as F26 candidates

Only one candidate is live this round; the rest of the supply line is recorded rejects and deferred leads. `corpus/SOURCES.md` `## Leads (unopened)` (S:141-147) and the per-row `REJECTED:` cells are the authoritative inventory.

| candidate | supply line | intra-lane overlap | cross-lane overlap | ruling |
|---|---|---|---|---|
| **S069 Google Cloud VRP rules** (`SOURCES.md:75`, capture `corpus/source-snapshots/round-44/S069.txt`, sha256 `0932279c…974f2`) | landed as F26 `[worktree]` `README.md:628`, entry `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`, PROVINCE amendment `PROVINCE.md:167` | F03 disclaims its ground (§2a); F16 shares row *shape* (§2b) | no sibling claims the ground (§3); two citation seams (§4.3, §4.4) | **admissible** — fills a gap F03 explicitly excludes |
| **S070 Google Bug Hunters rules directory** (`SOURCES.md:76`, tier C) | the C2 reject control | — | — | **reject stands**: JS shell / directory welcome, no operative rule; flip recorded |
| **S065 OSV schema** (`SOURCES.md:71`, tier A, rejected) | r42 reject record | F25 CVE-JSON record-format family | **rejected on the cross-lane tie-break itself**: `kaidoku-shokunin` holds an OSV record instance (`SOURCES.md` S015) — precedent that sibling-adjacency is a reject criterion | **reject stands** |
| **S066 NVD API 2.0 schema** (`SOURCES.md:72`, tier A, rejected) | r42 reject record | derived projection of F25's CVE record | — | **reject stands**: primary-of-record fails |
| VEX family S056/S058/S059/S061/S062 (`SOURCES.md:63-68`, all rejected) | r38-r40 rejects | F21 CSAF/VEX, F22 VEX issuance, F23 CycloneDX analysis — saturated | kake holds the security.txt↔CSAF seam only (`lessons/round-38.md:79-83`) | rejects stand; **S059's own flip names the one still-open future candidate**: "a CycloneDX-vs-CSAF frontier entry" |
| `## Leads` | ISO 29147/30111 (already F11), AISI AI-cyber report, Big Sleep tracker | F11 admitted; AISI/Big Sleep fold into F04 | AISI AI-capability ground is kengaku-contested (PROVINCE: `kengaku = LLM evaluation and benchmarks`) | none is a new frontier |

## 2. Intra-lane overlap — where F26 is new and where it duplicates

- **(a) New ground F03 disclaims.** `corpus/knowledge/authorization-safe-harbor-and-scope.md:39`: "These sources do not resolve third-party asset ownership, external legal protection, or whether an unlisted activity is authorized in a particular jurisdiction." The F26 ground — one program's customer-ownership boundary — is exactly the clause F03 excludes.
- **(b) Same row shape as F16.** `README.md:335` (F16, "Chinese crowdsourced-testing platform scope and reward rules") vs `[worktree]` `README.md:628` (F26): both are one platform's scope + reward rules. The new ground is only the **ownership-boundary + reward-ineligibility coupling** (`S069.txt:61-72`). A reader comparing topic cells sees "a second platform ladder"; the row's `next` cell carries the separation ("Keep the Cloud VRP boundary distinct from general authorization, other Google reward programs, and customer permission").
- **(c) F10** (`README.md:211`, vendor policies as corpus objects S036-S040) is vendor-*policy*, not program-*scope-rule*; **F13** (`README.md:264`) is reward *scales*, not eligibility. Adjacent, not duplicative.

## 3. Cross-lane scope ledger — who may hold this ground

`[out-of-base corroboration]` — sibling `PROVINCE.md` clauses, read-only:

- **chousa** `PROVINCE.md:10` — "Refuses: bounty-program scope and claim packages (→ kasegi)". Positive cession to this lane.
- **kake** `PROVINCE.md:290-294` — "Vulnerability handling itself stays out of province: report intake, triage, remediation, disclosure timing, **bounty and policy operation** … are not kake's ground". Positive refusal.
- **kotoba** `PROVINCE.md:65` — "kasegi owns bounty and security research (programs, rules, claim packages …) and states no split with kotoba". Recorded acknowledgement.
- **kengaku** `PROVINCE.md:143` — cedes "bounty-ledger mission-state / dispatcher semantics" to kasegi.
- **revenger** `PROVINCE.md:9-12` + `corpus/training/bounty-triage/MODULE.md:1-5` — bounty triage enters only as an *instruction* module ("fills no coverage-map row, carries no Evidence ID"); artifact-first, excludes "live-target activity … disclosure outside the program channel". Coverage overlap: none by its own declaration.
- Token scan across all `*/corpus` (24 lanes): `bughunters.google.com`, `Cloud VRP`, `Vulnerability Reward Program` → **0 non-kasegi files**. `bug bounty` → revenger(4, the training module), chousa(2, its own gate entries), kotoba(1). `written authorization` → revenger `MODULE.md` only. `Google Cloud` → 15 files (kagi/kake/kama/etc., none a program-rules claim).

## 4. Contested scope — stated, not smoothed

4.1 **C2's own frozen counter cannot report the after-state.** `claims.json:23` counter field: `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md`. Measured: `0` at `HEAD`, `0` on the worktree *with F26 landed* — the `admitted` cell is in column 3, not column 2, so the pattern never matches this row shape. The do-nothing control's pattern `^\| F[0-9]+ \| .* \| admitted \|` measures `25 → 26`. → C2's after-state is **unmeasurable by its own frozen counter**; whichever string is canonical is a contested contract point, and it does not touch C1.

4.2 **Ownership suffix is not an ownership signal — a sibling holds the counterexample.** F26's rule text cites `*.bc.googleusercontent.com` and `*.appspot.com` as customer-owned (`S069.txt:68-69`). `tabi-shokunin/corpus/SOURCES.md:122` (S108) registers `chromiumdash.appspot.com` — a **Google-operated** endpoint — as its own dataset source. So "appspot.com ⇒ customer-owned" is false in-fleet. The staged entry's hedge (`knowledge/google-cloud-vrp-customer-resource-boundary.md`: "the suffix alone is a reason to inspect the program's ownership boundary, not proof that a target is Google-owned") is therefore *required*, not decorative; any tightening of the row's `next` cell would contradict a sibling's first-party record.

4.3 **The `written authorization` token is shared with revenger, different grantor.** `revenger/corpus/training/bounty-triage/MODULE.md:29,56-61` gates on "written authorization, a non-bare policy anchor" and `STOP`s on a third-party component under a different policy (`:61`); `S069.txt:65-67` gates on "written authorization from the customer". Same adversarial invariant — *a third party's permission is not the program's scope* — different object (shipped artifact vs. cloud resource) and different grantor (program/engagement vs. the customer). Citation seam, not absorption; the two lanes should *point at each other's record*, not restate the principle as new.

4.4 **The method seam is chousa's.** The F26 row's `next`-cell "re-open the policy before relying on it" is chousa's claim-vs-source verification method. `corpus/QUALITY.md:8`: "the research method is chousa's — this file duplicates neither." Acceptable as a pointer only; the entry must not teach method.

4.5 **Entry lacks `ground: F26`.** Every recent admission (F11-F25) carries a `ground:` header; the staged entry carries `source:`/`verified-at:`/`recheck:` only. `grep 'ground:' corpus/instruments/*` → no consumer, so this is cosmetic, but the entry↔row binding is currently one-directional (row → entry path only).

4.6 **One entry quote is outside the manifest's pinned set.** `corpus/source-snapshots/round-44/manifest.json` pins Q1-Q3 (anchors 61/62/70); all three verified verbatim in the capture. The entry's quote at `S069.txt:9-11` is **not** manifest-pinned and is not byte-verbatim — the capture reads `any [Google Cloud](https://…)` where the entry renders `any Google Cloud` (inline link markup elided; rendered text matches). `capture-binding-check.py` does not validate quote strings (grep: no `quotes[]` validator; it delegates pin checks to `source-recheck.py`, which reads the manifest's list). Minor: add Q4 to the manifest or mark the elision.

## 5. Checked — *not* defects (reported to prevent false alarms)

- **Backticked entry cell in the F26 row does not break the frontier gate.** `frontier-recheck-count.py:104` `FRONTIER_ROW = …\|\s*`?([^|`]+?)`?\s*\|` strips optional backticks; the captured path resolves under both `root/<entry>` and `root/corpus/<entry>` (`:174-177`). Rule E `missing-entry` would not fire.
- **Expected-entry list already moves with the entry.** `[worktree]` `corpus/instruments/knowledge-expected.txt` non-comment count `63` (was `62` at HEAD, `+1` diff) and names the new entry → `recheck-audit.py`'s expectation is in step.
- **S069 digest binds.** file sha256 `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2` = `manifest.json` `.sha256` = the SOURCES row's anchor cell.
- **Census warnings unchanged.** `W04 S028`, `W04 S029` are pre-existing per `controls/do-nothing.txt`; S069/S070 add no new duplicate-URL row.

## 6. Do-nothing discrimination and live-drift disclosure

- At frozen base `HEAD 6631401`: F26 row `0`, `S069` `0`, entry file absent, `google-cloud` in expected-list `0`; counters `25 / 68 / 62` — matching `controls/do-nothing.txt`. Do-nothing cannot produce the after-state.
- **Drift:** the F26 artifacts are **uncommitted** in the worktree, written `2026-10-28 15:55:21`-`15:57:09` (mtime) *during this scan*: `corpus/source-snapshots/round-44/{S069.txt,manifest.json}`, the entry, `README.md +19`, `SOURCES.md +2` (S069,S070), `PROVINCE.md +2`, `knowledge-expected.txt +1`. Every "[worktree]" claim above is worktree-state, not committed-state. If L1 commits a different row shape, §2 and §4.1-4.2 must be re-measured.

## 7. Limitations

- Sibling reads (PROVINCE files, corpus token scans) are outside the seat's declared "lane PROVINCE/corpus only" base — reported as corroboration for the integrator to re-run, not as the binding record; nothing was written there.
- No live HTTP re-open of S069; I used the committed capture + manifest. The "official article API" provenance is the manifest's own assertion (`capture_url` field), not independently re-fetched.
- Lexical scans can miss a sibling holding the concept under different wording (e.g., a non-English program-rules row). I did not open every sibling corpus in full.
- This lane's recorded overlap precedent (`lessons/round-35.md:187-189` "19 of 20 sibling lanes hold zero hits"; `lessons/round-38.md:79-83` kake security.txt seam; `lessons/round-41-verifier-spotcheck.md:90-103` kake RFC 9116 "reported, not absorbed"; `lessons/round-25.md:93-94` chousa/kake cessions) sets the ruling shape I applied.

## 8. Commands run (read-only)

```bash
# pinned counters — HEAD vs worktree
git show HEAD:corpus/README.md | grep -cE '^\| F[0-9]+ \| .* \| admitted \|'   # => 25
git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  # => 68
git ls-tree -r --name-only HEAD corpus/knowledge | grep -c '\.md$'           # => 62
git show HEAD:corpus/README.md | grep -cE '^\| F[0-9]+ \| admitted \|'       # => 0  (claims.json:23 pattern)
grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md                       # => 0  (worktree, F26 landed)
# candidate inventory — registry ids, statuses, used-by, frontier consumption
python3  # parse SOURCES.md + README.md F rows; consumed-by-frontier = 47 ids; unbound = 24 ids
# cross-lane token scans (fleet root, read-only)
grep -rl --include='*.md' 'bughunters.google.com|Cloud VRP|Vulnerability Reward Program' */corpus  # => 0 non-kasegi
grep -rl --include='*.md' 'googleusercontent' */corpus   # => kake (4 files, crawler verification)
grep -rl --include='*.md' 'appspot' */corpus             # => tabi (4 files, chromiumdash dataset)
grep -nEi 'bount|reward|vulnerab|disclos' */PROVINCE.md  # => chousa:10, kake:290-294, kotoba:65, kengaku:143, revenger:9-12
# binding verification
sha256sum corpus/source-snapshots/round-44/S069.txt      # = manifest.sha256 = SOURCES:75 anchor
grep -nE 'strictly limited to Google-owned|Customer Domains|ineligible' corpus/source-snapshots/round-44/S069.txt  # => 61, 68, 71
awk 'NR>=59&&NR<=87{printf "%d| %s\n",NR,$0}' corpus/source-snapshots/round-44/S069.txt  # entry locators verified
grep -nE '^FRONTIER_ROW' corpus/instruments/frontier-recheck-count.py  # => :104 backtick-tolerant
```

Scratch `$HYAKU_SCRATCH/kasegi-r44/R44Conn3/` created; nothing written to it (no drafts needed); removed on exit. No installs; no pacman; no git/jj/index mutation; no sibling writes; no production edits.
