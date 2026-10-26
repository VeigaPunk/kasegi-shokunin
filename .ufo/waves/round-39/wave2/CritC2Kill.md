# CritC2Kill — round 39, wave 2 (falsify): C2 (coverage) attacked as frozen

Seat: critic, leaf (no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
only. Judged head **J = 46c66c268502abd1b2c342fc71bf88ccf721845b** and lane tip
**Y = 5006097a84305267c9a3e8c1e1d560e60fe41d37** (from `final-gates/all-gates.txt`
`export-ref=` and `git log`); all attack targets were read at **HEAD = Y** (the C2 artifacts
are unchanged between J and Y — `git diff --name-only J Y` carries only the receipt, per the
judged-head rule). I did not author any C2 byte under attack.

## Verdict

**C2 holds. No kill limb fired.** Every frozen counter reproduces exactly at HEAD, the negative
twin stays 4×`MISMATCH exit=1` under four attempt classes, deleting the capture or the manifest
reds both the harness and `source-recheck`, and a tier-C downgrade produces a new census W code.
One live Q3-precision candidate (a blockquote cited one line short), one stale-scope measurement
(the id-collision rerun), and four instrument-boundary defects were found; none changes a frozen
number, and each is listed with its smallest safe correction in §6–§7.

Axes touched: **coverage** (claim under attack), **depth:verifiability** (every finding below is
about what the instruments can and cannot see). No move here lowers any axis.

## 0. Ground truth at HEAD (before any attack)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                          -> 22
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 59   (erratum E1; as-frozen 58)
$ grep -rlE '^source: S057' corpus/knowledge | wc -l                   -> 1
  corpus/knowledge/cisa-when-to-issue-vex.md
$ ls corpus/knowledge/*.md | wc -l                                     -> 51
$ python3 corpus/instruments/frontier-recheck-count.py
  PASS     F22  knowledge/cisa-when-to-issue-vex.md  ids=S057  exit=0
  entries=25 pass=25 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057
  S057:sha256 OK
  S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
  S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
  S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
  S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
  EXIT=0
$ python3 corpus/instruments/capture-binding-check.py
  AUDIT records=46 with_url=46 with_fetched_utc=8 with_archival=38 snapshot_dirs=15 manifest_dirs=15 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
  records=46 bound=46 unbound=0
  EXIT=0
$ python3 corpus/instruments/recheck-audit.py --quiet
  strict pass=51/51 cdroot_fail=0 instrument_fail=0 own_fail=0
  lines=51 total=51 pass=51 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
  expect=present expected=51 missing=0 unexpected=0 exit=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
  kasegi  W04  S028 duplicate url docs.hackerone.com/...
  kasegi  W04  S029 duplicate url eur-lex.europa.eu/...
  kasegi  ok   /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
  EXIT=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
  kasegi rows 59 | tier.A 55 | tier.B 2 | tier.C 2 | status.mined 44 | status.queued 9 | status.rejected 6
  EXIT=0
```

Base/before state, read from the base commit (not from `before.txt`):

```
$ git show 480b1a50:corpus/README.md | grep -cE '^\| F[0-9]+ \|'         -> 21
$ git show 480b1a50:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' -> 55
$ git ls-tree --name-only 480b1a50 corpus/knowledge/ | wc -l             -> 50
$ git ls-tree --name-only 480b1a50 corpus/source-snapshots/round-39/     -> (empty)
```

Row/registry shape and provenance, checked byte-wise:

```
$ awk -F'|' 'NR==62{print "NF="NF}' corpus/SOURCES.md                  -> NF=13
$ awk -F'|' '$2 ~ /S057/{print $4,$5,$9,$10,$11,$12}'                   -> docs A mined 2026-10-26 180d corpus/knowledge/cisa-when-to-issue-vex.md
$ awk -F'|' '$2 ~ /S05[689]/{print $2,$9,($8 ~ /flip:/ ? "flip=yes":"flip=NO")}'
  S056 rejected flip=yes | S058 rejected flip=yes | S059 rejected flip=yes
$ sha256sum corpus/source-snapshots/round-39/S057.txt
  11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f      (== manifest sha256, == entry prose, == wave1/ExecFrontierCapture.S057.txt)
$ wc -l -c corpus/source-snapshots/round-39/S057.txt                    -> 275 17971   (== entry prose)
$ git ls-tree -r --name-only HEAD corpus/source-snapshots/round-39/     -> S057.txt, manifest.json   (both committed)
$ sha256sum corpus/.../S057.txt .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt  -> identical digest
$ wc -c .ufo/waves/round-39/wave1/ScribeRowS057.row.md                  -> 948
  (row line in SOURCES.md is the same 948 bytes, sha256 176762ea6a22ecff…: "byte-identical" confirmed)
$ ls corpus/knowledge | wc -l ; grep -vc '^#' corpus/instruments/knowledge-expected.txt -> 51 / 51
```

Both instruments' own controls are intact: `frontier-recheck-count.py --selftest` →
`selftest cases=6 failures=0 exit=0`; `source-recheck.py --selftest` → `selftest cases=10
failures=0 exit=0`.

## 1. Item (a) — can the junk-f22 claims be accepted?

Baseline (independent re-run, capture + manifest copied to scratch so nothing in the lane is touched):

```
$ S=/fast/scratch/hyaku/kasegi-r39/CritC2Kill; cd $S/junk
  (S057.txt = corpus capture copy; junk-manifest.json = c2-controls/junk-manifest.json)
$ python3 <lane>/corpus/instruments/source-recheck.py --manifest junk-manifest.json
  S057:sha256 OK
  S057:J1 MISMATCH reason=quote-not-found
  S057:J2 MISMATCH reason=quote-not-found
  S057:J3 MISMATCH reason=quote-not-found
  S057:J4 MISMATCH reason=quote-not-found
  EXIT=1
```

Four attempt classes, each aimed at a limb that could launder a fabricated sentence:

| attempt | variant | result |
|---|---|---|
| a1 anchors | every J-quote given an in-range `anchor` (13..16) | `J1..J4 MISMATCH reason=quote-not-found`, `EXIT=1` |
| a2 markup | each quote wrapped `<u>…</u>` (normalizer strips tags) | `J1..J4 MISMATCH`, `EXIT=1` |
| a3 whitespace | quote rebuilt with newlines/double spaces (collapse path) | `J1..J4 MISMATCH`, `EXIT=1` |
| a4 forbidden routes | duplicate ids / empty quote / quote < 12 normalized chars | `UNAVAILABLE reason=duplicate-quote-id` / `reason=empty-quote` / `reason=quote-too-short-to-be-evidence`, exit 2 |

**The four claims as worded cannot be accepted.** Two adjacent routes do pass, and both are the
instrument's *declared* semantics, not a defect of this round's control:

```
a5  replace the quote with a genuine capture sentence, keeping id=J1 and location="fabricated claim 1"
    -> S057:J1 OK normalized=markup-whitespace occurrences=1 ; EXIT=0
a6  16-char generic phrase "VEX information" + anchor=12
    -> S057:J1 OK occurrences=50 anchor=12-ok ; EXIT=0
```

`source-recheck.py` verifies that a pinned quote still exists in the capture; it does not verify
that the quote supports the claim (its docstring says so). a5/a6 are the residual gap between
"quote present" and "claim supported" — see F5 in §6. Neither route can rescue J1–J4, which are
paraphrases absent from the capture under every normalization the instrument applies.

## 2. Item (b) — swap the S057 citation to S054/S055

Mirror construction (this matters; see F2): `L` = `git archive HEAD corpus` extracted to scratch,
with every entry's absolute `cd` path rewritten to the copy (`perl -pi -e 's|…/L|…/L_x|'`).
Baseline on the mirror: `F22 … ids=S057 exit=0`, `entries=25 pass=25 exit=0`.

| # | swap | harness verdict |
|---|---|---|
| b1 | entry header `source: S057` → `source: S054` only | **FAIL** `problems=header-sources-not-rechecked,selection-not-declared-by-entry`, `entries=25 pass=24 exit=1` |
| b2 | header + `recheck: … --source S057` → `--source S054` (round-39 manifest unchanged) | **FAIL** `problems=manifest-missing-ids`, `pass=24 exit=1` |
| b3b | recheck manifest only → `round-37/manifest.json` (header stays S057) | **FAIL** `problems=manifest-missing-ids`, `pass=24 exit=1` |
| b5 | README row entry cell → the S054 SSVC entry | **FAIL** `DUPLICATE-ENTRY F20,F22 …`, `exit=1` |
| b3 | header + recheck + manifest all moved to S054; body quotes left as S057's | **PASS** `ids=S054 exit=0`, `entries=25 pass=25 exit=0` |
| b4 | F22 row `sources` cell `S057` → `S054` only, everything else untouched | **PASS** `ids=S057 exit=0`, `entries=25 pass=25 exit=0` |

Reading: the *entry's* citation is bound — an inconsistent swap reds on three different limbs
(declaration↔selection both directions, selection↔manifest). The two survivors are exactly the
places where nothing binds: the entry's evidence text is never compared to the manifest's quote
set (b3), and the frontier row's `sources` cell is read by no instrument (b4). F1/F5 in §6.

## 3. Item (c) — delete the capture or the manifest (scratch mirror, `cd` repointed at the copy)

```
c1  rm corpus/source-snapshots/round-39/S057.txt
    harness: FAIL F22 … exit=2 problems=recheck-exit-2 ; entries=25 pass=24 exit=1
    source-recheck: S057:source UNAVAILABLE reason=missing ; EXIT=2
c2  rm corpus/source-snapshots/round-39/manifest.json
    harness: FAIL F22 … problems=manifest-unreadable ; entries=25 pass=24 exit=1
    source-recheck: manifest UNAVAILABLE reason=missing ; EXIT=2
    binding: FAIL rule=missing-manifest dir=round-39 ; records=45 bound=45 (record set shrinks with the manifest)
```

Both red as the kill rule requires. The binding instrument stays **green** on c1 (`records=46
bound=46 unbound=0`) — that is its documented scope ("the reverse direction (a record naming a
file that is absent) is not a rule here — `source-recheck.py` fails closed"), not a defect:
`source-recheck` is the limb that carries it.

Control confirming the capture is load-bearing: delete the capture **and** drop the record, leaving
`--source S057` in the entry → `manifest-missing-ids` (no second manifest in the lane lists S057).

## 4. Item (d) — downgrade S057 tier A→C on a mirror

```
tier=[ C ] status=[ mined ] usedby=[ corpus/knowledge/cisa-when-to-issue-vex.md ]
$ bash <fleet>/scripts/sources-census.sh validate $S/L_d
  L_d  W04  S028 … | L_d  W04  S029 …
  L_d  W01  S057 tierC mined used-by=corpus/knowledge/cisa-when-to-issue-vex.md
  L_d  ok   …/L_d/corpus/SOURCES.md
  EXIT=0
```

Flagged, as the rule (`tier=="C" && status=="mined" && usedby!="—"` → W01) requires. Fleet
property worth recording: **W codes never change census exit** ("exit: 0 clean or warnings"), so
`exit=0` alone does not carry this; the kill rule's "a new W/E code" limb is the discriminating
half. Baseline census (before/after) prints the same two pre-existing W04 and nothing else, so W01
is unambiguously new.

Adjacent probes on the same axis:

```
tier A -> B   : census `ok`, exit=0, no W/E code.  PASSES SILENTLY  (F3)
status mined -> rejected : census `ok` exit=0, but binding FAILs `rule=rejected-row-anchor record=S057 row=S057`
used-by -> corpus/knowledge/nonexistent-s057-entry.md : census `E11 S057 missing used-by …`, EXIT=1
```

## 5. Item (e) — prose citation with the binding on another source

Built on the mirror: a new entry `corpus/knowledge/prose-s057.md` whose header is `source: S054`,
whose recheck selects `--source S054` against the round-37 manifest, and whose body mentions S057
only in prose; the F22 frontier row points at it with `sources` cell `S057`.

```
$ python3 …/frontier-recheck-count.py --root $S/L_e | grep -E 'F20|F22|entries='
  PASS     F20  knowledge/ssvc-… .md  ids=S054  exit=0
  PASS     F22  knowledge/prose-s057.md  ids=S054  exit=0
  entries=25 pass=25 exit=0        HARNESS_EXIT=0
$ grep -n '^| F22 ' $S/L_e/corpus/README.md
  506:| F22 | … | admitted | knowledge/prose-s057.md | S057 | …
```

Confirmed **known property, as the item states**: a prose mention is a reference, not a
declaration (`entry_contract` skips declaration lines before collecting `cited`), so an entry that
binds S054 while the row advertises S057 still PASSes. The PASS line is not forgeable *by prose*
(the `--source` set is what is executed and it is bound to the declared set), but it is also not a
verdict about the row's advertised source.

## 6. Defects found in the landed bytes and instruments

Each has a measured counterexample above; severity is my judgment of harm to the frozen claims.

**F1 — the frontier row's `sources` cell is read by no instrument (b4).**
`frontier-recheck-count.py:95` documents "Return [(id, title, status, entry_path)]" and
`rows.append((m.group(1), m.group(2), m.group(3), m.group(4).strip()))` discards group 5; no other
instrument of record parses the F table (`r39-closure.sh` reads `corpus/README.md` only for the
declared tail and the fence walk). Swapping `S057`→`S054` in the F22 row leaves
`entries=25 pass=25 exit=0`. Consequence: erratum E5 §9's content binding ("the F22 frontier row
names entry … and sources `S057`") is editorially verified only. **Axis:** depth:verifiability.
**Smallest safe correction:** extend `evaluate()` with one limb — `sources cell ⊆ declared ∪
evidence ∪ {row-level source ids}`; or, if the row cell is meant to be editorial, state the limit
in the docstring (one sentence) and keep the spot-check item that reads it by eye.

**F2 — `--root` does not scope the executed command; the entry's own `cd` does (mirror trap).**
Counterexample on the mirror `L_c1x` = copy of L with `S057.txt` deleted and the entry's `cd`
left pointing at `L`:

```
$ ls $S/L_c1x/corpus/source-snapshots/round-39/     -> manifest.json          (capture absent from the audited root)
$ grep -o 'cd [^ ]*' …/L_c1x/corpus/knowledge/cisa-when-to-issue-vex.md | head -1
  cd /fast/scratch/hyaku/kasegi-r39/CritC2Kill/L
$ python3 …/frontier-recheck-count.py --root $S/L_c1x | grep -E 'F22|entries='
  PASS     F22  knowledge/cisa-when-to-issue-vex.md  ids=S057  exit=0
  entries=25 pass=25 exit=0        HARNESS_EXIT=0
```

The harness runs the entry's command with `cwd=root`, but a leading `cd <abs>` overrides it, so a
mirror run can certify a tree it never read. The lane's own `recheck-audit.py` already carries the
missing limb (`(d) cdroot`) and catches exactly this: `--root L_c1x` → `strict pass=1/51
cdroot_fail=50 … exit=1`. **Axis:** depth:verifiability (this wave runs mirrors; its c1/c2 arms
were only valid after I repointed each copy). **Smallest safe correction:** copy audit's cdroot
limb into the harness (`recheck-cd-not-root` when the leading `cd` ≠ `realpath(root)`) plus one
selftest case; or forbid `--root` mirror use in the docstring.

**F3 — tier A→B is invisible to every instrument.** Census enforces only `tier ∈ {A,B,C}`, the
A/community rule, and C+mined+used-by. `A→B` prints `ok`, exit 0, no code. The frozen "tier A" is
therefore prose-only; `A→C` is caught (W01) but only as a warning. **Axis:** coverage /
depth:verifiability. **Smallest safe correction:** none required for this claim (the landed row is
`A`); record the limit beside the row-anchor rule, or add a tier-transition log (census has no such
rule today).

**F4 — capture bytes are forgeable together with the manifest digest; all three instruments stay
green.** On a mirror: append a fabricated sentence to `S057.txt`, update the record's `sha256`:

```
$ python3 …/source-recheck.py --manifest corpus/source-snapshots/round-39/junk-manifest.json (retargeted quote J1 = the appended sentence)
  S057:sha256 OK / S057:J1 OK occurrences=1 (J2-J4 still MISMATCH)
$ python3 …/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057
  S057:sha256 OK ; Q1..Q4 OK ; EXIT=0
$ harness --root $S/L_a7        -> PASS F22 ids=S057 exit=0 ; entries=25 pass=25 exit=0
$ capture-binding-check (in L_a7) -> records=46 bound=46 unbound=0
```

The only remaining pins for the capture are (i) the entry's and row's prose digest and (ii) the
committed wave-1 seat copy `ExecFrontierCapture.S057.txt` (same digest) — **and no instrument
compares either**. So "committed and bound" means *same-commit consistency*, not tamper evidence;
a round-39 capture has no earlier round to anchor it, only a live re-fetch. **Axis:**
depth:verifiability. **Smallest safe correction:** one limb (or G-check) comparing
`corpus/source-snapshots/round-39/S057.txt` to
`.ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt` (and to the row's prose digest); the
wave-1 artifact already exists, so this is a comparison, not new capture work.

**F5 — the harness never binds the entry's evidence text to the manifest's pinned quotes (b3).**
The entry can declare and recheck S054 (SSVC pins) while every blockquote in the body still cites
`S057.txt` — `PASS ids=S054 exit=0`. This is the mechanism behind a5 (quote substitution) too.
**Axis:** coverage (evidence fidelity) / depth:verifiability. **Smallest safe correction:** a
receipt-side limb "every `S0NN.txt:L…` citation in the entry body names a source in the entry's
declared set" (cheap, no capture read); the deeper "quote is in the manifest's pin set" limb is a
new instrument and should be scoped as such.

**F6 — one of 22 blockquotes is cited one line short; FC-1's headline rule contradicts its own
measurement rule.**
Entry line 36: `> "When the investigation has concluded, … “affected” or “not_affected.”" —
S057.txt:L134-L135`. The capture has the sentence beginning at the end of L133 and continuing on
L134-L135:

```
132: In general, VEX issuers are expected to communicate any changes in status. Ideally, when a
133: new vulnerability is disclosed, an “under_investigation” status should be issued. When the
134: investigation has concluded, status should be updated, for example, noting that the product is
135: “affected” or “not_affected.”
```

Machine check of all 22 blockquotes: `spans 22 distinct 22 words_max 25`,
**strict (quote fully on its declared lines) = 21/22, lenient (+1 line slack) = 22/22**; the sole
failure is `(134, 135)`. FC-1's headline says "every quoted span is verbatim, ≤25 words, **on its
declared line**", but its measured rule is the lenient one ("each declared line lies inside its
occurrence"), which is how it prints `anchors_ok=22 of 22`. **Axis:** coverage (QUALITY Q3,
"verbatim quote … with its exact location"). **Smallest safe correction:** `L134-L135` →
`L133-L135` in the entry (not in a declared G1 tail block, so G1 is unaffected; it does change Y's
tree, so it lands at the next head or as an appended correction, never as an in-place edit at Y).

**F7 — the harness prints `pass=25` while exiting 1 on a duplicate entry (b5).**
`DUPLICATE-ENTRY F20,F22 …` alongside `entries=25 pass=25 exit=1`: fail-closed on the exit, but a
receipt that quotes the `pass=` figure without `exit=` reads green. Minor. **Smallest safe
correction:** print `pass=` only over entries whose own status is PASS and count duplicate rows as
failing, or state in the docstring that `pass=` excludes the fail-closed checks.

## 7. Stale-scope measurement in the landed lesson (id collision)

`corpus/lessons/round-39.md` §Assimilation: "Id-collision rerun (0-3-space extractor): reg-ids 55
(S001-S055), staged-ids 94 (S031-S124), `comm -12` = 25 collisions (S031-S055)". The committed
evidence agrees — `wave1/ExecAssimilationIds.reg-ids` has 55 lines — because the wave-1 seat ran the
extractor on the **base** registry ("the base now carries `S048`–`S055`"). The landed registry,
however, is S001–**S059** (`legacy: census rows=59`; ids contiguous, unique), and the staged set is
S031–S124 (`corpus/lessons/round-24.md:36`, `round-29.md:80`; `SOURCES.append.md` has 94 rows).
Re-running the same 0-3-space extractor on the **landed** registry:

```
reg-ids: 59  staged-ids: 94  collisions: 29   (first S031, last S059; pre-addition subset = 25)
$ grep -E '^\|S05[6-9]\|' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md
  S056 Cybozu FAQ（脆弱性報奨金制度） | S057 脆弱性報告制度 (pepabo.com) | S058 IPA 届出受付 | S059 CNVD 漏洞周报
```

So all four ids the round adds (S056–S059) collide by number with staged *pointer* ids naming
different documents — staged S057 is GMOペパボ's vulnerability-reporting page
(`corpus/lessons/round-25.md:109`), not CISA. Under round-25's declared convention ("the
staged-package ids in parentheses are pointers, never ids") the reuse is legitimate, but the number
the round records (25) is the pre-addition value, presented in the same section as the addition.
**Axis:** coverage (identity/assessment precision). **Smallest safe correction:** append one
sentence to §Assimilation recording `reg-ids 59 → 29 collisions (S031-S059)`, noting the four added
ids are staged pointers; it is a lesson addition, so it goes through the same declaration/G1 path
as any other tail change at the next head.

## 8. What did **not** kill C2 (do-nothing and adversarial controls)

- Frozen counters: 22 / 59 (E1) / 1 / 51 / 25-25-0 / 46-46-0 / 51-0-0 / census 0 — all reproduce.
- Base state is genuinely before: 21 / 55 / 50 / no `round-39` snapshot dir / no S057 row.
- S057 row: NF=13, kind `docs`, tier `A`, status `mined`, opened `2026-10-26`, 180d, used-by the
  entry, one `https://` token equal to the manifest URL (binding B4/B5 pass).
- Entry: header shape matches F20/F21 (`source:`/`verified-at:`/`ground:`/`recheck:`), recheck
  executable and cwd-independent (`recheck-audit`: `parse_fail=0 cwd_fail=0`, strict 51/51), body
  ≫ 10 lines beyond the provenance trio, 8 rejected over-generalizations, Q1–Q6 otherwise met.
- Vocabulary self-checks in FC-2/3/4/5/6 reproduce exactly: `VEX=101 KEV=1 EPSS=0 SSVC=0 CSAF=0
  CVSS=0 inherit=4 action_statement=2 impact_statement=1 under_investigation=2 not_affected=3`;
  `component_not_present=1 vulnerable_code_not_present=1` and the other three flags `=0`;
  `under_investigation` at L111/L133; `could be inherited downstream` at L190; `business
  decision` at L13/L80.
- Row deliverable is byte-identical (`948 B`, sha256 `176762ea…`); capture 275 lines / 17,971 B,
  digest matches manifest, entry prose and the wave-1 seat copy.
- Junk twin: 4×`MISMATCH exit=1` under baseline, anchored, markup and whitespace variants.
- Deleting the capture or manifest reds harness + `source-recheck` (+ binding for the manifest).

## 9. Environment, scratch, tooling

- All scratch under `/fast/scratch/hyaku/kasegi-r39/CritC2Kill/` (`S`), `TMPDIR` not inherited;
  mirrors built with `git -C <lane> archive HEAD corpus | tar -x -C $S/L`; no writes to the lane
  except this receipt; `git status --porcelain -- corpus` empty after the runs;
  `PYTHONDONTWRITEBYTECODE=1` on every Python invocation.
- No tool installs, no upgrades, no `pacman`; nothing written to any PATH directory, no git/jj
  mutation (read-only `git show/ls-tree/log` only), no network fetch. Disk guard green
  (`/fast` 619 G free at start).
- Scratch dir removed before yielding.

## 10. Bottom line for the judge

C2's ten kill limbs were probed with the strongest local counterexamples I could build, including
mirror deletion, consistent citation swap, forged capture+manifest, tier and status downgrades, and
four junk-claim laundering routes. **No limb fired.** The claim as frozen is true at J/Y and its
negative controls are discriminating. The findings that a reviewer should carry forward are
precision and boundary items — F1/F2/F4/F5 (what the instruments cannot see), F6 (one blockquote
cited one line short, and FC-1's headline rule over-claiming relative to its measurement), F7
(minor receipt granularity) and §7 (collision count stated pre-addition). F6 is the only finding
that could be argued under the kill rule's "failing QUALITY Q1–Q6" limb, and only on a strict
reading of Q3's "exact location"; the one-line correction is named above.
