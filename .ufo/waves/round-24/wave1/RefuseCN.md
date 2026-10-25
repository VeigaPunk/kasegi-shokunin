# RefuseCN — critic, round 24 wave 1

**Seat:** L1Kasegi24.RefuseCN (critic, read-only). **Axes named:** `depth:verifiability`, `coverage`.
**Judged bytes:** `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/chinese-criminal-thresholds-and-authorisation.md`
(frozen claims: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json`, `candidate_refuse`[0]).
**Lane base:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, registry ceiling S031, 33 `corpus/knowledge` entries, Frontier F01–F08.
**No installs performed.** Used the host's existing `/usr/bin/pdftotext` (poppler, already installed); no package manager calls.

# Verdict: REFUSE

The file is refused on **Q2 + Q4 with a falsifier inside its own cited source**, secondarily Q1, Q3, Q5, Q7.
The numeric core is *not* the problem: I re-opened S044 today and articles 第一条–第四条 and 第十一条 read as the entry summarizes them
(items 1–4 of 第一条, the five-fold 特别严重 rule, the 第十一条 definitions of 计算机信息系统 / 身份认证信息 / 经济损失).
What fails is the entry's **conclusion** and its **provenance**.

## Findings

### R1 — PRIMARY. The entry's central practical rule is falsified by the statute it cites. (Q2, Q4; axis `coverage`)

Entry, line 49–51: *"the Chinese criminal risk attaches to **scale and effect**, not to the mere act of unauthorised
access. A researcher who stays inside an authorisation and does not accumulate authentication data, control twenty
systems or earn five thousand yuan is nowhere near the 情节严重 line"*.

The same entry (line 27–30) and S045 itself say 285(1) has **no** 情节严重 element. Re-opened 2026-10-25:

```
$ curl -sS -o /tmp/s045.pdf -w 'http=%{http_code} bytes=%{size_download}\n' 'https://czt.ln.gov.cn/czt/attachDir/2026/05/2026050715041524122.pdf'
http=200 bytes=589780
$ file /tmp/s045.pdf   ->  PDF document, version 1.7, 88 page(s)
$ pdftotext /tmp/s045.pdf /tmp/s045.txt && sed -n '2121,2124p' /tmp/s045.txt
第二百八十五条 【非法侵入计算机信息系统罪】违反国家规定，侵入国家事
务、国防建设、尖端科学技术领域的计算机信息系统的，处三年以下有期徒刑或者
拘役。
```

For 国家事务 / 国防建设 / 尖端科学技术 systems the offence is complete on the act. The entry's own
"purely quantitative ⇒ scale not act" inference therefore does not survive its own quote: the criminal risk attaches
to *which system* first and to scale second. This is the A6/Q4 class (an empty observation overclaimed) and it is
load-bearing — the entire "Why it matters" and the closing "corollary" rest on it.

Evidence path: `/tmp/s045.txt:2121-2124` (re-derived this round; not committed in the lane, see R3).

### R2 — "purely quantitative" is falsified by 第一条(五), the item the entry's own recheck drops. (Q3, Q4)

Entry line 33: *"it is purely quantitative"*. Re-opened S044 2026-10-25 (`http=200 bytes=27296`), 第一条 reads
`（一）…十组以上；（二）…五百组以上；（三）…二十台以上；（四）违法所得五千元以上或者造成经济损失一万元以上的；（五）其他情节严重的情形。`
Item (五) is an open qualitative catch-all; 第二条(三) and 第三条(六) carry the same shape. The entry's
`recheck:` text names "**five** 情节严重 thresholds (expect 身份认证信息十组以上, 五百组以上, 二十台以上, 五千元以上)" —
four tokens for five items, and the missing fifth is exactly the one that refutes the thesis. Numbers for (一)–(四)
are correct; the *characterisation* of the list is not.

Evidence: `/tmp/s044.html` (extracted 第一条–第四条 to `/tmp`), and the entry's own `recheck:` at line 8.

### R3 — The `source:` rows do not exist in this lane, and the renumber map the claims name is absent. (Q1; `depth:verifiability`)

```
$ grep -cE '^\| *S0[0-9][0-9] ' corpus/SOURCES.md          -> 31
$ grep -oE '^\| *S0[0-9][0-9] ' corpus/SOURCES.md | sort -u | tail -1 -> | S031
$ grep -nE '^\| *S04[4-6] ' corpus/SOURCES.md              -> rc=1 (no output)
$ grep -rn 'S034' corpus/ SKILL.md                          -> no output
$ find . -name 'renumber-map*' -o -name '*renumber*'        -> no output
```

`claims.json` names the collision map as `.ufo/waves/round-24/assimilation/renumber-map.tsv`; that directory contains
only `census-before.txt`, `collisions` (`S031`), `reg-ids`, `staged-ids`. **No renumber map exists**, and the collision
is real and offsetting: the package's `S031` is *HackerOne standard program policy* while the lane's `S031` is *CNA
Operational Rules 4.2.6* (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:7` vs
`corpus/SOURCES.md:37`). A naive append shifts every package id, so S044/S045/S046 cannot be resolved to lane rows
mechanically. Q1 requires the header to name a *row*; an unresolvable id is not a row, and Q2's "opened in the admitting
round" cannot be attributed per-row without the map.

### R4 — The `recheck:` cannot fail closed; an absent base passes. (Q1, Q7)

Entry line 8, verbatim: ``recheck: 730d — `curl -sSL https://www.court.gov.cn/fabu/xiangqing/3085.html` then confirm 第一条 still lists the five … (ran 2026-10-23)``

Demonstrated on the entry's own host and command shape:

```
$ curl -sSL --max-time 20 'https://www.court.gov.cn/fabu/xiangqing/000000-does-not-exist.html' >/tmp/nope.html
exit=0 bytes=3144          # soft-404 page, success exit
$ curl -sSfL --max-time 20 '<same url>' >/dev/null 2>&1 ; echo $?
22                          # -f is what fails closed; the entry's command omits it
```

Q7: the field is a command **plus prose** ("then confirm …") and carries no missing/corrupted-source control that must
fail. Q1: "failing closed when the base is absent" is not satisfied — a removed article or a rewritten page exits 0.

### R5 — No rejected over-generalization is recorded. (Q5)

```
$ grep -nE '^#+ *Rejected|Rejected:' <entry>   -> rc=1
$ grep -c 'Rejected' authorised-testing-rules-of-engagement.md -> 3
```
Q5 requires at least one rejected over-generalization with its reason. The entry has none, and R1/R2 show two
over-generalizations that needed rejecting.

### R6 — The Japan comparison is the entry's frame and carries no row at all. (Q2, Q3, Q4)

Line 31–32 / 44–45: *"Japanese law has both; Chinese criminal law has neither in its articles"*; *"the opposite of
Japan's on every axis that matters to a researcher"*. All three headers are PRC instruments (S044 court.gov.cn,
S045 czt.ln.gov.cn, S046 nj.jsjc.gov.cn); no Japanese statute is cited, and the lane holds no Japanese row
(`grep -rlnE '刑法|情节严重|285|未经授权' corpus/knowledge/ SKILL.md` → 0 files; JP rows S039–S041 exist only in the
package). Q2 has no tier-A/B row for the comparative claim's scope; Q4 requires each party's position to be stated as
that party's position, and here one side has no source.

**Compounding authority conflict:** the sibling admit candidate `statutory-authorization-in-three-traditions.md` states
*"The **Chinese** half … is not covered: the official text of 刑法 第285条 … could not be opened in this round (see
`CANNOT-ANSWER.md`), and no substitute was admitted."* (`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/statutory-authorization-in-three-traditions.md`, "The honest limit"). It cites a `CANNOT-ANSWER.md` that
does not exist in the package (`$ find . -iname 'CANNOT*'` → no output). Two entries proposed for the same round assert
opposite availability states for the same document. Admitting both creates two authorities and one false provenance
register; that hazard belongs to C2, not to this file alone.

### R7 — `ground: F12` names a Frontier item that does not exist, and the body cites a row that does not carry the claim. (Q1/Q4)

```
$ grep -rn 'F12\|F09' . --include=*.md --include=*.py --include=*.json   (excluding .ufo/waves) -> no output
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / {print NR": "$2}' corpus/README.md       -> 198: F01 … 205: F08
$ grep -rn '互联网漏洞' /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/
  -> chinese-criminal-thresholds-and-authorisation.md:50   (the only occurrence in the package)
```

`ground: F12 (extends F03 …)` points at a topic that is not in README's Frontier table. And the body's
*"(wave-1 row S034)"* attribution for the 众测 platform's exclusion of 互联网漏洞 is unsupported twice over: the lane
holds no S034, and the package's S034 row records the scoring multiplier and "its scope rule for authorised testing"
(`SOURCES.append.md:10`) — not an 互联网漏洞 exclusion. No other entry in the package attests that exclusion.

### R8 — Admission would move neither C2 counter. (axis `coverage`)

```
$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l   -> 0
```
The entry cites S044–S046, so it cannot reach counter B's `S1xx` shape. Counter A counts admitted **F rows**; a third
entry under the one new topic leaves A at 9 only by a row the frozen predicate describes as carrying *two* entries, and
its own label (F12) already collides with both admit candidates (also F12) while `claims.json` C2 names **F09**. Net:
the file would add a third authority on one topic and zero measured coverage.

### R9 — Domain: in-domain only at its edges. (PROVINCE)

`PROVINCE.md` owns "bounty & security research — scopes, program rules, claim packages" and refuses "anything outside
this domain". The in-domain kernel ("authorisation is not self-executing; exceeding scope is intrusion") is real but is
already the F03 boundary plus the better-sourced package entry `cn-criminal-offence-art285-baseline.md` (S084 npc.gov.cn,
tier A, whose *Rejected* section at line 34 states the 285(1) conduct-offence split **correctly**). The remainder is
penal commentary the lane's surfaces never invoke. Secondary ground, not the primary one.

## (b) Is the ground already held?

- **No, not in the lane.** `grep -rlnE '刑法|情节严重|285|未经授权' corpus/knowledge/ SKILL.md` → 0 of 33 files;
  `grep -riE 'rules of engagement|statutory auth' SKILL.md corpus/knowledge/` → 0 hits (matches C2's premise).
  `grep -rn 'F12\|F09'` outside `.ufo/waves` → 0.
- **But the correct version of its strongest claim is held in the package, better sourced, and is not in
  `candidates_admit`:** `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/cn-criminal-offence-art285-baseline.md`
  (S084 = `npc.gov.cn`, the enacting body, tier A; S088 = 检察日报 via web.archive.org), §Rule: *"Article 285(1) …
  carries **no** 情节严重 threshold: it is a conduct offence"*. Refusing this file therefore costs no coverage that a
  sibling cannot supply correctly.

## (d) Assertions this lane cannot document-only support

1. The Japanese-law comparison ("Japanese law has both … the opposite of Japan's on every axis") — no Japanese row in
   the entry, none in the lane registry.
2. "A researcher who stays inside an authorisation … is **nowhere near** the 情节严重 line" — a criminal-exposure
   prediction no cited text states, and false for 285(1) systems per R1. Q6 is not breached (no probing/scanning/
   submitting instruction), but this sentence functions as permission advice and must not be admitted as a rule.
3. "the exclusion of 互联网漏洞 by the 众测 platform (wave-1 row S034)" — row absent from the lane; the package row's
   recorded scope/anchor does not carry the exclusion (R7).

## (c) Flip condition — what would clear the refusal

All of the following, together:

1. **Register the rows first.** S044/S045/S046 adopted as lane rows with addendum-10 ids and the lane's **own** open date
   and located quote (Q1/Q2); this requires the missing `.ufo/waves/round-24/assimilation/renumber-map.tsv` (or an
   explicit, committed offset rule) so that package S031=HackerOne ≠ lane S031=CNA 4.2.6 is resolved, not overwritten.
2. **Fix the conclusion to the text.** Restate that 285(1) is a conduct offence for 国家事务/国防建设/尖端科学技术
   systems (quoting `/tmp/s045.txt:2121`), and delete "scale not act" as a general rule (R1).
3. **Quote 第一条 in full, including (五) 其他情节严重的情形**, and replace "purely quantitative" with "quantitative with
   an open catch-all" (R2).
4. **Make `recheck:` fail closed**: `curl -sSfL` + a capture comparison under a declared normalization (Q7/Q8), with at
   least one missing/corrupted control that must fail.
5. **Add a `### Rejected` section** rejecting at minimum: "purely quantitative", "risk attaches to scale not the act",
   and "Japanese law has both" absent a Japanese row (Q5).
6. **Delete or source the Japan comparison**; do not carry a comparative frame with one side unsourced (R6).
7. **Re-anchor `ground:` to the one F id the round actually admits** (F09 per `claims.json` C2, or F12 if L1 changes the
   row) — one id, committed in README, not two (R7/R8).
8. **Delete the "(wave-1 row S034)" clause** or register a row whose anchor actually carries the 互联网漏洞 exclusion (R7).

## Smallest safe correction (routing note for L1, not an edit)

Refuse this file; do not carry S044–S046 into the registry this round. If a Chinese leg is wanted under the new topic,
the lane already has a package entry that states the 285 rule correctly with a tier-A row from the enacting body —
`cn-criminal-offence-art285-baseline.md` (S084/S088) — and it carries its own *Rejected* and *Limits* sections. Adopt
that one, register its two rows this round, and let a thresholds-only entry follow once the five 第一条 items can be
quoted verbatim with the catch-all intact. That preserves C2's "each row re-opened by this lane with its own access date
and located quote" without creating a second authority on 285 and without a false-provenance register.

## Axis impact summary

| axis | impact of refusing | impact of admitting |
|---|---|---|
| `depth:verifiability` | none; the three unregistrable rows and the non-fail-closed recheck stay out | negative — 3 ids that resolve to no lane row, a recheck that exits 0 on a soft-404, and a renumber map that does not exist |
| `coverage` | C2 lands on the two admit candidates; no measured unit lost | none — counter B stays 0, counter A gains a third entry under one topic, frozen predicate names two |
