# -*- coding: utf-8 -*-
# 每日同步 dist/vendor 的预压缩 .gz：仅当源文件比 .gz 新时才重建
# （nginx 开了 gzip_static，防止以后升级第三方库后仍发送旧的 .gz）
import os, glob, gzip, shutil
V = "/home/ubuntu/node-backend/dist/vendor"
changed = 0
for f in glob.glob(V + "/*"):
    if f.endswith(".gz") or not os.path.isfile(f):
        continue
    gz = f + ".gz"
    if os.path.exists(gz) and os.path.getmtime(gz) >= os.path.getmtime(f):
        continue
    try:
        if os.path.exists(gz):
            os.remove(gz)
        with open(f, "rb") as src, gzip.open(gz, "wb", compresslevel=9) as dst:
            shutil.copyfileobj(src, dst)
        changed += 1
        print("REGEN", os.path.basename(f))
    except Exception as e:
        print("SKIP", os.path.basename(f), str(e)[:80])
print("DONE changed=%d" % changed)
