# CISA Known Exploited Vulnerabilities catalog — exploitation membership with a per-record remediation clock

source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture corpus/source-snapshots/round-35/S052.txt (27,870 lines; sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826): title L2, catalogVersion L3, dateReleased and count L4-L5, first record L7-L22, the FCEB deadline sentence L5423 (again L5439), record assertions L15465-L15475 and L19161-L19168
verified-at: 2026-10-26
ground: F18
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052   # five assertions (Q1-Q5) at anchors 2, 3, 4, 15472 and 19165, each `occurrences=1` with `sha256 OK`; exits 2 when the manifest or capture is absent and 1 when a quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

CISA's catalog, read as CISA's own machine-readable feed and nothing wider (Q4). The snapshot's only descriptive text is its title (L2); it carries no prose definition of "known exploited", so this entry does not attribute a definition sentence to S052 — it records what the fields and the per-record deadline text do. The directives the feed names are CISA's own field text, not the directive documents, which are not in the capture.

## Claim 1 — one JSON object: title, version stamp, release instant, a declared count, and the array

> "title": "CISA Catalog of Known Exploited Vulnerabilities", — L2

> "dateReleased": "2026-10-23T19:30:18.9209Z", "count": 1756, — L4-L5 (whitespace-joined across the line break)

Five top-level keys (FC-1). The declared `count` equals the array length and the number of distinct `cveID` values: **1,756** records (FC-1, FC-2). A `"catalogVersion": "2026.10.23",` stamp sits directly under the title (L3). So 1,756 is this capture's record count at catalog version 2026.10.23, not a live total — and not the F18 brief's ~1,300.

## Claim 2 — twelve per-record keys, one key set for every record

> "dueDate": "2022-07-18", "knownRansomwareCampaignUse": "Known", "forensicTriage": "No", "notes": "https:\/\/nvd.nist.gov\/vuln\/detail\/CVE-2022-29499", — L15472-L15475, record cveID L15465 (CVE-2022-29499)

> "dateAdded": "2022-03-25", "shortDescription": "Citrix SD-WAN and NetScaler SD-WAN allow SQL Injection.", "requiredAction": "Apply updates per vendor instructions.", "dueDate": "2022-04-15", — L19165-L19168, record cveID L19161 (CVE-2019-12989)

The keys are `cveID`, `vendorProject`, `product`, `vulnerabilityName`, `dateAdded`, `shortDescription`, `requiredAction`, `dueDate`, `knownRansomwareCampaignUse`, `forensicTriage`, `notes`, `cwes`: 12 keys, one distinct key set across all 1,756 records (FC-3). The F18 brief lists nine; `forensicTriage`, `notes` and `cwes` are additional. Two fields are closed vocabularies: `knownRansomwareCampaignUse` Known 361 / Unknown 1,395 and `forensicTriage` Yes 91 / No 1,665 (FC-4). No field records exploitation evidence, an actor, or an exploited/not-exploited status.

## Claim 3 — a per-record remediation clock: dateAdded → dueDate

The Q5 assertion quoted in Claim 2 carries one record's clock in full: `dateAdded` 2022-03-25 to `dueDate` 2022-04-15, a 21-day gap on CVE-2019-12989 (L19165, L19168).

`dueDate` is later than `dateAdded` in all 1,756 records (FC-5); the 21-day gap is the mode (1,025 records), then 14 days (280) and 181 days (238), and 513 distinct due dates occur. The feed assigns each record its own deadline rather than one global date.

## Claim 4 — whose clock, and which directive: FCEB in the sentence, BOD 22-01 or BOD 26-04 per record

> "The KEV due date refers to the deadline by which FCEB agencies are expected to review" — L5423-L5424 (the sentence continues to name Emergency Directive (ED) 25-03 at the same lines); it occurs twice (L5423, L5439), so it is anchored and not a manifest assertion (FC-9)

> "Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable." — L2246; this sentence is identical in 327 records, so it is anchored too (FC-10)

The capture is explicit where the brief was not. Its deadline sentence names FCEB agencies and Emergency Directive (ED) 25-03 — "the deadline by which FCEB agencies are expected to review" — the one place the feed states an addressee. Directive naming varies by record: 340 `requiredAction` values cite BOD 22-01, 139 cite BOD 26-04 (138 of those same records also cite it in `notes`), no record cites both, and 1,277 cite neither (FC-6). There are 46 distinct `requiredAction` values; 893 records share the single most common value, `Apply updates per vendor instructions.` (as at L19167; FC-7 prints the value and its count). So the dueDate clock is tied to BOD 22-01 only on the 340 records that say so, and 139 name BOD 26-04 instead; these bytes establish neither directive's status nor its force, and no claim in this entry depends on one. The live page that states the directives' status is noted, not claimed, in Scope.

## Claim 5 — not a severity ladder: no CVSS, no score field

The 12-key list has no score, severity, CVSS or risk field, and `cvss` occurs 0 times, `base score` 0, `risk rating` 0 (FC-8). `severity` occurs twice and `score` once in the whole capture, all inside free text — L5135 and L11629 are URL slugs inside `notes` strings, L23592 is prose inside a `shortDescription` — so "no severity field" is the measured statement, not "no severity token". KEV membership is CISA's inclusion decision, and the feed carries no severity number to band against a CVSS score: a record's presence is a different signal from a high severity score.

## Claim 6 — not a reward ladder

`reward` and `bounty` occur 0 times and there is no amount, currency or payout field (FC-8); the single `$` in the capture is inside a Java class identifier, `org.ajax4jsf.resource.UserResource$UriData`, in a `shortDescription` at L11954 (FC-11). F13 holds platform reward ladders and F17 a Web3 impact ladder; both price impacts, while this feed lists membership plus a deadline.

## Honest limit

- **No definitional sentence.** "Known Exploited" is the title's phrase (L2), and no field encodes exploitation evidence; any definition must be attributed to CISA's catalog page, not to S052.
- **Directive coverage is per record.** BOD 22-01 (340), BOD 26-04 (139), neither (1,277); the capture names no directive for the majority.
- **A dated count.** 1,756 records at catalog version 2026.10.23, released 2026-10-23; `dateAdded` runs from 2021-11-03 to 2026-10-23.
- **A pin, not a live endpoint.** The recheck compares this entry's quotes with the captured bytes; it says nothing about the feed after 2026-10-26T06:32:40Z.

## Falsifiable rule and checks

**Falsifiable rule.** Any capture where (a) the top-level or 12-key shape changes, (b) some `dueDate` is not later than its `dateAdded`, (c) a `knownRansomwareCampaignUse` value falls outside {Known, Unknown}, (d) a `forensicTriage` value falls outside {Yes, No}, or (e) the declared `count` differs from the array length, makes the claims above false. Run from the lane root.

- **FC-1 — declared count equals the array.** `python3 -c 'import json;d=json.load(open("corpus/source-snapshots/round-35/S052.txt"));print("keys",len(d),"count",d["count"],"records",len(d["vulnerabilities"]))'` → `keys 5 count 1756 records 1756`.
- **FC-2 — 1,756 distinct cveIDs.** `python3 -c 'import json;v=json.load(open("corpus/source-snapshots/round-35/S052.txt"))["vulnerabilities"];print("ids",len({r["cveID"] for r in v}),"of",len(v))'` → `ids 1756 of 1756`.
- **FC-3 — one key set, 12 keys.** `python3 -c 'import json;v=json.load(open("corpus/source-snapshots/round-35/S052.txt"))["vulnerabilities"];ks={tuple(sorted(r)) for r in v};print("keysets",len(ks),"keys",len(next(iter(ks))))'` → `keysets 1 keys 12`.
- **FC-4 — the two closed vocabularies.** `python3 -c 'import json,collections as c;v=json.load(open("corpus/source-snapshots/round-35/S052.txt"))["vulnerabilities"];print(dict(c.Counter(r["knownRansomwareCampaignUse"] for r in v)),dict(c.Counter(r["forensicTriage"] for r in v)))'` → `{'Unknown': 1395, 'Known': 361} {'No': 1665, 'Yes': 91}`.
- **FC-5 — the clock is forward.** `python3 -c 'import json,collections as c,datetime as t;v=json.load(open("corpus/source-snapshots/round-35/S052.txt"))["vulnerabilities"];dl=[(t.date.fromisoformat(r["dueDate"])-t.date.fromisoformat(r["dateAdded"])).days for r in v];print("forward",sum(x>0 for x in dl),"of",len(dl),c.Counter(dl).most_common(3))'` → `forward 1756 of 1756 [(21, 1025), (14, 280), (181, 238)]`.
- **FC-6 — directive rows.** `python3 -c 'import json;v=json.load(open("corpus/source-snapshots/round-35/S052.txt"))["vulnerabilities"];b22=[r for r in v if "BOD 22-01" in r["requiredAction"]];b26=[r for r in v if "BOD 26-04" in r["requiredAction"]];print("bod22",len(b22),"bod26",len(b26),"both",len([r for r in b22 if "BOD 26-04" in r["requiredAction"]]),"neither",sum("BOD 22-01" not in r["requiredAction"] and "BOD 26-04" not in r["requiredAction"] for r in v))'` → `bod22 340 bod26 139 both 0 neither 1277`.
- **FC-7 — requiredAction variety.** `python3 -c 'import json,collections as c;v=json.load(open("corpus/source-snapshots/round-35/S052.txt"))["vulnerabilities"];ra=c.Counter(r["requiredAction"] for r in v);print("distinct",len(ra),"top",ra.most_common(1))'` → `distinct 46 top [('Apply updates per vendor instructions.', 893)]`.
- **FC-8 — severity and reward absence.** `for p in cvss "base score" "risk rating" reward bounty; do printf '%s=%s ' "$p" "$(grep -ci "$p" corpus/source-snapshots/round-35/S052.txt)"; done; printf 'severity+score=%s\n' "$(grep -oi 'severity\|score' corpus/source-snapshots/round-35/S052.txt | wc -l)"` → `cvss=0 base score=0 risk rating=0 reward=0 bounty=0 severity+score=3`.
- **FC-9 — the FCEB sentence occurs twice.** `grep -c 'The KEV due date refers to the deadline by which FCEB agencies are expected to review' corpus/source-snapshots/round-35/S052.txt` → `2`.
- **FC-10 — the BOD 22-01 sentence occurs 327 times.** `grep -c 'follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable\.' corpus/source-snapshots/round-35/S052.txt` → `327`.
- **FC-11 — one dollar sign, in an identifier.** `grep -n 'UserResource\$UriData' corpus/source-snapshots/round-35/S052.txt | cut -d: -f1` → `11954`.
- **FC-12 — the live directive page still says what the Scope note quotes.** `curl -sSL -A 'kasegi-shokunin/1.0 (documentation capture)' https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk | python3 -c 'import sys,re,html;t=sys.stdin.read();t=re.sub(r"<(script|style)\b.*?</\1>"," ",t,flags=re.I|re.S);t=re.sub(r"<[^>]+>"," ",t);t=html.unescape(t);n=" ".join(t.split());print("revoked",n.count("BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Revoked)"),"compulsory",n.count("A Binding Operational Directive is a compulsory direction to federal, executive branch, departments, and agencies"),"three_days",n.count("within the timeline (three days)"),"evolves",n.count("This Directive evolves upon CISA"))'` → `revoked 1 compulsory 1 three_days 1 evolves 1` (a network check, unlike the pinned S052 assertions).
- **FC-13 — every manifest anchor holds its quote.** `python3 -c 'import json;m=json.load(open("corpus/source-snapshots/round-35/manifest.json"));r=m["sources"][0];c=open("corpus/source-snapshots/round-35/S052.txt").read().splitlines();norm=lambda s:" ".join(s.split());ok=sum(norm(q["quote"]) in norm(" ".join(c[max(0,q["anchor"]-1):q["anchor"]+3])) for q in r["quotes"]);print("anchors_ok",ok,"of",len(r["quotes"]))'` → `anchors_ok 5 of 5`; a retargeted anchor on an exactly-once quote still passes `source-recheck` (its anchor limb is fatal only when `occurrences>1`), so this check is what keeps the entry's cited L15472 and L19165 honest.

## Rejected over-generalizations

1. **"KEV membership is a CVSS severity band."** Rejected: `cvss` 0, no score/severity/risk key (Claim 5); the feed carries no severity number, so a high score is not the same signal as a listing.
2. **"The capture defines 'known exploited'."** Rejected: the only descriptive text is the title (L2) and no field records exploitation evidence; quoting a definition against S052 would cite text that is not there.
3. **"dueDate is a deadline for every reader."** Rejected: the capture's one addressee sentence names FCEB agencies (L5423), and the deadline sits in CISA's `requiredAction` field; the directive documents are absent, so force beyond that text is unasserted.
4. **"1,756 is the number of known-exploited vulnerabilities in existence."** Rejected: it is the declared `count` for catalog version 2026.10.23 at a dated release (FC-1), not a population estimate.
5. **"Unknown ransomware use means no ransomware use."** Rejected: the field is two-valued Known/Unknown (361/1,395) and the capture states no meaning for Unknown; absence of the flag is not evidence of absence.
6. **"KEV is a payout ladder."** Rejected: no reward, bounty or currency vocabulary (FC-8); F13 and F17 carry price structures, this feed carries a deadline.

## Scope and limits

- Pin: `corpus/source-snapshots/round-35/S052.txt` (1,479,694 bytes, 27,870 lines, sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`), bound by `corpus/source-snapshots/round-35/manifest.json` (record S052: same digest, the feed URL, `fetched_utc` 2026-10-26T06:32:40Z, and the five Q1-Q5 assertions quoted above). The capture was fetched by `corpus/instruments/capture-source.py --id S052 --kind text` (the JSON body must not pass through the HTML converter's entity decoding).
- **Two quoted strings are deliberately outside the manifest.** The FCEB deadline sentence (2 occurrences) and the BOD 22-01 sentence (327) cannot be exactly-once, so they are anchored in this entry and counted by FC-9/FC-10 instead of being manifest assertions; every manifest assertion is `occurrences=1`.
- **Three assertions are whitespace-normalized across line breaks.** Q3, Q4 and Q5 each span consecutive source lines; the instrument prints `normalized=markup-whitespace occurrences=1 anchor=N-ok` for them, and Q1/Q2 match raw.
- **Directive status: a live-page note, not an admitted claim (Q2).** CISA's Binding Operational Directive 26-04 page, https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk, read 2026-10-26 (HTTP 200, text/html, 84,350 bytes), lists "BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Revoked)" under "Related Directives" (extraction L208), describes itself as "A Binding Operational Directive is a compulsory direction to federal, executive branch, departments, and agencies" (introduction, L92), and names three days only for the "& forensic triage" case (Appendix A, L179). The page has no registry row and no capture in this lane, so these are a dated live read: **no claim above rests on them**, and FC-12 re-fetches the page. Registering a row plus capture is the repair that would let a later round admit the statement under Q2.
- `verified-at: 2026-10-26` is when this entry was written and its quotes checked against the pin, not the capture instant.
- Documentation only: the capture carries no credential, session or private URL, and this entry quotes no such line (Q6). Nothing here authorizes probing, scanning, login, or submission against any target.
