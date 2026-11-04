import signal, sys
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
out = sys.stdout.buffer
out.write(b"FIRST-LINE bigwriter\n")
out.flush()
chunk = b"x" * 63 + b"\n"
for _ in range(40000):
    out.write(chunk)
    out.flush()
