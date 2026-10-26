# CritBoundary — province-boundary review of F16 (round 33, wave 1)

Seat: `CritBoundary` (critic, leaf — no delegation, no background workers, no swarm).
Answering model: `opencode-go/deepseek-v4.1-flash` (config route table; no model passed by hand —
bound 10). Tools installed/upgraded: none; no pacman transaction; no network fetch; no live bounty
target contacted; no git/jj mutation (read-only `git show`/`git diff` only).

Write scope exercised: this receipt only. Everything read was read-only (lane files, six sibling
lanes, `shokuknow/merge/kasegi/`, `shokuknow/.ufo/waves/corpus-expansion-1/`).

## Verdict

**F16 sits inside kasegi's province; it is not contested. No adjacent-lane evidence was absorbed
instead of reported. The PROVINCE append is additions-only (2 added lines, 0 deleted, first 72
lines byte-identical). The entry refuses out-of-scope targets and is documentation-only, with no
credential material reproduced.** One routed wording defect in the entry (called out below, §8);
it does not change any of the four verdicts.

## 1. Province text read (line-numbered)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -n '' PROVINCE.md | sed -n '1,12p;40,52p'
1:# kasegi-shokunin — Province
3:**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages
...
40:corpus objects; 10/10 admitted).
41:F11 — ISO/IEC 29147/30111 division-of-labour (JPCERT/CC 2026 guideline) — admitted round 26
43:## Adjacent
45:Sibling lanes are reported, not absorbed:
47:- chousa — research method and source hierarchy
48:- kagi — secrets and vault handling
49:- kake — web properties
50:- kengaku — LLM evaluation and benchmarks
52:Live-target testing is refused; this corpus is documentation only.
```

Core (PROVINCE.md:7-13) is "program rules, scopes, and claim packages" plus "triage and claim
gates, and submission/disclosure packaging". F16's object — CNVD 众测 platform intake/scope rules
and 360SRC's handling + reward standard — is exactly program rules/scope/reward of security
platforms, the same lineage as the already-admitted F13 (severity ladders and reward scales) and
F15 (vendor research programme). The province's domain sentence is not geographically bounded, and
the round-15/round-19 annotations say the domain is unchanged; a Chinese platform document is not
off-domain on the file's own text.

## 2. Adjacent evidence — scanned by ConnSibling, re-run by me

ConnSibling (`.ufo/waves/round-33/wave1/ConnSibling.md` §1-§2) reports zero F16-scoped hits across
chousa / kengaku / kake / kagi / kumitate / kotoba. Re-ran the count command myself on the six
lanes' `corpus/README.md` + `corpus/knowledge/`:

```
$ for d in chousa-shokunin kengaku-shokunin kake-shokunin kagi-shokunin kumitate-shokunin kotoba-shokunin; do
    n=$(grep -rinE 'CNVD|360SRC|众测|zc\.cnvd\.org\.cn|security\.360\.cn|crowdsourced' \
        "$d/corpus/README.md" "$d/corpus/knowledge/" 2>/dev/null | wc -l); echo "$d: scoped-terms=$n"; done
chousa-shokunin: scoped-terms=0
kengaku-shokunin: scoped-terms=0
kake-shokunin: scoped-terms=0
kagi-shokunin: scoped-terms=0
kumitate-shokunin: scoped-terms=0
kotoba-shokunin: scoped-terms=0
```

Two siblings disclaim the ground outright (re-opened, not taken from the receipt):

```
$ sed -n '15,25p' chousa-shokunin/corpus/knowledge/scope-refusal-r12.md
| `bug bounty`, `bounty program(s)`, `bounty hunt(ing)`, `bounty scope`, `claim package(s)`, `kasegi` | `SCOPE_BOUNTY_ABSORBED` | kasegi |
$ sed -n '464,465p' kake-shokunin/corpus/README.md
Vulnerability handling itself (report intake, triage, remediation, disclosure timing, bounty and policy
operation) stays outside this province
```

So the direction of travel is the opposite of absorption: chousa and kake route this ground to
kasegi. The lane therefore has nothing adjacent to absorb, and no cross-domain item needed
reporting back to the orchestrator.

## 3. No adjacent or campaign evidence inside the entry

The entry cites only lane rows S049/S050 and same-lane entries F13/F15:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && E=corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
$ grep -cE 'chousa|kengaku|kumitate|kotoba|kake|kagi|shokuknow|merge/kasegi' "$E"
0
$ grep -cE 'staged|shokuknow|merge/kasegi' "$E"
0
$ grep -cE 'roles-and-conduct|national-standard' "$E"
0
```

The only `source:` lines are S049 (`https://zc.cnvd.org.cn/news/helpList`) and S050
(`https://security.360.cn/Reward/rules`); both rows are registered exactly once in the lane
registry (`corpus/SOURCES.md:55`, `:56`). The `merge/kasegi/` staged rows that supply these two
documents keep their own id namespace (staged S034 = CNVD helpList, staged S035 = 360SRC rules;
staged/registered id collisions 18, `S031-S048`) — the entry uses the lane ids, not the staged
ones, and the id-collision guard proof is committed at
`.ufo/waves/round-33/assimilation/guard-proof.txt` (`reg_ids=48`, `staged_ids=94`,
`collisions=18`). That is adoption of the lane's own merge-package rows by document, not sibling
absorption.

## 4. PROVINCE append — additions-only (R6)

```
$ git diff --numstat 690b69da -- PROVINCE.md
2	0	PROVINCE.md
$ git show 690b69da:PROVINCE.md | cmp - <(head -n 72 PROVINCE.md) && echo first72_identical=yes
first72_identical=yes
$ wc -l PROVINCE.md ; sha256sum PROVINCE.md
74 PROVINCE.md
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md
$ tail -1 PROVINCE.md
[r33 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F16 — Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) — admitted round 33
$ grep -c 'F16' PROVINCE.md
1
```

Base `PROVINCE.md` (690b69da) sha256 `b42e5fbb…60a76`; the worktree's first 72 lines compare
identical to it byte for byte, so every pre-existing line keeps its number (R6) and no existing
paragraph was rewritten (R9). The append adds one blank line plus one factual line at end of file —
no edit to the Domain sentence (:3), the Core paragraph (:7-13), the Frontier paragraph, the
Adjacent list (:43-50), or the refusal line (:52, "Live-target testing is refused; this corpus is
documentation only."). No re-scope is asserted; the line records an admission only.

## 5. Entry refuses out-of-scope targets; documentation-only (Q6)

```
$ sed -n '303,305p' "$E"
- Documentation only: this entry records two platforms' published rules. It instructs no
  probing, scanning, login or submission against any target, quotes no credential material, and
  carries no session or private URL beyond the two public document URLs in its `source:` lines.
$ sed -n '191,194p' "$E"
Credential material: the CNVD 众测 page contains platform-issued VPN account/password retrieval
steps (S049.txt:202-205) and an OpenVPN client walkthrough for projects under third-party audit
(S049.txt:398-406). That material is **not reproduced** here — no account, password, profile or
certificate value appears in this entry, and none of those lines is quoted (Q6).
```

The entry also refuses the "platform registration = authorization" reading (Rejected
over-generalizations 1 and 6, `$E:210-234`), and states that both documents are neither
authorization nor a liability carve-out (Honest limit, `$E:170-190`). It gives no instruction
toward any target.

Credential audit run against the capture, printing only match counts and line numbers (no
credential text emitted): S049.txt has 34 lines matching `密码|口令|password|passwd|账号|帐户|VPN|
OpenVPN|证书|profile`. Sliding-window comparison between the entry and those lines produced two
matches, both URL fragments only:

```
credential-pattern lines: 34 matches: 2
matched windows: ["'ps://zc.cn'", "'http://www'"]
```

No account, password, profile, certificate or session value appears; `grep -nE 'op://|vault'` on
the entry → no output. The two `source:` URLs and the two public page URLs discussed in the text
(`cnvd.org.cn`, `security.360.cn/Product/product`) are the only URLs.

## 6. Counterexample tested — false provenance found, then fixed by the owner

At the 01:20 state the entry carried two provenance claims that failed on the landed bytes:
(1) it pinned the round-32 manifest as `635cfad4…`, while the file and `ExecManifest32.md` §1 both
give `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774` (5753 B; also unequal to
compact/indent-1/indent-2 serializations, so not a formatting artifact); (2) its `recheck:` comment
said "12 assertions (6 per capture)" while the manifest carries 14 (S049 Q1-Q8 + S050 Q1-Q6). I
messaged `ExecEntryF16` with both; the owner had already corrected them on measured bytes and
replied with the same digests. Current landed state:

```
$ grep -n '6e4e719a\|635cfad' "$E"
270:  `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774`).
$ grep -n '14 assertions' "$E" | cut -c1-120
7:recheck: ... # 14 assertions on the round-32 manifest (S049 Q1-Q8, S050 Q1-Q6) ...
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json >/dev/null 2>&1; echo "source_recheck_exit=$?"
source_recheck_exit=0
```

The entry's self-referential vocabulary check was also re-cut to a scoped command and re-measured;
it now returns the stated count:

```
$ awk '/^## Attribution/{f=1} /^## What this adds/{f=0} f' "$E" | grep -c -E 'CVSS|0.85|时效评价|利用代码'
1
```

## 7. Quiescence / PRE-STATE disclosure (M30-3, bound 6)

The entry was revised three times while this review ran; each hash below is a distinct state and
only the last is the reviewed state:

```
159356b9c264…  (01:21, after my first read)
eebd5ea572b3…  (01:25)
53c48b3b322a…  (01:28:10 -03:00, 24492 B)  ← verdict measured here
PROVINCE.md b57de5d9… (01:27:02 -03:00, 74 lines)
```

If either file moves again, re-run §4's three commands and §6's `source-recheck` exit before
citing this review.

## 8. Routed observation (not a province defect)

`$E:276` calls `chinese-program-severity-instrument.md` "the refused package entry". No lane
lesson records a refusal of that file:

```
$ grep -rc 'chinese-program-severity-instrument' corpus/lessons/ | grep -v ':0' || echo "no lesson names it"
no lesson names it
```

Its overlap substance does hold — the staged package entry holds the same reward multiplication in
prose ("multiplies it by validity, test difficulty, impact, target-enterprise size and report
quality", `shokuknow/merge/kasegi/knowledge/corpus/knowledge/chinese-program-severity-instrument.md:37-39`)
— but the *label* "refused" is unsupported by a lane gate record. Smallest safe correction, for
the entry owner (`ExecEntryF16`): call it "the staged package entry" (or cite the lesson that
refused it). This is a wording/provenance defect inside the C2 restatement argument; `CritExpansion`
holds that argument and has already recorded the same missing-gate fact
(`wave1/CritExpansion.md:126`), so I do not duplicate it as a boundary finding.

## 9. Axes impacted

- `coverage` — F16 is admitted on ground the coverage map did not hold, and the province file does
  not contest it; chousa and kake route this ground *to* kasegi, so there is no cross-lane
  duplicate authority. No coverage collateral: the append does not redefine the domain.
- `depth:verifiability` — the append is proven additions-only by byte comparison, the entry's
  out-of-scope/documentation-only refusal is shown at named lines, and the entry's two stale
  provenance claims were caught and corrected on landed bytes; the residual defect (§8) is a
  one-word label, not a false number.

## 10. Scratch and tooling

No clone, mirror, work tree or fixture was created for this review (read-only greps and read-only
git only). Two temporary files made while proving the append were removed and verified absent
(`/fast/scratch/hyaku/tmp-base-province`, `$HOME/.cache/head72.txt`); the final proof uses
`git show … | cmp - <(head -n 72 PROVINCE.md)` and writes nothing. `ls -d
/fast/scratch/hyaku/kasegi-r33/CritBoundary` → does not exist. No tools installed.
