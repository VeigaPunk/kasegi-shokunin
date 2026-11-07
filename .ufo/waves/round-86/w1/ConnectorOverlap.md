# ConnectorOverlap — round 86, wave 1 (kasegi)

- seat: ConnectorOverlap (leaf; no subagents, no background jobs); date 2026-11-06
- lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin; base d7296645c2cd9f631329fa8e2f38328a4c9c89a5; freeze 252df0c90c066d83d229e3107811a6bc05e8feed
- scratch: /fast/scratch/hyaku/kasegi-r86/ConnectorOverlap (deleted before yield; TMPDIR passed explicitly)
- writes: this file + ConnectorOverlap-receipts/ (index in its README.md). Everything else read-only.
- no S<digits>.txt was copied anywhere; snapshots are cited by path and sha256.

## 1. Sibling-overlap scan — clean

20 sibling lane repos (`/home/vgpnk/Projects/shokunin/*-shokunin/corpus/`) grepped for `1997312`,
`Internet Bug Bounty`, `hackerone.com/ibb`, `daniel.haxx.se/blog/2026/01/26`, plus `CVE-2023-28319`,
`hackerone.com/reports`, `curl.se/docs/CVE`, `libssh`.

- **No sibling holds C2's subject or sources.** The only `1997312` hits are a binary run log
  (`audio-shokunin/.../bp/drain_quit/stdout.bin`) and a numeric CSV field
  (`kengaku-shokunin/.../bn_sample_10k.csv`); `libssh` hits are audio strace text. Zero hits for the
  four named tokens as sources, zero for the CVE, zero for any `hackerone.com/reports` URL.
- **No reusable knowledge-scope instrument to collide with:** `corpus/instruments/` and
  `corpus/instruments/resolve.py` exist only in kasegi (1 dir, 1 file); no `knowledge-meter*` or
  `*repair-map*` elsewhere.
- Nearest *patterns* (shape only, not code): lore r101 `V03-c1-repointed` (stale fixture red /
  repointed fixture green through the same frozen replayer, run twice, plus only-delta) and kotodama
  r26 `pin-repoint-check.py` (same paired-control shape). C1's M1 do-nothing control is the same
  family, so C1 is not inventing a new verification convention.
- Each lane owns its own `S###` namespace, so there is no cross-lane id space. C2 has no collision.

## 2. Assimilation id-collision (A = receipts/assimilation)

Mandated pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}` on `corpus/SOURCES.md` vs
`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`:

```
reg=123  staged=94  collisions=93  (comm -12; staged-only = S124; reg-only = S001..S030)
```

**The 93 collisions are not duplicates: 0 of 93 rows are identical and all 93 hold a different
source.** The staged file is a pre-expansion snapshot — its own `MERGE-REPORT.md` says "lane registry
currently holds **30** rows; first staged id is **S031**" — and the lane's later expansion put
different sources at S031..S123 (e.g. lane S031 = CVE CNA Rules v4.2.6; staged S031 = HackerOne
policy versions; lane S123 = the curl bug-bounty post; staged S123 = NIST SP 800-115). The staged
S120 row is malformed (`fields=12`).

Union dry-run through the **existing** fleet census (scratch root, no lane write; 94 staged rows
inserted inside `## Registry`): rc 1 with **E03 92** duplicate ids, **E01 1**, **E09 43**, **E04 4**,
**W01 3** — control (same root, unmodified registry) has **none** of those. Adversarial placement:
appending the same rows after the registry section yields `E12 x94` and `E03 0`, i.e. the duplicate-id
check does not see out-of-section rows.

Guard proof: a scratch registry with an indented `  | S002 |` row gives `S002` under the mandated
pattern and **empty** collisions under a naive `^\|` pattern — a collision counter built on the naive
pattern silently returns "no collisions" on a poisoned package.

Fleet-wide (`receipts/fleet-merge-collision.tsv`): 21 lanes have a staged append; **every lane's
common rows all differ (0 identical anywhere)** — chousa 114/114, kotodama 132/132, mori 136/136,
revenger 155/155, tsukuroi 147/147, kengaku 167/167, kasegi 93/93 — and five queues have zero free
ids (chousa, kotodama, mori, revenger, tsukuroi). kama's registry moved 337 → 339 during this scan
(its round-92 is live): the target id space is a moving surface.

**Hazard (re-runnable).** A merge is caught only *after* the bytes land (census E03, and C2's P4 row
count 123 would fail then, not before). Nothing in round 86's frozen predicates inspects the queue.
C1 makes it concrete: 10 of its 15 repointed basenames (S071, S073, S075, S076, S078, S089, S090,
S103, S105, S106 — **198 of the 203 keys**) sit inside the colliding `S031..S123` range, so a blind
merge would give those ids a second meaning while `corpus/knowledge` still cites `S071.txt:117` etc.;
the queue's only free id, S124, is already assigned to GB/T 28458-2020. Reproduce with:

```
S=/fast/scratch/hyaku/kasegi-r86/<seat>/dryrun; R=$S/root
mkdir -p $R/kasegi-shokunin/corpus; cp <lane>/corpus/SOURCES.md $R/kasegi-shokunin/corpus/
cp /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md $S/staged.md
# insert the 94 staged rows inside ## Registry (line 136), copy the fleet shokunin.conf to $R
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $R $R/kasegi-shokunin
# rc 1; E03 92, E01 1 (S120 fields=12), E09 43, E04 4
```

This is reported as collision risk, not as the round's move: it protects the registry substrate, not
the axis reading.

## 3. considerthese — pointer

Eight files, `2026-10-19.md` .. `2026-10-26.md` (daily bot reflections). Implemented already:
`2026-10-26.md` §2 (public disclosed report → six-file package → price) is exactly r85/r86 C2;
`2026-10-21.md` §"run the knowledge scope read-only against the committed tree" is C1's scope.
Still unimplemented and adjacent to depth:verifiability: `2026-10-19.md` proposal 1 — a
`corpus/instruments/test_anchorcheck.py` regression test for the `94aace2` prefix-resolution fix
(confirmed ABSENT on disk). It is a fail-before fixture for a *different* instrument (anchorcheck),
so it is a next-round candidate, not a C1/C2 slot. `2026-10-22.md`'s "stale source IDs in the corpus
index" is the observation C1 now partly addresses.

## 4. Proposal — one bounded move: make C1's measuring root a machine-checked operand

**Evidence.** The 203-key map is constructively reproducible from the frozen builder at base
(byte-identical `dd40455a…`, excluded `920641e6…`, 89 tokens; two runs identical; 0.44 s, 27 MB) and
root-invariant: in a fleet-root-like parent (`MISSION.md` beside the clone) the rebuilt map is the
same bytes, **0 of 406 key/value classifications flip**, and the excluded set is identical. But the
score itself is root-bound by exactly one token: base `398/1721` vs `399/1721`, after `596/1716` vs
`597/1716`, and only `../MISSION.md:49-56` flips (GONE → INTERNAL). So the published counting command
run with the lane in a fleet-root-like parent prints `after=597/1716`, `LIMB M1 FAIL`, rc 1 — a
silent red that is indistinguishable from a bad landing unless the verifier reads the parent clause
in P1. The counter prints `mirror_absent` but not the root class.

**Move (depth:verifiability; no other axis touched).** Freeze a `W` limb family in
`knowledge-meter.py` at the next freeze; pin **deltas**, not absolutes, so it survives a base change:

- **W1 class** — derive `root_class = present` iff `os.path.dirname(lane)/MISSION.md` exists, print
  `root_class=` on the `KNOWLEDGE-METER` line, and fail when `--expect-root` names a different class.
- **W2 delta** — with `--root-pair <clone-in-fleet-root-like-parent>`: the builder at `--base-rev`
  inside that root yields byte-identical map and excluded files; the base and after rates each differ
  by exactly +1 non-GONE and 0 denominator (at this base: 398/1721→399/1721, 596/1716→597/1716);
  M2–M6 pass in both roots; the classification flip set over all keys + values + both token sets is
  exactly `{'../MISSION.md:49-56'}`.
- **W3 no-op** — the limb reads only; with it unrequested the printed rates and M1–M6 are unchanged,
  so no landing can gain score through W and this round's frozen target cannot be moved by it.

**Controls (executed now, receipts/root-witness.txt).** both roots measured; map sha equal across
roots; 0/406 flips; the one flip is the named token; scratch-parent run reproduces the frozen
`398/1721` / `596/1716`, fleet-root-like run gives `399/1721` / `597/1716` with M2–M6 pass.

**Why this and not a map-provenance limb.** M1+M2+M3+M4 already force the map: every removed token
must be a key, every added token a value, every changed line a key substitution, every key GONE with
a unique in-range basename — so a provenance limb would re-derive a forced object. The root class is
the one assumption the counter cannot see and the claim states only in prose.

**Risks.** (a) Marker-name inference can miss a differently-named fleet root — W2's flip-set check,
not W1, is the real guard. (b) A future base with different relative tokens needs a re-frozen flip
set. (c) Adding a limb changes the counter bytes, so P2 must be re-frozen at that freezes — not now.
(d) Cost: one builder run (0.44 s) + two meter runs (1.5 s, 1.2 s) at this scope; no lane census.

**Verification (re-runnable against today's frozen bytes):**

```
S=/fast/scratch/hyaku/kasegi-r86/<seat>/rootw; mkdir -p $S/fleetroot
cp /home/vgpnk/Projects/shokunin/MISSION.md $S/fleetroot/MISSION.md
git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin $S/fleetroot/kasegi-r86-land
cd <lane>
python3 -B .ufo/waves/round-86/c1/knowledge-meter.py --lane $S/fleetroot/kasegi-r86-land \
  --measure-rev d7296645c2cd9f631329fa8e2f38328a4c9c89a5          # 399/1721
python3 -B .ufo/waves/round-86/c1/build-map.py --lane $S/fleetroot/kasegi-r86-land \
  --rev d7296645c2cd9f631329fa8e2f38328a4c9c89a5 --out $S/fm.json --excluded $S/fe.json --work $S/w
sha256sum $S/fm.json                                             # dd40455a...
python3 -B .ufo/waves/round-86/c1/apply-map.py --root $S/fleetroot/kasegi-r86-land \
  --map .ufo/waves/round-86/c1/repair-map.json                   # APPLY files_changed=14 keys=203
python3 -B .ufo/waves/round-86/c1/knowledge-meter.py --lane $S/fleetroot/kasegi-r86-land \
  --base-rev d7296645c2cd9f631329fa8e2f38328a4c9c89a5 --map .ufo/waves/round-86/c1/repair-map.json \
  --target 596/1716 --map-sha256 dd40455a379eb53b75bf5a15772fe675efae79eda2516ea7fac50f86420bce12
# 597/1716, M1 FAIL, M2-M6 pass
```

## 5. Contradictions stated plainly

1. The merge queue declares 94 accepted rows continuing the lane's S-space from a 30-row registry;
   the live registry has 123 rows and 0 of the 93 shared ids are identical. The queue is not
   replayable, and the round's predicates do not look at it.
2. C1's root dependence is real, measured, and exactly one token — but it lives in `host_note` prose,
   while the counter prints only `mirror_absent`. The same published command yields rc 1 in a
   fleet-root-like parent; the failure is silent about its cause.

## 6. Limits of this report

No landing exists, so the official counting command was not run at a landing; no full `resolve.py`
lane census was run (forbidden, ~6 min/13 GB); the fleet numbers are a snapshot (kama moved during
the scan); the union census dry-run holds only `SOURCES.md` in its scratch root, so absolute E11
counts are inflated in both union and control — the delta is the signal.

## 7. Files written

- `.ufo/waves/round-86/w1/ConnectorOverlap.md` (this file)
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/README.md`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/sibling-scan.txt`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/kasegi-merge-detail.txt`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/fleet-merge-collision.tsv`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/root-witness.txt`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/union-validate-inside.txt`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/union-validate-control.txt`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/union-append-at-eof.txt`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/rebuilt-map.json`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/rebuilt-excl.json`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/assimilation/{reg.ids,staged.ids,collisions.txt}`
- `.ufo/waves/round-86/w1/ConnectorOverlap-receipts/assimilation/guard/{registry-guard.md,guard-reg.ids,guard-lane.ids,guard-collisions.txt}`
