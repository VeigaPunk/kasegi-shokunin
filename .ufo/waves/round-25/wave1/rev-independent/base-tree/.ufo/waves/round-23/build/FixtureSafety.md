# Fixture safety review — round 23

**Axes:** `depth:verifiability` (C1 mirror-containment detector) and `coverage` (fixture safety / corpus-input boundaries).

**Scope and method:** Static review only of frozen `.ufo/waves/round-23/claims.json` C1, assigned `FixtureSafety` instructions in `build-spec.json`, `corpus/instruments/resolve.py`, `test_resolve.py`, the instrument README/quality rules, and the separate `anchorcheck.py` path gate. No test, resolver, network, credential, or live-target operation was run; no secret/account path was opened. Findings below are source-derived and falsifiable, not runtime observations.

## Findings

### F1 — High, conditional: alternate-resolver setting is an arbitrary file-to-code execution boundary

**Evidence:** `test_resolve.py:39-48` accepts any `KASEGI_RESOLVER_UNDER_TEST` path that `os.path.isfile` accepts (including a symlink target); `:117` copies that file with `shutil.copy2`; `:130-132` executes the copied bytes as Python via `subprocess.run([sys.executable, ...])`. There is no origin/hash allowlist or timeout. `corpus/instruments/README.md:120-122` documents this override for baseline replay.

**Exploit path (not executed):** A caller-controlled test environment sets `KASEGI_RESOLVER_UNDER_TEST` to an arbitrary local file. The harness copies and runs it with the caller's OS privileges; a Python payload can read account/credential material, produce external effects, or hang the test. A non-Python secret file is still copied and interpreted; syntax errors can also surface source excerpts in captured stderr and assertion output.

**Impact:** The normal suite's local fixture isolation does not constrain the alternate-resolver input. Thus the test harness cannot guarantee the required “never read secret/account material or live security targets” invariant when run with an untrusted override.

**Smallest remediation:** Accept only a resolver from a narrowly defined trusted fixture/source location and verify an expected digest before copying/executing; reject symlinks and all unpinned paths. Add a subprocess timeout as a separate hang guard, not as a substitute for the trust check.

**Falsifier:** With an unapproved path or symlink set in `KASEGI_RESOLVER_UNDER_TEST`, the harness must reject before copying or starting Python; approved pinned baseline/fixed resolver inputs must still work.

### F2 — High: corpus ingestion follows Markdown symlinks outside the selected lane root

**Evidence:** `resolve.py:250-266` walks `<lane_root>/corpus`, includes every filename ending `.md`, checks `os.path.isfile(candidate)` (follows symlinks), then opens it directly. The root `SKILL.md` is likewise opened with no regular-file/symlink or resolved-root check (`:253`, `:263-267`). The documented corpus scope is `SKILL.md + corpus/**/*.md` (`corpus/instruments/README.md:11`); nothing states that symlink targets are in scope.

**Exploit path (not executed):** A local checkout contains `corpus/knowledge/leak.md` as a symlink to a private Markdown/text file outside the checkout, or `SKILL.md` itself is a symlink. Running the census reads the target line-by-line. `os.walk`'s default refusal to recurse into directory symlinks does not protect symlinked files in `filenames`.

**Impact:** A contributor-controlled corpus tree can make a lane-local census read account/private material outside the corpus. It also lets out-of-root content affect the generated census and any downstream gate.

**Smallest remediation:** Reject symlinked `SKILL.md`, `corpus`, and Markdown candidates; before opening, require the candidate's resolved path to remain beneath the resolved selected lane root. Keep this check on every file actually opened.

**Falsifier:** A corpus Markdown symlink to an outside file must be rejected without opening it; ordinary in-root files must remain countable.

### F3 — Medium: visible regression suite lacks cases for the C1 fallback branches it is meant to evidence

**Evidence:** Frozen claim C1 names bounty-prefixed and relative mirror fallback escapes, and the known pre-fix bounty escape `~/Projects/bounties/../outside.md`. Current `test_resolve.py:249-253` has only a *confined* bounty-positive control. Its `:255-279` traversal/symlink cases use `CAND1_TILDE`, the explicit canonical-mirror branch, which is confined at `resolve.py:214-222`; they do not exercise the bounty fallback at `:204-213` or relative fallback at `:226-234`. The ordinary relative controls at test lines `221-235` cover an in-lane file, a confined mirror file, and a miss, not an escaped mirror fallback.

**Concrete falsifiable counterexample (derived, not run):** In the same fake-home fixture layout, create `<mirror-parent>/outside-vault/secret.mjs` outside `<mirror-root>`. An absent canonical source plus citation `~/Projects/bounties/../outside-vault/secret.mjs:1` reaches `exists_any(join(mirror_root, rel))`; the current branch returns `MIRROR-EQUIVALENT` on a hit without `under_mirror`. For the relative fallback, place the outside file beside the mirror but ensure `join(lane_root, '../outside-vault/secret.mjs')` is absent; citation `../outside-vault/secret.mjs:1` similarly hits the unchecked mirror fallback. Both should be `GONE` under C1, while a real in-lane `../` hit must remain `INTERNAL` (the frozen claim explicitly preserves lane-relative semantics).

**Impact:** The visible legacy regression cannot independently establish the frozen soundness claim. Canonical-mirror escape coverage does not exercise the bounty/relative branches where the old gap lies.

**Smallest remediation:** The separate round-23 copied-CLI matrix must pin and execute these exact fallback cases, with outside targets physically present in a disposable fixture, alongside confined, missing, prefix-sibling, direct-bounty, and in-lane `../` controls. `build-spec.json`'s `CountMirror` assignment requires eight escape cases, four controls, and a prefix-boundary case; I did not find `mirror-containment-check.py` in the inspected instrument directory, so this report does not assess that planned tool.

### F4 — Medium: test scratch is inside the production corpus and can contaminate a later census after interruption

**Evidence:** `test_resolve.py:67` creates each disposable fixture with `tempfile.mkdtemp(..., dir=HERE)`, where `HERE` is `corpus/instruments`; `:76-77` removes it only through unittest teardown. The fixture writes nested `lane/SKILL.md` and work outputs (`:113-117`, `:130-141`). `resolve.py:255-260` recursively ingests Markdown under `corpus` and excludes only the exact root-relative `corpus/instruments/citation-survival.md`, not nested fixture reports. The wave instructions require read-only seats to avoid production writes and designate scratch as `/tmp`.

**Exploit/failure path (not executed):** An interrupted/killed test leaves `.test-resolve-*` under `corpus/instruments`; a later census can ingest its synthetic `lane/SKILL.md` and nested generated `citation-survival.md`, changing counts and citing fixture-only paths. Even a clean run transiently writes into the source tree, contrary to the read-only wave contract.

**Impact:** Reproducible corpus measurements can be contaminated by abandoned synthetic artifacts, and fixture execution is not source-tree read-only.

**Smallest remediation:** Put fixtures under the system temporary directory (or an explicitly supplied scratch root outside the repository); continue running the copied resolver there. Independently, keep the corpus collector from ingesting generated/fixture trees rather than relying only on teardown.

**Falsifier:** After an interrupted fixture run, a corpus census must not include any fixture `SKILL.md` or generated report, and a normal fixture run must leave the repository tree unchanged.

## Separate gate boundary note

`anchorcheck.py` is not the frozen C1 detector, so its behavior is not counted as a C1 result. Its explicit ORIGIN/MIRROR branches do realpath confinement (`:165-195`), but lane-relative/bare candidates are only checked with `exists` (`:202-218`) and then opened/read and excerpts printed (`:222-227`) without an equivalent resolved-path containment check. A symlink or `../` citation can therefore make that separate gate read and print lines from outside the lane. Apply the same resolved-root invariant before those opens, or document and enforce a deliberately different allowlist; do not treat explicit-root confinement as proof that all anchorcheck reads are lane-confined.

## Scope limits

The visible normal test inputs create their synthetic files under the fixture, set a fake `HOME` and `KASEGI_MIRROR`, pass a minimal child environment (`PATH`, `LANG`, `LC_ALL`, plus fixture values), invoke Python with an argv list rather than a shell, and contain no network client or target operation (`test_resolve.py:66-77, 106-135, 255-279`). The fixtures' `secret.mjs` / `outside-vault` names are synthetic decoys. This is not a proof against the unpinned resolver override or symlinked corpus inputs, and no live/credential access was tested or attempted.