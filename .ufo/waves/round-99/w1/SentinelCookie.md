# SentinelCookie — round 99, C2 session-cookie window: the attacker's matrix

Seat: SentinelCookie (leaf; no subagent dispatched). Lane: `kasegi-shokunin`.
Landing under test: `a3db47e71fe292c03b00ba11f38cccbec45d3966` (C2), read-only.
Instrument `corpus/instruments/capture-secret-scan.py` sha256
`8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a` — equal to
the frozen pin, and `git show a3db47e7:corpus/instruments/capture-secret-scan.py`
hashes to the same value (receipt `landed-shape.txt`). Python 3.14.8, stdlib
only; **no tool installed or upgraded** this seat.

Question: can a real 64-hex GitLab session value be written into a capture so
that the landed gate never sees it, while GitLab's own rule (S140 + S150) does?

## The shape under test, exactly

`capture-secret-scan.py:318-320`, with `_GL_LB` at `:286`:

```
_GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[^\n]{0,8}[:=][^\n]{0,8}"
        rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])"
```

S140 (`corpus/source-snapshots/round-94/S140.txt:548-551`) publishes
`keywords = ["_gitlab_session"]`, `regex = '''(?:cell-[0-9]+-)?[0-9a-f]{64}'''`,
`assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''`,
`keywordGroupType = "raw"`; S150 (`corpus/SOURCES.md:162`) expands that to
`<keyword>.{0,8}[:=].{0,8}<value>`. **S140_A** = that expansion, applied with
`search`, with no left boundary and no right boundary — the published rule has
neither. I ran S140_A under two engine models: byte semantics (the lane's own
round-98 model, `SentinelShapes.md`) and rune semantics (Go `regexp`, which is
what consumes the rules file).

## Volume

| harness | cells | receipt |
|---|---|---|
| structured matrix, 14 families (39 separators, 26 contexts, 20 `cell-` prefixes, 10 `_geo_` forms, gaps 0-12, tabs, 9 newline/CRLF forms, 5 case variants, 23 right boundaries, 10 left boundaries, 10 value grammars, 6 non-ASCII windows) | 192 | `matrix-run.txt` |
| ASCII sweeps: byte before the keyword, byte after the value, byte before the operator, byte after the operator | 4 × 128 | `sweeps-run.txt` |
| randomized structural fuzz over the operator/gap/cell/value vocabulary | 4000 | `fuzz-run.txt` |
| replay of the twelve round-98 MUST-FIX payloads and the ten frozen negatives | 22 | `sweeps-run.txt` |
| end-to-end CLI, landed vs round-98 instrument | 5 files | `cli-checks.txt` |
| remediation candidates A and B | 2 × 22 | `remedy-run.txt` |

```
MATRIX cases=192 AGREE-HIT=121 AGREE-MISS=37 MUST-FIX=7 MUST-FIX-RUNE=4 REGRESSION-R98=23
NEW-HIT-VS-R98=39  LOST-HIT-VS-R98=23        (delta.txt)
FUZZ cases=4000 AGREE-HIT=189 AGREE-MISS=3778 MUST-FIX=33   (all the 74-hex form)
```

## MUST-FIX — landed miss, S140_A hit

`<H64>` = 64 synthetic lower-case hex, built at runtime; the exact byte strings
are in `payloads.txt` (escaped, values redacted).

| id | payload | landed `scan_bytes` | S140_A | realism |
|---|---|---|---|---|
| MF-1a..e | `x_gitlab_session=<H64>`, `2_…`, `__…`, `my_…`, `A_…` | no hit (full 39-pattern set) | hit | low-medium: the 64-hex value is real, the cookie name is not GitLab's |
| MF-2a | `_gitlab_session=<H64>012345678` (73 hex) | no hit | hit (first 64) | low: 73 hex is not a session value |
| MF-2b | `_gitlab_session=cell-12-<H64>0` (65 hex behind `cell-N-`) | no hit | hit (first 64) | low |
| MF-3a..f | non-ASCII window: `_gitlab_session（会话）=<H64>`, `_gitlab_session　会话　=<H64>`, 5×NBSP, 3×`→`, 3×em-space, 5×NBSP after `=` | no hit | hit under **rune** semantics only | low-medium: a localized capture with CJK parentheses |

**MF-1 — the keyword's left boundary.** `_GL_LB` (`:286`) requires the byte
before `_gitlab_session` not to be `[A-Za-z0-9_]`; S140_A's raw keyword group
has no left boundary. The 128-cell sweep quantifies the class exactly:

```
SWEEP pre-keyword  AGREE-HIT=65 S140-ONLY=63
  s140_only_bytes=[48-57, 65-90, 95, 97-122]   # [0-9A-Za-z_]
```

63 of 128 preceding ASCII bytes are scanner-miss ∧ S140-hit. This is round-98's
Q1 (`SentinelShapes.md`), unchanged by the landing. **Governance point, not a
code point:** the frozen counter *pins the miss as a requirement* — the probe's
negative `n-left-word` is `x_gitlab_session=<H64>`
(`.ufo/waves/round-99/c2/session-cookie-probe.py:53`) and the instrument's
selftest case `gl-session-ck-left-word` expects the empty set
(`capture-secret-scan.py:666`). Any future widening of the left boundary fails
K2 and the selftest, so this divergence cannot be fixed without re-freezing the
counter. Flagging for the integrator: the negative set is not S140-faithful
here, and K2 cannot distinguish "correctly refused" from "S140-divergent".

**MF-2 — the value's right boundary.** `(?![0-9a-f])` is stricter than S140,
which has no right boundary. The window absorbs 1-8 extra hex bytes, so
65-72 hex now *hits* (an improvement over round 98, which missed 65+); 73+
misses, and so does 65 hex behind a `cell-N-` prefix, because the fixed prefix
blocks the absorption. Round-98 Q2, narrowed from `65+` to `73+`.

**MF-3 — byte window vs rune window (conditional).** `[^\n]{0,8}` counts bytes;
Go's `.{0,8}` counts runes. A window of 3 CJK characters (9 bytes) or 5 NBSP
(10 bytes) is inside S140's budget and outside the landed one. Under the lane's
own byte model these are AGREE-MISS; under the engine that actually consumes
`gitlab.toml` they are MUST-FIX. I report them separately for that reason.

## REGRESSION — landed miss, round-98 instrument hit, S140_A miss

23 of 192 cells. None is a MUST-FIX (S140 misses all of them), but each is a
real 64-hex value the lane's gate detected yesterday and does not detect today.

| id | payload | landed | r98 | S140_A | realism |
|---|---|---|---|---|---|
| RG-1 | Netscape cookie jar, tab-separated: `.gitlab.com\tTRUE\t/\tTRUE\t0\t_gitlab_session\t<H64>` | no hit | **hit** | miss | **high** — standard curl/browser jar, a normal capture artifact |
| RG-2 | same jar, space-separated | no hit | **hit** | miss | high |
| RG-3 | `_gitlab_session_geo_<H64> <H64>` (space, no operator) | no hit | **hit** | miss | medium |
| RG-4 | `_gitlab_session_geo_<H64>\n=<H64>` | no hit | **hit** | miss | low |
| RG-5..8 | gap 9-12 spaces/tabs before or after the operator | no hit | **hit** | miss | low (S140-faithful bound) |
| RG-9..13 | newline/CRLF before or after the operator | no hit | **hit** | miss | low (S140-faithful) |

End-to-end, same file, same command shape (`cli-checks.txt`):

```
landed  --files fix/jar.txt  -> CAPTURE-SECRET-SCAN mode=files scanned=1 hits=0 files=0 rc=0
r98     --files fix/jar.txt  -> HIT shape=gitlab-session-cookie path=.../fix/jar.txt line=1
                                CAPTURE-SECRET-SCAN mode=files scanned=1 hits=1 files=1 rc=1
```

Cause: the landing replaced round-98's `[\s"'=:;]+` with `[^\n]{0,8}[:=][^\n]{0,8}`
instead of taking the union. Round-98's own remediation text named the
trade-off (`r98-remediation.txt`): "replace … with the union
`(?:[\s"'=:;]+|.{0,8}[:=].{0,8})` (keeps every current detection and adds the
S140 assignment gaps), **or** with `.{0,8}[:=].{0,8}` alone for strict S140
parity (which drops the current no-operator/newline detections)". The landing
chose the second. That is defensible against the claim, but it means the C2
probe's ten negatives (K2) are *structurally blind* to the loss: none of them
is a no-operator or jar form, so `negatives_extra=0` cannot move.

Impact: a curl cookie jar captured under `corpus/practice/*/evidence/` (an
`is_capture_path` hit, `capture-secret-scan.py:382-387`) with a live GitLab
session is now committed silently. That is the one finding here with a
high-realism exploit path.

## Routed qualifiers — both the scanner and S140_A miss

| id | payload | why | status |
|---|---|---|---|
| Q-1 | `_gitlab_session%3A<H64>` | percent-encoded operator; `[:=]` is literal in both | documented known limit (`capture-secret-scan.py:218`) |
| Q-2 | `{"name":"_gitlab_session","value":"<H64>"}` (HAR/JSON name-value object) | 11-byte gap, no operator within the window | **not** in the known-limits list (which names HAR name/value objects only for CloudFront signed cookies) — doc gap |
| Q-3 | `_GITLAB_SESSION=<H64>` and four other case variants | both are case-sensitive; the recorded S150 form carries no `(?i)` | routed; would become MUST-FIX if the generator emits `(?i)` |
| Q-4 | 63 hex | length | frozen negative N1 |
| Q-5 | upper-case hex | alphabet | frozen negative N3 |
| Q-6 | gap 9-12, newline, CRLF | S140's own bound | S140-faithful |

## What holds (verified, not assumed)

- The window is **S140-equivalent on ASCII**: `window-before-op` and
  `window-after-op` sweeps are 127/128 AGREE-HIT, and the single miss in each is
  byte `0x0a` (`SWEEP-BYTE … landed_miss_bytes=[10]`), which S140's `.` also
  refuses. Zero S140-only cells in either sweep.
- The value's right boundary is a superset of S140 for every ASCII trailing
  byte: `post-value` sweep 128/128 AGREE-HIT.
- The twelve round-98 MUST-FIX payloads all hit (`mustfix_hit=12/12`) and the
  ten frozen negatives all stay clean (`negatives_hit=0/10`) — K2 reproduced
  independently of the committed probe.
- `--selftest` at the landing prints `SELFTEST-RESULT pass cases=192`
  (`selftest-pin.txt`) — K1 reproduced.
- 39 cells that round 98 missed now hit (18 separators, 3 contexts, 11 `cell-`
  forms, 2 `_geo_` forms, 3 right-boundary forms, 2 non-ASCII windows) — the
  widening is real, not cosmetic.
- No catastrophic backtracking: the shape costs 0.080 s on a 1.1 MB adversarial
  line (`_gitlab_session` × 70 000, space-separated); the full 39-pattern gate
  costs 1.94 s on the same line, dominated by other shapes
  (`perf-and-sweepbyte.txt`).
- The instrument never prints a matched value, and `scan_bytes` does no I/O —
  nothing here mutates state, writes the cache, or leaks the secret into the
  receipt.

## Smallest remediation (reported, not applied — read-only seat)

Candidate **B**, the round-98 union with the whitespace run bounded and
newline-excluded, keeps S140 parity and recovers the jar at zero cost against
the frozen negatives:

```
_GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?"
        rb"(?:[^\S\n\"'=:;]{1,8}|[^\n]{0,8}[:=][^\n]{0,8})"
        rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])"
```

Measured (`remedy-run.txt`):

```
CAND A-union          mustfix=12/12 negatives=2/10   (hits N7 gap-9 and N8 newline)
CAND B-bounded-union  mustfix=12/12 negatives=0/10
CAND B-bounded-union  jar-tab hit=True  jar-space hit=True  geo-space hit=True
CAND B-bounded-union  nl-before-eq hit=False  gap9 hit=False   (S140-faithful)
```

For MF-1/MF-2/MF-3 the fix is a claim re-freeze, not a patch: widening the left
boundary or dropping `(?![0-9a-f])` breaks the frozen negatives/selftest, and
the rune window cannot be expressed in a bytes regex at all.

## Evidence index

- `landed-shape.txt` — instrument sha at HEAD and at the landing, the exact
  regex lines, the round-98 regex.
- `s140-source.txt` — S140:547-551, the knowledge-entry row, the S150 row.
- `r98-remediation.txt` — round-98's union-vs-parity trade-off, and its Q1/Q2
  routing.
- `payloads.txt` — every finding payload (values redacted to `<H64>`), with the
  landed, round-98, S140-byte and S140-rune hit sets.
- `matrix.py`, `matrix-run.txt`, `delta.txt` — the 192-cell matrix and deltas.
- `sweeps.py`, `sweeps-run.txt` — the four 128-cell sweeps and the 12/10 replay.
- `fuzz.py`, `fuzz-run.txt` — 4000 randomized payloads.
- `remedy.py`, `remedy-run.txt` — candidates A and B.
- `cli-checks.txt` — end-to-end `--files` runs, both instruments.
- `perf-and-sweepbyte.txt` — the miss byte in each window sweep and the
  adversarial-line timings.
- `selftest-pin.txt` — `SELFTEST-RESULT pass cases=192`.
- `receipts-selfscan.txt` — the landed scanner over this receipt directory:
  `scanned=16 hits=0 rc=0`.

Commands (all read-only; the scratch tree is removed after the seat):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
R=.ufo/waves/round-99/w1/SentinelCookie-receipts
S=$(mktemp -d); cp "$R"/*.py "$S"/
mkdir -p "$S/r98" && git show e2caf4a1:corpus/instruments/capture-secret-scan.py \
  > "$S/r98/capture-secret-scan.py"
sha256sum corpus/instruments/capture-secret-scan.py
python3 -B corpus/instruments/capture-secret-scan.py --selftest
python3 -B "$S/matrix.py" "$PWD" "$S"
python3 -B "$S/sweeps.py" "$PWD" "$S"
python3 -B "$S/remedy.py" "$PWD" "$S"
python3 -B "$S/fuzz.py"   "$PWD" "$S"
python3 -B corpus/instruments/capture-secret-scan.py --files "$S/fix/jar.txt"
```

VERDICT: C2 K1 (selftest 192 + instrument pin) — PASS: `SELFTEST-RESULT pass cases=192`, sha256 `8b338726…` at HEAD and at `a3db47e7`.
VERDICT: C2 K2 (12 round-98 MUST-FIX hit, 10 negatives clean) — PASS, reproduced independently: `mustfix_hit=12/12 negatives_hit=0/10`.
VERDICT: `gitlab-session-cookie` against S140_A — MUST-FIX: MF-1 left boundary (5 payloads; 63/128 preceding bytes), MF-2 right boundary (73+ hex and 65-hex behind `cell-N-`), MF-3 non-ASCII window (6 payloads, rune semantics only). None is high-realism; MF-1 is pinned as a required negative by the frozen counter.
VERDICT: coverage delta vs the round-98 instrument — REGRESSION: 23/192 cells lost, including the Netscape cookie jar (end-to-end: landed `hits=0 rc=0`, round-98 `hits=1 rc=1`); the C2 probe's ten negatives cannot see it.
VERDICT: window ASCII equivalence — PASS: 127/128 AGREE-HIT in both window sweeps, the only miss is `0x0a`, which S140 also refuses; zero S140-only cells.
VERDICT: smallest remediation — candidate B measured `mustfix=12/12 negatives=0/10` and recovers the jar; candidate A measured `12/12, 2/10`.
