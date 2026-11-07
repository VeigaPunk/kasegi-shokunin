#!/usr/bin/env python3
"""Extra independent checks for CriticClaimsC2 (round 97): K5 row parse,
old-shape survival, kept-limit probes, redaction arithmetic, and the
deploy-token-URL hit at the pre-redaction revisions."""
import importlib.util
import subprocess

S = "/fast/scratch/hyaku/kasegi-r97/CriticClaimsC2"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"


def load(p, n):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


new = load(S + "/work-7001/inst-rev/corpus/instruments/capture-secret-scan.py", "n")
base = load(S + "/work-7001/inst-base/corpus/instruments/capture-secret-scan.py", "b")
OLD = {"github-token", "github-refresh-token", "gitlab-pat", "gitlab-jwt-token",
       "gitlab-runner-auth-token", "gitlab-deploy-token", "aws-access-key-id",
       "aws-sts-session-token", "gcs-signed-url-signature", "azure-sas-signature",
       "cloudfront-signed-url-signature", "cloudfront-signed-cookie-signature",
       "gitlab-pat-versioned", "gitlab-pat-routable",
       "gitlab-runner-auth-token-versioned", "gitlab-deploy-token-versioned",
       "gitlab-agent-token-versioned", "gitlab-workspace-token-versioned",
       "gitlab-pipeline-trigger-token"}
bn = {n for n, _ in base.patterns()}
nn = {n for n, _ in new.patterns()}
print("SHAPES base=%d new=%d added=%s removed=%s" % (
    len(bn), len(nn), sorted(nn - bn), sorted(bn - nn) or "none"))
print("OLD-SHAPES base=%d/%d new=%d/%d" % (
    len(OLD & bn), len(OLD), len(OLD & nn), len(OLD)))

dp = dict(new.patterns())
probes = {
    "glft-64hex-dash-digits": b"glft-" + b"0123456789abcdef" * 4 + b"-12345 ",
    "t1_-legacy-bare": b" t1_" + b"A" * 20 + b" ",
    "t1_-legacy-glrt": b"glrt-t1_" + b"A" * 20 + b" ",
    "trigger-pipeline-url": b"https://gitlab.com/api/v4/projects/1/trigger/pipeline?token=" + b"A" * 20 + b" ",
    "feed_token-19": b"?feed_token=" + b"B" * 19 + b"&",
    "glft-64hex-plain": b"glft-" + b"0123456789abcdef" * 4 + b" ",
}
for k, v in probes.items():
    got = sorted(n for n, rx in dp.items() if rx.search(v))
    print("PROBE %-24s shapes=%s" % (k, ",".join(got) or "none"))

# K5: SCORECARD row
land = "a9a53608dce6aea07d298bb9d5133532078eb1dd"
score = subprocess.run(["git", "-C", LANE, "show", land + ":SCORECARD.md"],
                       capture_output=True, text=True).stdout
lines = score.split("\n")
secs = [i for i, l in enumerate(lines) if l.startswith("## ")]
cap = [i for i in secs if lines[i].strip().lower().startswith("## capabilities")]
start = cap[0]
end = next((i for i in secs if i > start), len(lines))
rows = [(i, l) for i, l in enumerate(lines[start:end], start)
        if l.startswith("| `capture-secret-scan`") or l.startswith("| capture-secret-scan")]
allrows = [(i, l) for i, l in enumerate(lines)
           if l.startswith("| `capture-secret-scan`") or l.startswith("| capture-secret-scan")]
cells = [c.strip() for c in rows[0][1].rstrip().rstrip("|").split("|")]
NEW = ["gitlab-runner-registration-token", "gitlab-feed-token", "gitlab-oauth-app-secret",
       "gitlab-feed-token-v2", "gitlab-incoming-email-token", "gitlab-scim-oauth-token",
       "gitlab-deploy-token-in-url", "gitlab-feature-flags-client-token",
       "gitlab-runner-controller-token", "gitlab-kubernetes-agent-token"]
print("K5 capabilities-section=%s rows_in_section=%d rows_in_file=%d last_cell=%r named_all=%s named=%s"
      % ([i + 1 for i in cap], len(rows), len(allrows), cells[-1],
         all(s in rows[0][1] for s in NEW), {s: (s in rows[0][1]) for s in NEW}))

# redaction arithmetic on the 19 round-96 receipt files
rec = open(LANE + "/.ufo/waves/round-97/l1/redaction-r97.txt").read().split("\n")
files = [l.split()[0] for l in rec if l.startswith(".ufo/waves/round-96/w1/")]
base_rev = "b06af5e07efbd961a8449f7de6b57eeea62c6bd3"


def blob(rev, p):
    return subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, p)],
                          capture_output=True).stdout


allp = list(base.patterns())
tb = sum(sum(len(rx.findall(blob(base_rev, p))) for _, rx in allp) for p in files)
import re
mk = re.compile(rb"\[[a-z0-9-]+-fixture-redacted-r97\]")
tl = sum(len(mk.findall(blob(land, p))) for p in files)
tr = sum(sum(len(rx.findall(blob(land, p))) for _, rx in allp) for p in files)
print("REDACTION round96_files=%d base_shape_matches=%d landing_markers=%d landing_residual=%d"
      % (len(files), tb, tl, tr))

# deploy-token URL hit at pre-redaction revisions
rx = dp["gitlab-deploy-token-in-url"]
p = ".ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt"
for rev in ["7ef1d365eb523a83b2567342a6c0f585ab028ab0", base_rev, land]:
    d = blob(rev, p)
    hits = [(d.count(b"\n", 0, m.start()) + 1, len(m.group(0))) for m in rx.finditer(d)]
    print("DEPLOY-URL-FIXTURE rev=%s bytes=%d matches=%d line/length=%s" % (rev[:8], len(d), len(hits), hits))
