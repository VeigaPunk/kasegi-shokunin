# ScoutCensusWarnings — census baseline + duplicate-URL risk for the five new rows

Seat: `L1Kasegi25.ScoutCensusWarnings` (scout, read-only). Round 25, wave 1.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. No production file was edited.
Date of run: 2026-10-25 (UTC).

Adopted rows under test (id mapping from `RowsScratch`, document-order, not arithmetic):

| new lane id | staged id | URL | source file |
|---|---|---|---|
| S036 | S055 | `https://cybozu.co.jp/company/security-policy/` | `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` |
| S037 | S056 | `https://cybozu.co.jp/products/bug-bounty/faq/` | same |
| S038 | S057 | `https://pepabo.com/contact/vulnerability-reporting/` | same |
| S039 | S060 | `https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html` | same |
| S040 | S068 | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | same |

## a) Baseline (before the append)

Command (exactly as the item specifies):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

Full stdout:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

`EXIT=0`.

Companion `census` mode on the same lane (same shell), `EXIT=0`:

```
kasegi	rows	35
kasegi	tier.A	32
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	23
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	35
FLEET	tier.A	32
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	23
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
```

This matches the frozen `frontier_step.census_before` in `.ufo/waves/round-25/claims.json`
(exit 0, rows 35, malformed 0, tier A=32 B=1 C=2, mined=23 queued=9 rejected=3, W04 x2 on
S028/S029 pre-existing). No drift.

Instrument health: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` →
96 `killed`, 0 `SURVIVED`, `exit=0`. The checker is not silently blind (see the positive
controls in §d).

## b) Duplicate-URL check, per new URL

Normalization the census applies (`url_of()` in `sources-census.sh`): first `https?://…`
token of the `source` cell, drop `#fragment`, drop one trailing `/`, drop the scheme,
lowercase the **host only** — the path keeps its case. The key is therefore *host+path*,
never host alone.

| new id | normalized key the census will compute | occurrence in `corpus/SOURCES.md` (pre-append) |
|---|---|---|
| S036 | `cybozu.co.jp/company/security-policy` | **none** |
| S037 | `cybozu.co.jp/products/bug-bounty/faq` | **none** |
| S038 | `pepabo.com/contact/vulnerability-reporting` | **none** |
| S039 | `www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html` | **none** |
| S040 | `www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | **none** |

Evidence for "none": `grep -n 'cybozu\|pepabo\|hitachi\|cisco' corpus/SOURCES.md` prints
nothing and exits 1; the full normalized dump of all 35 registry URLs (S001–S035) contains no
`cybozu`, `pepabo`, `hitachi` or `cisco` host at all. Host-sharing with an existing row:
**no** — not one of the five hosts appears anywhere in the registry, so the question of a
host-level collision does not arise for this append.

Fleet-wide (`shared` mode, 56 shared URLs across all lanes): no line matches
`cybozu|pepabo|hitachi|cisco`, so none of the five is already held by a sibling lane either.
(`validate` would not have reported that anyway — see §c, W04 is file-local.)

Staged-cell hygiene that also bears on E01/E09 (checked on the five staged rows, `NF=13` each):
no literal or escaped `|` in any cell (`grep -c '\\|'` = 0), `recheck` is already the schema
cadence `180d` (not prose), `status=mined`, `kind=docs`, `tier=A`.

## c) Expected post-append warning set

Simulated by copying the lane's real `corpus/SOURCES.md` + `corpus/knowledge/` into a scratch
root and appending the five normalized rows (`status=mined`, `opened=2026-10-25`,
`recheck=180d`, `used-by` = the two round-25 entries), then running the census with
`--file <mirror>/corpus/SOURCES.md`.

**Result with both round-25 entries present — the expected state:**

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/tmp/census-B-entries-present-95s_0vag/corpus/SOURCES.md
exit= 0
```

**Expected post-append warning set = {W04 S028, W04 S029} — unchanged, i.e. the append adds
ZERO new W-codes and ZERO E-codes.** Post-append totals: `rows 40`, `tier.A 37`, `tier.B 1`,
`tier.C 2`, `status.mined 28`, `status.queued 9`, `status.rejected 3`, `FLEET.missing 0`,
census `exit=0`.

**Conditional risk — E11, and it is a sequencing risk, not a URL risk.** E11 ("used-by path
missing on disk") resolves each `used-by` path as `$lane_dir/$path`, and it only inspects
`status=mined` rows. If the five rows are appended **before** the two entries exist, validate
returns exit 1 with exactly:

```
file	E11	S036 missing used-by corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
file	E11	S037 missing used-by corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
file	E11	S038 missing used-by corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
file	E11	S039 missing used-by corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
file	E11	S040 missing used-by corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

(pasted verbatim from the run; the five lines are the only new output — the two pre-existing
W04 lines also print, in the same order as in §a.)

Neither entry exists on disk at the time of this report
(`ls corpus/knowledge/ | grep -i 'vendor\|crosswalk'` → empty; 35 entries). **Append order
required for C2's "census exit 0": the two entry files land first, the five rows after.**

Two further E-code traps the L1 must avoid, both already excluded by the `RowsScratch` spec:

- **E11 from copied staged `used-by`.** All five staged rows name entries that do not exist in
  this lane (`program-quirks-2026-10-23-amendment.md`, `japanese-vendor-disclosure-policies-2026-10-23.md`,
  `authorization-safe-harbor-and-scope-2026-10-23-amendment.md`,
  `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md`, `vendor-cvd-policy-crosswalk-2026-10-23.md`
  — all five verified MISSING). Copying the staged `used-by` cell verbatim would emit one E11
  per path and fail the claim.
- **E09 from prose `recheck`.** A `recheck` of the form `90d — re-open the page …` is neither
  an ISO date, nor `NNd`, nor a symbolic cadence → E09. The staged cells are already `180d`;
  keep `180d`.

`--file` mode note for the `RowsScratch` seat: with `--file`, the lane dir becomes
`dirname(file)/..`, so a mirror that lacks `corpus/knowledge/` reports **E11 for every mined
row in the file (all 35–40 of them)** — that is a mirror-placement artifact, not a defect in
the rows. Either place the mirror as `<tmp>/corpus/SOURCES.md` with `corpus/knowledge/`
present, or run the authoritative validate against the real lane after the append.

## d) What each relevant code actually keys on (read from the script, `sources-census.sh:620-670`)

- **W04** `same URL across scopes` — fires when the normalized URL was already seen in this
  file **and** the `(url, scope)` pair is new. Warning only; never changes exit status.
- **E04** `duplicate URL+scope (no supersedes)` — same `(url, scope)` pair, row not
  `rejected`, an earlier non-rejected row holds that pair, and `teaches` does not contain
  `supersedes S###`. Error → exit 1.
- **W01** tier-C mined with non-`—` used-by · **W02** rejected row with `teaches` < 8 chars ·
  **W03** mined row with `used-by = —` — none applicable (all five are tier A, mined, with a
  real used-by).
- **E11** used-by path missing on disk, per comma-separated path, mined rows only.
- **E12** row-shaped source outside `## Registry` — the five must go inside the registry table,
  not after it.
- **Warnings never change status** (script header lines 33–35 and the selftest
  `W-only-registry-exit-0` case); only `E[0-9]+` and overdue findings set exit 1.

Positive controls proving the check is live (scratch mirrors, since removed):

| control | constructed row | observed |
|---|---|---|
| W04 control | new row reusing S001's exact URL under a different scope | `file	W04	S036 duplicate url www.first.org/cvss/v4.0/user-guide across scopes`, exit 1 |
| E04 control | same URL **and** S001's scope, `teaches` without `supersedes` | `file	E04	S037 duplicate url www.first.org/cvss/v4.0/user-guide within scope CVSS v4 scoring guidance for severity communication`, exit 1 |
| host-only control | new row on S001's host, different path (`/cvss/v4.0/metrics`) | **no W04/E04**, `file ok`, exit 0 |

The host-only control is the direct answer to "shares a host in a way the census would flag":
**it would not** — host equality alone is invisible to the census; only the normalized
host+path string is compared. The S036/S037 pair (both `cybozu.co.jp`, distinct paths) is
therefore safe for the same reason.

## e) Bottom line for the L1

1. Append adds no new warning and no new error: post-append warning set stays
   `{W04 S028, W04 S029}`, validate `exit 0`, census `rows 40 / tier.A 37 / status.mined 28`.
2. Prerequisite, in order: `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`
   and `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` must exist on disk
   before the rows are appended, or the append turns exit 0 into exit 1 with 5 x E11.
3. Do not carry the staged `used-by` cell or any prose `recheck` across; use the two round-25
   entry paths and `180d`.
4. Nothing else in the five rows touches a code path: ids S036–S040 are free (registry max is
   S035), opened 2026-10-25 is not in the future, kind/tier/status are in enum, no cell carries
   a pipe.

## Remaining unknowns

- The exact final `scope`/`anchor`/`teaches` wording from `RowsScratch` was not available when
  this ran; the simulation used the staged cells for those columns. Irrelevant to the verdict:
  no existing row holds any of the five URLs, so W04/E04 cannot fire regardless of scope
  wording, and scope text affects nothing else in the code set.
- Whether the L1 appends S040 (Cisco) at all: `claims.json` lists it as `planned_reject`
  (S068 unreachable this round) while `RowsScratch`/`CollisionGuard` map it to S040. If S040 is
  dropped, the warning set is unchanged (still `{W04 S028, W04 S029}`) and the E11 exposure
  shrinks by one row; the crosswalk entry would then need its own used-by re-pointing.

Tooling: none installed or upgraded for this item (read-only seat; bash, gawk, python3 stdlib
only). All scratch mirrors were created under `/tmp` and removed.
