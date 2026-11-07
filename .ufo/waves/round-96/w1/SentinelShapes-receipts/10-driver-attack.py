#!/usr/bin/env python3
"""Round-96 SentinelShapes: attack the seven landed GitLab shapes.

For each synthetic token (never a real credential) and each bypass class,
report HIT/MISS from the landed scanner and the same payload against S140's
published regex, so a MISS can be classified as scanner defect or
source-inherited limit.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
SCANNER = os.path.join(S, "scanner-7ef1d36.py")
S140 = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-94/S140.txt"

spec = importlib.util.spec_from_file_location("landed", SCANNER)
landed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(landed)
PATS = landed.patterns()
SHAPE_NAMES = [n for n, _ in PATS]

# --- S140's seven published rules (the source of the claim) -----------------
S140_IDS = {
    "gitlab_personal_access_token_routable": "gitlab-pat-routable",
    "gitlab_personal_access_token_routable_versioned": "gitlab-pat-versioned",
    "gitlab_runner_auth_token_routable": "gitlab-runner-auth-token-versioned",
    "gitlab_deploy_token_routable": "gitlab-deploy-token-versioned",
    "gitlab_kubernetes_agent_token_routable": "gitlab-agent-token-versioned",
    "gitlab_workspace_token": "gitlab-workspace-token-versioned",
    "gitlab_pipeline_trigger_token": "gitlab-pipeline-trigger-token",
}
text = open(S140, "rb").read().decode("utf-8")
s140 = {}
for m in re.finditer(r'id = "([^"]+)"\s*\n(?:keywords = \[[^\]]*\]\s*\n)?regex = \'\'\'(.*?)\'\'\'', text, re.S):
    rid, rx = m.group(1), m.group(2)
    if rid in S140_IDS:
        s140[S140_IDS[rid]] = re.compile(rx.encode())

# --- synthetic tokens (repeated letters; no real value) ---------------------
TOK = {
    "gitlab-pat-versioned": b"glpat-" + b"A" * 28 + b".de.fg1234567",
    "gitlab-pat-routable": b"glpat-" + b"B" * 28 + b".defg12345",
    "gitlab-runner-auth-token-versioned": b"glrtr-" + b"C" * 30 + b".ab.cd1234567",
    "gitlab-deploy-token-versioned": b"gldt-" + b"D" * 30 + b".ab.cd1234567",
    "gitlab-agent-token-versioned": b"glagent-" + b"E" * 30 + b".ab.cd1234567",
    "gitlab-workspace-token-versioned": b"glwt-" + b"F" * 30 + b".ab.cd1234567",
    "gitlab-pipeline-trigger-token": b"glptt-" + b"G" * 40,
}
TOK20 = {"gitlab-pipeline-trigger-token": b"glptt-" + b"H" * 20}


def head_len(tok):
    # prefix + '-' ; used to split inside the body for the line-wrap class
    return tok.index(b"-") + 1


def cases(shape, tok):
    """Return [(class, payload)] for one token."""
    h = head_len(tok)
    out = [
        ("baseline", b"t " + tok + b" end"),
        ("A1_entity_nosemi", b"q=a&#x26" + tok),
        ("A1_entity_semi_control", b"q=a&#x26;" + tok),
        ("A2_hex_escape", b"q=a\\x26" + tok),
        ("A3_dec_nosemi", b"q=a&#38" + tok),
        ("A3_dec_semi_control", b"q=a&#38;" + tok),
        ("A4_double_pct", b"q=a%2526" + tok),
        ("A4_double_amp_control", b"q=a&amp;amp;" + tok),
        ("B_wrap_lf", tok[: h + 10] + b"\n" + tok[h + 10:]),
        ("B_wrap_crlf", tok[: h + 10] + b"\r\n" + tok[h + 10:]),
        ("B_wrap_cont", tok[: h + 10] + b"\\\n" + tok[h + 10:]),
        ("C_left_alnum", b"x" + tok),
        ("C_right_alnum", tok + b"Z"),
        ("C_both_alnum", b"x" + tok + b"Z"),
        ("C_left_underscore", b"_" + tok),
        ("D_trailing_underscore", tok + b"_"),
        ("D_trailing_hyphen_control", tok + b"-"),
        ("E_query", b"https://h/p?token=" + tok + b"&x=1"),
        ("E_query_pct_eq", b"https://h/p?token%3D" + tok),
        ("E_query_frag", b"https://h/p?t=" + tok + b"#f"),
        ("G_prefix_20_control", b"R" * 20 + b"-" + tok),
        ("G_prefix_21", b"P" * 21 + b"-" + tok),
        ("G_prefix_30", b"Q" * 30 + b"-" + tok),
    ]
    if b"." in tok:
        out += [
            ("F_pct_dot_upper", tok.replace(b".", b"%2E")),
            ("F_pct_dot_lower", tok.replace(b".", b"%2e")),
            ("F_u002e_dot", tok.replace(b".", b"\\u002e")),
            ("F_html_dec_dot", tok.replace(b".", b"&#46;")),
            ("F_html_hex_dot", tok.replace(b".", b"&#x2e;")),
        ]
    return out


rows = []
for shape, tok in list(TOK.items()) + list(TOK20.items()):
    for cls, payload in cases(shape, tok):
        found = {s for s, _ in landed.scan_bytes(payload, PATS)[0]}
        s140hit = shape in s140 and bool(s140[shape].search(payload))
        rows.append({
            "shape": shape,
            "class": cls,
            "bytes_repr": payload.decode("latin-1"),
            "scanner_hit": shape in found,
            "scanner_shapes": sorted(found),
            "s140_hit": s140hit,
            "parity": (shape in found) == s140hit,
        })

# --- CLI end-to-end: one file per case, --files ------------------------------
casedir = os.path.join(S, "cases")
os.makedirs(casedir, exist_ok=True)
paths = []
for i, r in enumerate(rows):
    p = os.path.join(casedir, "c%03d.txt" % i)
    with open(p, "wb") as fh:
        fh.write(r["bytes_repr"].encode("latin-1"))
    paths.append(p)
cli = subprocess.run([sys.executable, "-B", SCANNER, "--files"] + paths,
                     capture_output=True, text=True)
cli_hits = {}
for m in re.finditer(r"HIT shape=([a-z0-9-]+) path=(\S+) line=(\d+)", cli.stdout):
    cli_hits.setdefault(os.path.basename(m.group(2)), set()).add(m.group(1))
for i, r in enumerate(rows):
    got = cli_hits.get("c%03d.txt" % i, set())
    r["cli_hit"] = r["shape"] in got
    r["cli_shapes"] = sorted(got)
    r["cli_agrees"] = r["cli_hit"] == r["scanner_hit"]

print("%-42s %-26s %-5s %-5s %-6s %-5s %s" % ("shape", "class", "scan", "s140", "parity", "cli", "other"))
for r in rows:
    other = [s for s in r["scanner_shapes"] if s != r["shape"]]
    print("%-42s %-26s %-5s %-5s %-6s %-5s %s" % (
        r["shape"], r["class"], "HIT" if r["scanner_hit"] else "MISS",
        "HIT" if r["s140_hit"] else "MISS", "ok" if r["parity"] else "DIFF",
        "HIT" if r["cli_hit"] else "MISS", ",".join(other) or "-"))

summary = {
    "scanner_sha256": __import__("hashlib").sha256(open(SCANNER, "rb").read()).hexdigest(),
    "rows": len(rows),
    "parity_diffs": [r for r in rows if not r["parity"]],
    "cli_disagreements": [r for r in rows if not r["cli_agrees"]],
    "misses": [r for r in rows if not r["scanner_hit"]],
    "s140_misses": [r for r in rows if not r["s140_hit"]],
}
with open(os.path.join(S, "attack.json"), "w") as fh:
    json.dump({"summary": {k: v for k, v in summary.items() if k != "rows"}, "rows": rows}, fh, indent=1)
print("\nPARITY_DIFFS=%d CLI_DISAGREEMENTS=%d MISSES=%d S140_MISSES=%d" % (
    len(summary["parity_diffs"]), len(summary["cli_disagreements"]),
    len(summary["misses"]), len(summary["s140_misses"])))
print("CLI_RC=%d" % cli.returncode)
