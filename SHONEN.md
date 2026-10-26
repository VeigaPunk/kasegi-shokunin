# kasegi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 31, HEAD `eecad59`; `SKILL.md` sha256
      `817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7`, clean in
      `git status --porcelain -- SKILL.md`): `density.py SKILL.md` prints mean dens 191.5 over
      24 blocks and 689 path-citation instances, `density_exit=0`; `anchorcheck.py SKILL.md` prints
      `7 in-range cite instances, 0 bad`, `anchor_exit=0` — compared against an r30 replay (mean 171.1,
      23 blocks, 662 cites, `0 bad`) in `.ufo/waves/round-31/wave2/ExecNoHarmDensity.md` §1b/§2b. The
      mean move comes only from the round-31 appended block 24, whose resolvable share is 11/27 =
      40.74%, so the receipt claims no quality gain for it (§1d).

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 31): `LOG.md:1469` carries the round-30 entry, appended in round 31 by seat
      `ScribeLogR30` (`.ufo/waves/round-31/wave1/ScribeLogR30.md`), and round-31's own end-to-end
      commands land with receipts: the C1 counter prints `limbs=13 killed=13 survivors=0` and
      `controls=3 rejected=3`, exit 0 (`.ufo/waves/round-31/wave2/ExecRegressionC1.md` §2), and C2's
      census exits 0 with the harness at `entries=18 pass=18 exit=0`
      (`.ufo/waves/round-31/wave2/ExecCensusFinal.md`). No round-31 `LOG.md` entry exists yet at HEAD
      `eecad59`; the box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 31, HEAD `eecad59` plus the wave-2 counter fix, `limb-mutation-check.py` sha256
      `237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4`): every one of the 44
      `corpus/knowledge/*.md` entries carries one `recheck:` command;
      `recheck-audit.py --quiet` prints `strict pass=44/44` and
      `expect=present expected=44 missing=0 unexpected=0`, exit 0 from the lane root and from `/` with `--root`
      (`.ufo/waves/round-31/wave2/ExecRegressionC1.md` §3); `frontier-recheck-count.py` prints
      `PASS F15 knowledge/vendor-third-party-finding-coordination.md ids=S048` and
      `entries=18 pass=18 exit=0` (§4 and `.ufo/waves/round-31/wave2/ExecCensusFinal.md`); and
      `source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048`
      exits 0 with 8 assertion `OK` lines (ExecCensusFinal.md §3).

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 31): `PROVINCE.md` gained only an end-of-file amendment (`git diff --numstat
      b374febb -- PROVINCE.md` = `20	0`), naming F12–F15 and keeping the older F01–F10 paragraph as
      history; the sibling sweep in `.ufo/waves/round-31/wave1/ConnSibling.md` §1.5/§2.2 found zero
      MSVR and zero "vendor research" hits across the six sibling corpora, placed F15 inside this
      province, and recorded `kake-shokunin/corpus/README.md:457-460` as an explicit refusal of
      vulnerability intake; adjacency reported, nothing absorbed.
