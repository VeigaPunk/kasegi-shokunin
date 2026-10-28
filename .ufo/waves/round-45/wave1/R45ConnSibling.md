VERDICT: INFO

# R45ConnSibling — sibling-overlap scan (kasegi round 45, read-only)

Scope: other lanes' round-45/46 wave dirs and claims, fleet-wide kernel security-reporting claims, freeze-check tooling names, and S0xx registry-id collisions with S071/S072. No file was edited, committed or staged. The kasegi lane is the only lane that declares the kernel security-bugs process.

## Findings

### F1 — Kernel security-reporting claims in other lanes: none

Command (round-45/46 dirs of every non-kasegi lane; 22 dirs, `ls -d */.ufo/waves/round-4[56] | grep -v '^kasegi'`):

    grep -rIl -i -E "security-bugs|security@kernel|kernel security|linux kernel.*(security|vulnerab)|freeze-check\.py|r45-c2-gate|r45-routed|kernel\.org/process" $(ls -d */.ufo/waves/round-4[56] | grep -v '^kasegi-shokunin')
    echo "(end non-kasegi kernel-specific: $(... | wc -l) files)"

Printed: `(end non-kasegi kernel-specific: 0 files)`.

Fleet-root wave dirs: `ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-45` → `No such file or directory`; `round-46` likewise. `round-47` holds only `w1/C1Tokens` (empty). `round-50/w2`, `round-56/w3` (`T56W3Led13.md`), `round-62/w2`: the kernel-pattern grep printed nothing.

URL sweep: `grep -rIl -F "docs.kernel.org/process/security-bugs" --include=SOURCES.md .` (fleet root) → empty.

Prose warning from another lane (not a claim): `.ufo/reports/round-45/chousa.md:101` reads "prose ids such as S071 point at other documents in lane numbering; flip in the lesson's Gate". It concerns id tokens, not kernel reporting.

### F2 — Freeze-check tooling: no committed path collision

Fleet search: `find . -path '*/.git' -prune -o -path '*/node_modules' -prune -o \( -iname '*freeze-check*' -o -iname '*freeze_check*' \) -print`. The only `.py` hits are kasegi's in-round sibling drafts (uncommitted):

- `kasegi-shokunin/.ufo/waves/round-45/wave1/R45ExecFreezeA.draft/freeze-check.py`
- `kasegi-shokunin/.ufo/waves/round-45/wave1/R45ExecFreezeB.draft/freeze-check.py`

Other hits are artifact names, not tools: kake `round-43/verification/freeze/registry-count-r43-freeze-check.txt`, tsukuroi `round-42/w1/GateAllRegistry/attribution/freeze-check-*.py.out` (outputs; I did not locate the scripts they came from), tabi `round-40/w1/ScribeLesson/freeze-check.txt`, mado `round-51/w2/SentinelC1Pointers/receipts/freeze-checker.txt`, kotoba `round-74/w1/build/ExecSibRowsDR74/freeze-check.tsv`, tameshi `round-55/w1/T55W1ScribeNote-receipts/freeze-check.txt`, kama `round-53/w1/out/Sc1Freeze/evidence-freeze-checks.txt`, kotodama `round-76/w1/stage/ExecAdaptScripts/receipts/freeze-check.txt`, mori `round-24/evidence/c2-freeze-check-register.json`.

Base tree (the C1 R4 target path must be free): `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-tree -r --name-only dc5bb8c6e31efc4a6650819df85e79b72fd64bcd -- corpus/instruments | grep freeze` → `corpus/instruments/r43-limbs/k19-freeze.sh` only. So `corpus/instruments/freeze-check.py` is unoccupied at base.

Conceptual adjacency, different lane and different names: kaidoku `.ufo/waves/round-31/controls/freeze-integrity-*.txt` and `round-32/a2before/freeze-claims*.json.txt`. No path collision.

### F3 — S071/S072 registry-id tokens: lane-local, no kasegi collision

(a) kasegi committed registry. `git show dc5bb8c6e31efc4a6650819df85e79b72fd64bcd:corpus/SOURCES.md | grep -cE "^\| S07[12] "` → `0`. Last row is S070 (`corpus/SOURCES.md:76`). CORPUS.md:86-ish id rule: "`id` — `S` + 3 or more digits, the next unused; never reused." S071 is the next unused id.

(b) kasegi round-24 staged merge package (dormant). `.ufo/waves/round-24/assimilation/staged-ids:41-42` lists `S071`, `S072`. `.ufo/waves/round-24/wave1/ScoutMergeOther.md:63` maps staged S072 to `chinese-grading-annexes-transcribed-2026-10-23.md` (ADJ, "none — lane artifact"); `:84` maps staged S071 to `cnvd-canonical-advisory-cross-references-2026-10-23.md` (ADJ). `renumber-map.tsv` has no S06x/S07x/S08x row: `awk -F'\t' '$1 ~ /^S0(6|7|8)/' renumber-map.tsv` printed nothing. Adoption is by document: `corpus/SOURCES.md:96-97,127` ("staged S080 → lane S048, mapped by DOCUMENT"; "staged S081/S082 on no lane row"). Risk: none in the registry; the staged numbers must not be reused for the kernel row.

(c) Other lanes' own registries. 16 `*-shokunin/corpus/SOURCES.md` files contain S071 or S072 tokens (`grep -cw -E "S071|S072"`): chousa 3, kaidoku 4, kake 2, kama 6, kengaku 3, kotoba 2, kotodama 5, kumitate 2, lane3 3, mado 4, mori 5, revenger 3, souji 5, tabi 7, tameshi 5, tsukuroi 3. Each token names a different document in its own lane: `kumitate-shokunin/corpus/SOURCES.md:84` (`| S071 | proc_pid_environ(5)`), `:85` (S072 systemd 262); `lane3/corpus/SOURCES.md:93` (S071 Python json), `:94` (S072 WebArena). This matches the namespace trap in `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md:34-36` (S069 footnote): identical token, different document, lane-local namespace.

(d) Shared URL across lanes (the cross-lane question). `bash scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin` (read-only; stdout only) printed 74 lines. `... | grep -i kernel` printed one line: `raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c	shared	tsukuroi,mori` (unrelated source file). `... | grep -c -i -E "security-bugs|S07[12]"` → `0`.

(e) In-flight round-45/46 dirs of other lanes reuse the token for other documents: `grep -rIl -w -E "S071|S072"` across the 22 non-kasegi dirs → 170 files (mostly `reg-ids`/census files). Examples: `tsukuroi-shokunin/.ufo/waves/round-46/w1/D2D3Draft/reg-4456059.md:77-78` (systemd.timer, systemd-run), `mado-shokunin/.ufo/waves/round-46/w1/ExecIdGuard/reg-ids.txt:71-72`, `kengaku-shokunin/.ufo/waves/round-45/claims/census-before.txt:12` (`W04 S071 duplicate url docs.python.org/3/library/json.html`, kengaku's own row). None concerns kernel reporting.

### F4 — Adjacent ground (no claim collision; absorption risk only)

- kake `corpus/knowledge/security-txt-publishing.md:1` cites S078 (RFC 9116) and S079 (securitytxt.org), rows at `kake-shokunin/corpus/SOURCES.md:86-87`. This is web-property disclosure, not the kernel process. F27 must not absorb it.
- kasegi in-lane: `corpus/knowledge/coordinated-disclosure-timelines.md:25` already cites S005 for a "14-day grace extension" from another vendor's policy. F27's 14-day exception needs its own kernel citation (S071); it is not novel ground. Other kasegi disclosure files that grep matched: `vendor-disclosure-policies-as-corpus-objects.md`, `iso-29147-divergence-and-clause-crosswalk.md`, `iso-29147-and-30111-division-of-labour.md`, `japanese-domestic-disclosure-workflow.md`, `vendor-third-party-finding-coordination.md`, `cisa-when-to-issue-vex.md`, `anthropic-cvd-provenance-and-pacing.md`, `nist-sp800-216-vdp-framework.md`, `doj-vdp-framework-scope-and-authorization.md`.
- Discarded false positive: `kotodama-shokunin/corpus/knowledge/synthesis/contact-scenario-builder.md:59` ("Embargo or diaspora dispersal", linguistics).

## Controls and discrimination

- Do-nothing control (base): `git show dc5bb8c…:corpus/SOURCES.md | grep -cE "^\| S07[12] "` → `0`; fleet kernel-URL grep → empty. A clean base is the expected state.
- Grep positive control: the same token grep over `kasegi-shokunin` returns the round-24 `staged-ids` hits (F3b), so the S07x token search does match when the token exists.
- Census positive control: the shared-mode census lists real shared URLs, e.g. `docs.python.org/3/library/json.html	shared	kaidoku,kengaku,kake,kotoba,tameshi,mori,chousa,souji`. An empty kernel-line result therefore means "not shared", not "census blind".

## Limitations

- String and token sweeps, not semantic review. Paraphrased kernel-process text (for example, "Documentation/process" wording) would be missed; the URL sweep and the S07x sweep are the backstops.
- The census `shared` mode is URL-based and does not test id collisions; id checks rest on grep plus the registry rows read above.
- Only grep hits in other lanes' round-45/46 dirs were read, not their prompts or spec bodies.
- Freeze-check tool scripts in other lanes were not located; only artifact names were seen (F2).
- Kasegi's in-round drafts `R45ExecFreezeA/B.draft/freeze-check.py` were listed, not read or changed; they are sibling-seat outputs.
- Snapshot of the working trees at 2026-10-28; sibling lanes are still writing.
- Hygiene: I accidentally redirected census output into `~/.cache/.none` (5,116 bytes) and `/fast/scratch/hyaku/.r45-shared-census.tsv` (74 lines). Both were removed (`rm -f`; the scratch file's absence was confirmed by `ls`). No other writes, no git mutation, no install. Scratch dir `/fast/scratch/hyaku/kasegi-r45/R45ConnSibling` was created empty and removed on exit.
