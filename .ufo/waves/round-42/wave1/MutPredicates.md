# MutPredicates — round-42 wave-1 predicate-satisfaction probes (receipt)

Scope: cheapest-satisfaction attack on each frozen predicate in `.ufo/waves/round-42/claims.json`
— for C1 a suite that *prints* the required lines without checking anything; for C2 the assigned
O4-class junk twin (mined-marked rows without capture), plus a deeper self-consistent *fabricated*
twin as the limit case. Question: do the claims' own `counting_commands` alone catch each cheat,
and where they do not, which limb is missing.

Everything ran on scratch copies (`/fast/scratch/hyaku/kasegi-r42/MutPredicates/`, removed on
yield). The lane repo was never written; `git status` shows only sibling wave-1 receipts.
No lane commit, no mutating git anywhere; `git archive` used read-only.

## C1 — print-without-checking suite (SURVIVES all five counting commands)

Mutant: `fake-r42-closure.sh` (31 lines, sha256 ee4a0d47…2717d3cc0). It does exactly five
branches: no `--export-ref` → exit 2; `git rev-parse --verify` fails → `ref-not-found` red;
either of the two frozen negative-control hashes → `closed=10/13 exit=1`; anything else →
thirteen `J<n> … closed=1` lines + `closed=13/13 exit=0`, and under `--selftest` thirteen
`selftest case=J<n> mutants=0/0 positive=pass payload-match=1 verdict=pass` lines +
`selftest cases=13 failures=0`. It never runs `git archive`, never touches `--work`, never
reads one byte of any exported tree. Runtime: 0.003 s.

Actual outputs (scratch, `--export-ref <ref> --work <dir> --scratch-root <dir>`):

| probe | result | exit |
|---|---|---|
| lane HEAD 0566bd6 (resolvable "Y" stand-in) | 13×`J<n> closed=1`, `closed=13/13 exit=0` | 0 |
| `--selftest` same ref | 13 graded case lines + `selftest cases=13 failures=0` | 0 |
| base 5053a7f | `closed=10/13 exit=1` | 1 |
| r41 judged head 1f74646 | `closed=10/13 exit=1` | 1 |
| plain run | `refusal: no --export-ref` | 2 |
| lane HEAD~30 57ea9ea (round-39 ref, no r42 artifacts at all) | `closed=13/13 exit=0` | 0 |
| unresolvable deadbeef… | `ref-not-found` + `closed=0/13 exit=1` | 1 |

Evidence nothing ran: `workdirs_found=0` — none of the passed `--work` dirs was ever created;
`git archive 0566bd6 | tar -t | grep -c r42-closure` → 0 (the suite isn't even in the ref it
"verifies"), green printed anyway.

**Verdict: the five counting commands are output-grammar checks, not behavior checks — the
print-only suite satisfies every one of them.** The whole discrimination load rests on two
frozen literal hashes; the suite needs no tree sensitivity at all. Missing limbs:

1. **Content-sensitivity / defeat-injection limb** — no counting command commits a *new* ref
   carrying an in-family defect (any F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP input)
   and requires the suite to red it. The negative controls are two fixed constants a cheat
   enumerates verbatim; an un-named ref like HEAD~30 greens freely.
2. **Export-execution witness** — no command verifies that `git archive <ref> | tar -x`
   actually ran or that the suite read the export (a `--work` side-effect, an instrument-sha
   bound to the exported tree, anything). The fake ran in 3 ms and created nothing.
3. **Payload-binding at count time** — J8 re-derives receipt payload values internally, but no
   counting command independently re-derives and compares a payload (r41 I8's own discipline,
   not present at the claims level).
4. **Selftest-depth limb** — `mutants=0/0 positive=pass verdict=pass` satisfies the required
   line shape; no command requires ≥1 actually-executed mutant per case or inspects the
   `selftest detail=`/`judge=` evidence lines the real suite prints.

Residual coverage exists only outside the counting commands: the kill rule's committed-artifact
and replay-limb clauses (a wave-2 receipt showing an in-family input accepted, or a J1–J7 check
lacking its replay) would kill this mutant — but nothing in the counting set itself forces a
defeat to be *executed*, so until such an artifact exists the cheat is indistinguishable.

## C2a — assigned O4 junk twin: mined-marked rows, no capture (CAUGHT, partially)

Mutation on a HEAD copy: appended `| S064 | … | spec | A | … | mined | 2026-10-28 | on-release |
corpus/README.md |` after S063 in `corpus/SOURCES.md`, and `| F25 | OSV schema | admitted | — |
S064 | … |` after F24 in `corpus/README.md`. Nothing else — no capture, no manifest, no entry.
Hashes: SOURCES.md baf2f44a→337c38a2; README.md 55710368→d1938dc8.

Counting commands, actual output:

| # | command | mutant output | claim wants | verdict |
|---|---|---|---|---|
| 1 | `grep -cE '^\| F[0-9]+ \|'` README | 25 | 25 | FOOLED (mark counted) |
| 2 | `grep -cE '^\|\s*S[0-9]{3,}\s*\|'` SOURCES | 64 | 64 | FOOLED |
| 3 | awk S064 `mined` cell | 1 | 1 | FOOLED |
| 4 | `grep -rlE '^source: S064' knowledge` | 0 | 1 | **CAUGHT** |
| 5 | `ls knowledge/*.md` | 60 | 61 | **CAUGHT** |
| 6 | `frontier-recheck-count.py --root` | `FAIL F25 — … problems=missing-entry`; `entries=28 pass=27 exit=1` | 28/28 + PASS F25 | **CAUGHT** — an admitted row's entry cell is a *counted* record; `—` fails closed |
| 7 | `capture-binding-check.py --root` | `records=55 bound=55 unbound=0` | records=56 | **CAUGHT** by the absolute count, *not* by unbinding: the instrument exits 0 and sees no anomaly at all (manifests are the only counted thing) |
| 8 | `recheck-audit.py --quiet --root --cdroot <lane>` | `expected=60 missing=0 unexpected=0 exit=0` | expected=61 | **CAUGHT** by the absolute count alone |
| 9 | `sources-census.sh validate <mut>` | `W04 S028`, `W04 S029`, `ok` → exit 0 | exit 0 | FOOLED — census validates row *shape* only; `used-by` just needs any existing path (E11), not a capture |

Verdict: the O4 class is caught — by five numeric assertions (4–8), not by any semantic limb.
Commands 1–3 and 9 see only marks and pass a junk row cleanly.

## C2b — limit case: self-consistent *fabricated* twin (SURVIVES all nine commands)

Same two rows, but this time backed by a hand-typed (never fetched) "capture":
`corpus/source-snapshots/round-42/S064.txt` (4 fabricated lines, sha256 72d280db…6027e6c) +
`manifest.json` whose record carries `status:200`, `fetched_utc:"2026-10-28T13:00:00Z"`, a real
`url`, and one quote verbatim from the fabricated text; entry `knowledge/osv-schema.md` with
the full provenance trio (`source:`/`verified-at:`/`recheck:` — every claimed value a lie);
name appended to `knowledge-expected.txt`. (My `recheck:` uses absolute scratch paths + a
`test -f ~/Projects/…` limb so it passes `--cdroot` outside the lane; a committed cheat needs
none of that — plain relative paths work inside the lane.)

Every counting command greens on fabricated bytes:

- `source-recheck.py --manifest …round-42/manifest.json --source S064` →
  `S064:sha256 OK`, `S064:Q1 OK occurrences=1 anchor=2-ok`, exit 0 — the manifest's sha256/quote
  fields are trusted verbatim; the URL in the record is never dereferenced.
- cmd1=25, cmd2=64, cmd3=1, cmd4=1, cmd5=61 — all pass.
- cmd6 `frontier-recheck-count.py` → `PASS F25 knowledge/osv-schema.md ids=S064 exit=0`;
  `entries=28 pass=28 exit=0`.
- cmd7 `capture-binding-check.py` → `MANIFEST round-42 records=1 url_bound=1 fetched=1`;
  `records=56 bound=56 unbound=0` — "bound" = URL-string-in-row + parseable `fetched_utc`;
  nothing asks whether a fetch happened.
- cmd8 `recheck-audit.py` → `osv-schema.md frozen=111 strict=111111 executes PASS`;
  `expect=present expected=61 missing=0 unexpected=0 exit=0` — my recheck *genuinely executes*
  (and genuinely verifies my own fabrication).
- cmd9 census → `ok`, exit 0 (standing W04 S028/S029 only, as the predicate allows).

Verdict: **counting commands check internal consistency of the artifacts; they are blind to
capture provenance.** No limb anywhere in the set binds bytes to a fetch — a discovery-receipt
hash, a re-fetch byte comparison, an instrument-stamped capture, or Gate-record verification.
Missing limbs: (i) capture-authenticity witness; (ii) Gate screened-reject check (the
reason+flip+URL+date+≤25-word-quote requirement has *no* counting command — my twin did zero
screening and is invisible to the set); (iii) PROVINCE.md F25-amendment presence (uncommanded);
(iv) measure `45/45 = 1.000` (asserted, uncommanded); (v) scout no-overlap verification
(uncommanded); (vi) tracked-deletion guard (kill-rule only).

## Bottom line

- C1 print-only: **survives**; counting = grammar; missing limbs named above (content-sensitivity,
  export-witness, payload-binding, selftest-depth).
- C2 O4 (assigned): **caught** by substance-counting commands 4–8; marks commands 1–3, 9 fooled.
- C2 self-consistent fabrication: **survives all nine**; the boundary is provenance, not
  consistency — a wave-2 attack that *re-fetches or disproves* the capture/entry/Gate is the
  only limb that distinguishes real mining from a forged twin.

Tooling: none installed. Scratch `/fast/scratch/hyaku/kasegi-r42/MutPredicates` removed at exit.
No network fetched. Lane bytes untouched: lane `corpus/SOURCES.md` sha256 baf2f44a identical to
the exported HEAD copy (verified post-run).
