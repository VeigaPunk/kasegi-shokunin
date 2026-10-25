# RevCensusDry — round-29 wave-1 census-gate review

Seat: `RevCensusDry` (reviewer, leaf — no subagent dispatch, no writes outside the lane repo).
Reviewed: 2026-10-25, runs at 18:20:08Z–18:26:00Z UTC. Instrument of record:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet root, read-only; no tool installed or upgraded by this seat; census runs are deterministic shell — no model-dependent judgment, no model identity asserted).
Lane base `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`.

**Verdict: GATE 1 PASS · GATE 2 PASS · GATE 3 PASS** — one LOW finding (gate-1 draft carried a stale `opened` date; corrected and disclosed at landing), residual gaps named below.

## Gate 1 — ExecCensusDry scratch-mirror validation receipt: PASS

Receipt: `.ufo/waves/round-29/wave1/ExecCensusDry.md` (seat `ExecCensusDry-2`, mtime 18:16:58Z — **before** the live append at 18:19:11Z, which is before ScribeSourcesGate's receipt at 18:20:06Z; mtimes stat'ed directly). The receipt pastes `validate --file <scratch>/corpus/SOURCES.md` → exit 0, warnings = pre-existing W04 S028/S029 only, no E03/E04/E11/E12; scratch census rows=45/tier.A=42/mined=33; live frozen census run recorded at its before-state (42 rows, exit 0).

Independent re-execution (my own run on the scratch mirror while it still existed, ~18:20Z, before deletion):

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-29/wave1/ExecCensusDry/corpus/SOURCES.md
scratch_validate_exit=0        # E03|E04 grep over the same output: no hits (grep exit 1)
```

E11 semantics verified in the instrument (`resolve_targets`: in `--file` mode `dir_abs = dirname(file)/..`), so used-by resolves against the mirror tree — the receipt's "knowledge drain = E11's dependency set" claim is accurate, and gate-1 E11 is mirror-relative by construction (the live E11 check is gate 2's).

**Finding LOW-1 (fidelity, not safety):** my `diff live scratch` on the appended rows (captured pre-deletion) shows the scratch block carried staged `opened 2026-10-23` and prose anchors, while the ScribeSourcesGate item mandates `opened 2026-10-25` and capture-derived anchors. The census instrument cannot catch this (E08 only requires a past/present date), so gate 1 proved shape/safety, not date fidelity. Landed rows are correct (`opened=2026-10-25`, capture-pinned anchors — field audit below) and ScribeSourcesGate.md explicitly discloses `2026-10-23 → 2026-10-25`; the ExecCensusDry receipt presents `2026-10-23` as the planned block without flagging the divergence from the scribe item.

## Gate 2 — frozen census command against the LIVE registry after the append: PASS

PRE-STATE labels (bound 6): at review start (~18:0xZ) my grep for `^\|\s*S04[3-5]\s*\|` on live SOURCES.md returned **0 hits** (pre-append), and HEAD `46e07f6` carries the 42-row registry (sha256 `e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d`, 79 lines, zero round-29 Registry-changes bullets — measured from `git show HEAD:`). The append landed in the worktree at 18:19:11Z (rows, then the 4 `## Registry changes` bullets — I observed the intermediate rows-without-bullets state mid-write; final bytes settled below). Freeze baseline: `.ufo/waves/round-29/census-before.txt` (W04 S028/S029, `ok`, exit 0).

Independent re-run of the frozen C2 counter, final state, **18:26:00Z**:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0

$ …/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi   (first 8 lines)
kasegi	rows	45
kasegi	tier.A	42
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	33
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	45
```

Row count `grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|'` → **45** (42+3, matching C2's 42→45). Only the pre-existing W04 S028/S029 appear — no new W04/E-code for any appended URL. Worktree sha256 `fa54ba528eadc032e3cf0cbc6f431e683b2d0d5e7bc1123dd5bb874ac92d1836` — byte-identical to the after-digest in ScribeSourcesGate.md (86 lines = 79 baseline + 3 rows + 4 Registry-changes bullets, bullets present at lines 83–86, `S041/S042 untouched` recorded). The registry edit is uncommitted worktree state (` M corpus/SOURCES.md`); the integration commit is the integrator's.

S043–S045 field audit (awk over the live file): each NF=13, kind docs/docs/dataset, tier A, status mined, `opened=2026-10-25`, `recheck=90d`, used-by byte-exactly `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (match=YES ×3); the entry exists on disk (7,583 B), so E11 is clean.

## Gate 3 — malformed / dup / enum probes over the committed SOURCES.md: PASS (0 hits)

Independent awk probes mirroring the instrument's E-definitions (kind enum `spec|docs|paper|code|tool|dataset|talk|book|community|own-work`, tier `[ABC]`, status `queued|mined|rejected`), run over **both** the 45-row worktree file and the 42-row HEAD blob:

| probe | worktree (45) | HEAD (42) |
|---|---|---|
| E01-like NF≠13 | 0 | 0 |
| E02-like id not `S[0-9]{3,}` | 0 | 0 |
| E03-like duplicate id | 0 | 0 |
| E05/E06/E07-like enum violations | 0 | 0 |
| E10-like community-at-A | 0 | 0 |

rows counted: 45 / 42 — matches the instrument. Instrument self-trust: `sources-census.sh selftest` → exit 0, `96` killed, `0` SURVIVED, `selftest ok` (round-28 recorded 95; the fixture set grew by one since — not a regression, exit 0).

## Findings by severity

1. **LOW — gate-1 draft fidelity gap (no gate bypass).** Scratch append block carried staged `opened 2026-10-23` vs the mandated `2026-10-25`, and prose anchors vs mandated capture-derived anchors. Caught and corrected by the landing seat with explicit disclosure; the dry-run receipt does not flag the divergence. A future census gate that promises "the appended rows match the dry-run block byte-for-byte" would fail today's process — the gate validated shape/safety only.
2. **INFO — scratch evidence deleted post-gate.** `.ufo/waves/round-29/wave1/ExecCensusDry/` no longer exists (R14-economy-consistent). Gate-1 scratch bytes are evidenced by the receipt's pasted output plus this seat's pre-deletion independent re-run (transcript above); they cannot be re-inspected.
3. **INFO — path hygiene:** `.ufo/waves/round-29/wave1/README.md` contains the Bugcrowd VRT README capture text (a capture artifact at a conventional wave-README path), not a wave index.
4. **INFO — mid-write observation:** SOURCES.md was observed in an intermediate state (rows appended, Registry-changes bullets not yet) between 18:19:00–18:19:11Z; final bytes carry the receipt digest, so no integrity issue.

## Residual risk and verification gaps

- Scratch mirror unrecoverable → gate 1 rests on receipt + my single pre-deletion re-run (both exit 0, no E03/E04); ordering is mtime-evidenced, not byte-evidenced.
- Whether ExecCensusDry's projection included the `## Registry changes` bullets is unverifiable post-deletion (its receipt doesn't mention them); the landed bullets match ScribeSourcesGate's claim and are byte-covered by the after-digest.
- The census instrument cannot bind `opened` to the capture date (E08 is past/present only) — the LOW-1 class stays invisible to it by design.
- Out of scope here (other seats/reviewers): capture line-anchor correctness (`anchorcheck` territory), F13 entry Q1–Q10 conformance, frontier row F13, C2's harness/recheck counters. The worktree registry edit is uncommitted; the frozen census must be re-run post-integration-commit before C2's census_exit claim is filed as landed.
