# Round 50 — census-freshness gate (C1) and the OSV affected-range surface (C2')

Two declared claims, superseded from the inherited freeze by `.ufo/waves/round-50/claims-erratum-1.md` and
re-frozen in `.ufo/waves/round-50/claims.v2.json`: C1 on depth:verifiability (the lane's lowest non-retired
axis, score 4 — the census-freshness gate, capability acquisition) and C2' on coverage (frontier admission
F31 = OSV affected-range events, grounded on S080). Base `c5e36360f5226c97d28f1937961b15c90e58827f`; the
round ran on a NEW host (Windows workspace, Git Bash, interpreter `python` 3.13.15; `python3` is the Store
stub; `/home/vgpnk` absent), which is what surfaced the inherited freeze's defects.

## Mistakes

Sweep that found them (paste, per contract): `grep -h "^recheck:" corpus/knowledge/*.md | grep -c "cd /home/vgpnk"` → 67;
`python3 --version` → "Python was not found; run without arguments to install from the Microsoft Store";
`ls /home/` → "No such file or directory"; `grep -n "F19" PROVINCE.md` → line 78 (EPSS admitted round 36);
`grep -oE "\| F3[0-9] \|" corpus/README.md | sort -u` → only F30 (F31 free); the committed controls pair read
side by side: `.ufo/waves/round-50/controls/do-nothing-c1.txt` (Windows CPython error string) vs
`do-nothing-c2.txt` (30 FRONTIER-PASS rows) — outputs no single host could have produced together.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| claim frozen against a surface the lane had already admitted | `.ufo/waves/round-50/claims.json` C2 frozen sentence: "F31 — EPSS exploit-prediction scoring ... used-by `corpus/knowledge/epss-exploit-prediction-sco...`" vs `PROVINCE.md:78` (F19 — FIRST EPSS, admitted round 36, entry `corpus/knowledge/epss-exploit-prediction-scoring.md`, source S053) and the frontier counter's duplicate-entry guard; the frozen sentence names distinctions against F01/F05/F13/F18 and never against F19, the row it actually collides with; the committed wave spec even schedules "does a kasegi F31 (EPSS ...) duplicate" as a seat question — after the freeze | none at freeze time: the round-34 pre-freeze satisfiability rule was applied to counter satisfiability, not to surface-level newness; no lane criterion required grepping the province for the surface before freezing | `claims-erratum-1.md` D1 supersedes C2; the superseding C2' admits OSV affected-range events (F31) — a surface proven free by the same grep sweep and reached by re-opening the round-42 S065 screen under its own recorded flip condition (corpus/SOURCES.md S065, rejected 2026-10-28). Rule applied going forward: a frontier freeze must name its distinctions against the actual neighbor rows, read from the province, before the freeze lands. |
| freeze predicates bound to a host that no longer exists | every frozen counter command in `claims.json` names `python3` and `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; this host has neither (`python3` = Store stub, `/home/` absent), and all 67 committed entry recheck lines share the binding — so the frozen C2 expect_after (`entries=34 pass=34 exit=0`) is unreachable here regardless of lane work; the live counter run reads `entries=34 pass=1 exit=1` with 33 `recheck-exit-1` | none: the host move happened between rounds and no freeze carries a host-bindings declaration; the r50 commit `28c65eb` even carried the staleness note (`r50-live-resolve.txt`) without carrying the host audit | `claims.v2.json` re-freezes both claims with host-portable commands (`python`, repo-root cwd, sys.executable) and host-honest predicates that name the inherited failure taxonomy; the new F31 entry's recheck line is interpreter-portable (`python3 ... || python ...`); the 67-line portability repair is filed as an L0 question (fleet `.ufo/l0-questions.md`, kasegi round-50 row) — operator-owned, not silently rewritten. |
| a committed control's output could not have been produced on the host that committed it | `.ufo/waves/round-50/controls/do-nothing-c2.txt` prints `rows=30 admitted=30 closed=30 problem-rows=0 registry=79`, thirty `FRONTIER-PASS` rows and `entries=33 pass=33 exit=0` for a `/fast/scratch/...` base export, while its sibling `do-nothing-c1.txt` carries a Windows CPython error string; no host passes both descriptions: on THIS host the same counter run at a real base export reads `entries=33 pass=0` with 33 `recheck-exit-1` (`controls/do-nothing-c2-winhost.txt`, produced this round) | the round's own before→after re-derivation: the before-value had to be reproduced on the host measuring the after-value, and it would not reproduce | superseded as a control by `controls/do-nothing-c2-winhost.txt` (the real run); the original file is kept byte-identical as the mistake's evidence of record. Rule applied: a receipt carries its producing host; a control imported from another host is labelled as imported, never pasted in place. |
| manifest anchor written from a displayed range, not a line number | first verify of the S080 manifest printed `S080:Q8 OK occurrences=1 anchor=752-BROKEN` — the quote sits at S080.txt:751-752 and the anchor had been read off a `sed -n '751,756p'` display instead of `grep -n`; exit stayed 0 only because the quote occurs exactly once (the anchor note is advisory for unique quotes — a weaker check than it looks) | the recheck instrument's own anchor verdict (`anchor=N-BROKEN`), on the first run, before any commit | anchors are now taken from `grep -n` output; the committed manifest's 16 anchors all read `-ok` (`grep -c BROKEN` = 0) and the receipt records that count, not just the exit code. |
| probe defects that fake a battery verdict | two defects in the first mutant-battery run (scratch, pre-receipt): the "same-length" tamper was a no-op string replace that also normalized line endings (pristine gate exited 1 on a world that should have been fresh — the want-matrix caught the impossible result), and the no-restore mutant patch produced an IndentationError crash (fresh-world exit 1 for a gate that never ran) | the battery's own want-matrix: a world that surprises its definer is a broken world, and a mutant that cannot run is not a mutant | same-length tamper redone as a byte-level edit (`citations` → `citationZ`, binary I/O, line endings untouched); mutant patches verified runnable by the fresh-world row before any defect world is read; the committed receipt (`.ufo/waves/round-50/controls/c1-mutbat.txt`) is the fixed battery's output: 6 mutants, 5 closed, 1 survivor named. |

## Gate

**S080 admitted** — OpenSSF OSV format specification page, `https://ossf.github.io/osv-schema/`, kind
`spec`, tier A, status `mined`, opened 2026-11-01, recheck `90d`, used-by
`corpus/knowledge/osv-affected-range-events.md`. Capture
`corpus/source-snapshots/round-50/S080.txt` (sha256 `97b850a4bcd90600bb39391df3293e4591b9dd84170e94ecfd48f40e08cfeda9`,
70913 bytes, 1462 lines; fetched 2026-11-01T01:17:14Z, HTTP 200, 228890 raw bytes — the same raw byte count
the round-42 S065 screen recorded on 2026-10-28), manifest
`corpus/source-snapshots/round-50/manifest.json` (16 assertions Q1-Q16, each exactly-once at its pinned
anchor; `python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-50/manifest.json --source S080`
exits 0).

Located quote grounding `teaches` (14 words by `wc -w`): "This document defines a standard interchange
format for describing vulnerabilities in open source packages." (S080.txt:9-10). The further anchors the
entry cites: S080.txt:4 (version line, 5 words), S080.txt:17 (stability, 13 words), S080.txt:374-375
(required fields, 19 words), S080.txt:706-708 (range type, 23 words), S080.txt:739-742 (the four event
verbs), S080.txt:751-755 (introduced "0" and the implicit limit), S080.txt:763-764 (last_affected ceiling,
24 words), S080.txt:788 (GIT repo duty, 10 words), S080.txt:790-793 (database_specific out of scope).

**Admitted:** the OSV affected-range surface as frontier row F31 — the per-package version timeline
(`affected[].ranges[].events`: introduced/fixed/last_affected/limit, at least one introduced event, an
implicit `limit` `"*"`, three range types ordered by SemVer precedence, ecosystem logic or Git
reachability) — admitted on the lane's own coverage map with a first-party capture, a knowledge entry whose
`recheck:` line re-verifies its own declared source and is executable on this host, a registry row whose URL
binds to the capture, and the S065 flip condition explicitly fired in both the row and the entry.

**Rejected / refused, with reason and flip:** the inherited C2 (F31 = EPSS) was refused as a duplicate of
F19 — see M1; flip condition: none needed, the surface is already admitted (re-opening it again would be
manufactured work). No new rejected SOURCES row this round: the round's screening ledger is the S065
flip (the only candidate re-open), and the EPSS freeze refusal is recorded here and in
`claims-erratum-1.md` rather than as a registry row, because the EPSS surface already has an admitted row.

**Spot-check:** the round's gate decisions (admit S080 / admit F31; refuse the inherited EPSS C2; supersede
the freeze) have **no independent non-author spot-check**. The most recent outside check is
`corpus/lessons/round-49-verifier-spotcheck.md` (commit `c5e3636`), which covers the prior round. The
committed wave-1 spec targets the superseded freeze and never ran on this host; this round claims no
falsification credit from it.

**Wave disposition — inherited spec, released UN-DISPATCHED, stale against claims.v2.** The round inherits
`.ufo/waves/round-50/wave1-spec.json` (32 seats, policy v1 band 32-48, commit `28c65eb`) whose CONTEXT
names the Linux-only roots and whose seats attack the superseded C2=EPSS freeze; no AgentSwarm surface
exists on this host and no seat ran. The claims verify on their re-frozen predicates by re-derivable
commands only.

## Limits

- The gate certifies census freshness, not citation truth: byte-identical regeneration proves the census
  describes the current tree, not that the citations resolve or mean what their sentences say —
  `resolve.py` and `anchorcheck.py` keep those jobs.
- The committed census embeds this host's lane path; a Linux-host gate run against it reads stale by
  mechanism, not by drift (instruments README, round-50 section). Re-baselining on a host move is
  operator-owned (L0 kasegi round-50).
- The F31 admission inherits the host split: the counter's `entries=34 pass=1` is the honest host truth;
  `pass=34` remains reachable only where the 67 inherited recheck lines can run (L0 question). No coverage
  score is asserted from the frontier row; the score's denominator stays the lost domain root's 18-surface
  set.
- The C2' capture is one release of one page (byte-count-stable across 2026-10-28 and 2026-11-01). The
  recheck verifies the pinned bytes and located quotes; it does not claim the live page still says this.
- The battery's one survivor (error-exit-0) is named, not hidden: no fixture world forces a resolver
  failure; the error limb's fail-closed behavior is evidenced by the base-export control exiting 2.

## Erratum (appended before round close, 2026-11-01)

The census figures first filed in this lesson and in the SCORECARD/LOG round-50 rows — "203 files / 4784
distinct" — were the pre-lesson regeneration (run 1). The census of record regenerated over the final tree
reads **204 files / 4807 distinct**; the figures above are corrected to it. The gap itself demonstrated the
gate: after the controls rename (`c1-mutbat-out.txt` → `c1-mutbat.txt`) the tip read
`CENSUS-FRESH=stale` (one `.ufo/waves/round-50/controls/c1-mutbat.txt` citation flipped GONE → INTERNAL)
until the census was regenerated — the instrument catching exactly the drift it exists for, on its own
round.

## Erratum 2 (appended round 51, 2026-11-01 — closure D2 correction, R9 append)

The census-of-record figure in this lesson's Erratum above — "204 files / 4807 distinct" — is itself
wrong, and so are the same figures in the round-50 LOG entry and SCORECARD row. The census of record at
the round-50 tip `021989bf4f5699fa55c6d90abd37ce6ad1caa50a` reads **204 files / 4809 distinct** (GONE
3738; total occurrences 10298): `git show 021989b:corpus/instruments/citation-survival.md | grep -c 4809`
prints 4 in the committed census bytes, while the prose records were written from the previous
regeneration (GONE 3736, total 10295). One of the two census runs was not taken over the bytes it shipped
with — the exact regenerated-after-record pattern the round's own C1 gate exists to catch: the census was
regenerated once more after the figures had already been quoted into prose, and nothing re-checked the
prose against the new bytes. Rule applied going forward (round-51 C2): the figures of record are quoted
only from the final regeneration at the measured tip, after the last corpus edit, never from an earlier
run. The filed 4807 lines above are retained byte-identical; this erratum is the correction (R9). See
also `.ufo/waves/round-51/erratum-1-c1-control-provenance.md` for the closure's D1 relabel (the C1
do-nothing control was an imported old-host receipt, not a run on the committing host).

## Correction (round 57, 2026-11-02) — scope of F31 semantic verification

The round-50 F31 source-binding checks did not establish the correctness of every reading:
README F31:743 wrongly excludes explicit versions, and knowledge Claim 3:60 wrongly scopes
fixed/last_affected exclusion to a record. Round-57 S089 reopens the unchanged source and
corrects both append-only. See `corpus/lessons/round-57.md` and the existing knowledge entry's
named correction. Historical closure/counters are not reset or upgraded by this correction.
