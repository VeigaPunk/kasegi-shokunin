# ExecMirrorCensus — wave-1 receipt (round 26, kasegi)

Seat: `L1Kasegi26.ExecMirrorCensus` (leaf). Date: 2026-10-25 (UTC).
Scope: mirror census gate (pre-append) + C2 do-nothing control receipt.

## 1. Mirror build

- Destination: `/tmp/kasegi-r26-mirror`.
- Copied from lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`:
  - `corpus/` (full tree: `knowledge/`, `lessons/`, `instruments/`, `source-snapshots/`, `README.md`, `SOURCES.md`, `QUALITY.md`) — `cp -a`.
  - `SCORECARD.md`.
  - Nothing from `.ufo/waves` (nothing under `.ufo` copied at all).
- Verified post-copy: `corpus/` present, `SCORECARD.md` present, no `.ufo` in mirror.

## 2. Sources census — runs and exits

Script: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (read-only; writes only stdout).

### 2a. Literal command as assigned

```
sources-census.sh validate --root /tmp/kasegi-r26-mirror kasegi
```

Output:
```
ERROR: config not found: /tmp/kasegi-r26-mirror/shokunin.conf
ERROR: unknown lane (not a dir, not in conf or root): kasegi
```
Exit: **2**. The script resolves lane names via `$ROOT/shokunin.conf` or `$ROOT/*-shokunin` dirs; the mirror root is the lane itself (corpus/ at root) and contains neither, so lane `kasegi` is unresolvable under `--root <mirror>`.

### 2b. Mirror as explicit lane dir (working form)

```
sources-census.sh validate /tmp/kasegi-r26-mirror
```

Output:
```
kasegi-r26-mirror	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-r26-mirror	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-r26-mirror	ok	/tmp/kasegi-r26-mirror/corpus/SOURCES.md
```
Exit: **0**. Only pre-existing W04 warnings (S028/S029 duplicate-URL across scopes; W-codes do not affect status). All E-checks clean, including E11 used-by path existence inside the mirror.

### 2c. Live lane, claim-counter form (fleet root)

```
sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

Output:
```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```
Exit: **0**.

### 2d. Live lane, explicit lane dir

```
sources-census.sh validate /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Output: identical lines with lane `kasegi-shokunin`; Exit: **0**.

## 3. C2 do-nothing control receipt

Written to `.ufo/waves/round-26/c2-controls/do-nothing.json`.

| Measure | Command | Expected | Measured |
|---|---|---|---|
| Frontier admitted | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | 10 | **10** |
| Entries citing S04x | `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md \| wc -l` | 0 | **1** |
| Entries citing S041–S049 (round-26 rows only) | `grep -lE '^source: S04[1-9] ' corpus/knowledge/*.md \| wc -l` | — | **0** |

**Observation (counter overmatch):** the frozen counter `^source: S04[0-9] ` also matches round-25 `S040`, cited at `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:2`. The baseline therefore reads **1**, not 0, with zero round-26 work. The round-26-relevant measure (S041–S049) is **0**. No S041+ row exists in SOURCES.md; no staged entry is present in `corpus/knowledge/`. Frontier table holds 10 admitted rows (F01–F10).

Census exits for the receipt: mirror-literal 2, mirror-explicit-dir 0, live-fleet-root 0, live-explicit-dir 0.

## 4. Files changed

- `/tmp/kasegi-r26-mirror` (scratch mirror, outside repo).
- `.ufo/waves/round-26/c2-controls/do-nothing.json` (new).
- `.ufo/waves/round-26/wave1/ExecMirrorCensus.md` (this report).

## 5. Risks / blockers

- **C2 counter baseline discrepancy (reported, not fixed):** the frozen do-nothing expectation of 0 for `entries_citing_S04x` does not hold at baseline (measured 1 via S040 overmatch). This is a counter-definition property, not a round-26 adoption; the kill rule's substantive test (new S04x row appended without an admitted entry) is unaffected, and no S041+ citation exists. Flag for the L1/reviewer if the C2 after-value (>=1) is to be measured with the same counter — after adoption it will read >=1 for the right reason, but the "before" of 0 is already violated at freeze.
- The literal `--root <mirror> kasegi` form cannot resolve; if a mirror-root census with `--root` is required, the mirror must contain either a `shokunin.conf` or a `<lane>-shokunin` subdir. The explicit lane-dir form is the working equivalent and exits 0.
