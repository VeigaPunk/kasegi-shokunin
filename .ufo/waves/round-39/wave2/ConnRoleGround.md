# ConnRoleGround — round 39 wave 2 (falsify) receipt

Seat: ConnRoleGround (connector, leaf; no subagents spawned)
Item: route-map verification + seat-model report stub
Axes judged: depth:verifiability, coverage
Deliverable: .ufo/waves/round-39/wave2/ConnRoleGround.routing.txt (written)
Run window: 2026-10-26T20:15Z – 20:18Z

## What I verified (commands run, actual output)

1. Read frozen claims and erratum first: `.ufo/waves/round-39/claims.json` and
   `claims-erratum-1.md` (read-only; not edited).

2. Read `/home/vgpnk/.omp/agent/config.yml` task.agentModelOverrides (lines 350-368)
   with grep. Observed verbatim:
   ```
   task: "@m_opus"  main: "@m_opus"  planner: "@m_opus"
   executor/scribe/critic/sentinel/simplifier/labrat: "@m_flash"
   reviewer/mutation-tester/security-reviewer: "@m_zfl"
   scout: "@m_sonnet"  connector: "@m_kfc"
   ```
   Comparison against the seat spec's expected map: MATCH on all thirteen role entries
   (executor/scribe/critic/sentinel/simplifier/labrat→m_flash; reviewer/mutation-tester→m_zfl;
   scout→m_sonnet; connector→m_kfc; task/main/planner→m_opus). Extra configured roles
   (revenger/sonic→m_flash, distiller/seance→m_haiku) are unused by wave-1/wave-2 seats.

3. Alias resolution (config.yml lines 327-346): m_flash=opencode-go/deepseek-v4.1-flash:high;
   m_zfl=zai/glm-5.3-flash:max; m_sonnet=anthropic/claude-sonnet-5-5:high;
   m_kfc=kimi-code/kimi-for-coding:max; m_opus=anthropic/claude-opus-5-5:high. All five
   targets appear in enabledModels — no dangling override.

4. "No wave item passes a model" — Python scan (json load + regex over member entries and
   full spec bytes) of wave1-dispatch.json (49 members), wave2-dispatch.json (37 members),
   wave1-spec.json, wave2-spec.json:
   - registry member schema is {kind, agentId, role, item, axes, milestone}; 0 members
     carry any model field or model-alias string;
   - dispatch policy block carries only concurrency/ramp keys (source, maxLanes,
     minLanes, waveMinLanes, waveMaxLanes, declaredMaxLanes, hardCeiling, rampBatchSize,
     rampIntervalMs, globalRunnerCeiling) — no model key;
   - the only 'model' token hits in item prompts are semantic (RevSuiteDesign/ExecSuiteBuild
     "fence model", ExecWholeTailFixture truth-model wording, and this seat's own item
     naming the role map). Verdict: roles only; routing is config-driven.

5. Seat-model stub: named expected model per role (alias + resolved string) and enumerated
   all 37 wave-2 seats -> expected model from the registry. Actual answering model per seat
   is NOT exposed via proc:// (job listings at 2026-10-26T20:17Z carry name/role/status/
   uptime only, live and exited jobs alike); stub marks the per-seat actual-model fill as
   PENDING from results. This seat's own session context reports
   Model: kimi-code/kimi-for-coding — consistent with connector→m_kfc.

6. Lane state at verification (read-only git): HEAD=5006097a84305267c9a3e8c1e1d560e60fe41d37,
   `git status --porcelain` shows only untracked wave-2 runtime files (.ready markers,
   wave2-dispatch.json, wave2-run.err, wave2/) — no tracked-file dirt.

## Finding

No falsification on the routing surface: the configured role map equals the wave policies'
expected map on every role entry, every alias resolves and is enabled, and no wave-1 or
wave-2 item passes a model. The do-nothing control (config-driven routing, model-free
items) holds as designed. C1/C2 claims are unaffected by any routing defect.

## Scope discipline

Wrote only: this receipt and ConnRoleGround.routing.txt in the wave2 dir. No other lane
file touched; no git/jj mutation anywhere (read-only git only). Scratch
/fast/scratch/hyaku/kasegi-r39/ConnRoleGround/ created, used for the Python scans, and
removed before yield. No network fetches. No tools installed this run (nothing needed;
existing python3/grep/git sufficed).

## Report trailer

Report: .ufo/waves/round-39/wave2/ConnRoleGround.md
