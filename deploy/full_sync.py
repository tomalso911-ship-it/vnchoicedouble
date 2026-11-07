#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHOICE /lite 全量部署（唯一入口）

    本地 C:\\vnchoicedouble  ->  https://choice-vn-crm.duckdns.org/lite (/opt/choice-pm)
                            ->  GitHub origin/main

约定：所有代码/配置改动只在本地 C:\\vnchoicedouble 进行；服务器只接收文件，
      绝不直接在服务器上改代码。服务端数据（数据库/上传/财务缓存/汇率历史）
      永不从本地覆盖，以服务器 + backups/auto 为准。

用法：
    python deploy/full_sync.py                    # 全量同步 + 提交推送 GitHub
    python deploy/full_sync.py -m "提交说明"      # 自定义提交信息
    python deploy/full_sync.py --no-git          # 只同步线上，不提交 GitHub
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import tarfile
import time
from pathlib import Path

# Windows 控制台默认 cp1252，中文日志会触发 UnicodeEncodeError；统一切到 UTF-8
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deploy" / ".out"
OUT.mkdir(parents=True, exist_ok=True)

KEY = "C:/Users/tomal/.ssh/agi_pm_deploy"
HOST = "ubuntu@choice-vn-crm.duckdns.org"
RDIR = "/opt/choice-pm"

# 服务端数据 / 运行时产物：绝不从本地覆盖
SKIP_DIRS = {
    ".git", ".venv", "__pycache__", "uploads", "backups", "logs",
    "finance_data", "android-app", "_chrome_tmp", "training_shots",
    "generated-images", "_tmp_bak_probe", "_tmpdwg", "_jschk_head",
    ".codebuddy",
}
SKIP_FILES = {
    "agi_pm.db", "vendor/fx_history.js", "price_snapshot.json",
    "fin_trans_cache.json", "fin_sheet_titles.json",
}
SKIP_SUFFIX = (
    ".db", ".db-journal", ".db-wal", ".db-shm", ".log", ".pyc",
    ".apk", ".xlsx", ".xls", ".zip", ".7z",
)

# 运行必需的核心文件（即使未被 git 跟踪也必须同步）
CORE = [
    "app.py", "choice_lite.html", "choice_lite.min.html",
    "build_lite_min.py", "requirements.txt",
]
# 提交到 GitHub 的明确路径（不含运行时数据、日志、临时探针）
GIT_ADD = ["app.py", "choice_lite.html", "requirements.txt", "deploy", ".gitignore"]


def log(*args):
    print("[sync]", *args, flush=True)


def run(argv, check=True, timeout=300):
    return subprocess.run(
        argv, cwd=str(ROOT), capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=check, timeout=timeout,
    )


def ssh(cmd, timeout=300):
    return run(
        ["ssh", "-i", KEY, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", HOST, cmd],
        check=False, timeout=timeout,
    )


def scp(local, remote):
    r = run(["scp", "-i", KEY, "-o", "BatchMode=yes", str(local), f"{HOST}:{remote}"])
    return r


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_files():
    r = run(["git", "-c", "core.quotepath=false", "ls-files", "-z"])
    return [x.replace("\\", "/") for x in r.stdout.split("\0") if x]


def build_list():
    files = set()
    for rel in tracked_files():
        if not rel.isascii():          # 中文名截图等，tar/md5sum -c 易踩编码坑，运行不需要
            continue
        if rel.split("/")[0] in SKIP_DIRS or rel in SKIP_FILES:
            continue
        if rel.endswith(SKIP_SUFFIX):
            continue
        if not (ROOT / rel).is_file():
            continue
        files.add(rel)
    for name in CORE:
        if (ROOT / name).is_file():
            files.add(name)
    for p in (ROOT / "deploy").iterdir():   # 尚未 git add 的新部署配置也要同步
        if p.is_file():
            files.add(f"deploy/{p.name}")
    return sorted(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--message", default="")
    ap.add_argument("--no-git", action="store_true")
    args = ap.parse_args()

    log("1/6 本地准备：重建 min + app.py 语法检查")
    r = run([sys.executable, "build_lite_min.py"])
    log("   ", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "ok")
    run([sys.executable, "-m", "py_compile", "app.py"])

    files = build_list()
    if not all((ROOT / c).is_file() for c in CORE):
        raise SystemExit("核心文件缺失，已中止")
    log(f"    部署清单 {len(files)} 个文件")

    if not args.no_git:
        log("2/6 提交并推送 GitHub（pre-commit 硬锁会在此运行）")
        run(["git", "add", "--"] + GIT_ADD)
        staged = run(["git", "diff", "--cached", "--quiet"], check=False)
        if staged.returncode != 0:
            msg = args.message or (
                f"FULL-SYNC-{time.strftime('%Y%m%d')} 本地→线上→GitHub 全量同步"
            )
            c = run(["git", "commit", "-m", msg], check=False, timeout=900)
            if c.returncode != 0:
                log("commit 失败：\n" + (c.stdout or "") + (c.stderr or ""))
                raise SystemExit("提交被拦截，未改动线上")
            log("   ", (c.stdout or "").strip().splitlines()[0])
        else:
            log("    无新改动，跳过 commit")
        p = run(["git", "push", "origin", "main"], check=False, timeout=600)
        if p.returncode != 0:
            log("push 失败：\n" + (p.stdout or "") + (p.stderr or ""))
            raise SystemExit("GitHub 推送失败，未改动线上")
        log("   ", (p.stderr or p.stdout or "").strip().splitlines()[-1])

    log("3/6 打包 + 生成 md5 清单")
    tgz, man, paths = OUT / "choice_full.tgz", OUT / "manifest.txt", OUT / "paths.txt"
    with man.open("w", encoding="utf-8", newline="\n") as f:
        for rel in files:
            f.write(f"{md5(ROOT / rel)}  {rel}\n")
    paths.write_text("\n".join(files) + "\n", encoding="utf-8", newline="\n")
    with tarfile.open(tgz, "w:gz", compresslevel=6) as t:
        for rel in files:
            t.add(str(ROOT / rel), arcname=rel, recursive=False)
    log(f"    tar {tgz.stat().st_size / 1048576:.1f} MB / md5 {len(files)} 条")

    log("4/6 上传 + 服务器先备份将被覆盖的文件")
    scp(tgz, "/tmp/choice_full.tgz")
    scp(man, "/tmp/choice_manifest.txt")
    scp(paths, "/tmp/choice_paths.txt")
    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = f"{RDIR}/backups/sync_{ts}.tgz"
    b = ssh(
        f"mkdir -p {RDIR}/backups && cd {RDIR} && "
        f"tar -czf {bak} --ignore-failed-read -T /tmp/choice_paths.txt 2>/dev/null; "
        f"echo BACKUP_RC=$?; ls -lh {bak} 2>/dev/null; "
        f"sudo -n nginx -t >/dev/null 2>&1 && echo NGINX_OK || echo NGINX_FAIL"
    )
    log("   ", (b.stdout or "").strip().replace("\n", " | ")[:500])

    log("5/6 全量覆盖 + md5 逐文件校验")
    v = ssh(
        f"cd {RDIR} && tar -xzf /tmp/choice_full.tgz && "
        f"md5sum -c /tmp/choice_manifest.txt > /tmp/choice_verify.txt 2>&1; "
        f"echo VERIFY_OK=$(grep -c ': OK$' /tmp/choice_verify.txt) "
        f"VERIFY_BAD=$(grep -vc ': OK$' /tmp/choice_verify.txt); "
        f"grep -v ': OK$' /tmp/choice_verify.txt | head -15"
    )
    out = (v.stdout or "").strip()
    log("   ", out[:1200])
    if f"VERIFY_BAD=0" not in out:
        raise SystemExit("线上文件校验未全通过，请用上面的备份回滚后检查")

    log("6/6 重启服务 + 健康检查 + 三方一致性")
    h = ssh(
        "sudo -n systemctl restart choice-pm; sleep 4; "
        "echo SERVICE=$(systemctl is-active choice-pm); "
        "curl -sSL -o /dev/null -w 'HTTP=%{http_code}\\n' "
        "-H 'Accept-Encoding: br, gzip' http://127.0.0.1:5060/lite; "
        "curl -sSL -D - -o /dev/null -H 'Accept-Encoding: br, gzip' "
        "http://127.0.0.1:5060/lite | grep -i '^content-encoding' | tail -1; "
        f"cd {RDIR} && md5sum app.py choice_lite.html choice_lite.min.html; "
        "echo GIT_HEAD=$(git -C /opt/choice-pm rev-parse --short HEAD)"
    )
    health = (h.stdout or "").strip()
    log("   ", health.replace("\n", " | ")[:900])
    local = {c: md5(ROOT / c) for c in ("app.py", "choice_lite.html", "choice_lite.min.html")}
    for name, digest in local.items():
        if digest not in health:
            raise SystemExit(f"线上 {name} 与本地不一致（本地 {digest}）")
    if "SERVICE=active" not in health:
        raise SystemExit("choice-pm 未处于 active")

    heads = run(["git", "rev-parse", "--short", "HEAD", "origin/main"])
    log("完成：本地/线上/GitHub 核心文件一致；HEAD/origin =",
        " / ".join(heads.stdout.split()))
    log("页面：https://choice-vn-crm.duckdns.org/lite")


if __name__ == "__main__":
    main()
