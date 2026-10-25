# Citation bases — round-16 vocabulary, completed in round 18

This is the one vocabulary for `path:line` bases used by `SKILL.md` and
`corpus/**/*.md`. A file header names only the bases that file uses and points
here; it does not repeat these definitions. Round 16 was operator-terminated
with this normalization in flight; round 18 verified and landed it. Evidence:
the round-18 entry in `LOG.md` and `corpus/instruments/README.md`.

## Base names

**LANE** means this repository: `SKILL.md`, `corpus/...`, and other files under
the lane root. Use the full internal path for knowledge cross-references, for
example `corpus/knowledge/ops-invariants.md:18`; do not use a bare
`ops-invariants.md:18` or `claim-gates.md:3` when the target is in the lane —
the resolver only tries the lane root for relative paths, so a bare cite of a
file in a subdirectory classifies GONE (`corpus/instruments/resolve.py:164-172`).
The resolver classifies existing lane-relative paths as INTERNAL
(`corpus/instruments/resolve.py:31-48`).

**MIRROR** means the frozen code mirror `~/Projects/the-bounty-hunter` at git
HEAD `1cfbd86` (2026-09-05 genesis snapshot, CODE half only) — **ABSENT since
2026-10-12** (`corpus/knowledge/root-loss-2026-10-12.md`); its files are no
longer live-checkable on this host. While it stood, a matching path was only
name-surviving/anchor-compatible, never proof that lost bytes were identical
(`corpus/instruments/README.md:31-38`; per-file provenance verdicts:
`corpus/knowledge/source-tree-loss-2026-09-28.md` §4.1). Mirror-relative
`ops/...`, `fleets/...`, `docs/...`, `bounty-map/...` tokens classify
MIRROR-EQUIVALENT under the resolver's relative-path fallback
(`corpus/instruments/resolve.py:164-172`). When a mirror anchor could be
confused with a lost-tree anchor, write the explicit root
(`~/Projects/the-bounty-hunter/ops/rank.mjs:55-58`, which classified RESOLVES while the mirror stood — now `[lost-base]` and BASE-ABSENT)
or label the base in the sentence.

**ORIGIN-WORK** means the data root
`~/Projects/origin-work/open-bug-bounties` (live repo while it stood, HEAD `1307b8b`,
2026-09-14 — **the entire `origin-work` tree is ABSENT since 2026-10-12**,
`corpus/knowledge/root-loss-2026-10-12.md`), including its claim packages,
`.ufo-missions`, and `data/` inventories. Use the full root, for example
`~/Projects/origin-work/open-bug-bounties/claim-packages/`; that form
classified RESOLVES under the resolver's other-root rule while the root stood
(`corpus/instruments/resolve.py:161-163`) — now GONE; use `[lost-base] `.
This root MUTATED during rounds:
its `.ufo-missions` subtree lost 681 files at 2026-09-28T22:45:06-03:00
(recorded in `corpus/knowledge/open-bug-bounties-census.md` §loss-event).
Every count taken from it carries an as-of timestamp.

**LOST-TREE** means the deleted `~/Projects/bounties` root, read last at
2026-09-28T23:32Z and removed at 2026-09-28T23:51:31Z
(`corpus/knowledge/source-tree-loss-2026-09-28.md`). Its historical source
anchors are never presented as openable: prefix the token with `[lost-tree] `
INSIDE the backticks, then retain the original relative path and line, for
example `[lost-tree] ops/claim-check.mjs:174-199`. The prefix intentionally
classifies GONE with noise flag `synthetic`, so it cannot inflate the
resolving numerator, and `corpus/instruments/anchorcheck.py` reports it as
LOST-RECORDED instead of PAST-EOF. Facts from the lost DATA half carry the
exact stamp `[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]`
(`corpus/knowledge/source-tree-loss-2026-09-28.md` §5).

**LOST-BASE** means any cited base tree that went absent after the
`~/Projects/bounties` loss — currently the MIRROR and ORIGIN-WORK trees above
(removed on/around 2026-10-12; evidence `corpus/knowledge/root-loss-2026-10-12.md`).
Its historical anchors carry the parallel prefix `[lost-base] ` INSIDE the
backticks, same semantics as `[lost-tree]` (recorded, deliberately
non-openable, `LOST-RECORDED` under `anchorcheck.py`, GONE+synthetic under
`resolve.py`, never counts as verified). `ufo-fsd-alpha` is NOT a lost base —
it relocated intact to `~/Projects/ufo-fsd-alpha`, and citations to it are
re-anchored, not prefixed.

**BLOB-PIN** means a git object used when a lane file's line numbers move.
`SKILL.md:NNN` spans in `corpus/knowledge/triage-thresholds.md` are pinned to
the round-12 blob `fc6d398` (546-line `SKILL.md`); commands resolve a pin with
the shell command git -C /home/vgpnk/projects/shokunin/kasegi-shokunin show [r22 correction: lowercase lane path absent on 2026-10-19; test -e failed 2026-10-19; historical]
fc6d398:SKILL.md (pipe to sed -n 'NNNp' for one line). Machine-readable pin
declaration for `anchorcheck.py` (plain HTML comment, never backticked):
`pin: SKILL.md fc6d398` inside an HTML comment tag. Other measured lane
snapshots: `7483333` (round-13, 590-line `SKILL.md`), `eb5b590` (round-15,
997-line `SKILL.md`). NEVER put a bare blob reference (`fc6d398:SKILL.md`) or
an at-blob path form in backticks — the measured resolver classifies both
GONE; blob references live inside shell-command spans (not extracted) or in
plain prose.

## Rules that prevent silent base changes

1. Bare mirror-relative `ops/...`, `fleets/...`, `docs/...`, or
   `bounty-map/...` tokens in a knowledge file are historical lost-tree source
   anchors unless the file header or the sentence labels them MIRROR; a
   same-named mirror file is name survival, not proof of live content. Where a
   lost-tree line number diverges from the mirror (fleet-dispatch, shared,
   claim-check — divergence table in
   `corpus/knowledge/source-tree-loss-2026-09-28.md` §4.1), the file header
   says so, and anchors past the mirror EOF carry the `[lost-tree] ` prefix.
2. A line number on a file this lane keeps editing is not stable: use the
   BLOB-PIN command or re-verify the current INTERNAL anchor and quote the
   line. Round-16 rewrites were re-derived for every lane anchor they changed
   (65 of 132 bare lane cites had drifted; corrections were content-verified,
   not uniform offsets); round 18 records the resumed work in `LOG.md`.
3. `~/Projects/bounties/...` is never silently rewritten to the mirror. Mark
   it LOST-TREE unless the citation explicitly says the mirror is an
   equivalent path; MIRROR-EQUIVALENT is a resolver class meaning name
   survival, not content identity (`corpus/instruments/README.md:31-38`).
4. Keep historical `[lost-tree]` citations and DATA as-of stamps when they are
   evidence of what the lost system contained; replace only repeated
   explanations with a pointer to this vocabulary.
5. One cite per anchor: comma-anchor lists (`file.md:83,104,118`) defeat the
   resolver's line-anchor rule (`corpus/instruments/resolve.py:74`) and
   classify GONE; split them into separate backticked cites.
6. Legacy form (pre-r16): `corpus/lessons/*.md` files written before round 16
   may contain bare `file.md:NN` cites of lane-corpus files. Their base is the
   lane corpus directory holding the file (search `.`, `corpus/knowledge`,
   `corpus/lessons`, `corpus/instruments`). Round 16 deliberately did NOT
   rewrite them: a lesson's anchors are historical claims verified as-of that
   lesson's round, and rewriting them (prefix or renumber) would either
   falsify the record or require per-round archaeology. The census counts them
   GONE; that is the honest cost of preserving append-only audit trails. This
   rule is their written base declaration, so a reader can resolve them
   without oral context. Round-16 rewrites were confined to live documents
   (SKILL.md, `corpus/README.md`, `corpus/instruments/README.md`,
   `corpus/knowledge/*.md`), where every renumbered anchor was
   content-verified against the current target line (mapping of record: the
   round-18 `LOG.md` entry + regenerated citation census).

## Provenance (round-22 correction, appended)

source: Lane rounds 18–19 — LOG.md:705-716 and 790-793; base vocabulary in sections Base names and Rules that prevent silent base changes.
verified-at: 2026-10-14
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true
