# Renumber map — round 25 assimilation (staged → lane)

Scope: the five rows round 25 adopts. Keyed by DOCUMENT, not by staged id.
Rule: **a lane id follows the document's URL + anchor.** Arithmetic on staged ids is
forbidden and, as shown in §3, would produce a wrong map on this very package.

Lane registry head: `corpus/SOURCES.md` holds S001–S035 (35 rows), so the next free lane id is S036.
Adoption order below follows the order the documents first appear in the adopted entry set
(Cybozu policy → Cybozu bounty FAQ → Pepabo safe harbour → Hitachi disclosure process → Cisco policy).

| staged id | new lane id | document title | document identity (URL) | anchor that fixes the document |
|---|---|---|---|---|
| S055 | **S036** | 脆弱性情報ハンドリングポリシー (Cybozu) | https://cybozu.co.jp/company/security-policy/ | 脆弱性対応 → 対象範囲; 脆弱性対応フロー 1 情報収集・2 影響の確認・3 対策; 脆弱性情報の公開 → 対象範囲 / 2 JVNでの公開 |
| S056 | **S037** | FAQ（脆弱性報奨金制度） (Cybozu) | https://cybozu.co.jp/products/bug-bounty/faq/ | FAQ 「脆弱性を見つけたので報告したいのですが、どうしたら良いですか？」; 「脆弱性報奨金制度に参加せずに報告したいのですが？」; 「Webサイトの脆弱性を見つけました。報告しても良いですか？」; 「報奨金はいつ支払われますか？」 |
| S057 | **S038** | 脆弱性報告制度 (GMO Pepabo) | https://pepabo.com/contact/vulnerability-reporting/ | 脆弱性報告制度; 脆弱性の評価について; 脆弱性の検証目的であっても、以下の行為については禁止いたします 1・2 |
| S060 | **S039** | 日立グループにおける製品脆弱性情報の開示プロセス（HIRT-PUB10008） (Hitachi) | https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html | body paragraphs: product-vendor IRT focus, and the coordinated-report case for findings affecting another vendor's product |
| S068 | **S040** | Cisco Security Vulnerability Policy (Cisco) | https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html | "Cisco Product Security Incident Response"; the third-party coordination paragraph; "Disclosure of Security Vulnerabilities" |

## 1. Invariants this map holds

1. **Identity is the document.** The lane id is bound to the (URL, anchor) pair in column 4–5.
   Re-order the staged file, re-run the package, or split the merge report differently: each
   document still lands on the id above, because the id is looked up by URL, not by position.
2. **No arithmetic.** S055→S036 is *not* `55 − 19`, and no single offset maps the five rows
   (55−36=19, 56−37=19, 57−38=19, 60−39=21, 68−40=28). The offsets differ because the staged
   ids skip rows the round does not adopt (S058, S059, S061–S067).
3. **Renumbering is a projection, not a translation.** Staged ids of non-adopted rows never
   become lane ids. Staged S036–S040 name five *other* documents (BILISRC, GB/T 30279 openstd,
   GB/T 30279 std.samr, e-Gov 法令, MIC citizen page) — so a "staged id − 19" rule would hand
   S036 to BILISRC, not to the Cybozu policy. The lane ids S036–S040 are free (verified §4).
4. **The map must be applied to entry headers.** Any `corpus/knowledge/*.md` header written
   against the staged numbering must carry the lane id (`source: S036`, not `source: S055`).
   The C2 counter greps `^source: S0(3[6-9]|[4-9][0-9])`, so a staged id left in a header
   fails the claim.

## 2. What this map is NOT

- It is not a renumbering of the staged file. `/home/vgpnk/Projects/shokuknow` is read-only for
  this lane; the staged ids are external and stay as they are.
- It does not adopt anything. S068 is listed because the round's adoption set names it
  (`S068->S040`); whether the Cisco row is actually admitted or rejected is the C2 seat's call.
  If S068 is rejected, S040 stays free and the remaining four ids are unchanged — the map is
  per-document, so dropping a row never shifts the others.
- It does not touch `corpus/SOURCES.md`. The append is the registry owner's write.

## 3. Why the id-space collision (S031–S035) forbids arithmetic

The collision check found 5 numeric collisions between lane ids and staged ids. Each pair is a
*different document*, not a duplicate row:

| id | lane document URL | staged document URL | same document? |
|---|---|---|---|
| S031 | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | https://hackerone.com/security/policy_versions | NO |
| S032 | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf | https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md | NO |
| S033 | https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 | https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json | NO |
| S034 | https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/ | https://zc.cnvd.org.cn/news/helpList | NO |
| S035 | https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf | https://security.360.cn/Reward/rules | NO |

So the staged numbering is a separate id space that overlaps the lane's. Any rule that reads a
staged id as a lane id, or that shifts by a constant, silently binds a lane id to the wrong
document. That is the failure the §10 guard exists to catch before append.

## 4. Verification actually run (lane root = /home/vgpnk/Projects/shokunin/kasegi-shokunin)

```
$ wc -l .ufo/waves/round-25/assimilation/ids/reg-ids .ufo/waves/round-25/assimilation/ids/staged-ids .ufo/waves/round-25/assimilation/ids/collisions
 35 reg-ids
 94 staged-ids
  5 collisions

$ cat .ufo/waves/round-25/assimilation/ids/collisions
S031
S032
S033
S034
S035

$ for id in S036 S037 S038 S039 S040; do grep -cE "^ {0,3}\|[[:space:]]*$id " corpus/SOURCES.md; done
0 0 0 0 0        # every target lane id is free

$ grep -cF '<each adopted URL>' corpus/SOURCES.md
0 0 0 0 0        # no adopted document is already registered under another id
```

Collision count: **5**. Adopted ids S055/S056/S057/S060/S068 are all above the registry head
(S035), so **no collision falls on an adopted row**; the five collisions are id-space overlaps
on rows this round does not adopt.
