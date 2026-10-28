# R44Exec8 — source snapshot manifests and entries: nearby unused candidate domains

Seat: leaf executor (read-only reconnaissance). Assigned item: "Inspect source snapshot manifests and entries for
nearby unused candidate domains; no external writes."
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `5ab3a60`, claims commit `6631401`, working tree dirty
(round-44 admission in flight). No production/shared file was written by this seat; only this report.

Axes: depth:verifiability, coverage.

---

## 0. What was measured, and how

All commands below were run from the lane root unless a `--root`/`--manifest` path is given. Scratch:
`/fast/scratch/hyaku/kasegi-r44/R44Exec8` (`HYAKU_SCRATCH` was unset in this seat's shell; base resolved from the
fleet convention `/fast/scratch/hyaku` recorded in `.ufo/prompts/kaisegi-round-*.md`, e.g. `HYAKU_SCRATCH=/fast/scratch/hyaku`).
No external fetch was made (opening candidates is the scout seats' item), no pacman, no tool install, no git/jj mutation.

```sh
# 1. every manifest, all quote pins and digests
for m in corpus/source-snapshots/round-*/manifest.json; do
  python3 corpus/instruments/source-recheck.py --manifest "$m" >/dev/null; echo "$m exit=$?"; done
# 2. manifest <-> registry binding, orphans, provenance
python3 corpus/instruments/capture-binding-check.py --scratch "$TMPDIR"
# 3. registry capture-path references vs files/digests  (inline python, read-only)
# 4. C2 counters, claims string and control string separately
grep -cE '^\| F[0-9]+ \| admitted \|'            corpus/README.md
grep -cE '^\| F[0-9]+ \| .* \| admitted \|'      corpus/README.md
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l
# 5. frozen-base replay of the same counters
git show 5ab3a60:corpus/README.md | grep -cE '^\| F[0-9]+ \| .* \| admitted \|'
git show 5ab3a60:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
git ls-tree -r --name-only 5ab3a60 corpus/knowledge | grep -c '\.md$'
# 6. census
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

---

## 1. Manifest layer: intact, 58/58 bound, 20/20 recheck exit 0

`source-recheck.py` over all twenty manifests: **20/20 exit 0**. Last line of each run (round-44 included):

```
round-43/manifest.json: exit=0 S067:Q6 OK occurrences=1 anchor=103-ok
round-44/manifest.json: exit=0 S069:Q3 OK normalized=markup-whitespace occurrences=1 anchor=70-ok
```

`capture-binding-check.py` (rules A per-file binding, B registry binding, C provenance, D integrity):

```
MANIFEST round-44 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=58 with_url=58 with_fetched_utc=20 with_archival=38 snapshot_dirs=20 manifest_dirs=20
      missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=58 bound=58 unbound=0
binding_exit=0
```

Independent cross-checks (inline python over `corpus/SOURCES.md` + manifests):

| check | result |
|---|---|
| registry rows | 70 (`S001`–`S070`; 56 mined, 14 rejected) |
| mined rows with ≥1 lane capture | 56 / 56 — none missing |
| rows with no capture at all | exactly the 14 rejected: `S022 S024 S026 S027 S028 S056 S058 S059 S061 S062 S065 S066 S068 S070` |
| manifest ids with no registry row | none |
| ids captured more than once | `S041` only (`round-26`, `round-28`, `round-30`; all three digests `e18acbf9…` = same bytes) |
| `corpus/source-snapshots/round-N/Sxxx.txt` references inside registry cells | 19 references, 19 present, 19 digests match the recorded prefix, 0 bad |
| manifest files present / digest match / anchor resolves | 58 / 58 / all anchored quotes resolve (hand re-verified separately for S069, §3) |

Structural fact worth recording for the planner: **the capture layer's invariant is "mined ⇒ captured, rejected ⇒
uncaptured"**. It holds at this revision, so a future admission that names a document without landing a capture
will be the first violation and will be visible (`records=` will not grow while a row does).

---

## 2. C2 after-state, measured (and the frozen counter defect)

Working tree, this instant:

| counter | base `5ab3a60` | `6631401` (HEAD) | working tree |
|---|---|---|---|
| claims C2 string `^\| F[0-9]+ \| admitted \|` | **0** | **0** | **0** |
| control string `^\| F[0-9]+ \| .* \| admitted \|` | 25 | 25 | **26** |
| `^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|` | 68 | 68 | **70** |
| `find corpus/knowledge -maxdepth 1 -name '*.md' \| wc -l` | 62 | 62 | **63** |

**V1 (claim-level, verifiability).** `claims.json` C2 `counter` uses
`grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md`. The frontier table's column 3 is the status cell
(`| F26 | <topic> | admitted | ... |`), so that regex returns **0 in every state** — at the frozen base, at HEAD, and
in the after-state. It cannot discriminate do-nothing from the round-44 move; the `controls/do-nothing.txt` string
(`^\| F[0-9]+ \| .* \| admitted \|`, 25 → 26) is the discriminating one. The C2 after-state is reachable and reached,
but the counter printed in the claim does not show it. This is a defect in the frozen claim text, not in the landed work.

**V2 (state is uncommitted).** `git status --porcelain corpus/`:

```
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/instruments/knowledge-expected.txt
?? corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
?? corpus/source-snapshots/round-44/
```

HEAD still reads 25/68/62. C2's counter greps the working tree, so it passes pre-commit; C1's claim text
("one committed read-only counter over committed lane evidence") is commit-scoped while C2's is not. Stated as a
fact, not a verdict: C2's numeric after-state exists only in the dirty tree at this measurement.

Registry row that carries the admission (`corpus/SOURCES.md:75`) is complete on every C2-required cell:
`tier=A`, `status=mined`, `opened=2026-10-28`, `recheck=180d`, `used-by=corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`,
anchor pins `corpus/source-snapshots/round-44/S069.txt`, `sha256 0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2`,
`quotes Q1-Q3 at lines 61-72`. Reject row `S070` (`corpus/SOURCES.md:76`, tier C, rejected, flip recorded).
Frontier row `F26` at `corpus/README.md:628`, coverage-map row at `:624`. Knowledge ledger
`corpus/instruments/knowledge-expected.txt` = 63 entries + 2 comment lines, set-difference against
`corpus/knowledge/*.md` is empty in both directions (no drift).

Census, read-only, matches the frozen baseline exactly:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

The two W04 lines are the same two the do-nothing control recorded, so the census adds no new warning class.

---

## 3. The round-44 manifest record: what it pins, what it leaves to an untracked file

Current `corpus/source-snapshots/round-44/manifest.json` record (read after the integrator's mid-session update that
added `url`/`capture_url`/`http`):

```json
{"id":"S069","url":"https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules",
 "capture_url":"https://bughunters.google.com/rest/v1/articles/about/rules/google-friends/cloud-vulnerability-reward-program-rules",
 "http":{"status":200,"final_url":"…/rest/v1/articles/…"},
 "kind":"text","fetched_utc":"2026-10-28T18:53:38Z","path":"S069.txt",
 "sha256":"0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2",
 "bytes":45681,"snapshot_bytes":45681,"lines":1132,
 "quotes":[Q1 anchor 61, Q2 anchor 62, Q3 anchor 70]}
```

Verified against the file and the recon artifacts:

```sh
sha256sum corpus/source-snapshots/round-44/S069.txt
# 0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2
sha256sum .ufo/waves/round-44/source-recon/S069-body.txt
# 0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2   (byte-identical to the capture)
sha256sum .ufo/waves/round-44/source-recon/S069.txt
# 7e2004ba30638ba8ce2a123d6385ade62685e148c661b46ffd93519db0bc4609   (raw API JSON, 47136 bytes)
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069
# S069:sha256 OK ; Q1/Q2/Q3 OK normalized=markup-whitespace occurrences=1 anchor=61/62/70-ok ; exit 0
```

Extraction relation proved exactly (inline python): `json.loads(raw)["body"].encode() + b"\n" == capture`
(body 45680 bytes, 1131 newlines; capture 45681 bytes, 1132 newlines). The capture is the API `body` field with one
trailing newline, not the served response.

**V4 (provenance gap).** The record carries no `raw_sha256`, `raw_bytes`, `status` or `tool`, unlike the immediately
preceding round-43 record (`round-43/manifest.json` S067 carries `raw_sha256`). Consequently the served API response
(47136 bytes, sha256 `7e2004ba…`) and the body→capture newline append are evidenced **only** by the untracked file
`.ufo/waves/round-44/source-recon/S069.txt`. If that directory is not committed or is deleted on scratch cleanup, a
reader can still re-run `source-recheck` (local bytes) but can no longer tell what the server served, how the capture
was derived, or that `bytes=45681` is the extracted body rather than the response.

**V5 (schema heterogeneity, no instrument enforces it).** Across 58 records: only 2 carry `kind` (S069 `text`,
S067 `html`); 13 carry `raw_sha256`; 20 carry `fetched_utc`, 38 fall back to `archival:true`; the round-44 manifest has
no `purpose` field (18 of 20 do). `source-recheck` enforces id/stem/digest/quote/anchor; `capture-binding-check`
enforces url-binding/status/orphans/provenance-UTC. Neither enforces a common record schema, so provenance richness
drifts downward by round with no counter showing it.

**V3 (entry quotes beyond the pins).** The new entry cites seven loci; the manifest pins three. Hand-verified against
`S069.txt` this seat:

| entry citation | S069.txt content | verdict |
|---|---|---|
| `:9-11` scope sentence | L9-11 `In principle, any [Google Cloud](…) product or web service … is intended / to be in scope.` | resolves (quote drops the markdown link markup) |
| `:61-62` strictly limited | L61-62 `The Google Cloud VRP scope is strictly limited to Google-owned infrastructure / and services.` | resolves |
| `:62-63` strictly prohibited | L62-63 `… testing customer resources / is strictly prohibited:` | resolves |
| `:65-72` written authorization + ineligibility | L65-67 `No Unauthorized Scanning or Access … without written authorization from the customer is prohibited.`; L70-72 ineligibility | resolves |
| `:68-69` customer domains | L68-69 `Customer-owned domains include, not limited to, *.bc.googleusercontent.com and *.appspot.com` | resolves |
| `:70-72` reward ineligibility | L70-72 `the report is ineligible for a reward if finding or verifying it involved testing or accessing customer resources` | resolves |
| `:78-86` multi-tenant | L78-86 sandbox/sole-tenant/local-repro instruction | resolves |

None of these five unpinned citations is instrument-checked by the entry's own documented recheck command
(`--source S069` re-checks Q1-Q3 only; run, exit 0). One is unpinnable as written: `:9-11` contains
`[Google Cloud](https://cloud.google.com/products?e=48754805)` in the capture, and `source-recheck.normalize()`
strips only `<u>`/`</u>` markup, so a manifest quote of that sentence would fail unless the quote text omits the
link (as the entry does) — the entry's range citation is the right form, the manifest pin count is the residual gap.

---

## 4. Nearby unused candidate domains (the item's deliverable)

Classification rule used, because C2 demands a **newly opened tier-A source row** plus a knowledge entry, and
`capture-binding-check` B5 requires the manifest `url` to equal the row's source-cell `https://` token byte-for-byte:

> A candidate can satisfy C2 only if (a) no existing registry row already names that document, (b) a capture lands in a
> round directory and is recorded in that directory's manifest, (c) the row's URL and the manifest `url` agree.
> A domain that is merely an unmined section of an already-registered source fails (a).

### 4A. Genuinely uncovered domains that sit inside the already-captured S069 — real gaps, but they cannot be C2's new row

`S069.txt` has 28 headings; the F26 entry and the S069 anchor cite **one** section (`Do Not Test Customer Projects &
Resources`, L59-88) plus the scope sentence (L9-11). Coverage probe over `corpus/knowledge/*.md` and `SKILL.md`
(case-insensitive file counts):

| domain | locus | probe hits | note |
|---|---|---|---|
| post-compromise stop boundary ("Hard Stop … Borg") | `S069.txt:89-103` — L91-92 not permitted to test Borg; L95-97 immediate stop; L98-100 no lateral movement; L101-103 maximum-potential-impact evaluation keeps Safe Harbor | `Borg` 0, `lateral movement` 0, `post-compromise` 0, `maximum potential impact` 0 | uncovered |
| responsibility for automated agents/tools | `S069.txt:105-112` — "You are responsible for all actions and network traffic generated by any automated scanners, fuzzers, custom scripts, or AI agents you run" | `automated scanner` 0, `fuzzer` 0, `AI agent` 1 (only `cve-bench-agent-exploitation-benchmark.md`, a benchmark claim, not liability) | uncovered |
| vendor root-in-cloud validation protocol | `S069.txt:448-526` — Path A challenge service account L456, Path B infrastructure RCE L493, validation criteria L513 | `challenge service account` 0, `root-in-cloud` 0 | uncovered |
| non-qualifying third-party components | `S069.txt:114-141` | `third-party software` 1 (`vendor-third-party-finding-coordination.md` — MSVR intake ground, not non-qualifying rules) | partially adjacent |
| reward tiering / precedents / upgrades / downgrades | `S069.txt:231-985` | covered by S043/S044/S049/S050/S051 entries | **not a gap** — do not mine |

Consequence for the planner: 4A items are the cheapest *substantive* ground still open in the lane, but a future
F-row built on them **cannot** be counted as C2's "newly opened tier-A source row" — S069 already exists. They can
only produce a second entry citing S069 (knowledge +1, source rows +0), or they need a *different* first-party
document stating the same domain (which then must be opened and captured).

### 4B. Same-site neighbour already screened and refused

`S070` (`corpus/SOURCES.md:76`, tier C, rejected 2026-10-28, no capture): the Bug Hunters rules *directory* —
"the page's accessible body is a JavaScript shell and its metadata is a directory welcome, not an operative program
rule; flip: the page itself exposes a located, program-specific rule absent from the linked policy text."
Unused by construction; admissible only on that flip.

### 4C. Leads the lane itself records as unopened (`corpus/SOURCES.md:106-108`)

| lead | URL | state |
|---|---|---|
| Google Big Sleep reporting beyond the Project Zero-linked tracker | `https://goo.gle/bigsleep` (first DeepMind URL 404'd) | never opened, no capture, no row |
| ISO/IEC 29147 and 30111 standard records | `https://www.iso.org/standard/72311.html`, `https://www.iso.org/standard/69725.html` | never opened; the lane's open view of this ground is already S041 付録6 and S040's ISO-alignment cells, so a record page may add metadata only |
| UK AI Security Institute, rate of autonomous AI cyber-capability progress | `https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing` | never opened; adjacent to F02/F03 (S009-S012, S025) and to 4A's agent-responsibility domain |

These are the only recorded candidates that can still produce a *new* registry row without re-mining an existing
source. Opening them is scout territory (R44Scout1/2/3/7), not this seat's; none was fetched here.

### 4D. Rejected format-family rows adjacent to F21/F23/F25 — flip-gated, capture-less

`S056` CISA min-VEX, `S058` OpenVEX, `S059` CycloneDX v1.7 (superseded by captured S060), `S061` CISA VEX status
justifications PDF, `S062` CSAF v2.1 CSD04, `S065` OSV schema, `S066` NVD API schema, `S068` GHSA entry. Every one
carries a recorded flip condition and **no lane capture**, so re-admission would need both the flip and a fresh
capture recorded in a manifest (B5 + rule A).

### 4E. Orphan capture (coverage ambiguity, not a candidate domain)

`corpus/source-snapshots/round-26/S040-live.txt` is present but named by no `sources[].path` and not declared in an
`orphans` list; the binding instrument reports it as `orphans=1 orphan=S040-live.txt` (exit still 0). It is the same
residue round-33 R6 recorded; it is inert but means the round-26 directory's file count (2) is not its record count (1).

---

## 5. Do-nothing discrimination

| observation | do-nothing (base `5ab3a60`) | this tree | discriminating? |
|---|---|---|---|
| F admitted rows (control string) | 25 | 26 | yes |
| SOURCES registry rows | 68 | 70 | yes (S069 mined + S070 reject) |
| knowledge entries | 62 | 63 | yes |
| `corpus/source-snapshots/round-44/` | absent | `S069.txt` + `manifest.json`, recheck exit 0 | yes |
| F admitted rows (claims string) | 0 | 0 | **no** (V1) |
| census exit / W04 pair | 0 / S028+S029 | 0 / S028+S029 | no |
| binding instrument | n/a (no round-44 dir; records 57) | records=58 bound=58 unbound=0 orphans=1 | yes, by the S069 record |
| orphan `S040-live.txt` | present | present | no |

---

## 6. Findings, stated without inflation

1. **C2's numeric after-state is reached in the working tree and is instrument-verified**: F26 row, tier-A mined S069
   row citing the new entry, capture + manifest rechecking exit 0, one recorded reject (S070), knowledge 63, census
   exit 0 with the pre-existing two W04 warnings. Nothing in this seat's evidence shows C2's *substance* failing.
2. **C2's frozen counter string is defective** (V1): it reads 0 at base, at HEAD, and in the after-state. The
   after-state is only visible through the control's `.*` form. Fixing the claim's counter text is a claim-level
   correction; the landed work does not need to change for it.
3. **C2's after-state is uncommitted** (V2); HEAD reads 25/68/62. A C2 counter over the working tree passes
   before anything is committed, unlike C1's commit-scoped evidence.
4. **The S069 manifest pins only 3 of the entry's 7 citations** (V3); the other five resolve by hand but are not
   instrument-checked, and `:9-11` is unpinnable as written because of the inline markdown link.
5. **S069's fetch provenance is thinner than the round-43 record's** (V4): no `raw_sha256`/`raw_bytes`, and the raw API
   response digest (`7e2004ba…`, 47136 B) plus the body+newline derivation live only in an untracked recon file.
6. **Four substantive domains are still uncovered inside an already-mined source** (§4A), and the only candidates that
   can still yield a *new* tier-A row are the three unopened leads (§4C) — an F-row built from S069's unmined sections
   would fail C2's "newly opened source row" clause.
7. **Layer invariants hold**: mined ⇒ captured (56/56), rejected ⇒ uncaptured (14/14), 58/58 records bound, 19/19
   registry capture references resolve with matching digests, 20/20 manifests recheck exit 0.

No falsification of C2's substance was found; the falsifiable defects found are in the claim's counter string, the
commit-scope of its evidence, and the provenance completeness of the newest manifest record.

## 7. Limitations

- No external fetch: candidate admissibility for §4C was not tested live (scout-owned); §4C entries are the lane's own
  recorded leads, not opened sources.
- C1 was not measured here: `corpus/instruments/r44-routed-defects.py` exists and
  `grep -Ec '^6\. Routed defects|^[0-9]+\. \*\*' corpus/lessons/round-43-verifier-spotcheck.md` = 8 at this tree, but
  running the C1 counter (lane export + baseline) belongs to the C1 seats; no C1 claim is made from this seat.
- The round-44 manifest changed under this seat mid-session (the `url`/`capture_url`/`http` block appeared between two
  reads); every verification above was re-run against the post-change bytes.
- Census, entry and counter checks read the working tree, not a committed revision (V2).
- `source-recheck` verifies captured bytes, not current upstream availability; no freshness claim is made for S069.

Scratch `/fast/scratch/hyaku/kasegi-r44/R44Exec8` removed on exit (see §8).

## 8. Cleanup

```sh
rm -rf /fast/scratch/hyaku/kasegi-r44/R44Exec8
```
