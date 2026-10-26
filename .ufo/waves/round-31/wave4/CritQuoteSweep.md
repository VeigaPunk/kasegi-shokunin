# CritQuoteSweep — mechanical quote sweep, F15 entry (round 31, wave 4)

- **Seat:** `CritQuoteSweep` (critic, leaf — no subagent dispatch, no background jobs, no installs needed)
- **Answering model:** `opencode-go/deepseek-v4.1-flash` (workstation route table; no model passed by this seat)
- **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope; this receipt is the only write)
- **Lane base:** `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`; HEAD at measurement `43c364d06ccf`; both measured files clean under `git status --porcelain`
- **Measured bytes:** entry `a488df492e2a72a929e0502ac9fabc80d00214a8fd6d83335ac624deb9c8d56f`; capture `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55` (3755 B, 97 lines)
- **Scope:** the quote/citation surface of `corpus/knowledge/vendor-third-party-finding-coordination.md` only. No network fetch, no package tool run, no git/jj mutation, no live target contact.

## 0. Method (reproducible)

Every `"` in the entry was paired mechanically (60 chars → 30 spans), and every `>` blockquote
line was taken as one quoted string: **30 spans + 7 blockquotes = 37 quote rows**. Each was then
bound against the opened cited line/range with a whitespace-normalised substring test
(`' '.join(s.split())`; multi-line entry quotes normalised the same way), plus a count in the
cited range and in the whole target file, plus a word count. The extraction and binding command:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 - <<'PY'
import re
L='/home/vgpnk/Projects/shokunin/kasegi-shokunin/'
S48='corpus/source-snapshots/round-31/S048.txt'; S40='corpus/source-snapshots/round-25/S040.txt'
F06='corpus/knowledge/multiparty-vulnerability-coordination.md'; RD='corpus/README.md'
STG='/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md'
rd=lambda p: open(p if p.startswith('/') else L+p,encoding='utf-8').read().split('\n')
F={p:rd(p) for p in (S48,S40,F06,RD,STG)}
norm=lambda s:' '.join(s.split())
# (id, entry line, quote, target file, cited line or a-b)
R=[('Q00',2,'Microsoft Security Vulnerability Research (MSVR)',S48,'28'),('Q01',14,'MSVR is a program specifically designed to help improve the security ecosystem as a whole through the sharing of knowledge and best practices.',S48,'29'),('Q02',19,'MSVR learns about vulnerabilities in third-party products in three ways:',S48,'31'),('Q03',26,'Internal Microsoft engineers',S48,'32'),('Q04',26,'These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue.',S48,'32'),('Q05',27,'External reports to the Microsoft Security Response Center (MSRC)',S48,'33'),('Q06',27,'These issues are coordinated by MSVR.',S48,'33'),('Q07',28,'Internal research projects',S48,'34'),('Q08',28,'Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices.',S48,'34'),('Q09',32,'products that run on Microsoft operating systems, but that are not developed by Microsoft',S48,'34'),('Q10',43,"This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach.",S48,'35'),('Q11',48,'as a vendor affected by vulnerabilities in its products and services',S48,'35'),('Q12',51,'as a finder of new vulnerabilities in third-party products and services',S48,'35'),('Q13',54,'as a coordinator of vulnerabilities that affect multiple vendors',S48,'35'),('Q14',64,'Optional participant that can assist vendors and finders',F06,'25'),('Q15',70,"A vendor's published policy is a standing first-party statement, not a programme",RD,'211'),('Q16',74,'may impact multiple vendors',S40,'185-193'),('Q17',75,'manage a coordinated industry\ndisclosure',S40,'185-193'),('Q18',88,'As time and resources permit',S48,'34'),('Q19',88,'that are not\n   developed by Microsoft',S48,'34'),('Q20',91,'as a coordinator of\n   vulnerabilities that affect multiple vendors',S48,'35'),('Q21',108,'$t',None,None),('Q22',124,'third-party product of affects both',S48,'33'),('Q23',133,"MSVR's N-day embargo",None,None),('Q24',133,'report it to MSVR at \u27e8address\u27e9',None,None),('Q25',134,'Microsoft Bug Bounty Programs',S48,'15'),('Q26',139,'Every large vendor runs such a programme.',None,None),('Q27',143,"A third-party finding sent to a vendor's response centre bypasses the affected\n   vendor.",None,None),('Q28',144,'with the affected vendor to fix\n   the issue',S48,'32'),('Q29',145,'reported to the affected vendor',S48,'34'),('Q30',147,'MSVR is a bug bounty programme.',None,None),('Q31',149,'Microsoft Bug Bounty Programs',S48,'15'),('Q32',150,'The page imposes a coordinated-disclosure obligation on finders.',None,None),('Q33',153,'the finder also has a coordinated-disclosure obligation',STG,'28'),('Q34',155,'A vendor that coordinates third-party findings replaces the external coordinator.',None,None),('Q35',156,'Optional participant',F06,'25'),('Q36',159,'Certified Refurbished',S48,'48')]
def at(p,c):
    if '-' in c: a,b=map(int,c.split('-')); return '\n'.join(F[p][a-1:b])
    return F[p][int(c)-1]
for rid,eln,q,tgt,c in R:
    w=len(q.split()); nq=norm(q)
    if tgt is None:
        n=sum(1 for x in F[S48] if nq in norm(x)); print(rid,'unbound',w,'shell/hypothetical/rejected','S048hits',n); continue
    span=norm(at(tgt,c)); hits=span.count(nq); nf=sum(1 for x in F[tgt] if nq in norm(x))
    v = 'Y' if hits else ('Y-emphasis' if tgt==STG and nq in norm(re.sub(r'[*_]','',open(tgt,encoding='utf-8').read())) else 'N')
    print(rid,'L%d'%eln,'words=%d'%w,tgt.split('/')[-1]+':'+str(c),'verbatim='+v,'hits=%d'%hits,'filehits=%d'%nf)
PY
```

This is the exact checker that produced Table 1 (row data inline, so the run is self-contained; the
staged-package row is the only one where the `*emphasis*` markers matter). The pairing pass on the
same bytes found 30 `"`-delimited spans (0 unbalanced quote characters) and 7 blockquote quote
lines (entry L14, L19, L32, L43, L48, L51, L54). The
binding table below is the direct output of the checker (`Q00`–`Q36`).

```
$ sha256sum corpus/knowledge/vendor-third-party-finding-coordination.md corpus/source-snapshots/round-31/S048.txt
a488df492e2a72a929e0502ac9fabc80d00214a8fd6d83335ac624deb9c8d56f  corpus/knowledge/vendor-third-party-finding-coordination.md
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
$ wc -l -c corpus/source-snapshots/round-31/S048.txt
  97 3755 corpus/source-snapshots/round-31/S048.txt
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048; echo "exit=$?"
S048:sha256 OK
S048:Q1 OK occurrences=1
... (Q2..Q10 identical) ...
S048:Q11 OK occurrences=1
exit=0
```

## 1. Quote table — 37 rows, one per quoted string

| # | entry L | quoted string (from the entry) | words | cited location | opened cited text (first 70 ch, ws-normalised) | verbatim | count cited range | count target file | line right |
|---|---|---|---|---|---|---|---|---|---|
| Q00 | 2 | "Microsoft Security Vulnerability Research (MSVR)" | 5 | S048.txt:28 | Microsoft Security Vulnerability Research (MSVR)… | Y | 1 | 1 | Y |
| Q01 | 14 | "MSVR is a program specifically designed to help improve the security ecosystem as a whole throu…" | 23 | S048.txt:29 | MSVR is a program specifically designed to help improve the security e… | Y | 1 | 1 | Y |
| Q02 | 19 | "MSVR learns about vulnerabilities in third-party products in three ways:" | 10 | S048.txt:31 | MSVR learns about vulnerabilities in third-party products in three way… | Y | 1 | 1 | Y |
| Q03 | 26 | "Internal Microsoft engineers" | 3 | S048.txt:32 | Internal Microsoft engineers: In the course of their regular work, eng… | Y | 1 | 1 | Y |
| Q04 | 26 | "These vulnerabilities are reported to the MSVR team, which then works with the affected vendor …" | 19 | S048.txt:32 | Internal Microsoft engineers: In the course of their regular work, eng… | Y | 1 | 1 | Y |
| Q05 | 27 | "External reports to the Microsoft Security Response Center (MSRC)" | 9 | S048.txt:33 | External reports to the Microsoft Security Response Center (MSRC): On … | Y | 1 | 1 | Y |
| Q06 | 27 | "These issues are coordinated by MSVR." | 6 | S048.txt:33 | External reports to the Microsoft Security Response Center (MSRC): On … | Y | 1 | 1 | Y |
| Q07 | 28 | "Internal research projects" | 3 | S048.txt:34 | Internal research projects: As time and resources permit, Microsoft pe… | Y | 1 | 1 | Y |
| Q08 | 28 | "Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclos…" | 14 | S048.txt:34 | Internal research projects: As time and resources permit, Microsoft pe… | Y | 1 | 1 | Y |
| Q09 | 32 | "products that run on Microsoft operating systems, but that are not developed by Microsoft" | 14 | S048.txt:34 | Internal research projects: As time and resources permit, Microsoft pe… | Y | 1 | 1 | Y |
| Q10 | 43 | "This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) appr…" | 11 | S048.txt:35 | This coordination takes place under Microsoft's Coordinated Vulnerabil… | Y | 1 | 1 | Y |
| Q11 | 48 | "as a vendor affected by vulnerabilities in its products and services" | 11 | S048.txt:35 | This coordination takes place under Microsoft's Coordinated Vulnerabil… | Y | 1 | 1 | Y |
| Q12 | 51 | "as a finder of new vulnerabilities in third-party products and services" | 11 | S048.txt:35 | This coordination takes place under Microsoft's Coordinated Vulnerabil… | Y | 1 | 1 | Y |
| Q13 | 54 | "as a coordinator of vulnerabilities that affect multiple vendors" | 9 | S048.txt:35 | This coordination takes place under Microsoft's Coordinated Vulnerabil… | Y | 1 | 1 | Y |
| Q14 | 64 | "Optional participant that can assist vendors and finders" | 8 | multiparty-vulnerability-coordination.md:25 | \| Definitions — Coordinator \| “Optional participant that can assist ve… | Y | 1 | 1 | Y |
| Q15 | 70 | "A vendor's published policy is a standing first-party statement, not a programme" | 12 | README.md:211 | \| F10 \| Vendor-side disclosure policies as corpus objects \| admitted \|… | Y | 1 | 1 | Y |
| Q16 | 74 | "may impact multiple vendors" | 4 | S040.txt:185-193 (hit L191) | Incidents that may impact other vendors: The Cisco PSIRT works with th… | Y | 1 | 1 | Y |
| Q17 | 75 | "manage a coordinated industry disclosure" | 5 | S040.txt:185-193 (hit L190) | Incidents that may impact other vendors: The Cisco PSIRT works with th… | Y | 1 | 1 | Y |
| Q18 | 88 | "As time and resources permit" | 5 | S048.txt:34 | Internal research projects: As time and resources permit, Microsoft pe… | Y | 1 | 1 | Y |
| Q19 | 88 | "that are not developed by Microsoft" | 6 | S048.txt:34 | Internal research projects: As time and resources permit, Microsoft pe… | Y | 1 | 1 | Y |
| Q20 | 91 | "as a coordinator of vulnerabilities that affect multiple vendors" | 9 | S048.txt:35 | This coordination takes place under Microsoft's Coordinated Vulnerabil… | Y | 1 | 1 | Y |
| Q21 | 108 | "$t" | 1 | not a source quote (shell variable in the sweep command) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q22 | 124 | "third-party product of affects both" | 5 | S048.txt:33 | External reports to the Microsoft Security Response Center (MSRC): On … | Y | 1 | 1 | Y |
| Q23 | 133 | "MSVR's N-day embargo" | 3 | not a source quote (hypothetical unsupported line) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q24 | 133 | "report it to MSVR at ⟨address⟩" | 6 | not a source quote (hypothetical unsupported line) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q25 | 134 | "Microsoft Bug Bounty Programs" | 4 | S048.txt:15 | Microsoft Bug Bounty Programs… | Y | 1 | 1 | Y |
| Q26 | 139 | "Every large vendor runs such a programme." | 7 | not a source quote (rejected over-generalization) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q27 | 143 | "A third-party finding sent to a vendor's response centre bypasses the affected vendor." | 13 | not a source quote (rejected over-generalization) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q28 | 144 | "with the affected vendor to fix the issue" | 8 | S048.txt:32 | Internal Microsoft engineers: In the course of their regular work, eng… | Y | 1 | 1 | Y |
| Q29 | 145 | "reported to the affected vendor" | 5 | S048.txt:34 | Internal research projects: As time and resources permit, Microsoft pe… | Y | 1 | 1 | Y |
| Q30 | 147 | "MSVR is a bug bounty programme." | 6 | not a source quote (rejected over-generalization) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q31 | 149 | "Microsoft Bug Bounty Programs" | 4 | S048.txt:15 | Microsoft Bug Bounty Programs… | Y | 1 | 1 | Y |
| Q32 | 150 | "The page imposes a coordinated-disclosure obligation on finders." | 8 | not a source quote (rejected over-generalization) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q33 | 153 | "the finder also has a coordinated-disclosure obligation" | 7 | staged pkg:28 | the *finder* also has a coordinated-disclosure obligation when the fin… | N raw / Y rendered (M1) | 0 | 0 | Y (only occurrence) |
| Q34 | 155 | "A vendor that coordinates third-party findings replaces the external coordinator." | 10 | not a source quote (rejected over-generalization) | — | n/a (expects absent) | — | 0 in S048 | — |
| Q35 | 156 | "Optional participant" | 2 | multiparty-vulnerability-coordination.md:25 | \| Definitions — Coordinator \| “Optional participant that can assist ve… | Y | 1 | 1 | Y |
| Q36 | 159 | "Certified Refurbished" | 2 | S048.txt:48 | Certified Refurbished… | Y | 1 | 1 | Y |

Totals: **23 rows bound to S048** (all 23 verbatim, exactly once in the capture, right line);
5 rows bound to other lane files (F06 ×2, S040 ×2, README ×1, all verbatim exactly once);
1 row bound to the staged package (Q33, `verbatim=Y-emphasis` in the checker — raw bytes N, see
M1); 8 rows are not source quotes (1 shell variable, 2 explicitly unsupported hypotheticals,
5 rejected over-generalizations) and none of their strings occurs in S048 (0 each), which is the
required result. **No quote exceeds 25 words; maximum is 23 (Q01).** Completeness: the entry
contains exactly these 37 quoted strings (30 straight-`"` spans, 0 unbalanced, plus 7 blockquote
quote lines; `grep -c '[“”「」『』]'` → `0`, so no typographic-quote span escapes the pairing), hence
no 40th quote exists to row; the remaining rows in this receipt are the 33 citation anchors.

## 2. Citation table — 33 rows, every `file:line` / `L<n>` anchor outside a quote

| # | entry L | anchor | command run (from lane root) | observed | right? |
|---|---|---|---|---|---|
| B01 | 2 | `S048.txt:28-35` | `sed -n '28p;35p;36p' corpus/source-snapshots/round-31/S048.txt` | L28 heading; L35 role sentence; L36 footer starts | Y |
| B02 | 2 | programme description `L29` | Q01 binding | verbatim at L29 | Y |
| B03 | 2 | three-route sentence `L31` | Q02 binding | verbatim at L31 | Y |
| B04 | 2 | three routes `L32-L34` | Q03–Q08 bindings | labels+handling at L32/L33/L34 | Y |
| B05 | 2 | three-role sentence `L35` | Q10–Q13 bindings | verbatim at L35 | Y |
| B06 | 4 | "the three route labels at `L26-28`" | `cat -n` entry L26-28; `sed -n '26,28p' S048.txt` | entry L26-28 = the three label rows; capture L26-28 = chrome | entry-relative Y; unqualified (N1) |
| B07 | 63 | `S018 FIRST v1.1` | `sed -n '2p' corpus/knowledge/multiparty-vulnerability-coordination.md` | `source: S018 — https://www.first.org/…/guidelines-v1.1 — version 1.1` | Y |
| B08 | 65, 66 | F06 `line 25` | `sed -n '25p' corpus/knowledge/multiparty-vulnerability-coordination.md` | `\| Definitions — Coordinator \| “Optional participant …”` | Y |
| B09 | 69 | `corpus/README.md` F10 row | `sed -n '211p' corpus/README.md` | row begins `\| F10 \| Vendor-side disclosure policies as corpus objects \| admitted` | Y |
| B10 | 73 | `S039.txt:506` | `sed -n '506p' corpus/source-snapshots/round-25/S039.txt \| grep -c '届出窓口'` | `1` | Y |
| B11 | 73 | VDO `Claim 7` | `sed -n '126p;132p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` | L126 `## Claim 7 — Hitachi's …`; L132 carries `capture S039.txt:506` | Y |
| B12 | 76 | `S040.txt:185-193` | `sed -n '185,193p' …/round-25/S040.txt \| grep -c 'may impact multiple vendors\|manage a coordinated industry'` | `2` (L190, L191) | Y |
| B13 | 76 | `cisco-jpcert-partner` row | `sed -n '49p' corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | `\| cisco-jpcert-partner \| Cisco (S040) \| "Japan Computer Emergency Response Team …` | Y |
| B14 | 78 | `S036.txt:15` | `sed -n '15p' …/round-25/S036.txt` | `当社が利用しているサードパーティー製品` | Y |
| B15 | 79 | `line 35` of VDO | `sed -n '35p' …/vendor-disclosure-policies-as-corpus-objects.md` | `> 当社が利用しているサードパーティー製品` | Y |
| B16 | 81 | `line 23` of same entry | `sed -n '23p' … \| grep -c '社内での検出'` | `1` | Y |
| B17 | 90 | `S039.txt:506` | same as B10 | `1` | Y |
| B18 | 94 | `S040.txt:185-193` | same as B12 | `2` | Y |
| B19 | 95 | `S039.txt:506` | same as B10 | `1` | Y |
| B20 | 101 | F11 entry + `S041` | `grep -n 'source: S041' corpus/knowledge/iso-29147-and-30111-division-of-labour.md` | line 2 `source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | Y |
| B20b | 102–103 | "assigns no finder or coordinator seat to a vendor" | `grep -niE 'finder\|coordinator' …/iso-29147-and-30111-division-of-labour.md` | 0 matching lines | consistent (vacuous) |
| B21 | 111 | own path | `test -f corpus/knowledge/vendor-third-party-finding-coordination.md` | exists | Y |
| B22 | 122 | "navigation chrome is `L3-L27`" | `sed -n '27,28p' S048.txt` | L27 `Security Researcher Leaderboard`, L28 programme heading | Y |
| B23 | 122 | "footer `L36-L97`" | `sed -n '36p' S048.txt`; `wc -l` | L36 `Surface Laptop Ultra`; file has 97 lines | Y |
| B24 | 123 | "`L2` carries a per-request Trace Id" | `sed -n '2p' S048.txt` | `This is the Trace Id: f97e6b1c…` | Y |
| B25 | 123 | "`L33` carries a source typo" | Q22 binding | `third-party product of affects both` at L33 | Y |
| B26 | 134 | navigation item at `L15` | `grep -ni bounty S048.txt` | `15:Microsoft Bug Bounty Programs` | Y |
| B27 | 147 | "programme body `(L28-L35)`" | B01 | body = L28-L35 | Y |
| B28 | 149 | `(L15)` | B26 | same | Y |
| B29 | 151 | CVD framing `(L35)` | Q10 binding | verbatim at L35 | Y |
| B30 | 156 | F06 `(line 25)` | B08 | same | Y |
| B31 | 159 | "only `cert` match … at `L48`" | `grep -ci cert S048.txt`; `grep -ni cert S048.txt` | `1`; `48:Certified Refurbished` | Y |
| B32 | 164–165 | `3755 B, 97 lines, sha256 2001ad…` | `wc -l -c`; `sha256sum` | `97 3755`; digest identical to the quoted one | Y |

## 3. The entry's own numeric assertions (counts re-derived, not retyped)

| assertion (entry L) | command | quoted value | observed |
|---|---|---|---|
| FC-1 label enumeration (131) | `grep -cE '^(Internal Microsoft engineers\|External reports to the Microsoft Security Response Center \(MSRC\)\|Internal research projects):' S048.txt` | `3` | `3` |
| FC-1 "in three ways" (131) | `grep -c 'in three ways' S048.txt` | `1` | `1` |
| FC-1 "only" / no exclusivity (131) | `grep -ci 'only' S048.txt` | `0` | `0` |
| FC-2 coordinator sentence (132) | `grep -c 'as a coordinator of vulnerabilities that affect multiple vendors' S048.txt` | `1` | `1` |
| FC-3 / honest limit clock words (118, 133) | `grep -ciE '90[ -]day\|deadline\|embargo\|timeline' S048.txt` | `0` | `0` |
| FC-3 address token (118, 133) | `grep -ci '@microsoft' S048.txt` | `0` | `0` |
| honest limit URL token (119) | `grep -ci 'http' S048.txt` | `0` | `0` |
| FC-4 body has no payment term (134) | `sed -n '28,35p' S048.txt \| grep -ci bounty` | `0` | `0` |
| FC-4 page has one bounty line (134) | `grep -ci bounty S048.txt` | `1` (L15) | `1`, L15 |
| FC-5 affected-vendor mentions (135) | `grep -c 'affected vendor' S048.txt` | `2` (L32, L34) | `2`, L32/L34 |
| FC-5 external centres absent (157) | `grep -c 'CERT/CC'`; `'JPCERT'`; `'IPA'` | `0`; `0`; `0` | `0`; `0`; `0` |
| FC-5 cert match (158) | `grep -ci cert S048.txt` | `1` (L48) | `1`, L48 |
| manifest assertion count (4) | manifest ids | 11 | Q1–Q11, all `occurrences=1`, exit 0 |

## 4. Obligation / deadline / address check

Sentence-level scan (`must|should|shall|required|obligation|deadline|embargo|timeline|within|N-day|report(ing|ed|s) to|contact|e-mail|@|address`) returns **no sentence that states an obligation, deadline or address as carried by the capture**. The only rule-shaped sentence is entry L160:

> "and a package must record which party coordinates rather than assume either."

That is a recording rule the lane imposes on corpus packages, inside the rejected-over-generalizations section; it is not attributed to S048 and asserts nothing about vendors or finders. Every other occurrence is negative or explicitly unsupported: L116–L120 ("It does not state the coordination agreements, a timeline, a reporting address or a per-vendor process"), L133 ("Any "MSVR's N-day embargo" or "report it to MSVR at ⟨address⟩" line cannot be supported from S048"), L151–L154 ("it states no obligation, no deadline and no address … is an inference these bytes do not carry"). The only URL in the entry is the `source:` URL on L2; `grep -nE '@|op://|vault|token'` returns only L118 and L133, both hits being the literal pattern text `'@microsoft'` inside the quoted grep commands, and the only `session` mention is the negative disclosure sentence at L172 ("session or private URL"). No address, credential material, session URL or vault reference is carried. The capture itself carries no `@`, no `http`, and no clock word (Section 3).

## 5. Findings

**M1 — Q33 is the one byte-level deviation (non-defect; rejected-inference quote, outside S048).**
Entry L153 quotes "the finder also has a coordinated-disclosure obligation" as the staged package's sentence. The staged bytes are:

```
$ grep -rn 'coordinated-disclosure obligation' /home/vgpnk/Projects/shokuknow/merge/kasegi/
/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md:28:the *finder* also has a coordinated-disclosure obligation when the finding is not
$ python3 -c "
import re
p='/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md'
t=open(p,encoding='utf-8').read()
q='the finder also has a coordinated-disclosure obligation'
print('raw substring:', q in t)
print('emphasis-stripped:', q in re.sub(r'[*_]','',t))
print([i for i,l in enumerate(t.split(chr(10)),1) if 'coordinated-disclosure obligation' in l])
"
raw substring: False
emphasis-stripped: True
[28]
```

So the quote is faithful to the *rendered* sentence but not to the raw bytes (`*finder*`), it truncates the clause "when the finding is not solely about the finder" without an ellipsis, and the citing sentence names no path:line. This is not a Q3 failure: the quoted sentence is a rejection ("is an inference these bytes do not carry"), not a load-bearing claim, and it does not occur in S048 (0). Smallest safe correction, if the lane wants byte-strict quoting of a rejected inference: cite it as ``the *finder* also has a coordinated-disclosure obligation …`` plus the staged path and `:28`; otherwise leave as is.

**N1 — "the three route labels at L26-28" (entry L4) is unqualified.** Read entry-relative it is correct (entry L26-L28 are exactly the three label rows, hand-measured, as the sentence says). Read capture-relative it is wrong (S048 L26-L28 are chrome: `AI Safety Acknowledgements`, `Security Researcher Leaderboard`, the programme heading). The note's own clause ("the strings in the falsifiable checks are hand-measured, not manifest-bound") makes the entry-relative reading the only coherent one; a one-word fix ("entry L26-28") would remove the ambiguity.

**N2 (observation, no action).** Q14 truncates F06's sentence mid-clause ("…vendors and finders" drops "in handling and disclosing vulnerability information"). Verbatim substring, 8 words — Q3-compliant; noted only because the truncation is unmarked.

Everything else: no mismatched quote, no wrong line number, no quote over 25 words, no cited location that fails to open, and no stray quotation of capture chrome as programme text (Q22 is explicitly labelled a source typo and appears in no quote; the L15 bounty line is quoted only as chrome and rejected as evidence).

## Verdict

**`clean`** — zero mismatches among the 28 source-bound quote rows (23 bound to S048, 2 to F06, 2 to S040, 1 to README), and the 8 non-source rows are correctly absent from the capture. The mismatch list is exactly one entry, **M1 (Q33)**, which is a rejected-inference quote against the staged package and not part of the entry's S048 binding; N1 is an anchor-qualification ambiguity, not a wrong line.
