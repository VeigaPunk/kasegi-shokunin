# CriticClaims — round 83 attempt 1 (C1 depth:verifiability, C2 coverage)

Seat: critic. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, freeze
`0cd499dbdfc0bf9ce3095681af9bc76588d76f31`, base `834bf78eaca70a69294f2ecfefa89b73c3fa85b8`.
One v1 wave of 13 seats. Scratch `/fast/scratch/hyaku/kasegi-r83/CriticClaims`
(deleted before yield). Receipts in `CriticClaims-receipts/` (index at the end).

## Frozen bytes read

`git rev-parse HEAD` = the freeze commit. Hashes match `claims.json`:

| artefact | sha256 |
|---|---|
| `.ufo/waves/round-83/c1/recheck-cwd-census.py` | `343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9` |
| `.ufo/waves/round-83/c1/mutbat.py` | `2f7c49d44bb1f21e8286d1a8b54d4c57bccc0be990fd7946a57813db0d81cb7d` |
| `.ufo/waves/round-83/c1/mutant-table.json` | `5b1d99f59cede6cffa36d554ce7e8256bf1eba1cb84a9591bfbb9f7f386b6f44` |
| `.ufo/waves/round-83/c2/entry-gate.py` | `42f4b2accf704455325f8d1eb8ca4ec21401e35397af7a36861c33a27ace6302` |
| `corpus/source-snapshots/round-83/S117.txt` | `0a5fa51c987544789d3c84fee6be2b1246a7a6a865457668f9e94a37e60bd53e` |

The S117 draft entry read as `a91963a84e72bb38a78668a6a1c44b2f2ab90ceef0e898b92c135bcd62af00b0`
(untracked). ScribeLesson's `c3499b12…` is a stale revision; `corpus/SOURCES.md` is already
modified in the worktree and the SKILL/README pin rows already name `cases=27` there: the L1 is
integrating concurrently, so B1-B3 are not scored by me (landing obligations); B4-B7 are
recorded in the prefreeze receipt `.ufo/waves/round-83/controls/c2-prefreeze-r83.txt` and I did
not rerun them.

First-hand runs (receipts): P1 `selftest cases=27 failures=0` rc 0; P2 hash match; P3 exact line
rc 0 in 80.8 s (`p3-frozen-candidate.txt` + full 67-line output); P4 twelve FORGERY lines with
the expected rc values (`p4-forgeries.txt`); P5 `entries=97 … conformant` rc 0; P6
`mutbat selftest ok` with `r83_forgeries={'count': (True, False), 'hashwl': (True, False),
'path': (True, False)}`; B0 `S117:sha256 OK` + six `OK occurrences=1`; B8 first limb
`untied=0 … pass` on the draft; B8 second limb reproduced (`c2-controls.txt`).

**Absolute-lane trap (not a claim defect, a runner trap).** P5 with `--lane .` prints
`noprefix=97 … nonconformant`; B8 with `--lane .` prints `header=bad`. Both predicates need the
absolute lane the claims' `<lane>` means; a runner using `.` gets a spurious failure.

## (a) Predicate attacks

### F12 — a marker-aware table-reading forgery scores rc 0 (new residual class, not F8)

`build-f12-f13.py --kind f12` appends a block to the frozen candidate that replaces the main
guard and exits in `_fg_selftest()` on `--selftest`: the candidate's assertions never run. It
embeds the frozen table, reads its own bytes, and passes clean whenever its source contains the
counter's decoy markers (`_mutbat_k` from D1/D2, `# mutbat-<nonce>` from D3); otherwise it fails
the `kill_cases` of every row whose anchor/replacement count differs from the candidate's.

```
$ python3 -B .ufo/waves/round-83/w1/CriticClaims-receipts/build-f12-f13.py --kind f12 --lane . \
    --out <scratch>/f12/target.py --counter .ufo/waves/round-83/c1/mutbat.py \
    --seed 00000000000000a1 --work <scratch>/f12/w
COUNTER rc=0
DECOY keyed=yes nonce=00000000000000a1 d3_row=K-X1
MUTBAT target_sha256=f7560f158824b63314b1d9113bb79c25280b94cdb956fec49a937d98afb439fa \
  baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 \
  decoy=ok decoy_hidden=63/64
```

This is the exact P3 suffix at rc 0 with a different target. It is not F8: no AST comparison, no
embedded original, no candidate assertion. The keyed decoys are self-defeating against a target
that reads its own source: the nonce and the `# mutbat-` comment are visible in the target's
bytes, so "keyed" defeats a *precomputed hash whitelist* (F10) but not a *source-reading* forgery.
The claim's declared limit names only AST embedding; this class is unnamed.

### F13 — a comment-stripping missing-anchor-count forgery scores rc 0 under both counters

F11 (missing-anchor count, `>= 10` tolerance) plus a `tokenize` pass that drops COMMENT tokens
and right-strips the line. D1/D2 hide ~63 anchors and the tolerance accepts them; D3 hides
exactly one anchor by inserting a comment, and the strip restores it; a mutant (one anchor gone)
is still reported.

```
$ ... --kind f13 ... --seed 00000000000000a1
COUNTER rc=0
DECOY keyed=yes nonce=00000000000000a1 d3_row=K-X1
MUTBAT target_sha256=127c32a1fd3fdb243dbb4016a4e808f70ba274397e4acfede6bed19ef4c1e56a \
  baseline=ok rows=67 killed=64 survived=0 … neutral_ok=3/3 decoy=ok decoy_hidden=63/64
$ ... --seed 0123456789abcdef        # different D3 row
COUNTER rc=0 … d3_row=K-CL … decoy=ok
$ python3 -B .ufo/waves/round-82/c1/mutbat.py --target <same> --table <r83 table> …
MUTBAT … decoy=ok   (counter rc=0)
```

The literal task shape — tokenize, drop comments, then F6-style compare *without* the count
tolerance — is rejected (`--kind f6s`: `decoy=broken`, rc 1) by D1/D2. So the surviving residual
is the **count-tolerance variant**: D3's single comment is strippable, and D1/D2's 63 hidden
anchors are absorbed by the `>= 10` tolerance. The claim's "the decoy limbs reject the
enumerated path, hash and count forgeries" is true of F11's bytes and false of the count class:
a tokenize-based comment strip defeats the r83 D3, and the r82 counter already accepted the same target
(rc 0). This is a second residual class beside F8, and it is not the AST class.

### P1/P5 are one-line-junk-satisfiable; P3's summary is target-controlled

- Base instrument (`81677e9d…`) with one line changed —
  `print("selftest cases=%d failures=%d" % (len(done), len(failures)))` →
  `print("selftest cases=27 failures=%d" % len(failures))` — prints
  `selftest cases=27 failures=0` rc 0 and stays `RECHECK-CWD-RESULT conformant` rc 0
  (`p1-p5-junk.txt`). The three r83 checks do not exist in that file. P1 checks the printed
  count, not that 27 checks ran; P5 passes on the do-nothing base. This is the r82 F2 observation
  with a cheaper instance; P2 is the only anti-junk pin.
- F12/F13 print the exact P3 suffix with `target_sha256` of a forgery. P3 checks the suffix, not
  `target_sha256`, and not the 67 `MUTANT` lines; a counter that inflated the tally would pass.
  P3 is a re-run of the P2-pinned bytes, not an independent discrimination limb.

## (b) Claim statements vs the predicates

C1:
- The kill rule freezes the **counter, table, driver and stub-builder** bytes, but no P hashes
  them. P2 hashes only the candidate; P3/P4/P6 execute the others. A landing edit to
  `mutbat.py`, `mutant-table.json` or `c1-forgeries-r83.py` that prints the expected lines is not
  caught by P1-P8 (the kill rule's "bytes differ" limb is manual, not a predicate).
- "all three keyed decoys": P3 checks only `decoy=ok` (a conjunction inside the counter). The
  `DECOY keyed=yes nonce=<hex> d3_row=<id>` line is not a P3 condition, and P6's selftest
  exercises the keyed decoys on the TOY, not on the real target. A counter that ran two decoys
  but printed `decoy=ok` would pass P3.
- "killed on its declared check by all 64 non-neutral rows": P3 checks `killed=64` in the
  summary, not the per-row verdicts; F12/F13 show the summary is target-controlled.
- The C1 statement's sentence "three forgeries … that the r82 counter scores rc 0 exit 1 under
  the r83 counter" is garbled; P4's intended reading (rc 0 under r82, rc 1 under r83) is clear.
- P8 is a text pin; the freeze rows name `cases=24` (base and freeze), the worktree rows now
  name `cases=27`. P8 does not verify the instrument; P1/P3 do (for the pinned bytes).

C2:
- The kill rule freezes the **gate, manifest, snapshot and controls** bytes; B0 checks S117
  against the manifest but nothing hashes the manifest, the gate (`42f4b2ac…`) or
  `c2-controls-r83.py`. B8 runs them; a landing edit that prints the expected lines passes.
- B1's "no other registry row changes" *is* checked by the diff predicate (this is not a gap);
  B1's content is a manual reading of the diff.
- B2/B3 are count-level (96→97, 58→59); an empty/junk `.md` plus the frontier row would satisfy
  them. B8's gate is the only content check, and it is lexical (below).
- B8's first limb ("the entry passes the round-83 entry gate") is junk-satisfiable: an entry
  whose six `Falsifiable rule:` lines are vacuous restatements passes both gates (below).
- B4/B7 are global instruments (all snapshots / the registry), not S117-specific; they do not
  bind the new entry beyond the global audit.

## (c) Does the B8 forgery set prove G6 adds discrimination G5 lacked?

Yes for the three shapes, no for the class. Reproduced `c2-controls-r83.py`:
filler, crosscite and copyrule are **rc 0 under gate=r82** (G1-G5) and **rc 1 with untied=1**
under gate=r83; S113/S114/S116 pass both; S115 passes r82 and fails r83 (`c2-controls.txt`).
So G5 alone does **not** reject the three: G6's tie limb is what rejects them, and the set is a
fair demonstration for "rule cites another section's line" and "rule shares no content word".

It does not show G6 closes the class. A fourth forgery — six vacuous restatements, one per
claim, each reusing ≥2 content stems of its quote — passes **both** gates
(`g6-echo-bypass.txt`):

```
$ python3 -B .ufo/waves/round-83/w1/CriticClaims-receipts/build-all-echo.py \
    --src <scratch>/c2r/draft.md --out <scratch>/c2r/all-echo.md
$ python3 -B .ufo/waves/round-83/c2/entry-gate.py --entry <scratch>/c2r/all-echo.md \
    --manifest corpus/source-snapshots/round-83/manifest.json --source S117 --lane <abs lane>
ENTRY-GATE sid=S117 claims=6 want=6 spans=7 … ruleless=0 untied=0 header=ok
ENTRY-GATE-RESULT pass   rc=0
```

The six replacement rules are at `all-echo.md:17,25,33,41,49,57`; e.g. Claim 1 becomes "a
withdrawn record is a record whose field the page excludes (S117.txt:112)". They are
restatements, not falsifiable rules. G6 measures word overlap, so an echo passes; G5 measures
own-words + citation, so an echo passes there too. B8's first limb therefore admits a junk entry
whose rules are vacuous; the second limb's three forgeries do not cover this shape.

## (d) The S115 G6 finding: false positive of G6, not a defect of the entry

The frozen gate prints `sid=S115 … untied=1 … fail` (rc 1); the r82 gate passes the same entry.
Claim 2's rule is:

> a bounty hunter or a scanner author is not the audience the page names; a plan that treats
> this endpoint as a consumer-side vulnerability feed contradicts S115.txt:32. A reader checks
> it by reading the second sentence of the Experimental endpoint paragraph.

quote at S115.txt:32: "It is targeted to operators of home databases that OSV.dev imports from."

The gate's own `words()` sets are disjoint (`s115-words.txt`): quote
`{datab, home, impor, opera, targe}`, rule `{audie, autho, bount, check, consu, contr, endpo,
exper, feed, hunte, names, parag, plan, reade, readi, scann, secon, sente, side, treat, vulne}`,
intersection empty. The rule is a valid complement inference (targeted at home-database
operators ⇒ bounty hunters/scanner authors are not the audience; a consumer-side feed
contradicts the audience/purpose), cites the right line, and passes G5. QUALITY Q5 asks for a
falsifiable rule a reader can check; this is one. ScribeLesson's section B rewrites the same
rule to name "operators of home databases" and it passes `untied=0` — the gate rewards echoing
the quote's terms, which is not evidence the original is defective. Verdict: **G6 false
positive**; the entry is already admitted and the r83 gate would reject it. The claim's B8 does
not disclose this regression (the control output records it, but the claim's statement and
`do_nothing` do not).

The ScribeLesson vacuous echo ("a withdrawn record is a record whose field the page excludes
(S117.txt:112)") is the **same residual class as my six-rule echo bypass**: G6's ≥2-stem
overlap is a lexical tie, so a restatement that reuses quote words passes. The S115 finding is
the opposite-direction error of the same proxy: a legitimate complement rule with zero overlap
is rejected. Both are consequences of G6 being lexical; my six-rule version generalizes the
ScribeLesson probe to all six claims and shows B8's first limb admits it.

## Verdict and routed defects

No P1-P7 or B0/B8 predicate is false at the bytes I read; P8 and B1-B3 are landing obligations
(the freeze pins name `cases=24`, S117 is `queued`, knowledge 96 and FRONTIER 58; the worktree is
mid-integration). B4-B7 hold at the freeze per the prefreeze receipt (I did not rerun B4/B7). C1 and C2 as written are not
killed. The routed defects are instrument-level; the two that would change a class-level reading
of the prose are F13 (count class) and the G6 echo (gate class).

1. **C1 counter, Major (fixable).** F12 (marker-aware, rc 0) and F13 (comment-strip count,
   rc 0 under r82 and r83) are accepted by the frozen counter; the declared limit names only F8.
   Smallest safe correction: replace `single_decoy`'s comment insertion with a
   semantics-preserving **single-identifier rename chosen to touch exactly one row anchor**
   (29/64 rows have a unique identifier in their anchor). Probe: renaming `root6` keeps the
   frozen candidate at `selftest cases=27 failures=0` and makes both F12 and F13 report
   `FAIL gate-consume` (rc 1), so a rename-based D3 scores them `decoy=broken`
   (`d3-rename-fix-probe.txt`). A target that embeds the original (F8) still passes; that
   remains the declared limit. Alternatively declare F12/F13 beside F8 and add them to
   `mutbat --selftest`.
2. **C1 predicates, Minor (fixable).** Add sha256 predicates for the frozen counter, table and
   driver (and for C2's gate, manifest and controls); check the `DECOY` line and
   `target_sha256` in P3; or state that P2 is the only identity pin and P1/P5/P3 are re-runs.
   P1/P5 are one-line-junk-satisfiable (`p1-p5-junk.txt`); P3's summary is target-controlled.
3. **C2 gate, Major (partly fixable).** G6 has a false negative (vacuous echo passes both gates)
   and a false positive (S115, an admitted entry, fails r83). A non-echo limb (require a content
   word absent from the cited span/paraphrase, or a falsifiability marker) would reject the
   six-echo entry while a complement/body tie would pass S115; any lexical tie remains spoofable,
   so the honest fix is to declare G6 a heuristic and not use its pass as a rule-quality
   certificate. Calibrate on S115 (must pass) and `all-echo.md` (must fail).
4. **C2 predicates, Minor (fixable).** B8's first limb is junk-satisfiable (six echo rules pass
   both gates); B2/B3 are count-level; the gate/manifest/controls are unhashed. The same hash
   fix as (2) plus the echo calibration.

Fixable vs tradeoff: F12/F13, the S115 false positive and the unhashed artefacts are fixable;
the general "target inspects its own bytes/AST" class (F8) and the lexical nature of any G6 tie
are tradeoffs that must be declared, not solved. The canonical judge should not reject C1/C2 on
P1-P8/B0-B8 (none is false), but should read the class-level phrases ("count forgeries", "the
entry passes the gate") as instance-level unless the fixes above land.

## Files written

- `.ufo/waves/round-83/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-83/w1/CriticClaims-receipts/`: `frozen-bytes.txt`,
  `p3-frozen-candidate.txt`, `p3-frozen-candidate-full.txt`, `p4-forgeries.txt`,
  `p6-counter-selftest.txt`, `p1-p5-junk.txt`, `f12-marker-forgery.txt`,
  `f13-strip-forgery.txt`, `f6strip-control.txt`, `d3-rename-fix-probe.txt`,
  `c2-controls.txt`, `s117-gate.txt`, `g6-echo-bypass.txt`, `s115-words.txt`,
  `all-echo.md`, `build-f12-f13.py`, `build-all-echo.py`.

Tooling: none installed or upgraded (no pacman; no uv/npx/binary install). Scratch deleted at
yield.
