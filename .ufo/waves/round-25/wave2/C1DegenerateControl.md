# C1DegenerateControl — attack on the frozen three limbs with degenerate controls

Seat: `L1Kasegi25.C1DegenerateControl` (critic, wave 2, READ-ONLY on production).
Target: the *frozen* C1 counter `corpus/instruments/recheck-audit.py` (sha256 `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` — matches `c1-instrument-digest.txt` and the live file).
Controls: `true`, `false`, `syntax-error`, `nonexistent-cd`, `own-file` (+ assistant controls `good`, `missing`, `wrongown`, `basestate`, `noline`).

## Verdict

- **The frozen three limbs (`parse`/`cwd`/`paths`) reject exactly one of the five named degenerate controls: `syntax-error`.** The other four (`true`, `false`, `nonexistent-cd`, `own-file`) all pass the frozen limbs (frozen=111) — frozen pass=7/9 on the fixture.
- **The strict repair (added `cdroot`/`instrument`/`own` limbs) rejects all five named controls**: strict `pass_strict=2/9` — `true`, `false`, `nxcd`, `ownfile` are FROZEN-ONLY; `syntax` is FAIL. The wave-1 claim (strict 35/35 on the frozen surface, 37/37 final tree) survives every named attack.
- **One escape hatch found in the strict gate itself**: a vacuous `test -d ~/Projects/<anything>` line (names no corpus artifact, no instrument, no own entry, and the `~/Projects` target need not exist) passes **all six strict limbs** (`basestate.md` → strict=111111, `pass_strict=True`). It is a documented `base_state` carve-out (`recheck-audit.py:127-130`) grandfathered for two historical lines; the strict gate certifies *shape*, not execution — the line "passes" even while failing closed (lane=1).

Falsifiable evidence below: commands, outputs, exits, `file:line` for every claim.

---

## 1. Setup

Decimal fixture in `/tmp/c1deg/root` (no production edits — working tree untouched, git status still 39 modified `corpus/` files exactly as found; no VCS write):

```
root/corpus/knowledge/{true,false,syntax,nxcd,ownfile,good,missing,wrongown,basestate,noline}.md
root/corpus/instruments/tool.py              (empty stub; allows instrument-limb isolation)
root/corpus/source-snapshots/snap/manifest.json
```

Recheck lines (lane-shaped, `cd <lane> && …`, lane = `/home/vgpnk/Projects/shokunin/kasegi-shokunin`):

| entry | line | purpose |
|---|---|---|
| `true.md` | `cd LANE && true corpus/knowledge/true.md` | **true** |
| `false.md` | `cd LANE && false corpus/knowledge/false.md` | **false** |
| `syntax.md` | `cd LANE && python3 corpus/instruments/tool.py corpus/knowledge/syntax.md (note)` | **syntax-error** (prose tail ⇒ `bash -n` fails) |
| `nxcd.md` | `cd /nonexistent-round25-c1deg && python3 corpus/instruments/tool.py corpus/knowledge/nxcd.md` | **nonexistent-cd** |
| `ownfile.md` | `cd LANE && test -e corpus/knowledge/ownfile.md` | **own-file** (test, not instrument) |
| `good.md` | `cd LANE && python3 corpus/instruments/tool.py corpus/knowledge/good.md` | positive control |
| `wrongown.md` | `cd LANE && python3 corpus/instruments/tool.py corpus/knowledge/good.md` | own-limb isolate (names another file) |
| `missing.md` | `cd LANE && python3 corpus/instruments/tool.py corpus/knowledge/ghost-absent.md` | paths-limb isolate (ghost) |
| `basestate.md` | `cd LANE && test -d ~/Projects/definitely-absent-c1deg` | base-state escape probe |
| `noline.md` | (no recheck line) | completeness rule |

## 2. Exact command and receipt

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/recheck-audit.py --root /tmp/c1deg/root \
        --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin \
        --json /tmp/c1deg/result.json
AUDIT_EXIT=1
```

Per-entry verdicts (verbatim from run):

```
basestate.md   frozen=111 strict=111111 lane=1 foreign=1 gated  PASS
false.md       frozen=111 strict=111101 lane=1 foreign=1 gated  FROZEN-ONLY
good.md        frozen=111 strict=111111 lane=2 foreign=2 gated  PASS
missing.md     frozen=110 strict=110110 lane=2 foreign=2 gated  FAIL
nxcd.md        frozen=111 strict=111011 lane=1 foreign=1 gated  FROZEN-ONLY
ownfile.md     frozen=111 strict=111101 lane=1 foreign=1 gated  FROZEN-ONLY
syntax.md      frozen=011 strict=011111 lane=2 foreign=2 broken FAIL
true.md        frozen=111 strict=111101 lane=0 foreign=0 executes FROZEN-ONLY
wrongown.md    frozen=111 strict=111110 lane=2 foreign=2 gated  FROZEN-ONLY
strict pass=2/10 cdroot_fail=1 instrument_fail=3 own_fail=2
lines=9 total=10 pass=7 fail-closed=8 parse_fail=1 cwd_fail=0 paths_fail=1 exit=1
```

## 3. The five named controls — verdicts and strict failures

| control | frozen (parse,cwd,paths) | strict (parse,cwd,paths,cdroot,instrument,own) | frozen PASS? | strict PASS? | strict limb rejected by |
|---|---|---|---|---|---|
| `true` | `111` | `111101` | **YES** | no | `instrument` (names no corpus/instruments/*.py, no `~/Projects` test) — `recheck-audit.py:122-124` |
| `false` | `111` | `111101` | **YES** | no | `instrument` (same) |
| `syntax-error` | `011` | `011111` | **NO** | no | `parse` — `bash -n` exit nonzero |
| `nonexistent-cd` | `111` | `111011` | **YES** | no | `cdroot` (`cd` target ≠ lane root) — `recheck-audit.py:119-121` |
| `own-file` | `111` | `111101` | **YES** | no | `instrument` (`test -e` names no instrument) |

Only `syntax-error` fails the *frozen* triple. The strict gate — the repair added after the mutation seats (claims.json `counter_notes.counter_repair`) — rejects all five.

## 4. Evidence each limb fired as designed (exact runs)

- `parse` — `syntax.md` `bash -n` fails (broken, lane=2 foreign=2); consumed by `parse_ok = bash -n … returncode == 0` (`recheck-audit.py:85-86`).
- `cwd` — all nine fixture lines have identical exit **and** identical stdout+stderr SHA-256 from lane root and `/` (for example `true.md`: lane=0 foreign=0, `6e340b9cffb3…` == `6e340b9cffb3…`; `syntax.md`: lane=2 foreign=2, `e71efb6dc7de…` == `e71efb6dc7de…`); digest equality enforced at `recheck-audit.py:107-109`.
- `paths` — `missing.md` fails with `missing_paths=['corpus/knowledge/ghost-absent.md']` (`recheck-audit.py:115-116`); every named control names an existing path, so only `missing` trips it.
- `cdroot` — `nxcd.md` `cd_target=/nonexistent-round25-c1deg` ≠ lane ⇒ `strict["cdroot"]=False` (`recheck-audit.py:121`).
- `instrument` — `true`/`false`/`ownfile` name no instrument token ⇒ `strict["instrument"]=False` (`recheck-audit.py:122-124`); `good.md` passes despite lane=2 because `tool.py` exists under `--root` (`recheck-audit.py:122`).
- `own` — `wrongown.md` shows `1` only for `own` (`111110`), proving the limb is independently load-bearing (`recheck-audit.py:125`); `ownfile.md`'s `test -e` passes `own` (token `corpus/knowledge/ownfile.md` present) but is rejected by `instrument` (not by `own`).
- Completeness — `noline.md` ⇒ `lines=9 total=10 complete=False` ⇒ exit 1 even though 7/9 frozen-pass (`recheck-audit.py:251`).

## 5. Counterexample: the `base_state` escape hatch passes strict do-nothing

`basestate.md` line `cd LANE && test -d ~/Projects/definitely-absent-c1deg`:

- strict=111111, `pass_strict=True` — **passes all six strict limbs**;
- `~/Projects/definitely-absent-c1deg` does not exist on this host (`test -d` → exit 1; host `~/Projects` exists, no such child);
- the line names no `corpus/` path, no instrument, and not its own entry (tokens empty).

Code path: `BASE_TEST_RE = test[ \t]+-[def][ \t]+~/Projects/` (`recheck-audit.py:69`), `base_test = bool(BASE_TEST_RE.search(line))` (`:123`), `base_state = base_test and not tokens` (`:130`), `strict["own"] = own or sourced or base_state` (`:131`). The carve-out is deliberate (`:127-130` — grandfathered for `repo-git-state.md` and `root-loss-2026-10-12.md`), and it is the singleton strict-passing degenerate line in the fixture.

So while the strict gate rejects all five *named* controls, it does not reject a do-nothing `~/Projects` shape line — and it certifies that line even when it fails closed (lane=1). Impacted axes: `depth:verifiability` (the "own" and "instrument" limbs as written do not bind a `base_state` line to its entry or to an existing base). The wave-1 receipts are not wrong — the repair stands for the named control set — but the claim's strict wording should not be read as "strict = cannot be degenerate".

**Smallest safe correction (report-only, no production edit):** add an existence/binding check to the `base_state` arm, e.g. `base_state = base_test and not tokens and os.path.exists(os.path.expanduser("~/Projects")) and <bound-to-entry-or-existing-base>` — or explicitly document the `base_state` shape as an intent-only carve-out (as the code comment does). Note: tightening it to require the `~/Projects` target to exist would flip `root-loss-2026-10-12.md`, which asserts *absence* (`test ! -e ~/Projects/bounties …`), so any fix must be scoped to the binding, not to target existence.

## 6. Wave-1 receipts re-verified (all reproduce)

| receipt | command | result | exit |
|---|---|---|---|
| frozen before | `--root .ufo/waves/round-25/c1-controls/base --cdroot LANE` | `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0` | 1 |
| frozen surface | `--root .ufo/waves/round-25/c1-after-35 --cdroot LANE` | `strict pass=35/35 lines=35 pass=35` | 0 |
| final tree (live) | `--root /home/vgpnk/Projects/shokunin/kasegi-shokunin` (default cdroot) | `strict pass=37/37 lines=37 pass=37` | 0 |
| instrument selftest | `--selftest` | `selftest cases=14 failures=0 exit=0` | 0 |
| instrument digest | sha256sum | `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` | — |

JSON meta matches committed receipts (`root`/`cdroot`/`foreign_cwd` = `/`), and `c1-after-35.json`'s `cdroot` equals the lane root as in the committed file.

## 7. Files written (this seat)

- `.ufo/waves/round-25/wave2/C1DegenerateControl.md` (this report)
- `artifact` receipts in `/tmp/c1deg/`: `result.json`, `after35-rerun.json`, `before-rerun.json`, `live.json`, fixture root

No tool installed or upgraded (no pacman — per RULES.md read; used only `python3`, `bash`, system utils).
No production file edited; no VCS write.
