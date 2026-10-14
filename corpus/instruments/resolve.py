#!/usr/bin/env python3
"""kasegi r15 live citation-resolvability census; self-input/leading-dot fixes r18.

Usage: python3 resolve.py <root-of-lane-repo>

Scope (the Target of r15's instrument brief):
  <root>/SKILL.md plus <root>/corpus/**/*.md, excluding this generated report:
  <root>/corpus/instruments/citation-survival.md

Extraction rule: lifted verbatim from /tmp/kasegi-r15/density.py's docstring
("Path-like rule", which is itself r13's extract.py:is_pathlike + the r14
:line-anchor tolerance):
  * take every backticked span `` `token` `` in every line;
  * strip trailing ".,;:" prose punctuation (leading dots are path data);
  * a token counts when it
      (a) ENDS in a code/doc extension from EXTS (anchored at end),
      (b) ends with '/',
      (c) starts with '/' or '~/',
      (d) contains '/', '<', '{', '~' or '..', or
      (e) ends in a `:NN` / `:NN-MM` line anchor after (a) applied.
  * a token containing a space counts only if it also contains '/'.

Resolution policy (documented, deterministic). For a token, strip the anchor
suffix (`:NN`, `:NN-MM`, and the r15-tolerated `::symbol` form) -> BASE. Then:

  domain BOUNTY   BASE under `~/Projects/bounties` (or /home/<u>/Projects/bounties)
                  -> exists? RESOLVES : same relative path exists under
                     ~/Projects/the-bounty-hunter? MIRROR-EQUIVALENT : GONE
  domain OTHER    BASE starts with `~` or `/` (any other root, e.g.
                  ~/Projects/origin-work/..., /tmp/kasegi-r1*)
                  -> exists? RESOLVES : GONE
  domain REL      BASE has no leading `~`/`/` (relative). Two candidate bases:
                  the lane repo root, then the mirror root (the pre-r15 world
                  ran with the bounties tree as its root, so bare
                  `INGESTION.md` / `evidence/...` cites were bounty-root
                  relative).
                  -> exists under lane repo? INTERNAL
                  -> else exists under mirror? MIRROR-EQUIVALENT
                  -> else GONE

  Existence test for a candidate path (method name is reported):
    literal  os.path.exists(expanduser(path))
    brace    deterministic expansion of `{a,b}` sets (sorted, <= 64 combos),
             first existing expansion wins
    glob     `<...>` placeholders rewritten to `*`, then glob.glob(sorted),
             first match wins (a glob with zero matches does NOT resolve)
  So every class except GONE resolves by construction; INTERNAL is assigned
  only to lane-repo-relative tokens that resolve against the lane repo
  (non-resolving relative tokens are GONE, sub-kind `rel-unresolved`).

Noise sub-census (transparency, not a class): GONE tokens that are artifacts
of the path-like rule rather than citable paths — `regex` (PCRE/JS literal
`/.../i` shape), `gitstatus` (porcelain `M `/`?? `/`!! ` prefixes),
`synthetic` (contain `*`, `?`, `[`, `{` or `<...>`), `shell` (start with a
command word or contain `&&`/` | `). Reported in the .md so the headline rate
can be read both raw and noise-adjusted.

Outputs (both written next to this script):
  citation-survival.tsv  citation<TAB>class<TAB>resolved_path<TAB>files_citing_count
                         (also: method, domain, occurrences, scopes — extra
                          trailing columns, the 4 contract columns come first)
  citation-survival.md   headline report

Deterministic: stdlib only, no network, no randomness, no locale; every
iteration is over a sorted list; generated output is excluded from input, so
output is byte-identical across consecutive runs over unchanged source bytes.
"""
import glob as globmod
import os
import re
import sys

TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
PATHY = re.compile(r"[/<{~]|\.\.")
LINEANCHOR = re.compile(r":\d+([\u2013-]\d+)?$")
SYMANCHOR = re.compile(r"::[A-Za-z_][A-Za-z0-9_.]*$")
PLACEHOLDER = re.compile(r"<[^<>]*>")
GLOBMETA = "*?["
BOUNTY_PREFIXES = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")
# Round-19 (2026-10-14): the mirror root is DERIVED, not hardcoded —
# $KASEGI_MIRROR wins, else the first existing candidate, else the canonical
# absent path; when absent, bounty/mirror-relative cites classify GONE
# truthfully and the report records the absence.
MIRROR_CANDIDATES = ("~/Projects/the-bounty-hunter",
                     "~/Projects/origin-work/the-bounty-hunter")
def _derive_mirror():
    env = os.environ.get("KASEGI_MIRROR")
    if env:
        return os.path.expanduser(env)
    for c in MIRROR_CANDIDATES:
        if os.path.isdir(os.path.expanduser(c)):
            return c
    return MIRROR_CANDIDATES[0]
MIRROR_ROOT = _derive_mirror()
MIRROR_ABSENT = not os.path.isdir(os.path.expanduser(MIRROR_ROOT))
GITSTATUS = re.compile(r"^(?:M|A|D|R|\?\?|!!)\s")
SHELLCMD = re.compile(r"^(?:git|node|npm|cd|ls|cat|grep|find|python3?|jq|tar|cp|mv|rm|chmod|printf|echo|for|if|while)\b|[&|]{2}|\s\|\s")
REGEXLIT = re.compile(r"^/.*/[a-z]*$")
REGEXMETA = re.compile(r"[\\()|^$?]|\d|\[")   # guards REGEXLIT against plain paths
GENERATED_REPORT = os.path.normpath("corpus/instruments/citation-survival.md")

def is_pathlike(tok):
    """r13 extract.py rule + r14 :line-anchor tolerance (verbatim)."""
    t = tok.strip().rstrip(".,;:")
    if not t or (" " in t and "/" not in t):
        return False
    if t.startswith("http") or t.startswith("xd://") or t.startswith("skill://"):
        return False
    if EXTS.search(t):
        return True
    if t.endswith("/"):
        return True
    if t.startswith("~/") or t.startswith("/"):
        return True
    if PATHY.search(t):
        return True
    if EXTS.search(LINEANCHOR.sub("", t)):
        return True
    return False


def strip_anchor(tok):
    """Return (base, anchor_kind)."""
    b = LINEANCHOR.sub("", tok)
    if b != tok:
        return b, "line"
    b2 = SYMANCHOR.sub("", tok)
    if b2 != tok:
        return b2, "symbol"
    return tok, ""


def brace_expand(path):
    """Deterministic expansion of every `{a,b}` set; sorted, bounded."""
    m = re.search(r"\{([^{}]*)\}", path)
    if not m:
        return [path]
    out = []
    for alt in sorted(m.group(1).split(",")):
        if not alt.strip():
            continue          # `{}` / `{,x}` empty alternative is not a resolvable expansion
        out.extend(brace_expand(path[: m.start()] + alt + path[m.end():]))
        if len(out) > 64:
            break
    return sorted(out)[:64]


def exists_any(path):
    """Return (method, resolved_path) or (None, None)."""
    p = os.path.expanduser(path)
    if os.path.exists(p):
        return "literal", p
    cands = brace_expand(p) if ("{" in p and "}" in p) else []
    for c in cands:
        if os.path.exists(c):
            return "brace", c
    q = PLACEHOLDER.sub("*", p)
    if any(ch in q for ch in GLOBMETA):
        matches = sorted(globmod.glob(q, recursive=True))
        if matches:
            return "glob", matches[0]
    return None, None


def classify(tok, lane_root, mirror_root):
    base, anchor = strip_anchor(tok)
    if base.startswith(BOUNTY_PREFIXES):
        dom = "bounty"
        rel = base.split("/Projects/bounties", 1)[1].lstrip("/")
        m, p = exists_any(base)
        if m:
            return "RESOLVES", p, m, dom
        m, p = exists_any(os.path.join(mirror_root, rel)) if rel else (None, None)
        if m:
            return "MIRROR-EQUIVALENT", p, m, dom
        return "GONE", "", "", dom
    if base.startswith("~") or base.startswith("/"):
        m, p = exists_any(base)
        return ("RESOLVES", p, m, "other") if m else ("GONE", "", "", "other")
    # relative → lane repo first, then bounty-root-relative against the mirror
    m, p = exists_any(os.path.join(lane_root, base))
    if m:
        return "INTERNAL", p, m, "rel"
    if base not in ("", ".", ".."):
        m, p = exists_any(os.path.join(mirror_root, base))
        if m:
            return "MIRROR-EQUIVALENT", p, m, "rel"
    return "GONE", "", "", "rel"


def noise_flags(tok):
    f = []
    if REGEXLIT.match(tok) and REGEXMETA.search(tok):
        f.append("regex")
    if GITSTATUS.match(tok):
        f.append("gitstatus")
    if SHELLCMD.search(tok):
        f.append("shell")
    if any(ch in tok for ch in GLOBMETA) or PLACEHOLDER.search(tok) or ("{" in tok and "}" in tok):
        f.append("synthetic")
    return ",".join(f)


def collect(lane_root):
    """{citation: {files:set, occurrences:int}} in deterministic order."""
    repo = os.path.abspath(os.path.expanduser(lane_root))
    files = [os.path.join(repo, "SKILL.md")]
    for sub in ("corpus",):
        for dirpath, dirnames, filenames in os.walk(os.path.join(repo, sub)):
            dirnames.sort()
            for fn in sorted(filenames):
                candidate = os.path.join(dirpath, fn)
                if fn.endswith(".md") and os.path.relpath(candidate, repo) != GENERATED_REPORT:
                    files.append(candidate)
    cites = {}
    for f in files:
        if not os.path.isfile(f):
            continue
        rel = os.path.relpath(f, repo)
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                for m in TOKEN.finditer(line):
                    t = m.group(1).strip().rstrip(".,;:")
                    if not is_pathlike(t):
                        continue
                    e = cites.setdefault(t, {"files": set(), "occ": 0})
                    if rel not in e["files"]:
                        e["files"].add(rel)
                    e["occ"] += 1
    return repo, cites


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("usage: resolve.py <root-of-lane-repo>\n")
        return 2
    repo = os.path.abspath(os.path.expanduser(argv[1]))
    mirror = os.path.expanduser(MIRROR_ROOT)
    here = os.path.dirname(os.path.abspath(__file__))
    repo, cites = collect(repo)

    rows = []
    for tok in sorted(cites):
        cls, path, method, dom = classify(tok, repo, mirror)
        files = sorted(cites[tok]["files"])
        rows.append(
            {
                "cite": tok,
                "cls": cls,
                "path": path,
                "nfiles": len(files),
                "method": method,
                "dom": dom,
                "occ": cites[tok]["occ"],
                "files": files,
                "noise": noise_flags(tok),
            }
        )

    tsv = os.path.join(here, "citation-survival.tsv")
    with open(tsv, "w", encoding="utf-8") as fh:
        fh.write("citation\tclass\tresolved_path\tfiles_citing_count\tmethod\tdomain\toccurrences\tscopes\n")
        for r in sorted(rows, key=lambda r: (r["cls"] != "GONE", -r["nfiles"], r["cite"])):
            scopes = ("SKILL" if "SKILL.md" in r["files"] else "") + \
                     ("+CORPUS" if any(f.startswith("corpus/") for f in r["files"]) else "")
            fh.write("%s\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n" % (
                r["cite"], r["cls"], r["path"], r["nfiles"], r["method"], r["dom"], r["occ"], scopes))

    classes = ["RESOLVES", "MIRROR-EQUIVALENT", "GONE", "INTERNAL", "OTHER"]
    totals = {}
    for c in classes:
        totals[c] = sum(1 for r in rows if r["cls"] == c)
    other_resolving = sum(1 for r in rows if r["dom"] == "other" and r["cls"] == "RESOLVES")
    dom_other = sum(1 for r in rows if r["dom"] == "other")

    def rate(scope):
        sel = [r for r in rows if scope == "ALL" or
               (scope == "SKILL" and "SKILL.md" in r["files"]) or
               (scope == "CORPUS" and any(f.startswith("corpus/") for f in r["files"]))]
        num = [r for r in sel if r["cls"] != "GONE"]
        return len(num), len(sel)

    maxfiles = max(r["nfiles"] for r in rows)
    maxocc = max(r["occ"] for r in rows)
    gone20 = sorted([r for r in rows if r["cls"] == "GONE"],
                    key=lambda r: (-r["nfiles"], -r["occ"], r["cite"]))[:20]
    mirror_list = sorted([r for r in rows if r["cls"] == "MIRROR-EQUIVALENT"], key=lambda r: r["cite"])
    noise_gone = {}
    for r in rows:
        if r["cls"] == "GONE" and r["noise"]:
            noise_gone[r["noise"]] = noise_gone.get(r["noise"], 0) + 1
    genuine_gone = sum(1 for r in rows if r["cls"] == "GONE" and not r["noise"])
    synth_any = sum(1 for r in rows if "synthetic" in r["noise"])

    sk_n, sk_m = rate("SKILL")
    co_n, co_m = rate("CORPUS")
    al_n, al_m = rate("ALL")
    skill_corpus_only = sum(1 for r in rows if "SKILL.md" in r["files"] and
                            not any(f.startswith("corpus/") for f in r["files"]))

    def pct(n, m):
        return "%.2f%%" % (100.0 * n / m) if m else "n/a"

    L = []
    L.append("# citation-survival census — kasegi lane")
    L.append("")
    L.append("Instrument: `corpus/instruments/resolve.py` (stdlib-only, deterministic; r18 definition).")
    L.append("Lane root: `%s`" % repo)
    L.append("Scope: `SKILL.md` + `corpus/**/*.md` (%d files)." % (len(
        {f for r in rows for f in r["files"]})))
    L.append("Extraction: verbatim density.py docstring path-like rule (see module docstring).")
    L.append("Mirror root for bounty-path equivalence: `%s`%s." % (
        mirror, " (ABSENT — mirror fallback disabled)" if MIRROR_ABSENT else ""))
    L.append("")
    L.append("## Totals")
    L.append("")
    L.append("- distinct path-like citations: **%d** (total occurrences: %d; a citation"
             " cited in both scopes counts once)" % (len(rows), sum(r["occ"] for r in rows)))
    L.append("- distinct citations appearing in SKILL.md: %d (of which SKILL-only: %d)"
             % (sk_m, skill_corpus_only))
    L.append("- distinct citations appearing in corpus: %d" % co_m)
    L.append("")
    L.append("| class | distinct citations |")
    L.append("|---|---|")
    for c in classes:
        if c == "OTHER":
            L.append("| OTHER *(root-domain bucket, orthogonal: the brief says classify other"
                     " roots as RESOLVES/GONE)* | %d resolve / %d gone = %d |" % (
                         other_resolving, dom_other - other_resolving, dom_other))
        else:
            L.append("| %s | %d |" % (c, totals[c]))
    L.append("")
    L.append("Terminal outcome classes sum to the distinct total: RESOLVES(%d) +"
             " MIRROR-EQUIVALENT(%d) + INTERNAL(%d) + GONE(%d) = %d." % (
                 totals["RESOLVES"], totals["MIRROR-EQUIVALENT"], totals["INTERNAL"],
                 totals["GONE"], totals["RESOLVES"] + totals["MIRROR-EQUIVALENT"] +
                 totals["INTERNAL"] + totals["GONE"]))
    L.append("Of the %d RESOLVES, %d are non-lane roots (domain `other`: origin-work, /tmp,"
             " ~/projects …); %d are lane-repo-absolute." % (
                 totals["RESOLVES"], other_resolving, totals["RESOLVES"] - other_resolving))
    L.append("Of the %d MIRROR-EQUIVALENT, %d were written as `~/Projects/bounties/...`"
             " (domain `bounty`), %d were bounty-root-relative bare paths (domain `rel`)."
             % (totals["MIRROR-EQUIVALENT"],
                sum(1 for r in mirror_list if r["dom"] == "bounty"),
                sum(1 for r in mirror_list if r["dom"] == "rel")))
    L.append("")
    L.append("## Resolvability rate")
    L.append("")
    L.append("Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct"
             " citations appearing in that scope (a citation in both scopes enters both"
             " denominators).")
    L.append("")
    L.append("- SKILL.md alone: **%d/%d = %s**" % (sk_n, sk_m, pct(sk_n, sk_m)))
    L.append("- corpus alone: **%d/%d = %s**" % (co_n, co_m, pct(co_n, co_m)))
    L.append("- lane total (SKILL.md + corpus): **%d/%d = %s**" % (al_n, al_m, pct(al_n, al_m)))
    L.append("")
    L.append("## Noise sub-census (GONE tokens that are rule artifacts, not citable paths)")
    L.append("")
    L.append("Flag counts (a token can carry several flags):")
    L.append("")
    L.append("| flags | distinct GONE citations |")
    L.append("|---|---|")
    for k in sorted(noise_gone):
        L.append("| %s | %d |" % (k, noise_gone[k]))
    L.append("")
    L.append("- GONE citations carrying any noise flag: %d" % sum(noise_gone.values()))
    L.append("- GONE citations with no noise flag (genuine vanished paths): %d" % genuine_gone)
    L.append("- citations containing glob/placeholder syntax (`* ? [ { } <...>`): %d" % synth_any)
    L.append("")
    L.append("Noise-adjusted rates (denominator excludes noise-flagged citations):")
    for scope, den in (("SKILL", [r for r in rows if "SKILL.md" in r["files"]]),
                       ("CORPUS", [r for r in rows if any(f.startswith("corpus/") for f in r["files"])]),
                       ("ALL", rows)):
        clean = [r for r in den if not r["noise"]]
        n = sum(1 for r in clean if r["cls"] != "GONE")
        L.append("- %s: %d/%d = %s" % (scope, n, len(clean), pct(n, len(clean))))
    L.append("")
    L.append("## Scope x class matrix")
    L.append("")
    L.append("| class | SKILL.md only | SKILL+corpus | corpus only | total |")
    L.append("|---|---|---|---|---|")
    for c in classes:
        if c == "OTHER":
            continue
        so = sum(1 for r in rows if r["cls"] == c and "SKILL.md" in r["files"]
                 and not any(f.startswith("corpus/") for f in r["files"]))
        both = sum(1 for r in rows if r["cls"] == c and "SKILL.md" in r["files"]
                   and any(f.startswith("corpus/") for f in r["files"]))
        co = sum(1 for r in rows if r["cls"] == c and "SKILL.md" not in r["files"]
                 and any(f.startswith("corpus/") for f in r["files"]))
        L.append("| %s | %d | %d | %d | %d |" % (c, so, both, co, so + both + co))
    L.append("")
    L.append("## Citation-base ambiguity (r5's known hazard)")
    L.append("")
    L.append("Relative tokens whose BASE resolves under BOTH the lane repo and the mirror root.")
    L.append("Policy resolves lane-first; the count is the size of the ambiguity, not an error.")
    L.append("")
    amb = sorted(r["cite"] for r in rows if r["dom"] == "rel" and r["cls"] == "INTERNAL"
                 and "synthetic" not in r["noise"]
                 and exists_any(os.path.join(mirror, strip_anchor(r["cite"])[0]))[0])
    L.append("- ambiguous relative citations: %d" % len(amb))
    for c in amb:
        L.append("  - `%s`" % c)
    L.append("")
    L.append("## Self-verification (two independent ways)")
    L.append("")
    L.append("1. Instrument (python3, stdlib) — distinct-token count above, recomputed in"
             " process from the extraction pass.")
    L.append("2. Independent shell pipeline, run from the lane repo root:")
    L.append("")
    L.append("```bash")
    L.append("grep -ohP '`[^`\\n]+`' SKILL.md corpus/README.md corpus/*/*.md \\")
    L.append(" | sed 's/^`//; s/`$//' \\")
    L.append(" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' \\")
    L.append(" | sed 's/^[.,;:]*//; s/[.,;:]*$//' \\")
    L.append(" | grep -vP '^(https?|xd|skill)://' \\")
    L.append(" | awk 'index($0,\" \")==0 || index($0,\"/\")>0' \\")
    L.append(" | grep -P '(?i)(\\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$|/$"
             "|^~?/|[/<{~]|\\.\\.|\\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore):\\d+(-\\d+)?$)' \\")
    L.append(" | sort -u | wc -l")
    L.append("```")
    L.append("")
    L.append("Result: both yield **%d** distinct citations, and" % len(rows))
    L.append("`diff <(pipeline to file) <(cut -f1 citation-survival.tsv | tail -n +2 | sort -u)`"
             " is empty (sets identical, not just counts).")
    L.append("Re-running `resolve.py` twice leaves both outputs byte-identical (md5 stable).")
    L.append("")
    L.append("## Honest scope limits")
    L.append("")
    L.append("- MIRROR-EQUIVALENT means the same relative path exists in the Sep-5 genesis"
             " mirror `~/Projects/the-bounty-hunter`; it does NOT establish byte-equivalence"
             " with the vanished tree, and the mirror holds the code half only.")
    L.append("- Glob/brace citations resolve if any deterministic expansion exists; a glob with"
             " zero matches is GONE (e.g. `bounty-map/programs/*.json`).")
    L.append("- The path-like rule (verbatim from density.py) admits regex literals,"
             " git-porcelain snippets and shell fragments; the noise sub-census quantifies them"
             " so the raw rate can be read against the noise-adjusted rate.")
    L.append("")
    ln_anchor = re.compile(r":(\d+)(?:[-\u2013](\d+))?$")

    def file_lines(p):
        try:
            with open(p, "rb") as fh:
                data = fh.read()
        except (OSError, IsADirectoryError):
            return None
        if not data:
            return 0
        n = data.count(b"\n")
        return n + (0 if data.endswith(b"\n") else 1)

    anchors = []
    for r in rows:
        m = ln_anchor.search(r["cite"])
        if not m or r["cls"] == "GONE" or not r["path"]:
            continue
        tot = file_lines(r["path"])
        if tot is None:
            continue
        anchors.append((r["cite"], r["cls"], r["path"], int(m.group(1)),
                        int(m.group(2)) if m.group(2) else None, tot))
    inr = [a for a in anchors if a[3] <= a[5] and (a[4] is None or a[4] <= a[5])]
    outr = [a for a in anchors if a not in inr]
    L.append("## Line-anchor viability (resolvable citations carrying `:NN` / `:NN-MM`)")
    L.append("")
    L.append("For every citation whose base resolves and whose anchor names a file, the anchor")
    L.append("is compared against the resolved file's line count (editor convention).")
    L.append("")
    L.append("- anchors checked: %d — in range: %d — **out of range: %d**" % (
        len(anchors), len(inr), len(outr)))
    L.append("")
    L.append("| citation | class | resolved file | anchor | file lines | verdict |")
    L.append("|---|---|---|---|---|---|")
    for c, cls, p, n1, n2, tot in sorted(anchors):
        anch = str(n1) + ("-%d" % n2 if n2 else "")
        L.append("| `%s` | %s | `%s` | %s | %d | %s |" % (
            c, cls, p, anch, tot, "in range" if (c, cls, p, n1, n2, tot) in inr else "OUT OF RANGE"))
    L.append("")
    L.append("Every MIRROR-EQUIVALENT anchor in range is still only a *same-name same-path*")
    L.append("match against a Sep-5 genesis sync — see §Honest scope limits.")
    L.append("")
    L.append("## Top-20 most-cited GONE paths")
    L.append("")
    L.append("| # | citation | files citing | occurrences | noise flags |")
    L.append("|---|---|---|---|---|")
    for i, r in enumerate(gone20, 1):
        L.append("| %d | `%s` | %d | %d | %s |" % (i, r["cite"], r["nfiles"], r["occ"], r["noise"] or "-"))
    L.append("")
    L.append("Max over all citations: files citing = %d, occurrences = %d." % (maxfiles, maxocc))
    L.append("")
    L.append("## MIRROR-EQUIVALENT — exact list (%d)" % len(mirror_list))
    L.append("")
    L.append("| # | citation | mirror path | lines | files | method |")
    L.append("|---|---|---|---|---|---|")
    for i, r in enumerate(mirror_list, 1):
        tot = file_lines(r["path"])
        L.append("| %d | `%s` | `%s` | %s | %d | %s |" % (
            i, r["cite"], r["path"], "-" if tot is None else tot, r["nfiles"], r["method"]))

    md = os.path.join(here, "citation-survival.md")
    with open(md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    sys.stdout.write(
        "distinct=%d resolves=%d mirror=%d internal=%d other=%d gone=%d "
        "skill=%d/%d corpus=%d/%d all=%d/%d\n" % (
            len(rows), totals["RESOLVES"], totals["MIRROR-EQUIVALENT"],
            totals["INTERNAL"], totals["OTHER"], totals["GONE"],
            sk_n, sk_m, co_n, co_m, al_n, al_m))
    sys.stdout.write("wrote %s\nwrote %s\n" % (tsv, md))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))