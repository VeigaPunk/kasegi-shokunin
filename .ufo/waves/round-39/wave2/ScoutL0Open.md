# ScoutL0Open — kasegi round 39 wave 2 (falsify): L0 questions + stale-lane scout

Leaf scout; read-only. Did not author any round-39 deliverable. Read at 2026-10-26T20:14Z (17:14 -03). Scratch /fast/scratch/hyaku/kasegi-r39/ScoutL0Open (used for nothing but cwd; removed). No tool installs.

Deliverable: `.ufo/waves/round-39/wave2/ScoutL0Open.l0.txt` (full list + evidence).

## Observed facts
Commands: `grep -n -i kasegi /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (12 lines: 1,10,12,14,16,17,19,20,39,50,101,175 of 178; file is append-only, no answered/RESOLVED marker on any of them), `sed -n Np` of each, `grep -n 'kasegi' .ufo/watchdog.log`, `tail .ufo/state/inline-dispatcher.log`, `git log` (read-only).

Open questions filed by kasegi:
- L1  kasegi | round-12 | ~/Projects/bounties is stalled mid-interactive-rebase (detached HEAD 58acb6d8 ...
- L10 kasegi | round-15 | ~/Projects/bounties — the kasegi PROVINCE root and the anchor of all ~376 SKILL.md path citations — is GONE ...
- L16 kasegi | round-16 | SECOND in-round source loss on a surviving domain root: ~/Projects/origin-work/open-bug-bounties/.ufo-missions/groknight lost 8 mission dirs ...
- L39 kasegi | round-17 | Reconcile the relaunched round namespace and craft dispatch contract before the next launch? ...
- L175 kasegi | round-32 | wave1.ready (37 seats, validated, written 23:14 -03) was cap-deferred by the dispatcher ... Ruling wanted: re-dispatch r32 with a swarm ... or admit the L1-only landing as the round.

Other-lane questions mentioning kasegi: L12 aggregator r9 (CORPUS.md op:// count), L14 kake r15 and L19 kake r16 and L20 kake r17 (corroborate L10/L16, "no new decision requested"), L17 kama r1 (.gitignore omits kama), L50 kotoba r22 (r16adj packets incl. kasegi unacknowledged), L101 kotoba r49 (retire round-1 -L1.md prompts incl. kasegi).

**Round-39 impact: none binding.** The C1/C2 predicates touch only the lane repo, corpus/, `corpus/instruments/r39-closure.sh` over a git-archive export, and the fleet census validator; none reads ~/Projects/bounties or depends on a pending ruling. L175's pattern (spawn-cap / cap-defer) recurred for round 39's falsify wave at 17:13:57 (`spawn-cap ... Background job limit reached (100)`, `cap-defer occupied 89`) and self-healed at 17:14:00 (`spawned kasegi 39 kasegi-r39-falsify 37`); informational only. No open question requires a round-39 decision.

## Stale-lane check
- Round-39 launch: `watchdog.log:1549` `2026-10-26T16:23:01-03:00 launch kasegi round=39 pgid=3965921 driver=hyaku-inline attempt=1`. Age at check (17:14:22 -03) = 3081 s = 51 min 21 s.
- Tick definition: `scripts/shokunin-watchdog.sh` TICK_SECONDS default 450 → two ticks = 900 s. Round 39 is 3.42x that (6.8 ticks) but the live driver is event-driven hyaku-inline (legacy watchdog `tick=` lines end 2026-10-15). It is one respawn-per-round mission making progress (build results done 17:11:04, falsify spawned 17:14:00); no `lane-dead-no-report` for r39. **No other kasegi mission is open** (r38 `complete` 16:14:03; r39 `launch` 16:23:01). `state/kasegi.round=17`/`kasegi.mission` are legacy files from 2026-10-15, not current.
- Fleet-wide launch-without-complete, for context: aggregator r10, audio r1, lore r1, protocol r14 (11.6 days, legacy 2026-10-15 launches); tsukuroi r42 4537 s, tabi r34 3079 s, kama r46 2093 s, tameshi r49 1519 s, kengaku r42 1238 s, mado r46 647 s, kaidoku r41 445 s.

## Side finding (freeze hygiene, not C1/C2 predicate)
`claims.json` `frozen_at_utc` = `2026-10-26T20:30:00Z`, but claims-freeze commit dcd3170 is committer-dated 2026-10-26T16:26:41-03:00 (19:26:41Z) and claims.json mtime 16:26:35 -03 (19:26:35Z); the stamp is ~63 min after the commit and in the future at wave-2 start (now 20:14Z). The commit hash is the authoritative freeze; the timestamp field is wrong. Lane tip at read: 5006097 (receipt Y) over 46c66c2 (J2).

## Unresolved
Whether the Sep-2026 filesystem losses (L10/L16) have any operator ruling lives outside this file; none recorded here. Not round-39-relevant.
