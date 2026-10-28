# ScoutSibling — round-42 wave1 receipt

Seat: ScoutSibling (scout, leaf). Task: sibling-overlap scan for the two F25 lead-class doc families — OSV schema and CVE Record Format — across every sibling lane repo `/home/vgpnk/Projects/shokunin/*-shokunin` except kasegi-shokunin. Deliverable: `ScoutSibling.txt` beside this receipt.

## Deliverable

- File: `.ufo/waves/round-42/wave1/ScoutSibling.txt`
- Lines: 49 (wc -l)
- sha256: `163bf9371a8631c0dc6a6cc76dc9175ba5391dfec7b9f062389cf4941b1d5229`

## Frozen claim read

`claims.json` read first (sha of file read-only): C1 r42-closure.sh J1–J13 suite; C2 F25 lead screen from "machine-readable vulnerability-data standards the lane does not yet hold (lead class: the OSV schema or the CVE Record Format)" with the scout verifying "no lane row/entry already covers the chosen document". This seat's scan supplies the sibling-side of that no-overlap check.

## Scan surfaces and method

- Lane enumeration: `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` → 21 entries, minus kasegi-shokunin = 20 siblings.
- Per-lane surface check: every sibling has `corpus/SOURCES.md` and `corpus/knowledge/`; `SKILL.md` absent in `audio-shokunin` and `game-dev-2d-shokunin`; all 20 have `corpus/README.md` (frontier map analogue; no `PROVINCE.md`/`coverage*` at corpus root in any sibling).
- Greps (grep tool, case-insensitive, run against explicit per-lane path lists):
  1. `(?i)\bosv([-_]?schema)?\b|osv\.dev|ossf\.github\.io` over each sibling's whole `corpus/` + `SKILL.md` — hits only in kaidoku (S015 row, evidence JSON, lesson) and kotodama (linguistic OSV false positive).
  2. `(?i)cve[ _-]?record|cveSchema|schema\.cve\.org|cveproject|(?<![\w.])cve\.org` over whole `corpus/` + `SKILL.md` → **no matches** in any lane.
  3. `(?i)cve\.org|cveproject\.github\.io|CVE_Record_Format|cve[ -]record[ -]format` whole-corpus sweep → 1 hit: `revenger-shokunin/corpus/snapshots/claude-red-security.md:39` (MITRE CNA partner-list URL inside a captured third-party doc).
  4. Scoped re-runs restricted to `corpus/knowledge/` + `corpus/SOURCES.md` + `SKILL.md` for `(?i)\bosv\b|osv\.dev|ossf\.github\.io|\baffected\b` (81 files / ~126 hit lines, tallied per lane in the deliverable; `affected` is generic prose everywhere except the two named rows) and for the CVE term set → **no matches** in-scope.
  5. `(?i)\bosv\b|osv\.dev|ossf\.github\.io` scoped alone → only `kaidoku/corpus/SOURCES.md:21` and `kotodama/.../syntax-typology.md:11,32`.
  6. Wider ecosystem stems (`schema.osv|GHSA-|security/advisories|nvd.nist.gov|cve.mitre.org|cveawg|vulnogram|cve-services`) whole-corpus → additionally `kagi/corpus/lessons/round-28.md:43,151` (NVD REST JSON query, recorded NOT REGISTERED) and `mori/corpus/SOURCES.md:18` + mori evidence/lesson rows (GHSA advisory).
  7. Full term set over all 20 `corpus/README.md` frontier maps → **no matches**.
- LSP: not applicable — target is 20 heterogeneous prose/data lanes, not a code workspace; text grep is the correct instrument here (scout mandate allows literal grep when no semantic server answers the files).

## Findings (condensed; full file:line table in ScoutSibling.txt)

- CVE Record Format: zero substantive sibling ground — no in-scope hits in any of the 20 lanes; two informational out-of-scope artifacts only (kagi's rejected NVD-API lesson row, revenger's captured cve.org CNA-list link).
- OSV schema: the schema document itself is unheld fleet-wide, but substantive-adjacent ground exists — `kaidoku-shokunin/corpus/SOURCES.md:21` row S015 is a mined `api.osv.dev` OSV record with field-level lesson ground (`corpus/lessons/round-13.md:42,59`), and `mori-shokunin/corpus/SOURCES.md:18` row S012 holds a GHSA advisory bounding affected/patched versions.
- Named sibling ground the F25 pick must weigh: **kaidoku** (OSV record instance) and **mori** (GHSA advisory). Recommendation recorded in the deliverable: prefer the CVE Record Format; if OSV schema is chosen the lead must distinguish schema-document vs record-instance coverage.
- F24/RFC 9116: untouched (parked per freeze; never screened here).

## Tooling / network

- No installs or upgrades; no network fetches (read-only local grep). Tools: grep tool, `ls`, `find`, `wc`, `sha256sum` (system). pacman not run (host pause honored).

## Hygiene

- Writes this seat made: `ScoutSibling.txt` and this `ScoutSibling.md` under `.ufo/waves/round-42/wave1/` only. No lane/fleet/sibling source files edited; no mutating git/jj commands anywhere; no PATH-directory writes; no network.
- Scratch `/fast/scratch/hyaku/kasegi-r42/ScoutSibling` contained only transient command output; removed before yield.
- Remaining unknowns: none for the assigned question — whether the L1/lead treats kaidoku S015 + mori S012 as disqualifying adjacency for the OSV schema candidate is the lead's call; the evidence is named with file:line.
