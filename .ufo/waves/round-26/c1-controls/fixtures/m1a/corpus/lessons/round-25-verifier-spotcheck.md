# Round 25 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_flash)

Scope: kasegi lane-round 25 only. Base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` →
tip `41a77b83f3a338053fa69629d753546b8d592617` (branch `master`). Every figure below was
re-run by this reviewer on 2026-10-25 against committed bytes (`git show <rev>:<path>`
extracted to a scratch dir, or the clean lane worktree at the tip). The lane's report
figures were not trusted.

Driver digest (copied from mutable `.ufo/watchdog.log`):

```
2026-10-25T05:06:21-03:00 launch kasegi round=25 pgid=4033181 driver=hyaku-inline attempt=1
2026-10-25T06:09:34-03:00 complete kasegi round=25; hyaku-inline attempt=1
```

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report authored by lane identity | `git log --format='%an <%ae> %H' -- .ufo/reports/round-25/kasegi.md` (fleet repo) | `kasegi-shokunin <kasegi@shokunin.local> b051de355432baf65f5399559f65a15f0b89b587` | ok |
| `SHONEN` heading, one line per box | read report | `## SHONEN` with 4 `[~]` lines | ok |
| cited commits exist + on branch | `git cat-file -t` and `git merge-base --is-ancestor <h> master` for `98261eb…`, `41a77b8…` | `commit`, ancestor-of-master ok (both) | ok |
| round commits carry lane identity | `git log --format='%an <%ae> \| %cn' b49948f..41a77b8` | both commits `kasegi-shokunin <kasegi@shokunin.local>` | ok |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `branch=master local=remote=41a77b8… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | ok |
| prompt carries template contract | `diff <(sed -n '1,140p' .ufo/prompts/kasegi-round-25.md) templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §6 hyaku addendum appended | ok |
| misroot sweep (lesson M25-4) | `ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-25/` | `No such file or directory`; both files present under the lane's `wave1/` | ok |

Not a marker report: two claims with commands, receipts and a landed commit.

## Claims — re-measured

### C1 · depth:verifiability — re-measured (plain shell, no lane instrument executed)

Per `corpus/knowledge/*.md`, the first `recheck:` line, value after `recheck:` piped to
`bash -n`; prefix test for `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `.

| bytes | files | recheck lines | `bash -n` fail | abs `cd` prefix | other cwd-invariant |
|---|---|---|---|---|---|
| base `b49948f` | 35 | 35 | **23** | 5 | 1 (`root-loss-2026-10-12.md`, `~/`-only tests) |
| tip `41a77b8` | 37 | 37 | **0** | 36 | 1 (same file, unchanged) |

So pass-by-form before = 5 + 1 = **6/35**, the other 6 parse-OK lines use bare
`python3 corpus/instruments/…` relative paths (cwd-dependent) — matches the reported
`pass=6 parse_fail=23 cwd_fail=6`. After: 37/37 parse and are cwd-invariant by form —
matches `pass=35` (frozen surface) and `pass=37` (final tree).

Kill rule ("a line reaches pass by deleting its fail-closed test") re-checked: of the 35
base entries 29 changed, each by exactly one line (`diff | grep -c '^[<>]'` = 2 for all 29);
every `test [!] -X <path>` clause in a base line appears verbatim in its tip line
(**lost_test_clauses=0**, 34 base clauses total). Gated/executes split, evaluating only
the `test` builtins of each tip line: all-true **14**, at least one false **23** — matches
`executes=14 gated=23`.

Evidence-verified, not re-run (lane instrument): `sha256sum corpus/instruments/recheck-audit.py`
= `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`, equal to
`c1-instrument-digest.txt` and to `instrument_sha256` in `c1-before-strict.json`,
`c1-after-35.json`, `c1-after.json` (pass 6 / 35 / 37). Selftest tally
`cases=14 failures=0 exit=0` is evidenced only in wave-2 reviewer prose
(`wave2/C1InstrumentDigest.md:61`, `C1SemanticsAudit.md:30`, `C1FrozenPredicate.md:34`) — see R25-2.

Verdict: **improved** (score held 4, as the lane itself says; the measured surface moved
6→35/35, 23 syntax-error lines became fail-closed commands). Caveat accepted from the
lane's own disclosure: the frozen limb (b) is an equality check; the claim is met via the
strict limbs added post-freeze; my plain re-measure is independent of either.

### C2 · coverage — re-measured

| counter (frozen in `claims.json`) | base `b49948f` | tip `41a77b8` |
|---|---|---|
| `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}'` over `git show <rev>:corpus/README.md` | 9 | **10** |
| `grep -lE '^source: S0(3[6-9]\|[4-9][0-9])' corpus/knowledge/*.md \| wc -l` | 0 | **2** |
| `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| *S[0-9]{3} '` | 35 | **40** |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (tip) | — | `ok`, exit 0; only W04 S028, W04 S029 (pre-existing) |

Kill rule ("row appended without an admitted entry citing it"): `grep -l S03N
corpus/knowledge/vendor-*.md` — S036, S038, S039 cited by both entries; S037 by
`…as-corpus-objects.md`; S040 by `…commitments-crosswalk.md`. 5/5 cited. `SOURCES.md`
numstat `5 0` (append-only). Capture digests: `sha256sum S036..S040.txt` prefixes
`022ca4f4 b204aa7f 09e077d3 657e7b4c b7f7b55f` = manifest `sha256` fields. Manifest
round-25: 5 records / **40** assertions (`sum(len(s['quotes']))`).
`frontier-recheck-count.py` 12/12 evidence-verified from wave-2 receipts, not re-run.

Verdict: **improved** (score held 7).

### Routed-defect corrections (D24-*) — spot re-checks

- D24-2: `sum(len(s['quotes']))` over `corpus/source-snapshots/round-24/manifest.json` = **76**
  over 19 records — matches.
- D24-3: `.ufo/waves/round-25/d24-3/receipt.txt` shows mutant resolver `88122e10…`
  `cases=8 pass=8 exit=0` (dispatch) and the containment run — receipt exists and matches the
  SCORECARD sentence.
- Append-only: `LOG.md` `59 0`, `corpus/lessons/round-24.md` `18 0` (erratum appended).

### No owned axis harmed

`git diff b49948f 41a77b8 -- SCORECARD.md`: no axis-score row changed; only the R11
paragraph and the source-capture row (77→76) were edited, plus the round-25 section.
`SKILL.md` is absent from `git diff --name-status` (bytes untouched) → depth:density
**unchanged**. PROVINCE.md: frontier sentence F01–F09 → F01–F10 only.

| axis | verdict |
|---|---|
| depth:verifiability | improved |
| coverage | improved |
| depth:density | unchanged |

## Discernment spot-check (lesson `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S038 GMOペパボ 脆弱性報告制度 | admit | `curl -sSL` https://pepabo.com/contact/vulnerability-reporting/ → http 200, 37,806 B; `法的措置をとらない方針です` 1 hit, `現在、報奨金制度は設けておりません` 1 hit; capture `S038.txt:17` holds the lesson's quote byte-exact | agree | live page and capture both carry the no-legal-action undertaking and the no-bounty sentence the row teaches (L17, L20) |
| S040 Cisco Security Vulnerability Policy | admit | browser UA → http **403** (as the lesson's access note says); instrument UA (`capture-source.py:32`) `curl -L` → 301 → `sec.cloudapps.cisco.com/…/security_vulnerability_policy.html` http 200, 94,027 B; `aligns its practices with <a …>` present; four `<li>` expedite bullets | agree | row's "four situations … (L301 to L309)" matches live page and `S040.txt:301-309`; note the canonical URL now redirects (R25-5) |
| staged `vendor-cvd-policy-crosswalk-2026-10-23.md` (`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`) | reject | file L31 "**two conditions** under which it will go faster"; L6 `recheck:` is prose around a backticked `curl`; L7 `ground: F20`; `grep -cE '\| F20 ' corpus/README.md` → 0; `S040.txt:301-309` and the live page list four bullets | agree | all three refusal grounds reproduce; the theme is still admitted under the re-grounded lane entry, so the refusal targets the staged text |
| correction "invitation-only unsupported" | (gate correction) | `grep -c 招待 corpus/source-snapshots/round-25/S03[6-9].txt` → 0,0,0,0 | agree | the staged wording has no support in any Japanese capture |

`SOURCES.md` row re-opened: **S040** — `teaches` "states alignment with ISO/IEC 29147:2018
(L58) … lists four situations in which it will expedite disclosure … (L301 to L309) …
discloses … simultaneously (L310)"; `S040.txt:310` = "All Cisco security publications are
disclosed to customers and the public simultaneously." The ≤25-word located quote for the
row is in the lesson Gate table (`"The Cisco PSIRT aligns its practices with ISO/IEC
29147:2018,"`, capture L58, 9 words) — within limit, location named.

Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok`, exit 0.

## Trend verdicts

- **expansion — improved.** README frontier admitted 9→10 (F10 row at `corpus/README.md:211`);
  registry 35→40 tier-A rows; two new entries citing all five.
- **quality — improved.** 23 non-parsing `recheck:` lines → 0; 6 cwd-dependent → 0; zero
  fail-closed tests lost; the round-24 assertion count corrected to the measured 76; five
  captures hash-pinned and equal to their manifest digests.
- **discernment — improved.** The refusal and the capture-forced corrections reproduce on
  re-open (four bullets, `招待` absent, F20 absent); 4/4 sampled decisions agree.

## Routed defects (lane fixes next round)

- **R25-1 · frozen claims file edited after freeze.** `claims.json` says frozen
  `2026-10-25T08:13:38Z`, but the lesson (`round-25.md:130-131`) states its planned reject
  reason was "corrected in place", and it carries a post-freeze `counter_notes` block; the file
  was first committed only at round end (`98261eb`), so no commit pins the frozen bytes.
  Fix: commit `claims.json` at freeze; land corrections as a separate appended file.
- **R25-2 · selftest tally not in the committed receipt.** `wave2/C1InstrumentDigest.md`
  says the selftest "matches `c1-receipt-index.txt:4` exactly"; committed line 4 is
  `executes=12 gated=0 broken=23` and the index has no selftest line. Fix: commit a selftest
  receipt at digest `c3c19adc…` and correct the reviewer cross-reference.
- **R25-3 · new gate without a registry row.** `recheck-audit.py` exits 0/1 and has
  `--selftest`, but `grep -c recheck-audit SKILL.md` → 0 (registry home per PROTOCOL
  §Gate standard, Registry/Delivery). Not gradable conformant until registered as
  `gate|probe` with verdict map, selftest spelling and pinned-value path.
- **R25-4 · fix-control fails on its own bytes.** Lesson "Fixes that can fail" #3 says
  `grep -rn '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md
  corpus/lessons/round-24.md` returns 0 hits; it returns 1 (`corpus/lessons/round-24.md:77`,
  the retained historical sentence). Restate the control to exclude the historical line.
- **R25-5 · S040 recheck URL drift.** The registry URL now 301-redirects to
  `sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`
  and 403s a browser UA; record the final URL / UA requirement in the row's next recheck.
- **Lane-declared open debt (carried, still open):** entry-file deletion shrinks the audited
  set while passing; `anchorcheck.py` exits 0 on every verdict; `capture-source.py` `TAG_RE`
  lossy + no `render`/`raw_sha256` fields; `source-recheck.py --source` single-valued.

Operator note (not a defect): the round committed ~3.77k files / ~65 MB of wave evidence
under `.ufo/waves/round-25/` (`wave1/` 33M, `wave2/` 18M, `c1-controls/` 12M); a full
`git diff` over the round takes ~40 s.

SHONEN: all four boxes remain `[~]` lane self-assessment. Boxes 2 (end-to-end task logged)
and 4 (no cross-domain bleed) look checkable by a non-author from committed evidence; box 1
leans on `anchorcheck.py bad=0`, which the lane shows cannot fail, and box 3 holds by form
only (23/37 rechecks gated on lost bases). Promotion stays operator-owned.
