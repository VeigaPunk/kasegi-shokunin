# MutationC1 — kasegi round-70 w1 — R70 rule limbs against the gate's own selftest (pin 96)

- Seat: MutationC1 (leaf; no subagents; read-only on the lane except this file). Mutants were written only under `/fast/scratch/hyaku/kasegi-r70/MutationC1/`; the lane copy `corpus/instruments/figure-audit.py` was never opened for write and never edited.
- Revs: base `e7c02bddaa32…`, frozen claims/pins `e74ba6b5d522…`, C1 implementation `c1051749571c…`, C2 landing `b4afd8a0206b…` (C2 out of scope here).
- Tooling: nothing installed (PACMAN GUARD respected). `/usr/bin/python3` 3.14.8, git 2.56.0, `/usr/bin/sort` GNU coreutils 9.12 — the host binaries the gate executes.
- Scratch: `/fast/scratch/hyaku/kasegi-r70/MutationC1/` (NVMe), every run with `HYAKU_SCRATCH` inside it. Tree removed before yield; all decisive receipts are embedded below.
- Frozen inputs read first: `.ufo/waves/round-70/claims.json` and `.ufo/waves/round-70/controls/pins-r70.txt` at `e74ba6b5…`.

## 0. Exported bytes

```
$ git -C <lane> show c1051749…:corpus/instruments/figure-audit.py > S/gate.py
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  S/gate.py   (811 lines)
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  pins-r70.txt .ufo/waves/round-70/controls/candidate-gate-r70.py
$ git -C <lane> show c1051749…:.ufo/waves/round-70/controls/c1-probe-run-r70.py > S/counter.py
aaee62290853791d0d0768fa7633f908e32ae5783c6c72a8cc354050f5276176  S/counter.py  (286 lines; matches pins-r70.txt)
```

Exported gate == frozen candidate gate == `pins-r70.txt`. Every mutant below is that exact byte string with **one** textual replacement; the driver asserts `src.count(anchor) == 1` before writing (assertion fires and aborts the sweep otherwise).

## 1. Baseline and restoration

```
$ HYAKU_SCRATCH=S/base python3 S/gate.py --selftest      → exit 0
selftest cases=96 failures=0
```

```
$ HYAKU_SCRATCH=S/work/restore python3 S/gate.py --selftest   (after the whole sweep) → exit 0
selftest cases=96 failures=0
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  S/gate.py   (sha unchanged)
```

Honest note: the first restore attempt inside the driver ran before `work/restore` existed and died `FileNotFoundError` from `tempfile.mkdtemp` (exit 1, no case lines) — an inconclusive run, not a detector result. It was re-run after `mkdir -p` and the green receipt above is that re-run. Byte restoration is exact (`sha_unchanged=true`), so no restore-mutant-verify cycle is affected.

## 2. Exact mutation text (anchor → replacement)

`python_flags_ok` body as exported (lines 364–390):

```
    for tok in args:
        if tok == "--":                              # A: separator early return
            return True
        if not tok.startswith("-") or tok == "-":
            continue
        if not tok.startswith("--"):
            if tok == "-o" or tok.startswith("-o"):   # B: short -o limbs
                return False
            continue
        name = tok.split("=", 1)[0]                   # C: value split
        if len(name) <= 2:                            # D: len guard
            continue
        for flag in PY_DENIED_FLAGS:
            if name == flag or flag.startswith(name): # E: exact | abbreviation
                return False
```

| id | anchor (exactly once) | replacement |
|---|---|---|
| M1-{root,out,output,json,scratch,url,work} | `PY_DENIED_FLAGS = ("--root", "--out", "--output", "--json", "--scratch", "--url", "--work")` | same tuple with that one entry deleted |
| M2 | `if name == flag or flag.startswith(name):` | `if name == flag:` (drops abbreviation limb) |
| M3 | `if name == flag or flag.startswith(name):` | `if flag.startswith(name):` (drops exact limb) |
| M4 | `        if tok == "--":\n            return True\n` | `` (empty — separator no longer ends option scanning) |
| M5 | `            if tok == "-o" or tok.startswith("-o"):\n                return False\n` | `` (empty) |
| M6 | `    for tok in args:\n        if tok == "--":` | `    return True\n    for tok in args:\n        if tok == "--":` (always admit) |
| M7 | `        if len(name) <= 2:\n            continue\n` | `` (empty) |
| M8 | `    run_case("git-show-no-operand-refused", 2, _one("s-gitshowbare", "git show", "35"))\n` | `` (empty) |
| M9 | `    run_case("git-show-separator-refused", 2,\n             _one("s-gitshowsep", "git show HEAD:g.txt -- g.txt", "35"))\n` | `` (empty) |
| M10 | `    run_case("python-head-dashdash-operand-admitted", 0,\n             _one("s-pydashdash", "python3 corpus/instruments/ok.py -- --root", "35"))\n` | `` (empty) |
| M11 | `        if not tok.startswith("-") or tok == "-":\n            continue` | same with `break` (stop scanning at the first operand) |
| M12 | `        name = tok.split("=", 1)[0]` | `        if "=" in tok:\n            continue\n        name = tok.split("=", 1)[0]` |
| M13 | `        name = tok.split("=", 1)[0]` | `        name = tok` (no value split) |
| M14 | `        if tok == "--":\n            return True` | `        if tok == "--":\n            return False` |
| M15 | `    if "--" in parts[2:] or not operands:\n        return False\n` | `    if "--" in parts[2:]:\n        return False\n` (git_show no-operand limb) |
| M16 | `    if "--" in parts[2:] or not operands:\n        return False\n` | `    if not operands:\n        return False\n` (git_show separator limb) |

M15/M16 are own additions: M8/M9 test deletion of the *cases*, M15/M16 test deletion of the *limbs those cases are supposed to pin*.

## 3. Sweep result (22 mutants, 13 killed / 9 survived)

Command per mutant: `HYAKU_SCRATCH=S/work/<id> python3 S/mutants/<id>.py --selftest`.

| id | exit | verdict | failing selftest case ids | mutant sha256 |
|---|---|---|---|---|
| M1-root | 1 | **killed** | python-head-root-space-refused, -root-equals-refused, -root-abbrev-refused (cases=96 failures=3) | `1fda00986107b164b423121ad2deef16fe3d31f96cfa720958954a179962add4` |
| M1-out | 0 | survived | — (cases=96 failures=0) | `80b3ea7a158f1c652e29e99ad509a864e2495b5dc26f88c69857b30430640467` |
| M1-output | 0 | survived | — (96/0) | `d3c8b6c3e3d62fb2d0f11a2e284228a98f3eae474fdbcf396eed256b0f8de1a5` |
| M1-json | 1 | **killed** | python-head-json-refused (96/1) | `8dcb07cf738c2207a91f3cb22f55ce3d307af5cde8e4b50067409478d1d0e2d3` |
| M1-scratch | 0 | survived | — (96/0) | `7a1fff02f6c0bed7fdbb6a9a1af427fa0829be7fc4f49d1a51ca2b827573c98f` |
| M1-url | 0 | survived | — (96/0) | `9aa9c049551f07367a5ad755f9dc6f351bb8e888868054ab09806f37df843223` |
| M1-work | 0 | survived | — (96/0) | `bfe8bc284f8af3868b6179fbab554a264ea2c7103e297e3bf0f47207b04769bb` |
| M2 | 1 | **killed** | python-head-root-abbrev-refused (96/1) | `7a98454d4e40946253b613148f6870efb232f36b18d5df53223f4f16edb2db50` |
| M3 | 0 | survived | — (96/0) | `e1b83e26186f8f1c6ce3d15646e634a5b078e1d5cb9fdc57fe8c900edda4597d` |
| M4 | 1 | **killed** | python-head-dashdash-operand-admitted (96/1) | `5e29cc583ded65907b4f59816f73f68397bd209a6ba6a46719d3916d88bbf4e2` |
| M5 | 0 | survived | — (96/0) | `157f835a492c2d35f3349f672144f07c4361f93f9fdf880de21305ab4efeb5ec` |
| M6 | 1 | **killed** | root-space, root-equals, root-abbrev, out-space, out-equals, out-abbrev, json (96/7) | `48cf2b153e3a92b5848f73febfade926680f3c94946c8000efce6db3c246cec4` |
| M7 | 0 | survived | — (96/0) | `017c6f999dacfd376d81aa43fbed0143bac860e7d49c3e2e97e5bb5c0c074f93` |
| M8 | 1 | **killed** | none — `selftest pin cases=95 expected=96 verdict=fail` | `e6d55bdefca74225afb26a04da082c8215c8d0958b97860eb03e6be3f2d00a1a` |
| M9 | 1 | **killed** | none — `selftest pin cases=95 expected=96 verdict=fail` | `4594c8f1bf0ee8561831c5cf198f16bc66fe6fa9a3ae6b690773ad956c4348c6` |
| M10 | 1 | **killed** | none — `selftest pin cases=95 expected=96 verdict=fail` | `667d4678584f2ff24362211e91092c2862ca4aedea8e8c72e49767b80a36ed7d` |
| M11 | 1 | **killed** | out-space, out-equals, out-abbrev (96/3) | `2eea3b8d44f256bd1d1515b36c84e16462accc55e3b1abf1cd820de4d0867ecc` |
| M12 | 1 | **killed** | python-head-root-equals-refused (96/1) | `014425b57b5078f7dcdf4b6a12049c49e4941087dad20ca4c19db79de92535e5` |
| M13 | 1 | **killed** | python-head-root-equals-refused (96/1) | `4458d8d133a83bb5a63af8f43b8fe99aadbb4e4d55eaafafc9a4798645084c73` |
| M14 | 1 | **killed** | python-head-dashdash-operand-admitted (96/1) | `cf8b6c03a14edc736b6cb56128800558b3e92b1ab1d992bf0f873cf46a70c48e` |
| M15 | 1 | **killed** | git-show-no-operand-refused (96/1) | `eff5551ea51d6da889a035d8239cd2e89303ba0739956b4900f357df9d0419c5` |
| M16 | 0 | survived | — (96/0) | `46bdae55454b461a0b4ebb17283d90d7a356433c8bd7442b261eafc544c4d25e` |

Restored bytes after the sweep: `selftest cases=96 failures=0`, exit 0, gate sha `7a8d52eb…` unchanged.

## 4. Survivors: equivalent mutants vs real coverage holes

Behavioural differential over a 67-token × 335-argv matrix (every prefix of every denied flag, `=VALUE` forms, short forms, `--`, `--=X`, operand and post-separator positions), pristine `python_flags_ok` vs mutant:

```
M1-root     differing_argsets=33   e.g. ["--r"]  pristine=False mutant=True
M1-out      differing_argsets=0    EQUIVALENT on this matrix
M1-output   differing_argsets=12   e.g. ["--outp"] pristine=False mutant=True
M1-json     differing_argsets=16   M1-scratch 28   M1-url 27   M1-work 16
M2 84   M3 0 (EQUIVALENT)   M4 58   M5 4 (["-o"])   M6 250   M7 4 (["--="])   M11 125   M12 56   M13 56   M14 69
```

### 4a. M1-out and M3 — equivalent mutants, no case can kill them

- **M1-out**: `--out` is a strict prefix of `--output`, so every option name that `--out` refuses (`--o`, `--ou`, `--out`, `--out=…`) is also a prefix of `--output` and is refused by the surviving entry. Deletion is behaviourally null while `--output` stays. Measured: proposed isolated case `python3 corpus/instruments/capture-source.py --id x --out out.txt` (no `--url` in the derive) is **green on both** pristine and M1-out (`exit=2 want=2 verdict=pass` on each) — the case cannot discriminate, confirming equivalence rather than a gap. A future edit that also drops `--output` makes M1-out a real defect; the pair must be treated as one rule.
- **M3**: `name == flag ⟹ flag.startswith(name)`, so `name == flag or flag.startswith(name) ≡ flag.startswith(name)`; 0/335 argv differences. Equivalent mutant, not a coverage hole.

### 4b. Real coverage holes — each killed by one named missing case (R103)

Each proposed case was added to the **pristine** gate (with `EXPECTED_CASES` 96→97/98 so the count pin does not mask the case verdict) and to the mutant; control green, mutant red on exactly that case:

| survivor | missing case (proposed text) | control (pristine+case) | mutant+case |
|---|---|---|---|
| M1-output | `run_case("python-head-outputp-abbrev-refused", 2, _one("s-pyoutputp", "python3 corpus/instruments/ok.py --outp X", "35"))` | `cases=97 failures=0` exit 0; case `exit=2 want=2 pass` | case `exit=0 want=2 **fail**`; `97/1` exit 1 |
| M1-scratch | `run_case("python-head-scratch-refused", 2, _one("s-pyscratch", "python3 corpus/instruments/ok.py --scratch X", "35"))` | `97/0` exit 0; `exit=2 pass` | `exit=0 want=2 **fail**`; `97/1` |
| M1-url | `run_case("python-head-url-only-refused", 2, _one("s-pyurl", "python3 corpus/instruments/ok.py --url file:///dev/null", "35"))` | `97/0` exit 0; `exit=2 pass` | `exit=0 want=2 **fail**`; `97/1` |
| M1-work | `run_case("python-head-work-refused", 2, _one("s-pywork", "python3 corpus/instruments/ok.py --work X", "35"))` | `97/0` exit 0; `exit=2 pass` | `exit=0 want=2 **fail**`; `97/1` |
| M2 (second gap) | `run_case("python-head-out-abbrev-isolated-refused", 2, _one("s-pyoutab2", "python3 corpus/instruments/capture-source.py --id x --ou out.txt", "35"))` | `97/0` exit 0; `exit=2 pass` | `exit=1 want=2 fail reasons=derive-exit-2`; `97/2` (this + root-abbrev) |
| M5 | `python-head-short-o-refused` (`ok.py -o out.txt`) **and** `python-head-short-o-bundle-refused` (`ok.py -oout.txt`), both want exit 2 | `cases=98 failures=0` exit 0; both `exit=2 pass` | both `exit=0 want=2 **fail**`; `98/2` exit 1 |
| M7 | `run_case("python-head-dashdash-equals-admitted", 0, _one("s-pydasheq", "python3 corpus/instruments/ok.py --=x", "35"))` | `97/0` exit 0; `exit=0 want=0 pass` | `exit=2 want=0 **fail**`; `97/1` |
| M16 | (git_show separator limb) `git show HEAD:g.txt -- HEAD:g.txt` — a derive whose post-separator operand *does* carry a colon, so only the separator limb refuses it | not built (out of the selftest's 96; needs a new case) | M16 admits it (unit: `git_show_operands_ok(["git","show","HEAD:g.txt","--","HEAD:g.txt"])` pristine=False, M16=True) |

Why the existing cases miss these:
- **`--scratch`, `--work`, `--url` have no case at all.** `--url` appears in the selftest only inside the three out-* derives (`capture-source.py --id x --url file:///dev/null --out …`), where `--out` refuses first — so M1-url survives, and M2's out-abbrev case survives too because `--url` (an exact match) is still refused by the `name == flag` limb.
- **`--out`/`--output` are only ever exercised as the pair** — the only abbreviation case for that family is `--ou`, a prefix of both.
- **The declared short `-o` limb is implemented but pinned by nothing**: no selftest case and no counter probe names a short form (the two existing `-o` cases are `sort -o` / `sort -uo`, i.e. `DENIED_FLAGS`, not `python_flags_ok`). This is the same declared-vs-pinned gap `w1/ReviewerC1.md` recorded, now demonstrated by mutation.
- **The `len(name) <= 2` guard is nearly dead**: a bare `--` token is consumed by the separator early return, so the guard is reachable only through the `--=…` shape (`name = "--"`). M7 proves it changes behaviour there; the guard is what keeps `--=x` an operand-looking token admitted rather than a blanket refusal.
- **`python-head-dashdash-operand-admitted` is the only case that pins the separator limb** (M4 and M14 both die on it) — the limb is well pinned.
- **M8/M9/M10 are caught only by the count pin**, never by a case: deleting a case yields `selftest pin cases=95 expected=96 verdict=fail` with zero failing cases. The pin is therefore the sole guard against case deletion, and it does not guard against *weakening* a case's derive. M15 vs M16 shows the asymmetry inside the R103 pair: `git-show-no-operand-refused` is load-bearing for its limb (M15 red, `exit=1 want=2`), while `git-show-separator-refused` is **over-determined** — M16 drops the separator limb and the case still passes `exit=2 verdict=pass`, because the trailing operand `g.txt` has no colon and the per-operand colon rule refuses it anyway (independently reproduces `w1/ReviewerC1.md` §5 mutB).

## 5. Cross-check against the frozen outer detector (12 measurements)

The claim's predicate is not the selftest but `.ufo/waves/round-70/controls/c1-probe-run-r70.py` (`VERIFY measurements=12 failures=0`). Each survivor was run through it (`HYAKU_SCRATCH=S/cw python3 S/counter.py --gate S/mutants/<id>.py --work S/cw/<id> --mode candidate`):

```
pristine    VERIFY measurements=12 failures=0 gate_sha256=7a8d52eb… mode=candidate
M1-out      VERIFY measurements=12 failures=0 gate_sha256=80b3ea7a…   survived the counter
M1-output   VERIFY measurements=12 failures=0 gate_sha256=d3c8b6c3…   survived
M1-scratch  VERIFY measurements=12 failures=0 gate_sha256=7a1fff02…   survived
M1-url      VERIFY measurements=12 failures=0 gate_sha256=9aa9c049…   survived
M1-work     VERIFY measurements=12 failures=0 gate_sha256=bfe8bc28…   survived
M5          VERIFY measurements=12 failures=0 gate_sha256=157f835a…   survived  (short -o unpinned end to end)
M7          VERIFY measurements=12 failures=0 gate_sha256=017c6f99…   survived
M2          MEASURE P3-python-root-abbrev FAIL rc=1 refused=0 marker_runs=1 wrote=0
            MEASURE selftest FAIL selftest cases=96 failures=1 rc=1
            MEASURE mutbat FAIL rc=1 mutbat killed=5/5 survivors=0 invalid=0 controls=fail
            MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=1
            VERIFY measurements=12 failures=4 gate_sha256=7a98454d… mode=candidate
```

- The frozen predicate is exactly as blind as the selftest to the seven survivor limbs: it has no probe naming `--scratch`, `--work`, `--url`, `--output`-only abbreviations, a short `-o`, or `--=…`, and its P4/P5/P6 carry `--url` alongside `--out` (same non-isolation as the selftest).
- Where it does bite (M2) it bites twice: P3 shows the real side effect (`marker_runs=1` — the fixture entry's `recheck:` payload ran through `bash -c`), not just a status change. That is the correct failure anatomy for this class.
- `MEASURE mutbat` is **not** evidence about R70: the lane's `corpus/instruments/figure-audit-mutbat.py` at `c1051749…` carries five mutants, all on pre-R70 limbs (`m4-drop-stale-literal-case`, `m6-readonly-gate-off`, `m7-python-confinement-off`, `m8-python-prefix-off`, `m9-python-boundary-separator-off`) plus one trailing-space control. `mutbat killed=5/5` says nothing about `PY_DENIED_FLAGS`, `python_flags_ok` or the R70 git-show pins. The 22-mutant set above is the first sweep that covers them.

## 6. Verdict

- **The R70 rule limbs are correctly pinned for the shapes the selftest enumerates, and under-pinned outside them.** 13/22 mutants killed, 9 survived; the 7 survivors that were run through the frozen 12-measurement counter (§5) all survive it. M3 and M16 were not run through the counter — M3 is equivalent by algebra, M16 touches only `git_show_operands_ok`, which no counter probe exercises — so their survival there is [INFERENCE], not measured.
- Killed with the expected detector: every limb that has a case or probe aimed at it — root name/equals/abbrev, json, the `--` separator (both directions), the whole `python_flags_ok` body, the value-split limb, the exact limb, and the git-show no-operand limb.
- Equivalent (no case can kill, correctly so): **M1-out**, **M3** — proven by predicate algebra and 0/335 argv differences, not by absence of data.
- Real coverage holes (R103 findings), each with the missing case measured to kill it: **M1-output**, **M1-scratch**, **M1-url**, **M1-work**, **M5** (the *declared* short `-o` limb), **M7**, **M16** (git-show separator limb), plus the non-isolating `--url` in the out-* cases that hides **M2**'s abbreviation limb.
- Nothing here defeats C1 as frozen: the predicate is the enumerated P1..P7 set plus `selftest cases=96 failures=0`, and both hold (`w1/ReviewerC1.md` reproduced them from committed bytes). These are pin-strength findings for the next round, not a refutation of the frozen claim.

Ranked repair list (smallest first, for L1 to route — not applied by this seat):
1. Isolate the abbreviation limb: one case `capture-source.py --id x --ou out.txt` (no `--url`) — kills M2's out-side gap.
2. Add `python-head-short-o-refused` (`ok.py -o out.txt`) and `-oout.txt` — the declared limb currently has no detector at all, in the selftest or the counter.
3. Add `--scratch` / `--work` / `--url` refusal cases and a `--outp` abbreviation case — each kills a surviving M1 mutant.
4. Add a `git show HEAD:g.txt -- HEAD:g.txt` case so the separator limb is pinned by a derive only it refuses (M16).
5. Optional: add a `--=x` admission case if the `len(name) <= 2` guard is to stay load-bearing (M7); otherwise the guard is untested and effectively dead behind the separator return.
6. Keep `--out` and `--output` together (M1-out is only null while both remain) and remember the count pin is the only guard against case deletion (M8/M9/M10).

## 7. Receipts

- Driver: `S/drive.py` (sweep, per-mutant `count(anchor)==1` assert, `results.json`, `restored.txt`), `S/probe.py` (missing-case probe, `probe.json`), `S/diff.txt` (335-argv differential), `S/cw/<id>/` (counter work dirs). All under `/fast/scratch/hyaku/kasegi-r70/MutationC1/`, removed on yield after these receipts were copied into this file.
- Lane mutations performed by this seat: none. Lane files created: this report only.
