# MutC2Counter — round-99 C2 mutation probe

Seat: `MutC2Counter` (leaf; no subagent dispatch). Read-only attacker: no commit, no push, no
mutating git/jj in the lane repo. Every clone, mutant and work dir lived under
`S=/fast/scratch/hyaku/kasegi-r99/MutC2Counter` (removed after the receipts were copied here).

Fixture: `git clone --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin $S/clone`, checked out
at the C2 landing `a3db47e71fe292c03b00ba11f38cccbec45d3966`.
`git -C $S/clone rev-parse --show-toplevel` → `/fast/scratch/hyaku/kasegi-r99/MutC2Counter/clone`.

## 1. Pins and pristine baseline

```
$ git -C $S/clone rev-parse HEAD
a3db47e71fe292c03b00ba11f38cccbec45d3966
$ sha256sum $S/clone/corpus/instruments/capture-secret-scan.py
8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a
$ sha256sum $S/clone/.ufo/waves/round-99/c2/session-cookie-probe.py
79b2235d94295129fbc6c404a6d7005772099dd9489e446df875488d3fef6904
```

Both equal the pins in `claims.json` (instrument `8b338726…`, counter `79b2235d…`).

```
$ python3 -B $S/clone/corpus/instruments/capture-secret-scan.py --selftest
SELFTEST-RESULT pass cases=192          rc=0
$ python3 -B $S/clone/.ufo/waves/round-99/c2/session-cookie-probe.py \
    --lane $S/clone --instrument $S/clone/corpus/instruments/capture-secret-scan.py --work $S/base
PROBE-RESULT mustfix_hit=12/12 negatives_extra=0 negatives=10 \
  instrument_sha256=8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a rc=0
```

Baseline reproduces K1 and K2 exactly (receipt `-receipts/baseline.txt`).

## 2. Method

The landed shape is `corpus/instruments/capture-secret-scan.py:318-320`:

```
    ("gitlab-session-cookie", re.compile(
        _GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[^\n]{0,8}[:=][^\n]{0,8}"
        rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])")),
```

Twelve mutants were built by replacing that two-line literal (lines 318-319) with one line that
differs in exactly one semantic point. `difflib.SequenceMatcher` on each full file reports exactly
one non-equal hunk, `('replace', 318, 320, 318, 319)`, for all twelve; no other byte of the
instrument changes. Each mutant was staged beside copies of `claim-package-check.py` and
`capture-secret-allow.tsv` (the scanner loads both from its own directory), then run as:

```
python3 -B $S/mut/<name>/capture-secret-scan.py --selftest
python3 -B $S/clone/.ufo/waves/round-99/c2/session-cookie-probe.py \
    --lane $S/clone --instrument $S/mut/<name>/capture-secret-scan.py --work $S/mut/<name>/work
```

A mutant is **killed** when `--selftest` exits non-zero (`SELFTEST-RESULT fail`) or the probe
prints `mustfix_hit` < 12/12 or `negatives_extra` > 0. Pristine is the control and passes both.

## 3. Results

Full hashes and raw result lines: `-receipts/mutants.tsv`, `-receipts/mutant-runs.txt`; exact
mutated regex per mutant: `-receipts/mutant-regex.txt`.

| mutant | single-point change | sha256 (mutant) | selftest | probe | verdict |
|---|---|---|---|---|---|
| M01-narrow-window-s-plus | separator → `[\s]+` | `bd8868fbbb769933d131a39724538a3e1b93450373d59c746681dbed83743e00` | fail, 15 cases | 0/12 | killed by both |
| M02-drop-operator | `[^\n]{0,8}[:=][^\n]{0,8}` → `[^\n]{0,8}[^\n]{0,8}` | `bee0903d40ff0b6173845c029eeedf5f99989bfa59bb16bdfd88281bbfb7e0d6` | fail, 2 cases | 12/12, extra=2 | killed by both |
| M03-widen-gap-9 | first gap `{0,8}` → `{0,9}` | `ff3632f814fb73e1e04382d20ea010e9de4c52b8f580635881bfd9156d12ac93` | fail, 1 case | 12/12, extra=1 | killed by both |
| M04-allow-newline | `[^\n]` → `[\s\S]` in both gaps | `921305ffacc75ae51d1879196f6c2aabee4a7db9e4a50124e3ecc1664ad68209` | fail, 1 case | 12/12, extra=1 | killed by both |
| M05-drop-cell-group | remove `(?:cell-[0-9]+-)?` | `7060950af0b5d5941913d291707e7f16eafdaf740e9305b5aec865f2564098ba` | **pass, 192** | **12/12, extra=0** | **SURVIVED** |
| M06-hex-63 | value `{64}` → `{63}` | `ed3134a1732857c43c7b8607ba4255e9b7fc132068890bde5b7de649d01f68c4` | fail, 2 cases | 12/12, extra=1 | killed by both |
| M07-hex-upper | value `[0-9a-f]` → `[0-9a-fA-F]` | `5cf3b191da5a50368f9600c5060084d48594aca11528562eaaf59a63913c29f9` | fail, 2 cases | 12/12, extra=1 | killed by both |
| M08-drop-right-boundary | remove `(?![0-9a-f])` | `a63061a729e82932f6a8ffd0faafc27495f094ec09ed84266c8424fda7ae95ce` | **pass, 192** | **12/12, extra=0** | **SURVIVED** |
| M09-drop-left-boundary | remove `_GL_LB + ` | `c0c75aa77ac7290626b445cb1e5f7d2e5ddd86908770975a5c44c3b7163e2f7a` | fail, 1 case | 12/12, extra=1 | killed by both |
| M10-drop-geo-group | remove `(?:_geo_[0-9a-f]{64})?` | `dbd6dc1a2123a59dc02d9cc95e5fbff0cde3b7b9d8718281f67257fafec903b9` | fail, 2 cases | 11/12 | killed by both |
| M11-gap1-7 | first gap `{0,8}` → `{0,7}` | `2e4cf29cf5ed26e3e5bbd1f5bfeb94c5b00045ca54be443f4778c3c0f4aaf360` | **pass, 192** | **12/12, extra=0** | **SURVIVED** |
| M12-gap2-7 | second gap `{0,8}` → `{0,7}` | `8164c22d3baec771aaf730e69bd3c69849a2a1c36dbaea587cb7cf6dba133a33` | **pass, 192** | **12/12, extra=0** | **SURVIVED** |

Pristine control before and after the run: `8b338726…`, selftest `pass cases=192`, probe
`12/12 negatives_extra=0`.

### Kills, with the case that caught each

- **M01** — selftest 15 FAIL: the three pre-round-99 positives (`gl-session-cookie`,
  `-cell`, `-geo`) plus all twelve round-99 positives; probe 0/12. Narrowing to whitespace loses
  the whole separator class.
- **M02** — selftest `gl-session-ck-cell-nondigit`, `gl-session-ck-gap-9`; probe
  `n-cell-nondigit`, `n-gap-9`. Positives stay 12/12: dropping `[:=]` widens the total window to
  16 bytes and the operator's load-bearing role in this case set is width limiting, not
  punctuation.
- **M03** — selftest `gl-session-ck-gap-9`; probe `n-gap-9`.
- **M04** — selftest `gl-session-ck-gap-newline`; probe `n-gap-newline`.
- **M06** — selftest `gl-session-ck-63-hex`, `gl-session-cookie-63`; probe `n-63-hex`.
  Positives stay 12/12: the 64-hex values are rejected by the quantifier, so the length error is
  caught only from the negative side.
- **M07** — selftest `gl-session-ck-upper-hex`, `gl-session-cookie-upper`; probe `n-upper-hex`.
  Same pattern: alphabet widening is caught only by the negative.
- **M09** — selftest `gl-session-ck-left-word`; probe `n-left-word`.
- **M10** — selftest `gl-session-cookie-geo`, `gl-session-ck-geo-pct20`; probe `ck-geo-pct20`
  (11/12). The only mutant killed from the positive side by the probe.

### Survivors are not equivalent mutants

Each survivor was compared with pristine through the instrument's own `scan_bytes` on crafted
inputs (`-receipts/discrimination.txt`). All four differ from pristine on inputs the detectors
never exercise, so each is a real capability loss that both detectors miss:

| survivor | pristine | mutant | discriminating input |
|---|---|---|---|
| M05 | hit | miss | `_gitlab_session=cell-<N>-<64 hex>` with N ≥ 3 digits (`cell-123-` is 9 bytes, past the 8-byte gap) |
| M08 | miss | hit | 73+ consecutive lower-case hex after `_gitlab_session=` |
| M11 | hit | miss | exactly 8 bytes between `_gitlab_session` and the operator |
| M12 | hit | miss | exactly 8 bytes between the operator and the value |

Sweeps (pristine / mutant):

```
hex-run length: 63 F/F, 64..72 T/T, 73..77 F/T          (M08)
cell-N digits:  0,1,2 T/T, 3,4,5 T/F                    (M05)
gap1 bytes:     6,7 T/T, 8 T/F, 9 F/F                   (M11)
gap2 bytes:     6,7 T/T, 8 T/F, 9 F/F                   (M12)
```

Note the 65-72 row: pristine itself accepts a 65-72 hex run because the 8-byte gap absorbs the
extra digits, so the right boundary only bites at ≥73. The 63-hex negative does not test the
boundary at all — it is rejected by the `{64}` quantifier.

## 4. Coverage gaps named

1. **Gap width is pinned only by rejection at 9, never by acceptance at 8.** Both `{0,8}` windows
   can shrink to `{0,7}` with selftest 192/192 and probe 12/12 (M11, M12). The frozen negatives
   test `n-gap-9` on the left side only; there is no exactly-8 positive and no 9-byte right-gap
   negative.
2. **The right boundary `(?![0-9a-f])` is untested.** Removing it passes both detectors (M08).
   `n-63-hex`/`gl-session-cookie-63` are rejected by the quantifier; the 65-72 hex region is
   accepted by pristine anyway through gap absorption; only a ≥73-hex run separates the two.
3. **The `cell-<N>-` group is untested for N ≥ 3 digits.** Removing it passes both detectors
   (M05): the 8-byte gap absorbs `cell--` and `cell-7-`, so the only cell cases in the suite do not
   exercise the group at all.
4. **No asymmetric kill, and none is possible from this case set in practice.** The probe's ten
   negatives carry the same ten intents as the selftest's round-99 negatives (payloads are
   re-encodings, e.g. the probe's value-hyphen is 64 bytes and the selftest's 63), and its twelve
   positives are the same twelve separator shapes as the selftest's twelve. Across 12 mutants every
   kill was registered by both detectors and every survivor passed both. The probe therefore adds
   verbatim provenance and an independent execution path, not boundary coverage: the two detectors
   share the same blind spots.
5. **Direction asymmetry worth recording:** length and alphabet errors are caught only from the
   negative side (M06, M07 keep 12/12 positives), while separator/geo losses are caught from the
   positive side (M01, M10). No mutant in this set was caught by one detector only.

## 5. Restoration and integrity

- The pristine fixture file was never edited; mutants are separate copies under `$S/mut/`.
- After the run: `sha256sum $S/clone/corpus/instruments/capture-secret-scan.py` →
  `8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a` (unchanged);
  `git -C $S/clone status --porcelain` → empty; `git -C $S/clone rev-parse HEAD` →
  `a3db47e71fe292c03b00ba11f38cccbec45d3966`.
- Lane repo: no tracked file touched. `git -C <lane> status --porcelain -- corpus/instruments/capture-secret-scan.py .ufo/waves/round-99/c2` → empty; the only untracked entry is
  `.ufo/waves/round-99/w1/` (this report and its receipts).
- Scratch `$S` removed after `-receipts/` was written here.

Tooling: none installed or upgraded; the probe used the host `python3` (stdlib only), per the
paused-pacman constraint.

## 6. Verdicts

VERDICT: M01-narrow-window-s-plus — KILLED (selftest fail 15 cases; probe 0/12).
VERDICT: M02-drop-operator — KILLED (selftest `gl-session-ck-cell-nondigit`,`gl-session-ck-gap-9`; probe `negatives_extra=2`).
VERDICT: M03-widen-gap-9 — KILLED (selftest `gl-session-ck-gap-9`; probe `n-gap-9`).
VERDICT: M04-allow-newline — KILLED (selftest `gl-session-ck-gap-newline`; probe `n-gap-newline`).
VERDICT: M05-drop-cell-group — SURVIVED both detectors; real capability loss at `cell-<N>-` with N ≥ 3 digits (pristine hit, mutant miss).
VERDICT: M06-hex-63 — KILLED (selftest `gl-session-ck-63-hex`,`gl-session-cookie-63`; probe `n-63-hex`).
VERDICT: M07-hex-upper — KILLED (selftest `gl-session-ck-upper-hex`,`gl-session-cookie-upper`; probe `n-upper-hex`).
VERDICT: M08-drop-right-boundary — SURVIVED both detectors; real capability loss at 73+ hex runs (pristine miss, mutant hit).
VERDICT: M09-drop-left-boundary — KILLED (selftest `gl-session-ck-left-word`; probe `n-left-word`).
VERDICT: M10-drop-geo-group — KILLED (selftest `gl-session-cookie-geo`,`gl-session-ck-geo-pct20`; probe `ck-geo-pct20`, 11/12).
VERDICT: M11-gap1-7 — SURVIVED both detectors; real capability loss at exactly 8 gap bytes before the operator.
VERDICT: M12-gap2-7 — SURVIVED both detectors; real capability loss at exactly 8 gap bytes after the operator.
VERDICT: coverage — 8/12 mutants killed by both detectors, 4/12 survive both (M05, M08, M11, M12); no asymmetric kill; the detector pair pins rejection at 9 gap bytes, 63-hex, upper-hex, cell-nondigit, left-word and the geo group, but never exercises acceptance at exactly 8 gap bytes, `cell-N` with ≥3 digits, or a hex run ≥73, so the C2 claim's separator window and right boundary are only partially pinned.
