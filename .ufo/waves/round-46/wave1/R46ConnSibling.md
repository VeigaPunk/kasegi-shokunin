VERDICT: INFO

# R46ConnSibling — sibling-overlap scan for S073 / F28 and the C1 re-grounds

Scope: read-only scan of the fleet (kasegi excluded) for other lanes declaring or carrying work on (a) GitHub private vulnerability reporting, GHSA, SECURITY.md / security.txt reporting surfaces, and (b) gated-recheck or re-grounding of lost-base kasegi entries (`claim-package-contract.md`, `claim-gates.md`). No file was edited, no git/jj command was run, no scratch directory was created. The only write is this Report file.

Result in one line: no sibling lane has a live round-46 claim on GitHub private vulnerability reporting, on GHSA reporting flows, or on re-grounding the two C1 entries. Four adjacency or dependency points exist (kake security.txt, kaika F3 publishability flag, kotoba citation routing, revenger read-only note). Each is listed below with its boundary.

## Collision 1 — kake security.txt entry (adjacent surface, no claim collision)

Surface: reporting-channel discovery. `kake-shokunin/corpus/knowledge/security-txt-publishing.md` (verified-at 2026-10-22, recheck 90d) serves `/.well-known/security.txt` from GitHub Pages. The file's `Contact` field is what points a researcher to a channel. GitHub's served body is quoted at `security-txt-publishing.md:99-100`: "GitHub's retained body has one `Contact` (`https://hackerone.com/github`)". That is a different channel from GitHub's built-in private reporting that F28 covers.

Boundary: `kake-shokunin/PROVINCE.md:289-292` says "Vulnerability handling itself stays out of province: report intake, triage, remediation, disclosure timing, bounty and policy operation, and whether any named contact channel works, are not kake's ground." F28 (reporter flow of the repository advisory form) falls on the kasegi side of that line. F28 must not describe `security.txt` fields or `Contact` ordering, which are kake's ground.

Round-46 status: kake's round-46 work does not touch it. Commands and output:

    grep -rIl -i -E "security|vulnerab|disclos" kake-shokunin/.ufo/waves/round-46/w1 kake-shokunin/.ufo/waves/round-46/attack kake-shokunin/.ufo/waves/round-46/build
    -> kake-shokunin/.ufo/waves/round-46/w1/ConnectorSiblingOverlap.md
    -> kake-shokunin/.ufo/waves/round-46/build/connector-overlap.md
    grep -n -i -E "security|vulnerab|disclos|GHSA|reporting" kake-shokunin/.ufo/waves/round-46/w46-spec.json kake-shokunin/.ufo/waves/round-46/make_w46_spec.py kake-shokunin/.ufo/waves/round-46/residual-spec.json
    -> (no output)

Both hits are kake's redirect and commit-citation sibling-overlap scan. They name "security" only in a sibling header description (`ConnectorSiblingOverlap.md:53`: "Domain specialist — bounty & security research"). They are not a security.txt or reporting claim. The kake round-46 spec's C1 and C2 are robots/redirect matrix work (`w46-spec.json:10,27,91`).

Risk to F28: low. The only shared word is "reporting channel". Keep F28 on the reporter flow; cite kake only as "separate from `security.txt` discovery, see kake's entry", never as a source for the channel.

## Collision 2 — kaika F3 publishability flag on claim-package-contract.md (same file as C1; open flag, no claim)

`.ufo/waves/kaika-w3/publish-lane-security.md:86-90` (dated 2026-10-19) flags **F3**: "kasegi knowledge text carries private engagement identifiers". It lists `corpus/knowledge/{claim-package-contract,ev-model,intake-and-finalize,...}.md` and `corpus/SOURCES.md` as carrying lost-tree claim and VDP directory names. The flag was routed "to the content/metadata lane to decide publishability".

The follow-up at `publish-lane-security.md:104-124` concluded: "5 of 6 identifiers are literally public already. The sixth is not literally present publicly, but both of its components are public ... the merge adds an **un-braced respelling**, not a new identifier disclosure."

Why it matters for C1: C1 edits `claim-package-contract.md`. Its re-ground rows cite committed anchors (`path:line`, token). If a row quotes a lost-tree `claims/...` or VDP directory name, it reintroduces the F3 class. Constraint: C1 rows cite only committed `path:line` and tokens and never a `claims/<...>` or platform/vendor/finding-class path from the lost tree. This is a constraint, not a claim collision.

Round status: no kaika round-46 prompt exists (`ls -t .ufo/prompts | grep -i kaika` returns only `*-round-1-continuation-kaika.md`). The F3 item is dated and not an active claim.

## Collision 3 — kotoba citation routing points at claim-gates.md (dependency, not a claim)

`kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json` carries kasegi-token rows with `"resolved": true`, for example `"lane": "kasegi", "line": 154, "token": "corpus/knowledge/claim-gates.md"`. `kotoba-shokunin/corpus/knowledge/fleet-skill-audit-round5.md:60` has the row `kasegi L86 | corpus/knowledge/claim-gates.md resolves under the skill repo ... ambiguous cwd`.

Why it matters: kotoba resolves the token path. C1 is append-only on `claim-gates.md` (`## Re-ground (round 46)` section, recheck line rewritten only on the re-grounded entry). Path existence and the token survive. The risk would be a rename or a deletion of `claim-gates.md`, which C1 does not do. Note for the C1 author: keep the file at `corpus/knowledge/claim-gates.md`.

Round status: kotoba round-46 and round-47 prompts do not reference kasegi (`grep -n claim-gates kotoba-shokunin/.ufo/waves/round-47` returned nothing).

## Collision 4 — revenger R62ConnectKasegi (stale, read-only; not live)

`revenger-shokunin/.ufo/waves/round-62/build/R62ConnectKasegi.md:13` says "`kasegi-shokunin/corpus/knowledge/claim-gates.md` has **no** deployed/bytecode/contract/pin content". It is a dated (2026-10-21) read-only probe. Revenger's live waves are round-69 through round-72 (`ls revenger-shokunin/.ufo/waves | sort -V | tail -4` → `round-69 ... round-72`). Their `grep -rIl -i -E "kasegi|claim-package|claim-gates|GHSA|security\.txt|private vulnerab|vulnerability reporting"` returned only `round-69/R69MisrootSweep.md` and `round-69/R69ConnectorOverlap.md` (kasegi listed as a lane name, no claim). Not a collision.

## Id-token overlap — S073 (per-lane namespace, no content collision)

`S073` is used by other lanes for unrelated sources:
- `chousa-shokunin/corpus/SOURCES.md:83`: `| S073 | GNU coreutils sha256sum(1) manual ...`
- `tameshi-shokunin/corpus/SOURCES.md:82`: `| S073 | Command line and environment (CPython 3.15.0 docs) ...`

Kasegi's own registry is free at S073: `grep -cE '^\|[[:space:]]*S073[[:space:]]*\|' kasegi-shokunin/corpus/SOURCES.md` → `0`, and the highest id is `072` (`grep -oE '^\|[[:space:]]*S[0-9]{3,}' ... | sort -n | tail -1` → `072`). C2's `S073` cannot collide with a sibling row because each lane has its own `corpus/SOURCES.md`. Do not cross-reference a sibling `S073` from F28. The chousa round-47 assimilation census (`chousa-shokunin/.ufo/waves/round-47/assimilation/census-after-append.txt:3`) reports `S073 duplicate url` only within chousa's own scopes.

## Round-46/47 "Re-ground each entry" template (shared text; no sibling action on kasegi entries)

The same clause appears in the in-flight prompts for chousa, kaidoku, kama, kengaku, mado, mori, tameshi and tsukuroi (`.ufo/prompts/<lane>-round-46.md` lines 407/569/504/513/504/411/457/513): "Re-ground each entry in-round under CORPUS.md rule 1 ... entries sit at `knowledge/<target path>`". It governs their own `merge/<lane>/` assimilation packages. Tameshi's round-46 clause names `merge/tameshi/` explicitly (`tameshi-round-46.md:456-458`). Nothing in those prompts names `claim-package-contract` or `claim-gates`. A sibling assimilation of kasegi entries would have to come from `~/Projects/shokuknow`, which I was forbidden to read. See Limitations.

## GHSA / advisory tokens in other lanes (different surface, not a collision)

- `mori-shokunin/corpus/lessons/round-12.md:138`: `| S012 | https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6 ...` cites an advisory as evidence. Advisory content, not a reporting flow.
- `.ufo/waves/kaika-w1/mori-art.md:80,106` (dated 2026-10-19): the same GHSA as an adjacency note.
- `kotoba-shokunin/.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:151060` contains `GHSA-` as a string literal in a binary dump.
F28 is about the reporter flow of a repository's private advisory form. None of these is a claim on it.

## Do-nothing control and discrimination

Loop run over every lane directory except kasegi, counting files under `corpus/`, `SCORECARD.md` and `PROVINCE.md` matching `private vulnerability|GHSA-|SECURITY\.md|security\.txt|vulnerability reporting`, and files matching `lost-base|lost-tree|Re-ground|re-ground|recheck: .*test -d` under `corpus/knowledge` and `SCORECARD.md`. Output (excerpt):

    kake-shokunin         vuln-files=7   regrounds-files=2   r46/47-wave-entries=3
    kaidoku-shokunin      vuln-files=2   regrounds-files=3   r46/47-wave-entries=18
    kotoba-shokunin       vuln-files=1   regrounds-files=3   r46/47-wave-entries=0
    mori-shokunin         vuln-files=5   regrounds-files=0   r46/47-wave-entries=15
    revenger-shokunin     vuln-files=3   regrounds-files=0   r46/47-wave-entries=0
    tabi-shokunin         vuln-files=1   regrounds-files=3   r46/47-wave-entries=0
    tameshi-shokunin      vuln-files=0   regrounds-files=3   r46/47-wave-entries=22
    chousa-shokunin       vuln-files=0   regrounds-files=1   r46/47-wave-entries=21
    (all other lanes: vuln-files=0 unless listed above)

Positive control (token present, known): `grep -rIl -E "security-txt-publishing" kake-shokunin/corpus kake-shokunin/.ufo/waves/round-46` → `kake-shokunin/corpus/lessons/round-35.md`, `round-35-verifier-spotcheck.md`, `corpus/README.md`. Returns hits.

Do-nothing / negative control (nonsense token, same scope): `grep -rIl -i -E 'ZZQ-R46-NOMATCH-7731' --exclude-dir=kasegi-shokunin --exclude-dir=.git .` → `0`. Per-lane spot check (kake, tameshi, chousa) → `0` each.

So the scan returns hits when a token exists and none when it does not. The vulnerability-term hits are all security.txt, GHSA-as-advisory or SECURITY.md-as-file-content, catalogued above. The re-ground-term hits are shared template text or each lane's own `lost-tree` notes.

Stray artifact (observation, not touched): a directory named `D=` exists at the fleet root (`ls -ld -- ./D=` → `drwxr-xr-x 1 vgpnk vgpnk 8 Oct 28 12:07 ./D=`, containing `fast/`). It looks like a shell-quoting mistake from a `D=$(mktemp ...)` line. It is outside this lane and was not modified. The fleet root is the L0 owner's to clean.

Peers (roster and history): the live roster in my spawn context lists sibling-lane seats `KamaR63`, `TameshiR56a4`, `MadoR55`, `SoujiR41`, `R41sentinel02`, `RV06Hygiene-2`. Their in-flight prompts (`kama-round-63.md`, `tameshi-round-56.md`, `mado-round-55.md`, `souji-round-41.md`) were grepped for the same terms. Each matches only the shared "Re-ground each" line at 569/569/504/... (same as above). The roster entries' stated work (e.g. "Waiting for remaining wave seats", "Moving misrooted seat file into lane", "Fix tool docstring range claim") does not concern security reporting or lost-base re-grounding. The R46* seats in the roster are kasegi's own seats (`KasegiR46` is the lane's waiting seat), not siblings.

## Collisions summary

| # | Lane / path | Surface | Collision with S073 / F28 / C1 entries | Action for L1 |
|---|---|---|---|---|
| 1 | kake `corpus/knowledge/security-txt-publishing.md`, `PROVINCE.md:289-292` | security.txt / Contact discovery | adjacent, no claim | F28 stays on reporter flow; cite kake only as "separate from security.txt discovery" |
| 2 | kaika-w3 `publish-lane-security.md:86-124` (F3) | publishability of claim-package-contract.md | open flag, same file as C1 | C1 rows cite committed path:line and tokens only; no lost-tree claims/VDP names |
| 3 | kotoba `sibling-citation-routing-round16.json` (lane kasegi, claim-gates.md) | citation token resolution | dependency | keep `corpus/knowledge/claim-gates.md` path; append-only edits |
| 4 | revenger `round-62/build/R62ConnectKasegi.md:13` | read-only probe, dated | none live | none |

No sibling lane currently declares a claim on GitHub private vulnerability reporting, GHSA reporting, SECURITY.md reporting, or re-grounding of `claim-package-contract.md` / `claim-gates.md`.

## Limitations

- `~/Projects/shokuknow` was off-limits for this seat. I could not check whether any `merge/<lane>/` package stages kasegi entries (`claim-package-contract`, `claim-gates`) for re-grounding. The C1 finding "no sibling re-grounds these entries" holds only for the fleet outside shokuknow.
- The grep is lexical. A sibling could describe reporter flow without the words used here. The vocabulary covered was `private vulnerability|GHSA-|SECURITY\.md|security\.txt|vulnerability reporting|privately report`. The `privately report` term was not run in the lane loop. Run `grep -rIl -i "privately report"` over the fleet if an exhaustive check is needed.
- The history:// listing was read only as a roster (1005 lines, mostly parked seats). I did not read the body of any parked transcript; the roster is a list of names and timestamps, not content.
- Round-46 in-flight state was read from prompt files and wave directories as they stand on disk at the time of the scan. A sibling could commit a claim after this read.
- I did not run the kasegi counters (`r46-c1-gate.py`, `r46-c2-gate.py`) and did not build F28 or the C1 re-grounds. My assignment is the sibling scan only.
- No scratch directory was created; nothing needed removal.
