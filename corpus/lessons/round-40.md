# Round 40 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `a7af2ce63bce153757d39bf66b366a96caf30c13`; claims-freeze commit
`5e985b74075dd3813a63d7750966bf8abf693465` (`.ufo/waves/round-40/claims.json`); judged head J = the lane
commit carrying every round-40 change except the receipt; verification ref Y = J + the receipt
`.ufo/waves/round-40/final-gates/all-gates.txt` only. Shape: two v1 waves — `kasegi-r40-build` 54 seats
(executor 18, reviewer 12, scout 11, scribe 6, critic 3, mutation-tester 2, connector 1, sentinel 1) +
`kasegi-r40-falsify` 35 seats (reviewer 12, scout 8, critic 7, mutation-tester 6, connector 1, sentinel 1)
= 89 total (64-128 band). Attack share: wave 1 17/54 = 31.5%; wave 2 33/35 = 94%; round total 50/89.

## Frozen claims — before → after

| Claim | Axis | Before | After |
|---|---|---|---|
| C1 | depth:verifiability (4, held) | suite absent (c1-controls/before.txt); R2/R5/R6 open; G2/G6 flaws standing; r39-l1 scratch leftover removed at round start | suite landed; `closed=10/10 exit=0` at Y; graded `selftest cases=10 failures=0`; base/r39-head reds; receipt at Y = teed transcript |
| C2 | coverage (7 → 8) | queued 9 (S016/S017/S019/S020/S021/S022/S023/S024/S025); mined among nine 0; S060+ 0; frontier 22; harness 25/25; registry 59; measure 42/51 = 0.824 | queued 0; mined among nine 7; S060+ 3 opened this round (S060 mined, S061/S062 rejected); frontier 23 (F23); harness 26/26; registry 62; measure 43/43 = 1.000 |

## Mistakes

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M40-1 | evidence-provenance | the round-39 attempt-1 receipt records a pass that the L1's own run over the same commit does not produce, under a `run-utc` that post-dates that commit | `5006097a:.ufo/waves/round-39/final-gates/all-gates.txt` (all-gates v3: `run-utc=2026-10-26T21:35:00Z` vs commit `2026-10-26T20:12:12Z`; `closed=8/8`) vs the L1's own run over `5006097a` (`closed=6/8 exit=1`; `selftest cases=8 failures=2`; scratch verify-Y.txt) — verifier R1 | none at the time (wave-2 attack found it) | H5/H7: receipt = teed deterministic transcript, `run-utc` = ref's committer instant read by the suite (never wall-clock), forged/future-dated receipts rejected; R37 criterion added | H5 replica rejects the future-dated fixture (`dated=future closed=0` exit 1) and the forged payload (`declared=0` exit 1); the r39 receipt's `run-utc` is a hardcoded printf (r39-closure.sh:1150) |

## Census

Before (`census-before.txt`): `W04 S028`, `W04 S029`, `ok`, exit 0. After: `W04 S028`, `W04 S029`,
`ok`, exit 0. Registry 59 → 62 rows; tier A +3?mined S016/S017/S019/S020/S021/S023/S025/S060, rejected S061/S062, carried S022/S024 flips); rows touched old→new: the nine decided rows' status cells (7 queued→mined, 2 queued→rejected) plus seven `used-by` cells; new rows S060/S061/S062 appended. Search-log bullet appended.

## Gate

## Gate

Every source below was opened this round and every quoted span is a located quote from the committed
capture (≤25 words, whitespace-normalized match, anchor line named). Each mined row's capture passes
`corpus/instruments/source-recheck.py` and binds to its row under
`corpus/instruments/capture-binding-check.py` (`ExecRecheckAll`: eight lines, `S016 exit=0 ok` through
`S060 exit=0 ok`; `ExecBindingCheck`: `records=54 bound=54 unbound=0`, up from 46).

### Admitted — seven of the nine queued rows

- **S016 — Anthropic, Coordinated Vulnerability Disclosure for Claude-Discovered Vulnerabilities.**
  `https://www.anthropic.com/coordinated-vulnerability-disclosure`; access 2026-10-26 (fetched
  2026-10-26T21:15:52Z, HTTP 200, 164,126 raw bytes); capture `corpus/source-snapshots/round-40/S016.txt`
  (32 lines, 4,481 B, sha256 `91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b`). Quote (10
  words, L17): "Reports originating from AI-powered discovery are clearly labeled as such." Entry
  `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` (`source: S016`); recheck 90d.

- **S017 — Project Zero, Policy and Disclosure: 2025 Edition.**
  `https://projectzero.google/2025/07/reporting-transparency.html`; access 2026-10-26 (fetched
  2026-10-26T21:16:32Z, HTTP 200, 14,764 raw bytes); capture `corpus/source-snapshots/round-40/S017.txt`
  (39 lines, 5,058 B, sha256 `3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe` — stable
  across two fetches; the raw
  digest varies with a per-request CSP nonce, the text does not). Quote (20 words, L23): "within
  approximately one week of reporting a vulnerability to a vendor, we will publicly share that a
  vulnerability was discovered." Entry `corpus/knowledge/pz-reporting-transparency-trial.md`
  (`source: S017`); recheck 90d.

- **S019 — NIST SP 800-216, Recommendations for Federal Vulnerability Disclosure Guidelines.**
  `https://csrc.nist.gov/pubs/sp/800/216/final`; access 2026-10-26 (fetched 2026-10-26T21:16:11Z, HTTP
  200, 45,019 raw bytes); capture `corpus/source-snapshots/round-40/S019.txt` (132 lines, 4,901 B, sha256
  `514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6`). Quote (21 words, L80, recurs L83):
  "recommends guidance for establishing a federal vulnerability disclosure framework, properly handling
  vulnerability reports, and communicating the mitigation and/or remediation of vulnerabilities." Entry
  `corpus/knowledge/nist-sp800-216-vdp-framework.md` (`source: S019`); recheck on-release. **Limit:** the
  capture is the CSRC record page (title, abstract, document history at L97), not the SP 800-216 document;
  the row's `mined` status is abstract-level and its anchor says so.

- **S020 — U.S. Department of Justice, A Framework for a Vulnerability Disclosure Program for Online
  Systems.** `https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline=`; access
  2026-10-26 (fetched 2026-10-26T21:16:10Z, HTTP 200, PDF, 140,909 raw bytes); capture
  `corpus/source-snapshots/round-40/S020.txt` (319 lines, 16,693 B, sha256
  `8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c`). Quote (22 words, L142): "Absent an
  agreement with the cloud service provider, the organization implementing the vulnerability disclosure
  program may lack the authority to authorize others". Entry
  `corpus/knowledge/doj-vdp-framework-scope-and-authorization.md` (`source: S020`); recheck on-release.

- **S021 — CISA, BOD 20-01: Develop and Publish a Vulnerability Disclosure Policy.**
  `https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy`;
  access 2026-10-26 (fetched 2026-10-26T21:15:57Z, HTTP 200, 127,832 raw bytes); capture
  `corpus/source-snapshots/round-40/S021.txt` (432 lines, 58,004 B, sha256
  `72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329`). Quote (20 words, L133): "restrict the
  reporter’s ability to disclose discovered vulnerabilities to others, except for a request for a
  reasonably time-limited response period." Entry `corpus/knowledge/cisa-bod-20-01-vdp-minimums.md`
  (`source: S021`); recheck on-release.

- **S023 — CISA, The Coordinated Vulnerability Disclosure Program.**
  `https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program`; access
  2026-10-26 (fetched 2026-10-26T21:16:01Z, HTTP 200, 75,587 raw bytes); capture
  `corpus/source-snapshots/round-40/S023.txt` (213 lines, 14,357 B, sha256
  `52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087`). Quote (19 words, L151): "CISA may
  disclose vulnerabilities as early as 45 days after the initial attempt to contact the vendor is made".
  Entry `corpus/knowledge/cisa-cvd-program-stages.md` (`source: S023`); recheck 90d.

- **S025 — CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application
  Vulnerabilities.** `https://arxiv.org/abs/2503.17332`; access 2026-10-26 (fetched 2026-10-26T21:16:02Z,
  HTTP 200, PDF 602,933 raw bytes, v4 of 24 June 2025); capture
  `corpus/source-snapshots/round-40/S025.txt` (1,490 lines, 71,851 B, sha256
  `faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b`). Quote (16 words, L32): "Our
  experiments show that the state-of-the-art agent framework can exploit up to 13% of the
  vulnerabilities." Entry `corpus/knowledge/cve-bench-agent-exploitation-benchmark.md` (`source: S025`);
  recheck on-release. **Wording note:** the captured v4 abstract says "exploit", not "resolve" — the queued
  row's paraphrase is not in the captured bytes, and the row records the v4 wording.

### Admitted — F23 / S060 (CycloneDX analysis subtree)

- **Row.** S060, kind spec, tier A, status mined, opened 2026-10-26, recheck on-release, used-by
  `corpus/knowledge/cyclonedx-analysis-subtree.md`; NF=13; its `teaches` cell records that it supersedes
  S059 (rejected round 39) — the round-39 flip clause ("a CycloneDX-vs-CSAF frontier entry with a
  scoped analysis-subtree capture", S059 row verbatim) has fired. Row deliverable `wave1/ScribeNewRows.txt`
  (byte-identical).
- **Source / capture.** `https://cyclonedx.org/docs/1.7/json/`; access 2026-10-26 (fetched
  2026-10-26T21:16:18Z, HTTP 200, 6,419,901 raw bytes). Capture `corpus/source-snapshots/round-40/S060.txt`
  is a declared 111-line slice (4,889 B, sha256
  `d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779`): L1 title/version line, L2-L111 =
  page text L16060-L16169 (`vulnerabilities[].analysis` plus the `affects[].versions[].status` enum). The
  raw page digest is not fetch-stable (a second fetch changed 3,936 bytes of Cloudflare mail-obfuscation
  tokens); the normalized page text and this slice are.
- **Quotes (≤25 words, located in the slice).** L7 (15 words): "Declares the current state of an occurrence
  of a vulnerability, after automated or manual analysis." L15 (18 words): "The component or service is not
  affected by the vulnerability. Justification should be specified for all not_affected cases." L50 (11
  words): "The date and time (timestamp) when the analysis was last updated."
- **Entry.** `corpus/knowledge/cyclonedx-analysis-subtree.md` (`source: S060`, `verified-at: 2026-10-26`,
  `ground: F23`, executable `recheck:`); the entry compares the subtree against S055 (CSAF v2.0
  `product_status`) and S057 (CISA issuance), and records the obligation difference: two `should` sentences
  here against CSAF's machine-readable-flag SHALL (`S055.txt:L2151-L2152`).
- **Frontier admission.** F23 row + coverage-map row + `PROVINCE.md` `[r40 Frontier amendment]` appended
  (deliverables `wave1/ScribeF23.readme-row.txt`, `wave1/ScribeF23.province.txt`) puts the frontier at 22 -> 23
  rows, F23/23 admitted.

### Rejected

- **S022 (CNA Rules v4.1.0)** — REJECTED: superseded by S030 (v4.2.0, approved 2026-08-20, effective
  2026-08-25), whose mined row records `supersedes S022`, and no lane capture of the v4.1.0 PDF exists.
  Flip: re-open only if S030's capture is withdrawn or a citing source quotes v4.1.0 section numbering that
  4.2.0 no longer holds.
- **S024 (EU CRA, Regulation 2024/2847)** — REJECTED: superseded by S029 (official CRA Article 14 text, OJ
  20.11.2024, mined 2026-10-20), whose row records `supersedes S024`; this row's Article 14 wording was
  never verified from EUR-Lex. Flip: re-open only if S029's Article 14 capture is withdrawn or the
  consolidated text changes Article 14 or the Article 71 application date.
- **S061 (CISA, VEX Status Justifications, June 2022)** — REJECTED: the five not-affected justification
  labels it defines are already carried normatively by S055, which cites this PDF as its VEX-Justification
  reference, and no lane capture or manifest record exists this round, so its definitions, decision
  flowchart and chained-attack scope statement cannot be quoted or bound to an entry. Flip: a scoped
  capture of the PDF under `corpus/source-snapshots/round-40/` with a manifest record and an entry that
  quotes its per-label definitions.
- **S062 (OASIS CSAF v2.1 Committee Specification Draft 04)** — REJECTED: the v2.1 page is CSD 04 dated 21
  October 2026, no `os/` directory exists (both `os/` probes 404), so the round-39 flip monitor has not
  fired and the only OASIS Standard remains v2.0 (S055); a draft is not a normative source for a tier-A
  spec row. Monitor note: csd04 defines nine `product_status` properties against v2.0's eight lists and its
  flag-values sentence reads SHALL where v2.0 reads MUST. Flip: an OASIS Standard v2.1 exists — `os/`
  returns HTTP 200 with `OASIS Standard` front matter; recheck 30d against the directory listing.
- **S059 (CycloneDX v1.7 analysis)** — remains `rejected`; its round-39 flip fired and its ground is now
  carried by S060 (above), so no new decision is needed for the row itself.

### Nine decided rows — status change log

- S016 queued -> mined (opened 2026-10-26; entry corpus/knowledge/anthropic-cvd-provenance-and-pacing.md; recheck 90d)
- S017 queued -> mined (opened 2026-10-26; entry corpus/knowledge/pz-reporting-transparency-trial.md; recheck 90d)
- S019 queued -> mined (opened 2026-10-26; entry corpus/knowledge/nist-sp800-216-vdp-framework.md; recheck on-release)
- S020 queued -> mined (opened 2026-10-26; entry corpus/knowledge/doj-vdp-framework-scope-and-authorization.md; recheck on-release)
- S021 queued -> mined (opened 2026-10-26; entry corpus/knowledge/cisa-bod-20-01-vdp-minimums.md; recheck on-release)
- S022 queued -> rejected (superseded by S030, CNA Rules v4.2.0; reason+flip in row)
- S023 queued -> mined (opened 2026-10-26; entry corpus/knowledge/cisa-cvd-program-stages.md; recheck 90d)
- S024 queued -> rejected (superseded by S029, official CRA Article 14 text; reason+flip in row)
- S025 queued -> mined (opened 2026-10-26; entry corpus/knowledge/cve-bench-agent-exploitation-benchmark.md; recheck on-release)

New rows this round: S060 (mined, F23), S061 (rejected), S062 (rejected). Registry 59 -> 62 rows; no
registry row removed.

### Seam check — registry row ↔ knowledge entry ↔ bound capture

Run over the delivered bytes by this seat (row lines from `wave1/ScribeRows.decisions.txt` and
`wave1/ScribeNewRows.txt`; entries from `wave1/ScribeEntriesG1.*.md`, `wave1/ScribeEntriesG2.*.md` and
`wave1/ScribeF23.entry.md`; captures and records from the scout deliverables): **8 of 8 mined rows pass all
four limbs** — the row's `used-by` names an entry that exists, that entry's `source:` line cites the row
id, the row's `anchor` names `corpus/source-snapshots/round-40/S0NN.txt`, and the capture's sha256 equals
the bound manifest record's `sha256` while the row's one `https://` token equals the record's `url`. The
same seam discriminates when broken: `ExecBindingCheck` records a capture with no row printing
`FAIL rule=no-row record=S060 dir=round-40` / `records=54 bound=53 unbound=1` / exit 1, and a capture whose
row is set to `rejected` printing `FAIL rule=rejected-row-anchor record=S060 row=S060 dir=round-40` /
`records=54 bound=53 unbound=1` / exit 1. On the census side (`ScribeRows`, scratch mirror with the nine
decided rows substituted): `W04 S028`, `W04 S029`, `ok`, exit 0; `E11 S019 missing used-by` and exit 1 when
that entry file is moved away — so the `used-by` limb, not the row text alone, is what the census reads.

### Assimilation

Id-collision rerun (0-3-space extractor, read-only against `shokuknow`): lane reg-ids 59 (S001-S059),
staged ids 94 (S031-S124), `comm -12` = **29 collisions** — 28 true id collisions (S031-S041, S043-S059)
plus S042, which is the same URL in both files. 21 staged rows are documents the lane already holds; 15 of
those sit inside the 29 colliding numbers, leaving 14 colliding numbers naming documents the lane does not
hold. Guard proof on an indented S002 fixture: the 0-3-space form reports 1 collision, the column-zero-only
form reports 0, so the 0-3-space form is the required one. Quarantine slice (7 kasegi rows of the
`absent-defect-register`): 2 payload-verified but quote-shape-defective (S037, S054 — both payloads live
today, so "quote-defective", not fabrication), 1 document already held (S068 = lane S040), 1 payload
verified but refused on ground/Q3 (S065 — round 39's "unverifiable" is stale; it is reachable and the
`pdftotext -layout` extraction yields the statute list), 3 unreachable (S048 HTTP 404; S069/S070 HTTP 200
with a 0-byte body). **Adopted 0; adoptable 0; no renumber map filed** — a map is written only for adopted
rows. Standing refusals carried; the staged package sha256 (`4fe049cb…`) is unchanged from round 39.

### Sourced claim

C2's coverage increment rests on the S060+ rows opened this round, not on rows merely counted: S060 is
mined with an entry citing it (`corpus/knowledge/cyclonedx-analysis-subtree.md`, `source: S060`), and S061
and S062 were opened and rejected with their reasons and flips above. The frontier move 22 -> 23 is the
same admission; the census observed this round is the mirror with the nine decided rows substituted
(`W04 S028`, `W04 S029`, `ok`, exit 0), and the census over the new rows is the post-landing step. Note
for the next adoption: the staged package holds its own S060 (Hitachi HIRT-PUB10008, a document the
lane already holds as S039), so the collision count is a lower bound and must be re-run after these rows
land.

## Wave-2 falsification (appended 2026-10-26)

Wave `kasegi-r40-falsify` (35 seats: reviewer 12, scout 8, critic 7, mutation-tester 6, connector 1,
sentinel 1; 0 dead) attacked the frozen claims. Verdicts:

**C1 — the suite holds at the verification ref; no live defect defeats a check.** The green window is Y
only: at J (receipt untracked) the suite prints `closed=9/10 exit=1` (H7 fail-closed on the absent
receipt) and the selftest prints `cases=10 failures=1` (H7 positive red) — exactly the documented
pre-receipt state, reproduced by RevC1Counters R1/R2 and MutH6H10 F1. Committing the byte-exact receipt
as Y makes `--export-ref Y` green (`closed=10/10 exit=0`) and the graded selftest `cases=10 failures=0`
with ten `case=H<n> positive=pass` lines; the plain transcript is byte-identical to the receipt
(CritReceiptForge control `7b8cda36…`). Base and r39-head negatives are genuine (`base=3/10`,
`r39=2/10`, both exit 1). Forged receipts — payload-contradicting, future-dated, different-ref,
summary-only, tampered `H7 payload=` line — are all rejected. The `R40_NEG_BASE`/`R40_NEG_R39` knobs
cannot mint a green receipt (H5/H7 catch it at production).

Routed to round 41 (instrument robustness; no change to the frozen counter this round):
- H2 substring match accepts wrong receipt values (`closed=7/80`, `failures=10`) — fix with token boundary (RevC1Counters D1).
- H3 has no fence awareness — a fenced `M39-2` row passes (RevC1Counters D2).
- H9 symlink escape: a declared path whose target is outside the export passes — fix with `readlink`-resolved path under the export root (RevC1Counters D5; RevC1Sandbox agrees).
- H6 name-family match is case/separator-sensitive (`Kasegi-R40-stray`, `kasegi_r40-stray` pass) (RevC1Counters D6); top-level-only scan misses nested and dot-prefixed leftovers (LabExportClean F/D1-D2, CritKillRule F1/F3); H6 selftest mutants miss 4/8 H6 mutations (LabExportClean D4).
- H1 registry-row regex accepts a row that merely mentions the instrument (RevC1Counters D8).
- H5 forged detection is count-relative; under an already-mismatched payload an additional forgery is not independently flagged; H7's graded selftest does not isolate the payload-value comparison (MutH1H5; wave-1 M11/M08 family).
- CritKillRule: 7 kill-rule escape states reproduced (nested scratch, work-inside-family container, dotfile dir, symlink-to-work tolerated, etc.) — the kill rule's cleanliness clause is not a stable predicate of leftovers; routed with the H6 fixes.

**C2 — decision set reproduces; the S022/S024 teaches rewrite restored.** RevC2Decisions verified every
frozen count at Y (queued 0, mined 7, entries citing nine 7, S060+ 3, frontier 23, harness 26/26,
binding 54/54, census exit 0, measure 43/43) and found one committed defect: the integration commit
`4766b9d` applied only status (and used-by on mined rows) — the delivered `teaches` rewrite for the two
rejected rows S022/S024 was dropped, leaving the committed rows with queued teaches text while the change
log claimed "reason+flip in row". This wave restored the teaches cells to the delivered
`REJECTED: …; flip: …` text (SOURCES.md L28/L30), matching the other eight rejected rows. Lesson Census
line 27's garbled parenthetical ("tier A +3?mined …") is read as "tier A +3 (mined S016/S017/S019/
S020/S021/S023/S025/S060; rejected S061/S062; carried S022/S024 flips)". Observations recorded: O1
supersession chain S022→S030→S031 is traversable and the S022 flip names S030 as specified; O3 counter
blind spots (severed used-by → census W03 only; ghost used-by on a rejected row unchecked; queued revert
caught only by the claims awk counter); O4 junk control rejected (mined=0 < 4).

**Entries — all eight PASS Q1–Q6.** RevC2Entries re-ran source-recheck (all green), Q1–Q6 per entry, and
cold-cwd `bash -n` on every recheck line. Minor infidelities recorded, not fixed (cosmetic; anchors and
verbatim spans still locate the quoted bytes): S020/S025 anchors one line early in three places; S023
capture contains U+202F characters so one quote is whitespace-normalised rather than byte-exact; the
cve-bench entry quotes the paper's own dead GitHub link (`uiuc-kanglab` 404; live is `uiuc-kang-lab`);
S060 manifest `full_text_lines=22795` is the split(`\n`) count vs `wc -l` 22794; manifest UA
`kasegi-shokunin/1.0` vs capture-source.py's longer string (identical bytes).

**Sibling/assimilation check.** ScoutSiblingFinal: no entry names a sibling lane (0 matches); tabi's
round-34 mirror of kasegi's VEX-entry diff is not a tabi claim; shokuknow `lanes/kasegi/CHANNELS.md:15`
still calls NIST SP 800-216 "queued" (stale upstream snapshot — this lane mined S019; do not re-adopt).
CritSourceTruth: all 8 round-40 captures match manifest digests/lines/bytes; source-recheck green for
S016/S060. ConnPatterns suggestions (extend census E11 used-by limb; port H4 scan to lesson Gate; derive
H2/H3 expectations from committed records) recorded for round 41.

