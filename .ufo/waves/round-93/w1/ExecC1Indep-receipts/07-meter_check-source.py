#!/usr/bin/env python3
"""ExecC1Indep's own independent knowledge-meter reimplementation and
label-row byte checker. Written from the DOCUMENTED semantics (resolve.py
docstring extraction rule + classification domains; citation-bases.md).
No counter code imported."""
import csv
import glob as globmod
import os
import pathlib
import re
import sys

TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
LINEANCHOR = re.compile(r":\d+([\u2013-]\d+)?$")
SYMANCHOR = re.compile(r"::[A-Za-z_][A-Za-z0-9_.]*$")
PLACEHOLDER = re.compile(r"<[^<>]*>")
PATHY = re.compile(r"[/<{~]|\.\.")
BRACE = re.compile(r"\{([^{}]*)\}")
GLOBMETA = "*?["
BOUNTY = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")
MIRROR_ROOTS = ("~/Projects/the-bounty-hunter",
                "/home/vgpnk/Projects/the-bounty-hunter",
                "~/Projects/origin-work/the-bounty-hunter")
GITSTATUS = re.compile(r"^(?:M|A|D|R|\?\?|!!)\s")
SHELLCMD = re.compile(r"^(?:git|node|npm|cd|ls|cat|grep|find|python3?|jq|tar|cp|mv|rm|chmod|printf|echo|for|if|while)\b|[&|]{2}|\s\|\s")
REGEXLIT = re.compile(r"^/.*/[a-z]*$")
REGEXMETA = re.compile(r"[\\()|^$?]|\d|\[")  # guards REGEXLIT against plain paths


def strip_tail(tok):
    return tok.strip().rstrip(".,;:")


def counted_form(tok):
    t = strip_tail(tok)
    if not t or (" " in t and "/" not in t):
        return None
    if t.startswith("http") or t.startswith("xd://") or t.startswith("skill://"):
        return None
    if EXTS.search(t):
        return t
    if t.endswith("/"):
        return t
    if t.startswith("~/") or t.startswith("/"):
        return t
    if PATHY.search(t):
        return t
    if EXTS.search(LINEANCHOR.sub("", t)):
        return t
    return None


def base_of(t):
    b = LINEANCHOR.sub("", t, count=0) if LINEANCHOR.search(t) else t
    if SYMANCHOR.search(b):
        b = SYMANCHOR.sub("", b)
    return b


def brace_expand(path):
    m = BRACE.search(path)
    if not m:
        return [path]
    out = []
    alts = sorted(m.group(1).split(","))
    for alt in alts:
        if alt.strip() or (not alt and len(alts) > 1):
            out.extend(brace_expand(path[: m.start()] + alt + path[m.end():]))
        if len(out) > 64:
            break
    return sorted(out)[:64]


def path_exists(base):
    p = os.path.expanduser(base)
    if os.path.exists(p):
        return "literal"
    cands = brace_expand(p) if ("{" in p and "}" in p) else []
    for c in cands:
        if os.path.exists(c):
            return "brace"
    for c in cands:
        qc = PLACEHOLDER.sub("*", c)
        if any(ch in qc for ch in GLOBMETA):
            for hit in sorted(globmod.glob(qc, recursive=True)):
                if os.path.exists(hit):
                    return "brace-glob"
    q = PLACEHOLDER.sub("*", p)
    if any(ch in q for ch in GLOBMETA):
        for c in sorted(globmod.glob(q, recursive=True)):
            if os.path.exists(c):
                return "glob"
    return None


def classify(t, lane):
    b = base_of(t)
    if b.startswith("~") or b.startswith("/"):
        exp = os.path.expanduser
        for r in MIRROR_ROOTS:
            r, rb = exp(r), exp(r)
            if b == r or b == rb or b.startswith(r.rstrip("/") + "/") or b.startswith(rb.rstrip("/") + "/"):
                return "GONE"  # canonical mirror alias; mirror absent on host
        return "RESOLVES" if path_exists(b) else "GONE"
    for bp in BOUNTY:
        bp = os.path.expanduser(bp)
        if b == bp or b.startswith(bp + "/"):
            if path_exists(b):
                return "RESOLVES"
            return "GONE"  # mirror fallback; mirror absent on host
    if path_exists(os.path.join(lane, b)):
        return "INTERNAL"
    return "GONE"


def noise_kind(t):
    if REGEXLIT.match(t) and REGEXMETA.search(t):
        return "regex"
    if GITSTATUS.match(t):
        return "gitstatus"
    if any(ch in t for ch in GLOBMETA) or PLACEHOLDER.search(t) or BRACE.search(t):
        return "synthetic"
    if SHELLCMD.search(t):
        return "shell"
    return None


def measure(tree):
    lane = str(tree)
    counts = {"RESOLVES": 0, "INTERNAL": 0, "GONE": 0, "MIRROR-EQUIVALENT": 0}
    cls = {}
    noise = {}
    kb = pathlib.Path(tree) / "corpus" / "knowledge"
    for f in sorted(kb.rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in TOKEN.finditer(text):
            t = counted_form(m.group(1))
            if t is None:
                continue
            c = classify(t, lane)
            cls.setdefault(t, c)
            nk = noise_kind(t)
            if nk:
                noise.setdefault(t, nk)
    for t, c in cls.items():
        counts[c] += 1
    resolved = counts["RESOLVES"] + counts["INTERNAL"]
    gone = counts["GONE"] + counts["MIRROR-EQUIVALENT"]
    return {
        "resolved": resolved, "gone": gone, "total": len(cls),
        "by_class": counts, "cls": cls, "noise": noise,
        "noise_total": len(noise),
    }


def rows_from_labels(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        return list(rd)


def check_rows(base, after, labels):
    oks = []
    for r in labels:
        site, key, label, fix = r["line"], r["key"], r["label"], r["fix"]
        f, _, ln = site.rpartition(":")
        n = int(ln)
        bl = (pathlib.Path(base) / f).read_text(encoding="utf-8").splitlines()[n - 1]
        al = (pathlib.Path(after) / f).read_text(encoding="utf-8").splitlines()[n - 1]
        if label == "CORRECT":
            exp = bl
            detail = "unchanged"
        elif label == "cell-repair":
            assert fix.startswith("Replace cell with: "), site
            cell = fix[len("Replace cell with: "):]
            assert cell and "|" not in cell, site
            end = bl.rfind("|")
            start = bl.rfind("|", 0, end)
            exp = bl[:start + 1] + " " + cell + " |"
            detail = f"cell old={bl[start + 1:end].strip()[:48]!r}"
        else:
            exp = bl.replace(key, label, 1)
            detail = f"range {key}->{label}"
        ok = (exp == al)
        oks.append((site, key, label, ok, detail))
        print(f"ROW {'OK ' if ok else 'BAD'} {site} key={key} kind={label} expected==after={ok} {detail}")
    return oks


def main():
    base, after, labels_path = sys.argv[1], sys.argv[2], sys.argv[3]
    print("HOST mirror-present=", any(os.path.isdir(os.path.expanduser(r)) for r in MIRROR_ROOTS),
          "bounty-present=", any(os.path.exists(os.path.expanduser(b)) for b in BOUNTY),
          "KASEGI_MIRROR=", repr(os.environ.get("KASEGI_MIRROR")))
    labels = rows_from_labels(labels_path)
    print("== LABEL ROWS =", len(labels))
    oks = check_rows(base, after, labels)
    mb = measure(base)
    ma = measure(after)
    for name, m, want in (("base", mb, "1007/2001"), ("after", ma, "1009/2000")):
        got = f"{m['resolved']}/{m['total']}"
        print(f"METER {name}: resolved/total={got} gone={m['gone']} want={want} match={got == want}")
        print(f"  by_class={m['by_class']} noise_tokens={m['noise_total']} noise_adj_resolved/total={m['resolved']}/{m['total'] - m['noise_total']}")
    cb, ca = mb["cls"], ma["cls"]
    rem = {t: cb[t] for t in sorted(set(cb) - set(ca))}
    add = {t: ca[t] for t in sorted(set(ca) - set(cb))}
    flip = {t: (cb[t], ca[t]) for t in sorted(set(cb) & set(ca)) if cb[t] != ca[t]}
    print("== TOKEN-SET DIFF ==")
    print("removed:")
    for t, c in rem.items():
        print(f"  - [{c}] {t}")
    print("added:")
    for t, c in add.items():
        print(f"  + [{c}] {t}")
    print("class-flips:", flip if flip else "none")
    nflip = {t: (mb["noise"].get(t), ma["noise"].get(t)) for t in set(mb["noise"]) | set(ma["noise"]) if mb["noise"].get(t) != ma["noise"].get(t)}
    print("noise-flips:", nflip if nflip else "none")
    all_ok = all(o[3] for o in oks) and f"{mb['resolved']}/{mb['total']}" == "1007/2001" and f"{ma['resolved']}/{ma['total']}" == "1009/2000"
    print("OVERALL", "PASS" if all_ok else "MISMATCH")


if __name__ == "__main__":
    main()
