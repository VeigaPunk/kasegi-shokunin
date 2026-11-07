#!/usr/bin/env python3
"""probe-skill-anchor-drift.py — Cross-axis audit of anchor-content-drift in SKILL.md.

Applies the C1 M8 content proxy (reproduced from knowledge-meter.py) to all
corpus/knowledge/*.md line-anchor citations in kasegi SKILL.md.

Outputs detailed classification:
  - Valid & Content-Passing
  - Anchor-Content-Drift (shares no identifier)
  - Anchor-Out-Of-Range
"""
import os
import re
import sys

KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{4,}")
PATHLIKE = re.compile(r"^[\w./~-]+\.(?:md|mjs|js|py|json|jsonl|txt|tsv|sh)(?::[\d,-]+)?$")

def idents(line):
    """Extract backtick and double-quoted identifiers from a line, ignoring path-like tokens."""
    spans = re.findall(r"`([^`]+)`", line) + re.findall(r'"([^"]+)"', line)
    out = set()
    for sp in spans:
        if PATHLIKE.match(sp.strip()):
            continue
        out |= set(WORD.findall(sp))
    return out

def run_probe(lane_root):
    skill_file = os.path.join(lane_root, "SKILL.md")
    k_dir = os.path.join(lane_root, "corpus", "knowledge")
    
    with open(skill_file, "r", encoding="utf-8") as fh:
        skill_lines = fh.readlines()
        
    k_files = {}
    for fn in sorted(os.listdir(k_dir)):
        if fn.endswith(".md"):
            with open(os.path.join(k_dir, fn), "r", encoding="utf-8") as fh:
                k_files[fn] = fh.read().splitlines()
                
    tok_pat = re.compile(r"`([^`\n]+)`")
    
    anchored = []
    for idx, line in enumerate(skill_lines, 1):
        for m in tok_pat.finditer(line):
            tok = m.group(1).strip().rstrip(".,;:")
            if tok.startswith("corpus/knowledge/"):
                rest = tok[len("corpus/knowledge/"):]
                km = KEY.match(rest)
                if km and km.group(2) is not None:
                    anchored.append({
                        "line_no": idx,
                        "line_text": line.strip(),
                        "token": tok,
                        "k_fn": km.group(1),
                        "lo": int(km.group(2)),
                        "hi": int(km.group(3) or km.group(2)),
                        "kind": "canonical-backtick",
                    })
            else:
                km = KEY.match(tok)
                if km and km.group(1) in k_files and km.group(2) is not None:
                    anchored.append({
                        "line_no": idx,
                        "line_text": line.strip(),
                        "token": tok,
                        "k_fn": km.group(1),
                        "lo": int(km.group(2)),
                        "hi": int(km.group(3) or km.group(2)),
                        "kind": "bare-backtick",
                    })
                    
    # Also evaluate the parenthesized multi-anchor format in SKILL.md:472-473
    vdp_ranges = [
        (472, "corpus/knowledge/vdp-disclosure-packages.md", 3, 5),
        (472, "corpus/knowledge/vdp-disclosure-packages.md", 9, 9),
        (472, "corpus/knowledge/vdp-disclosure-packages.md", 13, 16),
        (472, "corpus/knowledge/vdp-disclosure-packages.md", 20, 20),
        (473, "corpus/knowledge/vdp-disclosure-packages.md", 22, 31),
    ]
    for lno, kfn, lo, hi in vdp_ranges:
        anchored.append({
            "line_no": lno,
            "line_text": skill_lines[lno - 1].strip(),
            "token": f"{kfn}:{lo}-{hi}" if lo != hi else f"{kfn}:{lo}",
            "k_fn": os.path.basename(kfn),
            "lo": lo,
            "hi": hi,
            "kind": "parenthesized-subanchor",
        })

    passing = []
    drifting = []
    out_of_bounds = []

    for item in anchored:
        k_fn = item["k_fn"]
        if k_fn not in k_files:
            continue
        tgt_lines = k_files[k_fn]
        n_lines = len(tgt_lines)
        lo, hi = item["lo"], item["hi"]
        if not (1 <= lo <= hi <= n_lines):
            out_of_bounds.append(item)
            continue
        tw = set(WORD.findall("\n".join(tgt_lines[lo - 1:hi])))
        c_ids = idents(item["line_text"])
        shared = c_ids & tw
        item["shared"] = shared
        item["c_ids"] = c_ids
        item["tw"] = tw
        item["tgt_snippet"] = tgt_lines[lo - 1:hi]
        if shared:
            passing.append(item)
        else:
            drifting.append(item)

    print("================================================================================")
    print("SKILL.md KNOWLEDGE CITATION ANCHOR DRIFT AUDIT (M8 CONTENT PROXY)")
    print("================================================================================")
    print(f"Total anchored citations inspected: {len(anchored)}")
    print(f"  - Canonical backticked citations : {sum(1 for x in anchored if x['kind'] == 'canonical-backtick')}")
    print(f"  - Parenthesized sub-anchors      : {sum(1 for x in anchored if x['kind'] == 'parenthesized-subanchor')}")
    print(f"Passing M8 content proxy           : {len(passing)}")
    print(f"Failing M8 (anchor-content-drift)  : {len(drifting)}")
    print(f"Out of line-range                  : {len(out_of_bounds)}")
    print("--------------------------------------------------------------------------------")
    canon_drift = sum(1 for x in drifting if x['kind'] == 'canonical-backtick')
    print(f"Drift rate (canonical backticked)  : {canon_drift} / 7 ({canon_drift/7.0:.1%})")
    print(f"Drift rate (all citations)         : {len(drifting)} / {len(anchored)} ({len(drifting)/float(len(anchored)):.1%})")
    print("================================================================================\n")

    print("=== PASSING CITATIONS (IDENTIFIERS MATCH) ===")
    for p in passing:
        print(f"PASS [line {p['line_no']}] `{p['token']}`")
        print(f"     Shared identifiers : {sorted(p['shared'])}")
        print(f"     Citing text snippet: {p['line_text'][:100]}...\n")

    print("=== FAILING CITATIONS (ANCHOR-CONTENT-DRIFT) ===")
    for d in drifting:
        print(f"DRIFT [line {d['line_no']}] `{d['token']}` ({d['kind']})")
        print(f"      Citing text        : {d['line_text']}")
        print(f"      Citing idents      : {sorted(d['c_ids'])}")
        print(f"      Target words       : {sorted(list(d['tw'])[:10])}...")
        print(f"      Target lines {d['lo']}-{d['hi']}:")
        for idx, tline in enumerate(d['tgt_snippet'], d['lo']):
            print(f"        {d['k_fn']}:{idx}: {tline}")
        print()

if __name__ == "__main__":
    lane = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
    run_probe(lane)
