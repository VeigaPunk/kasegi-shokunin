# ScoutDatawalk — round-29 bounded data-walk receipt

Seat: `ScoutDatawalk` (scout, wave `kasegi-r29-build`). Role: L1 planner's bounded
data-walk over the frozen C1/C2 counters (claims.json, base `7a6591c1…`, freeze
`f28ff5d…`). I wrote nothing outside the lane repo; no edits were made by this seat.

Answering model actually used: **minimax-code/MiniMax-M3.1-Flash** (route table:
`scout → @m_mim = minimax-code/MiniMax-M3.1-Flash:high` in `~/.omp/agent/config.yml:343,359`;
matches the workstation model). No model-dependent inference was needed — every value
below is a measured command output.

---

## 0. Lane/tree state (measurement frame)

Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

- `git rev-parse HEAD` → `46e07f6ae8f23debb10034164252e7027b4d9091` (round-29 wave-1 spec + dispatch)
- `git rev-parse master` → same `46e07f6…`
- Lineage (all verified `git merge-base --is-ancestor` exit 0):
  `7a6591c1…` (base) ← `f28ff5d…` (freeze) ← `46e07f6…` (dispatch)
- `git log --oneline 7a6591c..master`:
  ```
  f28ff5d round-29: claims freeze + before receipts
  46e07f6 round-29: wave-1 spec + dispatch (v2, 64 seats)
  ```
- Freeze commit `f28ff5d` adds exactly the 4 receipt files (claims.json,
  c1-controls/before.txt, c2-controls/before.txt, census-before.txt); `git show --stat`
  confirms no corpus/ production files changed in the freeze.
- `git diff --stat 7a6591c f28ff5d HEAD -- corpus/` → **empty** (corpus bytes are
  identical across base → freeze → HEAD; I verified by `git archive` of both revisions
  into scratch trees and re-running every counter there).

`git status --porcelain` at walk time was **not clean** due to *sibling seats'
mid-flight edits* (walk made none): `M LOG.md`, `M corpus/QUALITY.md`,
`M corpus/instruments/anchorcheck.py`, `?? corpus/source-snapshots/round-29/`,
`?? .ufo/waves/round-29/{assimilation,wave1-run.err,wave1.ready*,wave1/}`.
The tracked corpus tree at base and freeze is clean (diff base→freeze over `corpus/`
is empty). Master has advanced one commit past the freeze with the dispatch commit,
which is the expected post-freeze state for a dispatched wave.

---

## 1. Frozen counters — BEFORE values at base 7a6591c and freeze f28ff5d

Every counter below was run (a) in the extracted base tree (B), (b) in the extracted
freeze tree (F), and (c) in the live lane root at walk start. B/F runs use:
`git archive <rev> corpus | tar -x -C $D`. Values are identical in all three frames.

### C1/depth:verifiability

| Check | Command | Expected (BEFORE) | B | F | Live (start) |
|---|---|---|---|---|---|
| selftest | `python3 corpus/instruments/anchorcheck.py --selftest` | `selftest cases=9 failures=0`, exit 0 | ✅ 9/0, exit 0 | ✅ 9/0, exit 0 | ✅ 9/0, exit 0 |
| limb-coverage assertion grep | `grep -cE 'limbs=[0-9]+ covered=' corpus/instruments/anchorcheck.py` | `0` (exit 1) | ✅ 0 | ✅ 0 | ✅ 0 |
| git-free PATH run | `T=$(mktemp -d); ln -s "$(command -v python3)" "$T/python3"; env -i PATH=$T "$T/python3" corpus/instruments/anchorcheck.py --selftest` | exit 1 + `FileNotFoundError: 'git'` | ✅ exit 1, traceback ends `FileNotFoundError: [Errno 2] No such file or directory: 'git'` | ✅ exit 1, same | ✅ exit 1, same |

All three BEFORE values hold at base **and** freeze, and reproduce the committed
control receipt `.ufo/waves/round-29/c1-controls/before.txt` byte-for-byte (which
records the same selftest line, the same 0, and the same exit-1 git-free traceback,
and the instrument digest `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`
= `git show 7a6591c:corpus/instruments/anchorcheck.py | sha256sum`, verified).

### C2/coverage

| Check | Command | Expected (BEFORE) | B | F | Live (start) |
|---|---|---|---|---|---|
| frontier admitted | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | `12` | ✅ 12 | ✅ 12 | ✅ 12 |
| entries citing S042 | `grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l` | `1` | ✅ 1 | ✅ 1 | ✅ 1 |
| S042 registry row | `grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md` | `1` | ✅ 1 | ✅ 1 | ✅ 1 |
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]+[[:space:]]*\|' corpus/SOURCES.md` | `42` | ✅ 42 | ✅ 42 | ✅ 42 |
| sources census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0, W04 ×2 only | ✅ (live) | ✅ (live) | ✅ exit 0: `W04 S028 duplicate url …`, `W04 S029 duplicate url …`, `ok …/corpus/SOURCES.md` |
| frontier harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=15 pass=15 exit=0` | ✅ 15/15/0 | ✅ 15/15/0 | ✅ 15/15/0 |

C2 BEFORE values hold at base and freeze; they match the committed controls
`.ufo/waves/round-29/c2-controls/before.txt` (12 / 0 for S04[3-5] / S042 entry 1 /
S042 row 1 / 42 rows / harness 15/15) and `census-before.txt` (exit 0, W04 S028/S029).

### Frozen counter-command parses and self-emission (M28-3 class check)

All 9 frozen counter commands pass `bash -n` (exit 0 each) and each **emits its own
value** — verified by executing each verbatim from the lane root:

- C1 cmd1 → prints `selftest cases=… failures=…`; C1 cmd2 → prints
  `selftest cases=|limbs=` lines; C1 cmd3 → prints `nogit_exit=$E`.
- C2 cmd1 → prints the awk count; cmd2 → prints the `wc -l` count; cmd3 → prints the
  `grep -c` count (note: exits 1 when the count is 0 — grep semantics, value still
  printed); cmd4 → prints `census_exit=$?`; cmd5 → prints `entries=/pass=/exit=` plus
  `harness_exit=$?`; cmd6 → prints per-id source-recheck `OK` lines and
  `recheck_exit=$?`.
No frozen counter is malformed the way round-28's `bad=` sed limb was (M28-3); the
`bad` sed limb is gone from the round-29 claim set.

---

## 2. Lane tip / status (item 2)

- Base tip `7a6591c1…` and freeze tip `f28ff5d…` hold exactly as claimed (both are
  ancestors of master; the freeze commit is the parent of HEAD).
- `git status --porcelain` at walk start showed **only** untracked `.ufo/waves/round-29/…`
  artifacts (my first inspection) and, by the end of the walk, sibling in-flight
  tracked edits (`LOG.md`, `corpus/QUALITY.md`, `corpus/instruments/anchorcheck.py`).
  The tracked tree at base/freeze is clean (empty corpus diff across base→freeze→HEAD);
  the live dirty state is the wave's own landing, not a base/freeze violation.

---

## 3. claims.json predicate/kill-rule cross-check (item 3)

### Predicate sentence consistency

- The **exact predicate sentence** (C1 and C2) appears verbatim **only in claims.json**.
  It is not reproduced as one string in the plan text (`wave1-spec.json` context),
  `wave1-dispatch.json`, or `build-spec.py` — but those artifacts carry the same
  **values/limbs** via fragments (e.g. `limbs=9 covered=9` ×5, `entries=16 pass=16` ×2,
  `selftest cases=12`, `registry rows (expect 45)`, frontier/entry/row expectations in
  the `ExecCanonC1`/`ExecCanonC2`/`ExecHarnessC2` prompts).
- The counter commands are shell encodings of the predicate limbs (not prose), and each
  emits the exact value the predicate names (verified above).
- The committed receipt labels (`c1-controls/before.txt`, `c2-controls/before.txt`) use
  the same limb vocabulary (`== selftest run ==`, `== limb-coverage assertion grep
  (expect 0) ==`, `== git-free PATH run (expect exit 1 + FileNotFoundError 'git' traceback) ==`,
  `== frontier admitted ==`, `== registry rows (expect 42) ==`, …) and their recorded
  values match exactly what I reproduced. Semantic equivalence across plan/counters/
  receipt labels holds on every predicate limb.

### Kill rule → do-nothing control receipt naming

Finding — **neither kill rule literally names its do-nothing control receipt file**:

- C1 kill_rule names `c1-receipt-index.txt` (the canonical *after* index) and the
  do_nothing_control names `c1-controls/before.txt` (which exists and whose digest
  matches the base blob). The kill rule itself does not name `c1-controls/before.txt`.
- C2 kill_rule names **no** receipt path, and its do_nothing_control text names no
  receipt path either (it restates the baseline numbers only); `c2-controls/before.txt`
  exists on disk but is not referenced from claims.json.
- Round-28's claims carried an explicit `control_receipts` field naming both control
  trees; round-29's claims.json dropped that field (check `cl.keys()`: C1 has
  `counter_commands, do_nothing_control, kill_rule, predicate_sentence, surface, …`,
  no `control_receipts`). This is a convention regression worth flagging to the L1 and
  to the `ConnClaims` seat.

### Live landing-state observation (labeled, not compared to before columns)

Because sibling seats were landing while I walked, I re-ran C1/C2 counters at the end:

- C1 (post-`ExecImplC1` landing, worktree `anchorcheck.py` sha256
  `68e1bdc6…`): `selftest cases=12 failures=0`, `limbs=9 covered=9`, exit 0; limbs
  grep now `1`; git-free run now `nogit_exit=0` (prints `SKIP pin-broken (git not found)`
  then `selftest cases=12 failures=0` / `limbs=9 covered=9`). The C1 predicate's after
  targets are being reached; these are AFTER-state observations and were not compared
  against before columns.
- C2: the F13 README row was not yet present at walk end (`awk` → 12; `grep -nE '^\| *F13 '`
  empty), but registry rows were already 45 with S043/S044/S045 rows present (SOURCES.md
  lines 49–51) and one knowledge entry cites S043/S044/S045
  (`program-severity-ladders-and-reward-scales.md:2-4`). Harness still 15/15 until the
  F13 row lands. All of this is mid-flight.
- **C2 source-recheck on the round-29 manifest** (untracked, still landing; sha256
  `3a0dec1b…` at measurement): `S043:Q1`/`Q2`/`Q4` report **`occurrences=12`**, not 1,
  `Q3` reports 1; S044/S045 all 1. Cause: `S043.txt` is a single-line JSON array of 153
  HackerOne policy records (1,220,741 B, `NR=1`), so the boilerplate scope text recurs
  across records. The currently-committed anchors are all `1`, making the anchor check
  degenerate on a one-line file (`anchor=1-ok` because the window is the whole file).
  The C2 kill rule requires `any manifest assertion not occurrences=1` — the current
  manifest does **not** satisfy that, while `source-recheck.py` exits 0
  (the M28-8-class gap: occurrences are printed, not gated on exit). Flagged for the
  owning seats (`ExecManifest`/`ScribeEntryF13`/`ExecCanonC2`); nothing here is final
  until those seats land.

---

## 4. Gaps / not reproduced

- No frozen counter failed to reproduce at base or freeze (all B/F/live values listed
  above). Every number in the item's list was reproduced exactly.
- The only "not reproducible at walk time" values are the **after**-state targets
  (`entries=16 pass=16`, frontier 13, registry 45 in README row state, manifest
  `occurrences=1` on all assertions) — those belong to still-landing sibling seats and
  are labeled PRE-STATE/landing here; I never compared them to before columns.
- The C1 kill-rule "canonical `c1-receipt-index.txt`" for round 29 did not exist at
  walk time (it is produced by `ExecCanonC1`; round-28's lives at
  `.ufo/waves/round-28/c1-receipt-index.txt`). Path ambiguity (wave-root vs
  `wave1/`) is worth naming.

## 5. Model note

Answering model: **minimax-code/MiniMax-M3.1-Flash** (scout route `@m_mim`). No
model-dependent computation was used; all values are command outputs.

## 6. Handoff notes

- Verification to run once the wave lands: re-check the C2 kill rule against the landed
  manifest (`occurrences=1` for every S043/S044/S045 assertion — the currently observed
  12 for S043 Q1/Q2/Q4 will fail it), and confirm the canonical round-29
  `c1-receipt-index.txt` carries an `instrument_sha256` line matching the committed
  `anchorcheck.py` digest.
- Flag to L1/ConnClaims: round-29 claims dropped the `control_receipts` field
  (round-28 convention), and neither kill rule names its do-nothing control receipt file.
