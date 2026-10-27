# CritSync — round-41 wave-1 C2 instrument-chain integration attack

Seat: CritSync (critic, leaf). Item: attack the C2 instrument chain integration with four
landing-failure scenarios; run the relevant instrument on a scratch mirror demonstrating
the red; confirm the kill rule fires in each case. Judged axes: depth:verifiability, coverage.

## Method and provenance

- Scratch mirror `$M=/fast/scratch/hyaku/kasegi-r41/CritSync/mirror` = byte copy of the
  lane corpus at the claims-freeze state. Verified before copying: `git diff --stat
  fbba3d96cdf8d37c1ea41304a1ba35691329684b HEAD -- corpus` is empty and
  `git status --porcelain -- corpus` is clean, so the copied tree equals the frozen base
  (`5b29ea14`/`fbba3d9` corpus content). Copied: `corpus/knowledge/`, `corpus/instruments/`
  (minus `__pycache__`), `corpus/source-snapshots/`, `corpus/README.md`, `corpus/SOURCES.md`.
- Mirror adaptation: every knowledge entry's `recheck:` line begins
  `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`; in the mirror copies only, that
  prefix was rewritten to `cd $M` (same adaptation the audit's own selftest fixtures use),
  so the strict `cdroot` limb holds against the mirror. No other byte was changed.
- Simulated "good" C2 landing on the mirror (the state sibling seats are building):
  README F24 row (`admitted`, entry cell `knowledge/rfc-9116-security-txt.md`) inserted
  directly after the F23 row; SOURCES.md S063 row appended inside the Registry table
  (`kind spec, tier A, status mined, opened 2026-10-27, recheck 180d, used-by
  corpus/knowledge/rfc-9116-security-txt.md`); capture
  `corpus/source-snapshots/round-41/S063.txt`; `manifest.json` record
  `{id S063, path S063.txt, sha256 <real>, url <registry url>, fetched_utc, quotes Q1 Q2}`;
  knowledge entry `corpus/knowledge/rfc-9116-security-txt.md` with the provenance trio
  (`source: S063` / `verified-at: 2026-10-27` / `recheck: ... source-recheck.py
  --manifest corpus/source-snapshots/round-41/manifest.json --source S063`) and a prose
  citation of S063; `knowledge-expected.txt` sorted-insert of the new entry (60 lines).
- Capture fetch record: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0
  https://www.rfc-editor.org/rfc/rfc9116.txt` -> HTTP 200, 45,129 bytes, fetched
  2026-10-27T08:26:39Z; sha256 `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9`,
  1,122 lines. Quotes pinned: Q1 = the Expires staleness sentence (L343-L345, occurrences=1),
  Q2 = the Contact encryption recommendation span (L300-L301, occurrences=1).
- Tooling: no installs/upgrades were needed or performed; instruments ran as committed.
  Host versions: Python 3.14.8, GNU bash 5.3.20, GNU Awk 5.4.1.
- Each scenario ran on a fresh `cp -a` of the good mirror (`s1`..`s4`) with the same
  cd-prefix rewrite applied to the copy, so every red below is attributable only to the
  named mutation.

## Good-mirror baseline (all four instruments green — the exact C2 after-state)

```
$ python3 corpus/instruments/frontier-recheck-count.py --root mirror | tail -2
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
entries=27 pass=27 exit=0
$ python3 corpus/instruments/capture-binding-check.py --root mirror | tail -1
records=55 bound=55 unbound=0
$ python3 corpus/instruments/recheck-audit.py --root mirror --quiet | tail -2
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0
$ bash scripts/sources-census.sh validate --file mirror/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r41/CritSync/mirror/corpus/SOURCES.md   (exit 0)
```

Counting commands on the good mirror: frontier rows 24; registry rows 63; S063-mined awk
1; entries citing `^source: S063` 1; knowledge files 60.

## Scenario 1 — entry lands but knowledge-expected.txt is NOT synced

Mutation: delete the new entry's line from `s1/corpus/instruments/knowledge-expected.txt`
(list stays at 59 entries; the entry file itself is present and well-formed).

```
$ grep -vc "^#" s1/corpus/instruments/knowledge-expected.txt
59
$ python3 s1/corpus/instruments/recheck-audit.py --root s1 --quiet
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=59 missing=0 unexpected=1 exit=1
exit=1
# rest of chain stays green:
$ python3 s1/corpus/instruments/frontier-recheck-count.py --root s1 | tail -1
entries=27 pass=27 exit=0
$ python3 s1/corpus/instruments/capture-binding-check.py --root s1 | tail -1
records=55 bound=55 unbound=0
```

Verdict: RED. The stale list makes the landed entry `unexpected`; the audit exits 1 with
`expected=59`, never reaching the claimed `expected=60 missing=0 unexpected=0 exit=0`.
Kill rule FIRES — limb: `recheck-audit expected!=60`. Integration note: the harness and
binding checks stay green; the committed expected list is the lone sentinel for this
defect class, so the L1 must land `knowledge-expected.txt` in the same commit as the entry.

## Scenario 2 — manifest record carries a wrong sha256

Mutation: flip the first hex char of the S063 record's sha256 in
`s2/corpus/source-snapshots/round-41/manifest.json` (`79d1…` -> `09d1…`); capture bytes
untouched.

```
$ python3 s2/corpus/instruments/source-recheck.py --manifest s2/corpus/source-snapshots/round-41/manifest.json --source S063
S063:sha256 MISMATCH expected=09d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9 actual=79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9
exit=1
$ python3 s2/corpus/instruments/frontier-recheck-count.py --root s2
FAIL     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=1    problems=recheck-exit-1
entries=27 pass=26 exit=1
exit=1
# capture-binding stays GREEN (it binds id/url/provenance, never hashes the capture):
$ python3 s2/corpus/instruments/capture-binding-check.py --root s2 | tail -1
records=55 bound=55 unbound=0
exit=0
# recheck-audit stays GREEN (a failing recheck line is class "gated" and still passes form):
$ python3 s2/corpus/instruments/recheck-audit.py --root s2 --quiet | tail -2
lines=60 total=60 pass=60 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0
exit=0
```

Verdict: RED via two independent limbs. Kill rule FIRES — limbs: `its capture failing
source-recheck` (the named per-source counting command
`source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063`
prints MISMATCH exit 1) AND `harness not entries=27 pass=27 or no PASS F24 line`
(`problems=recheck-exit-1`). Integration finding (correction to the item's parenthetical):
the item predicted "(binding unbound)" — that is NOT what happens. `capture-binding-check.py`
never hashes capture content (its selftest fixtures literally use `"sha256": "0"*64`), so it
stays `records=55 bound=55 unbound=0 exit=0`; `recheck-audit.py` also stays green because a
non-zero recheck run is class `gated` and passes the frozen form limbs (fail-closed count
rises 24 -> 25). A sha256 slip is caught only by `source-recheck.py` directly and by the
frontier harness executing the entry's recheck line — both are in the C2 counting command
set, so the kill rule still fires, but a seat running only binding+audit would see all-green.

## Scenario 3 — README F24 row admitted but the entry filename differs from the row

Mutation: `mv s3/corpus/knowledge/rfc-9116-security-txt.md
s3/corpus/knowledge/rfc9116-security-txt.md` (hyphen dropped — the plausible two-seat
divergence). The README F24 row still names `knowledge/rfc-9116-security-txt.md`. The
expected list is synced to the DELIVERED name so the audit limb is isolated out.

```
$ python3 s3/corpus/instruments/frontier-recheck-count.py --root s3
FAIL     F24  knowledge/rfc-9116-security-txt.md                   ids=-              exit=-    problems=missing-entry
entries=27 pass=26 exit=1
exit=1
# rest of chain (green — the row<->filename binding is the harness's lone sentinel):
$ python3 s3/corpus/instruments/recheck-audit.py --root s3 --quiet | tail -2
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0
exit=0
$ python3 s3/corpus/instruments/capture-binding-check.py --root s3 | tail -1
records=55 bound=55 unbound=0
exit=0
$ python3 s3/corpus/instruments/source-recheck.py --manifest s3/corpus/source-snapshots/round-41/manifest.json --source S063 | tail -1
S063:Q2 OK occurrences=1
exit=0
```

Verdict: RED. Kill rule FIRES — limb: `harness not entries=27 pass=27 or no PASS F24 line`
(the harness's rule-E fail-closed `missing-entry` names the row id and the row's path; there
is no `PASS F24` line and the summary is `entries=27 pass=26 exit=1`). Integration note:
every other instrument stays green — the audit sees 60 files with a synced expected list,
binding sees a bound record, and direct source-recheck passes on the delivered file. Only
the README row cell -> entry path binding catches this; the row cell and the on-disk
filename must be landed by the same hand (or the divergence reds F24 exactly here).

## Scenario 4 — two seats deliver conflicting S063 registry rows (duplicate id)

Mutation: insert a second, conflicting `| S063 |` row directly after the first in
`s4/corpus/SOURCES.md`: seat B's source cell names
`https://datatracker.ietf.org/doc/html/rfc9116` (vs seat A's
`https://www.rfc-editor.org/rfc/rfc9116.txt`), status `mined`, opened 2026-10-27.

```
$ python3 s4/corpus/instruments/capture-binding-check.py --root s4 | tail -2
FAIL rule=dup-id record=S063 rows=2 dir=round-41
records=55 bound=54 unbound=1
exit=1
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file s4/corpus/SOURCES.md
file	W04	S028 ... (pre-existing)
file	W04	S029 ... (pre-existing)
file	E03	S063 duplicate id
exit=1
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' s4/corpus/SOURCES.md   # want 63
64
$ awk -F'|' '/^\|[[:space:]]*S063[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if(s=="mined") n++} END{print n+0}' s4/corpus/SOURCES.md   # want 1
2
# harness and audit stay GREEN (the harness never reads SOURCES.md):
$ python3 s4/corpus/instruments/frontier-recheck-count.py --root s4 | tail -1
entries=27 pass=27 exit=0
exit=0
$ python3 s4/corpus/instruments/recheck-audit.py --root s4 --quiet | tail -1
expect=present expected=60 missing=0 unexpected=0 exit=0
exit=0
```

Verdict: RED. Kill rule FIRES — three limbs at once: `its manifest record unbound` /
`capture-binding unbound!=0` (`FAIL rule=dup-id record=S063 rows=2`, `bound=54 unbound=1`,
exit 1 — `bind_record` rejects any id with more than one registry row regardless of the
URLs); `census exit!=0 or a new W/E code` (new E-code `E03 S063 duplicate id`, exit 1);
and the counting commands themselves miss the after-state (`registry rows 64 != 63`,
`S063-mined 2 != 1`). Integration note: the frontier harness (27/27) and the recheck audit
(exit 0) are both registry-unaware and stay green — capture-binding-check and the fleet
census are the sentinels for registry-row uniqueness, so a conflicting second S063 row is
caught before it could be rationalized as "one row opened this round".

## Verdicts and impacted axes

All four kill-rule scenarios FIRE on the committed instruments as they stand at the
claims-freeze base; no instrument edit is needed for any of them, and none of the four
reds is a tradeoff the canonical Rust judge must reject — they are fixable landing defects
the chain already catches:

| # | Defect | Red instrument(s) | Kill limb(es) fired | Green (gaps) |
|---|--------|-------------------|---------------------|--------------|
| 1 | expected list not synced | recheck-audit exit 1 (`expected=59 unexpected=1`) | `recheck-audit expected!=60` | harness, binding |
| 2 | manifest sha256 wrong | source-recheck MISMATCH exit 1; harness `FAIL F24 recheck-exit-1` (27/26) | `capture failing source-recheck`; `harness not 27/27 / no PASS F24` | binding (content-blind), audit (gated) |
| 3 | row/entry filename divergence | harness `FAIL F24 missing-entry` (27/26) | `harness not 27/27 / no PASS F24` | audit, binding, source-recheck |
| 4 | duplicate S063 rows | binding `dup-id` (unbound=1); census `E03`; counts 64/2 | `manifest record unbound`; `capture-binding unbound!=0`; `census exit!=0 / new W/E code` | harness, audit |

Impacted axes: depth:verifiability (each red is a named, reproduced kill-rule firing with
the failing limb identified — and scenario 2 corrects the item's routing assumption with
evidence), coverage (all four F24 landing paths are shown to be guarded, and the
sentinel-per-defect map tells the L1 exactly which instrument must see each byte it lands).

Smallest safe correction: none to the instruments — the corrections land on the build side:
(1) land `knowledge-expected.txt` in the same commit as the entry; (2) treat
`source-recheck.py --source S063` (not capture-binding) as the sha256 gate, with the
harness as the executing backstop; (3) land the README F24 row cell and the entry filename
from one hand; (4) open exactly one S063 row — capture-binding and census E03 make a
second row fatal, not advisory.

Scratch cleanup: `s1`-`s4`, `mirror`, and `*-transcript.txt` under
`/fast/scratch/hyaku/kasegi-r41/CritSync/` were removed before yield (I6 guard).
