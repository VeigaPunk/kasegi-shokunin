#!/usr/bin/env python3
"""Single-transform mutants of the frozen B8 gate. Each mutant: (a) the gate's own
--selftest, (b) a 7-probe negative suite + 4 forgery negative probes the selftest lacks,
(c) two positive controls. Reports survivors of each suite."""
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MAN = os.path.join(LANE, "corpus/source-snapshots/round-81/manifest.json")
BASE = os.path.join(S, "gate.py")
SRC = open(BASE, encoding="utf-8").read()
MUT = os.path.join(S, "mutants")
os.makedirs(MUT, exist_ok=True)

NEG = [(os.path.join(S, p), MAN, LANE) for p in (
    "forgeries/f5_paraphrase_mislocated.md", "forgeries/f6_moved_line.md",
    "forgeries/f15_overlong_span.md", "forgeries/f16_repeat_one_pin.md",
)]
NEG += [(os.path.join(S, "probes", n + ".md"), MAN, LANE) for n in (
    "p_dump_unsectioned", "p_norule", "p_pins_outside_claims", "p_header_no_recheck",
    "p_header_other_sid", "p_header_no_verified", "p_header_late", "p_header_dash_missing",
    "p_header_verified_inline", "p_header_recheck_suffix", "p_claim_unnumbered",
    "p_empty_span_claims", "p_five_claims", "p_seven_claims", "p_rule_no_colon",
    "p_rule_midline", "p_rejected_midline", "p_span_casefold", "p_span_padded",
    "p_overlong_pin", "p_pin_fragment_claims", "p_span_case_variant_extra")]
SYN = os.path.join(S, "probes/syn_zero")
NEG.append((os.path.join(S, "probes/p_line_zero_syn.md"),
            os.path.join(SYN, "corpus/source-snapshots/r/manifest.json"), SYN))
POS = [os.path.join(S, "forgeries/f10_bare_no_prose.md"),
       os.path.join(S, "forgeries/f1_boilerplate.md"),
       os.path.join(S, "probes/p_claim_no_dash.md"),
       os.path.join(S, "probes/p_claim_zero_pad.md"),
       os.path.join(S, "probes/p_two_spans_on_line.md")]

T = [
    ("M01_overlong_neutered", "if len(t.split()) > 25", "if len(t.split()) > 999999"),
    ("M02_overlong_threshold_250", "if len(t.split()) > 25", "if len(t.split()) > 250"),
    ("M03_overlong_counts_chars", "if len(t.split()) > 25", "if len(t) > 25"),
    ("M04_mislocated_off",
     "if not (1 <= int(n) <= len(snapshot_lines) and t in snapshot_lines[int(n) - 1])",
     "if False"),
    ("M05_mislocated_whole_snapshot",
     "1 <= int(n) <= len(snapshot_lines) and t in snapshot_lines[int(n) - 1]",
     "1 <= int(n) and t in \"\".join(snapshot_lines)"),
    ("M06_mislocated_lowerbound_dropped",
     "1 <= int(n) <= len(snapshot_lines) and t in snapshot_lines[int(n) - 1]",
     "int(n) <= len(snapshot_lines) and t in snapshot_lines[int(n) - 1]"),
    ("M07_unpinned_off", "if not any(q in t for t in claim_spans)", "if False"),
    ("M08_unpinned_join", "any(q in t for t in claim_spans)", "any(q in \" \".join(claim_spans))"),
    ("M09_unpinned_reversed", "any(q in t for t in claim_spans)", "any(t in q for t in claim_spans)"),
    ("M10_claim_spans_from_all",
     "claim_spans.extend(t for t, _n in cs)", "claim_spans.extend(t for t, _n in spans)"),
    ("M11_claimless_dropped_from_ok", "and claimless == 0", ""),
    ("M12_claimless_spans_only", "if not (cs and re.search(r\"(?m)^Falsifiable rule:\", body)",
     "if not cs and not (cs and re.search(r\"(?m)^Falsifiable rule:\", body)"),
    ("M13_header_always_true", '    header = (any(l.startswith("source: %s \u2014 " % sid) for l in head)\n'
     '              and any(l.startswith("verified-at: ") for l in head)\n'
     '              and any(l == recheck for l in head))', "    header = True"),
    ("M14_header_window_80", "head = lines[:8]", "head = lines[:80]"),
    ("M15_header_source_prefix_only", 'l.startswith("source: %s \u2014 " % sid)',
     'l.startswith("source: ")'),
    ("M16_header_dash_dropped", 'l.startswith("source: %s \u2014 " % sid)',
     'l.startswith("source: %s " % sid)'),
    ("M17_header_verified_anywhere", 'l.startswith("verified-at: ")', '"verified-at:" in l'),
    ("M18_header_recheck_prefix", "any(l == recheck for l in head)",
     'any(l.startswith("recheck:") for l in head)'),
    ("M19_claims_le", "len(claims) == len(quotes)", "len(claims) <= len(quotes)"),
    ("M20_claims_ge", "len(claims) == len(quotes)", "len(claims) >= len(quotes)"),
    ("M21_claim_regex_loose", 're.match(r"Claim \\d+\\b", s)', 're.match(r"Claim", s)'),
    ("M22_claim_regex_requires_dash", 're.match(r"Claim \\d+\\b", s)',
     're.match(r"Claim \\d+ \u2014", s)'),
    ("M23_span_allows_empty", "SPAN_RE = r'\"([^\"\\n]+)\"", "SPAN_RE = r'\"([^\"\\n]*)\""),
    ("M24_span_any_line", "SPAN_RE = r'\"([^\"\\n]+)\"", "SPAN_RE = r'\"(.+)\""),
    ("M25_sid_not_escaped", "SPAN_RE % re.escape(sid)", "SPAN_RE % sid"),
    ("M26_line_match_casefold", "t in snapshot_lines[int(n) - 1]",
     "t.lower() in snapshot_lines[int(n) - 1].lower()"),
    ("M27_line_match_stripped", "t in snapshot_lines[int(n) - 1]",
     "t.strip() in snapshot_lines[int(n) - 1].strip()"),
    ("M28_rule_colon_optional", 're.search(r"(?m)^Falsifiable rule:", body)',
     're.search(r"(?m)^Falsifiable rule", body)'),
    ("M29_rule_anywhere", 're.search(r"(?m)^Falsifiable rule:", body)',
     're.search(r"Falsifiable rule:", body)'),
    ("M30_rejected_anywhere", 're.search(r"(?m)^Rejected over-generalization", body)',
     're.search(r"Rejected over-generalization", body)'),
    ("M31_spans_truthiness_dropped", "and spans and mislocated == 0", "and mislocated == 0"),
    ("M32_body_first_section_only", 'body = body.split("\\n## ")[0]', 'body = body'),
]


def run(gate, args, tmp):
    r = subprocess.run([sys.executable, gate] + args, capture_output=True, text=True,
                       env={**os.environ, "TMPDIR": tmp})
    return r.returncode, (r.stdout or "").strip()


rows = []
for name, old, new in T:
    if SRC.count(old) != 1:
        print("%-34s TRANSFORM-RESOLUTION-FAIL count=%d" % (name, SRC.count(old)))
        rows.append({"name": name, "status": "TRANSFORM-RESOLUTION-FAIL",
                     "count": SRC.count(old)})
        continue
    d = os.path.join(MUT, name)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "gate.py")
    open(p, "w", encoding="utf-8").write(SRC.replace(old, new, 1))
    rc_st, out_st = run(p, ["--selftest"], d)
    selftest = "KILLED" if rc_st != 0 else "SURVIVED"
    caught = []
    for probe, pman, plane in NEG:
        psid = "S9" if "syn_zero" in plane else "S115"
        rc, out = run(p, ["--entry", probe, "--manifest", pman, "--source", psid,
                          "--lane", plane], d)
        if rc == 0:
            caught.append(os.path.basename(probe)[:-3])
    posfail = []
    for pos in POS:
        rc, out = run(p, ["--entry", pos, "--manifest", MAN, "--source", "S115",
                          "--lane", LANE], d)
        if rc != 0:
            posfail.append(os.path.basename(pos)[:-3])
    print("%-34s selftest=%-8s probes_caught=%-2d pos_broken=%-6s %s" % (
        name, selftest, len(caught), ",".join(posfail) or "-", ",".join(caught) or "-"))
    rows.append({"name": name, "selftest": selftest, "caught_by": caught,
                 "positive_broken": posfail, "stdout": out_st})

# controls
rc, out = run(BASE, ["--selftest"], S)
print("%-34s base_selftest rc=%d %s" % ("BASE", rc, out.replace("\n", " ")))
for probe, pman, plane in NEG:
    psid = "S9" if "syn_zero" in plane else "S115"
    rc, out = run(BASE, ["--entry", probe, "--manifest", pman, "--source", psid,
                         "--lane", plane], S)
    print("   base neg %-28s rc=%d" % (os.path.basename(probe), rc))
for pos in POS:
    rc, out = run(BASE, ["--entry", pos, "--manifest", MAN, "--source", "S115",
                         "--lane", LANE], S)
    print("   base pos %-28s rc=%d" % (os.path.basename(pos), rc))

json.dump(rows, open(os.path.join(S, "mutants2.json"), "w"), indent=1)
print("SUMMARY transforms=%d selftest_killed=%d selftest_survived=%d "
      "undetected_by_any_probe=%d" % (
          len(rows), sum(1 for x in rows if x.get("selftest") == "KILLED"),
          sum(1 for x in rows if x.get("selftest") == "SURVIVED"),
          sum(1 for x in rows if x.get("selftest") == "SURVIVED" and not x.get("caught_by"))))
