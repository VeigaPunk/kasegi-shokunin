# RecheckSafety — read-only snapshot tool review

**Axis/scope:** `depth:verifiability` safety boundary for the round-23 local-source recheck; frozen claims C2 and `corpus/QUALITY.md` Q7 require pinned captured-source verification, not fresh-network credit. Reviewed the unintegrated author draft `/tmp/kasegi-r23-RecheckSources-5/corpus/instruments/source-recheck.py` (author reports clone base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`). No production edits, tests, `--selftest`, or external requests were made. The private clone had no round-23 manifest at review time.

## Finding — LOW, conditional local TOCTOU read escape

**Exploit path:** A caller supplies a manifest under a writable local directory with a record path such as `snapshot.txt`; another local writer changes that in-root path to a symlink to an outside file after canonicalization but before the read. The check retains a pathname, not an opened file handle, so `read_bytes()` resolves the changed pathname again. The manifest's quote assertions can then act as a substring oracle, and a digest mismatch prints the outside file's SHA-256. This requires concurrent write access to the manifest directory and depends on the recheck process having permission to read the outside file; it is not an unauthenticated remote path.

**Evidence:** `source-recheck.py:99-106` resolves `base` and `(base / path)`, checks `os.path.commonpath(...)`, then separately calls `resolved.read_bytes()`. The static check correctly rejects ordinary `..` traversal and symlink escapes already present at `resolve()` time. `:114-117` emits actual digest on mismatch; `:127-132` emits per-quote presence results.

**Impact:** Under the stated local race prerequisites, the tool can read outside the manifest directory and disclose a file digest plus quote-match bits. No file contents are printed. Static path traversal or symlink escapes without a race are contained by the current `resolve` + `commonpath` check.

**Smallest remediation:** Bind the read to the checked directory/file object instead of re-opening a resolved string path: open beneath a pinned base directory with component-wise no-follow semantics, reject non-regular files, and read only from that validated descriptor. Keep the current failure-closed containment behavior.

## External-command review — no manifest-to-command execution found

The only `subprocess.run` is in `selftest` (`:188-197`): it launches `sys.executable` with the already-resolved `__file__` and fixed CLI arguments as an argv list, uses a temporary working directory, captures output, and does not enable a shell. Manifest-controlled values are not used as an executable or shell command. The normal `recheck` path (`:137-159`) uses Python file reads, SHA-256, and quote checks; no network or source-triggered command execution is present in the reviewed code. This is a static code review, not a run of the child process.

**Falsifiable check:** The conditional finding is disproved if the source read is changed to an open-handle operation whose identity/containment is validated before bytes are consumed; static `../` and pre-existing symlink escapes are already rejected by lines 101-105. The command-execution conclusion changes if manifest fields become executable input or any subprocess shell/executable is derived from caller-controlled data.
