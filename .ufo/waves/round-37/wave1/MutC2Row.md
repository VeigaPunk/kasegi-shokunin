# MutC2Row — S054 registry-row mutation probe (round 37, C2 coverage)

Seat: `MutC2Row` (mutation-tester), leaf. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
probed at lane head `b362068195d5489aa94b31e6ec8f880c367e0ba0` (claims-erratum-1). Every write was
scratch; the lane file was never modified (restoration evidence §5).

## 1. Probe subject

The planned S054 registry row, taken verbatim from `.ufo/waves/round-37/wave1/ScribeRowS054.md`
line 11 — the erratum row shape (source URL `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`,
per claims-erratum-1 @ `b362068`; L1 re-confirmed mid-probe).

- Row sha256: `83020b30ca32fd49c2a1cd85864792d01004a594b59ad2f13fb83e1e6f734f03` (866 B with trailing
  newline) — byte-identical to the sha the ScribeRowS054 receipt publishes.
- Detector: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (806 lines; the lane has no
  `scripts/` dir), invoked as `validate --file <fixture>/corpus/SOURCES.md`. Exit contract per its
  header: 0 = clean or warnings, 1 = any E-finding, 2 = usage/env. No tool was installed or
  upgraded; bash + gawk 5.4.1 (system) only.

## 2. Fixture (isolated scratch, mutated in place)

`/fast/scratch/hyaku/kasegi-r37/MutC2Row/root/`:

- `corpus/SOURCES.md` — working-tree copy (sha256 `2ff7818ad2179c1f8ecf89262e3f8a84a585dfb4f64bbc1fa0e7dbc3be2465fe`,
  53 rows, `| S053 |` at line 59) with the planned row inserted after it (row becomes line 60).
  Pristine fixture hash `ead94cc69c09afc2da890c7124f09852b4da26880de193e782dfba03eaf6e671`.
- `corpus/knowledge/` — copy of the lane's 48 entries **plus a fixture-only stub**
  `ssvc-stakeholder-specific-vulnerability-categorization.md` so the pristine row's `used-by`
  resolves (the real entry is the entry seat's deliverable and did not exist at head `b362068`).

`--file` mode resolves each `used-by` path against the file's grandparent dir (script line ~490:
`dir_abs=$(realpath "$(dirname file)/..")`, E11 test `[ ! -e "$dir/$path" ]`), so all disk checks
stayed inside the fixture.

## 3. Results

Baseline first (a baseline failure would make every mutant inconclusive); then one smallest-point
mutation at a time, detector run, exact-byte restore, hash check.

| # | mutant (single-point) | census exit | findings naming S054 | verdict |
|---|---|---|---|---|
| 00 | none — pristine planned row | 0 | none (`file ok`; only pre-existing W04 S028/S029) | baseline clean |
| a | tier `A` → `C` (tier inflation) | **0** | `W01 S054 tierC mined used-by=corpus/knowledge/ssvc-…md` | **SURVIVED as exit-0** — flagged in warning text only |
| b | kind `docs` → `community`, tier stays `A` | 1 | `E10 S054 community-at-A` | killed |
| c1 | `recheck` cell (`90d`) deleted → NF=12 | 1 | `E01 S054 fields=10` | killed |
| c2 | literal `\|` injected into `teaches` → NF=14 | 1 | `E01 S054 fields=12` | killed |
| d | status `mined`, used-by target absent (stub removed) | 1 | `E11 S054 missing used-by corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` | killed |
| e | row duplicated, adjacent, both in-Registry | 1 | `E03 S054 duplicate id` + `E04 S054 duplicate url certcc.github.io/SSVC/tutorials/ssvc_overview within scope …` | killed |

Planned-state counters (`census --file`, baseline): `rows 54 · tier.A 51 · tier.B 1 · tier.C 2 ·
mined 42 · queued 9 · rejected 3` — i.e. the row moves the registry 53→54 exactly as C2 claims.

## 4. Transcripts (validate --file, verbatim; W04 S028/S029 lines elided as `…` — they are the frozen-claim's disclosed pre-existing warnings and appear identically in every run)

**00 pristine**
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r37/MutC2Row/root/corpus/SOURCES.md
EXIT=0
```

**(a) tier C**
```
…W04 ×2 elided…
file	W01	S054 tierC mined used-by=corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
file	ok	/fast/scratch/hyaku/kasegi-r37/MutC2Row/root/corpus/SOURCES.md
EXIT=0
```

**(b) community at tier A**
```
…W04 ×2 elided…
file	E10	S054 community-at-A
EXIT=1
```

**(c1) missing column**
```
…W04 ×2 elided…
file	E01	S054 fields=10
EXIT=1
```

**(c2) extra pipe**
```
…W04 ×2 elided…
file	E01	S054 fields=12
EXIT=1
```

**(d) mined + used-by missing on disk**
```
…W04 ×2 elided…
file	E11	S054 missing used-by corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
EXIT=1
```

**(e) duplicate id**
```
…W04 ×2 elided…
file	E03	S054 duplicate id
file	E04	S054 duplicate url certcc.github.io/SSVC/tutorials/ssvc_overview within scope CERT/CC's own SSVC documentation: decision-point-based prioritization for vulnerability management
EXIT=1
```

## 5. Restoration evidence

- After **every** mutant the fixture `SOURCES.md` was restored from the saved pristine copy and
  re-hashed: `ead94cc6…e671` matched each time (driver aborts on mismatch; none occurred). The (d)
  stub was recreated and its existence re-checked (`no` during the probe, `yes` after).
- Final re-run on restored bytes: exit 0, output byte-identical to baseline, `diff vs pristine: empty`.
- Lane `corpus/SOURCES.md` before probe and after: `2ff7818ad2179c1f8ecf89262e3f8a84a585dfb4f64bbc1fa0e7dbc3be2465fe`;
  `git status --porcelain -- corpus/SOURCES.md` → 0 lines. No lane, fleet, sibling-lane or
  source-tree write; no mutating git command; scratch dir removed after this receipt was filed.

## 6. Findings for the L1

1. **Five of six probes are killed by exit code** (E10, E01×2, E11, E03+E04): the census contract
   hard-rejects kind/tier-A conflict, malformed row width, dangling `mined` used-by, and duplicate
   ids for this row.
2. **Coverage finding (a): tier inflation is warn-only.** `S054` at tier C still yields exit 0
   (W01); the round's required exit-0 census would not fail a lane that landed the row as tier C.
   Recorded as a detector-coverage fact, not a contract change — W-codes "never change status" by
   design (script header). If the round wants tier inflation of *this specific admitted row* to be
   machine-rejected, that is a new check decision above my seat.
3. The planned row itself is clean under the full validator at head `b362068` (baseline exit 0 with
   only the two frozen-claim-disclosed W04 warnings), and its disk-binding hinge (E11) is live: the
   row may only land `mined` once
   `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` exists.

Report: `.ufo/waves/round-37/wave1/MutC2Row.md`
