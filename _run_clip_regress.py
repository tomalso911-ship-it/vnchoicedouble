# -*- coding: utf-8 -*-
"""串行跑剪贴板/撤销回归探针，结果统一写 _regress_out.txt（避免控制台管道丢失）。"""
import subprocess
import sys
import time

PROBES = ["_pw_clip43.py", "_pw_undo51.py", "_pw_excel59.py"]
OUT = "_regress_out.txt"


def main():
    lines = []
    for p in PROBES:
        lines.append("=" * 70)
        lines.append("[RUN] %s" % p)
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, p], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=300)
            lines.append("[exit] %s   %.1fs" % (r.returncode, time.time() - t0))
            lines.append(r.stdout or "")
            if r.stderr:
                lines.append("[stderr]\n" + r.stderr)
        except Exception as e:
            lines.append("[exception] %r" % (e,))
        with open(OUT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    lines.append("=" * 70)
    lines.append("[DONE]")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
