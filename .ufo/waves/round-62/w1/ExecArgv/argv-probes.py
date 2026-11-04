#!/usr/bin/env python3
"""Bounded argv comparisons; all fixture writes stay under an explicit scratch root."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    base, candidate, scratch = map(Path, sys.argv[1:])
    with tempfile.TemporaryDirectory(prefix="argv-probes-", dir=scratch) as temporary:
        root = Path(temporary)
        (root / "corpus/instruments").mkdir(parents=True)
        (root / "corpus/instruments2").mkdir()
        (root / "g.txt").write_text("35\n")
        (root / "corpus/instruments/ok.py").write_text("print(35)\n")
        writer = "from pathlib import Path\nPath('marker').write_text('executed')\nprint(35)\n"
        (root / "out.py").write_text(writer)
        (root / "corpus/instruments2/ok.py").write_text(writer)
        (root / "corpus/instruments/write.py").write_text(writer)
        environment = os.environ.copy()
        environment.update(AUDIT_ESCAPE="../..", TMPDIR=str(scratch), HYAKU_SCRATCH=str(scratch))
        probes = [
            ("quoted-traversal", 'python3 corpus/instruments/"../../out.py"'),
            ("dot-prefix", "python3 ./corpus/instruments/ok.py"),
            ("sibling-boundary", "python3 corpus/instruments/../instruments2/ok.py"),
            ("dollar-expansion", "python3 corpus/instruments/$AUDIT_ESCAPE/out.py"),
            ("quoted-sort-flag", "sort '-o' marker g.txt && cat g.txt"),
            ("escaped-sort-flag", r"sort -\o marker g.txt && cat g.txt"),
            ("quoted-separator", "cat g.txt | grep -e '35' -e ';'"),
            ("quoted-regex-dollar", "grep -E '^35$' g.txt"),
            ("quoted-inside-script", "python3 'corpus/instruments/ok.py'"),
            ("and-shortcircuit-marker", "cat missing.txt && python3 corpus/instruments/write.py"),
        ]
        for label, instrument in (("baseline", base), ("candidate", candidate)):
            print(label, "sha256=" + hashlib.sha256(instrument.read_bytes()).hexdigest())
            for name, derive in probes:
                marker = root / "marker"
                marker.unlink(missing_ok=True)
                ledger = root / "ledger.json"
                ledger.write_text(json.dumps({"figures": [{"id": name, "record": "fixture", "recorded": "35", "derive": derive, "want": "35"}]}))
                command = [sys.executable, str(instrument), "--ledger", str(ledger), "--root", str(root)]
                result = subprocess.run(command, capture_output=True, text=True, env=environment, timeout=30)
                print(json.dumps({"instrument": label, "case": name, "derive": derive, "exit": result.returncode, "marker": marker.exists(), "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
