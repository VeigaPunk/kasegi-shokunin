# ConnSibling — round 35 wave 1 (connector seat: sibling-overlap scan → contested-scope ruling)

Seat id: `ConnSibling-3`. Assignment: synthesize the sibling-overlap scan (`ScoutSiblingSweep`)
into a contested-scope ruling draft for the lesson; any sibling corpus holding CISA/KEV/
known-exploited ground is reported, not absorbed (PROVINCE adjacency); state the ruling
(no contested scope / report-to-lane) for each hit. Deliverable ruling draft:
`.ufo/waves/round-35/wave1/ConnSibling-ruling-draft.md`.

Doctrine read: `PROTOCOL.md:457-461` (contested-scope invariant: report in the lane report,
integrator arbitrates, unruled reports are re-flagged, silence is not a ruling);
`kasegi-shokunin/PROVINCE.md` Adjacent ("Sibling lanes are reported, not absorbed: chousa, kagi,
kake, kengaku"). Object under protection: C2 / F18 / S052 (`corpus/SOURCES.md:58`).

## Report

Every load-bearing claim of `ScoutSiblingSweep.md` was independently re-run; outputs below are
mine, not quoted from the scout.

### 1. Sibling lane count

```
$ cd /home/vgpnk/Projects/shokunin && ls -d *-shokunin | wc -l && ls -d *-shokunin | grep -v '^kasegi-shokunin$' | wc -l
21
20
```
Exit 0. 20 siblings, matches the sweep's "19+1".

### 2. Token sweep over sibling corpus + SKILL.md (the five ground tokens)

```
$ cd /home/vgpnk/Projects/shokunin
$ P='\bCISA\b|\bKEV\b|known exploited|BOD 22-01|exploited vulnerabilit|remediation deadline'
$ for d in *-shokunin; do [ "$d" = kasegi-shokunin ] && continue; rg -i -n --no-heading -e "$P" "$d/corpus" "$d/SKILL.md" 2>/dev/null | sed "s|^|$d: |"; done; echo "SWEEP_DONE exit=$?"
kake-shokunin: kake-shokunin/corpus/lessons/round-35.md:58:none a row. It proposed rejecting the CISA BOD 20-01 template: “Your policy must be published as
kake-shokunin: kake-shokunin/corpus/SOURCES.md:255:Round 35 bounded question (2026-10-22): how does a publisher serve a valid security.txt (RFC 9116) … [line truncated by display; full line in artifact] …
SWEEP_DONE exit=0
```
Exit 0; exactly the two kake lines the scout reported, nothing else. Confirms "19 lanes ZERO, kake 2 lines".

Missing-SKILL.md note confirmed: `ls audio-shokunin/SKILL.md game-dev-2d-shokunin/SKILL.md` →
"No such file or directory" for both; their corpora were covered by the loop above (zero hits).

False-positive class confirmed: `grep -rn exercisable kaidoku-shokunin/corpus | wc -l` → 4
(the scout's word-boundary justification is real).

### 3. kake hit content (quoted, named locations)

`kake-shokunin/corpus/lessons/round-35.md:58-60` (context lines 50-66 read; the sentence spans
lines 58-59 and completes at :60, with doubled smart quotes around the path):
> "It proposed rejecting the CISA BOD 20-01 template: “Your policy must be published as a public web
> page in plain text or HTML at the “/vulnerability-disclosure-policy” path”. That template names
> neither security.txt nor `.well-known` (`w1/ScoutSecurityTxtCandidates.md`)."

`grep -n "BOD 20-01" kake-shokunin/corpus/SOURCES.md` → exit 0, **only** line 255 (the round-35
bounded-question paragraph recording the same screened-and-rejected candidate; the paragraph's
rows S078–S087 are RFC 9116 / GitHub Pages / security.txt rows — no KEV, no BOD 22-01).

Ruling for both: **no contested scope** — (a) directive discrimination BOD 20-01 ≠ BOD 22-01/KEV;
(b) topic = VDP publication path, not exploitation-status prioritization; (c) kake created no row
(its own scout's rejection record); (d) prior occupancy: kasegi already holds the BOD 20-01 template
as `corpus/SOURCES.md:14` (S008) and `:27` (S021).

### 4. Zero-hit surfaces (negative space, re-run)

```
$ rg -i -n -e "$P" -g '!kasegi-shokunin/**' -g '!*/corpus/**' --glob '!.git/**' *-shokunin
noncorpus_exit=1        # zero hits: PROVINCE.md, README, considerthese/, plans/, SCORECARD, LOG of all 20 siblings
$ rg -i -n -e "$P" -g '!*-shokunin/**' --glob '!.git/**' .
fleetroot_exit=1        # zero hits at fleet root; ls -d merge considerthese → "No such file or directory" (both)
$ rg -i -n -e "$P" /home/vgpnk/Projects/shokuknow/{merge,doctrine,lanes,README.md}
# only kasegi-owned rows: doctrine/channel-recurrence.md:62 "| `cisa.gov` | kasegi |";
# lanes/kasegi/{DOMAIN,CHANNELS,CANNOT-ANSWER,round7,round8} CISA rows (S008 VDP template "held as S008",
# F02/F03 references, round7/8 SSVC citation in kasegi's own evidence)
```
Exit 1 = rg "no matches" for the two zero surfaces; shokuknow run exit 0 with only kasegi-owned
rows. Confirms: shokuknow `merge/*` (21 lane dirs incl. kasegi) has **zero** hits; the doctrine
host table assigns `cisa.gov` to kasegi (ratifies, does not contest).

### 5. Adjacent-theme spot checks (semantic sweep claims)

```
$ rg -i -n "CVSS|EPSS|SSVC|actively exploited|in the wild|NVD|exploitation status|vulnerability prioriti" kagi-shokunin/corpus kagi-shokunin/SKILL.md
kagi-shokunin/corpus/lessons/round-28.md:43  (CVE-2020-10735 via NVD API; "NOT REGISTERED" as a source)
kagi-shokunin/corpus/lessons/round-28.md:151,154 ; kagi-shokunin/corpus/SOURCES.md:89
# topic = version-token typing; no exploitation-status teaching anywhere
$ grep -c "CVSS overall score" mori-shokunin/corpus/evidence/recheck-r32/S012.src
1       # raw fetched advisory HTML blob, not a taught claim
```
Exit 0 both. Ruling for all adjacent-theme hits: **no contested scope** (rationale in the draft).

### 6. kasegi baseline (scout said `rg -i -c` → 10)

```
$ cd kasegi-shokunin && rg -i -c '\bCISA\b|\bKEV\b' corpus/SOURCES.md
11      # at this seat's run time
```
Exit 0. **Precision finding:** the scout's baseline of 10 is stale by one landed edit — the added
line is the round-35 search-log scope-correction note at `corpus/SOURCES.md:112` (line-census of
the 11 matches: rows S003/S008/S021/S023/S026/S052 + sweep notes at :70/:71/:79/:108/:112). No claim
(C1/C2) counts this baseline; recorded in the ruling draft so the lesson does not re-quote 10.

### 7. F18/S052 occupancy in the working tree (context for the ruling)

- `corpus/SOURCES.md:58` — S052 KEV catalog row (tier A, mined, opened 2026-10-26) — present.
- `grep -rn "^source: S052" corpus/knowledge/` → `corpus/knowledge/cisa-kev-catalog.md:3` — present.
- S008 (`:14`) and S021 (`:27`) confirm kasegi's prior occupancy of BOD 20-01 ground.

## Verdict

**No contested scope anywhere in the 20 sibling lanes; no report-to-lane item; no PROVINCE.md
refinement required.** The only CISA tokens in any sibling corpus are kake's *rejection record* of
the BOD 20-01 VDP template (a directive kasegi already holds as S008/S021, on a topic — VDP
publication path — that is not exploitation-status prioritization). The ruling per hit is tabulated
in `ConnSibling-ruling-draft.md` with discriminating tests and an embeddable re-run command block.

Bounded connector proposal (for the L1, not executed this round): mint a registered
`sibling-overlap.sh` probe (five-token pattern, word-boundary false-positive rule, verdict map,
`--selftest`) in a future round's claim — the scan is currently prose-only. Improves
depth:verifiability (non-author-runnable) and guards coverage-class novelty claims; no harm to
frozen claims since nothing is written this round.

## Housekeeping

- Post-review amendment (ScribeGateAssimilation scope call, this wave): the ruling stays in
  `ConnSibling-ruling-draft.md` as the L1-splice artifact — not in the assimilation Gate block
  (disjoint records; the scribe measured zero package-token intersection with its seven rows).
  Two amendments landed in the draft: (1) claim 1 now cites `kake…/round-35.md:58-60` with the
  byte-faithful two-line quote (doubled smart quotes; the scout receipt's `:17` rendering is the
  elided variant — the scribe's follow-up confirmed my rendering is the faithful one); (2) the
  precision note now binds pattern to count: narrow `\bCISA\b|\bKEV\b` → 11 lines, wider five-token
  sweep pattern → 12 (adds `:111`), each measured twice independently. Draft re-digested above.

- Scratch: `/fast/scratch/hyaku/kasegi-r35/ConnSibling/` was created at seat start and removed at
  exit (`rmdir`, verified empty — no fixtures were needed; all work was read-only search + two
  wave-dir files). Nothing left on disk.
- No tool installs/upgrades (none needed; pacman pause respected).
- No writes outside the lane repo; fleet root, sibling lanes, `/home/vgpnk/Projects/bounties`, and
  shokuknow untouched (shokuknow read-only greps only; no campaign tools run). No git/jj mutations.
  No subagents dispatched; no `agent://all`.
- Coordination: ruling-draft path messaged to `ScribeGateAssimilation` (lesson Gate owner) for
  absorption into `corpus/lessons/round-35.md`.

## File digests (sha256)

- `.ufo/waves/round-35/wave1/ConnSibling.md` (this receipt) — self-pin omitted: any sha256 quoted inside the file is invalidated by filling it in; the digest of record is whatever the L1 computes at land time.
- `.ufo/waves/round-35/wave1/ConnSibling-ruling-draft.md` `ef6096653ca6e1f30694053ff5248a4e09530ba6e4db00634dcbb1bfb64b18ea` (amended post-review; prior digest `8d2ed7f0…`)
- `.ufo/waves/round-35/wave1/ScoutSiblingSweep.md` `cc7a797b946aa69fd5a1f495adaf9eefbc0d5916a15bc7eba8ef9f2b3301b768`
- `kake-shokunin/corpus/lessons/round-35.md` `cffb84a5e1e8627aebe51eddf36fe487b165f15fc652bf63e6174dc45282c413`
- `kake-shokunin/corpus/SOURCES.md` `57c83362dbc6ba81dc45351f1bcdc33aecbb2b448a6343a95a1a585feccbe4ea`
- shokuknow `doctrine/channel-recurrence.md` `7ec813c70973b4d3c37210120b88889b558a1c7a30b395220d7b9df29c1400d1`
- `corpus/SOURCES.md` (working tree at this receipt) `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba`
- `corpus/knowledge/cisa-kev-catalog.md` `0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74`
- `.ufo/waves/round-35/claims.json` `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982`
- fleet `PROTOCOL.md` `886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a`
