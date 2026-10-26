#!/usr/bin/env python3
"""Build the three junk-variant fixture lanes for CritC2Junk (round 40).

varA: all nine queued rows flipped to `rejected` with no flip text, no entries,
       no captures, no F23 (the shipped junk control junk-decisions.md shape).
varB: four rows `mined` with dummy knowledge entries and NO captures/manifest;
       five rows `rejected` with reason+flip text; no F23.
varC: four rows `mined` with fully fabricated-but-coherent captures (self-authored
       capture bytes + manifest sha256 + quotes), five rows `rejected` with
       reason+flip text, F23 + S060 opened with a fabricated capture.
"""
import hashlib
import json
import os
import re
import shutil

S = "/fast/scratch/hyaku/kasegi-r40/CritC2Junk"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
NINE = ["S016", "S017", "S019", "S020", "S021", "S022", "S023", "S024", "S025"]
MINED4 = ["S016", "S017", "S019", "S020"]

URLS = {
    "S016": "https://www.anthropic.com/coordinated-vulnerability-disclosure",
    "S017": "https://projectzero.google/2025/07/reporting-transparency.html",
    "S019": "https://csrc.nist.gov/pubs/sp/800/216/final",
    "S020": "https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline=",
    "S060": "https://cyclonedx.org/docs/1.7/json/",
}

QUOTES = {
    "S016": [("Q1", "Anthropic states that coordination begins after a report is triaged.", 5)],
    "S017": [("Q1", "Project Zero's reporting-transparency trial publishes some details before full disclosure.", 5)],
    "S019": [("Q1", "NIST SP 800-216 recommends formal intake and assessment procedures for federal VDPs.", 5)],
    "S020": [("Q1", "The DOJ framework requires agencies to document authorized testing scope explicitly.", 5)],
    "S060": [
        ("Q1", "analysis.state enumerates six values from exploited to resolved across the CycloneDX reference.", 5),
        ("Q2", "analysis.justification carries nine not-affected labels in the JSON reference.", 10),
    ],
}

REJECT_TEACHES = {
    "S021": "REJECTED: directive-level policy, duplicated by the newer VDP guidance sweep; flip: a claim that BOD 20-01 is the current authority despite newer guidance",
    "S022": "REJECTED: superseded by S030 (current CNA rules 4.2.0+); flip: reopen only if the 4.2.x rules are withdrawn",
    "S023": "REJECTED: program-description page without a checkable process contract; flip: a ground needing CISA's own intake steps as evidence",
    "S024": "REJECTED: superseded by S029 (official EUR-Lex Article 14 text); flip: reopen only if the OJ text changes",
    "S025": "REJECTED: arXiv preprint, not a stable pinned venue; flip: a ground needing the CVE-Bench task definitions as evidence",
}


def read_rows(path):
    rows = {}
    lines = []
    for line in open(path, encoding="utf-8").read().splitlines():
        m = re.match(r"^\| ([A-Z]\d{3}) \|", line)
        if m:
            rows[m.group(1)] = line
        lines.append(line)
    return rows, lines


def cell(line, idx, value):
    cells = line.split("|")
    cells[idx] = " " + value + " "
    return "|".join(cells)


def set_status(line, status, teaches=None, usedby=None):
    line = cell(line, 8, status)
    if teaches is not None:
        line = cell(line, 7, teaches)
    if usedby is not None:
        line = cell(line, 11, usedby)
    return line


def patch_sources(variant):
    path = f"{S}/{variant}/kasegi-shokunin/corpus/SOURCES.md"
    rows, lines = read_rows(path)
    for sid in NINE:
        assert sid in rows, sid
    if variant == "varA":
        for sid in NINE:
            rows[sid] = set_status(rows[sid], "rejected")
    else:
        for sid in MINED4:
            rows[sid] = set_status(rows[sid], "mined",
                                   usedby=f"corpus/knowledge/junk-{sid.lower()}.md")
        for sid in REJECT_TEACHES:
            rows[sid] = set_status(rows[sid], "rejected", teaches=REJECT_TEACHES[sid])
    if variant == "varC":
        s060 = ("| S060 | CycloneDX v1.7 JSON Reference — analysis subtree (vulnerability analysis "
                "states and justifications) — https://cyclonedx.org/docs/1.7/json/ | spec | A | "
                "CycloneDX's own vulnerability analysis vocabulary: the six analysis states, the nine "
                "not-affected justifications and the response values | capture corpus/source-snapshots/"
                "round-40/S060.txt (20 lines; sha256 <HASH>) | supersedes S059 — scoped analysis-subtree "
                "capture of analysis.state and analysis.justification | mined | 2026-10-26 | on-release | "
                "corpus/knowledge/cyclonedx-analysis-subtree.md |")
        rows["S060"] = s060
    out = []
    for line in lines:
        m = re.match(r"^\| ([A-Z]\d{3}) \|", line)
        if m and m.group(1) in rows:
            out.append(rows[m.group(1)])
        else:
            out.append(line)
    # append S060 after the last registry row (search for the last S-id row line)
    if variant == "varC":
        # find index of the final row line
        last = max(i for i, l in enumerate(out) if re.match(r"^\| [A-Z]\d{3} \|", l))
        out.insert(last + 1, rows["S060"])
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


def capture_lines(sid, quotes):
    lines = []
    lines.append("# Captured source text (fabricated demonstration capture)")
    lines.append(f"Document: {sid}")
    lines.append(f"URL: {URLS[sid]}")
    lines.append("")
    placed = {}
    for n in range(1, 21):
        hit = [a for _qid, _q, a in quotes if a == n]
        if hit:
            for qid, q, anchor in quotes:
                if anchor == n:
                    placed[qid] = len(lines) + 1
                    lines.append(q)
        else:
            lines.append(f"Paragraph {n}: routine background text for {sid} that carries no quotable substance beyond the pinned sentences.")
    return lines, placed


def write_captures(variant):
    base = f"{S}/{variant}/kasegi-shokunin/corpus/source-snapshots/round-40"
    os.makedirs(base, exist_ok=True)
    records = []
    for sid in list(MINED4) + (["S060"] if variant == "varC" else []):
        quotes = QUOTES[sid]
        lines, placed = capture_lines(sid, quotes)
        text = "\n".join(lines) + "\n"
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        with open(f"{base}/{sid}.txt", "w", encoding="utf-8") as fh:
            fh.write(text)
        qlist = []
        for qid, q, anchor in quotes:
            actual = placed[qid]
            qlist.append({"id": qid, "quote": q, "anchor": actual,
                          "location": f"L{actual} of the committed capture"})
        records.append({
            "id": sid, "path": f"{sid}.txt", "url": URLS[sid],
            "capture_url": URLS[sid], "fetched_utc": "2026-10-26T20:00:00Z",
            "fetched_bytes": len(text), "snapshot_bytes": len(text), "lines": len(lines),
            "sha256": h, "snapshot_sha256": h, "raw_sha256": h, "raw_bytes": len(text),
            "tool": "corpus/instruments/capture-source.py html_to_text()",
            "normalized": "capture-source.py html_to_text(): HTML-strip, whitespace collapse",
            "http": {"status": 200, "content_type": "text/html; charset=utf-8",
                     "final_url": URLS[sid], "redirects": 0,
                     "user_agent": "kasegi-shokunin/1.0",
                     "fetched_utc": "2026-10-26T20:00:00Z",
                     "date": "Mon, 26 Oct 2026 20:00:00 GMT"},
            "quotes": qlist,
        })
    manifest = {
        "schema_version": 1,
        "purpose": "Round-40 demonstration manifest (fabricated)", "sources": records,
    }
    with open(f"{base}/manifest.json", "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
        fh.write("\n")
    return records


def write_knowledge(variant):
    base = f"{S}/{variant}/kasegi-shokunin/corpus/knowledge"
    for sid in MINED4:
        h = sha_of(sid, variant)
        body = (
            f"# Junk entry for {sid} (demonstration)\n\n"
            f"source: {sid} — {URLS[sid]} — capture corpus/source-snapshots/round-40/{sid}.txt "
            f"(20 lines; sha256 {h[:16]}…)\n"
            "verified-at: 2026-10-26\n"
            f"ground: {sid}\n"
            "recheck: python3 corpus/instruments/source-recheck.py --manifest "
            "corpus/source-snapshots/round-40/manifest.json "
            f"--source {sid}\n\n"
            "## Claim 1\n\n"
            f"> \"{QUOTES[sid][0][1]}\" — {sid}.txt:L5\n"
        )
        with open(f"{base}/junk-{sid.lower()}.md", "w", encoding="utf-8") as fh:
            fh.write(body)
    if variant == "varC":
        h = sha_of("S060", variant)
        body = (
            "# CycloneDX v1.7 JSON Reference — analysis subtree: analysis.state and analysis.justification "
            "enums, scoped to the vulnerability-analysis surface (F23)\n\n"
            f"source: S060 — {URLS['S060']} — capture corpus/source-snapshots/round-40/S060.txt "
            f"(20 lines; sha256 {h[:16]}…)\n"
            "verified-at: 2026-10-26\n"
            "ground: F23\n"
            "recheck: python3 corpus/instruments/source-recheck.py --manifest "
            "corpus/source-snapshots/round-40/manifest.json --source S060\n\n"
            "## Attribution\n\n"
            "The S060 capture pins the analysis subtree of the CycloneDX v1.7 JSON Reference.\n\n"
            "## Claim 1\n\n"
            f"> \"{QUOTES['S060'][0][1]}\" — S060.txt:L5\n\n"
            "## Claim 2\n\n"
            f"> \"{QUOTES['S060'][1][1]}\" — S060.txt:L10\n"
        )
        with open(f"{base}/cyclonedx-analysis-subtree.md", "w", encoding="utf-8") as fh:
            fh.write(body)


def sha_of(sid, variant):
    p = f"{S}/{variant}/kasegi-shokunin/corpus/source-snapshots/round-40/{sid}.txt"
    if os.path.isfile(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    return "0" * 64


def patch_readme(variant):
    if variant != "varC":
        return
    path = f"{S}/{variant}/kasegi-shokunin/corpus/README.md"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write("\n## Round-40 admission — coverage map row and Frontier F23 (appended 2026-10-26)\n\n")
        fh.write("| F23 | CycloneDX analysis subtree (v1.7 JSON Reference vulnerability-analysis states and "
                 "justifications) | admitted | knowledge/cyclonedx-analysis-subtree.md | S060 | Read the "
                 "analysis vocabulary scoped to the CycloneDX v1.7 JSON Reference analysis subtree: "
                 "analysis.state and analysis.justification are enums independent of CSAF/VEX "
                 "product-status categories. |\n")


def write_conf(variant):
    path = f"{S}/{variant}/shokunin.conf"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write('LANES="\nkasegi|kasegi-shokunin|fixture\n"\n')


def main():
    for variant in ("varA", "varB", "varC"):
        patch_sources(variant)
        write_conf(variant)
        patch_readme(variant)
        if variant == "varC":
            write_captures(variant)
            write_knowledge(variant)
        elif variant == "varB":
            write_knowledge(variant)
    print("done")


if __name__ == "__main__":
    main()
