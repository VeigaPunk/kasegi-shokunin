# Round 51 — the routed-defect corrections (C1, C2) and the CISA Vulnrichment surface (C3)

Three declared claims, frozen in `.ufo/waves/round-51/claims.json` at base `bcd5d89a65ab612ef88e3d49cea0ef3cb3ccca09`
before implementation: C1 on depth:verifiability (the lane's lowest non-retired axis, score 4 — the round-50 closure's
D1 fix: a genuinely host-produced C1 do-nothing control plus the provenance erratum), C2 on calibration (verdict row,
not a number — the D2 fix: the census-of-record figure correction 4807 → 4809, append-only), C3 on coverage (frontier
admission F32 = CISA Vulnrichment ADP enrichment on S081, with the pre-freeze neighbor screen the round-50 D1 lesson
made mandatory). Host unchanged from round 50 (Windows workspace, `python` 3.13.15, `python3` = Store stub, no /home,
no /fast).

## Mistakes

Sweep that found them (paste, per contract): the round's own run log — first `git archive c5e3636 | tar -x`
aborted with `error: invalid path '.ufo/waves/round-46/attempt2/wave1/R46bRevNoHarm.draft/aux.txt'` (the
NTFS-uncheckoutable-path class round-50 already recorded; the per-file `git show` build is the host's standing
method); then the first export build wrote 0 files to the scratch path while reporting `files=496`; then
`capture-source.py --url https://raw.githubusercontent.com/cisagov/vulnrichment/main/README.md` exited with
`HTTPError: HTTP Error 404: Not Found`; then `gh api repos/VeigaPunk/open-bug-bounties/commits/1307b8b` returned
`422 "No commit found for SHA"` — the negative answer that became S082.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a script that `cd`s and then resolves its output path relative to the new cwd | the first `build-export.sh` took a relative DEST, `cd "$REPO"` to read the tree, and wrote all 496 exported files into the LANE REPO worktree (`<lane>/base-c5e3636/`) instead of the scratch dir — caught because the immediately following `find <scratch>/base-c5e3636 -type f \| wc -l` printed 0 while the script self-reported `files=496` | the counting command disagreeing with the script's own success report, on the first run, before any commit | the stray dir was removed from the lane worktree before anything else ran (`rm -rf <lane>/base-c5e3636`, untracked, nothing else touched); the script now asserts an absolute destination (`case "$DEST" in /*\|[A-Za-z]:/*) ;; *) exit 9;; esac`) before it cd's — the general rule: a script that changes directory must take or assert absolute output paths, and a success message is never accepted over the counter that is supposed to observe it |
| a capture URL written from an assumed branch ref instead of the repository's declared default | `capture-source.py --url .../raw.githubusercontent.com/cisagov/vulnrichment/main/README.md` → HTTP 404 (the repo's default branch is `develop`, read afterwards via `gh api repos/cisagov/vulnrichment` → `default_branch: develop`); the round-38 S058 rejection already mined the mutable-ref class for OpenVEX and this repeats it on the fetch side | the capture instrument failing closed on the first attempt, before any capture existed | re-fetched against the declared default branch (`develop`), and the S081 row, manifest `url`/`capture_url` and the entry's `verified-at` all name the branch explicitly, with the entry's recheck line pinning the captured bytes (a 90d row recheck exists to re-open the ref, not to trust it); rule applied: a raw-URL capture resolves `default_branch` first, and the row names the ref it pinned |
| (inherited, fixed this round) a committed control attributed to a host that cannot produce its bytes | round-50 closure D1: `controls/do-nothing-c1.txt`'s bytes are an old-Linux-host run (`python3` working, `/fast/...` path) while four filed places label it host-produced, one of them claiming a "Windows CPython error string" that this host's CPython provably does not print (probe receipt `controls/probe-host-r51.txt`) | the round-50 non-author closure; re-verified first-hand this round before fixing (python3 stub exit 49; /fast absent; `python /fast/...` prints the Git-mount path form) | C1: `.ufo/waves/round-51/controls/do-nothing-c1-winhost.txt` is the host-produced control of record (real run at the c5e3636 export built per-file), and `.ufo/waves/round-51/erratum-1-c1-control-provenance.md` relabels the imported receipt (kept byte-identical) and corrects the wrong distinguishing claim |
| (inherited, fixed this round) prose figures quoted from an earlier census regeneration than the one that shipped | round-50 closure D2: report/LOG/SCORECARD/lesson say 204/4807 while the certified tip census at `021989b` reads 204/4809 (GONE 3738, total 10298) — verified first-hand from committed bytes before fixing | the round-50 non-author closure; re-derived this round via `git show 021989b:corpus/instruments/citation-survival.md` | C2: lesson round-50 Erratum 2 names 4809 at `021989b` and the regenerated-after-record pattern; LOG and SCORECARD carry the round-51 corrections; this round's own figures were measured only AFTER the final regeneration (below) |

## Gate

**S081 admitted** — CISA Vulnrichment README, `https://raw.githubusercontent.com/cisagov/vulnrichment/develop/README.md`
(CISA's own repository, default branch `develop`), kind `docs`, tier A, status `mined`, opened 2026-11-01, recheck
`90d`, used-by `corpus/knowledge/cisa-vulnrichment-adp-enrichment.md`. Capture
`corpus/source-snapshots/round-51/S081.txt` (sha256 `2da0941448d88f48bfc7275c6444abf3aaf57244719e64b3b3ab6591f4458b65`,
8290 bytes, 120 lines; fetched 2026-11-01T02:48:34Z, HTTP 200, 8501 raw bytes), manifest
`corpus/source-snapshots/round-51/manifest.json` (12 assertions Q1-Q12, each exactly-once at its pinned anchor;
`python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-51/manifest.json --source S081`
exits 0 — receipt `controls/s081-recheck.txt`).

Located quote grounding `teaches` (24 words by `wc -w`): "the public repository of CISA's enrichment of public CVE
records through CISA's ADP (Authorized Data Publisher) container" (S081.txt:2). The further anchors the entry cites:
S081.txt:6 (SSVC first), S081.txt:7 (conditional CWE/CVSS), S081.txt:8 (no CNA overwrite), S081.txt:14 (three decision
points), S081.txt:58 (KEV condition), S081.txt:104 (CPE stop), S081.txt:114 (drop rule + precedence), S081.txt:117-118
(version encoding), S081.txt:3 (consumption note).

**Admitted:** the CISA Vulnrichment surface as frontier row F32 — CISA's ADP-container enrichment program and its
data rules (what CISA writes into CVE records' ADP containers, when it yields to the CNA, how its SSVC data is
versioned, and what its silences do and do not mean) — admitted with the pre-freeze neighbor screen named against
F18/F20/F22/F25/F30 (entry §Distinctness; the screen's commands and zero-hit results are quoted there and ran before
the freeze landed). Counter before→after ON THIS HOST: `rows=31 admitted=31 closed=1 problem-rows=30 registry=80`,
`entries=34 pass=1`, zero F32 lines (`controls/do-nothing-c2-r51-winhost.txt`, base export bcd5d89) → `rows=32
admitted=32 closed=2 problem-rows=30 registry=82`, `entries=35 pass=2`, `PASS F32 ids=S081 exit=0`, all 33 inherited
fails exactly `recheck-exit-1` (`controls/c2-counter-final-r51.txt`).

**Rejected / refused, with reason and flip:** S082 — the public GitHub mirror `VeigaPunk/open-bug-bounties`, screened
as a possible upstream relocation of the lost `origin-work/open-bug-bounties` checkout and refused because the
identity question answers negatively on the probed evidence: the mirror's history does not contain the lost
checkout's recorded HEAD `1307b8b` (gh api → 422), and its root inventory matches neither the r15 package-dir layout
nor the receipt-store (`controls/mirror-probe.txt`). Consequence recorded: RECEIPT-STORE-LOST stays
corpus-attested-only; PROVINCE carries the append-only r51 status annotation. Flip: a commit-level identity link
(`1307b8b` appearing in the mirror's history, or byte-identical `submission-review/` receipt blobs). Also refused
this round: any portability rewrite of the 67 host-bound recheck lines — L0 kasegi round-50 is unanswered and stays
routed-around, not treated as answered.

**Spot-check:** none of this round's gate decisions has an independent non-author spot-check yet; the most recent
outside check is `corpus/lessons/round-50-verifier-spotcheck.md` (commit `bcd5d89`), which routed the two defects
this round fixes. The claims verify on their frozen predicates by re-derivable commands only.

**Wave disposition — no AgentSwarm surface on this host; no seats ran.** As in rounds 49-50, no AgentSwarm/Kimi
host surface exists in this environment and no L2 wave was dispatched; the round's craft, commits and verdicts are
the L1's own. The MISSION.md L2 floor stays unsatisfiable on this host and is recorded as such, not simulated.

## Limits

- The C1 erratum corrects a provenance label, not the round-50 C1 predicate: the frozen sentence's bytes
  (`CENSUS-FRESH=ok` exit 0 at tip; exit 2 do-nothing semantics) were true then and re-verified here; only "produced
  on this host" and the "Windows CPython error string" claim were wrong.
- The S081 capture pins one README at one mutable ref (`develop`); the recheck verifies the pinned bytes and located
  quotes and does not claim the live branch still says this — the 90d row recheck exists to re-open it.
- The F32 admission inherits the host split unchanged: the counter reads `entries=35 pass=2` with 33 inherited
  `recheck-exit-1` rows (L0 kasegi round-50, operator-owned). No coverage score is asserted from the frontier row;
  the score's denominator stays the lost domain root's 18-surface set.
- The mirror probe answers identity negatively on two probes (history lookup, root inventory); it cannot prove a
  negative about content the mirror does not expose — the flip condition is what a future claim would need.
- The gate certifies census freshness, not citation truth (unchanged from round 50); `resolve.py` and `anchorcheck.py`
  keep those jobs.

## Census of record at this round's tip (quoted only from the final regeneration)

Measured AFTER the last corpus edit of the round (the C2 rule): the figures below are the regenerated census of
record at the final tip, and the gate receipt `controls/c1-gate-final-r51.txt` certifies the committed census bytes
byte-identical to a fresh regeneration (`CENSUS-FRESH=ok files=2`). Figures: recorded in SCORECARD round-51 row from
that regeneration (this lesson intentionally quotes them only by pointer, so the lesson bytes cannot drift from the
gate-certified census they describe).
