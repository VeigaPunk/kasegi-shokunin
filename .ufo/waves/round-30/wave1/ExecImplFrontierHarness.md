# ExecImplFrontierHarness — round-30 wave-1, C1 limbs A1+A2

Seat: `ExecImplFrontierHarness` (L2 leaf, kasegi lane). Assignment: implement C1 limbs
A1+A2 in `corpus/instruments/frontier-recheck-count.py` (single owner), preserve all
existing behavior and CLI flags (`--root`, `--json`), update the module docstring to state
the new fail-closed behaviors, show the diff and new sha256, and demonstrate the A1/A2
fixtures from `.ufo/waves/round-30/c1-controls/`.

Write scope: `corpus/instruments/frontier-recheck-count.py` only. No other file was
written. No `git`/`jj` mutation, no tool installed (nothing was needed; no pacman
attempted per the host-wide pause). No live target contacted (fixtures are local).

## Instrument digests

- Before (claims-freeze bytes): `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261`
  (matches `.ufo/waves/round-30/c1-controls/before.txt`).
- After (landed working-tree bytes): `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`.

## Diff (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff corpus/instruments/frontier-recheck-count.py`)

```
diff --git i/corpus/instruments/frontier-recheck-count.py w/corpus/instruments/frontier-recheck-count.py
index af831d0..351fc2c 100755
--- i/corpus/instruments/frontier-recheck-count.py
+++ w/corpus/instruments/frontier-recheck-count.py
@@ -18,8 +18,18 @@ line to the entry it belongs to before it runs it:
   D. only then is the line executed, from the lane root, and its exit code is
      the entry's result.
 
-An entry passes only when A-D all hold and the line exits 0. Exit 0 when every
-admitted Frontier entry passes, 1 otherwise, 2 on a harness/read error.
+An entry passes only when A-D all hold and the line exits 0. The harness also
+fails closed before any line runs:
+
+  E. an admitted row whose entry file does not exist fails with a named-row
+     `missing-entry` problem (the row id and path are printed; never an
+     uncaught FileNotFoundError traceback);
+  F. two admitted rows resolving to the same entry realpath fail the run with
+     a `DUPLICATE-ENTRY` note naming the duplicate rows and the entry.
+
+Exit 0 when every admitted Frontier entry passes, 1 otherwise (any failing
+row, a missing entry, or a duplicate entry realpath), 2 on a harness/read
+error.
 
 This instrument measures recheck coverage only: a passing entry proves its
 pinned captures still hold its own assertions, not that the entry's claims are
@@ -56,11 +66,17 @@ def entry_contract(root, entry_path):
 
     `declared` is the header `source:` id set; `cited` is every S-id the entry's
     body mentions. The recheck must select a superset of the header ids (nothing
-    dropped) and a subset of the cited ids (no cross-entry credit)."""
+    dropped) and a subset of the cited ids (no cross-entry credit).
+
+    Returns None when the entry file exists under neither candidate path
+    (`root/<entry_path>` or the corpus-relative form); callers must treat None
+    as a fail-closed missing-entry outcome."""
     full = os.path.join(root, entry_path)
     if not os.path.isfile(full):
         # README rows name entries relative to corpus/ (`knowledge/...`).
         full = os.path.join(root, "corpus", entry_path)
+    if not os.path.isfile(full):
+        return None
     declared, cited, recheck, manifest = [], set(), "", None
     with open(full, encoding="utf-8") as fh:
         body = fh.read()
@@ -99,7 +115,24 @@ def manifest_ids(root, manifest):
 
 
 def evaluate(root, entry_path):
-    declared, cited, recheck, recheck_ids, manifest = entry_contract(root, entry_path)
+    contract = entry_contract(root, entry_path)
+    if contract is None:
+        return {
+            "entry": entry_path,
+            "declared_ids": [],
+            "cited_ids": [],
+            "recheck_ids": [],
+            "manifest": None,
+            "exit": None,
+            "realpath": None,
+            "problems": ["missing-entry"],
+            "status": "FAIL",
+        }
+    declared, cited, recheck, recheck_ids, manifest = contract
+    full = os.path.join(root, entry_path)
+    if not os.path.isfile(full):
+        full = os.path.join(root, "corpus", entry_path)
+    realpath = os.path.realpath(full)
     problems = []
     if not declared:
         problems.append("no-source-line")
@@ -133,6 +166,7 @@ def evaluate(root, entry_path):
         "cited_ids": cited,
         "recheck_ids": recheck_ids,
         "manifest": manifest,
+        "realpath": realpath,
         "exit": exit_code,
         "problems": problems,
         "status": "PASS" if not problems else "FAIL",
@@ -165,14 +199,29 @@ def main(argv=None):
                 "-" if record["exit"] is None else record["exit"],
                 (" problems=" + ",".join(record["problems"])) if record["problems"] else ""))
     passed = sum(1 for r in records if r["status"] == "PASS")
-    print("entries=%d pass=%d exit=%d" % (len(records), passed, 0 if passed == len(records) and records else 1))
+    duplicate = None
+    seen_realpath = {}
+    for record in records:
+        rp = record.get("realpath")
+        if rp is None:
+            continue
+        if rp in seen_realpath:
+            duplicate = (seen_realpath[rp], record["frontier"], record["entry"])
+            break
+        seen_realpath[rp] = record["frontier"]
+    if duplicate:
+        print("DUPLICATE-ENTRY %s,%s %s" % (duplicate[0], duplicate[1], duplicate[2]))
+    fail_closed = duplicate is not None or not records or passed != len(records)
+    print("entries=%d pass=%d exit=%d" % (len(records), passed, 1 if fail_closed else 0))
     if args.json:
         with open(args.json, "w", encoding="utf-8") as fh:
             json.dump({"schema": "kasegi-frontier-recheck-receipt-v1", "root": root,
-                       "entries": len(records), "pass": passed, "records": records},
+                       "entries": len(records), "pass": passed,
+                       "duplicate_entry": duplicate[2] if duplicate else None,
+                       "records": records},
                       fh, indent=2, sort_keys=True)
             fh.write("\n")
-    return 0 if records and passed == len(records) else 1
+    return 1 if fail_closed else 0
 
 
 if __name__ == "__main__":
```

## Fixture demonstration (committed controls, `.ufo/waves/round-30/c1-controls/`)

A1 — missing entry (`harness-root-a1`, row F98 names `knowledge/zz-missing.md`):

```
$ python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
$ echo "a1_exit=$?"
a1_exit=1
```

Names row id F98 and the path; no `FileNotFoundError` traceback; exit 1. (Before:
traceback, no named-row marker, `a1.err`.)

A2 — duplicate entry realpath (`harness-root-a2`, F98 and F97 both name
`knowledge/dup-entry.md`):

```
$ python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a2
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
$ echo "a2_exit=$?"
a2_exit=1
```

Names the duplicate rows and the entry; exit 1. (Before: `pass=2 exit=0` on the duplicate
target.)

`--json` receipts (both exits 1, receipts written):

- A1: `entries=1 pass=0 duplicate_entry=None first_problems=['missing-entry']`
- A2: `entries=2 pass=2 duplicate_entry='knowledge/dup-entry.md'`

## Real-corpus run at these bytes

```
$ python3 corpus/instruments/frontier-recheck-count.py
PASS F01..F13 (16 rows as before)
FAIL     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=-              exit=-    problems=missing-entry
entries=17 pass=16 exit=1
```

The lane README already carries the round-30 F14 admitted row, but the C2 entry file
`knowledge/japanese-severity-vocabulary-and-impact-model.md` is not yet on disk at this
wave's timestamp (landed by the peer C2 seat, whose scope that file is). The A1 limb
therefore fires on the live row — named row + path, exit 1 — which is the intended
fail-closed behavior, not a regression of the instrument. Once the C2 entry lands, the
harness returns to `pass=17 exit=0` as C2's kill rule expects. No other row regressed
(16/16 previously-admitted rows still PASS and exit 0 individually).

## Behavior preservation

- CLI flags unchanged: `--root` (default lane root) and `--json` both still work.
- Per-row print format, summary line shape, A-D contract checks, and exit semantics for
  all pre-existing outcomes are unchanged (exit 0 all pass, 1 any fail, 2 harness/read
  error). New exit-1 causes are additive: missing entry (A1) and duplicate entry realpath
  (A2).
- Only `frontier-recheck-count.py` changed; `source-recheck.py` and every other path
  untouched.

## Risks / notes

- The lane currently exits 1 solely because the F14 entry file is pending in the peer C2
  seat; this will close when that seat lands its file (C2 kill rule expects `entries=17
  pass=17 exit=0`).
- A2's duplicate check keys on `os.path.realpath` of the resolved entry file, so distinct
  rows pointing at the same file (including via symlink) fail; distinct files pass.
- No tool installed; no pacman transaction attempted.
