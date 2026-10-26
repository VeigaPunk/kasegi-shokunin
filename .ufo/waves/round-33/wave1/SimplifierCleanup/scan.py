#!/usr/bin/env python3
"""Read-only scan of a wave evidence dir: sizes, duplicate digests, empty files,
scratch-path references, receipt command-evidence census. Never writes into the lane."""
import argparse, hashlib, json, os, re, sys

SCRATCH_RE = re.compile(rb"HYAKU_SCRATCH|/fast/scratch|/tmp/")
DOLLAR_RE = re.compile(rb"^\s*\$ ", re.M)
FENCE_RE = re.compile(rb"^```", re.M)
INDENTED_RE = re.compile(rb"^ {4,}\S", re.M)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                out.append((os.path.relpath(full, root), full, os.lstat(full).st_size, True))
                continue
            out.append((os.path.relpath(full, root), full, os.path.getsize(full), False))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--receipt-dir", default="wave1")
    ap.add_argument("--big", type=int, default=1024 * 1024)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    files = walk(root)

    rows = []
    for rel, full, size, is_link in files:
        digest = sha256(full) if not is_link else None
        rows.append({"path": rel, "bytes": size, "sha256": digest, "symlink": is_link})

    by_key = {}
    for r in rows:
        if r["sha256"]:
            by_key.setdefault(r["sha256"], []).append(r["path"])
    dups = {k: v for k, v in by_key.items() if len(v) > 1}

    receipt_dir = os.path.join(root, args.receipt_dir)
    recs = [r for r in rows if os.path.dirname(os.path.join(root, r["path"])) == receipt_dir
            and r["path"].endswith(".md")]

    refs = []
    for rel, full, size, is_link in files:
        if is_link or size == 0 or size > 8 * 1024 * 1024:
            continue
        try:
            with open(full, "rb") as f:
                blob = f.read()
        except OSError:
            continue
        hits = sorted({m.group(0).decode() for m in SCRATCH_RE.finditer(blob)})
        if hits:
            refs.append({"path": rel, "patterns": hits,
                         "is_receipt": os.path.dirname(os.path.join(root, rel)) == receipt_dir,
                         "lines": len([1 for ln in blob.splitlines() if SCRATCH_RE.search(ln)])})

    rec_detail = []
    for r in recs:
        full = os.path.join(root, r["path"])
        with open(full, "rb") as f:
            blob = f.read()
        dollar = len(DOLLAR_RE.findall(blob))
        fences = len(FENCE_RE.findall(blob)) // 2
        indented = len(INDENTED_RE.findall(blob))
        rec_detail.append({
            "path": r["path"], "bytes": r["bytes"], "sha256": r["sha256"],
            "dollar_cmd_lines": dollar, "fences": fences, "indented_code_lines": indented,
            "prose_only": fences == 0 and indented == 0 and dollar == 0,
        })

    dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        if dirpath == root:
            continue
        rel = os.path.relpath(dirpath, root)
        depth = rel.count(os.sep)
        if depth > 1:
            continue
        n = sum(len(fn) for _, _, fn in os.walk(dirpath))
        b = 0
        for dp, _, fns in os.walk(dirpath):
            for fn in fns:
                p = os.path.join(dp, fn)
                try:
                    b += os.lstat(p).st_size
                except OSError:
                    pass
        parent_files = len([f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))])
        dirs.append({"path": rel, "files": n, "bytes": b, "direct_files": parent_files})

    result = {
        "root": root,
        "files": len(rows),
        "bytes": sum(r["bytes"] for r in rows),
        "big": [r for r in rows if r["bytes"] > args.big],
        "empty": [r["path"] for r in rows if r["bytes"] == 0],
        "dups": dups,
        "scratch_refs": refs,
        "receipts": rec_detail,
        "dirs": dirs,
        "rows": rows,
    }
    if args.json:
        json.dump(result, sys.stdout, indent=1, sort_keys=True)
    else:
        print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
