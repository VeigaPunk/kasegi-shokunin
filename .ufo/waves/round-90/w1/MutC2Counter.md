# MutC2Counter — mutation test of the frozen C2 counter (round 90, wave 1)

Seat: MutC2Counter (attack, leaf). Subject: `.ufo/waves/round-90/c2/capability-check.py`
(sha256 `339c98019f3be9ed37c316025e9a05c749d0c997734a122ed434c9690c3e825d`, the
claims.json pin). Judged on the frozen predicate at the landing commit
`643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2` (base `6088c3eb…`, candidate
`0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf`). Findings below are
routed defects and qualifiers, never a re-score.

## Method

30 single-point mutants, each one exact-string substitution on the frozen counter with the
anchor count asserted `== 1` (mutant files live in scratch only; no counter copy, scanner copy
or fixture byte was written into the lane). Every mutant plus the pristine counter ran the
same 8-target panel, `python3 -B`, seed 9090, `--work` under scratch:

| target | invocation | expected |
|---|---|---|
| landed | `--rev 643ddb43 --base-rev 6088c3eb --instrument-sha256 0630d32b…` (no override) | rc 0 |
| forge:F1…F6 | same revs, `--instrument` each forgery built by `controls/c2-forgeries.py` from the frozen candidate | rc 1 |
| base | `--rev 6088c3eb --base-rev 6088c3eb` (no override, no-work control) | rc 1 |

Verdicts: **KILLED-BY-PANEL** = a forgery the pristine counter rejects is accepted (rc 0);
**SELF-BREAKING** = the mutant rejects the landed instrument; **SURVIVED** = landed passes,
base still fails, every forgery still rejected. The controls receipt ran the forgeries against
`--rev 6088c3eb` with the override; this panel runs them against the landed tree (same forgery
bytes, instrument resolved at `643ddb43`).

## Result

- Pristine baseline reproduces at seed 9090: landed `rc=0` (G0–G6 and P pass), base `rc=1`,
  all six forgeries `rc=1`. Catching limbs: F1[G1,G3,G4], F2[G1,G4], F3[G2,G6], F4[G3,G4],
  F5[G4,G5], **F6[G1]**.
- 30 mutants: **27 SURVIVED**, **2 KILLED-BY-PANEL** (M06, M07 — both weaken G1's leak
  conjunct), **1 SELF-BREAKING** (M24 — G4's allowlist digest binding, rejected by the landed
  instrument). 0 inconclusive.
- Exactly one forgery ever escapes: **F6-leaky**, from M06 and M07. No mutant lets F1–F5
  through.

| id | limb | mutation | landed | base | forgeries escaped | verdict |
|---|---|---|---|---|---|---|
| PRISTINE | – | pristine counter | 0 | 1 | none | baseline |
| M01 | G0 | drop missing-shapes conjunct | 0 | 1 | none | SURVIVED |
| M02 | G0 | drop extra-shapes conjunct | 0 | 1 | none | SURVIVED |
| M03 | G1 | drop rc==3 conjunct | 0 | 1 | none | SURVIVED |
| M04 | G1 | drop not-written conjunct | 0 | 1 | none | SURVIVED |
| M05 | G1 | drop named-shape conjunct | 0 | 1 | none | SURVIVED |
| M06 | G1 | drop leak conjunct entirely | 0 | 1 | F6-leaky | KILLED-BY-PANEL |
| M07 | G1 | leak: stderr only (drop stdout) | 0 | 1 | F6-leaky | KILLED-BY-PANEL |
| M08 | G1 | leak: stdout only (drop stderr) | 0 | 1 | none | SURVIVED |
| M09 | G1 | named: drop trailing-space anchor | 0 | 1 | none | SURVIVED |
| M10 | G1 | named: accept any INTAKE-REFUSED line (wrong shape passes) | 0 | 1 | none | SURVIVED |
| M11 | G2 | drop kept conjunct | 0 | 1 | none | SURVIVED |
| M12 | G2 | drop rc==3 conjunct | 0 | 1 | none | SURVIVED |
| M13 | G2 | kept: existence only, drop byte equality | 0 | 1 | none | SURVIVED |
| M14 | G3 | drop instrument rc==0 conjunct | 0 | 1 | none | SURVIVED |
| M15 | G3 | drop base rc==0 conjunct | 0 | 1 | none | SURVIVED |
| M16 | G3 | drop byte-equality conjunct | 0 | 1 | none | SURVIVED |
| M17 | G3 | same: existence only, drop base byte comparison | 0 | 1 | none | SURVIVED |
| M18 | G4 | drop allowed rc==0 conjunct | 0 | 1 | none | SURVIVED |
| M19 | G4 | drop allowed-written conjunct | 0 | 1 | none | SURVIVED |
| M20 | G4 | drop other-path rc==3 conjunct | 0 | 1 | none | SURVIVED |
| M21 | G4 | drop other-path not-written conjunct | 0 | 1 | none | SURVIVED |
| M22 | G4 | drop never-allowed rc==3 conjunct | 0 | 1 | none | SURVIVED |
| M23 | G4 | drop never-allowed not-written conjunct | 0 | 1 | none | SURVIVED |
| M24 | G4 | allowlist digest not bound to matched bytes (`0`*64) | **1** | 1 | none | SELF-BREAKING |
| M25 | G5 | drop rc==3 conjunct | 0 | 1 | none | SURVIVED |
| M26 | G5 | drop not-written conjunct | 0 | 1 | none | SURVIVED |
| M27 | G5 | drop G5 limb entirely | 0 | 1 | none | SURVIVED |
| M28 | G6 | drop G6 limb entirely | 0 | 1 | none | SURVIVED |
| M29 | P | drop P limb | 0 | 1 | none | SURVIVED |
| M30 | P | drop sha256 case folding | 0 | 1 | none | SURVIVED |

## Why 27 survive: the panel is redundant by construction

F6 is the only **single-limb** forgery. Every other forgery is rejected by two or three
limbs, so a one-conjunct weakening is masked by a sibling limb. Of the counter's 22
single-conjunct weakenings, the panel detects **one** (G1 leak, stdout channel) and the landed
run detects **one more** (G4 allowlist digest binding); 20 have no killing input at all.

| limb | conjuncts | detected by the panel | detected by the landed run | note |
|---|---|---|---|---|
| G0 | missing, extra | 0 | 0 | static: no forgery alters the scanner's shape list |
| G1 | rc, written, named, leak | leak (stdout channel only) | 0 | stderr channel unobservable (M08) |
| G2 | rc, kept-exists, kept-bytes | 0 | 0 | F3 unlinks, so existence alone catches it (M11, M13) |
| G3 | instrument rc, base rc, byte-equality | 0 | 0 | no forgery writes different clean bytes (M16, M17) |
| G4 | allowed rc, allowed-written, other rc, other-written, never-allowed rc, never-allowed-written | 0 | digest binding (M24) | each sub-check masked by a sibling |
| G5 | rc, not-written | 0 | 0 | F5 also fails G4 (M27) |
| G6 | rc | 0 | 0 | F3 also fails G2 (M28) |
| P | sha256 equality | 0 | pin is the landed run itself (M29, M30) | static |

Degradations the survivors expose (catching set after mutation): M05/M10 leave F1 caught only
by [G3,G4] — a gate that refuses with the wrong shape name is not caught by G1; M11 leaves F3
caught only by [G6]; M27 leaves F5 caught only by [G4]; M28 leaves F3 caught only by [G2].
M24 additionally makes G4 fail for F3 and F6 (a wrong-digest allowlist refuses the allowed
capture), which is why the landed run rejects it.

## Escapes, per mutant

- **M06** (leak conjunct dropped): F6-leaky returns rc 3, writes nothing and names the shape,
  so G1 passes; no other limb reads the refusal text → counter `rc=0`. F6 is the only forgery
  whose sole detector is G1.
- **M07** (leak checks stderr only): F6 echoes the matched line to stdout, `leak=False`, G1
  passes → counter `rc=0`.
- No other mutant lets any forgery through; F1–F5 remain caught by their sibling limbs in every
  case.

## Do the 11 plants cover each pattern's boundaries? No — one representative per shape

G0 compares **names only** (`set(shapes) - set(P)`), so losing an alternation branch inside a
pattern leaves G0 and all 11 plants green. Each plant exercises one branch and sits 1.1–6.7×
above its regex floor (only `aws-access-key-id` is exactly at its floor). Untested boundaries:

| shape | planted representative | untested branches / forms | untested floor |
|---|---|---|---|
| private-key | `BEGIN <name> PRIVATE KEY` (name random: EC at 9090, RSA at 1/2/3, EC at 7; OPENSSH never drawn in 5 seeds) | empty-middle PKCS#8 header; lowercase header (scanner misses, real PEM is uppercase) | n/a |
| op-ref | 20-char path | – | 3-char floor |
| bearer | 32 alnum | lowercase `bearer`; base64 values with `+` or `/` (scanner misses: the 16-char run breaks) | 16 floor |
| authorization | 30 alnum after `Authorization: ` | `bearer ` sub-form; JSON-quoted; `=` separator | 16 floor |
| credential | `api_key=` + 28 | `apikey=`, `api-key=`, `secret=`, `token=`, `password=`, JSON-quoted (all hit the scanner; none planted) | 16 floor |
| session-cookie | `session_cookie=` + 28 | `session-cookie=`, `sessioncookie=` | 16 floor |
| aws-sts-session-token | `=` query form, 64 chars | header `: ` form; JSON-key form | 20 floor (16–19 alnum still hit `credential`) |
| aws-access-key-id | `AKIA` or `ASIA` + 16 (one per run: ASIA at 9090/1/3, AKIA at 2/7) | the other prefix per run; 17-char id (scanner misses) | exactly at floor |
| gcs-signed-url-signature | `=` + 128 lowercase hex | header form; JSON-key form (uppercase hex is matched) | 64 floor |
| azure-sas-signature | `sv=`-first, `&amp;`, 44 chars | `sig=`-first; `&` and `\u0026` separators; internal `%26` (documented limit) | 40 floor |
| cloudfront-signed-url-signature | `Signature=`-first, `&amp;`, 60 chars, 14-char key-pair id | key-pair-id-first; `&` and `\u0026`; lowercase names (correctly miss) | 40 floor; 8-char key-pair-id floor |

Two further plant-set facts, both evidenced:

1. **The leak conjunct is vacuous for `private-key`.** `plants()` returns `sec=None` for that
   shape, so `leak = bool(sec) and …` is always False. F6-leaky echoes the matched line for
   10 of 11 shapes and its G1 bad list omits `private-key` (receipt
   `pristine-forge-F6-leaky.log`): a refusal that echoed the private-key header alone would
   pass G1 and escape the panel entirely.
2. **The aws-sts plant also matches `credential`** (pattern order puts `credential` first), and
   G1's `named` check accepts any number of shapes in any position — a refusal naming the wrong
   shape is only caught because F1 also fails G3/G4 (M10).

## Routed defects (for round-91 controls; not a re-score)

- **D1 — panel redundancy.** Add single-limb forgeries so each conjunct has a detector: a gate
  that returns rc 3 and writes nothing but names no shape (G1-named); a gate that writes a new
  `--out` and returns rc 3 without deleting it (G1-written); a gate that refuses a new `--out`
  but exits 0 (G1-rc); a gate that writes different bytes for clean inputs (G3 byte-equality); a
  gate that overwrites an existing file with different bytes but returns rc 3 (G2 byte-equality);
  a gate that lets an allowed value through at any path (G4 other-path, split rc/written); a gate
  that fails open only on a bad allowlist (G4 never-allowed, split rc/written); a gate that
  inlines the patterns instead of loading the scanner (only G5 would catch it; today F5 is also
  caught by G4). Each forgery must change only the targeted limb's observable — e.g. exit 0 or
  write only for a *new* `--out`, since a blanket write-then-refuse or refuse-with-0 also fails
  G2 and would not isolate G1's conjunct.
- **D2 — plant branch/floor coverage.** Add one plant per alternation branch and one per floor
  (`floor-1` + `floor`) from the table above; derive the branch list from the regex source, not
  from a hand list (same lesson as G0's name derivation).
- **D3 — private-key leak vacuity.** Give the private-key plant a leak value (the header text)
  so the leak conjunct is live for all 11 shapes, and add a private-key-only leaky forgery.
- **D4 — G0 is name-only.** A scanner that drops a branch inside a pattern passes G0 and every
  plant; G0 cannot see branch loss.
- **D5 — seed dependence.** `private-key` name and `aws-access-key-id` prefix are one draw per
  run; the three-seed claim does not guarantee OPENSSH or PKCS#8 coverage (OPENSSH absent at
  seeds 9090/1/2/3/7). Either plant all branches or assert the drawn branch set.

## Reproduction

```
python3 -B .ufo/waves/round-90/w1/MutC2Counter-receipts/repro-mutants.py --work <scratch>   # 30 mutants x 8 targets, ~80 s
```

`repro-mutants.py` is a harness written by this seat (not a copy of the counter or scanner); it
reads the frozen bytes read-only and writes only under `--work`. Re-run from the shipped receipt
into a fresh work dir it reproduced `summary.txt` identically (diff over
mutant/limb/verdict/landed/base/escapes: empty). The plant/branch/floor probe
harness is scratch-only: its fixtures are credential-shaped by design (that is what it probes),
and this round forbids fixture bytes under `w1`; `probe.txt` is its scanner-clean output. To
re-create it, import `capture-secret-scan.patterns()` from a `git archive` of the landing rev
and feed the labelled variants listed in the boundary table above, printing labels, lengths and
shape names only.

## Evidence and restoration

- Frozen counter sha256 `339c9801…` and candidate `0630d32b…` read before and after the run;
  unchanged. No lane file outside `.ufo/waves/round-90/w1/` was written; no git/jj write.
- Receipts in `.ufo/waves/round-90/w1/MutC2Counter-receipts/`: `matrix.tsv` (248 rows),
  `summary.txt`, `mutants.tsv` (id, limb, description, mutant sha256, anchor count, substitution),
  `probe.txt`, `pristine-landed.log`, `pristine-forge-F6-leaky.log`, `M06-forge-F6-leaky.log`,
  `M07-forge-F6-leaky.log`, `M24-landed.log`, `repro-mutants.py`.
- Scratch `/fast/scratch/hyaku/kasegi-r90/MutC2Counter/` is deleted before yield.
